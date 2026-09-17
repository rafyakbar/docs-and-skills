# Academic Paper Structure Patterns — 6 Canonical Models

This guide details the structural architectures, section organizations, paragraph progression models, and word allocation budgets across the 6 canonical academic paper types.

---

## The Paragraph-by-Paragraph Architectural Principle

Regardless of which model is selected, outlines generated under this skill **MUST NOT** stop at high-level chapter titles or superficial sub-headings. Every section must be broken down into **discrete paragraph units** following the standard blueprint:

```
### Paragraph X: [Descriptive Sub-Theme / Function]
- Target Word Count: [100–160 words]
- Objective: [1 sentence defining the rhetorical or scientific function]
- Narrative Points: [1. Topic Sentence | 2. Elaboration/Evidence | 3. Context/Boundary]
- Assigned Evidence & Citations: [Explicit literature, dataset, or equation anchors]
- Transition Sentence: [Concluding sentence bridging to the next paragraph]
```

---

## Pattern 1: IMRaD (Empirical Research)

**Best for**: Empirical research based on quantitative experiments, qualitative fieldwork, or mixed-methods data.  
**Standard Disciplines**: Computer Science, Engineering, Medicine, Psychology, Social Sciences, Natural Sciences.  
**Typical Length**: 5,000 – 8,000 words.

IMRaD papers exist in two primary architectural variants depending on the target venue:

### Pattern 1A: Integrated IMRaD (Results and Discussion Combined)
*Standard in: Computer Science, Machine Learning, Electrical Engineering, IEEE, ACM, and Applied Engineering.*  
*(See `references/sample-paragraph-outline.md` for a full, self-contained exemplar of Pattern 1A).*

#### Section Architecture & Paragraph Budget (6,000-word example)
| Section | % of Total | Target Words | Paragraph Count | Paragraph Progression |
|---|:---:|:---:|:---:|---|
| Front Matter & Abstract | — | 200 words | 1 (Unified) | Context → Objective → Method → Results → Conclusion |
| **Section I: Introduction** | 15% | ~900 words | 6–7 paragraphs | P1: Urgency & Real-world Context<br>P2: Problem Statement & Sensory/Domain Blind Spots<br>P3: Technological Advances & Foundational Paradigms<br>P4: Critical Literature Gaps<br>P5: Proposed Framework Overview<br>P6: Enumerated Scientific Contributions<br>P7: Article Organization Roadmap |
| **Section II: Related Works** | 15% | ~900 words | 5–6 paragraphs | P1–P4: Thematic syntheses of prior approaches (max 3 cites/sentence)<br>P5: Critical comparative synthesis of limitations<br>P6: Research positioning & differentiation statement |
| **Section III: Materials and Methods** | 25% | ~1,500 words | 10–12 paragraphs | **Overview**: Full-width pipeline architecture (Figure 1)<br>**III.A Dataset**: P1 Context, P2 Partitioning, P3 Preprocessing<br>**III.B Feature Extraction**: P4–P6 Backbone architecture & equations<br>**III.C Optimization Pipeline**: P7–P9 Algorithm search space & fold isolation<br>**III.D Evaluation Protocol**: P10–P11 Metrics & statistical testing |
| **Section IV: Results and Discussion** | 40% | ~2,400 words | 12–15 paragraphs | **IV.A Global Benchmark**: P1–P3 Primary performance & comparative baseline analysis (Table III)<br>**IV.B Feature Ablation**: P4–P6 Component-wise contribution (Figure 2)<br>**IV.C Subgroup & Error Analysis**: P7–P9 Class-level stability & error patterns<br>**IV.D Computational Complexity**: P10–P11 Runtime & memory profiling<br>**IV.E Discussion**: P12–P14 Triangulation with prior literature, theoretical implications, and boundary constraints |
| **Section V: Conclusion** | 5% | ~300 words | 3 paragraphs | P1: Synthesis of primary findings answering RQs<br>P2: Honest disclosure of technical/practical limitations<br>P3: Actionable roadmap for future research |

---

### Pattern 1B: Classical Split IMRaD (Results and Discussion Separated)
*Standard in: Clinical Medicine, Biomedical Sciences, Experimental Psychology, Pure Social Sciences.*

#### Section Architecture & Paragraph Budget (6,000-word example)
| Section | % of Total | Target Words | Paragraph Count | Paragraph Progression |
|---|:---:|:---:|:---:|---|
| Front Matter & Abstract | — | 250 words | 1 (Structured) | Objective → Methods → Results → Conclusion |
| **1. Introduction** | 15% | ~900 words | 5–6 paragraphs | Broad problem context → Specific clinical/empirical tension → Unresolved knowledge deficit → Study objective & hypotheses |
| **2. Literature Review / Theoretical Framework** | 20% | ~1,200 words | 7–8 paragraphs | Theoretical constructs → Empirical findings across themes → Inconsistencies/controversies in prior data → Hypothesis justification |
| **3. Methodology** | 15% | ~900 words | 6–8 paragraphs | Participants/Sample criteria → Operationalization of measures → Experimental procedure & ethics → Statistical analysis strategy |
| **4. Results** | 20% | ~1,200 words | 7–9 paragraphs | *Purely factual reporting without interpretation*:<br>Descriptive statistics (Table 1) → Primary hypothesis testing H1 (Table 2) → Secondary hypothesis testing H2 → Subgroup/sensitivity analyses |
| **5. Discussion** | 25% | ~1,500 words | 8–10 paragraphs | Summary of core findings → Interpretation & comparison with past studies → Theoretical mechanisms explaining results → Clinical/practical implications → Methodological limitations |
| **6. Conclusion** | 5% | ~300 words | 2–3 paragraphs | Final synthesis → Definitive takeaway message |

