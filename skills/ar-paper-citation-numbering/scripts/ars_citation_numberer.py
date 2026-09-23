#!/usr/bin/env python3
"""
scripts/ars_citation_numberer.py

Mesin Deterministik Penomoran & Penautan Sitasi Teks Markdown (In-Text Citation Numberer).
Step 4 dalam alur publikasi naskah akademik.

Fungsi:
- Membaca urutan kemunculan dari paper/references.txt dan mencocokkan dengan paper/06_references.md.
- Normalisasi Windows path (konversi backslash ke forward slash) untuk kompatibilitas lintas platform.
- Perlindungan blok kode berpagar (fenced code blocks) agar tidak terkena injeksi sitasi.
- Validasi silang aktif dengan paper/06_references.md untuk memastikan integritas indeks referensi.
- Pemotongan tanda baca penutup klaim (rstrip) agar kurung siku sitasi IEEE selalu disuntikkan SEBELUM tanda baca terminal (. , ; : |).
- Mencocokkan kalimat klaim dalam draf bab naskah (Exact Match -> Normalized Match -> Fuzzy SequenceMatcher).
- Menyuntikkan sitasi braket interaktif ber-anchor: [[N]](06_references.md#refN).
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
RE_FENCE_START = re.compile(r"^ {0,3}(`{3,}|~{3,})")


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


def extract_reference_index_from_md(compiled_refs_path: Path) -> Dict[int, int]:
    """
    Ekstrak mapping nomor referensi dan jangkar dari 06_references.md:
    Contoh: <a id="ref1"></a>\n[1] ... -> { 1: 1 }
    Returns: { bracket_num: anchor_id_num }
    """
    if not compiled_refs_path.exists():
        return {}

    content = compiled_refs_path.read_text(encoding="utf-8")
    ref_map: Dict[int, int] = {}

    # Toleran terhadap format newline \n maupun \r\n serta spasi antar-tag
    pattern = re.compile(r'<a\s+id=["\']ref(\d+)["\']>\s*</a>\s*\[(\d+)\]', re.IGNORECASE)
    for match in pattern.finditer(content):
        anchor_num = int(match.group(1))
        bracket_num = int(match.group(2))
        ref_map[bracket_num] = anchor_num

    return ref_map


def extract_and_mask_code_blocks(text: str) -> Tuple[str, List[str]]:
    """
    Menemukan seluruh blok kode berpagar (fenced code blocks) dan menggantinya dengan placeholder unik
    agar terproteksi dari injeksi dan pembersihan sitasi.
    """
    code_blocks: List[str] = []
    lines = text.splitlines(keepends=True)
    new_lines: List[str] = []
    in_code = False
    fence_char = ""
    fence_len = 0
    current_block: List[str] = []

    for line in lines:
        m = RE_FENCE_START.match(line)
        if m:
            fence = m.group(1)
            char = fence[0]
            length = len(fence)
            if not in_code:
                in_code = True
                fence_char = char
                fence_len = length
                current_block = [line]
            else:
                if char == fence_char and length >= fence_len:
                    current_block.append(line)
                    idx = len(code_blocks)
                    code_blocks.append("".join(current_block))
                    new_lines.append(f"<<<CODE_BLOCK_{idx}>>>\n")
                    in_code = False
                    fence_char = ""
                    fence_len = 0
                    current_block = []
                else:
                    current_block.append(line)
        else:
            if in_code:
                current_block.append(line)
            else:
                new_lines.append(line)

    if in_code and current_block:
        idx = len(code_blocks)
        code_blocks.append("".join(current_block))
        new_lines.append(f"<<<CODE_BLOCK_{idx}>>>\n")

    return "".join(new_lines), code_blocks


def restore_code_blocks(text: str, code_blocks: List[str]) -> str:
    """Mengembalikan blok kode asli dari placeholder terproteksi."""
    restored = text
    for idx, block in enumerate(code_blocks):
        placeholder = f"<<<CODE_BLOCK_{idx}>>>\n"
        if placeholder in restored:
            restored = restored.replace(placeholder, block, 1)
        else:
            placeholder_no_nl = f"<<<CODE_BLOCK_{idx}>>>"
            restored = restored.replace(placeholder_no_nl, block.rstrip("\r\n"), 1)
    return restored


def parse_references_txt(
    refs_txt_path: Path,
) -> Tuple[Dict[str, List[Tuple[str, List[str]]]], List[str]]:
    """
    Parse paper/references.txt:
    Menghasilkan:
      - claims_by_file: { 'paper/01_introduction.md': [ (claim_sentence, [ref_files]) ] }
      - appearance_order: [ ref_file_1, ref_file_2, ... ] (Order of First Appearance)
    Mendukung normalisasi path Windows (backslash ke slash) dan pemotongan tanda baca akhir klaim.
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

        # Normalisasi path Windows (\ -> /) di awal loop agar pencocokan path 100% konsisten
        norm_line = raw_line.replace("\\", "/")

        # Deteksi baris header seksi/file: "paper/01_introduction.md: paragraf 1:"
        if norm_line.startswith("paper/") and ":" in norm_line and not norm_line.startswith("paper/references/"):
            # Simpan klaim sebelumnya
            if current_claim and current_file:
                claims_by_file.setdefault(current_file, []).append((current_claim, current_refs))
                current_claim = ""
                current_refs = []

            # Format: paper/nama-file.md: paragraf X:
            header_parts = norm_line.split(":")
            current_file = header_parts[0].strip()
            claims_by_file.setdefault(current_file, [])
            continue

        # Deteksi baris klaim: - "Teks klaim...":
        if (
            norm_line.startswith('- "')
            or norm_line.startswith("- '")
            or (norm_line.startswith("- ") and ":" in norm_line and "paper/references" not in norm_line)
        ):
            if current_claim and current_file:
                claims_by_file.setdefault(current_file, []).append((current_claim, current_refs))
                current_refs = []

            match = re.search(r'^-\s*["\'](.*?)["\']\s*:', raw_line)
            if match:
                current_claim = match.group(1).strip()
            else:
                current_claim = raw_line.lstrip("-").strip().strip('"').strip("'").rstrip(":")
            # Potong tanda baca akhir klaim agar tidak mengganggu penempatan sitasi sebelum tanda baca terminal
            current_claim = current_claim.rstrip(".,;:|").strip()
            continue

        # Deteksi baris berkas rujukan: - paper/references/2021_...
        if "paper/references/" in norm_line:
            ref_path = norm_line.lstrip("-").strip()
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
    Menjamin kurung siku selalu disuntikkan SEBELUM tanda baca terminal (. , ; : |).
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

        # Potong tanda baca akhir klaim agar pencocokan presisi dan sitasi diletakkan sebelum tanda baca
        claim_clean = claim_text.strip().rstrip(".,;:|").strip()
        if not claim_clean:
            continue

        # -------------------------------------------------------------
        # 1. Exact Substring Matching
        # -------------------------------------------------------------
        if claim_clean in updated_p:
            match_idx = updated_p.find(claim_clean)
            claim_end = match_idx + len(claim_clean)

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

            # Tangani tanda baca terminal (. , ; : |)
            punct_match = re.match(r"^(\s*)([\.,;:|])", remainder)
            if punct_match:
                punct = punct_match.group(2)
                remainder_after = remainder[punct_match.end() :]
                # Bersihkan sitasi keliru jika sebelumnya terpasang salah setelah tanda baca (e.g. kalimat. [[1]])
                legacy_match = re.match(
                    r"^\s*\[\[\d+\]\]\(06_references\.md#ref\d+\)(?:,\s*\[\[\d+\]\]\(06_references\.md#ref\d+\))*",
                    remainder_after,
                )
                if legacy_match:
                    remainder_after = remainder_after[legacy_match.end() :]

                # Untuk pembatas tabel (|), sisipkan spasi sebelum | agar format tabel tetap rapi
                space_prefix = " " if punct == "|" else ""
                updated_p = updated_p[:claim_end] + f" {brackets}{space_prefix}{punct}" + remainder_after
            else:
                updated_p = updated_p[:claim_end] + f" {brackets}" + remainder
            injected_count += 1
            continue

        # -------------------------------------------------------------
        # 2. Normalized & Fuzzy Sentence Matching
        # -------------------------------------------------------------
        norm_claim = normalize_sentence(claim_clean)
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
                space_prefix = " " if punct == "|" else ""
                new_sent = f"{core} {brackets}{space_prefix}{punct}"
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
    Memproses satu berkas bab Markdown draf dengan proteksi penuh terhadap fenced code blocks.
    Returns (jumlah_injeksi, status_berubah).
    """
    if not md_path.exists():
        return 0, False

    original_text = md_path.read_text(encoding="utf-8")

    # Proteksi blok kode Markdown (fenced code blocks ``` / ~~~) dengan masking
    masked_text, code_blocks = extract_and_mask_code_blocks(original_text)

    if strip_mode:
        cleaned_text = strip_citations_from_text(masked_text)
        restored_text = restore_code_blocks(cleaned_text, code_blocks)
        changed = restored_text != original_text
        if changed and not dry_run:
            atomic_write_text(md_path, restored_text)
        return 0, changed

    paragraphs = masked_text.split("\n\n")
    total_injected = 0
    new_paragraphs = []

    for p in paragraphs:
        p_stripped = p.strip()
        # Lewati heading, placeholder kode berpagar, dan baris kosong
        if not p_stripped or p_stripped.startswith("#") or p_stripped.startswith("<<<CODE_BLOCK_"):
            new_paragraphs.append(p)
            continue

        updated_p, count = inject_citations_into_paragraph(p, claims, ref_map)
        new_paragraphs.append(updated_p)
        total_injected += count

    new_masked_text = "\n\n".join(new_paragraphs)
    restored_text = restore_code_blocks(new_masked_text, code_blocks)
    changed = restored_text != original_text

    if changed and not dry_run:
        atomic_write_text(md_path, restored_text)

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

    print("=== Menjalankan ARS Citation Numberer ===")
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

    # Validasi Silang dengan 06_references.md jika argumen diberikan dan berkasnya ada
    if args.references and args.references.exists():
        md_anchors = extract_reference_index_from_md(args.references)
        defined_numbers = set(md_anchors.keys())
        allocated_numbers = set(ref_map.values())
        print(f"Validasi Silang: {len(defined_numbers)} entri jangkar terdefinisi di '{args.references}'.")

        mismatches = [b for b, a in md_anchors.items() if b != a]
        if mismatches:
            print(
                f"[PERINGATAN] Terdapat {len(mismatches)} ketidakcocokan [bracket] vs ref[anchor] di '{args.references}': {mismatches}",
                file=sys.stderr,
            )

        missing_in_md = allocated_numbers - defined_numbers
        if missing_in_md:
            print(
                f"[PERINGATAN] {len(missing_in_md)} nomor referensi dari references.txt belum terdefinisi di '{args.references}': {sorted(list(missing_in_md))}",
                file=sys.stderr,
            )
        else:
            print(f"[OK] Seluruh {len(allocated_numbers)} nomor referensi selaras dengan '{args.references}'.")
    elif args.references:
        print(f"[INFO] Berkas referensi '{args.references}' tidak ditemukan; validasi silang dilewati.")

    # Target berkas yang akan diproses
    if args.section:
        target_files = [args.section]
    else:
        discovered_files = {Path(f) for f in claims_by_file.keys()}
        # Jika dalam strip mode dan draft_dir ada, tambahkan seluruh bab kanonikal dari draft_dir
        if args.strip and args.draft_dir.exists():
            for f in args.draft_dir.glob("*.md"):
                name = f.name.lower()
                if any(name.startswith(p) for p in ("01_", "02_", "03_", "04_", "05_")) or (
                    name.startswith("07_") and "biograph" in name
                ):
                    discovered_files.add(f)
        target_files = sorted(list(discovered_files), key=lambda p: str(p))

    grand_injected = 0
    files_modified = 0

    for tf in target_files:
        actual_path = tf
        if not actual_path.exists() and args.draft_dir and (args.draft_dir / actual_path.name).exists():
            actual_path = args.draft_dir / actual_path.name

        norm_key = str(tf).replace("\\", "/")
        norm_actual = str(actual_path).replace("\\", "/")
        claims = claims_by_file.get(norm_key, []) or claims_by_file.get(norm_actual, [])
        if not claims:
            for k in claims_by_file:
                if norm_key.endswith(k) or k.endswith(tf.name) or norm_actual.endswith(k):
                    claims = claims_by_file[k]
                    break

        if not claims and not args.strip:
            print(f"[-] {actual_path}: Tidak ada pemetaan klaim pada references.txt.")
            continue

        injected_count, changed = process_markdown_file(
            actual_path, claims, ref_map, dry_run=args.dry_run, strip_mode=args.strip
        )
        status_str = "BERUBAH" if changed else "TIDAK BERUBAH"
        if args.strip:
            print(f"[OK] {actual_path}: {status_str} (strip mode)")
        else:
            print(f"[OK] {actual_path}: {injected_count} klaim disuntikkan ({status_str})")

        grand_injected += injected_count
        if changed:
            files_modified += 1

    print("-------------------------------------------------------------")
    print(f"Ringkasan: {grand_injected} sitasi diproses di {files_modified} berkas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
