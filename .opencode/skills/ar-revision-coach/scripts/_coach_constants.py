#!/usr/bin/env python3
"""Konstanta dan skema kanonikal untuk skill ar-revision-coach.

Mendukung Kontrak Schema 11 R&R Traceability Matrix, Schema 7 Revision Roadmap,
invarian nested-object Commitment Ledger (#268 / Kong et al. 2026 §7.4.3),
dan standarisasi taksonomi evaluasi ulasan naskah ilmiah.
"""
from __future__ import annotations

import re

# Tipe ekstraksi komitmen (Schema 11 / Kong A1)
EXTRACTION_FIELDS = ("commitment_text", "commitment_type", "required_evidence_type")

COMMITMENT_TYPES = {
    "add_experiment",
    "add_analysis",
    "add_clarification",
    "add_citation",
    "restructure",
    "other",
}

# 9 tipe bukti yang disyaratkan (7 bukti naskah + 1 surat respons + 1 escape hatch)
EVIDENCE_TYPES = {
    "new_section",
    "new_figure",
    "new_table",
    "new_citation",
    "methods_paragraph",
    "discussion_paragraph",
    "prose_edit",
    "acknowledgment_only",
    "other",
}

MANUSCRIPT_EVIDENCE_TYPES = {
    "new_section",
    "new_figure",
    "new_table",
    "new_citation",
    "methods_paragraph",
    "discussion_paragraph",
    "prose_edit",
}

# Status siklus hidup komitmen (Lifecycle status - Schema 11)
STATUS_ENUM = {
    "fulfilled",
    "partial",
    "not-fulfilled",
    "explicitly-rejected-with-rationale",
}

NONFULFILLED_STATUSES = STATUS_ENUM - {"fulfilled"}

# Status penyelesaian isu (Resolution status per-concern)
RESOLUTION_STATUSES = {
    "RESOLVED",
    "DELIBERATE_LIMITATION",
    "UNRESOLVABLE",
    "REVIEWER_DISAGREE",
}

# Klasifikasi keparahan komentar reviewer
SEVERITY_TYPES = {
    "Major",
    "Minor",
    "Editorial",
    "Positive",
}

# Prioritas roadmap revisi (Schema 7)
PRIORITIES = {"P1", "P2", "P3"}

PRIORITY_LABELS = {
    "P1": "must_fix",
    "P2": "should_fix",
    "P3": "consider",
}

PRIORITY_FROM_LABEL = {
    "must_fix": "P1",
    "should_fix": "P2",
    "consider": "P3",
}

# Estimasi beban kerja revisi
EFFORT_LEVELS = {
    "Light": "0-2 Major, <5 Minor, mayoritas editorial (1-3 hari)",
    "Moderate": "3-5 Major, 5-10 Minor (1-2 minggu)",
    "Substantial": ">5 Major, membutuhkan data/analisis baru (2-4 minggu)",
    "Fundamental": "Restrukturisasi total atau studi baru (4+ minggu; pertimbangkan submit ulang)",
}

# Kamus kata kunci pemetaan bab naskah
SECTION_MAPPING_KEYWORDS = {
    "00_abstract": ["title", "abstract", "saripati", "judul", "keywords", "kata kunci"],
    "01_introduction": ["introduction", "pendahuluan", "motivation", "motivasi", "background", "latar belakang", "opening", "claim", "contribution", "kontribusi"],
    "02_related-works": ["literature", "literatur", "prior work", "related work", "penelitian terkait", "theoretical framework", "landasan teori", "state-of-the-art", "sota"],
    "03_methodology": ["method", "metode", "metodologi", "design", "desain", "sample", "sampel", "dataset", "data collection", "pengumpulan data", "analysis", "analisis", "validity", "validitas", "algorithm", "arsitektur", "pipeline"],
    "04_results": ["results", "hasil", "findings", "temuan", "table", "tabel", "figure", "gambar", "grafik", "data", "statistics", "statistik", "metric", "metrik", "auroc", "f1", "p-value", "ablation", "ablasi"],
    "05_discussion": ["discussion", "pembahasan", "diskusi", "implications", "implikasi", "interpretation", "interpretasi", "comparison", "perbandingan", "limitation", "limitasi", "keterbatasan", "future work", "riset mendatang"],
    "06_references": ["references", "referensi", "daftar pustaka", "citation", "sitasi", "bibliography", "bibliografi"],
    "general": ["overall", "general", "keseluruhan", "structure", "struktur", "flow", "koherensi"],
}

# Pola regex untuk mendeteksi label reviewer
REVIEWER_HEADER_PATTERN = re.compile(
    r"^(?:#+\s*)?(?:Reviewer\s*#?([0-9]+)|(?:Reviewer|R)\s*([0-9]+)|(Editor-in-Chief|Editor|EIC)|(Devil['’]s\s*Advocate|DA))(?:\s*[:\-\(\[])?",
    re.IGNORECASE | re.MULTILINE
)

# Pola regex untuk mendeteksi nomor komentar
COMMENT_ITEM_PATTERN = re.compile(
    r"^(?:(?:\*|\-|\d+[\.\)])\s+|###?\s+(?:Comment\s+)?([A-Za-z0-9\-]+)[:\.]?\s*)(.*)",
    re.MULTILINE
)

# Frasa imperatif untuk mendeteksi janji perbaikan / komitmen
IMPERATIVE_COMMITMENT_PATTERNS = [
    (re.compile(r"\b(?:please\s+add|add|include|menyertakan|tambahkan|tambah)\s+([^,\.;\n]+)", re.IGNORECASE), "add_experiment", "new_table"),
    (re.compile(r"\b(?:clarify|jelaskan|klarifikasi|explain|elucidate)\s+([^,\.;\n]+)", re.IGNORECASE), "add_clarification", "discussion_paragraph"),
    (re.compile(r"\b(?:run\s+ablation|ablation|eksperimen\s+tambahan|additional\s+experiment)\s+([^,\.;\n]+)", re.IGNORECASE), "add_experiment", "new_table"),
    (re.compile(r"\b(?:cite|reference|rujuk|sitasi|referensi\s+tambahan|discuss\s+the\s+recent)\s+([^,\.;\n]+)", re.IGNORECASE), "add_citation", "new_citation"),
    (re.compile(r"\b(?:restructure|reorganize|reframe|susun\s+ulang|ubah\s+struktur)\s+([^,\.;\n]+)", re.IGNORECASE), "restructure", "new_section"),
    (re.compile(r"\b(?:fix\s+typo|typo|grammar|tata\s+bahasa|ejaan|formatting|format\s+persamaan)\s+([^,\.;\n]+)", re.IGNORECASE), "other", "prose_edit"),
]

# Deteksi notasi indeks parallel-list yang telah usang (#268 regression guard)
RETIRED_INDEX_NOTATION = re.compile(
    r"\b(?:fulfillment_status|unfulfilled_rationale)\s*\[\s*\w+\s*\]"
)
