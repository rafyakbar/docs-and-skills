# Panduan Penyusunan Surat Tanggapan Reviewer (Response to Reviewers Guide — Schema 8)

Surat Tanggapan Reviewer (*Point-by-Point Response to Reviewers Letter*) adalah dokumen formal yang menyertai naskah hasil revisi saat proses pengajuan ulang (*resubmission*) ke jurnal ilmiah atau saat bimbingan intensif dengan dosen pembimbing.

Berdasarkan **Schema 8**, dokumen ini menghubungkan setiap keberatan reviewer dengan tindakan nyata penulis dan bukti mekanis ID blok naskah hasil penyambungan patch.

---

## 1. Struktur Standar Surat Tanggapan

Surat tanggapan terdiri dari tiga bagian utama:
1. **Bagian Pembuka & Ikhtisar Global (*Overview & Summary Counters*)**:
   - Metadata naskah (Judul, ID Naskah, Putaran Revisi).
   - Surat pengantar kepada Editor dan Reviewer yang menyatakan apresiasi dan ringkasan perbaikan.
   - Ringkasan metrik kuantitatif: total catatan terselesaikan, batasan yang diakui, selisih kata (*word count delta*), dan referensi baru yang ditambahkan.
2. **Tanggapan Butir-per-Butir (*Point-by-Point Responses*)**:
   - Pengelompokan per Reviewer (Reviewer 1, Reviewer 2, Editor/Reviewer 3).
   - Format standar **R $\to$ A $\to$ C** (*Reviewer Comment $\to$ Author Response $\to$ Changes Made*).
3. **Bagian Penutup & Deklarasi**:
   - Pernyataan kesiapan melakukan penyesuaian lanjutan jika diperlukan.
   - Tanda tangan perwakilan penulis korespondensi (*Corresponding Author*).

---

## 2. Pola R $\to$ A $\to$ C (*Gold Standard Response Pattern*)

Setiap poin komentar wajib diuraikan menggunakan tiga elemen terstruktur:

### (R) Reviewer Comment (*Kutipan Komentar Asli*)
- Kutip komentar asli reviewer secara verbatim (kata per kata) tanpa diringkas atau diubah maknanya.
- Berikan penomoran yang jelas sesuai roadmap (misal: `### REV-001 (R1 — Major #1, must_fix)`).

### (A) Author Response (*Argumen & Penjelasan Penulis*)
- Awali dengan ucapan terima kasih yang tulus atas ketajaman evaluasi reviewer.
- Jelaskan penalaran ilmiah, metodologi baru, analisis tambahan, atau alasan teoretis yang mendasari revisi.
- Hindari nada defensif. Jika reviewer menunjukkan kelemahan nyata, akui dengan lugas dan jelaskan bagaimana kelemahan tersebut kini telah diatasi.

### (C) Changes Made (*Uraian Perubahan Spesifik & Lokasi Naskah*)
- Sebutkan secara eksplisit bab, sub-bab, nomor halaman, dan nomor paragraf tempat perubahan berada.
- Kutip teks baru atau rangkuman data baru yang telah disisipkan ke dalam naskah.
- **Sertakan ID Blok Mekanis (`change_block_ids`)**: Cantumkan ID blok (`B0042`, `B0043`, dll.) yang diperoleh langsung dari berkas `<output>.apply-report.json`.

---

## 3. Contoh Implementasi Butir Tanggapan

