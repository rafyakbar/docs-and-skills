#!/usr/bin/env python3
"""
scripts/ars_citation_numberer.py

Mesin Deterministik Penomoran & Penautan Sitasi Teks Markdown (In-Text Citation Numberer).
Step 4 dalam alur publikasi naskah akademik.

Fungsi:
- Membaca urutan kemunculan dari paper/references.txt dan mencocokkan dengan paper/06_references.md.
- Mencocokkan kalimat klaim dalam draf bab naskah (Exact Match -> Normalized Match -> Fuzzy SequenceMatcher).
- Menyuntikkan sitasi braket interaktif ber-anchor: [[N]](06_references.md#refN).
- Menjamin penempatan tanda baca presisi: sebelum tanda titik (.), koma (,), titik koma (;), atau pembatas sel tabel (|).
- Menjamin sifat idempoten (anti duplikasi dan aman dari double injection).
- Menyediakan opsi --dry-run, --strip (pembersihan sitasi), dan penulisan atomik (Atomic Write).
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import string
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Reconfigure standard output for Windows UTF-8 console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Regex untuk mendeteksi atau membersihkan sitasi interaktif
RE_BRACKET_LINK = re.compile(r"\[\[(\d+)\]\]\(06_references\.md#ref\d+\)")
RE_MULTI_BRACKET_CLUSTER = re.compile(
    r"\s*\[\[\d+\]\]\(06_references\.md#ref\d+\)(?:\s*,\s*\[\[\d+\]\]\(06_references\.md#ref\d+\))*"
)
RE_CLEAN_PUNCT = str.maketrans("", "", string.punctuation)


def normalize_sentence(text: str) -> str:
    """Normalisasi kalimat untuk pencocokan toleran spasi dan kutip."""
    cleaned = (
        text.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("–", "-")
        .replace("—", "-")
    )
    cleaned = cleaned.translate(RE_CLEAN_PUNCT).lower()
    return " ".join(cleaned.split())


def atomic_write_text(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    """Menulis berkas teks secara atomik untuk mencegah korupsi file jika crash."""
    dir_name = file_path.parent
    dir_name.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding=encoding) as tf:
        tf.write(content)
        temp_name = tf.name
    os.replace(temp_name, file_path)


def extract_reference_index_from_md(compiled_refs_path: Path) -> Dict[str, int]:
    """
    Ekstrak mapping dari 06_references.md:
    Contoh: <a id="ref1"></a>\n[1] ... -> id 1
    """
    if not compiled_refs_path.exists():
        return {}

    content = compiled_refs_path.read_text(encoding="utf-8")
    ref_map: Dict[str, int] = {}
    
    # Ambil setiap anchor dan nomor
    pattern = re.compile(r'<a\s+id=["\']ref(\d+)["\']>\s*</a>\s*\n\s*\[(\d+)\]', re.IGNORECASE)
    for match in pattern.finditer(content):
        anchor_num = int(match.group(1))
        bracket_num = int(match.group(2))
        if anchor_num == bracket_num:
            ref_map[f"ref{anchor_num}"] = anchor_num

    return ref_map


def parse_references_txt(
    refs_txt_path: Path,
) -> Tuple[Dict[str, List[Tuple[str, List[str]]]], List[str]]:
    """
    Parse paper/references.txt:
    Menghasilkan:
      - claims_by_file: { 'paper/01_introduction.md': [ (claim_sentence, [ref_files]) ] }
      - appearance_order: [ ref_file_1, ref_file_2, ... ] (Order of First Appearance)
    """
    if not refs_txt_path.exists():
        raise FileNotFoundError(f"Berkas mapping tidak ditemukan: {refs_txt_path}")

    claims_by_file: Dict[str, List[Tuple[str, List[str]]]] = {}
    appearance_order: List[str] = []
    seen_refs: Set[str] = set()

    current_file = ""
    current_claim = ""
    current_refs: List[str] = []

    lines = refs_txt_path.read_text(encoding="utf-8").splitlines()

    for line in lines:
        raw_line = line.strip()
        if not raw_line:
            continue

        # Deteksi baris header seksi/file: "paper/01_introduction.md: paragraf 1:"
        if raw_line.startswith("paper/") and ":" in raw_line and not raw_line.startswith("paper/references/"):
            # Simpan klaim sebelumnya
            if current_claim and current_file:
                claims_by_file.setdefault(current_file, []).append((current_claim, current_refs))
                current_claim = ""
                current_refs = []

            # Format: paper/nama-file.md: paragraf X:
            header_parts = raw_line.split(":")
            current_file = header_parts[0].strip()
            claims_by_file.setdefault(current_file, [])
            continue

        # Deteksi baris klaim: - "Teks klaim...":
        if raw_line.startswith('- "') or raw_line.startswith("- '") or (raw_line.startswith("- ") and ":" in raw_line and not "paper/references" in raw_line):
            if current_claim and current_file:
                claims_by_file.setdefault(current_file, []).append((current_claim, current_refs))
                current_refs = []

            match = re.search(r'^-\s*["\'](.*?)["\']\s*:', raw_line)
            if match:
                current_claim = match.group(1).strip()
            else:
                current_claim = raw_line.lstrip("-").strip().strip('"').strip("'").rstrip(":")
            continue

        # Deteksi baris berkas rujukan: - paper/references/2021_...
        if "paper/references/" in raw_line:
            ref_path = raw_line.lstrip("-").strip()
            # Normalisasi path separators
            ref_path = ref_path.replace("\\", "/")
            current_refs.append(ref_path)
            if ref_path not in seen_refs:
                seen_refs.add(ref_path)
                appearance_order.append(ref_path)

    # Simpan klaim terakhir
    if current_claim and current_file:
        claims_by_file.setdefault(current_file, []).append((current_claim, current_refs))

    return claims_by_file, appearance_order


def build_ref_mapping(appearance_order: List[str]) -> Dict[str, int]:
    """Menghasilkan pemetaan path rujukan fisik -> integer N (1-based index)."""
    return {ref: idx + 1 for idx, ref in enumerate(appearance_order)}


def format_citation_brackets(ref_numbers: List[int]) -> str:
    """
    Format nomor referensi menjadi Markdown links berurutan menaik:
    Contoh: [[1]](06_references.md#ref1), [[2]](06_references.md#ref2)
    """
    unique_sorted = sorted(list(set(ref_numbers)))
    return ", ".join([f"[[{num}]](06_references.md#ref{num})" for num in unique_sorted])


def strip_citations_from_text(text: str) -> str:
    """Menghapus seluruh sitasi interaktif [[N]](06_references.md#refN) dari teks."""
    return RE_MULTI_BRACKET_CLUSTER.sub("", text)


def inject_citations_into_paragraph(
    paragraph: str,
    claims: List[Tuple[str, List[str]]],
    ref_map: Dict[str, int],
    fuzzy_threshold: float = 0.85,
) -> Tuple[str, int]:
    """
    Menyisipkan sitasi ke dalam paragraf dengan pencocokan kalimat dan penempatan tanda baca teliti.
    Returns: (paragraf_hasil, jumlah_injeksi)
    """
    updated_p = paragraph
    injected_count = 0

    for claim_text, ref_paths in claims:
        # Resolusi nomor referensi
        ref_nums = [ref_map[p] for p in ref_paths if p in ref_map]
        if not ref_nums:
            continue

        brackets = format_citation_brackets(ref_nums)

        # -------------------------------------------------------------
        # 1. Exact Substring Matching
        # -------------------------------------------------------------
        if claim_text in updated_p:
            match_idx = updated_p.find(claim_text)
            claim_end = match_idx + len(claim_text)

            # Cek teks setelah klaim
            remainder = updated_p[claim_end:]

            # Cek apakah sudah terinjeksi sitasi yang sesuai
            existing_match = re.match(
                r"^(\s*\[\[\d+\]\]\(06_references\.md#ref\d+\)(?:,\s*\[\[\d+\]\]\(06_references\.md#ref\d+\))*)",
                remainder,
            )
            if existing_match:
                existing_cluster = existing_match.group(1).strip()
                if existing_cluster == brackets:
                    # Sudah terpasang dengan tepat (idempoten)
                    continue
                else:
                    # Gantikan dengan sitasi baru
                    remainder_after = remainder[existing_match.end() :]
                    updated_p = updated_p[:claim_end] + f" {brackets}" + remainder_after
                    injected_count += 1
                    continue

            # Tangani tanda baca terminal (. , ; :)
            punct_match = re.match(r"^(\s*)([\.,;:|])", remainder)
            if punct_match:
                punct = punct_match.group(2)
                remainder_after = remainder[punct_match.end() :]
                updated_p = updated_p[:claim_end] + f" {brackets}{punct}" + remainder_after
            else:
                updated_p = updated_p[:claim_end] + f" {brackets}" + remainder
            injected_count += 1
            continue

        # -------------------------------------------------------------
        # 2. Normalized & Fuzzy Sentence Matching
        # -------------------------------------------------------------
        norm_claim = normalize_sentence(claim_text)
        sentences = re.split(r"(?<=[.?!])\s+", updated_p)
        matched_idx = -1
        best_ratio = 0.0

        for s_idx, sent in enumerate(sentences):
            # Bersihkan sitasi lama saat menghitung kemiripan
            clean_sent = strip_citations_from_text(sent)
            norm_sent = normalize_sentence(clean_sent)
            ratio = difflib.SequenceMatcher(None, norm_claim, norm_sent).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                if ratio >= fuzzy_threshold:
                    matched_idx = s_idx

        if matched_idx != -1 and best_ratio >= fuzzy_threshold:
            target_sent = sentences[matched_idx]
            clean_sent = strip_citations_from_text(target_sent).rstrip()

            # Tangani tanda baca terminal kalimat
            m_end = re.search(r"([\.,;:|])\s*$", clean_sent)
            if m_end:
                punct = m_end.group(1)
                core = clean_sent[: m_end.start()].rstrip()
                new_sent = f"{core} {brackets}{punct}"
            else:
                new_sent = f"{clean_sent} {brackets}"

            if new_sent != target_sent:
                sentences[matched_idx] = new_sent
                updated_p = " ".join(sentences)
                injected_count += 1

    return updated_p, injected_count


def process_markdown_file(
    md_path: Path,
    claims: List[Tuple[str, List[str]]],
    ref_map: Dict[str, int],
    dry_run: bool = False,
    strip_mode: bool = False,
) -> Tuple[int, bool]:
    """
    Memproses satu berkas bab Markdown draf.
    Returns (jumlah_injeksi, status_berubah).
    """
    if not md_path.exists():
        return 0, False

    original_text = md_path.read_text(encoding="utf-8")

    if strip_mode:
        cleaned_text = strip_citations_from_text(original_text)
        changed = cleaned_text != original_text
        if changed and not dry_run:
            atomic_write_text(md_path, cleaned_text)
        return 0, changed

    paragraphs = original_text.split("\n\n")
    total_injected = 0
    new_paragraphs = []

    for p in paragraphs:
        p_stripped = p.strip()
        # Lewati heading dan baris tabel murni (kecuali tabel komparasi metode)
        if not p_stripped or p_stripped.startswith("#"):
            new_paragraphs.append(p)
            continue

        updated_p, count = inject_citations_into_paragraph(p, claims, ref_map)
        new_paragraphs.append(updated_p)
        total_injected += count

    new_text = "\n\n".join(new_paragraphs)
    changed = new_text != original_text

    if changed and not dry_run:
        atomic_write_text(md_path, new_text)

    return total_injected, changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suntikkan nomor sitasi interaktif [[N]](06_references.md#refN) ke dalam draf naskah bab."
    )
    parser.add_argument(
        "-m",
        "--mapping",
        type=Path,
        default=Path("paper/references.txt"),
        help="Path ke berkas pemetaan references.txt (default: paper/references.txt)",
    )
    parser.add_argument(
        "-r",
        "--references",
        type=Path,
        default=Path("paper/06_references.md"),
        help="Path ke berkas naskah 06_references.md (default: paper/06_references.md)",
    )
    parser.add_argument(
        "-d",
        "--draft-dir",
        type=Path,
        default=Path("paper"),
        help="Direktori naskah bab draf (default: paper)",
    )
    parser.add_argument(
        "-s",
        "--section",
        type=Path,
        default=None,
        help="Proses hanya satu berkas seksi spesifik (misal: paper/01_introduction.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Tampilkan hasil penomoran di terminal tanpa mengubah berkas fisik di disk",
    )
    parser.add_argument(
        "--strip",
        action="store_true",
        help="Bersihkan seluruh nomor sitasi braket dari draf naskah untuk mengembalikan ke bentuk teks polos",
    )
    parser.add_argument(
        "--fuzzy-threshold",
        type=float,
        default=0.85,
        help="Ambang batas kemiripan difflib SequenceMatcher (default: 0.85)",
    )

    args = parser.parse_args()

    if not args.mapping.exists():
        print(f"[ERROR] Berkas pemetaan '{args.mapping}' tidak ditemukan!", file=sys.stderr)
        return 1

    print(f"=== Menjalankan ARS Citation Numberer ===")
    print(f"Mapping File  : {args.mapping}")
    print(f"Ref List File : {args.references}")
    print(f"Mode          : {'STRIP' if args.strip else ('DRY-RUN' if args.dry_run else 'INJECT')}")

    try:
        claims_by_file, appearance_order = parse_references_txt(args.mapping)
    except Exception as exc:
        print(f"[ERROR] Gagal mem-parse '{args.mapping}': {exc}", file=sys.stderr)
        return 1

    ref_map = build_ref_mapping(appearance_order)
    print(f"Total referensi unik terdaftar: {len(ref_map)} entri.")

    # Target berkas yang akan diproses
    if args.section:
        target_files = [args.section]
    else:
        # Kumpulkan berkas dari claims_by_file
        target_files = [Path(f) for f in claims_by_file.keys()]

    grand_injected = 0
    files_modified = 0

    for tf in target_files:
        norm_key = str(tf).replace("\\", "/")
        claims = claims_by_file.get(norm_key, [])
        if not claims:
            for k in claims_by_file:
                if norm_key.endswith(k) or k.endswith(tf.name):
                    claims = claims_by_file[k]
                    break

        if not claims and not args.strip:
            print(f"[-] {tf}: Tidak ada pemetaan klaim pada references.txt.")
            continue

        injected_count, changed = process_markdown_file(
            tf, claims, ref_map, dry_run=args.dry_run, strip_mode=args.strip
        )
        status_str = "BERUBAH" if changed else "TIDAK BERUBAH"
        if args.strip:
            print(f"[OK] {tf}: {status_str} (strip mode)")
        else:
            print(f"[OK] {tf}: {injected_count} klaim disuntikkan ({status_str})")

        grand_injected += injected_count
        if changed:
            files_modified += 1

    print("-------------------------------------------------------------")
    print(f"Ringkasan: {grand_injected} sitasi diproses di {files_modified} berkas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
