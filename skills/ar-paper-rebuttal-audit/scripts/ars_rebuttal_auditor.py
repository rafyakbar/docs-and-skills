#!/usr/bin/env python3
"""ARS Rebuttal Auditor — Advisory QA for Response to Reviewers.

Normative source: ARS academic-paper `rebuttal-audit` mode.
Evaluates an author's existing rebuttal / response-to-reviewers draft against
the original reviewer comments across 4 dimensions:
  1. Zero-Orphan Coverage (every comment accounted for, no dropped concerns)
  2. Tone & Academic Diplomacy (anti-defensive, anti-sycophancy, non-hostile)
  3. Evidence Grounding & Locators (section, page, table, figure, block IDs)
  4. Disagreement & Limitation Justification (scientifically sound rationale)

IRON RULE — integrity boundary (no false certification):
  This is an advisory QA auditor. It does NOT generate a new response,
  does NOT rewrite text silently, and does NOT emit Schema 11 / Material
  Passport / verified status.

Pure Python Standard Library only (zero pip dependencies).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Ensure script's directory is in sys.path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from _rebuttal_constants import (
    AUDIT_REPORT_FORMAT_VERSION,
    BLOCK_ID_LOCATOR_RE,
    COMBATIVE_PATTERNS,
    COMMENT_DELIMITER_RE,
    DOC_HEADER_SKIP_RE,
    EVASIVE_PATTERNS,
    PAGE_LINE_LOCATOR_RE,
    RESPONSE_DELIMITER_RE,
    REVIEWER_HEADER_RE,
    SYCOPHANTIC_PATTERNS,
)


@dataclass
class ReviewerComment:
    comment_id: str
    reviewer: str
    raw_text: str
    summary: str


@dataclass
class ResponseEntry:
    entry_id: str
    matched_comment_id: str
    raw_text: str
    author_response: str
    changes_made: str
    status: str
    locators: list[str]


@dataclass
class RiskFlag:
    category: str  # combative | evasive | sycophantic | ungrounded | unjustified_refusal
    severity: str  # HIGH | MEDIUM | LOW
    target_id: str
    quote: str
    explanation: str
    suggested_rewording: str


@dataclass
class ItemAuditResult:
    comment_id: str
    reviewer: str
    comment_snippet: str
    coverage_status: str  # ADDRESSED | PARTIALLY_ADDRESSED | MISSING | UNRESOLVED_DISAGREE
    response_snippet: str
    locators_found: list[str]
    risk_flags: list[RiskFlag] = field(default_factory=list)


def parse_reviewer_comments(text: str) -> list[ReviewerComment]:
    """Parse raw reviewer comments into discrete structured items."""
    lines = text.splitlines()
    comments: list[ReviewerComment] = []

    current_reviewer = "Reviewer"
    current_id = ""
    current_lines: list[str] = []
    item_counter = 1

    def _flush():
        nonlocal current_id, current_lines, item_counter
        if current_lines:
            raw = "\n".join(current_lines).strip()
            if raw and len(raw.split()) >= 3:
                cid = current_id or f"C{item_counter:03d}"
                first_line = current_lines[0].strip()
                if len(first_line) > 100:
                    summary = first_line[:97] + "..."
                else:
                    summary = first_line
                comments.append(
                    ReviewerComment(
                        comment_id=cid,
                        reviewer=current_reviewer,
                        raw_text=raw,
                        summary=summary,
                    )
                )
                item_counter += 1
            current_lines = []
            current_id = ""

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_lines:
                current_lines.append(line)
            continue

        if not current_lines and DOC_HEADER_SKIP_RE.match(stripped):
            continue

        # Check for reviewer header
        rev_match = REVIEWER_HEADER_RE.match(stripped)
        if rev_match:
            _flush()
            rev_label = rev_match.group(0).lstrip("#").strip()
            current_reviewer = rev_label
            continue

        # Check for comment delimiter (e.g. "### Comment 1:", "Comment 1 (R1-1):", "REV-001", "1. ")
        comm_match = COMMENT_DELIMITER_RE.match(stripped)
        if comm_match:
            _flush()
            # If group 3 exists (e.g. in parentheses like (R1-1)), prioritize it
            cid_tag = comm_match.group(3) or comm_match.group(1) or comm_match.group(2)
            if cid_tag:
                clean_tag = re.sub(r"[^A-Za-z0-9_.-]", "", cid_tag)
                current_id = clean_tag if len(clean_tag) <= 15 else f"C{item_counter:03d}"
            current_lines.append(line)
            continue

        current_lines.append(line)

    _flush()
    return comments


def parse_rebuttal_draft(text: str) -> list[ResponseEntry]:
    """Parse author's response letter into discrete response entries."""
    sections = re.split(r"\n(?=#{1,4}\s+(?:REV|Comment|Point|Item|R\d+|Response\s+to\s+Reviewer|[0-9]+[.)]))", text)
    entries: list[ResponseEntry] = []
    entry_counter = 1

    for sec in sections:
        sec_str = sec.strip()
        if not sec_str or len(sec_str.split()) < 5:
            continue

        first_line = sec_str.splitlines()[0]
        # Look for comment ID reference (e.g. REV-001, Comment 1, R1-M1)
        cid_match = re.search(r"\b(REV-\d+|C\d+|R\d+[-_]?[A-Za-z0-9]+|Comment\s*\d+|M\d+|m\d+)\b", first_line, re.IGNORECASE)
        entry_id = cid_match.group(1) if cid_match else f"RESP-{entry_counter:03d}"
        entry_counter += 1

        # Extract status tag if present
        status_match = re.search(
            r"\b(RESOLVED|DELIBERATE_LIMITATION|UNRESOLVABLE|REVIEWER_DISAGREE|PARTIALLY_RESOLVED)\b",
            sec_str,
            re.IGNORECASE,
        )
        status = status_match.group(1).upper() if status_match else "RESOLVED"

        # Find locators (Block IDs and Page/Section references)
        block_ids = BLOCK_ID_LOCATOR_RE.findall(sec_str)
        page_secs = PAGE_LINE_LOCATOR_RE.findall(sec_str)
        locators = list(set(block_ids + page_secs))

        # Split into author response vs changes made if demarcated
        author_resp = sec_str
        changes_made = ""
        if "Changes Made" in sec_str or "Changes:" in sec_str:
            parts = re.split(r"(?:Changes\s*Made|Changes)\s*[:\-–]?", sec_str, flags=re.IGNORECASE)
            author_resp = parts[0]
            changes_made = parts[1] if len(parts) > 1 else ""

        entries.append(
            ResponseEntry(
                entry_id=entry_id,
                matched_comment_id=entry_id,
                raw_text=sec_str,
                author_response=author_resp.strip(),
                changes_made=changes_made.strip(),
                status=status,
                locators=locators,
            )
        )

    return entries


