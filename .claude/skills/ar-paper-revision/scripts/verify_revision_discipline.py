#!/usr/bin/env python3
"""Linter for revision patch discipline and integrity (ARS Spec #390 / #424).

Verifies:
  1. Patch document JSON schema compliance (pure stdlib).
  2. Base draft hash agreement between patch and draft on disk.
  3. Single-target rule: each block_id appears in at most one op.
  4. No embedded `<!--block:` markers in `new_text`.
  5. Touched ratio calculation and structural flag triggers (threshold 0.6).
  6. Apply report consistency (output_draft_hash and patch_digest binding).
  7. Marker integrity in drafts (no orphan markers, no duplicate block IDs).

Exit codes:
  0 = all discipline checks passed
  1 = discipline violations detected

Usage:
    python scripts/verify_revision_discipline.py --draft draft.md --patch patch.json
    python scripts/verify_revision_discipline.py --draft draft.md --patch patch.json --output draft.rev1.md --report draft.rev1.md.apply-report.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# Ensure script's directory is in sys.path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from _block_parser import (
    BlockParseError,
    base_draft_hash,
    parse_document,
)
from ars_apply_revision_patch import (
    DEFAULT_TOUCHED_RATIO_THRESHOLD,
    validate_patch_schema_native,
)


def verify_discipline(
    draft_path: Path | None,
    patch_path: Path | None,
    output_path: Path | None = None,
    report_path: Path | None = None,
    touched_ratio_threshold: float = DEFAULT_TOUCHED_RATIO_THRESHOLD,
) -> tuple[bool, list[str]]:
    """Verify revision discipline and return (success, failure_messages)."""
    failures: list[str] = []

    # 1. Verify Draft integrity if provided
    base_parsed = None
    base_raw = b""
    if draft_path is not None:
        if not draft_path.exists():
            failures.append(f"Base draft file not found: {draft_path}")
        else:
            base_raw = draft_path.read_bytes()
            try:
                base_text = base_raw.decode("utf-8")
                base_parsed = parse_document(base_text)
            except UnicodeDecodeError as exc:
                failures.append(f"Base draft UTF-8 decoding error: {exc}")
            except BlockParseError as exc:
                failures.append(f"Base draft malformed [{exc.kind}]: {exc}")

    # 2. Verify Patch document if provided
    patch_obj = None
    patch_raw = b""
    if patch_path is not None:
        if not patch_path.exists():
            failures.append(f"Patch file not found: {patch_path}")
        else:
            patch_raw = patch_path.read_bytes()
            try:
                patch_obj = json.loads(patch_raw.decode("utf-8"))
            except Exception as exc:
                failures.append(f"Patch JSON parse error: {exc}")

            if patch_obj is not None:
                # Schema check
                schema_errs = validate_patch_schema_native(patch_obj)
                for err in schema_errs:
                    failures.append(f"Schema violation: {err}")

                # Base hash check
                if base_raw and "base_draft_hash" in patch_obj:
                    expected_hash = base_draft_hash(base_raw)
                    actual_in_patch = patch_obj["base_draft_hash"]
                    if expected_hash != actual_in_patch:
                        failures.append(
                            f"Base draft hash mismatch: patch expects {actual_in_patch}, "
                            f"actual base draft is {expected_hash}"
                        )

                # Single-target rule & marker prohibition
                if "ops" in patch_obj and isinstance(patch_obj["ops"], list):
                    seen_targets: dict[str, int] = {}
                    touched_count = 0
                    for idx, op in enumerate(patch_obj["ops"]):
                        if not isinstance(op, dict):
                            continue
                        bid = op.get("block_id")
                        if bid in seen_targets:
                            failures.append(
                                f"Duplicate target block '{bid}' in op {idx} (previously in op {seen_targets[bid]})"
                            )
                        elif bid:
                            seen_targets[bid] = idx

                        if op.get("op") in ("replace_block", "delete_block"):
                            touched_count += 1

                        new_text = op.get("new_text")
                        if new_text and "<!--block:" in new_text:
                            failures.append(
                                f"Marker prohibition violated in op {idx}: new_text contains '<!--block:'"
                            )

                    # Touched ratio check
                    if base_parsed is not None:
                        total_blocks = len(base_parsed.blocks)
                        if total_blocks > 0:
                            ratio = touched_count / total_blocks
                            if ratio > touched_ratio_threshold:
                                failures.append(
                                    f"Structural warning: touched ratio {ratio:.4f} strictly exceeds "
                                    f"threshold {touched_ratio_threshold:.4f} ({touched_count}/{total_blocks} blocks)"
                                )

    # 3. Verify Output and Report if provided
    if output_path is not None and output_path.exists():
        out_raw = output_path.read_bytes()
        try:
            out_parsed = parse_document(out_raw.decode("utf-8"))
            # Assert marker uniqueness
            ids = [b.block_id for b in out_parsed.blocks if b.block_id is not None]
            if len(ids) != len(set(ids)):
                failures.append("Revised output draft contains duplicate block IDs")
        except Exception as exc:
            failures.append(f"Revised output draft parse error: {exc}")

        if report_path is not None and report_path.exists():
            try:
                rep = json.loads(report_path.read_text(encoding="utf-8"))
                expected_out_hash = base_draft_hash(out_raw)
                if rep.get("output_draft_hash") != expected_out_hash:
                    failures.append(
                        f"Apply report output_draft_hash mismatch: report states {rep.get('output_draft_hash')}, "
                        f"actual output draft is {expected_out_hash}"
                    )
                if patch_raw:
                    expected_patch_digest = hashlib.sha256(patch_raw).hexdigest()
                    if rep.get("patch_digest") != expected_patch_digest:
                        failures.append(
                            f"Apply report patch_digest mismatch: report states {rep.get('patch_digest')}, "
                            f"actual patch digest is {expected_patch_digest}"
                        )
            except Exception as exc:
                failures.append(f"Apply report JSON parse error: {exc}")

    return len(failures) == 0, failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--draft", type=Path, default=None, help="base draft markdown")
    parser.add_argument("--patch", type=Path, default=None, help="revision patch JSON")
    parser.add_argument("--output", type=Path, default=None, help="revised draft markdown (optional)")
    parser.add_argument("--report", type=Path, default=None, help="apply report JSON (optional)")
    parser.add_argument(
        "--touched-ratio-threshold",
        type=float,
        default=DEFAULT_TOUCHED_RATIO_THRESHOLD,
        help="touched ratio threshold (default 0.6)",
    )
    args = parser.parse_args(argv)

    if not args.draft and not args.patch:
        parser.error("At least --draft or --patch must be provided.")

    ok, failures = verify_discipline(
        draft_path=args.draft,
        patch_path=args.patch,
        output_path=args.output,
        report_path=args.report,
        touched_ratio_threshold=args.touched_ratio_threshold,
    )

    if ok:
        print("verify_revision_discipline: OK (all checks passed)")
        return 0
    else:
        print("verify_revision_discipline: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
