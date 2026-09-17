#!/usr/bin/env python3
"""Shared title-similarity + retry-budget helpers for citation verification.

Implements:
- `_normalize_title`: case-insensitivity, punctuation to whitespace, whitespace collapse.
- `_normalize_title_acronym`: dotted acronym normalization (e.g. `R.A.G.` -> `RAG`).
- `_similarity`: Levenshtein SequenceMatcher ratio with acronym pre-pass.
- `exact_normalized_title`: exact title matching gate (#431).
- `generic_title`: closed set of generic section/type titles rejection.
"""
from __future__ import annotations

import re
import string
from difflib import SequenceMatcher

_PUNCT_TRANSLATION = str.maketrans({c: " " for c in string.punctuation})

# Collapse a run of two-or-more `<letter>.` units at a word boundary
# (`R.A.G.` -> `RAG`) BEFORE punctuation->whitespace.
_DOTTED_ACRONYM = re.compile(r"\b(?:[A-Za-z]\.){2,}")

# Shared retry budget for index clients
_BACKOFF_SECONDS = 2.0
_MAX_RETRIES = 3

# Canonical title-similarity threshold for "matched" verdict
_TITLE_SIMILARITY_THRESHOLD = 0.70


def _normalize_title(s: str) -> str:
    """Case-insensitive, stripped of punctuation before computing similarity."""
    cleaned = s.lower().translate(_PUNCT_TRANSLATION)
    return " ".join(cleaned.split())


def _normalize_title_acronym(s: str) -> str:
    """Base normalization plus dotted-acronym pre-pass."""
    collapsed = _DOTTED_ACRONYM.sub(lambda m: m.group(0).replace(".", ""), s)
    return _normalize_title(collapsed)


def _similarity(a: str, b: str) -> float:
    """Levenshtein ratio over base and dotted-acronym normalizations."""
    a_base, b_base = _normalize_title(a), _normalize_title(b)
    base = SequenceMatcher(None, a_base, b_base).ratio()
    a_acr, b_acr = _normalize_title_acronym(a), _normalize_title_acronym(b)
    if a_acr == a_base and b_acr == b_base:
        return base
    return max(base, SequenceMatcher(None, a_acr, b_acr).ratio())


def exact_normalized_title(a: str, b: str) -> bool:
    """True iff two titles match under base or acronym normalization."""
    return (
        _normalize_title(a) == _normalize_title(b)
        or _normalize_title_acronym(a) == _normalize_title_acronym(b)
    )


# Closed generic/section/type/notice set to prevent false generic title matches.
_GENERIC_TITLES = frozenset(
    _normalize_title(t)
    for t in (
        "editorial", "guest editorial", "editorial comment", "introduction",
        "preface", "foreword", "letter", "letters", "letter to the editor",
        "letters to the editor", "reply", "comment", "commentary", "response",
        "correspondence", "book review", "book reviews", "review", "news",
        "obituary", "in memoriam", "acknowledgements", "front matter",
        "back matter", "table of contents", "abstracts", "abstract",
        "proceedings", "keynote", "panel discussion", "workshop summary",
        "special issue", "untitled", "note", "notes", "highlights", "errata",
        "erratum", "corrigendum", "addendum", "author correction",
        "publisher correction", "retraction", "expression of concern",
        "short communication", "rapid communication", "brief communication",
        "short report", "brief report", "technical report", "meeting report",
        "conference report", "case report", "case study", "research article",
        "original article", "original research", "short paper", "perspective",
        "perspectives", "viewpoint", "opinion", "discussion", "summary",
        "conclusion", "conclusions", "abstract only", "supplementary material",
    )
)


def generic_title(title: str) -> bool:
    """True iff normalized title is a member of the closed generic set."""
    return _normalize_title(title) in _GENERIC_TITLES


__all__ = [
    "_BACKOFF_SECONDS",
    "_MAX_RETRIES",
    "_TITLE_SIMILARITY_THRESHOLD",
    "_normalize_title",
    "_normalize_title_acronym",
    "_similarity",
    "exact_normalized_title",
    "generic_title",
]
