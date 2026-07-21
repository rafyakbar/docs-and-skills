---
name: skill-sync
description: "Activate when the user asks to check, verify, sync, or audit skills across agent folders. This includes crosschecking which skills exist in each agent directory, identifying missing or extra skills, ensuring all folders have identical copies, and fixing discrepancies. Trigger words: sync skills, check skills, crosscheck, verify skills, missing skill, skill audit, skill consistency. Do NOT activate when creating a new skill (use skill-development instead) or when working on non-skill features."
license: MIT
metadata:
  author: project
---

# Skill Sync & Crosscheck

How to audit, verify, and synchronize skills across agent folders in this project.

## Overview

This project supports multiple AI agents, each with their own skills directory. All shared skills must be present and identical across every agent folder. This skill provides the process for detecting and fixing discrepancies.

## When to Activate

- User asks to check or audit skill consistency across folders
- User asks to sync skills to all agents
- User notices a skill is missing in one agent but present in another
- User asks "are all skills in sync?"
- After creating or updating a skill (as a follow-up verification step)

## Source of Truth

The `skills/` folder is the **single source of truth** for shared skills. All other agent folders should mirror it exactly. A skill can contain more than just `SKILL.md`; it may include subfolders for references, rules, or other supporting files.

```text
skills/                         ← SOURCE OF TRUTH
├── <skill-name>/
│   ├── SKILL.md                  # Required: overview and instructions
│   ├── references/               # Optional: detailed documentation
│   │   ├── api-guide.md
│   │   └── examples.md
│   └── rules/                    # Optional: categorized rule files
│       ├── security.md
│       └── testing.md
└── <another-skill>/
    └── SKILL.md

.agents/skills/                 ← MIRROR (must match source)
.opencode/skills/               ← MIRROR (must match source)
.claude/skills/                 ← MIRROR (must match source)
```

## Agent Folders to Sync

```text
skills/               ← Source of truth
.agents/skills/       ← Mirror
.opencode/skills/     ← Mirror
.claude/skills/       ← Mirror
```

## Crosscheck Process

### Step 1: List All Skills in Every Location

List the contents of:
- `skills/` (source of truth)
- `.agents/skills/`
- `.opencode/skills/`
- `.claude/skills/`

### Step 2: Build a Comparison Matrix

Create a table showing which skills exist where:

| Skill | skills/ | .agents | .opencode | .claude |
|-------|---------|---------|-----------|---------|
| skill-a | ✓ | ✓ | ✓ | ✓ |
| skill-b | ✓ | ✓ | ✓ | ✗ |

### Step 3: Identify Discrepancies

Flag any of these issues:

| Issue | Meaning | Action |
|-------|---------|--------|
| Skill in `skills/` but NOT in mirror | Mirror is out of sync | Copy skill TO the mirror folder |
| Skill in mirror but NOT in `skills/` | Source of truth is incomplete | Copy skill FROM mirror INTO `skills/` |
| Skill differs between folders (hash mismatch) | Stale copy | Overwrite mirror copy with `skills/` version |
| Skill in one mirror but not the other | Partial sync | Copy to missing mirror folder |

### Step 4: Fix Discrepancies

For each issue found:

1. **Missing from source**: Copy from the mirror that has it into `skills/<name>/`
2. **Missing from mirror**: Copy from `skills/<name>/` into the mirror folder
3. **Content mismatch**: The `skills/` version wins. Overwrite mirror copies.
4. **Include subfolders**: If the skill has `references/`, `rules/`, or other subfolders, those must be synced too

### Step 5: Verify Registration

After syncing files, check that ALL skills are registered in instruction files:

- `AGENTS.md`, `## Skills Activation` section
- `CLAUDE.md`, `## Skills Activation` section

### Step 6: Final Verification

Run a hash comparison to confirm all copies are identical:

```powershell
# PowerShell: Compare hashes for a specific skill
$skill = "skill-name"
$sourceHash = (Get-FileHash "skills/$skill/SKILL.md").Hash
$folders = @('skills', '.agents', '.opencode', '.claude')
foreach ($f in $folders) {
    $path = "$f/skills/$skill/SKILL.md"
    if (Test-Path $path) {
        $hash = (Get-FileHash $path).Hash
        $match = if ($hash -eq $sourceHash) { "OK" } else { "MISMATCH" }
        Write-Host "$match  $f"
    } else {
        Write-Host "MISSING  $f"
    }
}
```

## Quick Sync Command

To force-sync ALL skills from `skills/` to all mirror folders:

```powershell
$mirrors = @('.agents', '.opencode', '.claude')
$skills = Get-ChildItem "skills" -Directory
foreach ($skill in $skills) {
    foreach ($mirror in $mirrors) {
        $dest = "$mirror/skills/$($skill.Name)"
        if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
        Copy-Item "$($skill.FullName)/*" $dest -Recurse -Force
    }
    Write-Host "Synced: $($skill.Name)"
}
```

## Do and Don't

| Do | Don't |
|----|-------|
| Always treat `skills/` as source of truth | Let agent folders diverge without fixing |
| Sync ALL subfolders (references/, rules/) too | Only sync SKILL.md and forget subfolders |
| Verify with hash after syncing | Assume copy worked without checking |
| Report the full comparison matrix to user | Silently fix without showing what changed |
| Check instruction files after sync | Only sync files but forget registration |
| Ask user before deleting a skill from any location | Remove skills without confirmation |
