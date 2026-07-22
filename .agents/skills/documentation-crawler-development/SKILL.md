---
name: documentation-crawler-development
description: "Activate when creating or modifying documentation web crawlers in Jupyter Notebooks (.ipynb) that scrape documentation websites and convert them to structured Markdown. Covers crawling scripts using Python (requests, BeautifulSoup, html_to_markdown), sidebar link extraction, HTML-to-Markdown conversion, image tag removal, and output organization under docs/. Use when working with PROMPTEN.md, PROMPTID.md, or any .ipynb crawler. Do NOT activate for non-crawling notebooks, pure Python scripts, or frontend/backend project code."
license: MIT
metadata:
  author: Rafy
---

# Documentation Crawler Development

## Overview

Instructions for building documentation web crawlers in Jupyter Notebooks. A crawler scrapes all pages from a documentation website via its sidebar menu, saves raw HTML, then converts everything to structured Markdown files organized under `docs/<topic>_v<version>/`.

## Workflow Overview

The crawler creation follows this exact flow:

1. **Ask for URL** — if user didn't provide one, ask before proceeding
2. **Inspect site** — manually visit the URL to find sidebar/content CSS selectors
3. **Create notebook** — build `filament-v5.ipynb` with 6 steps, do NOT execute
4. **Instruct user** — tell user to run notebook from Step 1 to Step 6
5. **Wait for user** — user must notify AI when notebook execution is complete
6. **Read all files** — AI reads every `.md` in `references/` to extract accurate summaries
7. **Update references.md** — AI rewrites `references.md` with proper section groupings and at least 1 short paragraph per entry

## Ask for URL if Not Provided

If the user activates this skill but does **not** provide a target documentation URL, the AI must ask for it before proceeding. Do not guess or assume the URL. Examples:

- "What documentation URL do you want to crawl?"
- "Please provide the starting documentation page URL."

Wait for the user's response before continuing.

## When to Activate

- User asks to crawl a documentation website
- User works with PROMPTEN.md or PROMPTID.md prompt templates
- User creates or edits an .ipynb crawler for any doc site
- User references `html_to_markdown`, `BeautifulSoup`, sidebar selectors
- User asks to generate `references.md` or `references/` structured docs
- User mentions documentation-crawler-development skill

## When NOT to Activate

- Non-crawling notebooks (ML, EDA, ETL, etc.)
- Pure Python scripts (.py) — use jupyter-notebook-development instead
- Non-crawler project code

## Scope

- **In scope:** Documentation crawler notebooks, PROMPTEN.md / PROMPTID.md prompts, sidebar extraction, HTML-to-Markdown conversion, output structuring
- **Out of scope:** Non-crawler notebooks, non-documentation scraping, frontend/backend code, AI agent configuration

## Dependency: Use jupyter-notebook-development Skill

When writing `.ipynb` notebook cells, first load the `jupyter-notebook-development` skill which provides:
- Cell structure conventions (one cell, one purpose)
- Configuration separation pattern
- tqdm progress bar usage
- Markdown documentation standards
- Grouped imports

Always activate both skills when creating a crawler notebook.

## Manual Site Inspection (Step 2)

Before writing any code, the AI must **manually visit the target URL** to inspect the HTML structure. This is critical because every site uses different CSS classes and HTML containers.

### What to Inspect

1. **Sidebar/menu container** — find the HTML element that holds documentation navigation links
2. **Menu link pattern** — identify which `<a href>` links point to actual documentation pages vs. external/anchor links
3. **Main content container** — find the element wrapping the documentation body text
4. **Image placement** — note where `img`, `svg`, `picture` tags appear so they can be removed

### How to Inspect

Use `webfetch` tool or write a small Python script with `requests` + `BeautifulSoup` to print the parsed structure. Look for unique CSS classes, `id` attributes, or custom HTML tags that can serve as selectors.

### Document Findings

Record the selectors before generating code. This becomes the basis for the notebook's `SIDEBAR_SELECTOR` and `CONTENT_SELECTOR` config variables.

### Beware of Client-Side Rendering

Some documentation sites are client-side rendered (SPA/Next.js). In such cases, `requests.get()` may not return the full HTML. If the sidebar or content area appears empty, try:
- Checking if content is loaded via JavaScript (use `webfetch` tool or check the raw HTML response)
- If the site is client-side rendered, you may need to use a different approach or select a static version of the docs

## Directory Structure Convention

All crawled documentation must follow this structure:

