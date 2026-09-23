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
   - Dokumen induk (`access.tex` untuk IEEE Access atau `main.tex` untuk IEEEtran, Springer, ACM, dan generic article) mengorkestrasi seluruh seksi menggunakan perintah `\input{sections/...}`. Dilarang menggabungkan seluruh naskah ke dalam satu berkas monolitik raksasa.
2. **Aturan Pembersihan Bersih (*Clean Stripping Rule*)**:
   - Wajib membersihkan seluruh penanda blok revisi `<!--block:BNNNN-->`, komentar HTML `<!-- ... -->`, dan tag jangkar `<a id="..."></a>`.
   - Tautan internal Markdown seperti `[Figure 1](#fig1)` atau `[Table 1](#tab1)` diubah menjadi format perujukan formal `Figure~\ref{fig:1}` dan `Table~\ref{tab:1}` (angka Arab terharmonisasi).
3. **Urutan Wajib Caption Sebelum Label (*Caption-Before-Label Order*)**:
   - Pada seluruh lingkungan visual (`figure`, `figure*`, `table`, `table*`), perintah `\caption{...}` **WAJIB diletakkan SEBELUM** `\label{...}`.
   - Penempatan terbalik dilarang keras karena menyebabkan nomor referensi salah menunjuk ke nomor seksi bab.
4. **Aturan Tanpa-Yatim (*Zero-Orphan Cross-Referencing*)**:
   - Setiap gambar (`\label{fig:...}`), tabel (`\label{tab:...}`), dan persamaan (`\label{eq:...}`) wajib dirujuk di dalam paragraf naskah (`Figure~\ref{...}`, `Table~\ref{...}`, `\eqref{...}`).
   - Seluruh entri di `references.bib` wajib disitasi dengan `\cite{...}`. Seluruh sitasi in-text wajib memiliki entri padanan di `references.bib`.
5. **Penempatan Sitasi Sebelum Tanda Baca (*Pre-Punctuation Citation Placement*)**:
   - Nomor sitasi wajib diletakkan **sebelum** titik atau koma (misal: `... in recent studies \cite{ref1}, \cite{ref2}.`). Dilarang meletakkan sitasi setelah titik atau koma.
6. **Higienitas Karakter & Tipografi (*Character & Typography Hygiene*)**:
   - **Sanitasi Karakter Khusus**: Karakter `%`, `_`, `&`, `#` di luar mode math dan verbatim wajib di-escape (`\%`, `\_`, `\&`, `\#`) agar persentase `95%` tidak terpotong sebagai komentar dan identifier seperti `DemogPairs_v1` tidak memicu crash kompilasi.
   - **Larangan Em Dash**: Karakter em dash (`—`) dilarang keras pada naskah LaTeX. Gunakan tanda hubung standar (`-`) atau kurung.
   - **Tabel Booktabs**: Seluruh tabel wajib menggunakan paket `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) tanpa garis kisi vertikal (`|`). Penomoran tabel distandarisasikan dengan angka Arab (`\label{tab:1}`).
   - **English Title Case**: Seluruh judul artikel (`\title`), judul seksi (`\section`, `\subsection`), serta caption gambar dan tabel wajib ditulis dalam English Title Case.
7. **Dukungan Kode & Pengecualian Berkas Non-Naskah**:
   - Fenced code block (```lang ... ```) dikonversi ke lingkungan `\begin{verbatim} ... \end{verbatim}` dan inline backticks (`` `code` ``) dikonversi ke `\texttt{code}`.
   - Berkas non-naskah seperti `07_editorial_decision.md`, `08_revision_roadmap.md`, `09_response_letter.md`, dan `cover_letter.md` secara otomatis dikecualikan dari konversi naskah.

---

## 2. Struktur Proyek LaTeX yang Dihasilkan

```
paper_latex/
├── access.tex / main.tex            # Dokumen induk orkestrator (access.tex khusus ieeeaccess; main.tex untuk ieeetran, springer, acm, article)
├── references.bib                   # Basis data bibliografi BibTeX (tersinkronisasi 100% dengan paper/references.txt)
├── conversion_report.json           # Laporan rekapitulasi konversi
├── ieeeaccess.cls / IEEEtran.cls    # Berkas kelas template penerbit (bila tersedia)
├── images/                          # Seluruh aset gambar dan pasfoto
│   ├── overview.png
│   ├── author_ricky.jpg
│   └── ...
└── sections/                        # Berkas seksi modular 1:1
    ├── 00_title.tex                 # Metadata judul, penulis, afiliasi, grant
    ├── 00_abstract.tex              # Lingkungan abstract dan keywords/index terms
    ├── 01_introduction.tex          # Bab 1 Introduction
    ├── 02_related-works.tex         # Bab 2 Related Works
    ├── 03_materials-and-methods_*.tex
    ├── 04_results-and-discussion_*.tex
    ├── 05_conclusion.tex            # Bab 5 Conclusion
    └── 07_biographies.tex           # Biografi akademik berfoto IEEEbiography (IEEE)
