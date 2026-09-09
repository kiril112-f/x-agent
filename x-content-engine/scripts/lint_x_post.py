#!/usr/bin/env python3
"""Mechanical guardrails for final X drafts.

This is intentionally a linter, not a quality score or AI detector. It catches
project-specific hard patterns and flags claims that still need human/source QA.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BANNED_PHRASES = (
    "what nobody tells you is",
    "what nobody tells you",
    "the future isn't coming. it's already here",
    "the future isn’t coming. it’s already here",
    "let's dive in",
    "let’s dive in",
    "unlock the power",
    "in today's fast-paced world",
    "in today’s fast-paced world",
    "this changes everything",
    "this is huge",
    "read that again",
    "let that sink in",
    "follow for more",
    "like if you agree",
    "rt if you agree",
)

AI_SLOP_WORDS = (
    "delve",
    "game-changer",
    "game changer",
    "cutting-edge",
    "paradigm shift",
    "ever-evolving",
    "tapestry",
)

PATTERNS = (
    (
        "binary_contrast",
        "error",
        re.compile(r"\bit(?:'|’)s\s+not\b.{0,100}\bit(?:'|’)s\b", re.I | re.S),
        "Replace the canned 'It's not X. It's Y.' contrast with the actual claim.",
    ),
    (
        "faux_insight",
        "error",
        re.compile(
            r"\b(?:what most people get wrong|the part everyone misses|the uncomfortable truth is)\b",
            re.I,
        ),
        "State the evidence-backed point directly.",
    ),
    (
        "engagement_bait",
        "error",
        re.compile(r"\b(?:comment ['\"]?\w+['\"]? and i(?:'|’)ll dm|thoughts\?|agree\?)\s*$", re.I),
        "Use a real next action or end on the concrete point.",
    ),
    (
        "empty_transition",
        "error",
        re.compile(
            r"\b(?:"
            r"and that unlocks something completely new|"
            r"this opens up a whole new world|"
            r"the possibilities are endless|"
            r"this marks a new era|"
            r"this is where things get interesting|"
            r"and here(?:'|’)s why that matters"
            r")[!.]?",
            re.I,
        ),
        "Delete the importance-announcing transition and state the concrete consequence directly.",
    ),
)

HASHTAG_RE = re.compile(r"(?<!\w)#[A-Za-z][A-Za-z0-9_]*")
URL_RE = re.compile(r"https?://\S+", re.I)
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
NUMERIC_CLAIM_RE = re.compile(
    r"(?:[$€£]\s?\d[\d,.]*|\b\d+(?:[.,]\d+)?\s?(?:%|k|m|b|million|billion|followers?|users?|installs?|views?|mrr|arr)\b)",
    re.I,
)
EMOJI_RE = re.compile(
    "[\U0001F1E6-\U0001F1FF\U0001F300-\U0001FAFF\u2600-\u27BF]"
)
LIST_LINE_RE = re.compile(r"^(?:→|•|-|\*|\d+[.)])\s+")


def _issue(code: str, severity: str, message: str, match: str | None = None) -> dict[str, str]:
    item = {"code": code, "severity": severity, "message": message}
    if match:
        item["match"] = match
    return item


def lint_text(text: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    lower = normalized.lower()

    for phrase in BANNED_PHRASES:
        if phrase in lower:
            issues.append(
                _issue("banned_phrase", "error", "Remove the banned/canned phrase.", phrase)
            )

    for word in AI_SLOP_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lower):
            issues.append(
                _issue("ai_slop_word", "error", "Replace generic AI/marketing language with a concrete fact.", word)
            )

    for code, severity, pattern, message in PATTERNS:
        match = pattern.search(normalized)
        if match:
            issues.append(_issue(code, severity, message, match.group(0)[:160]))

    paragraphs = [part.strip() for part in re.split(r"\n[ \t]*\n", normalized) if part.strip()]
    if len(normalized) > 220 and len(paragraphs) == 1:
        issues.append(
            _issue(
                "missing_paragraph_breaks",
                "error",
                "Split multi-beat X copy into semantic paragraphs with one blank line between them.",
            )
        )

    if re.search(r"\n[ \t]*\n[ \t]*\n", normalized):
        issues.append(
            _issue(
                "excessive_blank_lines",
                "warning",
                "Use one empty line between paragraphs, not multiple empty lines.",
            )
        )

    if any(re.match(r"^[ \t]{2,}\S", line) for line in normalized.splitlines()):
        issues.append(
            _issue(
                "fake_indent",
                "warning",
                "Do not use leading spaces or tabs as visual indentation in X copy.",
            )
        )

    for paragraph in paragraphs:
        lines = [line.strip() for line in paragraph.split("\n") if line.strip()]
        for current, following in zip(lines, lines[1:]):
            if not LIST_LINE_RE.match(current) and not LIST_LINE_RE.match(following):
                issues.append(
                    _issue(
                        "arbitrary_hard_wrap",
                        "warning",
                        "Use a blank line at semantic boundaries; let X wrap sentences to viewport width.",
                        f"{current[:70]} / {following[:70]}",
                    )
                )
                break

    for paragraph in paragraphs:
        if len(paragraph) > 420 and "\n" not in paragraph:
            issues.append(
                _issue(
                    "dense_paragraph",
                    "warning",
                    "This paragraph is dense for mobile. Check whether it contains multiple semantic beats.",
                    paragraph[:160],
                )
            )

    hashtags = HASHTAG_RE.findall(normalized)
    if hashtags:
        issues.append(
            _issue("hashtag", "error", "Project voice uses no hashtags by default.", " ".join(hashtags))
        )

    if CYRILLIC_RE.search(normalized):
        issues.append(
            _issue("non_english_final", "error", "Final public copy must be English; translate remaining Cyrillic.")
        )

    numeric_claims = NUMERIC_CLAIM_RE.findall(normalized)
    if numeric_claims:
        issues.append(
            _issue(
                "verify_numeric_claim",
                "warning",
                "Verify each precise number against Kirill's proof ledger or a named primary source.",
                ", ".join(numeric_claims[:8]),
            )
        )

    urls = URL_RE.findall(normalized)
    if urls:
        issues.append(
            _issue(
                "primary_post_url",
                "warning",
                "Confirm that the URL belongs in the primary post rather than a first reply.",
                " ".join(urls[:3]),
            )
        )

    emoji_count = len(EMOJI_RE.findall(normalized))
    if emoji_count > 1:
        issues.append(
            _issue("emoji_count", "warning", "Voice normally uses zero or one contextual emoji.", str(emoji_count))
        )

    em_dash_count = normalized.count("—")
    if em_dash_count and len(normalized) < 1200:
        issues.append(
            _issue("em_dash", "warning", "Short X copy should not use em dashes as a rhythm crutch.", str(em_dash_count))
        )

    return issues


def read_input(path: str) -> str:
    if path == "-":
        import sys

        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a final X draft against project guardrails.")
    parser.add_argument("path", help="UTF-8 text/Markdown file, or - for stdin")
    args = parser.parse_args()
    text = read_input(args.path)
    issues = lint_text(text)
    payload = {
        "ok": not any(item["severity"] == "error" for item in issues),
        "errors": sum(item["severity"] == "error" for item in issues),
        "warnings": sum(item["severity"] == "warning" for item in issues),
        "issues": issues,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