---

## Pattern 2: Thematic Literature Review

**Best for**: Systematic reviews, meta-analyses (PRISMA), and state-of-the-art scoping reviews.  
**Standard Disciplines**: All academic fields.  
**Typical Length**: 6,000 – 10,000 words.

### Paragraph Progression Architecture
- **Section 1: Introduction & Motivation (3–4 paragraphs, ~800 words)**
  - P1: Evolution and contemporary significance of the field.
  - P2: Boundaries, scope, and specific review questions (RQs).
  - P3: Justification of this review compared to prior surveys.
  - P4: Overview of review structure.
- **Section 2: Review Methodology & Search Strategy (3–4 paragraphs, ~800 words)**
  - P1: Database selection, search string syntax, and temporal boundaries.
  - P2: Inclusion and exclusion criteria (PRISMA Flowchart / Figure 1).
  - P3: Screening protocol, inter-rater reliability, and risk-of-bias assessment.
  - P4: Bibliometric profile of the finalized corpus (Table 1).
- **Sections 3–5: Thematic Clusters (4–6 paragraphs per theme, ~3,600 words)**
  - *Theme A*: Foundational paradigms, taxonomies, and core constructs.
  - *Theme B*: Methodological implementations and empirical patterns.
  - *Theme C*: Drivers, moderating factors, and observed outcomes.
  - *Internal paragraph flow*: Synthesis of consensus → Divergent evidence → Underlying methodological drivers.
- **Section 6: Critical Synthesis & Research Gaps (4–5 paragraphs, ~1,200 words)**
  - P1: Theoretical blind spots across literature clusters.
  - P2: Methodological deficits and sampling biases in existing studies.
  - P3: Contradictory evidence and empirical tensions.
  - P4: Summary matrix of identified research gaps (Table 2).
- **Section 7: Integrative Framework & Future Agenda (3–4 paragraphs, ~1,000 words)**
  - P1: Presentation of the proposed integrative conceptual model (Figure 2).
  - P2: Specific, high-priority research questions for future investigation.
  - P3: Methodological recommendations for subsequent empirical work.
- **Section 8: Conclusion (2 paragraphs, ~400 words)**
  - P1: Synthesis of primary contributions.
  - P2: Concluding remarks on the future trajectory of the domain.

---

## Pattern 3: Theoretical Analysis

**Best for**: Developing new conceptual frameworks, mathematical formulations, or critical theoretical paradigm critiques.  
**Standard Disciplines**: Philosophy, Economics, Sociology, Critical Theory, Pure Mathematics, Theoretical CS.  
**Typical Length**: 6,000 – 9,000 words.

### Paragraph Progression Architecture
- **Section 1: Introduction & The Theoretical Paradox (3–4 paragraphs, ~900 words)**
  - P1: Real-world anomaly or conceptual puzzle that existing theory cannot resolve.
  - P2: Shortcomings and breakdown points of prevailing theoretical paradigms.
  - P3: The proposed theoretical contribution, core thesis, and analytical boundary.
- **Section 2: Theoretical Foundations & Critical Review (5–6 paragraphs, ~1,500 words)**
  - Historical lineage of the concept → Dominant formulations → Critique of hidden assumptions and internal logical tensions.
- **Section 3: Formulation of the Novel Theoretical Model (8–10 paragraphs, ~2,500 words)**
  - P1–P2: Axiomatic foundations, primitive definitions, and ontology.
  - P3–P5: Mathematical derivations, propositions, or formal logic chains (Eq. 1..N).
  - P6–P8: Interactions between constructs and causal mechanisms.
  - P9–P10: Formal boundary conditions and scope limitations.
- **Section 4: Conceptual Application / Thought Experiment (5–6 paragraphs, ~1,600 words)**
  - Testing the proposed model against known paradoxes, edge cases, or historical anomalies (Table 1 comparing legacy vs. new model).
- **Section 5: Epistemological Implications & Discussion (4–5 paragraphs, ~1,100 words)**
  - Broader epistemological consequences → Re-interpretation of existing empirical findings → Methodological implications for testing the model.
- **Section 6: Conclusion (2 paragraphs, ~400 words)**
  - Final synthesis and prospective theoretical extensions.

---

## Pattern 4: Case Study