```text
docs/
└── <topic>_v<version>/
    ├── references.json           ← AI/notebook-generated index metadata (title, slug, url per entry)
    ├── references.md             ← AI-authored index file with section groupings and descriptions
    ├── references/               ← Individual detailed Markdown files
    │   ├── 001_<subject>.md
    │   ├── 002_<subject>.md
    │   └── ...
    └── html/                     ← Temporary raw HTML downloads
        ├── 001_<subject>.html
        ├── 002_<subject>.html
        └── ...
```

### Naming Rules

- `topic`: lowercase, kebab-case (e.g., `livewire`, `fluxui`, `alpinejs`)
- `version`: use `v<major>` format (e.g., `v4`, `v5`, `v3`, `v2`)
- Example: `docs/livewire_v4/`, `docs/fluxui_v2/`, `docs/alpinejs_v3/`
- `references.json`: link metadata saved by Step 3, consumed by Steps 4-6
- `references.md`: the AI-authored index file with section groupings and descriptions
- `references/`: contains individually numbered markdown files with 3-digit zero padding

### Configuration Variables

```python
NAME = "<topic>-v<version>"                    # e.g. "filament-v5"
BASE_URL = "https://filamentphp.com"           # Documentation site base URL
START_URL = "https://filamentphp.com/docs/..." # Starting page

BASE_DIR = f"docs/{NAME.replace('-', '_')}"    # e.g. "docs/filament_v5"
HTML_DIR = f"{BASE_DIR}/html"                  # Raw HTML files (temporary)
REFERENCES_DIR = f"{BASE_DIR}/references"      # Individual markdown files
REFERENCES_JSON = os.path.join(BASE_DIR, "references.json")  # Link metadata
```

## Step-by-Step Notebook Implementation

The notebook must have exactly these cells. Each code cell must have a Markdown cell above it explaining the purpose.

### Cell Layout

| # | Type | Content |
|---|------|---------|
| 1 | Markdown | Title + introduction |
| 2 | Markdown | Library Imports header |
| 3 | Code | Grouped imports |
| 4 | Markdown | Configuration header |
| 5 | Code | All config variables, `os.makedirs()` |
| 6 | Markdown | Step 2 header |
| 7 | Code | Fetch start page, parse with BeautifulSoup |
| 8 | Markdown | Step 3 header |
| 9 | Code | Extract sidebar links, save to `references.json` |
| 10 | Markdown | Step 4 header |
| 11 | Code | Read JSON, crawl each page with caching |
| 12 | Markdown | Step 5 header |
| 13 | Code | Read JSON, convert HTML to Markdown |
| 14 | Markdown | Step 6 header |
| 15 | Code | Read JSON, generate `references.md` |
| 16 | Markdown | Summary |

### Step 1: Configuration

See [`references/step-01-configuration.md`](references/step-01-configuration.md) for detailed explanation.

Create a dedicated cell with all tunable parameters. Include:

- `NAME`, `BASE_URL`, `START_URL`
- `BASE_DIR`, `HTML_DIR`, `REFERENCES_DIR`, `REFERENCES_JSON`
- `DELAY_RANGE = (0.2, 0.6)`
- `MAX_AGE_DAYS = 7` and `MAX_AGE_SECONDS = MAX_AGE_DAYS * 86400`
- `HEADERS` with browser-like User-Agent
- `SIDEBAR_SELECTOR` and `CONTENT_SELECTOR` (found during site inspection)
- Print all variables and create directories with `os.makedirs()`

### Step 2: Fetch Start Page

See [`references/step-02-fetch-start-page.md`](references/step-02-fetch-start-page.md) for detailed explanation.

Send HTTP GET to `START_URL`, parse with `BeautifulSoup`, store in `soup` variable.

### Step 3: Extract Sidebar Menu Links

See [`references/step-03-extract-links.md`](references/step-03-extract-links.md) for detailed explanation.

Using the selector from site inspection:
1. Find sidebar container with `soup.select_one(SIDEBAR_SELECTOR)`
2. Extract all `<a href>` links, filter for internal doc paths
3. Deduplicate with a set
4. Slugify menu text into safe filenames (lowercase, hyphens, no special chars)
5. Save to `references.json` as array of `{"title": ..., "slug": ..., "url": ...}`

### Step 4: Crawl Each Page

See [`references/step-04-crawl-pages.md`](references/step-04-crawl-pages.md) for detailed explanation.

1. Read `references.json`
2. Iterate with `tqdm`, build filename as `{idx:03d}_{slug}.html`
3. Check `MAX_AGE_DAYS` cache: if file exists and age < `MAX_AGE_SECONDS`, skip
4. Download, save, apply random delay
5. Collect errors in a list and print after loop

### Step 5: Convert HTML to Markdown

