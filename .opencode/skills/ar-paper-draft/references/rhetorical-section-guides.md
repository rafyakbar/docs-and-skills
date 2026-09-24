# Panduan Retorika Seksi untuk Penulisan Draf Paper Akademik

Dokumen referensi ini menyediakan cetak biru retorika, tahapan fungsional (*functional moves*), serta konvensi penulisan prosa akademik untuk menyusun bab-bab utama naskah ilmiah berdasarkan outline tingkat paragraf.

---

## 1. Seksi Pendahuluan (Model CARS Swales / Create A Research Space)

Seksi Pendahuluan harus mampu meyakinkan pembaca akademik bahwa domain riset yang diangkat sangat krusial, terdapat celah (*gap*) atau pertentangan nyata yang belum terselesaikan, dan penelitian ini hadir untuk menjembatani celah tersebut. Terapkan model **Create A Research Space (CARS)** dari John Swales melalui tiga tahapan retorika (*rhetorical moves*):

```
┌───────────────────────────────────────────────────────────┐
│ Move 1: Membangun Teritori Riset (Establish Territory)    │
│ • Nyatakan urgensi domain & signifikansi ilmiah/praktis   │
│ • Tinjau literatur fundamental & praktik umum yang ada    │
└─────────────────────────────┬─────────────────────────────┘
                              ▼
┌───────────────────────────────────────────────────────────┐
│ Move 2: Menetapkan Celah Riset (Establish Niche / Pivot)  │
│ • Identifikasi celah empiris/teoretis/metodologis spesifik│
│ • Paparkan batasan pendekatan terdahulu atau konflik data │
└─────────────────────────────┬─────────────────────────────┘
                              ▼
┌───────────────────────────────────────────────────────────┐
│ Move 3: Mengisi Celah Riset (Occupy Niche)                │
│ • Nyatakan pendekatan, kerangka kerja, atau tesis usulan  │
│ • Rincikan kontribusi ilmiah yang eksplisit & tak tumpang │
│ • Sajikan peta jalan organisasional naskah (roadmap)      │
└───────────────────────────────────────────────────────────┘
```

### Move 1: Membangun Teritori Riset (Establishing the Territory)
- **Klaim Sentralitas (*Centrality Claim*)**: Buka bab dengan mendefinisikan mengapa permasalahan riset ini berkedudukan krusial bagi komunitas ilmiah sasaran.
- **Sintesis Latar Belakang (*Background Synthesis*)**: Rajut literatur fundamental secara tematik. Jangan menyajikan ringkasan umum layaknya buku teks dasar; fokuskan pembahasan semata-mata pada evolusi ilmiah yang mengarah langsung ke inti persoalan.
- **Klaim Faktual yang Dapat Diverifikasi (*Verifiable Factual Claims*)**: Rumuskan setiap pernyataan faktual mengenai paradigma terdahulu atau signifikansi domain sebagai proposisi mandiri yang siap dipetakan dalam kurasi sitasi Langkah 2. Dilarang keras menyisipkan penanda sitasi numerik pada tahap ini.

### Move 2: Menetapkan Celah Riset (Establishing the Niche — Titik Balik Kritis)
- **Perumusan Celah yang Tajam (*Sharp Gap Formulation*)**: Paparkan secara gamblang apa yang gagal diselesaikan, diabaikan, atau masih diperdebatkan oleh penelitian sebelumnya.
- **Hindari Klaim Negatif Mutlak (*Avoid Universal Negatives*)**: Hindari klaim mutlak yang tak terverifikasi seperti *"Belum pernah ada studi yang meneliti X"*. Gunakan perumusan terukur dan dapat dipertanggungjawabkan: *"Literatur yang ada saat ini mayoritas berfokus pada representasi domain tunggal, sehingga interaksi bersama antara X dan Y relatif belum banyak dieksplorasi."*
- **Pernyataan Masalah (*Problem Statement*)**: Hubungkan keterbatasan teknis atau kelemahan empiris metode terdahulu secara langsung dengan konsekuensi praktis atau hambatan teoretis nyata di dunia nyata.

### Move 3: Mengisi Celah Riset (Occupying the Niche)
- **Pernyataan Tujuan (*Purpose Statement*)**: Umumkan solusi atau kerangka usulan secara tegas: *"Guna menjembatani celah riset yang telah diidentifikasi tersebut, artikel ini mengusulkan [Kerangka Kerja/Metode/Hipotesis]..."*
- **Daftar Kontribusi Ilmiah Inti (*Core Scientific Contributions*)**: Sajikan daftar poin kontribusi orisinal yang terperinci dan tidak tumpang tindih (biasanya 3–4 poin):
  1. Kontribusi Metodologis/Arsitektural (model, algoritma, atau intervensi eksperimental baru).
  2. Kontribusi Empiris/Tolok Ukur (eksperimen komparatif, kurasi dataset, atau studi ablasi).
  3. Kontribusi Analitis/Diagnostik (disparitas subkelompok, analisis kesalahan, atau pembuktian teoretis).
