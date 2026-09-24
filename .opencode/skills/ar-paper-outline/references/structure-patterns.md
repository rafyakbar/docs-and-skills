# Pola Struktur Paper Akademik — 6 Model Kanonikal

Panduan ini memerinci arsitektur struktural, organisasi bab, model progresi paragraf, dan alokasi anggaran kata di seluruh 6 model paper akademik kanonikal.

---

## Prinsip Arsitektural Paragraf demi Paragraf

Model apa pun yang dipilih, outline yang disusun menggunakan skill ini **TIDAK BOLEH** berhenti pada judul bab tingkat tinggi atau sub-judul yang dangkal. Setiap bab wajib dipecah menjadi **unit paragraf diskret** yang mengikuti cetak biru standar:

```
### Paragraf X: [Sub-Tema Deskriptif / Fungsi]
- Target Jumlah Kata: [100–160 kata]
- Tujuan: [1 kalimat yang mendefinisikan fungsi retoris atau ilmiah]
- Poin-Poin Naratif: [1. Kalimat Topik | 2. Elaborasi/Bukti | 3. Konteks/Batasan]
- Penugasan Bukti & Sitasi: [Jangkar literatur, dataset, atau persamaan eksplisit]
- Kalimat Transisi: [Kalimat penutup yang menjembatani ke paragraf berikutnya]
```

---

## Pola 1: IMRaD (Penelitian Empiris)

**Paling Cocok Untuk**: Penelitian empiris berbasis eksperimen kuantitatif, kerja lapangan kualitatif, atau data metode campuran (*mixed-methods*).  
**Disiplin Ilmu Standar**: Ilmu Komputer, Teknik/Rekayasa, Kedokteran, Psikologi, Ilmu Sosial, Sains Alam.  
**Panjang Tipikal**: 5.000 – 8.000 kata.

Paper IMRaD memiliki dua varian arsitektur utama tergantung pada venue target yang dituju:

### Pola 1A: IMRaD Terintegrasi (Hasil dan Pembahasan Digabung)
*Standar di: Ilmu Komputer, Machine Learning, Teknik Elektro, IEEE, ACM, dan Rekayasa Terapan.*  
*(Lihat `references/sample-paragraph-outline.md` untuk contoh lengkap mandiri dari Pola 1A).*

#### Arsitektur Bab & Anggaran Paragraf (Contoh 6.000 kata)
| Bab / Bagian | % dari Total | Target Kata | Jumlah Paragraf | Progresi Paragraf |
|---|:---:|:---:|:---:|---|
| Bagian Depan & Abstrak | — | 200 kata | 1 (Terpadu) | Konteks → Tujuan → Metode → Hasil → Kesimpulan |
| **Bagian I: Pendahuluan** | 15% | ~900 kata | 6–7 paragraf | P1: Urgensi & Konteks Nyata<br>P2: Rumusan Masalah & Titik Buta Sensorik/Domain<br>P3: Kemajuan Teknologi & Paradigma Fondasional<br>P4: Kesenjangan Kritis Literatur<br>P5: Gambaran Umum Kerangka yang Diusulkan<br>P6: Poin-Poin Kontribusi Ilmiah Terinci<br>P7: Peta Jalan Organisasi Artikel |
| **Bagian II: Kajian Pustaka Terkait** | 15% | ~900 kata | 5–6 paragraf | P1–P4: Sintesis tematik pendekatan terdahulu (maks 3 sitasi/kalimat)<br>P5: Sintesis komparatif kritis mengenai keterbatasan metode yang ada<br>P6: Pernyataan pemosisian riset & diferensiasi kebaruan |
| **Bagian III: Materi dan Metode** | 25% | ~1.500 kata | 10–12 paragraf | **Gambaran Umum**: Diagram arsitektur pipeline lebar penuh (Gambar 1)<br>**III.A Dataset**: P1 Konteks, P2 Partisi Data, P3 Prapemrosesan<br>**III.B Ekstraksi Fitur**: P4–P6 Arsitektur backbone & formulasi persamaan<br>**III.C Pipeline Optimasi**: P7–P9 Ruang pencarian algoritma & isolasi lipatan (*fold*)<br>**III.D Protokol Evaluasi**: P10–P11 Metrik & pengujian statistik |
| **Bagian IV: Hasil dan Pembahasan** | 40% | ~2.400 kata | 12–15 paragraf | **IV.A Tolok Ukur Global**: P1–P3 Kinerja utama & analisis pembanding baseline (Tabel III)<br>**IV.B Ablasi Fitur**: P4–P6 Kontribusi per komponen (Gambar 2)<br>**IV.C Analisis Subkelompok & Galat**: P7–P9 Stabilitas tingkat kelas & pola galat<br>**IV.D Kompleksitas Komputasi**: P10–P11 Pemprofilan waktu eksekusi & memori<br>**IV.E Pembahasan**: P12–P14 Triangulasi dengan literatur terdahulu, implikasi teoretis, dan batasan cakupan |
| **Bagian V: Kesimpulan** | 5% | ~300 kata | 3 paragraf | P1: Sintesis temuan utama yang menjawab RQs<br>P2: Pengungkapan jujur keterbatasan teknis/praktis<br>P3: Peta jalan tindak lanjut untuk riset masa depan |

