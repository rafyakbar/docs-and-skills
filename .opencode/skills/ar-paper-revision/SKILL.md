---
name: ar-paper-revision
description: "Aktifkan ketika pengguna meminta untuk mengeksekusi revisi naskah akademik (paper/*.md) berdasarkan hasil peer review atau bimbingan, menerapkan patch presisi blok (ARS Spec #390/#424 diff/patch revision mode), menyusun surat tanggapan reviewer (Response to Reviewers Schema 8), atau memperbarui matriks komitmen (Schema 11). Mendukung penstempelan blok deterministik (<!--block:BNNNN-->), validasi fail-closed dua fase, penyambungan aliran byte (byte-span splicing), pemicu struktural (ambang rasio 0.6), dan integrasi ID blok hasil apply ke dalam respons formal. Kata kunci pemicu: revisi paper, revision patch, apply patch, response to reviewers, revisi naskah, response letter, eksekusi revisi, perbaiki naskah, patch revisi, ars-revision, ar-paper-revision. JANGAN aktifkan untuk simulasi mock peer review (gunakan ar-paper-reviewer), perencanaan dekonstruksi komentar review (gunakan ar-paper-revision-coach), penulisan draf bab baru dari nol (gunakan ar-paper-draft), perancangan outline (gunakan ar-paper-outline), pencarian sitasi kalimat (gunakan ar-paper-sentence-citation), kompilasi daftar pustaka (gunakan ar-paper-reference-compiler), atau penomoran sitasi braket teks (gunakan ar-paper-citation-numbering)."
---

# Academic Research Skills: Paper Revision & Diff-Patch Execution (`ar-paper-revision`)

Skill ini merupakan mesin operasional **Fase 22 (Revision Execution)** dalam siklus riset ilmiah akademik. Mengadopsi arsitektur normatif **ARS Spec #390** dan amandemen **#424 Slice B**, skill ini bertugas menerapkan modifikasi naskah bab (`paper/*.md`) menggunakan pendekatan **Diff/Patch Berbasis Blok Jangkar Deterministik** untuk membatalkan fenomena distorsi emisi ulang naskah utuh (*DELEGATE-52*). Skill ini juga menyusun surat tanggapan butir-per-butir (*Point-by-Point Response to Reviewers* Schema 8) dan memutakhirkan Matriks Keterlacakan Komitmen Revisi (Schema 11).

---

## Kapan Mengaktifkan Skill Ini
- Pengguna meminta mengeksekusi perbaikan bab naskah paper berdasarkan catatan reviewer atau bimbingan dosen pembimbing.
- Pengguna meminta menstempel blok jangkar (`<!--block:BNNNN-->`) dan menerbitkan manifest blok (`.block-manifest.json`).
- Pengguna meminta menyusun berkas patch revisi JSON (`revision_patch.json`) dengan operasi tertutup (`replace_block`, `insert_after`, `delete_block`).
- Pengguna meminta menerapkan patch ke naskah dasar menggunakan `ars_apply_revision_patch.py`.
- Pengguna meminta menyusun Surat Tanggapan Reviewer formal (*Response to Reviewers Letter*) dengan menyertakan `change_block_ids`.
- Pengguna meminta memperbarui status pemenuhan komitmen bertingkat (*fulfillment status*) pada Matriks Schema 11.

## Kapan TIDAK Mengaktifkan Skill Ini
- **Simulasi Mock Review Awal**: Jika pengguna ingin melakukan evaluasi kritis/simulasi peer review naskah dari nol, gunakan `ar-paper-reviewer`.
- **Dekonstruksi Komentar & Pembuatan Roadmap**: Jika pengguna baru saja menerima komentar reviewer mentah dan ingin menganalisisnya menjadi rencana aksi, gunakan `ar-paper-revision-coach`.
- **Penulisan Draf Bab Baru dari Nol**: Jika pengguna ingin menulis bab baru dari outline, gunakan `ar-paper-draft`.
- **Penyusunan Kerangka Naskah**: Jika pengguna ingin merancang struktur bab atau outline, gunakan `ar-paper-outline`.
- **Kurasi Sitasi Per Kalimat**: Jika pengguna ingin mencari literatur untuk klaim naskah, gunakan `ar-paper-sentence-citation`.
- **Kompilasi Daftar Pustaka**: Jika pengguna ingin mengompilasi `06_references.md`, gunakan `ar-paper-reference-compiler`.
- **Injeksi Penomoran Sitasi Braket**: Jika pengguna ingin menghubungkan nomor sitasi braket interaktif, gunakan `ar-paper-citation-numbering`.
- **Pembuatan Abstrak & Front Matter**: Jika pengguna ingin menulis abstrak, gunakan `ar-paper-abstract`.

