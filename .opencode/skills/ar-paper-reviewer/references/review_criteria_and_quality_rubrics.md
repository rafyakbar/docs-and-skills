# Rubrik Kualitas, Standar Pelaporan Statistik & Checklist Cacat Fatal

Dokumen ini memuat rubrik evaluasi kuantitatif 0–100, pemetaan status mutu per dimensi, standar pelaporan statistik universal, serta daftar periksa (*checklist*) cacat fatal metodologis naskah akademik.

---

## 1. Pemetaan Skor Kualitas (0 – 100) ke Keputusan Editorial

| Rentang Skor | Tingkat Kualitas (*Quality Descriptor*) | Karakteristik Utama | Rekomendasi Editorial |
|:---:|---|---|:---:|
| **$\ge 80$** | **Exceptional (90–100) / Strong (80–89)** | Riset sangat matang, metodologi kokoh tanpa cacat, kontribusi teoritis/praktis jelas, penulisan elegan dan transparan. | **Accept** |
| **65 – 79** | **Strong (75–79) / Adequate (65–74)** | Kualitas di atas rata-rata, desain penelitian valid, menyisakan beberapa pertanyaan klarifikasi narasi atau tambahan analisis sensitivitas minor. | **Minor Revision** |
| **50 – 64** | **Adequate (60–64) / Weak (50–59)** | Memiliki potensi kontribusi tetapi menyisakan kelemahan metodologis substantif, kekurangan baseline pembanding utama, atau overklaim. | **Major Revision** |
| **$< 50$** | **Weak (35–49) / Insufficient (<35)** | Memuat cacat fatal pada desain penelitian (misal: kebocoran data subjek, metrik invalid, data tidak memadai) yang tidak dapat diperbaiki melalui revisi. | **Reject** |

---

## 2. Rubrik Evaluasi Lengkap 6 Dimensi (D1 – D6)

### D1: Rigor Metodologis (`methodology_rigor` - Mandatory)
- **Exceptional (90–100)**: Partisi data strictly subject/patient-level, cross-validation multi-fold yang terlindungi dari kebocoran, pelaporan metrik lengkap dengan interval kepercayaan 95% (95% CI), uji signifikansi inferensial formal (DeLong test / Wilcoxon / ANOVA terkoreksi), dan repositori kode publik yang dapat direproduksi.
- **Strong (75–89)**: Desain penelitian solid dan bebas kebocoran data, namun interval kepercayaan belum dilaporkan pada beberapa sub-metrik sekunder.
- **Adequate (60–74)**: Penjelasan validasi kurang transparan; data train/test split tidak dijelaskan apakah berbasis subjek unik atau irisan acak; ukuran sampel pengujian terbatas.
- **Insufficient (<50)**: Terbukti terjadi kebocoran data (*data leakage*) atau metrik evaluasi salah secara matematis.

### D2: Akurasi Domain & Literatur (`domain_accuracy` - Mandatory)
- **Exceptional (90–100)**: Tinjauan pustaka mencakup karya seminal hingga paper SOTA 1–2 tahun terakhir; perbandingan baseline mencakup model arsitektur terkini dengan konfigurasi adil; terminologi domain presisi.
- **Strong (75–89)**: Cakupan literatur memadai namun mengabaikan 1–2 paper relevan dari tahun berjalan; perbandingan baseline cukup lengkap.
- **Adequate (60–74)**: Sebagian besar referensi sudah kedaluwarsa (>5 tahun lalu); baseline pembanding hanya menggunakan model usang tanpa model mutakhir.
- **Insufficient (<50)**: Tinjauan pustaka salah merepresentasikan temuan paper acuan; klaim domain bertentangan dengan konsensus ilmiah tanpa bukti tandingan.

### D3: Koherensi Argumen & Pengujian Adversarial (`argumentative_coherence` - Mandatory)
- **Exceptional (90–100)**: Tesis sentral dipertahankan dengan argumen logis yang ketat; penulis secara terbuka mengakui keterbatasan studi; kebal terhadap skenario penyangkalan counter-arguments.
- **Strong (75–89)**: Alur penalaran logis dan konsisten; diskusi keterbatasan ada namun dapat diperdalam pada aspek generalisasi lingkungan/scanner.
- **Adequate (60–74)**: Ditemukan indikasi cherry-picking pada metrik evaluasi; penjelasan diskrepansi performa pada kasus sulit dihindari.
- **Insufficient (<50)**: Kesimpulan tidak didukung oleh data hasil eksperimen (*non-sequitur*); penulis mengabaikan faktor perancu (*confounding variables*) utama.

### D4: Relevansi Lintas Disiplin & Etika (`cross_disciplinary_relevance` - High)
- **Exceptional (90–100)**: Implikasi studi dijabarkan dengan jelas bagi praktisi lapangan; perizinan komite etik (IRB) dan anonimisasi data subjek/pasien terdokumentasi lengkap.
- **Strong (75–89)**: Relevansi praktis baik; protokol etika disebutkan namun nomor registrasi protokol belum dicantumkan secara eksplisit.
- **Adequate (60–74)**: Naskah ditulis dalam jargon subdisiplin yang sangat tertutup; tidak ada pembahasan mengenai implikasi biaya komputasi atau penerapannya di lingkungan terbatas.
- **Insufficient (<50)**: Menggunakan data medis/manusia tanpa bukti izin komite etik (*ethical clearance*); potensi pelanggaran privasi data.

