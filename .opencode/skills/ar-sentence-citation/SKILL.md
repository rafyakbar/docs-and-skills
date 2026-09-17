---
name: ar-sentence-citation
description: "Aktifkan ketika pengguna meminta untuk mencari, mengurasi, atau memetakan sitasi literatur ilmiah per kalimat (sentence-level citation) berdasarkan draf naskah paper untuk menyusun berkas paper/references.txt dan mengunduh rekaman bibliografi (.bib, .ris, .nbib) ke dalam paper/references/. Mencakup ekstraksi klaim per kalimat, perumusan query pencarian akademis, verifikasi reputasi sumber (Scopus, WoS, IEEE, PubMed, arXiv), standardisasi penamaan file bibliografi [Tahun]_[Judul].[ext], dan penyusunan berkas pemetaan paper/references.txt. Kata kunci pemicu: cari sitasi, sitasi per kalimat, references.txt, sentence citation, mapping sitasi, cari referensi klaim, kurasi sitasi. JANGAN aktifkan untuk menulis draf naskah (gunakan ar-paper-draft), menyusun naskah 06_references.md (gunakan ar-reference-compiler), atau penomoran sitasi teks (gunakan ar-citation-numbering)."
license: MIT
metadata:
  author: Rafy
---

# Kurasi Sitasi Per Kalimat & Pemetaan Referensi (Sentence-Level Citation Mapping)

## Gambaran Umum (Overview)

Skill ini menjalankan proses **pencarian, kurasi, dan pemetaan sitasi ilmiah granular pada tingkat kalimat** (*sentence-level citation grounding*). Setelah draf bab naskah ditulis (menggunakan `ar-paper-draft`), skill ini membedah paragraf demi paragraf, mengidentifikasi setiap kalimat yang memuat klaim faktual, temuan terdahulu, atau metodologi, mencari literatur ilmiah bereputasi pendukungnya, menyimpan berkas rekaman bibliografi (`.bib`, `.ris`, `.nbib`) ke folder `paper/references/`, dan menyusun berkas pemetaan terstruktur `paper/references.txt`.

> [!NOTE]
> **Fokus Khusus Step 2**
> Skill ini hanya bertugas memetakan kalimat ke berkas referensi pada `paper/references.txt`. Skill ini **TIDAK melakukan penomoran sitasi pada teks draf** (penomoran braket `[[1]](06_references.md#ref1)` dilakukan pada Step 4) dan **TIDAK menyusun naskah daftar pustaka akhir** (penyusunan `06_references.md` dilakukan pada Step 3).

## Kapan Mengaktifkan Skill Ini

- Pengguna meminta untuk mencari atau mengurasi sitasi per kalimat untuk draf naskah (misal: *"Cari sitasi untuk draf 01_introduction.md"* atau *"Petakan referensi ke references.txt"*).
- Pengguna meminta untuk membuat atau memperbarui berkas pemetaan `paper/references.txt`.
- Pengguna meminta mengumpulkan dan mengunduh berkas catatan bibliografi (`.bib`, `.ris`, `.nbib`) ke direktori `paper/references/`.
- Kata kunci pemicu: `cari sitasi`, `sitasi per kalimat`, `references.txt`, `sentence citation`, `mapping sitasi`, `cari referensi klaim`, `kurasi sitasi`.

## Kapan TIDAK Mengaktifkan Skill Ini

- Menulis draf teks kalimat atau menyusun naskah bab dari outline (gunakan `ar-paper-draft` / Step 1).
- Merancang garis besar atau blueprint paragraf dari nol (gunakan `ar-paper-outline` / Step 0).
- Menyusun atau mengompilasi naskah daftar pustaka akhir `06_references.md` (gunakan `ar-reference-compiler` / Step 3).
- Memberikan penomoran angka sitasi dan penautan tautan markdown `[[1]]` pada teks bab (gunakan `ar-citation-numbering` / Step 4).
- Membuat atau menyunting ringkasan abstrak paper `00_abstract.md` (gunakan `ar-paper-abstract` / Step 5).

## Ruang Lingkup (Scope)

- **Dalam Lingkup:** Ekstraksi kalimat klaim per paragraf dari berkas draf (`01_introduction.md` s.d. `05_conclusion.md`), perumusan kueri pencarian ilmiah, verifikasi reputasi sumber (Scopus, WoS, IEEE, PubMed, arXiv), penyimpanan berkas catatan bibliografi berformat `[Tahun]_[Judul].[ext]`, dan penyusunan hierarkis berkas `paper/references.txt`.
- **Luar Lingkup:** Menulis nomor sitasi ke dalam teks draf, menyusun teks daftar pustaka IEEE/APA, atau mengarang sitasi palsu (*phantom citations*).

---

## Langkah Wajib 0: Verifikasi Input & Ruang Lingkup

Sebelum memulai pencarian sitasi, pastikan parameter berikut terdefinisi:

1. **Berkas Draf Target**: Konfirmasi berkas draf mana yang hendak diproses (misal: `paper/01_introduction.md` atau `paper/02_related-works.md`). Lakukan secara modular berkas per berkas.
2. **Ketersediaan Folder Referensi**: Pastikan direktori `paper/references/` siap digunakan untuk menyimpan file `.bib`, `.ris`, atau `.nbib`.
3. **Kriteria Seleksi Sumber**: Utamakan paper jurnal/konferensi bereputasi terindeks (Scopus/WoS) terbitan 3–5 tahun terakhir (misal 2021–2026), kecuali paper fundamental.
4. **Target Kepadatan**: 1 hingga 2 rujukan per kalimat klaim (maksimal 3 rujukan jika merangkum variasi arah riset).

---

## Arsitektur Berkas Sitasi Modular

Struktur penempatan berkas sitasi pada direktori riset adalah sebagai berikut:

```text
paper/
├── 01_introduction.md                         # Draf teks per section (tanpa nomor sitasi)
├── 02_related-works.md
├── references.txt                             # Master mapping: kalimat draf -> berkas rujukan
└── references/                                # Kumpulan berkas catatan bibliografi primer
    ├── 2021_Privacy–Enhancing Face Biometrics A Comprehensive Survey.bib
    ├── 2022_A comprehensive survey on techniques to handle face identity threats.ris
    ├── 2022_Automatic Ethnicity Classification Using CNN.bib
    ├── 2022_The unseen Black faces of AI algorithms.nbib
    └── 2023_A Multidimensional Analysis of Social Biases in Vision Transformers.bib
```

---

## Protokol Eksekusi Kurasi Sitasi

### 1. Ekstraksi Klaim Kalimat
Baca naskah draf paragraf per paragraf. Ekstrak kalimat yang memenuhi syarat wajib sitasi:
- Pernyataan fakta empiris atau data disparitas domain.
- Pernyataan mengenai capaian, kelemahan, atau mekanisme model terdahulu.
- Pernyataan kesenjangan literatur (*literature gaps*).
- Metode komputasi, algoritma, atau pipeline evaluasi baku (misal: *Stratified Cross-Validation*, *GridSearchCV*).

*(Catatan: Kalimat yang memuat kontribusi penelitian sendiri atau sistematika penulisan naskah/roadmap TIDAK memerlukan sitasi).*

### 2. Pencarian Akademis & Pengambilan Metadata
- Formulasikan kueri pencarian berdasarkan kata kunci teknis utama pada kalimat klaim.
- Cari melalui repositori ilmiah resmi (Crossref, Semantic Scholar, arXiv, IEEE Xplore, PubMed).
- Dapatkan metadata bibliografi resmi lengkap dengan judul asli, penulis, tahun, nama jurnal/prosiding, volume, nomor, halaman, dan DOI resmi.

### 3. Standardisasi Penamaan Berkas Bibliografi
Simpan metadata rujukan ke dalam direktori `paper/references/` dengan konvensi penamaan:
```text
paper/references/[Tahun]_[Judul Paper Lengkap atau Ringkas].[bib|ris|nbib]
```
- Hindari karakter ilegal sistem operasi (`:`, `*`, `?`, `"`, `<`, `>`, `|`). Gantikan dengan spasi atau tanda strip `-`.
- Pastikan isi berkas bibliografi memuat field minimal: `AUTHOR`, `TITLE`, `JOURNAL` (atau `BOOKTITLE`), `YEAR`, dan `DOI`.

### 4. Penyusunan Berkas Pemetaan `paper/references.txt`
Susun atau perbarui `paper/references.txt` dengan format hierarkis:
```text
paper/[nama-berkas].md: paragraf [X]:
- "[Kutipan teks kalimat klaim persis dari draf]":
  - paper/references/[Tahun]_[Judul Paper 1].[ext]
  - paper/references/[Tahun]_[Judul Paper 2].[ext]
- "[Kutipan teks kalimat klaim berikutnya]":
  - paper/references/[Tahun]_[Judul Paper 3].[ext]
```
- **Teks Kalimat Persis**: Kalimat di dalam tanda kutip wajib sama persis dengan kalimat yang tertulis di draf markdown untuk memfasilitasi otomatisasi penomoran di Step 4.

---

## Panduan Do and Don't

| Do | Don't |
|:---|:---|
| Ekstrak kalimat secara utuh dan persis sesuai berkas draf | Mengubah susunan kata kalimat saat memetakan ke `references.txt` |
| Pastikan paper rujukan benar-benar memvalidasi isi klaim kalimat | Mencocokkan paper hanya berdasarkan kemiripan judul tanpa membaca abstrak |
| Simpan berkas catatan bibliografi dengan format `[Tahun]_[Judul].[ext]` | Menyimpan file referensi dengan nama acak atau tidak beraturan |
| Prioritaskan publikasi jurnal/prosiding bereputasi 3–5 tahun terakhir | Menggunakan blog pribadi, forum diskusi, atau jurnal predator |
| Batasi 1–3 rujukan per kalimat klaim secara proporsional | Melakukan *citation dumping* (>3 rujukan pada satu klaim tunggal) |
| Kerjakan kurasi secara modular berkas per berkas | Memproses seluruh bab paper sekaligus secara terburu-buru |
| Biarkan teks draf tetap bersih tanpa nomor sitasi braket `[1]` | Memasukkan nomor sitasi ke dalam draf naskah pada tahap ini |