---

### Pola 1B: IMRaD Pemisahan Klasik (Hasil dan Pembahasan Dipisah)
*Standar di: Kedokteran Klinis, Ilmu Biomedis, Psikologi Eksperimental, Ilmu Sosial Murni.*

#### Arsitektur Bab & Anggaran Paragraf (Contoh 6.000 kata)
| Bab / Bagian | % dari Total | Target Kata | Jumlah Paragraf | Progresi Paragraf |
|---|:---:|:---:|:---:|---|
| Bagian Depan & Abstrak | — | 250 kata | 1 (Terstruktur) | Tujuan → Metode → Hasil → Kesimpulan |
| **1. Pendahuluan** | 15% | ~900 kata | 5–6 paragraf | Konteks masalah luas → Ketegangan klinis/empiris spesifik → Defisit pengetahuan yang belum terpecahkan → Tujuan studi & hipotesis |
| **2. Tinjauan Pustaka / Kerangka Teoretis** | 20% | ~1.200 kata | 7–8 paragraf | Konstruk teoretis → Temuan empiris lintas tema → Inkonsistensi/kontroversi data terdahulu → Justifikasi hipotesis |
| **3. Metodologi** | 15% | ~900 kata | 6–8 paragraf | Partisipan/Kriteria sampel → Operasionalisasi pengukuran → Prosedur eksperimen & etika → Strategi analisis statistik |
| **4. Hasil** | 20% | ~1.200 kata | 7–9 paragraf | *Pelaporan murni faktual tanpa interpretasi*:<br>Statistik deskriptif (Tabel 1) → Pengujian hipotesis primer H1 (Tabel 2) → Pengujian hipotesis sekunder H2 → Analisis subkelompok/sensitivitas |
| **5. Pembahasan** | 25% | ~1.500 kata | 8–10 paragraf | Rangkuman temuan inti → Interpretasi & perbandingan dengan studi terdahulu → Mekanisme teoretis penjelas hasil → Implikasi klinis/praktis → Keterbatasan metodologis |
| **6. Kesimpulan** | 5% | ~300 kata | 2–3 paragraf | Sintesis akhir → Pesan utama yang definitif |

---

## Pola 2: Thematic Literature Review (Tinjauan Pustaka Tematik)

**Paling Cocok Untuk**: Tinjauan sistematis (*systematic review*), meta-analisis (PRISMA), dan tinjauan cakupan mutakhir (*scoping review*).  
**Disiplin Ilmu Standar**: Semua bidang akademik.  
**Panjang Tipikal**: 6.000 – 10.000 kata.

### Arsitektur Progresi Paragraf
- **Bagian 1: Pendahuluan & Motivasi (3–4 paragraf, ~800 kata)**
  - P1: Evolusi dan signifikansi kontemporer dari bidang kajian.
  - P2: Batasan cakupan, ruang lingkup, dan pertanyaan tinjauan spesifik (*review questions* / RQs).
  - P3: Justifikasi perlunya tinjauan ini dibandingkan survei terdahulu.
  - P4: Gambaran umum struktur tinjauan.
