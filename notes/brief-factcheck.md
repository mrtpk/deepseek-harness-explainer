# Fact-check brief — NOT used as a separate subagent in this project

Light fact-check mode (plan.md §2, §11): the supervisor spot-checks each batch instead of running a
separate fact-checker subagent. This file is kept as the supervisor's own checklist for that spot-check —
read it before reviewing each batch, do not send it to a writer.

Spot-check focus per batch: the writer's "claims you are less sure of", every default/config value cited,
every "always"/"only when" claim, and 2-3 other claims picked at random. Open the cited lines yourself.

## Paths
- Explainer folder: /mnt/c/Users/tpesc/Downloads/test-harness/deepseek-harness-explainer (do not commit
  from a subagent — the supervisor commits).
- Target repo (READ ONLY): /mnt/c/Users/tpesc/Downloads/test-harness/deepseek-harness at
  ce7073d51254c26cd63b22a60835b8f948deb447.
- Sibling site: none.

## Read first
STYLE.md §6-7; skills/codebase-explainer/references/writing-and-accuracy.md; notes/facts.md ([FC]/[S] =
verified; [W] = not); notes/brief-writer.md §"Accuracy lessons" (the defect types found so far).

## For every claim
(prose, stop titles, tables, captions, alt text, diagram labels, visual rules and texts, quiz answers, glossary text):
1. Open the cited lines. Does the code say exactly this? Is the citation the narrowest correct range?
2. Check numbers, defaults (trace to where the value is finally set), types, shapes, call order, which
   process or thread runs it, conditions.
3. Claims with no citation: add a citation or remove the claim.
4. Derived claims: check step by step; reword ("can", "at the earliest") if the derivation has gaps.
5. General domain statements are correct.
6. Every recap link to the sibling site is true to that page.
7. Arithmetic in worked examples: recompute.
Fix defects in place in the batch's files only (pages, diagrams/<batch>_*.py, assets/viz/<visual>.js,
src/glossary/<batch>.json). Keep the writer's structure and the language rules. Run
`python3 build.py --preview` until the batch has 0 errors and no language warnings.

## No subagents
Do NOT start subagents or forks. The user allows <N> running agents; you are one of them. Do all the work yourself.

## Claims that the code has a bug
Do NOT put a "this looks like a bug" claim on a page. Re-read the control flow twice (indentation: is the
line inside or after the loop or if? the caller and the callee) and report it to the supervisor with exact
lines. Fact checkers can be wrong too.

## Report (final message only)
- Number of claims checked and defects fixed, by type (citation, value, logic, missing source, other).
- The most important corrections (one line each).
- Corrections for notes/facts.md: confirm or refute the writer's NEW FACTS with file:line.
- Other pages that may repeat a wrong claim (for the FINAL-PASS TODO list).
- Anything you could not decide.
