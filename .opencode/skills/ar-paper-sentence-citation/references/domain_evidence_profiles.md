# Profil Bukti Ilmiah Berbasis Domain (Domain Evidence Profiles)

> **Bersifat Pedoman / Penyesuaian Inklusi.** Profil bukti domain menentukan tipe bukti apa yang *diterima* (*admitted*) saat penyaringan literatur ilmiah. Profil ini tidak mengubah nilai keseluruhan naskah, melainkan menyesuaikan jenis literatur yang sah menurut norma disiplin ilmu terkait.

---

## 1. Profil Bukti Domain Standar

Terdapat 4 profil domain utama (dengan `unknown_user_defined` sebagai profil netral bawaan):

| Profil Domain | Jenis Bukti Standar yang Diterima | Persyaratan Pembuktian (*Provenance*) | Titik Kritis yang Wajib Diawasi | Keterangan |
|:---|:---|:---|:---|:---|
| **`general_social_science`** | Studi empiris *peer-reviewed*, metode campuran (*mixed-methods*), laporan panel ahli, analisis kebijakan berbasis konteks. | Jurnal terindeks atau prosiding; laporan panel ahli dapat diterima bila relevan dengan konteks. | Generalisasi berlebih dari satu konteks; validitas eksternal yang lemah. | Siap pakai (Peleburan resmi: kajian Kebijakan Publik / *Policy* sepenuhnya masuk ke profil ini). |
| **`cs_ml`** | Artikel jurnal, prosiding konferensi bereputasi tinggi (IEEE, ACM, NeurIPS, CVPR), naskah pra-cetak arsip resmi (arXiv), laporan teknis industri terkemuka. | Repositori pra-cetak atau prosiding konferensi; siklus peer-review jurnal formal sering kali tertinggal dari inovasi lapangan. | Hasil yang tidak dapat direproduksi (*non-reproducible*); pemilihan tolok ukur yang bias (*benchmark cherry-picking*). | Siap pakai |
| **`humanities_interpretive`** | Sumber primer (*primary sources*), bahan arsip sejarah, teks kanonikal/klasik, monograf akademik penerbit universitas. | Autentisitas sumber primer; aturan kebaruan (3–5 tahun) **bukan** penentu mutu utama dalam epistemologi humaniora. | Interpretasi yang melampaui bukti teks (*interpretive over-reach*); minimnya pijakan pada sumber primer. | Siap pakai |
| **`unknown_user_defined`** | Piramida bukti netral standar — memprioritaskan artikel jurnal yang melalui *peer-review* formal konvensional. | Ekspektasi *peer-review* baku (Scopus / Web of Science). | Tidak ada pelonggaran khusus domain. | Profil netral bawaan |

---

## 2. Profil Cadangan (Reserved Profiles)

Profil-profil berikut dipetakan ke profil netral `unknown_user_defined` dengan panduan disiplin khusus:
- **`clinical`** (Medis & Kesehatan): Berorientasi pada Tradisi *Evidence-Based Medicine* (EBM). Standar emas: Tingkat I–II (RCTs, Meta-analisis). Naskah pra-cetak klinis dibatasi ketat untuk mencegah misinformasi protokol medis.
- **`education`** (Pendidikan): Berorientasi pada penelitian kuasi-eksperimental (Tingkat III–IV). Pengacakan murni (*randomization*) sering kali tidak praktis di lingkungan kelas nyata.
- **`wet_lab`** & **`materials_physics`**: Memerlukan data eksperimen laboratorium terkalibrasi dan kepatuhan terhadap standar bahan/metrologi.
- **`legal_case_based`**: Berorientasi pada yurisprudensi putusan pengadilan dan teks peraturan perundang-undangan primer.

---

## 3. Prinsip Inklusi Monotonik (*Monotonic Admit-Only Rule*)

Penyesuaian gerbang penyaringan literatur berdasarkan profil domain bersifat **aditif (hanya melonggarkan penerimaan jenis bukti yang sah)**:
- Profil domain dapat **menerima tipe bukti yang biasanya dikecualikan oleh aturan netral** (misalnya: memperbolehkan arXiv pada profil `cs_ml`, atau memperbolehkan teks klasik abad ke-19 pada profil `humanities_interpretive`).
- Profil domain **DILARANG KERAS** mengecualikan, menurunkan nilai, atau menggagalkan sumber yang sudah sah diterima oleh kriteria netral.
- **Tiga Gerbang Mutlak Universal** yang **TIDAK BOLEH** dilonggarkan oleh profil apa pun:
  1. *Relevansi*: Abstrak rujukan wajib menjawab pertanyaan penelitian.
  2. *Metodologi*: Tidak memiliki cacat logika atau kecacatan desain yang fatal.
  3. *Integritas*: Bukan publikasi predator dan bukan referensi palsu/halusinasi.

---

## 4. Catatan Batas Arsitektur (#246 Forward Reference)

Profil domain ini bertindak murni pada gerbang penerimaan bukti (*admissibility gate*) saat menyeleksi literatur. Penilaian agregasi nilai keseluruhan (A–F) untuk naskah tetap mengacu pada tabel acuan umum di `source_quality_hierarchy.md` hingga modul agregasi nilai relatif disiplin diimplementasikan secara terpisah.