See [`references/step-05-convert-to-markdown.md`](references/step-05-convert-to-markdown.md) for detailed explanation.

1. Read `references.json`
2. For each entry, read HTML file, find content container with `CONTENT_SELECTOR`
3. Remove `img`, `svg`, `picture`, `source` tags
4. Convert with `html_to_markdown.convert()` (`heading_style="atx"`, `wrap=False`)
5. Use `result.content` (the library returns a `ConversionResult` object)
6. Save as `.md` with matching filename

### Step 6: Generate references.md Index

See [`references/step-06-generate-index.md`](references/step-06-generate-index.md) for detailed explanation.

1. Read `references.json`
2. Build a bullet list using original `title` from the sidebar
3. Save as `references.md` at `BASE_DIR`

## After Notebook Execution (AI Task)

Once the user finishes running the notebook, the AI must:

1. **Read every `.md` file** in `references/` to extract the H1 title and first meaningful paragraph
2. **Update `references.md`** with:
   - Section groupings based on the documentation sidebar structure
   - At least 1 short paragraph description per entry (extracted from the actual content)
   - Accurate titles from the H1 of each page

Use a Python script or read files individually to ensure descriptions are accurate.

## Inline Comments Convention

Use English inline comments explaining key steps, parameters, and non-obvious logic.

```python
# Project identifier and URLs
NAME = "filament-v5"

# Throttle between requests to avoid rate-limiting
DELAY_RANGE = (0.2, 0.6)
```

Do NOT use bilingual (EN+ID) comments. Do NOT use decorative `# =====` section comment blocks — the Markdown cells already explain each section.

## Common Python Libraries

```python
import os
import re
import time
import random
import json
import warnings
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from html_to_markdown import convert, ConversionOptions
```

## Content Selectors (Per-Site)

Each documentation site has different HTML structure. Always inspect the site first:

| Website | Sidebar Selector | Content Selector |
|---------|-----------------|-----------------|
| Livewire v4 | `ul.list-none.space-y-5...` | `div.pt-12.docsearch-content...` |
| Alpine.js v3 | `aside` | `div.m-auto.max-w-3xl...` |
| Filament v5 | `div#navigation-items` | `div#content-area` |
| FluxUI v2 | `ui-sidebar` | `div[data-flux-main]` |

## Image Tag Removal

Always remove image-related tags (`img`, `svg`, `picture`, `source`) before Markdown conversion to keep output files lean.

## Do and Don't

| Do | Don't |
|----|-------|
| Ask for URL if user didn't provide one | Guess or assume the target URL |
| Manually inspect the site before coding | Write crawler without verifying HTML structure |
| Use `HEADERS`, `DELAY_RANGE`, `MAX_AGE_DAYS` config vars | Hardcode headers or skip delays |
| Use English-only inline comments | Use decorative `# ====` section blocks |
| Load jupyter-notebook-development skill for .ipynb | Write crawlers as pure .py scripts |
| Use `REFERENCES_JSON` for cross-cell data sharing | Rely on variables from previous cells |
| Implement `MAX_AGE_DAYS` cache in Step 4 | Forget to implement caching |
| Follow required cell layout (16 cells) | Add extra cells or merge steps |
| Create notebook but do NOT execute | Run the notebook for the user |
| Wait for user to finish before updating references.md | Update references.md without reading actual content |
| Read every `.md` file to write accurate descriptions | Guess or hallucinate descriptions |
| Write at least 1 short paragraph per entry | Use one-liner or empty descriptions |
| Use 3-digit zero padding (`001`, `002`) | Use 4-digit padding or no padding |
| Save raw HTML in `html/` folder | Save in `htmls/` or mix with markdown |
| Inspect site for correct sidebar/content selectors | Hardcode selectors without verification |
| Remove image tags before conversion | Leave img/svg tags that bloat output |
| Use tqdm with error collection after loop | Call `print()` inside tqdm loop |
| Use `result.content` for ConversionResult | Write `result` directly to file |
| Compute paths inline in each cell | Rely on keys set by a previous cell |

## References

- `references/step-01-configuration.md` — Detailed explanation of all config variables
- `references/step-02-fetch-start-page.md` — Fetching, parsing, troubleshooting
- `references/step-03-extract-links.md` — Sidebar extraction, slugify, JSON output
- `references/step-04-crawl-pages.md` — Download with caching and delay
- `references/step-05-convert-to-markdown.md` — Content extraction, image removal, conversion
- `references/step-06-generate-index.md` — Build references.md from JSON
- `references/known-selectors.md` — Known site selector patterns and troubleshooting
- `jupyter-notebook-development` skill — Notebook structure and conventions (load before writing .ipynb cells)
