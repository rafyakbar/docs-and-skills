---
name: jupyter-notebook-development
description: "Activate when creating, editing, or reviewing Jupyter Notebook (.ipynb) files for data analysis, machine learning, deep learning, web crawling, ETL, EDA, big data, or benchmarking. Covers notebook structure conventions, Markdown documentation, configuration separation, function extraction, reproducibility, and template patterns for ML/DL, crawling, EDA, cleaning, big data, ETL, and benchmark notebooks. Do NOT activate for pure Python scripts (.py), non-notebook code files, or when the task is about configuring AI agents or skills."
license: MIT
metadata:
  author: Rafy
---

# Jupyter Notebook Development

## Overview

Guidelines for writing **Jupyter Notebooks (`.ipynb`)** using best practices for structure, readability, maintainability, extensibility, and reproducibility. Suitable for research, data analysis, Machine Learning, Deep Learning, Big Data, Web Crawling, ETL, and experimentation.

A notebook is not just a place to run code; it is a **technical document** that communicates the thought process, experiments, implementation, and results.

## When to Activate

- User creates, edits, or reviews `.ipynb` files
- User works on data analysis, EDA, machine learning, deep learning
- User works on web crawling, scraping, data cleaning, preprocessing
- User works on ETL pipeline, big data processing, or benchmarking
- User mentions "notebook", "jupyter", ".ipynb", "colab"

## When NOT to Activate

- Pure Python scripts (`.py`) or non-notebook code files
- AI agent or skill configuration
- Documentation files other than notebooks

## Scope

- **In scope:** Notebook structure, Markdown documentation, configuration separation, function extraction, reproducibility, templates for ML/DL, crawling, EDA, cleaning, big data, ETL, benchmark
- **Out of scope:** Pure Python scripts, AI agent configuration, non-notebook documentation

## General Principles

- Have a single main objective
- Use a clear structure with Markdown explaining each stage
- Runnable from scratch via **Restart Kernel → Run All**, not dependent on cell execution order
- Separate configuration from program logic
- When making HTTP requests, use browser-like headers and a random delay range (`0.2-0.6s`)

## Patterns & Conventions

### 1. Cell Structure

One cell, one purpose. Never mix multiple processes in a single cell. Every code cell must have a Markdown cell directly above it explaining what the code does and why.

### 2. Comments Inside Code Cells

Include inline comments explaining key steps, parameters, and non-obvious logic. Comments should explain **why** something is done, not just **what**.

### 3. Informative Print Statements

Every code cell must include `print()` statements displaying key variables, shapes, sample data, or results. Use `display()` for DataFrames.

### 4. Configuration Separation

Place all tunable values in a dedicated cell at the top. Print each variable so the user can see the configuration at a glance. Avoid magic numbers.

```python
RANDOM_SEED = 42
BATCH_SIZE = 32
DATASET_PATH = 'data/dataset.csv'
DELAY_RANGE = (0.2, 0.6)
```

### 5. Use Functions

Logic used more than once must be extracted into `utils.py`. When it exceeds ~200 lines, refactor into a `utils/` package (see `references/utils-package.md`). The notebook must only import from `utils`, never from sub-modules directly.

### 6. Group Imports

Order: Standard Library, Third-party, Visualization, ML/DL, Utility. Always include `import warnings; warnings.filterwarnings('ignore')`.

### 7. Reproducibility

Must run from start to finish without errors. For short-running notebooks, verify via **Restart Kernel → Run All**. For long-running notebooks, ensure correct cell dependencies.

### 8. File Age Caching

Use `MAX_AGE_DAYS` with `time.time() - os.path.getmtime()` comparison, not `date.today()`.

### 9. tqdm Progress Bars

Use tqdm directly in the for loop. Collect errors in a list and print them after the loop to avoid breaking the progress bar display.

```python
for item in tqdm(all_items, desc='Processing'):
    try:
        ...
    except Exception as e:
        errors.append(f'{item}: {e}')
```

Never call `print()` inside a tqdm loop.

### 10. Cell Independence

Each cell should compute its own file paths and not rely on keys set by previous cells.

### 11. Browser Headers for HTTP

Include browser-like headers when scraping. Use `random.uniform()` delay between requests.

## Notebook Templates

Cells 1-3 (Title/Introduction, Library Imports, Configuration) are **mandatory** in every notebook. See `references/templates.md` for detailed template tables for ML/DL, crawling, EDA, cleaning, and generic notebooks.

| Section | Content |
|---------|---------|
| 1. Title & Introduction | Markdown: objective, dataset, approach |
| 2. Library Imports | All imports grouped by category |
| 3. Configuration | All tunable parameters |
| 4+. Workflow | Task-specific cells (see templates) |
| Last. Conclusion | Markdown: summary of results |

## Do and Don't

| Do | Don't |
|----|-------|
| Use Markdown for each major section | Put everything in one cell |
| Separate configuration from logic | Use magic numbers or hard-coded values |
| Use functions for repeated logic | Copy-paste duplicate code |
| Move large functions to `utils.py` / `utils/` | Keep 200+ line functions in the notebook |
| Include inline comments in every code cell | Write code cells without explanation |
| Print key variables for intermediate results | Print excessively long or binary output |
| Set random seed for reproducibility | Create notebooks dependent on execution order |
| Compute paths inline in each cell | Rely on keys set by a previous cell |
| Use tqdm in the for loop, collect errors after | Call `print()` inside tqdm loops |
| Use `time.time() - getmtime()` for caching | Use `date.today()` comparison |
| Clear notebook output before Git commit | Keep thousands of lines of unnecessary output |

## Checklist

Before finalizing a notebook, ensure:

### Structure
- [ ] Clear objective defined
- [ ] Cell structure is consistent, one purpose per cell
- [ ] Markdown explains each stage before code cells
- [ ] Imports appear only once at the top, grouped by category
- [ ] Configuration is in one dedicated cell, no magic numbers

### Code Quality
- [ ] No duplicated code; functions extracted to `utils.py`
- [ ] Variable names are self-explanatory
- [ ] Inline comments explain key logic in every code cell
- [ ] `print()` or `display()` shows key variables after each cell
- [ ] Random seed set for reproducibility

### Correctness
- [ ] Notebook is reproducible (or correct cell dependency order)
- [ ] File paths computed inline, no cross-cell dependencies
- [ ] Visualizations have titles and axis labels
- [ ] Final results include a summary or conclusion

### Crawling-Specific
- [ ] `HEADERS`, `DELAY_RANGE`, `MAX_AGE_DAYS` configured
- [ ] tqdm used in the for loop, errors collected in list
- [ ] Output cells cleared before Git commit

### References
- `references/utils-package.md` — Full utils package pattern and examples
- `references/templates.md` — Detailed notebook templates for all task types
- `references/crawling-pattern.md` — Full web crawling code pattern
