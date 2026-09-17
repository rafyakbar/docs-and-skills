---
name: ar-paper-abstract
description: "Activate when the user asks to write, generate, refine, or translate an academic paper abstract, keywords, or title/front matter (typically for 00_abstract.md). Covers the 5-component rhetorical model (Context/Problem, Purpose, Methodology, Quantitative Findings, Implications), first-mention acronym introduction and registration into paper/acronyms.txt, keyword curation (5-7 terms), author metadata formatting (ORCID, affiliations, corresponding author), and bilingual abstract generation. Trigger keywords: write abstract, buat abstrak, paper abstract, abstract and keywords, saripati, generate abstract, draft abstract, 00_abstract.md. Do NOT activate for full-text manuscript drafting (use ar-paper-draft), outline planning (use ar-paper-outline), citation curation, or peer review."
license: MIT
metadata:
  author: Rafy
---

# Academic Paper Abstract & Front Matter Generation

## Overview

This skill generates publication-grade academic abstracts, keywords, and master front matter (typically formatted as `00_abstract.md`). It implements a rigorous **5-component rhetorical framework** (Context & Problem $\rightarrow$ Purpose & Proposed Solution $\rightarrow$ Methodology $\rightarrow$ Key Quantitative Findings $\rightarrow$ Conclusion & Impact), enforces strict **first-mention acronym registration** into `paper/acronyms.txt`, curates 5–7 search-optimized keywords, and structures complete author metadata with active ORCID hyperlinks.

## When to Activate

- User asks to write, draft, generate, or refine an academic paper abstract, keywords, or front matter.
- User requests creation or updates to `00_abstract.md`.
- User invokes trigger phrases: `write abstract`, `buat abstrak`, `paper abstract`, `abstract and keywords`, `saripati`, `generate abstract`, `draft abstract`, `00_abstract.md`.
- User provides experimental findings or full manuscript drafts and asks to synthesize an abstract.
- User requests a bilingual abstract (e.g., English + Indonesian or other languages).

## When NOT to Activate

- Drafting full manuscript body sections like Introduction, Methods, or Discussion (use `ar-paper-draft`).
- Generating paper outlines or paragraph blueprints from scratch (use `ar-paper-outline`).
- Searching, scraping, or curating citations and BibTeX entries (use citation curation skills / Step 2).
- Compiling reference lists or assigning in-text citation numbering (use Step 3 & 4 skills).
- Peer-review simulation or reviewer critique scoring.
- Non-academic summaries or general blog executive summaries.

## Scope

- **In scope:** Drafting dense, publication-ready abstracts (150–250 words), 5-component rhetorical structure, exact quantitative metric extraction, first-mention acronym expansion and synchronization with `paper/acronyms.txt`, 5–7 keyword curation, author metadata formatting with ORCID links, and bilingual abstract pairs.
- **Out of scope:** Inserting bibliographic citations into the abstract (strictly prohibited in scholarly abstracts), fabricating unverified experimental numbers, or generating body sections.

---

## Mandatory Step 0: Input Verification & Context Calibration

Before generating the abstract, verify or elicit the following parameters:

1. **Source Material Availability**: Identify the underlying paper materials (e.g., draft files `01_introduction.md` through `05_conclusion.md`, or outline blueprint and empirical results table). Extract the exact core achievement and best-performing quantitative metrics.
2. **Target Word Budget & Format**: Check target journal guidelines (standard unstructured dense paragraph of 150–250 words, structured abstract with labeled subheadings, or extended conference abstract).
3. **Language Policy**: Determine whether the abstract is monolingual (e.g., English) or bilingual (e.g., Indonesian + English).
4. **Author & Affiliation Metadata**: Confirm author names, academic titles, ORCID identifiers, department/faculty affiliations, and corresponding author email address.

---

## The 5-Component Rhetorical Architecture

