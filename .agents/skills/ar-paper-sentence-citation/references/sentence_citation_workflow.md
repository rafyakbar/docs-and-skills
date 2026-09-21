# Alur Kerja Kurasi Sitasi Per Kalimat & Penyusunan references.txt

Panduan teknis ini menguraikan prosedur langkah demi langkah dalam membedah draf naskah ilmiah, mencari literatur bereputasi yang relevan untuk setiap kalimat klaim, menyimpan berkas bibliografi, serta menyusun berkas pemetaan `paper/references.txt`.

---

## 1. Siklus 5 Tahap Kurasi Sitasi

Proses pencarian dan kurasi sitasi per kalimat dijalankan dengan alur terstruktur berikut:

```
┌─────────────────────────────────────────────────────────────┐
│ Tahap 1: Ekstraksi Klaim Per Kalimat                        │
│ • Baca draf section (misal 01_introduction.md)              │
│ • Identifikasi kalimat yang memuat klaim ilmiah/faktual     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Tahap 2: Pembentukan Kueri Pencarian Akademis               │
│ • Ekstrak konsep inti, variabel teknis, & metodologi        │
│ • Batasi rentang tahun publikasi (3–5 tahun terakhir)       │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Tahap 3: Pencarian & Validasi Literatur                     │
│ • Cari pada Crossref, Semantic Scholar, arXiv, IEEE, PubMed │
│ • Validasi kecocokan temuan paper terhadap klaim kalimat    │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Tahap 4: Penyimpanan Rekaman Bibliografi                    │
│ • Simpan berkas .bib, .ris, atau .nbib ke paper/references/ │
│ • Format nama: [Tahun]_[Judul Paper Ringkas].[ext]          │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Tahap 5: Pemetaan ke paper/references.txt                   │
│ • Petakan kalimat klaim ke path berkas bibliografi          │
│ • Kelompokkan per nomor paragraf secara rapi                │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Tahap 1: Ekstraksi Kalimat Klaim

### Klasifikasi Kalimat: Wajib vs Tidak Wajib Sitasi

| Kategori Kalimat | Contoh Kalimat | Wajib Sitasi? |
|:---|:---|:---:|
| **Klaim Faktual / Masalah Domain** | *"Disparitas performa pada subkelompok wajah perempuan dan kulit gelap masih menjadi kendala nyata."* | **Ya** (Cari studi disparitas) |
| **Kajian Literatur / Metode Terdahulu** | *"ViT memanfaatkan Multi-Head Self-Attention untuk memodelkan hubungan patch global."* | **Ya** (Cari paper ViT/MHSA) |
| **Pernyataan Kesenjangan Riset** | *"Fusi representasi afektif, biometrik, dan penuaan dalam satu model terpadu masih terbatas."* | **Ya** (Cari riset terkait/survey) |
| **Metodologi / Algoritma Eksternal** | *"Seluruh classifier dievaluasi menggunakan Stratified Cross-Validation."* | **Ya** (Cari paper metodologi/tutorial) |
| **Kontribusi Peneliti Sendiri** | *"Penelitian ini mengusulkan kerangka kerja fusi fitur Tri-Domain..."* | **Tidak** (Karya sendiri) |
| **Peta Sistematika Naskah (Roadmap)** | *"Sistematika penulisan artikel ini disusun sebagai berikut: Section II membahas..."* | **Tidak** (Struktur internal) |

---

## 3. Tahap 2 & 3: Kueri Pencarian & Validasi Sumber

### Teknik Pembentukan Kueri
1. **Identifikasi Konsep Kunci**: Ambil entitas utama kalimat.
   * *Kalimat*: *"Pemodelan atribut secara terpisah dapat membatasi analisis terhadap kelompok yang terbentuk dari kombinasi ras dan gender."*
   * *Kata Kunci*: `"intersectional facial attribute classification" OR "gender and race classification bias"`.
2. **Prioritaskan Paper Primer**: Cari paper yang pertama kali memperkenalkan model, dataset, atau metrik yang dirujuk.
3. **Verifikasi Kesesuaian Isi**: Pastikan abstrak atau isi paper rujukan benar-benar membenarkan proposisi yang ditulis dalam kalimat naskah (bukan sekadar kemiripan kata kunci).

---

## 4. Tahap 4: Konvensi Penamaan Berkas Bibliografi

Simpan berkas catatan bibliografi pada folder `paper/references/` dengan aturan penamaan yang ketat:

### Pola Nama Berkas
```text
paper/references/[Tahun]_[Judul Paper Lengkap atau Ringkas].[ext]
```

### Contoh Penamaan:
- `paper/references/2022_Automatic Ethnicity Classification from Middle Part of the Face Using Convolutional Neural Networks.bib`
- `paper/references/2023_A Multidimensional Analysis of Social Biases in Vision Transformers.bib`
- `paper/references/2022_A comprehensive survey on techniques to handle face identity threats challenges and opportunities.ris`
- `paper/references/2022_The unseen Black faces of AI algorithms.nbib`

> [!TIP]
> Hindari karakter terlarang dalam penamaan berkas Windows (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`). Gantikan titik dua (`:`) atau tanda hubung panjang dengan spasi atau tanda hubung standar (`-`).

---

## 5. Tahap 5: Format Baku Berkas `paper/references.txt`

Berkas `paper/references.txt` disusun secara hierarkis berdasarkan nama berkas draf dan nomor paragraf:

```text
paper/[nama-berkas-draf].md: paragraf [X]:
- "[Kutipan teks kalimat klaim persis dari draf]":
  - paper/references/[Tahun]_[Judul Paper 1].[ext]
  - paper/references/[Tahun]_[Judul Paper 2].[ext]
- "[Kutipan teks kalimat klaim berikutnya]":
  - paper/references/[Tahun]_[Judul Paper 3].[ext]

paper/[nama-berkas-draf].md: paragraf [X+1]:
- "[Kutipan kalimat klaim pada paragraf baru]":
  - paper/references/[Tahun]_[Judul Paper 4].[ext]
```

### Aturan Format `references.txt`:
1. **Kutipan Kalimat Persis**: Teks di dalam tanda kutip `"[teks]"` harus identik dengan kalimat yang ada di draf naskah markdown. Ini memastikan otomasi pencocokan pada Step 4 (penomoran sitasi) berjalan tanpa kesalahan string.
2. **Indentasi Bersarang**:
   - Baris kalimat klaim diawali tanda hubung `- "Kalimat...":`
   - Baris berkas referensi di bawahnya diindentasi dua spasi: `  - paper/references/...`
3. **Pemisah Paragraf**: Berikan satu baris kosong antar-paragraf untuk menjaga keterbacaan (*human readability*).
