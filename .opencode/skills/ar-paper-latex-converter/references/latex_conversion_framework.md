# Kerangka Kerja Konversi LaTeX Akademik (LaTeX Conversion Framework)

Dokumen ini memaparkan arsitektur, filosofi desain, dan standar teknis konversi naskah paper akademik berbasis Markdown modular (`paper/*.md`) ke dalam format publikasi ilmiah **LaTeX modular siap submit** (Fase 16 / Kluster D siklus riset akademik).

---

## 1. Filosofi Modularitas 1:1 (*Modular Section Architecture*)

Siklus riset modern memisahkan penulisan draf naskah ke dalam berkas-berkas Markdown modular (`paper/01_introduction.md`, `paper/02_related-works.md`, dst.). Pendekatan ini mencegah pemusatan kode yang rentan konflik (*merge conflict*) dan membatasi radius modifikasi model AI (DELEGATE-52).

Dalam konversi LaTeX, filosofi ini dipertahankan secara utuh melalui pemetaan **1-ke-1**:

```
paper/                                       paper_latex/
├── 00_abstract.md           ─────────►     ├── sections/00_abstract.tex
├── 01_introduction.md       ─────────►     ├── sections/01_introduction.tex
├── 02_related-works.md      ─────────►     ├── sections/02_related-works.tex
├── 03_materials-and-...md   ─────────►     ├── sections/03_materials-and-...tex
├── 04_results-and-...md     ─────────►     ├── sections/04_results-and-...tex
├── 05_conclusion.md         ─────────►     ├── sections/05_conclusion.tex
├── 07_biographies.md        ─────────►     ├── sections/07_biographies.tex
├── images/                  ─────────►     ├── images/
└── references/*.bib         ─────────►     ├── references.bib
                                            └── access.tex / main.tex (Dokumen Induk)
```

Dokumen induk (`access.tex` untuk IEEE Access atau `main.tex` untuk template lain) bertindak sebagai **orkestrator struktural**:
- Memuat preamble paket (`amsmath`, `graphicx`, `booktabs`, `hyperref`).
- Mengatur konfigurasi tautan dan makro interaktif.
- Menyisipkan seluruh berkas seksi secara runtut melalui perintah `\input{sections/...}`.
- Memanggil pustaka BibTeX melalui `\bibliography{references}`.

---

## 2. Pembersihan Artefak Markdown (*Clean Stripping Rule*)

Naskah Markdown yang dihasilkan oleh pipeline revisi presisi blok (`ar-paper-revision` Spec #390) mengandung berbagai penanda sintaks yang tidak boleh lolos ke dalam naskah publikasi LaTeX:

1. **Stempel Blok Revisi**: Penanda seperti `<!--block:B0012-->` dibersihkan seluruhnya tanpa menyisakan baris kosong artifisial.
2. **Komentar HTML**: Komentar `<!-- ... -->` dihilangkan.
3. **Jangkar HTML & Tautan Internal**: Tag seperti `<a id="fig1"></a>` atau tautan Markdown `[Figure 1](#fig1)` diubah menjadi format standar perujukan LaTeX (`Figure~\ref{fig:1}`).
4. **Duplikasi Judul Caption**: Baris tebal yang sengaja dituliskan di Markdown sebelum tabel atau gambar (misal `**Figure 1. End-to-End Framework...**`) disatukan ke dalam perintah formal `\caption{...}` dan dibersihkan dari teks tubuh paragraf.

---

## 3. Tata Kelola Aset Grafis & Bibliografi

1. **Aset Gambar (`images/`)**:
   - Seluruh citra pendukung disinkronkan ke subdirektori `images/` pada paket LaTeX.
   - Preamble LaTeX menyetel `\graphicspath{{images/}}`, sehingga penulisan kode di seksi naskah cukup memanggil nama berkas: `\includegraphics[width=\columnwidth]{model_architecture.png}`.
2. **Basis Data Rujukan BibTeX (`references.bib`)**:
   - Seluruh berkas entri bibliografi (`.bib`) yang dikumpulkan pada fase kurasi sitasi (`ar-paper-sentence-citation`) digabungkan ke dalam berkas `references.bib` di akar folder LaTeX.
   - Kunci sitasi distandarisasi (misal `ref1`, `ref2`, atau `AuthorYear`) agar cocok dengan perintah pemanggilan `\cite{...}` di dalam teks.

---

## 4. Alur Kompilasi & Opsi Ekspor Dokumen

### 4.1. Kompilasi Standar Terminal (pdfLaTeX)
Untuk menghasilkan berkas PDF final dari naskah LaTeX yang dihasilkan:
```bash
pdflatex access.tex
bibtex access
pdflatex access.tex
pdflatex access.tex
```
Urutan 4 tahap ini memastikan:
1. Ekstraksi kunci sitasi dan label ke dalam berkas `.aux`.
2. Resolusi bibliografi oleh `bibtex` ke dalam berkas `.bbl`.
3. Penyisipan daftar pustaka dan resolusi nomor rujukan.
4. Finalisasi tautan hiperteks dan nomor halaman definitif.

### 4.2. Ekspor Alternatif via Pandoc (DOCX / PDF)
Jika penerbit jurnal memerlukan format Microsoft Word (`.docx`):
```bash
pandoc paper/01_introduction.md paper/02_related-works.md ... \
  -o paper_manuscript.docx \
  --bibliography=paper_latex/references.bib \
  --csl=ieee.csl
```
