# Paket Contoh Audit Surat Tanggapan (Sample Rebuttal Audit Package)

Dokumen ini mendemonstrasikan eksekusi audit penjaminan mutu surat tanggapan reviewer (*rebuttal QA audit*) secara *end-to-end*, mencakup masukan komentar asli, draf awal penulis yang memiliki kelemahan tipikal, laporan hasil audit yang mendeteksi bendera risiko, serta draf revisi final yang disempurnakan.

---

## 1. Dokumen Masukan 1: Komentar Reviewer Asli (`comments.md`)

```markdown
# Reviewer Comments for Manuscript #TMI-2025-0842
Title: Multi-Domain Vision Transformer for Fair Facial Demographic Classification

## Reviewer 1
Comment 1 (R1-1): The sample size justification in Section 3 is inadequate. A statistical power analysis is required to demonstrate whether N=120 per ethnic group is sufficient.
Comment 2 (R1-2): The transition between the problem description and the proposed attention architecture in the Introduction feels abrupt. A clearer research gap statement is needed.
Comment 3 (R1-3): The authors should report the 95% confidence intervals for all AUROC metrics in Table 3, not just the mean values.

## Reviewer 2
Comment 4 (R2-1): The paper claims to achieve state-of-the-art fairness across all demographic groups, but the False Positive Rate disparity on dark-skinned female faces remains substantial (Table 4). This contradicts the central thesis of the paper.
Comment 5 (R2-2): Please explain why the authors chose not to evaluate on the FairFace public benchmark.
```

---

## 2. Dokumen Masukan 2: Draf Awal Surat Tanggapan Penulis (`response_draft.md`)

*(Draf ini sengaja memuat 4 kelemahan umum: R1-3 terlewat, R2-1 bernada defensif, R1-2 tidak memiliki lokator naskah, dan R2-2 disampaikan secara evasif).*

```markdown
# Response to Reviewers — Round 1

### REV-001 (R1-1)
**Reviewer Comment:** "The sample size justification in Section 3 is inadequate. A statistical power analysis is required..."
**Status:** RESOLVED
**Response:** We have performed a formal power analysis using G*Power 3.1. The results confirm that our sample size yields 0.88 power at alpha=0.05.
**Changes Made:** Added power analysis explanation in Section 3.1, p. 6, lines 112–125 (Block B0034).

### REV-002 (R1-2)
**Reviewer Comment:** "The transition between the problem description and the proposed attention architecture..."
**Status:** RESOLVED
**Response:** We have revised the text to make the research gap much clearer as requested.
**Changes Made:** Clarified in the Introduction.

### REV-004 (R2-1)
**Reviewer Comment:** "The paper claims to achieve state-of-the-art fairness across all demographic groups, but FPR disparity remains..."
**Status:** REVIEWER_DISAGREE
**Response:** The reviewer completely misunderstood our point. We never claimed zero disparity, only state-of-the-art relative to existing CNNs. Anyone in fairness AI knows that perfect parity is mathematically impossible under calibration constraints.
**Changes Made:** None.

### REV-005 (R2-2)
**Reviewer Comment:** "Please explain why the authors chose not to evaluate on the FairFace public benchmark."
**Status:** DELIBERATE_LIMITATION
**Response:** We did not use FairFace because it was beyond the scope of our research. Evaluating on FairFace is left for future work.
**Changes Made:** None.
```

*(Perhatikan: Komentar `Comment 3 (R1-3)` sama sekali tidak dijawab dalam draf ini).*

---

## 3. Hasil Eksekusi Audit: Laporan QA (`11_rebuttal_audit_report.md`)

Diterbitkan secara otomatis oleh `ars_rebuttal_auditor.py`:

