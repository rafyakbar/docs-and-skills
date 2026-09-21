# Buku Panduan Nada Bahasa & Diplomasi Akademik (Tone & Diplomacy Playbook)

Dalam proses penelaahan sejawat (*peer review*), nada bahasa (*tone*) pada surat tanggapan memiliki pengaruh psikologis yang sangat besar terhadap keputusan akhir editor dan reviewer. Sikap defensif, konfrontatif, atau meremehkan dapat mengubah keputusan *Minor Revision* menjadi penolakan langsung (*Reject*).

Buku panduan ini menguraikan taktik diplomasi akademik dan pola transformasi kalimat untuk menyusun respons yang persuasif, santun, dan berbasis bukti empiris.

---

## 1. Pola Diplomasi Empat Tahap: A $\to$ V $\to$ E $\to$ C (*The AVEC Pattern*)

Untuk setiap butir tanggapan kritis, gunakan struktur empat pilar **AVEC**:

```
[A] Acknowledge  ──▶ [V] Validate     ──▶ [E] Evidence     ──▶ [C] Clarify & Change
 Ucapan terima        Validasi inti        Sajikan bukti        Tunjukkan lokasi
 kasih objektif       kekhawatiran         angka & literatur    perubahan naskah
```

1. **A — Acknowledge (*Pengakuan & Apresiasi*)**:
   - Awali dengan mengakui pentingnya topik yang disoroti reviewer tanpa kesan menjilat.
   - *Contoh:* "We thank the reviewer for raising this critical point regarding cross-scanner variability."
2. **V — Validate (*Validasi Perspektif*)**:
   - Tunjukkan bahwa Anda memahami mengapa reviewer menyampaikan kritik tersebut. Jika terjadi kesalahpahaman, akui bahwa teks awal penulis mungkin kurang jelas (*own the ambiguity*).
   - *Contoh:* "We agree that without evaluating diverse acquisition protocols, the clinical generalizability of our model remains unverified."
3. **E — Evidence (*Penyajian Bukti Objektif*)**:
   - Sajikan bukti empiris, metrik statistik, atau kutipan ilmiah untuk menjawab persoalan.
   - *Contoh:* "To address this, we conducted an additional evaluation on 40 patients from an external hospital cohort (Siemens Somatom Definition, 120 kVp), achieving an AUROC of 0.928 (95% CI: 0.891–0.965)."
4. **C — Clarify & Change (*Klarifikasi Lokasi Perubahan Naskah*)**:
   - Jelaskan di mana letak revisi naskah beserta rujukan halaman, tabel, atau nomor blok jangkar.
   - *Contoh:* "These new findings have been incorporated into Section 4.3 (Table 4b) and discussed in Section 5, paragraph 3 (Blocks B0112–B0114)."

---

## 2. Bedah Profil Nada Bahasa Toksik & Transformasi Perbaikan

### Profil 1: Pembelaan Diri yang Defensif (*Combative Pushback*)
- **Penyebab:** Peneliti merasa diserang secara personal atas hasil karyanya.
- **Karakteristik Teks:** Menuduh reviewer tidak membaca dengan teliti, salah paham, atau keliru.

| Sebelum (Defensif / Berisiko Tinggi) | Sesudah (Diplomatis & Persuasif) |
|---|---|
| *"The reviewer completely misunderstood our method. As we already stated in Section 2, our architecture uses cross-attention, so this critique is unfounded."* | *"We appreciate the reviewer's observation. We recognize that our original description in Section 2 did not sufficiently emphasize how the cross-attention mechanism handles this issue. To avoid any ambiguity, we have thoroughly rewritten Section 2.3 to explicitly clarify the attention routing mechanism (see Section 2.3, p. 7, Block B0045)."* |
| *"The reviewer is wrong about our sample size; 100 patients is standard in clinical AI papers."* | *"We thank the reviewer for highlighting the sample size consideration. To provide rigorous justification for our cohort of N=100, we have conducted a formal statistical power analysis (G*Power 3.1) which confirms a statistical power of 0.86 at $\alpha=0.05$. We have also cited three recent benchmark studies in this domain (Smith et al., 2024; Chen et al., 2023) that utilized comparable sample sizes (see Section 3.1, p. 5, Block B0028)."* |

---

### Profil 2: Sikap Menggurui & Meremehkan (*Condescending / Dismissive*)
- **Penyebab:** Penulis merasa memiliki keahlian teknis yang lebih tinggi daripada reviewer.
- **Karakteristik Teks:** Menggunakan frasa *"as any expert knows"*, *"it is obvious that"*, atau *"elementary machine learning principles"*.

