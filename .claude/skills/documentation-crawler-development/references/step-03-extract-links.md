# Step 3: Extract Sidebar Menu Links

## Purpose

Find the sidebar navigation container, extract all documentation links, deduplicate them, slugify the menu text into safe filenames, assign sequential indices, and save everything to `references.json`. This JSON file is then consumed by Steps 4, 5, and 6, ensuring cell independence.

## Code

```python
print("Scanning sidebar menu...")

sidebar_container = soup.select_one(SIDEBAR_SELECTOR)

if sidebar_container is None:
    raise Exception(f"Sidebar container '{SIDEBAR_SELECTOR}' not found!")

links = sidebar_container.find_all("a", href=True)

entries = []
seen_urls = set()

for link in links:
    href = link["href"].strip()

    if not href.startswith("/docs/"):
        continue

    full_url = urljoin(BASE_URL, href)

    if full_url in seen_urls:
        continue
    seen_urls.add(full_url)

    title = link.get_text(strip=True)
    if not title:
        continue

    slug = title.lower().strip()
    slug = re.sub(r'[\\/*?:"<>| ]', "-", slug)
    slug = re.sub(r'-+', "-", slug).strip("-")
    entries.append({"title": title, "slug": slug, "url": full_url})

for idx, entry in enumerate(entries, start=1):
    entry["idx"] = idx

with open(REFERENCES_JSON, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print(f"Total menu items found: {len(entries)}")
print(f"Saved to: {REFERENCES_JSON}")
print(f"\nFirst 5 items:")
for entry in entries[:5]:
    print(f"  {entry['idx']:03d} - {entry['title']} -> {entry['url']}")
```

## Step-by-Step Explanation

### 1. Locate Sidebar Container

```python
sidebar_container = soup.select_one(SIDEBAR_SELECTOR)
```

Uses the CSS selector discovered during site inspection. `select_one()` returns the first matching element.

The selector varies per site. Common patterns:
- **ID selector**: `div#navigation-items`, `nav#sidebar`
- **Tag selector**: `aside`, `nav`
- **Class selector**: `ul.sidebar`, `div.menu`

### 2. Validate Sidebar Exists

```python
if sidebar_container is None:
    raise Exception(f"Sidebar container '{SIDEBAR_SELECTOR}' not found!")
```

If the sidebar isn't found, the remaining steps cannot proceed. The exception message includes the selector used, making it easy to debug — the selector is wrong, or the page structure changed.

### 3. Extract All Links

```python
links = sidebar_container.find_all("a", href=True)
```

Gets every anchor tag that has an `href` attribute within the sidebar. This includes both documentation links and other navigation elements (anchors, external links).

### 4. Filter and Deduplicate

```python
for link in links:
    href = link["href"].strip()

    if not href.startswith("/docs/"):
        continue

    full_url = urljoin(BASE_URL, href)

    if full_url in seen_urls:
        continue
    seen_urls.add(full_url)
```

**Filtering**: `href.startswith("/docs/")` keeps only internal documentation URLs. This filter must be customized for each site:
- `/docs/5.x/...` for versioned docs
- `/docs/` for unversioned docs
- `/en/docs/` for localized docs

**Deduplication**: The same URL might appear multiple times in a sidebar (e.g., nested menus where a parent page is also listed as a child). Using a `set` prevents duplicates. Always compare against the full resolved URL (`full_url`), not the relative `href`.

### 5. Extract and Slugify Title

```python
title = link.get_text(strip=True)
if not title:
    continue

slug = title.lower().strip()
slug = re.sub(r'[\\/*?:"<>| ]', "-", slug)
slug = re.sub(r'-+', "-", slug).strip("-")
entries.append({"title": title, "slug": slug, "url": full_url})
```

- **`title`**: The original menu text from the sidebar (e.g., "What is Filament?"). Preserved for display in `references.md`.
- **`slug`**: A filesystem-safe version of the title. The transformation does three things:
  1. `lower().strip()` — lowercase and trim
  2. Replace illegal filename characters AND spaces with hyphens: `re.sub(r'[\\/*?:"<>| ]', "-", ...)`
  3. Collapse multiple hyphens and strip leading/trailing ones: `re.sub(r'-+', "-", ...).strip("-")`

### 6. Assign Sequential Index

```python
for idx, entry in enumerate(entries, start=1):
    entry["idx"] = idx
```

Each entry gets a unique sequential number starting from 1. This becomes the `001`, `002`, ... prefix in filenames, ensuring consistent ordering across HTML, Markdown, and the index.

### 7. Save to JSON

```python
with open(REFERENCES_JSON, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)
```

Writes the entries as a JSON array. Key details:
- `encoding="utf-8"` — handles special characters in titles
- `indent=2` — human-readable output for debugging
- `ensure_ascii=False` — preserves non-ASCII characters (e.g., accented letters, em dashes) instead of escaping them

### Sample JSON Output

```json
[
  {
    "idx": 1,
    "title": "What is Filament?",
    "slug": "what-is-filament",
    "url": "https://filamentphp.com/docs/5.x/introduction/overview"
  },
  {
    "idx": 2,
    "title": "Installation",
    "slug": "installation",
    "url": "https://filamentphp.com/docs/5.x/introduction/installation"
  }
]
```

## Why Save to JSON Instead of Using Variables?

The jupyter-notebook-development skill requires **cell independence**: each cell must compute its own paths and not rely on variables set by a previous cell. Saving to `references.json` means:

- Step 4, 5, 6 each read the file independently
- The notebook works correctly even if cells are run out of order
- If execution is interrupted, progress is not lost
- The JSON file can be inspected or modified by the user
