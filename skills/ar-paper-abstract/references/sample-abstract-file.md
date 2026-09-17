# Sample Abstract File (Illustrative Reference Exemplar)

> [!IMPORTANT]
> **Purely Illustrative Reference Exemplar**
> The following markdown snippet demonstrates the structural format and rhetorical execution of a complete `00_abstract.md` file. It features the paper title, author list with active ORCID links and affiliations, a dense 5-component abstract paragraph with first-mention acronyms, and a curated keyword list.
> This example is provided for instructional purposes. Always craft abstract content and author metadata strictly tailored to the user's specific empirical findings and publication parameters.

---

```markdown
# Multi-Domain Vision Transformer Fusion for Intersectional Demographic Classification from Facial Images

## Authors & Affiliation

1. **Dr. Alex R. Bennett, Ph.D.** ([ORCID: 0000-0002-1234-5678](https://orcid.org/0000-0002-1234-5678))  
   Department of Computer Science, Faculty of Engineering, Metropolitan State University, Metropolis 10115, Country  
   Corresponding Author Email: `a.bennett@metropolitan.edu`

2. **Claire S. Dupont, M.Sc.** ([ORCID: 0009-0001-2345-6789](https://orcid.org/0009-0001-2345-6789))  
   Department of Computer Science, Faculty of Engineering, Metropolitan State University, Metropolis 10115, Country

3. **Prof. Marcus H. Thorne, Ph.D.** ([ORCID: 0000-0003-3456-7890](https://orcid.org/0000-0003-3456-7890))  
   Department of Computer Science, Faculty of Engineering, Metropolitan State University, Metropolis 10115, Country

---

## Abstract

Simultaneous demographic attribute recognition from facial imagery faces substantial challenges arising from subtle expression variations, biological aging, phenotypic overlap, and the inherent representational constraints of single-domain models. This paper proposes a multi-domain latent feature fusion framework that integrates task-specific visual representations extracted from three pre-trained Vision Transformer (ViT) backbones specialized for facial biometrics, affective expression, and age estimation, coupled with an optimized classical machine learning pipeline for intersectional demographic classification across balanced evaluation cohorts. Latent feature vectors are extracted offline from frozen transformer backbones, yielding an integrated representation that captures complementary cross-domain visual semantics without the computational overhead of end-to-end retraining. Seven feature ablation configurations are evaluated using 5-Fold Stratified Cross-Validation across four downstream classifiers: Random Forest (RF), Gaussian Naive Bayes (GNB), Logistic Regression (LR), and Support Vector Machine (SVM) optimized via Grid Search Cross-Validation (GridSearchCV). Experimental evaluations demonstrate that tri-domain fusion achieves superior performance across three of the four evaluated classifiers, with the optimized SVM configuration yielding the highest overall classification capability, recording 93.70% accuracy, 93.72% precision, 93.70% recall, and a 93.69% macro F1-score on independent evaluation data. Granular subgroup diagnostics across six intersectional cohorts demonstrate consistent F1-scores spanning 91.74% to 96.14%, confirming the efficacy of multi-domain latent representation fusion in mitigating intersectional demographic performance disparities.

---

## Keywords

Race and gender classification, intersectional demographic recognition, multi-domain feature fusion, algorithmic fairness, Vision Transformer.
```
