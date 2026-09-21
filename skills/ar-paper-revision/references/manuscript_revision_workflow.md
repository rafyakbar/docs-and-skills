# Panduan Alur Kerja Revisi Naskah Ilmiah (Fase 22 Execution Workflow)

Panduan ini menjabarkan langkah-langkah praktis bagi agen dan peneliti akademik dalam mengeksekusi perbaikan draf naskah paper (`paper/*.md`) berdasarkan rekomendasi reviewer, matriks komitmen (Schema 11), dan rencana aksi revisi (Schema 7).

---

## 1. Tahap 1: Persiapan & Penstempelan Jangkar Draf (*Intake & Anchorize*)

Sebelum menyusun perbaikan apa pun, draf naskah bab yang akan direvisi harus distempel jangkar blok deterministik terlebih dahulu.

### Langkah Eksekusi:
Jalankan skrip `ars_anchorize_draft.py` pada berkas bab sasaran:
```bash
python skills/ar-paper-revision/scripts/ars_anchorize_draft.py paper/01_introduction.md
```

### Hasil yang Dihasilkan:
1. Berkas `paper/01_introduction.md` diperbarui di tempat (*in-place*) dengan menambahkan marker `<!--block:BNNNN-->` di atas setiap blok paragraf, tabel, heading, atau cuplikan kode.
2. Berkas sidecar `paper/01_introduction.md.block-manifest.json` otomatis terbit.

### Aturan Keamanan Jeda Tulis (*No-Rewrite Window*):
> **PERINGATAN PENTING**: Setelah berkas manifest blok terbit, **DILARANG KERAS** melakukan modifikasi manual atau pemformatan apa pun terhadap berkas naskah dasar sebelum patch diterapkan. Modifikasi apa pun akan mengubah `base_draft_hash` atau `old_hash` dari blok terkait dan menyebabkan kegagalan eksekusi (*stale-base rejection*).

---

## 2. Tahap 2: Pembacaan Manifest & Perumusan Patch (*Patch Construction*)

Penulis membuka berkas manifest blok untuk mengekstrak informasi hash yang dibutuhkan.

### Contoh Membaca Manifest:
```json
{
  "manifest_format_version": "1.0",
  "base_draft_hash": "a1b2c3d4e5f6",
  "blocks": [
    {
      "block_id": "B0001",
      "old_hash": "e4f5a6b7c8d9",
      "first_line_excerpt": "# 1. Introduction"
    },
    {
      "block_id": "B0002",
      "old_hash": "7a8b9c0d1e2f",
      "first_line_excerpt": "Facial recognition systems have achieved remarkable accuracy in recent years..."
    }
  ]
}
```

### Aturan Perumusan Operasi Patch:
1. **Salin Hash Mekanis**: Salin nilai `base_draft_hash` langsung ke tingkat akar berkas patch. Untuk setiap operasi pada blok `B0002`, salin nilai `old_hash` ("7a8b9c0d1e2f"). Jangan mencoba menghitung ulang hash!
2. **Keterlacakan Roadmap**: Setiap operasi wajib mengaitkan `roadmap_item_ids` yang bersumber dari Schema 7 (misalnya `["REV-001"]`).
3. **Preservasi Sitasi Braket**:
   - Jika teks asli mengandung sitasi naskah yang sudah terhubung `[[1]](06_references.md#ref1)`, pertahankan tautan tersebut secara utuh.
   - Jika paragraf baru menambahkan klaim pustaka baru yang belum terindeks di `06_references.md`, cantumkan sitasi sementara seperti `(Wang et al., 2024)` atau `<!--ref:wang2024-->` yang nantinya akan dikompilasi oleh `ar-paper-sentence-citation` dan `ar-paper-reference-compiler`.
4. **Hindari Sintaks Marker di `new_text`**: Jangan sekali-kali mengetik `<!--block:B...-->` di dalam teks baru.

---

## 3. Tahap 3: Penerapan Patch Deterministik (*Deterministic Apply*)

Terapkan patch menggunakan skrip `ars_apply_revision_patch.py`. Target keluaran **wajib merupakan berkas versi baru** (misal `.rev1.md` atau langsung menggantikan draf jika dikelola sistem kontrol versi git):

```bash
python skills/ar-paper-revision/scripts/ars_apply_revision_patch.py \
    paper/01_introduction.md \
    paper/revisions/patch_round1_intro.json \
    --output paper/01_introduction.rev1.md
```

### Evaluasi Laporan Hasil Eksekusi (`.apply-report.json`):
Periksa laporan sidecar yang terbit di samping berkas keluaran:
```json
{
  "report_format_version": "1.2",
  "mode": "patch",
  "base_draft_hash": "a1b2c3d4e5f6",
  "output_draft_hash": "f6e5d4c3b2a1",
  "patch_digest": "4c8f2b...",
  "ops_applied": [
    {
      "op_index": 0,
      "op": "replace_block",
      "block_id": "B0002",
      "roadmap_item_ids": ["REV-001"],
      "new_block_ids": []
    }
  ],
  "counters": {
    "blocks_total": 15,
    "blocks_touched": 2,
    "blocks_preserved_byte_identical": 13,
    "preserved_ratio": 0.8667
  }
}
```

Informasi penting yang didapat:
- `preserved_ratio`: Menunjukkan persentase blok yang terlindungi secara identik (pada contoh di atas: 86.67%).
- `fresh_block_ids`: Berisi ID blok baru yang tercipta dari operasi `insert_after` atau pecahan multi-paragraf. Simpan daftar ID ini untuk mengisi bidang `change_block_ids` pada berkas respons reviewer (Schema 8).

---

## 4. Tahap 4: Verifikasi Disiplin Patch (*Discipline Verification*)

Jalankan skrip pemeriksa kepatuhan disiplin revisi:
```bash
python skills/ar-paper-revision/scripts/verify_revision_discipline.py \
    --draft paper/01_introduction.md \
    --patch paper/revisions/patch_round1_intro.json \
    --output paper/01_introduction.rev1.md \
    --report paper/01_introduction.rev1.md.apply-report.json
```

Pastikan skrip menghasilkan status `OK (all checks passed)`.

---

## 5. Tahap 5: Promosi Draf & Sinkronisasi Bab (*Draft Promotion*)

Setelah verifikasi selesai dan dipastikan tidak ada kesalahan:
1. Gantikan naskah kerja utama dengan naskah revisi (misal `mv 01_introduction.rev1.md 01_introduction.md`).
2. Perbarui berkas manifesto blok untuk putaran selanjutnya (`python ars_anchorize_draft.py 01_introduction.md`).
3. Jika terdapat sitasi baru yang ditambahkan, lanjutkan ke alur `ar-paper-sentence-citation` dan `ar-paper-reference-compiler` untuk memastikan daftar pustaka tetap selaras (*zero-orphan*).
4. Lengkapi draf Surat Tanggapan Reviewer (*Response to Reviewers*) dan perbarui Matriks Komitmen R&R (Schema 11).
