# Eksemplar Referensi Ilustratif: Cetak Biru Paper Akademik Paragraf demi Paragraf

> [!NOTE]
> ### MURNI CONTOH ILUSTRATIF — JANGAN DIGUNAKAN ULANG SECARA VERBATIM
> Dokumen ini **murni merupakan contoh percontohan demonstratif** yang ditujukan semata-mata untuk menunjukkan standar format yang diharapkan, tingkat rincian paragraf demi paragraf, progresi naratif, dan pemetaan bukti.
> 
> - **Seluruh konten di bawah ini—termasuk topik penelitian, algoritma vision transformer, nama dataset, persamaan, temuan numerik, dan sitasi literatur—sepenuhnya merupakan skenario tiruan (*mock scenario*) ilustratif.**
> - **JANGAN menyalin, mengasumsikan, atau menerapkan topik, domain, atau venue spesifik ini pada permintaan pengguna.**
> - Untuk setiap tugas penyusunan outline riil, AI wajib menghasilkan cetak biru yang sepenuhnya orisinal dan disesuaikan berdasarkan fokus riset riil pengguna, data empiris, persyaratan publikasi target, dan model struktural yang dikonfirmasi setelah konsultasi intake.

---

## 0. Protokol Intake Pengguna & Penyiapan Skenario Tiruan (Mock Scenario Setup)

> [!IMPORTANT]
> **ATURAN INTAKE PENGGUNA WAJIB:**
> Sebelum menyusun outline, AI **TIDAK BOLEH** secara sepihak berasumsi atau memaksakan venue tertentu (seperti IEEE Access, Elsevier, Nature, dll.). AI wajib berkonsultasi dan mengonfirmasi parameter-parameter berikut dengan pengguna terlebih dahulu:
> 
> 1. **Target Publikasi / Venue**: Apakah ditujukan untuk jurnal internasional bereputasi (misal, IEEE Transactions, Elsevier Pattern Recognition, Nature Communications, ACM Computing Surveys), jurnal nasional terakreditasi, prosiding konferensi, atau bab tesis/disertasi?
> 2. **Gaya & Format Sitasi**: Format sitasi apa yang diwajibkan oleh panduan penulis (IEEE numerik, APA 7, Harvard, ACM, Vancouver, Chicago)?
> 3. **Bahasa Naskah & Kebijakan Terminologi**: Bahasa Inggris formal, atau naskah dengan istilah teknis standar bahasa Inggris?
> 4. **Model Struktural**: Apakah penelitian mengikuti IMRaD (penelitian empiris), Thematic Literature Review, Theoretical Analysis, Case Study, atau Policy Brief?
> 5. **Target Jumlah Kata**: Berapa rentang target jumlah kata total (misalnya, 6.000–8.000 kata)?
>
> *(Bagian berikut mengilustrasikan cetak biru tiruan yang dihasilkan **SETELAH** pengguna hipotetis mengonfirmasi bahwa target mereka adalah jurnal internasional Q1 bereputasi di bidang Multimedia / Machine Learning, ditulis dalam bahasa Inggris formal, menggunakan format sitasi IEEE, dan mengikuti model IMRaD empiris).*

### Konfigurasi Tiruan Ilustratif (Pilihan Hipotetis Pengguna)
- **Target Venue**: [Pilihan Tiruan Pengguna: Jurnal Internasional Bereputasi di bidang Multimedia / AI, misal, IEEE / ACM / Elsevier]
- **Bahasa Naskah**: [Pilihan Tiruan Pengguna: Bahasa Inggris formal dengan terminologi teknis standar]
- **Format Sitasi**: [Pilihan Tiruan Pengguna: Format numerik IEEE dengan referensi kontekstual penulis-tahun dalam teks selama penulisan draf]
- **Topik Demonstrasi**: Multi-Domain Latent Representation Fusion using Vision Transformers and Classical Machine Learning Optimization for Robust Acoustic-Visual Scene Classification

---

## Aturan Penulisan Global & Batasan Klaim Demonstratif

