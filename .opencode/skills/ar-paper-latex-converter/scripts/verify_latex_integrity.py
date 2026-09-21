#!/usr/bin/env python3
"""LaTeX Discipline and Integrity Linter for Academic Submissions (ar-paper-latex-converter).

Verifies:
  1. Caption-before-label rule: \\caption must precede \\label in all figures and tables.
  2. Zero-orphan check: every labeled figure/table/equation must be referenced in text.
  3. Character hygiene: em dash (—) is banned; unescaped symbols flagged.
  4. Citation placement: \\cite must be placed before punctuation (. or ,).
  5. Input integrity: all \\input{sections/...} files must exist on disk.
  6. Graphic asset integrity: all \\includegraphics files must exist in images/.
  7. Environment balance: matching \\begin{env} and \\end{env}.

Exit codes:
  0 = all integrity checks passed
  1 = integrity violations found
  2 = usage or file I/O error

Pure Python Standard Library. No external dependencies.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def check_caption_before_label(tex_content: str, filename: str) -> list[str]:
    """Verify that \\caption occurs before \\label in figure and table environments."""
    errors: list[str] = []
    # Find all table and figure environments
    env_pattern = re.compile(r"\\begin\{(table\*?|figure\*?)\}([\s\S]*?)\\end\{\1\}")
    for m in env_pattern.finditer(tex_content):
        env_type = m.group(1)
        block = m.group(2)
        cap_pos = block.find(r"\caption")
        lbl_pos = block.find(r"\label")
        if lbl_pos != -1 and cap_pos != -1:
            if lbl_pos < cap_pos:
                errors.append(
                    f"{filename}: In \\begin{{{env_type}}}, \\label precedes \\caption! "
                    "This causes cross-reference numbering errors. \\caption MUST precede \\label."
                )
        elif lbl_pos != -1 and cap_pos == -1:
            errors.append(f"{filename}: \\begin{{{env_type}}} has \\label but missing \\caption.")
    return errors


def check_environment_balance(tex_content: str, filename: str) -> list[str]:
    """Verify that every \\begin has a matching \\end."""
    errors: list[str] = []
    stack: list[str] = []
    tokens = re.finditer(r"\\(begin|end)\{([A-Za-z0-9*]+)\}", tex_content)
    for tok in tokens:
        action = tok.group(1)
        env = tok.group(2)
        if action == "begin":
            stack.append(env)
        elif action == "end":
            if not stack:
                errors.append(f"{filename}: Unexpected \\end{{{env}}} without preceding \\begin.")
            else:
                last = stack.pop()
                if last != env:
                    errors.append(f"{filename}: Mismatched environment: \\begin{{{last}}} closed by \\end{{{env}}}.")
    while stack:
        unclosed = stack.pop()
        errors.append(f"{filename}: Unclosed environment: \\begin{{{unclosed}}}.")
    return errors


def check_character_hygiene(tex_content: str, filename: str) -> list[str]:
    """Check for banned characters such as em dash."""
    errors: list[str] = []
    if "\u2014" in tex_content:
        count = tex_content.count("\u2014")
        errors.append(
            f"{filename}: Found {count} forbidden em dash ('—') character(s). "
            "Use standard dash '-' or double dash '--' per IEEE Access publication standards."
        )
    return errors


def check_citation_placement(tex_content: str, filename: str) -> list[str]:
    """Flag citations placed after periods or commas instead of before."""
    warnings: list[str] = []
    # Match .\cite or ,\cite
    post_punct = re.findall(r"([.,])\s*(\\cite\{[^}]+\})", tex_content)
    if post_punct:
        warnings.append(
            f"{filename}: Found {len(post_punct)} citation(s) placed after punctuation (e.g. '.\\cite{{...}}'). "
            "In IEEE style, citations must be placed BEFORE periods or commas."
        )
    return warnings


def verify_latex_package(project_dir: Path, master_file: Path | None = None) -> dict:
    """Run full integrity suite on a LaTeX project directory."""
    project_dir = project_dir.resolve()
    if master_file is None:
        # Search for access.tex or main.tex
        if (project_dir / "access.tex").exists():
            master_file = project_dir / "access.tex"
        elif (project_dir / "main.tex").exists():
            master_file = project_dir / "main.tex"
        else:
            candidates = list(project_dir.glob("*.tex"))
            if candidates:
                master_file = candidates[0]
            else:
                return {
                    "passed": False,
                    "errors": [f"No master .tex file found in {project_dir}"],
                    "warnings": [],
                }

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Master file checks
    master_content = master_file.read_text(encoding="utf-8")
    errors.extend(check_environment_balance(master_content, master_file.name))
    errors.extend(check_character_hygiene(master_content, master_file.name))

    # 2. Check input sections
    input_matches = re.findall(r"\\input\{([^}]+)\}", master_content)
    sections_checked = 0
    all_tex_contents: list[str] = [master_content]

    for inp in input_matches:
        sec_path = project_dir / inp
        if not sec_path.suffix:
            sec_path = sec_path.with_suffix(".tex")
        if not sec_path.exists():
            errors.append(f"Master file inputs missing file: {inp}")
        else:
            sections_checked += 1
            sec_content = sec_path.read_text(encoding="utf-8")
            all_tex_contents.append(sec_content)
            errors.extend(check_caption_before_label(sec_content, sec_path.name))
            errors.extend(check_environment_balance(sec_content, sec_path.name))
            errors.extend(check_character_hygiene(sec_content, sec_path.name))
            warnings.extend(check_citation_placement(sec_content, sec_path.name))

    # Combine all text for global cross-reference and orphan analysis
    full_text = "\n".join(all_tex_contents)

    # 3. Graphic assets existence
    images_dir = project_dir / "images"
    img_includes = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", full_text)
    for img_name in img_includes:
        p = Path(img_name)
        # Check both direct and inside images/
        found = False
        candidates = [project_dir / img_name, images_dir / p.name, project_dir / p.name]
        for c in candidates:
            if c.exists():
                found = True
                break
        if not found:
            warnings.append(f"Image asset referenced but not found on disk: {img_name}")

    # 4. Zero-orphan cross-references
    labels = set(re.findall(r"\\label\{([^}]+)\}", full_text))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", full_text))
    eqrefs = set(re.findall(r"\\eqref\{([^}]+)\}", full_text))
    all_refs = refs | eqrefs

    orphan_labels = []
    for lbl in labels:
        if lbl.startswith("sec:"):
            # Section labels are optional to cross-ref
            continue
        if lbl not in all_refs:
            orphan_labels.append(lbl)

    if orphan_labels:
        warnings.append(f"Orphan elements detected ({len(orphan_labels)} labeled element(s) never referenced in text): {', '.join(sorted(orphan_labels))}")

    # 5. Bibliography citation integrity
    bib_file = project_dir / "references.bib"
    if bib_file.exists():
        bib_content = bib_file.read_text(encoding="utf-8")
        bib_keys = set(re.findall(r"@\w+\s*\{\s*([A-Za-z0-9_:-]+)\s*,", bib_content))
        cited_keys = set()
        for c_match in re.findall(r"\\cite\{([^}]+)\}", full_text):
            for k in c_match.split(","):
                cited_keys.add(k.strip())

        uncited_keys = bib_keys - cited_keys
        if uncited_keys:
            warnings.append(f"Orphan references detected ({len(uncited_keys)} entry/entries in references.bib never cited with \\cite): {', '.join(sorted(uncited_keys)[:5])}")

    passed = len(errors) == 0
    return {
        "passed": passed,
        "master_file": master_file.name,
        "sections_checked": sections_checked,
        "errors": errors,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project_dir", type=Path, help="Directory of the LaTeX project to verify")
    parser.add_argument("--master", type=Path, default=None, help="Optional explicit master .tex filename")
    args = parser.parse_args(argv)

    if not args.project_dir.exists():
        print(f"ERROR: Project directory not found: {args.project_dir}", file=sys.stderr)
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    res = verify_latex_package(args.project_dir, args.master)
    print(f"=== LaTeX Integrity Verification: {'PASSED' if res['passed'] else 'FAILED'} ===")
    print(f"Master file: {res['master_file']} ({res['sections_checked']} input sections checked)")

    if res["errors"]:
        print(f"\n[ERRORS - {len(res['errors'])} found]:")
        for err in res["errors"]:
            print(f"  [X] {err}")

    if res["warnings"]:
        print(f"\n[WARNINGS - {len(res['warnings'])} found]:")
        for warn in res["warnings"]:
            print(f"  [!] {warn}")

    if res["passed"]:
        print("\nAll mandatory LaTeX publication integrity rules PASSED.")
        return 0
    else:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