- **Paragraf Peta Jalan Naskah (*Roadmap Paragraph*)**: Sediakan panduan struktural ringkas yang memetakan bab-bab selanjutnya menggunakan tautan Markdown relatif:
  * Contoh: *"Sistematika penulisan artikel ini disusun sebagai berikut: Seksi [II](02_related-works.md) meninjau literatur terkait. Seksi [III](03_materials-and-methods_0-overview.md) merinci metodologi yang diusulkan. Seksi [IV](04_results-and-discussion_a-global-performance.md) menyajikan evaluasi empiris. Terakhir, Seksi [V](05_conclusion.md) menyimpulkan keseluruhan studi."*

---

## 2. Seksi Kajian Terkait / Tinjauan Pustaka (Related Work)

Seksi Kajian Terkait merupakan sintesis kritis terhadap dialektika intelektual di bidang terkait, bukan sekadar anotasi bibliografi yang dinarasikan.

### Protokol Pengelompokan Tematik (Thematic Clustering Protocol)
- **Organisasikan Berdasarkan Konsep, Bukan Penulis**: Kelompokkan literatur terdahulu ke dalam kategori tematik, paradigma metodologis, atau trajektori evolusi, bukan daftar kronologis paper individual (*"Peneliti A melakukan X. Lalu Peneliti B melakukan Y."*).
- **Pola Kalimat Sintesis Ilmiah**:
  * Lemah (Daftar Penulis): *"Peneliti A menggunakan CNN untuk klasifikasi. Kemudian Peneliti B menggunakan ResNet. Selanjutnya Peneliti C memakai ViT."*
  * Kuat (Sintesis Tematik): *"Paradigma arsitektur awal mayoritas bertumpu pada ekstraksi fitur terlokalisasi melalui jaringan konvolusional, sedangkan formulasi mutakhir memanfaatkan mekanisme atensi mandiri multitranslasi untuk menangkap korelasi spasial jarak jauh."*
- **Pembeda Komparatif (*Comparative Differentiator*)**: Akhiri setiap subbagian tematik dengan membandingkan secara eksplisit keunggulan serta perbedaan mendasar pendekatan yang diusulkan dalam penelitian ini terhadap metode-metode yang disurvei.

---

## 3. Seksi Materi dan Metode / Metodologi (Materials and Methods)

Metodologi riset wajib memberikan transparansi prosedural yang lengkap, sehingga memungkinkan peneliti independen mereplikasi studi secara presisi.

### Organisasi Subseksi Modular
Pada studi berskala kompleks, pisahkan metodologi ke dalam berkas Markdown tersendiri:
- `03_materials-and-methods_0-overview.md`: Arsitektur sistem menyeluruh, bagan alur (*pipeline*), dan ringkasan tingkat tinggi.
- `03_materials-and-methods_a-dataset.md`: Karakteristik kohort, distribusi data, pra-pemrosesan, augmentasi, dan protokol pembagian (*data split*).
- `03_materials-and-methods_b-[teknik-utama].md`: Formulasi matematis, fungsi kerugian (*loss functions*), dan lapisan arsitektur.
- `03_materials-and-methods_c-[model-pembanding].md`: Baseline pembanding, model komparatif, dan varian algoritmik.
- `03_materials-and-methods_g-pipeline.md`: Protokol pelatihan model, hiperparameter optimasi, kriteria konvergensi.
- `03_materials-and-methods_h-evaluation-metrics.md`: Definisi formal metrik performa, skema validasi statistik, dan mekanisme proteksi kebocoran data.

### Aturan Penulisan Metodologis
1. **Ketelitian Matematis**: Setiap simbol dalam persamaan matematika wajib didefinisikan langsung sebelum atau sesudah persamaan tersebut. Nyatakan dimensi variabel dan indeks matriks secara eksplisit.
2. **Proteksi Kebocoran Data (*Data Leakage Safeguards*)**: Dokumentasikan batas pemisahan data dengan tegas. Nyatakan secara eksplisit bahwa seluruh standardisasi, normalisasi, dan penalaan parameter dipelajari secara ketat hanya dari partisi data latih (*training split*).
3. **Transparansi Hiperparameter**: Laporkan seluruh nilai parameter penting secara lengkap (*learning rate*, *batch size*, *epoch*, koefisien regularisasi, *random seed*).

