# Acronym Registry & Keyword Curation Standards

This reference governs acronym handling within the abstract, synchronization with `paper/acronyms.txt`, keyword selection strategies, and author metadata formatting.

---

## 1. Acronym Protocols in the Abstract

Because the abstract is indexed independently in scientific databases (such as IEEE Xplore, Scopus, and PubMed), it operates under strict abbreviation standards:

### The First-Mention Rule in `00_abstract.md`
1. **Full Form on First Mention**: Every technical term possessing an official acronym introduced in the abstract must appear in full, followed immediately by its abbreviation in parentheses:
   * *Example*: `Vision Transformer (ViT)`, `Random Forest (RF)`, `Gaussian Naive Bayes (GNB)`, `Logistic Regression (LR)`, `Support Vector Machine (SVM)`, `Grid Search Cross-Validation (GridSearchCV)`.
2. **Subsequent Mentions in Abstract**: If the same term is used again within the abstract paragraph, use strictly the abbreviation.
3. **Registration in `paper/acronyms.txt`**: All abbreviations introduced in the abstract must be registered at the top of the central registry file (`paper/acronyms.txt`) with their first introduction location logged explicitly as `paper/00_abstract.md (Abstract)`:

```text
====================================================================================================
ACRONYM & ABBREVIATION REGISTRY
Guideline: First-Mention Full Form & Subsequent Acronym Only
File Location: paper/acronyms.txt
====================================================================================================

----------------------------------------------------------------------------------------------------
NO  | ACRONYM / ABBREVIATION | FULL FORM                        | FIRST INTRODUCTION LOCATION
----+------------------------+----------------------------------+-----------------------------------
1   | ViT                    | Vision Transformer               | paper/00_abstract.md (Abstract)
2   | RF                     | Random Forest                    | paper/00_abstract.md (Abstract)
3   | GNB                    | Gaussian Naive Bayes             | paper/00_abstract.md (Abstract)
4   | LR                     | Logistic Regression              | paper/00_abstract.md (Abstract)
5   | SVM                    | Support Vector Machine           | paper/00_abstract.md (Abstract)
6   | GridSearchCV           | Grid Search Cross-Validation     | paper/00_abstract.md (Abstract)
====================================================================================================
```

> [!IMPORTANT]
> Because terms registered in `00_abstract.md` are now recorded in `paper/acronyms.txt`, authors drafting downstream sections (`01_introduction.md`, `02_related-works.md`, `03_materials-and-methods_*.md`, etc.) must use **only the acronym** without repeating the full expansion.

---

## 2. Keyword Curation & Search Discoverability

Keywords determine how search engines, indexing services, and journal editors categorize the manuscript. Effective keywords optimize citation discovery.

### Heuristics for Selecting 5–7 Keywords
1. **Target Range**: Provide exactly **5 to 7 high-impact keywords**, separated by commas.
2. **Title Complementarity**: Avoid exact duplication with the paper's main title. If the title already contains *"Multi-Domain Vision Transformer Fusion"*, choose complementary keywords such as *"algorithmic fairness"*, *"intersectional demographic recognition"*, or *"latent feature representation"*. Search engines already index title words; complementary keywords expand retrieval reach.
3. **The 5-Tier Coverage Taxonomy**: A robust keyword set spans five distinct research facets:
   - **Tier 1 (Problem / Task Domain)**: e.g., *Race and gender classification*, *Face recognition*.
   - **Tier 2 (Specific Paradigm / Theoretical Context)**: e.g., *Intersectional demographic recognition*, *Algorithmic fairness*.
   - **Tier 3 (Core Methodological Mechanism)**: e.g., *Multi-domain feature fusion*, *Latent representation learning*.
   - **Tier 4 (Primary Computational Architecture)**: e.g., *Vision Transformer*, *Ensemble learning*.
   - **Tier 5 (Evaluation Focus / Application)**: e.g., *Benchmarking*, *Subgroup disparity analysis*.
4. **Capitalization Norm**: Capitalize the first letter of each keyword/phrase, or capitalize proper nouns and acronyms according to venue guidelines.

---

## 3. Author Metadata & Front Matter Architecture

In modular manuscript workflows, `00_abstract.md` serves as the master front matter document. Structure the header block cleanly as follows:

```markdown
# [Full Manuscript Title: Clear, Specific, Informative]

## Authors & Affiliation

1. **[Author 1 Full Name, Degrees]** ([ORCID: 0000-000X-XXXX-XXXX](https://orcid.org/0000-000X-XXXX-XXXX))  
   Department of Informatics, Faculty of Informatics, Universitas Negeri Surabaya, Surabaya 60231, Indonesia  
   Corresponding Author Email: `author1@unesa.ac.id`

2. **[Author 2 Full Name, Degrees]** ([ORCID: 0009-000X-XXXX-XXXX](https://orcid.org/0009-000X-XXXX-XXXX))  
   Department of Informatics, Faculty of Informatics, Universitas Negeri Surabaya, Surabaya 60231, Indonesia

3. **[Author 3 Full Name, Degrees]** ([ORCID: 0000-000X-XXXX-XXXX](https://orcid.org/0000-000X-XXXX-XXXX))  
   Department of Informatics, Faculty of Informatics, Universitas Negeri Surabaya, Surabaya 60231, Indonesia

---

## Abstract

[Single cohesive paragraph following the 5-component rhetorical framework]

---

## Keywords

Keyword 1, Keyword 2, Keyword 3, Keyword 4, Keyword 5.
```

### Standards for Metadata
- **ORCID Identifiers**: Formatted as active Markdown hyperlinks to `https://orcid.org/[ID]`.
- **Institutional Details**: Include department, faculty, institution name, city, postal code, and country.
- **Corresponding Author**: Clearly designate the primary point of contact with an official institutional email.
