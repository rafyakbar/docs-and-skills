# Contoh Format Berkas Pemetaan Sitasi (Contoh Ilustratif)

> [!IMPORTANT]
> **Berkas Referensi Contoh Murni Ilustratif**
> Potongan teks di bawah ini menyajikan contoh mandiri (*self-contained exemplar*) mengenai format penyusunan berkas pemetaan sitasi `paper/references.txt` beserta contoh isi berkas catatan bibliografi (`.bib` dan `.ris`).
> Seluruh judul dan kalimat disajikan murni untuk tujuan ilustrasi format. Saat menjalankan proses kurasi riil, sesuaikan kalimat klaim dan paper rujukan secara spesifik dengan topik riset pengguna.

---

## 1. Contoh Berkas Pemetaan: `paper/references.txt`

```text
paper/01_introduction.md: paragraf 1:
- "Pengenalan otomatis atribut demografis wajah memegang peranan penting dalam berbagai domain aplikasi cerdas, termasuk sistem forensik digital, kontrol akses biometrik, interaksi manusia-komputer, dan personalisasi layanan interaktif":
  - paper/references/2022_A comprehensive survey on techniques to handle face identity threats challenges and opportunities.ris
  - paper/references/2021_Privacy–Enhancing Face Biometrics A Comprehensive Survey.bib
- "Namun, sejumlah studi melaporkan adanya disparitas performa pada subkelompok demografis tertentu, termasuk perempuan dan individu dengan warna kulit lebih gelap":
  - paper/references/2022_The unseen Black faces of AI algorithms.nbib
  - paper/references/2024_Reinvention mediates impacts of skin tone bias in algorithms implications for technology diffusion.bib
- "Ketimpangan tersebut dapat dipengaruhi oleh berbagai faktor, termasuk ketidakseimbangan distribusi data dan keterbatasan representasi fitur terhadap variasi visual":
  - paper/references/2022_A Comprehensive Study on Face Recognition Biases Beyond Demographics.bib

paper/01_introduction.md: paragraf 2:
- "Sebagian pendekatan pengenalan atribut wajah memodelkan atribut secara terpisah, sedangkan multi-task learning memungkinkan beberapa atribut dipelajari secara simultan":
  - paper/references/2023_Facial attribute classification by deep mining inter-attribute correlations.bib
- "Pemodelan atribut secara terpisah dapat membatasi analisis terhadap kelompok yang terbentuk dari kombinasi atribut, seperti ras dan gender":
  - paper/references/2022_Racial, skin tone, and sex disparities in automated proctoring software.bib
  - paper/references/2022_Gender and race classification using geodesic distance measurement.bib
- "Akibatnya, metrik agregat berpotensi tidak menangkap disparitas performa pada subkelompok tertentu":
  - paper/references/2023_Balancing Biases and Preserving Privacy on Balanced Faces in the Wild.nbib
- "Evaluasi pada subkelompok demografis dengan representasi yang seimbang secara terkontrol dapat menyediakan landasan komparatif yang lebih konsisten dan objektif untuk mengukur variasi performa antarkelompok":
  - paper/references/2023_Balancing Biases and Preserving Privacy on Balanced Faces in the Wild.nbib
- "Pemodelan interseksional juga menghadapi tantangan representasi karena karakteristik wajah dan ekspresi dapat bervariasi antar kelompok demografis, sehingga diperlukan representasi visual yang mampu mempertahankan informasi diskriminatif sekaligus robust terhadap variasi tersebut":
  - paper/references/2021_Racial Identity-Aware Facial Expression Recognition Using Deep Convolutional Neural Networks.bib

paper/01_introduction.md: paragraf 3:
- "Pada era arsitektur Convolutional Neural Networks (CNN), berbagai penelitian mengeksplorasi ekstraksi ciri demografis melalui pemanfaatan region spesifik wajah seperti area wajah bagian tengah, kerangka kerja multi-tugas berbasis multi-skala untuk estimasi usia dan gender secara simultan, serta model CNN mendalam untuk pengenalan etnisitas":
  - paper/references/2022_Automatic Ethnicity Classification from Middle Part of the Face Using Convolutional Neural Networks.bib
  - paper/references/2022_Face Gender and Age Classification Based on Multi-Task, Multi-Instance and Multi-Scale Learning.bib
  - paper/references/2022_Intelligent deep learning based ethnicity recognition and classification using facial images.bib
- "ViT mampu memodelkan hubungan global antarpatch melalui Multi-Head Self-Attention (MHSA), sehingga berpotensi menghasilkan representasi visual yang lebih kontekstual, sementara pemanfaatan representasi generatif sintetis turut dikembangkan untuk memitigasi disparitas demografis":
  - paper/references/2023_A Multidimensional Analysis of Social Biases in Vision Transformers.bib
  - paper/references/2023_Deep Generative Views to Mitigate Gender Classification Bias Across Gender-Race Groups.bib
```

---

## 2. Contoh Berkas Rekaman Bibliografi

### Contoh Berkas BibTeX: `paper/references/2021_Privacy–Enhancing Face Biometrics A Comprehensive Survey.bib`

```bibtex
@Article{biometrics2021survey,
  AUTHOR = {Smith, John and Doe, Jane and Al-Mansoor, Tariq},
  TITLE = {Privacy-Enhancing Face Biometrics: A Comprehensive Survey},
  JOURNAL = {IEEE Transactions on Information Forensics and Security},
  VOLUME = {16},
  YEAR = {2021},
  PAGES = {1042-1057},
  DOI = {10.1109/TIFS.2021.3051234}
}
```

### Contoh Berkas RIS: `paper/references/2022_A comprehensive survey on techniques to handle face identity threats challenges and opportunities.ris`

```text
TY  - JOUR
TI  - A comprehensive survey on techniques to handle face identity threats: challenges and opportunities
AU  - Zhang, Wei
AU  - Kumar, Rajesh
AU  - Patel, Ananya
JO  - Information Fusion
VL  - 85
SP  - 120
EP  - 142
PY  - 2022
DO  - 10.1016/j.inffus.2022.03.015
ER  - 
```
