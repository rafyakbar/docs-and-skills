---
name: ar-paper-reference-compiler
description: "Aktifkan ketika pengguna meminta untuk mengompilasi, memformat, menyusun, atau mengaudit naskah daftar pustaka akhir (06_references.md) dari berkas pemetaan paper/references.txt dan berkas catatan bibliografi (.bib, .ris, .nbib) di paper/references/. Mendukung berbagai gaya sitasi standar (IEEE numerik ber-anchor, APA 7th edisi, Harvard, ACM, Vancouver), pembersihan sintaks LaTeX, proteksi akronim komputasi, dan validasi segitiga integritas referensi. Kata kunci pemicu: compile references, susun daftar pustaka, buat 06_references.md, kompilasi referensi, format references, validasi referensi, check reference integrity, generate bibliography. JANGAN aktifkan untuk menulis draf naskah (gunakan ar-paper-draft), mencari sitasi kalimat (gunakan ar-paper-sentence-citation), atau penomoran braket teks naskah (gunakan ar-paper-citation-numbering)."
license: MIT
metadata:
  author: Rafy
---

# Kompilasi & Pemformatan Daftar Pustaka (Academic Reference Compiler)

## Gambaran Umum (Overview)

Skill ini menjalankan proses **kompilasi deterministik, standardisasi format, dan validasi integritas naskah daftar pustaka akhir (`paper/06_references.md`)**. Sebagai **Step 3** dalam alur penerbitan naskah akademik, skill ini membaca urutan kemunculan rujukan dari berkas pemetaan granular `paper/references.txt` (hasil Step 2), mengekstrak dan menormalisasi metadata catatan bibliografi (`.bib`, `.ris`, `.nbib`) dari folder `paper/references/`, lalu memformatnya menjadi entri daftar pustaka yang taat asas (*IEEE, APA 7th, Harvard, ACM, Vancouver*) lengkap dengan tautan HTML anchor `<a id="refN"></a>` untuk memfasilitasi penautan sitasi braket pada Step 4.

> [!NOTE]
> **Fokus Khusus Step 3**
> Skill ini hanya menyusun berkas naskah daftar pustaka `paper/06_references.md`. Skill ini **TIDAK mengubah teks draf bab atau menyisipkan nomor sitasi braket pada bab** (tugas tersebut dikerjakan pada Step 4 oleh `ar-paper-citation-numbering`) dan **TIDAK mencari literatur baru** (dikerjakan pada Step 2 oleh `ar-paper-sentence-citation`).

## Kapan Mengaktifkan Skill Ini

- Pengguna meminta mengompilasi atau membuat naskah daftar pustaka akhir `paper/06_references.md`.
- Pengguna meminta memformat ulang daftar pustaka ke gaya sitasi tertentu (IEEE numerik, APA 7th, Harvard, ACM, atau Vancouver).
- Pengguna meminta memeriksa integritas segitiga referensi (*triangular audit* antara `references.txt`, berkas pada `paper/references/`, dan `06_references.md`).
- Pengguna meminta memperbaiki format metadata penulis, kapitalisasi judul (*Title Case* vs *Sentence case*), nama jurnal miring, atau tautan aktif HTTPS DOI.
- Kata kunci pemicu: `compile references`, `susun daftar pustaka`, `buat 06_references.md`, `kompilasi referensi`, `format references`, `validasi referensi`, `check reference integrity`, `generate bibliography`.

## Kapan TIDAK Mengaktifkan Skill Ini

- Merancang struktur atau blueprint paragraf naskah paper dari nol (gunakan `ar-paper-outline` / Step 0).
- Menulis draf teks bab naskah per bagian (gunakan `ar-paper-draft` / Step 1).
- Mencari literatur ilmiah per kalimat atau menyusun pemetaan `paper/references.txt` (gunakan `ar-paper-sentence-citation` / Step 2).
- Mengganti teks draf menjadi nomor sitasi braket dan tautan markdown `[[N]](06_references.md#refN)` (gunakan `ar-paper-citation-numbering` / Step 4).
- Menulis atau menyunting ringkasan abstrak naskah `00_abstract.md` (gunakan `ar-paper-abstract` / Step 5).

## Ruang Lingkup (Scope)

- **Dalam Lingkup:** Ekstraksi urutan kemunculan unik rujukan dari `paper/references.txt`, parsing multi-format (`.bib`, `.ris`, `.nbib`), normalisasi teks (pembersihan LaTeX escape accents, proteksi akronim komputasi), pemformatan sesuai gaya sitasi (IEEE, APA 7th, Harvard, ACM, Vancouver), penyusunan berkas `paper/06_references.md` dengan anchor tag `<a id="refN"></a>`, serta validasi konsistensi integritas referensi tanpa *orphan* atau *missing files*.
- **Luar Lingkup:** Mengedit berkas draf bab (`01_introduction.md` s.d. `05_conclusion.md`), mengubah teks sitasi di dalam bab draf, mengunduh rujukan baru dari web, atau mengarang metadata fiktif.

