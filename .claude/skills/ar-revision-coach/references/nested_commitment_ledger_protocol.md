# Protokol Nested Commitment Ledger (Schema 11 & Kong et al. 2026 / #268)

Dokumen ini mendefinisikan spesifikasi teknis Kontrak **Schema 11 R&R Traceability Matrix** dan struktur **Nested Commitment Ledger** berdasarkan temuan empiris Kong et al. 2026 §7.4.3 serta perbaikan arsitektur #268.

---

## 1. Landasan Masalah: Commitment-Fulfillment Gap (Kong et al. 2026)

Dalam publikasi ilmiah internasional, analisis terhadap proses peer review ICLR 2025 [21] oleh Kong et al. 2026 membuktikan adanya **kesenjangan komitmen-pemenuhan (*commitment-fulfillment gap*)**:
- Penulis sering kali menulis surat tanggapan (*rebuttal / response letter*) dengan bahasa persuasif yang sangat meyakinkan dan memberi tanda *"Verified: Yes"*.
- Namun pada kenyataannya, eksperimen yang dijanjikan tidak pernah dijalankan, tabel baru tidak pernah dimasukkan ke naskah revisi, atau klaim perbaikan hanya berupa klarifikasi retoris tanpa bukti empiris.

### Solusi Arsitektur
Schema 11 memaksakan **ketertelusuran tingkat janji (*per-promise lifecycle traceability*)**:
Setiap komentar reviewer diurai menjadi objek komitmen independen. Pemenuhan janji diverifikasi langsung pada artefak naskah nyata berdasarkan tipe bukti yang disyaratkan, bukan sekadar mempercayai klaim penulis.

---

## 2. Invarian Bentuk Bersarang (#268 Nested-Object Shape)

### Perbedaan Bentuk Lama (Parallel Lists) vs Bentuk Baru (Nested Objects)

```
❌ BENTUK LAMA (Parallel-List Anti-Pattern):
Row: R1-1
commitment_extracted: ["add ablation", "clarify choice"]
fulfillment_status:   ["fulfilled", "partial"]
unfulfilled_rationale: ["", "3 seeds only"]
=> Rentan desinkronisasi indeks jika ada elemen terlewat!

✅ BENTUK BARU (#268 Nested-Object Shape):
- concern_id: R1-1
  commitment_extracted:
    - commitment_text: "add ablation"
      commitment_type: add_experiment
      required_evidence_type: new_table
      fulfillment_status: fulfilled
      # unfulfilled_rationale dihilangkan total (tanpa placeholder "")
    - commitment_text: "clarify choice"
      commitment_type: add_clarification
      required_evidence_type: discussion_paragraph
      fulfillment_status: partial
      unfulfilled_rationale: "3 seeds only due to compute budget"
```

### Invarian Kunci #268:
1. **N1**: Setiap entri di dalam `commitment_extracted[]` adalah sebuah *mapping* objek yang membawa 3 field ekstraksi wajib:
   - `commitment_text`
   - `commitment_type`
   - `required_evidence_type`
2. **N2**: Dilarang menggunakan list paralel tingkat atas (`expected_fulfillment_status` atau `expected_unfulfilled_rationale`).
3. **N3**: `fulfillment_status` (jika terisi) harus berada dalam enum valid. `unfulfilled_rationale` **WAJIB DIHILANGKAN** (*omitted*) jika statusnya `fulfilled` (dilarang menggunakan placeholder string kosong `""`). `unfulfilled_rationale` **WAJIB BERISI TEKS NON-KOSONG** jika statusnya selain `fulfilled`.
4. **N4 & N5**: Dilarang menyisakan notasi indeks usang seperti `fulfillment_status[i]` atau `unfulfilled_rationale[i]` pada dokumentasi atau teks naskah.

---

## 3. Enam Tipe Komitmen (`commitment_type`)

Setiap janji perbaikan diklasifikasikan ke dalam 6 tipe diskrit:

| Tipe Komitmen | Definisi Operasional | Contoh Masukan Reviewer |
| :--- | :--- | :--- |
| **`add_experiment`** | Menjalankan eksperimen komputasi baru, ablasi model, atau evaluasi dataset baru. | *"Please run an ablation study comparing Cross-Attention ViT vs Standard ViT."* |
| **`add_analysis`** | Melakukan analisis data tambahan dari hasil eksperimen yang sudah ada (uji statistik, CI, korelasi). | *"Report 95% confidence intervals and p-values using DeLong test."* |
| **`add_clarification`** | Memperjelas motivasi teoretis, alasan pemilihan hiperparameter, atau nuansa interpretasi. | *"Clarify why a 5-fold cross-validation was chosen instead of 10-fold."* |
| **`add_citation`** | Merujuk dan membandingkan literatur penting yang terlewat oleh penulis. | *"Discuss the recent benchmark by Patel et al. (2025)."* |
| **`restructure`** | Menata ulang urutan bab, memindahkan sub-bab, atau membagi pembahasan yang terlalu padat. | *"Reorganize Section 3 so data preprocessing precedes model architecture."* |
| **`other`** | Perbaikan tipografi, formatting persamaan matematika, kosmetik tata bahasa (*copy-edit*). | *"Correct the typo in Equation 2 and reformat Table 3 footnotes."* |

