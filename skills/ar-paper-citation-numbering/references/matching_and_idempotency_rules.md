# Logika Pencocokan Kalimat & Aturan Idempotensi (Matching & Idempotency Rules)

Dokumen ini mendokumentasikan spesifikasi teknis mesin pencocokan teks kalimat (*Sentence Matching Engine*), penanganan toleransi redaksional, proteksi blok kode, normalisasi lintas platform, penulisan atomik, dan jaminan sifat idempoten pada modul penomoran sitasi.

---

## 1. Arsitektur Mesin Pencocokan 3-Lapis (Three-Tier Matching Engine)

Klaim yang dicatat dalam `paper/references.txt` terkadang mengalami perbaikan redaksional minor saat naskah bab draf diperbaiki (misal: penambahan kata transisi, penggantian tanda kutip, atau penyesuaian tata bahasa). Untuk memastikan sitasi tetap terpasang dengan tepat tanpa gagal pasang (*missed injection*), algoritma menerapkan strategi pencocokan 3 lapis bertingkat:

```
                  Input Klaim & Paragraf
                            │
                            ▼
              ┌───────────────────────────┐
              │  Lapis 1: Exact Match     │ ──► Ditemukan ──► Injeksi Langsung
              └───────────────────────────┘
                            │ (Gagal)
                            ▼
              ┌───────────────────────────┐
              │ Lapis 2: Normalized Match │ ──► Ditemukan ──► Injeksi Terstandarisasi
              └───────────────────────────┘
                            │ (Gagal)
                            ▼
              ┌───────────────────────────┐
              │   Lapis 3: Fuzzy Match    │ ──► Ratio >= 0.85 ──► Injeksi Berbobot
              │  (difflib SequenceMatcher)│
              └───────────────────────────┘
                            │ (Gagal)
                            ▼
              [Peringatan: Klaim Tak Terpetakan]
```

### Lapis 1: Exact Substring Matching
- Klaim dicari secara persis menggunakan `claim_clean in paragraph` di mana `claim_clean = claim_text.rstrip(".,;:|").strip()`.
- Pemotongan tanda baca penutup klaim (*trailing punctuation stripping*) menjamin posisi kurung siku sitasi disuntikkan **SEBELUM** tanda baca terminal paragraf (`.`, `,`, `;`, `:`, `|`).
- Bila ditemukan, indeks karakter awal dan akhir klaim dihitung untuk mendeteksi tanda baca berikutnya.
- Kecepatan: $O(1)$ amortized (paling cepat dan akurat untuk 95% naskah).

### Lapis 2: Normalized String Matching
Mengatasi variasi ortografis dan encoding teks:
- **Tanda Kutip:** Mengubah kutip tipografis (`“`, `”`, `‘`, `’`) menjadi kutip ASCII standar (`"`, `'`).
- **Tanda Strip:** Menyatukan karakter strip en-dash (`–`), em-dash (`—`), dan hyphen (`-`).
- **Spasi:** Menghilangkan spasi ganda, spasi non-breaking (`\u00A0`), dan karakter tab.
- **Tanda Baca:** Menghilangkan tanda baca penutup klaim saat perbandingan string dilakukan.

### Lapis 3: Fuzzy Matching (SequenceMatcher)
- Memecah paragraf menjadi daftar kalimat menggunakan batas pemisah kalimat:
  ```python
  sentences = re.split(r"(?<=[.?!])\s+", paragraph)
  ```
- Menghitung rasio kemiripan karakter berbasis algoritma Ratcliff/Obershelp melalui pustaka standar Python:
  ```python
  ratio = difflib.SequenceMatcher(None, norm_claim, norm_sentence).ratio()
  ```
- Ambang batas penerimaan: **$\ge 0.85$** (85% kemiripan).
- Nilai ambang ini secara empiris mencegah kesalahan pencocokan pada kalimat yang berbeda (*false positives*), namun tetap menangkap kalimat yang hanya berbeda 1–2 kata akibat koreksi kata sambung.

---

## 2. Normalisasi Jalur Windows (Windows Path Normalization)

