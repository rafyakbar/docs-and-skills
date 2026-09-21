# Alur Kerja Kompilasi Daftar Pustaka (Reference Compiler Workflow)

Dokumen ini mendefinisikan siklus hidup kompilasi daftar pustaka akademik, algoritma pemrosesan data, struktur *Intermediate Representation* (IR), penanganan tag anchor HTML, dan prosedur audit validasi untuk menghasilkan berkas `paper/06_references.md`.

---

## 1. Gambaran Umum & Siklus Kompilasi 6 Tahap

Kompilasi daftar pustaka mentransformasikan catatan bibliografi mentah (`.bib`, `.ris`, `.nbib`) yang terpetakan dalam `paper/references.txt` menjadi naskah daftar pustaka formal `paper/06_references.md`.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SIKLUS KOMPILASI DAFTAR PUSTAKA 6 TAHAP                         │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
  [Tahap 1: Ekstraksi Sekuensial]          ▼  Membaca paper/references.txt secara linier,
                                              merekam kemunculan berkas unik pertama kali.
                                           │
  [Tahap 2: Parsing Multi-Format]          ▼  Membaca .bib, .ris, dan .nbib ke dalam
                                              Canonical Reference Object (IR).
                                           │
  [Tahap 3: Resolusi & Normalisasi]        ▼  Normalisasi nama penulis, kapitalisasi
                                              sentence case, pembersihan DOI HTTPS.
                                           │
  [Tahap 4: Pengurutan / Ordering]         ▼  IEEE/Vancouver: Order of First Appearance.
                                              APA/Harvard: Alfabetis nama belakang penulis.
                                           │
  [Tahap 5: Pembangkitan Markdown]         ▼  Format tipografi style + anchor <a id="refN"></a>
                                              menghasilkan paper/06_references.md.
                                           │
  [Tahap 6: Audit Integritas Segitiga]     ▼  Memastikan 0 orphan reference dan 0 missing files.
```

---

## 2. Rincian Eksekusi Setiap Tahap

### Tahap 1: Ekstraksi Sekuensial dari `references.txt`
1. Buka dan baca berkas pemetaan `paper/references.txt` dari baris paling atas hingga paling bawah.
2. Temukan setiap baris referensi yang diawali pola `-\s*(paper/references/[^\r\n]+)`.
3. Lakukan normalisasi string path (tangani tanda minus vs en-dash, spasi ganda, dan case-sensitivity).
4. Catat urutan kemunculan pertama (*first appearance order*):
   - Jika berkas baru pertama kali ditemukan: tambahkan ke daftar `unique_refs` dan berikan indeks $1, 2, \dots, K$.
   - Jika berkas sudah pernah muncul di paragraf sebelumnya: pertahankan indeks awal dan abaikan duplikasi.

### Tahap 2: Parsing Multi-Format ke Canonical IR
Setiap berkas pada `paper/references/` di-parse ke dalam struktur kamus terstandarisasi (*Canonical Intermediate Representation*):

```json
{
  "ref_id": "ref1",
  "source_file": "paper/references/2022_A comprehensive survey...ris",
  "entry_type": "journal",
  "authors": [
    {"first": "Mayank Kumar", "last": "Rusia"},
    {"first": "Dushyant Kumar", "last": "Singh"}
  ],
  "title": "A comprehensive survey on techniques to handle face identity threats: challenges and opportunities",
  "container_title": "Multimedia Tools and Applications",
  "year": 2023,
  "month": "Jan",
  "volume": "82",
  "issue": "2",
  "pages": "1669-1748",
  "article_number": null,
  "doi": "10.1007/s11042-022-13248-6",
  "url": "https://doi.org/10.1007/s11042-022-13248-6",
  "publisher": "Springer"
}
```

### Tahap 3: Resolusi & Normalisasi Tipografi
1. **Normalisasi Nama Penulis**:
   - BibTeX (`Last, First` atau `First Last` dipisahkan `and`).
   - RIS (`AU  - Last, First`).
   - NBIB (`FAU - Last, First` atau `AU  - Last F`).
   - Ekstraksi inisial secara presisi: `"Mayank Kumar"` $\rightarrow$ `"M. K."`.
2. **Kapitalisasi Judul Artikel**:
   - Standar IEEE/APA/Vancouver mewajibkan **Sentence case** untuk judul artikel/makalah (hanya huruf pertama judul, huruf pertama setelah titik dua, dan kata benda khusus/akronim yang berhuruf kapital).
   - Lindungi akronim domain komputasi: `AI`, `CNN`, `ViT`, `PCA`, `SVM`, `MHSA`, `ROC`, `AUC`, `GAN`, `BERT`, `LLM`, `GDPR`, dll.
3. **Format DOI**:
   - Selalu bersihkan dari tanda titik penutup (`.`).
   - Standar IEEE menggunakan prefiks: `doi: 10.xxxx/...`.
   - Standar APA 7th menggunakan tautan HTTPS: `https://doi.org/10.xxxx/...`.

