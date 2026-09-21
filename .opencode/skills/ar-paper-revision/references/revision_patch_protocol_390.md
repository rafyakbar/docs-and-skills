# Protokol Patch Revisi Naskah Ilmiah (ARS Spec #390 & #424)

Dokumen ini merupakan panduan normatif dan operasional untuk eksekusi revisi naskah akademik menggunakan arsitektur **Diff/Patch Revision Mode** berdasarkan **ARS Spec #390** dan amandemen **#424 Slice B**.

---

## 1. Landasan Filosofis & Motivasi (DELEGATE-52)

Dalam alur revisi paper akademik konvensional, model bahasa (LLM) biasanya diminta menulis ulang seluruh naskah (*full draft re-emission*). Temuan empiris dari studi **DELEGATE-52 (arXiv:2604.15597)** membuktikan bahwa:
1. Model skala besar (*frontier models*) mendegradasi dokumen melalui **modifikasi halus yang tidak disengaja (*subtle modification distortion*)**, bukan penghapusan teks secara gamblang.
2. Sebanyak **80% hingga 98% penurunan kualitas dokumen** berakar dari *rare single-step critical failures* (kegagalan fatal acak pada satu putaran).
3. Melakukan emisi ulang naskah utuh mengekspos setiap karakter, simbol matematika, dan sitasi di seluruh bab paper terhadap risiko distorsi, meskipun bagian tersebut tidak diminta direvisi oleh reviewer.

### Klaim Kejujuran (*Honest Claim*)
Arsitektur Diff/Patch Revision Mode **mempersempit bidang paparan distorsi senyap (*silent-distortion surface*) dari "seluruh naskah paper" menjadi hanya "blok paragraf yang secara eksplisit disentuh oleh operasi revisi."**
> Protokol ini **TIDAK** membuat kualitas argumen revisi secara otomatis lebih baik, dan tidak merevisi restrukturisasi global secara otomatis. Yang dijamin oleh protokol ini adalah: **blok-blok naskah yang tidak disebut dalam patch diproteksi secara deterministik identik byte-per-byte (*byte-identical by construction*) tanpa pernah melewati proses generasi ulang LLM.**

---

## 2. Mekanisme Tiga Lapisan (*Three-Layer Architecture*)

```
+-------------------------------------------------------------------------+
| Lapisan 1: Blok Jangkar Deterministik (ars_anchorize_draft.py)          |
|  - Menstempel <!--block:BNNNN--> di atas tiap blok                      |
|  - Menghasilkan sidecar: <draft>.block-manifest.json                    |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
| Lapisan 2: Dokumen Patch Tertutup (revision_patch.json)                 |
|  - Kosakata tertutup: replace_block, insert_after, delete_block         |
|  - Menyalin old_hash dari manifest (penulis TIDAK PERNAH menghitung)   |
|  - Memetakan setiap operasi ke roadmap_item_ids                         |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
| Lapisan 3: Mesin Eksekusi Fail-Closed (ars_apply_revision_patch.py)     |
|  - Fase 1 (Validasi): Validasi schema, base_draft_hash, old_hash       |
|  - Fase 2 (Penyambungan): Byte-span splicing pada stream asli           |
|  - Pemicu Struktural: touched_ratio > 0.6, perubahan heading            |
|  - Menghasilkan sidecar: <output>.apply-report.json                     |
+-------------------------------------------------------------------------+
```

### Lapisan 1: Lapisan Blok Jangkar (*Block Anchor Layer*)
1. **Gramatika Marker**: `<!--block:BNNNN-->` diletakkan tepat pada baris tunggal di atas setiap blok teks tanpa baris kosong pemisah.
2. **Penomoran Monotonik**: `NNNN` adalah angka desimal 4 digit (`B0001`, `B0002`, dst.) yang bertambah secara monotonik (`max(existing) + 1`).
3. **Kemandirian Konten**: ID blok tidak bergantung pada konten teks dan **tidak boleh dinomori ulang**. ID melekat secara posisional-historis.
4. **Otoritas Skrip**: Hanya skrip `ars_anchorize_draft.py` yang berhak memberi ID. LLM dilarang keras menstempel, mengarang, atau menomori ulang ID blok.
5. **Manifest Blok Sidecar (`<draft>.block-manifest.json`)**:
   - `base_draft_hash`: 12 karakter heksadesimal pertama dari SHA-256 seluruh byte mentah berkas draf.
   - `blocks`: Daftar entri `[{block_id, old_hash, first_line_excerpt}]`.
   - Menjadi **satu-satunya sumber rujukan hash yang sah**. LLM menyalin nilai hash dari manifest, bukan menghitungnya sendiri.

