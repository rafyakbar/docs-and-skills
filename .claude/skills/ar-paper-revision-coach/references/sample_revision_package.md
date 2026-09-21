# Paket Contoh Ulasan & Dekonstruksi Revisi (Sample Revision Package)

Dokumen ini menyajikan contoh kasus nyata lengkap dekonstruksi komentar reviewer untuk naskah penelitian klasifikasi stroke iskemik dini pada citra CT non-kontras menggunakan arsitektur Cross-Attention Vision Transformer (ViT).

---

## 1. Teks Masukan Ulasan Reviewer Mentah (Raw Input Reviews)

```markdown
# Editorial Decision Letter - IEEE Transactions on Medical Imaging
Manuscript ID: TMI-2026-0842
Title: Multi-Domain Cross-Attention Vision Transformer for Early Ischemic Stroke Detection on Non-Contrast CT

Dear Authors,
The peer-review panel has evaluated your manuscript. While the clinical relevance is recognized, critical methodological and theoretical concerns were identified. The decision is: MAJOR REVISION.

Editor-in-Chief Comments:
1. The paper claims robustness across clinical settings, but testing is confined to a single center dataset. An external cohort evaluation is required before publication.
2. Ensure the ethical clearance (IRB approval) and patient data de-identification protocol are fully stated in the Methods section.

Reviewer 1 (Methodology):
1. Please add an ablation study analyzing the specific contribution of the Cross-Attention fusion module compared to standard concatenated ViT and 3D ResNet-50.
2. Report 95% confidence intervals for AUROC and Sensitivity, and provide p-values calculated using DeLong's test rather than relying solely on point estimates.
3. Fix the formatting of Equation 3 on page 5 where the loss weighting parameter lambda is not defined.

Reviewer 2 (Clinical Domain):
1. The discussion of competing diagnostic frameworks is incomplete. Please cite and compare the recent baseline by Patel et al. (2025) on NCCT stroke detection.
2. We appreciate the clear Grad-CAM saliency visualizations in Figure 4, which convincingly highlight the middle cerebral artery territory without cranial bone interference.
3. Clarify whether patients with prior stroke lesions were excluded from the evaluation set, as old infarcts could confound acute lesion detection.

Devil's Advocate:
1. The claim that the proposed model 'replaces emergency neuroradiologist triage' is a dangerous overclaim. Emergency AI serves as assistive augmentation, not replacement. The authors must reframe the narrative in Section 1 and Section 5 to acknowledge human-in-the-loop clinical realities.
```

---

## 2. Revision Roadmap (Schema 7: `08_revision_roadmap.md`)

# Revision Roadmap: Multi-Domain Cross-Attention Vision Transformer for Early Ischemic Stroke Detection on Non-Contrast CT

> Dokumen ini dihasilkan secara terstruktur melalui skill `ar-paper-revision-coach` (Fase 19–21).
> Membedah komentar ulasan reviewer menjadi matriks prioritas terarah sebelum eksekusi revisi.

## 1. Ikhtisar Editorial & Beban Kerja (Overview)
- **Keputusan Editorial**: `Major Revision`
- **Total Komentar Diurai**: 8 butir
- **Distribusi Kategori**: 3 Major | 3 Minor | 1 Editorial | 1 Positive
- **Estimasi Beban Revisi**: `Moderate` (3-5 Major, 5-10 Minor: 1-2 minggu pengerjaan)

---

## 2. Matriks Prioritas Aksi Revisi

### Prioritas 1: Must Fix (P1 — Isu Kritis Penentu Akseptasi)
| ID | Reviewer | Seksion Target | Ringkasan Masukan Reviewer | Usulan Tindakan Penulis |
|:---|:---|:---|:---|:---|
| `EIC-1` | EIC | `03_methodology` | Menuntut pengujian kohort eksternal untuk klaim ketahanan lintas center | Jalankan pengujian inferensi tambahan pada 40 kasus benchmark terbuka CQ500 tanpa melatih ulang model |
| `EIC-2` | EIC | `03_methodology` | Memastikan pernyataan komite etik (IRB) dan de-identifikasi data lengkap | Tambahkan paragraf kepatuhan etik rumah sakit mitra dan protokol anonimisasi citra di Bagian 3.1 |
| `DA-1` | DA | `01_introduction` | Klaim 'menggantikan triage neuroradiologis' merupakan overclaim berbahaya | Susun ulang narasi pengantar dan pembahasan dari dikotomi penggantian menjadi model asistif kolaboratif |

