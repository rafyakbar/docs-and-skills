#!/usr/bin/env python3
"""ARS Rebuttal Auditor — Advisory QA for Response to Reviewers.

Normative source: ARS academic-paper `rebuttal-audit` mode.
Evaluates an author's existing rebuttal / response-to-reviewers draft against
the original reviewer comments across 4 dimensions:
  1. D1 Tone & Academic Diplomacy (anti-defensive, anti-sycophancy, non-hostile) [25%]
  2. D2 Completeness / Zero-Orphan Coverage (every comment accounted for, no dropped concerns) [35%]
  3. D3 Verifiability & Block Mapping (section, page, table, figure, block IDs) [20%]
  4. D4 Coherence & Claim Preservation (scientifically sound rationale, claim preservation) [20%]

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
    DIMENSION_SPECS,
    DOC_HEADER_SKIP_RE,
    EVASIVE_PATTERNS,
    PAGE_LINE_LOCATOR_RE,
    READINESS_VERDICTS,
    RESPONSE_DELIMITER_RE,
    REVIEWER_HEADER_RE,
    SYCOPHANTIC_PATTERNS,
    VERDICT_BADGES,
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


def clean_author_response(text: str) -> str:
    """Clean out reviewer comment quotes, headers, status tags, and blockquotes,
    leaving purely the author's own response text for accurate word count and audit."""
    # 1. If explicit response marker exists, extract text following it
    resp_match = re.search(
        r"(?:#{1,5}\s*)?(?:\*\*)?(?:Author(?:'s)?\s*Response|Response)(?:\*\*)?\s*[:\-–]?\s*(?:\*\*)?\s*",
        text,
        re.IGNORECASE,
    )
    if resp_match:
        body = text[resp_match.end():].strip()
        cleaned_lines = []
        for line in body.splitlines():
            s = line.strip()
            if re.match(r"^(?:\*\*)?Status(?:\*\*)?\s*[:\-–]?", s, re.IGNORECASE):
                continue
            cleaned_lines.append(line)
        res = "\n".join(cleaned_lines).strip()
        if res:
            return res

    # 2. Line-by-line filtering if no explicit response marker
    lines = []
    in_quote_block = False
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith(">"):
            continue
        if re.match(r"^(?:\*\*)?Status(?:\*\*)?\s*[:\-–]?", s, re.IGNORECASE):
            continue
        if re.match(
            r"^(?:\*\*)?(?:Reviewer(?:\s*Comment)?|Comment|Point|Issue|Question|Q)(?:\*\*)?\s*[:\-–]?",
            s,
            re.IGNORECASE,
        ):
            if s.count('"') % 2 == 1 or s.count('“') != s.count('”'):
                in_quote_block = True
            continue
        if in_quote_block:
            if '"' in s or '”' in s:
                in_quote_block = False
            continue
        lines.append(line)

    res = "\n".join(lines).strip()
    return res if res else text.strip()