def audit_tone(text: str, target_id: str) -> list[RiskFlag]:
    """Audit text against combative, evasive, and sycophantic patterns."""
    flags: list[RiskFlag] = []

    # 1. Combative
    for name, pattern in COMBATIVE_PATTERNS:
        match = pattern.search(text)
        if match:
            quote = match.group(0)
            flags.append(
                RiskFlag(
                    category="combative",
                    severity="HIGH",
                    target_id=target_id,
                    quote=quote,
                    explanation="Nada defensif atau agresif dapat memicu reaksi negatif dari reviewer dan editor.",
                    suggested_rewording="Ganti dengan pengakuan objektif berdiplomasi, misalnya: 'We appreciate this thoughtful critique and have clarified our theoretical boundary in Section X.'",
                )
            )

    # 2. Evasive
    for name, pattern in EVASIVE_PATTERNS:
        match = pattern.search(text)
        if match:
            quote = match.group(0)
            flags.append(
                RiskFlag(
                    category="evasive",
                    severity="MEDIUM",
                    target_id=target_id,
                    quote=quote,
                    explanation="Tanggapan terlalu singkat dan ambigu tanpa rincian perubahan konkret atau nomor halaman/baris.",
                    suggested_rewording="Sebutkan secara spesifik perubahan teks apa yang dilakukan dan kutip kalimat kunci yang ditambahkan.",
                )
            )

    # 3. Sycophantic
    for name, pattern in SYCOPHANTIC_PATTERNS:
        match = pattern.search(text)
        if match:
            quote = match.group(0)
            flags.append(
                RiskFlag(
                    category="sycophantic",
                    severity="LOW",
                    target_id=target_id,
                    quote=quote,
                    explanation="Pujian atau sanjungan yang berlebihan terdengar tidak tulus (*inauthentic sycophancy*).",
                    suggested_rewording="Gunakan ucapan terima kasih akademis yang lugas dan profesional: 'We thank the reviewer for this constructive suggestion.'",
                )
            )

    return flags