---

## 4. Sembilan Tipe Bukti yang Disyaratkan (`required_evidence_type`)

Tipe bukti menentukan di mana verifikator mencari bukti pemenuhan komitmen:

### A. Tujuh Bukti Naskah (*Manuscript Evidence*)
Bukti diverifikasi secara fisik pada naskah revisi (`revision_location`):
1. **`new_section`**: Sub-bab atau bab baru yang dibuat khusus untuk menjawab masukan (misal: Bab 2.3 Teori Pembanding).
2. **`new_figure`**: Diagram arsitektur, grafik ROC/PR, visualisasi Grad-CAM, atau diagram alir baru.
3. **`new_table`**: Tabel metrik eksperimen tambahan, tabel ablasi, atau tabel komparasi SOTA baru.
4. **`new_citation`**: Sitasi literatur baru di badan teks naskah dan daftar pustaka `06_references.md`.
5. **`methods_paragraph`**: Paragraf penjelasan tambahan yang disisipkan ke bab Metodologi (`03_methodology.md`).
6. **`discussion_paragraph`**: Paragraf analisis komparatif atau batas studi yang disisipkan ke bab Pembahasan (`05_discussion.md`).
7. **`prose_edit`**: Perbaikan teks granular tingkat kalimat atau frasa (koreksi tipo, penyesuaian istilah, notasi rumus).

### B. Satu Bukti Surat Tanggapan (*Response Letter Evidence*)
8. **`acknowledgment_only`**: Komitmen dipenuhi secara eksklusif pada dokumen surat tanggapan (*Response to Reviewers*) tanpa mengubah teks naskah (contoh: mengapresiasi komentar positif atau merangkum klarifikasi umum).

### C. Satu Pintu Darurat Terkelola (*Escape-Hatch*)
9. **`other`**: Digunakan hanya jika reviewer menyampaikan komentar yang sangat abstrak atau tidak spesifik lokasinya (contoh: *"The framing feels slightly incomplete"*). Menghasilkan peringatan peninjau (*advisory*) agar penulis menentukan lokasinya secara manual.

---

## 5. Empat Status Siklus Hidup (`fulfillment_status`)

Status ini diisi saat tahap revisi dieksekusi:

1. **`fulfilled`**:
   Komitmen telah dipenuhi sepenuhnya. Bukti nyata hadir di naskah dan secara substantif menjawab permintaan reviewer.
   *(Catatan: `unfulfilled_rationale` dilarang hadir pada status ini).*
2. **`partial`**:
   Komitmen dipenuhi sebagian (contoh: reviewer meminta 5 bibit acak, namun sumber daya komputasi lab hanya memungkinkan 3 bibit acak).
   *(Wajib menyertakan `unfulfilled_rationale` yang valid).*
3. **`not-fulfilled`**:
   Komitmen tidak dikerjakan sama sekali dalam naskah revisi ini.
   *(Wajib menyertakan `unfulfilled_rationale` yang menjelaskan alasannya).*
4. **`explicitly-rejected-with-rationale`**:
   Penulis secara sadar menolak permintaan reviewer atas dasar metodologis, teoretis, atau batasan etik yang sah.
   *(Wajib menyertakan `unfulfilled_rationale` berisi sanggahan saintifik dan sitasi).*

---

## 6. Tiga Format Rationale Valid (`unfulfilled_rationale`)

Jika sebuah komitmen berstatus selain `fulfilled`, penjelasannya harus mematuhi salah satu dari 3 format kanonikal:

1. **Format (a) Penunjuk Lokasi Lain (*Pointer*)**:
   > *"Analisis variasi scanner telah tercakup pada Tabel 4 dan dibahas di Bagian 5.2 Paragraf 3."*
2. **Format (b) Sanggahan Ilmiah (*Methodological Justification*)**:
   > *"Kami menolak penambahan SMOTE pada data tabular karena uji van den Goorbergh et al. (2022) membuktikan interpolasi sintetis merusak kalibrasi risiko klinis pada stroke."*
3. **Format (c) Pengakuan Batasan Studi (*Future Work Acknowledgment*)**:
   > *"Validasi prospektif multi-senter ditunda untuk penelitian mendatang karena keterbatasan protokol etik IRB retrospektif saat ini; limitasi ini diakui secara eksplisit pada Bagian 5.4."*

---

## 7. Deteksi COMMITMENT_GAP

Jika ditemukan sebuah komitmen dengan status `not-fulfilled` atau `partial` yang **tidak memiliki `unfulfilled_rationale`**:
Sistem verifikasi akan mengeluarkan peringatan keras:
```
[COMMITMENT_GAP] (R1-1): Komitmen "lakukan uji pada dataset eksternal" berstatus not-fulfilled
tanpa rationale. Penulis wajib menyertakan alasan penolakan, penunjuk lokasi lain, atau pengakuan
keterbatasan sebelum naskah dapat diserahkan kembali.
```
Mekanisme ini menjamin bahwa seluruh kesenjangan komitmen terdeteksi sebelum naskah masuk ke meja editor jurnal.
