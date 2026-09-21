# Panduan Siklus Hidup Matriks Komitmen Bertingkat (Schema 11 Nested Commitment Ledger Guide)

Panduan ini mendokumentasikan tata kelola dan pembaruan **Matriks Keterlacakan Revisi dan Komitmen (Schema 11 R&R Traceability Matrix & Commitment Ledger)** yang diadopsi dari kerangka kerja *Kong et al. (2026)* serta arsitektur objek bertingkat (*nested-object architecture* issue #268).

---

## 1. Siklus Hidup Komitmen (3 Tahapan Utama)

Sebuah komitmen perbaikan naskah melewati 3 tahapan hidup dalam siklus riset akademik:

```
[Tahap 1: Ekstraksi] ──▶ [Tahap 2: Eksekusi Revisi] ──▶ [Tahap 3: Re-Review & Verifikasi]
  ar-paper-revision-coach        ar-paper-revision                  ar-paper-reviewer
  (Mengisi teks komitmen,       (Mengisi status pemenuhan,         (Mengaudit bukti naskah,
   tipe bukti, prioritas)        alasan jika parsial, lokasi)       memberikan vonis akseptasi)
```

1. **Tahap Ekstraksi (*Extraction Phase*)**:
   - Dijalankan oleh `ar-paper-revision-coach` dari komentar mentah reviewer.
   - Mengisi bidang: `concern_id`, `priority`, `original_comment`, `reviewer_source`, dan array objek `commitment_extracted[]` (hanya bidang ekstraksi).
2. **Tahap Eksekusi (*Execution Phase*) — PERAN UTAMA `ar-paper-revision`**:
   - Dijalankan saat patch revisi naskah disusun dan diterapkan.
   - Penulis melengkapi bidang klaim: `authors_claim`, `revision_location`, dan menyuntikkan bidang siklus hidup (*lifecycle fields*) ke dalam setiap objek komitmen: `fulfillment_status` dan `unfulfilled_rationale`.
3. **Tahap Audit & Verifikasi (*Verification Phase*)**:
   - Dijalankan oleh `ar-paper-reviewer` saat simulasi mock review putaran kedua.
   - Menilai keabsahan bukti dan mengisi: `verified` (`YES`/`PARTIAL`/`NO`), `status` (`FULLY_ADDRESSED`, dll.), dan `quality_assessment`.

---

## 2. Struktur Objek Bertingkat (*Nested-Object Shape* #268)

Sebelum amandemen #268, status pemenuhan disimpan dalam array terpisah di tingkat atas, yang sering menyebabkan ketidaksinkronan indeks (*index desynchronization*). 

Dalam arsitektur saat ini, bidang siklus hidup **bersarang langsung (*nested*) di dalam setiap objek komitmen**:

```yaml
commitment_extracted:
  - commitment_text: "Tambahkan analisis kolinearitas (VIF) pada model regresi"
    commitment_type: add_analysis
    required_evidence_type: new_table
    fulfillment_status: fulfilled
    # unfulfilled_rationale DIHILANGKAN jika fulfilled

  - commitment_text: "Kumpulkan data objektif pelacakan kerja alumni 2 tahun"
    commitment_type: add_experiment
    required_evidence_type: discussion_paragraph
    fulfillment_status: partial
    unfulfilled_rationale: "Data pelacakan alumni 2 tahun belum tersedia secara lengkap pada siklus wisuda tahun berjalan; keterbatasan ini telah didiskusikan secara mendalam pada Sub-bab 5.4 Batasan Penelitian."
```

---

## 3. Spesifikasi Bidang Siklus Hidup (*Lifecycle Fields*)

### 1. `fulfillment_status` (Wajib diisi saat revisi)
Pilihan nilai tertutup (*enum*):
- `fulfilled`: Komitmen telah dipenuhi secara menyeluruh sesuai bukti yang diminta.
- `partial`: Komitmen dipenuhi sebagian (misal: analisis dilakukan untuk 2 dari 3 variabel yang diminta).
- `not-fulfilled`: Komitmen belum/tidak dipenuhi pada putaran ini (misal: eksperimen ditunda).
- `explicitly-rejected-with-rationale`: Komitmen ditolak secara sadar dengan argumen ilmiah yang kuat atau pembatasan ruang lingkup.

### 2. `unfulfilled_rationale` (Kondisional Ketat)
- **WAJIB ADA dan TIDAK BOLEH KOSONG** jika `fulfillment_status` bernilai `partial`, `not-fulfilled`, atau `explicitly-rejected-with-rationale`.
- **WAJIB DIHILANGKAN (omitted, bukan string kosong `""`)** jika `fulfillment_status == fulfilled`.
- Tiga format rasionalisasi yang sah:
  1. *Done elsewhere pointer*: "Telah diakomodasi melalui pengujian alternatif, lihat Sub-bab 3.4."
  2. *Refusal rationale*: "Ditolak karena asumsi parametrik tidak terpenuhi pada distribusi sampel, didukung literatur Chen et al. (2023)."
  3. *Deferred acknowledgment*: "Ditunda untuk riset lanjutan dalam skala konsorsium multi-institusi."

---

## 4. Taksonomi Tipe Bukti Naskah (*Evidence Types*)

Terdapat **9 tipe bukti yang diakui** dalam Schema 11:

### Bukti Naskah Fisik (*Manuscript Evidence* — 7 Tipe)
Diverifikasi langsung pada berkas draf naskah bab di `revision_location`:
1. `new_section`: Sub-bab baru yang independen (misal: sub-bab tinjauan literatur baru atau sub-bab batasan).
2. `new_figure`: Gambar visual, diagram alir model, atau grafik performa baru.
3. `new_table`: Tabel data, matriks perbandingan pustaka, atau tabel diagnostik statistik baru.
4. `new_citation`: Penambahan sitasi literatur baru yang relevan untuk mendukung klaim.
5. `methods_paragraph`: Paragraf penjelasan tambahan di bab Metodologi (misal detail pra-pemrosesan data atau konfigurasi hyperparameter).
6. `discussion_paragraph`: Paragraf pembahasan komparatif di bab Diskusi.
7. `prose_edit`: Perubahan redaksional kalimat atau paragraf (perbaikan salah ketik, klarifikasi definisi istilah, notasi rumus, penyesuaian gaya bahasa).

### Bukti Surat Tanggapan (*Response Letter Evidence* — 1 Tipe)
8. `acknowledgment_only`: Tanggapan konseptual atau apresiasi yang cukup dinyatakan dalam surat tanggapan (Schema 8) tanpa mengubah tubuh draf paper.

### Bukti Pelarian Cadangan (*Escape Hatch* — 1 Tipe)
9. `other`: Bukti khusus di luar kategori baku (memicu tinjauan manusia saat re-review).

---

## 5. Contoh Pembaruan Matriks Schema 11

```markdown
| Field | Nilai / Rincian |
|---|---|
| `concern_id` | **REV-003** |
| `reviewer_source` | Reviewer 1 (R1) |
| `priority` | `MUST_FIX` |
| `original_comment` | "The regression model in Table 4 reports only R-squared and beta coefficients, lacking collinearity diagnostics (VIF) and residual analysis." |
| `authors_claim` | Telah ditambahkan pengujian diagnostik multikolinearitas lengkap (VIF) dan analisis residual (Cook's Distance) pada model regresi di bab Hasil Penelitian. |
| `revision_location` | `paper/04_results-and-discussion.md`, Sub-bab 4.3, Tabel 4a dan Paragraf 3. Block IDs: `B0112`, `B0113`. |
| `commitments` | `[{"commitment_text": "Tambahkan pengujian VIF dan residual Cook's Distance", "commitment_type": "add_analysis", "required_evidence_type": "new_table", "fulfillment_status": "fulfilled"}]` |
```
