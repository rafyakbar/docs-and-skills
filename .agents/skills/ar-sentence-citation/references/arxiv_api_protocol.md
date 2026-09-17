# Protokol Verifikasi & Kueri arXiv API

Dokumen ini mendefinisikan protokol kueri dan verifikasi bibliografi untuk naskah pra-cetak (*preprints*) menggunakan arXiv Query API. Protokol ini melengkapi indeks literatur terbitan resmi dengan memeriksa naskah pra-cetak bidang Ilmu Komputer (CS), Kecerdasan Buatan (AI), Matematika, dan Fisika.

---

## 1. Informasi Dasar & Syarat Penggunaan (Terms of Use / ToU)

- **API Base URL**: `http://export.arxiv.org/api/query`
- **Rate Limit Mutlak**:
  - **Maksimal 1 request setiap 3 detik** (interval minimal 3 detik antarkueri).
  - **Koneksi Tunggal**: Dilarang membuka koneksi paralel simultan.
  - Pembatasan ini berlaku untuk seluruh mesin klien di bawah kendali pemanggil. Melakukan *multi-connection fan-out* untuk mengakali batasan kecepatan dilarang keras oleh arXiv dan memicu pemblokiran IP permanen.
- **Header Khusus**: Tidak ada mekanisme *polite pool* atau kunci API khusus pada arXiv.

---

## 2. Format Respons XML Atom 1.0

Berbeda dengan repositori berbasis JSON lainnya, arXiv API mengembalikan dokumen berformat **Atom 1.0 XML Feed** (namespace `{http://www.w3.org/2005/Atom}`).
- Hasil pencarian yang cocok menghasilkan satu atau lebih elemen `<entry>`.
- Hasil pencarian yang tidak menemukan paper menghasilkan feed XML valid dengan **nol elemen `<entry>`** (bukan galat HTTP 404).
- Field kunci yang dibaca dari elemen `<entry>`:
  - `<entry><title>`: Judul karya ilmiah (spasi ganda dan baris baru bawaan arXiv dinormalisasi menjadi spasi tunggal).
  - `<entry><published>`: Timestamp ISO-8601; 4 digit awal menunjukkan tahun publikasi resmi untuk perbandingan *tie-breaker*.

---

## 3. Pola Kueri (Query Patterns)

### Pola 1: Pencarian Berbasis arXiv ID dengan Cross-Check Judul (Primer jika ID tersedia)

Gunakan parameter `id_list` ketika pengenal arXiv (misal: `2303.08774` atau `cs/0101001`) diketahui:
```http
GET http://export.arxiv.org/api/query?id_list={arxiv_id}
```

**Aturan Pencocokan & Deteksi Ketidakcocokan ID**:
- Respons diuji silang terhadap judul draf menggunakan batas kemiripan **Levenshtein $\ge 0.70$**.
- Jika ID ditemukan namun kemiripan judul $< 0.70$, tandai sebagai ketidakcocokan ID (`ID_MISMATCH`), tolak hasil ID tersebut, dan lakukan pencarian ulang berbasis judul (*fall through*).
- Feed kosong (nol `<entry>`) menandakan ID tidak terdaftar.

---

### Pola 2: Pencarian Berbasis Judul (Fallback jika ID tidak ada atau terjadi ID_MISMATCH)

Gunakan kueri bidang judul (`ti:`):
```http
GET http://export.arxiv.org/api/query?search_query=ti:"{url_encoded_title}"&max_results=5
```

**Aturan Pencocokan & Tie-Breaker**:
- Kemiripan Levenshtein $\ge 0.70$.
- Jika beberapa entri lolos ambang batas, berikan bonus $+0.05$ untuk kesesuaian tahun dari tag `<published>`.

---

## 4. Gerbang Proteksi Judul Wajib Persis (#431 Exact-Title-or-Bust Gate)

Untuk menghindari salah pencocokan preprint dari penulis yang sama:
1. Skor rasio kemiripan Levenshtein wajib **$\ge 0.70$**.
2. Kandidat pada jalur pencarian judul (fallback) **wajib lolos pencocokan identik ternormalisasi (*exact normalized title match*)**, dengan penyeragaman singkatan bertitik (misal: `"R.A.G."` identik dengan `"RAG"`).
3. **Penolakan Judul Generik**: Judul generik murni (seperti *"Editorial"*, *"Introduction"*, *"Review"*) **ditolak pada pencarian judul murni** jika tidak didukung oleh arXiv ID resmi.

---

## 5. Aturan Gating: Kapan arXiv Diaktifkan

> [!IMPORTANT]
> **Pengecekan arXiv Berbasis Keberadaan ID (*ID-Gated Applicability*)**
> Verifikasi arXiv **HANYA** diaktifkan bila rujukan memiliki pengenal arXiv ID atau secara eksplisit diklaim sebagai naskah pra-cetak arXiv.
> 
> Referensi artikel jurnal atau buku yang tidak memuat penanda arXiv berstatus **dilewati (*skipped*)**, bukan berstatus *unmatched*. Artikel jurnal cetak tidak boleh disematkan status gagal verifikasi arXiv karena ketiadaannya di arXiv adalah hal yang wajar.

Status `arxiv_unmatched = true` ditetapkan jika dan hanya jika:
- Sitasi **memiliki arXiv ID**, DAN
- Kueri ID mengembalikan feed kosong atau gagal uji kemiripan judul, DAN
- Pencarian judul cadangan juga tidak menemukan entri yang memenuhi ambang batas $\ge 0.70$.

---

## 6. Penanganan Degradasi Jaringan & Galat

| Kondisi Galat | Tindakan Sistem |
|:---|:---|
| **Feed Kosong** (0 `<entry>`) | Dianggap sebagai *miss* wajar. Sistem melanjutkan ke pencarian judul fallback. |
| **HTTP 200 dengan Root Non-Atom** | Respons HTML dari server CDN/proxy (bukan XML Atom feed) diperlakukan sebagai **Degradasi Layanan (`ArxivUnavailable`)**, BUKAN sebagai miss feed kosong. Hal ini mencegah sinyal palsu `arxiv_unmatched`. |
| **HTTP 429** (Rate Limit) | Terapkan jeda minimal 3 detik (sesuai batas ToU), ulangi maksimal 3 kali. Jika terus berlanjut, lewati arXiv. |
| **HTTP 5xx** | Segera lewati arXiv tanpa pengulangan (*immediate skip*). |
| **Network Timeout** (30 detik) | Putuskan koneksi dan lewati arXiv. |
| **arXiv Tidak Tersedia** | Hilangkan sinyal verifikasi arXiv dari hasil evaluasi (`absent != false`) tanpa mematikan alur kerja keseluruhan. |

---

## 7. Batasan Fallback Peramban Web (Browser Fallback Boundary)

- Inspeksi langsung ke tautan web `https://arxiv.org/abs/<id>` hanya diizinkan untuk memeriksa catatan penarikan (*withdrawal notes*) atau versi revisi paper yang ambigu.
- Dilarang keras melakukan crawling massal, mengunduh berkas PDF dalam jumlah besar, atau menggunakan skrip multi-threading untuk melewati aturan batas 1 request per 3 detik.
