---
name: ar-citation-numbering
description: "Aktifkan ketika pengguna meminta untuk menyuntikkan (inject), menomori, memperbarui, atau menyinkronkan nomor sitasi braket interaktif [[N]](06_references.md#refN) ke dalam draf naskah bab (paper/*.md) berdasarkan berkas pemetaan paper/references.txt dan daftar pustaka paper/06_references.md. Mendukung penempatan tanda baca presisi sebelum titik/koma (IEEE style), multi-sitasi terpisah, sitasi naratif, pencegahan duplikasi (idempotensi), dan audit zero-orphan. Kata kunci pemicu: inject citation, nomori sitasi, citation numbering, in-text citation, sinkronkan sitasi naskah, hubungkan sitasi, bracket citations, pasang nomor referensi. JANGAN aktifkan untuk membuat outline (gunakan ar-paper-outline), menulis draf bab baru (gunakan ar-paper-draft), mencari sitasi kalimat (gunakan ar-sentence-citation), atau mengompilasi naskah 06_references.md (gunakan ar-reference-compiler)."
license: MIT
metadata:
  author: Rafy
---

# Penomoran & Penautan Sitasi Teks Naskah (In-Text Citation Numbering & Linking)

## Gambaran Umum (Overview)

Skill ini menjalankan proses **penomoran deterministik, penyuntikan tautan braket interaktif markdown (`[[N]](06_references.md#refN)`), dan audit integritas sitasi dalam teks draf naskah bab (`paper/*.md`)**. Sebagai **Step 4** dalam alur penerbitan manuskrip akademik bereputasi (IEEE, Elsevier, Springer, Nature), skill ini menghubungkan hasil kurasi kalimat klaim Step 2 (`paper/references.txt`) dan naskah daftar pustaka akhir Step 3 (`paper/06_references.md`) ke dalam kalimat-kalimat draf naskah bab yang telah disusun pada Step 1 (`ar-paper-draft`).

> [!NOTE]
> **Fokus Khusus Step 4**
> Skill ini hanya menyisipkan nomor sitasi braket ke dalam teks draf naskah bab. Skill ini **TIDAK mengubah makna atau menulis ulang teks narasi draf** (ditulis pada Step 1 oleh `ar-paper-draft`), **TIDAK mencari literatur rujukan baru** (dikerjakan pada Step 2 oleh `ar-sentence-citation`), dan **TIDAK menyusun berkas daftar pustaka** (dikerjakan pada Step 3 oleh `ar-reference-compiler`).

## Kapan Mengaktifkan Skill Ini

- Pengguna meminta memberikan atau menyuntikkan nomor referensi ke seluruh kalimat klaim pada `paper/*.md`.
- Pengguna meminta menyinkronkan nomor sitasi teks draf dengan daftar pustaka `paper/06_references.md`.
- Pengguna meminta mengaudit konsistensi nomor sitasi, posisi tanda baca, atau mendeteksi sitasi yatim (*orphan citations*).
- Pengguna meminta membersihkan (*strip*) seluruh sitasi untuk mengembalikan draf bab ke bentuk teks polos atau melakukan penomoran ulang (*renumbering*).
- Kata kunci pemicu: `inject citation`, `nomori sitasi`, `citation numbering`, `in-text citation`, `sinkronkan sitasi naskah`, `hubungkan sitasi`, `bracket citations`, `pasang nomor referensi`.

## Kapan TIDAK Mengaktifkan Skill Ini

- Merancang struktur atau blueprint paragraf naskah paper dari nol (gunakan `ar-paper-outline` / Step 0).
- Menulis draf teks bab naskah per bagian (gunakan `ar-paper-draft` / Step 1).
- Mencari literatur ilmiah per kalimat atau menyusun pemetaan `paper/references.txt` (gunakan `ar-sentence-citation` / Step 2).
- Mengompilasi naskah daftar pustaka akhir `paper/06_references.md` dari berkas bibliografi (gunakan `ar-reference-compiler` / Step 3).
- Menulis atau menyunting ringkasan abstrak naskah `00_abstract.md` (gunakan `ar-paper-abstract` / Step 5).

## Ruang Lingkup (Scope)

