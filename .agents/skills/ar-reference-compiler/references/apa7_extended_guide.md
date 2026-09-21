# Panduan Standar Kompilasi Referensi APA Edisi ke-7 (APA 7th Reference Guide)

Dokumen ini mendefinisikan aturan penyusunan naskah daftar pustaka berbasis standar resmi APA (*American Psychological Association*) Edisi ke-7, mencakup aturan penulis tunggal hingga jamak (21+ penulis), pengurutan alfabetis, format berbagai tipe media, dan standardisasi tautan aktif DOI.

---

## 1. Karakteristik Utama Daftar Pustaka APA 7th

1. **Pengurutan Alfabetis (*Alphabetical Ordering*)**:
   - Berbeda dengan IEEE yang memakai urutan kemunculan, APA 7th mengurutkan daftar referensi secara **alfabetis berdasarkan nama belakang penulis pertama** (*first author's surname*).
   - Jika terdapat beberapa karya oleh penulis pertama yang persis sama, urutkan berdasarkan **tahun terbit** (dari yang paling lama ke yang terbaru).
   - Jika penulis dan tahun sama, tambahkan huruf kecil setelah tahun: `2023a`, `2023b`.
2. **Struktur Penulis**:
   - Nama belakang diikuti inisial nama depan dan tengah: `Smith, J. A.`.
   - Gunakan simbol ampersand (`&`) sebelum penulis terakhir: `Rusia, M. K., & Singh, D. K.`.
   - **Karya hingga 20 Penulis**: Sebutkan seluruh nama penulis (hingga 20 orang) tanpa disingkat *et al.*
   - **Karya dengan 21 Penulis atau Lebih**: Tuliskan 19 penulis pertama, tanda elipsis tiga titik (`...`), lalu nama penulis paling akhir.
3. **Format Judul & Wadah**:
   - Judul artikel atau bab buku: **Sentence case**, huruf tegak, tanpa tanda petik.
   - Judul jurnal / prosiding: *Italic*, **Title Case penuh**, diikuti volume dalam format *Italic*, dan nomor edisi dalam tanda kurung tegak: `*Multimedia Tools and Applications*, *82*(2), 1669–1748`.
4. **Format DOI**:
   - Wajib ditulis sebagai tautan aktif HTTPS penuh: `https://doi.org/10.xxxx/...` (tanpa tanda titik di akhir).

---

## 2. Aturan Penulis Khusus

### A. Karya dengan 21 Penulis atau Lebih
Pada daftar pustaka APA 7th, tuliskan 19 penulis pertama, diikuti tanda elipsis tiga titik (`...`), lalu diakhiri oleh nama penulis paling akhir:
```text
Author, A. A., Author, B. B., Author, C. C., Author, D. D., Author, E. E., Author, F. F.,
Author, G. G., Author, H. H., Author, I. I., Author, J. J., Author, K. K., Author, L. L.,
Author, M. M., Author, N. N., Author, O. O., Author, P. P., Author, Q. Q., Author, R. R.,
Author, S. S., ... Author, Z. Z. (2024). Title of massive collaboration paper. *Journal of Big Science*, *10*(1), 1–25. https://doi.org/10.xxxx/...
```

### B. Penulis Berupa Organisasi / Institusi (*Group Authors*)
Tuliskan nama lengkap institusi tanpa singkatan pada daftar pustaka:
```text
World Health Organization. (2024). *Global status report on biometric identity systems*. World Health Organization. https://www.who.int/...
```

### C. Karya Tanpa Penulis
Tempatkan judul karya pada posisi penulis:
```text
Comprehensive study of face biometrics. (2023). *Biometric Review*, *15*(3), 45–60. https://doi.org/10.xxxx/...
```

---

## 3. Format Baku Berbagai Tipe Publikasi

### A. Artikel Jurnal (*Journal Article*)
**Struktur**:
```text
<a id="ref{N}"></a>
{Authors}. ({Year}). {Article title}. *{Journal Name}*, *{Volume}*({Issue}), {Pages}. https://doi.org/{DOI}
```
**Contoh**:
```markdown
<a id="ref1"></a>
Rusia, M. K., & Singh, D. K. (2023). A comprehensive survey on techniques to handle face identity threats: challenges and opportunities. *Multimedia Tools and Applications*, *82*(2), 1669–1748. https://doi.org/10.1007/s11042-022-13248-6

<a id="ref2"></a>
Meden, B., Rot, P., Terhörst, P., Damer, N., Kuijper, A., Scheirer, W. J., Ross, A., Peer, P., & Štruc, V. (2021). Privacy-enhancing face biometrics: a comprehensive survey. *IEEE Transactions on Information Forensics and Security*, *16*, 4147–4183. https://doi.org/10.1109/TIFS.2021.3096024
```

### B. Makalah Prosiding Konferensi Terbit Berkala (*Conference Proceedings as Journal*)
Jika prosiding diterbitkan secara berkala, format persis seperti artikel jurnal:
```markdown
<a id="ref14"></a>
Brinkmann, J., Swoboda, P., & Bartelt, C. (2023). A multidimensional analysis of social biases in vision transformers. *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 4891–4900. https://doi.org/10.1109/ICCV51070.2023.00453
```

### C. Buku Lengkap & Bab dalam Buku (*Book & Book Chapter*)
**Buku Utuh**:
```text
Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep learning*. MIT Press.
```
**Bab dalam Buku Kumpulan Tulisan (*Edited Book Chapter*)**:
```text
Ramachandran, S., & Rattani, A. (2023). Deep generative views to mitigate gender classification bias across gender-race groups. In J.-J. Rousseau & B. Kapralos (Eds.), *Pattern recognition, computer vision, and image processing* (pp. 551–569). Springer. https://doi.org/10.1007/978-3-031-37731-0_40
```

### D. Naskah Pra-Cetak (*Preprint* arXiv)
**Struktur**:
```text
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). *Attention is all you need*. arXiv. https://doi.org/10.48550/arXiv.1706.03762
```

### E. Halaman Web / Situs Berita Sains
**Struktur**:
```text
Birhane, A. (2022, October 19). *The unseen Black faces of AI algorithms*. Nature. https://doi.org/10.1038/d41586-022-03050-7
```

---

## 4. Format Hanging Indent pada Markdown

Dalam APA 7th resmi, daftar pustaka dicetak dengan format *hanging indent* (baris pertama rata kiri, baris kedua dan seterusnya menjorok 0.5 inci). Dalam berkas Markdown `06_references.md`, keterbacaan dipertahankan melalui pemisahan baris kosong antar-entri rujukan dan penomoran anchor `<a id="ref{N}"></a>`.
