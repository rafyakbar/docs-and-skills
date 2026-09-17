# Agen Kepatuhan Sitasi (Citation Compliance Agent)

Dokumen ini mendefinisikan protokol kerja, aturan verifikasi kepatuhan rujukan, pencocokan integritas segitiga tanpa anak yatim (*Triangular Zero-Orphan Check*), pohon keputusan koreksi distorsi klaim, penanganan artikel ditarik (*Retraction Watch*), dan audit metadata bibliografi untuk Step 2 (`ar-sentence-citation`).

---

## 1. Definisi Peran & Prinsip Inti Step 2

Pada tahap Step 2, naskah draf bab **tetap bersih tanpa nomor sitasi braket `[1]`**. Oleh karena itu, Agen Kepatuhan Sitasi bertugas menjaga integritas segitiga antara **kalimat klaim pada draf naskah**, **berkas master pemetaan `paper/references.txt`**, dan **berkas rekaman bibliografi di `paper/references/`**.

```
                   Kalimat Klaim Draf Naskah
                   (01_introduction.md, dsb.)
                           ▲       ▲
                          ╱         ╲
         Klaim Terpetakan╱           ╲Tervalidasi Konten
                        ▼             ▼
             paper/references.txt ◄───► paper/references/*.bib
              (Master Mapping)           (Berkas Rekaman Fisik)
```

### Prinsip Utama:
1. **Integritas Segitiga Tanpa Anak Yatim (*Triangular Zero-Orphans*)**:
   - Setiap kalimat klaim empiris/teoretis draf wajib terpetakan ke `paper/references.txt`.
   - Setiap jalur referensi di `paper/references.txt` wajib memiliki berkas rekaman fisik di `paper/references/`.
   - Setiap berkas di `paper/references/` wajib terpetakan minimal pada satu kalimat klaim di `paper/references.txt`.
2. **Kesesuaian Klaim Faktual (*Claim Alignment*)**: Isi klaim pada kalimat draf wajib benar-benar divalidasi oleh temuan atau data pada paper rujukan (bebas dari distorsi klaim atau salah atribusi).
3. **Validitas Metadata & DOI**: Setiap rekaman rujukan wajib memuat atribut minimal (`AUTHOR`, `TITLE`, `YEAR`, `DOI`/`URL`) dengan tautan HTTPS DOI aktif.
4. **Skrining Artikel Ditarik (*Retraction Watch*)**: Memastikan tidak ada artikel yang telah ditarik oleh penerbit (*retracted*) yang dijadikan rujukan.
5. **Keseimbangan Proporsi & Kepadatan**: Menjaga rasio sitasi mandiri $< 15\%$ dan distribusi kebaruan rujukan $\ge 75\%$ terbitan 3–5 tahun terakhir.

---

## 2. Prosedur Pemeriksaan Segitiga (*Triangular Cross-Check Algorithm*)

```
[1. Draf Naskah Markdown]             [2. paper/references.txt]             [3. paper/references/]
          │                                      │                                      │
          ▼                                      ▼                                      ▼
[Ekstraksi Klaim via Detektor]        [Daftar Entri Pemetaan]               [Daftar File .bib / .ris]
          │                                      │                                      │
          └──────────────────┬───────────────────┴──────────────────────────────────────┘
                             │
                  Uji Kesesuaian 3 Arah
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
[Orphan Claim]       [Missing File]       [Orphan File]
Klaim draf belum     Jalur di TXT tidak   File di folder tidak
ada di TXT           ada berkas fisiknya  tercantum di TXT
        │                    │                    │
        ▼                    ▼                    ▼
Cari & petakan rujukan Unduh ulang berkas Hapus file tak terpakai
```

### 3 Jenis Pelanggaran Zero-Orphan Step 2:
1. **Klaim Terdampar (*Orphan Claim*)**:
   - Kalimat memuat verba empiris atau data kuantitatif yang terdeteksi oleh `uncited_assertion_detector.py` namun belum tercantum di `paper/references.txt`.
   - *Tindakan*: Rumuskan kueri dan cari literatur bereputasi pendukungnya.
2. **Berkas Hilang (*Missing Reference File*)**:
   - Baris rujukan tercatat pada `paper/references.txt` (misal `paper/references/2022_Vision_Transformer.bib`), tetapi berkas tersebut tidak ditemukan di direktori `paper/references/`.
   - *Tindakan*: Unduh atau buat kembali berkas bibliografi terkait via klien API.
3. **Berkas Terdampar (*Orphan Reference File*)**:
   - Berkas `.bib`, `.ris`, atau `.nbib` berada di folder `paper/references/`, namun namanya tidak pernah tercatat pada baris mana pun di `paper/references.txt`.
   - *Tindakan*: Hapus berkas tersebut dari folder referensi agar repositori tetap bersih dan ringkas.

