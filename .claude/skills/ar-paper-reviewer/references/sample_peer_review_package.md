# Contoh Paket Ulasan Peer Review Lengkap: Simulasi Klasifikasi Stroke

Berkas ini memuat contoh nyata laporan ulasan dari kelima penilai independen beserta hasil sintesis editorial resmi (`07_editorial_decision.md`) dan matriks rencana aksi terprioritas (`08_revision_roadmap.md`).

---

## 1. Laporan Ulasan Panel Reviewer (Input Simulasi)

### Peer Review Report — Editor-in-Chief (EIC)
- **Reviewer Role**: Editor-in-Chief (EIC)
- **Recommendation**: Minor Revision
- **Confidence Score**: 5
- **Summary Assessment**: Naskah ini mengusulkan arsitektur Vision Transformer multimodal untuk klasifikasi stroke iskemik dini pada CT-scan darurat IGD. Topik riset sangat relevan dengan scope jurnal transaksi pencitraan medis. Kontribusi naskah jelas, namun diskusi mengenai keterbatasan variabilitas vendor scanner perlu diperdalam.
- **Strengths**:
  - **S1: Relevansi Scope Jurnal**: Topik klasifikasi stroke darurat sangat sesuai dengan pembaca IEEE TMI.
    - Evidence Anchor: `[section: 01_introduction]`
- **Weaknesses**:
  - **W1: Keterbatasan Diskusi Generalisasi Vendor Scanner**: Penulis belum secara memadai mendiskusikan performa model jika diuji pada citra dari scanner vendor yang berbeda.
    - Evidence Anchor: `[section: 05_conclusion]`
    - Severity: MINOR

---

### Peer Review Report — Reviewer 1 (Methodology)
- **Reviewer Role**: Peer Reviewer 1 (Methodology)
- **Recommendation**: Major Revision
- **Confidence Score**: 5
- **Summary Assessment**: Metodologi eksperimen komputasi dirancang dengan baik, namun terdapat ambiguitas kritis mengenai protokol partisi dataset pada validasi silang 5-fold yang berpotensi memicu kebocoran data (*data leakage*).
- **Strengths**:
  - **S1: Pelaporan Metrik Komprehensif**: Penulis menyertakan interval kepercayaan 95% dan uji DeLong p-value pada seluruh tabel utama.
    - Evidence Anchor: `[table: 3]`
- **Weaknesses**:
  - **W1: Ambiguitas Protokol Patient-Level Data Split**: Pada bab metode tidak disebutkan secara eksplisit apakah pemisahan 5-fold cross-validation dilakukan pada tingkat pasien (*patient-level*) atau tingkat irisan citra acak (*random slice*). Hal ini merupakan celah validitas kritis.
    - Evidence Anchor: `[section: 03_materials-and-methods_02_experimental-setup]`
    - Severity: CRITICAL
  - **W2: Ketiadaan Uji Koreksi Bonferroni**: Pengujian ablasi terhadap 8 variasi modul tidak menyertakan koreksi uji berganda.
    - Evidence Anchor: `[section: 04_results-and-discussion_03_ablation-study]`
    - Severity: MINOR

---

### Peer Review Report — Reviewer 2 (Domain Expert)
- **Reviewer Role**: Peer Reviewer 2 (Domain Expert)
- **Recommendation**: Minor Revision
- **Confidence Score**: 4
- **Summary Assessment**: Evaluasi domain radiologi menunjukkan akurasi anatomi yang baik pada heatmaps Grad-CAM. Namun, penulis mengabaikan beberapa literatur benchmark stroke internasional 2024–2025.
- **Strengths**:
  - **S1: Akurasi Interpretasi Klinis**: Peta atensi model terbukti fokus pada area hipodensitas arteri serebri media tanpa terdistorsi artefak kranium.
    - Evidence Anchor: `[figure: 4]`
- **Weaknesses**:
  - **W1: Pengabaian Benchmark SOTA ISLES 2024**: Penulis membandingkan model dengan baseline 2021 tetapi mengabaikan arsitektur Swin UNETR terbaru pada benchmark ISLES.
    - Evidence Anchor: `[section: 02_related-works]`
    - Severity: MAJOR

---