**Best for**: Single-case or multiple-case in-depth organizational, technological, or policy investigations.  
**Standard Disciplines**: Management, Information Systems, Public Administration, Education, Sociology.  
**Typical Length**: 6,000 – 8,000 words.

### Paragraph Progression Architecture
- **Section 1: Introduction & Case Phenomenon (3–4 paragraphs, ~800 words)**
  - Empirical phenomenon in context → Practical stakes → Research questions and rationale for selecting qualitative case methodology.
- **Section 2: Theoretical Grounding (3–4 paragraphs, ~1,000 words)**
  - Sensitizing theoretical concepts or analytical framework guiding field observation.
- **Section 3: Research Methodology & Case Context (4–6 paragraphs, ~1,200 words)**
  - P1: Rationale for case selection (revelatory, extreme, or representative case criteria).
  - P2: Institutional background and operational setting of the case organization.
  - P3: Triangulated data collection (interviews, field observation, archival documents).
  - P4–P5: Coding procedure, construct validity, and analytical within-case / cross-case strategy.
- **Section 4: Case Findings & Narrative Analysis (8–12 paragraphs, ~2,200 words)**
  - Chronological or thematic narrative progression: Baseline conditions → Critical incident / Intervention → Organizational response → Emergent dynamics and outcomes.
- **Section 5: Discussion & Emergent Grounded Framework (5–6 paragraphs, ~1,400 words)**
  - Inductive framework developed from case observations (Figure 1) → Comparison with prevailing literature → Transferability and analytical generalization boundaries.
- **Section 6: Practical Implications & Conclusion (2–3 paragraphs, ~400 words)**
  - Actionable managerial/policy lessons → Methodological limitations → Concluding remarks.

---

## Pattern 5: Policy Brief

**Best for**: Evidence-based briefs translating complex empirical research into actionable policy recommendations for decision-makers.  
**Standard Disciplines**: Public Policy, Public Health, Environmental Governance, Economics.  
**Typical Length**: 3,000 – 5,000 words.

### Paragraph Progression Architecture
- **Executive Summary (2 paragraphs, ~250 words)**
  - P1: The core policy dilemma, urgency, and primary finding.
  - P2: The definitive policy recommendation and projected impact.
- **Section 1: Policy Context & Root Causes (3–4 paragraphs, ~800 words)**
  - Socio-economic or institutional problem context → Root structural drivers → Immediate risks to affected stakeholder populations.
- **Section 2: Critique of Existing Policy Measures (3–4 paragraphs, ~800 words)**
  - Analysis of current regulatory/legislative efforts → Identified systemic deficiencies, budget inefficiencies, or unintended perverse incentives.
- **Section 3: Empirical Evidence & Impact Analysis (4–5 paragraphs, ~1,200 words)**
  - Quantitative research findings, cost-benefit calculations, and demographic impact distribution (Table 1 & Figure 1).
- **Section 4: Policy Options & Comparative Evaluation (3–4 paragraphs, ~1,000 words)**
  - Option A vs. Option B vs. Status Quo evaluated against feasibility, cost, equity, and political viability (Evaluation Matrix Table 2).
- **Section 5: Actionable Recommendations & Implementation Roadmap (3 paragraphs, ~600 words)**
  - P1: Recommended policy package and rationale.
  - P2: Phased implementation timeline and lead agency responsibilities.
  - P3: Key performance indicators (KPIs) and accountability monitoring.

---

## Pattern 6: Conference Paper

**Best for**: Fast-track, space-constrained papers (typically 4–8 pages / 3,000–4,500 words).  
**Standard Disciplines**: Computer Science, AI/ML, Electrical Engineering, Human-Computer Interaction.  
**Typical Length**: 3,000 – 4,500 words.

### Paragraph Progression Architecture
- **Section 1: Introduction (3–4 paragraphs, ~600 words)**
  - P1: Motivation and core technical problem.
  - P2: Limitations of existing baseline approaches.
  - P3: Proposed technical contribution and methodology overview.
  - P4: Bulleted list of primary contributions (typically 3 points).
- **Section 2: Related Work (2–3 paragraphs, ~500 words)**
  - P1: Evolution of related baseline algorithms.
  - P2: Specific distinction of this work from closest competing methods.
- **Section 3: Proposed Methodology (4–6 paragraphs, ~1,200 words)**
  - P1: System pipeline overview (Figure 1).
  - P2–P4: Algorithmic details, mathematical formulations (Eq. 1..N), and novel loss functions / mechanisms.
- **Section 4: Experimental Evaluation (6–8 paragraphs, ~1,600 words)**
  - P1: Datasets, baseline models, and evaluation metrics.
  - P2–P3: Quantitative benchmark results vs. baselines (Table 1 & Figure 2).
  - P4–P5: Component ablation studies validating architectural decisions.
  - P6: Qualitative examples or failure case analysis.
- **Section 5: Conclusion & Limitations (1–2 paragraphs, ~300 words)**
  - P1: Summary of results.
  - P2: Primary limitation and future research direction.
