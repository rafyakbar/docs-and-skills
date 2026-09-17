#!/usr/bin/env python3
"""arXiv API client wrapper.

Implements:
- arXiv-ID-first lookup with title cross-check (Levenshtein similarity >= 0.70)
- Title search fallback with exact-title-or-bust gate (#431)
- 3-second request pacing floor adhering to arXiv Terms of Use (ToU)
- Atom 1.0 XML parsing with xml.etree.ElementTree
- CLI invocation for terminal queries

Usage:
    python arxiv_client.py --id "1706.03762" --title "Attention Is All You Need"
    python arxiv_client.py --title "Deep Residual Learning for Image Recognition"
"""
from __future__ import annotations

import argparse
import http.client
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from _text_similarity import (
        _MAX_RETRIES,
        _TITLE_SIMILARITY_THRESHOLD,
        _similarity,
        exact_normalized_title,
        generic_title,
    )
except ImportError:
    from scripts._text_similarity import (
        _MAX_RETRIES,
        _TITLE_SIMILARITY_THRESHOLD,
        _similarity,
        exact_normalized_title,
        generic_title,
    )

_API_BASE = "http://export.arxiv.org/api/query"
_ATOM_NS = "{http://www.w3.org/2005/Atom}"
_ARXIV_MIN_INTERVAL = 3.0


def _extract_title(entry: ET.Element) -> str:
    node = entry.find(f"{_ATOM_NS}title")
    if node is None or node.text is None:
        return ""
    return " ".join(node.text.split())


def _extract_year(entry: ET.Element) -> int | None:
    node = entry.find(f"{_ATOM_NS}published")
    if node is None or not node.text:
        return None
    head = node.text[:4]
    return int(head) if head.isdigit() else None


def _extract_id(entry: ET.Element) -> str:
    node = entry.find(f"{_ATOM_NS}id")
    if node is None or not node.text:
        return ""
    raw_id = node.text.strip()
    return raw_id.split("/abs/")[-1]


def _entry_to_dict(entry: ET.Element) -> dict[str, Any]:
    return {
        "id": _extract_id(entry),
        "title": _extract_title(entry),
        "year": _extract_year(entry),
    }


class ArxivUnavailable(Exception):
    """arXiv API degraded or unavailable."""


class ArxivClient:
    """Production lookup-by-(arxiv-id-with-cross-check-then-title) client."""

    def __init__(self) -> None:
        self._min_interval = _ARXIV_MIN_INTERVAL
        self._last_request_at: float | None = None
        self._user_agent = "AcademicResearchSkill/1.0"

    def _throttle(self) -> None:
        if self._last_request_at is None:
            return
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

    def _get(self, query: dict[str, str]) -> list[ET.Element]:
        url = _API_BASE
        if query:
            url += "?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"User-Agent": self._user_agent})

        self._throttle()
        self._last_request_at = time.monotonic()

        for attempt in range(_MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    try:
                        body = resp.read()
                        root = ET.fromstring(body)
                    except (
                        OSError,
                        http.client.HTTPException,
                        ET.ParseError,
                    ) as e:
                        raise ArxivUnavailable(f"arXiv response read/parse failed: {e}") from e

                    if root.tag != f"{_ATOM_NS}feed":
                        raise ArxivUnavailable(
                            f"arXiv returned non-Atom body (tag: {root.tag!r})"
                        )
                    return root.findall(f"{_ATOM_NS}entry")
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < _MAX_RETRIES:
                    time.sleep(_ARXIV_MIN_INTERVAL)
                    self._last_request_at = time.monotonic()
                    continue
                raise ArxivUnavailable(f"arXiv HTTP {e.code}: {e.reason}") from e
            except (urllib.error.URLError, TimeoutError) as e:
                raise ArxivUnavailable(f"arXiv network error: {e}") from e

        raise ArxivUnavailable("arXiv rate limit exhausted after retries")

    def arxiv_id_lookup(
        self, arxiv_id: str, expected_title: str | None = None,
    ) -> dict[str, Any] | None:
        """arXiv ID lookup with title cross-check."""
        entries = self._get({"id_list": arxiv_id})
        if not entries:
            return None
        entry = entries[0]
        title = _extract_title(entry)
        if not expected_title:
            return _entry_to_dict(entry)
        if _similarity(title, expected_title) >= _TITLE_SIMILARITY_THRESHOLD:
            return _entry_to_dict(entry)
        return None  # ID_MISMATCH

    def title_search(
        self, title: str, year: int | None = None,
    ) -> dict[str, Any] | None:
        """Title search under the exact-title-or-bust gate."""
        if generic_title(title):
            return None
        entries = self._get({"search_query": f'ti:"{title}"', "max_results": "5"})
        scored = []
        for cand in entries:
            cand_title = _extract_title(cand)
            sim = _similarity(cand_title, title)
            if sim < _TITLE_SIMILARITY_THRESHOLD:
                continue
            if not exact_normalized_title(title, cand_title):
                continue
            year_match = year is not None and _extract_year(cand) == year
            score = sim + (0.05 if year_match else 0.0)
            scored.append((cand, score))
        if not scored:
            return None
        scored.sort(key=lambda cand_score: -cand_score[1])
        return _entry_to_dict(scored[0][0])


def main() -> int:
    parser = argparse.ArgumentParser(description="arXiv API metadata query client.")
    parser.add_argument("--id", help="arXiv paper ID (e.g. 1706.03762)")
    parser.add_argument("--title", help="Paper title to query or cross-check")
    parser.add_argument("--year", type=int, help="Publication year for tie-breaking")

    args = parser.parse_args()
    client = ArxivClient()

    try:
        if args.id:
            res = client.arxiv_id_lookup(args.id, args.title)
            if res:
                output = {
                    "matched": True,
                    "queried_by": "id",
                    "id": res.get("id"),
                    "title": res.get("title"),
                    "year": res.get("year"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "id"}, indent=2))
            return 1
        elif args.title:
            res = client.title_search(args.title, args.year)
            if res:
                output = {
                    "matched": True,
                    "queried_by": "title",
                    "id": res.get("id"),
                    "title": res.get("title"),
                    "year": res.get("year"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "title"}, indent=2))
            return 1
        else:
            parser.print_help()
            return 0
    except ArxivUnavailable as e:
        print(json.dumps({"error": str(e), "status": "unreachable"}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