### D5: Penulisan & Struktur Naskah (`writing_and_structure` - Normal)
- **Exceptional (90–100)**: Struktur IMRaD kanonikal mengalir dengan kohesi sempurna; resolusi visualisasi grafik/tabel berstandar cetak tinggi dengan keterangan mandiri (*self-contained captions*); tata bahasa akademik elegan.
- **Strong (75–89)**: Alur naskah terstruktur baik; tabel dan grafik jelas; terdapat beberapa kesalahan tipografi minor yang tidak mengganggu pemahaman.
- **Adequate (60–74)**: Beberapa seksi naskah tidak proporsional (misal Discussion terlalu pendek); grafik beresolusi rendah atau sumbu grafik tidak diberi label satuan jelas.
- **Insufficient (<50)**: Naskah tidak mengikuti struktur ilmiah baku; eksposisi membingungkan; visualisasi tidak terbaca.

### D6: Kesesuaian Venue & Kontribusi (`venue_fit_and_contribution` - Mandatory)
- **Exceptional (90–100)**: Topik dan kedalaman riset sangat selaras dengan minat pembaca jurnal target; kontribusi orisinalitas tinggi dan mampu memicu arah riset lanjutan.
- **Strong (75–89)**: Relevansi venue kuat; kontribusi jelas meskipun bersifat pembaruan arsitektural bertahap (*incremental progress*).
- **Adequate (60–74)**: Relevansi dengan pembaca jurnal marginal; kontribusi ilmiah tipis dan belum diposisikan secara jelas terhadap batasan masalah.
- **Insufficient (<50)**: Di luar ruang lingkup jurnal (*out-of-scope*); tidak menyajikan kebaruan ilmiah (*no novelty*).

---

## 3. Standar Pelaporan Statistik Universal (APA 7.0 & Biomedical Rigor)

1. **Format Pelaporan Angka Statistik**:
   - Angka probabilitas tidak diawali angka nol (*no leading zero*): $p < .001$, $p = .042$.
   - Larangan mutlak pelaporan $p = .000$ (wajib ditulis $p < .001$).
   - Simbol statistik dicetak miring: *$t$*, *$F$*, *$p$*, *$r$*, *$N$*, *$d$*, *$z$*.
2. **Kewajiban Pelaporan Estimasi Ketidakpastian**:
   - Setiap metrik performa (AUROC, Sensitivitas, Akurasi, F1-Score) wajib disertai interval kepercayaan 95% ($\text{95\% CI: } [X, Y]$).
   - Perbandingan antar-model wajib menggunakan uji signifikansi inferensial berpasangan (uji DeLong untuk kurva ROC, uji Wilcoxon signed-rank untuk data non-parametrik).
3. **Kewajiban Pelaporan Ukuran Efek (*Effect Size*)**:
   - Tidak cukup hanya melaporkan nilai $p$; wajib menyertakan Cohen's $d$, odds ratio (OR), atau $\eta^2$ untuk menunjukkan signifikansi praktis temuan.
4. **Koreksi Pengujian Berganda (*Multi-Hypothesis Correction*)**:
   - Pengujian terhadap $\ge 3$ kelompok perlakuan atau ablasi wajib menerapkan koreksi Bonferroni, Holm, atau False Discovery Rate (FDR).

---

## 4. Checklist Deteksi Dini Cacat Fatal (Fatal Flaws Checklist)

Jika salah satu dari kondisi berikut terbukti terjadi, reviewer wajib mengeluarkan status `CRITICAL / FATAL` yang memicu penolakan naskah (*Desk Reject / Reject*):

- [ ] **1. Subject/Entity-Level Data Contamination & Leakage**:  
  Data pengujian (irisan citra, sesi pengguna, deret waktu) dari entitas atau subjek yang sama terdistribusi ke dalam set training dan testing.
- [ ] **2. P-Hacking, HARKing & Flexible Stopping Rules**:  
  Pengujian berulang hingga mencapai ambang batas $p < .05$ tanpa koreksi statistik, atau memformulasikan hipotesis setelah melihat data (*Hypothesizing After the Results are Known*).
- [ ] **3. Flawed Ground Truth / Label Noise**:  
  Pelabelan data dasar tidak memiliki validasi ahli klinis/domain atau tingkat kesepakatan penilai (*inter-observer agreement / Cohen's kappa*) tidak dilaporkan.
- [ ] **4. Extreme Multicollinearity (VIF > 10)**:  
  Model regresi atau penjelas menyertakan variabel prediktor dengan korelasi linear ekstrem tanpa mitigasi atau uji VIF.
- [ ] **5. Overclaimed Novelty (Klaim Kebaruan Palsu)**:  
  Penulis mengklaim menciptakan metode baru, padahal metode tersebut telah dipublikasikan oleh pihak lain tanpa atribusi sah.
- [ ] **6. Unreproducible Pipeline (Eksperimen Gelap)**:  
  Hiperparameter kritis, seed pengacakan, normalisasi data, atau detail kode disembunyikan sehingga studi mustahil direplikasi.
- [ ] **7. Ketiadaan Persetujuan Etik (Ethical Clearance)**:  
  Studi yang melibatkan subjek manusia, pasien, atau data sensitif tidak menyertakan pernyataan persetujuan komite etik resmi (IRB Approval).
