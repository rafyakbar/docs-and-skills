# Buku Pedoman Format Tabel, Gambar, dan Rumus Matematika (LaTeX Formatting Handbook)

Dokumen ini memuat aturan baku tipografi ilmiah untuk penyusunan elemen visual (tabel dan gambar) serta formulasi matematika dalam naskah publikasi LaTeX internasional.

---

## 1. Aturan Baku Penyajian Data & Tabel (`booktabs`)

### 1.1. Tipografi Bersih Tanpa Garis Vertikal
- **Wajib `booktabs`**: Seluruh tabel wajib menggunakan tiga pembatas horizontal utama: `\toprule` (garis atas tabel), `\midrule` (garis pemisah header dan isi), dan `\bottomrule` (garis penutup tabel).
- **Larangan Garis Vertikal**: DILARANG menggunakan garis vertikal (`|`) pada spesifikasi kolom (misal `{|c|c|}`). Standar jurnal internasional (IEEE, ACM, Springer, Elsevier) melarang garis kisi vertikal.

### 1.2. Format Tabel 1 Kolom (`table`)
Digunakan untuk tabel ramping (2–4 kolom) dengan spesifikasi lebar selebar kolom teks:

```latex
\begin{table}[htbp]
\caption{Performance Comparison Across Evaluated Configurations.}
\label{tab:I}
\centering
\begin{tabular}{lcccc}
\toprule
Model / Method & Accuracy & Precision & Recall & F1-Score \\
\midrule
Baseline A & 0.852 & 0.840 & 0.835 & 0.837 \\
Baseline B & 0.884 & 0.879 & 0.881 & 0.880 \\
\textbf{Proposed (Ours)} & \textbf{0.931} & \textbf{0.928} & \textbf{0.930} & \textbf{0.929} \\
\bottomrule
\end{tabular}
\end{table}
```

### 1.3. Format Tabel 2 Kolom Penuh (`table*`)
Digunakan untuk tabel lebar ($\ge 5$ kolom) yang membentang melintasi kedua kolom halaman:

```latex
\begin{table*}[htbp]
\caption{Comprehensive Comparison with Existing Benchmark Studies.}
\label{tab:II}
\centering
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lcccccc}
\toprule
Method & Backbone & Parameter Count & Accuracy & Precision & Recall & F1-Score \\
\midrule
Method X & ResNet-50 & 25.6M & 0.882 & 0.875 & 0.880 & 0.877 \\
Method Y & ViT-Base & 86.0M & 0.914 & 0.910 & 0.912 & 0.911 \\
\textbf{Tri-Domain ViT (Ours)} & \textbf{ViT-Base} & \textbf{86.0M} & \textbf{0.937} & \textbf{0.935} & \textbf{0.936} & \textbf{0.935} \\
\bottomrule
\end{tabular*}
\end{table*}
```

### 1.4. Aturan Penempatan Caption Tabel
- Caption tabel **WAJIB berada di ATAS** tabel (`\caption` sebelum `\begin{tabular}`).
- Nilai metrik terbaik ditebalkan dengan `\textbf{...}`.
- Perujukan dalam teks menggunakan `Table~\ref{tab:X}` (dengan spasi non-breaking `~`).

---

## 2. Aturan Baku Penyajian Gambar (Figures)

### 2.1. Aturan Kritis: Posisi Caption SEBELUM Label
> [!CAUTION]
> Pada lingkungan gambar (`figure` atau `figure*`), perintah `\caption{...}` **WAJIB diletakkan SEBELUM** `\label{fig:...}`.  
> Jika posisi terbalik (`\label` sebelum `\caption`), kompilator LaTeX akan meregistrasikan nomor seksi bab sebagai rujukan, bukan nomor gambar!

### 2.2. Gambar 1 Kolom (`figure`)
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{architecture.png}
\caption{Architecture of the Proposed Neural Framework.}
\label{fig:1}
\end{figure}
```

### 2.3. Gambar 2 Kolom Penuh (`figure*`)
```latex
\begin{figure*}[htbp]
\centering
\includegraphics[width=\textwidth]{pipeline_overview.png}
\caption{Overall Workflow and Experimental Pipeline Across Evaluation Cohorts.}
\label{fig:2}
\end{figure*}
```

### 2.4. Grid Multi-Subfigure (2 Kolom)
```latex
\begin{figure}[htbp]
\centering
\begin{subfigure}[b]{0.48\columnwidth}
  \centering
  \includegraphics[width=\linewidth]{images/sample_Asian.jpg}
  \caption{Asian Cohort}
  \label{fig:3a}
\end{subfigure}\hfill
\begin{subfigure}[b]{0.48\columnwidth}
  \centering
  \includegraphics[width=\linewidth]{images/sample_Black.jpg}
  \caption{Black Cohort}
  \label{fig:3b}
\end{subfigure}
\caption{Sample Facial Images across Demographic Cohorts.}
\label{fig:3}
\end{figure}
```

---

## 3. Formulasi Persamaan Matematika (Equations)

### 3.1. Lingkungan Persamaan Bernomor
```latex
\begin{equation}
\mathbf{y} = \sigma(\mathbf{W} \mathbf{x} + \mathbf{b})
\label{eq:1}
\end{equation}
```
Rujuk di dalam teks menggunakan perintah `\eqref{eq:1}` (bukan `\ref`).

### 3.2. Kewajiban Penjelasan Simbol Variabel
Setiap kali rumus dirujuk di dalam paragraf, kalimat tersebut **wajib** menjelaskan arti variabel penyusunnya:
> *"Mekanisme klasifikasi dirumuskan pada \eqref{eq:1}, di mana $\mathbf{x} \in \mathbb{R}^d$ menyatakan vektor fitur input, $\mathbf{W}$ adalah matriks bobot proyeksi, $\mathbf{b}$ merupakan vektor bias, dan $\sigma(\cdot)$ menyatakan fungsi aktivasi non-linier."*

### 3.3. Penulisan Dimensi & Simbol Sederhana dalam Teks Narasi
Untuk operasi aritmetika sederhana, dimensi, atau toleransi, gunakan teks biasa tanpa mode matematika:
- **Dimensi**: berukuran 224 × 224 piksel (simbol unicode `×`, bukan `$\times$`).
- **Penjumlahan Dimensi**: 1024 + 768 = 1792 (teks biasa).
- **Rentang & Toleransi**: ±5%, ±10° (simbol `±` dan `°`, bukan `$\pm$`).
- **Rasio**: 80/10/10 atau 0.8 / 0.2 (teks biasa).
- Mode matematika (`$...$`) dikhususkan untuk variabel simbolik murni: $\mathbf{z}$, $\mu$, $\sigma^2$, $\mathbf{W}$.

---

## 4. Aturan Tanpa-Yatim (*Zero-Orphan Rule*)

Dilarang menyematkan elemen visual atau matematis yang tidak dirujuk dalam naskah:
- Setiap `\label{fig:X}` WAJIB dirujuk dengan `Figure~\ref{fig:X}` di dalam paragraf.
- Setiap `\label{tab:X}` WAJIB dirujuk dengan `Table~\ref{tab:X}` di dalam paragraf.
- Setiap `\label{eq:X}` WAJIB dirujuk dengan `\eqref{eq:X}` di dalam paragraf.
- Setiap entri di `references.bib` WAJIB disitasi dengan `\cite{...}` di dalam naskah.