def audit_rebuttal(
    comments_text: str,
    rebuttal_text: str,
) -> dict:
    """Execute complete 4-dimension audit and return structured audit report dict."""
    comments = parse_reviewer_comments(comments_text)
    responses = parse_rebuttal_draft(rebuttal_text)

    # Index responses for fast matching
    response_map: dict[str, ResponseEntry] = {}
    for r in responses:
        clean_id = re.sub(r"[^A-Za-z0-9]", "", r.entry_id).lower()
        response_map[clean_id] = r

    item_results: list[ItemAuditResult] = []
    all_flags: list[RiskFlag] = []

    addressed_count = 0
    partially_count = 0
    missing_count = 0

    for comm in comments:
        clean_cid = re.sub(r"[^A-Za-z0-9]", "", comm.comment_id).lower()
        matched_resp: ResponseEntry | None = None

        # Search matching response by ID or substring
        if clean_cid in response_map:
            matched_resp = response_map[clean_cid]
        else:
            # Fallback search by keyword/comment snippet match
            for r in responses:
                if clean_cid in re.sub(r"[^A-Za-z0-9]", "", r.raw_text).lower():
                    matched_resp = r
                    break

        item_flags: list[RiskFlag] = []

        if matched_resp is None:
            coverage_status = "MISSING"
            missing_count += 1
            resp_snippet = "(Tidak ditemukan tanggapan untuk komentar ini di dalam draf)"
            locators = []
            item_flags.append(
                RiskFlag(
                    category="missing_comment",
                    severity="HIGH",
                    target_id=comm.comment_id,
                    quote=comm.summary,
                    explanation="Zero-Orphan Violation: Komentar reviewer ini diabaikan dan tidak dijawab sama sekali dalam surat tanggapan.",
                    suggested_rewording="Tambahkan butir tanggapan khusus yang merujuk komentar ini secara eksplisit.",
                )
            )
        else:
            resp_snippet = matched_resp.author_response[:120].replace("\n", " ") + "..."
            locators = matched_resp.locators

            # Audit tone
            tone_flags = audit_tone(matched_resp.raw_text, comm.comment_id)
            item_flags.extend(tone_flags)

            # Audit locators (Dimension 3)
            if not locators and "acknowledg" not in matched_resp.author_response.lower():
                item_flags.append(
                    RiskFlag(
                        category="ungrounded",
                        severity="MEDIUM",
                        target_id=comm.comment_id,
                        quote=matched_resp.author_response[:80],
                        explanation="Klaim revisi tidak menyertakan locator naskah (Section, Page, Tabel, atau Block ID BNNNN).",
                        suggested_rewording="Tambahkan rujukan lokasi presisi: misalnya 'See revised manuscript Section 3.2, paragraph 2 (Block B0042)'.",
                    )
                )

            # Audit disagreement / limitation (Dimension 4)
            if matched_resp.status in ("REVIEWER_DISAGREE", "DELIBERATE_LIMITATION", "UNRESOLVABLE"):
                if len(matched_resp.author_response.split()) < 30:
                    item_flags.append(
                        RiskFlag(
                            category="unjustified_refusal",
                            severity="HIGH",
                            target_id=comm.comment_id,
                            quote=matched_resp.author_response[:80],
                            explanation="Penolakan atau batasan disampaikan terlalu singkat tanpa bukti data atau kutipan literatur pendukung.",
                            suggested_rewording="Jelaskan kendala empiris, batas etik IRB, atau kutip literatur metodologi yang memvalidasi keputusan tersebut.",
                        )
                    )

            # Evaluate coverage status
            has_high_flag = any(f.severity == "HIGH" for f in item_flags)
            if has_high_flag and any(f.category == "unjustified_refusal" for f in item_flags):
                coverage_status = "UNRESOLVED_DISAGREE"
                partially_count += 1
            elif len(matched_resp.author_response.split()) < 20 or any(f.category == "evasive" for f in item_flags):
                coverage_status = "PARTIALLY_ADDRESSED"
                partially_count += 1
            else:
                coverage_status = "ADDRESSED"
                addressed_count += 1

        all_flags.extend(item_flags)
        item_results.append(
            ItemAuditResult(
                comment_id=comm.comment_id,
                reviewer=comm.reviewer,
                comment_snippet=comm.summary,
                coverage_status=coverage_status,
                response_snippet=resp_snippet,
                locators_found=locators,
                risk_flags=item_flags,
            )
        )

    total_comments = len(comments)
    coverage_ratio = (addressed_count / total_comments) if total_comments > 0 else 1.0

    high_risk_count = sum(1 for f in all_flags if f.severity == "HIGH")
    med_risk_count = sum(1 for f in all_flags if f.severity == "MEDIUM")
    low_risk_count = sum(1 for f in all_flags if f.severity == "LOW")

    if missing_count == 0 and high_risk_count == 0 and coverage_ratio >= 0.90:
        verdict = "PASSED_READINESS"
        verdict_badge = "SIAP SUBMIT (HIGH READINESS)"
    elif missing_count > 0 or high_risk_count > 0:
        verdict = "ACTION_REQUIRED"
        verdict_badge = "PERLU PERBAIKAN KRITIS (ACTION REQUIRED)"
    else:
        verdict = "ADVISORY_POLISHING"
        verdict_badge = "PERBAIKAN MINOR (ADVISORY POLISHING)"

    return {
        "report_format_version": AUDIT_REPORT_FORMAT_VERSION,
        "mode": "rebuttal-audit",
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "counters": {
            "total_comments": total_comments,
            "addressed_count": addressed_count,
            "partially_count": partially_count,
            "missing_count": missing_count,
            "coverage_ratio": round(coverage_ratio, 4),
            "high_risk_flags": high_risk_count,
            "medium_risk_flags": med_risk_count,
            "low_risk_flags": low_risk_count,
        },
        "item_results": [asdict(r) for r in item_results],
        "risk_flags": [asdict(f) for f in all_flags],
    }


