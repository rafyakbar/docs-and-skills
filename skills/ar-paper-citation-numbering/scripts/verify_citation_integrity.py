#!/usr/bin/env python3
"""
scripts/verify_citation_integrity.py

Auditor Integritas Sitasi Naskah Bab & Daftar Pustaka (In-Text Citation Integrity Auditor).
Step 4 dalam alur publikasi naskah akademik.

Fungsi Pemeriksaan:
1. Validasi Tautan Jangkar: Memastikan setiap [[N]](06_references.md#refN) terhubung ke <a id="refN"></a>.
2. Aturan Zero-Orphan (Dua Arah):
   - Tidak ada sitasi dalam bab yang tidak memiliki entri di 06_references.md.
   - Tidak ada entri di 06_references.md yang tidak pernah disitir di seluruh naskah bab (Zero-Orphan Reference).
3. Urutan Kemunculan Pertama (IEEE Monotonic Order of First Appearance):
   - Referensi baru harus muncul secara berurutan [1], [2], [3], ... tanpa melompat.
4. Kepatuhan Tanda Baca & Sitasi Naratif:
   - Memastikan sitasi diletakkan sebelum tanda baca terminal (. , ;), bukan setelah tanda baca.
   - Pengecualian bebas false-positive untuk singkatan sah sitasi naratif (et al., i.e., e.g.).
5. Proteksi Blok Kode Berpagar (Fenced Code Blocks):
   - Menghiraukan isi blok kode Markdown (``` / ~~~) agar tidak menimbulkan deteksi palsu.
6. Penyaringan Bab Kanonikal:
   - Hanya mengaudit bab resmi (01_ s.d. 05_ serta 07_biographies), mengabaikan berkas review (07_editorial_decision, 08_revision_roadmap).
7. Luaran Terstruktur: Mendukung format konsol manusiawi dan JSON (--json).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# Reconfigure standard output for Windows UTF-8 console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

RE_CITATION_LINK = re.compile(r"\[\[(\d+)\]\]\((?:06_references\.md)?#ref(\d+)\)")
RE_ANCHOR_DEF = re.compile(r'<a\s+id=["\']ref(\d+)["\']>\s*</a>\s*\[(\d+)\]', re.IGNORECASE)
RE_PUNCT_AFTER_PERIOD = re.compile(r"(?<!\bet al)(?<!\bi\.e)(?<!\be\.g)\.\s*\[\[\d+\]\]", re.IGNORECASE)
RE_PUNCT_AFTER_COMMA = re.compile(r"(?<!\))(?<!\])\s*,\s*\[\[\d+\]\]")
RE_FENCE_START = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def get_canonical_file_order(draft_dir: Path) -> List[Path]:
    """
    Mengembalikan daftar berkas bab markdown dalam urutan baca naskah IEEE kanonikal.
    Hanya menyertakan bab naskah resmi (01_ s.d. 05_ serta 07_biographies)
    dan mengabaikan berkas non-bab/review seperti 00_abstract, 06_references, 07_editorial_decision,
    08_revision_roadmap, serta ref_part_*.
    """
    if not draft_dir.exists():
        return []

    all_files = list(draft_dir.glob("*.md"))
    content_files = []

    for f in all_files:
        name = f.name.lower()
        # Saring keluar berkas non-bab dan artefak review/pipeline
        if (
            name.startswith("00_")
            or name.startswith("06_")
            or name.startswith("08_")
            or name.startswith("09_")
            or name.startswith("ref_part")
            or "editorial_decision" in name
            or "revision_roadmap" in name
        ):
            continue

        # Hanya sertakan bab naskah resmi 01_ s.d. 05_ serta 07_biographies
        if any(name.startswith(p) for p in ("01_", "02_", "03_", "04_", "05_")):
            content_files.append(f)
        elif name.startswith("07_") and "biograph" in name:
            content_files.append(f)

    # Urutkan secara alfabetis kanonikal (01_..., 02_..., 03_..., 04_..., 05_...)
    return sorted(content_files, key=lambda p: p.name)


def parse_reference_anchors(refs_md_path: Path) -> Dict[int, int]:
    """
    Ekstrak seluruh definisi jangkar pada 06_references.md:
    Returns: { bracket_num: anchor_number }
    """
    if not refs_md_path.exists():
        return {}

    content = refs_md_path.read_text(encoding="utf-8")
    anchors: Dict[int, int] = {}

    for match in RE_ANCHOR_DEF.finditer(content):
        anchor_id = int(match.group(1))
        bracket_num = int(match.group(2))
        anchors[bracket_num] = anchor_id

    return anchors


def audit_citations(
    draft_dir: Path,
    refs_md_path: Path,
) -> Dict[str, Any]:
    """Melakukan audit menyeluruh terhadap seluruh sitasi di naskah bab."""
    anchors = parse_reference_anchors(refs_md_path)
    defined_ref_nums = set(anchors.keys())

    canonical_files = get_canonical_file_order(draft_dir)

    all_citations_found: List[Tuple[Path, int, int]] = []  # (file, line_no, ref_num)
    cited_ref_nums: Set[int] = set()
    first_appearance_order: List[int] = []

    mismatched_anchors: List[Dict[str, Any]] = []
    orphan_in_text: List[Dict[str, Any]] = []
    punctuation_faults: List[Dict[str, Any]] = []

    for fpath in canonical_files:
        lines = fpath.read_text(encoding="utf-8").splitlines()
        in_code_block = False
        fence_char = ""
        fence_len = 0

        for line_no, line in enumerate(lines, start=1):
            # Proteksi fenced code block: deteksi pembuka dan penutup blok kode
            m_fence = RE_FENCE_START.match(line)
            if m_fence:
                fence = m_fence.group(1)
                char = fence[0]
                length = len(fence)
                if not in_code_block:
                    in_code_block = True
                    fence_char = char
                    fence_len = length
                    continue
                else:
                    if char == fence_char and length >= fence_len:
                        in_code_block = False
                        fence_char = ""
                        fence_len = 0
                        continue

            # Abaikan seluruh baris yang berada di dalam blok kode
            if in_code_block:
                continue

            # Cek penempatan salah (setelah titik/koma selain singkatan sah)
            if RE_PUNCT_AFTER_PERIOD.search(line) or RE_PUNCT_AFTER_COMMA.search(line):
                punctuation_faults.append({
                    "file": str(fpath.name),
                    "line": line_no,
                    "text": line.strip()[:100],
                })

            # Ekstrak seluruh sitasi braket
            for m in RE_CITATION_LINK.finditer(line):
                bracket_num = int(m.group(1))
                anchor_num = int(m.group(2))

                all_citations_found.append((fpath, line_no, bracket_num))

                if bracket_num != anchor_num:
                    mismatched_anchors.append({
                        "file": str(fpath.name),
                        "line": line_no,
                        "bracket": bracket_num,
                        "anchor": anchor_num,
                    })

                if bracket_num not in defined_ref_nums:
                    orphan_in_text.append({
                        "file": str(fpath.name),
                        "line": line_no,
                        "ref_num": bracket_num,
                    })

                if bracket_num not in cited_ref_nums:
                    cited_ref_nums.add(bracket_num)
                    first_appearance_order.append(bracket_num)

    # Cek urutan kemunculan pertama IEEE (harus 1, 2, 3, 4, ... berurutan tanpa lompat)
    expected_seq = list(range(1, len(first_appearance_order) + 1))
    order_violations: List[Dict[str, Any]] = []
    for idx, (actual, expected) in enumerate(zip(first_appearance_order, expected_seq)):
        if actual != expected:
            order_violations.append({
                "step": idx + 1,
                "expected_new_ref": expected,
                "actual_ref": actual,
            })

    # Cek orphan references (ada di 06_references.md tapi tidak pernah disitir)
    orphan_references = sorted(list(defined_ref_nums - cited_ref_nums))

    # Ringkasan status
    is_clean = (
        len(mismatched_anchors) == 0
        and len(orphan_in_text) == 0
        and len(orphan_references) == 0
        and len(order_violations) == 0
        and len(punctuation_faults) == 0
    )

    return {
        "status": "PASS" if is_clean else "FAIL",
        "total_files_audited": len(canonical_files),
        "total_citations_found": len(all_citations_found),
        "unique_references_cited": len(cited_ref_nums),
        "total_references_defined": len(defined_ref_nums),
        "mismatched_anchors": mismatched_anchors,
        "orphan_in_text_citations": orphan_in_text,
        "orphan_references": orphan_references,
        "first_appearance_violations": order_violations,
        "punctuation_faults": punctuation_faults,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit integritas sitasi braket interaktif pada bab naskah terhadap 06_references.md."
    )
    parser.add_argument(
        "-d",
        "--draft-dir",
        type=Path,
        default=Path("paper"),
        help="Direktori naskah bab draf (default: paper)",
    )
    parser.add_argument(
        "-r",
        "--references",
        type=Path,
        default=Path("paper/06_references.md"),
        help="Path ke berkas naskah 06_references.md (default: paper/06_references.md)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Cetak hasil laporan dalam format JSON",
    )

    args = parser.parse_args()

    if not args.references.exists():
        print(f"[ERROR] Berkas referensi '{args.references}' tidak ditemukan!", file=sys.stderr)
        return 1

    report = audit_citations(args.draft_dir, args.references)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["status"] == "PASS" else 1

    print("=== LAPORAN AUDIT INTEGRITAS SITASI TEKS (Step 4) ===")
    print(f"Status Audit             : {report['status']}")
    print(f"Berkas Bab Diaudit       : {report['total_files_audited']}")
    print(f"Total Tautan Sitasi Teks : {report['total_citations_found']}")
    print(f"Rujukan Unik Disitir     : {report['unique_references_cited']}")
    print(f"Entri di 06_references.md: {report['total_references_defined']}")
    print("-------------------------------------------------------------")

    if report["status"] == "PASS":
        print("[OK] Kepatuhan Sempurna: Zero orphans, urutan IEEE taat asas, tautan anchor valid.")
        return 0

    if report["orphan_in_text_citations"]:
        print(f"\n[!] Sitasi Yatim di Teks (Tidak terdaftar di daftar pustaka): {len(report['orphan_in_text_citations'])}")
        for item in report["orphan_in_text_citations"][:5]:
            print(f"    - {item['file']}:{item['line']} -> [{item['ref_num']}]")

    if report["orphan_references"]:
        print(f"\n[!] Referensi Yatim (Ada di daftar pustaka tapi tidak disitir): {len(report['orphan_references'])}")
        print(f"    - Nomor entri: {report['orphan_references']}")

    if report["first_appearance_violations"]:
        print(f"\n[!] Pelanggaran Urutan Kemunculan Pertama IEEE: {len(report['first_appearance_violations'])}")
        for item in report["first_appearance_violations"][:5]:
            print(f"    - Langkah {item['step']}: diharapkan baru [{item['expected_new_ref']}], ditemukan [{item['actual_ref']}]")

    if report["mismatched_anchors"]:
        print(f"\n[!] Ketidakcocokan Nomor Braket vs Anchor ID: {len(report['mismatched_anchors'])}")
        for item in report["mismatched_anchors"][:5]:
            print(f"    - {item['file']}:{item['line']} -> [{item['bracket']}] vs ref{item['anchor']}")

    if report["punctuation_faults"]:
        print(f"\n[!] Penempatan Sitasi Setelah Tanda Baca: {len(report['punctuation_faults'])}")
        for item in report["punctuation_faults"][:5]:
            print(f"    - {item['file']}:{item['line']} -> {item['text']}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
