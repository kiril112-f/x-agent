#!/usr/bin/env python3

import contextlib
import io
import unittest

from apify_x_scrape import build_input, parse_args, resolve_token


class ApifyXScrapeTests(unittest.TestCase):
    def test_profile_defaults(self) -> None:
        args = parse_args(["--handles", "levelsio", "ErnestoSOFTWARE", "--max-items", "20"])
        payload = build_input(args)
        self.assertEqual(payload["mode"], "profileTweets")
        self.assertEqual(payload["twitterHandles"], ["levelsio", "ErnestoSOFTWARE"])
        self.assertEqual(payload["maxItems"], 20)
        self.assertEqual(payload["outputVariant"], "rich")

    def test_search_defaults(self) -> None:
        args = parse_args(["--search", "AI lang:en", "mobile app min_faves:50"])
        payload = build_input(args)
        self.assertEqual(payload["mode"], "search")
        self.assertEqual(payload["queryType"], "Latest + Top")
        self.assertTrue(payload["includeSearchTerms"])

    def test_hard_cap(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["--handles", "levelsio", "--max-items", "501"])

    def test_filters(self) -> None:
        args = parse_args(
            [
                "--search",
                "AI",
                "--min-likes",
                "50",
                "--min-replies",
                "5",
                "--min-retweets",
                "10",
            ]
        )
        payload = build_input(args)
        self.assertEqual(payload["min_faves"], 50)
        self.assertEqual(payload["min_replies"], 5)
        self.assertEqual(payload["min_retweets"], 10)

    def test_primary_token_is_preferred(self) -> None:
        token, source = resolve_token(
            {"APIFY_TOKEN": "primary", "APIFY_TOKEN_FALLBACK": "fallback"}
        )
        self.assertEqual(token, "primary")
        self.assertEqual(source, "APIFY_TOKEN")

    def test_fallback_token_is_used_when_primary_is_missing(self) -> None:
        token, source = resolve_token({"APIFY_TOKEN_FALLBACK": "fallback"})
        self.assertEqual(token, "fallback")
        self.assertEqual(source, "APIFY_TOKEN_FALLBACK")


if __name__ == "__main__":
    unittest.main()