---

## Skrip Pembantu CLI (Helper Scripts)

Untuk mempercepat otomatisasi deteksi dan verifikasi sitasi secara deterministik tanpa dependensi eksternal (menggunakan pustaka standar Python), skill ini menyediakan sekumpulan skrip pada direktori `scripts/`:

1. **Deteksi Klaim Tanpa Sitasi**:
   ```bash
   python scripts/uncited_assertion_detector.py paper/01_introduction.md
   python scripts/uncited_assertion_detector.py --text "Baseline kami menghasilkan akurasi 94.2%."
   ```
2. **Kueri & Verifikasi API Crossref**:
   ```bash
   python scripts/crossref_client.py --doi "10.1145/3375627.3375820" --title "Expected Title"
   python scripts/crossref_client.py --title "Attention Is All You Need" --year 2017
   ```
3. **Kueri & Verifikasi API Semantic Scholar**:
   ```bash
   python scripts/semantic_scholar_client.py --doi "10.1145/3375627.3375820"
   python scripts/semantic_scholar_client.py --title "Attention Is All You Need"
   ```
4. **Kueri & Verifikasi API OpenAlex**:
   ```bash
   python scripts/openalex_client.py --title "BERT: Pre-training of Deep Bidirectional Transformers"
   ```
5. **Kueri & Verifikasi API arXiv**:
   ```bash
   python scripts/arxiv_client.py --id "1706.03762" --title "Attention Is All You Need"
   ```
6. **Triangulasi Verifikasi Multi-Indeks**:
   ```bash
   python scripts/citation_verification_summary.py '{"crossref": {"status": "matched"}, "arxiv": {"status": "skipped"}}'
   ```

---

Untuk panduan mendalam, protokol teknis, dan standar referensi lengkap, pelajari berkas-berkas rujukan berikut:

### Alur Kerja & Pemetaan Sitasi
- `references/sentence_citation_workflow.md`: Siklus 5 tahap kurasi, klasifikasi proposisi kalimat, formulasi kueri pencarian, dan sintaks pemetaan `references.txt`.
- `references/sample_references_mapping.md`: Contoh konkret hierarki master mapping `paper/references.txt` beserta sampel berkas `.bib` dan `.ris`.
- `references/uncited_assertion_detector.md`: Aturan Tiga Kondisi (*Three-Condition Rule*), kamus penanda empiris/kuantitatif, verba fakta, dan skema deteksi klaim tanpa sitasi.

### Protokol Kueri API & Triangulasi Multi-Indeks
- `references/crossref_api_protocol.md`: Kueri DOI primer, pencarian judul cadangan, Levenshtein title cross-check $\ge 0.70$, dan etiket polite pool.
- `references/semantic_scholar_api_protocol.md`: Kueri Semantic Scholar Graph API, ekstraksi metadata, pencocokan skor kemiripan, dan deduplikasi Paper ID.
- `references/openalex_api_protocol.md`: Kueri OpenAlex catalog sains terbuka, penanganan kuota harian freemium, dan mitigasi kepalsuan positif.
- `references/arxiv_api_protocol.md`: Kueri Atom XML feed arXiv, pembatasan ketat ToU 1 request/3 detik, dan aturan gating berbasis ketersediaan ID.

### Standar Kualitas Bukti & Profil Disiplin
- `references/source_quality_hierarchy.md`: Piramida bukti 7 tingkat, rubrik penilaian mutu A–F, aturan agregasi integritas dasar, dan checklist jurnal predator.
- `references/domain_evidence_profiles.md`: Standar keberterimaan bukti per disiplin (`cs_ml`, `clinical_health`, `general_social_science`, `humanities`), aturan inklusi aditif, dan akseptabilitas naskah pra-cetak.

### Spesifikasi & Logika Kerja Agen Ahli
- `references/bibliography_agent.md`: Prosedur penelusuran literatur sistematis, strategi boolean, penyaringan dua putaran (*two-pass screening*), dan deduplikasi.
- `references/source_verification_agent.md`: Prosedur pengujian keabsahan rujukan (Tier 0–2), deteksi `DOI_MISMATCH`, audit red flags halusinasi, dan konflik kepentingan.
- `references/citation_compliance_agent.md`: Protokol audit integritas segitiga (draf klaim $\leftrightarrow$ `references.txt` $\leftrightarrow$ `paper/references/`), skrining artikel ditarik (*Retraction Watch*), dan pohon keputusan distorsi klaim.
- `references/literature_strategist_agent.md`: Dekonstruksi konsep kueri, pemilihan basis data spesifik disiplin, dan penyusunan matriks sintesis literatur.