- **Dalam Lingkup:** Ekstraksi nomor rujukan dari urutan kemunculan pertama pada `paper/references.txt`, pencocokan kalimat klaim 3-lapis (*Exact, Normalized, Fuzzy*), penyuntikan tautan braket interaktif `[[N]](06_references.md#refN)` sebelum tanda baca terminal (`.`, `,`, `;`, atau `|`), penanganan multi-sitasi terpisah, sitasi naratif, sitasi tabel, jaminan sifat idempoten (anti duplikasi), dan verifikasi kepatuhan *zero-orphan*.
- **Luar Lingkup:** Menulis teks draf baru dari nol, mengunduh file `.bib` baru, mengubah isi entri referensi pada `06_references.md`, atau mengarang nomor sitasi fiktif.

---

## Langkah Wajib 0: Verifikasi Prasyarat Input

Sebelum memulai proses penomoran sitasi, pastikan berkas-berkas berikut telah tersedia:

1. **Berkas Pemetaan Tersedia**: `paper/references.txt` memuat pemetaan kalimat draf terhadap berkas rujukan di `paper/references/`.
2. **Daftar Pustaka Lengkap**: `paper/06_references.md` sudah dikompilasi dan memuat tag anchor `<a id="refN"></a>\n[N]`.
3. **Berkas Bab Draf Siap**: Berkas bab draf (`paper/01_introduction.md`, `paper/02_related-works.md`, dst.) telah selesai ditulis.

---

## Arsitektur Berkas Penomoran Sitasi

Struktur alur berkas yang terlibat pada Step 4:

```text
paper/
├── references.txt                # INPUT 1: Master mapping klaim -> file rujukan
├── 06_references.md              # INPUT 2: Naskah daftar pustaka ber-anchor <a id="refN"></a>
├── 01_introduction.md            # TARGET INJEKSI: Draf bab naskah modular
├── 02_related-works.md
├── 03_materials-and-methods_*.md
├── 04_results-and-discussion_*.md
└── 05_conclusion.md
```

Contoh Hasil Injeksi pada Teks Kalimat:
```markdown
# Sebelum Injeksi (Hasil Step 1):
Pengenalan otomatis atribut demografis wajah memegang peranan penting dalam berbagai domain aplikasi cerdas, termasuk sistem forensik digital, kontrol akses biometrik, interaksi manusia-komputer, dan personalisasi layanan interaktif.

# Setelah Injeksi (Hasil Step 4):
Pengenalan otomatis atribut demografis wajah memegang peranan penting dalam berbagai domain aplikasi cerdas, termasuk sistem forensik digital, kontrol akses biometrik, interaksi manusia-komputer, dan personalisasi layanan interaktif [[1]](06_references.md#ref1), [[2]](06_references.md#ref2).
```

---

## Protokol Eksekusi Penomoran Sitasi

### 1. Registrasi Urutan Kemunculan Pertama (IEEE Monotonic Order)
- Ekstrak seluruh rujukan unik dari `paper/references.txt` berdasarkan urutan pertama kali muncul pada naskah.
- Petakan setiap berkas referensi ke indeks integer $N = 1, 2, 3, \dots, K$.
- Verifikasi keselarasan nomor $N$ dengan entri `[N]` pada `paper/06_references.md`.

### 2. Pencocokan Kalimat Klaim Multi-Lapis (Sentence Matching Engine)
- **Lapis 1 (Exact Match):** Cari substring teks klaim persis di dalam paragraf.
- **Lapis 2 (Normalized Match):** Hilangkan perbedaan variasi kutip (`“`, `”`, `'`), en-dash/em-dash, spasi ganda, dan titik akhir klaim.
- **Lapis 3 (Fuzzy Match):** Bila ada revisi redaksional minor pada draf, gunakan algoritma `difflib.SequenceMatcher` dengan batas ambang kemiripan $\ge 0.85$.

### 3. Konstruksi Tautan Braket Interaktif
- Ambil nomor referensi pendukung klaim, lakukan deduplikasi, dan urutkan secara menaik (*ascending order*).
- Bangun string tautan:
  - Sitasi Tunggal: `[[1]](06_references.md#ref1)`
  - Multi-Sitasi Terpisah: `[[1]](06_references.md#ref1), [[2]](06_references.md#ref2)`
- Tautan diskrit dipertahankan agar setiap nomor dapat diklik secara interaktif langsung menuju jangkar `<a id="refN"></a>` pada daftar pustaka.

### 4. Penempatan Tanda Baca Sadar Konteks (Punctuation Placement)
- Nomor sitasi diletakkan persis di ujung kata terakhir klaim, dipisahkan satu spasi, dan menempel **SEBELUM** tanda baca penutup kalimat:
  - Sebelum titik: `... personalisasi layanan interaktif [[1]](06_references.md#ref1), [[2]](06_references.md#ref2).`
  - Sebelum koma: `... dipelajari secara simultan [[6]](06_references.md#ref6), sedangkan ...`
  - Sebelum pembatas tabel: `| MD-ViT [[20]](06_references.md#ref20) | 89.07% |`
  - Sitasi Naratif: `Menurut Sunitha et al. [[13]](06_references.md#ref13), pendekatan CNN ...`

