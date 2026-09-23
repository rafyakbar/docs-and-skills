# Paket Contoh Konversi LaTeX (Sample LaTeX Conversion Package)

Dokumen ini mendemonstrasikan eksekusi konversi naskah Markdown modular (`paper/*.md`) ke proyek **LaTeX modular siap submit** secara lengkap (*end-to-end*), mencakup berkas masukan Markdown, berkas keluaran `.tex` yang dihasilkan, laporan konversi JSON, serta hasil verifikasi linter penjaminan mutu.

---

## 1. Berkas Masukan Markdown

### 1.1. `paper/00_abstract.md`
```markdown
# Abstract

Intersectional facial demographic analysis poses significant challenges for conventional deep learning architectures due to subtle biometric and expressive variations across demographic cohorts. This study proposes a Tri-Domain Vision Transformer feature fusion framework integrating face biometric, expression, and age representations into a unified latent vector. Evaluated on the DemogPairs benchmark dataset across six intersectional subgroups, the proposed framework achieves an overall classification accuracy of 93.70% and a macro F1-score of 0.935, reducing False Positive Disparities compared to conventional single-domain baselines.

**Keywords**: Demographic classification, Vision Transformer, feature fusion, algorithmic fairness, facial analysis.
```

### 1.2. `paper/01_introduction.md`
```markdown
# Section I: Introduction

<!--block:B0001-->
Automated demographic recognition from facial images plays a pivotal role in digital forensics, biometric access control, and human-computer interaction [[1]](06_references.md#ref1), [[2]](06_references.md#ref2). However, demographic disparities across gender and racial intersections continue to challenge real-world deployments [[3]](06_references.md#ref3). Conventional convolutional neural networks often fail to capture fine-grained affective cues, leading to performance gaps on underrepresented cohorts [[4]](06_references.md#ref4).

<!--block:B0002-->
The proposed pipeline is outlined in [Figure 1](#fig1). As detailed in Section III, three pre-trained Vision Transformer backbones extract latent feature vectors that are subsequently classified through optimized classical models.

<a id="fig1"></a>
**Figure 1. End-to-End Architecture of the Proposed Framework.**

![End-to-End Architecture of the Proposed Framework](images/overview.png)
```

### 1.3. `paper/03_materials-and-methods_c-random-forest.md`
```markdown
## C. Random Forest

<a id="tab3"></a>
**Table III. Hyperparameter Search Space for Random Forest Classifier.**

| Component / Hyperparameter | Evaluated Values | Count |
|---|---|:---:|
| Feature Scaler | `None`, `MinMaxScaler` | 2 |
| Dimensionality Reduction (PCA) | `None`, `0.50`, `0.75` | 3 |
| Number of Trees | 100, 200 | 2 |
| **Total Grid Combinations** | - | **288 (1,440 fits)** |

The Random Forest model aggregates predictions across decision trees optimized via 5-Fold Stratified Cross-Validation as summarized in [Table III](#tab3). Formally, the decision tree ensemble prediction is obtained by:

<a id="eq1"></a>
$$
\hat{y} = \operatorname{argmax}_{c} \sum_{b=1}^{B} I(T_b(\mathbf{x}) = c) \tag{1}
$$

where $\mathbf{x}$ represents the input latent vector, $B$ is the number of trees, and $T_b(\mathbf{x})$ denotes the class prediction of tree $b$ [[5]](06_references.md#ref5).
```

---

## 2. Perintah Eksekusi Konversi

Jalankan skrip konversi:
```bash
python scripts/ars_latex_converter.py \
  --paper-dir paper \
  --output-dir paper_latex \
  --template ieeeaccess
```

---

## 3. Berkas Keluaran LaTeX yang Dihasilkan

### 3.1. `paper_latex/sections/00_abstract.tex`
```latex
\begin{abstract}
Intersectional facial demographic analysis poses significant challenges for conventional deep learning architectures due to subtle biometric and expressive variations across demographic cohorts. This study proposes a Tri-Domain Vision Transformer feature fusion framework integrating face biometric, expression, and age representations into a unified latent vector. Evaluated on the DemogPairs benchmark dataset across six intersectional subgroups, the proposed framework achieves an overall classification accuracy of 93.70\% and a macro F1-score of 0.935, reducing False Positive Disparities compared to conventional single-domain baselines.
\end{abstract}

\begin{keywords}
Demographic classification, Vision Transformer, feature fusion, algorithmic fairness, facial analysis.
\end{keywords}
```

### 3.2. `paper_latex/sections/01_introduction.tex`
```latex
\section{Introduction}
\label{sec:introduction}

Automated demographic recognition from facial images plays a pivotal role in digital forensics, biometric access control, and human-computer interaction \cite{ref1, ref2}. However, demographic disparities across gender and racial intersections continue to challenge real-world deployments \cite{ref3}. Conventional convolutional neural networks often fail to capture fine-grained affective cues, leading to performance gaps on underrepresented cohorts \cite{ref4}.

The proposed pipeline is outlined in Figure~\ref{fig:1}. As detailed in Section III, three pre-trained Vision Transformer backbones extract latent feature vectors that are subsequently classified through optimized classical models.

\begin{figure*}[htbp]
\centering
\includegraphics[width=\textwidth]{overview.png}
\caption{End-to-End Architecture of the Proposed Framework.}
\label{fig:1}
\end{figure*}
```

### 3.3. `paper_latex/sections/03_materials-and-methods_c-random-forest.tex`
```latex
\subsection{Random Forest}
\label{sec:random_forest}

\begin{table}[htbp]
\caption{Hyperparameter Search Space for Random Forest Classifier.}
\label{tab:3}
\centering
\begin{tabular}{llc}
\toprule
Component / Hyperparameter & Evaluated Values & Count \\
\midrule
Feature Scaler & None, MinMaxScaler & 2 \\
Dimensionality Reduction (PCA) & None, 0.50, 0.75 & 3 \\
Number of Trees & 100, 200 & 2 \\
\textbf{Total Grid Combinations} & - & \textbf{288 (1,440 fits)} \\
\bottomrule
\end{tabular}
\end{table}

The Random Forest model aggregates predictions across decision trees optimized via 5-Fold Stratified Cross-Validation as summarized in Table~\ref{tab:3}. Formally, the decision tree ensemble prediction is obtained by:

\begin{equation}
\hat{y} = \operatorname{argmax}_{c} \sum_{b=1}^{B} I(T_b(\mathbf{x}) = c)
\label{eq:1}
\end{equation}

where $\mathbf{x}$ represents the input latent vector, $B$ is the number of trees, and $T_b(\mathbf{x})$ denotes the class prediction of tree $b$ \cite{ref5}.
```

---

## 4. Laporan Hasil Konversi & Verifikasi Integritas

### 4.1. Laporan JSON (`conversion_report.json`)
```json
{
  "status": "SUCCESS",
  "template": "ieeeaccess",
  "master_file": "access.tex",
  "converted_sections": [
    "sections/00_abstract.tex",
    "sections/00_title.tex",
    "sections/01_introduction.tex",
    "sections/03_materials-and-methods_c-random-forest.tex"
  ],
  "images_copied": 1,
  "references_bib_created": true,
  "total_sections": 4
}
```

### 4.2. Hasil Verifikasi Linter (`verify_latex_integrity.py`)
```bash
python scripts/verify_latex_integrity.py paper_latex
```

**Keluaran Terminal**:
```text
=== LaTeX Integrity Verification: PASSED ===
Master file: access.tex (4 input sections checked)

All mandatory LaTeX publication integrity rules PASSED.
```