### Peer Review Report — Reviewer 3 (Cross-Perspective)
- **Reviewer Role**: Peer Reviewer 3 (Cross-Disciplinary Perspective)
- **Recommendation**: Minor Revision
- **Confidence Score**: 3
- **Summary Assessment**: Naskah menyajikan potensi dampak klinis yang nyata bagi penanganan IGD rumah sakit, namun estimasi waktu komputasi inferensi belum diuji pada perangkat edge lokal.
- **Strengths**:
  - **S1: Dampak Nyata bagi Jendela Emas IGD**: Pengurangan waktu deteksi hingga sub-detik memiliki implikasi positif bagi terapi trombolisis.
    - Evidence Anchor: `[section: 05_conclusion]`
- **Weaknesses**:
  - **W1: Ketiadaan Analisis Biaya Komputasi Inferensi**: Belum ada laporan penggunaan memori GPU dan latensi inferensi per pasien pada perangkat standar IGD.
    - Evidence Anchor: `[section: 04_results-and-discussion]`
    - Severity: MINOR

---

### Peer Review Report — Devil's Advocate (Adversarial)
- **Reviewer Role**: Devil's Advocate (Adversarial Evaluator)
- **Recommendation**: Major Revision
- **Confidence Score**: 5
- **Strongest Counter-Argument**: Peningkatan sensitivitas sebesar 11.8% yang diklaim penulis sangat mungkin didorong oleh pra-pemrosesan normalisasi kontras citra (*windowing Hounsfield Unit*) yang secara kebetulan menguntungkan lesi hiperdens, bukan karena modul cross-attention. Penulis belum menguji ketahanan model terhadap variasi windowing yang berbeda.
- **Weaknesses**:
  - **C1: Kerentanan terhadap Variasi Windowing HU**: Penulis tidak melakukan uji sensitivitas terhadap pergeseran jendela kontras CT scan (center/width HU shift).
    - Evidence Anchor: `[section: 03_methods]`
    - Severity: CRITICAL
  - **M1: Potensi Cherry-Picking pada Pemilihan Kasus Visualisasi**: Empat citra Grad-CAM yang ditampilkan semuanya merupakan kasus lesi besar (>5 cm); penulis tidak memperlihatkan visualisasi model pada lesi kecil (<1 cm) di mana model sering gagal.
    - Evidence Anchor: `[figure: 4]`
    - Severity: MAJOR

---

## 2. Contoh Luaran: `paper/07_editorial_decision.md`

