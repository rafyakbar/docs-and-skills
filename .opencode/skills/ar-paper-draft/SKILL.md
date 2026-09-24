---
name: ar-paper-draft
description: "Aktifkan ketika pengguna meminta untuk menyusun draf, menulis, atau menghasilkan seksi atau subseksi naskah paper akademik tertentu (satu berkas per iterasi) berdasarkan outline paper. Mencakup penulisan draf seksi modular ke dalam berkas markdown terpisah (misalnya 01_introduction.md, 02_related-works.md, atau subseksi di bawah 03_materials-and-methods_*.md dan 04_results-and-discussion_*.md), eksekusi cetak biru paragraf, retorika pendahuluan CARS, penalaran CER empiris, pelacakan alokasi jumlah kata, dan standar mutu penulisan akademik anti-slop yang ketat. Secara tegas tidak mencakup penomoran referensi dan kompilasi referensi (ditangani pada langkah berikutnya), serta menyusun draf satu seksi dalam satu waktu. Kata kunci pemicu: draft paper, buat draft paper, tulis naskah, draft section, write introduction, write methodology, write discussion, draft manuscript, paper draft. JANGAN aktifkan untuk membuat outline (gunakan ar-paper-outline), pencarian/kompilasi sitasi, penomoran sitasi, evaluasi peer review, atau penulisan umum non-akademik."
license: MIT
metadata:
  author: Rafy
---

# Penulisan Draf Paper Akademik (Penyusunan Prosa Seksi per Seksi)

## Gambaran Umum (Overview)

Skill ini mentransformasikan cetak biru (*blueprint*) naskah akademik terstruktur (seperti yang dihasilkan oleh `ar-paper-outline`) menjadi prosa manuskrip berstandar publikasi jurnal bereputasi. Skill ini menerapkan **disiplin penulisan iteratif seksi per seksi**: menulis tepat **satu berkas modular dalam satu waktu** (misalnya `01_introduction.md` atau berkas subseksi spesifik). Proses penulisan mematuhi secara ketat tujuan paragraf, alur narasi, alokasi batas kata, serta standar mutu penulisan akademik yang ketat.

> [!IMPORTANT]
> **Larangan Penomoran Sitasi pada Langkah Ini**
> Pada Langkah 1 (Step 1), draf prosa disusun **tanpa penanda referensi numerik** (JANGAN menyisipkan `[1]`, `[[1]]`, atau tautan seperti `[[1]](06_references.md#ref1)`). Kurasi sitasi (`references.txt`), kompilasi daftar pustaka (`06_references.md`), dan penomoran sitasi dalam teks dieksekusi pada langkah-langkah berikutnya (Langkah 2, 3, dan 4). Setiap kalimat harus dirumuskan sebagai pernyataan ilmiah yang lugas, presisi, dan dapat diverifikasi, siap untuk dipetakan dalam kurasi sitasi per kalimat.

## Kapan Mengaktifkan Skill Ini

- Pengguna meminta untuk menulis, menyusun draf, atau menghasilkan seksi atau subseksi tertentu dari naskah paper akademik berdasarkan outline (misalnya `01_introduction.md`, `02_related-works.md`, `03_materials-and-methods_a-dataset.md`, dst.).
- Pengguna memanggil frasa pemicu: `draft paper`, `buat draft paper`, `tulis naskah`, `draft section`, `write introduction`, `write methodology`, `write discussion`, `draft manuscript`, `paper draft`.
- Pengguna memberikan outline naskah per paragraf dan meminta untuk menulis draf seksi berikutnya.

## Kapan TIDAK Mengaktifkan Skill Ini

- Menulis draf seluruh seksi secara serentak dalam satu perintah sekaligus (selalu tulis satu seksi per iterasi).
- Membuat, merencanakan, atau merancang outline naskah paper dari nol (gunakan `ar-paper-outline`).
- Mencari, mengurasi, atau memetakan sitasi literatur ke rekaman bibliografi (gunakan `ar-paper-sentence-citation` / Langkah 2).
- Mengompilasi naskah daftar pustaka (`06_references.md`) atau menyuntikkan nomor sitasi ke dalam teks draf (gunakan `ar-paper-reference-compiler` / Langkah 3 dan `ar-paper-citation-numbering` / Langkah 4).
- Menyintesis naskah abstrak atau kata kunci secara terisolasi (gunakan `ar-paper-abstract` / Langkah 5).
- Melakukan evaluasi kritik *peer review* atau penilaian skor penelaah (gunakan `ar-paper-reviewer`).
- Penulisan naskah umum non-akademik (artikel blog, dokumentasi teknis umum, materi promosi).

