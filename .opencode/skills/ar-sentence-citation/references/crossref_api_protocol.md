# Protokol Verifikasi & Kueri Crossref API

Dokumen ini mendefinisikan protokol kueri dan verifikasi bibliografi terprogram menggunakan Crossref API untuk memvalidasi keberadaan paper ilmiah ber-DOI dan mengekstrak metadatanya secara akurat.

---

## 1. Informasi Dasar & Batas Kecepatan (Rate Limits)

- **API Base URL**: `https://api.crossref.org`
- **Rate Limit**:
  - *Polite Pool*: 10 request/detik (dengan menyertakan alamat email pada header `User-Agent: ... (mailto:nama@domain.com)`).
  - *Anonymous*: ~5 request/detik (bervariasi tergantung beban server Crossref).
- **Variabel Lingkungan Email**: `CROSSREF_POLITE_EMAIL` (opsional namun sangat disarankan).

---

## 2. Tujuan & Peran dalam Triangulasi

Crossref adalah *registry of record* resmi untuk DOI (Digital Object Identifier) di seluruh dunia. Repositori ini memiliki cakupan terlengkap untuk artikel jurnal dan prosiding konferensi yang memiliki DOI resmi.

> [!NOTE]
> **Catatan Cakupan Monograf & Buku**: Cakupan Crossref sangat dominan pada artikel jurnal ber-DOI. Cakupan untuk bab buku (*book chapters*) dan monograf bergantung pada keikutsertaan penerbit dalam mendaftarkan DOI.

Dalam sistem verifikasi sitasi multi-indeks ($k=3$ / $k=4$), Crossref bertindak sebagai penentu keabsahan DOI primer bersama Semantic Scholar dan OpenAlex. Kegagalan pencarian di Crossref (`crossref_unmatched`) dicatat sebagai indikator ketidakberadaan sumber bila penelusuran judul juga gagal.

---

## 3. Pola Kueri (Query Patterns)

### Pola 1: Pencarian Berbasis DOI dengan Cross-Check Judul (Primer jika DOI tersedia)

Gunakan endpoint berikut ketika nomor DOI sudah diketahui:
```http
GET /works/{doi}
```
> [!NOTE]
> Masukkan nilai DOI murni tanpa awalan `doi:` (berbeda dengan OpenAlex yang menggunakan format `/works/doi:{doi}`).

**Aturan Pencocokan & Deteksi `DOI_MISMATCH`**:
Hasil kueri DOI wajib diverifikasi silang (*cross-check*) terhadap judul paper yang diklaim menggunakan perhitungan kemiripan Levenshtein:
1. Ambil elemen pertama dari daftar judul yang dikembalikan (`message.title[0]`).
2. Hitung rasio kemiripan Levenshtein antara judul target dan judul resmi dari Crossref (dalam format huruf kecil dan tanda baca dihilangkan).
3. Jika rasio kemiripan **$< 0.70$**, respons diklasifikasikan sebagai **`DOI_MISMATCH`** (indikasi halusinasi di mana DOI valid merujuk ke paper yang sama sekali berbeda). Sistem menolak hasil ini dan beralih ke pencarian judul (*fallback*).

---

### Pola 2: Pencarian Berbasis Judul (Fallback jika DOI tidak ada atau terjadi DOI_MISMATCH)

Gunakan endpoint berikut untuk mencari karya ilmiah berdasarkan judul:
```http
GET /works?query.title={url_encoded_title}&rows=5
```

**Aturan Pencocokan & Tie-Breaker**:
- Hitung kemiripan Levenshtein terhadap setiap kandidat pada `message.items`.
- Ambang batas penerimaan: **kemiripan $\ge 0.70$**.
- Jika terdapat beberapa kandidat yang memenuhi ambang batas $\ge 0.70$, berikan **bonus skor tie-breaker $+0.05$** untuk kandidat yang memiliki tahun publikasi yang cocok.
- Tahun publikasi kanonikal diambil dari field `issued.date-parts[0][0]` (atau fallback ke `published-print` / `published-online`).

---

## 4. Gerbang Proteksi Judul Wajib Persis (#431 Exact-Title-or-Bust Gate)

Untuk menghindari false-positive pada karya ilmiah berbeda dari penulis yang sama (misal: dokumen koreksi/*erratum*, tanggapan/*reply*, atau seri *Part I / Part II*):
1. Skor rasio kemiripan Levenshtein wajib **$\ge 0.70$**.
2. Kandidat pada jalur pencarian judul (fallback) **wajib lolos pencocokan identik ternormalisasi (*exact normalized title match*)**, dengan penyeragaman singkatan bertitik (misal: `"R.A.G."` identik dengan `"RAG"`).
3. **Penolakan Judul Generik**: Judul yang tergolong generik murni (seperti *"Editorial"*, *"Case Report"*, *"Introduction"*, *"Review"*) **ditolak pada pencarian judul murni** jika tidak didukung oleh nomor DOI resmi.

---

## 5. Penentuan Status `crossref_unmatched`

Status `crossref_unmatched = true` ditetapkan jika dan hanya jika:
1. **DOI Tersedia**: Kueri DOI mengembalikan 404 ATAU gagal pada cross-check judul ($< 0.70$), DAN pencarian judul fallback juga tidak menghasilkan satupun kandidat yang memenuhi ambang batas $\ge 0.70$; ATAU
2. **DOI Tidak Tersedia**: Pencarian judul murni tidak menghasilkan kandidat yang memenuhi ambang batas $\ge 0.70$.

Pengecekan ini hanya berlaku untuk rujukan yang diperoleh secara otomatis dari model AI, bukan entri manual yang telah divalidasi langsung oleh pengguna.

---

## 6. Pengabaian Field Klasifikasi (Aturan R-L3-2-D)

Crossref mengembalikan field `type` (seperti `journal-article`, `book-chapter`, `proceedings-article`). Sistem verifikasi sitasi **secara sadar mengabaikan (*ignores*) field ini** karena standardisasi kategori penerbit pada Crossref belum seragam dan tidak mempengaruhi pembuktian keberadaan fisik paper.

---

## 7. Penanganan Degradasi Jaringan & Galat

| Kondisi Galat | Tindakan Sistem |
|:---|:---|
| **HTTP 404** pada kueri DOI | Dianggap sebagai *miss* wajar. Sistem otomatis beralih (*fall through*) ke Pola 2 (pencarian judul). Bukan kegagalan sistem. |
| **HTTP 429** (Rate Limit terlampaui) | Terapkan jeda bertahap (*backoff*) 2 detik, ulangi hingga maksimal 3 kali. Segarkan jangkar throttle waktu. Jika tetap gagal, lewati Crossref untuk batch ini. |
| **HTTP 5xx** (Server Error) | Langsung lewati Crossref tanpa mencoba ulang (*immediate skip*). |
| **Network Timeout** (standar 30 detik) | Putuskan koneksi dan lewati Crossref. |
| **Crossref Tidak Tersedia** | Jika layanan Crossref mengalami gangguan, hilangkan sinyal `crossref_unmatched` dari evaluasi (`absent != false`). Indeks lain tetap berjalan independen. |

---

## 8. Batasan Fallback Peramban Web (Browser Fallback Boundary)

- Pencarian via API terstruktur adalah saluran pengambilan data utama (*primary retrieval channel*).
- Penelusuran berbasis peramban web (*WebSearch / WebFetch*) hanyalah fallback terbatas untuk inspeksi halaman resmi penerbit ketika metadata API tidak lengkap atau saling bertentangan.
- Dilarang keras menggunakan penelusuran peramban web untuk memotong batasan *rate limit* API resmi.