```markdown
# Laporan Audit Penjaminan Mutu Surat Tanggapan Reviewer (Rebuttal QA Report)

**Skor Kesiapan:** `43.2/100`  
**Status Evaluasi:** `DITOLAK / BELUM SIAP (REJECTED UNPREPARED)`  
**Rasio Cakupan Komentar (*Coverage Ratio*):** `20.0%` (1/5 komentar terjawab tuntas)  
**Rasio Lokator Naskah (*Locator Grounding*):** `25.0%`  
**Indikator Risiko (*Risk Flags*):** `3 Tinggi (High)` · `3 Sedang (Medium)` · `0 Rendah (Low)`

### Skor 4 Dimensi Kualitas:
- **D1 Tone & Academic Diplomacy:** `70.0/100` (Bobot: 25%)
- **D2 Completeness / Zero-Orphan Coverage:** `25.0/100` (Bobot: 35%)
- **D3 Verifiability & Block Mapping:** `25.0/100` (Bobot: 20%)
- **D4 Coherence & Claim Preservation:** `60.0/100` (Bobot: 20%)
- **Skor Komposit Akhir:** `43.2/100`

> [!NOTE]
> Laporan ini bersifat penasihat independen (*advisory QA*). Sesuai aturan integritas repositori (*Iron Rule*), audit ini tidak mengubah naskah surat secara otomatis dan tidak menerbitkan status sertifikasi pengajuan formal.

---

## 1. Matriks Cakupan Butir-per-Butir (*Zero-Orphan Coverage Matrix*)

| ID | Reviewer | Komentar Asli (Cuplikan) | Status Cakupan | Locator Naskah | Risiko |
|:---|:---|:---|:---:|:---:|:---:|
| `R1-1` | Reviewer 1 | Comment 1 (R1-1): The sample size justification in Section 3 is inadequate. A statistical power a... | ✅ Lengkap | Section 3.1, p. 6, lines 112, B0034 | Aman |
| `R1-2` | Reviewer 1 | Comment 2 (R1-2): The transition between the problem description and the proposed attention archi... | ⚠️ Sebagian | *(Nihil)* | 1 isu |
| `R1-3` | Reviewer 1 | Comment 3 (R1-3): The authors should report the 95% confidence intervals for all AUROC metrics in... | ❌ Terlewat | *(Nihil)* | 1 isu |
| `R2-1` | Reviewer 2 | Comment 4 (R2-1): The paper claims to achieve state-of-the-art fairness across all demographic gr... | ⚠️ Nada Defensif | *(Nihil)* | 2 isu |
| `R2-2` | Reviewer 2 | Comment 5 (R2-2): Please explain why the authors chose not to evaluate on the FairFace public ben... | 🔍 Penolakan | *(Nihil)* | 2 isu |

---

## 2. Temuan Peringatan Kritis & Nada Bahasa (*Tone & Risk Flags*)

### #1. [MEDIUM] UNGROUNDED pada Butir `R1-2`
> [!WARNING]
> **Kutipan Teks:** *"We have revised the text to make the research gap much clearer as requested."*  
> **Analisis Masalah:** Klaim revisi tidak menyertakan locator naskah (Section, Page, Tabel, atau Block ID BNNNN).  
> **Saran Perbaikan:** Tambahkan rujukan lokasi presisi: misalnya 'See revised manuscript Section 3.2, paragraph 2 (Block B0042)'.

### #2. [HIGH] MISSING_COMMENT pada Butir `R1-3`
> [!CAUTION]
> **Kutipan Teks:** *"Comment 3 (R1-3): The authors should report the 95% confidence intervals for all AUROC metrics in..."*  
> **Analisis Masalah:** Zero-Orphan Violation: Komentar reviewer ini diabaikan dan tidak dijawab sama sekali dalam surat tanggapan.  
> **Saran Perbaikan:** Tambahkan butir tanggapan khusus yang merujuk komentar ini secara eksplisit.

### #3. [HIGH] COMBATIVE pada Butir `R2-1`
> [!CAUTION]
> **Kutipan Teks:** *"The reviewer completely misunderstood"*  
> **Analisis Masalah:** Nada defensif atau agresif dapat memicu reaksi negatif dari reviewer dan editor.  
> **Saran Perbaikan:** Ganti dengan pengakuan objektif berdiplomasi, misalnya: 'We appreciate this thoughtful critique and have clarified our theoretical boundary in Section X.'

### #4. [MEDIUM] UNGROUNDED pada Butir `R2-1`
> [!WARNING]
> **Kutipan Teks:** *"The reviewer completely misunderstood our point. We never claimed zero disparity"*  
> **Analisis Masalah:** Klaim revisi tidak menyertakan locator naskah (Section, Page, Tabel, atau Block ID BNNNN).  
> **Saran Perbaikan:** Tambahkan rujukan lokasi presisi: misalnya 'See revised manuscript Section 3.2, paragraph 2 (Block B0042)'.

### #5. [MEDIUM] UNGROUNDED pada Butir `R2-2`
> [!WARNING]
> **Kutipan Teks:** *"We did not use FairFace because it was beyond the scope of our research. Evaluat"*  
> **Analisis Masalah:** Klaim revisi tidak menyertakan locator naskah (Section, Page, Tabel, atau Block ID BNNNN).  
> **Saran Perbaikan:** Tambahkan rujukan lokasi presisi: misalnya 'See revised manuscript Section 3.2, paragraph 2 (Block B0042)'.

### #6. [HIGH] UNJUSTIFIED_REFUSAL pada Butir `R2-2`
> [!CAUTION]
> **Kutipan Teks:** *"We did not use FairFace because it was beyond the scope of our research. Evaluat"*  
> **Analisis Masalah:** Penolakan atau batasan disampaikan terlalu singkat tanpa bukti data atau kutipan literatur pendukung.  
> **Saran Perbaikan:** Jelaskan kendala empiris, batas etik IRB, atau kutip literatur metodologi yang memvalidasi keputusan tersebut.

---

## 3. Rekomendasi Tindakan Pra-Bimbingan Dosen (*Actionable Advice*)

1. **Segera Selesaikan 1 Komentar Terlewat**: Reviewer jurnal sangat peka terhadap poin yang diabaikan. Lengkapi tanggapan untuk butir yang berstatus `MISSING`.
2. **Netralkan Nada Defensif**: Kalimat yang teridentifikasi konfrontatif wajib disesuaikan dengan pola *Acknowledge $\to$ Validate $\to$ Evidence $\to$ Clarify*.
3. **Lengkapi Bukti Locator Naskah**: Pastikan setiap pernyataan perbaikan merujuk ke nomor bab, sub-bab, nomor halaman, atau nomor blok jangkar naskah (`B0042`).
4. **Konsultasikan Penolakan dengan Dosen Pembimbing**: Pastikan butir yang berstatus `REVIEWER_DISAGREE` atau `DELIBERATE_LIMITATION` telah disetujui oleh dosen sebelum diunggah.
```

