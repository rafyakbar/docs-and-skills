# Panduan Rangka Surat Tanggapan (*Response Letter Skeleton Guide*)

Dokumen ini menjelaskan struktur, standar etika diplomasi akademik, dan arsitektur formal dokumen **Response to Reviewers** (surat sanggahan / tanggapan bebestari) yang disiapkan oleh skill `ar-paper-revision-coach`.

---

## 1. Arsitektur Tiga Tingkat (Pola R $\to$ A $\to$ C)

Setiap butir komentar reviewer dalam surat tanggapan wajib disusun mengikuti struktur tiga tingkat:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. REVIEWER COMMENT (R)                                     │
│    Kutipan utuh (verbatim) dari teks asli ulasan reviewer.  │
├─────────────────────────────────────────────────────────────┤
│ 2. AUTHOR RESPONSE (A)                                      │
│    Jawaban argumentatif penulis: apresiasi masukan, logika  │
│    penyelesaian, atau penjelasan pembelaan metodologis.     │
├─────────────────────────────────────────────────────────────┤
│ 3. CHANGES MADE (C)                                         │
│    Tindakan nyata pada naskah: nomor bab, nomor halaman,    │
│    nomor baris, dan kutipan teks baru yang ditambahkan.     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Prinsip Diplomasi Akademik & Anti-Defensif

### 1. *Polite but Principled* (Santun namun Berprinsip)
- Ucapkan terima kasih atas ketelitian penelaah (*"We thank the reviewer for raising this critical point"*).
- Jangan gunakan register bahasa defensif (*"The reviewer failed to understand"*, *"As we already stated"*).
- Ubah kalimat konfrontatif menjadi klarifikasi saintifik (*"We recognize that our original phrasing may have been ambiguous. To clarify this distinction, we have revised Section 3.2 as follows..."*).

### 2. *Independence of Tone and Severity* (#574 B1)
- Pujian berlebihan (*sycophancy*) tidak dapat menggantikan bukti empiris.
- Nada reviewer yang ketus atau skeptis tidak boleh dibalas dengan emosi, melainkan dengan bukti angka, interval kepercayaan 95%, dan sitasi literatur yang kokoh.

### 3. Penanganan Komentar Apresiatif (*Strengths / Positive Feedback*)
- Sesuai kaidah #574 A1, jika reviewer memberikan pujian atas aspek tertentu (misal: desain eksperimen atau visualisasi), akui secara ringkas pada bagian awal respons reviewer terkait.
- **JANGAN MENGARANG PUJIAN**: Jika review tidak memiliki kalimat pujian (ulasan murni berisi daftar kelemahan), lewati blok apresiasi tanpa menciptakan pujian palsu.

---

## 3. Struktur Dokumen Resmi Surat Tanggapan

Dokumen `10_response_letter_skeleton.md` disusun dalam 4 bagian kanonikal:

### Bagian I: Halaman Judul & Informasi Meta
- Judul Paper (*Manuscript Title*).
- Nomor Naskah (*Manuscript Tracking ID*).
- Nama Jurnal Target (*Target Journal*).
- Tanggal Penyerahan Revisi (*Revision Date*).

### Bagian II: Pernyataan Pembuka (*Opening Statement to EIC*)
- Ucapan terima kasih resmi kepada Editor-in-Chief dan seluruh penilai atas waktu dan evaluasi mendalam.
- Ringkasan eksekutif perubahan utama yang dilakukan pada naskah (300–500 kata).
- Penegasan bahwa seluruh masukan bebestari telah diakomodasi secara komprehensif.

### Bagian III: Tanggapan Khusus kepada Editor (EIC Comments)
- Menjawab setiap instruksi spesifik dari editor (misal: pemangkasan jumlah kata, kepatuhan template, atau resolusi isu *blocking* yang disorot editor).

### Bagian IV: Tanggapan Poin-demi-Poin kepada Reviewer
Dikelompokkan per penilai:
- `Reviewer 1 (Metodologi)`
- `Reviewer 2 (Domain Pakar)`
- `Reviewer 3 (Perspektif Silang)`
- `Devil's Advocate (Penantang Adversarial)`

---

## 4. Format Kutipan Perubahan Teks (Changes Made)

Untuk memudahkan penelaah memverifikasi perbaikan naskah, format bagian `Changes Made` wajib menyertakan rujukan silang presisi:

```markdown
**Changes Made**:
- **Lokasi Naskah**: Bab 3 Metodologi (`03_methodology.md`), Sub-bab 3.2, Halaman 6, Baris 142–158.
- **Teks yang Ditambahkan**:
  > *"To ensure robustness against scanner variability across multi-vendor hospital settings, we incorporated an additional external evaluation on 40 cohort scans from the CQ500 benchmark (Siemens Somatom Definition Flash). As reported in Table 4, the model maintained an AUROC of 0.928 [95% CI: 0.891–0.965], demonstrating cross-scanner generalization."*
```

---

## 5. Hubungan dengan Skill Downstream (`ar-rebuttal-audit`)

Rangka surat tanggapan yang dihasilkan oleh `ar-paper-revision-coach` akan dilengkapi teks responsnya pada Fase 22 (`ar-revision`), kemudian diaudit kualitasnya oleh `ar-rebuttal-audit` (Fase 23) untuk memastikan:
- Tidak ada komentar reviewer yang terlewat (*Zero-Orphan Check*).
- Setiap kalimat *"We have revised the text"* benar-benar memiliki lokasi halaman dan baris yang valid.
- Tidak ada bahasa yang bernada defensif atau berdebat tanpa dasar data.