### 5. Jaminan Idempotensi & Keamanan Tulis Atomik
- **Anti Dobel Injeksi:** Periksa apakah kalimat sudah memuat tautan sitasi yang sama. Jika sudah ada, lewati (*skip*).
- **Atomic Write:** Penulisan berkas menggunakan temporary file dan `os.replace` tingkat kernel untuk mencegah file draf korup bila proses terputus.

---

## Panduan Do and Don't

| Do | Don't |
|:---|:---|
| Letakkan nomor sitasi **SEBELUM** tanda baca titik (`.`), koma (`,`), atau titik koma (`;`) | Menempatkan nomor sitasi setelah tanda titik (`kalimat. [[1]]`) |
| Gunakan format tautan interaktif `[[N]](06_references.md#refN)` | Menggunakan teks kurung mati `[N]` tanpa tautan markdown |
| Pisahkan multi-sitasi dengan koma dan spasi: `[[1]], [[2]]` | Menggabungkan nomor di dalam satu kurung siku: `[1, 2]` |
| Urutkan nomor multi-sitasi secara menaik: `[[11]], [[12]], [[13]]` | Menulis nomor multi-sitasi secara acak: `[[13]], [[11]]` |
| Gunakan nomor yang sama secara konsisten saat merujuk sumber yang sama | Membuat nomor baru untuk sumber yang sudah pernah disitir |
| Pertahankan integritas kalimat asli tanpa mengubah substansi kata | Mengubah susunan kalimat klaim saat menyisipkan sitasi |
| Jalankan audit integritas dua arah (*zero-orphan*) setelah penomoran | Membiarkan adanya sitasi di teks yang tidak ada di daftar pustaka |

---

## Skrip Pembantu CLI (Helper Scripts)

Skill ini dilengkapi dengan modul dan skrip CLI berbasis pustaka standar Python (Python 3.10+) pada direktori `scripts/`:

1. **Penyuntikan Nomor Sitasi ke Naskah Bab**:
   ```bash
   # Suntikkan nomor sitasi ke seluruh berkas bab naskah di folder paper/:
   python scripts/ars_citation_numberer.py -m paper/references.txt -r paper/06_references.md -d paper

   # Suntikkan sitasi hanya pada satu berkas bab tertentu (misal: 01_introduction.md):
   python scripts/ars_citation_numberer.py -m paper/references.txt -s paper/01_introduction.md

   # Mode Dry-Run (periksa perubahan di terminal tanpa mengubah berkas fisik):
   python scripts/ars_citation_numberer.py -m paper/references.txt -d paper --dry-run

   # Mode Strip (bersihkan seluruh sitasi braket untuk mengembalikan naskah ke teks polos):
   python scripts/ars_citation_numberer.py -m paper/references.txt -d paper --strip
   ```

2. **Audit Integritas Sitasi Naskah Bab (Zero-Orphan Audit)**:
   ```bash
   # Audit kepatuhan sitasi seluruh bab terhadap 06_references.md:
   python scripts/verify_citation_integrity.py -d paper -r paper/06_references.md

   # Luaran audit dalam format terstruktur JSON:
   python scripts/verify_citation_integrity.py -d paper -r paper/06_references.md --json
   ```

---

## Panduan Rujukan Teknis (Technical References)

Untuk protokol teknis, aturan tanda baca mendalam, dan penanganan kasus khusus, pelajari berkas-berkas rujukan di direktori `references/`:

- `references/citation_numbering_workflow.md`: Siklus operasional 6 tahap penomoran sitasi teks, integrasi pipeline naskah, dan penanganan galat.
- `references/ieee_in_text_guidelines.md`: Pedoman resmi penulisan sitasi IEEE, aturan spasi, multi-sitasi, sitasi naratif, dan sitasi dalam sel tabel.
- `references/matching_and_idempotency_rules.md`: Spesifikasi mesin pencocokan 3 lapis (*Exact, Normalized, Fuzzy*), aturan idempotensi, dan protokol atomic write.
- `references/zero_orphan_integrity_guide.md`: Protokol audit dua arah bebas yatim (*Zero-Orphan*), urutan kemunculan pertama monotonik IEEE, dan kriteria lolos audit.
