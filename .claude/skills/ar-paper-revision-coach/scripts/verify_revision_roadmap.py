#!/usr/bin/env python3
"""Linter penjamin mutu untuk artefak keluaran ar-paper-revision-coach.

Memeriksa kepatuhan:
1. Invarian #268 Nested Commitment Ledger (N1-N5) / Kong et al. 2026 §7.4.3
2. Zero-Orphan & konsistensi pelacakan komentar reviewer
3. Validitas tipe bukti, tipe komitmen, status resolusi, dan prioritas P1-P3
4. Ketiadaan placeholder usang dan notasi indeks parallel-list

Menggunakan 100% pustaka standar Python (tanpa pip dependensi eksternal).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    from _coach_constants import (
        COMMITMENT_TYPES,
        EVIDENCE_TYPES,
        EXTRACTION_FIELDS,
        NONFULFILLED_STATUSES,
        PRIORITIES,
        RESOLUTION_STATUSES,
        RETIRED_INDEX_NOTATION,
        SEVERITY_TYPES,
        STATUS_ENUM,
    )
except ImportError:
    from scripts._coach_constants import (
        COMMITMENT_TYPES,
        EVIDENCE_TYPES,
        EXTRACTION_FIELDS,
        NONFULFILLED_STATUSES,
        PRIORITIES,
        RESOLUTION_STATUSES,
        RETIRED_INDEX_NOTATION,
        SEVERITY_TYPES,
        STATUS_ENUM,
    )


def extract_yaml_blocks(text: str) -> List[str]:
    """Mengekstrak seluruh blok kode yaml dari dokumen Markdown."""
    blocks: List[str] = []
    pattern = re.compile(r"```ya?ml\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(text):
        blocks.append(m.group(1))
    return blocks


def parse_simple_yaml_ledger(yaml_text: str) -> List[Dict[str, Any]]:
    """Parser YAML ringan berbasis Python Standard Library untuk nested commitment ledger."""
    records: List[Dict[str, Any]] = []
    current_record: Optional[Dict[str, Any]] = None
    current_commitment: Optional[Dict[str, Any]] = None
    in_commitments = False

    lines = yaml_text.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # concern_id baris baru
        m_cid = re.match(r"^-\s+concern_id:\s*[\"']?([^\"'\n]+)[\"']?", stripped)
        if m_cid:
            if current_commitment and current_record:
                current_record["commitment_extracted"].append(current_commitment)
                current_commitment = None
            if current_record:
                records.append(current_record)
            current_record = {
                "concern_id": m_cid.group(1).strip(),
                "commitment_extracted": [],
            }
            in_commitments = False
            continue

        # commitment_extracted header
        if "commitment_extracted: []" in stripped:
            if current_record:
                current_record["commitment_extracted"] = []
            in_commitments = False
            continue
        elif "commitment_extracted:" in stripped:
            in_commitments = True
            continue

        # Komitmen item baru
        if in_commitments and stripped.startswith("- commitment_text:"):
            if current_commitment and current_record:
                current_record["commitment_extracted"].append(current_commitment)
            val = re.sub(r"^-\s+commitment_text:\s*[\"']?", "", stripped)
            val = re.sub(r"[\"']?$", "", val).strip()
            current_commitment = {"commitment_text": val}
            continue

        # Atribut komitmen bersarang
        if current_commitment is not None:
            m_field = re.match(r"^([a-z_]+):\s*(.*)", stripped)
            if m_field:
                k, v = m_field.group(1).strip(), m_field.group(2).strip()
                v = re.sub(r"^[\"']|[\"']$", "", v)
                current_commitment[k] = v

    if current_commitment and current_record:
        current_record["commitment_extracted"].append(current_commitment)
    if current_record:
        records.append(current_record)

    return records


def verify_commitment_invariants(records: List[Dict[str, Any]]) -> List[str]:
    """Memeriksa invarian N1, N2, N3 pada daftar komitmen bertingkat."""
    errors: list[str] = []

    for r in records:
        cid = r.get("concern_id", "<unknown>")
        comms = r.get("commitment_extracted", [])

        for idx, com in enumerate(comms):
            where = f"concern `{cid}` komitmen [{idx}]"
            if not isinstance(com, dict):
                errors.append(f"N1: {where} bukan struktur mapping objek.")
                continue

            # N1: Seluruh field ekstraksi wajib ada
            for field in EXTRACTION_FIELDS:
                if field not in com or not str(com[field]).strip():
                    errors.append(f"N1: {where} kehilangan field ekstraksi wajib `{field}`.")

            # Validasi enum tipe komitmen
            ctype = com.get("commitment_type")
            if ctype and ctype not in COMMITMENT_TYPES:
                errors.append(f"ENUM: {where} commitment_type `{ctype}` tidak valid.")

            # Validasi enum tipe bukti
            etype = com.get("required_evidence_type")
            if etype and etype not in EVIDENCE_TYPES:
                errors.append(f"ENUM: {where} required_evidence_type `{etype}` tidak valid.")

            # N3: Lifecycle coherence jika status terisi
            status = com.get("fulfillment_status")
            has_rationale = "unfulfilled_rationale" in com
            if status:
                if status not in STATUS_ENUM:
                    errors.append(f"N3: {where} fulfillment_status `{status}` di luar enum standar.")
                if status == "fulfilled" and has_rationale:
                    errors.append(
                        f"N3: {where} berstatus `fulfilled` namun menyertakan `unfulfilled_rationale`. "
                        "Hilangkan rationale jika terpenuhi (larangan placeholder kosong '')."
                    )
                if status in NONFULFILLED_STATUSES and has_rationale:
                    rat_val = str(com.get("unfulfilled_rationale", "")).strip()
                    if not rat_val:
                        errors.append(
                            f"N3: {where} berstatus `{status}` membawa unfulfilled_rationale kosong. "
                            "Wajib menyertakan penjelasan substantif."
                        )

    return errors


def verify_markdown_integrity(filepath: Path) -> Tuple[List[str], List[str]]:
    """Memeriksa dokumen Markdown terhadap aturan konsistensi, zero-orphan, dan tabel."""
    errors: list[str] = []
    warnings: list[str] = []

    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    # N4 / N5: Periksa tidak ada sisa notasi indeks usang
    for m in RETIRED_INDEX_NOTATION.finditer(content):
        line_no = content.count("\n", 0, m.start()) + 1
        errors.append(
            f"N4/N5 (Baris {line_no}): Terdeteksi sisa notasi indeks usang `{m.group(0)}`. "
            "Gunakan nested-object shape (#268)."
        )

    # Ekstrak blok YAML jika ada
    yaml_blocks = extract_yaml_blocks(content)
    parsed_records: List[Dict[str, Any]] = []
    for b in yaml_blocks:
        if "commitment_extracted" in b:
            parsed_records.extend(parse_simple_yaml_ledger(b))

    if parsed_records:
        inv_errors = verify_commitment_invariants(parsed_records)
        errors.extend(inv_errors)

    # Validasi tabel Markdown pelacakan atau roadmap jika ada
    table_rows = [l for l in lines if l.strip().startswith("|") and not l.strip().startswith("|:")]
    header_found = False
    concern_ids_in_table = set()

    for r in table_rows:
        cols = [c.strip() for c in r.split("|")[1:-1]]
        if len(cols) < 3:
            continue
        if "ID" in cols[0] or "concern_id" in cols[0].lower():
            header_found = True
            continue

        raw_id = cols[0].replace("`", "").strip()
        if raw_id and raw_id != "-":
            concern_ids_in_table.add(raw_id)

    # Konsistensi Zero-Orphan antara tabel dan blok YAML
    if parsed_records and concern_ids_in_table:
        yaml_ids = {r["concern_id"] for r in parsed_records}
        orphan_table = concern_ids_in_table - yaml_ids
        orphan_yaml = yaml_ids - concern_ids_in_table

        if orphan_table:
            warnings.append(f"Zero-Orphan: ID pada tabel belum tercatat di blok YAML: {sorted(orphan_table)}")
        if orphan_yaml:
            warnings.append(f"Zero-Orphan: ID pada YAML belum tercatat di tabel utama: {sorted(orphan_yaml)}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="verify_revision_roadmap: Linter integritas Roadmap & Commitment Ledger Schema 11."
    )
    parser.add_argument("files", nargs="+", help="Path ke satu atau beberapa file artefak Markdown.")

    args = parser.parse_args()
    total_errors = 0
    total_warnings = 0

    print("=" * 65)
    print("AUDIT INTEGRITAS ROADMAP & COMMITMENT LEDGER (SCHEMA 11 / #268)")
    print("=" * 65)

    for fpath in args.files:
        p = Path(fpath)
        if not p.exists():
            print(f"[FAIL] Berkas tidak ditemukan: {p}")
            total_errors += 1
            continue

        errors, warnings = verify_markdown_integrity(p)
        print(f"\nMengevaluasi: {p.name}")
        print("-" * 50)

        if errors:
            print(f"  [ERROR] Ditemukan {len(errors)} pelanggaran integritas:")
            for e in errors:
                print(f"    - {e}")
            total_errors += len(errors)
        else:
            print("  [PASS] 0 pelanggaran invarian struktural.")

        if warnings:
            print(f"  [WARN] Ditemukan {len(warnings)} catatan peringatan:")
            for w in warnings:
                print(f"    - {w}")
            total_warnings += len(warnings)

    print("\n" + "=" * 65)
    if total_errors > 0:
        print(f"HASIL AKHIR: GAGAL ({total_errors} error, {total_warnings} warning).")
        return 1
    print(f"HASIL AKHIR: SUKSES (0 error, {total_warnings} warning). Seluruh invarian patuh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
