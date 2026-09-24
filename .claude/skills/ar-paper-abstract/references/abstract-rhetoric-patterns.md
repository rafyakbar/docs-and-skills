# Pola Retorika Abstrak & Standar Penulisan Akademik (Abstract Rhetoric Patterns & Writing Standards)

Berkas rujukan ini menetapkan standar struktural, retorika, tata bahasa, dan gaya penulisan untuk menyusun abstrak akademik berstandar publikasi jurnal internasional bereputasi.

---

## 1. Kerangka Kerja Retorika 5 Komponen (The 5-Component Rhetorical Framework)

Abstrak akademik adalah representasi mandiri (*self-contained*) dan sangat padat yang merangkum keseluruhan naskah penelitian. Abstrak harus memungkinkan pembaca dan reviewer untuk menilai relevansi, ketelitian metodologi, dan kontribusi ilmiah penelitian dalam rentang 150–250 kata. Setiap abstrak harus mengikuti lima gerakan retorika berurutan:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Konteks & Masalah Penelitian (1–2 kalimat)               │
│ • Nyatakan urgensi domain, relevansi praktis, & hambatan    │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Tujuan & Solusi yang Diusulkan (1–2 kalimat)             │
│ • Umumkan model, kerangka kerja, atau tesis yang diajukan   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Metodologi & Pengaturan Eksperimen (1–2 kalimat)         │
│ • Sebutkan dataset, protokol validasi, pengklasifikasi/dasar│
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Temuan Empiris Kuantitatif Utama (2–3 kalimat)           │
│ • Laporkan metrik numerik presisi, komparasi, & margin nilai│
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Kesimpulan & Signifikansi Ilmiah (1 kalimat)             │
│ • Sampaikan intisari utama, dampak luas, & relevansi ilmiah │
└─────────────────────────────────────────────────────────────┘
```

### Rincian Komponen & Pola Kalimat

#### 1. Konteks & Masalah Penelitian (Context & Research Problem, 1–2 kalimat)
- **Tujuan (Objective)**: Membangun domain masalah dan mengartikulasikan hambatan teknis atau konseptual spesifik yang belum mampu diatasi oleh metode-metode terdahulu.
- **Rumusan Kalimat (Formulation)**:
  * *"Simultaneous demographic attribute classification from facial imagery faces significant challenges from subtle expression variations, biological aging, phenotypic overlap, and single-domain representation limitations."*  
    *(Klasifikasi atribut demografis simultan dari citra wajah menghadapi tantangan berat akibat variasi ekspresi mikro, penuaan biologis, tumpang tindih fenotipik, serta keterbatasan inheren representasi domain tunggal.)*
  * *"While vision transformers excel at global feature extraction, their application to multi-attribute classification is hindered by domain-specific feature entanglement."*  
    *(Meskipun Vision Transformer unggul dalam ekstraksi fitur global, penerapannya pada klasifikasi multi-atribut terhambat oleh keterikatan fitur spesifik domain.)*
- **Hal yang Harus Dihindari (What to Avoid)**: Pernyataan klise umum (*"Deep learning telah menjadi sangat populer"*), pengantar historis yang bertele-tele, atau memulai naskah secara canggung seperti *"Paper ini membahas..."*.

#### 2. Tujuan & Solusi yang Diusulkan (Purpose & Proposed Solution, 1–2 kalimat)
- **Tujuan (Objective)**: Memperkenalkan kontribusi ilmiah utama, arsitektur yang diajukan, kerangka kerja, atau hipotesis penelitian.
- **Rumusan Kalimat (Formulation)**:
  * *"This study proposes a multi-domain latent feature fusion framework that integrates task-specific visual representations extracted from frozen Vision Transformer (ViT) backbones..."*  
    *(Penelitian ini mengusulkan kerangka kerja fusi fitur laten multi-domain yang mengintegrasikan representasi visual spesifik tugas dari backbone Vision Transformer (ViT) yang dibekukan...)*
  * *"To resolve this bottleneck, this paper introduces an automated pipeline combining..."*  
    *(Untuk mengatasi hambatan tersebut, makalah ini memperkenalkan pipeline terotomatisasi yang menggabungkan...)*
- **Hal yang Harus Dihindari (What to Avoid)**: Pernyataan eksploratif yang lemah atau ragu (*"Kami bermaksud melihat apakah..."*). Gunakan kata kerja aktif yang tegas (*"proposes"*, *"develops"*, *"introduces"*, *"evaluates"*).

#### 3. Metodologi & Pengaturan Eksperimen (Methodology & Experimental Setup, 1–2 kalimat)
- **Tujuan (Objective)**: Merangkum sumber data, kondisi eksperimen, metodologi validasi, dan konfigurasi *baseline* pembanding.
- **Rumusan Kalimat (Formulation)**:
  * *"Latent features are extracted offline from pre-trained backbones and evaluated across seven feature configurations using 5-Fold Stratified Cross-Validation on four classifiers: Random Forest (RF), Gaussian Naive Bayes (GNB), Logistic Regression (LR), and Support Vector Machine (SVM) optimized via Grid Search Cross-Validation (GridSearchCV)."*  
    *(Vektor fitur laten diekstraksi secara luring dari backbone pra-latih dan dievaluasi pada tujuh konfigurasi fitur menggunakan 5-Fold Stratified Cross-Validation terhadap empat model pengklasifikasi: Random Forest (RF), Gaussian Naive Bayes (GNB), Logistic Regression (LR), dan Support Vector Machine (SVM) yang dioptimalkan melalui Grid Search Cross-Validation (GridSearchCV).)*
- **Hal yang Harus Dihindari (What to Avoid)**: Mengabaikan protokol validasi silang (*cross-validation*) atau tidak menyebutkan model pembanding (*baseline*) utama secara eksplisit.

#### 4. Temuan Empiris Kuantitatif Utama (Key Empirical Findings, 2–3 kalimat)
- **Tujuan (Objective)**: Menyajikan hasil kuantitatif paling unggul dan meyakinkan. Abstrak tanpa angka numerik pasti kehilangan bobot pembuktian ilmiah (*evidentiary authority*).
- **Rumusan Kalimat (Formulation)**:
  * *"Experimental evaluations demonstrate that tri-domain fusion achieves superior performance across three of the four evaluated classifiers, with the SVM configuration yielding the highest performance: 93.70% accuracy, 93.72% precision, 93.70% recall, and 93.69% macro F1-score on independent test data."*  
    *(Evaluasi eksperimental menunjukkan bahwa fusi tri-domain mencapai kinerja superior pada tiga dari empat pengklasifikasi yang diuji, dengan konfigurasi SVM menghasilkan performa tertinggi: akurasi 93,70%, presisi 93,72%, recall 93,70%, dan skor makro F1 93,69% pada data uji independen.)*
  * *"Subgroup diagnostics reveal consistent performance gains, with intersectional F1-scores spanning 91.74% to 96.14%."*  
    *(Diagnostik subkelompok menunjukkan peningkatan performa yang konsisten, dengan skor F1 interseksional berkisar antara 91,74% hingga 96,14%.)*
- **Hal yang Harus Dihindari (What to Avoid)**: Ringkasan kualitatif yang mengambang (*"Model yang diajukan mencapai hasil yang sangat baik dan mengalahkan metode lain"*). Selalu laporkan persentase konkret, metrik baku, atau signifikansi statistik ($p < 0.05$).

#### 5. Kesimpulan & Signifikansi Ilmiah (Conclusion & Significance, 1 kalimat)
- **Tujuan (Objective)**: Menyampaikan intisari utama, implikasi teoretis, atau kegunaan praktis dari temuan penelitian.
- **Rumusan Kalimat (Formulation)**:
  * *"...demonstrating the efficacy of multi-domain latent representations in mitigating intersectional demographic performance disparities."*  
    *(...membuktikan efektivitas representasi laten multi-domain dalam memitigasi disparitas performa demografis interseksional.)*
  * *"These findings provide a lightweight, reproducible foundation for fair biometric verification in production systems."*  
    *(Temuan ini menyediakan fondasi yang ringan dan dapat direproduksi untuk verifikasi biometrik berkeadilan pada sistem produksi.)*
- **Hal yang Harus Dihindari (What to Avoid)**: Janji masa depan yang berlebihan dan tidak berdasar (*"Penelitian ini akan melenyapkan seluruh bias demografis dalam AI"*).

---

## 2. Jenis Abstrak & Format Struktural (Abstract Types & Structural Formats)

| Format | Struktur | Norma Tempat Publikasi Tipikal |
|:---|:---|:---|
| **Paragraf Padat Tidak Terstruktur** (*Unstructured Dense Paragraph*, Paling Umum) | Paragraf tunggal kohesif berukuran 150–250 kata yang mengintegrasikan seluruh 5 komponen retorika tanpa subjudul. | Transaksi IEEE, jurnal ACM, jurnal rekayasa Elsevier, jurnal ilmu komputer Springer. |
| **Abstrak Terstruktur** (*Structured Abstract*) | Memiliki label subjudul tebal eksplisit: **Background**, **Methods**, **Results**, **Conclusions** (atau **Latar Belakang**, **Metode**, **Hasil**, **Kesimpulan**). | Jurnal medis, klinis, dan informatika kesehatan tertentu (misalnya Lancet, JAMA, BMJ). |
| **Abstrak Diperluas** (*Extended Abstract*) | Ringkasan multi-paragraf (500–1.000 kata) yang memuat sub-bagian mini, tabel awal, atau daftar poin kontribusi. | Workshop konferensi teknis bergengsi dan pengajuan simposium ilmiah. |

---

## 3. Konvensi Tata Bahasa & Kala Waktu (Grammatical & Tense Conventions)

- **Kala Lampau (Past Tense)**: Gunakan bentuk lampau (*simple past tense*) untuk tindakan dan prosedur yang dilakukan secara spesifik dalam penelitian ini:
  * *"Features were extracted offline..."*
  * *"The model achieved an accuracy of 93.70%..."*
  * *"We evaluated four downstream classifiers..."*
- **Kala Kini (Present Tense)**: Gunakan bentuk kini (*simple present tense*) untuk kebenaran ilmiah umum, deskripsi sistem/arsitektur yang diusulkan, atau signifikansi temuan yang berlaku universal:
  * *"Automated demographic recognition faces significant variance..."*
  * *"The framework integrates three complementary representations..."*
  * *"These results demonstrate that..."*
- **Larangan Mutlak Sitasi (Strict Prohibition of Citations)**: Jangan pernah menyertakan rujukan berkurung siku (`[1]`, `[2]`, atau sitasi penulis-tahun) di dalam abstrak. Abstrak harus mampu berdiri sendiri secara utuh (*fully self-contained*) saat diindeks secara terpisah pada pangkalan data bibliografi global (Scopus, IEEE Xplore, Web of Science, PubMed).
