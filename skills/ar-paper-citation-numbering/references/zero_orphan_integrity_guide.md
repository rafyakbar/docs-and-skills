# Panduan Integritas Referensi Bebas Yatim (Zero-Orphan Integrity Guide)

Dokumen ini menjelaskan protokol audit kepatuhan tanpa referensi yatim (*Zero-Orphan Protocol*), pengecualian sitasi naratif, proteksi blok kode, dan pemeriksaan integritas nomor sitasi antara teks bab draf dan naskah daftar pustaka `paper/06_references.md`.

---

## 1. Prinsip Mutlak Tanpa Yatim (The Zero-Orphan Principle)

Dalam publikasi ilmiah bereputasi internasional, ketidakcocokan antara teks naskah dan daftar pustaka merupakan salah satu penyebab utama penolakan administratif (*desk rejection*). Prinsip *Zero-Orphan* mewajibkan kepatuhan dua arah yang simetris:

```
┌──────────────────────────────────────┐          ┌──────────────────────────────────────┐
│        SITASI DALAM TEKS BAB         │          │       DAFTAR PUSTAKA LENGKAP         │
│             (paper/*.md)             │          │       (paper/06_references.md)       │
│                                      │          │                                      │
│  "Pengenalan demografis [[1]], [[2]]"│ ───────► │  <a id="ref1"></a> [1] Ref Satu...   │
│                                      │ ───────► │  <a id="ref2"></a> [2] Ref Dua...    │
│  "Model transformer [[14]]..."       │ ───────► │  <a id="ref14"></a> [14] Ref Empat...│
└──────────────────────────────────────┘          └──────────────────────────────────────┘
                   ▲                                                 │
                   │                                                 │
                   └─────────────────────────────────────────────────┘
                     Setiap entri daftar pustaka WAJIB disitir 
                     minimal satu kali di dalam bab naskah
```

### A. Arah 1: Ketiadaan Sitasi Yatim di Teks (*Zero In-Text Orphans*)
- Setiap nomor sitasi `[[N]](06_references.md#refN)` yang tercantum pada bab draf harus memiliki jangkar `<a id="refN"></a>` dan entri bibliografi `[N]` yang sah pada `06_references.md`.
- **Dilarang keras:** Mengutip nomor rujukan fiktif atau nomor yang belum didefinisikan pada daftar pustaka.

### B. Arah 2: Ketiadaan Referensi Yatim di Daftar Pustaka (*Zero Reference List Orphans*)
- Setiap entri `[N]` yang terdaftar pada `06_references.md` harus disitir minimal satu kali pada salah satu berkas bab draf (`01_introduction.md` s.d. `05_conclusion.md` atau `07_biographies.md`).
- **Dilarang keras:** Memasukkan literatur ke dalam daftar pustaka hanya sebagai pelengkap atau pemanis naskah (*phantom bibliography*) tanpa pernah merujuknya di dalam narasi.

---

## 2. Aturan Urutan Kemunculan Pertama (IEEE Monotonic Order)

Gaya IEEE mewajibkan penomoran referensi mengikuti kronologi pertama kali rujukan tersebut disebutkan di dalam teks:

1. **Kemunculan Pertama Bersifat Monotonik Naik:**
   - Referensi pertama yang muncul di bab `01_introduction.md` **harus** bernomor `[1]`.
   - Rujukan baru berikutnya **harus** bernomor `[2]`, kemudian `[3]`, `[4]`, dst.
   - Tidak boleh ada lompatan nomor pada kemunculan pertama (misal: setelah `[2]` tiba-tiba muncul rujukan baru `[5]`).
2. **Penggunaan Ulang Bebas:**
   - Setelah sebuah rujukan didefinisikan untuk pertama kali, rujukan tersebut boleh disitir ulang di bab mana pun dengan nomor aslinya.
   - Contoh: Rujukan `[11]` pertama kali muncul di `01_introduction.md`, lalu disitir kembali di `02_related-works.md` dan `03_materials-and-methods_*.md` tetap dengan nomor `[11]`.

---

## 3. Pengecualian Bebas False-Positive untuk Sitasi Naratif

Dalam penulisan akademik gaya IEEE, rujukan sering kali disebutkan secara naratif langsung setelah nama penulis:
```markdown
Menurut Vaswani et al. [[1]](06_references.md#ref1), arsitektur transformer ...
```

Pada deteksi tanda baca konvensional, tanda titik pada singkatan `et al.` dapat secara keliru dideteksi sebagai tanda baca penutup kalimat. Auditor integritas menggunakan *negative lookbehind* cerdas:
```python
RE_PUNCT_AFTER_PERIOD = re.compile(
    r"(?<!\bet al)(?<!\bi\.e)(?<!\be\.g)\.\s*\[\[\d+\]\]",
    re.IGNORECASE
)
```
Dengan mekanisme ini, singkatan sah seperti `et al.`, `i.e.`, dan `e.g.` tidak akan memicu kesalahan tanda baca palsu (*false positive*), sementara kesalahan penempatan nyata seperti `kalimat selesai. [[1]]` tetap terdeteksi 100% akurat.

---

## 4. Cakupan Audit & Penyaringan Bab Kanonikal

Auditor secara ketat menyaring berkas yang diperiksa hanya pada bab-bab naskah ilmiah resmi:
- **Bab yang Diaudit:**
  - `01_introduction.md`
  - `02_related-works.md`
  - `03_materials-and-methods_*.md`
  - `04_results-and-discussion_*.md`
  - `05_conclusion.md`
  - `07_biographies.md`
- **Berkas yang Dikecualikan dari Audit Bab:**
  - `00_abstract.md` (Abstrak naskah mandiri)
  - `06_references.md` (Daftar pustaka target tautan)
  - `07_editorial_decision.md` (Artefak luaran peer review)
  - `08_revision_roadmap.md` (Rencana aksi revisi reviewer)
  - `ref_part_*.md` (Fragmen kompilasi bibliografi)

Selain itu, seluruh blok kode berpagar (```` ``` ```` atau `~~~`) di dalam naskah dilewati (*bypassed*) agar instruksi kode atau komentar di dalamnya tidak mengganggu audit sitasi teks.

---

## 5. Eksekusi Audit Otomatis dengan Skrip

Untuk memvalidasi kepatuhan naskah secara komprehensif:

```bash
# Menjalankan audit integritas sitasi standar:
python scripts/verify_citation_integrity.py -d paper -r paper/06_references.md

# Menghasilkan luaran terstruktur JSON untuk integrasi pipeline:
python scripts/verify_citation_integrity.py -d paper -r paper/06_references.md --json
```

**Kriteria Lolos Audit (`PASS`):**
- `status == "PASS"`
- `orphan_in_text_citations` kosong (0 temuan).
- `orphan_references` kosong (0 temuan).
- `first_appearance_violations` kosong (0 pelanggaran urutan).
- `punctuation_faults` kosong (0 kesalahan penempatan tanda baca).
