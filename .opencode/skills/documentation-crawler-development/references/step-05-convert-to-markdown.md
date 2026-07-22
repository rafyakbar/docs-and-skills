# Step 5: Convert HTML to Markdown

## Purpose

Read each raw HTML file, extract the main content area, strip image tags, convert to clean Markdown, and save individual `.md` files.

## Code

```python
with open(REFERENCES_JSON, "r", encoding="utf-8") as f:
    entries = json.load(f)

print(f"Total entries to convert: {len(entries)}")

options = ConversionOptions(heading_style="atx", wrap=False)
conversion_errors = []

for entry in tqdm(entries, desc="Converting"):
    html_filename = f"{entry['idx']:03d}_{entry['slug']}.html"
    html_path = os.path.join(HTML_DIR, html_filename)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    content_div = soup.select_one(CONTENT_SELECTOR)

    if content_div is None:
        conversion_errors.append(f"Content container not found in: {html_filename}")
        continue

    for tag in ["img", "svg", "picture", "source"]:
        for element in content_div.find_all(tag):
            element.decompose()

    result = convert(str(content_div), options)

    md_filename = html_filename.replace(".html", ".md")
    md_file_path = os.path.join(REFERENCES_DIR, md_filename)

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(result.content)

if conversion_errors:
    print(f"\nConversion errors ({len(conversion_errors)}):")
    for err in conversion_errors:
        print(f"  {err}")

print(f"\nConversion completed. Files saved in: {REFERENCES_DIR}")
```

## Step-by-Step Explanation

### 1. Read Metadata

```python
with open(REFERENCES_JSON, "r", encoding="utf-8") as f:
    entries = json.load(f)
```

Same pattern as Step 4. Each cell reads `references.json` independently.

### 2. Configure Conversion Options

```python
options = ConversionOptions(heading_style="atx", wrap=False)
```

- **`heading_style="atx"`**: Produces `# Heading` instead of the alternative Setext style (`Heading\n======`). ATX is more compact and consistent.
- **`wrap=False`**: Disables automatic line wrapping. Documentation text converted to Markdown should preserve the original paragraph structure, not be reflowed at a specific column width.

### 3. Read HTML and Parse

```python
html_filename = f"{entry['idx']:03d}_{entry['slug']}.html"
html_path = os.path.join(HTML_DIR, html_filename)

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")
```

Constructs the filename using the same pattern as Step 4, reads the HTML file, and parses it with BeautifulSoup.

### 4. Extract Content Container

```python
content_div = soup.select_one(CONTENT_SELECTOR)

if content_div is None:
    conversion_errors.append(f"Content container not found in: {html_filename}")
    continue
```

Uses the `CONTENT_SELECTOR` found during site inspection to isolate the main documentation body. This is critical because the raw HTML includes:

- Navigation headers and footers
- Sidebar menus
- Search bars
- Theme/script tags

By selecting only the content container, we get clean documentation text without boilerplate.

If a file doesn't have the expected container, it's logged as an error and skipped rather than crashing the entire conversion.

### 5. Remove Image Tags

```python
for tag in ["img", "svg", "picture", "source"]:
    for element in content_div.find_all(tag):
        element.decompose()
```

Removes all image-related tags before Markdown conversion. Why?

- Images don't convert well to Markdown — their `alt` text is often empty or uninformative
- SVGs add massive amounts of inline XML that bloats the output
- The output is meant as a text reference, not a visual replica

**`decompose()` vs `extract()`**: `decompose()` removes the tag and all its children from the tree permanently. `extract()` returns the removed tag, which we don't need.

### 6. Convert to Markdown

```python
result = convert(str(content_div), options)
```

Converts the HTML snippet to Markdown using the `html_to_markdown` library.

**Important**: The library returns a `ConversionResult` object, not a string. Access the Markdown text via `result.content`.

### 7. Save Markdown File

```python
md_filename = html_filename.replace(".html", ".md")
md_file_path = os.path.join(REFERENCES_DIR, md_filename)

with open(md_file_path, "w", encoding="utf-8") as f:
    f.write(result.content)
```

Mirrors the HTML filename exactly but with a `.md` extension. This ensures a one-to-one mapping:

```text
html/001_what-is-filament.html  →  references/001_what-is-filament.md
html/002_installation.html       →  references/002_installation.md
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Content container not found | `CONTENT_SELECTOR` is wrong for this site | Re-inspect the site and update the selector |
| Output has random navigation text | Content selector is too broad — includes sidebar | Narrow the selector to the main content area |
| Output is empty | Content exists but selector doesn't match | Check if the HTML structure differs between pages |
| `TypeError: write() argument must be str` | Writing `result` instead of `result.content` | Use `result.content` (the library returns a `ConversionResult` object) |
| Garbled characters (Unicode issues) | Wrong encoding when reading HTML | Ensure `encoding="utf-8"` in both read and write |
