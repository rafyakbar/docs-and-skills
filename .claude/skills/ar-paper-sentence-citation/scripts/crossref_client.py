#!/usr/bin/env python3
"""Crossref API client wrapper.

Implements:
- DOI-first lookup with title cross-check (Levenshtein similarity >= 0.70)
- Title search fallback with exact-title-or-bust gate (#431)
- Polite pool email header support
- Rate-limit throttling and exponential backoff
- CLI invocation for terminal queries

Usage:
    python crossref_client.py --doi "10.1145/3375627.3375820" --title "Face Recognition"
    python crossref_client.py --title "Attention Is All You Need" --year 2017
"""
from __future__ import annotations

import argparse
import http.client
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

_API_BASE = "https://api.crossref.org"
_API_HOST = "api.crossref.org"
_POLITE_EMAIL_ENV = "CROSSREF_POLITE_EMAIL"

_POLITE_MIN_INTERVAL = 0.1
_ANONYMOUS_MIN_INTERVAL = 0.2


def _require_api_url(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != _API_HOST:
        redacted = urllib.parse.urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, "", "")
        )
        raise CrossrefUnavailable(f"Refusing non-Crossref URL: {redacted}")


def _extract_title(message_or_item: Mapping[str, Any]) -> str:
    titles = message_or_item.get("title") or []
    return titles[0] if titles else ""


def _extract_year(item: Mapping[str, Any]) -> int | None:
    for key in ("issued", "published-print", "published-online"):
        val = item.get(key)
        if not isinstance(val, dict):
            continue
        date_parts = val.get("date-parts")
        if date_parts and date_parts[0]:
            return date_parts[0][0]
    return None


class CrossrefUnavailable(Exception):
    """Crossref API degraded or unavailable."""


class CrossrefClient:
    """Production lookup-by-(doi-with-cross-check-then-title) client for Crossref."""

    def __init__(self, polite_email: str | None = None):
        self._polite_email = polite_email or os.environ.get(_POLITE_EMAIL_ENV)
        self._min_interval = (
            _POLITE_MIN_INTERVAL if self._polite_email else _ANONYMOUS_MIN_INTERVAL
        )
        self._last_request_at: float | None = None
        ua = "AcademicResearchSkill/1.0"
        if self._polite_email:
            ua += f" (mailto:{self._polite_email})"
        self._user_agent = ua

    def _throttle(self) -> None:
        if self._last_request_at is None:
            return
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

    def _get(self, path: str, query: Mapping[str, str]) -> dict[str, Any]:
        url = f"{_API_BASE}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        _require_api_url(url)
        req = urllib.request.Request(url, headers={"User-Agent": self._user_agent})

        self._throttle()
        self._last_request_at = time.monotonic()

        for attempt in range(_MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    try:
                        body = resp.read()
                        return json.loads(body.decode("utf-8"))
                    except (
                        OSError,
                        http.client.HTTPException,
                        UnicodeDecodeError,
                        json.JSONDecodeError,
                    ) as e:
                        raise CrossrefUnavailable(
                            f"Crossref response read/parse failed: {e}"
                        ) from e
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return {}
                if e.code == 429 and attempt < _MAX_RETRIES:
                    time.sleep(_BACKOFF_SECONDS)
                    self._last_request_at = time.monotonic()
                    continue
                raise CrossrefUnavailable(f"Crossref HTTP {e.code}: {e.reason}") from e
            except (urllib.error.URLError, TimeoutError) as e:
                raise CrossrefUnavailable(f"Crossref network error: {e}") from e

        raise CrossrefUnavailable("Crossref rate limit exhausted after retries")

    def doi_lookup_with_title_check(
        self, doi: str, expected_title: str | None = None,
    ) -> dict[str, Any] | None:
        """DOI lookup with optional/mandatory Levenshtein 0.70 title cross-check."""
        data = self._get(f"/works/{urllib.parse.quote(doi, safe='')}", {})
        if not data:
            return None
        message = data.get("message", {})
        if not expected_title:
            return message
        title = _extract_title(message)
        if _similarity(title, expected_title) >= _TITLE_SIMILARITY_THRESHOLD:
            return message
        return None  # DOI_MISMATCH

    def title_search(
        self, title: str, year: int | None = None,
    ) -> dict[str, Any] | None:
        """Title search under the exact-title-or-bust gate."""
        if generic_title(title):
            return None
        data = self._get("/works", {"query.title": title, "rows": "5"})
        candidates = data.get("message", {}).get("items", [])
        scored = []
        for cand in candidates:
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
        scored.sort(key=lambda cand_score: (-cand_score[1],))
        return scored[0][0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Crossref API metadata query client.")
    parser.add_argument("--doi", help="DOI string to look up (e.g. 10.1145/3375627.3375820)")
    parser.add_argument("--title", help="Paper title to query or cross-check")
    parser.add_argument("--year", type=int, help="Publication year for tie-breaking")
    parser.add_argument("--email", help="Polite pool email address")

    args = parser.parse_args()
    client = CrossrefClient(polite_email=args.email)

    try:
        if args.doi:
            result = client.doi_lookup_with_title_check(args.doi, args.title)
            if result:
                output = {
                    "matched": True,
                    "queried_by": "doi",
                    "title": _extract_title(result),
                    "year": _extract_year(result),
                    "doi": result.get("DOI"),
                    "publisher": result.get("publisher"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "doi"}, indent=2))
            return 1
        elif args.title:
            result = client.title_search(args.title, args.year)
            if result:
                output = {
                    "matched": True,
                    "queried_by": "title",
                    "title": _extract_title(result),
                    "year": _extract_year(result),
                    "doi": result.get("DOI"),
                    "publisher": result.get("publisher"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "title"}, indent=2))
            return 1
        else:
            parser.print_help()
            return 0
    except CrossrefUnavailable as e:
        print(json.dumps({"error": str(e), "status": "unreachable"}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
