# Web Crawling Code Pattern

Use this pattern for any notebook that downloads files from the web:

```python
# Config cell
MAX_AGE_DAYS = 30
DELAY_RANGE = (0.2, 0.6)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
}

# Download cell
print(f'Mendownload {len(all_items)} item...')
done = 0
failed = 0
errors = []

for item in tqdm(all_items, desc='Download'):
    # compute path inline (don't rely on previous cell)
    fname = f'{item_id}.html'
    html_path = os.path.join(OUTPUT_DIR, fname)

    if os.path.exists(html_path):
        age = time.time() - os.path.getmtime(html_path)
        if age < MAX_AGE_DAYS * 86400:
            done += 1
            continue

    try:
        resp = requests.get(item['url'], headers=HEADERS, timeout=30)
        resp.raise_for_status()
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(resp.text)
        done += 1
        time.sleep(random.uniform(*DELAY_RANGE))
    except Exception as e:
        failed += 1
        errors.append(f'{item}: {e}')

print(f'Selesai: {done} OK, {failed} gagal')
if errors:
    print('\\nError detail:')
    for err in errors:
        print(f'  - {err}')
```
