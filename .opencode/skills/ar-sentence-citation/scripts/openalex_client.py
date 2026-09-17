#!/usr/bin/env python3
"""OpenAlex API client wrapper.

Implements:
- DOI-first lookup with title cross-check (Levenshtein similarity >= 0.70)
- Title search fallback with exact-title-or-bust gate (#431)
- Exponential backoff (2s -> 4s -> 8s) on burst HTTP 429
- Daily budget exhaustion fail-fast detection
- CLI invocation for terminal queries

Usage:
    python openalex_client.py --doi "10.1145/3375627.3375820" --title "Face Recognition"
    python openalex_client.py --title "Attention Is All You Need" --year 2017
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

_API_BASE = "https://api.openalex.org"
_API_HOST = "api.openalex.org"
_API_KEY_ENV = "OPENALEX_API_KEY"
_POLITE_EMAIL_ENV = "OPENALEX_POLITE_EMAIL"
_FIELDS = "id,title,authorships,publication_year,doi,primary_location"

_AUTHENTICATED_MIN_INTERVAL = 0.1
_ANONYMOUS_MIN_INTERVAL = 1.0


def _require_api_url(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != _API_HOST:
        redacted = urllib.parse.urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, "", "")
        )
        raise OpenAlexUnavailable(f"Refusing non-OpenAlex URL: {redacted}")


def _daily_budget_exhausted(headers: Any) -> bool:
    if headers is None:
        return False
    value = headers.get("X-RateLimit-Remaining")
    if value is None:
        return False
    try:
        return int(value) == 0
    except (ValueError, TypeError):
        return False


class OpenAlexUnavailable(Exception):
    """OpenAlex API degraded or unavailable."""


class OpenAlexClient:
    """Production lookup-by-(doi-with-cross-check-then-title) client for OpenAlex."""

    def __init__(
        self,
        polite_email: str | None = None,
        api_key: str | None = None,
    ):
        self._api_key = api_key or os.environ.get(_API_KEY_ENV)
        self._polite_email = polite_email or os.environ.get(_POLITE_EMAIL_ENV)
        self._min_interval = (
            _AUTHENTICATED_MIN_INTERVAL
            if (self._api_key or self._polite_email)
            else _ANONYMOUS_MIN_INTERVAL
        )
        self._last_request_at: float | None = None

    def _throttle(self) -> None:
        if self._last_request_at is None:
            return
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

    def _get(self, path: str, query: Mapping[str, str]) -> dict[str, Any]:
        params = dict(query)
        if self._api_key:
            params["api_key"] = self._api_key
        if self._polite_email:
            params["mailto"] = self._polite_email
        url = f"{_API_BASE}{path}?{urllib.parse.urlencode(params)}"
        _require_api_url(url)
        req = urllib.request.Request(
            url, headers={"User-Agent": "AcademicResearchSkill/1.0"}
        )

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
                        raise OpenAlexUnavailable(
                            f"OpenAlex response read/parse failed: {e}"
                        ) from e
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return {}
                if e.code == 429:
                    if _daily_budget_exhausted(e.headers):
                        raise OpenAlexUnavailable(
                            "OpenAlex daily budget exhausted (refills midnight UTC)"
                        ) from e
                    if attempt < _MAX_RETRIES:
                        time.sleep(_BACKOFF_SECONDS * (2 ** attempt))
                        self._last_request_at = time.monotonic()
                        continue
                raise OpenAlexUnavailable(f"OpenAlex HTTP {e.code}: {e.reason}") from e
            except (urllib.error.URLError, TimeoutError) as e:
                raise OpenAlexUnavailable(f"OpenAlex network error: {e}") from e

        raise OpenAlexUnavailable("OpenAlex rate limit exhausted after retries")

    def doi_lookup_with_title_check(
        self, doi: str, expected_title: str | None = None,
    ) -> dict[str, Any] | None:
        """DOI lookup with mandatory Levenshtein 0.70 title cross-check."""
        quoted_doi = urllib.parse.quote(doi, safe="")
        data = self._get(f"/works/doi:{quoted_doi}", {"select": _FIELDS})
        if not data:
            return None
        if not expected_title:
            return data
        title = data.get("title") or ""
        if _similarity(title, expected_title) >= _TITLE_SIMILARITY_THRESHOLD:
            return data
        return None  # DOI_MISMATCH

    def title_search(
        self, title: str, year: int | None = None,
    ) -> dict[str, Any] | None:
        """Title search under the exact-title-or-bust gate."""
        if generic_title(title):
            return None
        data = self._get(
            "/works",
            {"search": title, "per-page": "5", "select": _FIELDS},
        )
        candidates = data.get("results", [])
        scored = []
        for cand in candidates:
            cand_title = cand.get("title") or ""
            sim = _similarity(cand_title, title)
            if sim < _TITLE_SIMILARITY_THRESHOLD:
                continue
            if not exact_normalized_title(title, cand_title):
                continue
            year_match = year is not None and cand.get("publication_year") == year
            score = sim + (0.05 if year_match else 0.0)
            scored.append((cand, score))
        if not scored:
            return None
        scored.sort(key=lambda cand_score: (-cand_score[1],))
        return scored[0][0]


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenAlex API metadata query client.")
    parser.add_argument("--doi", help="DOI string to look up (e.g. 10.1145/3375627.3375820)")
    parser.add_argument("--title", help="Paper title to query or cross-check")
    parser.add_argument("--year", type=int, help="Publication year for tie-breaking")
    parser.add_argument("--api-key", help="OpenAlex API Key")
    parser.add_argument("--email", help="Polite email address")

    args = parser.parse_args()
    client = OpenAlexClient(polite_email=args.email, api_key=args.api_key)

    try:
        if args.doi:
            res = client.doi_lookup_with_title_check(args.doi, args.title)
            if res:
                output = {
                    "matched": True,
                    "queried_by": "doi",
                    "id": res.get("id"),
                    "title": res.get("title"),
                    "year": res.get("publication_year"),
                    "doi": res.get("doi"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "doi"}, indent=2))
            return 1
        elif args.title:
            res = client.title_search(args.title, args.year)
            if res:
                output = {
                    "matched": True,
                    "queried_by": "title",
                    "id": res.get("id"),
                    "title": res.get("title"),
                    "year": res.get("publication_year"),
                    "doi": res.get("doi"),
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
                return 0
            print(json.dumps({"matched": False, "queried_by": "title"}, indent=2))
            return 1
        else:
            parser.print_help()
            return 0
    except OpenAlexUnavailable as e:
        print(json.dumps({"error": str(e), "status": "unreachable"}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
