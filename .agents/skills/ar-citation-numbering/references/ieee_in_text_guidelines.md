# Panduan Sitasi Teks Gaya IEEE (IEEE In-Text Citation Guidelines)

Dokumen ini memuat standar penulisan dan penempatan sitasi dalam teks (*in-text citations*) mengacu pada pedoman baku **IEEE Citation Guidelines** yang diadaptasi untuk naskah riset modern berbasis Markdown interaktif.

---

## 1. Aturan Dasar Gaya IEEE (Rules at a Glance)

1. **Format Penomoran:** Menggunakan kurung siku berangka arabik: `[1]`, `[2]`, `[3]`. Pada format Markdown interaktif, dikodekan sebagai `[[N]](06_references.md#refN)`.
2. **Urutan Kronologis Kemunculan (*Order of First Appearance*):** Rujukan yang pertama kali disitir dalam naskah bab mendapatkan nomor terkecil `[1]`, rujukan kedua mendapatkan `[2]`, dan seterusnya.
3. **Penggunaan Ulang Nomor (*Number Reuse*):** Nomor yang sama wajib dipakai ulang setiap kali sumber yang sama disitir di bagian bab mana pun. Jangan pernah membuat nomor ganda untuk sumber yang sama.
4. **Penempatan Tanda Baca (*Punctuation Placement*):** Nomor sitasi diletakkan **SEBELUM** tanda baca kalimat (titik `.`, koma `,`, titik koma `;`, atau pembatas sel tabel `|`), bukan sesudahnya.

---

## 2. Tipologi Sitasi Dalam Teks

### A. Sitasi Parentetikal / Ujung Kalimat (Parenthetical Citations)
Sitasi diletakkan di akhir klaim atau kalimat faktual, menempel tepat sebelum tanda baca penutup:

- ✅ **Format Benar:**
  ```markdown
  Pengenalan demografis wajah memegang peranan penting dalam forensik digital [[1]](06_references.md#ref1).
  ```
- ❌ **Format Salah (Setelah Titik):**
  ```markdown
  Pengenalan demografis wajah memegang peranan penting dalam forensik digital. [[1]](06_references.md#ref1)
  ```
- ❌ **Format Salah (Tanpa Spasi Pemisah):**
  ```markdown
  Pengenalan demografis wajah memegang peranan penting dalam forensik digital[[1]](06_references.md#ref1).
  ```

---

### B. Multi-Sitasi Terpisah (Multiple In-Text Citations)
Bila satu kalimat didukung oleh beberapa sumber referensi sekaligus:
- Setiap rujukan wajib memiliki kurung siku mandiri dan tautan URL jangkar independen.
- Dipisahkan dengan tanda koma dan satu spasi: `, `.
- Nomor diurutkan secara menaik (*ascending order*).

- ✅ **Format Benar (Markdown Interaktif):**
  ```markdown
  Sejumlah studi melaporkan adanya disparitas performa pada kelompok tertentu [[3]](06_references.md#ref3), [[4]](06_references.md#ref4).
  ```
  ```markdown
  Berbagai penelitian mengeksplorasi ekstraksi ciri demografis berbasis CNN [[11]](06_references.md#ref11), [[12]](06_references.md#ref12), [[13]](06_references.md#ref13).
  ```
- ❌ **Format Salah (Kurung Gabungan):**
  ```markdown
  ... mengeksplorasi ekstraksi ciri demografis berbasis CNN [11, 12, 13].
  ```
- ⚠️ **Catatan Rentang Angka (*Range Compression*):**
  Pada teks cetak polos, $\ge 3$ nomor berurutan sering diringkas menjadi `[11]–[13]`. Namun, pada naskah Markdown interaktif daring, bentuk terpisah `[[11]], [[12]], [[13]]` dipertahankan agar pembaca dapat mengeklik tautan ke rujukan `[12]` secara langsung.

---

### C. Sitasi Naratif (Narrative Citations)
Ketika nama peneliti disebut secara eksplisit sebagai subjek kalimat, nomor sitasi diletakkan langsung setelah nama peneliti:

- ✅ **Format Benar:**
  ```markdown
  Menurut Meden et al. [[2]](06_references.md#ref2), privasi biometrik wajah memerlukan pengamanan representasi fitur.
  ```
  ```markdown
  Kalkatawi dan Saeed [[18]](06_references.md#ref18) mendemonstrasikan efektivitas arsitektur transformer dalam klasifikasi etnisitas.
  ```
- ❌ **Format Salah:**
  ```markdown
  Menurut Meden et al., privasi biometrik wajah memerlukan pengamanan representasi fitur [[2]](06_references.md#ref2).
  ```

---

### D. Sitasi di Dalam Tabel & Judul Kolom
Sitasi pada tabel komparasi atau tinjauan literatur disematkan di dalam sel sebelum garis pembatas `|`:

```markdown
| Model | Accuracy | Precision | Recall | F1-Score |
|---|:---:|:---:|:---:|:---:|
| MD-ViT [[20]](06_references.md#ref20) | 89.07% | 89.12% | 89.07% | 89.01% |
| Dual-ViT [[19]](06_references.md#ref19) | 92.41% | 92.48% | 92.41% | 92.38% |
| **Ours** | **93.70%** | **93.72%** | **93.70%** | **93.69%** |
```

---

## 3. Matriks Komparasi Tanda Baca per Gaya Sitasi

| Fitur | IEEE Numeric | APA 7th Edition | Chicago 17th | Vancouver |
|---|---|---|---|---|
| **Pemisah Antar-Rujukan** | Koma dan spasi: `[[1]], [[2]]` | Titik koma: `(Smith, 2023; Tan, 2024)` | Koma/spasi: `(Smith 2023, Tan 2024)` | Koma: `¹˒²` |
| **Posisi terhadap Titik** | Sebelum titik: `fakta [1].` | Sebelum titik: `fakta (Smith, 2024).` | Sebelum titik: `fakta (Smith 2024).` | Setelah titik: `fakta.¹` |
| **Posisi terhadap Koma** | Sebelum koma: `metode [1], dan` | Sebelum koma: `metode (Smith, 2024), dan` | Sebelum koma: `metode (Smith 2024), dan` | Setelah koma: `metode,¹ dan` |
| **Panggilan Naratif** | `Smith [[1]] menyatakan` | `Smith (2024) menyatakan` | `Smith (2024) menyatakan` | `Smith¹ menyatakan` |