- **Bagian 2: Metodologi Tinjauan & Strategi Penelusuran (3–4 paragraf, ~800 kata)**
  - P1: Pemilihan basis data, sintaks string penelusuran, dan batasan rentang waktu.
  - P2: Kriteria inklusi dan eksklusi (Diagram Alir PRISMA / Gambar 1).
  - P3: Protokol penyaringan (*screening*), reliabilitas antarraya (*inter-rater reliability*), dan penilaian risiko bias.
  - P4: Profil bibliometrik dari korpus artikel final (Tabel 1).
- **Bagian 3–5: Kluster Tematik (4–6 paragraf per tema, ~3.600 kata)**
  - *Tema A*: Paradigma fondasional, taksonomi, dan konstruk inti.
  - *Tema B*: Implementasi metodologis dan pola temuan empiris.
  - *Tema C*: Faktor pendorong, variabel pemoderasi, dan luaran yang teramati.
  - *Alur internal paragraf*: Sintesis konsensus → Bukti divergen/kontradiktif → Pendorong metodologis yang mendasarinya.
- **Bagian 6: Sintesis Kritis & Kesenjangan Riset (4–5 paragraf, ~1.200 kata)**
  - P1: Titik buta teoretis di berbagai kluster literatur.
  - P2: Defisit metodologis dan bias penarikan sampel dalam studi-studi terdahulu.
  - P3: Bukti yang saling bertentangan dan ketegangan empiris.
  - P4: Matriks ringkasan kesenjangan riset yang teridentifikasi (Tabel 2).
- **Bagian 7: Kerangka Integratif & Agenda Masa Depan (3–4 paragraf, ~1.000 kata)**
  - P1: Penyajian model konseptual integratif yang diusulkan (Gambar 2).
  - P2: Pertanyaan penelitian spesifik dan berprioritas tinggi untuk investigasi masa depan.
  - P3: Rekomendasi metodologis untuk karya empiris berikutnya.
- **Bagian 8: Kesimpulan (2 paragraf, ~400 kata)**
  - P1: Sintesis kontribusi utama tinjauan.
  - P2: Catatan penutup mengenai arah dan trajektori domain penelitian di masa mendatang.

---

## Pola 3: Theoretical Analysis (Analisis Teoretis)

**Paling Cocok Untuk**: Pengembangan kerangka konseptual baru, perumusan formulasi matematis, atau kritik terhadap paradigma teoretis yang ada.  
**Disiplin Ilmu Standar**: Filsafat, Ilmu Ekonomi, Sosiologi, Teori Kritis, Matematika Murni, Ilmu Komputer Teoretis.  
**Panjang Tipikal**: 6.000 – 9.000 kata.

### Arsitektur Progresi Paragraf
- **Bagian 1: Pendahuluan & Paradoks Teoretis (3–4 paragraf, ~900 kata)**
  - P1: Anomali dunia nyata atau teka-teki konseptual yang gagal dipecahkan oleh teori yang ada.
  - P2: Kelemahan dan titik kegagalan paradigma teoretis dominan saat ini.
  - P3: Kontribusi teoretis yang diusulkan, tesis inti, dan batas analitis.
- **Bagian 2: Fondasi Teoretis & Tinjauan Kritis (5–6 paragraf, ~1.500 kata)**
  - Asal-usul historis konsep → Formulasi dominan → Kritik terhadap asumsi tersembunyi dan ketegangan logika internal.
- **Bagian 3: Perumusan Model Teoretis Baru (8–10 paragraf, ~2.500 kata)**
  - P1–P2: Landasan aksiomatis, definisi primitif, dan ontologi.
  - P3–P5: Derivasi matematis, proposisi, atau rantai logika formal (Persamaan 1..N).
  - P6–P8: Interaksi antarkonstruk dan mekanisme kausalitas.
  - P9–P10: Batasan kondisi formal dan limitasi ruang lingkup.
