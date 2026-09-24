---
name: ar-paper-outline
description: "Aktifkan ketika pengguna meminta untuk membuat, merancang, atau menyempurnakan outline naskah paper akademik yang mendalam, menyusun peta bukti (evidence map), atau merencanakan struktur artikel penelitian atau manuskrip jurnal hingga tingkat paragraf. Mencakup cetak biru komprehensif per paragraf (tujuan paragraf, poin naratif, target jumlah kata, penugasan bukti/sitasi, dan kalimat transisi), aturan penulisan global, batasan klaim (klaim yang diizinkan dan batasan negatif), perencanaan persamaan matematika, serta spesifikasi tata letak master visual/tabel pada seluruh model akademik kanonikal (IMRaD, Thematic Literature Review, Theoretical Analysis, Case Study, Policy Brief, Conference Paper). Kata kunci pemicu: paper outline, buat outline paper, outline naskah, rancang struktur paper, kerangka paper, outline per paragraf, evidence map, academic outline, paper blueprint. JANGAN aktifkan untuk penulisan draf naskah lengkap (gunakan ar-paper-draft), simulasi peer-review, pemformatan sitasi, atau penulisan umum non-akademik."
license: MIT
metadata:
  author: Rafy
---

# Pembuatan Outline Paper Akademik (Cetak Biru Tingkat Paragraf)

## Gambaran Umum (Overview)

Skill ini menghasilkan cetak biru (*blueprint*) naskah akademik berbutir halus (*granular*) dan siap publikasi. Alih-alih berhenti pada judul sub-bab yang dangkal, skill ini membangun **arsitektur paragraf demi paragraf**: menetapkan tujuan retoris yang presisi, progresi naratif, jangkar bukti yang ditugaskan, target jumlah kata numerik, dan kalimat transisi untuk setiap paragraf individual. Skill ini juga mengodifikasikan batasan klaim global (*allowed vs. disallowed claims*) serta urutan tata letak master (*master layout sequence*) untuk persamaan matematika, gambar, dan tabel sebelum penulisan draf naskah lengkap dimulai.

## Kapan Mengaktifkan Skill Ini

- Pengguna meminta outline terperinci, cetak biru (*blueprint*), atau rencana arsitektural untuk paper akademik, manuskrip jurnal, bab tesis/disertasi, atau makalah konferensi.
- Pengguna meminta outline dengan detail tingkat paragraf, alur naratif, atau pemetaan bukti (*evidence mapping*).
- Pengguna menyebutkan kata kunci pemicu: `paper outline`, `buat outline paper`, `outline naskah`, `rancang struktur paper`, `kerangka paper`, `outline per paragraf`, `evidence map`, `academic outline`, `paper blueprint`.
- Pengguna menyediakan pertanyaan penelitian (*research questions*), hasil empiris, atau basis literatur dan memerlukan struktur bab dan paragraf yang ketat sebelum penulisan draf.

## Kapan TIDAK Mengaktifkan Skill Ini

- Penulisan prosa naskah lengkap atau menulis bab akhir (gunakan skill penulisan draf seperti `ar-paper-draft`).
- Simulasi peer review, penilaian reviewer, atau keputusan editorial (gunakan skill reviewer seperti `ar-paper-reviewer`).
- Curah gagasan (*brainstorming*) terbuka tanpa luaran struktural yang konkret.
- Penulisan non-akademik (artikel blog, esai umum, materi pemasaran).
- Pembuatan perayap kode (*code crawler*), skrip ekstraksi data, atau tugas pengembangan perangkat lunak.

## Ruang Lingkup (Scope)

- **Dalam Lingkup:** 4 lapisan cetak biru (Meta-konfigurasi, Batasan Klaim Global & Aturan Penulisan, Spesifikasi Paragraf demi Paragraf, Pemetaan Bukti & Kesenjangan Bukti), 6 model struktural kanonikal, perencanaan tata letak visual/tabel, perencanaan notasi matematika.
- **Luar Lingkup:** Penulisan prosa naskah lengkap, kueri API eksternal langsung, kompilasi LaTeX, eksekusi submisi jurnal.

---

## Langkah Wajib 0: Klarifikasi & Intake Pengguna

