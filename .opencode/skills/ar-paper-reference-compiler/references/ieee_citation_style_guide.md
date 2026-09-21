# Panduan Standar Sitasi IEEE (IEEE Citation Style Guide)

Dokumen ini memuat spesifikasi lengkap pemformatan daftar pustaka berbasis standar resmi IEEE (*Institute of Electrical and Electronics Engineers*), mencakup struktur entri, aturan singkatan, penanganan penulis jamak (*et al.*), tag anchor HTML, dan contoh riil dari publikasi ilmiah internasional.

---

## 1. Karakteristik Utama Format IEEE

1. **Sistem Numerik Berurutan Kemunculan (*Order of Appearance*)**:
   - Nomor referensi `[1], [2], [3]` ditentukan berdasarkan urutan pertama kali rujukan tersebut muncul di dalam teks naskah / pemetaan `references.txt`.
   - Rujukan yang dikutip berulang kali tetap menggunakan nomor kemunculan pertamanya.
2. **Struktur Penulis**:
   - Inisial nama depan dan tengah ditempatkan di depan nama belakang: `J. A. Smith`.
   - Dua penulis: `M. K. Rusia and D. K. Singh`.
   - Tiga hingga lima penulis: `J. Brinkmann, P. Swoboda, and C. Bartelt`.
   - **Enam penulis atau lebih**: Tuliskan nama penulis pertama diikuti singkatan *et al.*: `B. Meden et al.`.
3. **Tipografi Judul**:
   - Judul artikel jurnal, bab buku, atau makalah konferensi diapit oleh **tanda kutip ganda** `"..."` dan menggunakan kapitalisasi **Sentence case** (kecuali huruf pertama setelah titik dua dan kata benda khusus / akronim).
   - Judul jurnal, nama prosiding, atau judul buku ditulis dengan format **cetak miring (*Italics*)**.
4. **Format DOI & URL**:
   - DOI ditulis dengan format: `doi: 10.xxxx/...` (tanpa `https://doi.org/`).
   - Sumber daring ditulis: `[Online]. Available: URL. [Accessed: DD-Mmm-YYYY]`.

---

## 2. Format Baku per Jenis Publikasi

### A. Artikel Jurnal Ilmiah (*Journal Article*)
**Struktur**:
```text
<a id="ref{N}"></a>
[{N}] {Authors}, "{Article Title}," *{Journal Name}*, vol. {Vol}, no. {Issue}, pp. {Pages}, {Month} {Year}, doi: {DOI}.
```
**Contoh Riil**:
```markdown
<a id="ref1"></a>
[1] M. K. Rusia and D. K. Singh, "A comprehensive survey on techniques to handle face identity threats: challenges and opportunities," *Multimedia Tools and Applications*, vol. 82, no. 2, pp. 1669-1748, Jan. 2023, doi: 10.1007/s11042-022-13248-6.

<a id="ref2"></a>
[2] B. Meden et al., "Privacy-enhancing face biometrics: a comprehensive survey," *IEEE Transactions on Information Forensics and Security*, vol. 16, pp. 4147-4183, 2021, doi: 10.1109/TIFS.2021.3096024.
```

### B. Artikel dengan Nomor Elektronik (*Article Number*)
Jika jurnal tidak menggunakan rentang halaman tradisional melainkan nomor artikel:
**Struktur**:
```text
<a id="ref{N}"></a>
[{N}] {Authors}, "{Article Title}," *{Journal Name}*, vol. {Vol}, no. {Issue}, Art. no. {ArticleNumber}, {Month} {Year}, doi: {DOI}.
```
**Contoh Riil**:
```markdown
<a id="ref10"></a>
[10] M. Sohail et al., "Racial identity-aware facial expression recognition using deep convolutional neural networks," *Applied Sciences*, vol. 12, no. 1, Art. no. 88, 2022, doi: 10.3390/app12010088.

<a id="ref13"></a>
[13] G. Sunitha, K. Geetha, S. Neelakandan, A. K. S. Pundir, S. Hemalatha, and V. Kumar, "Intelligent deep learning based ethnicity recognition and classification using facial images," *Image and Vision Computing*, vol. 121, Art. no. 104404, 2022, doi: 10.1016/j.imavis.2022.104404.
```

