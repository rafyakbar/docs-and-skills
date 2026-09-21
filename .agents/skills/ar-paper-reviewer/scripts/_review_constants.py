#!/usr/bin/env python3
"""
scripts/_review_constants.py

Konstanta, Skema, dan Aturan Kontrak Sprint Schema 13 untuk Reviewer Akademik.
Mencakup 6 Dimensi Akseptasi (D1-D6), Eligible Roles, Quantifier Konsensus,
Failure Conditions (F0-F5), Finding Contract #574 (A1/A2/A3/B1), dan Data Fences.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

# 6 Dimensi Akseptasi (Schema 13.2)
ACCEPTANCE_DIMENSIONS: Dict[str, Dict[str, Any]] = {
    "D1": {
        "id": "D1",
        "name": "methodology_rigor",
        "description": "Desain studi, partisi data bebas kebocoran, validitas statistik (95% CI, p-value), dan reprodusibilitas.",
        "priority": "mandatory",
        "eligible_roles": ["methodology"],
        "owner_role": "methodology",
    },
    "D2": {
        "id": "D2",
        "name": "domain_accuracy",
        "description": "Kesesuaian klaim dengan bukti domain, akurasi teori, peliputan literatur primer, dan perbandingan SOTA adil.",
        "priority": "mandatory",
        "eligible_roles": ["domain"],
        "owner_role": "domain",
    },
    "D3": {
        "id": "D3",
        "name": "argumentative_coherence",
        "description": "Konsistensi tesis inti, rantai logika, deteksi bias (cherry-picking/confirmation), dan ketahanan counter-argument.",
        "priority": "mandatory",
        "eligible_roles": ["da", "methodology"],
        "owner_role": "da",
    },
    "D4": {
        "id": "D4",
        "name": "cross_disciplinary_relevance",
        "description": "Keterbacaan lintas disiplin, potensi adopsi praktis, dan implikasi etika data pasien/kebijakan.",
        "priority": "high",
        "eligible_roles": ["perspective"],
        "owner_role": "perspective",
    },
    "D5": {
        "id": "D5",
        "name": "writing_and_structure",
        "description": "Struktur naskah IMRaD, kejelasan visualisasi grafik/tabel, dan kepatuhan konvensi penulisan ilmiah.",
        "priority": "normal",
        "eligible_roles": ["eic"],
        "owner_role": "eic",
    },
    "D6": {
        "id": "D6",
        "name": "venue_fit_and_contribution",
        "description": "Kesesuaian dengan scope penerbit/jurnal target, kebaruan (novelty), dan signifikansi kontribusi bagi pembaca.",
        "priority": "mandatory",
        "eligible_roles": ["eic"],
        "owner_role": "eic",
    },
}

# 5 Persona Penilai Kanonikal
PANEL_ROLES: List[str] = [
    "eic",
    "methodology",
    "domain",
    "perspective",
    "da",
]

ROLE_DISPLAY_NAMES: Dict[str, str] = {
    "eic": "Editor-in-Chief (EIC)",
    "methodology": "Reviewer 1 (Methodology)",
    "domain": "Reviewer 2 (Domain Expert)",
    "perspective": "Reviewer 3 (Cross-Disciplinary Perspective)",
    "da": "Devil's Advocate (Adversarial Evaluator)",
}

# Nilai Keputusan Resmi Kanonikal
DECISIONS: List[str] = [
    "ACCEPT",
    "MINOR_REVISION",
    "MAJOR_REVISION",
    "REJECT",
]

# Status Adjudikasi Tripartit DA CRITICAL
DA_ADJUDICATION_STATES: List[str] = [
    "VALIDATED",
    "REJECTED",
    "UNRESOLVED",
]

# Tingkat Keparahan Temuan (Severity)
SEVERITIES: List[str] = [
    "CRITICAL",
    "MAJOR",
    "MINOR",
]

# 5 Tingkat Kualitas Rubrik (0 - 100)
QUALITY_LEVELS: Dict[str, Tuple[int, int]] = {
    "Exceptional": (80, 100),
    "Strong": (65, 79),
    "Adequate": (50, 64),
    "Weak": (35, 49),
    "Insufficient": (0, 34),
}

# Pola Regex untuk Evidence Anchor yang Valid (6 Tipe Kanonikal Upstream + Section/Page)
RE_EVIDENCE_ANCHOR = re.compile(
    r"\[(?:section|page|table|figure|equation|text|dataset|absence):\s*[^\]]+\]",
    re.IGNORECASE,
)

# Pola Regex untuk Menemukan Severity Tag
RE_SEVERITY_TAG = re.compile(
    r"\b(?:Severity|Tingkat Keparahan)\s*:\s*(CRITICAL|MAJOR|MINOR)\b",
    re.IGNORECASE,
)

# Pola Regex untuk Menemukan Dimensi Tag Eksplisit
RE_DIMENSION_TAG = re.compile(
    r"\[(?:dimension|dimensi):\s*(D[1-6])\]|\b(?:Dimension|Dimensi)\s*:\s*(D[1-6])\b",
    re.IGNORECASE,
)

# Pola Regex untuk Menemukan Rekomendasi Penilai
RE_RECOMMENDATION = re.compile(
    r"\b(?:Recommendation|Rekomendasi)\s*:\s*(Accept|Minor Revision|Major Revision|Reject)\b",
    re.IGNORECASE,
)

# Pola Regex untuk Menemukan Confidence Score (1-5)
RE_CONFIDENCE = re.compile(
    r"\b(?:Confidence Score|Tingkat Keyakinan)\s*:\s*([1-5])\b",
    re.IGNORECASE,
)

# Pola Anti-Kuota (#574 A1 Regression Patterns)
QUOTA_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(?:list|provide|identify|find)\s+(?:3-5|3 to 5|at least \d+|top \d+)\s+(?:weaknesses|strengths|issues|findings)\b", re.IGNORECASE),
    re.compile(r"\b(?:minimum|maximum|quota)\s+of\s+\d+\s+(?:weaknesses|strengths|issues)\b", re.IGNORECASE),
    re.compile(r"\b\(\s*3-5\s+items\s*\)", re.IGNORECASE),
]

# Aturan Kegagalan Kontrak Sprint Schema 13 (F1 - F5, F0)
FAILURE_CONDITIONS: List[Dict[str, Any]] = [
    {
        "id": "F1",
        "severity": 95,
        "cross_reviewer_quantifier": "any",
        "expression": "any mandatory dimension has a fatal block",
        "description": "Terdapat salah satu dimensi wajib (mandatory) yang memiliki status fatal block",
        "action": "editorial_decision=reject",
        "decision": "REJECT",
    },
    {
        "id": "F2",
        "severity": 90,
        "cross_reviewer_quantifier": "any",
        "expression": "any mandatory dimension scores 'block'",
        "description": "Terdapat salah satu dimensi wajib (mandatory) yang memiliki status block",
        "action": "editorial_decision=major_revision",
        "decision": "MAJOR_REVISION",
    },
    {
        "id": "F3",
        "severity": 70,
        "cross_reviewer_quantifier": "majority",
        "expression": "two or more mandatory dimensions score 'warn' or worse",
        "description": "Dua atau lebih dimensi wajib memiliki status warn atau lebih buruk berdasarkan mayoritas",
        "action": "editorial_decision=major_revision",
        "decision": "MAJOR_REVISION",
    },
    {
        "id": "F4",
        "severity": 60,
        "cross_reviewer_quantifier": "any",
        "expression": "any high-priority dimension scores 'block'",
        "description": "Terdapat dimensi prioritas tinggi (D4) yang memiliki status block",
        "action": "editorial_decision=major_revision",
        "decision": "MAJOR_REVISION",
    },
    {
        "id": "F5",
        "severity": 40,
        "cross_reviewer_quantifier": "any",
        "expression": "any dimension scores 'warn' or worse",
        "description": "Terdapat setidaknya satu dimensi yang memiliki status warn atau lebih buruk",
        "action": "editorial_decision=minor_revision",
        "decision": "MINOR_REVISION",
    },
    {
        "id": "F0",
        "severity": 10,
        "cross_reviewer_quantifier": "all",
        "expression": "every dimension scores 'pass'",
        "description": "Seluruh dimensi memiliki status pass tanpa kelemahan material",
        "action": "editorial_decision=accept",
        "decision": "ACCEPT",
    },
]