### Lapisan 2: Dokumen Patch (*Revision Patch Document*)
Dokumen berformat JSON terstruktur (`revision_patch.json`) dengan skema ketat:
- `patch_format_version`: `"1.0"`.
- `revision_round`: Integer $\ge 1$.
- `base_draft_hash`: 12-hex hash berkas dasar (dari manifest).
- `emitted_by`: Identitas agen penulis (misal: `"draft_writer_agent"`).
- `ops`: Daftar operasi blok yang didefinisikan serentak terhadap berkas dasar.

#### Kosakata Operasi Tertutup (*Closed Vocabulary*)
1. `replace_block`:
   - Bidang: `op`, `block_id`, `old_hash`, `new_text`, `roadmap_item_ids`.
   - Mengganti teks blok. Jika `new_text` menghasilkan multiblok, blok pertama mewarisi ID target, sedangkan blok berikutnya diberi ID baru berturut-turut.
2. `insert_after`:
   - Bidang: `op`, `block_id`, `old_hash` (dihilangkan jika target sentinel), `new_text`, `roadmap_item_ids`.
   - Menyisipkan blok teks baru setelah blok target jangkar.
   - Mendukung sentinel posisional `"DOC-BODY-START"` (posisi setelah frontmatter YAML dan sebelum blok teks pertama tubuh paper). Pada sentinel ini, `old_hash` tidak digunakan.
3. `delete_block`:
   - Bidang: `op`, `block_id`, `old_hash`, `roadmap_item_ids`.
   - Menghapus blok beserta marker jangkarnya.

#### Batasan Kritis (*Strict Patch Constraints*)
- **Aturan Target Tunggal (*Single-Target Rule*)**: Setiap `block_id` hanya boleh muncul paling banyak di **satu operasi**, dalam peran apa pun.
- **Larangan Marker di `new_text`**: Bidang `new_text` **DILARANG KERAS** mengandung sintaks `<!--block:`. Penetapan ID baru adalah hak eksklusif mesin penyambung patch.
- **Traceability Wajib**: Bidang `roadmap_item_ids` wajib diisi daftar ID roadmap revisi (misal `["REV-001"]`).

### Lapisan 3: Eksekusi Deterministik Dua Fase (*Deterministic Two-Phase Apply*)
Dijalankan oleh `ars_apply_revision_patch.py`:

#### Fase 1: Validasi Utuh, Sentuh Nol (*Validate Everything, Touch Nothing*)
- Validasi skema JSON patch.
- Validasi kecocokan `base_draft_hash` terhadap berkas draf saat ini.
- Parsing draf dasar dengan parser bersama `_block_parser.py`.
- Memverifikasi keberadaan seluruh `block_id` target dan mencocokkan `old_hash` terhadap teks blok ternormalisasi saat ini.
- Memastikan tidak ada marker tersemat di `new_text`.
- **Kegagalan sekecil apa pun membatalkan seluruh operasi secara fail-closed**: berkas naskah dasar tidak disentuh sama sekali (*byte-untouched*), mencegah patch setengah jalan.

