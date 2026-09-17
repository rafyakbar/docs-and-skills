#!/usr/bin/env python3
"""Shared constants for claim-faithfulness and uncited-assertion detection.

Provides bilingual (English & Indonesian) keywords, regexes, and guard rules
for identifying empirical statements and ensuring proper citation attribution.
"""
from __future__ import annotations

import re

# Rule version
UNCITED_RULE_VERSION = "D4-c-bilingual-v1"

# Condition 1: empirical-claim verbs (case-insensitive whole-word match).
# Includes canonical English verbs + Indonesian empirical research verbs.
UNCITED_EMPIRICAL_VERBS: frozenset[str] = frozenset(
    {
        # English
        "showed",
        "demonstrated",
        "observed",
        "proved",
        "confirmed",
        "found",
        "revealed",
        "achieved",
        # Indonesian
        "menunjukkan",
        "membuktikan",
        "mengamati",
        "mengonfirmasi",
        "ditemukan",
        "memperlihatkan",
        "menghasilkan",
        "mencapai",
        "mengindikasikan",
    }
)

# Condition 1: fuzzy quantifier words (case-insensitive whole-word).
# Includes canonical English quantifiers + Indonesian equivalents.
UNCITED_FUZZY_QUANTIFIERS: frozenset[str] = frozenset(
    {
        # English
        "most",
        "several",
        "two-thirds",
        "majority",
        "minority",
        # Indonesian
        "sebagian besar",
        "beberapa",
        "dua pertiga",
        "separuh",
        "mayoritas",
        "minoritas",
    }
)

# Condition 1: numerical quantifier regex.
# Matches:
# 1. Percentages (e.g., 50%, 94.2%)
# 2. Ratio idioms (e.g., "67 of 100", "8 dari 10")
# 3. Bare numbers (filtered by guard pass to eliminate years/sections)
RE_NUMERIC_QUANTIFIER = re.compile(
    r"\b\d+(?:\.\d+)?%"
    r"|\b\d+(?:\.\d+)?\s+(?:of|dari)\s+\d+\b"
    r"|\b\d+(?:\.\d+)*\b"
)

# Condition 1 guard: rejects bare numbers representing publication years,
# version numbers, or section/table references rather than empirical quantities.
RE_BARE_NUMERIC_YEAR = re.compile(r"^(19|20)\d{2}$")
RE_DOTTED_TRIPLE_OR_MORE = re.compile(r"^\d+(?:\.\d+){2,}$")
RE_DOTTED_PAIR = re.compile(r"^\d+\.\d+$")

# Section and reference cue words in English and Indonesian within a left window
RE_SECTION_CUE = re.compile(
    r"(?:section|chapter|figure|table|fig\.|tbl\.|step|appendix|§|bab|gambar|tabel|langkah|lampiran|persamaan|eq\.)\s*$",
    re.IGNORECASE,
)
RE_VERSION_PREFIX = re.compile(r"v\s*$", re.IGNORECASE)
RE_NUMERIC_LEFT_ATTACHED = re.compile(r"\d+\.$")

# Condition 2: citation reference marker probe.
# Detects:
# - Three-layer citation markers: `<!-- ref:slug -->` or `<!--ref:slug-->`
# - Markdown bracket citations: `[1]`, `[1, 2]`, `[1-3]`, `[@smith2023]`, `[[1]](...)`
RE_REF_MARKER = re.compile(
    r"<!--\s*ref:[^\s>][^>]*?-->|"
    r"\[\[?\d+(?:[,\s-]+\d+)*\]?\](?:\([^)]*\))?|"
    r"\[@[a-zA-Z0-9_-]+\]"
)

# Condition 3: definitional-phrase substrings (case-insensitive).
# Excludes methodological definitions, paper roadmap statements, and self-defined terms.
UNCITED_DEFINITION_PHRASES: tuple[str, ...] = (
    # English
    "refers to",
    "is defined as",
    "we define",
    "for the purposes of",
    "in this paper, we",
    "we propose",
    "our contribution",
    "the remainder of this paper",
    # Indonesian
    "mengacu pada",
    "didefinisikan sebagai",
    "kami mendefinisikan",
    "untuk keperluan",
    "pada makalah ini, kami",
    "kami mengusulkan",
    "kontribusi kami",
    "sistematika penulisan naskah",
    "merupakan istilah",
)

__all__ = [
    "UNCITED_RULE_VERSION",
    "UNCITED_EMPIRICAL_VERBS",
    "UNCITED_FUZZY_QUANTIFIERS",
    "RE_NUMERIC_QUANTIFIER",
    "RE_BARE_NUMERIC_YEAR",
    "RE_DOTTED_TRIPLE_OR_MORE",
    "RE_DOTTED_PAIR",
    "RE_SECTION_CUE",
    "RE_VERSION_PREFIX",
    "RE_NUMERIC_LEFT_ATTACHED",
    "RE_REF_MARKER",
    "UNCITED_DEFINITION_PHRASES",
]