| Sebelum (Menggurui / Berisiko Tinggi) | Sesudah (Diplomatis & Persuasif) |
|---|---|
| *"As should be obvious to anyone familiar with deep learning, data augmentation prevents overfitting."* | *"We thank the reviewer for questioning the efficacy of our augmentation pipeline. In response, we have added an explicit ablation experiment comparing models trained with and without our specific augmentation strategy. The empirical results confirm that augmentation yields a 4.2% gain in test AUROC while reducing validation variance (see Table 3a, p. 12)."* |
| *"This is common knowledge in neurology and does not require additional justification."* | *"We appreciate this reminder. To ensure our manuscript is fully accessible to readers across multidisciplinary backgrounds (including computer science and clinical medicine), we have added a concise explanatory paragraph outlining this clinical principle in Section 1.2 (p. 3)."* |

---

### Profil 3: Ambiguitas & Menghindar (*Evasive Handwaving*)
- **Penyebab:** Penulis ingin menyelesaikan revisi dengan cepat tanpa melakukan pekerjaan nyata.
- **Karakteristik Teks:** *"We have addressed this"*, *"Clarified as suggested"*, atau menunda ke *"future work"* tanpa argumen batas yang transparan.

| Sebelum (Ambigual / Berisiko Tinggi) | Sesudah (Diplomatis & Persuasif) |
|---|---|
| *"We have revised the text accordingly."* | *"We thank the reviewer for this suggestion. We have revised the Discussion section to explicitly address the clinical trade-offs of false positives in emergency triage. Specifically, we have added: '[Kutipan 2–3 kalimat baru yang ditambahkan]' (see Section 5.2, p. 16, Block B0140)."* |
| *"Testing on other datasets is left for future work."* | *"We fully agree that multi-center evaluation across diverse imaging protocols is essential for clinical adoption. While acquiring external hospital datasets was beyond our current IRB protocol timeline, we have transparently acknowledged this as a core limitation in Section 5.4 and delineated a structured validation roadmap for future clinical trials (see Section 5.4, p. 18, Block B0155)."* |

---

### Profil 4: Pujian Berlebihan yang Palsu (*Inauthentic Sycophancy*)
- **Penyebab:** Penulis mengira sanjungan berlebihan akan melunakkan hati reviewer yang kritis.
- **Karakteristik Teks:** *"We are eternally indebted to the reviewer's divine wisdom"*, *"The most brilliant feedback we ever received"*.

| Sebelum (Sycophantic / Berisiko Rendah-Sedang) | Sesudah (Diplomatis & Persuasif) |
|---|---|
| *"We are deeply humbled and eternally grateful for the reviewer's brilliant and unrivaled wisdom which completely enlightened our research."* | *"We express our sincere appreciation to Reviewer 2 for this insightful critique, which has significantly enhanced the methodological clarity of our paper."* |

---

## 3. Taktik Menangani Reviewer yang Keliru (*Handling Factual Errors*)

Terkadang, reviewer membuat kesalahan faktual dalam membimbing atau menelaah (misal: mengira model menggunakan arsitektur A padahal naskah menggunakan arsitektur B).

### Tiga Prinsip Diplomasi Menghadapi Kekeliruan Reviewer:
1. **Ambil Tanggung Jawab atas Ambiguitas (*Own the Ambiguity*)**: Asumsikan bahwa reviewer keliru karena cara penulis menyajikan teks awal kurang lugas.
2. **Jangan Menggunakan Kata "Salah" (*Avoid 'Wrong'*)**: Hindari kata *wrong*, *incorrect*, atau *misread*. Gunakan kata *clarify*, *disambiguate*, atau *provide clearer framing*.
3. **Sajikan Bukti Komparatif Netral**: Tunjukkan perbedaannya secara ilmiah melalui tabel atau bagan alir.

**Contoh Kasus:** Reviewer mengira Anda menggunakan CT angiografi (CTA), padahal penelitian menggunakan Non-Contrast CT (NCCT).
> *"We appreciate the opportunity to clarify this point. While CTA is indeed utilized in advanced intervention planning, our study deliberately focuses on Non-Contrast CT (NCCT), as NCCT is the universally available first-line screening modality in emergency departments worldwide. We recognize that our original title and abstract could have highlighted this distinction more prominently. Accordingly, we have updated the title and Section 1 to explicitly emphasize NCCT (see Title and Section 1.1, p. 2, Block B0012)."*
