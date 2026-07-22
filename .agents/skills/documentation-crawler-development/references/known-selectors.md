# Known Site Selectors

These selectors were discovered through manual site inspection of each documentation site.

## Reference Table

| Website | Sidebar Selector | Content Selector |
|---------|-----------------|-----------------|
| Livewire v4 | `ul.list-none.space-y-5.divide-y.divide-slate-700.px-3` | `div.pt-12.docsearch-content.overflow-hidden.flex-1.mx-auto.max-w-prose.w-full` |
| Alpine.js v3 | `aside` | `div.m-auto.max-w-3xl.px-6.pb-24.text-gray-800.antialiased.markdown` |
| Filament v5 | `div#navigation-items` | `div#content-area` |
| FluxUI v2 | `ui-sidebar` | `div[data-flux-main]` |

## How to Discover Selectors for a New Site

Always inspect the site manually before writing the notebook:

1. **Open the documentation URL** in a browser
2. **Right-click the sidebar** → Inspect Element
3. **Find a unique identifier** — look for `id`, unique `class`, or custom HTML tags like `<ui-sidebar>`
4. **Right-click the main content** → Inspect Element
5. **Find a unique content identifier** — look for `id="content-area"`, `main`, `article`, or unique classes
6. **Test with Python**: Use `requests` + `BeautifulSoup` to verify the selectors work on the raw HTML

## Common Selector Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| ID | `div#navigation-items`, `nav#sidebar` | Most reliable — IDs are unique |
| Tag | `aside`, `nav`, `main` | Good when the site uses semantic HTML |
| Class | `div.sidebar-content`, `ul.menu` | Works but may need multiple classes |
| Attribute | `div[data-flux-main]`, `div[role="navigation"]` | Useful for custom framework elements |
| Custom tag | `ui-sidebar`, `doc-content` | Framework-specific (e.g., web components) |

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Selector not found | Site uses different HTML structure | Re-inspect the site structure |
| Multiple matches | Selector is too broad | Use a more specific selector (add parent context) |
| Empty content | Content is loaded via JavaScript | Check if the page is client-side rendered; try a different URL |
| Sidebar not found in raw HTML | Page is a client-side rendered SPA | Check the raw response from `requests.get()` — if sidebar is missing, try finding a static version or use the page's embedded data |