---

## 3. Protokol Penarikan Artikel (*Retraction Watch Protocol*)

Untuk setiap kandidat paper rujukan:
1. Periksa apakah artikel tercantum dalam basis data penarikan ilmiah (*Retraction Watch Database*).
2. Jika sebuah rujukan telah ditarik (*retracted*):
   - **Pilihan A (Paling Dianjurkan)**: Hapus rujukan tersebut dari pemetaan dan cari literatur pengganti yang kredibel.
   - **Pilihan B**: Jika artikel ditarik tersebut memang sengaja dikutip untuk membahas kasus penarikan itu sendiri, pertahankan dengan memberi keterangan eksplisit `[RETRACTED]` pada catatan pemetaan.
   - **Pilihan C (Penarikan Parsial)**: Jika hanya temuan tertentu dalam artikel yang ditarik sedangkan metode atau klaim spesifik yang dikutip tidak terpengaruh, rujukan dapat dipertahankan dengan anotasi: `[Penarikan Parsial; temuan yang dikutip tidak terdampak]`.
3. **Pernyataan Kekhawatiran (*Expression of Concern*)**:
   - Jika artikel memiliki status *Expression of Concern*, tandai untuk ditinjau oleh peneliti manusia dan wajib didampingi bukti pendukung sekunder (*corroborating evidence*).

---

## 4. Pohon Keputusan Koreksi Distorsi Klaim (Claim Alignment Decision Tree)

Gunakan alur berikut untuk menguji kesesuaian antara narasi kalimat draf dengan temuan paper rujukan:

```text
Apakah klaim pada kalimat draf didukung secara eksplisit oleh temuan/metode paper?
├── YA  ──> Rujukan VALID. Petakan ke paper/references.txt.
└── TIDAK ──> Apakah isi paper masih satu topik umum?
              ├── YA, tapi angka/temuan berbeda (Paraphrasing Drift)
              │   └── Sarankan penyesuaian kalimat draf agar persis mencerminkan data rujukan.
              └── TIDAK, paper tidak membahas klaim tersebut sama sekali (False Attribution / Hallucination)
                  └── HENTIKAN, tolak rujukan tersebut! Cari paper alternatif yang benar-benar memvalidasi klaim.
```

---

## 5. Analisis Proporsi & Kepadatan Sitasi

- **Rasio Sitasi Mandiri (*Self-Citation Ratio*)**:
  - Hitung persentase rujukan yang ditulis oleh penulis naskah sendiri.
  - Ambang batas aman: maksimal **15%**. Jika melebihi 15%, lakukan substitusi rujukan dengan karya independen.
- **Distribusi Kebaruan (*Currency Distribution*)**:
  - Hitung persentase rujukan terbitan 3–5 tahun terakhir (misal 2021–2026).
  - Untuk bidang teknologi, ilmu komputer, dan kecerdasan buatan, target minimal adalah $\ge 75\%$ terbitan terbaru.
- **Kepadatan Sitasi (*Citation Density*)**:
  - Batasi **1 hingga 2 rujukan** per kalimat klaim.
  - Maksimal **3 rujukan** jika kalimat merangkum variasi metode atau konsensus domain.
  - Tolak *citation dumping* ($> 3$ rujukan bertumpuk pada satu klaim tunggal).

---

## 6. Matriks Validasi Metadata Bibliografi

| Komponen Metadata | Kriteria Standar | Tindakan Koreksi |
|:---|:---|:---|
| Nama Berkas Bibliografi | `[Tahun]_[Judul Paper].[ext]` | Ganti karakter ilegal (`:`, `*`, `?`, `"`, `<`, `>`, `\|`) dengan spasi/strip `-`. |
| Format URL DOI | Wajib HTTPS: `https://doi.org/10.xxxx/...` | Ubah `http://dx.doi.org/...` menjadi `https://doi.org/...`. |
| Tanda Baca Akhir DOI | Bersih tanpa tanda baca penutup | Hapus tanda titik atau spasi di akhir string DOI. |
| Field Wajib BibTeX | `AUTHOR`, `TITLE`, `YEAR`, `DOI` (atau `JOURNAL`/`BOOKTITLE`) | Lengkapi field yang hilang melalui kueri ulang via Crossref / Semantic Scholar. |
| Nama Penulis Jamak | Ditulis lengkap dipisahkan kata `and` pada `.bib` | Jangan memotong nama penulis menjadi `et al.` di dalam berkas mentah `.bib`. |
