---
name: ar-paper-abstract
description: "Aktifkan ketika pengguna meminta untuk menulis, membuat, menyempurnakan, atau menerjemahkan abstrak paper akademik, kata kunci (keywords), atau judul/halaman depan (front matter, umumnya untuk 00_abstract.md). Mencakup model retorika 5 komponen (Konteks/Masalah, Tujuan, Metodologi, Temuan Kuantitatif Utama, Implikasi/Signifikansi), pengenalan akronim pada kemunculan pertama dan registrasi ke paper/acronyms.txt, kurasi 5–7 kata kunci, pemformatan metadata penulis (ORCID, afiliasi, corresponding author), serta pembuatan abstrak dwibahasa (bilingual). Kata kunci pemicu: write abstract, buat abstrak, paper abstract, abstract and keywords, saripati, generate abstract, draft abstract, 00_abstract.md. JANGAN aktifkan untuk penulisan draf naskah lengkap (gunakan ar-paper-draft), perancangan outline (gunakan ar-paper-outline), kurasi sitasi (gunakan ar-paper-sentence-citation), atau peer review (gunakan ar-paper-reviewer)."
license: MIT
metadata:
  author: Rafy
---

# Penyusunan Abstrak & Halaman Depan Naskah Akademik (Academic Paper Abstract & Front Matter Generation)

## Gambaran Umum (Overview)

Skill ini menghasilkan abstrak akademik berstandar publikasi jurnal internasional, kurasi kata kunci, serta dokumen halaman depan master (*master front matter*, umumnya diformat sebagai `00_abstract.md`). Skill ini menerapkan **kerangka retorika 5 komponen** yang ketat (Konteks & Masalah $\rightarrow$ Tujuan & Solusi yang Diusulkan $\rightarrow$ Metodologi $\rightarrow$ Temuan Empiris Kuantitatif Utama $\rightarrow$ Kesimpulan & Dampak Ilmiah), menegakkan **registrasi akronim kemunculan pertama** ke dalam `paper/acronyms.txt`, mengurasi 5–7 kata kunci yang dioptimalkan untuk indeks pencarian, serta menyusun metadata penulis secara lengkap dengan tautan hiperlink ORCID aktif.

## Kapan Mengaktifkan Skill Ini (When to Activate)

- Pengguna meminta untuk menulis, menyusun draf, menghasilkan, atau menyempurnakan abstrak paper ilmiah, kata kunci, atau *front matter*.
- Pengguna meminta pembuatan atau pembaruan berkas `00_abstract.md`.
- Pengguna menggunakan frasa pemicu: `write abstract`, `buat abstrak`, `paper abstract`, `abstract and keywords`, `saripati`, `generate abstract`, `draft abstract`, `00_abstract.md`.
- Pengguna menyediakan temuan eksperimen atau draf naskah lengkap dan meminta untuk menyintesiskan abstrak.
- Pengguna meminta abstrak dwibahasa (*bilingual abstract*, misalnya Bahasa Indonesia + Bahasa Inggris).

## Kapan TIDAK Mengaktifkan Skill Ini (When NOT to Activate)

- Menulis bagian isi utama naskah (*body sections*) seperti Pendahuluan, Metodologi, atau Pembahasan (gunakan `ar-paper-draft`).
- Merancang kerangka naskah (*paper outline*) atau cetak biru paragraf (*paragraph blueprint*) dari awal (gunakan `ar-paper-outline`).
- Mencari, menelusuri, atau mengurasi sitasi dan entri BibTeX per kalimat klaim (gunakan `ar-paper-sentence-citation` / Step 2).
- Mengompilasi naskah daftar pustaka akhir atau menyuntikkan penomoran sitasi ke dalam teks naskah (gunakan `ar-paper-reference-compiler` / Step 3 dan `ar-paper-citation-numbering` / Step 4).
- Simulasi *peer review* atau penilaian kritik reviewer (gunakan `ar-paper-reviewer`).
- Ringkasan non-akademik atau ringkasan eksekutif untuk artikel blog umum.

## Ruang Lingkup (Scope)

- **Dalam Lingkup:** Penulisan abstrak padat siap publikasi (150–250 kata), struktur retorika 5 komponen, ekstraksi metrik numerik kuantitatif presisi, ekspansi akronim kemunculan pertama dan sinkronisasinya dengan `paper/acronyms.txt`, kurasi 5–7 kata kunci berfaset, pemformatan metadata penulis berhiperlink ORCID aktif, serta penyusunan pasangan abstrak dwibahasa.
- **Luar Lingkup:** Menyisipkan sitasi bibliografi ke dalam abstrak (dilarang keras dalam konvensi abstrak ilmiah), mengarang metrik eksperimen yang tidak terverifikasi, atau menulis bab isi naskah.

