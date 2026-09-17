# Single-Section Drafting Workflow & File Architecture

This reference outlines the step-by-step procedure for translating a paragraph-by-paragraph outline into modular Markdown files, drafting **one section or sub-section at a time**, and strictly deferring citation numbering to downstream pipeline steps.

---

## 1. Single Section Drafting Discipline

Do not draft multiple sections or the entire paper in a single turn. Drafting one modular section at a time guarantees:
- **Maximum Analytical Focus**: Allows thorough adherence to each paragraph's objective and evidence requirements.
- **Iterative Human-AI Review**: Enables the user to inspect, revise, and approve each section before moving forward.
- **Token Efficiency & Quality Control**: Avoids context truncation, rushing, or shallow prose.

### Canonical File Architecture
```text
paper/
├── 01_introduction.md
├── 02_related-works.md
├── 03_materials-and-methods_0-overview.md
├── 03_materials-and-methods_a-dataset.md
├── 03_materials-and-methods_b-[primary-method].md
├── 03_materials-and-methods_c-[secondary-models].md
├── 03_materials-and-methods_g-classification-pipeline.md
├── 03_materials-and-methods_h-evaluation-metrics.md
├── 04_results-and-discussion_a-global-performance.md
├── 04_results-and-discussion_b-feature-ablation-study.md
├── 04_results-and-discussion_c-subgroup-analysis.md
├── 04_results-and-discussion_d-error-pattern-assessment.md
├── 04_results-and-discussion_e-comparison-with-prior-studies.md
├── 05_conclusion.md
├── acronyms.txt            (centralized registry of technical abbreviations)
├── images/                 (diagrams, figures, and plots)
└── references/             (BibTeX, RIS, or NBIB bibliographic records)
```

---

## 2. The 5-Stage Writing Cycle (Per Single Section)

When the user specifies a section to write (e.g., *"Draft 01_introduction.md"* or *"Draft methods sub-section on dataset"*), execute this cycle:

```
┌──────────────────────────────────────────────┐
│ Stage 1: Ingest Specific Section Blueprint   │
│ • Read target word count & objectives        │
│ • Identify assigned claims & constraints     │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│ Stage 2: Draft Clean Scholarly Sentences     │
│ • Formulate topic sentences & CER arguments  │
│ • Ensure distinct, verifiable assertions     │
│ • Do NOT insert citation numbers ([1], [[1]])│
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│ Stage 3: Section Transitions & Linking       │
│ • Connect paragraphs with logical bridges    │
│ • Add relative links to other section files  │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│ Stage 4: Writing Quality & Anti-Slop Audit   │
│ • Sweep for banned AI buzzwords              │
│ • Enforce punctuation limits (em dashes ≤ 2) │
│ • Check burstiness (sentence length rhythm)  │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│ Stage 5: Emit the Single File & Await Review │
│ • Save to designated modular markdown path   │
│ • Verify word count against outline target   │
│ • Await user inspection before next section  │
└──────────────────────────────────────────────┘
```

---

## 3. Sentence-Level Claim Crafting (Strictly No Citation Numbering)

A critical principle of the research writing pipeline is separating **prose drafting** (Step 1) from **citation search and mapping** (Step 2), **reference compilation** (Step 3), and **citation numbering** (Step 4).

### Why Citation Numbering is Forbidden in Step 1
- **Unstable Numbering**: If numbers like `[1]`, `[2]`, `[3]` are assigned during initial drafting, adding, removing, or reordering a sentence immediately corrupts the numerical sequence across the entire paper.
- **False Precision**: Generating artificial citation numbers or speculative reference anchors creates phantom citations.

### How to Formulate Claims in Step 1
1. **Discrete Assertions**: Ensure each sentence that makes an empirical or theoretical claim is written as a clear, self-contained proposition.
   * *Example*: *"Multi-task learning frameworks have demonstrated capability in predicting demographic attributes simultaneously, yet they frequently underperform on fine-grained intersectional cohorts."*
