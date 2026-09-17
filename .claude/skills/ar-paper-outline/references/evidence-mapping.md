# Evidence Mapping & CER Framework Guide

In academic writing, an outline is not merely a list of headings—it is an **argumentative and empirical blueprint**. This guide explains how to integrate Claim-Evidence-Reasoning (CER) and gap tracking into outlines.

---

## 1. The Claim-Evidence-Reasoning (CER) Pattern

For each substantive section of the outline, specify the argument chain:

```
┌──────────────────────────────────────────────────────────┐
│ CLAIM: What asserting statement is made in this section? │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ EVIDENCE: What empirical data, statistics, or citations   │
│           directly support this claim?                   │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ REASONING: How does the evidence logically demonstrate   │
│            the claim and connect to the broader thesis?  │
└──────────────────────────────────────────────────────────┘
```

### Example CER Breakdown in Outline Format

```markdown
#### 5.2 Findings for RQ1: AI Assistance Effect on Writing Latency
- **Target Budget**: 400 words (6.6% of paper)
- **Objective**: Report quantitative differences in task completion time between control and treatment groups.
- **CER Argument Map**:
  - **Claim**: Participants using AI assistants completed manuscript drafting 34% faster than the manual control group.
  - **Evidence**: ANOVA test results on experiment cohort ($F(1, 142) = 18.42, p < 0.001$, Cohen's $d = 0.72$), summarized in Table 2.
  - **Reasoning**: The automated retrieval and citation indexing modules significantly reduced cognitive overhead during initial literature synthesis.
- **Assigned Sources/Data**: Experiment Trial Dataset B, Table 2.
- **Visuals**: Table 2 (Completion time by task type).
```

---

## 2. Managing Material Gaps (`[MATERIAL GAP]`)

Before drafting begins, an outline must make missing evidence transparent. This prevents author halucinations, unsupported assertions, or phantom literature citations.

### Tagging Protocol

When a section requires a claim that currently lacks sufficient supporting data or verified literature, annotate it explicitly with:

```markdown
[MATERIAL GAP: <description of required data/source>]
```

### Severity Levels of Gaps

1. **Empirical Data Gap**:
   - `[MATERIAL GAP: Requires ANOVA post-hoc test results from survey cohort]`
   - *Action*: Flagged for data team / researcher to compute before drafting Section 5.3.
2. **Literature Support Gap**:
   - `[MATERIAL GAP: Need 2024-2026 citations on cross-disciplinary AI adoption in HEI]`
   - *Action*: Flagged for targeted literature search before drafting Section 3.2.
3. **Methodological Justification Gap**:
   - `[MATERIAL GAP: Justify why convenience sampling does not compromise internal validity]`
   - *Action*: Flagged for author to draft specific defense in Section 4.2.

---

## 3. Evidence Matrix Format

For papers handling extensive literature bases, generate an **Evidence-to-Section Matrix** at the end of the outline:

| Section | Core Claim | Primary Citation / Data Source | Status |
|---|---|---|:---:|
| 2.2 Problem Statement | AI integration creates new epistemic validation risks | Smith & Lee (2025); Nature (2026) | Verified |
| 3.1 Theoretical Model | Cognitive load theory explains drafting acceleration | Sweller (2011); Paas et al. (2024) | Verified |
| 4.3 Instruments | SUS survey demonstrates high interface usability | Usability trial scores ($n=85$) | Verified |
| 5.4 Long-term Retention | Long-term knowledge retention remains unaffected | `[MATERIAL GAP: Delayed post-test data pending]` | **GAP** |

This guarantees that when full drafting begins, every section has verified grounding.