> [!IMPORTANT]
> **JANGAN berasumsi atau menetapkan venue atau target jurnal tertentu (seperti IEEE Access, Elsevier, dll.) tanpa berkonsultasi dengan pengguna.**
> Jika pengguna belum secara eksplisit menentukan detail publikasi di awal, AI **wajib mengonfirmasi atau menanyakan** parameter berikut sebelum menyusun outline:
> 1. **Target Publikasi / Venue**: Apakah ditujukan untuk jurnal internasional bereputasi (IEEE, Elsevier, Springer, Nature, ACM), jurnal nasional terakreditasi, prosiding konferensi, atau bab tesis/disertasi?
> 2. **Gaya & Format Sitasi**: Gaya sitasi apa yang diwajibkan oleh panduan penulis (*author guidelines*) (IEEE numerik, APA 7 nama-tahun, Harvard, ACM, Vancouver, Chicago)?
> 3. **Bahasa Naskah & Kebijakan Terminologi**: Bahasa Inggris formal, atau bahasa lain dengan istilah teknis standar?
> 4. **Model Struktural & Target Jumlah Kata**: Model mana yang paling sesuai (IMRaD, Thematic Literature Review, Theoretical Analysis, Case Study, Policy Brief, Conference Paper), dan berapa target jumlah kata total (misalnya, 5.000–8.000 kata)?
> 5. **Fokus Utama & Materi yang Tersedia**: Apa Pertanyaan Penelitian (*Research Questions* / RQs) atau Hipotesis utama, dan temuan empiris atau sumber literatur apa saja yang telah tersedia?

---

## 4 Lapisan Cetak Biru (The 4 Blueprint Layers)

Setiap outline mendalam wajib menetapkan empat lapisan operasional:

### Lapisan 1: Halaman Depan & Meta-Konfigurasi
- **Target Publikasi & Venue**: Ditetapkan berdasarkan hasil intake pengguna.
- **Bahasa & Register Naskah**: Nada akademik formal dan kebijakan standardisasi istilah teknis.
- **Format Sitasi**: IEEE, APA 7, Harvard, ACM, dll., sesuai konfirmasi pengguna.
- **Judul & Penulis**: Judul kerja (*working title*) dan afiliasi penulis.
- **Cetak Biru Abstrak Terstruktur**: 150–250 kata mengikuti 5 pergerakan retoris: *Konteks/Latar Belakang → Masalah/Tujuan → Metode yang Diusulkan → Temuan Empiris Utama → Kesimpulan/Implikasi*.
- **Kata Kunci (*Keywords*)**: 5–7 istilah terindeks.

### Lapisan 2: Aturan Penulisan Global & Batasan Klaim
1. **Klaim yang Diizinkan & Fokus Inti (*Allowed Claims & Core Focus*)**: Pernyataan faktual yang presisi mendefinisikan temuan empiris utama, metrik kuantitatif, dan kontribusi arsitektural yang diizinkan untuk diklaim.
2. **Batasan Negatif & Klaim yang Dilarang (*Negative Constraints & Disallowed Claims*)**: Batasan ketat yang merinci apa yang **TIDAK** boleh diklaim oleh naskah (misalnya, tidak membuat klaim keunggulan universal tanpa bukti, tidak menyatakan klaim absolut nol-bias, tidak membuat klaim kausalitas yang belum terbukti, tidak mengklaim di luar dataset yang dievaluasi).
3. **Urutan Elemen Master (*Master Element Sequence*)**: Registri kronologis seluruh Persamaan (Eq. 1..N), Gambar (Fig. 1..N), dan Tabel (Table I..N) disertai spesifikasi tata letak LaTeX (misalnya, bentang lebar penuh dua kolom `\begin{table*} ... \end{table*}` vs. satu kolom).
4. **Batasan Stilistika & Leksikal**:
   - Larangan superlatif kosong ("revolutionary", "game-changing", "state-of-the-art" kecuali telah diuji secara terukur terhadap metode pembanding/baseline).
   - Larangan penggunaan kata "significantly" / "secara signifikan" kecuali disertai uji hipotesis statistik formal ($p < 0.05$).
   - Batas densitas sitasi: maksimal 3 sitasi per kalimat untuk mencegah penumpukan sitasi (*citation dumping*).
   - Standardisasi akronim teknis: tulis kepanjangan lengkap disertai singkatan pada penyebutan pertama.

### Lapisan 3: Cetak Biru Paragraf demi Paragraf
Untuk **setiap paragraf individual** di seluruh bab naskah, sediakan cetak biru khusus:

```markdown
### Paragraf X: [Sub-Tema Deskriptif / Fungsi]
- **Target Jumlah Kata**: [misal, 110–150 kata]
- **Tujuan (Objective)**: 1 kalimat lugas yang mendefinisikan fungsi retoris atau ilmiah dari paragraf ini.
- **Poin-Poin Naratif**:
  1. [Kalimat topik / Pernyataan inti]
  2. [Elaborasi teknis atau empiris, mekanisme, atau bukti komparatif]
  3. [Konteks pendukung, batasan kendala, atau temuan sekunder]
- **Penugasan Bukti & Sitasi**: Referensi literatur eksplisit (Penulis, Tahun / Judul), tabel eksperimen, atau nomor persamaan yang mendasari paragraf ini.
- **Kalimat Transisi / Jembatan**: Draf kalimat penutup yang menghubungkan secara logis ke paragraf berikutnya.
```

