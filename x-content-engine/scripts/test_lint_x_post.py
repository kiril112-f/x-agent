#!/usr/bin/env python3

import unittest

from lint_x_post import lint_text


def codes(text: str) -> set[str]:
    return {issue["code"] for issue in lint_text(text)}


class XPostLintTests(unittest.TestCase):
    def test_approved_voice_is_not_removed(self) -> None:
        text = "Let me tell you what shipped.\n\nGuess what: the Android build finally works, bro."
        self.assertNotIn("banned_phrase", codes(text))
        self.assertNotIn("faux_insight", codes(text))

    def test_banned_future_phrase(self) -> None:
        text = "The future isn't coming. It's already here."
        self.assertIn("banned_phrase", codes(text))

    def test_binary_contrast(self) -> None:
        text = "It's not the app. It's the distribution."
        self.assertIn("binary_contrast", codes(text))

    def test_numeric_claim_needs_verification(self) -> None:
        text = "We got 120,000 installs without spending a dollar on ads."
        self.assertIn("verify_numeric_claim", codes(text))

    def test_hashtags_are_errors(self) -> None:
        self.assertIn("hashtag", codes("Shipped the beta. #buildinpublic"))

    def test_final_cyrillic_is_error(self) -> None:
        self.assertIn("non_english_final", codes("We shipped сегодня."))

    def test_link_is_warning_not_error(self) -> None:
        result = lint_text("The full build log is here: https://example.com")
        issue = next(item for item in result if item["code"] == "primary_post_url")
        self.assertEqual(issue["severity"], "warning")

    def test_clean_direct_post(self) -> None:
        self.assertEqual(codes("I killed three features this week. The app got easier to explain."), set())

    def test_long_wall_of_text_is_error(self) -> None:
        text = (
            "I spent this week studying mobile app distribution because shipping the product is only half the job. "
            "A creator account can test hooks, formats, and objections every day. "
            "The comments then show which part of the offer still confuses people."
        )
        self.assertIn("missing_paragraph_breaks", codes(text))

    def test_semantic_paragraphs_pass(self) -> None:
        text = (
            "I spent this week studying mobile app distribution because shipping the product is only half the job.\n\n"
            "A creator account can test hooks, formats, and objections every day.\n\n"
            "The comments show which part of the offer still confuses people."
        )
        self.assertNotIn("missing_paragraph_breaks", codes(text))
        self.assertNotIn("arbitrary_hard_wrap", codes(text))

    def test_short_one_liner_needs_no_blank_line(self) -> None:
        self.assertNotIn("missing_paragraph_breaks", codes("Shipped the first Android build today."))

    def test_arrow_list_single_lines_are_allowed(self) -> None:
        text = "Every post improves the next:\n→ sharper hooks\n→ clearer objections\n→ repeatable formats"
        self.assertNotIn("arbitrary_hard_wrap", codes(text))

    def test_prose_hard_wrap_warns(self) -> None:
        text = "This sentence was manually wrapped\nwithout reaching a semantic boundary."
        self.assertIn("arbitrary_hard_wrap", codes(text))

    def test_multiple_empty_lines_warn(self) -> None:
        self.assertIn("excessive_blank_lines", codes("First beat.\n\n\nSecond beat."))

    def test_fake_indent_warns(self) -> None:
        self.assertIn("fake_indent", codes("First beat.\n\n  Second beat."))

    def test_empty_importance_transition_is_error(self) -> None:
        text = (
            "The model generates 15 seconds of video in 9 seconds.\n\n"
            "And that unlocks something completely new!\n\n"
            "A stream can render its next scene while viewers watch the current one."
        )
        self.assertIn("empty_transition", codes(text))

    def test_concrete_consequence_is_not_empty_transition(self) -> None:
        text = (
            "The model generates 15 seconds of video in 9 seconds.\n\n"
            "A stream can render its next scene while viewers watch the current one."
        )
        self.assertNotIn("empty_transition", codes(text))


if __name__ == "__main__":
    unittest.main()