---

## Langkah Wajib 0: Verifikasi Prasyarat Input

Sebelum memulai proses kompilasi naskah daftar pustaka, pastikan parameter berikut terpenuhi:

1. **Berkas Pemetaan Ada**: Verifikasi keberadaan dan isi berkas `paper/references.txt`.
2. **Koleksi Bibliografi Lengkap**: Pastikan setiap berkas catatan bibliografi yang dirujuk dalam `references.txt` benar-benar ada secara fisik di dalam direktori `paper/references/`.
3. **Pilihan Gaya Sitasi**: Konfirmasi gaya sitasi target (default: `ieee` numerik urut kemunculan; alternatif: `apa7`, `harvard`, `acm`, `vancouver`).
4. **Target Berkas Output**: Naskah daftar pustaka ditulis ke `paper/06_references.md`.

---

## Arsitektur Berkas Kompilasi Referensi

Hubungan antar berkas pada pipeline kompilasi adalah sebagai berikut:

```text
paper/
├── references.txt                # INPUT 1: Urutan kemunculan & pemetaan klaim -> file
├── references/                   # INPUT 2: Rekaman bibliografi primer
│   ├── 2021_Privacy–Enhancing.bib
│   ├── 2022_Techniques.ris
│   └── 2022_Black_faces.nbib
└── 06_references.md              # OUTPUT: Naskah daftar pustaka dengan anchor tag
```

Struktur entri pada `paper/06_references.md` (Contoh Gaya IEEE):
```markdown
# References

<a id="ref1"></a>
[1] J. Deng, J. Guo, N. Xue, and S. Zafeiriou, "ArcFace: Additive Angular Margin Loss for Deep Face Recognition," in *IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2019, pp. 4690–4699. doi: [10.1109/CVPR.2019.00482](https://doi.org/10.1109/CVPR.2019.00482).

<a id="ref2"></a>
[2] P. J. Phillips et al., "Face Recognition Vendor Test (FRVT) Part 3: Demographic Effects," National Institute of Standards and Technology, Tech. Rep. NISTIR 8280, 2019. doi: [10.6028/NIST.IR.8280](https://doi.org/10.6028/NIST.IR.8280).
```

---

## Protokol Eksekusi Kompilasi Rujukan

### 1. Ekstraksi Urutan & Deduplikasi Rujukan
- Baca berkas `paper/references.txt` baris demi baris.
- Ekstrak seluruh path rujukan pada baris indentasi `- paper/references/...`.
- Lakukan deduplikasi berurutan (*order-preserving deduplication*): entri rujukan hanya dicatat saat pertama kali muncul dalam draf (*Order of First Appearance*).
- Setiap entri rujukan unik diberikan indeks sequential $N = 1, 2, 3, \dots$.

### 2. Multi-Format Parsing & Normalisasi
- Buka dan parse berkas bibliografi berdasarkan ekstensinya:
  - `.bib`: Parse BibTeX entry type (`@article`, `@inproceedings`, `@book`, `@techreport`, `@misc`), tangani nested braces, dan bersihkan LaTeX escapes (`{\"a}` $\rightarrow$ ä, `\textendash` $\rightarrow$ –).
  - `.ris`: Parse tag RIS (`TY`, `AU`/`A1`, `TI`/`T1`, `JO`/`JF`, `PY`/`Y1`, `VL`, `IS`, `SP`, `EP`, `DO`).
  - `.nbib`: Parse PubMed tagged format (`PT`, `FAU`/`AU`, `TI`, `JT`/`TA`, `DP`, `VI`, `IP`, `PG`, `AID`).
- Bangun objek rujukan standar (*Canonical Reference Object*) yang memuat penulis, judul, wadah terbit (*container*), tahun, volume, issue, halaman, publisher, dan DOI.

### 3. Pemformatan Gaya Sitasi & Proteksi Akronim
- **Penulis**: Format inisial nama depan dan nama keluarga (misal: `J. Smith and A. Taylor`, atau `J. Smith et al.` jika $\ge 7$ penulis pada IEEE).
- **Judul**: Format *Title Case* untuk artikel IEEE (`"Title of Paper,"`), cetak miring untuk judul buku. Lindungi akronim komputasi baku (CNN, ViT, ResNet, GAN, LSTM, AI, RoBERTa, BERT).
- **Wadah Terbit**: Cetak miring untuk nama jurnal/prosiding (`*IEEE Transactions on Pattern Analysis and Machine Intelligence*`).
- **DOI**: Selalu sediakan tautan aktif berformat `doi: [10.xxx](https://doi.org/10.xxx)`.
- **Anchor Tag**: Sisipkan `<a id="refN"></a>` tepat satu baris sebelum nomor entri `[N]` untuk mendukung penautan tautan internal markdown dari naskah bab draf.