---

## 4. Draf Final Surat Tanggapan yang Disempurnakan (`response_draft_v2.md`)

Setelah menerima laporan audit, penulis menyempurnakan surat tanggapan:

```markdown
# Point-by-Point Response to Reviewers — Round 1

### REV-001 (R1-1)
**Reviewer Comment:** "The sample size justification in Section 3 is inadequate. A statistical power analysis is required..."
**Status:** RESOLVED
**Response:** We thank Reviewer 1 for this rigorous recommendation. We have conducted a formal statistical power analysis using G*Power 3.1. Assuming a medium effect size (f=0.25) at alpha=0.05, our sample size of N=120 per ethnic cohort achieves a statistical power of 0.88, confirming adequate sensitivity to detect demographic disparities.
**Changes Made:** Added formal power analysis discussion in Section 3.1, p. 6, lines 112–125 (Block B0034).

### REV-002 (R1-2)
**Reviewer Comment:** "The transition between the problem description and the proposed attention architecture..."
**Status:** RESOLVED
**Response:** We appreciate this constructive suggestion. We agree that the motivation for cross-attention routing required stronger positioning. In response, we have added an explicit paragraph identifying the primary research gap: prevailing CNNs entangle demographic morphology with sensor illumination artifacts.
**Changes Made:** Added research gap paragraph in Section 1.3, p. 3, lines 45–62 (Block B0018).

### REV-003 (R1-3)
**Reviewer Comment:** "The authors should report the 95% confidence intervals for all AUROC metrics in Table 3..."
**Status:** RESOLVED
**Response:** We thank the reviewer for emphasizing metric transparency. We have re-computed all test AUROC metrics using 1,000 bootstrap resamples and now report the complete 95% confidence intervals for every ethnic group in Table 3.
**Changes Made:** Table 3 has been updated with 95% bootstrap CIs (Section 4.2, p. 11, Table 3, Block B0072).

### REV-004 (R2-1)
**Reviewer Comment:** "The paper claims to achieve state-of-the-art fairness across all demographic groups, but FPR disparity remains..."
**Status:** RESOLVED
**Response:** We are grateful to Reviewer 2 for this critical and perceptive insight. We fully agree that our original manuscript overstated the claim of uniform fairness. While our Multi-Domain Vision Transformer substantially reduces the maximum False Positive Disparity from 14.2% (ResNet baseline) to 4.8%, a residual disparity of 4.8% on darker-skinned female cohorts persists. We have toned down our claims throughout the paper, replacing 'state-of-the-art fairness' with 'improved cross-demographic parity', and added a dedicated discussion on algorithmic fairness trade-offs in Section 5.3.
**Changes Made:** Revised abstract, introduction, and added parity trade-off analysis in Section 5.3, p. 17, lines 290–315 (Blocks B0134–B0136).

### REV-005 (R2-2)
**Reviewer Comment:** "Please explain why the authors chose not to evaluate on the FairFace public benchmark."
**Status:** DELIBERATE_LIMITATION
**Response:** We thank Reviewer 2 for highlighting the FairFace benchmark. Our decision to prioritize the UTKFace and Racial Faces in-the-Wild (RFW) datasets was guided by their inclusion of high-resolution frontal imagery with verified clinical lighting variations. In contrast, FairFace exhibits lower average resolution (224x224) which limits fine-grained cross-attention visualization. However, we agree that cross-benchmark validation is crucial. We have cited FairFace in Section 2 as an important benchmark and explicitly acknowledged this evaluation boundary in Section 5.4 (*Limitations*), scheduling FairFace evaluation for upcoming multi-institution consortium trials.
**Changes Made:** Added FairFace literature citation in Section 2 and detailed scope boundary in Section 5.4, p. 18, lines 340–355 (Block B0155).
```

Jika draf `response_draft_v2.md` diaudit ulang menggunakan skrip, hasilnya akan meraih status **`PASSED_READINESS` (Skor Kesiapan 100.0/100, 100% Coverage, 0 Risk Flags, 100% Locator Grounded)** dan siap ditandatangani oleh dosen pembimbing!
