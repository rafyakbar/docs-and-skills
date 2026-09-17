# Rhetorical Section Guides for Academic Paper Drafting

This reference provides rhetorical blueprints, functional moves, and prose conventions for drafting the major sections of an academic manuscript based on a paragraph-level outline.

---

## 1. Introduction Section (Swales CARS Model)

The Introduction must persuade the scholarly reader that the research domain is significant, an important gap or conflict exists, and the current study resolves that gap. Follow Swales' **Create A Research Space (CARS)** model across three rhetorical moves:

```
┌───────────────────────────────────────────────────────────┐
│ Move 1: Establish the Territory                           │
│ • State domain importance & real-world/scientific stakes │
│ • Review foundational literature & broad practices       │
└─────────────────────────────┬─────────────────────────────┘
                              ▼
┌───────────────────────────────────────────────────────────┐
│ Move 2: Establish the Niche (The Pivot)                  │
│ • Identify specific empirical/theoretical/method gap     │
│ • Frame limitations of prior approaches or conflicts     │
└─────────────────────────────┬─────────────────────────────┘
                              ▼
┌───────────────────────────────────────────────────────────┐
│ Move 3: Occupy the Niche                                  │
│ • State proposed approach, framework, or thesis          │
│ • Enumerate explicit, non-overlapping contributions      │
│ • Outline the organizational roadmap of the manuscript    │
└───────────────────────────────────────────────────────────┘
```

### Move 1: Establishing the Territory
- **Centrality Claim**: Open by defining why the research problem is vital to the target scientific community.
- **Background Synthesis**: Weave foundational literature thematically. Do not write a generic textbook summary; focus strictly on the evolution leading to the research problem.
- **Verifiable Factual Claims**: Formulate each factual statement regarding prior paradigms or domain importance as a discrete assertion ready for sentence-level citation mapping in Step 2. Strictly omit numeric citation markers at this stage.

### Move 2: Establishing the Niche (The Critical Pivot)
- **Sharp Gap Formulation**: Explicitly articulate what prior work has failed to resolve, overlooked, or left contested.
- **Avoid Universal Negatives**: Avoid unverifiable blanket statements such as *"No study has ever examined X"*. Instead, use scoped, defensible formulations: *"Existing literature has predominantly focused on single-domain representations, leaving the joint interaction of X and Y comparatively underexplored."*
- **Problem Statement**: Directly link the technical or empirical limitation of prior methods to real-world consequences or theoretical bottlenecks.

### Move 3: Occupying the Niche
- **Purpose Statement**: Explicitly announce the proposed solution: *"To bridge these identified gaps, this paper proposes [Framework/Method/Hypothesis]..."*
- **Core Scientific Contributions**: Present a clear, itemized list of novel contributions (typically 3–4 items):
  1. Methodological/Architectural contribution (the model, algorithm, or experimental intervention).
  2. Empirical/Benchmarking contribution (comparative experiments, dataset curation, or ablations).
  3. Analytical/Diagnostic contribution (subgroup disparities, error analysis, or theoretical proofs).
- **Roadmap Paragraph**: Provide a concise structural guide mapping out the rest of the manuscript, using markdown links to corresponding section files:
  * Example: *"The remainder of this article is organized as follows: Section [II](02_related-works.md) reviews relevant literature. Section [III](03_materials-and-methods_0-overview.md) details the proposed methodology. Section [IV](04_results-and-discussion_a-global-performance.md) presents empirical evaluations. Finally, Section [V](05_conclusion.md) concludes the study."*

---

## 2. Related Work / Literature Review Section

Related Work is a critical synthesis of the intellectual conversation, not an annotated bibliography in prose.

### Thematic Clustering Protocol
- **Organize by Concept, Not Author**: Group prior literature into thematic categories, methodological paradigms, or historical evolutions rather than chronological lists of individual papers (*"Smith et al. did X. Then Jones did Y."*).
- **Synthesizing Sentence Pattern**:
  * Weak (Author-list): *"Author A used CNNs for classification. Then Author B used ResNet. Subsequently, Author C used ViTs."*
  * Strong (Thematic synthesis): *"Early architectural paradigms predominantly relied on localized feature extraction via convolutional backbones, whereas recent formulations leverage multi-head self-attention to capture long-range spatial correlations."*
