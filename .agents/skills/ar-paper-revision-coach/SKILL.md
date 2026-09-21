---
name: ar-paper-revision-coach
description: "Aktifkan ketika pengguna meminta untuk mendekonstruksi komentar reviewer (peer review comments), menyusun rencana aksi revisi (revision roadmap), mengekstrak komitmen perbaikan (commitment ledger Kong et al. 2026), memetakan isu ke bab naskah, atau menyiapkan rangka surat sanggahan (response letter skeleton) pada Fase 19–21 siklus riset akademik. Mendukung parsing komentar mentah (email editor, PDF, teks bebas), taksonomi 4 tingkat (Major, Minor, Editorial, Positive), prioritisasi 3-tier (P1: must_fix, P2: should_fix, P3: consider), Kontrak Schema 11 R&R Traceability Matrix dengan nested-object shape (#268), dan penyusunan talking points untuk bimbingan dosen pembimbing. Kata kunci pemicu: revision coach, buat revision roadmap, analisis komentar reviewer, parse reviews, rencana revisi paper, dekonstruksi reviewer, commitment ledger, response letter skeleton, revision tracking, matriks revisi. JANGAN aktifkan untuk menulis draf bab naskah baru (gunakan ar-paper-draft), eksekusi patch revisi teks naskah (gunakan ar-revision), simulasi peer review independen dari nol (gunakan ar-paper-reviewer), atau audit penjaminan mutu surat sanggahan akhir (gunakan ar-rebuttal-audit)."
---

# ar-paper-revision-coach

Skill ini berfungsi sebagai **Perencana Strategis Revisi & Dekonstruksi Komentar Reviewer** (*Revision Coach Agent*) dalam siklus riset akademik internasional (Fase 19–21). Skill ini membedah masukan reviewer yang tidak terstruktur menjadi rencana tindakan terukur (*actionable roadmap*) dan mengunci komitmen perbaikan sebelum teks naskah dimodifikasi pada Fase 22 (`ar-revision`).

---

## Kapan Mengaktifkan
- Pengguna menerima surat keputusan editorial (*Major/Minor Revision*) beserta komentar reviewer dari jurnal internasional (IEEE, Elsevier, Springer, Nature, dll).
- Pengguna memiliki laporan review hasil simulasi bebestari internal dari skill `ar-paper-reviewer` (`07_editorial_decision.md` dan `08_revision_roadmap.md`).
- Pengguna ingin membedah komentar, memetakan isu per tingkat keparahan, dan menentukan prioritas perbaikan.
- Pengguna ingin menyusun matriks pelacakan status (*Revision Tracking Table*) dengan *Nested Commitment Ledger* (Schema 11 / Kong et al. 2026).
- Pengguna ingin menyiapkan bahan diskusi matang (*pre-advising talking points*) untuk divalidasi oleh dosen pembimbing (*Corresponding Author*).

## Kapan TIDAK Mengaktifkan
- **Eksekusi Penulisan Naskah Revisi**: Jangan gunakan untuk mengetik ulang bab atau menerapkan *diff patch* naskah (gunakan `ar-revision`).
- **Simulasi Peer Review Awal**: Jangan gunakan untuk menilai naskah draf awal yang belum direview (gunakan `ar-paper-reviewer`).
- **Audit Penjaminan Mutu Rebuttal**: Jangan gunakan untuk audit kelayakan surat sanggahan final (gunakan `ar-rebuttal-audit`).
- **Drafting Bab Naskah Pertama Kali**: Gunakan `ar-paper-draft`.

---

## 6 Aturan Mutlak (Iron Rules)

1. **No Comment Left Behind & Zero-Orphan**:
   Setiap kalimat saran, pertanyaan, atau kritik reviewer wajib dipertanggungjawabkan dan dipetakan ke dalam roadmap. Dilarang mengabaikan atau menghapus komentar reviewer secara sepihak.
