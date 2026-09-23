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

## 3. Empat Dimensi Penilaian Kualitas & Formula Skor Komposit

```
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 1 (D1): Nada & Etika Diplomasi (Tone & Academic Diplomacy)      |
|  - Bobot: 25%                                                           |
|  - Mendeteksi nada defensif, bermusuhan, atau meremehkan reviewer       |
|  - Menyaring sanjungan palsu berlebihan (inauthentic sycophancy)        |
+─────────────────────────────────────────────────────────────────────────+
                                    │
                                    ▼
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 2 (D2): Kelengkapan Komentar (Completeness / Zero-Orphan)       |
|  - Bobot: 35%                                                           |
|  - Memverifikasi 100% komentar terjawab (ADDRESSED / MISSING)           |
|  - Mendeteksi butir terlupakan atau sub-pertanyaan yang diabaikan       |
+─────────────────────────────────────────────────────────────────────────+
                                    │
                                    ▼
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 3 (D3): Keterverifikasian & Pemetaan Blok (Verifiability)       |
|  - Bobot: 20%                                                           |
|  - Memeriksa keabsahan rujukan (Section, Page, Tabel, Block ID BNNNN)   |
|  - Ambang batas keterpenuhan lokator naskah >= 80%                      |
+─────────────────────────────────────────────────────────────────────────+
                                    │
                                    ▼
+─────────────────────────────────────────────────────────────────────────+
| DIMENSI 4 (D4): Koherensi & Preservasi Klaim (Claim Preservation)       |
|  - Bobot: 20%                                                           |
|  - Menguji dasar ilmiah penolakan (DELIBERATE_LIMITATION / DISAGREE)    |
|  - Memastikan ada argumen literatur, kendala etik IRB, atau data riil  |
+─────────────────────────────────────────────────────────────────────────+
```

### Formula Skor Komposit Tertimbang (0–100):
$$\text{Composite Score} = (S_{D1} \times 0.25) + (S_{D2} \times 0.35) + (S_{D3} \times 0.20) + (S_{D4} \times 0.20)$$

---

### Dimensi 1: Nada & Etika Diplomasi (*D1 Tone & Academic Diplomacy*) — Bobot 25%
- **Tujuan**: Menjaga objektivitas, kerendahan hati ilmiah (*scientific humility*), dan mencegah gesekan emosional dengan reviewer.
- **Deteksi Pola Bahasa Negatif**:
  1. *Defensif / Agresif (`combative`)*: "Reviewer salah paham", "Kritik ini keliru". Butir dengan flag ini diklasifikasikan sebagai `UNRESOLVED_TONE_CONFLICT`.
  2. *Meremehkan / Menggurui (`condescending`)*: "Sebagaimana telah diketahui semua pakar", "Sangat jelas bahwa...".
  3. *Ambiguitas / Menghindar (`evasive`)*: "Sudah kami perbaiki" (tanpa rincian apa yang diubah).
  4. *Pujian Berlebihan (`sycophantic`)*: "Kami sangat takjub dengan kebijaksanaan reviewer yang agung".

### Dimensi 2: Kelengkapan Komentar (*D2 Completeness / Zero-Orphan Coverage*) — Bobot 35%
- **Tujuan**: Memastikan tidak ada satu pun komentar atau sub-pertanyaan reviewer yang "hilang" atau diabaikan secara sengaja (*Zero-Orphan Rule*).
- **Kategori Status**:
  - `ADDRESSED`: Komentar dijawab tuntas dengan penjelasan memadai dan tindakan konkret.
  - `PARTIALLY_ADDRESSED`: Komentar dijawab sebagian (misal: reviewer meminta A dan B, namun penulis hanya menjawab A; atau jawaban terlalu singkat `< 20` kata).
  - `UNRESOLVED_TONE_CONFLICT`: Komentar dijawab namun menggunakan nada agresif/defensif yang belum dinetralkan.
  - `UNRESOLVED_DISAGREEMENT`: Komentar ditolak tanpa dasar justifikasi ilmiah yang sah.
  - `MISSING`: Komentar tidak dijawab sama sekali (pelanggaran fatal *Zero-Orphan*).