### A. Klaim yang Diizinkan & Fokus Inti (Aturan Tiruan Ilustratif)
1. **Fokus Utama**: Evaluasi empiris sistematis terhadap fusi fitur laten luring (*offline latent feature fusion*) dari tiga domain audio-visual komplementer (spektrogram akustik ViT, pemandangan visual ViT, dan dinamika gerak spasial ViT) menggunakan Vision Transformer beku prapelatihan (*frozen pretrained ViT*) yang dipadukan dengan alur kerja pembelajaran mesin klasik teroptimasi (GridSearchCV dengan Stratified Cross-Validation 5-Lipatan).
2. **Keunggulan Fusi Tiga-Domain**: Fusi tiga-domain (2.304 dimensi) mencapai performa tertinggi pada **3 dari 4 pengklasifikasi yang dievaluasi** (Support Vector Machine / SVM, Logistic Regression / LR, dan Gaussian Naive Bayes / GNB), dengan model puncak **SVM Tiga-Domain** meraih akurasi **94,20%** dan Macro F1-Score **94,15%** pada dataset tolok ukur ($N = 2.400$ instans uji).
3. **Pencegahan Kebocoran Informasi (Information Leakage Prevention)**: Penskalaan prapemrosesan (StandardScaler) dan reduksi dimensi (PCA) disesuaikan (*fitted*) secara ketat hanya di dalam lipatan pelatihan (*training folds*) selama validasi silang, dan evaluasi akhir dijalankan pada kohort uji terisolasi (*held-out test cohort*).
4. **Stabilitas Performa Subkelompok**: Evaluasi per kelas yang terperinci di seluruh 6 kelas pemandangan lingkungan mempertahankan skor F1 di atas 91,50%, yang membuktikan stabilitas lintas-domain.

### B. Batasan Negatif & Klaim yang Dilarang (Aturan Tiruan Ilustratif)
1. **Tidak Ada Klaim Mutlak "Nol Kebocoran"**: Diformulasikan sebagai "dirancang secara metodologis untuk mencegah kebocoran informasi", alih-alih mengklaim infalibilitas matematis tanpa kebocoran sama sekali.
2. **Larangan Kata "Secara Signifikan" Tanpa Kualifikasi**: Kata "secara signifikan" (*significantly*) hanya boleh digunakan apabila didukung oleh pengujian hipotesis statistik formal ($p < 0,05$). Gunakan kata "secara substansial", "secara nyata", atau "mencapai performa lebih tinggi" untuk observasi deskriptif.
3. **Hindari Superlatif SOTA Tanpa Batasan**: Gunakan formulasi "mencapai performa teramati tertinggi di antara konfigurasi yang dievaluasi pada dataset tolok ukur", alih-alih mengklaim SOTA universal mutlak.
4. **Tidak Mengklaim Keunggulan Universal**: Mengakui secara faktual bahwa fusi tiga-domain unggul pada 3 dari 4 pengklasifikasi, sedangkan Random Forest mencapai puncaknya pada konfigurasi dua-domain (87,30%).
5. **Hindari Em-Dash (—)**: Gunakan koma (,), tanda kurung ( ), atau tanda hubung standar (-).
6. **Batas Densitas Sitasi**: Maksimal 3 sitasi per kalimat untuk menjaga keterbacaan naskah dan mencegah penumpukan sitasi (*citation dumping*).

### C. Urutan Elemen Master & Spesifikasi Tata Letak (Registri Tiruan Ilustratif)
- **Persamaan (1)–(8)**: Diberi nomor secara kronologis sesuai urutan kemunculan dalam narasi teks.
- **Gambar 1**: Diagram arsitektur kerangka kerja menyeluruh (*end-to-end framework*) (Lebar Penuh LaTeX: `\begin{figure*} ... \end{figure*}`).
- **Gambar 2**: Diagram radar F1-Score subkelompok lintas pengklasifikasi (Satu kolom).
- **Tabel I**: Distribusi dataset dan ringkasan atribut sensorik (Satu kolom).
- **Tabel II**: Ruang pencarian hiperparameter untuk pengklasifikasi klasik (Satu kolom).
- **Tabel III**: Tolok ukur performa global dan studi ablasi fitur (Lebar Penuh LaTeX: `\begin{table*} ... \end{table*}`).
- **Tabel IV**: Matriks konfusi dan distribusi galat per kelas (Satu kolom).

---

## Halaman Depan Demonstratif

### Judul Paper
**Multi-Domain Latent Representation Fusion with Pretrained Vision Transformers for Robust Acoustic-Visual Scene Classification**

