---
name: ar-paper-outline
description: "Activate when the user asks to generate, design, or refine a detailed academic paper outline, create an evidence map, or plan the structure of a research paper or journal manuscript down to the paragraph level. Covers comprehensive paragraph-by-paragraph blueprints (paragraph objective, narrative points, target word count, evidence/citation assignment, and transition sentences), global writing rules, claim boundaries (allowed claims and negative constraints), mathematical equation planning, and master visual/table layout specifications across canonical academic models (IMRaD, Thematic Literature Review, Theoretical Analysis, Case Study, Policy Brief, Conference Paper). Trigger keywords: paper outline, buat outline paper, outline naskah, rancang struktur paper, kerangka paper, outline per paragraf, evidence map, academic outline, paper blueprint. Do NOT activate for full-text drafting, peer-review simulation, citation formatting, or non-academic general writing."
license: MIT
metadata:
  author: Rafy
---

# Academic Paper Outline Generation (Paragraph-Level Blueprint)

## Overview

This skill generates granular, publication-ready academic paper blueprints. Rather than stopping at superficial section headings, it constructs a **paragraph-by-paragraph architecture**: establishing the exact rhetorical purpose, narrative progression, assigned evidence anchors, numerical word targets, and transition sentences for every individual paragraph. It also codifies global claim boundaries (allowed vs. disallowed claims) and master layout sequences for equations, figures, and tables prior to full manuscript drafting.

## When to Activate

- User requests a detailed outline, blueprint, or architectural plan for an academic paper, journal manuscript, thesis chapter, or conference paper.
- User requests an outline with paragraph-level detail, narrative flow, or evidence mapping.
- User invokes trigger terms: `paper outline`, `buat outline paper`, `outline naskah`, `rancang struktur paper`, `kerangka paper`, `outline per paragraf`, `evidence map`, `academic outline`, `paper blueprint`.
- User provides a research question, empirical results, or literature base and needs a rigorous section-and-paragraph structure before drafting.

## When NOT to Activate

- Full-text prose drafting or writing final sections (use paper drafting skills instead).
- Peer review simulation, reviewer scoring, or editorial decisions (use reviewer skills).
- Open-ended general brainstorming without structural deliverables.
- Non-academic writing (blogs, general essays, marketing copy).
- Code crawlers, data extraction scripts, or software development tasks.

## Scope

- **In scope:** 4 blueprint layers (Meta-configuration, Global Claim Boundaries & Writing Rules, Paragraph-by-Paragraph Specifications, Evidence & Gap Mapping), 6 structural models, visual/table layout planning, mathematical notation planning.
- **Out of scope:** Full prose writing, live external API queries, LaTeX compilation, journal submission execution.

---

## Mandatory Step 0: User Intake & Clarification

> [!IMPORTANT]
> **Do NOT assume or fix a specific target venue or journal (such as IEEE Access, Elsevier, etc.) without consulting the user.**
> If the user has not explicitly specified publication details at the outset, the AI **must confirm or ask** the following parameters before constructing the outline:
> 1. **Target Publication / Venue**: Is it aimed at a reputable international journal (IEEE, Elsevier, Springer, Nature, ACM), a national journal, conference proceedings, or a thesis/dissertation chapter?
> 2. **Citation Style & Format**: What citation style is required by author guidelines (IEEE numerical, APA 7 author-date, Harvard, ACM, Vancouver, Chicago)?
> 3. **Manuscript Language & Terminology Policy**: Formal English, or other language with standardized English technical terms?
> 4. **Structural Model & Target Word Count**: Which model fits best (IMRaD, Thematic Literature Review, Theoretical Analysis, Case Study, Policy Brief, Conference Paper), and what is the target word count (e.g., 5,000–8,000 words)?
> 5. **Core Focus & Available Materials**: What are the primary Research Questions (RQs) / Hypotheses, and what empirical findings or literature sources are available?

---

## The 4 Blueprint Layers

Every detailed outline must establish four operational layers:

### Layer 1: Front Matter & Meta-Configuration
- **Target Publication & Venue**: Established from user intake.
- **Manuscript Language & Register**: Formal academic tone and standard terminology policies.
- **Citation Format**: IEEE, APA 7, Harvard, ACM, etc., based on user confirmation.
- **Title & Authors**: Working title and author affiliations.
- **Structured Abstract Blueprint**: 150–250 words following 5 rhetorical movements: *Context/Background → Problem/Objective → Proposed Method → Key Empirical Results → Conclusion/Implications*.
- **Keywords**: 5–7 indexed terms.