---

## Langkah Wajib 0: Verifikasi Input & Kalibrasi Konteks

Sebelum menyusun abstrak, lakukan verifikasi atau klarifikasi terhadap parameter-parameter berikut:

1. **Ketersediaan Materi Sumber**: Identifikasi berkas materi dasar naskah (misalnya draf bab `01_introduction.md` hingga `05_conclusion.md`, atau cetak biru outline dan tabel hasil empiris). Ekstraksi kontribusi inti dan metrik kuantitatif terbaik secara presisi.
2. **Batasan Kata & Format Target**: Periksa pedoman jurnal sasaran (paragraf tunggal padat tanpa subjudul berukuran 150–250 kata, abstrak terstruktur dengan label subjudul, atau abstrak konferensi yang diperluas/*extended abstract*).
3. **Kebijakan Bahasa**: Tentukan apakah abstrak disusun dalam format ekabahasa (misalnya Bahasa Inggris atau Bahasa Indonesia saja) atau dwibahasa (misalnya Bahasa Indonesia + Bahasa Inggris).
4. **Metadata Penulis & Afiliasi**: Konfirmasikan nama lengkap penulis, gelar akademik, pengenal unik ORCID, afiliasi departemen/fakultas/institusi, dan alamat email penulis korespondensi (*corresponding author*).

---

## Arsitektur Retorika 5 Komponen (The 5-Component Rhetorical Architecture)

Setiap naskah abstrak wajib menyintesiskan penelitian melalui lima gerakan retorika berurutan ke dalam satu paragraf yang kohesif:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Konteks & Masalah Penelitian (1–2 kalimat)               │
│ Nyatakan domain teknis dan hambatan/bottleneck spesifik     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Tujuan & Solusi yang Diusulkan (1–2 kalimat)             │
│ Umumkan model, kerangka kerja, atau tesis yang diajukan     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Metodologi & Pengaturan Eksperimen (1–2 kalimat)         │
│ Sebutkan kohort data, skema validasi, & pengklasifikasi     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Temuan Empiris Kuantitatif Utama (2–3 kalimat)           │
│ Laporkan metrik numerik presisi (Akurasi, F1, nilai-p)      │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Kesimpulan & Signifikansi Ilmiah (1 kalimat)             │
│ Sampaikan intisari utama dan dampak keilmuan yang lebih luas│
└─────────────────────────────────────────────────────────────┘
```

### Aturan Retorika Kritis:
- **Tanpa Sitasi**: Jangan pernah menyertakan braket sitasi literatur (`[1]`, `[2]`, atau format penulis-tahun).
- **Bukti Numerik Presisi**: Cantumkan metrik kuantitatif konkret untuk metode yang diajukan beserta *baseline* pembanding utama. Hindari pernyataan kualitatif samar seperti *"mencapai hasil yang menjanjikan"*.
- **Disiplin Kala Waktu (Tense)**: Gunakan *present tense* untuk latar belakang domain dan kebenaran umum; gunakan *past tense* untuk tindakan spesifik penelitian dan metrik yang diamati; gunakan *present tense* untuk kesimpulan signifikansi akhir.

---

## Protokol Akronim dalam Abstrak (`paper/acronyms.txt`)

Mengingat `00_abstract.md` sering dibaca secara terpisah dan posisinya mendahului bab isi naskah:

1. **Bentuk Lengkap pada Kemunculan Pertama (First-Mention Full Form)**: Setiap istilah teknis yang memiliki akronim resmi yang diperkenalkan dalam abstrak **wajib ditulis dalam bentuk lengkap diikuti singkatan dalam tanda kurung**:
   * *Contoh*: `Vision Transformer (ViT)`, `Support Vector Machine (SVM)`, `Grid Search Cross-Validation (GridSearchCV)`.
2. **Penyebutan Berikutnya dalam Abstrak**: Jika istilah diulang kembali dalam paragraf abstrak, gunakan hanya bentuk singkatannya.
3. **Pencatatan Segera ke `paper/acronyms.txt`**: Seluruh singkatan yang pertama kali diperkenalkan dalam `00_abstract.md` wajib dicatat pada bagian teratas registri sentral `paper/acronyms.txt` dengan lokasi pengenalan pertama ditandai sebagai `paper/00_abstract.md (Abstract)`:

```text
NO  | ACRONYM / ABBREVIATION | FULL FORM                        | FIRST INTRODUCTION LOCATION
----+------------------------+----------------------------------+-----------------------------------
1   | ViT                    | Vision Transformer               | paper/00_abstract.md (Abstract)
2   | RF                     | Random Forest                    | paper/00_abstract.md (Abstract)
3   | SVM                    | Support Vector Machine           | paper/00_abstract.md (Abstract)
```

> [!NOTE]
> Setelah terdaftar di sini, seluruh skill penulisan bab turunan (`ar-paper-draft`) wajib menggunakan **hanya bentuk singkatan (akronim)** pada bab isi tanpa perlu menguraikan kepanjangannya kembali.

---

## Heuristik Kurasi Kata Kunci (Keyword Curation Heuristics)

1. **Jumlah**: Tepat **5 hingga 7 kata kunci**, dipisahkan dengan tanda koma.
2. **Komplementaritas Judul (Title Complementarity)**: Jangan sekadar menduplikasi kata-kata pada judul naskah. Jika judul sudah memuat *"Multi-Domain Vision Transformer Fusion"*, pilihlah kata kunci yang merepresentasikan dimensi sekunder (misalnya *Algorithmic fairness*, *Intersectional demographic recognition*, *Latent representation learning*).
3. **Cakupan Faset (Facet Coverage)**: Pastikan kumpulan kata kunci mencakup domain masalah, mekanisme metodologi, arsitektur komputasi, dan fokus evaluasi.

---

## Metadata Penulis & Tata Letak Berkas Master (Author Metadata & Master File Layout)

Keluarkan berkas hasil akhir ke `paper/00_abstract.md` menggunakan tata letak standar berikut:

```markdown
# [Judul Lengkap Naskah / Full Manuscript Title]

## Authors & Affiliation

1. **[Nama Penulis 1, Gelar]** ([ORCID: 0000-000X-XXXX-XXXX](https://orcid.org/0000-000X-XXXX-XXXX))  
   Departemen Informatika, Fakultas Teknik, Universitas Negeri Surabaya, Surabaya 60231, Indonesia  
   Email Penulis Korespondensi: `penulis1@unesa.ac.id`

2. **[Nama Penulis 2, Gelar]** ([ORCID: 0009-000X-XXXX-XXXX](https://orcid.org/0009-000X-XXXX-XXXX))  
   Departemen Informatika, Fakultas Teknik, Universitas Negeri Surabaya, Surabaya 60231, Indonesia

---

## Abstract

[Paragraf abstrak padat 5 komponen, 150–250 kata, metrik numerik presisi, ekspansi akronim kemunculan pertama]

---

## Keywords

Kata Kunci 1, Kata Kunci 2, Kata Kunci 3, Kata Kunci 4, Kata Kunci 5.
```

---

## Panduan Do dan Don't (Do and Don't Guidelines)

| Do (Lakukan) | Don't (Hindari) |
|:---|:---|
| Laporkan metrik numerik presisi (Akurasi, F1, nilai-p) | Menggunakan klaim kualitatif yang samar (*"mencapai akurasi tinggi"*) |
| Uraikan kepanjangan akronim pada kemunculan pertama: `Bentuk Lengkap (AKRONIM)` | Menggunakan akronim gundul tanpa definisi di dalam abstrak |
| Catat seluruh akronim abstrak ke dalam `paper/acronyms.txt` | Lupa mendaftarkan akronim abstrak ke berkas registri sentral |
| Sediakan 5–7 kata kunci yang melengkapi judul naskah | Menduplikasi istilah judul kata-per-kata pada kata kunci |
| Jaga jumlah kata strictly dalam batasan publikasi (150–250 kata) | Menulis abstrak bertele-tele multi-halaman atau di bawah 100 kata |
| Format tautan ORCID sebagai tautan hiperlink Markdown aktif | Mengabaikan pengenal ORCID atau rincian afiliasi institusi |
| Larang secara mutlak sitasi bibliografi di dalam abstrak | Menyisipkan nomor braket sitasi (`[1]`, `[2]`) di dalam naskah abstrak |

---

## Referensi (References)

Untuk panduan mendalam, pola konsultasi, dan contoh berkas terperinci, rujuk berkas-berkas berikut:
- `references/abstract-rhetoric-patterns.md`: Rincian kerangka kerja 5 komponen, konvensi kala waktu (*tenses*), dan jenis format abstrak.
- `references/acronym-and-keyword-standards.md`: Invarian registri akronim, taksonomi kata kunci 5-tier, dan pemformatan metadata penulis.
- `references/sample-abstract-file.md`: Berkas teladan rujukan ilustratif untuk struktur lengkap dokumen `00_abstract.md`.
