# Protokol Verifikasi Semantic Scholar API

Dokumen ini mendefinisikan protokol kueri, verifikasi keberadaan referensi, dan ekstraksi metadata bibliografi terprogram menggunakan Semantic Scholar Academic Graph API. Protokol ini melengkapi penelusuran manual dengan pemeriksaan terstruktur yang mengembalikan metadata mesin yang valid.

---

## 1. Informasi Dasar & Batas Kecepatan (Rate Limits)

- **API Base URL**: `https://api.semanticscholar.org/graph/v1`
- **Rate Limit**:
  - *Tanpa Autentikasi (Anonim)*: 1 request/detik (~30–80 detik per naskah paper).
  - *Dengan API Key*: 10 request/detik (~3–8 detik per naskah paper, menyertakan header `x-api-key: {S2_API_KEY}`).
- **Variabel Lingkungan**: `S2_API_KEY` (opsional; kunci gratis dapat diperoleh dari `https://www.semanticscholar.org/product/api#api-key`).

---

## 2. Tujuan & Triangulasi Multi-Indeks

Semantic Scholar menyediakan graf pengetahuan akademis berbasis NLP/AI yang sangat luas (terutama di bidang Computer Science, Biomedis, dan Neurosains). Bersama Crossref dan OpenAlex, Semantic Scholar membentuk sistem triangulasi multi-indeks ($k=3$).

Sinyal verifikasi yang dihasilkan adalah status kanonikal **`semantic_scholar_unmatched = true | false`**:
- `false`: Rujukan berhasil diverifikasi di Semantic Scholar (kemiripan $\ge 0.70$).
- `true`: Rujukan gagal diverifikasi setelah melalui kueri DOI dan pencarian judul fallback.
- Jika API mengalami gangguan (*degradation*), sinyal ini **wajib ditiadakan (*omitted*)** (`absent != false`), sehingga tidak menghasilkan vonis fabrikasi palsu.

---

## 3. Pola Kueri (Query Patterns)

### Pola 1: Pencarian Berbasis Judul (Metode Fallback & Non-DOI)

Gunakan endpoint ini untuk mencari karya ilmiah berdasarkan judul draf kalimat:
```http
GET /paper/search?query={url_encoded_title}&limit=5&fields=title,authors,year,externalIds,venue,publicationDate
```
*(Catatan efisiensi payload: jangan meminta field `citationCount` pada pencarian awal).*

**Aturan Pencocokan & Bonus Tie-Breaker**:
- Hitung kemiripan Levenshtein antara judul kueri dan setiap judul hasil pencarian (huruf kecil, tanda baca dihilangkan).
- Ambang batas penerimaan: **kemiripan $\ge 0.70$**.
- **Bonus Tie-Breaker Tahun (+0.05)**: Jika beberapa kandidat memenuhi nilai $\ge 0.70$, tambahkan bonus skor `+0.05` pada kandidat yang tahun terbitnya cocok (atau $\pm 1$ tahun toleransi pencatatan).
- Kandidat dengan skor gabungan tertinggi dipilih.

---

### Pola 2: Pencarian Berbasis DOI (Primer jika DOI Tersedia)

Gunakan endpoint ini ketika DOI sudah teridentifikasi:
```http
GET /paper/DOI:{doi}?fields=title,authors,year,externalIds,venue,publicationDate,citationCount
```

**Aturan Pencocokan & Deteksi `DOI_MISMATCH`**:
- Pencocokan DOI bersifat mutlak (*exact*).
- **Verifikasi Silang Judul**: Judul yang dikembalikan oleh S2 wajib diuji terhadap judul referensi draf menggunakan kemiripan Levenshtein.
- **Deteksi `DOI_MISMATCH` & Alur Fall-Through**:
  - Jika judul yang dikembalikan memiliki kemiripan **$< 0.70$**, tandai sebagai **`DOI_MISMATCH`** (indikasi halusinasi di mana DOI valid merujuk ke paper yang tidak berhubungan).
  - **Wajib Beralih (*Fall-Through*) ke Pencarian Judul**: Ketika terjadi `DOI_MISMATCH` atau DOI mengembalikan status 404, sistem **tidak langsung menetapkan status unmatched**, melainkan wajib melanjutkan eksekusi ke Pola 1 (Pencarian Judul).

