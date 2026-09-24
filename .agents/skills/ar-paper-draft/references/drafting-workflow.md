# Alur Kerja Penulisan Draf Seksi Tunggal & Arsitektur Berkas

Dokumen referensi ini menguraikan prosedur langkah demi langkah untuk menerjemahkan cetak biru (*outline*) per paragraf menjadi berkas Markdown modular, dengan menulis **satu seksi atau subseksi dalam satu waktu**, serta secara tegas menunda penomoran sitasi ke tahapan alur kerja berikutnya.

---

## 1. Disiplin Penulisan Seksi Tunggal (Single-Section Drafting Discipline)

Jangan menulis draf beberapa seksi sekaligus atau menghasilkan seluruh naskah paper dalam satu kali interaksi. Menyusun satu seksi modular dalam satu waktu menjamin:
- **Fokus Analitis Maksimal**: Memungkinkan kepatuhan mendalam terhadap tujuan setiap paragraf dan kebutuhan bukti empiris yang dipersyaratkan.
- **Tinjauan Iteratif Manusia-AI**: Memberi ruang bagi pengguna untuk memeriksa, merevisi, dan menyetujui setiap seksi sebelum melanjutkan ke bab berikutnya.
- **Efisiensi Token & Kendali Mutu**: Mencegah pemotongan konteks (*context truncation*), ketergesa-gesaan luaran, atau kedangkalan kualitas prosa ilmiah.

### Arsitektur Berkas Baku (Canonical File Architecture)
```text
paper/
├── 01_introduction.md
├── 02_related-works.md
├── 03_materials-and-methods_0-overview.md
├── 03_materials-and-methods_a-dataset.md
├── 03_materials-and-methods_b-[primary-method].md
├── 03_materials-and-methods_c-[secondary-models].md
├── 03_materials-and-methods_g-classification-pipeline.md
├── 03_materials-and-methods_h-evaluation-metrics.md
├── 04_results-and-discussion_a-global-performance.md
├── 04_results-and-discussion_b-feature-ablation-study.md
├── 04_results-and-discussion_c-subgroup-analysis.md
├── 04_results-and-discussion_d-error-pattern-assessment.md
├── 04_results-and-discussion_e-comparison-with-prior-studies.md
├── 05_conclusion.md
├── acronyms.txt            (registri terpusat akronim & singkatan teknis)
├── images/                 (diagram skematis, bagan, dan plot visual)
└── references/             (rekaman bibliografi format BibTeX, RIS, atau NBIB)
```

---

## 2. Siklus Penulisan 5 Tahap (Per Seksi Tunggal)

Ketika pengguna menentukan seksi yang akan ditulis (misalnya: *"Tulis 01_introduction.md"* atau *"Tulis subseksi metodologi bagian dataset"*), jalankan siklus 5 tahap berikut:

```
┌─────────────────────────────────────────────────────────┐
│ Tahap 1: Serap Cetak Biru Seksi Spesifik                │
│ • Baca target jumlah kata & sasaran paragraf            │
│ • Identifikasi klaim yang ditugaskan & batasan ruangnya │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ Tahap 2: Tulis Kalimat Ilmiah yang Lugas & Mandiri      │
│ • Rumuskan kalimat topik & argumen berpola CER          │
│ • Pastikan pernyataan tegas, diskret, & terverifikasi   │
│ • JANGAN sisipkan nomor sitasi ([1], [[1]])             │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ Tahap 3: Transisi Antar-Paragraf & Penautan Relatif     │
│ • Hubungkan paragraf dengan jembatan logika yang runtut │
│ • Tambahkan tautan relatif Markdown ke seksi lain       │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ Tahap 4: Audit Mutu Penulisan & Anti-Slop               │
│ • Pindai & bersihkan kata klise AI yang dilarang        │
│ • Terapkan batas tanda baca (em dash ≤ 2 per paper)     │
│ • Periksa variasi ritme panjang kalimat (burstiness)    │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ Tahap 5: Terbitkan Berkas Tunggal & Tunggu Tinjauan     │
│ • Simpan berkas ke path markdown modular yang sesuai    │
│ • Verifikasi jumlah kata terhadap target outline        │
│ • Tunggu inspeksi pengguna sebelum ke seksi berikutnya  │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Perumusan Klaim Tingkat Kalimat (Tegas Tanpa Penomoran Sitasi)

Prinsip fundamental dalam alur kepenulisan riset ini adalah memisahkan secara tegas antara **penulisan draf prosa** (Langkah 1), **pencarian & pemetaan sitasi** (Langkah 2), **kompilasi daftar pustaka** (Langkah 3), dan **penomoran sitasi dalam teks** (Langkah 4).

### Mengapa Penomoran Sitasi Dilarang pada Langkah 1
- **Ketidakstabilan Urutan Nomor (*Unstable Numbering*)**: Jika nomor seperti `[1]`, `[2]`, `[3]` ditetapkan selama penyusunan draf awal, penambahan, penghapusan, atau penataan ulang satu kalimat saja akan langsung merusak urutan numerik di seluruh naskah paper.
- **Presisi Semu (*False Precision*)**: Menghasilkan nomor sitasi buatan atau penanda rujukan spekulatif berisiko menciptakan sitasi fiktif (*phantom citations*).

### Cara Merumuskan Klaim pada Langkah 1
1. **Pernyataan Diskret (*Discrete Assertions*)**: Pastikan setiap kalimat yang membawa klaim empiris atau teoretis dirumuskan sebagai proposisi mandiri yang jelas dan utuh.
   * *Contoh*: *"Kerangka kerja pembelajaran multitugas telah menunjukkan kemampuan dalam memprediksi atribut demografis secara simultan, namun kinerjanya kerap menurun pada kohort interseksional yang granular."*
2. **Kesiapan untuk Langkah 2 (`references.txt`)**: Karena setiap klaim terbatasi dengan rapi di dalam batas kalimatnya, klaim tersebut dapat diekstraksi tanpa hambatan pada Langkah 2 untuk dicari dan diverifikasi sumber literatur pendukungnya:
   ```text
   paper/01_introduction.md: paragraf 2:
   - "Kerangka kerja pembelajaran multitugas telah menunjukkan kemampuan...":
     - paper/references/2023_Facial_attribute_classification.bib
   ```
3. **Penanganan Sumber yang Belum Tersedia**: Jika klaim tertentu pada outline membutuhkan literatur yang belum diidentifikasi, cantumkan penanda celah deskriptif alih-alih nomor angka: `[GAP: butuh sumber untuk atensi transformer pada patch wajah]`.

---

## 4. Protokol Registri Akronim & Singkatan (`acronyms.txt`)

Pada naskah akademik berskala modular, menjaga konsistensi penggunaan singkatan di puluhan berkas terpisah adalah hal yang krusial. Tanpa adanya registri terpusat, penulis sering kali mengekspansi ulang akronim yang sama berulang kali di berbagai bab, atau sebaliknya memunculkan singkatan baru tanpa definisi awal.

### Dua Invarian Utama
1. **Bentuk Lengkap pada Kemunculan Pertama**: Pertama kali suatu akronim muncul di bagian mana pun dalam paper (baik di abstrak, pendahuluan, maupun metodologi), tuliskan nama formal lengkapnya diikuti singkatan di dalam tanda kurung:
   * *Contoh*: `Vision Transformer (ViT)`, `Support Vector Machine (SVM)`, `Multi-Head Self-Attention (MHSA)`.
2. **Hanya Singkatan pada Kemunculan Berikutnya**: Pada seluruh kalimat berikutnya dan di seluruh berkas modular lanjutan, gunakan **hanya bentuk singkatannya secara konsisten**:
   * *Contoh*: `ViT`, `SVM`, `MHSA`.
   * **Jangan pernah mengulang bentuk panjangnya** setelah akronim tersebut resmi tercatat di registri.

### Format Berkas `paper/acronyms.txt`
Pelihara berkas tabel yang terstruktur rapi untuk melacak setiap singkatan yang diperkenalkan:

```text
====================================================================================================
REGISTRI AKRONIM & SINGKATAN TEKNIS
Panduan: Bentuk Lengkap pada Kemunculan Pertama & Hanya Akronim pada Kemunculan Berikutnya
Lokasi Berkas: paper/acronyms.txt
====================================================================================================