---

## 6 Aturan Emas Disiplin Revisi (*Iron Rules*)

1. **Preservasi Blok Identik (*Byte-Span Splicing Protection*)**:
   Blok naskah yang tidak disebut di dalam operasi patch **DILARANG KERAS** melewati proses generasi ulang model bahasa. Blok tersebut wajib disalin secara utuh byte-per-byte (*byte-identical by construction*) langsung dari aliran byte dokumen asli.
2. **Larangan Mengarang Hash (*Mechanical Hash Copy Rule*)**:
   Agen penulis **DILARANG KERAS** menghitung atau mengarang nilai hash (`base_draft_hash` dan `old_hash`). Semua nilai hash wajib disalin secara mekanis dari berkas sidecar manifest blok (`<draft>.block-manifest.json`) yang diterbitkan oleh skrip.
3. **Aturan Target Tunggal (*Single-Target Rule*)**:
   Setiap `block_id` hanya boleh muncul paling banyak di **satu operasi** dalam satu berkas patch (baik sebagai target penggantian, penyisipan, maupun penghapusan).
4. **Larangan Marker di Teks Baru (*No Block Markers in new_text*)**:
   Bidang `new_text` dalam patch **DILARANG KERAS** memuat sintaks `<!--block:`. Penetapan dan penomoran ID baru (`max(existing) + 1`) merupakan hak eksklusif skrip penyambung patch.
5. **Preservasi Sitasi Braket Naskah**:
   Semua penomoran sitasi braket markdown aktif (misal `[[1]](06_references.md#ref1)`) yang ada di dalam blok yang disentuh wajib dipertahankan konsistensinya. Sitasi baru wajib diformat bersih untuk diselaraskan kemudian.
6. **Eksklusivitas Peran Penulis vs Mesin Splicing (*Role Split*)**:
   Agen penulis hanya bertugas memproduksi berkas patch JSON (`revision_patch.json`) dan draf tanggapan sementara. Eksekusi penyambungan fisik naskah ke disk wajib diserahkan kepada skrip `ars_apply_revision_patch.py`.

---

## Alur Kerja 4 Tahap Eksekusi Revisi

```
[Tahap 1: Stempel Blok] ──▶ [Tahap 2: Rancang Patch] ──▶ [Tahap 3: Apply Deterministik] ──▶ [Tahap 4: Surat Tanggapan]
  ars_anchorize_draft.py      revision_patch.json         ars_apply_revision_patch.py        Response to Reviewers
  + block-manifest.json       (Salin hash manifest)       + apply-report.json                + Schema 11 Update
```

### Tahap 1: Penstempelan Blok & Penerbitan Manifest
1. Ambil berkas bab naskah yang akan direvisi (misal `paper/01_introduction.md`).
2. Jalankan skrip stempel jangkar blok deterministik:
   ```bash
   python skills/ar-paper-revision/scripts/ars_anchorize_draft.py paper/01_introduction.md
   ```
3. Skrip menstempel marker `<!--block:BNNNN-->` di atas setiap blok secara in-place dan menerbitkan berkas manifesto sidecar `paper/01_introduction.md.block-manifest.json`.
4. **Kunci Jeda Tulis**: Naskah dasar tidak boleh diubah manual setelah manifest terbit agar hash tidak basi.

### Tahap 2: Perumusan Dokumen Patch Revisi
1. Buka berkas manifest blok dan temukan `block_id` serta `old_hash` dari paragraf yang menjadi target perbaikan Roadmap (Schema 7).
2. Susun dokumen patch `paper/revisions/patch_round1.json` menggunakan kosakata tertutup:
   - `replace_block`: Mengganti isi paragraf yang sudah ada dengan teks baru yang telah disempurnakan.
   - `insert_after`: Menyisipkan paragraf/tabel/penjelasan baru setelah blok tertentu (atau setelah frontmatter menggunakan sentinel `"DOC-BODY-START"`).
   - `delete_block`: Menghapus blok yang tidak relevan/keliru.
3. Cantumkan `roadmap_item_ids` (misal `["REV-001"]`) pada setiap operasi untuk keterlacakan mutlak.

### Tahap 3: Penerapan Patch Deterministik Dua Fase
1. Terapkan patch ke naskah keluaran versi baru:
   ```bash
   python skills/ar-paper-revision/scripts/ars_apply_revision_patch.py \
       paper/01_introduction.md \
       paper/revisions/patch_round1.json \
       --output paper/01_introduction.rev1.md
   ```