```markdown
### REV-001 (R1 — Major Comment 1, must_fix)

**Reviewer Comment:**
> "There are serious concerns about the research methodology. The paper uses questionnaire surveys to collect students' self-assessed employability but does not employ any objective indicators for triangulation. Relying solely on self-assessment to measure employability has insufficient validity."

**Status:** `RESOLVED`

**Author Response:**
Kami sangat berterima kasih atas catatan kritis Reviewer 1 yang sangat mendasar ini. Kami sepenuhnya sepakat bahwa pengukuran kelayakan kerja (*employability*) yang hanya bersandar pada survei persepsi diri (*self-report*) memiliki kerentanan bias sosial (*social desirability bias*). 

Untuk mengatasi hal tersebut, kami telah melakukan dua langkah perbaikan signifikan:
1. Menambahkan sub-bab khusus metodologis yang mendiskusikan batasan skala persepsi diri secara transparan, serta mengutip studi validasi psikometrik terkini (Hora et al., 2024) yang membuktikan adanya korelasi moderat ($r = 0.52$) antara skor persepsi diri mahasiswa dan penilaian atasan kerja.
2. Memperluas bab Diskusi dan Batasan Penelitian (*Limitations*) dengan merumuskan rekomendasi operasional bagi penelitian lanjutan untuk mengintegrasikan data objektif pelacakan alumni (*tracer study*) pasca satu tahun kelulusan.

**Changes Made:**
- Bab 3: Ditambahkan Sub-bab 3.6 ("Methodological Limitations and Scale Validity", ~350 kata).
- Bab 5: Ditambahkan pembahasan triangulasi data objektif pada paragraf Batasan Penelitian (+200 kata).
- Lokasi Naskah: `paper/03_materials-and-methods.md`, `paper/05_discussion.md`.
- **Change Block IDs:** `B0084`, `B0085`, `B0142` (diverifikasi via `apply-report.json`).
```

---

## 4. Menangani Penolakan atau Batasan Secara Elegan

Tidak semua permintaan reviewer harus diakomodasi dengan mengubah eksperimen jika permintaan tersebut memang di luar cakupan penelitian (*out of scope*), terkendala persetujuan etik (IRB), atau bertentangan dengan konsensus literatur.

Terdapat 3 status non-`RESOLVED` yang sah dalam **Schema 8**:

### 1. `DELIBERATE_LIMITATION` (Batasan Sadar yang Diakui)
Gunakan jika permintaan reviewer valid namun secara logistik, temporal, atau perizinan etik tidak memungkinkan untuk dilakukan dalam revisi ini.
- **Wajib:** Jelaskan alasan keterbatasan secara objektif, dan pastikan keterbatasan tersebut telah ditambahkan ke bagian *Limitations* pada paper.

### 2. `REVIEWER_DISAGREE` (Ketidaksepakatan Penulis yang Beralasan)
Gunakan jika usulan reviewer bertentangan dengan landasan teoretis atau fakta empiris penelitian.
- **Wajib:** Berikan bukti literatur yang kuat, data kuantitatif, atau simulasi matematis yang mendasari mengapa pendekatan penulis saat ini adalah yang paling tepat. Gunakan bahasa diplomatis: *"While we understand the reviewer's perspective regarding X, empirical findings in our field (Y et al., 2023) suggest that..."*.

### 3. `UNRESOLVABLE` (Kondisi Tidak Dapat Diselesaikan)
Gunakan jika data mentah historis sudah tidak dapat diakses lagi (misal sensor rusak atau subjek uji telah purnatugas) tanpa membatalkan kontribusi utama.

---

## 5. Hubungan dengan Laporan Eksekusi Patch (*Apply Report Integration*)

Bidang `change_block_ids` adalah pembeda utama arsitektur ARS #390 dibandingkan surat tanggapan biasa. Bidang ini memberikan bukti mesin (*machine-verifiable evidence*) bahwa teks benar-benar diubah pada blok yang bersangkutan:
1. Setelah `ars_apply_revision_patch.py` selesai, buka berkas `<draft>.apply-report.json`.
2. Periksa entri `ops_applied[]`:
   - Operasi `replace_block` pada target `B0012` mengasosiasikan `B0012` ke item roadmap.
   - Operasi `insert_after` mencatat blok-blok baru pada `new_block_ids: ["B0045", "B0046"]`.
3. Masukkan ID blok tersebut ke dalam baris `change_block_ids` di berkas tanggapan.
4. Tim reviewer independen atau penguji dapat mencocokkan `change_block_ids` secara otomatis terhadap laporan eksekusi patch untuk membuktikan kepatuhan revisi secara matematis.