### Tahap 4: Pengurutan (*Ordering Constraint*)
- **Gaya Urutan Kemunculan (IEEE, ACM, Vancouver)**:
  Urutan entri pada `06_references.md` **harus persis 100% sama dengan urutan pemetaan pertama kali** pada `paper/references.txt`.
- **Gaya Alfabetis (APA 7th, Harvard, Chicago-AD)**:
  Urutan entri diurutkan secara leksikografis berdasarkan nama belakang penulis pertama (*first author's surname*). Jika penulis sama, urutkan berdasarkan tahun terbit.

### Tahap 5: Pembangkitan Berkas Markdown `06_references.md`
Setiap entri daftar pustaka disusun dengan menyertakan tag anchor HTML agar dapat ditautkan dari teks draf pada Step 4:

```markdown
# VI. REFERENCES

<a id="ref1"></a>
[1] M. K. Rusia and D. K. Singh, "A comprehensive survey on techniques to handle face identity threats: challenges and opportunities," *Multimedia Tools and Applications*, vol. 82, no. 2, pp. 1669-1748, Jan. 2023, doi: 10.1007/s11042-022-13248-6.

<a id="ref2"></a>
[2] B. Meden et al., "Privacy-enhancing face biometrics: a comprehensive survey," *IEEE Transactions on Information Forensics and Security*, vol. 16, pp. 4147-4183, 2021, doi: 10.1109/TIFS.2021.3096024.
```

### Tahap 6: Audit Integritas Segitiga (*Triangular Zero-Orphan Check*)
Sebelum menyelesaikan kompilasi, jalankan pemeriksaan konsistensi 3 arah:
1. **Jumlah Entri Cocok**: Jumlah total nomor referensi di `06_references.md` harus sama persis dengan jumlah berkas rujukan unik di `paper/references.txt`.
2. **Ketersediaan Berkas Fisik**: Setiap jalur berkas pada `06_references.md` harus ada secara fisik pada disk di `paper/references/`.
3. **Validitas Field Minimal**: Setiap entri memiliki nama penulis, judul, tahun terbit, wadah publikasi, dan tautan pengenal (DOI atau URL).

---

## 3. Penanganan Kasus Khusus & Edge Cases

| Kasus Khusus | Permasalahan | Solusi Deterministik |
|:---|:---|:---|
| **Penulis Jamak $\ge 6$ (IEEE)** | Daftar nama penulis terlalu panjang dalam teks rujukan | Sebutkan nama penulis pertama diikuti *"et al."*: `B. Meden et al.` |
| **Penulis Jamak 21+ (APA 7th)** | Penulis melebihi 20 orang | Tuliskan 19 penulis pertama, tanda elipsis `...`, dan nama penulis paling akhir |
| **Artikel dengan Nomor Artikel (*Article Number*)** | Tidak memiliki rentang halaman tradisional | Format sebagai: `Art. no. 104404` (IEEE) atau `Article 104404` (APA) |
| **Naskah Pra-Cetak (*Preprint* arXiv)** | Tidak memiliki volume atau halaman jurnal | Format sebagai: `arXiv:2303.12345, 2023` |
| **Prosiding Seminar / Konferensi** | Menggunakan `booktitle` bukan `journal` | Awali nama prosiding dengan *"in Proc. ..."* (IEEE) atau sebutkan nama editor dan penerbit (APA) |
| **Dokumen Daring / Repositori Kode** | Tidak memiliki DOI resmi | Cantumkan URL resmi dan tanggal akses: `[Online]. Available: https://... [Accessed: DD-Mmm-YYYY]` |