```markdown
# Surat Keputusan Editorial (Editorial Decision Letter)

**Status Keputusan**: **MAJOR REVISION**  
**Tanggal Evaluasi**: 2026-09-21  
**Panel Evaluator**: 5 Penilai Independen (EIC + 3 Peer Reviewers + Devil's Advocate)  
**Protokol Evaluasi**: Kontrak Sprint Schema 13 (Sprint Contract Protocol v2)  

---

## 0. Baris Audit Sintesis Kanonikal (Pinned Audit Grammar)
```text
dimension_verdicts: [D1=BLOCK, D2=WARN, D3=BLOCK, D4=PASS, D5=PASS, D6=PASS]
fired_conditions: [F2]
da_critical_adjudications: [C1=VALIDATED]
editorial_decision=major_revision
```

---

## 1. Ringkasan Rekomendasi Panel Reviewer

| Peran Reviewer | Fokus Ulasan | Rekomendasi Mandiri |
|---|---|---|
| **Editor-in-Chief (EIC)** | `venue_fit_and_contribution` | **Minor Revision** |
| **Reviewer 1 (Methodology)** | `methodology_rigor` | **Major Revision** |
| **Reviewer 2 (Domain Expert)** | `domain_accuracy` | **Minor Revision** |
| **Reviewer 3 (Cross-Disciplinary Perspective)** | `cross_disciplinary_relevance` | **Minor Revision** |
| **Devil's Advocate (Adversarial Evaluator)** | `argumentative_coherence` | **Major Revision** |

---

## 2. Evaluasi 6 Dimensi Akseptasi (Schema 13)

| Dimensi | Nama Dimensi | Prioritas | Eligible Roles | Owner Role | Status Evaluasi |
|:---:|---|:---:|:---:|:---:|:---:|
| **D1** | methodology_rigor | `mandatory` | methodology | `methodology` | **🚫 BLOCK** |
| **D2** | domain_accuracy | `mandatory` | domain | `domain` | **⚠️ WARN** |
| **D3** | argumentative_coherence | `mandatory` | da, methodology | `da` | **🚫 BLOCK** |
| **D4** | cross_disciplinary_relevance | `high` | perspective | `perspective` | **✅ PASS** |
| **D5** | writing_and_structure | `normal` | eic | `eic` | **✅ PASS** |
| **D6** | venue_fit_and_contribution | `mandatory` | eic | `eic` | **✅ PASS** |

> **Kondisi Aturan Terpicu**: `F2` (any mandatory dimension scores 'block') $\rightarrow$ `editorial_decision=major_revision`.

---

## 3. Top Blocking Issues (Isu Pemblokir Prioritas Tinggi)

| Peringkat | ID Isu | Sumber | Dimensi | Severity | Deskripsi Cacat Kritis & Rujukan Roadmap |
|:---:|:---:|:---:|:---:|:---:|---|
| **#1** | **`ISSUE-02`** | Reviewer 1 | `D1` | **`CRITICAL`** | Ambiguitas Protokol Patient-Level Data Split (`[section: 03_materials-and-methods_02_experimental-setup]`) |
| **#2** | **`ISSUE-06`** | Devil's Advocate | `D3` | **`CRITICAL`** | Kerentanan terhadap Variasi Windowing HU (`[section: 03_methods]`) |
| **#3** | **`ISSUE-04`** | Reviewer 2 | `D2` | **`MAJOR`** | Pengabaian Benchmark SOTA ISLES 2024 (`[section: 02_related-works]`) |

---

## 4. Catatan Evaluasi Kritis per Dimensi

### D1: Methodology Rigor (`methodology`)
- **[ISSUE-02] [CRITICAL] Ambiguitas Protokol Patient-Level Data Split**: Pada bab metode tidak disebutkan secara eksplisit apakah pemisahan 5-fold cross-validation dilakukan pada tingkat pasien (*patient-level*) atau tingkat irisan citra acak (*random slice*). Hal ini merupakan celah validitas kritis. (Lokasi: `[section: 03_materials-and-methods_02_experimental-setup]`)
- **[ISSUE-03] [MINOR] Ketiadaan Uji Koreksi Bonferroni**: Pengujian ablasi terhadap 8 variasi modul tidak menyertakan koreksi uji berganda. (Lokasi: `[section: 04_results-and-discussion_03_ablation-study]`)

### D2: Domain Accuracy (`domain`)
- **[ISSUE-04] [MAJOR] Pengabaian Benchmark SOTA ISLES 2024**: Penulis membandingkan model dengan baseline 2021 tetapi mengabaikan arsitektur Swin UNETR terbaru pada benchmark ISLES. (Lokasi: `[section: 02_related-works]`)

### D3: Argumentative Coherence (`da`)
- **[ISSUE-06] [CRITICAL] Kerentanan terhadap Variasi Windowing HU**: Penulis tidak melakukan uji sensitivitas terhadap pergeseran jendela kontras CT scan (center/width HU shift). (Lokasi: `[section: 03_methods]`)
- **[ISSUE-07] [MAJOR] Potensi Cherry-Picking pada Pemilihan Kasus Visualisasi**: Empat citra Grad-CAM yang ditampilkan semuanya merupakan kasus lesi besar (>5 cm); penulis tidak memperlihatkan visualisasi model pada lesi kecil (<1 cm) di mana model sering gagal. (Lokasi: `[figure: 4]`)

### D4: Cross Disciplinary Relevance (`perspective`)
- **[ISSUE-05] [MINOR] Ketiadaan Analisis Biaya Komputasi Inferensi**: Belum ada laporan penggunaan memori GPU dan latensi inferensi per pasien pada perangkat standar IGD. (Lokasi: `[section: 04_results-and-discussion]`)

### D5: Writing And Structure (`eic`)
- *Tidak ditemukan kelemahan material pada dimensi ini (Memenuhi standar publikasi).*

### D6: Venue Fit And Contribution (`eic`)
- **[ISSUE-01] [MINOR] Keterbatasan Diskusi Generalisasi Vendor Scanner**: Penulis belum secara memadai mendiskusikan performa model jika diuji pada citra dari scanner vendor yang berbeda. (Lokasi: `[section: 05_conclusion]`)

---

## 5. Instruksi Revisi & Batas Waktu

Naskah Anda membutuhkan **REVISI MAYOR (MAJOR REVISION)**. Diperlukan analisis tambahan atau klarifikasi mendalam terhadap celah metodologis dan argumen sebelum naskah dapat dievaluasi kembali (*re-review*). Batas waktu pengajuan: **6–8 minggu**.
```

---

## 3. Contoh Luaran: `paper/08_revision_roadmap.md`

