#!/usr/bin/env python3
"""Semantic Scholar API client wrapper.

Implements:
- DOI-first lookup with title cross-check (Levenshtein similarity >= 0.70)
- Title search fallback with exact-title-or-bust gate (#431)
- API key authentication (10 req/s) vs anonymous pacing (1 req/s)
- HTTP 429 backoff and network outage latching
- CLI invocation for terminal queries

Usage:
    python semantic_scholar_client.py --doi "10.1145/3375627.3375820" --title "Face Recognition"
    python semantic_scholar_client.py --title "Attention Is All You Need" --year 2017
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Mapping

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from _text_similarity import (
        _BACKOFF_SECONDS,
        _MAX_RETRIES,
        _TITLE_SIMILARITY_THRESHOLD,
        _similarity,
        exact_normalized_title,
        generic_title,
    )
except ImportError:
    from scripts._text_similarity import (
        _BACKOFF_SECONDS,
        _MAX_RETRIES,
        _TITLE_SIMILARITY_THRESHOLD,
        _similarity,
        exact_normalized_title,
        generic_title,
    )

_API_BASE = "https://api.semanticscholar.org/graph/v1"
_API_HOST = "api.semanticscholar.org"
_API_KEY_ENV = "S2_API_KEY"
_FIELDS = "title,authors,year,externalIds,venue,publicationDate"

_UNAUTHENTICATED_MIN_INTERVAL = 1.0
_AUTHENTICATED_MIN_INTERVAL = 0.1


def _require_api_url(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != _API_HOST:
        raise SemanticScholarUnavailable(f"Refusing non-S2 URL: {url}")


class SemanticScholarUnavailable(Exception):
    """Semantic Scholar API degraded or unavailable."""


class SemanticScholarClient:
    """Production lookup-by-(doi-then-title) client for Semantic Scholar."""

    def __init__(
        self,
        api_key: str | None = None,
        min_interval_seconds: float | None = None,
    ) -> None:
        self._api_key = api_key or os.environ.get(_API_KEY_ENV)
        if min_interval_seconds is None:
            self._min_interval = (
                _AUTHENTICATED_MIN_INTERVAL if self._api_key
                else _UNAUTHENTICATED_MIN_INTERVAL
            )
        else:
            self._min_interval = min_interval_seconds
        self._last_request_at: float | None = None
        self._latched_unavailable: bool = False

    def reset_outage_latch(self) -> None:
        """Clear outage latch to allow subsequent retry."""
        self._latched_unavailable = False

    def lookup(self, entry: Mapping[str, Any]) -> Mapping[str, Any]:
        """Lookup paper by DOI first, falling back to title."""
        doi = entry.get("doi")
        title = entry.get("title") or ""
        if doi:
            doi_result = self._lookup_by_doi(doi, title)
            if doi_result["matched"]:
                return doi_result
        if title:
            return self._lookup_by_title(title, entry.get("year"))
        return {"matched": False, "paperId": None}

    def _request(self, path: str) -> dict[str, Any]:
        if self._latched_unavailable:
            raise SemanticScholarUnavailable(
                "S2 API latched unavailable after prior network failure; "
                "call reset_outage_latch() to retry."
            )

        if self._last_request_at is not None and self._min_interval > 0:
            elapsed = time.monotonic() - self._last_request_at
            remaining = self._min_interval - elapsed
            if remaining > 0:
                time.sleep(remaining)
        self._last_request_at = time.monotonic()

        url = f"{_API_BASE}{path}"
        _require_api_url(url)
        headers = {"User-Agent": "AcademicResearchSkill/1.0"}
        if self._api_key:
            headers["x-api-key"] = self._api_key
        req = urllib.request.Request(url, headers=headers)

        for attempt in range(_MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return {}
                if e.code == 429 and attempt < _MAX_RETRIES:
                    time.sleep(_BACKOFF_SECONDS)
                    self._last_request_at = time.monotonic()
                    continue
                if 500 <= e.code < 600:
                    raise SemanticScholarUnavailable(f"S2 API HTTP {e.code}") from e
                raise SemanticScholarUnavailable(
                    f"S2 API HTTP {e.code} after {_MAX_RETRIES} retries"
                ) from e
            except urllib.error.URLError as e:
                self._latched_unavailable = True
                raise SemanticScholarUnavailable(f"S2 API network error: {e}") from e
            except (OSError, TimeoutError) as e:
                self._latched_unavailable = True
                raise SemanticScholarUnavailable(
                    f"S2 API I/O failure during response read: {e}"
                ) from e
        raise SemanticScholarUnavailable(f"S2 API exhausted {_MAX_RETRIES} retries")

    def _lookup_by_doi(self, doi: str, expected_title: str | None = None) -> dict[str, Any]:
        data = self._request(
            f"/paper/DOI:{urllib.parse.quote(doi, safe='')}?fields={_FIELDS}"
        )
        if not data or not data.get("paperId"):
            return {"matched": False, "paperId": None}
        if expected_title:
            returned_title = data.get("title") or ""
            if _similarity(expected_title, returned_title) < _TITLE_SIMILARITY_THRESHOLD:
                return {"matched": False, "paperId": None}
        return {"matched": True, "paperId": data["paperId"], "data": data}

    def _lookup_by_title(self, title: str, year: int | None = None) -> dict[str, Any]:
        if generic_title(title):
            return {"matched": False, "paperId": None}
        path = (
            f"/paper/search?query={urllib.parse.quote(title)}"
            f"&limit=5&fields={_FIELDS}"
        )
        data = self._request(path)
        candidates = data.get("data") or []
        best: tuple[float, dict[str, Any]] | None = None
        for cand in candidates:
            cand_title = cand.get("title") or ""
            sim = _similarity(title, cand_title)
            if sim < _TITLE_SIMILARITY_THRESHOLD:
                continue
            if not exact_normalized_title(title, cand_title):
                continue
            year_match = year is not None and cand.get("year") == year
            score = sim + (0.05 if year_match else 0.0)
            if best is None or score > best[0]:
                best = (score, cand)
        if best is None:
            return {"matched": False, "paperId": None}
        return {"matched": True, "paperId": best[1].get("paperId"), "data": best[1]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Semantic Scholar API metadata query client.")
    parser.add_argument("--doi", help="DOI string to look up (e.g. 10.1145/3375627.3375820)")
    parser.add_argument("--title", help="Paper title to query or cross-check")
    parser.add_argument("--year", type=int, help="Publication year for tie-breaking")
    parser.add_argument("--api-key", help="Semantic Scholar API Key")

    args = parser.parse_args()
    client = SemanticScholarClient(api_key=args.api_key)

    try:
        if args.doi:
            res = client._lookup_by_doi(args.doi, args.title)
            if res.get("matched"):
                data = res.get("data", {})
                output = {
                    "matched": True,
                    "queried_by": "doi",
                    "paperId": res.get("paperId"),
                    "title": data.get("title"),
                    "year": data.get("year"),
                    "venue": data.get("venue"),
                    "externalIds": data.get("externalIds"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "doi"}, indent=2))
            return 1
        elif args.title:
            res = client._lookup_by_title(args.title, args.year)
            if res.get("matched"):
                data = res.get("data", {})
                output = {
                    "matched": True,
                    "queried_by": "title",
                    "paperId": res.get("paperId"),
                    "title": data.get("title"),
                    "year": data.get("year"),
                    "venue": data.get("venue"),
                    "externalIds": data.get("externalIds"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "title"}, indent=2))
            return 1
        else:
            parser.print_help()
            return 0
    except SemanticScholarUnavailable as e:
        print(json.dumps({"error": str(e), "status": "unreachable"}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
