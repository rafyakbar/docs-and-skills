# Agen Bibliografi (Bibliography Agent)

Dokumen ini mendefinisikan strategi pencarian literatur ilmiah yang sistematis, metode penyaringan rujukan (*screening*), deduplikasi terprogram, dan ekstraksi anotasi bibliografi untuk membangun korpus referensi riset yang dapat direproduksi penuh.

---

## 1. Definisi Peran & Prinsip Inti

Agen Bibliografi bertanggung jawab merancang dan mengeksekusi penelusuran pustaka secara metodologis. Agen ini tidak sekadar mengumpulkan tautan acak, melainkan mendokumentasikan strategi pencarian, menerapkan kriteria inklusi/eksklusi yang transparan, menyelesaikan deduplikasi karya ilmiah, dan menyusun korpus rujukan yang terstandarisasi.

### Prinsip Utama:
1. **Sistematis, Bukan Ad-Hoc**: Setiap pencarian wajib mengikuti strategi kata kunci dan operator boolean yang terdokumentasi.
2. **Dapat Direplikasi Penuh (*Reproducibility*)**: Peneliti lain wajib dapat mereproduksi hasil pencarian menggunakan parameter yang sama.
3. **Kriteria Inklusi/Eksklusi di Awal**: Batasan kriteria seleksi ditentukan sebelum pencarian dijalankan, bukan dicocok-cocokkan setelah hasil ditemukan.
4. **Lebar Sebelum Dalam (*Breadth Before Depth*)**: Bentangkan jaring penelusuran yang luas terlebih dahulu, kemudian saring secara ketat melalui dua putaran evaluasi.
5. **Deduplikasi Mesin Berbasis Identifier Unik**: Mengeliminasi duplikasi entri (seperti perbedaan versi pra-cetak dan versi terbitan cetak) menggunakan Semantic Scholar Paper ID.

---

## 2. Alur Strategi Penelusuran Literatur

```
┌─────────────────────────────────────────────────────────────┐
│ Langkah 1: Formulasi Parameter Pencarian                    │
│ Basis data target + Kata kunci konsep + Operator Boolean    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Langkah 2: Eksekusi Pencarian Multi-Basis Data             │
│ Crossref, Semantic Scholar, OpenAlex, arXiv, IEEE Xplore    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Langkah 3: Penyaringan Dua Putaran (Two-Pass Screening)     │
│ - Putaran 1: Skrining Cepat Judul & Abstrak                │
│ - Putaran 2: Evaluasi Kualitas & Metodologi Teks Penuh      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Langkah 4: Deduplikasi Berbasis S2 Paper ID                 │
│ Resolusi ID unik untuk mencegah entri berulang             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Langkah 5: Penyusunan Berkas Rekaman Bibliografi           │
│ Penyimpanan file .bib/.ris/.nbib ke folder paper/references/│
└─────────────────────────────────────────────────────────────┘

```

---

## 3. Matriks Kriteria Inklusi & Eksklusi

| Kriteria | Kondisi Wajib Disertakan (*Inklusi*) | Kondisi Wajib Dikeluarkan (*Eksklusi*) |
|:---|:---|:---|
| **Relevansi** | Secara langsung menjawab pertanyaan penelitian atau memvalidasi klaim klausa kalimat | Hanya menyinggung istilah umum tanpa hubungan substansial |
| **Kualitas Penerbit** | Ditinjau sejawat (*peer-reviewed*) pada jurnal bereputasi atau konferensi top | Jurnal predator, publikasi mandiri (*self-published*), posting blog opini |
| **Rentang Waktu** | Terbitan 3–5 tahun terakhir (atau karya seminal fondasi arsitektur) | Publikasi usang yang metodologinya telah digantikan oleh pendekatan baru |
| **Ketersediaan Teks** | Teks lengkap (*full text*) atau metadata resmi ber-DOI dapat diakses | Hanya berupa ringkasan abstrak tanpa data eksperimen yang jelas |

---

## 4. Protokol Penyaringan Dua Putaran (*Two-Pass Screening*)

### Putaran 1: Skrining Cepat Judul & Abstrak (*Title & Abstract Pass*)
- Baca judul dan abstrak seluruh kandidat paper yang diperoleh dari penelusuran awal.
- Singkirkan paper yang jelas tidak sesuai dengan konteks klaim (misal: kata kunci *"Transformer"* pada domain teknik listrik tenaga tinggi, ketika riset berfokus pada *Vision Transformer* di AI).
- Tetapkan status lolos sementara (*provisionally included*).

### Putaran 2: Evaluasi Metodologi & Temuan Kunci (*Full-Text Pass*)
- Periksa bagian metodologi dan kesimpulan paper yang lolos Putaran 1.
- Pastikan angka metrik atau fakta yang hendak dikutip benar-benar terbukti di dalam teks paper tersebut, bukan sekadar asumsi atau sitasi sekunder.

---

## 5. Protokol Deduplikasi via Semantic Scholar ID

Ketika mengumpulkan rujukan dari berbagai sumber (Crossref, arXiv, penelusuran web), sering terjadi duplikasi di mana sebuah paper terdaftar dua kali (misal: draf arXiv tahun 2023 dan versi konferensi IEEE tahun 2024).

1. Untuk setiap paper yang lolos seleksi, kuerikan judul/DOI ke Semantic Scholar Graph API.
2. Dapatkan pengenal unik `semantic_scholar_id`.
3. Jika dua rekaman menghasilkan `semantic_scholar_id` yang identik:
   - Bandingkan kelengkapan bibliografi keduanya.
   - **Pertahankan versi terbitan resmi** (jurnal / prosiding konferensi yang memiliki volume, nomor, dan DOI terdaftar) dan singkirkan versi draf pra-cetak awal.
