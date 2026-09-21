# Detektor Klaim Tanpa Sitasi (Uncited Assertion Detector)

Dokumen ini mendefinisikan logika pendeteksian klaim tanpa sitasi (*Uncited Assertion Detection*) berdasarkan aturan berbasis token dan tata bahasa (*token-based grammar detection*), kamus penanda kuantitatif/empiris, pola regex idiom proporsi, jendela penyaring penunjuk seksi (*guard window*), daftar pengecualian, dan skema validasi terstruktur.

---

## 1. Aturan Tiga Kondisi (*The Three-Condition Rule*)

Sebuah kalimat dalam draf naskah diklasifikasikan sebagai **kandidat klaim wajib sitasi (*uncited assertion candidate*)** jika memenuhi **KETIGA** kondisi berikut secara bersamaan:

```
┌─────────────────────────────────────────────────────────────┐
│ Kondisi 1: Kehadiran Penanda Kuantitatif atau Verba Empiris │
│ Memuat angka, persentase, kuantifier, atau kata kerja fakta │
└──────────────────────────────┬──────────────────────────────┘
                               ▲ (DAN)
┌─────────────────────────────────────────────────────────────┐
│ Kondisi 2: Belum Memiliki Rujukan / Marker Sitasi           │
│ Kalimat belum dipetakan ke berkas di paper/references/      │
└──────────────────────────────┬──────────────────────────────┘
                               ▲ (DAN)
┌─────────────────────────────────────────────────────────────┐
│ Kondisi 3: Bukan Merupakan Kalimat Pengecualian             │
│ Bukan kalimat definisi, kontribusi mandiri, atau roadmap    │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Kamus Penanda Token & Verba Empiris (Kondisi 1)

### A. Token Kuantitatif, Statistik, & Pola Regex
Kalimat yang memuat representasi numerik hasil eksperimen atau data populasi:
- **Persentase**: Regex `\b\d+(?:\.\d+)?%` (e.g., `85%`, `12.4%`).
- **Idiom Proporsi ("N of M")**: Regex `\b\d+(?:\.\d+)?\s+(?:of|dari)\s+\d+\b` (e.g., *"67 of 100"*, *"8 dari 10 responden"*).
- **Ukuran Sampel / Partisipan**: `42 peserta`, `1,200 citra wajah`, `500 responden`, `10,000 sampel data`.
- **Metrik Kinerja Algoritma**: `akurasi mencapai 94.2%`, `F1-score sebesar 0.91`, `AUC 0.98`, `p < 0.05`.

> [!NOTE]
> **Jendela Penyaring Penunjuk Seksi (*Left-Window Guard - 24 Karakter*)**
> Angka numerik murni **TIDAK** memicu deteksi jika dalam rentang 24 karakter di sebelah kirinya didahului oleh kata penunjuk struktur naskah:
> `Section`, `Table`, `Figure`, `Gambar`, `Tabel`, `Bab`, `v` (versi), atau penyebutan tahun murni (`pada tahun 2023`).

### B. Kuantifier Eksplisit (*Explicit Quantifiers*)
Frasa yang menggeneralisasi fenomena empiris pada literatur atau populasi:
- *Bahasa Indonesia*: `sebagian besar`, `sejumlah studi`, `mayoritas penelitian`, `banyak kasus terdahulu`, `beberapa pendekatan`, `minimnya penelitian`.
- *Bahasa Inggris*: `most`, `several`, `numerous`, `a substantial proportion`, `the majority of prior studies`, `limited research`.

### C. Verba Empiris (*Empirical Verbs*)
Kata kerja yang menyatakan observasi eksperimental atau pengungkapan fakta oleh peneliti terdahulu:
- *Bahasa Indonesia*: `menunjukkan`, `membuktikan`, `menemukan`, `melaporkan`, `mengamati`, `menghasilkan`, `mengungkap`, `mencatat`, `menyimpulkan`.
- *Bahasa Inggris*: `showed`, `demonstrated`, `observed`, `proved`, `confirmed`, `revealed`, `reported`, `documented`, `indicated`.

---

## 3. Daftar Pengecualian Sitasi (*Exemptions - Kondisi 3*)

Kalimat-kalimat berikut **DIKECUALIKAN** dari kewajiban sitasi karena merupakan narasi internal orisinal peneliti:

1. **Kalimat Definisi Operasional Peneliti Sendiri**:
   - Frasa pemicu: *"merujuk pada"*, *"didefinisikan sebagai"*, *"dalam konteks penelitian ini, kami mendefinisikan"*, *"for the purposes of this study, we define"*.
2. **Pernyataan Kontribusi dan Usulan Penelitian Ini**:
   - Frasa pemicu: *"Penelitian ini mengusulkan..."*, *"Dalam artikel ini, kami mengembangkan..."*, *"Kontribusi utama dari riset ini adalah..."*, *"We propose a novel framework..."*.
3. **Sistematika Penulisan Naskah (*Paper Roadmap*)**:
   - Frasa pemicu: *"Sistematika penulisan artikel ini disusun sebagai berikut..."*, *"Section II membahas..."*, *"The remainder of this article is organized as follows..."*.
4. **Kalimat Hipotesis Murni atau Pertanyaan Riset**:
   - Pertanyaan riset eksplisit atau rumusan hipotesis awal sebelum pengujian dilakukan.

---

## 4. Skema Data Validasi Klaim Tanpa Sitasi (JSON Schema)

Setiap temuan klaim tanpa sitasi dicatat ke dalam format data terstruktur berikut:

```json
{
  "finding_id": "UA-001",
  "rule_version": "D4-c-v1",
  "sentence_text": "Prior studies demonstrated that demographic disparities in facial recognition models can exceed 15% across different ethnic groups.",
  "section_path": "paper/01_introduction.md > Paragraf 2",
  "trigger_tokens": ["demonstrated", "15%"],
  "detection_triggers": {
    "has_empirical_verb": true,
    "empirical_verb": "demonstrated",
    "has_quantitative_token": true,
    "quantitative_token": "15%",
    "has_quantifier": false
  },
  "exemption_status": {
    "is_exempt": false,
    "exemption_category": null
  },
  "action_required": "SEARCH_AND_MAP",
  "recommended_query": "demographic disparities facial recognition error rate ethnic groups"
}
```

---

## 5. Alur Tindakan Remediasi

1. **Ekstraksi Kueri**: Ubah kalimat klaim yang terdeteksi menjadi string kueri pencarian ilmiah (menggunakan kata kunci konsep dan kata kerja empiris).
2. **Pencarian Repositori**: Jalankan pencarian via Crossref, Semantic Scholar, OpenAlex, atau arXiv.
3. **Penyimpanan Bibliografi**: Simpan berkas catatan bibliografi (`.bib`, `.ris`, atau `.nbib`) ke dalam direktori `paper/references/`.
4. **Pencatatan Pemetaan**: Tambahkan pemetaan kalimat persis ke dalam `paper/references.txt`.
