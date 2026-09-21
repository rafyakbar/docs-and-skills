#!/usr/bin/env python3
"""Citation verification summary reducer.

Reduces per-resolver outcomes (Crossref, Semantic Scholar, OpenAlex, arXiv)
to a 3-class verdict:
- `true`: At least one applicable resolver matched.
- `false`: No resolver matched AND at least one ID-keyed query failed (fabrication evidence).
- `unresolvable`: Coverage gap (only title queries failed or all resolvers unreachable/skipped).

Usage:
    python citation_verification_summary.py '{"crossref": {"status": "matched"}, "arxiv": {"status": "skipped"}}'
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Mapping

STATUS_MATCHED = "matched"
STATUS_UNMATCHED = "unmatched"
STATUS_UNREACHABLE = "unreachable"
STATUS_SKIPPED = "skipped"

QUERIED_BY_ID = "id"


def reduce_lookup_verified(resolver_outcomes: Mapping[str, Any]) -> str:
    """Reduce per-resolver outcomes to a 3-class lookup_verified value.

    Rules:
    1. 'skipped' outcomes are excluded from classification.
    2. 'true' iff >= 1 applicable resolver is 'matched'.
    3. 'false' iff NO applicable resolver is 'matched' AND >= 1 applicable resolver
       is an ID-keyed 'unmatched' (status='unmatched' and queried_by='id').
    4. 'unresolvable' otherwise.
    """
    outcomes = [v or {} for v in resolver_outcomes.values()]
    applicable = [o for o in outcomes if o.get("status") != STATUS_SKIPPED]

    if any(o.get("status") == STATUS_MATCHED for o in applicable):
        return "true"

    id_keyed_unmatched = any(
        o.get("status") == STATUS_UNMATCHED and o.get("queried_by") == QUERIED_BY_ID
        for o in applicable
    )
    if id_keyed_unmatched:
        return "false"

    return "unresolvable"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Triangulate citation verification outcomes into a single verdict."
    )
    parser.add_argument(
        "json_input",
        nargs="?",
        help="JSON string or file path containing resolver outcomes mapping",
    )

    args = parser.parse_args()

    if not args.json_input:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
        else:
            parser.print_help()
            return 0
    else:
        raw = args.json_input

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Check if it's a file path
        try:
            with open(raw, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error: Invalid JSON or file path: {e}", file=sys.stderr)
            return 2

    verdict = reduce_lookup_verified(data)
    result = {
        "lookup_verified": verdict,
        "input_resolvers": list(data.keys()),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