### Cetak Biru Abstrak
*Target: 180–220 kata, satu paragraf terpadu mengikuti 5 pergerakan retoris:*
- **Pergerakan 1 (Konteks & Tantangan)**: Pengenalan pemandangan lingkungan otomatis pada sistem penginderaan IoT multimodal menghadapi interferensi derau akustik, oklusi visual, dan defisit representasi unimodal.
- **Pergerakan 2 (Tujuan)**: Penelitian ini mengusulkan kerangka kerja fusi representasi laten multi-domain yang mengintegrasikan sematan fitur luring dari tiga arsitektur tulang punggung (*backbone*) Vision Transformer (ViT) beku prapelatihan dengan alur kerja pembelajaran mesin klasik teroptimasi.
- **Pergerakan 3 (Metodologi)**: Representasi laten yang menangkap spektrogram akustik, pemandangan visual, dan dinamika gerak spasial diekstraksi secara luring dan digabungkan (*concatenated*) ke dalam ruang laten terpadu. Klasifikasi hilir dan penyetelan hiperparameter dijalankan pada empat algoritma (SVM, Logistic Regression, Random Forest, Gaussian Naive Bayes) menggunakan Stratified Cross-Validation 5-Lipatan dengan isolasi ketat data lipatan pelatihan.
- **Pergerakan 4 (Hasil Kunci)**: Model Support Vector Machine (SVM) tiga-domain mencapai performa tertinggi di antara konfigurasi yang dibandingkan, menghasilkan akurasi 94,20% dan Macro F1-score 94,15%, serta mempertahankan skor F1 per kelas di atas 91,50% pada seluruh kategori pemandangan yang dievaluasi.
- **Pergerakan 5 (Kesimpulan & Kontribusi)**: Temuan ini membuktikan bahwa fusi representasi transformer lintas-domain secara substansial meningkatkan ketahanan klasifikasi, menyediakan arsitektur yang modular dan efisien secara komputasi untuk kecerdasan sensorik multimodal.

### Kata Kunci
Acoustic-visual scene classification; Vision Transformer; multimodal feature fusion; algorithmic robustness; Support Vector Machine; cross-validation.

---

## Bagian I Demonstratif: PENDAHULUAN (INTRODUCTION)

### Peta Progresi Naratif
```
[Paragraf 1: Keberadaan Luas & Kerentanan Praktis Penginderaan Multimodal]
                               │
                               ▼
[Paragraf 2: Titik Buta Representasional pada Sistem Unimodal]
                               │
                               ▼
[Paragraf 3: Kemajuan Vision Transformer & Paradigma Self-Attention]
                               │
                               ▼
[Paragraf 4: Kesenjangan Riset Kritis dalam Literatur Kontemporer]
                               │
                               ▼
[Paragraf 5: Solusi Arsitektural yang Diusulkan: Fusi ViT Tiga-Domain]
                               │
                               ▼
[Paragraf 6: Empat Kontribusi Ilmiah Utama]
                               │
                               ▼
[Paragraf 7: Struktur Organisasi Artikel]
```

### Paragraf 1: Keberadaan Luas dan Tantangan Praktis dalam Penginderaan Lingkungan
- **Target Jumlah Kata**: 120–150 kata.
- **Tujuan (Objective)**: Menetapkan peran penting klasifikasi pemandangan akustik-visual dalam sistem cerdas modern serta menyoroti degradasi performa akibat derau lingkungan dunia nyata.
- **Poin-Poin Naratif**:
  1. Klasifikasi pemandangan lingkungan otomatis merupakan tulang punggung perseptual dari robotika otonom, pengawasan cerdas, dan pemantauan ekologis.
  2. Penerapan di dunia nyata menghadapi dengung akustik (*reverberation*), oklusi visual, dan derau sensor yang menurunkan ketepatan klasifikasi.
  3. Arsitektur tersemat konvensional mengalami penurunan akurasi drastis ketika kondisi operasional menyimpang dari distribusi data pelatihan yang ideal.
- **Penugasan Bukti & Sitasi**: Survei tolok ukur komprehensif tentang pemantauan lingkungan multimodal (Smith et al., 2023; Zhao & Vance, 2024).
- **Kalimat Transisi**: Meskipun integrasi multimodal diakui sangat penting, merancang arsitektur yang mampu menyelaraskan aliran sensorik yang heterogen secara sinergis di bawah variabilitas lingkungan tetap menjadi tantangan terbuka.