```

---

## 3. Alur Kerja Konversi 4 Tahap (*4-Stage Conversion Workflow*)

### Tahap 1: Analisis & Validasi Direktori Masukan
- Periksa kelengkapan berkas sumber di folder `paper/` (`*.md`, `references/`, `images/`).
- Identifikasi template penerbit target (`ieeeaccess`, `ieeetran`, `springer`, `acm`, atau `article`).

### Tahap 2: Eksekusi Konversi Deterministik
Jalankan skrip konversi mesin:
```bash
# Contoh untuk IEEE Access:
python scripts/ars_latex_converter.py \
  --paper-dir paper \
  --output-dir paper_latex \
  --template ieeeaccess

# Contoh untuk ACM Conference:
python scripts/ars_latex_converter.py \
  --paper-dir paper \
  --output-dir paper_latex \
  --template acm
```
Mesin konversi akan:
1. Menyalin dan menata aset grafis ke `paper_latex/images/`.
2. Membaca urutan rujukan dari `paper/references.txt`, mengonversi berkas `.bib`, `.ris`, atau `.nbib`, dan menyinkronkan kunci sitasi (`ref1`, `ref2`, dst.) ke `references.bib`.
3. Mengonversi tabel Markdown menjadi tabel `booktabs` ilmiah (`table` atau `table*`) dengan label angka Arab harmonis (`\label{tab:1}`).
4. Mengonversi gambar Markdown menjadi lingkungan `figure` atau `figure*` dengan caption di atas label.
5. Mengonversi rumus display math `$$ ... \tag{X} $$` menjadi `\begin{equation} ... \label{eq:X}`.
6. Memproduksi berkas seksi modular di `paper_latex/sections/` dan berkas induk (`access.tex` untuk `ieeeaccess`, `main.tex` untuk template lainnya).

### Tahap 3: Verifikasi Integritas Linter LaTeX
Jalankan skrip verifikasi:
```bash
python scripts/verify_latex_integrity.py paper_latex
```
Kriteria Kelulusan Mutu (*Pass Criteria*):
- `errors == 0` (Nol pelanggaran sintaks, urutan label, karakter non-higienis, atau sitasi tanpa entri BibTeX).
- Tidak ada em dash (`—`) dan karakter khusus (`%`, `_`, `&`, `#`) ter-escape dengan benar di luar math mode.
- Seluruh berkas `\input{sections/...}` terverifikasi ada dan valid.
- Seluruh lingkungan `\begin` tertutup rapi oleh `\end`.
- Setiap sitasi in-text `\cite{refN}` terdaftar pada `references.bib`.

### Tahap 4: Kompilasi Dokumen Akhir (Opsional)
Jalankan kompilasi pdfLaTeX di terminal sesuai nama master file:
```bash
# Template IEEE Access:
pdflatex access.tex && bibtex access && pdflatex access.tex && pdflatex access.tex

# Template Lainnya (IEEEtran, Springer, ACM, Article):
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

---

## 4. Referensi Pendukung (*References Guide*)

Bila membutuhkan panduan mendalam untuk konfigurasi template tertentu, rujuk berkas di `references/`:
- [latex_conversion_framework.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/latex_conversion_framework.md): Arsitektur modular 1:1, tata kelola aset grafis, dan opsi ekspor Pandoc.
- [ieee_access_and_ieee_tran_guide.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/ieee_access_and_ieee_tran_guide.md): Panduan resmi IEEE Access dan IEEEtran, makro link biru, kurung siku interaktif, `\EOD`, dan biografi.
- [springer_acm_generic_templates_guide.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/springer_acm_generic_templates_guide.md): Panduan Springer Nature (`sn-jnl`), ACM (`acmart`), generic article, dan XeLaTeX CJK.
- [table_figure_math_formatting_handbook.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/table_figure_math_formatting_handbook.md): Aturan tabel booktabs, posisi caption sebelum label, subfigures, dan penjelasan simbol rumus.
- [sample_latex_conversion_package.md](file:///D:/Code/docs-and-skills/skills/ar-paper-latex-converter/references/sample_latex_conversion_package.md): Contoh lengkap masukan, berkas `.tex` keluaran, laporan JSON, dan hasil linter lolos.
