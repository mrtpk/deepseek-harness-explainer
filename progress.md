# DeepSeek Harness Explainer — Progress

Last update: 2026-11-01
Current phase: **1b Samples** — B1 done and committed; starting B2 (home, one basics page, the tour) next.

This file is the memory of the project. A new session must be able to continue from it alone.
Update it after every subagent finishes and after every user decision.

## Phase status

| Phase | Status | Notes |
|---|---|---|
| 0 Plan approval | done (scaled-down scope) | plan.md §2, §11 |
| 1 Foundation + samples | in progress | B1 (foundation) not started |
| Full build (plan §13) | not started | |
| F Final pass | not started | |

## Full build — batch status

| Batch | Writer | Spot-check | Committed |
|---|---|---|---|
| B1 Foundation | done | done (supervisor) | 5f08df8 |
| B2 Samples | in progress | – | – |
| B3 Remaining basics | – | – | – |
| B4 Core runtime + tools | – | – | – |
| B5 Delegation | – | – | – |
| B6 Execution & protocols | – | – | – |
| B7 Code map + reference | – | – | – |

## USER INSTRUCTIONS

- 2026-11-01: "No need to dive into the nitty gritty, but needs an overview." → single-depth pages,
  code-reading is low priority, cite code but do not require full code excerpts/deep dives.
- 2026-11-01: Fact-check mode: light (supervisor spot-check only), not a full fact-checker subagent.
- 2026-11-01: Structure: approved 16-page overview, but add quizzes and one interactive visual.
- 2026-11-01: Budget: 1 subagent at a time.

## RESUME NOTES

(none — work has not started)

## Done

Newest first.

- 2026-11-01: B1 foundation committed (5f08df8). Supervisor spot-checked every citation on
  concepts/agent-loop-and-session.html against the target repo directly; all correct. `build.py`: 0 errors,
  6 expected "coming soon" warnings. Playwright is not installed — no screenshot check done yet.
- 2026-11-01: DECISION: explainer.json filled (project, repo path/url/sha, TypeScript Prism components).
  Starter kit copied from the skill templates. Git initialized, author set repo-local
  (Thomas Paul <contact@thomaspaul.dev>).
- 2026-11-01: USER DECISION: scaled-down "overview" scope approved — see plan.md §2 and §11.
- 2026-10-30: Codebase survey done (subagent, template A). Commit pinned: ce7073d51254c26cd63b22a60835b8f948deb447.
  Confirmed: deepseek-harness is a TypeScript AI agent-harness runtime (~1.48M lines), built on the Cordis
  plugin framework. 58 package groups under packages/. See plan.md §3 for the full digest.

## Next step

Start B2 (Phase 1b samples): home page + system map, one basics page (`learn/plugins-and-cordis`), and the
tour (`tours/life-of-a-headless-task`). After B2, supervisor spot-check, then **stop point 2**: show the
user the sample pages before the rest of the site is written.

## Questions for the user

(none open)

## Issues log

(none yet)

## Subagent log

| Date | Task | Result |
|---|---|---|
| 2026-10-30 | Codebase survey (template A) | Reported in plan.md §3. No files changed (read-only). |