### Paragraf 2: Keterbatasan Modalitas Sensorik Terisolasi
- **Target Jumlah Kata**: 110–140 kata.
- **Tujuan (Objective)**: Menjelaskan mengapa ketergantungan pada modalitas sensorik terisolasi (hanya audio atau hanya visual) memicu titik buta (*blind spots*) yang fatal.
- **Poin-Poin Naratif**:
  1. Pendekatan tradisional memproses spektrogram audio atau bingkai visual secara terisolasi atau mengandalkan pemungutan suara keputusan tahap akhir (*late decision voting*) yang naif.
  2. Model unimodal gagal mengurai ambiguitas sensorik, seperti membedakan taman kota dari hutan pinggiran kota di mana fitur visual tumpang tindih namun lanskap akustiknya sangat berbeda.
  3. Kegagalan menangkap korelasi lintas-modal membuat sistem rentan mengalami salah klasifikasi setiap kali salah satu aliran sensor terdegradasi.
- **Penugasan Bukti & Sitasi**: Studi komparatif mengenai pola kegagalan unimodal (Kwon et al., 2023; Martinez & Thorne, 2024).
- **Kalimat Transisi**: Mengatasi titik buta unimodal ini menuntut ruang representasi yang mampu memodelkan interaksi lintas-modalitas secara halus tanpa memicu lonjakan kompleksitas komputasi.

### Paragraf 3: Paradigma Vision Transformer dalam Representasi Multimodal
- **Target Jumlah Kata**: 140–180 kata.
- **Tujuan (Objective)**: Membahas transisi dari CNN berbidang reseptif lokal ke Vision Transformer (ViT) dan mekanisme self-attention global dalam pemrosesan data sensorik.
- **Poin-Poin Naratif**:
  1. Ekstraktor konvolusional klasik bergantung pada bidang reseptif lokal, yang membutuhkan penumpukan hierarkis dalam untuk menangkap konteks spasial global.
  2. Vision Transformer memanfaatkan Multi-Head Self-Attention (MHSA) untuk memodelkan interaksi berpasangan langsung antar seluruh patch citra atau bin frekuensi-waktu di seluruh bidang reseptif.
  3. Arsitektur backbone ViT prapelatihan menunjukkan daya transferabilitas yang kuat lintas domain visual dan spektrogram tanpa memerlukan modifikasi struktural mendasar.
- **Penugasan Bukti & Sitasi**: Makalah fondasional ViT dan mekanisme atensi yang diterapkan pada domain sensorik (Dosovitskiy et al., 2021; Radford et al., 2023; Patel et al., 2024). Maksimal 3 sitasi.
- **Kalimat Transisi**: Terlepas dari kemajuan representasional ini, dinamika interaksi sematan laten transformer multi-domain ketika dipadukan dengan alur klasifikasi hilir masih belum banyak dieksplorasi.

### Paragraf 4: Kesenjangan Riset Kritis
- **Target Jumlah Kata**: 120–150 kata.
- **Tujuan (Objective)**: Merumuskan tiga kesenjangan riset utama yang memotivasi penyelidikan ini.
- **Poin-Poin Naratif**:
  1. *Kesenjangan 1 (Isolasi Representasi)*: Literatur yang ada jarang mengintegrasikan spektrogram akustik, pemandangan visual statis, dan gerak spasial ke dalam ruang fitur laten terpadu.
  2. *Kesenjangan 2 (Dinamika Batas Keputusan)*: Riset terdahulu sebagian besar berfokus pada penyesuaian halus menyeluruh (*end-to-end fine-tuning*), sehingga perilaku batas keputusan pengklasifikasi klasik pada ruang laten transformer belum teruji secara sistematis.
  3. *Kesenjangan 3 (Kebocoran Prapemrosesan & Ketelitian Subkelompok)*: Sangat sedikit studi yang mengisolasi prapemrosesan data secara ketat di dalam lipatan validasi silang seraya mengevaluasi stabilitas subkelompok terperinci pada kategori pemandangan heterogen.
- **Penugasan Bukti & Sitasi**: Survei defisit yang belum terselesaikan dalam klasifikasi multimodal (Chen & Al-Mansoor, 2024).
- **Kalimat Transisi**: Guna mengatasi kesenjangan spesifik tersebut, penelitian ini memperkenalkan kerangka fusi fitur ViT multi-domain yang dipadukan dengan alur pengklasifikasi hilir yang dioptimasi secara ketat.

