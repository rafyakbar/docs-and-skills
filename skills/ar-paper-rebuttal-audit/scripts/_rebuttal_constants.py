"""Constants, lexicons, and evaluation rubrics for ar-paper-rebuttal-audit.

Normative source: ARS academic-paper `rebuttal-audit` mode.
Audits author's response-to-reviewers letter against reviewer comments.
Pure Python Standard Library only (zero external dependencies).
"""
from __future__ import annotations

import re

# Format and toolchain versions
AUDIT_REPORT_FORMAT_VERSION = "1.0"

# Regex patterns for parsing reviewer comments in various formats
REVIEWER_HEADER_RE = re.compile(
    r"^(?:#{1,4}\s*)?(?:Reviewer\s*#?(\d+|[A-Za-z]+)\s*$|Reviewer\s*#?(\d+)\b|Editor(?:-in-Chief)?\s*$|Devil's\s*Advocate|DA\b)",
    re.IGNORECASE,
)

COMMENT_DELIMITER_RE = re.compile(
    r"^(?:#{1,5}\s*)?(?:(?:Comment|Point|Issue|Item|REV\b|Q\b|Question)\s*#?([A-Za-z0-9_.-]+)|"
    r"([A-Z]\d+|(?:R\d+[-._])[A-Za-z0-9]+|[0-9]+[.)]))(?:\s*\(([^)]+)\))?\s*[:\-–]?\s*",
    re.IGNORECASE,
)

DOC_HEADER_SKIP_RE = re.compile(
    r"^(?:#{1,3}\s*)?(?:Reviewer\s+Comments|Reviewer\s+Report|Editorial\s+Decision|Manuscript\b|Title\b|Author\b)",
    re.IGNORECASE,
)

RESPONSE_DELIMITER_RE = re.compile(
    r"^(?:#{1,5}\s*)?(?:Response(?:\s*to\s*(?:Reviewer\s*\d+|Comment\s*#?[A-Za-z0-9_.-]+))?|"
    r"Author(?:'s)?\s*Response|Changes\s*Made|Status)\b",
    re.IGNORECASE,
)

BLOCK_ID_LOCATOR_RE = re.compile(r"\b(B\d{4,})\b")
PAGE_LINE_LOCATOR_RE = re.compile(
    r"\b(?:(?:page|p\.|pp\.)\s*\d+(?:-\d+)?|(?:line|lines|l\.|ll\.)\s*\d+(?:-\d+)?|"
    r"(?:section|sec\.|§)\s*\d+(?:\.\d+)*|(?:table|figure|fig\.)\s*\d+[a-z]?)\b",
    re.IGNORECASE,
)