### Layer 2: Global Writing Rules & Claim Boundaries
1. **Allowed Claims & Core Focus**: Precise, factual statements defining the primary empirical findings, quantitative metrics, and architectural contributions permitted to be claimed.
2. **Negative Constraints & Disallowed Claims**: Strict boundaries specifying what the manuscript must **NOT** claim (e.g., no unsubstantiated claims of universal superiority, no absolute zero-bias assertions, no unproven causal claims, no claims outside evaluated datasets).
3. **Master Element Sequence**: Chronological registry of all Equations (Eq. 1..N), Figures (Fig. 1..N), and Tables (Table I..N) with LaTeX layout specifications (e.g., full-width span `\begin{table*} ... \end{table*}` vs. single-column).
4. **Stylistic & Lexical Constraints**:
   - Forbid empty superlatives ("revolutionary", "game-changing", "state-of-the-art" unless benchmarked against baselines).
   - Forbid using "significantly" unless accompanied by formal statistical hypothesis testing ($p < 0.05$).
   - Citation density limits: maximum 3 citations per sentence to prevent citation dumping.
   - Standardize technical acronyms: write in full with abbreviation on first mention.

### Layer 3: Paragraph-by-Paragraph Blueprint
For **every individual paragraph** across all sections, provide a dedicated blueprint:

```markdown
### Paragraph X: [Descriptive Sub-Theme / Function]
- **Target Word Count**: [e.g., 110–150 words]
- **Objective**: 1 clear sentence defining the rhetorical or scientific function of this paragraph.
- **Narrative Points**:
  1. [Topic sentence / Core assertion]
  2. [Technical or empirical elaboration, mechanism, or comparative evidence]
  3. [Supporting context, boundary constraint, or secondary finding]
- **Assigned Evidence & Citations**: Explicit literature references (Author, Year / Title), experimental tables, or equation numbers grounding this paragraph.
- **Transition / Bridge Sentence**: Draft of the concluding sentence logically connecting to the subsequent paragraph.
```

### Layer 4: Visuals, Equations, and Gap Management
- **Equations Plan**: Sequentially numbered mathematical formulations with rigorous variable definitions.
- **Visuals & Tables Plan**: Title, caption, column schema, and explicit referencing paragraph.
- **Material Gap Tagging**: Sections lacking empirical proof or literature must be explicitly tagged: `[MATERIAL GAP: description of required data/citation]`. Never fabricate citations or conceal empirical deficits.

---

## Canonical Structural Models

Select the architecture fitting the research design:
1. **IMRaD (Pattern 1A: Integrated Results & Discussion / Pattern 1B: Classical Split)**: Standard for empirical research across engineering, CS, natural, and social sciences.
2. **Thematic Literature Review**: For systematic reviews, meta-syntheses, and scoping studies.
3. **Theoretical Analysis**: For mathematical proofs, conceptual derivations, and theoretical critique.
4. **Case Study**: For single/multi-case organizational or qualitative investigations.
5. **Policy Brief**: For evidence-based recommendations directed at decision-makers.
6. **Conference Paper**: For compact, space-constrained papers (4–8 pages).

*See `references/structure-patterns.md` for complete section breakdowns and word allocation tables.*

---

## Example Blueprint & Reference Files

Consult the following reference files for complete implementations and templates:

- **[`references/sample-paragraph-outline.md`](references/sample-paragraph-outline.md)**: An illustrative mock exemplar demonstrating the entire blueprint lifecycle from user intake, claim boundaries, and master element layout down to **paragraph-by-paragraph (Paragraph 1..N)** blueprints across Section I through Section V. Note: This is purely a demonstrative reference and must not be copied verbatim.
- **[`references/structure-patterns.md`](references/structure-patterns.md)**: Specifications and word count distribution percentages for all 6 canonical structural models.
- **[`references/evidence-mapping.md`](references/evidence-mapping.md)**: Claim-Evidence-Reasoning (CER) guidelines and `[MATERIAL GAP]` tracking protocols.

---

## Do and Don't

| Do | Don't |
|---|---|
| Ask the user for target venue, citation style, and language before outlining | Assume or force a specific venue (e.g., IEEE Access) without asking |
| Decompose every section down to granular paragraph blueprints (word count, objective, narrative points, transition) | Stop at chapter/sub-heading summaries without paragraph-level specifications |
| Define explicit Allowed Claims and Negative Constraints before drafting | Allow ungrounded claims, exaggerations, or speculation into the outline |
| Draft a clear transition sentence for every paragraph | Present isolated bullet points without cohesive narrative progression |
| Plan the chronological sequence of Tables, Figures, and Equations centrally | Insert tables and figures haphazardly without layout planning |
| Tag missing empirical data or citations with `[MATERIAL GAP]` | Fabricate citations, invent results, or gloss over missing evidence |
