#!/usr/bin/env python3
"""Multi-style citation formatter for IEEE, APA 7th, Harvard, ACM, and Vancouver.

Transforms Canonical Reference Objects into compliant publication-ready strings.
Pure Python standard library implementation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from _bib_parser import format_initials
except ImportError:
    from scripts._bib_parser import format_initials

# Acronyms and proper nouns protected from lowercase conversion in sentence case
_PROTECTED_ACRONYMS = {
    "AI", "CNN", "CNNs", "ViT", "ViTs", "PCA", "SVM", "SVMs", "MHSA",
    "ROC", "AUC", "BERT", "LLM", "LLMs", "GAN", "GANs", "ICCV", "CVPR",
    "ECCV", "IEEE", "ACM", "NLM", "GDPR", "COVID", "COVID-19", "MRI",
    "CT", "CT-Scan", "DNA", "RNA", "USA", "UK", "EU", "DemogPairs",
    "B-PETs", "RF", "GNB", "LR", "NLP", "ML", "DL",
    "ArcFace", "ResNet", "ResNets", "AlphaFold", "ChatGPT", "ImageNet",
    "FaceNet", "StyleGAN", "OpenAI", "LoRA", "BioBERT", "SciBERT", "PubMed",
    "NIST", "FRVT"
}

_MONTH_ABBRS = {
    "1": "Jan.", "01": "Jan.", "jan": "Jan.", "january": "Jan.",
    "2": "Feb.", "02": "Feb.", "feb": "Feb.", "february": "Feb.",
    "3": "Mar.", "03": "Mar.", "mar": "Mar.", "march": "Mar.",
    "4": "Apr.", "04": "Apr.", "apr": "Apr.", "april": "Apr.",
    "5": "May",  "05": "May",  "may": "May",
    "6": "June", "06": "June", "jun": "June", "june": "June",
    "7": "July", "07": "July", "jul": "July", "july": "July",
    "8": "Aug.", "08": "Aug.", "aug": "Aug.", "august": "Aug.",
    "9": "Sept.", "09": "Sept.", "sep": "Sept.", "sept": "Sept.", "september": "Sept.",
    "10": "Oct.", "oct": "Oct.", "october": "Oct.",
    "11": "Nov.", "nov": "Nov.", "november": "Nov.",
    "12": "Dec.", "dec": "Dec.", "december": "Dec.",
}


def format_sentence_case(title: str) -> str:
    """Transform title into Sentence case while protecting computing acronyms.

    Ensures titles starting with quotation marks, parentheses, or brackets have
    their first alphabetical character capitalized while preserving CamelCase
    and protected computing acronyms.
    """
    if not title:
        return ""
    title = title.strip().rstrip(".")
    words = title.split()
    if not words:
        return ""

    result = []
    capitalize_next = True

    for i, w in enumerate(words):
        # Extract leading punctuation, core word, and trailing punctuation
        m_lead = re.match(r"^[(\"'\u201c\u2018\u00ab\[\{]+", w)
        lead = m_lead.group(0) if m_lead else ""

        m_trail = re.search(r"[\"'),:;!?\u201d\u2019\u00bb\]\}]+$", w)
        trail = m_trail.group(0) if m_trail else ""

        if trail:
            core = w[len(lead) : len(w) - len(trail)]
        else:
            core = w[len(lead) :]

        if not core:
            result.append(w)
            continue

        clean_core = re.sub(r"[^a-zA-Z0-9_-]", "", core)

        if clean_core in _PROTECTED_ACRONYMS or core in _PROTECTED_ACRONYMS:
            formatted_core = core
        elif any(c.isupper() for c in core[1:]) and not core.isupper():
            # Mixed/CamelCase like ArcFace, ResNet, DemogPairs
            if capitalize_next or i == 0:
                formatted_core = core[0].upper() + core[1:]
            else:
                formatted_core = core
        elif capitalize_next or i == 0:
            formatted_core = core[0].upper() + core[1:].lower() if len(core) > 1 else core.upper()
        else:
            formatted_core = core.lower()

        result.append(lead + formatted_core + trail)
        capitalize_next = (
            w.endswith(":")
            or w.endswith("?")
            or w.endswith("!")
            or trail.endswith(":")
            or trail.endswith("?")
            or trail.endswith("!")
        )

    return " ".join(result)


def normalize_doi(doi: str | None) -> str | None:
    """Extract and normalize clean DOI string (10.xxxx/...)."""
    if not doi:
        return None
    d = doi.strip().rstrip(".")
    match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", d)
    return match.group(0) if match else d


def normalize_month(month: str | int | None) -> str | None:
    """Convert raw month string to standardized abbreviation."""
    if not month:
        return None
    clean = str(month).strip().lower()
    return _MONTH_ABBRS.get(clean, str(month).capitalize())


# ---------------------------------------------------------------------------
# IEEE Formatter
# ---------------------------------------------------------------------------

def format_authors_ieee(authors: list[dict[str, str]]) -> str:
    """Format authors list for IEEE style: J. A. Smith and B. C. Jones."""
    if not authors:
        return ""
    if len(authors) >= 6:
        # Rule: 6 or more authors -> first author et al.
        first = authors[0]
        init = format_initials(first.get("first", ""))
        last = first.get("last", "")
        lead = f"{init} {last}".strip() if init else last
        return f"{lead} et al."

    formatted = []
    for a in authors:
        init = format_initials(a.get("first", ""))
        last = a.get("last", "")
        name_str = f"{init} {last}".strip() if init else last
        formatted.append(name_str)

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]} and {formatted[1]}"
    else:
        return ", ".join(formatted[:-1]) + f", and {formatted[-1]}"


def format_ieee(ref: dict[str, Any], index: int) -> str:
    """Format a canonical reference dict into an IEEE markdown string with anchor."""
    authors = format_authors_ieee(ref.get("authors", []))
    title = format_sentence_case(ref.get("title", ""))
    container = ref.get("container", "").strip()
    year = ref.get("year")
    month = normalize_month(ref.get("month"))
    vol = ref.get("volume")
    issue = ref.get("issue")
    pages = ref.get("pages")
    art_no = ref.get("article_number")
    doi = normalize_doi(ref.get("doi"))
    url = ref.get("url")
    entry_type = ref.get("entry_type", "journal")

    parts = []
    if authors:
        parts.append(f"{authors},")
    if title:
        clean_title = title.strip()
        if clean_title.endswith(("?", "!")):
            parts.append(f'"{clean_title}"')
        else:
            clean_title = clean_title.rstrip(".,;:")
            parts.append(f'"{clean_title},"')

    if entry_type == "conference":
        if container:
            if not container.lower().startswith("in "):
                container = f"in *{container}*"
            else:
                container = f"*{container}*"
            parts.append(f"{container},")
        if pages:
            parts.append(f"pp. {pages},")
        date_str = f"{month} {year}" if month and year else str(year or "")
        if date_str:
            parts.append(f"{date_str},")
    elif entry_type == "book":
        if container:
            parts.append(f"in *{container}*,")
        if vol:
            parts.append(f"vol. {vol},")
        if pages:
            parts.append(f"pp. {pages},")
        if year:
            parts.append(f"{year},")
    elif entry_type == "online" or "arxiv" in (container.lower() + str(url).lower()):
        if year:
            parts.append(f"{year},")
        if "arxiv" in str(url).lower() or "arxiv" in container.lower():
            arxiv_id = ""
            if url:
                m = re.search(r"arxiv\.org/abs/([0-9]+\.[0-9]+)", url)
                if m:
                    arxiv_id = m.group(1)
            if arxiv_id:
                parts.append(f"arXiv:{arxiv_id}. [Online]. Available: https://arxiv.org/abs/{arxiv_id}")
            elif url:
                parts.append(f"[Online]. Available: {url}")
        elif url:
            parts.append(f"[Online]. Available: {url}")
    else:
        # Default journal article
        if container:
            parts.append(f"*{container}*,")
        if vol:
            parts.append(f"vol. {vol},")
        if issue:
            parts.append(f"no. {issue},")
        if art_no:
            parts.append(f"Art. no. {art_no},")
        elif pages:
            parts.append(f"pp. {pages},")
        date_str = f"{month} {year}" if month and year else str(year or "")
        if date_str:
            parts.append(f"{date_str},")

    if doi:
        parts.append(f"doi: {doi}.")
    elif url and not any("[Online]" in p for p in parts):
        parts.append(f"[Online]. Available: {url}.")

    ref_str = " ".join(parts).strip()
    if not ref_str.endswith("."):
        ref_str += "."

    return f'<a id="ref{index}"></a>\n[{index}] {ref_str}'


# ---------------------------------------------------------------------------
# APA 7th Formatter
# ---------------------------------------------------------------------------

def format_authors_apa7(authors: list[dict[str, str]]) -> str:
    """Format authors list for APA 7th style: Smith, J. A., & Jones, B. C."""
    if not authors:
        return ""
    formatted = []
    for a in authors:
        last = a.get("last", "")
        init = format_initials(a.get("first", ""))
        formatted.append(f"{last}, {init}".strip() if init else last)

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) <= 20:
        return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"
    else:
        # 21 or more authors: first 19, ellipsis, last author
        first_19 = ", ".join(formatted[:19])
        return f"{first_19}, ... {formatted[-1]}"


def format_apa7(ref: dict[str, Any], index: int) -> str:
    """Format a canonical reference dict into an APA 7th string with anchor."""
    authors = format_authors_apa7(ref.get("authors", []))
    title = format_sentence_case(ref.get("title", ""))
    container = ref.get("container", "").strip()
    year = ref.get("year", "n.d.")
    vol = ref.get("volume")
    issue = ref.get("issue")
    pages = ref.get("pages")
    art_no = ref.get("article_number")
    doi = normalize_doi(ref.get("doi"))
    url = ref.get("url")

    parts = []
    if authors:
        parts.append(f"{authors} ({year}).")
    else:
        parts.append(f"({year}).")

    if title:
        clean_title = title.strip()
        if clean_title.endswith(("?", "!")):
            parts.append(clean_title)
        else:
            clean_title = clean_title.rstrip(".,;:")
            parts.append(f"{clean_title}.")

    container_part = []
    if container:
        container_part.append(f"*{container}*")
        if vol:
            if issue:
                container_part.append(f", *{vol}*({issue})")
            else:
                container_part.append(f", *{vol}*")
        if art_no:
            container_part.append(f", Article {art_no}.")
        elif pages:
            container_part.append(f", {pages}.")
        else:
            container_part.append(".")
        parts.append("".join(container_part))

    if doi:
        parts.append(f"https://doi.org/{doi}")
    elif url:
        parts.append(url)

    ref_str = " ".join(parts).strip()
    return f'<a id="ref{index}"></a>\n{ref_str}'


# ---------------------------------------------------------------------------
# Harvard Formatter
# ---------------------------------------------------------------------------

def format_authors_harvard(authors: list[dict[str, str]]) -> str:
    """Format authors list for Harvard style: Smith, J.A. and Jones, B.C."""
    if not authors:
        return ""
    if len(authors) >= 4:
        first = authors[0]
        init = format_initials(first.get("first", "")).replace(" ", "")
        last = first.get("last", "")
        return f"{last}, {init} et al."

    formatted = []
    for a in authors:
        last = a.get("last", "")
        init = format_initials(a.get("first", "")).replace(" ", "")
        formatted.append(f"{last}, {init}".strip() if init else last)

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]} and {formatted[1]}"
    else:
        return ", ".join(formatted[:-1]) + f" and {formatted[-1]}"


def format_harvard(ref: dict[str, Any], index: int) -> str:
    """Format reference into Harvard citation style."""
    authors = format_authors_harvard(ref.get("authors", []))
    title = format_sentence_case(ref.get("title", ""))
    container = ref.get("container", "").strip()
    year = ref.get("year", "n.d.")
    vol = ref.get("volume")
    issue = ref.get("issue")
    pages = ref.get("pages")
    doi = normalize_doi(ref.get("doi"))

    parts = []
    if authors:
        parts.append(f"{authors}, {year}.")
    else:
        parts.append(f"{year}.")

    if title:
        clean_title = title.strip()
        if clean_title.endswith(("?", "!")):
            parts.append(f"'{clean_title}',")
        else:
            clean_title = clean_title.rstrip(".,;:")
            parts.append(f"'{clean_title}',")

    if container:
        parts.append(f"*{container}*,")
        vol_issue = ""
        if vol and issue:
            vol_issue = f"{vol}({issue})"
        elif vol:
            vol_issue = f"{vol}"
        if vol_issue:
            parts.append(f"{vol_issue},")
        if pages:
            parts.append(f"pp. {pages}.")

    if doi:
        parts.append(f"https://doi.org/{doi}.")

    ref_str = " ".join(parts).strip()
    return f'<a id="ref{index}"></a>\n{ref_str}'


# ---------------------------------------------------------------------------
# ACM Formatter
# ---------------------------------------------------------------------------

def format_authors_acm(authors: list[dict[str, str]]) -> str:
    """Format authors list for ACM style: First Last and First Last."""
    if not authors:
        return ""
    if len(authors) >= 3:
        first = authors[0]
        first_name = first.get("first", "")
        last_name = first.get("last", "")
        full = f"{first_name} {last_name}".strip()
        return f"{full} et al."

    formatted = []
    for a in authors:
        first_name = a.get("first", "")
        last_name = a.get("last", "")
        formatted.append(f"{first_name} {last_name}".strip())

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]} and {formatted[1]}"
    else:
        return ", ".join(formatted[:-1]) + f", and {formatted[-1]}"


def format_acm(ref: dict[str, Any], index: int) -> str:
    """Format reference into ACM citation style."""
    authors = format_authors_acm(ref.get("authors", []))
    title = ref.get("title", "").strip()
    container = ref.get("container", "").strip()
    year = ref.get("year", "n.d.")
    month = normalize_month(ref.get("month"))
    vol = ref.get("volume")
    issue = ref.get("issue")
    pages = ref.get("pages")
    doi = normalize_doi(ref.get("doi"))

    parts = []
    if authors:
        author_str = authors if authors.endswith(".") else f"{authors}."
        parts.append(f"{author_str} {year}.")
    else:
        parts.append(f"{year}.")

    if title:
        clean_title = title.strip()
        if clean_title.endswith(("?", "!")):
            parts.append(f'"{clean_title}"')
        else:
            clean_title = clean_title.rstrip(".,;:")
            parts.append(f'"{clean_title}."')

    if container:
        parts.append(f"*{container}*")
        if vol and issue:
            month_str = f"({month} {year})" if month else f"({year})"
            parts.append(f"{vol}, {issue} {month_str},")
        elif vol:
            parts.append(f"{vol},")
        if pages:
            parts.append(f"{pages}.")

    if doi:
        parts.append(f"https://doi.org/{doi}")

    ref_str = " ".join(parts).strip()
    return f'<a id="ref{index}"></a>\n[{index}] {ref_str}'


# ---------------------------------------------------------------------------
# Vancouver Formatter
# ---------------------------------------------------------------------------

def format_authors_vancouver(authors: list[dict[str, str]]) -> str:
    """Format authors list for Vancouver style: Smith JA, Jones BC."""
    if not authors:
        return ""
    formatted = []
    for a in authors:
        last = a.get("last", "")
        init = format_initials(a.get("first", "")).replace(" ", "").replace(".", "")
        formatted.append(f"{last} {init}".strip() if init else last)

    if len(formatted) >= 7:
        return ", ".join(formatted[:6]) + ", et al."
    return ", ".join(formatted)


def format_vancouver(ref: dict[str, Any], index: int) -> str:
    """Format reference into Vancouver citation style."""
    authors = format_authors_vancouver(ref.get("authors", []))
    title = format_sentence_case(ref.get("title", ""))
    container = ref.get("container", "").strip()
    year = ref.get("year", "")
    vol = ref.get("volume")
    issue = ref.get("issue")
    pages = ref.get("pages")
    doi = normalize_doi(ref.get("doi"))

    parts = []
    if authors:
        author_str = authors if authors.endswith(".") else f"{authors}."
        parts.append(author_str)
    if title:
        clean_title = title.strip()
        if clean_title.endswith(("?", "!")):
            parts.append(clean_title)
        else:
            clean_title = clean_title.rstrip(".,;:")
            parts.append(f"{clean_title}.")
    if container:
        parts.append(f"{container}.")

    vol_issue = ""
    if vol and issue:
        vol_issue = f"{vol}({issue})"
    elif vol:
        vol_issue = f"{vol}"

    art_no = ref.get("article_number")
    if vol_issue:
        prefix = f"{year};{vol_issue}" if year else vol_issue
        if pages:
            date_vol = f"{prefix}:{pages}."
        elif art_no:
            date_vol = f"{prefix}:{art_no}."
        else:
            date_vol = f"{prefix}."
    elif pages:
        date_vol = f"{year}:{pages}." if year else f"{pages}."
    elif art_no:
        date_vol = f"{year}:{art_no}." if year else f"{art_no}."
    elif year:
        date_vol = f"{year}."
    else:
        date_vol = ""

    if date_vol:
        parts.append(date_vol)

    if doi:
        parts.append(f"doi: {doi}.")

    ref_str = " ".join(parts).strip()
    return f'<a id="ref{index}"></a>\n{index}. {ref_str}'


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

_FORMATTERS = {
    "ieee": format_ieee,
    "apa7": format_apa7,
    "apa": format_apa7,
    "harvard": format_harvard,
    "acm": format_acm,
    "vancouver": format_vancouver,
}


def format_reference_entry(ref: dict[str, Any], index: int, style: str = "ieee") -> str:
    """Format a canonical reference dict into the requested citation style string."""
    style_key = style.lower().replace(" ", "").replace("-", "")
    formatter = _FORMATTERS.get(style_key, format_ieee)
    return formatter(ref, index)


__all__ = [
    "format_sentence_case",
    "normalize_doi",
    "normalize_month",
    "format_authors_ieee",
    "format_authors_apa7",
    "format_authors_harvard",
    "format_authors_acm",
    "format_authors_vancouver",
    "format_ieee",
    "format_apa7",
    "format_harvard",
    "format_acm",
    "format_vancouver",
    "format_reference_entry",
]
