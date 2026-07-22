# Step 6: Generate references.md Index

## Purpose

Read the link metadata from `references.json` and generate a basic `references.md` index file with numbered entries and links to each reference file. This auto-generated version is a starting point — the AI refines it later with section groupings and paragraph descriptions.

## Code

```python
REFERENCES_INDEX = os.path.join(BASE_DIR, "references.md")

with open(REFERENCES_JSON, "r", encoding="utf-8") as f:
    entries = json.load(f)

print(f"Generating references.md index with {len(entries)} entries...")

lines = []
lines.append("# Filament v5 Documentation Reference")
lines.append("")
lines.append(f"Crawled from [{BASE_URL}]({START_URL})")
lines.append("")
lines.append("## Contents")
lines.append("")

for entry in entries:
    link_target = f"references/{entry['idx']:03d}_{entry['slug']}.md"
    lines.append(f"- **{entry['idx']:03d}** - [{entry['title']}]({link_target})")

lines.append("")
lines.append("---")
lines.append("")
lines.append("> **Note:** This file was auto-generated. An AI should refine it with descriptions, section groupings, and context.")

content = "\n".join(lines)

with open(REFERENCES_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

print(f"references.md generated at: {REFERENCES_INDEX}")
```

## Step-by-Step Explanation

### 1. Define Output Path

```python
REFERENCES_INDEX = os.path.join(BASE_DIR, "references.md")
```

The index file lives at the root of the topic directory, alongside `html/` and `references/`:

```text
docs/filament_v5/
├── references.json    ← metadata
├── references.md      ← THIS FILE (index)
├── references/        ← individual .md files
└── html/              ← raw HTML files
```

### 2. Read Metadata

```python
with open(REFERENCES_JSON, "r", encoding="utf-8") as f:
    entries = json.load(f)
```

Same pattern as Steps 4 and 5. Each cell reads `references.json` independently.

### 3. Build Index Content

```python
lines = []
lines.append("# Filament v5 Documentation Reference")
lines.append("")
lines.append(f"Crawled from [{BASE_URL}]({START_URL})")
lines.append("")
lines.append("## Contents")
lines.append("")

for entry in entries:
    link_target = f"references/{entry['idx']:03d}_{entry['slug']}.md"
    lines.append(f"- **{entry['idx']:03d}** - [{entry['title']}]({link_target})")
```

The structure is simple:

1. **H1 heading**: The documentation title.
2. **Source link**: Link back to the original documentation site.
3. **Contents heading**: H2 section header.
4. **Bullet list**: Each entry is a bullet with the index number in bold, followed by a link using the original sidebar title.

**Why use `entry['title']` (original sidebar text) instead of reconstructing from the slug?**

The slug is a sanitized version (lowercase, hyphens). The title preserves the original formatting including capitalization, punctuation, and special characters. For example:

| Slug | Title |
|------|-------|
| `what-is-filament` | `What is Filament?` |
| `ai-assisted-development` | `AI-assisted development` |
| `modular-architecture-(ddd)` | `Modular architecture (DDD)` |

### 4. Save

```python
content = "\n".join(lines)

with open(REFERENCES_INDEX, "w", encoding="utf-8") as f:
    f.write(content)
```

Joins all lines with newline characters and writes to the output file.

## Sample Output

```markdown
# Filament v5 Documentation Reference

Crawled from [https://filamentphp.com](https://filamentphp.com/docs/5.x/introduction/overview)

## Contents

- **001** - [What is Filament?](references/001_what-is-filament.md)
- **002** - [Installation](references/002_installation.md)
- **003** - [AI-assisted development](references/003_ai-assisted-development.md)
...

---

> **Note:** This file was auto-generated. An AI should refine it with descriptions, section groupings, and context.
```

## After This Step (AI Task)

The notebook generates a minimal index. The AI must then:

1. **Read every `.md` file** in `references/` to extract the H1 title and first meaningful paragraph.
2. **Rewrite `references.md`** with:
   - Section groupings matching the documentation sidebar structure
   - At least one short paragraph per entry (accurate, not hallucinated)
   - Proper formatting and descriptions

This manual step ensures the descriptions are accurate and meaningful, not just auto-generated noise.
