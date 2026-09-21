"""Constants, regular expressions, and LaTeX document templates for ar-paper-latex-converter.

Pure Python standard library. No external dependencies.
"""
from __future__ import annotations

import re

# Block markers and HTML comments
BLOCK_MARKER_RE = re.compile(r"<!--\s*block:([A-Za-z0-9_-]+)\s*-->")
HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")

# Citations
# Interactive bracket citations from ar-paper-citation-numbering: [[N]](06_references.md#refN)
CITATION_BRACKET_LINK_RE = re.compile(r"\[\[(\d+)\]\]\(06_references\.md#ref\d+\)")
# Standard markdown citekey: [@AuthorYear] or [@ref1]
CITATION_CITEKEY_RE = re.compile(r"\[@([A-Za-z0-9_:-]+)\]")
# Simple bracket citations: [N] when preceded by text
CITATION_SIMPLE_NUM_RE = re.compile(r"(?<=\S)\s*\[(\d+)\]")

# Cross references in markdown text
CROSSREF_FIG_RE = re.compile(r"\b(Figure|Fig\.)\s*(\d+[a-z]?)", re.IGNORECASE)
CROSSREF_TAB_RE = re.compile(r"\b(Table|Tab\.)\s*([IVXLCDM\d]+)", re.IGNORECASE)
CROSSREF_EQ_RE = re.compile(r"\b(Equation|Eq\.)\s*\(?(\d+)\)?", re.IGNORECASE)
CROSSREF_SEC_RE = re.compile(r"\b(Section|Sec\.)\s*([IVXLCDM\d]+)", re.IGNORECASE)

# Markdown elements
MD_HEADING_RE = re.compile(r"^(#{1,4})\s+(.+)$", re.MULTILINE)
MD_IMAGE_RE = re.compile(r"!\[(.*?)\]\((.*?)\)")
MD_MATH_INLINE_RE = re.compile(r"\$([^\$\n]+)\$")
MD_MATH_BLOCK_RE = re.compile(r"\$\$([\s\S]*?)\$\$")

# Markdown tables: line containing pipes
MD_TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
MD_TABLE_SEP_RE = re.compile(r"^\s*\|(?:\s*:?-+:?\s*\|)+\s*$")

# Character hygiene
EM_DASH_RE = re.compile(r"\u2014")  # — (em dash banned in IEEE LaTeX)

# LaTeX environment checks
LATEX_BEGIN_ENV_RE = re.compile(r"\\begin\{([A-Za-z0-9*]+)\}")
LATEX_END_ENV_RE = re.compile(r"\\end\{([A-Za-z0-9*]+)\}")
LATEX_CAPTION_RE = re.compile(r"\\caption\{([^}]*)\}")
LATEX_LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
LATEX_CITE_RE = re.compile(r"\\cite\{([^}]+)\}")
LATEX_REF_RE = re.compile(r"\\ref\{([^}]+)\}")
LATEX_EQREF_RE = re.compile(r"\\eqref\{([^}]+)\}")

# Stopwords for English Title Case
TITLE_CASE_STOPWORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of",
    "on", "or", "so", "the", "to", "up", "yet", "with", "via", "across",
    "into", "from"
}

def to_english_title_case(text: str) -> str:
    """Convert text to proper English Title Case preserving acronyms and math."""
    words = text.strip().split()
    if not words:
        return ""
    result: list[str] = []
    for i, w in enumerate(words):
        # Preserve acronyms like ViT, CNN, SVM, RF, IEEE, PCA
        if any(c.isupper() for c in w[1:]):
            result.append(w)
            continue
        lower_w = w.lower()
        if i == 0 or i == len(words) - 1 or lower_w not in TITLE_CASE_STOPWORDS:
            result.append(w.capitalize())
        else:
            result.append(lower_w)
    return " ".join(result)


# ==============================================================================
# Master LaTeX Templates
# ==============================================================================