## Ruang Lingkup (Scope)

- **Dalam Lingkup:** Penulisan draf satu berkas seksi atau subseksi Markdown modular per permintaan, retorika Pendahuluan Swales CARS, interpretasi hasil Claim-Evidence-Reasoning (CER), presisi klaim tingkat kalimat, penautan relatif peta jalan (*roadmap*) antarseksi, pemantauan alokasi jumlah kata, dan kontrol leksikal anti-slop.
- **Luar Lingkup:** Menghasilkan seluruh manuskrip paper secara sekaligus, penomoran sitasi numerik (`[1]`, `[[1]]`), penyusunan daftar pustaka, eksekusi kompilasi LaTeX, atau otomasi penyerahan naskah (*submission*) ke jurnal.

---

## Langkah Wajib 0: Asupan & Verifikasi Ruang Lingkup

Sebelum mulai menulis prosa naskah, verifikasi parameter prasyarat berikut:

1. **Identifikasi Seksi Sasaran**: Konfirmasikan **satu berkas seksi atau subseksi tunggal** yang akan ditulis (misalnya `01_introduction.md` atau `03_materials-and-methods_b-[teknik].md`). **Jangan pernah mencoba menulis draf seluruh paper sekaligus.**
2. **Penyerapan Cetak Biru Paragraf**: Baca cetak biru paragraf yang telah disetujui untuk seksi spesifik tersebut (tujuan paragraf, poin narasi, target jumlah kata, dan klaim empiris yang ditugaskan).
3. **Kebijakan Tegas Tanpa Penomoran Sitasi**: Pastikan tidak ada penanda sitasi numerik yang dimasukkan ke dalam teks. Fokus pada perumusan pernyataan ilmiah yang kokoh dan berlandasan kuat.
4. **Materi Empiris & Figur**: Pastikan angka eksperimen, tabel, atau tahapan algoritmik yang diperlukan untuk seksi ini telah tersedia. Jangan pernah mengarang data fiktif (*hallucination*).
5. **Pemeriksaan Registri Akronim**: Baca `paper/acronyms.txt` (jika ada) untuk mengidentifikasi seluruh singkatan yang telah diperkenalkan sebelumnya, guna memastikan istilah yang sudah terdaftar tidak pernah diekspansi ulang dalam seksi ini.

---

## Arsitektur Berkas Modular

Setiap seksi atau subseksi ditulis ke dalam berkas Markdown tersendiri di bawah direktori kerja (misalnya `paper/`):

```text
paper/
├── 01_introduction.md                                      # Konteks, celah CARS, kontribusi, peta jalan naskah
├── 02_related-works.md                                     # Sintesis tematik literatur terdahulu
├── 03_materials-and-methods_0-overview.md                  # Alur kerja sistem & arsitektur global
├── 03_materials-and-methods_a-dataset.md                   # Karakteristik dataset & pra-pemrosesan
├── 03_materials-and-methods_b-[nama-metode].md             # Model matematis & ekstraksi fitur
├── 03_materials-and-methods_g-classification-pipeline.md   # Setup pelatihan & protokol anti kebocoran data
├── 03_materials-and-methods_h-evaluation-metrics.md        # Definisi metrik performa & validasi silang
├── 04_results-and-discussion_a-global-performance.md       # Evaluasi komparatif tolok ukur utama (benchmark)
├── 04_results-and-discussion_b-feature-ablation-study.md   # Eksperimen ablasi komponen/fitur
├── 04_results-and-discussion_c-subgroup-performance.md     # Analisis granular per subkelompok
├── 04_results-and-discussion_d-error-pattern-assessment.md # Diagnostik pola eror & kasus kegagalan
├── 04_results-and-discussion_e-comparison-with-prior-art.md# Penjajaran dengan tolok ukur literatur publikasi
├── 05_conclusion.md                                        # Sintesis, batasan metodologis, arah riset lanjutan
└── acronyms.txt                                            # Registri terpusat akronim & singkatan teknis
```

---

## Protokol Inti Penulisan Draf