### C. Makalah Prosiding Konferensi / Seminar (*Conference Proceedings*)
**Struktur**:
```text
<a id="ref{N}"></a>
[{N}] {Authors}, "{Paper Title}," in *{Conference Proceedings Name}*, {Conference City}, {Conference Country}, {Year}, pp. {Pages}, doi: {DOI}.
```
**Contoh Riil**:
```markdown
<a id="ref14"></a>
[14] J. Brinkmann, P. Swoboda, and C. Bartelt, "A multidimensional analysis of social biases in vision transformers," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, Paris, France, 2023, pp. 4891-4900, doi: 10.1109/ICCV51070.2023.00453.

<a id="ref19"></a>
[19] R. A. Putri, L. Anifah, R. E. Putra, Y. Yamasari, and R. A. Akbar, "Dual vision transformer integration for race and gender recognition based on facial images," in *Proc. 2025 8th Int. Conf. Vocational Educ. Elect. Eng. (ICVEE)*, Surabaya, Indonesia, 2025, pp. 258-264, doi: 10.1109/ICCVEE66651.2025.11281432.
```

### D. Buku & Bagian Buku (*Book & Book Chapter*)
**Struktur Buku**:
```text
<a id="ref{N}"></a>
[{N}] {Authors}, *{Book Title}*, {Edition} ed. {City}, {Country}: {Publisher}, {Year}.
```
**Struktur Bab Buku (Book Chapter)**:
```text
<a id="ref{N}"></a>
[{N}] {Authors}, "{Chapter Title}," in *{Book Title}*, {Editors}, Eds., {City}, {Country}: {Publisher}, {Year}, pp. {Pages}, doi: {DOI}.
```
**Contoh Riil**:
```markdown
<a id="ref15"></a>
[15] S. Ramachandran and A. Rattani, "Deep generative views to mitigate gender classification bias across gender-race groups," in *Pattern Recognition, Computer Vision, and Image Processing. ICPR 2022 International Workshops and Challenges*, J.-J. Rousseau and B. Kapralos, Eds., Cham, Switzerland: Springer, 2023, pp. 551-569, doi: 10.1007/978-3-031-37731-0_40.
```

### E. Naskah Pra-Cetak (*Preprint* arXiv / bioRxiv)
**Struktur**:
```text
<a id="ref{N}"></a>
[{N}] {Authors}, "{Paper Title}," {Year}, arXiv:{arXiv_ID}. [Online]. Available: https://arxiv.org/abs/{arXiv_ID}
```
**Contoh**:
```markdown
<a id="ref25"></a>
[25] A. Vaswani et al., "Attention is all you need," 2017, arXiv:1706.03762. [Online]. Available: https://arxiv.org/abs/1706.03762
```

### F. Standar Teknis & Laporan Riset (*Standard / Technical Report*)
**Struktur**:
```text
<a id="ref{N}"></a>
[{N}] {Corporate Author}, *{Standard / Report Title}*, {Standard Number}, {Year}.
```
**Contoh**:
```markdown
<a id="ref26"></a>
[26] IEEE Standards Association, *IEEE Standard for Information Technology—Telecommunications and Information Exchange Between Systems*, IEEE Standard 802.11-2020, 2021.
```

---

## 3. Singkatan Resmi Nama Bulan IEEE

Pada format IEEE, nama bulan disingkat secara baku:
- Januari $\rightarrow$ `Jan.`
- Februari $\rightarrow$ `Feb.`
- Maret $\rightarrow$ `Mar.`
- April $\rightarrow$ `Apr.`
- Mei $\rightarrow$ `May`
- Juni $\rightarrow$ `June`
- Juli $\rightarrow$ `July`
- Agustus $\rightarrow$ `Aug.`
- September $\rightarrow$ `Sept.`
- Oktober $\rightarrow$ `Oct.`
- November $\rightarrow$ `Nov.`
- Desember $\rightarrow$ `Dec.`

---

## 4. Format Anchor Tag HTML & Integrasi dengan Step 4

Setiap rujukan pada `paper/06_references.md` diawali oleh anchor tag HTML `<a id="ref{N}"></a>`:
```markdown
<a id="ref1"></a>
[1] ...
```
Tujuannya adalah agar pada **Step 4 (`ar-paper-citation-numbering`)**, kalimat draf naskah dapat mengarah langsung ke entri yang bersangkutan secara mulus:
```markdown
Metode pengenalan wajah cerdas telah berkembang pesat [[1]](06_references.md#ref1).
```
Pembaca yang mengklik link `[1]` pada browser atau PDF viewer markdown akan langsung diarahkan (*jump*) ke entri rujukan bersangkutan.
