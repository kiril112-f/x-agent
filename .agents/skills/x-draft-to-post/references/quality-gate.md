# Quality gate

## Hard failures

- The output changes the user's thesis.
- It invents personal experience, numbers, quotes, opinions or results.
- A precise external claim lacks a source or honest uncertainty label.
- The hook overpromises the body.
- It uses a banned phrase from `brand-voice.md` or a close canned variant.
- It copies distinctive wording from a reference creator.
- It relies on another person's idea but omits attribution or adds no original contribution.
- It invents a scene, dialogue, sequence, relationship or causal result for storytelling.
- It inserts people/resources as name-dropping without helping the reader.
- A multi-beat post is one dense paragraph or loses blank-line separators in the final handoff.
- It uses tabs/leading spaces as indentation or manually wraps sentences at an arbitrary width.
- Two or more sentences repeat the same claim, implication or conclusion.
- It keeps background, use cases or speculative branches that do not change the main thesis.
- It uses an empty transition to announce importance instead of moving directly to the next fact or consequence.
- It exposes private material from `privacy-and-approval.md`.
- It performs or implies a publish action without approval.

## Score 0–2 on each

- Thesis fidelity.
- Factual support.
- Voice match.
- Specificity.
- X-native readability.
- Paragraph rhythm and whitespace preservation.
- Information density and absence of redundancy.
- Hook/payoff honesty.
- Human cadence / absence of generic AI prose.
- Context richness and responsible attribution.
- Proportional editing: the draft still feels like Kirill.

Target at least 19/22 with no hard failure. A score is an internal editing aid, not a user-facing claim of objective quality.

Run `python x-content-engine/scripts/lint_x_post.py <draft-file>` for mechanical checks when a final draft is stored in a file.
