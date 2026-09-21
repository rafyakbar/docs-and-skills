# Pengalih Format Sitasi & Bibliografi (Citation Format Switcher)

Dokumen ini menyediakan matriks komparasi, aturan transformasi struktural, dan pedoman konversi antar **5 gaya sitasi akademis utama** (IEEE, APA 7th, Harvard, ACM, Vancouver) saat menyusun naskah daftar pustaka `paper/06_references.md`.

---

## 1. Matriks Komparasi 5 Gaya Sitasi

| Karakteristik | IEEE | APA 7th | Harvard | ACM | Vancouver |
|:---|:---|:---|:---|:---|:---|
| **Disiplin Utama** | Ilmu Komputer, Elektro, AI | Psikologi, Sosial, Bisnis | Multidisiplin, Humaniora | Ilmu Komputer / ACM | Kedokteran, Kesehatan |
| **Judul Bagian** | `# REFERENCES` / `# VI. REFERENCES` | `# References` | `# References` | `# REFERENCES` | `# References` |
| **Urutan Entri** | **Urutan Kemunculan** (*First Appearance*) | **Alfabetis** (Nama Belakang) | **Alfabetis** (Nama Belakang) | **Urutan Kemunculan** / Alfabetis | **Urutan Kemunculan** (*First Appearance*) |
| **Bentuk Penomoran** | `[1]`, `[2]`, ... | Tanpa nomor (Hanging indent) | Tanpa nomor (Hanging indent) | `[1]`, `[2]`, ... | `1.`, `2.`, ... |
| **Urutan Nama Penulis** | Inisial di depan: `J. A. Smith` | Nama belakang di depan: `Smith, J. A.` | Nama belakang di depan: `Smith, J.A.` | Nama lengkap: `John A. Smith` | Nama belakang di depan: `Smith JA` |
| **Tanda Hubung Jamak** | `"and"` | `"&"` | `"and"` | `"and"` | `","` (tanpa kata hubung) |
| **Batas Et Al.** | $\ge 6$ penulis $\rightarrow$ `First et al.` | $\ge 21$ penulis $\rightarrow$ `19, ... Last` | $\ge 4$ penulis $\rightarrow$ `First et al.` | $\ge 3$ penulis $\rightarrow$ `First et al.` | $\ge 7$ penulis $\rightarrow$ sebut 6, lalu `et al.` |
| **Tanda Petik Judul** | Ada (`"Article Title,"`) | Tidak ada (`Article title.`) | Petik tunggal (`'Article title.'`)| Ada (`"Article Title."`) | Tidak ada (`Article title.`) |
| **Kapitalisasi Judul** | **Sentence case** | **Sentence case** | **Sentence case** | **Title case** | **Sentence case** |
| **Format DOI** | `doi: 10.xxxx/...` | `https://doi.org/10.xxxx/...` | `https://doi.org/10.xxxx/...` | `https://doi.org/10.xxxx/...` | `doi: 10.xxxx/...` |

---

## 2. Struktur Transformasi per Entri Rujukan

Berikut contoh transformasi entri rujukan yang sama (Rusia & Singh, 2023) ke dalam 5 gaya sitasi:

### A. Format IEEE (Standar Engineering & CS)
```markdown
<a id="ref1"></a>
[1] M. K. Rusia and D. K. Singh, "A comprehensive survey on techniques to handle face identity threats: challenges and opportunities," *Multimedia Tools and Applications*, vol. 82, no. 2, pp. 1669-1748, Jan. 2023, doi: 10.1007/s11042-022-13248-6.
```

### B. Format APA 7th (Standar Psikologi & Sains Sosial)
```markdown
<a id="ref1"></a>
Rusia, M. K., & Singh, D. K. (2023). A comprehensive survey on techniques to handle face identity threats: challenges and opportunities. *Multimedia Tools and Applications*, *82*(2), 1669–1748. https://doi.org/10.1007/s11042-022-13248-6
```

### C. Format Harvard (Standar Multidisiplin Internasional)
```markdown
<a id="ref1"></a>
Rusia, M.K. and Singh, D.K., 2023. 'A comprehensive survey on techniques to handle face identity threats: challenges and opportunities', *Multimedia Tools and Applications*, 82(2), pp. 1669-1748. https://doi.org/10.1007/s11042-022-13248-6.
```

### D. Format ACM (Standar Association for Computing Machinery)
```markdown
<a id="ref1"></a>
[1] Mayank Kumar Rusia and Dushyant Kumar Singh. 2023. "A Comprehensive Survey on Techniques to Handle Face Identity Threats: Challenges and Opportunities." *Multimedia Tools and Applications* 82, 2 (Jan. 2023), 1669–1748. https://doi.org/10.1007/s11042-022-13248-6
```

### E. Format Vancouver (Standar Biomedis & Kedokteran)
```markdown
<a id="ref1"></a>
1. Rusia MK, Singh DK. A comprehensive survey on techniques to handle face identity threats: challenges and opportunities. Multimedia Tools and Applications. 2023;82(2):1669-1748. doi: 10.1007/s11042-022-13248-6
```

---

## 3. Logika Pemilihan Gaya Sitasi

Gunakan aturan keputusan berikut saat menentukan format kompilasi:

```text
Apakah bidang riset berfokus pada Teknik Elektro, Ilmu Komputer, atau Kecerdasan Buatan?
├── YA  ──> Gunakan IEEE (Gaya Default Repositori). Urutan: Order of First Appearance.
└── TIDAK ──> Apakah jurnal target berafiliasi dengan Elsevier / Multidisiplin / Sains Sosial?
              ├── YA ──> Gunakan APA 7th atau Harvard. Urutan: Alfabetis.
              └── TIDAK ──> Apakah jurnal biomedis / kesehatan (PubMed/NLM)?
                            └── YA ──> Gunakan Vancouver. Urutan: Order of Appearance.
```

---

## 4. Pelestarian Anchor HTML Lintas Gaya

Apapun gaya sitasi yang dipilih (bernomor seperti IEEE atau berbasis pengarang-tahun seperti APA), **tag `<a id="ref{N}"></a>` wajib selalu disematkan** di awal setiap entri pada `06_references.md`. Hal ini memastikan bahwa tautan rujukan dari naskah bab draf tetap berfungsi secara universal.
