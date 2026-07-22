# Step 4: Crawl Each Page

## Purpose

Read the link metadata from `references.json`, download each documentation page, and save the raw HTML to `HTML_DIR`. Implements file-age caching so existing files within `MAX_AGE_DAYS` are skipped on subsequent runs.

## Code

```python
print("Starting crawling process...")

with open(REFERENCES_JSON, "r", encoding="utf-8") as f:
    entries = json.load(f)

errors = []
skipped = 0

for entry in tqdm(entries, desc="Crawling"):
    filename = f"{entry['idx']:03d}_{entry['slug']}.html"
    file_path = os.path.join(HTML_DIR, filename)

    if os.path.exists(file_path):
        file_age = time.time() - os.path.getmtime(file_path)
        if file_age < MAX_AGE_SECONDS:
            skipped += 1
            continue

    try:
        r = requests.get(entry["url"], headers=HEADERS)
        r.raise_for_status()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(r.text)

        time.sleep(random.uniform(*DELAY_RANGE))

    except Exception as e:
        errors.append(f"Failed {entry['url']}: {e}")

if skipped:
    print(f"\nSkipped {skipped} files (cached within {MAX_AGE_DAYS} days).")
if errors:
    print(f"\nErrors encountered ({len(errors)}):")
    for err in errors:
        print(f"  {err}")

print(f"\nCrawling finished. Files saved in: {HTML_DIR}")
```

## Step-by-Step Explanation

### 1. Read Metadata

```python
with open(REFERENCES_JSON, "r", encoding="utf-8") as f:
    entries = json.load(f)
```

Reads the JSON file saved by Step 3. This is the only connection between the two cells — no variable sharing. The structure is an array of `{idx, title, slug, url}` objects.

### 2. File Path Construction

```python
filename = f"{entry['idx']:03d}_{entry['slug']}.html"
file_path = os.path.join(HTML_DIR, filename)
```

- **Zero-padded prefix** (`:03d`): Produces `001`, `002`, ... `145`. This ensures files sort alphabetically in the same order as they appear in the sidebar.
- **Slug**: The sanitized filename from Step 3.
- **Full path**: Joins the output directory with the filename.

Example: `docs/filament_v5/html/001_what-is-filament.html`

### 3. File-Age Caching

```python
if os.path.exists(file_path):
    file_age = time.time() - os.path.getmtime(file_path)
    if file_age < MAX_AGE_SECONDS:
        skipped += 1
        continue
```

This is the `MAX_AGE_DAYS` implementation:

1. **Check existence**: `os.path.exists(file_path)` — does the file already exist?
2. **Calculate age**: `time.time() - os.path.getmtime(file_path)` — get the file's last modified time as a Unix timestamp, subtract it from now to get the age in seconds.
3. **Compare**: If the age is less than `MAX_AGE_SECONDS` (7 days converted to seconds), skip the download.

**Why `time.time() - os.path.getmtime()` instead of `date.today()`?**

- `os.path.getmtime()` returns the actual file modification timestamp, which is more reliable than comparing dates.
- `MAX_AGE_SECONDS` is computed once at the start (`MAX_AGE_DAYS * 86400`), so the comparison is a simple numeric check.
- This approach works correctly even if the computer sleeps between runs.

### 4. Download with Error Handling

```python
try:
    r = requests.get(entry["url"], headers=HEADERS)
    r.raise_for_status()

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(r.text)

    time.sleep(random.uniform(*DELAY_RANGE))

except Exception as e:
    errors.append(f"Failed {entry['url']}: {e}")
```

- **Individual try/except**: Each page is wrapped in its own error handler. A failure on one page doesn't stop the entire crawl.
- **`raise_for_status()`**: Catches HTTP errors (404, 500, etc.).
- **Save raw HTML**: `r.text` preserves the exact HTML response, including any embedded scripts or styles.
- **Polite delay**: `random.uniform(*DELAY_RANGE)` sleeps between 0.2 and 0.6 seconds. The `*` operator unpacks the tuple into two arguments.
- **Error collection**: Failed URLs are stored in a list and printed after the loop completes, so the progress bar stays clean.

### 5. Summary Output

```python
if skipped:
    print(f"\nSkipped {skipped} files (cached within {MAX_AGE_DAYS} days).")
if errors:
    print(f"\nErrors encountered ({len(errors)}):")
    for err in errors:
        print(f"  {err}")

print(f"\nCrawling finished. Files saved in: {HTML_DIR}")
```

Reports how many files were skipped (cached), how many failed (if any), and the final output location.

## Expected Output

```
Crawling: 100%|██████████| 145/145 [01:57<00:00,  1.23it/s]
Crawling finished. Files saved in: docs/filament_v5/html
```

On a second run (with cache):

```
Crawling: 100%|██████████| 145/145 [00:00<00:00, 1450it/s]
Skipped 145 files (cached within 7 days).
Crawling finished. Files saved in: docs/filament_v5/html
```

Note the dramatic speed difference — cached files are skipped instantly.
