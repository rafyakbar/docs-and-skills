# Standar Registri Akronim & Kurasi Kata Kunci (Acronym Registry & Keyword Curation Standards)

Berkas rujukan ini mengatur tata kelola akronim di dalam naskah abstrak, sinkronisasi dengan `paper/acronyms.txt`, strategi seleksi kata kunci berdaya temu tinggi, dan pemformatan metadata kepengarangan.

---

## 1. Protokol Akronim dalam Abstrak (Acronym Protocols in the Abstract)

Mengingat abstrak diindeks secara mandiri pada berbagai basis data ilmiah global (seperti IEEE Xplore, Scopus, dan PubMed), penulisan singkatan tunduk pada standar ilmiah yang ketat:

### Aturan Kemunculan Pertama dalam `00_abstract.md` (The First-Mention Rule)
1. **Bentuk Lengkap pada Kemunculan Pertama**: Setiap istilah teknis yang memiliki singkatan atau akronim resmi yang diperkenalkan dalam abstrak **wajib ditulis dalam bentuk lengkap, segera diikuti oleh singkatannya di dalam tanda kurung**:
   * *Contoh*: `Vision Transformer (ViT)`, `Random Forest (RF)`, `Gaussian Naive Bayes (GNB)`, `Logistic Regression (LR)`, `Support Vector Machine (SVM)`, `Grid Search Cross-Validation (GridSearchCV)`.
2. **Penyebutan Berikutnya dalam Abstrak**: Jika istilah yang sama digunakan kembali di dalam paragraf abstrak, gunakan secara konsisten **hanya bentuk singkatannya**.
3. **Pencatatan ke `paper/acronyms.txt`**: Seluruh singkatan yang diperkenalkan di dalam abstrak wajib didaftarkan pada baris-baris teratas berkas registri sentral (`paper/acronyms.txt`) dengan lokasi pengenalan pertama dicatat secara eksplisit sebagai `paper/00_abstract.md (Abstract)`:

```text
====================================================================================================
ACRONYM & ABBREVIATION REGISTRY
Guideline: First-Mention Full Form & Subsequent Acronym Only
File Location: paper/acronyms.txt
====================================================================================================

----------------------------------------------------------------------------------------------------
NO  | ACRONYM / ABBREVIATION | FULL FORM                        | FIRST INTRODUCTION LOCATION
----+------------------------+----------------------------------+-----------------------------------
1   | ViT                    | Vision Transformer               | paper/00_abstract.md (Abstract)
2   | RF                     | Random Forest                    | paper/00_abstract.md (Abstract)
3   | GNB                    | Gaussian Naive Bayes             | paper/00_abstract.md (Abstract)
4   | LR                     | Logistic Regression              | paper/00_abstract.md (Abstract)
5   | SVM                    | Support Vector Machine           | paper/00_abstract.md (Abstract)
6   | GridSearchCV           | Grid Search Cross-Validation     | paper/00_abstract.md (Abstract)
====================================================================================================
```

> [!IMPORTANT]
> Karena istilah yang tercantum pada `00_abstract.md` telah resmi terdaftar di dalam `paper/acronyms.txt`, penulis atau skill penulisan bab hilir (`01_introduction.md`, `02_related-works.md`, `03_materials-and-methods_*.md`, dst.) wajib menggunakan **hanya bentuk akronim/singkatan** tanpa mengulang kepanjangannya kembali di bagian tubuh naskah.

---

## 2. Kurasi Kata Kunci & Kemampuan Temu Balik Pencarian (Keyword Curation & Search Discoverability)

Kata kunci menentukan bagaimana mesin pencari, layanan pengindeksan, dan dewan editor mengelompokkan naskah penelitian. Pemilihan kata kunci yang efektif memaksimalkan peluang sitasi dan temu balik artikel ilmiah.

