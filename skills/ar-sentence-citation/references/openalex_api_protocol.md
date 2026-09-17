# Protokol Verifikasi & Kueri OpenAlex API

Dokumen ini mendefinisikan protokol kueri dan verifikasi indeks bibliografi terprogram menggunakan OpenAlex API untuk mendukung triangulasi multi-indeks dan validasi sitasi terbuka global.

---

## 1. Informasi Dasar & Batas Kecepatan (Rate Limits)

- **API Base URL**: `https://api.openalex.org`
- **Rate Limit**:
  - Kuota harian freemium terkelola.
  - *Pacing Klien*: 10 request/detik (dengan API key atau email polite pool), 1 request/detik (anonim).
  - Batas ledakan (*burst cap*): hingga 100 request/detik.
- **Variabel Lingkungan & Penanganan Kredensial**:
  - `OPENALEX_API_KEY`: Kunci API gratis dari `https://openalex.org/settings/api`.
  - `OPENALEX_POLITE_EMAIL`: Alamat email kontak pengguna.
  - *Catatan Implementasi*: Kredensial (`api_key` dan `mailto`) dikirimkan sebagai **URL Query Parameters** (`?api_key=...&mailto=...`), bukan sebagai header khusus. Sistem wajib melakukan penyensoran query string pada pesan log galat (*credential scrubbing*) agar kunci API tidak bocor.

---

## 2. Peran dalam Triangulasi Multi-Indeks

OpenAlex adalah katalog pengetahuan sains terbuka berskala besar (penerus Microsoft Academic Graph / MAG). Cakupan OpenAlex sangat kuat dalam melengkapi Semantic Scholar dan Crossref, khususnya untuk:
- Publikasi akses terbuka (*Open Access / OA*).
- Monograf, tesis, dan bab buku akademik.
- Karya ilmiah yang tidak memiliki nomor DOI resmi.

Triangulasi lintas indeks secara dramatis menurunkan angka kepalsuan positif (*false-positive rate*). Sebuah karya yang tidak terindeks di Semantic Scholar tetapi terverifikasi di OpenAlex menunjukkan adanya kesenjangan indeksasi repositori, bukan bukti fabrikasi referensi.

---

## 3. Pola Kueri (Query Patterns)

### Pola 1: Pencarian Berbasis DOI dengan Cross-Check Judul (Primer jika DOI tersedia)

Gunakan endpoint berikut ketika nomor DOI telah diketahui:
```http
GET /works/doi:{doi}?select=id,title,authorships,publication_year,doi,primary_location
```
> [!NOTE]
> OpenAlex mewajibkan awalan `doi:` pada path URL (misal: `/works/doi:10.1145/3290605.3300233`).

**Aturan Pencocokan & Deteksi `DOI_MISMATCH`**:
- Hasil kueri DOI wajib diverifikasi silang (*cross-check*) terhadap judul paper yang diklaim menggunakan kemiripan Levenshtein.
- Jika judul yang dikembalikan oleh OpenAlex memiliki kemiripan **$< 0.70$** terhadap judul target, hasil DOI ditolak (`DOI_MISMATCH`). Sistem kemudian otomatis beralih (*fall through*) ke Pola 2 (pencarian judul).

---

### Pola 2: Pencarian Berbasis Judul (Fallback jika DOI tidak ada atau terjadi DOI_MISMATCH)

Gunakan endpoint pencarian teks bebas berikut:
```http
GET /works?search={url_encoded_title}&per-page=5&select=id,title,authorships,publication_year,doi,primary_location
```

**Aturan Pencocokan & Tie-Breaker**:
- Normalisasi teks: ubah ke huruf kecil, hilangkan tanda baca, dan hilangkan spasi berlebih.
- Ambang batas penerimaan: **kemiripan $\ge 0.70$**.
- Jika terdapat beberapa kandidat yang memenuhi ambang batas:
  1. Utamakan kandidat yang memiliki tahun publikasi yang sama (bonus $+0.05$).
  2. Utamakan kandidat dengan skor kemiripan tertinggi.
  3. Utamakan kandidat yang memiliki nomor DOI terisi.

---

## 4. Gerbang Proteksi Judul Wajib Persis (#431 Exact-Title-or-Bust Gate)

Untuk menghindari false-positive pada karya ilmiah berbeda dari penulis yang sama:
1. Skor rasio kemiripan Levenshtein wajib **$\ge 0.70$**.
2. Kandidat pada jalur pencarian judul (fallback) **wajib lolos pencocokan identik ternormalisasi (*exact normalized title match*)**, dengan penyeragaman singkatan bertitik (misal: `"R.A.G."` identik dengan `"RAG"`).
3. **Penolakan Judul Generik**: Judul yang tergolong generik murni (seperti *"Editorial"*, *"Case Report"*, *"Introduction"*, *"Review"*) **ditolak pada pencarian judul murni** jika tidak didukung oleh nomor DOI resmi.

---

## 5. Penentuan Status `openalex_unmatched`

Status `openalex_unmatched = true` ditetapkan jika dan hanya jika:
- **DOI Tersedia**: Kueri DOI gagal atau tidak lolos cross-check judul ($< 0.70$), DAN pencarian judul fallback juga tidak menghasilkan kandidat yang memenuhi ambang batas $\ge 0.70$; ATAU
- **DOI Tidak Tersedia**: Pencarian judul murni tidak menghasilkan kandidat yang memenuhi ambang batas $\ge 0.70$.

Pengecekan ini dilewati (*skipped*) untuk rujukan manual yang dimasukkan langsung oleh peneliti.

---

## 6. Penanganan Degradasi Jaringan & Galat

| Kondisi Galat | Tindakan Sistem |
|:---|:---|
| **HTTP 429** dengan header `X-RateLimit-Remaining: 0` | Kuota harian habis total (akan reset pada tengah malam UTC). Percobaan ulang tidak akan berhasil. Segera lewati OpenAlex untuk sesi ini tanpa menunggu (*no retry*). |
| **HTTP 429** (Batas lonjakan sementara / burst) | Lakukan *exponential backoff* (2s $\rightarrow$ 4s $\rightarrow$ 8s) hingga maksimal 3 kali percobaan. |
| **HTTP 5xx** (Gangguan Server) | Langsung lewati OpenAlex tanpa mencoba ulang. |
| **Network Timeout** (30 detik) | Putuskan sambungan dan lanjutkan alur kerja. |
| **OpenAlex Tidak Tersedia** | Hilangkan sinyal `openalex_unmatched` dari hasil akhir (`absent != false`). Indeks lain tetap berjalan independen. |

---

## 7. Batasan Fallback Peramban Web (Browser Fallback Boundary)

- Pencarian via API terstruktur adalah saluran pengambilan data utama (*primary retrieval channel*).
- Penelusuran berbasis peramban web (*WebSearch / WebFetch*) hanyalah fallback terbatas untuk inspeksi halaman resmi penerbit ketika metadata API tidak lengkap atau saling bertentangan.
- Dilarang keras menggunakan penelusuran peramban web untuk memotong batasan kuota harian API resmi OpenAlex.