- **Bagian 4: Penerapan Konseptual / Eksperimen Pikiran (5–6 paragraf, ~1.600 kata)**
  - Pengujian model yang diusulkan terhadap paradoks yang diketahui, kasus ekstrem (*edge cases*), atau anomali historis (Tabel 1 membandingkan model konvensional vs. model baru).
- **Bagian 5: Implikasi Epistemologis & Pembahasan (4–5 paragraf, ~1.100 kata)**
  - Konsekuensi epistemologis yang lebih luas → Interpretasi ulang temuan empiris yang ada → Implikasi metodologis untuk menguji model secara empiris.
- **Bagian 6: Kesimpulan (2 paragraf, ~400 kata)**
  - Sintesis akhir dan prospek perluasan teoretis lanjutan.

---

## Pola 4: Case Study (Studi Kasus)

**Paling Cocok Untuk**: Investigasi mendalam studi kasus tunggal atau jamak (*multiple-case*) dalam domain organisasi, teknologi, atau kebijakan.  
**Disiplin Ilmu Standar**: Manajemen, Sistem Informasi, Administrasi Publik, Ilmu Pendidikan, Sosiologi.  
**Panjang Tipikal**: 6.000 – 8.000 kata.

### Arsitektur Progresi Paragraf
- **Bagian 1: Pendahuluan & Fenomena Kasus (3–4 paragraf, ~800 kata)**
  - Fenomena empiris dalam konteksnya → Relevansi praktis → Pertanyaan penelitian dan rasional pemilihan metodologi studi kasus kualitatif.
- **Bagian 2: Landasan Teoretis (3–4 paragraf, ~1.000 kata)**
  - Konsep teoretis pemandu (*sensitizing concepts*) atau kerangka analitis yang memandu observasi lapangan.
- **Bagian 3: Metodologi Penelitian & Konteks Kasus (4–6 paragraf, ~1.200 kata)**
  - P1: Rasional pemilihan kasus (kriteria kasus luar biasa, ekstrem, atau representatif).
  - P2: Latar belakang institusional dan kondisi operasional organisasi kasus.
  - P3: Triangulasi pengumpulan data (wawancara mendalam, observasi lapangan, dokumen arsip).
  - P4–P5: Prosedur pengodean (*coding*), validitas konstruk, dan strategi analitis intrasubjek (*within-case*) / antarkasus (*cross-case*).
- **Bagian 4: Temuan Kasus & Analisis Naratif (8–12 paragraf, ~2.200 kata)**
  - Progresi naratif kronologis atau tematik: Kondisi dasar (*baseline*) → Insiden kritis / Intervensi → Respons organisasional → Dinamika dan dampak yang muncul.
- **Bagian 5: Pembahasan & Kerangka Konseptual yang Muncul (5–6 paragraf, ~1.400 kata)**
  - Kerangka induktif yang dibangun dari observasi kasus (Gambar 1) → Perbandingan dengan literatur terdahulu → Batasan keteralihan (*transferability*) dan generalisasi analitis.
- **Bagian 6: Implikasi Praktis & Kesimpulan (2–3 paragraf, ~400 kata)**
  - Pelajaran manajerial/kebijakan yang dapat ditindaklanjuti → Keterbatasan metodologis → Catatan penutup.

---

## Pola 5: Policy Brief (Ringkasan Kebijakan)

**Paling Cocok Untuk**: Dokumen ringkasan berbasis bukti yang menerjemahkan riset empiris kompleks menjadi rekomendasi kebijakan yang dapat ditindaklanjuti bagi pembuat keputusan.  
**Disiplin Ilmu Standar**: Kebijakan Publik, Kesehatan Masyarakat, Tata Kelola Lingkungan, Ilmu Ekonomi Terapan.  
**Panjang Tipikal**: 3.000 – 5.000 kata.

### Arsitektur Progresi Paragraf
- **Ringkasan Eksekutif (2 paragraf, ~250 kata)**
  - P1: Dilema kebijakan inti, urgensi masalah, dan temuan utama.
  - P2: Rekomendasi kebijakan definitif dan proyeksi dampaknya.