### 1. Disiplin Penulisan Seksi Tunggal (*Single-Section Discipline*)
Tulis draf tepat **satu berkas modular dalam satu giliran kerja**. Curahkan kapasitas analitis sepenuhnya untuk menuntaskan seksi tersebut dengan standar akademik tertinggi, memenuhi seluruh target cetak biru paragraf sebelum menyerahkannya ke tahap tinjauan pengguna.

### 2. Perumusan Klaim Tingkat Kalimat (Fondasi Pra-Sitasi / *Pre-Citation Grounding*)
Konstruksikan setiap kalimat sebagai pernyataan mandiri yang dapat diverifikasi:
- Tulis klaim ilmiah substantif secara langsung di dalam teks tanpa menyertakan nomor berkurung siku (`[1]`, `[[1]]`).
- Pastikan setiap kalimat yang memuat klaim empiris atau teoretis eksternal terbatasi secara jelas sehingga pada Langkah 2 dapat dipetakan langsung ke entri `.bib` atau `.ris` yang sesuai di `references.txt`.
- Apabila suatu fakta empiris belum memiliki rujukan pasti dalam outline, berikan penanda celah `[GAP: butuh sumber]` alih-alih mengarang referensi atau menciptakan nomor sitasi fiktif.

### 3. Protokol Registri Akronim & Singkatan (`acronyms.txt`)
Seluruh singkatan teknis di seluruh berkas naskah modular dikendalikan oleh registri terpusat (`paper/acronyms.txt`):
- **Pemeriksaan Pra-Penulisan**: Periksa `paper/acronyms.txt` sebelum menulis untuk mengidentifikasi singkatan yang telah diperkenalkan pada berkas sebelumnya.
- **Bentuk Lengkap pada Kemunculan Pertama**: Pertama kali suatu akronim muncul di bagian mana pun dalam naskah, tuliskan bentuk panjang resminya diikuti singkatan dalam tanda kurung: contohnya `Vision Transformer (ViT)`, `Support Vector Machine (SVM)`, `Principal Component Analysis (PCA)`.
- **Hanya Bentuk Singkatan pada Kemunculan Berikutnya**: Pada seluruh kemunculan berikutnya di semua berkas, gunakan **hanya bentuk singkatannya** (`ViT`, `SVM`, `PCA`). **Jangan pernah mengulang ekspansi bentuk lengkap dari istilah yang telah terdaftar.**
- **Pencatatan Pasca-Penulisan**: Jika seksi yang baru ditulis memperkenalkan singkatan teknis baru, segera catatkan ke dalam `paper/acronyms.txt` dengan mencantumkan: nomor urut, akronim, bentuk lengkap, dan lokasi kemunculan pertama (misalnya `paper/00_abstract.md (Abstract)` atau `paper/01_introduction.md (P3)`).

### 4. Standar Retorika per Seksi
- **Pendahuluan (`01_` )**: Terapkan model tahapan CARS dari Swales:
  * Move 1: Membangun teritori riset (*establish territory* — klaim sentralitas bidang, sintesis literatur dasar).
  * Move 2: Menetapkan celah riset (*establish niche* — identifikasi celah teoretis/empiris spesifik; hindari klaim negatif mutlak yang tidak terverifikasi).
  * Move 3: Mengisi celah riset (*occupy niche* — pernyataan solusi/tujuan yang ringkas, daftar kontribusi ilmiah bernomor yang eksplisit, serta paragraf peta jalan yang menautkan seksi berikutnya melalui tautan Markdown, misal `Seksi [II](02_related-works.md)...`).
- **Kajian Terkait (`02_` )**: Susun sintesis berdasarkan tema atau paradigma metodologis, bukan daftar kronologis nama penulis. Bandingkan pendekatan terdahulu secara langsung dengan pendekatan yang diusulkan.
- **Materi dan Metode (`03_` )**: Sajikan transparansi prosedural yang komprehensif. Definisikan setiap simbol variabel matematis. Dokumentasikan protokol perlindungan kebocoran data (*data leakage safeguards*).
- **Hasil dan Pembahasan (`04_` )**: Terapkan kerangka kerja CER (Claim $\rightarrow$ Evidence $\rightarrow$ Reasoning $\rightarrow$ Qualification). Selalu rujuk figur/tabel secara spesifik sebelum menguraikan mekanisme analitisnya.
- **Kesimpulan (`05_` )**: Sajikan 4 pilar utama: pernyataan ulang pencapaian inti, sintesis temuan utama, batasan metodologis yang transparan, dan rekomendasi arah penelitian lanjutan yang konkret dan dapat ditindaklanjuti.