def parse_rebuttal_draft(text: str) -> list[ResponseEntry]:
    """Parse author's response letter into discrete response entries."""
    sections = re.split(r"\n(?=#{1,4}\s+(?:REV|Comment|Point|Item|R\d+|Response\s+to\s+Reviewer|[0-9]+[.)]))", text)
    entries: list[ResponseEntry] = []
    entry_counter = 1

    for sec in sections:
        sec_str = sec.strip()
        if not sec_str or len(sec_str.split()) < 5:
            continue

        # Skip document-level header (e.g. "# Response to Reviewers — Round 1")
        if re.match(r"^(?:#{1,3}\s*)?(?:Point-by-Point\s+)?Response\s+to\s+Reviewers\b", sec_str, re.IGNORECASE) and not re.search(
            r"\b(REV-\d+|C\d+|R\d+[-_]?[A-Za-z0-9]+|Comment\s*\d+)\b", sec_str, re.IGNORECASE
        ):
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
            parts = re.split(r"(?:\*\*)?\s*(?:Changes\s*Made|Changes)(?:\*\*)?\s*[:\-–]?\s*(?:\*\*)?\s*", sec_str, flags=re.IGNORECASE)
            author_resp = parts[0]
            changes_made = parts[1] if len(parts) > 1 else ""

        # Clean author response so word count and tone audit accurately target pure author response
        pure_author_resp = clean_author_response(author_resp)

        entries.append(
            ResponseEntry(
                entry_id=entry_id,
                matched_comment_id=entry_id,
                raw_text=sec_str,
                author_response=pure_author_resp,
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

            # Audit tone on author's actual words
            author_text = f"{matched_resp.author_response}\n{matched_resp.changes_made}".strip()
            tone_flags = audit_tone(author_text, comm.comment_id)
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
                word_count = len(matched_resp.author_response.split())
                if word_count < 30:
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
            has_unjustified = any(f.category == "unjustified_refusal" for f in item_flags)
            has_combative = any(f.category == "combative" for f in item_flags)
            has_evasive = any(f.category == "evasive" for f in item_flags)
            word_count = len(matched_resp.author_response.split())

            if has_high_flag and has_unjustified:
                coverage_status = "UNRESOLVED_DISAGREEMENT"
                partially_count += 1
            elif has_combative:
                coverage_status = "UNRESOLVED_TONE_CONFLICT"
                partially_count += 1
            elif has_high_flag:
                coverage_status = "PARTIALLY_ADDRESSED"
                partially_count += 1
            elif word_count < 20 or has_evasive:
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

    # 4 Dimension Scores (0-100 scale)
    # D1: Tone & Academic Diplomacy (Weight: 0.25)
    combative_count = sum(1 for f in all_flags if f.category == "combative")
    evasive_count = sum(1 for f in all_flags if f.category == "evasive")
    sycophantic_count = sum(1 for f in all_flags if f.category == "sycophantic")
    s_d1 = max(0.0, 100.0 - (combative_count * 30.0 + evasive_count * 15.0 + sycophantic_count * 5.0))

    # D2: Completeness / Zero-Orphan Coverage (Weight: 0.35)
    if total_comments == 0:
        s_d2 = 100.0
    else:
        raw_d2 = ((addressed_count + 0.5 * partially_count) / total_comments) * 100.0
        s_d2 = max(0.0, min(100.0, raw_d2 - (25.0 * missing_count)))

    # D3: Verifiability & Block Mapping (Weight: 0.20)
    non_missing_count = total_comments - missing_count
    if non_missing_count <= 0:
        s_d3 = 0.0
        locator_ratio = 0.0
    else:
        grounded_count = sum(
            1 for it in item_results
            if it.locators_found or (it.coverage_status != "MISSING" and "acknowledg" in it.response_snippet.lower())
        )
        locator_ratio = grounded_count / non_missing_count
        s_d3 = round(locator_ratio * 100.0, 1)

    # D4: Coherence & Claim Preservation (Weight: 0.20)
    unjustified_count = sum(1 for f in all_flags if f.category == "unjustified_refusal")
    future_work_escape_count = sum(1 for f in all_flags if f.category == "unsupported_future_work_escape")
    s_d4 = max(0.0, min(100.0, 100.0 - (unjustified_count * 40.0 + future_work_escape_count * 20.0)))

    # Composite Score: (D1 * 0.25) + (D2 * 0.35) + (D3 * 0.20) + (D4 * 0.20)
    composite_score = round(
        (s_d1 * 0.25) + (s_d2 * 0.35) + (s_d3 * 0.20) + (s_d4 * 0.20),
        1,
    )

    # 4-Tier Verdict Assignment:
    # 1. PASSED_READINESS: Skor >= 80, 0 High Risk, 100% Coverage, Locators >= 80%
    if (
        composite_score >= 80.0
        and high_risk_count == 0
        and missing_count == 0
        and coverage_ratio >= 1.0
        and locator_ratio >= 0.80
    ):
        verdict = "PASSED_READINESS"
        verdict_badge = VERDICT_BADGES["PASSED_READINESS"]

    # 2. CONDITIONAL_REVISION: Skor 65–79, 0 High Risk, 100% Coverage
    elif (
        composite_score >= 65.0
        and high_risk_count == 0
        and missing_count == 0
        and coverage_ratio >= 1.0
    ):
        verdict = "CONDITIONAL_REVISION"
        verdict_badge = VERDICT_BADGES["CONDITIONAL_REVISION"]

    # 4. REJECTED_UNPREPARED: Skor < 50, atau banyak bendera nada agresif/combative
    elif composite_score < 50.0 or combative_count >= 2 or (combative_count > 0 and composite_score < 65.0):
        verdict = "REJECTED_UNPREPARED"
        verdict_badge = VERDICT_BADGES["REJECTED_UNPREPARED"]

    # 3. REVISE_AND_RESUBMIT: Skor 50–64, atau ada item belum terjawab/penolakan tak berdasar
    else:
        verdict = "REVISE_AND_RESUBMIT"
        verdict_badge = VERDICT_BADGES["REVISE_AND_RESUBMIT"]

    return {
        "report_format_version": AUDIT_REPORT_FORMAT_VERSION,
        "mode": "rebuttal-audit",
        "composite_score": composite_score,
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "dimension_scores": {
            "D1_tone_and_diplomacy": round(s_d1, 1),
            "D2_zero_orphan_coverage": round(s_d2, 1),
            "D3_verifiability_and_locators": round(s_d3, 1),
            "D4_coherence_and_claim_preservation": round(s_d4, 1),
        },
        "counters": {
            "total_comments": total_comments,
            "addressed_count": addressed_count,
            "partially_count": partially_count,
            "missing_count": missing_count,
            "coverage_ratio": round(coverage_ratio, 4),
            "locator_ratio": round(locator_ratio, 4),
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
    score = audit_data["composite_score"]
    dims = audit_data["dimension_scores"]

    out = []
    out.append("# Laporan Audit Penjaminan Mutu Surat Tanggapan Reviewer (Rebuttal QA Report)")
    out.append("")
    out.append(f"**Skor Kesiapan:** `{score:.1f}/100`  ")
    out.append(f"**Status Evaluasi:** `{badge}`  ")
    out.append(f"**Rasio Cakupan Komentar (*Coverage Ratio*):** `{c['coverage_ratio'] * 100:.1f}%` ({c['addressed_count']}/{c['total_comments']} komentar terjawab tuntas)  ")
    out.append(f"**Rasio Lokator Naskah (*Locator Grounding*):** `{c['locator_ratio'] * 100:.1f}%`  ")
    out.append(f"**Indikator Risiko (*Risk Flags*):** `{c['high_risk_flags']} Tinggi (High)` · `{c['medium_risk_flags']} Sedang (Medium)` · `{c['low_risk_flags']} Rendah (Low)`")
    out.append("")
    out.append("### Skor 4 Dimensi Kualitas:")
    out.append(f"- **D1 Tone & Academic Diplomacy:** `{dims['D1_tone_and_diplomacy']:.1f}/100` (Bobot: 25%)")
    out.append(f"- **D2 Completeness / Zero-Orphan Coverage:** `{dims['D2_zero_orphan_coverage']:.1f}/100` (Bobot: 35%)")
    out.append(f"- **D3 Verifiability & Block Mapping:** `{dims['D3_verifiability_and_locators']:.1f}/100` (Bobot: 20%)")
    out.append(f"- **D4 Coherence & Claim Preservation:** `{dims['D4_coherence_and_claim_preservation']:.1f}/100` (Bobot: 20%)")
    out.append(f"- **Skor Komposit Akhir:** `{score:.1f}/100`")
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
        elif status == "UNRESOLVED_TONE_CONFLICT":
            status_str = "⚠️ Nada Defensif"
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
        out.append(r"2. **Netralkan Nada Defensif**: Kalimat yang teridentifikasi konfrontatif wajib disesuaikan dengan pola *Acknowledge $\to$ Validate $\to$ Evidence $\to$ Clarify*.")
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
        f"rebuttal-audit [{audit_data['verdict']}]: Skor {audit_data['composite_score']}/100 | "
        f"{c['addressed_count']}/{c['total_comments']} comments addressed "
        f"({c['coverage_ratio']*100:.1f}%), {c['high_risk_flags']} high risk flags -> report {out_path}"
    )

    return 0 if audit_data["verdict"] in ("PASSED_READINESS", "CONDITIONAL_REVISION") else 1


if __name__ == "__main__":
    raise SystemExit(main())