- **Bagian 1: Konteks Kebijakan & Akar Masalah (3–4 paragraf, ~800 kata)**
  - Konteks masalah sosial-ekonomi atau kelembagaan → Pendorong struktural mendasar → Risiko langsung bagi populasi pemangku kepentingan terdampak.
- **Bagian 2: Evaluasi Kritis terhadap Kebijakan yang Ada (3–4 paragraf, ~800 kata)**
  - Analisis terhadap upaya regulasi/legislasi saat ini → Ketiadaan efisiensi anggaran, kelemahan sistemik yang teridentifikasi, atau insentif keliru yang tidak diharapkan.
- **Bagian 3: Bukti Empiris & Analisis Dampak (4–5 paragraf, ~1.200 kata)**
  - Temuan riset kuantitatif, kalkulasi analisis biaya-manfaat (*cost-benefit*), dan distribusi dampak demografis (Tabel 1 & Gambar 1).
- **Bagian 4: Opsi Kebijakan & Evaluasi Komparatif (3–4 paragraf, ~1.000 kata)**
  - Evaluasi Opsi A vs. Opsi B vs. Status Quo terhadap kelayakan, biaya, keadilan (*equity*), dan viabilitas politis (Matriks Evaluasi Tabel 2).
- **Bagian 5: Rekomendasi yang Dapat Ditindaklanjuti & Peta Jalan Implementasi (3 paragraf, ~600 kata)**
  - P1: Paket kebijakan yang direkomendasikan beserta rasional logisnya.
  - P2: Linimasa implementasi bertahap dan pembagian tanggung jawab instansi pelaksana.
  - P3: Indikator kinerja utama (*Key Performance Indicators* / KPI) dan pemantauan akuntabilitas.

---

## Pola 6: Conference Paper (Makalah Konferensi)

**Paling Cocok Untuk**: Paper jalur cepat (*fast-track*) dengan batasan ruang ketat (biasanya 4–8 halaman / 3.000–4.500 kata).  
**Disiplin Ilmu Standar**: Ilmu Komputer, AI/ML, Teknik Elektro, Interaksi Manusia-Komputer (HCI).  
**Panjang Tipikal**: 3.000 – 4.500 kata.

### Arsitektur Progresi Paragraf
- **Bagian 1: Pendahuluan (3–4 paragraf, ~600 kata)**
  - P1: Motivasi penelitian dan masalah teknis inti.
  - P2: Keterbatasan pendekatan tolok ukur (*baseline*) yang ada.
  - P3: Kontribusi teknis yang diusulkan dan gambaran umum metodologi.
  - P4: Daftar butir kontribusi utama (biasanya 3 poin utama).
- **Bagian 2: Kajian Pustaka Terkait (2–3 paragraf, ~500 kata)**
  - P1: Evolusi algoritma baseline terkait.
  - P2: Diferensiasi spesifik karya ini dibandingkan metode kompetitor terdekat.
- **Bagian 3: Metodologi yang Diusulkan (4–6 paragraf, ~1.200 kata)**
  - P1: Gambaran umum diagram alur sistem (*system pipeline*) (Gambar 1).
  - P2–P4: Rincian algoritmik, formulasi matematis (Persamaan 1..N), serta fungsi kerugian (*loss function*) atau mekanisme baru.
- **Bagian 4: Evaluasi Eksperimental (6–8 paragraf, ~1.600 kata)**
  - P1: Dataset, model pembanding baseline, dan metrik evaluasi.
  - P2–P3: Hasil tolok ukur kuantitatif vs. baseline (Tabel 1 & Gambar 2).
  - P4–P5: Studi ablasi komponen yang memvalidasi keputusan arsitektur.
  - P6: Contoh kualitatif atau analisis kasus kegagalan (*failure cases*).
- **Bagian 5: Kesimpulan & Keterbatasan (1–2 paragraf, ~300 kata)**
  - P1: Rangkuman ringkas hasil penelitian.
  - P2: Keterbatasan utama dan arah penelitian lanjutan di masa mendatang.