### Paragraf 5: Kerangka Arsitektur yang Diusulkan
- **Target Jumlah Kata**: 150–190 kata.
- **Tujuan (Objective)**: Menyajikan solusi fusi ViT multi-domain dan optimasi pengklasifikasi klasik yang diusulkan secara konseptual dan sistematis.
- **Poin-Poin Naratif**:
  1. Kami mengusulkan kerangka ekstraksi fitur laten luring yang memanfaatkan tiga backbone ViT beku prapelatihan: ViT-Spectrogram, ViT-Scene, dan ViT-Motion.
  2. Sematan laten yang diekstraksi disatukan melalui penggabungan langsung ($\mathbf{z}_{\text{tri}} = \mathbf{f}_{\text{audio}} \oplus \mathbf{f}_{\text{visual}} \oplus \mathbf{f}_{\text{motion}}$), membentuk representasi ringkas berdimensi 2.304.
  3. Sematan terpadu tersebut dievaluasi pada empat pengklasifikasi klasik (SVM, Logistic Regression, Random Forest, Gaussian Naive Bayes) yang dioptimasi melalui GridSearchCV.
  4. Penskalaan prapemrosesan dan reduksi dimensi diisolasi secara ketat di dalam lipatan pelatihan guna mengeliminasi kebocoran informasi.
- **Sitasi Visual Wajib**: Rujuk Gambar 1 (Diagram Alur Kerja Sistem Menyeluruh).
- **Kalimat Transisi**: Kerangka kerja sistematis ini menghasilkan peningkatan empiris yang terverifikasi dan ketelitian metodologis pada seluruh dimensi evaluasi.

### Paragraf 6: Kontribusi Riset Utama
- **Target Jumlah Kata**: 130–160 kata.
- **Tujuan (Objective)**: Memerinci empat kontribusi ilmiah dan empiris utama dari penelitian ini.
- **Poin-Poin Naratif (Daftar Kontribusi Terinci)**:
  1. **Kerangka Kerja Fusi Fitur ViT Multi-Domain Modular** yang menyatukan representasi frekuensi-waktu akustik, visual statis, dan gerak temporal ke dalam ruang laten yang kohesif.
  2. **Tolok Ukur Komparatif Empiris Lintas Paradigma Pengklasifikasi** yang mengevaluasi dinamika batas keputusan dan sensitivitas hiperparameter pada model linier, probabilistik, ensemble, dan berbasis kernel.
  3. **Demonstrasi Performa Kompetitif** yang membuktikan bahwa fusi SVM tiga-domain meraih akurasi 94,20%, mengungguli seluruh tolok ukur ablasi domain-tunggal dan domain-ganda pada dataset rujukan.
  4. **Validasi Bebas Kebocoran yang Ketat & Analisis Subkelompok** yang memverifikasi konsistensi skor F1 di atas 91,50% di seluruh kelas pemandangan di bawah prapemrosesan out-of-fold yang ketat.
- **Kalimat Transisi**: Bagian selanjutnya dari artikel ini menyajikan transparansi penuh mengenai dataset, metodologi, temuan eksperimental, dan implikasi teoretis.

### Paragraf 7: Gambaran Umum Struktur Artikel
- **Target Jumlah Kata**: 60–80 kata.
- **Tujuan (Objective)**: Menyediakan peta jalan organisasi artikel yang jelas bagi pembaca.
- **Poin-Poin Naratif**:
  - Bagian II menyintesis literatur yang relevan dan mengontekstualisasikan pemosisian riset.
  - Bagian III memaparkan dataset, alur kerja ekstraksi fitur, algoritma optimasi, dan metrik evaluasi.
  - Bagian IV menyajikan hasil empiris, studi ablasi, distribusi galat, dan pembahasan mendalam.
  - Bagian V menyimpulkan artikel dengan poin-poin utama, kendala praktis, dan arah riset di masa mendatang.

---

## Bagian II Demonstratif: KAJIAN PUSTAKA TERKAIT (RELATED WORKS) (Contoh Ilustratif)

*(Setiap paragraf di Bagian II menargetkan 100–120 kata dengan tujuan tematik yang terfokus, sintesis komparatif lintas makalah yang dirujuk, dan transisi penutup yang logis).*
- **Paragraf 1**: *Penginderaan Lingkungan Multimodal & Deskriptor Klasik* (Mengulas deskriptor akustik/visual buatan tangan (*handcrafted*) dan transisinya ke deep learning).
- **Paragraf 2**: *Vision Transformer untuk Representasi Spektrogram dan Visual* (Karakteristik struktural MHSA pada masukan sensor).
- **Paragraf 3**: *Strategi Fusi Fitur: Awal, Akhir, dan Menengah* (Membandingkan trade-off penggabungan representasi).
- **Paragraf 4**: *Pengklasifikasi Hilir pada Sematan Deep Learning* (Perilaku batas keputusan model kernel vs. linier pada vektor laten berdimensi tinggi).
- **Paragraf 5**: *Pemosisian Riset* (Sintesis orisinal yang mendefinisikan kebaruan penelitian ini tanpa memperkenalkan sitasi baru).

