# Panduan Khusus Template IEEE Access & IEEE Transactions

Dokumen ini memuat standarisasi, konfigurasi makro, dan aturan koding spesifik untuk template publikasi resmi **IEEE Access** (`ieeeaccess.cls`) dan **IEEE Transactions** (`IEEEtran.cls`).

---

## 1. Konfigurasi Preamble & Makro Interaktif (Clickable Hyperlinks)

Pada publikasi IEEE Access, seluruh tautan rujukan (nomor sitasi pustaka, nomor gambar, nomor tabel, dan nomor persamaan) diwajibkan interaktif saat dibuka pada penampil PDF dan berwarna biru seragam.

### 1.1. Paket Hyperref
```latex
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}
```

### 1.2. Makro Kurung Siku Sitasi Interaktif (Clickable Brackets)
Secara bawaan, paket `hyperref` hanya membungkus angka di dalam kurung siku `[1]`, bukan kurung siku luarnya. Tambahkan makro berikut pada preamble dokumen induk (`access.tex`):

```latex
\makeatletter
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
```

### 1.3. Makro Kurung Persamaan Interaktif (\eqref)
Agar tanda kurung `( )` pada nomor persamaan ikut menjadi link biru saat dirujuk dalam teks narasi:

```latex
\renewcommand{\eqref}[1]{\hyperref[#1]{(\ref*{#1})}}
\makeatother
```

---

## 2. Struktur Metadata Judul & Kepengarangan (`sections/00_title.tex`)

Metadata artikel dipisahkan ke dalam berkas modular `sections/00_title.tex` dengan format baku:

```latex
\title{Article Title in English Title Case}

\author{\uppercase{First Author}\authorrefmark{1}, 
\uppercase{Second Author}\authorrefmark{2}, and 
\uppercase{Corresponding Author}\authorrefmark{3}}

\address[1]{Department of Computer Science, Faculty of Engineering, University, City, Country (e-mail: first@domain.edu)}
\address[2]{Department of Informatics, University, City, Country (e-mail: second@domain.edu)}
\address[3]{School of Artificial Intelligence, Institution, City, Country (e-mail: corr@domain.edu)}

\tfootnote{This work was supported in part by the National Research Grant under Award No. 2026-XYZ.}

\corresp{Corresponding author: Corresponding Author Name (e-mail: corr@domain.edu).}
```

---

## 3. Format Biografi Penulis dengan Foto (`sections/07_biographies.tex`)

Pada akhir naskah IEEE Access, setiap penulis wajib memiliki profil biografi akademik disertai pasfoto formal:

```latex
\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{images/author_ricky.jpg}}]{Ricky Eka Putra}
received the M.Cs. degree in Computer Science from Institut Teknologi Sepuluh Nopember in 2018. He is currently an Assistant Professor with the Department of Informatics, Universitas Negeri Surabaya. His research interests include computer vision, medical image analysis, and deep learning fairness.
\end{IEEEbiography}
```

> [!NOTE]
> Dimensi bingkai pasfoto formal IEEE adalah **lebar 1 inci $\times$ tinggi 1.25 inci** (`width=1in,height=1.25in,clip,keepaspectratio`).

---

## 4. Aturan Khusus & Penutup Kolom IEEE Access (`\EOD`)

1. **Perintah Penutup Kolom (`\EOD`)**:
   - Berkas induk `access.tex` wajib menyertakan perintah `\EOD` tepat sebelum `\end{document}`. Perintah ini mengatur penyeimbangan tinggi dua kolom pada halaman terakhir naskah.
2. **Larangan Karakter Em Dash (`—`)**:
   - Karakter em dash unicode (`\u2014`) dilarang keras karena dapat merusak proses rendering font Type 1 pada kompilator pdfLaTeX IEEE Access. Gunakan tanda hubung standar (`-`) atau tanda kurung.
3. **Posisi Sitasi Sebelum Tanda Baca**:
   - Penempatan sitasi wajib sebelum titik atau koma:
     * **BENAR**: `... in recent vision architectures \cite{ref1}, \cite{ref2}.`
     * **SALAH**: `... in recent vision architectures. \cite{ref1}, \cite{ref2}`