---

## 4. Seksi Hasil dan Pembahasan (Results and Discussion)

Tergantung model struktur naskah yang dipilih, Hasil dan Pembahasan dapat digabungkan (Pola 1A, lazim di bidang Ilmu Komputer & Rekayasa) atau dipisahkan (Pola 1B, lazim di Ilmu Pengetahuan Alam).

### Kerangka Kerja Klaim-Bukti-Penalaran (Claim-Evidence-Reasoning / CER)
Setiap paragraf pembahasan hasil eksperimen wajib mengikuti urutan CER:
1. **Klaim (*Claim* — Pernyataan Temuan Pokok)**: Nyatakan temuan empiris utama secara langsung: *"Konfigurasi tri-domain yang diusulkan menghasilkan skor makro-F1 tertinggi di seluruh model tulang punggung yang diuji."*
2. **Bukti (*Evidence* — Landasan Kuantitatif)**: Rujuk data numerik presisi dari tabel atau grafik yang relevan: *"Sebagaimana diperlihatkan pada Tabel II, model kami mencatat skor F1 sebesar 94,2%, yang mencerminkan peningkatan absolut sebesar 3,8% dibandingkan model baseline (Tabel II, baris 4)."*
3. **Penalaran (*Reasoning* — Interpretasi Mekanisme Ilmiah)**: Jelaskan *faktor penyebab* fenomena tersebut terjadi: *"Keunggulan performa ini terjadi karena sifat komplementer antara representasi afektif dan geometris, yang mencegah keruntuhan batas keputusan di bawah variasi intensitas pencahayaan ekstrem."*
4. **Kualifikasi / Catatan Pengecualian (*Qualification / Caveat*)**: Catat kondisi batas atau subkelompok data tertentu di mana keunggulan model berkurang atau mengalami anomali.

### Pembagian Subseksi Terstruktur untuk Hasil
- **Performa Tolok Ukur Global (*Global Benchmark Performance*)**: Evaluasi komparatif menyeluruh terhadap metode-metode baseline terkemuka.
- **Studi Ablasi (*Ablation Studies*)**: Pengujian isolasi sistematis terhadap masing-masing modul, komponen *loss*, atau subset fitur untuk membuktikan kontribusi inkrementalnya.
- **Analisis Subkelompok & Interseksional (*Subgroup Analysis*)**: Pembongkaran performa model pada subset demografis, lingkungan, atau operasional guna mendeteksi disparitas atau konsistensi sistem.
- **Analisis Pola Kesalahan & Kasus Kegagalan (*Error Pattern Assessment*)**: Pemeriksaan kualitatif atau kuantitatif terhadap prediksi positif palsu, misklasifikasi, atau kerentanan pada kasus batas (*edge cases*).
- **Perbandingan dengan Literatur Terpublikasi (*Comparison with Prior Art*)**: Penjajaran langsung metrik temuan penelitian ini dengan tolok ukur hasil studi terkini di literatur.

---

## 5. Seksi Kesimpulan (Conclusion)

Seksi Kesimpulan memberikan penutup ilmiah dengan menyintesis kontribusi penelitian, membatasi temuan secara objektif, dan menetapkan trajektori riset lanjutan.

### 4 Pilar Kesimpulan Akademik
1. **Pernyataan Ulang Tujuan & Pencapaian Inti**: Rangkum permasalahan riset awal dan nyatakan secara ringkas bagaimana penelitian ini menyelesaikannya tanpa mengulang teks abstrak kata demi kata.
2. **Sintesis Temuan Utama**: Tegaskan kembali sorotan kuantitatif terpenting serta wawasan teoretis baru yang telah dibuktikan pada bagian pembahasan.
3. **Batasan Metodologis Eksplisit**: Paparkan secara jujur keterbatasan studi (misal: skala dataset, representasi demografis, beban komputasi, atau asumsi penyederhanaan). Mengakui batasan penelitian mencerminkan integritas ilmiah dan mengantisipasi kritik penelaah jurnal.
4. **Arah Penelitian Masa Depan yang Konkret**: Usulkan 2–3 langkah tindak lanjut yang berlandasan teknis kuat (misalnya: *"Mengembangkan mekanisme fusi laten untuk aliran video berkelanjutan"* alih-alih kalimat klise hampa seperti *"Penelitian lebih lanjut masih diperlukan"*).