#### Fase 2: Penyambungan Rentang Byte (*Byte-Span Splicing*)
- Pemotongan dan penyambungan dilakukan langsung pada **aliran byte asli (*byte stream*)**, bukan serialisasi ulang parser markdown.
- Semua blok yang tidak disentuh (beserta marker dan baris kosong pemisahnya) disalin secara identik dari byte asli.
- Blok baru diberi ID segar secara otomatis.
- Dilakukan verifikasi mandiri pasca-tulis (*post-write self-check*) untuk memastikan keunikan seluruh ID blok.
- Draf revisi ditulis sebagai berkas versi baru secara atomik (tidak pernah menimpa draf dasar).
- Menerbitkan laporan eksekusi `<output>.apply-report.json` (Format 1.2).

---

## 3. Pemicu Bentuk Struktural (*Structural-Shape Triggers*) & Eskalasi

Jika sebuah revisi menyentuh restrukturisasi global, perlindungan patch biasa tidak boleh menutupi perubahan besar tersebut secara diam-diam. Mesin eksekusi mengevaluasi pemicu berikut:

1. **Ambang Batas Rasio Sentuh (`touched_ratio > 0.6`)**:
   - $\text{touched\_ratio} = \frac{\text{blocks\_touched}}{\text{blocks\_total}}$.
   - `blocks_touched` menghitung blok yang di-`replace` atau di-`delete`.
   - Jika rasio $> 0.6$ (keputusan rilis #424), eksekusi **ditolak** kecuali ada konfirmasi eksplisit.
2. **Operasi pada Blok Judul (*Heading Blocks*)**:
   - Menghapus atau mengganti blok judul bab/sub-bab (`#`, `##`, `###`) memicu bendera struktural.
   - Perubahan jumlah total heading ($\Delta \ne 0$) memicu bendera struktural.
   - **Pengecualian Jangkar Judul (*Heading-Anchor Exemption*)**: Operasi `insert_after` yang hanya menggunakan heading sebagai titik jangkar (untuk menyisipkan paragraf teks di awal bab) **TIDAK** memicu bendera heading selama `new_text`-nya tidak mengandung heading.
3. **Pemeriksaan Pemindahan Murni (*Pure-Move Check*)**:
   - Jika ada blok yang dihapus dan teks persisnya disisipkan di tempat lain (hash identik), skrip mencatatnya secara otomatis sebagai pasangan `pure_move_pairs`.

### Jalur Penanganan Status Keluar Skrip (*Exit Codes*)

| Kode | Arti | Tindakan yang Harus Diambil |
|:---:|---|---|
| `0` | **Sukses (Applied)** | Draf revisi dan laporan berhasil ditulis. Lanjutkan ke verifikasi dan respons reviewer. |
| `2` | **Penolakan Fase 1 (Phase 1 Rejection)** | Terjadi ketidakcocokan hash, target tidak ditemukan, atau skema salah. Kirimkan pesan kegagalan ke agen penulis untuk **1 kali koreksi emisi ulang patch**. Jika gagal kedua kalinya, eskalasi ke pengguna. Jangan pernah mengedit manual hash patch! |
| `3` | **Penolakan Struktural (Structural Refusal)** | Patch menyentuh judul atau melebihi rasio 0.6. Evaluasi apakah perubahan struktural memang direncanakan. Jika ya, jalankan ulang dengan argumen `--acknowledge-structural`. |
| `4` | **Kegagalan Self-Check (Internal Bug)** | Integritas ID ganda terdeteksi pada draf keluaran. Laporkan sebagai kerusakan sistem perangkat lunak. |

---

## 4. Siklus Hidup Marker (*Marker Lifecycle*)

Tiga marker HTML-comment (`<!--block:-->`, `<!--ref:-->`, `<!--anchor:-->`) diatur oleh aturan baku repositori:
1. **Penghitungan Kata (*Word Count*)**: Seluruh marker `<!--...-->` wajib dibersihkan sebelum menghitung panjang kata (`len(body.split())`).
2. **Penyimpanan Berkas Kerja**: Berkas draf kerja (`paper/*.md`) tetap menyimpan seluruh marker untuk menjaga rantai audit dan putaran revisi berikutnya.
3. **Pembersihan Berkas Akhir**: Saat eksekusi formatting publikasi final (misal ekspor naskah ke PDF/LaTeX/Word), semua komentar HTML dibersihkan dari dokumen cetak akhir.