---

## Bagian III Demonstratif: MATERI DAN METODE (MATERIALS AND METHODS) (Contoh Ilustratif)

### Gambaran Umum
- **Target Jumlah Kata**: 150–200 kata.
- **Tujuan (Objective)**: Menjelaskan alur pemrosesan keseluruhan yang diilustrasikan pada Gambar 1.
- **Sitasi Visual**: Gambar 1 (Lebar Penuh LaTeX: `\begin{figure*} ... \end{figure*}`).
- **Rencana Formulasi Matematika**:
  - Persamaan (1): Partisi Patch ViT dan Proyeksi Linier.
  - Persamaan (2): Formulasi Multi-Head Self-Attention (MHSA).
  - Persamaan (3): Penggabungan Fitur Tiga-Domain $\mathbf{z}_{\text{tri}} = \mathbf{f}_{\text{audio}} \oplus \mathbf{f}_{\text{visual}} \oplus \mathbf{f}_{\text{motion}}$.
  - Persamaan (4): Formulasi Kernel Polinomial SVM $\mathcal{K}(\mathbf{x}_i, \mathbf{x}_j) = (\gamma \langle \mathbf{x}_i, \mathbf{x}_j \rangle + r)^d$.
  - Persamaan (5)–(8): Metrik Evaluasi One-vs-Rest (Akurasi, Presisi, Perolehan/Recall, Macro F1-Score).

### Pembagian Sub-Bab & Paragraf:
- **III.A Dataset dan Protokol Partisi Data** (Paragraf 1–3: Komposisi dataset, pemisahan latih/uji 80/20, augmentasi derau).
- **III.B Ekstraksi Fitur Multi-Domain melalui ViT Beku** (Paragraf 4–6: Spesifikasi backbone, pooling token [CLS], isolasi komputasi).
- **III.C Pipeline Pengklasifikasi Hilir & Penyetelan Hiperparameter** (Paragraf 7–9: Pipeline Scaler-PCA, ruang pencarian GridSearchCV, isolasi lipatan ketat).
- **III.D Metrik Evaluasi dan Lingkungan Eksperimen** (Paragraf 10–11: Definisi metrik, konfigurasi perangkat keras, pengujian signifikansi statistik).

---

## Bagian IV Demonstratif: HASIL DAN PEMBAHASAN (RESULTS AND DISCUSSION) (Contoh Ilustratif)

### Sub-Bab & Jangkar Visual:
- **IV.A Tolok Ukur Performa Global** (Tabel III: Akurasi keseluruhan, presisi makro, recall, F1 pada seluruh 4 pengklasifikasi).
- **IV.B Studi Ablasi Domain Fitur** (Gambar 2: Kontribusi empiris konfigurasi domain-tunggal, domain-ganda, dan tiga-domain).
- **IV.C Analisis Interseksional Subkelompok & Galat** (Tabel IV & Gambar 3: Stabilitas tingkat kelas dan pola salah klasifikasi).
- **IV.D Kompleksitas Komputasi dan Latensi Inferensi** (Tabel V: Tolok ukur waktu eksekusi ekstraksi fitur dan latensi pengklasifikasi).
- **IV.E Pembahasan & Implikasi Teoretis** (Menyintesis temuan dengan literatur terdahulu, menjelaskan perilaku kernel, dan memaparkan keterbatasan).

---

## Bagian V Demonstratif: KESIMPULAN (CONCLUSION) (Contoh Ilustratif)

- **Paragraf 1: Ringkasan Temuan Kunci** (100–120 kata: Sintesis jawaban atas pertanyaan penelitian dan metrik empiris utama).
- **Paragraf 2: Keterbatasan & Kendala Praktis** (80–100 kata: Pembahasan jujur mengenai resolusi sensor, dengung akustik, dan kebutuhan memori).
- **Paragraf 3: Arah Riset Masa Depan** (70–90 kata: Jalur penelitian prospektif, pembelajaran adaptif daring, dan prapelatihan multimodal swaselia/*self-supervised*).
