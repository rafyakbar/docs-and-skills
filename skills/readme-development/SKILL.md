---
name: readme-development
description: "Activate when the user asks to create, write, generate, or update a README.md file for any project. This includes creating a README from scratch, improving an existing README, or generating a README based on the project's codebase. Covers project exploration, README type classification, structure templates, writing rules, and update workflows. Trigger words: buat readme, create readme, generate readme, write readme, update readme, buat README.md. Do NOT activate for editing CHANGELOG, CONTRIBUTING, AGENTS.md, inline code comments, or API documentation."
license: MIT
metadata:
  author: project
---

# README Development

A guide for README.md creation that is effective for any software project. This skill is global and can be used in any project.

## Overview

The core principle: **understand the project first, then write the README**. Act as a senior expert software engineer with extensive open source experience. Make READMEs appealing, informative, and easy to read.

A good README is a landing page. It should answer "Is this for me?" in seconds and guide users from discovery to usage.

## When to Activate

- User asks to create a new README.md
- User asks to improve or update an existing README.md
- User mentions "create readme", "generate readme", "write readme", "buat readme"
- User says "there is no README" or "the README needs work"

## Scope

- **In scope:** Creating README.md from codebase analysis, improving existing READMEs, determining structure and content based on project type
- **Out of scope:** Creating CHANGELOG, CONTRIBUTING, LICENSE, API documentation, inline code comments

## Phase 1: Understand the Project (Mandatory)

Before writing a single line, thoroughly explore the project. Never create a README based on assumptions.

### 1.1 Scan Directory Structure

Read the root directory to understand scale and organization. Identify if it's a monorepo, main folders, and tool config files (`.eslintrc`, `tsconfig`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.).

### 1.2 Read Key Configuration Files

| File | Information |
|------|-------------|
| `package.json` | Name, description, version, scripts (Node.js) |
| `Cargo.toml` / `pyproject.toml` / `go.mod` / `composer.json` | Name, description, dependencies |
| `pom.xml` / `build.gradle` | Group, artifact, deps (Java/Kotlin) |
| `*.sln` / `*.csproj` | Project name, target framework (C#/.NET) |
| `Makefile` | Build targets, commands |
| `Dockerfile` / `docker-compose.yml` | Container setup |
| `.env.example` | Required environment variables |
| `LICENSE` | License type |

### 1.3 Read Existing Documentation

If a README.md exists, read it first. Also check `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/`, `AGENTS.md` / `CLAUDE.md`, `.github/`.

### 1.4 Identify Tech Stack + Purpose

Determine primary language, frameworks, database, build tools, target platform. Understand the problem it solves and who it's for. Scan source code for entry points, routes, main components, and CLI commands.

## Phase 2: Determine README Type

Classify the project into one of four types and use the corresponding template. See `references/templates.md` for full templates.

| Type | Examples | Focus |
|------|----------|-------|
| **A: Application** | Web apps, SaaS, Dashboards | Screenshots, Features, Quick Setup, Deployment |
| **B: Library/Package** | npm/Composer/PyPI packages | Installation, Usage, API, Examples |
| **C: Tool/CLI** | CLI generators, automation | Commands, Examples, Configuration |
| **D: Knowledge Repository** | AI Skills, Prompts, Datasets | Structure, Workflow, Activation Rules |

## Phase 3: Write the README

### Formatting Rules

- Use GFM (GitHub Flavored Markdown) for formatting
- Use GitHub admonition syntax for callouts:

```markdown
> [!NOTE]
> Useful information

> [!TIP]
> Helpful advice

> [!IMPORTANT]
> Critical information

> [!WARNING]
> Caution

> [!CAUTION]
> Dangerous action
```

### Content Rules

1. **Hero section** (Types C/D): Start with title + one-line description + optional compatibility badges. Do not overuse emojis.

2. **Title and description**: Title = project name. Description = `> One or two sentences` answering "What is it? Who is it for? Why does it matter?"

3. **Is This Project For You?**: Place early (after description, before Features). Use ✅ and ❌. Keep to 3-5 items per column.

4. **Features**: Bullet points, bold feature name + brief description. Max 6-8 key features.

5. **Tech Stack**: Group by category (Backend, Frontend, DevOps). Only what's actually used.

6. **Prerequisites**: Only truly needed items, with minimum versions and official download links.

7. **Installation**: Numbered steps, code blocks with language tags, each step copy-pasteable.

8. **Usage**: Include how to run + concrete examples with expected output.

9. **Testing**: Use commands from scripts (package.json, Makefile). Do not make up commands.

10. **Directory structure**: For complex projects, show tree with brief descriptions. Max depth 2-3.

11. **Works Best With** (AI projects only): Model compatibility table. Do not fabricate rankings.

12. **Badges**: Only relevant and functional. Do not add broken or invalid ones.

13. **Do NOT include**: LICENSE, CONTRIBUTING, CHANGELOG sections (they have dedicated files).

14. **No fabrication**: Do not make up commands, badge URLs, dependencies, features, or model rankings.

15. **README language**: Match project language. If user specifies, follow their request.

16. **Take inspiration** from quality READMEs when appropriate, but always match the actual project.

## Phase 4: Update Existing README

Do not rewrite from scratch. Follow this process:

1. **Audit**: Compare existing README against the template. Note missing, outdated, or incorrect sections.
2. **Plan**: Determine what to Keep, Update, Add, Remove.
3. **Apply**: Preserve existing structure, only modify what needs improvement.
4. **Summarize**: Provide a clear change summary at the end of your response (not in the README).

**Example summary:**

```
- **Added** "Is This Project For You?" section
- **Updated** "Installation" section with correct commands
- **Removed** outdated "Deployment" section
```

## Do and Don't

| Do | Don't |
|----|-------|
| Understand the project BEFORE writing | Write README without exploration |
| Classify into correct type (A/B/C/D) | Use same template for every project |
| Read config files to verify facts | Fabricate names, versions, dependencies |
| Use commands actually in scripts | Make up commands that don't exist |
| Include concrete, working examples | Write only abstract descriptions |
| Use GFM + GitHub admonitions | Use unsupported markup |
| Determine language from project | Assume language without checking |
| Select relevant sections only | Include every section without filtering |
| Verify commands are runnable | Assume commands are correct |
| Use code blocks with language tags | Code blocks without language tags |
| Place "Is This Project For You?" early | Bury relevance at the bottom |
| For updates: provide change summary | Silently modify without explaining |

## References

- `references/templates.md` — Full README templates for all 4 types
- `references/sample-readme.md` — Sample README (Type D)
- `references/writing-rules.md` — Detailed rules (Rules 1-16 with full examples)
