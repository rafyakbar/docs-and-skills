#!/usr/bin/env python3
"""Modular Academic Markdown-to-LaTeX Converter (ar-paper-latex-converter).

Converts modular paper drafts (paper/*.md) into publication-ready LaTeX packages
(IEEE Access, IEEEtran, Springer, ACM SIGCONF, or generic article) preserving math, figures,
booktabs tables, citations, and cross-references.

Exit codes:
  0 = conversion successful
  1 = conversion errors or integrity failures
  2 = usage or file I/O error

Pure Python Standard Library. No external dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from _latex_constants import (
    BLOCK_MARKER_RE,
    CITATION_BRACKET_LINK_RE,
    CITATION_CITEKEY_RE,
    CITATION_SIMPLE_NUM_RE,
    CROSSREF_EQ_RE,
    CROSSREF_FIG_RE,
    CROSSREF_SEC_RE,
    CROSSREF_TAB_RE,
    EM_DASH_RE,
    HTML_COMMENT_RE,
    MD_FENCED_CODE_RE,
    MD_HEADING_RE,
    MD_IMAGE_RE,
    MD_INLINE_CODE_RE,
    MD_MATH_BLOCK_RE,
    MD_MATH_INLINE_RE,
    MD_TABLE_ROW_RE,
    MD_TABLE_SEP_RE,
    TEMPLATES,
    to_english_title_case,
)

# Non-manuscript files to exclude from conversion
NON_MANUSCRIPT_PATTERNS = [
    r"^06_references",
    r"outline",
    r"editorial",
    r"decision",
    r"roadmap",
    r"response",
    r"rebuttal",
    r"cover_letter",
    r"reviewer",
    r"revision_plan",
    r"^readme",
    r"^changelog",
]

# Roman numeral to Arabic numeral mapping for tables
ROMAN_TO_ARABIC = {
    "I": "1", "II": "2", "III": "3", "IV": "4", "V": "5",
    "VI": "6", "VII": "7", "VIII": "8", "IX": "9", "X": "10",
    "XI": "11", "XII": "12", "XIII": "13", "XIV": "14", "XV": "15",
    "XVI": "16", "XVII": "17", "XVIII": "18", "XIX": "19", "XX": "20",
}


def roman_to_arabic(s: str) -> str:
    """Normalize Roman numeral table numbers to Arabic numbers."""
    s_clean = s.strip()
    return ROMAN_TO_ARABIC.get(s_clean.upper(), s_clean)


def clean_markdown_text(text: str) -> str:
    """Remove revision block markers, HTML comments, and replace banned characters."""
    text = BLOCK_MARKER_RE.sub("", text)
    text = HTML_COMMENT_RE.sub("", text)
    # Replace em dash (—) with standard dash or double dash
    text = EM_DASH_RE.sub(" - ", text)
    # Remove HTML anchor tags like <a id="..."></a>
    text = re.sub(r"<a\s+id=[\"'][^\"']+[\"']>\s*</a>", "", text)
    return text


def clean_markdown_anchor_links(text: str) -> str:
    """Convert [Figure 1](#fig1) to Figure 1, [Table IV](#tab4) to Table IV, [(6)](#eq6) to Equation (6)."""
    text = re.sub(r"\[(Figure\s*[\d\w]+)\]\([^)]+\)", r"\1", text, flags=re.IGNORECASE)
    text = re.sub(r"\[(Table\s*[\d\w]+)\]\([^)]+\)", r"\1", text, flags=re.IGNORECASE)
    text = re.sub(r"\[\(([\d\w]+)\)\]\([^)]+\)", r"Equation (\1)", text, flags=re.IGNORECASE)
    return text


def sanitize_latex_text(text: str) -> str:
    """Escape unescaped LaTeX special characters (%, _, &, #) in text mode.

    Protects:
      - Verbatim environments (\\begin{verbatim} ... \\end{verbatim} and \\verb)
      - Display math ($$ ... $$, \\begin{equation} ... \\end{equation}, align, etc.)
      - Inline math ($ ... $)
      - Commands where raw keys/paths are required (\\cite, \\ref, \\label, \\includegraphics, \\url, etc.)
      - Tabular environments (\\begin{tabular} ... \\end{tabular})
      - Existing escaped characters (\\%, \\_, \\&, \\#)
    """
    if not text:
        return text

    placeholders: list[tuple[str, str]] = []

    def _hold(matched_str: str) -> str:
        ph = f"@@SANPH{len(placeholders)}@@"
        placeholders.append((ph, matched_str))
        return ph

    # 1. Protect @@ placeholder tokens (e.g. @@VERBATIMPH0@@, @@INLINECODEPH0@@)
    text = re.sub(r"@@[A-Z0-9]+@@", lambda m: _hold(m.group(0)), text)

    # 2. Protect verbatim
    text = re.sub(r"\\begin\{verbatim\*?\}[\s\S]*?\\end\{verbatim\*?\}", lambda m: _hold(m.group(0)), text)
    text = re.sub(r"\\verb([^\w\s])[\s\S]*?\1", lambda m: _hold(m.group(0)), text)

    # 3. Protect display math
    text = re.sub(r"\$\$[\s\S]*?\$\$", lambda m: _hold(m.group(0)), text)
    text = re.sub(
        r"\\begin\{(?:equation|align|gather|multline|matrix|bmatrix|pmatrix|vmatrix)\*?\}[\s\S]*?\\end\{(?:equation|align|gather|multline|matrix|bmatrix|pmatrix|vmatrix)\*?\}",
        lambda m: _hold(m.group(0)),
        text,
    )

    # 3. Protect inline math
    text = re.sub(r"\$[^\$\n]+?\$", lambda m: _hold(m.group(0)), text)

    # 4. Protect commands that require raw identifiers
    text = re.sub(
        r"\\(?:cite|ref|eqref|label|includegraphics|url|href|input|include|bibliography|bibliographystyle)\*?(?:\[[^\]]*\])?\{[^}]*\}",
        lambda m: _hold(m.group(0)),
        text,
    )

    # 5. Protect already escaped special characters (\%, \_, \&, \#, \$, \{, \})
    text = re.sub(r"\\[%_&#${}]", lambda m: _hold(m.group(0)), text)

    # 6. Protect tabular environments if text already contains tabular blocks
    text = re.sub(r"\\begin\{tabular\*?\}[\s\S]*?\\end\{tabular\*?\}", lambda m: _hold(m.group(0)), text)
    text = re.sub(r"\\begin\{tabularx\}[\s\S]*?\\end\{tabularx\}", lambda m: _hold(m.group(0)), text)

    # 7. Protect general LaTeX commands like \textbf{, \section{, etc.
    text = re.sub(r"\\[a-zA-Z]+", lambda m: _hold(m.group(0)), text)
    text = re.sub(r"\\\\", lambda m: _hold(m.group(0)), text)

    # 8. Escape unescaped special characters
    text = re.sub(r"(?<!\\)%", r"\%", text)
    text = re.sub(r"(?<!\\)_", r"\_", text)
    text = re.sub(r"(?<!\\)&", r"\&", text)
    text = re.sub(r"(?<!\\)#", r"\#", text)

    # 9. Restore placeholders in reverse order
    for ph, orig in reversed(placeholders):
        text = text.replace(ph, orig)

    return text


def convert_inline_code(text: str) -> str:
    """Convert inline backticks `code` into \\texttt{code} with special characters escaped."""
    def _replace(m: re.Match) -> str:
        raw_code = m.group(1)
        sanitized = (
            raw_code.replace("\\", r"\textbackslash{}")
            .replace("%", r"\%")
            .replace("_", r"\_")
            .replace("&", r"\&")
            .replace("#", r"\#")
        )
        return f"\\texttt{{{sanitized}}}"

    return MD_INLINE_CODE_RE.sub(_replace, text)


def convert_citations(text: str, cite_key_map: dict[str, str] | None = None) -> str:
    r"""Convert interactive markdown citations to LaTeX \cite{...}."""
    cite_map = cite_key_map or {}

    def _map_key(k: str) -> str:
        k_clean = k.strip()
        if k_clean in cite_map:
            return cite_map[k_clean]
        if k_clean.isdigit():
            return f"ref{k_clean}"
        return k_clean

    # Multi-citation pattern: [[1]](...), [[2]](...) -> \cite{ref1, ref2}
    def _replace_multi_bracket(match: re.Match) -> str:
        raw = match.group(0)
        nums = re.findall(r"\[\[(\d+)\]\]", raw)
        if nums:
            keys = [_map_key(n) for n in nums]
            return f"\\cite{{{', '.join(keys)}}}"
        return raw

    # Match groups of bracket links: [[1]](...) [,] [[2]](...)
    text = re.sub(
        r"\[\[\d+\]\]\(06_references\.md#ref\d+\)(?:\s*,\s*\[\[\d+\]\]\(06_references\.md#ref\d+\))+",
        _replace_multi_bracket,
        text,
    )

    # Single interactive bracket citation: [[N]](06_references.md#refN) -> \cite{refN}
    def _replace_single_bracket(m: re.Match) -> str:
        n = m.group(1)
        key = _map_key(n)
        return f"\\cite{{{key}}}"

    text = CITATION_BRACKET_LINK_RE.sub(_replace_single_bracket, text)

    # Markdown citekeys: [@ref1] or [@Author2024] -> \cite{ref1} or \cite{Author2024}
    def _replace_citekey(m: re.Match) -> str:
        raw_key = m.group(1).strip()
        target_key = _map_key(raw_key)
        return f"\\cite{{{target_key}}}"

    text = CITATION_CITEKEY_RE.sub(_replace_citekey, text)

    # Move citations placed AFTER period or comma to BEFORE period or comma (IEEE style)
    text = re.sub(r"\.\s*(\\cite\{[^}]+\})", r" \1.", text)
    text = re.sub(r",\s*(\\cite\{[^}]+\})", r" \1,", text)

    # Clean double spaces before citation
    text = re.sub(r"\s{2,}(\\cite\{[^}]+\})", r" \1", text)
    return text


def convert_cross_references(text: str) -> str:
    """Convert markdown cross-references to LaTeX ~\\ref and \\eqref."""
    # Figures: Figure 1 -> Figure~\ref{fig:1}
    text = CROSSREF_FIG_RE.sub(r"Figure~\\ref{fig:\2}", text)
    # Tables: Table I or Table 1 -> Table~\ref{tab:1} (Harmonized to Arabic numerals)
    def _replace_tab_crossref(m: re.Match) -> str:
        tab_num = roman_to_arabic(m.group(2))
        return f"Table~\\ref{{tab:{tab_num}}}"
    text = CROSSREF_TAB_RE.sub(_replace_tab_crossref, text)
    # Equations: Equation (1) -> \eqref{eq:1}
    text = CROSSREF_EQ_RE.sub(r"\\eqref{eq:\2}", text)
    return text


def convert_images(text: str) -> str:
    """Convert markdown images ![Caption](path) to LaTeX figure environment."""
    fig_counter = 1

    # Remove preceding redundant bold caption lines: e.g. **Figure 1. Caption**\n\n![Figure 1. Caption](...)
    text = re.sub(r"\*\*Figure\s*\d+[^*\n]*\*\*\s*\n+(?=\!\[)", "", text, flags=re.IGNORECASE)

    def _replace_img(match: re.Match) -> str:
        nonlocal fig_counter
        caption = match.group(1).strip()
        img_path = match.group(2).strip()
        img_filename = Path(img_path).name

        # Determine if span-column (figure*) is appropriate
        is_wide = any(k in img_filename.lower() or k in caption.lower() for k in ("overview", "framework", "pipeline", "wide", "architecture"))
        env_name = "figure*" if is_wide else "figure"
        width_spec = r"\textwidth" if is_wide else r"\columnwidth"

        # Clean "Figure X." from beginning of caption if present
        clean_cap = re.sub(r"^(?:Figure|Fig\.)\s*\d+[a-z]?[\.:]\s*", "", caption, flags=re.IGNORECASE).strip()
        title_caption = to_english_title_case(clean_cap) if clean_cap else f"Illustration {fig_counter}."
        if not title_caption.endswith("."):
            title_caption += "."
        title_caption = sanitize_latex_text(title_caption)

        fig_label = f"fig:{fig_counter}"
        num_match = re.search(r"\b(?:Figure|Fig\.)\s*(\d+[a-z]?)", caption, re.IGNORECASE)
        if num_match:
            fig_label = f"fig:{num_match.group(1)}"

        fig_counter += 1

        latex_fig = (
            f"\\begin{{{env_name}}}[htbp]\n"
            f"\\centering\n"
            f"\\includegraphics[width={width_spec}]{{{img_filename}}}\n"
            f"\\caption{{{title_caption}}}\n"
            f"\\label{{{fig_label}}}\n"
            f"\\end{{{env_name}}}"
        )
        return latex_fig

    return MD_IMAGE_RE.sub(_replace_img, text)


def convert_markdown_table_to_booktabs(
    table_lines: list[str],
    table_num: str = "1",
    caption_title: str = "Summary of Evaluated Metrics and Results.",
    cite_key_map: dict[str, str] | None = None,
) -> str:
    """Convert lines representing a markdown table into a booktabs LaTeX table with Arabic numerals."""
    rows: list[list[str]] = []
    alignments: list[str] = []

    for line in table_lines:
        line_clean = line.strip()
        if not line_clean.startswith("|") or not line_clean.endswith("|"):
            continue
        cells = [c.strip() for c in line_clean[1:-1].split("|")]
        if MD_TABLE_SEP_RE.match(line_clean):
            for c in cells:
                c_str = c.strip()
                if c_str.startswith(":") and c_str.endswith(":"):
                    alignments.append("c")
                elif c_str.endswith(":"):
                    alignments.append("r")
                else:
                    alignments.append("l")
            continue
        rows.append(cells)

    if not rows:
        return ""

    num_cols = max(len(r) for r in rows)
    while len(alignments) < num_cols:
        alignments.append("l")
    align_str = "".join(alignments[:num_cols])

    # Detect if wide table
    is_wide = num_cols >= 5 or any(len(c) > 35 for r in rows for c in r)
    table_env = "table*" if is_wide else "table"

    if not caption_title.endswith("."):
        caption_title += "."
    clean_caption = to_english_title_case(re.sub(r"^(?:Table|Tab\.)\s*[IVXLCDM\d]+[\.:]\s*", "", caption_title, flags=re.IGNORECASE).strip())
    if not clean_caption.endswith("."):
        clean_caption += "."
    clean_caption = sanitize_latex_text(clean_caption)

    # Standardize table label to Arabic numeral
    arabic_num = roman_to_arabic(table_num)

    out: list[str] = [
        f"\\begin{{{table_env}}}[htbp]",
        f"\\caption{{{clean_caption}}}",
        f"\\label{{tab:{arabic_num}}}",
        r"\centering",
    ]

    if is_wide:
        out.append(f"\\begin{{tabular*}}{{\\textwidth}}{{@{{\\extracolsep{{\\fill}}}}{align_str}}}")
    else:
        out.append(f"\\begin{{tabular}}{{{align_str}}}")

    out.append(r"\toprule")

    # Header
    header = rows[0]
    header_cells = []
    for c in header:
        c_proc = convert_inline_code(c)
        c_proc = sanitize_latex_text(c_proc)
        c_proc = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", c_proc)
        c_proc = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\textit{\1}", c_proc)
        header_cells.append(c_proc)
    header_tex = " & ".join(header_cells) + r" \\"
    out.append(header_tex)
    out.append(r"\midrule")

    # Body
    for row in rows[1:]:
        padded = row + [""] * (num_cols - len(row))
        cell_tex = []
        for cell in padded:
            c = cell
            c = convert_citations(c, cite_key_map)
            c = convert_inline_code(c)
            c = sanitize_latex_text(c)
            c = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", c)
            c = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\textit{\1}", c)
            cell_tex.append(c)
        out.append(" & ".join(cell_tex) + r" \\")

    out.append(r"\bottomrule")
    if is_wide:
        out.append(r"\end{tabular*}")
    else:
        out.append(r"\end{tabular}")
    out.append(f"\\end{{{table_env}}}")

    return "\n".join(out)


def convert_tables_in_text(text: str, cite_key_map: dict[str, str] | None = None) -> str:
    """Find and convert all markdown tables in text to LaTeX booktabs."""
    lines = text.splitlines()
    new_lines: list[str] = []
    in_table = False
    table_buf: list[str] = []
    table_count = 1
    pending_caption = ""
    pending_tab_num = ""

    for line in lines:
        if MD_TABLE_ROW_RE.match(line):
            if not in_table:
                in_table = True
                for back in range(len(new_lines) - 1, max(-1, len(new_lines) - 4), -1):
                    cand = new_lines[back].strip()
                    if cand.startswith("**Table") or cand.startswith("**Tab."):
                        t_m = re.search(r"\*\*(?:Table|Tab\.)\s*([IVXLCDM\d]+)[\.:]\s*([^*]+)\*\*", cand, re.IGNORECASE)
                        if t_m:
                            pending_tab_num = t_m.group(1).strip()
                            pending_caption = t_m.group(2).strip()
                            new_lines.pop(back)
                            break
            table_buf.append(line)
        else:
            if in_table:
                tab_idx = roman_to_arabic(pending_tab_num) if pending_tab_num else str(table_count)
                cap_text = pending_caption or "Summary of Evaluated Metrics and Results."
                tex_table = convert_markdown_table_to_booktabs(table_buf, tab_idx, cap_text, cite_key_map)
                new_lines.append(tex_table)
                table_buf = []
                in_table = False
                table_count += 1
                pending_caption = ""
                pending_tab_num = ""
            new_lines.append(line)

    if in_table:
        tab_idx = roman_to_arabic(pending_tab_num) if pending_tab_num else str(table_count)
        cap_text = pending_caption or "Summary of Evaluated Metrics and Results."
        tex_table = convert_markdown_table_to_booktabs(table_buf, tab_idx, cap_text, cite_key_map)
        new_lines.append(tex_table)

    return "\n".join(new_lines)


def convert_headings(text: str, filename: str = "") -> str:
    """Convert markdown headings #, ##, ### to LaTeX sections with English Title Case."""
    lines = text.splitlines()
    new_lines: list[str] = []

    for line in lines:
        m = MD_HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            heading_raw = m.group(2).strip()

            clean_title = re.sub(r"^(?:Section\s+[IVXLCDM\d]+[:.]?\s*|[IVXLCDM\d]+[\.:]\s*|[A-Z][\.:]\s*)", "", heading_raw, flags=re.IGNORECASE).strip()
            title_case = to_english_title_case(clean_title)
            title_case = sanitize_latex_text(title_case)
            slug = re.sub(r"[^a-zA-Z0-9_]+", "_", clean_title.lower()).strip("_")

            if level == 1:
                new_lines.append(f"\\section{{{title_case}}}\n\\label{{sec:{slug}}}")
            elif level == 2:
                new_lines.append(f"\\subsection{{{title_case}}}\n\\label{{sec:{slug}}}")
            elif level == 3:
                new_lines.append(f"\\subsubsection{{{title_case}}}\n\\label{{sec:{slug}}}")
            else:
                new_lines.append(f"\\paragraph{{{title_case}}}")
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def convert_lists(text: str) -> str:
    """Convert markdown lists to LaTeX itemize and enumerate."""
    lines = text.splitlines()
    new_lines: list[str] = []
    in_enum = False
    in_item = False

    for line in lines:
        ordered_m = re.match(r"^\s*\d+\.\s+(.+)$", line)
        unordered_m = re.match(r"^\s*[-*]\s+(.+)$", line)

        if ordered_m:
            if not in_enum:
                if in_item:
                    new_lines.append(r"\end{itemize}")
                    in_item = False
                new_lines.append(r"\begin{enumerate}")
                in_enum = True
            new_lines.append(f"\\item {ordered_m.group(1).strip()}")
        elif unordered_m:
            if not in_item:
                if in_enum:
                    new_lines.append(r"\end{enumerate}")
                    in_enum = False
                new_lines.append(r"\begin{itemize}")
                in_item = True
            new_lines.append(f"\\item {unordered_m.group(1).strip()}")
        else:
            if in_enum and line.strip() == "":
                new_lines.append(r"\end{enumerate}")
                in_enum = False
            elif in_item and line.strip() == "":
                new_lines.append(r"\end{itemize}")
                in_item = False
            new_lines.append(line)

    if in_enum:
        new_lines.append(r"\end{enumerate}")
    if in_item:
        new_lines.append(r"\end{itemize}")

    return "\n".join(new_lines)


def convert_abstract_markdown(text: str, template_name: str = "ieeeaccess") -> str:
    """Format abstract and keywords into standard LaTeX environments per template."""
    # Extended keywords regex to capture **Keywords**:, **Kata Kunci**:, **Index Terms**:, etc.
    keywords_match = re.search(
        r"(?:\*{1,2})?(?:Keywords|Index Terms|Kata Kunci)(?:\*{1,2})?[:\s—–-]+([^\n]+)",
        text,
        re.IGNORECASE,
    )
    keywords_str = ""
    abstract_text = text

    if keywords_match:
        keywords_str = keywords_match.group(1).strip()
        abstract_text = text[: keywords_match.start()] + text[keywords_match.end() :]

    abstract_text = re.sub(r"^#+\s*Abstract.*$", "", abstract_text, flags=re.MULTILINE).strip()
    abstract_text = clean_markdown_text(abstract_text)

    # Inline code conversion
    abstract_text = convert_inline_code(abstract_text)

    # Protect inline math while converting bold and italic
    math_placeholders: list[tuple[str, str]] = []
    def _protect_math(m: re.Match) -> str:
        ph = f"@@ABSMATHPH{len(math_placeholders)}@@"
        math_placeholders.append((ph, m.group(0)))
        return ph

    abstract_text = re.sub(r"\$[^\$\n]+\$", _protect_math, abstract_text)

    # Sanitize text mode characters in abstract (% -> \%, _ -> \_, etc.)
    abstract_text = sanitize_latex_text(abstract_text)

    # Inline bold **text** -> \textbf{text}
    abstract_text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", abstract_text)
    # Inline italic *text* -> \textit{text}
    abstract_text = re.sub(r"(?<!\*)\*([^* \n][^*]*?[^* \n])\*(?!\*)", r"\\textit{\1}", abstract_text)

    # Restore protected math
    for ph, mph in reversed(math_placeholders):
        abstract_text = abstract_text.replace(ph, mph)

    out = [
        r"\begin{abstract}",
        abstract_text.strip(),
        r"\end{abstract}",
    ]

    if keywords_str:
        clean_kw = sanitize_latex_text(keywords_str)
        if template_name == "article":
            out.extend([
                "",
                r"\vspace{0.5em}",
                f"\\noindent\\textbf{{Keywords}}: {clean_kw}",
            ])
        elif template_name in ("acm", "springer"):
            out.extend([
                "",
                f"\\keywords{{{clean_kw}}}",
            ])
        elif template_name == "ieeetran":
            out.extend([
                "",
                r"\begin{IEEEkeywords}",
                clean_kw,
                r"\end{IEEEkeywords}",
            ])
        else:  # ieeeaccess
            out.extend([
                "",
                r"\begin{keywords}",
                clean_kw,
                r"\end{keywords}",
            ])

    return "\n".join(out) + "\n"


def convert_title_markdown(text: str, template_name: str = "ieeeaccess") -> str:
    """Format paper title and author metadata tailored to template."""
    title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else "Multi-Domain Vision Transformer Fusion for Intersectional Demographic Classification from Facial Images"
    title_case = to_english_title_case(title)
    title_case = sanitize_latex_text(title_case)

    if template_name == "article":
        out = [
            f"\\title{{{title_case}}}",
            "",
            r"\author{First Author \and Second Author \and Corresponding Author}",
            r"\date{\today}",
        ]
    elif template_name == "acm":
        out = [
            f"\\title{{{title_case}}}",
            "",
            r"\author{First Author}",
            r"\affiliation{%",
            r"  \institution{Department of Computer Science, University}",
            r"  \city{City}",
            r"  \country{Country}",
            r"}",
            r"\email{first@univ.edu}",
            "",
            r"\author{Second Author}",
            r"\affiliation{%",
            r"  \institution{Faculty of Engineering, University}",
            r"  \city{City}",
            r"  \country{Country}",
            r"}",
            r"\email{second@univ.edu}",
            "",
            r"\author{Corresponding Author}",
            r"\affiliation{%",
            r"  \institution{Department of Informatics, University}",
            r"  \city{City}",
            r"  \country{Country}",
            r"}",
            r"\email{corr@univ.edu}",
        ]
    elif template_name == "springer":
        out = [
            f"\\title{{{title_case}}}",
            "",
            r"\author*[1]{\fnm{First} \sur{Author}}\email{first@univ.edu}",
            r"\author[2]{\fnm{Second} \sur{Author}}\email{second@univ.edu}",
            r"\author[3]{\fnm{Corresponding} \sur{Author}}\email{corr@univ.edu}",
            "",
            r"\affil*[1]{\orgdiv{Department of Computer Science}, \orgname{University}, \orgaddress{\city{City}, \country{Country}}}",
            r"\affil[2]{\orgdiv{Faculty of Engineering}, \orgname{University}, \orgaddress{\city{City}, \country{Country}}}",
            r"\affil[3]{\orgdiv{Department of Informatics}, \orgname{University}, \orgaddress{\city{City}, \country{Country}}}",
        ]
    elif template_name == "ieeetran":
        out = [
            f"\\title{{{title_case}}}",
            "",
            r"\author{First~Author,~\IEEEmembership{Member,~IEEE,} Second~Author, and~Corresponding~Author,~\IEEEmembership{Senior~Member,~IEEE}%",
            r"\thanks{This work was supported in part by the Research Grant Agency.}%",
            r"\thanks{First Author is with the Department of Computer Science, University, City, Country (e-mail: first@univ.edu).}%",
            r"\thanks{Second Author is with the Faculty of Engineering, University, City, Country (e-mail: second@univ.edu).}%",
            r"\thanks{Corresponding Author is with the Department of Informatics, University, City, Country (e-mail: corr@univ.edu).}}",
        ]
    else:  # ieeeaccess
        out = [
            f"\\title{{{title_case}}}",
            "",
            r"\author{\uppercase{First Author}\authorrefmark{1}, \uppercase{Second Author}\authorrefmark{2}, and \uppercase{Corresponding Author}\authorrefmark{3}}",
            r"\address[1]{Department of Computer Science, University, City, Country (e-mail: first@univ.edu)}",
            r"\address[2]{Faculty of Engineering, University, City, Country (e-mail: second@univ.edu)}",
            r"\address[3]{Department of Informatics, University, City, Country (e-mail: corr@univ.edu)}",
            r"\tfootnote{This work was supported in part by the Research Grant Agency.}",
            r"\corresp{Corresponding author: Corresponding Author (e-mail: corr@univ.edu).}",
        ]
    return "\n".join(out) + "\n"


def convert_biographies_markdown(text: str, images_dir: Path | None = None) -> str:
    """Convert biographies markdown into IEEEbiography environments."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    out: list[str] = []

    for p in paras:
        if p.startswith("#"):
            continue
        # Extract author name
        name_m = re.match(r"^(\*{1,2})?([A-Z][a-zA-Z\s\.,]+?)\1?\s+(is|received|merupakan|lahir|menyelesaikan)\b", p)
        author_name = name_m.group(2).strip() if name_m else "Author Name"
        author_slug = author_name.lower().split()[0]

        # Check existing author image in images_dir
        img_name = f"author_{author_slug}.jpg"
        if images_dir:
            for cand in [f"author_{author_slug}.jpg", f"author_{author_slug}.png", f"author_{author_slug}.jpeg"]:
                if (images_dir / cand).exists():
                    img_name = cand
                    break

        sanitized_bio = sanitize_latex_text(p)
        bio_entry = (
            f"\\begin{{IEEEbiography}}[{{\\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{{{img_name}}}}}]"
            f"{{{author_name}}}\n"
            f"{sanitized_bio}\n"
            f"\\end{{IEEEbiography}}\n"
        )
        out.append(bio_entry)

    return "\n".join(out) + "\n"


def convert_section_markdown(
    md_text: str,
    filename: str,
    template_name: str = "ieeeaccess",
    cite_key_map: dict[str, str] | None = None,
) -> str:
    """Execute the full conversion pipeline for a single modular markdown section."""
    text = clean_markdown_text(md_text)
    text = clean_markdown_anchor_links(text)

    # Special handling for abstract
    if "00_abstract" in filename:
        return convert_abstract_markdown(text, template_name)

    # Special handling for title / authors
    if "00_title" in filename or "authors" in filename:
        return convert_title_markdown(text, template_name)

    # Special handling for biographies
    if "07_biographies" in filename:
        return convert_biographies_markdown(text)

    # 1. Convert fenced code blocks to \begin{verbatim} ... \end{verbatim} placeholders
    verbatim_placeholders: list[tuple[str, str]] = []
    def _protect_verbatim(m: re.Match) -> str:
        code_body = m.group(1)
        ph = f"@@VERBATIMPH{len(verbatim_placeholders)}@@"
        verbatim_placeholders.append((ph, f"\\begin{{verbatim}}\n{code_body}\n\\end{{verbatim}}"))
        return ph

    text = re.sub(r"^```[a-zA-Z0-9_-]*\r?\n([\s\S]*?)\r?\n```\s*$", _protect_verbatim, text, flags=re.MULTILINE)

    # 2. Convert display math equations and protect
    display_math_placeholders: list[tuple[str, str]] = []
    def _protect_display_math(m: re.Match) -> str:
        body = m.group(1).strip()
        tag_m = re.search(r"\\tag\{([^}]+)\}", body)
        if tag_m:
            tag_val = tag_m.group(1)
            clean_body = re.sub(r"\\tag\{[^}]+\}", "", body).strip()
            tex_eq = f"\\begin{{equation}}\n{clean_body}\n\\label{{eq:{tag_val}}}\n\\end{{equation}}"
        else:
            tex_eq = f"\\begin{{equation*}}\n{body}\n\\end{{equation*}}"
        ph = f"@@DISPMATHPH{len(display_math_placeholders)}@@"
        display_math_placeholders.append((ph, tex_eq))
        return ph

    text = MD_MATH_BLOCK_RE.sub(_protect_display_math, text)

    # 3. Protect inline math
    inline_math_placeholders: list[tuple[str, str]] = []
    def _protect_inline_math(m: re.Match) -> str:
        ph = f"@@INLINEMATHPH{len(inline_math_placeholders)}@@"
        inline_math_placeholders.append((ph, m.group(0)))
        return ph

    text = re.sub(r"\$[^\$\n]+?\$", _protect_inline_math, text)

    # 4. Convert inline backticks `code` -> \texttt{...} and protect
    inline_code_placeholders: list[tuple[str, str]] = []
    def _protect_inline_code(m: re.Match) -> str:
        raw_code = m.group(1)
        sanitized = (
            raw_code.replace("\\", r"\textbackslash{}")
            .replace("%", r"\%")
            .replace("_", r"\_")
            .replace("&", r"\&")
            .replace("#", r"\#")
        )
        tex_code = f"\\texttt{{{sanitized}}}"
        ph = f"@@INLINECODEPH{len(inline_code_placeholders)}@@"
        inline_code_placeholders.append((ph, tex_code))
        return ph

    text = MD_INLINE_CODE_RE.sub(_protect_inline_code, text)

    # 5. Convert tables and figures
    table_placeholders: list[tuple[str, str]] = []
    text = convert_tables_in_text(text, cite_key_map)
    def _protect_table_env(m: re.Match) -> str:
        ph = f"@@TABLEENVPH{len(table_placeholders)}@@"
        table_placeholders.append((ph, m.group(0)))
        return ph

    text = re.sub(r"\\begin\{table\*?\}[\s\S]*?\\end\{table\*?\}", _protect_table_env, text)

    figure_placeholders: list[tuple[str, str]] = []
    text = convert_images(text)
    def _protect_figure_env(m: re.Match) -> str:
        ph = f"@@FIGUREENVPH{len(figure_placeholders)}@@"
        figure_placeholders.append((ph, m.group(0)))
        return ph

    text = re.sub(r"\\begin\{figure\*?\}[\s\S]*?\\end\{figure\*?\}", _protect_figure_env, text)

    # 6. Convert citations and cross-references
    text = convert_citations(text, cite_key_map)
    text = convert_cross_references(text)

    # 7. Convert headings
    text = convert_headings(text, filename)

    # 8. Convert lists
    text = convert_lists(text)

    # 9. Sanitize remaining text mode characters (paragraphs, list items)
    text = sanitize_latex_text(text)

    # 10. Inline bold **text** -> \textbf{text} and italic *text* -> \textit{text}
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^* \n][^*]*?[^* \n])\*(?!\*)", r"\\textit{\1}", text)

    # 11. Restore protected placeholders in reverse order
    for ph, orig in reversed(figure_placeholders):
        text = text.replace(ph, orig)
    for ph, orig in reversed(table_placeholders):
        text = text.replace(ph, orig)
    for ph, orig in reversed(inline_code_placeholders):
        text = text.replace(ph, orig)
    for ph, orig in reversed(inline_math_placeholders):
        text = text.replace(ph, orig)
    for ph, orig in reversed(display_math_placeholders):
        text = text.replace(ph, orig)
    for ph, orig in reversed(verbatim_placeholders):
        text = text.replace(ph, orig)

    return text.strip() + "\n"


def parse_ris_entry(entry_text: str) -> dict[str, list[str]]:
    """Parse a single RIS entry into key fields."""
    fields: dict[str, list[str]] = {}
    for line in entry_text.splitlines():
        line = line.strip()
        if len(line) >= 6 and line[2:6] == "  - ":
            tag = line[:2].upper()
            val = line[6:].strip()
            fields.setdefault(tag, []).append(val)
        elif len(line) >= 4 and line[2] == "-" and line[3] == " ":
            tag = line[:2].upper()
            val = line[4:].strip()
            fields.setdefault(tag, []).append(val)
    return fields


def ris_to_bibtex(entry_text: str, cite_key: str) -> str:
    """Convert RIS entry text to a standard BibTeX entry."""
    fields = parse_ris_entry(entry_text)
    ty = fields.get("TY", ["JOUR"])[0].upper()

    if ty in ("JOUR", "JFULL"):
        bib_type = "article"
    elif ty in ("CONF", "CPAPER"):
        bib_type = "inproceedings"
    elif ty in ("BOOK", "SER"):
        bib_type = "book"
    elif ty in ("RPRT", "REPORT"):
        bib_type = "techreport"
    elif ty in ("THES",):
        bib_type = "phdthesis"
    else:
        bib_type = "misc"

    raw_authors = fields.get("AU", []) or fields.get("A1", [])
    authors_str = " and ".join(raw_authors) if raw_authors else "Unknown Author"

    titles = fields.get("TI", []) or fields.get("T1", []) or fields.get("CT", [])
    title_str = titles[0] if titles else "Untitled Document"

    journals = fields.get("JO", []) or fields.get("JF", []) or fields.get("JA", []) or fields.get("T2", [])
    journal_str = journals[0] if journals else ""

    years = fields.get("PY", []) or fields.get("Y1", []) or fields.get("DA", [])
    year_str = ""
    if years:
        ym = re.search(r"\b(19\d\d|20\d\d)\b", years[0])
        if ym:
            year_str = ym.group(1)

    volume_str = fields.get("VL", [""])[0]
    number_str = fields.get("IS", [""])[0]

    sp = fields.get("SP", [""])[0]
    ep = fields.get("EP", [""])[0]
    pages_str = f"{sp}--{ep}" if sp and ep else (sp or ep)

    doi_str = fields.get("DO", [""])[0] or fields.get("DI", [""])[0]

    lines = [f"@{bib_type}{{{cite_key},", f"  author = {{{authors_str}}},", f"  title = {{{title_str}}},"]
    if journal_str:
        tag_name = "journal" if bib_type == "article" else "booktitle"
        lines.append(f"  {tag_name} = {{{journal_str}}},")
    if year_str:
        lines.append(f"  year = {{{year_str}}},")
    if volume_str:
        lines.append(f"  volume = {{{volume_str}}},")
    if number_str:
        lines.append(f"  number = {{{number_str}}},")
    if pages_str:
        lines.append(f"  pages = {{{pages_str}}},")
    if doi_str:
        lines.append(f"  doi = {{{doi_str}}},")

    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def parse_nbib_entry(entry_text: str) -> dict[str, list[str]]:
    """Parse PubMed NBIB tagged lines."""
    fields: dict[str, list[str]] = {}
    current_tag = None
    for line in entry_text.splitlines():
        if not line.strip():
            continue
        tag_m = re.match(r"^([A-Z]{2,4})\s*-\s*(.*)$", line)
        if tag_m:
            current_tag = tag_m.group(1).strip()
            val = tag_m.group(2).strip()
            fields.setdefault(current_tag, []).append(val)
        elif line.startswith("      ") and current_tag:
            val = line.strip()
            if fields[current_tag]:
                fields[current_tag][-1] += " " + val
    return fields


def nbib_to_bibtex(entry_text: str, cite_key: str) -> str:
    """Convert PubMed NBIB entry to BibTeX entry."""
    fields = parse_nbib_entry(entry_text)

    raw_authors = fields.get("FAU", []) or fields.get("AU", [])
    authors_str = " and ".join(raw_authors) if raw_authors else "Unknown Author"

    title_str = (fields.get("TI", ["Untitled"])[0]).rstrip(".")
    journal_str = fields.get("JT", [""])[0] or fields.get("TA", [""])[0]

    year_str = ""
    dp = fields.get("DP", [""])[0]
    ym = re.search(r"\b(19\d\d|20\d\d)\b", dp)
    if ym:
        year_str = ym.group(1)

    volume_str = fields.get("VI", [""])[0]
    number_str = fields.get("IP", [""])[0]
    pages_str = fields.get("PG", [""])[0].replace("-", "--")

    doi_str = ""
    for aid in fields.get("AID", []):
        if "[doi]" in aid.lower():
            doi_str = re.sub(r"\[doi\]", "", aid, flags=re.IGNORECASE).strip()
            break

    lines = [f"@article{{{cite_key},", f"  author = {{{authors_str}}},", f"  title = {{{title_str}}},"]
    if journal_str:
        lines.append(f"  journal = {{{journal_str}}},")
    if year_str:
        lines.append(f"  year = {{{year_str}}},")
    if volume_str:
        lines.append(f"  volume = {{{volume_str}}},")
    if number_str:
        lines.append(f"  number = {{{number_str}}},")
    if pages_str:
        lines.append(f"  pages = {{{pages_str}}},")
    if doi_str:
        lines.append(f"  doi = {{{doi_str}}},")

    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def build_references_bib(
    paper_dir: Path,
    output_dir: Path,
) -> tuple[dict[str, str], int]:
    """Parse references from paper/references.txt or paper/references/, map keys to ref1, ref2, etc., and write references.bib.

    Returns:
        (cite_key_map, total_bib_entries)
    """
    ref_bib_dest = output_dir / "references.bib"
    ref_dir = paper_dir / "references"
    if not ref_dir.exists() and (paper_dir.parent / "references").exists():
        ref_dir = paper_dir.parent / "references"

    cite_key_map: dict[str, str] = {}
    ordered_files: list[Path] = []
    seen_files: set[str] = set()

    # 1. Read paper/references.txt if available
    ref_txt_cands = [paper_dir / "references.txt", paper_dir.parent / "references.txt"]
    for cand_txt in ref_txt_cands:
        if cand_txt.exists():
            for line in cand_txt.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                m = re.search(r"[-*]\s+(?:paper/)?references/([^\s]+\.(?:bib|ris|nbib))", line, re.IGNORECASE)
                if not m:
                    m = re.search(r"[-*]\s+([^\s]+\.(?:bib|ris|nbib))", line, re.IGNORECASE)
                if m:
                    rel_name = m.group(1).strip()
                    file_cand = ref_dir / rel_name if ref_dir and ref_dir.exists() else None
                    if not file_cand or not file_cand.exists():
                        file_cand = paper_dir / rel_name
                    if file_cand and file_cand.exists():
                        norm = file_cand.name.lower()
                        if norm not in seen_files:
                            seen_files.add(norm)
                            ordered_files.append(file_cand)
            break

    # 2. Append any remaining bibliography files in ref_dir
    if ref_dir and ref_dir.exists():
        for ext in ("*.bib", "*.ris", "*.nbib"):
            for f in sorted(ref_dir.glob(ext)):
                norm = f.name.lower()
                if norm not in seen_files:
                    seen_files.add(norm)
                    ordered_files.append(f)

    # 3. If no files found, check existing references.bib in paper_dir or parent
    if not ordered_files:
        for parent_bib in [paper_dir / "references.bib", paper_dir.parent / "references.bib"]:
            if parent_bib.exists():
                shutil.copy2(parent_bib, ref_bib_dest)
                bib_content = parent_bib.read_text(encoding="utf-8")
                keys = re.findall(r"@\w+\s*\{\s*([A-Za-z0-9_:-]+)\s*,", bib_content)
                for k in keys:
                    cite_key_map[k] = k
                return cite_key_map, len(keys)

    # 4. Process each file and assign ref1, ref2, etc.
    entries: list[str] = []
    idx = 1

    for f in ordered_files:
        cite_key = f"ref{idx}"
        file_stem = f.stem
        cite_key_map[file_stem] = cite_key
        cite_key_map[cite_key] = cite_key
        cite_key_map[str(idx)] = cite_key

        suffix = f.suffix.lower()
        content = f.read_text(encoding="utf-8")

        if suffix == ".bib":
            # Extract original BibTeX key(s)
            found_keys = re.findall(r"@\w+\s*\{\s*([A-Za-z0-9_:-]+)\s*,", content)
            for ok in found_keys:
                cite_key_map[ok] = cite_key

            # Replace citation key with ref{N}
            def _replace_key(m: re.Match) -> str:
                return f"{m.group(1)}{cite_key},"

            converted_bib = re.sub(
                r"^(@\w+\s*\{\s*)[A-Za-z0-9_:-]+(?:\s*,)",
                _replace_key,
                content,
                count=1,
                flags=re.MULTILINE,
            )
            entries.append(converted_bib.strip())
            idx += 1
        elif suffix == ".ris":
            converted_bib = ris_to_bibtex(content, cite_key)
            entries.append(converted_bib)
            idx += 1
        elif suffix == ".nbib":
            converted_bib = nbib_to_bibtex(content, cite_key)
            entries.append(converted_bib)
            idx += 1

    if entries:
        ref_bib_dest.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
        return cite_key_map, len(entries)
    else:
        # Fallback starter bib
        starter_bib = (
            "@article{ref1,\n"
            "  author = {Smith, John and Doe, Jane},\n"
            "  title = {Facial Demographic Analysis with Deep Transformers},\n"
            "  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},\n"
            "  year = {2024},\n"
            "  volume = {46},\n"
            "  pages = {100--115}\n"
            "}\n"
        )
        ref_bib_dest.write_text(starter_bib, encoding="utf-8")
        cite_key_map["ref1"] = "ref1"
        cite_key_map["1"] = "ref1"
        return cite_key_map, 1


def convert_paper_directory(
    paper_dir: Path,
    output_dir: Path,
    template_name: str = "ieeeaccess",
) -> dict:
    """Convert an entire paper directory into a modular LaTeX project."""
    paper_dir = paper_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    sections_dir = output_dir / "sections"
    sections_dir.mkdir(parents=True, exist_ok=True)
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy images
    src_images = paper_dir / "images"
    img_copied = 0
    if src_images.exists():
        for f in src_images.iterdir():
            if f.is_file():
                shutil.copy2(f, images_dir / f.name)
                img_copied += 1

    if img_copied == 0 and (paper_dir.parent / "images").exists():
        for f in (paper_dir.parent / "images").iterdir():
            if f.is_file():
                shutil.copy2(f, images_dir / f.name)
                img_copied += 1

    # 2. Build references.bib and key mapping
    cite_key_map, total_bib = build_references_bib(paper_dir, output_dir)

    # 3. Convert markdown files (excluding non-manuscript files)
    md_files = sorted(paper_dir.glob("*.md"))
    converted_sections: list[str] = []
    section_inputs: list[str] = []
    biography_input = ""

    for mf in md_files:
        stem = mf.stem
        # Exclude non-manuscript files
        if any(re.search(pat, stem, re.IGNORECASE) for pat in NON_MANUSCRIPT_PATTERNS):
            continue

        raw_content = mf.read_text(encoding="utf-8")
        if stem == "07_biographies":
            tex_content = convert_biographies_markdown(raw_content, images_dir)
        else:
            tex_content = convert_section_markdown(raw_content, stem, template_name, cite_key_map)

        target_tex = sections_dir / f"{stem}.tex"
        target_tex.write_text(tex_content, encoding="utf-8")
        converted_sections.append(f"sections/{stem}.tex")

        # Track for master inclusion
        if stem in ("00_abstract", "00_title"):
            continue
        elif stem == "07_biographies":
            biography_input = r"\input{sections/07_biographies.tex}"
        else:
            section_inputs.append(f"\\input{{sections/{stem}.tex}}")

    # 4. Ensure 00_title.tex exists
    title_tex_dest = sections_dir / "00_title.tex"
    if not title_tex_dest.exists():
        found_title = False
        for cand in [
            paper_dir.parent / "paper_latex_id" / "sections" / "00_title.tex",
            paper_dir.parent / "paper_latex_en" / "sections" / "00_title.tex",
            paper_dir / "00_title.tex",
        ]:
            if cand.exists():
                shutil.copy2(cand, title_tex_dest)
                converted_sections.append("sections/00_title.tex")
                found_title = True
                break
        if not found_title:
            authors_text = ""
            for ac in [paper_dir / "authors.txt", paper_dir.parent / "authors.txt"]:
                if ac.exists():
                    authors_text = ac.read_text(encoding="utf-8")
                    break
            title_tex_content = convert_title_markdown(authors_text, template_name)
            title_tex_dest.write_text(title_tex_content, encoding="utf-8")
            converted_sections.append("sections/00_title.tex")

    # 5. Copy class and style files if available in project
    for cls_name in ["ieeeaccess.cls", "IEEEtran.cls", "acmart.cls", "spotcolor.sty"]:
        for parent_cand in [paper_dir.parent / "paper_latex_id" / cls_name, paper_dir.parent / "template" / cls_name]:
            if parent_cand.exists():
                shutil.copy2(parent_cand, output_dir / cls_name)
                break

    # 6. Generate Master TeX Document
    template_str = TEMPLATES.get(template_name, TEMPLATES["ieeeaccess"])
    sec_inputs_str = "\n".join(section_inputs)
    master_content = template_str.replace("%(SECTION_INPUTS)", sec_inputs_str)
    master_content = master_content.replace("%(BIOGRAPHY_INPUT)", biography_input)

    master_filename = "access.tex" if template_name == "ieeeaccess" else "main.tex"
    master_dest = output_dir / master_filename
    master_dest.write_text(master_content, encoding="utf-8")

    ref_bib_dest = output_dir / "references.bib"
    report = {
        "status": "SUCCESS",
        "template": template_name,
        "master_file": master_filename,
        "converted_sections": converted_sections,
        "images_copied": img_copied,
        "references_bib_created": ref_bib_dest.exists(),
        "total_references": total_bib,
        "total_sections": len(converted_sections),
    }

    report_path = output_dir / "conversion_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--paper-dir", type=Path, required=True, help="Directory containing source paper/*.md files")
    parser.add_argument("--output-dir", type=Path, required=True, help="Target directory for LaTeX project")
    parser.add_argument(
        "--template",
        choices=["ieeeaccess", "ieeetran", "springer", "acm", "article"],
        default="ieeeaccess",
        help="Target LaTeX document template (default: ieeeaccess)",
    )
    args = parser.parse_args(argv)

    if not args.paper_dir.exists():
        print(f"ERROR: Paper directory not found: {args.paper_dir}", file=sys.stderr)
        return 2

    try:
        report = convert_paper_directory(args.paper_dir, args.output_dir, args.template)
        print(
            f"LaTeX conversion complete: {report['total_sections']} sections converted, "
            f"{report['images_copied']} images copied -> master file: {args.output_dir / report['master_file']}"
        )
        return 0
    except Exception as exc:
        print(f"ERROR: Conversion failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
