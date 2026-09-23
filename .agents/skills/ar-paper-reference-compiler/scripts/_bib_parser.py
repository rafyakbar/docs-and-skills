#!/usr/bin/env python3
"""Multi-format bibliographic parser for .bib (BibTeX), .ris (RIS), and .nbib (PubMed).

Extracts raw metadata into a Canonical Reference Object (dict) for downstream
style formatting. Pure Python standard library implementation.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

_ACCENT_COMBINING = {
    '"': "\u0308",  # diaeresis / umlaut
    "'": "\u0301",  # acute
    "^": "\u0302",  # circumflex
    "`": "\u0300",  # grave
    "~": "\u0303",  # tilde
    "=": "\u0304",  # macron
    ".": "\u0307",  # dot above
    "H": "\u030B",  # double acute / hungarumlaut
    "v": "\u030C",  # caron / hacek
    "u": "\u0306",  # breve
    "c": "\u0327",  # cedilla
    "d": "\u0323",  # dot below
    "b": "\u0331",  # bar below
    "r": "\u030A",  # ring above
    "k": "\u0328",  # ogonek
}

_SPECIAL_LATEX_COMMANDS = [
    (re.compile(r"\{\\AA\}|\\AA(?![a-zA-Z])(?:\{\})?"), "Å"),
    (re.compile(r"\{\\aa\}|\\aa(?![a-zA-Z])(?:\{\})?"), "å"),
    (re.compile(r"\{\\AE\}|\\AE(?![a-zA-Z])(?:\{\})?"), "Æ"),
    (re.compile(r"\{\\ae\}|\\ae(?![a-zA-Z])(?:\{\})?"), "æ"),
    (re.compile(r"\{\\OE\}|\\OE(?![a-zA-Z])(?:\{\})?"), "Œ"),
    (re.compile(r"\{\\oe\}|\\oe(?![a-zA-Z])(?:\{\})?"), "œ"),
    (re.compile(r"\{\\O\}|\\O(?![a-zA-Z])(?:\{\})?"), "Ø"),
    (re.compile(r"\{\\o\}|\\o(?![a-zA-Z])(?:\{\})?"), "ø"),
    (re.compile(r"\{\\L\}|\\L(?![a-zA-Z])(?:\{\})?"), "Ł"),
    (re.compile(r"\{\\l\}|\\l(?![a-zA-Z])(?:\{\})?"), "ł"),
    (re.compile(r"\{\\ss\}|\\ss(?![a-zA-Z])(?:\{\})?"), "ß"),
    (re.compile(r"\{\\SS\}|\\SS(?![a-zA-Z])(?:\{\})?"), "SS"),
    (re.compile(r"\{\\i\}|\\i(?![a-zA-Z])(?:\{\})?"), "i"),
    (re.compile(r"\{\\j\}|\\j(?![a-zA-Z])(?:\{\})?"), "j"),
]

_INSTITUTIONAL_KEYWORDS = re.compile(
    r"\b("
    r"organization|organisation|association|committee|institute|institution|"
    r"department|ministry|agency|council|commission|center|centre|"
    r"consortium|collaboration|team|society|foundation|bureau|corporation|"
    r"administration|group|working\s+group|task\s+force|university|college|academy|"
    r"national\s+institute|world\s+health|nist|ieee|acm|who"
    r")\b",
    re.IGNORECASE,
)


def clean_latex(text: str) -> str:
    """Clean LaTeX markup, braces, and accent codes into normal UTF-8 text."""
    if not text:
        return ""
    res = text.strip()

    # 1. LaTeX accent macros: handles {\"a}, \"{a}, \"a, {\c{c}}, \c{c}, \v{s}, etc.
    accent_regex = re.compile(
        r'\{\\([\"\'^`~=.Hvucdbrk])\{?([a-zA-Z])\}?\}'
        r'|\\([\"\'^`~=.Hvucdbrk])\{([a-zA-Z])\}'
        r'|\\([\"\'^`~=.])([a-zA-Z])'
        r'|\\([Hvucdbrk])\s+([a-zA-Z])'
    )

    def _accent_sub(m: re.Match) -> str:
        acc = m.group(1) or m.group(3) or m.group(5) or m.group(7)
        char = m.group(2) or m.group(4) or m.group(6) or m.group(8)
        comb = _ACCENT_COMBINING.get(acc, "")
        return char + comb

    res = accent_regex.sub(_accent_sub, res)

    # 2. Special LaTeX commands
    for pattern, repl in _SPECIAL_LATEX_COMMANDS:
        res = pattern.sub(repl, res)

    # 3. Formatting macros and escapes
    res = re.sub(r'\\(?:textbf|textit|emph|textrm|textsc|text)\{([^{}]*)\}', r'\1', res)
    res = re.sub(r'\\([&%$#_{}])', r'\1', res)
    res = res.replace(r"\textendash", "–").replace(r"\textemdash", "—")
    res = res.replace("---", "—").replace("--", "–")
    res = res.replace("{", "").replace("}", "")

    # 4. Normalize combining characters to single NFC Unicode codepoints
    res = unicodedata.normalize("NFC", res)
    return " ".join(res.split())


def parse_author_name(raw_name: str) -> dict[str, str]:
    """Parse a single author name string into {"first": ..., "last": ...}."""
    raw_stripped = raw_name.strip()
    if not raw_stripped:
        return {"first": "", "last": ""}

    # 1. Check for corporate author via enclosing braces: {{World Health Organization}} or {IBM}
    is_braced_corp = (
        (raw_stripped.startswith("{{") and raw_stripped.endswith("}}"))
        or (raw_stripped.startswith("{") and raw_stripped.endswith("}"))
    )

    cleaned = clean_latex(raw_name).strip()
    if not cleaned:
        return {"first": "", "last": ""}

    # 2. Check for institutional / corporate keywords
    is_keyword_corp = bool(_INSTITUTIONAL_KEYWORDS.search(cleaned))

    if is_braced_corp or is_keyword_corp:
        clean_corp = cleaned.strip("{}").strip()
        return {"first": "", "last": clean_corp}

    if "," in cleaned:
        parts = [p.strip() for p in cleaned.split(",", 1)]
        last = parts[0]
        first = parts[1] if len(parts) > 1 else ""
    else:
        parts = cleaned.split()
        if len(parts) == 1:
            last = parts[0]
            first = ""
        else:
            last = parts[-1]
            first = " ".join(parts[:-1])

    return {"first": first, "last": last}


def format_initials(first_name: str) -> str:
    """Convert 'Mayank Kumar' or 'M. K.' into standardized initials 'M. K.'."""
    if not first_name:
        return ""
    cleaned = first_name.replace(".", " ").strip()
    tokens = [t for t in cleaned.split() if t]
    initials = [f"{t[0].upper()}." for t in tokens]
    return " ".join(initials)


def parse_bibtex_content(content: str) -> dict[str, Any]:
    """Parse BibTeX string into a canonical reference dict."""
    ref: dict[str, Any] = {
        "entry_type": "journal",
        "authors": [],
        "title": "",
        "container": "",
        "year": None,
        "month": None,
        "volume": None,
        "issue": None,
        "pages": None,
        "article_number": None,
        "doi": None,
        "url": None,
        "publisher": None,
    }

    type_match = re.search(r"@([a-zA-Z]+)\s*\{", content)
    if type_match:
        raw_type = type_match.group(1).lower()
        if raw_type in ("inproceedings", "conference"):
            ref["entry_type"] = "conference"
        elif raw_type in ("book", "incollection"):
            ref["entry_type"] = "book"
        elif raw_type in ("techreport", "report"):
            ref["entry_type"] = "report"
        elif raw_type in ("misc", "online"):
            ref["entry_type"] = "online"
        else:
            ref["entry_type"] = "journal"

    field_pattern = re.compile(
        r'([a-zA-Z_]+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|([a-zA-Z0-9_.-]+))',
        re.DOTALL,
    )
    fields = {}
    raw_fields = {}
    for m in field_pattern.finditer(content):
        k = m.group(1).lower()
        val = m.group(2) or m.group(3) or m.group(4) or ""
        raw_fields[k] = val
        fields[k] = clean_latex(val)

    if "author" in raw_fields:
        raw_authors = raw_fields["author"].split(" and ")
        ref["authors"] = [parse_author_name(a) for a in raw_authors if a.strip()]

    ref["title"] = fields.get("title", "")
    ref["container"] = fields.get("journal") or fields.get("booktitle") or fields.get("series") or ""

    if "year" in fields:
        y_match = re.search(r"\b(19|20)\d{2}\b", fields["year"])
        if y_match:
            ref["year"] = int(y_match.group(0))

    ref["month"] = fields.get("month") or None
    ref["volume"] = fields.get("volume") or None
    ref["issue"] = fields.get("number") or None
    ref["pages"] = fields.get("pages") or None
    ref["article_number"] = fields.get("eid") or fields.get("art_no") or None
    ref["doi"] = fields.get("doi") or None
    ref["url"] = fields.get("url") or None
    ref["publisher"] = fields.get("publisher") or None

    return ref


def parse_ris_content(content: str) -> dict[str, Any]:
    """Parse RIS string into a canonical reference dict."""
    ref: dict[str, Any] = {
        "entry_type": "journal",
        "authors": [],
        "title": "",
        "container": "",
        "year": None,
        "month": None,
        "volume": None,
        "issue": None,
        "pages": None,
        "article_number": None,
        "doi": None,
        "url": None,
        "publisher": None,
    }

    start_page = None
    end_page = None

    for line in content.splitlines():
        line = line.strip()
        m = re.match(r"^([A-Z0-9]{2})\s*-\s*(.*)$", line)
        if not m:
            continue
        tag = m.group(1).upper()
        val = clean_latex(m.group(2))

        if tag == "TY":
            val_upper = val.upper()
            if val_upper in ("CONF", "CPAPER"):
                ref["entry_type"] = "conference"
            elif val_upper in ("BOOK", "CHAP"):
                ref["entry_type"] = "book"
            elif val_upper in ("ELEC", "WEBP"):
                ref["entry_type"] = "online"
            else:
                ref["entry_type"] = "journal"
        elif tag in ("AU", "A1"):
            ref["authors"].append(parse_author_name(val))
        elif tag in ("TI", "T1") and not ref["title"]:
            ref["title"] = val
        elif tag in ("JO", "JF", "T2", "JA") and not ref["container"]:
            ref["container"] = val
        elif tag in ("PY", "Y1"):
            if not ref["year"]:
                y_match = re.search(r"\b(19|20)\d{2}\b", val)
                if y_match:
                    ref["year"] = int(y_match.group(0))
            if not ref["month"]:
                m_name = re.search(
                    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b",
                    val,
                    re.IGNORECASE,
                )
                if m_name:
                    ref["month"] = m_name.group(1)
                else:
                    m_month = re.search(r"(?:(?:19|20)\d{2}[/-]|/)0?([1-9]|1[0-2])\b", val)
                    if m_month:
                        ref["month"] = m_month.group(1)
        elif tag == "DA":
            if not ref["year"]:
                y_match = re.search(r"\b(19|20)\d{2}\b", val)
                if y_match:
                    ref["year"] = int(y_match.group(0))
            if not ref["month"]:
                m_name = re.search(
                    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b",
                    val,
                    re.IGNORECASE,
                )
                if m_name:
                    ref["month"] = m_name.group(1)
                else:
                    m_month = re.search(r"(?:(?:19|20)\d{2}[/-]|/)0?([1-9]|1[0-2])\b", val)
                    if m_month:
                        ref["month"] = m_month.group(1)
        elif tag == "VL":
            ref["volume"] = val
        elif tag == "IS":
            ref["issue"] = val
        elif tag == "SP":
            start_page = val
        elif tag == "EP":
            end_page = val
        elif tag in ("DO", "M3"):
            d_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", val)
            if d_match:
                ref["doi"] = d_match.group(0)
        elif tag == "UR":
            ref["url"] = val
        elif tag == "PB":
            ref["publisher"] = val

    if start_page and end_page:
        ref["pages"] = f"{start_page}-{end_page}"
    elif start_page:
        ref["pages"] = start_page

    return ref


def parse_nbib_content(content: str) -> dict[str, Any]:
    """Parse PubMed NBIB string into a canonical reference dict."""
    ref: dict[str, Any] = {
        "entry_type": "journal",
        "authors": [],
        "title": "",
        "container": "",
        "year": None,
        "month": None,
        "volume": None,
        "issue": None,
        "pages": None,
        "article_number": None,
        "doi": None,
        "url": None,
        "publisher": None,
    }

    au_fallback = []

    for line in content.splitlines():
        line = line.strip()
        m = re.match(r"^([A-Z]{2,4})\s*-\s*(.*)$", line)
        if not m:
            continue
        tag = m.group(1).upper()
        val = clean_latex(m.group(2))

        if tag == "FAU":
            ref["authors"].append(parse_author_name(val))
        elif tag == "AU":
            au_fallback.append(parse_author_name(val))
        elif tag == "TI":
            ref["title"] = val.rstrip(".")
        elif tag in ("JT", "TA") and not ref["container"]:
            ref["container"] = val
        elif tag == "DP":
            y_match = re.search(r"\b(19|20)\d{2}\b", val)
            if y_match:
                ref["year"] = int(y_match.group(0))
            m_match = re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", val, re.IGNORECASE)
            if m_match:
                ref["month"] = m_match.group(0).capitalize()
        elif tag == "VI":
            ref["volume"] = val
        elif tag == "IP":
            ref["issue"] = val
        elif tag == "PG":
            ref["pages"] = val
        elif tag in ("LID", "AID"):
            if "[doi]" in val:
                d_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", val)
                if d_match:
                    ref["doi"] = d_match.group(0)

    if not ref["authors"] and au_fallback:
        ref["authors"] = au_fallback

    return ref


def parse_reference_file(file_path: Path | str) -> dict[str, Any]:
    """Parse any .bib, .ris, or .nbib file automatically by extension."""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"Reference file not found: {p}")

    content = p.read_text(encoding="utf-8", errors="replace")
    ext = p.suffix.lower()

    if ext in (".bib", ".bibtex"):
        ref = parse_bibtex_content(content)
    elif ext == ".ris":
        ref = parse_ris_content(content)
    elif ext in (".nbib", ".medline"):
        ref = parse_nbib_content(content)
    else:
        if "@" in content and "{" in content:
            ref = parse_bibtex_content(content)
        elif "TY  - " in content:
            ref = parse_ris_content(content)
        else:
            ref = parse_nbib_content(content)

    ref["source_file"] = str(p).replace("\\", "/")
    return ref


__all__ = [
    "clean_latex",
    "parse_author_name",
    "format_initials",
    "parse_bibtex_content",
    "parse_ris_content",
    "parse_nbib_content",
    "parse_reference_file",
]
