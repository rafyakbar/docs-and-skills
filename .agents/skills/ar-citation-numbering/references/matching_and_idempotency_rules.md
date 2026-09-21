# Logika Pencocokan Kalimat & Aturan Idempotensi (Matching & Idempotency Rules)

Dokumen ini mendokumentasikan spesifikasi teknis mesin pencocokan teks kalimat (*Sentence Matching Engine*), penanganan toleransi redaksional, penulisan atomik, dan jaminan sifat idempoten pada modul penomoran sitasi.

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
- Klaim dicari secara persis menggunakan `claim_text in paragraph`.
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

## 2. Aturan Idempotensi (Idempotency Guarantees)

Idempotensi adalah sifat di mana eksekusi berulang terhadap operasi yang sama tidak akan mengubah hasil di luar eksekusi pertama ($f(f(x)) = f(x)$).

### A. Pencegahan Dobel Injeksi (Anti Double-Injection)
Sebelum menyisipkan tautan braket, mesin memeriksa apakah di posisi target sudah terpasang sitasi:
```python
# Pola regex pendeteksi sitasi eksisting:
RE_EXISTING = re.compile(r"\[\[(\d+)\]\]\(06_references\.md#ref\d+\)")
```
- Jika kalimat sudah memiliki `[[N]](06_references.md#refN)` dengan nomor yang sama, proses **melewatkan (skip)** kalimat tersebut tanpa modifikasi.
- Berkas draf tidak akan mengalami perubahan tanggal modifikasi (*modification time*) jika seluruh sitasi sudah terpasang sempurna.

### B. Mode Pembersihan & Penomoran Ulang (`--strip`)
Bila susunan referensi diubah secara masif atau pengguna ingin mereset naskah bab ke bentuk murni:
- Parameter `--strip` memindai seluruh naskah dan menghapus semua blok `[[N]](06_references.md#refN)` secara aman.
- Tanda baca kalimat dan kerapian spasi dikembalikan ke keadaan semula:
  ```text
  Sebelum strip : "... layanan interaktif [[1]](06_references.md#ref1), [[2]](06_references.md#ref2)."
  Setelah strip  : "... layanan interaktif."
  ```

---

## 3. Protokol Penulisan Berkas Atomik (Atomic Write Protocol)

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
