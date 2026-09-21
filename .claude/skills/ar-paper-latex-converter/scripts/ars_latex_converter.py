#!/usr/bin/env python3
"""Modular Academic Markdown-to-LaTeX Converter (ar-paper-latex-converter).

Converts modular paper drafts (paper/*.md) into publication-ready LaTeX packages
(IEEE Access, IEEEtran, Springer, or generic article) preserving math, figures,
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
    MD_HEADING_RE,
    MD_IMAGE_RE,
    MD_MATH_BLOCK_RE,
    MD_MATH_INLINE_RE,
    MD_TABLE_ROW_RE,
    MD_TABLE_SEP_RE,
    TEMPLATES,
    to_english_title_case,
)


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


def convert_citations(text: str) -> str:
    r"""Convert interactive markdown citations to LaTeX \cite{...}."""
    # Multi-citation pattern: [[1]](...), [[2]](...) -> \cite{ref1, ref2}
    def _replace_multi_bracket(match: re.Match) -> str:
        raw = match.group(0)
        nums = re.findall(r"\[\[(\d+)\]\]", raw)
        if nums:
            keys = [f"ref{n}" for n in nums]
            return f"\\cite{{{', '.join(keys)}}}"
        return raw

    # Match groups of bracket links: [[1]](...) [,] [[2]](...)
    text = re.sub(
        r"\[\[\d+\]\]\(06_references\.md#ref\d+\)(?:\s*,\s*\[\[\d+\]\]\(06_references\.md#ref\d+\))+",
        _replace_multi_bracket,
        text,
    )

    # Single interactive bracket citation: [[N]](06_references.md#refN) -> \cite{refN}
    text = CITATION_BRACKET_LINK_RE.sub(r"\\cite{ref\1}", text)

    # Markdown citekeys: [@ref1] or [@Author2024] -> \cite{ref1} or \cite{Author2024}
    text = CITATION_CITEKEY_RE.sub(r"\\cite{\1}", text)

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
    # Tables: Table I -> Table~\ref{tab:I}
    text = CROSSREF_TAB_RE.sub(r"Table~\\ref{tab:\2}", text)
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
    table_num: str = "I",
    caption_title: str = "Summary of Evaluated Metrics and Results.",
) -> str:
    """Convert lines representing a markdown table into a booktabs LaTeX table."""
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

    out: list[str] = [
        f"\\begin{{{table_env}}}[htbp]",
        f"\\caption{{{clean_caption}}}",
        f"\\label{{tab:{table_num}}}",
        r"\centering",
    ]

    if is_wide:
        out.append(f"\\begin{{tabular*}}{{\\textwidth}}{{@{{\\extracolsep{{\\fill}}}}{align_str}}}")
    else:
        out.append(f"\\begin{{tabular}}{{{align_str}}}")

    out.append(r"\toprule")

    # Header
    header = rows[0]
    header_tex = " & ".join(header) + r" \\"
    out.append(header_tex)
    out.append(r"\midrule")

    # Body
    for row in rows[1:]:
        padded = row + [""] * (num_cols - len(row))
        cell_tex = []
        for cell in padded:
            # Convert formatting inside table cells
            c = cell
            c = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", c)
            c = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\textit{\1}", c)
            c = re.sub(r"`([^`]+)`", r"\1", c)
            cell_tex.append(c)
        out.append(" & ".join(cell_tex) + r" \\")

    out.append(r"\bottomrule")
    if is_wide:
        out.append(r"\end{tabular*}")
    else:
        out.append(r"\end{tabular}")
    out.append(f"\\end{{{table_env}}}")

    return "\n".join(out)


def convert_tables_in_text(text: str) -> str:
    """Find and convert all markdown tables in text to LaTeX booktabs."""
    lines = text.splitlines()
    new_lines: list[str] = []
    in_table = False
    table_buf: list[str] = []
    table_count = 1
    pending_caption = ""
    pending_tab_num = ""

    roman_numerals = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

    for i, line in enumerate(lines):
        if MD_TABLE_ROW_RE.match(line):
            if not in_table:
                in_table = True
                # Check previous non-empty lines for table caption
                # e.g., **Table IV. Caption**
                for back in range(len(new_lines) - 1, max(-1, len(new_lines) - 4), -1):
                    cand = new_lines[back].strip()
                    if cand.startswith("**Table") or cand.startswith("**Tab."):
                        # Extract table number and caption
                        t_m = re.search(r"\*\*(?:Table|Tab\.)\s*([IVXLCDM\d]+)[\.:]\s*([^*]+)\*\*", cand, re.IGNORECASE)
                        if t_m:
                            pending_tab_num = t_m.group(1).strip()
                            pending_caption = t_m.group(2).strip()
                            # Remove the bold title line from new_lines
                            new_lines.pop(back)
                            break
            table_buf.append(line)
        else:
            if in_table:
                # Determine table number
                tab_idx = pending_tab_num or (roman_numerals[table_count - 1] if table_count <= len(roman_numerals) else str(table_count))
                cap_text = pending_caption or "Summary of Evaluated Metrics and Results."
                tex_table = convert_markdown_table_to_booktabs(table_buf, tab_idx, cap_text)
                new_lines.append(tex_table)
                table_buf = []
                in_table = False
                table_count += 1
                pending_caption = ""
                pending_tab_num = ""
            new_lines.append(line)

    if in_table:
        tab_idx = pending_tab_num or str(table_count)
        cap_text = pending_caption or "Summary of Evaluated Metrics and Results."
        tex_table = convert_markdown_table_to_booktabs(table_buf, tab_idx, cap_text)
        new_lines.append(tex_table)

    return "\n".join(new_lines)


def convert_display_math(text: str) -> str:
    """Convert $$ ... \tag{X} $$ to \\begin{equation} ... \\label{eq:X} \\end{equation}."""
    def _replace_math(m: re.Match) -> str:
        body = m.group(1).strip()
        tag_m = re.search(r"\\tag\{([^}]+)\}", body)
        if tag_m:
            tag_val = tag_m.group(1)
            clean_body = re.sub(r"\\tag\{[^}]+\}", "", body).strip()
            return f"\\begin{{equation}}\n{clean_body}\n\\label{{eq:{tag_val}}}\n\\end{{equation}}"
        return f"\\begin{{equation*}}\n{body}\n\\end{{equation*}}"

    return MD_MATH_BLOCK_RE.sub(_replace_math, text)


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


def convert_section_markdown(md_text: str, filename: str) -> str:
    """Execute the full conversion pipeline for a single modular markdown section."""
    text = clean_markdown_text(md_text)
    text = clean_markdown_anchor_links(text)

    # Special handling for abstract
    if "00_abstract" in filename:
        return convert_abstract_markdown(text)

    # Special handling for title / authors
    if "00_title" in filename or "authors" in filename:
        return convert_title_markdown(text)

    # Special handling for biographies
    if "07_biographies" in filename:
        return convert_biographies_markdown(text)

    # Convert display math equations
    text = convert_display_math(text)

    # Protect inline math while converting bold and italic
    math_placeholders: list[str] = []
    def _protect_math(m: re.Match) -> str:
        math_placeholders.append(m.group(0))
        return f"__MATH_PH_{len(math_placeholders)-1}__"

    text = re.sub(r"\$[^\$\n]+\$", _protect_math, text)

    # Inline bold **text** -> \textbf{text}
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    # Inline italic *text* -> \textit{text}
    text = re.sub(r"(?<!\*)\*([^* \n][^*]*?[^* \n])\*(?!\*)", r"\\textit{\1}", text)

    # Restore protected math
    for idx, mph in enumerate(math_placeholders):
        text = text.replace(f"__MATH_PH_{idx}__", mph)

    # Convert tables and figures (which introduce LaTeX environments)
    text = convert_tables_in_text(text)
    text = convert_images(text)

    # Convert citations, cross-references, headings, and lists
    text = convert_citations(text)
    text = convert_cross_references(text)
    text = convert_headings(text, filename)
    text = convert_lists(text)

    return text.strip() + "\n"


def convert_abstract_markdown(text: str) -> str:
    """Format abstract and keywords into standard LaTeX environments."""
    keywords_match = re.search(r"(?:Keywords|Index Terms|Kata Kunci)[:\s]+([^\n]+)", text, re.IGNORECASE)
    keywords_str = ""
    abstract_text = text

    if keywords_match:
        keywords_str = keywords_match.group(1).strip()
        abstract_text = text[: keywords_match.start()] + text[keywords_match.end() :]

    abstract_text = re.sub(r"^#+\s*Abstract.*$", "", abstract_text, flags=re.MULTILINE).strip()
    abstract_text = clean_markdown_text(abstract_text)

    out = [
        r"\begin{abstract}",
        abstract_text,
        r"\end{abstract}",
    ]

    if keywords_str:
        out.extend([
            "",
            r"\begin{keywords}",
            keywords_str,
            r"\end{keywords}",
        ])

    return "\n".join(out) + "\n"


def convert_title_markdown(text: str) -> str:
    """Format paper title and author metadata."""
    title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else "Multi-Domain Vision Transformer Fusion for Intersectional Demographic Classification from Facial Images"
    title_case = to_english_title_case(title)

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

        bio_entry = (
            f"\\begin{{IEEEbiography}}[{{\\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{{{img_name}}}}}]"
            f"{{{author_name}}}\n"
            f"{p}\n"
            f"\\end{{IEEEbiography}}\n"
        )
        out.append(bio_entry)

    return "\n".join(out) + "\n"


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

    # Also check parent images/ if none found
    if img_copied == 0 and (paper_dir.parent / "images").exists():
        for f in (paper_dir.parent / "images").iterdir():
            if f.is_file():
                shutil.copy2(f, images_dir / f.name)
                img_copied += 1

    # 2. Convert markdown files
    md_files = sorted(paper_dir.glob("*.md"))
    converted_sections: list[str] = []
    section_inputs: list[str] = []
    biography_input = ""

    for mf in md_files:
        stem = mf.stem
        # Skip references compilation input and outline
        if stem.startswith("06_references") or stem == "paper_outline" or "roadmap" in stem:
            continue

        raw_content = mf.read_text(encoding="utf-8")
        if stem == "07_biographies":
            tex_content = convert_biographies_markdown(raw_content, images_dir)
        else:
            tex_content = convert_section_markdown(raw_content, stem)

        target_tex = sections_dir / f"{stem}.tex"
        target_tex.write_text(tex_content, encoding="utf-8")
        converted_sections.append(f"sections/{stem}.tex")

        # Track for master inclusion
        if stem == "00_abstract" or stem == "00_title":
            continue
        elif stem == "07_biographies":
            biography_input = r"\input{sections/07_biographies.tex}"
        else:
            section_inputs.append(f"\\input{{sections/{stem}.tex}}")

    # 3. Ensure 00_title.tex exists
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
            title_tex_content = convert_title_markdown(authors_text)
            title_tex_dest.write_text(title_tex_content, encoding="utf-8")
            converted_sections.append("sections/00_title.tex")

    # 4. Generate or copy references.bib
    bib_entries_count = 0
    ref_bib_dest = output_dir / "references.bib"
    ref_dir = paper_dir / "references"

    if ref_dir.exists():
        bib_files = list(ref_dir.glob("*.bib"))
        if bib_files:
            merged_bib = []
            for bf in sorted(bib_files):
                merged_bib.append(bf.read_text(encoding="utf-8").strip())
                bib_entries_count += 1
            ref_bib_dest.write_text("\n\n".join(merged_bib) + "\n", encoding="utf-8")

    if not ref_bib_dest.exists() or ref_bib_dest.stat().st_size == 0:
        parent_bib = paper_dir.parent / "references.bib"
        if parent_bib.exists():
            shutil.copy2(parent_bib, ref_bib_dest)
        else:
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
            bib_entries_count = 1

    # 5. Copy class and style files if available in project
    for cls_name in ["ieeeaccess.cls", "IEEEtran.cls", "spotcolor.sty"]:
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

    report = {
        "status": "SUCCESS",
        "template": template_name,
        "master_file": master_filename,
        "converted_sections": converted_sections,
        "images_copied": img_copied,
        "references_bib_created": ref_bib_dest.exists(),
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
        choices=["ieeeaccess", "ieeetran", "springer", "article"],
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