2. Skrip melakukan validasi Fase 1 secara *fail-closed* (jika ada hash tidak cocok, pembatalan total dilakukan tanpa menyentuh berkas dasar).
3. Jika validasi lolos, Fase 2 memotong dan menyambungkan aliran byte asli, menomori blok baru secara otomatis, dan menerbitkan `paper/01_introduction.rev1.md.apply-report.json`.
4. **Pemicu Struktural**: Jika perubahan menyentuh heading atau rasio blok disentuh $> 0.6$, skrip keluar dengan kode 3 (*refused structural*). Evaluasi apakah restrukturisasi memang disengaja; jika ya, jalankan ulang dengan flag `--acknowledge-structural`.
5. Jalankan audit disiplin revisi:
   ```bash
   python skills/ar-paper-revision/scripts/verify_revision_discipline.py \
       --draft paper/01_introduction.md \
       --patch paper/revisions/patch_round1.json \
       --output paper/01_introduction.rev1.md \
       --report paper/01_introduction.rev1.md.apply-report.json
   ```

### Tahap 4: Sintesis Surat Tanggapan & Pembaruan Matriks Komitmen
1. **Lengkapi Response to Reviewers (Schema 8)**:
   - Buka `paper/01_introduction.rev1.md.apply-report.json` untuk membaca `ops_applied` dan `fresh_block_ids`.
   - Susun tanggapan butir-per-butir menggunakan pola **R $\to$ A $\to$ C** (*Reviewer Comment $\to$ Author Response $\to$ Changes Made*).
   - Isi bidang `change_block_ids` dengan ID blok mekanis (`B0042`, `B0043`, dll.).
2. **Perbarui Matriks Komitmen (Schema 11)**:
   - Mutakhirkan baris kepatuhan: isi `authors_claim`, `revision_location`, dan ubah `fulfillment_status` pada objek komitmen menjadi `fulfilled`, `partial`, `not-fulfilled`, atau `explicitly-rejected-with-rationale`.
   - Sertakan `unfulfilled_rationale` jika status bukan `fulfilled`.
3. Promosikan naskah revisi menjadi berkas utama naskah kerja bab untuk putaran berikutnya.

---

## Perangkat Skrip Bantu (`scripts/`)

- `_block_parser.py`: Parser blok CommonMark deterministik berbasis aliran byte (fenced code, ATX heading, tabel, list, blockquote, text run). Pure Python Standard Library.
- `ars_anchorize_draft.py`: Menstempel marker jangkar `<!--block:BNNNN-->` secara in-place dan menerbitkan `<draft>.block-manifest.json`.
- `ars_apply_revision_patch.py`: Mesin eksekusi patch dua fase *fail-closed*, penyambung aliran byte asli, pemeriksa pemindahan murni (*pure move*), dan penerbit laporan `<output>.apply-report.json`.
- `verify_revision_discipline.py`: Linter penjamin mutu kepatuhan skema patch, verifikasi keselarasan hash naskah, audit aturan target tunggal, dan keutuhan integritas marker.

---

## Berkas Panduan Referensi (`references/`)

1. [Protokol Patch Revisi Spec #390 & #424](references/revision_patch_protocol_390.md): Landasan arsitektur tiga lapisan, kosakata operasi, aturan malformed state, kode keluar skrip, dan penanganan eskalasi struktural.
2. [Panduan Alur Kerja Eksekusi Revisi Naskah](references/manuscript_revision_workflow.md): Langkah teknis sistematis Fase 22 dari pembacaan manifest, formulasi operasi patch, penanganan sitasi, hingga promosi draf.
3. [Panduan Penyusunan Surat Tanggapan Reviewer](references/response_to_reviewers_authoring_guide.md): Standar penyusunan surat tanggapan formal Schema 8 berpolakan R $\to$ A $\to$ C, justifikasi penolakan sopan, dan injeksi `change_block_ids`.
4. [Panduan Siklus Hidup Matriks Komitmen Bertingkat](references/nested_ledger_lifecycle_guide.md): Pembaruan Schema 11 R&R Traceability Matrix dengan arsitektur objek bertingkat (#268), 9 tipe bukti naskah, dan aturan rasionalisasi.
5. [Paket Lengkap Contoh Eksekusi Revisi](references/sample_revision_execution_package.md): Contoh utuh dari naskah dasar, manifest blok, patch JSON, naskah revisi hasil splice, apply report, hingga surat tanggapan.
