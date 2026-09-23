#!/usr/bin/env python3
"""Main CLI Reference Compiler for academic manuscripts (Step 3).

Parses paper/references.txt and raw bibliography files (.bib, .ris, .nbib)
in paper/references/ to generate paper/06_references.md with HTML anchor tags.

Usage:
    python reference_compiler.py paper/references.txt -o paper/06_references.md --style ieee
    python reference_compiler.py -s apa7 --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Ensure sibling imports work across both local and package invocation
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


try:
    from _bib_parser import parse_reference_file
    from _citation_formatter import format_reference_entry
except ImportError:
    from scripts._bib_parser import parse_reference_file
    from scripts._citation_formatter import format_reference_entry

_DEFAULT_HEADINGS = {
    "ieee": "# VI. REFERENCES",
    "acm": "# REFERENCES",
    "apa7": "# References",
    "apa": "# References",
    "harvard": "# References",
    "vancouver": "# References",
}


def extract_unique_references_from_mapping(mapping_path: Path) -> list[str]:
    """Read references.txt and extract unique reference file paths in order of first appearance."""
    if not mapping_path.exists():
        raise FileNotFoundError(f"References mapping file not found: {mapping_path}")

    content = mapping_path.read_text(encoding="utf-8", errors="replace")
    unique_refs: list[str] = []
    seen = set()

    # Match patterns like:
    #   - paper/references/2021_...bib
    #   - references/2021_...ris
    ref_pattern = re.compile(r"^\s*-\s*([^\r\n]+\.(?:bib|ris|nbib|medline|bibtex))\s*$", re.MULTILINE | re.IGNORECASE)

    for m in ref_pattern.finditer(content):
        raw_path = m.group(1).strip()
        # Normalize slashes
        norm_path = raw_path.replace("\\", "/")
        norm_key = Path(norm_path).name.replace("–", "-").replace("—", "-").lower()
        if norm_key not in seen:
            seen.add(norm_key)
            unique_refs.append(norm_path)

    return unique_refs


def resolve_file_path(ref_path_str: str, base_dir: Path, ref_dir_override: Path | None = None) -> Path:
    """Resolve physical file path handling relative bases and en-dashes/hyphens."""
    p = Path(ref_path_str)

    # 1. Direct check
    if p.exists():
        return p

    # 2. Check relative to base_dir
    candidate = base_dir / p
    if candidate.exists():
        return candidate

    # 3. Check within ref_dir_override or paper/references
    filename = p.name
    if ref_dir_override and ref_dir_override.exists():
        cand = ref_dir_override / filename
        if cand.exists():
            return cand

    cand_default = base_dir / "paper" / "references" / filename
    if cand_default.exists():
        return cand_default

    cand_local = base_dir / "references" / filename
    if cand_local.exists():
        return cand_local

    # 4. Fuzzy dash matching (en-dash vs hyphen) and case-insensitive filename search
    target_clean = filename.replace("–", "-").replace("—", "-").lower()
    search_dirs = [ref_dir_override, base_dir / "paper" / "references", base_dir / "references"]
    for d in search_dirs:
        if d and d.exists():
            for f in d.iterdir():
                if f.is_file() and f.name.replace("–", "-").replace("—", "-").lower() == target_clean:
                    return f

    return candidate


def compile_references(
    mapping_file: str | Path,
    output_file: str | Path,
    style: str = "ieee",
    ref_dir: str | Path | None = None,
    custom_heading: str | None = None,
    dry_run: bool = False,
    as_json: bool = False,
) -> dict[str, Any]:
    """Execute full compilation workflow and return summary report."""
    map_p = Path(mapping_file).resolve()
    base_dir = map_p.parent
    if base_dir.name == "paper":
        project_root = base_dir.parent
    else:
        project_root = base_dir

    ref_dir_p = Path(ref_dir).resolve() if ref_dir else None
    out_p = Path(output_file).resolve()

    raw_ref_paths = extract_unique_references_from_mapping(map_p)
    parsed_entries = []
    missing_files = []

    for idx, raw_path in enumerate(raw_ref_paths, start=1):
        resolved_p = resolve_file_path(raw_path, project_root, ref_dir_p)
        if not resolved_p.exists():
            missing_files.append({"index": idx, "path": raw_path, "resolved": str(resolved_p)})
            continue

        try:
            entry = parse_reference_file(resolved_p)
            entry["original_ref_path"] = raw_path
            entry["original_order"] = idx
            parsed_entries.append(entry)
        except Exception as err:
            missing_files.append({"index": idx, "path": raw_path, "error": str(err)})

    # Sort if required by citation style
    style_clean = style.lower().replace("-", "").replace(" ", "")
    if style_clean in ("apa7", "apa", "harvard", "chicago"):
        # Sort alphabetically by first author's surname, then year
        def sort_key(e: dict[str, Any]):
            authors = e.get("authors", [])
            first_surname = authors[0].get("last", "").lower() if authors else ""
            year = e.get("year") or 9999
            title = e.get("title", "").lower()
            return (first_surname, year, title)

        parsed_entries.sort(key=sort_key)

    if as_json:
        return {
            "total_mapped": len(raw_ref_paths),
            "successfully_parsed": len(parsed_entries),
            "missing_files": missing_files,
            "style": style,
            "entries": parsed_entries,
        }

    # Format entries
    formatted_lines = []
    for i, entry in enumerate(parsed_entries, start=1):
        entry_str = format_reference_entry(entry, i, style_clean)
        formatted_lines.append(entry_str)

    heading = custom_heading or _DEFAULT_HEADINGS.get(style_clean, "# REFERENCES")
    markdown_content = f"{heading}\n\n" + "\n\n".join(formatted_lines) + "\n"

    if not dry_run:
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(markdown_content, encoding="utf-8")

    return {
        "total_mapped": len(raw_ref_paths),
        "successfully_compiled": len(parsed_entries),
        "missing_files": missing_files,
        "output_file": str(out_p),
        "dry_run": dry_run,
        "markdown_content": markdown_content if dry_run else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compile paper/references.txt and .bib/.ris files into paper/06_references.md."
    )
    parser.add_argument(
        "positional_mapping",
        nargs="?",
        default=None,
        metavar="mapping_file",
        help="Path to references.txt mapping file (positional fallback, default: paper/references.txt)",
    )
    parser.add_argument(
        "-m",
        "--mapping",
        dest="mapping",
        default=None,
        help="Path to references.txt mapping file (default: paper/references.txt)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="paper/06_references.md",
        help="Path to output markdown file (default: paper/06_references.md)",
    )
    parser.add_argument(
        "-s",
        "--style",
        default="ieee",
        choices=["ieee", "apa7", "harvard", "acm", "vancouver"],
        help="Citation style for bibliography compilation (default: ieee)",
    )
    parser.add_argument(
        "-d",
        "--ref-dir",
        help="Override directory where raw .bib/.ris files are stored (default: auto-detected)",
    )
    parser.add_argument(
        "--heading",
        help="Custom markdown heading for the references section (e.g. '# VI. REFERENCES')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate compilation and print output to stdout without writing to disk",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output parsed canonical reference objects in JSON format",
    )

    args = parser.parse_args()

    mapping_file = args.mapping or args.positional_mapping or "paper/references.txt"
    mapping_p = Path(mapping_file)
    if not mapping_p.exists():
        print(f"Error: Mapping file '{mapping_file}' not found.", file=sys.stderr)
        return 2

    res = compile_references(
        mapping_file=mapping_file,
        output_file=args.output,
        style=args.style,
        ref_dir=args.ref_dir,
        custom_heading=args.heading,
        dry_run=args.dry_run,
        as_json=args.json,
    )

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    if args.dry_run:
        print(res.get("markdown_content", ""))
        return 0

    print(f"[OK] References compiled successfully!")
    print(f"     Target Style: {args.style.upper()}")
    print(f"     Total Mapped: {res['total_mapped']}")
    print(f"     Compiled:     {res['successfully_compiled']}")
    print(f"     Output:       {res['output_file']}")

    if res["missing_files"]:
        print(f"\n[WARNING] {len(res['missing_files'])} reference files could not be found or parsed:")
        for m in res["missing_files"]:
            print(f"  - [{m.get('index')}] {m.get('path')} ({m.get('error', 'File not found')})")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