### Heuristik Pemilihan 5–7 Kata Kunci
1. **Rentang Target**: Sediakan tepat **5 hingga 7 kata kunci berdampak tinggi**, dipisahkan dengan tanda koma.
2. **Komplementaritas Judul (Title Complementarity)**: Hindari duplikasi kata-per-kata dengan judul utama naskah. Apabila judul sudah memuat frasa *"Multi-Domain Vision Transformer Fusion"*, pilihlah kata kunci pelengkap seperti *"algorithmic fairness"*, *"intersectional demographic recognition"*, atau *"latent feature representation"*. Mesin pencari telah mengindeks seluruh kosakata judul; kata kunci komplementer berfungsi memperluas jangkauan penemuan artikel (*search reach*).
3. **Taksonomi Cakupan 5-Tier (The 5-Tier Coverage Taxonomy)**: Kumpulan kata kunci yang tangguh mencakup lima dimensi faset penelitian yang saling melengkapi:
   - **Tier 1 (Domain Masalah / Tugas)**: mis., *Race and gender classification*, *Face recognition*.
   - **Tier 2 (Paradigma Spesifik / Konteks Teoretis)**: mis., *Intersectional demographic recognition*, *Algorithmic fairness*.
   - **Tier 3 (Mekanisme Metodologis Inti)**: mis., *Multi-domain feature fusion*, *Latent representation learning*.
   - **Tier 4 (Arsitektur Komputasi Utama)**: mis., *Vision Transformer*, *Ensemble learning*.
   - **Tier 5 (Fokus Evaluasi / Aplikasi)**: mis., *Benchmarking*, *Subgroup disparity analysis*.
4. **Norma Kapitalisasi**: Awali setiap kata kunci atau frasa dengan huruf kapital (*Title Case*), atau sesuaikan kapitalisasi nama diri dan akronim berdasarkan pedoman jurnal sasaran.

---

## 3. Metadata Penulis & Arsitektur Halaman Depan (Author Metadata & Front Matter Architecture)

Dalam alur kerja naskah modular, berkas `00_abstract.md` berfungsi sebagai dokumen halaman depan induk (*master front matter document*). Susun blok *header* secara terstruktur sebagai berikut:

```markdown
# [Judul Lengkap Naskah: Jelas, Spesifik, dan Informatif]

## Authors & Affiliation

1. **[Nama Lengkap Penulis 1, Gelar]** ([ORCID: 0000-000X-XXXX-XXXX](https://orcid.org/0000-000X-XXXX-XXXX))  
   Departemen Informatika, Fakultas Teknik, Universitas Negeri Surabaya, Surabaya 60231, Indonesia  
   Email Penulis Korespondensi: `penulis1@unesa.ac.id`

2. **[Nama Lengkap Penulis 2, Gelar]** ([ORCID: 0009-000X-XXXX-XXXX](https://orcid.org/0009-000X-XXXX-XXXX))  
   Departemen Informatika, Fakultas Teknik, Universitas Negeri Surabaya, Surabaya 60231, Indonesia

3. **[Nama Lengkap Penulis 3, Gelar]** ([ORCID: 0000-000X-XXXX-XXXX](https://orcid.org/0000-000X-XXXX-XXXX))  
   Departemen Informatika, Fakultas Teknik, Universitas Negeri Surabaya, Surabaya 60231, Indonesia

---

## Abstract

[Satu paragraf kohesif dan padat yang menerapkan kerangka kerja retorika 5 komponen]

---

## Keywords

Kata Kunci 1, Kata Kunci 2, Kata Kunci 3, Kata Kunci 4, Kata Kunci 5.
```

### Standar Metadata
- **Pengenal ORCID**: Diformat sebagai tautan hiperlink Markdown aktif menuju `https://orcid.org/[ID]`.
- **Rincian Afiliasi**: Cantumkan departemen, fakultas, institusi induk, kota, kode pos, dan negara secara lengkap.
- **Penulis Korespondensi (Corresponding Author)**: Nyatakan narahubung utama secara tegas dengan menyertakan alamat email institusional resmi.
