# Buku Panduan Ketidaksepakatan & Batasan Riset (Disagreement and Limitations Handbook)

Dalam proses penelaahan sejawat (*peer review*), penulis **tidak diwajibkan** untuk menyetujui atau menuruti 100% permintaan reviewer. Sering kali reviewer meminta eksperimen di luar ruang lingkup, mengusulkan metode yang secara teoretis tidak cocok, atau meminta data yang melanggar batasan etika (*ethical clearance / IRB*).

Menolak permintaan reviewer secara terhormat dan ilmiah adalah hak fundamental peneliti. Namun, penolakan yang tidak didukung dasar yang kuat akan langsung ditandai oleh auditor sebagai **`UNJUSTIFIED_REFUSAL`** dan dapat menyebabkan penolakan naskah.

Panduan ini mengatur tata cara menolak atau membatasi permintaan reviewer secara elegan, berintegritas, dan bersandar pada bukti ilmiah.

---

## 1. Tiga Status Resolusi Non-`RESOLVED` yang Sah (Schema 8)

Ketika penulis tidak dapat atau memilih tidak memenuhi permintaan reviewer, gunakan salah satu dari tiga status resmi berikut:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. DELIBERATE_LIMITATION (Batasan Sadar yang Diakui)                  │
│    Permintaan valid, namun tidak dapat diakomodasi saat ini karena     │
│    kendala logistik/IRB/waktu. Diakui secara terbuka di bab Limitations│
├────────────────────────────────────────────────────────────────────────┤
│ 2. REVIEWER_DISAGREE (Ketidaksepakatan Ilmiah yang Beralasan)         │
│    Permintaan reviewer bertentangan dengan konsensus literatur,        │
│    hukum metodologi, atau tujuan penelitian. Ditolak dengan argumen.   │
├────────────────────────────────────────────────────────────────────────┤
│ 3. UNRESOLVABLE (Kondisi Tidak Dapat Diselesaikan Fisik)               │
│    Data historis sudah tidak dapat diakses lagi (misal: subjek pasien  │
│    purnatugas atau data lama rusak) tanpa membatalkan kontribusi utama │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tiga Standar Pembuktian Penolakan yang Sah (*Canonical Justification*)

Setiap penolakan wajib didukung minimal oleh salah satu dari tiga standar bukti berikut:

### Standar 1: Kendala Protokol Etik, Akses Data, atau Fisik (*Empirical Constraint*)
- **Kondisi:** Reviewer meminta pengujian pada organ lain, modalitas kontras berisiko, atau pengumpulan data pasien baru.
- **Strategi:** Jelaskan bahwa protokol etik rumah sakit (IRB) yang telah disetujui hanya mengizinkan penggunaan data tertentu, dan pengumpulan data baru memerlukan persetujuan komite etik baru yang memakan waktu berbulan-bulan.
- **Contoh Kalimat:**
  > *"We agree that testing on intravenous contrast-enhanced scans would provide complementary insights. However, our Institutional Review Board approval (IRB No. 2024-MED-042) was specifically granted for non-contrast emergency triage data, and acquiring contrast scans for acute stroke patients requires separate ethical authorization and patient consent protocols that exceed the timeline of this revision. We have explicitly stated this constraint and discussed its implications in Section 5.4 (Limitations, p. 18, Block B0155)."*

### Standar 2: Konsensus Literatur Ilmiah & Metodologi (*Theoretical Justification*)
- **Kondisi:** Reviewer meminta penggunaan metrik atau arsitektur model yang sebenarnya tidak cocok untuk domain data tersebut (misal: meminta akurasi mentah pada dataset yang sangat timpang / *imbalanced*).
- **Strategi:** Tunjukkan dengan kutipan literatur otoritatif mengapa pendekatan reviewer kurang tepat dibandingkan pendekatan yang dipilih penulis.
- **Contoh Kalimat:**
  > *"While we appreciate the reviewer's suggestion to report raw Overall Accuracy, we respectfully note that in medical screening datasets with severe class imbalance (where negative cases account for 92% of the cohort), raw accuracy is known to produce overly optimistic and misleading evaluations (He & Garcia, IEEE TKDE 2009; Saito & Rehmsmeier, PLoS ONE 2015). Instead, we follow established biostatistical guidelines by prioritizing the Area Under the Precision-Recall Curve (PR-AUC), balanced sensitivity/specificity, and Cohen's Kappa. We have expanded Section 3.4 to explicitly explain this rationale for our metric selection (see p. 11, lines 180–195, Block B0062)."*

### Standar 3: Delineasi Ruang Lingkup & Pengakuan Terbuka (*Scope Delineation*)
- **Kondisi:** Reviewer meminta analisis tambahan yang mengalihkan fokus dari kontribusi utama paper (misal: meminta prediksi kelangsungan hidup 5 tahun ke depan, padahal paper berfokus pada deteksi lesi akut 3 jam).
- **Strategi:** Tegaskan batas masalah (*problem formulation*), akui bahwa ide reviewer sangat bernilai, dan cantumkan secara transparan sebagai agenda penelitian masa depan di bab *Discussion/Limitations*.
- **Contoh Kalimat:**
  > *"The reviewer raises an intriguing question regarding 5-year post-stroke survival prediction. While long-term prognostic modeling represents an important clinical frontier, the explicit objective of this manuscript is acute emergency triage within the critical 4.5-hour thrombolysis window. Attempting to integrate multi-year follow-up data would fundamentally alter the research design and triage-centric scope of this work. Nevertheless, we recognize the immense value of this direction and have added a dedicated paragraph in Section 5.5 discussing how our acute representations could be integrated into future long-term longitudinal prognostic pipelines (see Section 5.5, p. 19, Block B0168)."*

---

## 3. Apa yang Menyebabkan Bendera `UNJUSTIFIED_REFUSAL`?

Auditor `ar-paper-rebuttal-audit` memindai penolakan yang malas atau arogan (*lazy brush-offs*). Teks berikut **dilarang keras** dan akan memicu bendera risiko tinggi:

1. **Penolakan Satu Kalimat Tanpa Dasar:**
   - ❌ *"This is beyond the scope of our paper."* (Tanpa menjelaskan mengapa di luar ruang lingkup dan tanpa menambahkan pembahasan batasan di naskah).
2. **Penolakan Berbasis Preferensi Personal:**
   - ❌ *"We prefer using ResNet rather than Vision Transformer because it is easier to train."*
3. **Penolakan Tanpa Pembaruan Naskah:**
   - ❌ Mengatakan tidak setuju di surat tanggapan, namun di naskah paper sama sekali tidak ada pembahasan mengenai isu tersebut. Jika Anda tidak setuju dengan reviewer, Anda **tetap wajib** memperbarui naskah paper untuk menjelaskan mengapa batasan tersebut wajar!
