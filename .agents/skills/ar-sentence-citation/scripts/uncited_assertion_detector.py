#!/usr/bin/env python3
"""D4-c uncited-assertion token-rule detector.

Implements the three-condition rule:
1. Quantifier-or-empirical-verb present (percentages, ratios, bare numbers, fuzzy quantifiers, empirical verbs).
   Bare numbers are guarded against publication years, version triples, and section references.
2. No citation marker on the sentence (neither `<!--ref:...-->` nor `[1]`/`[@cite]`).
3. Not a definitional or self-contribution sentence.

Can be run via CLI to audit markdown drafts or individual sentences:
    python uncited_assertion_detector.py paper/01_introduction.md
    python uncited_assertion_detector.py --text "Our baseline model showed a 14.5% improvement."
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

# Support sibling and direct execution
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from _claim_audit_constants import (
        RE_BARE_NUMERIC_YEAR,
        RE_DOTTED_PAIR,
        RE_DOTTED_TRIPLE_OR_MORE,
        RE_NUMERIC_LEFT_ATTACHED,
        RE_NUMERIC_QUANTIFIER,
        RE_REF_MARKER,
        RE_SECTION_CUE,
        RE_VERSION_PREFIX,
        UNCITED_DEFINITION_PHRASES,
        UNCITED_EMPIRICAL_VERBS,
        UNCITED_FUZZY_QUANTIFIERS,
    )
except ImportError:
    from scripts._claim_audit_constants import (
        RE_BARE_NUMERIC_YEAR,
        RE_DOTTED_PAIR,
        RE_DOTTED_TRIPLE_OR_MORE,
        RE_NUMERIC_LEFT_ATTACHED,
        RE_NUMERIC_QUANTIFIER,
        RE_REF_MARKER,
        RE_SECTION_CUE,
        RE_VERSION_PREFIX,
        UNCITED_DEFINITION_PHRASES,
        UNCITED_EMPIRICAL_VERBS,
        UNCITED_FUZZY_QUANTIFIERS,
    )

# Word pattern for fuzzy quantifier and verb extraction
_RE_WORD = re.compile(r"[A-Za-z\u00C0-\u024F]+(?:-[A-Za-z\u00C0-\u024F]+)*")
_GUARD_LEFT_WINDOW = 24


def _is_year_or_version_or_section(
    sentence: str, match_text: str, match_start: int
) -> bool:
    """Guard pass: return True when a bare-number match is NOT an empirical quantifier."""
    if RE_BARE_NUMERIC_YEAR.match(match_text):
        return True
    if RE_DOTTED_TRIPLE_OR_MORE.match(match_text):
        return True

    left = sentence[max(0, match_start - _GUARD_LEFT_WINDOW) : match_start]
    if RE_SECTION_CUE.search(left):
        return True
    if RE_DOTTED_PAIR.match(match_text) and RE_VERSION_PREFIX.search(left):
        return True

    if match_start > 0:
        if sentence[match_start - 1] == ".":
            left_search_start = max(0, match_start - _GUARD_LEFT_WINDOW)
            left = sentence[left_search_start:match_start]
            if RE_NUMERIC_LEFT_ATTACHED.search(left):
                return True
        elif "." in match_text and sentence[match_start - 1].isspace():
            scan_idx = match_start - 1
            while scan_idx > 0 and sentence[scan_idx].isspace():
                scan_idx -= 1
            if sentence[scan_idx] == ".":
                left_search_start = max(0, scan_idx + 1 - _GUARD_LEFT_WINDOW)
                left = sentence[left_search_start : scan_idx + 1]
                if RE_NUMERIC_LEFT_ATTACHED.search(left):
                    return True
    return False


def detect_uncited(sentence: str) -> tuple[bool, list[str]]:
    """Return `(is_candidate, trigger_tokens)` for one sentence.

    Trigger tokens are returned in document order.
    """
    lowered = sentence.lower()
    # Condition 3: definition or contribution exclusion
    if any(phrase in lowered for phrase in UNCITED_DEFINITION_PHRASES):
        return False, []

    # Condition 2: citation reference marker present
    if RE_REF_MARKER.search(sentence):
        return False, []

    # Condition 1: quantifier or empirical verb detection
    matches: list[tuple[int, str]] = []
    for m in RE_NUMERIC_QUANTIFIER.finditer(sentence):
        text = m.group(0)
        # Percentages and ratio idioms always count as quantifiers
        if "%" not in text and " of " not in text and " dari " not in text:
            if _is_year_or_version_or_section(sentence, text, m.start()):
                continue
        matches.append((m.start(), text))

    # Fuzzy quantifiers + empirical verbs match
    triggers = UNCITED_FUZZY_QUANTIFIERS | UNCITED_EMPIRICAL_VERBS
    for m in _RE_WORD.finditer(sentence):
        token = m.group(0).lower()
        if token in triggers:
            matches.append((m.start(), token))

    # Also match multi-word fuzzy quantifiers (e.g. "sebagian besar", "dua pertiga")
    for phrase in UNCITED_FUZZY_QUANTIFIERS:
        if " " in phrase and phrase in lowered:
            idx = lowered.find(phrase)
            matches.append((idx, phrase))

    if not matches:
        return False, []

    matches.sort(key=lambda pair: pair[0])
    trigger_tokens = list(dict.fromkeys(token for _, token in matches))
    return (bool(trigger_tokens), trigger_tokens)


def detect_uncited_assertions(
    sentences: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Filter draft sentences down to uncited assertion candidates."""
    candidates: list[dict[str, Any]] = []
    for index, raw in enumerate(sentences):
        if "sentence_text" not in raw:
            raise ValueError(
                f"detect_uncited_assertions: sentences[{index}] missing 'sentence_text'"
            )
        sentence_text = raw["sentence_text"]
        if not isinstance(sentence_text, str):
            raise ValueError(
                f"detect_uncited_assertions: sentences[{index}]['sentence_text'] must be str"
            )
        is_candidate, tokens = detect_uncited(sentence_text)
        if not is_candidate:
            continue

        adjacent_text = raw.get("adjacent_text")
        if isinstance(adjacent_text, str) and RE_REF_MARKER.search(adjacent_text):
            continue

        enriched = dict(raw)
        enriched["trigger_tokens"] = tokens
        candidates.append(enriched)
    return candidates