### Prioritas 2: Should Fix (P2 — Peningkatan Substansi & Metodologi)
| ID | Reviewer | Seksion Target | Ringkasan Masukan Reviewer | Usulan Tindakan Penulis |
|:---|:---|:---|:---|:---|
| `R1-1` | R1 | `04_results` | Minta eksperimen ablasi modul Cross-Attention vs ViT standar dan ResNet | Buat Tabel 4 yang menyajikan metrik komparasi ablasi modul attention |
| `R1-2` | R1 | `04_results` | Laporkan CI 95% untuk AUROC dan nilai p uji signifikansi DeLong | Perbarui Tabel 3 dengan interval CI 95% dan cantumkan nilai p DeLong test (p = 0.0021) |
| `R2-1` | R2 | `02_related-works` | Rujuk dan bandingkan baseline Patel et al. (2025) pada bab literatur | Tambahkan sitasi Patel et al. (2025) di Bab 2 dan tambahkan baris pembanding di Tabel SOTA |
| `R2-3` | R2 | `03_methodology` | Klarifikasi kriteria eksklusi lesi infark stroke lama | Tambahkan kalimat kriteria eksklusi riwayat lesi kronis di Bagian 3.1 |

### Prioritas 3: Consider (P3 — Editorial, Tipografi & Kosmetik)
| ID | Reviewer | Seksion Target | Ringkasan Masukan Reviewer | Usulan Tindakan Penulis |
|:---|:---|:---|:---|:---|
| `R1-3` | R1 | `03_methodology` | Format Persamaan 3 dan definisikan parameter penyeimbang lambda | Perbaiki notasi LaTeX pada Persamaan 3 dan tambahkan penjelasan parameter lambda di bawah rumus |

---

## 3. Catatan Apresiatif Reviewer (Positive Feedback)
| ID | Reviewer | Aspek yang Diapresiasi |
|:---|:---|:---|
| `R2-2` | R2 | Apresiasi visualisasi Grad-CAM pada Gambar 4 yang secara presisi menyorot arteri serebri media tanpa terdistorsi tulang kranium |

---

## 4. Pola Isu Silang Reviewer (Cross-Reviewer Patterns)
- **Seksion `03_methodology`**: Disorot secara independen oleh `EIC`, `R1`, dan `R2`. Memerlukan perhatian konsolidasi terpadu terkait integritas dataset, pelaporan formula, dan kriteria inklusi sampel.
- **Seksion `01_introduction` & `05_discussion`**: Devil's Advocate mengingatkan pembatasan klaim klinis yang harus konsisten dari pengantar hingga kesimpulan.

---

## 5. Rekomendasi Urutan Eksekusi Revisi (Suggested Sequence)
1. **Konsultasi Dosen Pembimbing (Fase 21)**: Validasi izin akses data uji CQ500 dan konfirmasi klausul IRB rumah sakit mitra.
2. **Eksekusi Isu Metodologis P1**: Masukkan teks IRB di Bagian 3.1 dan lakukan inferensi pada dataset eksternal CQ500.
3. **Penyempurnaan Narasi & Kerangka P2**: Perbarui Tabel 3 & Tabel 4 dengan CI 95% dan DeLong test; masukkan sitasi Patel et al. (2025).
4. **Pembersihan Editorial P3**: Definisikan parameter lambda pada Persamaan 3.
5. **Audit Rebuttal (Fase 23)**: Jalankan audit surat sanggahan sebelum penyerahan kembali.

---

## 3. Revision Tracking Table dengan Nested Commitment Ledger (`09_revision_tracking.md`)

# Revision Tracking Table: Multi-Domain Cross-Attention Vision Transformer

## 1. Tabel Pelacakan Resolusi Komentar

| ID | Reviewer | Tipe | Seksion | Ringkasan Isu | Rencana Tindakan Resolusi | Lokasi Perubahan | Status | Alasan (Jika Non-Fulfilled) |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `EIC-1` | EIC | `Major` | `03_methodology` | Uji kohort eksternal | Tambahkan uji kohort 40 scan CQ500 | Section 4.4 Table 5 | `RESOLVED` | - |
| `EIC-2` | EIC | `Major` | `03_methodology` | Protokol etik IRB & de-identifikasi | Cantumkan nomor IRB dan protokol anonimisasi | Section 3.1 para 2 | `RESOLVED` | - |
| `DA-1` | DA | `Major` | `01_introduction` | Overclaim triage mandiri | Reframe narasi menjadi model asistif | Section 1 para 4; Section 5.3 | `RESOLVED` | - |
| `R1-1` | R1 | `Minor` | `04_results` | Ablasi modul Cross-Attention | Tambahkan Tabel 4 hasil ablasi ViT vs ResNet | Section 4.3 Table 4 | `RESOLVED` | - |
| `R1-2` | R1 | `Minor` | `04_results` | Pelaporan CI 95% & DeLong test | Laporkan interval kepercayaan dan p-value | Section 4.2 Table 3 | `RESOLVED` | - |
| `R1-3` | R1 | `Editorial` | `03_methodology` | Definisi parameter lambda Persamaan 3 | Definisikan lambda di bawah formula | Section 3.3 Equation 3 | `RESOLVED` | - |
| `R2-1` | R2 | `Minor` | `02_related-works` | Sitasi baseline Patel et al. 2025 | Tambahkan perbandingan literatur Patel 2025 | Section 2.2 para 3 | `RESOLVED` | - |
| `R2-2` | R2 | `Positive` | `04_results` | Apresiasi Grad-CAM Gambar 4 | Acknowledgment di surat tanggapan | Response Letter | `RESOLVED` | - |
| `R2-3` | R2 | `Minor` | `03_methodology` | Kriteria eksklusi lesi infark lama | Jelaskan kriteria eksklusi riwayat stroke | Section 3.1 para 3 | `RESOLVED` | - |