- **Comparative Differentiator**: Conclude each thematic subsection by explicitly contrasting the surveyed approaches against the approach taken in this paper.

---

## 3. Materials and Methods / Methodology Section

The methodology must provide exhaustive procedural transparency, enabling an independent researcher to replicate the study.

### Modular Sub-Section Organization
In complex studies, divide the methodology into distinct, focused markdown files:
- `03_materials-and-methods_0-overview.md`: End-to-end system architecture, pipeline schematic, and high-level workflow.
- `03_materials-and-methods_a-dataset.md`: Cohort characteristics, data distribution, preprocessing, augmentation, and split protocols.
- `03_materials-and-methods_b-[primary-technique].md`: Mathematical formulation, loss functions, and architectural layers.
- `03_materials-and-methods_c-[secondary-models].md`: Baselines, comparative models, and algorithmic variants.
- `03_materials-and-methods_g-pipeline.md`: Training protocol, optimization hyperparameters, convergence criteria.
- `03_materials-and-methods_h-evaluation-metrics.md`: Formal definitions of performance metrics, statistical validation schemes, and leakage prevention guardrails.

### Methodological Drafting Rules
1. **Mathematical Rigor**: Every symbol in equations must be defined immediately before or after the equation. State variable dimensions and indices explicitly.
2. **Data Leakage Safeguards**: Document split boundaries clearly. State explicitly how transformations, normalizations, and hyperparameter selections were learned strictly on training partitions.
3. **Hyperparameter Transparency**: Report all relevant parameters (learning rates, batch sizes, epochs, regularization coefficients, random seeds).

---

## 4. Results and Discussion Section

Depending on the chosen structural model, Results and Discussion may be integrated (Pattern 1A, common in Engineering/CS) or separated (Pattern 1B, common in Natural Sciences).

### The Claim-Evidence-Reasoning (CER) Pattern
Every results paragraph must follow the CER sequence:
1. **Claim (Topic Assertion)**: State the primary empirical finding directly: *"The proposed tri-domain configuration achieved the highest overall macro-F1 score across all tested backbones."*
2. **Evidence (Quantitative Grounding)**: Cite exact numerical figures from the corresponding table or figure: *"As shown in Table II, our model recorded an F1 score of 94.2%, representing an absolute improvement of 3.8% over the baseline (Table II, row 4)."*
3. **Reasoning (Analytical Interpretation)**: Explain *why* the data looks this way: *"This performance advantage is attributable to the complementary nature of affective and geometric representations, which prevents decision boundary collapse under heavy illumination variance."*
4. **Qualification / Caveat**: Note any boundary conditions or subgroups where the advantage diminishes.

### Structured Subsections for Results
- **Global Benchmark Performance**: Broad comparative evaluation against established baselines.
- **Ablation Studies**: Systematic isolation of individual modules, loss components, or feature subsets to prove their incremental necessity.
- **Subgroup & Intersectional Analysis**: Performance breakdown across demographic, environmental, or operational subsets to reveal disparities or consistency.
- **Error & Failure Case Analysis**: Qualitative or quantitative inspection of false positives, misclassifications, or edge-case breakdowns.
- **Comparison with Prior Art**: Direct juxtaposition of quantitative findings against recently published benchmarks in the literature.

---

## 5. Conclusion Section

The Conclusion provides closure by synthesizing scientific contributions, explicitly bounding findings, and setting future trajectories.

### The 4 Pillars of a Scholarly Conclusion
1. **Restatement of Objectives & Core Achievement**: Summarize the initial research problem and concisely state how the proposed work resolved it without repeating the abstract word-for-word.
2. **Synthesis of Principal Findings**: Reiterate key quantitative highlights and theoretical insights established in the discussion.
3. **Explicit Methodological Limitations**: Acknowledge valid constraints of the study (e.g., dataset scale, demographic coverage, computational overhead, assumption boundaries). Acknowledging limitations demonstrates scholarly maturity and preempts reviewer critique.
4. **Actionable Future Research Directions**: Propose 2–3 concrete, technically grounded next steps (e.g., *"Extending the latent fusion mechanism to continuous video streams"* rather than vague platitudes like *"More research is needed"*).