2. **Readiness for Step 2 (`references.txt`)**: Because each claim is clearly bounded within its sentence, it can be seamlessly extracted in Step 2 to locate and verify literature sources:
   ```text
   paper/01_introduction.md: paragraf 2:
   - "Multi-task learning frameworks have demonstrated capability...":
     - paper/references/2023_Facial_attribute_classification.bib
   ```
3. **Handling Missing Sources**: If a specific claim in the outline requires literature that is not yet identified, insert a descriptive gap marker rather than a number: `[GAP: source needed for transformer attention on facial patches]`.

---

## 4. Acronym & Abbreviation Registry Protocol (`acronyms.txt`)

In modular academic manuscripts, maintaining abbreviation consistency across dozens of discrete files is essential. Without a centralized registry, authors frequently either re-expand the same acronym repeatedly across multiple sections or introduce unexpanded abbreviations without prior definition.

### The Two Core Invariants
1. **First-Mention Full Form**: The first time an acronym appears anywhere in the paper (whether in the abstract, introduction, or methodology), write its complete formal term followed by the acronym in parentheses:
   * *Example*: `Vision Transformer (ViT)`, `Support Vector Machine (SVM)`, `Multi-Head Self-Attention (MHSA)`.
2. **Subsequent Acronym-Only**: In all subsequent sentences and throughout all subsequent modular files, use **strictly the acronym**:
   * *Example*: `ViT`, `SVM`, `MHSA`.
   * **Never repeat the full form** once the acronym has been registered.

### Format of `paper/acronyms.txt`
Maintain a clean, formatted table tracking every introduced abbreviation:

```text
====================================================================================================
ACRONYM & ABBREVIATION REGISTRY
Guideline: First-Mention Full Form & Subsequent Acronym Only
File Location: paper/acronyms.txt
====================================================================================================

Instructions:
1. Terms already recorded in this registry MUST NOT have their full expansion repeated in subsequent
   markdown draft files (use only the acronym).
2. When introducing a new technical term with an official abbreviation for the first time in a draft,
   write its full form with the abbreviation in parentheses, then immediately register it below.

----------------------------------------------------------------------------------------------------
NO  | ACRONYM / ABBREVIATION | FULL FORM                        | FIRST INTRODUCTION LOCATION
----+------------------------+----------------------------------+-----------------------------------
1   | ViT                    | Vision Transformer               | paper/00_abstract.md (Abstract)
2   | RF                     | Random Forest                    | paper/00_abstract.md (Abstract)
3   | SVM                    | Support Vector Machine           | paper/00_abstract.md (Abstract)
4   | CNN                    | Convolutional Neural Networks    | paper/01_introduction.md (P3)
5   | MHSA                   | Multi-Head Self-Attention        | paper/01_introduction.md (P3)
6   | PCA                    | Principal Component Analysis     | paper/01_introduction.md (P5)
====================================================================================================
```

### Lifecycle Integration in Single-Section Drafting
- **Before Writing**: The agent inspects `paper/acronyms.txt` (if existing) to learn which terms are already registered.
- **While Writing**: The agent uses acronym-only for registered terms. If an unregistered technical term appears, the agent writes `Full Form (ACRONYM)`.
- **After Writing**: The agent automatically updates or creates `paper/acronyms.txt` with newly introduced terms and their specific paragraph location.

---

## 5. Word Count Tracking & Adherence

Every section file drafted must monitor its word count against the budget defined in the paragraph blueprint:

| Section | Typical Target % of Total | Example Budget (6,000-word Paper) |
|:---|:---:|:---:|
| **01_introduction.md** | 12% – 16% | 750 – 950 words |
| **02_related-works.md** | 12% – 18% | 700 – 1,000 words |
| **03_materials-and-methods (all parts)** | 25% – 32% | 1,500 – 1,900 words |
| **04_results-and-discussion (all parts)** | 30% – 38% | 1,800 – 2,300 words |
| **05_conclusion.md** | 5% – 8% | 300 – 500 words |

- **Tolerance**: Maintain word count within $\pm 10\%$ of the paragraph outline budget.
- If a section expands beyond tolerance, eliminate redundant modifiers and trim throat-clearing phrasing rather than cutting essential technical details.