---

## 2. Nested Commitment Ledger (YAML Blok Terstruktur)

```yaml
# Schema 11 R&R Traceability Matrix - Nested Shape (#268)
- concern_id: "EIC-1"
  commitment_extracted:
    - commitment_text: "tambahkan uji kohort eksternal pada 40 scan CQ500"
      commitment_type: add_experiment
      required_evidence_type: new_table
- concern_id: "EIC-2"
  commitment_extracted:
    - commitment_text: "cantumkan nomor persetujuan etik IRB dan protokol anonimisasi data"
      commitment_type: add_clarification
      required_evidence_type: methods_paragraph
- concern_id: "DA-1"
  commitment_extracted:
    - commitment_text: "susun ulang narasi dari penggantian dokter menjadi model augmentasi asistif"
      commitment_type: restructure
      required_evidence_type: discussion_paragraph
- concern_id: "R1-1"
  commitment_extracted:
    - commitment_text: "jalankan eksperimen ablasi modul Cross-Attention ViT"
      commitment_type: add_experiment
      required_evidence_type: new_table
- concern_id: "R1-2"
  commitment_extracted:
    - commitment_text: "laporkan interval kepercayaan 95% dan nilai p uji signifikansi DeLong"
      commitment_type: add_analysis
      required_evidence_type: new_table
- concern_id: "R1-3"
  commitment_extracted:
    - commitment_text: "definisikan parameter lambda penyeimbang loss pada Persamaan 3"
      commitment_type: other
      required_evidence_type: prose_edit
- concern_id: "R2-1"
  commitment_extracted:
    - commitment_text: "sitasi dan bandingkan metode baseline Patel et al. 2025"
      commitment_type: add_citation
      required_evidence_type: new_citation
- concern_id: "R2-2"
  commitment_extracted: []
- concern_id: "R2-3"
  commitment_extracted:
    - commitment_text: "klarifikasi kriteria eksklusi pasien dengan lesi stroke iskemik kronis"
      commitment_type: add_clarification
      required_evidence_type: methods_paragraph
```

---

## 4. Response Letter Skeleton (`10_response_letter_skeleton.md`)

```markdown
# Response to Reviewers (Skeleton)
Manuscript ID: TMI-2026-0842
Title: Multi-Domain Cross-Attention Vision Transformer for Early Ischemic Stroke Detection on Non-Contrast CT
Target Journal: IEEE Transactions on Medical Imaging

Dear Editor-in-Chief and Reviewers,
We express our gratitude to the Editor and the Reviewers for their constructive evaluation. Below are our point-by-point responses and cross-references to the revised manuscript.

## Response to Editor-in-Chief (EIC)
### Comment EIC-1: External cohort evaluation
> "The paper claims robustness across clinical settings, but testing is confined to a single center dataset. An external cohort evaluation is required before publication."

**Author Response**: We fully concur. We conducted an external validation on 40 scans from the open-source CQ500 cohort. The model demonstrated robust generalization without fine-tuning.

**Changes Made**:
- Lokasi: Section 4.4, Table 5, Page 9.
- Teks: Added Section 4.4 and Table 5 reporting cross-center generalization metrics.

### Comment EIC-2: IRB and de-identification protocol
> "Ensure the ethical clearance (IRB approval) and patient data de-identification protocol are fully stated in the Methods section."

**Author Response**: The protocol details have been added to Section 3.1.

**Changes Made**:
- Lokasi: Section 3.1, Page 4, Paragraph 2.
- Teks: Explicitly stated institutional review board approval number IRB-MED-2025-0914 and DICOM anonymization protocol compliant with HIPAA.
```