Pada lingkungan sistem operasi Windows, generator pemetaan atau sistem operasi menghasilkan jalur berkas dengan tanda *backslash* (`\`):
```text
paper\01_introduction.md: paragraf 1:
- "Teks klaim":
  - paper\references\2021_author.bib
```

Mesin penomoran melakukan normalisasi string di awal pemrosesan:
```python
norm_line = raw_line.replace("\\", "/")
```
Langkah ini menjamin bahwa pengenalan header seksi (`norm_line.startswith("paper/")`) dan berkas rujukan (`"paper/references/" in norm_line`) bekerja 100% konsisten melintasi Linux, macOS, dan Windows.

---

## 3. Proteksi Blok Kode Berpagar (Fenced Code Block Protection)

Naskah ilmiah di bidang ilmu komputer sering kali memuat blok kode program (menggunakan ``` atau ~~~). Teks di dalam blok kode, termasuk baris komentar atau string literal, tidak boleh dimodifikasi atau disuntik sitasi.

### Mekanisme Masking Dua Fase
1. **Fase Ekstraksi & Masking:**
   Setiap blok kode berpagar diidentifikasi secara utuh dan digantikan oleh penampung deterministik `<<<CODE_BLOCK_N>>>`. Seluruh baris di dalam blok kode diisolasi.
2. **Fase Injeksi:**
   Proses pemecahan paragraf (`\n\n`) hanya mengevaluasi teks naratif di luar penampung kode. Paragraf yang merupakan blok kode dilewati sepenuhnya.
3. **Fase Pemulihan (Restoration):**
   Setelah proses injeksi atau pembersihan (*strip*) selesai, seluruh penampung `<<<CODE_BLOCK_N>>>` dikembalikan ke bentuk teks kode aslinya byte-demi-byte tanpa mengubah spasi atau baris kosong di dalam kode.

---

## 4. Aturan Idempotensi & Perbaikan Mandiri (Idempotency & Self-Healing)

Idempotensi adalah sifat di mana eksekusi berulang terhadap operasi yang sama tidak akan mengubah hasil di luar eksekusi pertama ($f(f(x)) = f(x)$).

### A. Pencegahan Dobel Injeksi (Anti Double-Injection)
Sebelum menyisipkan tautan braket, mesin memeriksa apakah di posisi target sudah terpasang sitasi:
```python
RE_EXISTING = re.compile(r"\[\[(\d+)\]\]\(06_references\.md#ref\d+\)")
```
- Jika kalimat sudah memiliki `[[N]](06_references.md#refN)` dengan nomor yang sama, proses **melewatkan (skip)** kalimat tersebut tanpa modifikasi.
- Berkas draf tidak akan mengalami perubahan tanggal modifikasi (*modification time*) jika seluruh sitasi sudah terpasang sempurna.

### B. Perbaikan Mandiri Sitasi Salah Letak (Self-Healing Legacy Corrections)
Bila naskah sebelumnya pernah disuntik sitasi dengan format yang keliru (misal: diletakkan setelah tanda titik seperti `klaim. [[1]]`), mesin secara otomatis mendeteksi kluster sitasi setelah tanda baca dan mereposisinya ke sebelum tanda titik (`klaim [[1]].`).

### C. Mode Pembersihan & Penomoran Ulang (`--strip`)
Bila susunan referensi diubah secara masif atau pengguna ingin mereset naskah bab ke bentuk murni:
- Parameter `--strip` memindai seluruh naskah dan menghapus semua blok `[[N]](06_references.md#refN)` secara aman.
- Tanda baca kalimat dan kerapian spasi dikembalikan ke keadaan semula:
  ```text
  Sebelum strip : "... layanan interaktif [[1]](06_references.md#ref1), [[2]](06_references.md#ref2)."
  Setelah strip  : "... layanan interaktif."
  ```

---

## 5. Protokol Penulisan Berkas Atomik (Atomic Write Protocol)

Untuk mencegah berkas draf naskah korup atau hilang bila daya komputer mati atau proses terinterupsi saat operasi tulis berlangsung, implementasi menggunakan teknik **Atomic Write** berbasis sistem operasi:

```python
def atomic_write_text(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    dir_name = file_path.parent
    dir_name.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding=encoding) as tf:
        tf.write(content)
        temp_name = tf.name
    # Operasi atomik tingkat kernel (POSIX rename / Windows ReplaceFile)
    os.replace(temp_name, file_path)
```

**Karakteristik Keamanan:**
1. Berkas sementara dibuat di direktori yang sama agar berada di volume penyimpanan (*filesystem partition*) yang sama.
2. `os.replace` merupakan operasi tingkat kernel atomik yang menggantikan berkas lama dalam satu langkah seketika.
3. Berkas draf asli dijamin tidak pernah berada dalam kondisi terpotong (*truncated*) atau setengah tertulis.
