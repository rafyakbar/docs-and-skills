---
name: ar-paper-latex-converter
description: Aktifkan ketika pengguna meminta untuk mengonversi draf naskah paper akademik Markdown (paper/*.md) ke dalam dokumen publikasi LaTeX modular siap submit (IEEE Access, IEEEtran, Springer LNCS, ACM, atau generic article), menata aset gambar dan basis data BibTeX (references.bib), membersihkan penanda blok revisi (<!--block:BNNNN-->), serta memverifikasi integritas tipografi jurnal ilmiah. Kata kunci pemicu: convert to latex, konversi latex, buat file tex, compile latex, latex converter, markdown to latex, format convert, export latex, ar-paper-latex-converter, ars-format-convert. JANGAN aktifkan untuk penulisan draf bab paper (gunakan ar-paper-draft), pembuatan outline (gunakan ar-paper-outline), kompilasi daftar pustaka (gunakan ar-paper-reference-compiler), penomoran sitasi naskah (gunakan ar-paper-citation-numbering), simulasi peer review (gunakan ar-paper-reviewer), eksekusi patch revisi (gunakan ar-paper-revision), atau audit surat tanggapan (gunakan ar-paper-rebuttal-audit).
---

# Panduan Skill: ar-paper-latex-converter

Skill ini mengatur konversi naskah paper akademik berbasis Markdown modular (`paper/*.md`) ke dalam proyek **LaTeX modular siap submit** sesuai standar publikasi jurnal internasional (Fase 16 / Kluster D siklus riset akademik).

---

## 1. Aturan Mutlak (*Iron Rules*)

1. **Arsitektur Seksi Modular 1:1 (*Modular Section Architecture*)**:
   - Setiap berkas Markdown (`00_abstract.md`, `01_introduction.md`, dst.) dikonversi menjadi berkas `.tex` tersendiri di subdirektori `sections/`.
   - Dokumen induk (`access.tex` atau `main.tex`) mengorkestrasi seluruh seksi menggunakan perintah `\input{sections/...}`. Dilarang menggabungkan seluruh naskah ke dalam satu berkas monolitik raksasa.
2. **Aturan Pembersihan Bersih (*Clean Stripping Rule*)**:
   - Wajib membersihkan seluruh penanda blok revisi `<!--block:BNNNN-->`, komentar HTML `<!-- ... -->`, dan tag jangkar `<a id="..."></a>`.
   - Tautan internal Markdown seperti `[Figure 1](#fig1)` atau `[Table IV](#tab4)` diubah menjadi format perujukan formal `Figure~\ref{fig:1}` dan `Table~\ref{tab:IV}`.
3. **Urutan Wajib Caption Sebelum Label (*Caption-Before-Label Order*)**:
   - Pada seluruh lingkungan visual (`figure`, `figure*`, `table`, `table*`), perintah `\caption{...}` **WAJIB diletakkan SEBELUM** `\label{...}`.
   - Penempatan terbalik dilarang keras karena menyebabkan nomor referensi salah menunjuk ke nomor seksi bab.
4. **Aturan Tanpa-Yatim (*Zero-Orphan Cross-Referencing*)**:
   - Setiap gambar (`\label{fig:...}`), tabel (`\label{tab:...}`), dan persamaan (`\label{eq:...}`) wajib dirujuk di dalam paragraf naskah (`Figure~\ref{...}`, `Table~\ref{...}`, `\eqref{...}`).
   - Seluruh entri di `references.bib` wajib disitasi dengan `\cite{...}`.
5. **Penempatan Sitasi Sebelum Tanda Baca (*Pre-Punctuation Citation Placement*)**:
   - Nomor sitasi wajib diletakkan **sebelum** titik atau koma (misal: `... in recent studies \cite{ref1}, \cite{ref2}.`). Dilarang meletakkan sitasi setelah titik atau koma.
6. **Higienitas Karakter & Tipografi (*Character & Typography Hygiene*)**:
   - **Larangan Em Dash**: Karakter em dash (`—`) dilarang keras pada naskah LaTeX. Gunakan tanda hubung standar (`-`) atau kurung.
   - **Tabel Booktabs**: Seluruh tabel wajib menggunakan paket `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) tanpa garis kisi vertikal (`|`).
   - **English Title Case**: Seluruh judul artikel (`\title`), judul seksi (`\section`, `\subsection`), serta caption gambar dan tabel wajib ditulis dalam English Title Case.

---

## 2. Struktur Proyek LaTeX yang Dihasilkan

```
paper_latex/
├── access.tex / main.tex            # Dokumen induk orkestrator naskah
├── references.bib                   # Basis data bibliografi BibTeX
├── conversion_report.json           # Laporan rekapitulasi konversi
├── ieeeaccess.cls / IEEEtran.cls    # Berkas kelas template penerbit
├── images/                          # Seluruh aset gambar dan pasfoto
│   ├── overview.png
│   ├── author_ricky.jpg
│   └── ...
└── sections/                        # Berkas seksi modular 1:1
    ├── 00_title.tex                 # Metadata judul, penulis, afiliasi, grant
    ├── 00_abstract.tex              # Lingkungan abstract dan keywords
    ├── 01_introduction.tex          # Bab 1 Introduction
    ├── 02_related-works.tex         # Bab 2 Related Works
    ├── 03_materials-and-methods_*.tex
    ├── 04_results-and-discussion_*.tex
    ├── 05_conclusion.tex            # Bab 5 Conclusion
    └── 07_biographies.tex           # Biografi akademik berfoto IEEEbiography
```

---

## 3. Alur Kerja Konversi 4 Tahap (*4-Stage Conversion Workflow*)

### Tahap 1: Analisis & Validasi Direktori Masukan
- Periksa kelengkapan berkas sumber di folder `paper/` (`*.md`, `references/`, `images/`).
- Identifikasi template penerbit target (`ieeeaccess`, `ieeetran`, `springer`, atau `article`).

### Tahap 2: Eksekusi Konversi Deterministik
Jalankan skrip konversi mesin:
```bash
python scripts/ars_latex_converter.py \
  --paper-dir paper \
  --output-dir paper_latex \
  --template ieeeaccess
```
Mesin konversi akan:
1. Menyalin dan menata aset grafis ke `paper_latex/images/`.
2. Menggabungkan seluruh berkas `.bib` di `paper/references/` menjadi `references.bib`.
3. Mengonversi tabel Markdown menjadi tabel `booktabs` ilmiah (`table` atau `table*`).
4. Mengonversi gambar Markdown menjadi lingkungan `figure` atau `figure*` dengan caption di atas label.
5. Mengonversi rumus display math `$$ ... \tag{X} $$` menjadi `\begin{equation} ... \label{eq:X}`.
6. Memproduksi berkas seksi modular di `paper_latex/sections/` dan berkas induk `access.tex`.

### Tahap 3: Verifikasi Integritas Linter LaTeX
Jalankan skrip verifikasi:
```bash
python scripts/verify_latex_integrity.py paper_latex
```
Kriteria Kelulusan Mutu (*Pass Criteria*):
- `errors == 0` (Nol pelanggaran sintaks atau urutan label).
- Tidak ada em dash (`—`).
- Seluruh berkas `\input{sections/...}` terverifikasi ada dan valid.
- Seluruh lingkungan `\begin` tertutup rapi oleh `\end`.

### Tahap 4: Kompilasi Dokumen Akhir (Opsional)
Jalankan kompilasi pdfLaTeX di terminal:
```bash
pdflatex access.tex && bibtex access && pdflatex access.tex && pdflatex access.tex
```

---

## 4. Referensi Pendukung (*References Guide*)

Bila membutuhkan panduan mendalam untuk konfigurasi template tertentu, rujuk berkas di `references/`:
- [latex_conversion_framework.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/latex_conversion_framework.md): Arsitektur modular 1:1, tata kelola aset grafis, dan opsi ekspor Pandoc.
- [ieee_access_and_ieee_tran_guide.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/ieee_access_and_ieee_tran_guide.md): Panduan resmi IEEE Access dan IEEEtran, makro link biru, kurung siku interaktif, `\EOD`, dan biografi.
- [springer_acm_generic_templates_guide.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/springer_acm_generic_templates_guide.md): Panduan Springer Nature (`sn-jnl`), ACM (`acmart`), generic article, dan XeLaTeX CJK.
- [table_figure_math_formatting_handbook.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/table_figure_math_formatting_handbook.md): Aturan tabel booktabs, posisi caption sebelum label, subfigures, dan penjelasan simbol rumus.
- [sample_latex_conversion_package.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/sample_latex_conversion_package.md): Contoh lengkap masukan, berkas `.tex` keluaran, laporan JSON, dan hasil linter lolos.
