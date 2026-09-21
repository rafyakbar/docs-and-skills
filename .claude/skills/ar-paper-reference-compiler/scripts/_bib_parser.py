#!/usr/bin/env python3
"""Multi-format bibliographic parser for .bib (BibTeX), .ris (RIS), and .nbib (PubMed).

Extracts raw metadata into a Canonical Reference Object (dict) for downstream
style formatting. Pure Python standard library implementation.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def clean_latex(text: str) -> str:
    """Clean LaTeX markup, braces, and accent codes into normal UTF-8 text."""
    if not text:
        return ""
    res = text.strip()
    # Handle LaTeX accent macros safely using lambdas
    res = re.sub(r'\{\\"([a-zA-Z])\}|\\"([a-zA-Z])', lambda m: (m.group(1) or m.group(2)) + "\u0308", res)
    res = re.sub(r"\{\\'([a-zA-Z])\}|\\'([a-zA-Z])", lambda m: (m.group(1) or m.group(2)) + "\u0301", res)
    res = re.sub(r'\{\\^([a-zA-Z])\}|\\^([a-zA-Z])', lambda m: (m.group(1) or m.group(2)) + "\u0302", res)
    res = re.sub(r'\{\\`([a-zA-Z])\}|\\`([a-zA-Z])', lambda m: (m.group(1) or m.group(2)) + "\u0300", res)
    res = re.sub(r'\{\\~([a-zA-Z])\}|\\~([a-zA-Z])', lambda m: (m.group(1) or m.group(2)) + "\u0303", res)
    res = re.sub(r'\{\\c\{([a-zA-Z])\}\}|\\c\{([a-zA-Z])\}', lambda m: (m.group(1) or m.group(2)) + "\u0327", res)
    res = re.sub(r'\{\\v\{([a-zA-Z])\}\}|\\v\{([a-zA-Z])\}', lambda m: (m.group(1) or m.group(2)) + "\u030C", res)
    res = res.replace(r"\AA", "Å").replace(r"\aa", "å").replace(r"\ss", "ß")
    res = res.replace("---", "-").replace("--", "-")
    res = res.replace("{", "").replace("}", "")
    return " ".join(res.split())


def parse_author_name(raw_name: str) -> dict[str, str]:
    """Parse a single author name string into {"first": ..., "last": ...}."""
    name = clean_latex(raw_name).strip()
    if not name:
        return {"first": "", "last": ""}

    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        last = parts[0]
        first = parts[1] if len(parts) > 1 else ""
    else:
        parts = name.split()
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

    field_pattern = re.compile(r'([a-zA-Z_]+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|([0-9]+))', re.DOTALL)
    fields = {}
    for m in field_pattern.finditer(content):
        k = m.group(1).lower()
        val = m.group(2) or m.group(3) or m.group(4) or ""
        fields[k] = clean_latex(val)

    if "author" in fields:
        raw_authors = fields["author"].split(" and ")
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
        elif tag in ("PY", "Y1") and not ref["year"]:
            y_match = re.search(r"\b(19|20)\d{2}\b", val)
            if y_match:
                ref["year"] = int(y_match.group(0))
        elif tag == "DA" and not ref["year"]:
            y_match = re.search(r"\b(19|20)\d{2}\b", val)
            if y_match:
                ref["year"] = int(y_match.group(0))
            m_month = re.search(r"/0?([1-9]|1[0-2])/", val)
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
