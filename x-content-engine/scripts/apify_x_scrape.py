#!/usr/bin/env python3
"""Run the project's Apify X scraper without storing API tokens in the repo.

The MCP server is the normal agent interface. This script is a deterministic
fallback for smoke tests, exports, and debugging. It reads APIFY_TOKEN, then
APIFY_TOKEN_FALLBACK when the primary is absent, and uses Apify's Authorization
header (never a token query string).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Mapping


ACTOR_ID = "xquik~x-tweet-scraper"
API_BASE = f"https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items"
DEFAULT_MAX_ITEMS = 50
HARD_MAX_ITEMS = 500
TOKEN_ENV_VARS = ("APIFY_TOKEN", "APIFY_TOKEN_FALLBACK")


def resolve_token(environment: Mapping[str, str]) -> tuple[str | None, str | None]:
    """Return the first configured token and its environment-variable name."""
    for name in TOKEN_ENV_VARS:
        token = environment.get(name)
        if token and token.strip():
            return token.strip(), name
    return None, None


def build_input(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "maxItems": args.max_items,
        "outputVariant": "rich",
        "fieldStyle": "camelCase",
        "outputPreset": "flat",
        "includeSearchTerms": True,
    }

    if args.handles:
        payload["mode"] = args.mode or "profileTweets"
        payload["twitterHandles"] = args.handles
        if args.max_items_per_target:
            payload["maxItemsPerTarget"] = args.max_items_per_target
    elif args.search:
        payload["mode"] = args.mode or "search"
        payload["searchTerms"] = args.search
        payload["queryType"] = args.sort
    elif args.urls:
        payload["startUrls"] = args.urls
        if args.mode:
            payload["mode"] = args.mode
    elif args.tweet_ids:
        payload["mode"] = args.mode or "tweets"
        payload["tweetIds"] = args.tweet_ids
    elif args.list_ids:
        payload["mode"] = args.mode or "listTweets"
        payload["listIds"] = args.list_ids

    if args.lang:
        payload["lang"] = args.lang
    if args.min_likes:
        payload["min_faves"] = args.min_likes
    if args.min_replies:
        payload["min_replies"] = args.min_replies
    if args.min_retweets:
        payload["min_retweets"] = args.min_retweets

    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Focused public X research through Apify/Xquik.")
    targets = parser.add_mutually_exclusive_group(required=True)
    targets.add_argument("--handles", nargs="+", help="X handles, with or without @")
    targets.add_argument("--search", nargs="+", help="X advanced-search queries")
    targets.add_argument("--urls", nargs="+", help="Tweet/profile/search/list URLs")
    targets.add_argument("--tweet-ids", nargs="+", help="Exact Tweet IDs")
    targets.add_argument("--list-ids", nargs="+", help="Exact X List IDs")
    parser.add_argument("--mode", help="Explicit Xquik mode; normally auto-selected")
    parser.add_argument("--max-items", type=int, default=DEFAULT_MAX_ITEMS)
    parser.add_argument("--max-items-per-target", type=int)
    parser.add_argument("--sort", choices=("Latest", "Top", "Latest + Top"), default="Latest + Top")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--min-likes", type=int, default=0)
    parser.add_argument("--min-replies", type=int, default=0)
    parser.add_argument("--min-retweets", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--output", type=Path, help="Write UTF-8 JSON instead of stdout")
    parser.add_argument("--dry-run", action="store_true", help="Print the Actor input without calling Apify")
    args = parser.parse_args(argv)

    if not 1 <= args.max_items <= HARD_MAX_ITEMS:
        parser.error(f"--max-items must be between 1 and {HARD_MAX_ITEMS}")
    if args.max_items_per_target is not None and args.max_items_per_target < 1:
        parser.error("--max-items-per-target must be positive")
    return args


def call_actor(payload: dict[str, Any], token: str, timeout: int) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode({"timeout": timeout, "maxItems": payload["maxItems"]})
    request = urllib.request.Request(
        f"{API_BASE}?{query}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout + 30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Apify returned HTTP {exc.code}: {body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Apify request failed: {exc.reason}") from exc

    if not isinstance(data, list):
        raise RuntimeError("Unexpected Apify response: expected a JSON array")
    return data


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = build_input(args)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    token, _token_source = resolve_token(os.environ)
    if not token:
        print(
            "Neither APIFY_TOKEN nor APIFY_TOKEN_FALLBACK is available in this process. "
            "Restart Codex after configuring them.",
            file=sys.stderr,
        )
        return 2

    try:
        rows = call_actor(payload, token, args.timeout)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    rendered = json.dumps(rows, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(json.dumps({"ok": True, "rows": len(rows), "output": str(args.output)}, ensure_ascii=False))
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