### Lapisan 4: Elemen Visual, Persamaan, dan Manajemen Kesenjangan Bukti
- **Rencana Persamaan**: Formulasi matematis bernomor urut kronologis dengan definisi variabel yang ketat.
- **Rencana Visual & Tabel**: Judul, takarir (*caption*), skema kolom, dan paragraf perujuk eksplisit.
- **Penandaan Kesenjangan Bukti (*Material Gap Tagging*)**: Bagian yang belum memiliki bukti empiris atau literatur pendukung wajib ditandai secara eksplisit: `[MATERIAL GAP: deskripsi data/sitasi yang dibutuhkan]`. Jangan pernah mengarang sitasi fiktif atau menyembunyikan defisit data empiris.

---

## Model Struktur Kanonikal

Pilih arsitektur yang sesuai dengan desain penelitian:
1. **IMRaD (Pola 1A: Hasil dan Pembahasan Terintegrasi / Pola 1B: Pemisahan Klasik)**: Standar untuk penelitian empiris di bidang teknik/rekayasa, ilmu komputer, sains alam, dan ilmu sosial.
2. **Thematic Literature Review**: Untuk tinjauan sistematis, meta-sintesis, dan tinjauan cakupan (*scoping review*).
3. **Theoretical Analysis**: Untuk pembuktian matematis, derivasi konseptual, dan kritik teoretis.
4. **Case Study**: Untuk investigasi organisasi atau kualitatif studi kasus tunggal/multikasus.
5. **Policy Brief**: Untuk rekomendasi berbasis bukti yang ditujukan kepada para pengambil keputusan.
6. **Conference Paper**: Untuk makalah ringkas dengan keterbatasan ruang halaman (4–8 halaman).

*Lihat `references/structure-patterns.md` untuk perincian bab lengkap dan tabel alokasi kata.*

---

## Contoh Cetak Biru & Berkas Referensi

Rujuk berkas-berkas referensi berikut untuk implementasi lengkap dan templat:

- **[`references/sample-paragraph-outline.md`](references/sample-paragraph-outline.md)**: Contoh ilustratif peniruan (*mock exemplar*) yang mendemonstrasikan siklus hidup cetak biru secara utuh, mulai dari intake pengguna, batasan klaim, tata letak elemen master, hingga cetak biru **paragraf demi paragraf (Paragraf 1..N)** dari Bagian I hingga Bagian V. Catatan: Ini murni referensi percontohan dan tidak boleh disalin mentah-mentah (*verbatim*).
- **[`references/structure-patterns.md`](references/structure-patterns.md)**: Spesifikasi dan persentase distribusi jumlah kata untuk seluruh 6 model struktur kanonikal.
- **[`references/evidence-mapping.md`](references/evidence-mapping.md)**: Panduan kerangka *Claim-Evidence-Reasoning* (CER) dan protokol pelacakan `[MATERIAL GAP]`.

---

## Hal yang Harus dan Jangan Dilakukan (Do and Don't)

| Hal yang Harus Dilakukan (Do) | Hal yang Jangan Dilakukan (Don't) |
|---|---|
| Tanyakan kepada pengguna target venue, gaya sitasi, dan bahasa sebelum menyusun outline | Mengasumsikan atau memaksakan venue tertentu (misalnya, IEEE Access) tanpa konfirmasi pengguna |
| Dekomposisikan setiap bab hingga ke cetak biru paragraf yang granular (jumlah kata, tujuan, poin naratif, transisi) | Berhenti pada ringkasan bab/sub-judul tanpa spesifikasi tingkat paragraf |
| Definisikan Klaim yang Diizinkan (*Allowed Claims*) dan Batasan Negatif (*Negative Constraints*) secara eksplisit sebelum penyusunan draf | Membiarkan klaim tanpa bukti, hiperbola, atau spekulasi masuk ke dalam outline |
| Susun kalimat transisi yang jelas dan mengalir untuk setiap paragraf | Menyajikan poin-poin terisolasi tanpa progresi naratif yang kohesif |
| Rencanakan urutan kronologis Tabel, Gambar, dan Persamaan secara terpusat sejak awal | Menyisipkan tabel dan gambar secara acak tanpa perencanaan tata letak |
| Tandai data empiris atau sitasi yang belum tersedia dengan label `[MATERIAL GAP]` | Mengarang sitasi fiktif, mereka-reka hasil penelitian, atau menutupi kekurangan bukti |
