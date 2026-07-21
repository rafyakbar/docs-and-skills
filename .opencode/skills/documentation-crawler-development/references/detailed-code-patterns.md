# Detailed Code Patterns for Documentation Crawler

## Step 1: Configuration

```python
# ==============================
# Configuration
# ==============================

NAME = "livewire-v4"
BASE_URL = "https://livewire.laravel.com"
START_URL = "https://livewire.laravel.com/docs/4.x/quickstart"

BASE_DIR = f"docs/{NAME.replace('-', '_')}"
HTML_DIR = f"{BASE_DIR}/html"
REFERENCES_DIR = f"{BASE_DIR}/references"
REFERENCES_MD = os.path.join(BASE_DIR, "references.md")

print("Configuration:")
print(f"NAME        : {NAME}")
print(f"BASE_URL    : {BASE_URL}")
print(f"START_URL   : {START_URL}")
print(f"BASE_DIR    : {BASE_DIR}")
print(f"HTML_DIR    : {HTML_DIR}")
print(f"REFERENCES_DIR : {REFERENCES_DIR}")

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(REFERENCES_DIR, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}
```

## Step 2: Fetch Start Page

```python
# ==============================
# Step 2: Fetch Start Page
# ==============================

print("Fetching start page...")

response = requests.get(START_URL, headers=headers)
response.raise_for_status()

print("Start page successfully fetched")

soup = BeautifulSoup(response.text, "html.parser")
```

## Step 3: Extract Sidebar Menu Links

```python
# ==============================
# Step 3: Extract Sidebar Menu Links
# ==============================

print("Scanning sidebar menu...")

# Replace with the actual selector found during inspection
sidebar = soup.find("aside")

if sidebar is None:
    raise Exception("Sidebar menu not found!")

links = sidebar.find_all("a", href=True)

seen_urls = set()
final_items = []

for link in links:
    href = link["href"].strip()

    if not href.startswith("/docs"):
        continue

    full_url = urljoin(BASE_URL, href)

    if full_url in seen_urls:
        continue
    seen_urls.add(full_url)

    menu_name = link.get_text(strip=True)
    if not menu_name:
        continue

    safe_name = re.sub(r'[\\/*?:"<>|]', "", menu_name)
    final_items.append((safe_name, full_url))

print(f"Total menus found: {len(final_items)}")
```

## Step 4: Crawl Each Page

```python
# ==============================
# Step 4: Crawl Each Page
# ==============================

print("Starting crawling process...")
errors = []

for idx, (safe_name, url) in enumerate(tqdm(final_items), start=1):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()

        prefix = f"{idx:03d}"
        filename = f"{prefix}_{safe_name}.html"
        file_path = os.path.join(HTML_DIR, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(r.text)

    except Exception as e:
        errors.append(f"Failed {url}: {e}")

if errors:
    for err in errors:
        print(err)

print("Crawling finished.")
```

## Step 5: Convert HTML to Markdown

```python
# ==============================
# Step 5: Convert HTML to Markdown
# ==============================

html_files = sorted([f for f in os.listdir(HTML_DIR) if f.endswith(".html")])

print(f"Total HTML files found: {len(html_files)}")

options = ConversionOptions(heading_style="atx", wrap=False)
all_markdown_content = []

for filename in tqdm(html_files):
    file_path = os.path.join(HTML_DIR, filename)

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Replace with the actual content selector found during inspection
    content_div = soup.find("div", class_="doc-content")

    if content_div is None:
        print(f"Content not found in: {filename}")
        continue

    # Remove image-related tags before conversion
    for tag in ["img", "svg", "picture", "source"]:
        for element in content_div.find_all(tag):
            element.decompose()

    markdown = convert(str(content_div), options)

    md_filename = filename.replace(".html", ".md")
    md_file_path = os.path.join(REFERENCES_DIR, md_filename)

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    title = md_filename.replace(".md", "")
    section_header = f"\n\n# {title}\n\n"
    all_markdown_content.append(section_header + markdown)

final_markdown = "\n\n".join(all_markdown_content)

with open(REFERENCES_MD, "w", encoding="utf-8") as f:
    f.write(final_markdown)

print("Conversion completed.")
print(f"Individual files saved in: {REFERENCES_DIR}")
print(f"Combined file created: {REFERENCES_MD}")
```

## Known Site Selectors Reference

| Website | Sidebar Selector | Content Selector |
|---------|-----------------|-----------------|
| Livewire v4 | `ul.list-none.space-y-5.divide-y.divide-slate-700.px-3` | `div.pt-12.docsearch-content.overflow-hidden.flex-1.mx-auto.max-w-prose.w-full` |
| Alpine.js v3 | `aside` | `div.m-auto.max-w-3xl.px-6.pb-24.text-gray-800.antialiased.markdown` |
| Filament v5 | `div#navigation-items` | `div#content-area` |
| FluxUI v2 | `ui-sidebar` | `div[data-flux-main]` |