IEEE_ACCESS_TEMPLATE = r"""\documentclass{ieeeaccess}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{multirow}
\usepackage{subfigure}
\usepackage{url}
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}

\usepackage{bm}
\makeatletter
\AtBeginDocument{\DeclareMathVersion{bold}
\SetSymbolFont{operators}{bold}{T1}{times}{b}{n}
\SetSymbolFont{NewLetters}{bold}{T1}{times}{b}{it}
\SetMathAlphabet{\mathrm}{bold}{T1}{times}{b}{n}
\SetMathAlphabet{\mathit}{bold}{T1}{times}{b}{it}
\SetMathAlphabet{\mathbf}{bold}{T1}{times}{b}{n}
\SetMathAlphabet{\mathtt}{bold}{OT1}{pcr}{b}{n}
\SetSymbolFont{symbols}{bold}{OMS}{cmsy}{b}{n}
\renewcommand\boldmath{\@nomath\boldmath\mathversion{bold}}}

% Include square brackets inside citation hyperlinks
\providecommand{\hyper@link@cite}[2]{\hyperlink{cite.#1}{#2}}
\def\@citex[#1]#2{%
  \let\@citea\@empty
  \@for\@citeb:=#2\do{%
    \@citea\def\@citea{, }%
    \edef\@citeb{\expandafter\@firstofone\@citeb\@empty}%
    \if@filesw\immediate\write\@auxout{\string\citation{\@citeb}}\fi
    \@ifundefined{b@\@citeb}{%
      {\reset@font\bfseries [?]}%
      \G@refundefinedtrue
      \@latex@warning{Citation `\@citeb' on page \thepage \space undefined}%
    }{%
      \hyper@link@cite{\@citeb}{[\csname b@\@citeb\endcsname\if@tempswa, #1\fi]}%
    }%
  }%
}
\def\@cite#1#2{#1}

% Include parentheses inside equation hyperlinks
\renewcommand{\eqref}[1]{\hyperref[#1]{(\ref*{#1})}}
\makeatother

\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}

% Path to graphics directory
\graphicspath{{images/}}

\begin{document}
\history{Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000.}
\doi{10.1109/ACCESS.2026.0000000}

% Title, Authors, Affiliations, Metadata & Funding
\input{sections/00_title.tex}

% Abstract and Index Terms (Keywords)
\input{sections/00_abstract.tex}

\maketitle

% Body Sections
%(SECTION_INPUTS)

% References (BibTeX)
\bibliographystyle{IEEEtran}
\bibliography{references}

%(BIOGRAPHY_INPUT)

\EOD

\end{document}
"""

IEEE_TRAN_TEMPLATE = r"""\documentclass[journal]{IEEEtran}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{url}
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}

\graphicspath{{images/}}

\begin{document}

% Title, Authors, Affiliations
\input{sections/00_title.tex}

% Abstract and Keywords
\input{sections/00_abstract.tex}

\maketitle

% Body Sections
%(SECTION_INPUTS)

% References
\bibliographystyle{IEEEtran}
\bibliography{references}

%(BIOGRAPHY_INPUT)

\end{document}
"""

SPRINGER_SN_TEMPLATE = r"""\documentclass[sn-mathphys,Numbered]{sn-jnl}
\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}

\graphicspath{{images/}}

\begin{document}

\input{sections/00_title.tex}

\input{sections/00_abstract.tex}

\maketitle

%(SECTION_INPUTS)

\bibliography{references}

\end{document}
"""

GENERIC_ARTICLE_TEMPLATE = r"""\documentclass[12pt, a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{natbib}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}

\bibliographystyle{IEEEtran}
\graphicspath{{images/}}

\begin{document}

\input{sections/00_title.tex}

\input{sections/00_abstract.tex}

\maketitle

%(SECTION_INPUTS)

\bibliography{references}

\end{document}
"""

TEMPLATES = {
    "ieeeaccess": IEEE_ACCESS_TEMPLATE,
    "ieeetran": IEEE_TRAN_TEMPLATE,
    "springer": SPRINGER_SN_TEMPLATE,
    "article": GENERIC_ARTICLE_TEMPLATE,
}