### 4. Validasi Integritas Segitiga (Triangular Audit)
- **Zero-Missing**: Pastikan tidak ada rujukan di `references.txt` yang tidak memiliki berkas fisik di `paper/references/`.
- **Zero-Orphan**: Laporkan jika ada berkas di `paper/references/` yang tidak pernah dirujuk pada `references.txt`.
- **Anchor-Parity**: Pastikan setiap `[N]` pada `06_references.md` memiliki tag `<a id="refN"></a>` yang tepat dan berurutan dari 1 sampai N maksimum.

---

## Panduan Do and Don't

| Do | Don't |
|:---|:---|
| Pertahankan urutan kemunculan pertama (*first appearance*) secara deterministik | Mengurutkan referensi secara acak atau mengubah urutan kemunculan draf |
| Sisipkan tag anchor HTML `<a id="refN"></a>` sebelum setiap entri `[N]` | Menghapus atau melupakan tag anchor yang diperlukan untuk Step 4 |
| Bersihkan kode escape LaTeX menjadi karakter Unicode bersih | Membiarkan teks mentah `{\"u}` atau `\textit{}` pada naskah markdown |
| Pertahankan kapitalisasi akronim teknis penting (CNN, ViT, AI, LLM) | Mengubah seluruh judul menjadi *lowercase* tanpa mengecualikan akronim |
| Format tautan DOI sebagai HTTPS aktif `https://doi.org/...` | Menulis DOI mentah tanpa tautan atau menggunakan protokol HTTP lawas |
| Lakukan validasi segitiga sebelum menyerahkan berkas output | Menyerahkan `06_references.md` yang memiliki entri hilang atau tidak konsisten |
| Gunakan pustaka standar Python tanpa dependensi pihak ketiga | Menambahkan dependensi berat seperti `bibtexparser` atau `pybtex` |

---

## Skrip Pembantu CLI (Helper Scripts)

Skill ini dilengkapi dengan modul dan skrip CLI berbasis pustaka standar Python (Python 3.10+) pada direktori `scripts/`:

1. **Kompilasi Naskah Daftar Pustaka**:
   ```bash
   # Kompilasi standar IEEE numerik ber-anchor:
   python scripts/reference_compiler.py -m paper/references.txt -d paper/references -o paper/06_references.md

   # Kompilasi dengan gaya APA 7th (urut alfabetis penulis):
   python scripts/reference_compiler.py -m paper/references.txt -d paper/references -o paper/06_references.md --style apa7

   # Kompilasi gaya Harvard, ACM, atau Vancouver:
   python scripts/reference_compiler.py -m paper/references.txt -d paper/references -o paper/06_references.md --style acm

   # Dry-run untuk memverifikasi output di terminal tanpa menimpa berkas:
   python scripts/reference_compiler.py -m paper/references.txt -d paper/references --dry-run
   ```

2. **Audit Integritas Segitiga (Triangular Integrity Audit)**:
   ```bash
   # Memeriksa konsistensi antara references.txt, direktori references/, dan 06_references.md:
   python scripts/check_reference_integrity.py -m paper/references.txt -d paper/references -o paper/06_references.md

   # Menghasilkan luaran audit dalam format JSON terstruktur untuk pipeline otomatis:
   python scripts/check_reference_integrity.py -m paper/references.txt -d paper/references -o paper/06_references.md --json
   ```

---

## Panduan Rujukan Teknis (Technical References)

Untuk protokol teknis, detail rumus pemformatan, dan spesifikasi parser, pelajari berkas-berkas rujukan di direktori `references/`:

- `references/reference_compiler_workflow.md`: Siklus hidup 6 tahap kompilasi daftar pustaka, arsitektur data *Canonical Reference Object*, dan penanganan galat.
- `references/ieee_citation_style_guide.md`: Aturan lengkap gaya IEEE (artikel jurnal, konferensi, buku, laporan teknis, preprint arXiv) dan penempatan tag anchor HTML.
- `references/apa7_extended_guide.md`: Format APA 7th edisi (1–20 penulis, 21+ penulis dengan elipsis, format organisasi, dan URL/DOI aktif).
- `references/citation_format_switcher.md`: Matriks komparatif 5 gaya sitasi utama (IEEE, APA 7, Harvard, ACM, Vancouver) dan aturan konversi antar format.
- `references/multi_format_bib_parsers.md`: Spesifikasi tata bahasa dan pemetaan field untuk format BibTeX (`.bib`), RIS (`.ris`), dan PubMed NBIB (`.nbib`).