# 1. Combative / Defensive / Hostile Tone Lexicon
COMBATIVE_PATTERNS: list[tuple[str, re.Pattern]] = [
    (
        "reviewer_misunderstood",
        re.compile(
            r"\b(?:the\s+reviewer\s+(?:completely\s+)?misunderstood|"
            r"reviewer\s+(?:clearly\s+)?missed\s+the\s+point|"
            r"the\s+reviewer\s+failed\s+to\s+(?:understand|grasp|read))\b",
            re.IGNORECASE,
        ),
    ),
    (
        "reviewer_wrong",
        re.compile(
            r"\b(?:the\s+reviewer\s+is\s+(?:completely\s+)?(?:wrong|incorrect|mistaken)|"
            r"this\s+(?:claim|criticism|comment)\s+is\s+(?:plainly\s+)?(?:false|wrong|untrue))\b",
            re.IGNORECASE,
        ),
    ),
    (
        "condescending_dismissive",
        re.compile(
            r"\b(?:as\s+(?:any\s+)?expert\s+(?:in\s+the\s+field\s+)?knows|"
            r"it\s+(?:is|should\s+be)\s+(?:completely\s+)?obvious\s+that|"
            r"as\s+(?:is\s+)?well[\s-]known\s+to\s+researchers|"
            r"common\s+knowledge\s+in\s+our\s+field)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "pejorative_commentary",
        re.compile(
            r"\b(?:absurd|ridiculous|bizarre|unreasonable\s+demand|pedantic|"
            r"waste\s+of\s+time|trivial\s+complaint|meaningless\s+critique)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "blunt_refusal",
        re.compile(
            r"\b(?:we\s+(?:simply\s+)?refuse\s+to|"
            r"we\s+will\s+not\s+(?:do|perform|add|test)\s+this|"
            r"we\s+decline\s+to\s+address\s+this)\b",
            re.IGNORECASE,
        ),
    ),
]

# 2. Evasive / Vague / Non-Committal Lexicon
EVASIVE_PATTERNS: list[tuple[str, re.Pattern]] = [
    (
        "vague_addressed",
        re.compile(
            r"^(?:we\s+have\s+)?(?:addressed|fixed|corrected|resolved|updated)\s+"
            r"(?:this|as\s+suggested|accordingly|as\s+requested)[.!]?\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        "vague_clarified",
        re.compile(
            r"^(?:we\s+have\s+)?(?:clarified|improved|rewritten|expanded)\s+"
            r"(?:the\s+text|this|the\s+manuscript|in\s+the\s+paper)[.!]?\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        "taken_into_account",
        re.compile(
            r"\b(?:we\s+have\s+taken\s+this\s+(?:comment\s+)?into\s+(?:account|consideration)|"
            r"duly\s+noted\s+and\s+considered)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unsupported_future_work_escape",
        re.compile(
            r"^(?:this\s+is\s+left\s+for|we\s+defer\s+this\s+to)\s+future\s+work[.!]?\s*$",
            re.IGNORECASE,
        ),
    ),
]

# 3. Excessive Sycophancy Lexicon
SYCOPHANTIC_PATTERNS: list[tuple[str, re.Pattern]] = [
    (
        "excessive_gratitude",
        re.compile(
            r"\b(?:eternally\s+grateful|deeply\s+humbled\s+and\s+honored|"
            r"immense\s+and\s+boundless\s+gratitude|words\s+cannot\s+express\s+our\s+gratitude)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "adulatory_praise",
        re.compile(
            r"\b(?:reviewer(?:'s)?\s+(?:supreme|unrivaled|towering)\s+wisdom|"
            r"most\s+brilliant\s+and\s+insightful\s+reviewer|"
            r"genius\s+suggestion|profound\s+mastery\s+of\s+science)\b",
            re.IGNORECASE,
        ),
    ),
]

# Classification enums
COVERAGE_STATUSES = {
    "ADDRESSED": "Komentar telah dijawab secara utuh dengan tindakan konkret atau argumen kuat.",
    "PARTIALLY_ADDRESSED": "Hanya sebagian aspek komentar yang dijawab; ada poin/permintaan yang terlewat.",
    "MISSING": "Komentar tidak dijawab sama sekali dalam draf surat tanggapan (zero-orphan violation).",
    "UNRESOLVED_DISAGREEMENT": "Penulis menolak permintaan reviewer tanpa disertai dasar ilmiah/empiris yang memadai.",
}

RISK_SEVERITY = {
    "HIGH": "Pelanggaran serius yang dapat memicu penolakan editorial atau kemarahan reviewer (nada defensif, komplain diabaikan).",
    "MEDIUM": "Kelemahan substansial yang mengurangi kredibilitas (jawaban ambigu, klaim tanpa bukti locator naskah).",
    "LOW": "Kelemahan minor editorial atau nada pujian berlebihan (sycophancy) yang perlu diperbaiki.",
}

DISAGREEMENT_VALIDITY = {
    "SOUND_EMPIRICAL": "Penolakan didasarkan pada kendala data objektif, batas protokol etik (IRB), atau temuan empiris.",
    "SOUND_THEORETICAL": "Penolakan didasarkan pada konsensus literatur internasional yang dikutip secara sah.",
    "SOUND_SCOPE_LIMIT": "Penolakan didasarkan pada batasan ruang lingkup riset yang telah dinyatakan transparan di Limitations.",
    "UNJUSTIFIED_REFUSAL": "Penolakan sepihak tanpa bukti angka, sitasi, atau penjelasan rasional yang memadai.",
}