2. **Classification Before Action**:
   Setiap butir komentar wajib diklasifikasikan ke dalam salah satu taksonomi diskrit (`Major`, `Minor`, `Editorial`, `Positive`) sebelum tindakan teknis dirancang.
3. **Invarian Nested Commitment Ledger (#268 / Kong et al. 2026)**:
   Seluruh janji tindakan wajib didekomposisi ke bentuk *nested-object shape* (`commitment_text`, `commitment_type`, `required_evidence_type`). Dilarang menggunakan list paralel lama yang rentan desinkronisasi indeks. Kolom `unfulfilled_rationale` dilarang membawa placeholder `""` jika status `fulfilled`.
4. **Preserved Intent & Tone Independence (#574 B1)**:
   Register bahasa penilai yang sopan tidak boleh menurunkan tingkat keparahan teknis (*politeness does not soften severity*). Sebaliknya, nada reviewer yang emosional/adversarial tidak boleh dibalas secara defensif, melainkan dihadapi dengan bukti empiris dan data kuantitatif.
5. **Pre-Advising Sparring Boundary (Dilarang Mengubah Naskah Mandiri)**:
   Skill ini adalah asisten perencanaan pra-konsultasi. Peneliti manusia bersama dosen pembimbing memegang otoritas penuh untuk menyetujui batasan eksperimen sebelum naskah diubah.
6. **Strict Python Standard Library Only**:
   Seluruh skrip pembantu CLI dan linter audit wajib beroperasi 100% menggunakan pustaka bawaan Python (`sys`, `re`, `argparse`, `pathlib`, `json`).

---

## Alur Kerja 6 Tahap (6-Step Processing Pipeline)

```mermaid
flowchart TD
    In[1. Ingesti Masukan<br/>Teks Review / Keputusan EIC] --> Parse[2. Penguraian & Dekomposisi<br/>Pisahkan Isu Jamak & Beri ID Unik]
    Parse --> Class[3. Klasifikasi Keparahan<br/>Major / Minor / Editorial / Positive]
    Class --> Commit[4. Ekstraksi Komitmen<br/>Kong et al. 2026 / Schema 11]
    Commit --> Map[5. Pemetaan Seksion Naskah<br/>Bab 00 s/d 06]
    Map --> Prio[6. Prioritisasi & Sintesis 3 Dokumen<br/>P1: must_fix • P2: should_fix • P3: consider]
```

### Tahap 1: Ingesti Masukan (Input Ingestion)
Terima materi ulasan reviewer dalam format apa pun: email editor, kutipan PDF, daftar bernomor, maupun paket `sample_peer_review_package.md`. Jika tersedia, sertakan draf naskah bab untuk pemetaan judul sub-bab yang akurat.

### Tahap 2: Penguraian Komentar (Comment Parsing)
- Deteksi identitas penilai: `EIC`, `R1`, `R2`, `R3`, `DA`.
- Berikan penomoran stabil: `<ReviewerID>-<Nomor>` (misal: `R1-1`, `EIC-1`, `DA-1`).
- Pisahkan komentar majemuk (*compound comments*) menjadi entri terpisah jika menuntut luaran yang berbeda.

### Tahap 3: Klasifikasi Mutu
- **`Major`**: Cacat metodologis, data leakage, overclaim, validitas statistik. Konsekuensi: penolakan jika diabaikan.
- **`Minor`**: Kelengkapan literatur, penjelasan rasional parameter, penyajian grafik.
- **`Editorial`**: Tipografi, ejaan, format persamaan matematika, caption.
- **`Positive`**: Apresiasi metode (diakui di surat respons tanpa modifikasi naskah).

### Tahap 4: Ekstraksi Komitmen Pas (Schema 11)
Deteksi frasa imperatif dan tetapkan:
- `commitment_type`: `add_experiment` | `add_analysis` | `add_clarification` | `add_citation` | `restructure` | `other`.
- `required_evidence_type`:
  - 7 bukti naskah: `new_section`, `new_figure`, `new_table`, `new_citation`, `methods_paragraph`, `discussion_paragraph`, `prose_edit`.
  - 1 bukti surat respons: `acknowledgment_only`.
  - 1 escape hatch: `other`.

### Tahap 5: Pemetaan Bab Naskah
Petakan setiap isu ke target naskah: `00_abstract.md`, `01_introduction.md`, `02_related-works.md`, `03_methodology.md`, `04_results.md`, `05_discussion.md`, atau `06_references.md`.

### Tahap 6: Prioritisasi & Pembentukan Artefak
- **P1 (`must_fix`)**: Isu Major, catatan EIC, dan temuan Critical DA.
- **P2 (`should_fix`)**: Isu Minor yang memperkokoh kualitas klaim.
- **P3 (`consider`)**: Kosmetik editorial dan saran opsional.
- Hasilkan 3 berkas terstruktur:
  1. `08_revision_roadmap.md`: Matriks P1/P2/P3, pola silang, urutan pengerjaan, estimasi beban kerja.
  2. `09_revision_tracking.md`: Tabel pelacakan status resolusi dan blok YAML *Nested Commitment Ledger*.
  3. `10_response_letter_skeleton.md`: Rangka surat tanggapan formal berpola R $\to$ A $\to$ C.

---

## Referensi Terpandu

| Berkas Referensi | Cakupan Pengetahuan Utama |
| :--- | :--- |
| [`revision_coach_pipeline_guide.md`](references/revision_coach_pipeline_guide.md) | Panduan detail 6 tahap pemrosesan, heuristik pemisahan isu jamak, estimasi beban kerja, dan talking points dosen. |
| [`nested_commitment_ledger_protocol.md`](references/nested_commitment_ledger_protocol.md) | Spesifikasi Kontrak Schema 11 (#268 / Kong et al. 2026), 6 tipe komitmen, 9 tipe bukti, dan pencegahan kesenjangan komitmen. |
| [`revision_status_and_resolution_guide.md`](references/revision_status_and_resolution_guide.md) | Kriteria 4 status resolusi (`RESOLVED`, `DELIBERATE_LIMITATION`, `UNRESOLVABLE`, `REVIEWER_DISAGREE`). |
| [`response_letter_skeleton_guide.md`](references/response_letter_skeleton_guide.md) | Arsitektur surat tanggapan resmi bebestari (pola R $\to$ A $\to$ C) dan etika diplomasi saintifik anti-defensif. |
| [`sample_revision_package.md`](references/sample_revision_package.md) | Contoh nyata end-to-end ulasan stroke ViT/NCCT lengkap dengan roadmap, tracking ledger YAML, dan response skeleton. |

---

## Panduan Eksekusi Skrip CLI

### 1. Dekonstruksi Ulasan & Pembuatan Roadmap Otomatis
```bash
python scripts/ars_revision_coach.py <path_ke_file_review.md> --outdir paper/ --all
```
*Opsi Tambahan*:
- `--roadmap`: Hanya menghasilkan `08_revision_roadmap.md`.
- `--tracking`: Hanya menghasilkan `09_revision_tracking.md`.
- `--skeleton`: Hanya menghasilkan `10_response_letter_skeleton.md`.
- `--title "<Judul Paper>"`: Menyematkan judul naskah.
- `--journal "<Nama Jurnal>"`: Menyematkan nama jurnal target.
- `--decision "<Major Revision|Minor Revision>"`: Mengatur tingkat keputusan editorial.

### 2. Audit Integritas Roadmap & Commitment Ledger (Linter Invarian)
```bash
python scripts/verify_revision_roadmap.py paper/08_revision_roadmap.md paper/09_revision_tracking.md
```
Memverifikasi:
- Kepatuhan invarian N1–N5 Schema 11 (#268).
- Validitas enum tipe komitmen, tipe bukti, dan status resolusi.
- Zero-orphan check antara tabel pelacakan dan blok YAML.
- Ketiadaan placeholder string kosong `""` pada komitmen yang telah berstatus `fulfilled`.