### 5. Standar Mutu Penulisan & Batasan Anti-Slop
- **Kata Klise AI yang Dilarang (*Banned AI Cliches*)**: Singkirkan kosakata populer buatan mesin (`delve`, `tapestry`, `pivotal`, `crucial`, `showcase`, `testament`, `multifaceted`, `plethora`, `groundbreaking`). Gunakan padanan akademik yang presisi (`investigate`, `interplay`, `critical`, `demonstrate`, `evidence`, `complex`).
- **Eliminasi Basa-Basi Pembuka (*Throat-Clearing*)**: Hapus frasa pembuka hampa (*"Penting untuk dicatat bahwa..."*, *"Dalam ranah..."*, *"Tak perlu dikatakan lagi bahwa..."*).
- **Batasan Tanda Baca**: Tanda pisah em dash / — ($\le 2$ per naskah paper); titik koma / ; ($\le 2$ per 1.000 kata).
- **Variasi Ritme Kalimat (*Burstiness*)**: Selang-selingkan kalimat pendek yang lugas (8–14 kata) dengan kalimat majemuk penjelas yang komprehensif (25–38 kata). Jangan menyusun 4 kalimat berturut-turut dengan panjang yang seragam.
- **Disiplin Pembatasan Derajat Kepastian (*Hedging*)**: Terapkan *hedging* pada interpretasi dan hipotesis (*"menyarankan"*, *"mengindikasikan"*, *"dapat merefleksikan"*), namun jangan gunakan *hedging* pada pengukuran empiris (*"mencapai 94,2%"*) atau prosedur metodologis baku (*"dievaluasi menggunakan"*).

---

## Panduan Boleh & Jangan (Do and Don't Guidelines)

| Boleh (Do) | Jangan (Don't) |
|:---|:---|
| Susun draf tepat satu berkas seksi atau subseksi per iterasi | Mencoba menghasilkan seluruh naskah atau banyak seksi sekaligus |
| Patuhi cetak biru paragraf yang disetujui dan alokasi batas kata | Menulis narasi bebas tanpa struktur yang melenceng dari blueprint |
| Tulis klaim yang jelas dan terpisah, siap untuk kurasi sitasi Langkah 2 | Menyisipkan nomor sitasi (`[1]`, `[[1]]`) sebelum waktunya |
| Sertakan tautan Markdown relatif antarseksi pada peta jalan naskah | Membiarkan referensi seksi naskah berupa teks polos tanpa tautan |
| Rumuskan celah riset yang terukur dan dapat dipertanggungjawabkan | Menggunakan klaim negatif mutlak (*"Belum pernah ada studi yang..."*) |
| Paparkan batasan metodologis nyata secara jujur pada kesimpulan | Mengklaim performa sempurna tanpa cela atau bebas bias sepenuhnya |
| Variasikan panjang kalimat untuk membentuk ritme akademik yang alami | Menghasilkan kalimat dengan panjang yang seragam dan monoton |
| Definisikan seluruh variabel matematis langsung di sekitar persamaan | Memunculkan simbol matematis mengambang tanpa definisi jelas |
| Konsultasikan `paper/acronyms.txt` sebelum menulis dan catat akronim baru | Mengekspansi ulang akronim terdaftar atau memakai singkatan tanpa definisi |

---

## Referensi Terkait (References)

Untuk panduan mendalam, tabel konsultasi, dan contoh penerapan, rujuk berkas berikut:
- `references/drafting-workflow.md`: Alur kerja penulisan seksi tunggal, arsitektur berkas, dan perumusan klaim pra-sitasi.
- `references/rhetorical-section-guides.md`: Panduan retorika mendalam untuk CARS Pendahuluan, Metode, CER Hasil & Pembahasan, serta Kesimpulan.
- `references/writing-quality-standards.md`: Kamus anti-slop lengkap, aturan tanda baca, profil burstiness kalimat, dan kaidah hedging.
- `references/sample-draft-section.md`: Contoh acuan ilustratif penulisan draf seksi modular tanpa nomor sitasi (`01_introduction.md`).
