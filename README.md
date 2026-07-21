# Docs & Skills

> AI-ready documentation crawler and multi-agent skill repository for Laravel/PHP frameworks.

Docs & Skills combines two things: a **documentation crawler** that converts official docs into clean Markdown for AI consumption, and a **multi-agent skill hub** that maintains synchronized AI agent instructions across OpenCode, Claude Code, and .agents environments.

## Is This Project For You?

✅ AI coding assistants that need local documentation context

✅ Developers using OpenCode, Claude Code, or .agents

✅ Teams maintaining skills across multiple AI agents

❌ Projects without AI coding assistant tooling

## What This Project Can Do

- Crawl official documentation websites and convert HTML to structured Markdown
- Maintain version-locked, AI-ready documentation datasets (Livewire v4, FluxUI v2, Filament v5, Alpine.js v3)
- Synchronize AI agent skills across 4 directories with hash verification
- Provide reusable skill templates for README, migration, and notebook development

## Directory Structure

```
docs-and-skills/
├── skills/                     # Source of truth for AI agent skills
│   ├── jupyter-notebook-development/
│   ├── laravel-migration-development/
│   ├── readme-development/
│   ├── skill-development/
│   └── skill-sync/
├── .agents/skills/             # Mirror for .agents
├── .opencode/skills/           # Mirror for OpenCode
├── .claude/skills/             # Mirror for Claude Code
├── docs/                       # Crawled documentation datasets
│   └── <topic>_v<version>/     # e.g., livewire-4x, fluxui-v2
│       ├── references.md       # Index/overview file
│       └── references/         # Detailed reference files
│           ├── 001_<subject>.md
│           ├── 002_<subject>.md
│           └── ...
├── *.ipynb                     # Jupyter crawler notebooks
├── PROMPTEN.md                 # English crawling prompt template
└── PROMPTID.md                 # Indonesian crawling prompt template
```

## Documentation Pipeline

Each Jupyter notebook follows a 4-step crawl-and-convert pipeline:

> [!NOTE]
> HTML files are gitignored. Only the final Markdown output is committed.

| Step | Description |
|------|-------------|
| **1. Fetch** | Download the start page |
| **2. Extract** | Collect all sidebar links |
| **3. Crawl** | Download each page as numbered HTML (`0001_Name.html`) |
| **4. Convert** | Strip images, convert to Markdown, save as numbered reference files |

### Supported Frameworks

| Framework | Version | Status |
|-----------|---------|--------|
| Livewire | 4.x | ✅ Complete |
| FluxUI | 2.x | ✅ Complete |
| Filament | 5.x | ✅ Complete |
| Alpine.js | 3.x | ✅ Complete |

## Skill Architecture

Skills are synchronized across 4 directories to ensure consistent behavior:

```
skills/               ← Source of truth (edit here)
.agents/skills/       ← Mirror
.opencode/skills/     ← Mirror
.claude/skills/       ← Mirror
```

> [!TIP]
> Use `skill-sync` to crosscheck and sync all skills. Use `skill-development` to create new skills.

## Use Cases

### AI Knowledge Base

Point your AI assistant to `docs/<topic>_v<version>/references.md` for local, version-locked documentation.

### RAG Pipeline

Split Markdown files per heading, generate embeddings, and store in a vector database for retrieval-augmented generation.

### Multi-Agent Skill Management

Define skills once in `skills/`, sync to all agent folders, and ensure consistent behavior across OpenCode, Claude Code, and .agents.
