# Panduan Bukti Naskah & Lokator Presisi (Evidence Grounding and Locators Guide)

Salah satu alasan paling umum mengapa surat tanggapan reviewer ditolak saat *re-review* adalah **klaim hampa tanpa bukti lokasi naskah (*ungrounded claims*)**. Ketika penulis menulis *"we have added an experiment"* atau *"we revised the text"*, reviewer dan editor dipaksa mencari sendiri di mana perubahan tersebut berada di naskah setebal 20–40 halaman. Hal ini menimbulkan kelelahan verifikasi (*reviewer fatigue*) dan menciptakan prasangka buruk bahwa perubahan tidak benar-benar dilakukan.

Panduan ini mengatur standar pencantuman bukti naskah dan lokator presisi pada surat tanggapan (Schema 8).

---

## 1. Empat Tingkatan Lokator Naskah (*Four Tiers of Locators*)

Setiap pernyataan perbaikan naskah wajib menyertakan minimal kombinasi dari tingkat lokator berikut:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Tingkat 1: Lokator Struktural (Section / Sub-section)                 │
│  - Contoh: "Section 3.2", "Section 4.1.2"                             │
├────────────────────────────────────────────────────────────────────────┤
│ Tingkat 2: Lokator Tipografis (Page / Line Number)                     │
│  - Contoh: "Page 14, lines 18–32", "pp. 18–19"                        │
├────────────────────────────────────────────────────────────────────────┤
│ Tingkat 3: Lokator Visual / Artefak (Table / Figure / Equation)        │
│  - Contoh: "Table 4b", "Figure 3", "Equation (7)"                      │
├────────────────────────────────────────────────────────────────────────┤
│ Tingkat 4: Lokator Blok Mekanis (Block ID ARS #390)                   │
│  - Contoh: "Block B0042", "Blocks B0084–B0086"                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Lokator Struktural (*Structural Locators*)
- Menunjukkan bab dan sub-bab di mana perubahan berada.
- *Format Standar:* `Section 3.2 (Model Architecture)` atau `Section 5.3 (Limitations)`.

### 2. Lokator Tipografis (*Typographical Locators*)
- Menunjukkan nomor halaman dan nomor baris pada naskah bersih atau naskah bertanda (*marked manuscript*).
- *Format Standar:* `p. 14, lines 210–225` atau `pp. 18–19`.

### 3. Lokator Visual & Tabular (*Visual / Tabular Locators*)
- Jika revisi melibatkan data eksperimen baru, jangan hanya menyebutkan teks. Sebutkan secara eksplisit tabel atau gambar yang memuat angka tersebut.
- *Format Standar:* `Table 3 (Collinearity Diagnostics)` atau `Figure 4 (Grad-CAM Saliency Maps)`.

### 4. Lokator Blok Mekanis (*Machine-Verifiable Block IDs*)
- Pembeda utama ekosistem ARS #390. Diperoleh langsung dari berkas sidecar `<output>.apply-report.json` yang diterbitkan oleh `ars_apply_revision_patch.py`.
- Memberikan bukti matematis bahwa patch diterapkan pada blok yang tepat tanpa mengubah blok lain.
- *Format Standar:* `Block B0042` atau `Blocks B0112, B0113`.

---

## 2. Format Penulisan Lokator Standar pada Surat Tanggapan

Gunakan blok ringkasan lokasi di akhir setiap butir tanggapan:

```markdown
**Changes Made:**
1. Menambahkan pengujian multikolinearitas (VIF) dan analisis outlier (Cook's Distance) untuk mengonfirmasi stabilitas model regresi.
2. Mengutip literatur standar pengujian ekonometrik (Hair et al., 2020) untuk mendukung batas ambang VIF < 5.0.

> **Location in Revised Manuscript:**
> - Section: Section 4.2 (*Statistical Diagnostics*)
> - Page/Lines: p. 17, lines 285–302
> - Table: Table 4a (*Variance Inflation Factors*)
> - Change Block IDs: `B0078`, `B0079` (verified via `04_results.rev1.md.apply-report.json`)
```

---

## 3. Menghubungkan Laporan Eksekusi Patch (`.apply-report.json`)

Ketika revisi dieksekusi menggunakan skill `ar-paper-revision`, skrip `ars_apply_revision_patch.py` menghasilkan berkas laporan sidecar berformat JSON.

### Cara Mengekstrak ID Blok untuk Surat Tanggapan:
1. Buka berkas `<output>.apply-report.json`.
2. Temukan array `ops_applied`:
   ```json
   {
     "op_index": 1,
     "op": "insert_after",
     "block_id": "B0042",
     "roadmap_item_ids": ["REV-001"],
     "new_block_ids": ["B0085", "B0086"]
   }
   ```
3. Untuk item `REV-001`, catat bahwa perubahan berada pada blok target `B0042` serta blok baru hasil insersi `B0085` dan `B0086`.
4. Masukkan daftar ID ini ke dalam berkas tanggapan: `Change Block IDs: B0042, B0085, B0086`.

Reviewer atau sistem audit otomatis dapat mencocokkan ID ini secara instan untuk membuktikan bahwa perubahan tidak fiktif.

---

## 4. Membedakan Bukti Naskah vs Bukti Surat Tanggapan

Berdasarkan taksonomi **Kong et al. (2026)** dan **Schema 11**, terdapat dua kategori komitmen:

### 1. Komitmen Bukti Naskah (*Manuscript Evidence*)
- Meliputi: `new_section`, `new_figure`, `new_table`, `new_citation`, `methods_paragraph`, `discussion_paragraph`, `prose_edit`.
- **Wajib menyertakan lokator naskah** (Section, Page, Tabel, atau Block ID). Jika lokator tidak ada, auditor akan memicu bendera `UNGROUNDED_CLAIM`.

### 2. Komitmen Bukti Surat Tanggapan (*Response Letter Evidence*)
- Meliputi: `acknowledgment_only`.
- Merupakan tanggapan atas pertanyaan konseptual reviewer, apresiasi, atau kesepakatan filosofis yang **tidak memerlukan perubahan fisik pada naskah paper**.
- Dalam kasus ini, bukti pemenuhannya adalah teks argumentatif di dalam surat tanggapan itu sendiri. Auditor **tidak** menuntut adanya lokator naskah untuk butir kategori ini.
