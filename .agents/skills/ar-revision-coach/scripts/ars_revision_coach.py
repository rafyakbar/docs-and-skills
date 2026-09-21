#!/usr/bin/env python3
"""CLI dan mesin pembantu ar-revision-coach.

Mendekonstruksi komentar reviewer mentah menjadi:
1. Revision Roadmap terstruktur (Schema 7: P1/P2/P3, pemetaan bab, urutan kerja, estimasi beban kerja)
2. Revision Tracking Table dengan nested-object Commitment Ledger YAML (#268 / Schema 11)
3. Response Letter Skeleton (Pola R -> A -> C)

Menggunakan 100% pustaka standar Python (tanpa pip dependensi eksternal).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from _coach_constants import (
        COMMITMENT_TYPES,
        EFFORT_LEVELS,
        EVIDENCE_TYPES,
        EXTRACTION_FIELDS,
        IMPERATIVE_COMMITMENT_PATTERNS,
        MANUSCRIPT_EVIDENCE_TYPES,
        NONFULFILLED_STATUSES,
        PRIORITIES,
        PRIORITY_FROM_LABEL,
        PRIORITY_LABELS,
        RESOLUTION_STATUSES,
        RETIRED_INDEX_NOTATION,
        SECTION_MAPPING_KEYWORDS,
        SEVERITY_TYPES,
        STATUS_ENUM,
    )
except ImportError:
    from scripts._coach_constants import (
        COMMITMENT_TYPES,
        EFFORT_LEVELS,
        EVIDENCE_TYPES,
        EXTRACTION_FIELDS,
        IMPERATIVE_COMMITMENT_PATTERNS,
        MANUSCRIPT_EVIDENCE_TYPES,
        NONFULFILLED_STATUSES,
        PRIORITIES,
        PRIORITY_FROM_LABEL,
        PRIORITY_LABELS,
        RESOLUTION_STATUSES,
        RETIRED_INDEX_NOTATION,
        SECTION_MAPPING_KEYWORDS,
        SEVERITY_TYPES,
        STATUS_ENUM,
    )


class ParsedComment:
    def __init__(
        self,
        concern_id: str,
        reviewer_id: str,
        raw_text: str,
        summary: str,
        severity: str = "Minor",
        section: str = "general",
        priority: str = "P2",
        action: str = "",
        commitments: Optional[List[Dict[str, str]]] = None,
    ):
        self.concern_id = concern_id
        self.reviewer_id = reviewer_id
        self.raw_text = raw_text.strip()
        self.summary = summary.strip() or self.raw_text[:120]
        self.severity = severity if severity in SEVERITY_TYPES else "Minor"
        self.section = section
        self.priority = priority if priority in PRIORITIES else "P2"
        self.action = action.strip() or "Klarifikasi dan lakukan perbaikan yang disyaratkan pada naskah."
        self.commitments = commitments or []


def detect_reviewer_id(header_line: str) -> str:
    line = header_line.strip()
    if re.search(r"editor|eic", line, re.IGNORECASE):
        return "EIC"
    if re.search(r"devil['’]?s\s*advocate|da\b", line, re.IGNORECASE):
        return "DA"
    m = re.search(r"(?:reviewer|r)\s*#?\s*([0-9]+)", line, re.IGNORECASE)
    if m:
        return f"R{m.group(1)}"
    return "R1"


def map_section_from_text(text: str) -> str:
    text_lower = text.lower()
    for section, keywords in SECTION_MAPPING_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return section
    return "general"


def classify_severity(text: str, reviewer_id: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ["praise", "good job", "appreciate", "well written", "menarik", "sangat baik", "kekuatan"]):
        return "Positive"
    if any(k in text_lower for k in ["typo", "grammar", "spelling", "formatting", "tata bahasa", "ejaan"]):
        return "Editorial"
    if any(k in text_lower for k in ["fatal", "critical", "leakage", "flaw", "cannot be accepted", "fundamental", "unsupported", "invalid", "overclaim"]):
        return "Major"
    if reviewer_id == "DA":
        return "Major"
    return "Minor"


def clean_single_line(text: str) -> str:
    """Membersihkan teks menjadi satu baris tanpa newline, tab, atau karakter kutip ganda/pipe."""
    cleaned = re.sub(r"[\r\n\t]+", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.replace('"', "'").replace("|", "/").strip()
    return cleaned


def extract_commitments(raw_text: str, severity: str) -> List[Dict[str, str]]:
    if severity == "Positive":
        return []

    commitments: List[Dict[str, str]] = []
    for pat, ctype, etype in IMPERATIVE_COMMITMENT_PATTERNS:
        matches = pat.findall(raw_text)
        for match in matches:
            text = clean_single_line(match)
            if len(text) > 5:
                commitments.append({
                    "commitment_text": text[:150],
                    "commitment_type": ctype,
                    "required_evidence_type": etype,
                })

    # Default commitment jika belum terdeteksi pola eksplisit
    if not commitments:
        cleaned_raw = clean_single_line(raw_text)
        if severity == "Major":
            commitments.append({
                "commitment_text": f"Selesaikan isu metodologi/analisis: {cleaned_raw[:80]}",
                "commitment_type": "add_analysis",
                "required_evidence_type": "discussion_paragraph",
            })
        elif severity == "Editorial":
            commitments.append({
                "commitment_text": f"Koreksi editorial/tata bahasa: {cleaned_raw[:80]}",
                "commitment_type": "other",
                "required_evidence_type": "prose_edit",
            })
        else:
            commitments.append({
                "commitment_text": f"Berikan penjelasan dan bukti tambahan: {cleaned_raw[:80]}",
                "commitment_type": "add_clarification",
                "required_evidence_type": "methods_paragraph",
            })

    return commitments


def parse_review_text(content: str) -> List[ParsedComment]:
    # Jika input dibungkus dalam blok ```markdown, ekstrak blok tersebut
    m_block = re.search(r"```markdown\s*\n(#+ Editorial Decision.*?)\n```", content, re.DOTALL | re.IGNORECASE)
    if m_block:
        content = m_block.group(1)

    lines = content.splitlines()
    current_reviewer = "Reviewer 1"
    comments: List[ParsedComment] = []
    buffer: List[str] = []
    item_counter = 1

    def flush_comment(buf: List[str], rev: str, count: int):
        if not buf:
            return
        raw = "\n".join(buf).strip()
        if len(raw) < 15:
            return
        rev_id = detect_reviewer_id(rev)
        cid = f"{rev_id}-{count}"
        sev = classify_severity(raw, rev_id)
        sec = map_section_from_text(raw)
        prio = "P1" if (sev == "Major" or rev_id == "EIC") else ("P3" if sev == "Editorial" else "P2")
        comms = extract_commitments(raw, sev)

        # Ringkasan baris pertama
        first_line = raw.split("\n")[0].strip()
        first_line = re.sub(r"^(?:[\*\-\d\.\)]+|###?\s*Comment\s*[\w\-]+:?)\s*", "", first_line)
        summary = clean_single_line(first_line)[:140]

        comments.append(ParsedComment(
            concern_id=cid,
            reviewer_id=rev_id,
            raw_text=raw,
            summary=summary,
            severity=sev,
            section=sec,
            priority=prio,
            action="Klarifikasi dan lengkapi bagian terkait sesuai masukan.",
            commitments=comms,
        ))

    for line in lines:
        stripped = line.strip()
        # Cek apakah pergantian reviewer
        if re.match(r"^(?:#+\s*)?(?:Reviewer\s*#?[0-9]+|Editor-in-Chief|Editor|EIC|Devil['’]?s\s*Advocate|DA\b)", stripped, re.IGNORECASE):
            flush_comment(buffer, current_reviewer, item_counter)
            buffer = []
            current_reviewer = stripped
            item_counter = 1
            continue

        # Cek apakah pergantian item komentar
        if re.match(r"^(?:(?:\*|\-|\d+[\.\)])\s+|###?\s+(?:Comment\s+)?([A-Za-z0-9\-]+)[:\.]?\s*)", stripped) and len(buffer) > 2:
            flush_comment(buffer, current_reviewer, item_counter)
            buffer = [stripped]
            item_counter += 1
            continue

        if stripped:
            buffer.append(stripped)
        elif buffer:
            buffer.append("")

    flush_comment(buffer, current_reviewer, item_counter)
    return comments


def calculate_effort_level(comments: List[ParsedComment]) -> Tuple[str, str]:
    major_count = sum(1 for c in comments if c.severity == "Major")
    minor_count = sum(1 for c in comments if c.severity == "Minor")
    if major_count > 5:
        return "Substantial", EFFORT_LEVELS["Substantial"]
    elif major_count >= 3 or minor_count > 8:
        return "Moderate", EFFORT_LEVELS["Moderate"]
    elif major_count == 0 and minor_count < 5:
        return "Light", EFFORT_LEVELS["Light"]
    return "Moderate", EFFORT_LEVELS["Moderate"]


def generate_revision_roadmap_md(
    comments: List[ParsedComment],
    title: str = "Naskah Penelitian Akademik",
    decision: str = "Major Revision",
) -> str:
    effort_level, effort_desc = calculate_effort_level(comments)
    major_c = sum(1 for c in comments if c.severity == "Major")
    minor_c = sum(1 for c in comments if c.severity == "Minor")
    edit_c = sum(1 for c in comments if c.severity == "Editorial")
    pos_c = sum(1 for c in comments if c.severity == "Positive")

    p1_items = [c for c in comments if c.priority == "P1"]
    p2_items = [c for c in comments if c.priority == "P2"]
    p3_items = [c for c in comments if c.priority == "P3"]
    pos_items = [c for c in comments if c.severity == "Positive"]

    lines = [
        f"# Revision Roadmap: {title}",
        "",
        "> Dokumen ini dihasilkan secara terstruktur melalui skill `ar-revision-coach` (Fase 19–21).",
        "> Membedah komentar ulasan reviewer menjadi matriks prioritas terarah sebelum eksekusi revisi.",
        "",
        "## 1. Ikhtisar Editorial & Beban Kerja (Overview)",
        f"- **Keputusan Editorial**: `{decision}`",
        f"- **Total Komentar Diurai**: {len(comments)} butir",
        f"- **Distribusi Kategori**: {major_c} Major | {minor_c} Minor | {edit_c} Editorial | {pos_c} Positive",
        f"- **Estimasi Beban Revisi**: `{effort_level}` ({effort_desc})",
        "",
        "---",
        "",
        "## 2. Matriks Prioritas Aksi Revisi",
        "",
        "### Prioritas 1: Must Fix (P1 — Isu Kritis Penentu Akseptasi)",
        "| ID | Reviewer | Seksion Target | Ringkasan Masukan Reviewer | Usulan Tindakan Penulis |",
        "|:---|:---|:---|:---|:---|",
    ]

    if not p1_items:
        lines.append("| - | - | - | _(Tidak ada isu kritis P1 terdeteksi)_ | - |")
    else:
        for it in p1_items:
            lines.append(f"| `{it.concern_id}` | {it.reviewer_id} | `{it.section}` | {it.summary} | {it.action} |")

    lines.extend([
        "",
        "### Prioritas 2: Should Fix (P2 — Peningkatan Substansi & Metodologi)",
        "| ID | Reviewer | Seksion Target | Ringkasan Masukan Reviewer | Usulan Tindakan Penulis |",
        "|:---|:---|:---|:---|:---|",
    ])

    if not p2_items:
        lines.append("| - | - | - | _(Tidak ada isu moderat P2 terdeteksi)_ | - |")
    else:
        for it in p2_items:
            lines.append(f"| `{it.concern_id}` | {it.reviewer_id} | `{it.section}` | {it.summary} | {it.action} |")

    lines.extend([
        "",
        "### Prioritas 3: Consider (P3 — Editorial, Tipografi & Kosmetik)",
        "| ID | Reviewer | Seksion Target | Ringkasan Masukan Reviewer | Usulan Tindakan Penulis |",
        "|:---|:---|:---|:---|:---|",
    ])

    if not p3_items:
        lines.append("| - | - | - | _(Tidak ada isu minor P3 terdeteksi)_ | - |")
    else:
        for it in p3_items:
            lines.append(f"| `{it.concern_id}` | {it.reviewer_id} | `{it.section}` | {it.summary} | {it.action} |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Catatan Apresiatif Reviewer (Positive Feedback)",
        "| ID | Reviewer | Aspek yang Diapresiasi |",
        "|:---|:---|:---|",
    ])

    if not pos_items:
        lines.append("| - | - | _(Komentar tidak menyertakan pujian khusus — tidak ada kuota buatan)_ |")
    else:
        for it in pos_items:
            lines.append(f"| `{it.concern_id}` | {it.reviewer_id} | {it.summary} |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Pola Isu Silang Reviewer (Cross-Reviewer Patterns)",
        "> Mengidentifikasi titik kelemahan yang disoroti oleh lebih dari satu penilai independen:",
        "",
    ])

    # Deteksi pola silang
    section_counts: Dict[str, List[str]] = {}
    for c in comments:
        section_counts.setdefault(c.section, []).append(c.reviewer_id)

    cross_found = False
    for sec, revs in section_counts.items():
        unique_revs = list(set(revs))
        if len(unique_revs) > 1 and sec != "general":
            cross_found = True
            lines.append(f"- **Seksion `{sec}`**: Diangkat secara independen oleh `{', '.join(unique_revs)}`. Memerlukan perhatian konsolidasi khusus.")

    if not cross_found:
        lines.append("- _Setiap penilai menyoroti area unik; tidak ada konsentrasi isu silang dominan._")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Rekomendasi Urutan Eksekusi Revisi (Suggested Sequence)",
        "1. **Konsultasi Dosen Pembimbing (Fase 21)**: Bawa dokumen roadmap ini untuk menyetujui batasan eksperimen tambahan.",
        "2. **Eksekusi Isu Metodologis P1**: Tangani kelemahan data, partisi, validasi silang, dan metrik di bab `03_methodology.md` dan `04_results.md`.",
        "3. **Penyempurnaan Narasi & Kerangka P2**: Perkuat bab `01_introduction.md` dan `05_discussion.md` untuk menjawab catatan reviewer.",
        "4. **Pembersihan Editorial P3**: Selesaikan tipo, notasi persamaan, dan format referensi.",
        "5. **Audit Rebuttal (Fase 23)**: Jalankan audit surat sanggahan sebelum kirim ulang (*resubmission*).",
    ])

    return "\n".join(lines) + "\n"


def generate_revision_tracking_md(
    comments: List[ParsedComment],
    title: str = "Naskah Penelitian Akademik",
) -> str:
    lines = [
        f"# Revision Tracking Table: {title}",
        "",
        "> Matriks pelacakan status resolusi dan Nested Commitment Ledger (Schema 11 / Kong et al. 2026 §7.4.3).",
        "> Memastikan seluruh janji perbaikan memiliki bukti nyata di naskah dan bebas desinkronisasi indeks (#268).",
        "",
        "## 1. Tabel Pelacakan Resolusi Komentar",
        "",
        "| ID | Reviewer | Tipe | Seksion | Ringkasan Isu | Rencana Tindakan Resolusi | Lokasi Perubahan | Status | Alasan (Jika Non-Fulfilled) |",
        "|:---|:---|:---|:---|:---|:---|:---|:---|:---|",
    ]

    for c in comments:
        lines.append(
            f"| `{c.concern_id}` | {c.reviewer_id} | `{c.severity}` | `{c.section}` | {c.summary} | {c.action} | `TBD` | `RESOLVED` | - |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. Nested Commitment Ledger (YAML Blok Terstruktur)",
        "",
        "```yaml",
        "# Schema 11 R&R Traceability Matrix - Nested Shape (#268)",
    ])

    for c in comments:
        lines.append(f"- concern_id: \"{c.concern_id}\"")
        if not c.commitments:
            lines.append("  commitment_extracted: []")
        else:
            lines.append("  commitment_extracted:")
            for comm in c.commitments:
                lines.append(f"    - commitment_text: \"{comm['commitment_text']}\"")
                lines.append(f"      commitment_type: {comm['commitment_type']}")
                lines.append(f"      required_evidence_type: {comm['required_evidence_type']}")
                # fulfillment_status diisi saat fase revisi dieksekusi

    lines.extend([
        "```",
        "",
        "---",
        "",
        "## 3. Glosarium Status Resolusi",
        "- `RESOLVED`: Isu reviewer sepenuhnya terselesaikan dengan bukti nyata di teks naskah baru.",
        "- `DELIBERATE_LIMITATION`: Isu diakui sebagai batasan desain riset yang disengaja dan dijelaskan di bab Keterbatasan.",
        "- `UNRESOLVABLE`: Isu mustahil diselesaikan tanpa studi baru total (dijadikan rekomendasi *Future Work*).",
        "- `REVIEWER_DISAGREE`: Penulis mempertahankan posisi awal dengan bukti ilmiah, sitasi, dan penalaran santun.",
    ])

    return "\n".join(lines) + "\n"


def generate_response_letter_skeleton_md(
    comments: List[ParsedComment],
    title: str = "Naskah Penelitian Akademik",
    journal: str = "Target Journal",
) -> str:
    lines = [
        f"# Response to Reviewers (Skeleton): {title}",
        "",
        f"**Journal**: {journal}  ",
        "**Revision Round**: Round 1  ",
        "",
        "---",
        "",
        "## Opening Statement",
        "Dear Editor-in-Chief and Reviewers,",
        "",
        f"We sincerely thank the Editor and the Reviewers for their thoughtful, constructive, and comprehensive evaluation of our manuscript titled \"{title}\". The insightful feedback has significantly helped us strengthen the methodological rigor, clarify theoretical nuances, and improve the overall presentation of our work.",
        "",
        "Below, we provide our detailed point-by-point responses to each comment, accompanied by precise cross-references to the revised manuscript.",
        "",
        "---",
        "",
        "## Summary of Major Revisions",
        "1. **Methodological & Empirical Rigor**: [Rangkum pengujian tambahan atau klarifikasi metrik utama].",
        "2. **Theoretical & Literature Context**: [Rangkum literatur baru atau perbandingan kerangka kerja].",
        "3. **Reporting & Presentation**: [Rangkum penyempurnaan tabel, grafik, dan kejelasan narasi].",
        "",
        "---",
    ]

    # Kelompokkan per reviewer
    by_rev: Dict[str, List[ParsedComment]] = {}
    for c in comments:
        by_rev.setdefault(c.reviewer_id, []).append(c)

    for rev_id, rev_comments in by_rev.items():
        lines.extend([
            f"## Detailed Responses to {rev_id}",
            "",
        ])
        for c in rev_comments:
            lines.extend([
                f"### Comment {c.concern_id}: {c.summary}",
                f"> \"{c.raw_text}\"",
                "",
                "**Author Response**:",
                f"[Tulis tanggapan santun penulis di sini. Jelaskan bagaimana masukan {rev_id} telah diakomodasi atau alasan jika mempertahankan posisi semula].",
                "",
                "**Changes Made**:",
                f"- **Lokasi Naskah**: Bab `{c.section}`, Halaman [X], Paragraf [Y].",
                "- **Rincian Teks**: [Kutip perubahan teks baru yang dimasukkan ke dalam naskah].",
                "",
                "---",
                "",
            ])

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ar-revision-coach: Parser komentar ulasan & generator Roadmap Revisi terstruktur."
    )
    parser.add_argument("review_file", help="Path ke berkas ulasan reviewer mentah (.md / .txt).")
    parser.add_argument("--outdir", default=".", help="Direktori keluaran untuk menyimpan artefak.")
    parser.add_argument("--title", default="Academic Manuscript", help="Judul naskah penelitian.")
    parser.add_argument("--decision", default="Major Revision", help="Keputusan editorial (Major/Minor Revision).")
    parser.add_argument("--journal", default="Target Journal", help="Nama jurnal target.")
    parser.add_argument("--all", action="store_true", help="Hasilkan ketiga berkas artefak sekaligus.")
    parser.add_argument("--roadmap", action="store_true", help="Hasilkan 08_revision_roadmap.md.")
    parser.add_argument("--tracking", action="store_true", help="Hasilkan 09_revision_tracking.md.")
    parser.add_argument("--skeleton", action="store_true", help="Hasilkan 10_response_letter_skeleton.md.")

    args = parser.parse_args()
    review_path = Path(args.review_file)

    if not review_path.exists():
        print(f"ERROR: Berkas ulasan tidak ditemukan: {review_path}", file=sys.stderr)
        return 1

    content = review_path.read_text(encoding="utf-8")
    comments = parse_review_text(content)

    if not comments:
        print(f"PERINGATAN: Tidak ada komentar reviewer yang berhasil diurai dari {review_path}.", file=sys.stderr)
        return 1

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    do_all = args.all or (not args.roadmap and not args.tracking and not args.skeleton)

    if do_all or args.roadmap:
        roadmap_content = generate_revision_roadmap_md(comments, title=args.title, decision=args.decision)
        roadmap_file = outdir / "08_revision_roadmap.md"
        roadmap_file.write_text(roadmap_content, encoding="utf-8")
        print(f"[OK] Revision Roadmap tersimpan di: {roadmap_file}")

    if do_all or args.tracking:
        tracking_content = generate_revision_tracking_md(comments, title=args.title)
        tracking_file = outdir / "09_revision_tracking.md"
        tracking_file.write_text(tracking_content, encoding="utf-8")
        print(f"[OK] Revision Tracking Table tersimpan di: {tracking_file}")

    if do_all or args.skeleton:
        skeleton_content = generate_response_letter_skeleton_md(comments, title=args.title, journal=args.journal)
        skeleton_file = outdir / "10_response_letter_skeleton.md"
        skeleton_file.write_text(skeleton_content, encoding="utf-8")
        print(f"[OK] Response Letter Skeleton tersimpan di: {skeleton_file}")

    print(f"\nBerhasil mendekonstruksi {len(comments)} komentar ulasan reviewer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