# Markdown Parsing Utility for CLI
_ABBREVIATIONS = (
    "e.g.", "i.e.", "et al.", "fig.", "tab.", "eq.", "cf.", "vs.",
    "dr.", "prof.", "al.", "no.", "vol.", "pp."
)


def split_sentences_from_text(text: str) -> list[str]:
    """Split paragraph text into individual sentences cleanly."""
    text = text.strip()
    if not text:
        return []

    # Protect common abbreviations from being split
    protected = text
    for i, abbr in enumerate(_ABBREVIATIONS):
        protected = re.sub(
            re.escape(abbr),
            f"__ABBR_{i}__",
            protected,
            flags=re.IGNORECASE,
        )

    # Split by standard sentence terminators followed by whitespace
    raw_sentences = re.split(r"(?<=[.!?])\s+", protected)

    restored = []
    for s in raw_sentences:
        res = s
        for i, abbr in enumerate(_ABBREVIATIONS):
            res = res.replace(f"__ABBR_{i}__", abbr)
        res = res.strip()
        if res:
            restored.append(res)
    return restored


def extract_sentences_from_markdown(md_content: str) -> list[dict[str, Any]]:
    """Parse a Markdown document into structured sentence entries with location metadata."""
    lines = md_content.splitlines()
    sentences_data: list[dict[str, Any]] = []
    in_code_block = False
    current_paragraph: list[str] = []
    paragraph_num = 0
    start_line = 1

    def flush_paragraph(p_lines: list[str], p_num: int, line_no: int):
        p_text = " ".join(l.strip() for l in p_lines if l.strip())
        if not p_text:
            return
        sentences = split_sentences_from_text(p_text)
        for s_idx, s in enumerate(sentences):
            prev_s = sentences[s_idx - 1] if s_idx > 0 else ""
            next_s = sentences[s_idx + 1] if s_idx + 1 < len(sentences) else ""
            adjacent = f"{prev_s} {next_s}".strip()
            sentences_data.append({
                "sentence_text": s,
                "paragraph": p_num,
                "approx_line": line_no,
                "adjacent_text": adjacent,
            })

    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Skip headers, tables, horizontal rules
        if (
            stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("---")
            or stripped.startswith("===")
        ):
            if current_paragraph:
                paragraph_num += 1
                flush_paragraph(current_paragraph, paragraph_num, start_line)
                current_paragraph = []
            continue

        if not stripped:
            if current_paragraph:
                paragraph_num += 1
                flush_paragraph(current_paragraph, paragraph_num, start_line)
                current_paragraph = []
        else:
            if not current_paragraph:
                start_line = line_idx
            current_paragraph.append(stripped)

    if current_paragraph:
        paragraph_num += 1
        flush_paragraph(current_paragraph, paragraph_num, start_line)

    return sentences_data