- **Rasio Cakupan**:
  $$\text{Coverage Ratio} = \frac{\text{Jumlah Komentar ADDRESSED}}{\text{Total Komentar Teridentifikasi}}$$
  Target kelulusan: **100%** (*0 Missing Items*).

### Dimensi 3: Keterverifikasian & Pemetaan Blok (*D3 Verifiability & Block Mapping*) — Bobot 20%
- **Tujuan**: Memverifikasi bahwa setiap klaim perubahan pada surat tanggapan memiliki jangkar fisik yang dapat diverifikasi pada draf naskah.
- **Kategori Lokator yang Sah**:
  - Lokator Bab/Sub-bab: `Section 3.2`, `Sub-section 4.1`.
  - Lokator Halaman/Baris: `Page 14, lines 12–25`, `pp. 18–19`.
  - Lokator Tabel/Gambar: `Table 4a`, `Figure 3`.
  - **Lokator ID Blok Mekanis**: `<!--block:BNNNN-->` (misal `B0042`, `B0043` dari laporan sidecar `apply-report.json`).
- Respon yang menyatakan *"we have revised the text"* tanpa lokator akan ditandai dengan bendera risiko `UNGROUNDED` (kecuali butir yang sifatnya *acknowledgment only*). Target ambang minimal: **$\ge 80\%$**.

### Dimensi 4: Koherensi & Preservasi Klaim (*D4 Coherence & Claim Preservation*) — Bobot 20%
- **Tujuan**: Memastikan bahwa penolakan atau penetapan batasan riset (*DELIBERATE_LIMITATION* / *REVIEWER_DISAGREE*) dilakukan secara ilmiah, transparan, dan tidak merusak integritas klaim naskah.
- Tiga dasar penolakan yang sah:
  1. *Kendala Empiris & Etik*: Terkendala protokol persetujuan etik rumah sakit (IRB) atau batas akuisisi sensor scanner.
  2. *Konsensus Teoretis*: Bertentangan dengan hukum metodologi mapan, didukung kutipan literatur otoritatif.
  3. *Batasan Ruang Lingkup*: Masalah diakui secara transparan pada sub-bab *Limitations* di naskah revisi.
- Penolakan tanpa alasan konkret (`len < 30` kata tanpa bukti/sitasi) ditandai sebagai `UNJUSTIFIED_REFUSAL` (risiko tinggi).

---

## 4. Matriks Vonis Kesiapan Pengajuan (*4-Tier Readiness Verdicts*)

| Vonis | Syarat Kelayakan | Rekomendasi Tindakan |
|---|---|---|
| **`PASSED_READINESS`** (Siap Submit) | Skor $\ge 80$, 0 bendera High Risk, Coverage = 100%, Locator Grounding $\ge 80\%$. | Surat tanggapan matang, santun, dan presisi. Siap diserahkan ke dosen pembimbing untuk *sign-off* dan diajukan ke portal jurnal. |
| **`CONDITIONAL_REVISION`** (Revisi Kondisional) | Skor 65–79, 0 bendera High Risk, Coverage = 100%. | Lengkapi kutipan nomor halaman/baris/blok naskah dan poles gaya bahasa minor sebelum diserahkan ke pembimbing. |
| **`REVISE_AND_RESUBMIT`** (Revisi Ulang Total) | Skor 50–64, atau terdapat butir `MISSING`, atau penolakan tanpa dasar (`UNJUSTIFIED_REFUSAL`). | **Dilarang disubmit!** Tuntaskan butir yang terlewat dan perkuat justifikasi ilmiah untuk setiap penolakan. |
| **`REJECTED_UNPREPARED`** (Ditolak / Belum Siap) | Skor $< 50$, atau banyak bendera nada agresif/defensif (`combative`). | **Draf belum siap secara akademis.** Lakukan penulisan ulang komprehensif dengan bimbingan dosen. |

