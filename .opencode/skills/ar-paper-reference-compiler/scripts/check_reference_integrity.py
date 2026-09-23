#!/usr/bin/env python3
"""Triangular reference integrity validator for academic papers.

Audits consistency between:
1. Mapping file (paper/references.txt)
2. Physical bibliography directory (paper/references/)
3. Compiled markdown output (paper/06_references.md)

Usage:
    python check_reference_integrity.py -m paper/references.txt -d paper/references/ -o paper/06_references.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass



def check_integrity(
    mapping_file: str | Path = "paper/references.txt",
    ref_dir: str | Path = "paper/references",
    output_file: str | Path = "paper/06_references.md",
) -> dict[str, Any]:
    """Perform comprehensive triangular audit and return diagnostic report."""
    map_p = Path(mapping_file)
    dir_p = Path(ref_dir)
    out_p = Path(output_file)

    report: dict[str, Any] = {
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "stats": {
            "mapped_unique_files": 0,
            "physical_files_on_disk": 0,
            "compiled_entries_in_output": 0,
        },
    }

    if not map_p.exists():
        report["status"] = "FAIL"
        report["errors"].append(f"Mapping file not found: {map_p}")
        return report

    # 1. Parse mapped references
    content_map = map_p.read_text(encoding="utf-8", errors="replace")
    ref_pattern = re.compile(r"^\s*-\s*([^\r\n]+\.(?:bib|ris|nbib|medline|bibtex))\s*$", re.MULTILINE | re.IGNORECASE)
    mapped_files_raw = [m.group(1).strip().replace("\\", "/") for m in ref_pattern.finditer(content_map)]
    unique_mapped_basenames = []
    seen = set()
    for f in mapped_files_raw:
        base = Path(f).name.replace("–", "-").replace("—", "-").lower()
        if base not in seen:
            seen.add(base)
            unique_mapped_basenames.append(Path(f).name)

    report["stats"]["mapped_unique_files"] = len(unique_mapped_basenames)

    # 2. Check physical files on disk
    physical_basenames = {}
    if dir_p.exists():
        for f in dir_p.iterdir():
            if f.is_file() and f.suffix.lower() in (".bib", ".ris", ".nbib", ".bibtex"):
                key = f.name.replace("–", "-").replace("—", "-").lower()
                physical_basenames[key] = f.name
        report["stats"]["physical_files_on_disk"] = len(physical_basenames)
    else:
        report["warnings"].append(f"References directory does not exist: {dir_p}")

    # Check 1: Missing physical files
    for orig_name in unique_mapped_basenames:
        norm_key = orig_name.replace("–", "-").replace("—", "-").lower()
        if norm_key not in physical_basenames:
            report["errors"].append(f"Missing physical file for mapped reference: '{orig_name}'")

    # Check 2: Orphan physical files (in directory but never referenced)
    mapped_keys = {name.replace("–", "-").replace("—", "-").lower() for name in unique_mapped_basenames}
    for phys_key, orig_phys_name in physical_basenames.items():
        if phys_key not in mapped_keys:
            report["warnings"].append(f"Orphan file in references directory (unreferenced): '{orig_phys_name}'")

    # 3. Check compiled output file
    if out_p.exists():
        out_content = out_p.read_text(encoding="utf-8", errors="replace")
        
        # Universal metric: anchor tags <a id="refN"></a> generated across all citation styles
        anchor_entries = re.findall(r'<a\s+id=["\']ref(\d+)["\']\s*></a>', out_content)
        
        # Fallback regex matching combined entry formats: [N], N., or <a id="refN">
        fallback_entries = re.findall(
            r'(?:(?:^|\n)\s*\[(\d+)\]\s+|(?:^|\n)\s*(\d+)\.\s+|<a\s+id=["\']ref(\d+)["\']\s*>)',
            out_content,
        )
        fallback_ids = [g1 or g2 or g3 for g1, g2, g3 in fallback_entries]

        # Use anchor tags as primary universal metric, with combined fallback regex if anchors missing
        if anchor_entries:
            compiled_count = len(anchor_entries)
        elif fallback_ids:
            compiled_count = len(dict.fromkeys(fallback_ids))
        else:
            compiled_count = 0

        report["stats"]["compiled_entries_in_output"] = compiled_count

        if compiled_count != len(unique_mapped_basenames):
            report["errors"].append(
                f"Count mismatch: {compiled_count} compiled entries vs {len(unique_mapped_basenames)} mapped references"
            )

        # Anchor check: detect numbered entries missing anchors
        numbered_matches = re.findall(r'(?:^|\n)\s*(?:\[(\d+)\]|(\d+)\.)\s+', out_content)
        numbered_entries = [g1 or g2 for g1, g2 in numbered_matches]
        if numbered_entries:
            missing_anchors = set(numbered_entries) - set(anchor_entries)
            if missing_anchors:
                report["warnings"].append(
                    f"Missing HTML anchor tags for entries: {', '.join(sorted(missing_anchors, key=int))}"
                )
        elif not anchor_entries and compiled_count > 0:
            report["warnings"].append("Missing HTML anchor tags (<a id=\"refN\"></a>) in compiled references output.")

        # Sequential anchor check
        if anchor_entries:
            expected_anchors = {str(i) for i in range(1, len(anchor_entries) + 1)}
            missing_seq = expected_anchors - set(anchor_entries)
            if missing_seq:
                report["warnings"].append(
                    f"Non-contiguous or missing anchor IDs in sequence: {', '.join(sorted(missing_seq, key=int))}"
                )

        # DOI syntax check
        invalid_dois = re.findall(r"doi:\s*([^,\s\n]+)", out_content)
        for d in invalid_dois:
            clean_d = d.strip(".[]()")
            if not clean_d.startswith("10.") and not clean_d.startswith("http"):
                report["warnings"].append(f"Suspicious DOI format in output: '{d}'")
    else:
        report["warnings"].append(f"Compiled references output file not found: {out_p}")

    if report["errors"]:
        report["status"] = "FAIL"
    elif report["warnings"]:
        report["status"] = "WARN"

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit triangular reference integrity.")
    parser.add_argument(
        "positional_mapping",
        nargs="?",
        default=None,
        metavar="mapping_file",
        help="Path to references.txt mapping file (positional fallback, default: paper/references.txt)",
    )
    parser.add_argument("-m", "--mapping", default=None, help="Path to references.txt (default: paper/references.txt)")
    parser.add_argument("-d", "--ref-dir", default="paper/references", help="Path to references/ directory")
    parser.add_argument("-o", "--output", default="paper/06_references.md", help="Path to compiled 06_references.md")
    parser.add_argument("--json", action="store_true", help="Output audit report as JSON")

    args = parser.parse_args()
    mapping_file = args.mapping or args.positional_mapping or "paper/references.txt"
    report = check_integrity(mapping_file, args.ref_dir, args.output)

    if args.json:
        print(json.dumps(report, indent=2))
        return 1 if report["status"] == "FAIL" else 0

    print(f"Audit Status: {report['status']}")
    print(f"Stats:")
    print(f"  - Mapped unique references:    {report['stats']['mapped_unique_files']}")
    print(f"  - Physical files on disk:       {report['stats']['physical_files_on_disk']}")
    print(f"  - Compiled entries in output:   {report['stats']['compiled_entries_in_output']}")

    if report["errors"]:
        print(f"\n[ERRORS] ({len(report['errors'])}):")
        for e in report["errors"]:
            print(f"  x {e}")

    if report["warnings"]:
        print(f"\n[WARNINGS] ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"  ! {w}")

    if report["status"] == "PASS":
        print("\n[OK] Perfect triangular consistency: 0 missing files, 0 orphans, valid anchors.")
        return 0

    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
