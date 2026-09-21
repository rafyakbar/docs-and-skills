# Panduan Parser Multi-Format Bibliografi (Multi-Format Bib Parsers)

Dokumen ini mendefinisikan aturan pemindaian (*parsing*), pemetaan medan (*field mapping*), penanganan karakter khusus LaTeX/Unicode, serta transformasi catatan bibliografi mentah berkas `.bib` (BibTeX), `.ris` (Research Information Systems), dan `.nbib` (PubMed NLM) ke dalam *Canonical Intermediate Representation* (IR).

---

## 1. Matriks Pemetaan Medan (*Field Mapping Matrix*)

Tabel berikut menunjukkan korespondensi antara ketiga format berkas bibliografi terhadap model data kanonikal:

| Medan Kanonikal (IR) | BibTeX (`.bib`) | RIS (`.ris`) | PubMed (`.nbib`) |
|:---|:---|:---|:---|
| **Tipe Entri (*Entry Type*)** | `@article`, `@inproceedings`, `@book`, `@misc` | `TY  - JOUR`, `CONF`, `BOOK`, `ELEC` | `PT  - Journal Article`, `Review` |
| **Daftar Penulis (*Authors*)** | `author = {Last, First and ...}` | Tag jamak `AU  - Last, First` | Tag jamak `FAU - Last, First` (atau `AU`) |
| **Judul Karya (*Title*)** | `title = {...}` | `TI  - ...` atau `T1  - ...` | `TI  - ...` |
| **Wadah Publikasi (*Container*)** | `journal = {...}` atau `booktitle = {...}` | `JO  - ...` atau `T2  - ...` | `JT  - ...` (atau `TA  - ...`) |
| **Tahun Terbit (*Year*)** | `year = {2023}` | `PY  - 2023` atau `DA  - 2023/...` | `DP  - 2023 ...` |
| **Bulan Terbit (*Month*)** | `month = {Jan}` atau `month = {1}` | `DA  - YYYY/MM/...` | `DP  - YYYY Mmm ...` |
| **Volume** | `volume = {82}` | `VL  - 82` | `VI  - 82` |
| **Nomor / Edisi (*Issue*)** | `number = {2}` | `IS  - 2` | `IP  - 2` |
| **Halaman Awal & Akhir** | `pages = {1669-1748}` | `SP  - 1669` dan `EP  - 1748` | `PG  - 1669-1748` |
| **Nomor Artikel (*Art. No.*)** | `pages = {Art. no. 104404}` atau `eid` | `C7  - ...` atau `M3  - ...` | `AID - ... [pii]` |
| **Digital Object Identifier** | `doi = {10.xxxx/...}` | `DO  - 10.xxxx/...` | `LID - 10.xxxx [doi]` atau `AID` |
| **Tautan Web (*URL*)** | `url = {https://...}` | `UR  - https://...` | `UR  - https://...` |
| **Penerbit (*Publisher*)** | `publisher = {...}` | `PB  - ...` | `PL  - ...` (Place) |

---

## 2. Karakteristik & Aturan Parsing per Format

### A. Format BibTeX (`.bib`, `.bibtex`)
- **Struktur Entri**:
  Diawali dengan tanda `@` diikuti tipe entri, kurung kurawal pembuka, citation key, dan daftar pasangan `key = {value}` atau `key = "value"`.
- **Penanganan Escape Sequence LaTeX**:
  Banyak berkas `.bib` menggunakan escape sequence LaTeX untuk karakter beraksen:
  - `{\"a}` $\rightarrow$ `ä`
  - `{\"u}` $\rightarrow$ `ü`
  - `{\v{S}}` $\rightarrow$ `Š`
  - `{\c{c}}` $\rightarrow$ `ç`
  - `{\'e}` $\rightarrow$ `é`
  - `{\AA}` $\rightarrow$ `Å`
  - `--` atau `---` $\rightarrow$ `-` (tanda hubung rentang halaman)
  Parser wajib membersihkan atau menerjemahkan escape sequence ini ke karakter UTF-8 yang bersih.
- **Parsing Penulis**:
  Penulis dipisahkan oleh kata kunci `and` (case-insensitive, diapit spasi). Bentuk nama dapat berupa `Nama Belakang, Nama Depan` atau `Nama Depan Nama Belakang`.

### B. Format RIS (`.ris`)
- **Struktur Baris Berbasis Tag**:
  Setiap baris diawali oleh 2 karakter tag huruf kapital/angka, diikuti spasi, tanda strip `-`, spasi, dan nilai medan:
  `TI  - Judul Paper Lengkap`
- **Tag Jamak (*Multiple Tags*)**:
  Penulis didefinisikan dengan mengulang tag `AU  - ` pada baris-baris baru:
  ```text
  AU  - Rusia, Mayank Kumar
  AU  - Singh, Dushyant Kumar
  ```
- **Rentang Halaman**:
  RIS memisahkan halaman awal (`SP`) dan halaman akhir (`EP`). Parser menggabungkannya menjadi bentuk rentang: `{SP}-{EP}`.
- **Akhir Entri**: Ditandai oleh baris `ER  - `.

### C. Format PubMed NBIB (`.nbib`)
- **Struktur Tag NLM Medline**:
  Mirip dengan RIS tetapi tag memiliki panjang 2 hingga 4 karakter (misal: `PMID- `, `TI  - `, `FAU - `, `DP  - `).
- **Penulis Lengkap**:
  Gunakan tag `FAU - ` (Full Author Name) untuk mendapatkan nama lengkap penulis, bukan `AU  - ` yang hanya memuat inisial.
- **Tanggal Terbit**:
  Tag `DP  - ` sering memuat tahun dan bulan secara gabungan (misal: `2022 Oct` atau `2023 Jan 15`). Parser mengekstrak 4 digit pertama sebagai tahun dan kata 3 huruf setelahnya sebagai bulan.

---

## 3. Struktur Objek Kanonikal (Canonical Reference Object)

Hasil ekstraksi dari ketiga format berkas disimpan ke dalam objek data standar (Python dict / dataclass) sebelum diserahkan ke mesin pemformat:

```python
class CanonicalReference:
    ref_id: str                   # e.g. "ref1"
    entry_type: str               # "journal", "conference", "book", "online"
    authors: list[dict[str, str]] # [{"first": "Mayank Kumar", "last": "Rusia"}, ...]
    title: str                    # "A comprehensive survey..."
    container: str                # "Multimedia Tools and Applications"
    year: int                     # 2023
    month: str | None             # "Jan"
    volume: str | None            # "82"
    issue: str | None             # "2"
    pages: str | None             # "1669-1748"
    article_number: str | None    # "104404"
    doi: str | None               # "10.1007/s11042-022-13248-6"
    url: str | None               # "https://doi.org/10.1007/s11042-022-13248-6"
    publisher: str | None         # "Springer"
```
Modul pemformat (*citation formatter*) kemudian membaca objek ini dan menghasilkan string teks sesuai gaya target secara deterministik.
