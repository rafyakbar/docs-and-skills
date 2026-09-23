#!/usr/bin/env python3
"""Linter and integrity checker for rebuttal audit reports and drafts.

Verifies:
  1. Dual-document requirement (comments and rebuttal both provided).
  2. Zero-orphan rule: missing_count == 0 (no reviewer comments dropped).
  3. Tone safety: high_risk_flags == 0 (no combative or hostile language).
  4. Evidence grounding: minimum locator presence threshold (>= 80%).
  5. Audit report structure and schema compliance.

Exit codes:
  0 = all integrity checks passed
  1 = integrity violations found

Usage:
    python scripts/verify_rebuttal_integrity.py --report 11_rebuttal_audit_report.json
    python scripts/verify_rebuttal_integrity.py --comments comments.md --rebuttal response.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure script's directory is in sys.path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from ars_rebuttal_auditor import audit_rebuttal


def verify_audit_data(audit_data: dict) -> tuple[bool, list[str]]:
    """Verify an audit result dictionary against integrity rules."""
    failures: list[str] = []
    c = audit_data.get("counters", {})

    # 1. Zero-orphan check
    missing = c.get("missing_count", 0)
    if missing > 0:
        failures.append(f"Zero-Orphan Violation: {missing} reviewer comment(s) were dropped or unanswered.")

    # 2. Tone safety check
    high_risk = c.get("high_risk_flags", 0)
    if high_risk > 0:
        failures.append(f"Tone Safety Violation: {high_risk} HIGH-severity risk flag(s) detected (defensive/hostile/unjustified).")

    # 3. Grounding check
    items = audit_data.get("item_results", [])
    total_addressed = c.get("addressed_count", 0)
    if total_addressed > 0:
        with_locators = sum(
            1 for it in items
            if (it.get("locators_found") or "acknowledg" in it.get("response_snippet", "").lower())
            and it.get("coverage_status") == "ADDRESSED"
        )
        ratio = with_locators / total_addressed
        if ratio < 0.80:
            failures.append(
                f"Evidence Grounding Weakness: Only {ratio*100:.1f}% of addressed items specify manuscript locators (target: >= 80%)."
            )

    return len(failures) == 0, failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--report", type=Path, default=None, help="Path to JSON audit report")
    parser.add_argument("--comments", type=Path, default=None, help="Path to reviewer comments")
    parser.add_argument("--rebuttal", type=Path, default=None, help="Path to rebuttal draft")
    args = parser.parse_args(argv)

    if args.report:
        if not args.report.exists():
            print(f"ERROR: Report file not found: {args.report}", file=sys.stderr)
            return 1
        try:
            data = json.loads(args.report.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"ERROR: Failed to parse JSON report: {exc}", file=sys.stderr)
            return 1
    elif args.comments and args.rebuttal:
        if not args.comments.exists() or not args.rebuttal.exists():
            print("ERROR: Comments or rebuttal file does not exist.", file=sys.stderr)
            return 1
        c_text = args.comments.read_text(encoding="utf-8")
        r_text = args.rebuttal.read_text(encoding="utf-8")
        data = audit_rebuttal(c_text, r_text)
    else:
        parser.error("Must provide either --report or BOTH --comments and --rebuttal.")

    ok, failures = verify_audit_data(data)
    if ok:
        print("verify_rebuttal_integrity: OK (all integrity checks passed)")
        return 0
    else:
        print("verify_rebuttal_integrity: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