Every abstract must synthesize the research across five sequential rhetorical movements into a single cohesive paragraph:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Context & Problem (1–2 sentences)                        │
│ State the technical domain and the specific bottleneck      │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Purpose & Proposed Solution (1–2 sentences)              │
│ Announce the proposed model, framework, or thesis           │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Methodology & Experimental Setup (1–2 sentences)         │
│ State data cohorts, validation schemes, and classifier types│
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Key Empirical Findings (2–3 sentences)                   │
│ Report exact numerical metrics (Accuracy, F1, p-values)     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Conclusion & Significance (1 sentence)                   │
│ Deliver the core takeaway and broader scientific impact     │
└─────────────────────────────────────────────────────────────┘
```

### Critical Rhetorical Rules:
- **No Citations**: Never include literature citation brackets (`[1]`, `[2]`, or author-year tags).
- **Exact Numerical Evidence**: Include concrete quantitative metrics for the proposed approach and primary baseline. Never use vague generalities like *"achieved promising results"*.
- **Tense Discipline**: Use present tense for domain background and broad truths; use past tense for study-specific actions and observed metrics; use present tense for the concluding significance.

---

## Acronym Protocol in the Abstract (`paper/acronyms.txt`)

Because `00_abstract.md` is often read independently and precedes the body sections:

1. **First-Mention Full Form**: Every technical term with an official acronym introduced in the abstract **must be written in full form followed by the abbreviation in parentheses**:
   * *Example*: `Vision Transformer (ViT)`, `Support Vector Machine (SVM)`, `Grid Search Cross-Validation (GridSearchCV)`.
2. **Subsequent Mentions in Abstract**: If repeated within the abstract, use only the acronym.
3. **Immediate Registration in `paper/acronyms.txt`**: All abbreviations introduced in `00_abstract.md` must be logged at the top of the central registry `paper/acronyms.txt` with their first appearance marked as `paper/00_abstract.md (Abstract)`:

```text
NO  | ACRONYM / ABBREVIATION | FULL FORM                        | FIRST INTRODUCTION LOCATION
----+------------------------+----------------------------------+-----------------------------------
1   | ViT                    | Vision Transformer               | paper/00_abstract.md (Abstract)
2   | RF                     | Random Forest                    | paper/00_abstract.md (Abstract)
3   | SVM                    | Support Vector Machine           | paper/00_abstract.md (Abstract)
```

> [!NOTE]
> Once registered here, all downstream drafting skills (`ar-paper-draft`) must use **only the acronym** in body sections without re-expanding the term.

---

## Keyword Curation Heuristics

1. **Count**: Exactly **5 to 7 keywords**, separated by commas.
2. **Title Complementarity**: Do not simply repeat title terms. If the title contains *"Multi-Domain Vision Transformer Fusion"*, select keywords that capture secondary dimensions (e.g., *Algorithmic fairness*, *Intersectional demographic recognition*, *Latent representation learning*).
3. **Facet Coverage**: Ensure terms represent problem domain, methodological mechanism, computational architecture, and evaluation focus.

---

## Author Metadata & Master File Layout

Emit the final output to `paper/00_abstract.md` using this standard layout:

```markdown
# [Full Manuscript Title]

## Authors & Affiliation

1. **[Author 1 Name, Degree]** ([ORCID: 0000-000X-XXXX-XXXX](https://orcid.org/0000-000X-XXXX-XXXX))  
   Department of Informatics, Faculty of Informatics, Universitas Negeri Surabaya, Surabaya 60231, Indonesia  
   Corresponding Author Email: `author1@unesa.ac.id`

2. **[Author 2 Name, Degree]** ([ORCID: 0009-000X-XXXX-XXXX](https://orcid.org/0009-000X-XXXX-XXXX))  
   Department of Informatics, Faculty of Informatics, Universitas Negeri Surabaya, Surabaya 60231, Indonesia

---

## Abstract

[Dense 5-component abstract paragraph, 150–250 words, exact metrics, first-mention acronyms]

---

## Keywords

Keyword 1, Keyword 2, Keyword 3, Keyword 4, Keyword 5.
```

---

## Do and Don't Guidelines

| Do | Don't |
|:---|:---|
| Report exact numerical metrics (Accuracy, F1, p-values) | Use vague qualitative claims (*"achieved great accuracy"*) |
| Expand every acronym on first mention: `Full Form (ACRONYM)` | Use naked acronyms without definition in the abstract |
| Log all abstract acronyms to `paper/acronyms.txt` | Forget to register abstract acronyms in the central file |
| Provide 5–7 keywords complementary to the paper title | Duplicate title terms word-for-word in keywords |
| Keep word count strictly within venue limits (150–250 words) | Write bloated multi-page abstracts or under 100 words |
| Format ORCID links as active Markdown hyperlinks | Omit ORCID identifiers or affiliation details |
| Strictly exclude bibliographic citations from the abstract | Insert bracketed citation numbers (`[1]`, `[2]`) in abstract |

---

## References

For detailed guidelines, consultation patterns, and exemplars, refer to:
- `references/abstract-rhetoric-patterns.md`: Detailed 5-component framework, tense usage, and abstract formatting types.
- `references/acronym-and-keyword-standards.md`: Acronym registry invariants, 5-tier keyword taxonomy, and metadata formatting.
- `references/sample-abstract-file.md`: Illustrative reference exemplar of a complete `00_abstract.md` document.