Petunjuk:
1. Istilah yang telah tercatat dalam registri ini TIDAK BOLEH diekspansi ulang bentuk lengkapnya pada
   berkas draf markdown berikutnya (gunakan hanya bentuk singkatannya).
2. Ketika memperkenalkan istilah teknis baru dengan singkatan resmi untuk pertama kalinya dalam draf,
   tuliskan bentuk lengkapnya diikuti singkatan dalam kurung, lalu segera catat di bawah ini.

----------------------------------------------------------------------------------------------------
NO  | AKRONIM / SINGKATAN    | BENTUK LENGKAP                   | LOKASI KEMUNCULAN PERTAMA
----+------------------------+----------------------------------+-----------------------------------
1   | ViT                    | Vision Transformer               | paper/00_abstract.md (Abstract)
2   | RF                     | Random Forest                    | paper/00_abstract.md (Abstract)
3   | SVM                    | Support Vector Machine           | paper/00_abstract.md (Abstract)
4   | CNN                    | Convolutional Neural Networks    | paper/01_introduction.md (P3)
5   | MHSA                   | Multi-Head Self-Attention        | paper/01_introduction.md (P3)
6   | PCA                    | Principal Component Analysis     | paper/01_introduction.md (P5)
====================================================================================================
```

### Integrasi Siklus Hidup dalam Penulisan Seksi Tunggal
- **Sebelum Menulis**: Agen memeriksa `paper/acronyms.txt` (jika ada) untuk memastikan istilah apa saja yang sudah terdaftar.
- **Saat Menulis**: Agen menggunakan bentuk singkatan saja untuk istilah yang sudah terdaftar. Apabila muncul istilah teknis baru yang belum terdaftar, agen menuliskan `Bentuk Lengkap (SINGKATAN)`.
- **Setelah Menulis**: Agen memperbarui atau membuat berkas `paper/acronyms.txt` dengan mencatat istilah baru beserta lokasi paragraf spesifiknya.

---

## 5. Pemantauan & Kepatuhan Alokasi Jumlah Kata

Setiap berkas seksi yang ditulis harus memantau akumulasi jumlah katanya terhadap alokasi anggaran yang ditetapkan dalam cetak biru outline:

| Seksi | Persentase Tipikal Target | Contoh Alokasi (Paper 6.000 Kata) |
|:---|:---:|:---:|
| **01_introduction.md** | 12% – 16% | 750 – 950 kata |
| **02_related-works.md** | 12% – 18% | 700 – 1.000 kata |
| **03_materials-and-methods (seluruh bagian)** | 25% – 32% | 1.500 – 1.900 kata |
| **04_results-and-discussion (seluruh bagian)** | 30% – 38% | 1.800 – 2.300 kata |
| **05_conclusion.md** | 5% – 8% | 300 – 500 kata |

- **Batas Toleransi**: Pertahankan jumlah kata aktual dalam rentang $\pm 10\%$ dari target anggaran outline paragraf.
- Apabila suatu seksi melebihi batas toleransi, pangkas kata keterangan yang redundan dan eliminasi frasa basa-basi daripada membuang rincian teknis penting.
