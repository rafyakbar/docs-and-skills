# Panduan Template Springer Nature, ACM, dan Generic Article

Dokumen ini memuat panduan konversi dan spesifikasi format dokumen LaTeX untuk jurnal atau prosiding di bawah naungan **Springer Nature**, **ACM (Association for Computing Machinery)**, serta format **Generic Article** serbaguna.

---

## 1. Template Springer Nature (`sn-jnl` & `llncs`)

Springer Nature mengadopsi format konsolidasi `sn-jnl.cls` untuk mayoritas jurnalnya, serta `llncs.cls` untuk prosiding konferensi (Lecture Notes in Computer Science).

### 1.1. Deklarasi Dokumen Springer Nature (`sn-jnl`)
```latex
\documentclass[sn-mathphys,Numbered]{sn-jnl}
\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}

\begin{document}
\title[Short Title]{Full Article Title in Title Case}

\author*[1]{\fnm{First} \sur{Author}}\email{first@domain.edu}
\author[2]{\fnm{Second} \sur{Author}}\email{second@domain.edu}

\affil*[1]{\orgdiv{Department}, \orgname{University}, \orgaddress{\city{City}, \country{Country}}}
\affil[2]{\orgdiv{Faculty}, \orgname{Institute}, \orgaddress{\city{City}, \country{Country}}}

\abstract{Abstract text here (150-250 words)...}
\keywords{keyword1, keyword2, keyword3}

\maketitle

%(SECTION_INPUTS)

\bibliography{references}
\end{document}
```

### 1.2. Opsi Sitasi Springer
Springer mendukung opsi sitasi numerik (`Numbered`) atau sistem penulis-tahun (`Author-Year`). Pada mode numerik, perintah `\cite{ref1}` menghasilkan `[1]`.

---

## 2. Template ACM (`acmart` SIGCONF)

ACM menggunakan berkas kelas terpadu `acmart.cls` untuk seluruh konferensi dan transaksi jurnalnya.

### 2.1. Deklarasi Dokumen ACM Conference
```latex
\documentclass[sigconf]{acmart}
\usepackage{booktabs}

\begin{document}
\title{Full Article Title in Title Case}

\author{First Author}
\affiliation{%
  \institution{University / Institution}
  \city{City}
  \country{Country}
}
\email{first@domain.edu}

\author{Second Author}
\affiliation{%
  \institution{University / Institution}
  \city{City}
  \country{Country}
}
\email{second@domain.edu}

\begin{abstract}
Abstract text here...
\end{abstract}

\keywords{keyword1, keyword2, keyword3}

\maketitle

%(SECTION_INPUTS)

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}
\end{document}
```

---

## 3. Template Generic Article (`article` Class)

Template `article` digunakan untuk pengajuan jurnal umum yang tidak menyediakan kelas dokumen khusus atau untuk draf pracetak (*preprint*):

```latex
\documentclass[12pt, a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{natbib}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}

\bibliographystyle{IEEEtran}
\graphicspath{{images/}}

\title{Full Article Title in Title Case}
\author{First Author \and Second Author}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
Abstract text...
\end{abstract}

%(SECTION_INPUTS)

\bibliography{references}
\end{document}
```

---

## 4. Dukungan Multi-Bahasa & Karakter CJK (XeLaTeX)

Bila naskah memuat karakter non-Latin (misalnya karakter Hanzi/Kanji untuk nama penulis atau abstrak bilingual):
1. Gunakan mesin kompilasi `xelatex` (bukan `pdflatex`).
2. Muat paket `fontspec` dan `xeCJK`:
```latex
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK TC}
```
3. Kompilasi dengan perintah:
```bash
xelatex access.tex
bibtex access
xelatex access.tex
xelatex access.tex
```