---

### Pola 3: Pencarian Berbasis Semantic Scholar ID (Re-verifikasi & Deduplikasi)

```http
GET /paper/{paperId}?fields=title,authors,year,externalIds,venue,publicationDate,citationCount
```
Digunakan saat melakukan verifikasi ulang pada entri yang telah memiliki ID resmi Semantic Scholar pada basis data sitasi.

---

## 4. Gerbang Proteksi Judul Wajib Persis (#431 Exact-Title-or-Bust Gate)

Untuk menghindari hasil keliru (*false-positive*) pada karya ilmiah berbeda dari penulis yang sama (misal: dokumen koreksi/*erratum*, tanggapan/*reply*, atau seri *Part I / Part II*):
1. Skor rasio kemiripan Levenshtein wajib **$\ge 0.70$**.
2. Pada jalur fallback judul, kandidat **wajib lolos pencocokan identik ternormalisasi (*exact normalized title match*)**, dengan penyeragaman singkatan bertitik (misal: `"R.A.G."` identik dengan `"RAG"`).
3. **Penolakan Judul Generik**: Judul yang tergolong generik murni (seperti *"Editorial"*, *"Case Report"*, *"Introduction"*, *"Review"*) **ditolak pada pencarian judul murni** jika tidak didukung oleh nomor DOI resmi.

---

## 5. Penanganan Respons API & Outage Latch

### Ketika Ditemukan Kecocokan (Match Berhasil)
Catat informasi berikut ke dalam riwayat audit verifikasi referensi:
- `semantic_scholar_id`: ID unik paper di Semantic Scholar (misal: `"649def34f8be52c8b66281af98ae884c09aef38b"`).
- `s2_title`: Judul resmi yang terdaftar.
- `s2_authors`: Daftar lengkap penulis.
- `s2_year`: Tahun publikasi resmi.
- `s2_venue`: Nama jurnal atau konferensi resmi.
- `match_score`: Skor rasio kemiripan Levenshtein.
- `verification_method`: `"s2_doi_lookup"` atau `"s2_title_search"`.

### Penanganan Galat API & Mekanisme Penguncian Gangguan (*Outage Latch*)
- **HTTP 429 (Rate Limit)**: Terapkan jeda 2 detik, ulangi hingga maksimal 3 kali.
- **HTTP 5xx**: Lewati pemeriksaan S2 untuk rujukan ini, beralih ke Crossref / OpenAlex.
- **Gangguan Jaringan / Soket Timeout**:
  - Terapkan mekanisme *Outage Latch* (`_latched_unavailable = True`): jika terjadi timeout jaringan, kunci status S2 sebagai *unavailable* untuk seluruh sisa batch agar tidak membuang waktu 30 detik per entri.
  - Catat log peringatan: `[S2-API-UNAVAILABLE]`.
  - Sistem dapat me-reset status penguncian antar-batch menggunakan fungsi reset berkala.

---

## 6. Deduplikasi Berbasis Semantic Scholar ID

Ketika dua referensi draf menghasilkan `semantic_scholar_id` yang sama, tandai entri tersebut sebagai rujukan duplikat. Sistem akan mempertahankan entri dengan metadata bibliografi paling lengkap (versi terbitan resmi jurnal ber-DOI lebih diutamakan daripada draf pra-cetak awal). Jika sebuah sumber tidak ditemukan di S2, tandai sebagai `s2_unresolved` dan lanjutkan pengujian ke Crossref / OpenAlex.

---

## 7. Batasan Fallback Peramban Web (Browser Fallback Boundary)

- Pencarian via API terstruktur adalah saluran pengambilan data utama (*primary retrieval channel*).
- Penelusuran berbasis peramban web (*WebSearch / WebFetch*) hanyalah fallback terbatas untuk memeriksa keabsahan landing page penerbit ketika metadata API tidak lengkap atau saling bertentangan.
- Dilarang keras menggunakan penelusuran peramban web untuk memotong (*bypass*) batasan *rate limit* API resmi.
