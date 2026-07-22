# Step 2: Fetch Start Page

## Purpose

Download the starting documentation page and parse it with BeautifulSoup so we can inspect the sidebar navigation tree in Step 3.

## Code

```python
print("Fetching start page...")

response = requests.get(START_URL, headers=HEADERS)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
print(f"Start page fetched successfully ({len(response.text)} bytes).")
```

## Explanation

### HTTP Request

```python
response = requests.get(START_URL, headers=HEADERS)
```

- Uses the configured `START_URL` and `HEADERS`.
- The `headers` argument is critical — without a browser User-Agent, some sites return a 403 Forbidden or an empty page.

### Error Handling

```python
response.raise_for_status()
```

Raises an exception if the HTTP status code indicates an error (4xx or 5xx). This fails early rather than proceeding with invalid data. Common issues:

- **403 Forbidden**: The site blocks automated requests. Try adding more headers or a different User-Agent.
- **404 Not Found**: The `START_URL` is incorrect or the documentation structure changed.
- **429 Too Many Requests**: You're being rate-limited. Increase `DELAY_RANGE`.

### Parsing

```python
soup = BeautifulSoup(response.text, "html.parser")
```

Parses the HTML response into a BeautifulSoup object. `html.parser` is Python's built-in parser — no additional installation needed. For problematic HTML, `lxml` is more forgiving but requires installation.

The `soup` variable is used by Step 3 to navigate the sidebar and extract links.

### Print Statement

```python
print(f"Start page fetched successfully ({len(response.text)} bytes).")
```

Confirms the page was downloaded and shows its size. A very small response (e.g., a few KB) might indicate an error page or a JavaScript-based redirect rather than actual documentation content.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Empty or very small response | Client-side rendering (React/Next.js) | Check if the content is loaded via JS. The sidebar might not be in the initial HTML. Look for `<script>` tags with embedded data or try fetching a versioned/static URL. |
| 403 Forbidden | Bot detection | Update `HEADERS` with a more complete browser fingerprint (add `Accept`, `Accept-Language`, `Referer`). |
| Slow response | Rate limiting | Increase `DELAY_RANGE` values. |
| "Sidebar not found" in Step 3 | Wrong selector or JS-rendered sidebar | Re-inspect the site. Check if the sidebar is inside an `<iframe>`, loaded via AJAX, or rendered by JavaScript. |