```markdown
# Rencana Aksi Revisi (Revision Roadmap Matrix)

Dokumen kerja ini memetakan seluruh catatan reviewer menjadi daftar tindakan perbaikan konkret dengan kriteria keterterimaan (*Acceptance Criteria*) terukur untuk persiapan draf revisi dan surat tanggapan (*Point-by-Point Response to Reviewers*).

---

## Matriks Tindakan Revisi Terprioritas

| ID Isu | Penilai Sumber | Dimensi | Severity | Ringkasan Isu & Lokasi Bukti | Rencana Aksi Perbaikan | Kriteria Keterterimaan (Acceptance Criteria) | Status |
|:---:|:---:|:---:|:---:|---|---|---|:---:|
| **`ISSUE-02`** | Reviewer 1 | `D1` | **`CRITICAL`** | Ambiguitas Protokol Patient-Level Data Split (`[section: 03_materials-and-methods_02_experimental-setup]`) | Berikan tabel distribusi pasien per fold dan tegaskan bahwa irisan dari pasien yang sama tidak pernah bercampur. | Distribusi pasien per fold diverifikasi bebas kebocoran (0% overlap) pada set validasi/pengujian. | [ ] |
| **`ISSUE-06`** | Devil's Advocate | `D3` | **`CRITICAL`** | Kerentanan terhadap Variasi Windowing HU (`[section: 03_methods]`) | Lakukan uji sensitivitas dengan menggeser center/width jendela sebesar ±15 HU dan laporkan stabilitas AUC. | Kurva ROC dan metrik AUROC terbukti stabil (variasi <1.5%) pada rentang pergeseran kontras HU yang wajar. | [ ] |
| **`ISSUE-04`** | Reviewer 2 | `D2` | **`MAJOR`** | Pengabaian Benchmark SOTA ISLES 2024 (`[section: 02_related-works]`) | Tambahkan sitasi paper Swin UNETR ISLES 2024 dan masukkan angka pembanding ke Tabel 2. | Paper Swin UNETR disitir dengan benar dan hasil komparasi metrik Dice score dicantumkan pada tabel hasil. | [ ] |
| **`ISSUE-07`** | Devil's Advocate | `D3` | **`MAJOR`** | Potensi Cherry-Picking pada Pemilihan Kasus Visualisasi (`[figure: 4]`) | Perbarui Gambar 4 dengan menyertakan 2 contoh kasus lesi kecil (<1 cm) di mana model berhasil dan gagal. | Gambar 4 memuat representasi berimbang antara kasus lesi stroke luas dan lesi dini samar (<1 cm). | [ ] |
| **`ISSUE-03`** | Reviewer 1 | `D1` | **`MINOR`** | Ketiadaan Uji Koreksi Bonferroni (`[section: 04_results-and-discussion_03_ablation-study]`) | Tambahkan catatan kaki nilai p terkoreksi Bonferroni pada Tabel 4. | Nilai p yang dilaporkan pada Tabel 4 disesuaikan dengan ambang batas signifikansi terkoreksi Bonferroni. | [ ] |
| **`ISSUE-05`** | Reviewer 3 | `D4` | **`MINOR`** | Ketiadaan Analisis Biaya Komputasi Inferensi (`[section: 04_results-and-discussion]`) | Catat latensi inferensi per volume 3D pada GPU RTX 3060/4090 di bab pembahasan. | Nilai latensi inferensi dalam detik/milidetik dicantumkan pada paragraf pembahasan efisiensi. | [ ] |
| **`ISSUE-01`** | Editor-in-Chief | `D6` | **`MINOR`** | Keterbatasan Diskusi Generalisasi Vendor Scanner (`[section: 05_conclusion]`) | Tambahkan 1 paragraf pengakuan keterbatasan scanner multi-vendor pada bab kesimpulan. | Bagian limitasi mencakup pengakuan eksplisit tentang perlunya validasi prospektif multi-vendor scanner. | [ ] |

---

## Pengelompokan Sprint Revisi Berdasarkan Prioritas

### Priority 1: Structural & Critical Revisions (Must Fix - Blocker)
- Wajib diselesaikan sebelum penyuntingan teks narasi; mencakup penegasan bebas data leakage pada partisi data dan pengujian sensitivitas windowing HU.

### Priority 2: Content & Literature Supplementation (Should Fix - Major)
- Menambahkan baseline pembanding ISLES 2024 dan menyajikan visualisasi Grad-CAM kasus lesi kecil yang seimbang.

### Priority 3: Text, Citations & Minor Formatting (Nice to Fix - Editorial)
- Menambahkan uji Bonferroni pada tabel ablasi, latensi komputasi, dan klausa limitasi scanner.
```
