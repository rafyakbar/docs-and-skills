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

## Manual Site Inspection

Before writing any code (especially Steps 2-4), the AI must **manually visit the target URL** to inspect the HTML structure of the documentation site. This is critical because every site uses different CSS classes and HTML containers.

### What to Inspect

1. **Sidebar/menu container** — find the HTML element that holds the documentation navigation links
2. **Menu link pattern** — identify which `<a href>` links point to actual documentation pages vs. external/anchor links
3. **Main content container** — find the element that wraps the documentation body text
4. **Image placement** — note where `img`, `svg`, `picture` tags appear so they can be removed

### How to Inspect

Use browser DevTools or fetch the page with `requests` + `BeautifulSoup` to print the parsed structure. Look for unique CSS classes, `id` attributes, or custom HTML tags (`<ui-sidebar>`, `[data-flux-main]`, etc.) that can serve as selectors.

### Document Findings

Record the selectors before generating code. This becomes the basis for Steps 2-5.

## Directory Structure Convention

All crawled documentation must follow this structure:

```text
docs/
└── <topic>_v<version>/
    ├── references.md              ← Combined index/overview Markdown file (REQUIRED)
    ├── references/                ← Individual detailed Markdown files
    │   ├── 001_<subject>.md
    │   ├── 002_<subject>.md
    │   └── ...
    └── html/                     ← Temporary raw HTML downloads (Step 4 output)
        ├── 001_<subject>.html
        ├── 002_<subject>.html
        └── ...
```

### Naming Rules

- `topic`: lowercase, kebab-case (e.g., `livewire`, `fluxui`, `alpinejs`)
- `version`: use `v<major>` format (e.g., `v4`, `v5`, `v3`, `v2`)
- Example: `docs/livewire_v4/`, `docs/fluxui_v2/`, `docs/alpinejs_v3/`
- `references.md`: the combined index/overview markdown file (replaces the old `<name>.md` pattern)
- `references/`: contains individually numbered markdown files

### Configuration Variables

```python
NAME = "<topic>-v<version>"                    # e.g. "livewire-v4"
BASE_URL = "https://example.com"               # Documentation site base URL
START_URL = "https://example.com/docs/start"   # Starting page

BASE_DIR = f"docs/{NAME.replace('-', '_')}"    # e.g. "docs/livewire_v4"
HTML_DIR = f"{BASE_DIR}/html"                  # Raw HTML files (temporary)
REFERENCES_DIR = f"{BASE_DIR}/references"      # Individual markdown files
REFERENCES_MD = os.path.join(BASE_DIR, "references.md")  # Combined markdown
```

## Step-by-Step Crawler Implementation

### Step 1: Configuration

Create a dedicated cell with all tunable parameters. Define `NAME`, `BASE_URL`, `START_URL`, `BASE_DIR`, `HTML_DIR`, `REFERENCES_DIR`, `REFERENCES_MD`. Create output directories with `os.makedirs()`. Set browser-like `headers`.

### Step 2: Fetch Start Page

Send an HTTP GET to `START_URL` with `requests.get()`, parse response with `BeautifulSoup`.

### Step 3: Extract Sidebar Menu Links

Using the selector found during Manual Site Inspection, find the sidebar container, extract all `<a href>` links, filter for internal doc paths only, deduplicate with a set, clean menu text into safe filenames with `re.sub(r'[\\/*?:"<>|]', "", text)`.

### Step 4: Crawl Each Page

Iterate with `tqdm`. Save each page to `HTML_DIR` with **3-digit zero-padded** prefix (`{idx:03d}`). Collect errors in a list and print after the loop.

### Step 5: Convert HTML to Markdown

For each HTML file:
1. Read the HTML
2. Find the main content container using the selector found during inspection
3. Remove image-related tags (`img`, `svg`, `picture`, `source`)
4. Convert to Markdown with `html_to_markdown.convert()` (`heading_style="atx"`, `wrap=False`)
5. Save individual `.md` to `REFERENCES_DIR`
6. Combine all sections into `REFERENCES_MD`

See `references/detailed-code-patterns.md` for complete runnable code for all 5 steps.

## Comments Convention

Only use English comments. Label sections with `# ==== Section Name ====` style.

```python
# ==============================
# Configuration
# ==============================

# Project name used for naming the final markdown file
NAME = "livewire-v4"

# Base URL of the documentation website
BASE_URL = "https://livewire.laravel.com"
```

Do NOT use bilingual (EN+ID) comments. English only.

## Common Python Libraries

```python
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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

When creating a crawler for a new site, instruct the user to:
1. Open the documentation page in a browser
2. Inspect the sidebar menu element to find a unique selector
3. Inspect the main content area to find a unique selector
4. Update the script accordingly

## Image Tag Removal

Always remove image-related tags (`img`, `svg`, `picture`, `source`) before Markdown conversion to keep output files lean. See Step 5 for the standard pattern.

## Do and Don't

| Do | Don't |
|----|-------|
| Ask for URL if user didn't provide one | Guess or assume the target URL |
| Manually inspect the site before coding | Write crawler without verifying HTML structure |
| Use English-only comments | Use bilingual (EN+ID) comments |
| Load jupyter-notebook-development skill for .ipynb | Write crawlers as pure .py scripts |
| Follow `docs/<topic>_v<version>/` convention with `html/` + `references/` | Use old `docs/<name>-<versionx>/` convention |
| Define `references.md` as combined output | Use `<name>.md` as combined output |
| Use 3-digit zero padding (`001`, `002`, ...) | Use 4-digit padding or no padding |
| Save raw HTML in `html/` folder | Save HTML in `htmls/` or mix with markdown |
| Inspect site for correct sidebar/content selectors | Hardcode selectors without verification |
| Remove image tags before conversion | Leave img/svg tags that bloat output |
| Use tqdm with error collection after loop | Call print() inside tqdm loop |
| Compute paths inline in each cell | Rely on variables from previous cells |

## References

- `references/detailed-code-patterns.md` — Complete runnable code for all 5 steps + known site selectors table
- `jupyter-notebook-development` skill — Notebook structure and conventions
- Existing notebooks: `alpinejs-v3.ipynb`, `filament-v5.ipynb`, `fluxui-v2.ipynb`, `livewire-v4.ipynb`
- Prompt templates: `PROMPTEN.md`, `PROMPTID.md`