def load_mapped_sentences_from_references_txt(ref_file_path: Path) -> set[str]:
    """Extract all quoted claim strings from a paper/references.txt file."""
    if not ref_file_path.exists():
        return set()
    mapped = set()
    content = ref_file_path.read_text(encoding="utf-8")
    # Match both `- "Sentence":` and `- 'Sentence':`
    for m in re.finditer(r'''-\s*["']([^"']+)["']\s*:''', content):
        cleaned = " ".join(m.group(1).split()).lower()
        mapped.add(cleaned)
    return mapped


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect uncited empirical assertions in draft papers (D4-c Rule)."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to markdown draft file (e.g. paper/01_introduction.md)",
    )
    parser.add_argument(
        "--text",
        help="Direct sentence text to inspect",
    )
    parser.add_argument(
        "-r",
        "--references-file",
        help="Path to paper/references.txt mapping file (filters out already-mapped sentences)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output findings in JSON format",
    )

    args = parser.parse_args()

    if args.text:
        is_candidate, tokens = detect_uncited(args.text)
        finding = {
            "sentence_text": args.text,
            "uncited": is_candidate,
            "trigger_tokens": tokens,
        }
        if args.json:
            print(json.dumps(finding, indent=2, ensure_ascii=False))
        else:
            if is_candidate:
                print(f"[!] Uncited Assertion Detected:")
                print(f"    Text: {args.text}")
                print(f"    Triggers: {', '.join(tokens)}")
            else:
                print("[OK] Sentence properly cited or exempt.")
        return 1 if is_candidate else 0

    if not args.file:
        parser.print_help()
        return 0

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        return 2

    content = file_path.read_text(encoding="utf-8")
    sentence_records = extract_sentences_from_markdown(content)
    findings = detect_uncited_assertions(sentence_records)

    mapped_sentences: set[str] = set()
    if args.references_file:
        ref_p = Path(args.references_file)
        if ref_p.exists():
            mapped_sentences = load_mapped_sentences_from_references_txt(ref_p)
            findings = [
                f for f in findings
                if " ".join(f["sentence_text"].split()).lower() not in mapped_sentences
            ]
        else:
            print(f"Warning: References file '{args.references_file}' not found.", file=sys.stderr)

    if args.json:
        print(json.dumps(findings, indent=2, ensure_ascii=False))
    else:
        print(f"Audit Target: {file_path}")
        print(f"Total Sentences Scanned: {len(sentence_records)}")
        if args.references_file:
            print(f"References Mapping Loaded: {args.references_file} ({len(mapped_sentences)} mapped claims)")
        print(f"Uncited Candidates Remaining: {len(findings)}\n")

        if not findings:
            print("[OK] All empirical sentences have citations or are mapped in references.txt.")
            return 0

        for i, item in enumerate(findings, 1):
            print(f"{i}. [Line ~{item.get('approx_line')}, Para {item.get('paragraph')}]:")
            print(f"   \"{item['sentence_text']}\"")
            print(f"   Triggers: {', '.join(item['trigger_tokens'])}\n")


    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