def generate_markdown_report(audit_data: dict) -> str:
    """Render audit data into comprehensive, readable GitHub-style Markdown."""
    c = audit_data["counters"]
    badge = audit_data["verdict_badge"]

    out = []
    out.append("# Laporan Audit Penjaminan Mutu Surat Tanggapan Reviewer (Rebuttal QA Report)")
    out.append("")
    out.append(f"**Status Evaluasi:** `{badge}`  ")
    out.append(f"**Rasio Cakupan Komentar (*Coverage Ratio*):** `{c['coverage_ratio'] * 100:.1f}%` ({c['addressed_count']}/{c['total_comments']} komentar terjawab tuntas)  ")
    out.append(f"**Indikator Risiko (*Risk Flags*):** `{c['high_risk_flags']} Tinggi (High)` · `{c['medium_risk_flags']} Sedang (Medium)` · `{c['low_risk_flags']} Rendah (Low)`")
    out.append("")
    out.append("> [!NOTE]")
    out.append("> Laporan ini bersifat penasihat independen (*advisory QA*). Sesuai aturan integritas repositori (*Iron Rule*), audit ini tidak mengubah naskah surat secara otomatis dan tidak menerbitkan status sertifikasi pengajuan formal.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## 1. Matriks Cakupan Butir-per-Butir (*Zero-Orphan Coverage Matrix*)")
    out.append("")
    out.append("| ID | Reviewer | Komentar Asli (Cuplikan) | Status Cakupan | Locator Naskah | Risiko |")
    out.append("|:---|:---|:---|:---:|:---:|:---:|")

    for item in audit_data["item_results"]:
        cid = item["comment_id"]
        rev = item["reviewer"]
        comm = item["comment_snippet"].replace("|", "\\|")
        status = item["coverage_status"]
        if status == "ADDRESSED":
            status_str = "✅ Lengkap"
        elif status == "PARTIALLY_ADDRESSED":
            status_str = "⚠️ Sebagian"
        elif status == "MISSING":
            status_str = "❌ Terlewat"
        else:
            status_str = "🔍 Penolakan"

        locs = ", ".join(item["locators_found"]) if item["locators_found"] else "*(Nihil)*"
        risks = f"{len(item['risk_flags'])} isu" if item["risk_flags"] else "Aman"
        out.append(f"| `{cid}` | {rev} | {comm} | {status_str} | {locs} | {risks} |")

    out.append("")
    out.append("---")
    out.append("")
    out.append("## 2. Temuan Peringatan Kritis & Nada Bahasa (*Tone & Risk Flags*)")
    out.append("")

    if not audit_data["risk_flags"]:
        out.append("✅ **Tidak ditemukan kalimat defensif, ambiguitas evasif, atau penolakan tanpa dasar.** Surat tanggapan menggunakan gaya bahasa akademis yang santun dan berbobot.")
    else:
        for idx, flag in enumerate(audit_data["risk_flags"], 1):
            sev = flag["severity"]
            cat = flag["category"].upper()
            tid = flag["target_id"]
            quote = flag["quote"]
            expl = flag["explanation"]
            reword = flag["suggested_rewording"]

            alert_type = "CAUTION" if sev == "HIGH" else ("WARNING" if sev == "MEDIUM" else "TIP")
            out.append(f"### #{idx}. [{sev}] {cat} pada Butir `{tid}`")
            out.append(f"> [!{alert_type}]")
            out.append(f"> **Kutipan Teks:** *\"{quote}\"*  ")
            out.append(f"> **Analisis Masalah:** {expl}  ")
            out.append(f"> **Saran Perbaikan:** {reword}")
            out.append("")

    out.append("---")
    out.append("")
    out.append("## 3. Rekomendasi Tindakan Pra-Bimbingan Dosen (*Actionable Advice*)")
    out.append("")
    if c["missing_count"] > 0:
        out.append(f"1. **Segera Selesaikan {c['missing_count']} Komentar Terlewat**: Reviewer jurnal sangat peka terhadap poin yang diabaikan. Lengkapi tanggapan untuk butir yang berstatus `MISSING`.")
    if c["high_risk_flags"] > 0:
        out.append("2. **Netralkan Nada Defensif**: Kalimat yang teridentifikasi konfrontatif wajib disesuaikan dengan pola *Acknowledge $\to$ Validate $\to$ Evidence $\to$ Clarify*.")
    if c["medium_risk_flags"] > 0:
        out.append("3. **Lengkapi Bukti Locator Naskah**: Pastikan setiap pernyataan perbaikan merujuk ke nomor bab, sub-bab, nomor halaman, atau nomor blok jangkar naskah (`B0042`).")
    out.append("4. **Konsultasikan Penolakan dengan Dosen Pembimbing**: Pastikan butir yang berstatus `REVIEWER_DISAGREE` atau `DELIBERATE_LIMITATION` telah disetujui oleh dosen sebelum diunggah.")
    out.append("")

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--comments", type=Path, required=True, help="Path to reviewer comments file")
    parser.add_argument("--rebuttal", type=Path, required=True, help="Path to rebuttal draft file")
    parser.add_argument(
        "--output-report",
        type=Path,
        default=None,
        help="Path for markdown QA report (default: 11_rebuttal_audit_report.md in rebuttal directory)",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path for structured JSON audit output",
    )
    args = parser.parse_args(argv)

    if not args.comments.exists():
        print(f"ERROR: Reviewer comments file not found: {args.comments}", file=sys.stderr)
        return 2

    if not args.rebuttal.exists():
        print(f"ERROR: Rebuttal draft file not found: {args.rebuttal}", file=sys.stderr)
        return 2

    comments_text = args.comments.read_text(encoding="utf-8")
    rebuttal_text = args.rebuttal.read_text(encoding="utf-8")

    if not comments_text.strip():
        print("ERROR: Reviewer comments file is empty.", file=sys.stderr)
        return 2

    if not rebuttal_text.strip():
        print("ERROR: Rebuttal draft file is empty.", file=sys.stderr)
        return 2

    audit_data = audit_rebuttal(comments_text, rebuttal_text)
    md_report = generate_markdown_report(audit_data)

    out_path = args.output_report or (args.rebuttal.parent / "11_rebuttal_audit_report.md")
    out_path.write_text(md_report, encoding="utf-8")

    if args.json_out:
        args.json_out.write_text(json.dumps(audit_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    c = audit_data["counters"]
    print(
        f"rebuttal-audit ok: {c['addressed_count']}/{c['total_comments']} comments addressed "
        f"({c['coverage_ratio']*100:.1f}%), {c['high_risk_flags']} high risk flags -> report {out_path}"
    )

    return 0 if audit_data["verdict"] != "ACTION_REQUIRED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
