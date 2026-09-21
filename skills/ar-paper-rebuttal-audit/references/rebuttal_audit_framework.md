# Kerangka Kerja Audit Surat Tanggapan Reviewer (Rebuttal Audit Framework)

Dokumen ini merupakan panduan normatif untuk eksekusi audit penjaminan mutu (*advisory QA audit*) terhadap draf surat tanggapan reviewer (*Point-by-Point Response to Reviewers*) pada **Fase 23 (Internal Review)** siklus riset ilmiah akademik.

---

## 1. Posisi Arsitektural & Batasan Integritas (*Integrity Boundary*)

Dalam siklus revisi paper internasional, peran audit surat tanggapan memiliki batasan yang tegas terhadap tahapan lain:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SIKLUS REVISI NASKAH                           │
├────────────────────────────────┬────────────────────────────────────────┤
│ Tahap                          │ Tanggung Jawab & Artefak               │
├────────────────────────────────┼────────────────────────────────────────┤
│ 1. ar-paper-reviewer (Fase 18) │ Evaluasi naskah; menerbitkan kritik &  │
│                                │ Editorial Decision (Schema 6 & 7)      │
├────────────────────────────────┼────────────────────────────────────────┤
│ 2. ar-paper-revision-coach     │ Membedah komentar mentah; menyusun     │
│    (Fase 19–21)                │ Roadmap & Skeleton (sebelum ada draf)  │
├────────────────────────────────┼────────────────────────────────────────┤
│ 3. ar-paper-revision (Fase 22) │ Eksekusi perbaikan draf (diff/patch) & │
│                                │ menyusun draf respons (Schema 8 & 11)  │
├────────────────────────────────┼────────────────────────────────────────┤
│ 4. ar-paper-rebuttal-audit     │ Audit mutu draf surat respons (Fase 23)│
│    (Fase 23 — SKILL INI)       │ Cakupan komentar, nada, & bukti locator│
├────────────────────────────────┼────────────────────────────────────────┤
│ 5. ar-paper-reviewer           │ Re-Review Stage 3'; verifikasi apakah  │
│    (Re-Review Stage 3')        │ naskah revisi benar-benar berubah      │
└────────────────────────────────┴────────────────────────────────────────┘
```

### Aturan Emas Integritas (*Iron Rule: No False Certification*)
1. **Advisory QA Standalone**: `ar-paper-rebuttal-audit` berjalan di luar *pipeline* utama dan berfokus mengevaluasi **kualitas teks surat tanggapan itu sendiri**, bukan naskah paper.
2. **Larangan Sertifikasi Palsu**: Skill ini **DILARANG KERAS** menerbitkan *Material Passport*, memperbarui Matriks Schema 11 secara sepihak, atau menandai paket pengajuan sebagai `ready_to_submit`.
3. **Larangan Penulisan Ulang Otomatis**: Skill ini bertindak sebagai auditor independen. Skill ini memberikan diagnosis, bendera risiko (*risk flags*), dan saran perbaikan (*actionable advice*), namun keputusan penulisan naskah tetap berada di tangan peneliti dan dosen pembimbing.

---

## 2. Gerbang Masukan Ganda (*Dual-Document Input Gate*)

Audit surat tanggapan **hanya dapat diaktifkan jika pengguna menyediakan KEDUA dokumen berikut**:
1. **Komentar Reviewer / Surat Keputusan Editor**: Teks lengkap masukan dari seluruh reviewer (Reviewer 1, 2, 3, Editor, atau Devil's Advocate).
2. **Draf Surat Tanggapan Penulis (*Existing Rebuttal Draft*)**: Berkas draf respons yang telah disusun oleh penulis untuk dievaluasi.

> **PENGALIHAN ALUR (*ROUTING*):**
> Jika pengguna hanya memiliki komentar reviewer tetapi **belum memiliki draf surat tanggapan**, arahkan ke **`ar-paper-revision-coach`** untuk menyusun rencana aksi dan kerangka respons. Jangan menebak draf yang belum ada!

---

## 3. Empat Dimensi Penilaian Kualitas (*Four Audit Dimensions*)

```
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 1: Audit Cakupan Komentar (Zero-Orphan Coverage)                |
|  - Memverifikasi 100% komentar terjawab (ADDRESSED / MISSING)           |
|  - Mendeteksi pertanyaan majemuk (compound asks) yang terlewat          |
+─────────────────────────────────────────────────────────────────────────+
                                    │
                                    ▼
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 2: Audit Nada & Etika Diplomasi (Tone & Academic Posture)       |
|  - Mendeteksi nada defensif, bermusuhan, atau meremehkan reviewer       |
|  - Menyaring sanjungan palsu berlebihan (inauthentic sycophancy)        |
+─────────────────────────────────────────────────────────────────────────+
                                    │
                                    ▼
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 3: Audit Bukti Naskah & Lokator Presisi (Evidence Grounding)    |
|  - Memeriksa keabsahan rujukan (Section, Page, Tabel, Block ID BNNNN)   |
|  - Mencegah klaim kosong tanpa bukti perubahan nyata                    |
+─────────────────────────────────────────────────────────────────────────+
                                    │
                                    ▼
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 4: Audit Ketidaksepakatan & Batasan (Justified Disagreements)   |
|  - Menguji dasar ilmiah penolakan (DELIBERATE_LIMITATION / DISAGREE)    |
|  - Memastikan ada argumen literatur, kendala etik IRB, atau data riil  |
+─────────────────────────────────────────────────────────────────────────+
```

### Dimensi 1: Audit Cakupan Komentar (*Zero-Orphan Coverage*)
- **Tujuan**: Memastikan tidak ada satu pun komentar atau sub-pertanyaan reviewer yang "hilang" atau diabaikan secara sengaja.
- **Kategori Status**:
  - `ADDRESSED`: Komentar dijawab tuntas dengan penjelasan memadai.
  - `PARTIALLY_ADDRESSED`: Komentar dijawab sebagian (misal: reviewer meminta A dan B, namun penulis hanya menjawab A).
  - `MISSING`: Komentar tidak dijawab sama sekali (pelanggaran *Zero-Orphan*).
- **Rasio Cakupan**:
  $$\text{Coverage Ratio} = \frac{\text{Jumlah Komentar ADDRESSED}}{\text{Total Komentar Teridentifikasi}}$$
  Target kelulusan: **100%**.

### Dimensi 2: Audit Nada & Etika Diplomasi (*Tone & Academic Posture*)
- **Tujuan**: Menjaga objektivitas, kerendahan hati ilmiah (*scientific humility*), dan mencegah gesekan emosional dengan reviewer.
- **Deteksi Pola Bahasa Negatif**:
  1. *Defensif / Agresif*: "Reviewer salah paham", "Kritik ini tidak masuk akal".
  2. *Meremehkan / Menggurui*: "Sebagaimana telah diketahui semua pakar", "Sangat jelas bahwa...".
  3. *Ambiguitas / Menghindar*: "Sudah kami perbaiki" (tanpa rincian apa yang diubah).
  4. *Pujian Berlebihan*: "Kami sangat takjub dengan kebijaksanaan reviewer yang agung".

### Dimensi 3: Audit Bukti Naskah & Lokator Presisi (*Evidence Grounding*)
- **Tujuan**: Memverifikasi bahwa setiap klaim perubahan pada surat tanggapan memiliki jangkar fisik yang dapat diverifikasi pada draf naskah.
- **Kategori Lokator yang Sah**:
  - Lokator Bab/Sub-bab: `Section 3.2`, `Sub-section 4.1`.
  - Lokator Halaman/Baris: `Page 14, lines 12–25`, `pp. 18–19`.
  - Lokator Tabel/Gambar: `Table 4a`, `Figure 3`.
  - **Lokator ID Blok Mekanis**: `<!--block:BNNNN-->` (misal `B0042`, `B0043` dari laporan `apply-report.json`).
- Respon yang menyatakan *"we have revised the text"* tanpa lokator akan ditandai dengan bendera risiko `UNGROUNDED_CLAIM`.

### Dimensi 4: Audit Ketidaksepakatan & Batasan Riset (*Justified Disagreements*)
- **Tujuan**: Memastikan bahwa penolakan terhadap usulan reviewer dilakukan secara ilmiah dan beretika tinggi.
- Tiga dasar penolakan yang sah:
  1. *Kendala Empiris & Etik*: Terkendala protokol persetujuan etik rumah sakit (IRB) atau keterbatasan fisik sensor scanner.
  2. *Konsensus Teoretis*: Bertentangan dengan hukum fisika/metodologi mapan, didukung kutipan literatur otoritatif.
  3. *Batasan Ruang Lingkup*: Masalah telah diakui secara transparan pada sub-bab *Limitations*.
- Penolakan tanpa alasan konkret ditandai sebagai `UNJUSTIFIED_REFUSAL` (risiko tinggi).

---

## 4. Matriks Vonis Kesiapan Pengajuan (*Readiness Verdicts*)

| Vonis | Syarat Kelayakan | Rekomendasi Tindakan |
|---|---|---|
| **`PASSED_READINESS`** (Siap Submit) | Coverage = 100%, 0 bendera High Risk, Locator Grounding $\ge 80\%$. | Surat tanggapan matang, santun, dan presisi. Siap diserahkan ke dosen pembimbing untuk *sign-off*. |
| **`ADVISORY_POLISHING`** (Perbaikan Minor) | Coverage = 100%, 0 bendera High Risk, beberapa kelemahan locator atau nada minor. | Perbaiki kutipan nomor halaman/baris dan haluskan kalimat sebelum diserahkan ke dosen. |
| **`ACTION_REQUIRED`** (Perlu Revisi Kritis) | Terdapat komentar `MISSING` atau terdeteksi bendera High Risk (defensif/penolakan tanpa dasar). | **Dilarang disubmit!** Lengkapi butir yang terlewat dan ubah kalimat konfrontatif menjadi diplomatis. |
