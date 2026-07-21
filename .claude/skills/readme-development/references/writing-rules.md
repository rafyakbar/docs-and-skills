# README Writing Rules (Detailed)

## Rule 1: Hero Section

For Types C and D, start with a hero section:

```
# 📚 Project Name

> One-line value proposition.

⚡ OpenCode Ready  ⚡ Claude Code Ready
```

- Communicates instantly what the project is
- Use emojis sparingly and meaningfully
- Keep to 3-5 lines maximum

## Rule 2: Is This Project For You?

Place early so users decide quickly:

```markdown
## Is This Project For You?

✅ AI Agents
✅ Developers building AI workflows

❌ Beginners learning programming
```

- Use ✅ and ❌
- Be honest about what it's NOT for
- Keep to 3-5 items per column

## Rule 3: Works Best With (AI projects)

```markdown
## Works Best With

| Model | Recommended |
|-------|-------------|
| Claude Opus 4.8 | ⭐⭐⭐⭐⭐ |
| GPT-5.5 | ⭐⭐⭐⭐⭐ |
```

## Rule 4: Title and Description

```
# Project Name

> One or two sentences describing what this project is and what problem it solves.
```

## Rule 5: Badges

```
![Build](https://img.shields.io/github/actions/workflow/status/USER/REPO/ci.yml)
```

## Rule 6: Features

```
- **Feature 1** — Brief description
- **Feature 2** — Brief description
```

## Rule 7: Tech Stack

```
- **Backend**: Node.js, Express, PostgreSQL
- **Frontend**: React, TypeScript, Tailwind CSS
```

## Rule 8: Prerequisites

```
- [Node.js](https://nodejs.org/) v18 or later
- [PostgreSQL](https://www.postgresql.org/) v15 or later
```

## Rule 9: Installation

Numbered steps with copy-pasteable code blocks. Use proper language tags.

## Rule 10: Usage

Always include how to run + concrete examples with expected output.

## Rule 11: Testing

Use commands from package.json or Makefile. Do not make up commands.

## Rule 12: Directory Structure

For complex projects, show tree with descriptions. Max depth 2-3.

## Rule 13: Do Not Include LICENSE/CONTRIBUTING/CHANGELOG

These sections have dedicated files. Do not duplicate them in README.

## Rule 14: No Fabrication

Do not make up commands, badge URLs, dependencies, features, or model rankings.

## Rule 15: README Language

Match the project language. If user specifies, follow their request.

## Rule 16: Take Inspiration

From quality READMEs when appropriate, but always match the actual project.
