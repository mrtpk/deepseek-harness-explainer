# DeepSeek Harness Explainer — Progress

Last update: 2026-11-02
Current phase: **DONE.** B1-B7 and the final pass (F) are all committed. 18/18 planned pages, 0 build
errors/warnings, 0 site-check defects, README written. See "Done" below for the full log.

This file is the memory of the project. A new session must be able to continue from it alone.
Update it after every subagent finishes and after every user decision.

## Phase status

| Phase | Status | Notes |
|---|---|---|
| 0 Plan approval | done (scaled-down scope) | plan.md §2, §11 |
| 1 Foundation + samples | done | B1-B2 |
| Full build (plan §13) | done | B1-B7, all 18 pages |
| F Final pass | done | site check 0 defects, README written |

## Full build — batch status

| Batch | Writer | Spot-check | Committed |
|---|---|---|---|
| B1 Foundation | done | done (supervisor) | 5f08df8 |
| B2 Samples | done | done (supervisor, 2 defects fixed) | cf46355 |
| B3 Remaining basics | done | done (supervisor, 0 defects) | (see log) |
| B4 Core runtime + tools | done | done (supervisor, 0 defects) | ae83de5 |
| B5 Delegation | done | done (supervisor, 0 defects) | f7f3fab |
| B6 Execution & protocols | done | done (supervisor, 0 defects) | dbe8299 |
| B7 Code map + reference | done | done (supervisor, 0 defects) | c3db451 |

## USER INSTRUCTIONS

- 2026-11-01: "No need to dive into the nitty gritty, but needs an overview." → single-depth pages,
  code-reading is low priority, cite code but do not require full code excerpts/deep dives.
- 2026-11-01: Fact-check mode: light (supervisor spot-check only), not a full fact-checker subagent.
- 2026-11-01: Structure: approved 16-page overview, but add quizzes and one interactive visual.
- 2026-11-01: Budget: 1 subagent at a time.
- 2026-11-02: "build everything" → supersedes the per-batch approval gate below for the remaining batches
  (B6, B7, F). Run them straight through, 1 subagent at a time, spot-check and commit each, no stopping.
- 2026-11-01: "Now usage is at 54%, I plan to use only 10% for this work... do B by B. You dont have to
  worry about token usage, but get my approval before you start the new batch." → a usage ceiling (about
  10% of the user's weekly allowance for the rest of this build) applies, but the supervisor does not
  self-monitor against it — the user does. Stop and get explicit user approval before starting each
  remaining batch (B3 through F), one at a time. Do not chain batches automatically anymore.

## RESUME NOTES

(none — work has not started)

## Done

Newest first.

- 2026-11-02: README.md written (bf40286): states the overview scope (single-depth pages, not the skill's
  full two-depth pattern) and the light, supervisor-only spot-check fact-check scope plainly, per plan.md
  §9 Definition of done. Points to plan.md §15 for what a deeper pass would add later.
- 2026-11-02: Final site check (Phase F) done, 0 defects, no files changed: 18/18 pages at 1280/390px, 0
  overflow, 0 JS errors; 1025 internal links + 92 glossary-term links spidered, 0 broken; the
  tool-pipeline-stepper visual passed mouse and keyboard interaction; all 13 quiz blocks interactive; dark
  mode checked on 5 sampled pages (home, a basics page, a concept page, the tour, a reference page) with an
  automated WCAG contrast scan plus manual screenshot review, no readability or layout problems (diagram
  SVGs intentionally stay light-styled in both themes, as designed).
- 2026-11-02: plan.md corrected: the original survey's "shells out to the real Claude Code binary" claim
  was wrong (B5 traced the code). plan.md §3 now carries the correction inline.
- 2026-11-02: B7 code map + reference committed (c3db451): code/central-files (18 files, verified line
  counts), reference/config-and-env (env vars, CLI flags, links to learn/profiles-and-bundles for
  layering). All 18 planned pages now exist. Supervisor spot-checked 2 line counts (wc -l) and 6 env/CLI
  claims directly against the target repo: all correct, 0 defects. build.py --strict: 0 errors, 0
  warnings, 0 "coming soon" placeholders. Playwright 1280/390px: 0 overflow, 0 JS errors.
- 2026-11-02: B6 execution & protocols committed (dbe8299): concepts/sandbox-and-execution,
  concepts/approval-and-interaction, concepts/acp-sdk-and-clients. Both sandbox/approval pages link to the
  already-written subagents-and-delegation page instead of re-explaining the delegated-child override.
  Supervisor spot-checked 4 claims (sandbox mode-resolution precedence/default, fs-sandbox's
  trusted-code-not-kernel-boundary nature, approval request()'s turn-enclosure throw and 'never'
  short-circuit, the ACP/Python-SDK protocol descriptions): all correct, 0 defects. build.py --strict:
  0 errors, 0 warnings. Playwright 1280/390px: 0 overflow, 0 JS errors.
- 2026-11-02: B5 delegation committed (f7f3fab): concepts/subagents-and-delegation,
  concepts/jobs-workflow-goal-plan. Writer correction: the Claude Code subagent provider does not shell out
  to the host's installed `claude` binary — it calls the official Claude Agent SDK, which spawns its own
  platform-pinned CLI process (subagent-claude-code/README.md:12). Supervisor spot-checked 6 claims
  (maxDepth/maxActiveSubagents defaults, the Claude Code provider correction, jobs-local registry
  defaults, goal maxGoalRounds=256 and resume-throws, workflow-ptc concurrency formula, the toolFilter
  legacy-migration error): all correct, 0 defects. build.py --strict: 0 errors, 0 warnings. Playwright
  1280/390px: 0 overflow, 0 JS errors.
- 2026-11-02: B4 core runtime + tools committed (ae83de5): concepts/llm-and-system-prompt,
  concepts/tools-and-mcp (+ tool-pipeline-stepper interactive visual), concepts/skills, and a
  consistency/linking-only pass on concepts/agent-loop-and-session (no content defect in the Phase-1
  sample). Supervisor spot-checked 10 claims directly against the target repo: system-prompt assembly and
  commit order (agent.ts), agent/request provider/model immutability throw, PromptSection.complete
  restoration (system-prompt/index.ts), the full tool/call -> tools/pre-execute -> tools/execute ->
  tools/post-execute -> tool/result order and guard timing (batch.ts + pipeline.ts), MCP public tool name
  format (mcp-client/tools.ts), catalogDescriptionMaxLength default (tool-skill/index.ts), skill discovery
  ranks incl. bundled=600 (skill-filesystem/index.ts, skill/index.ts), LlmAdapter.stream as the only
  required method (llm/index.ts). All correct — 0 defects. build.py --strict: 0 errors, 0 warnings.
  Playwright 1280/390px on all 4 touched pages: 0 overflow, 0 JS errors; stepper visual click-through
  confirmed working (DOM updates on click, no console errors).
- 2026-11-01: B2 samples committed (cf46355): home, learn/plugins-and-cordis, tours/life-of-a-headless-task.
  Supervisor spot-checked a sample of citations directly against the target repo; found and fixed 2
  defects: (1) core.json "job" term cited the wrong line in docs/subsystems/jobs.md (9 -> 21); (2)
  explainer.json's prism_components listed prism-jsx/prism-tsx without prism-markup, which threw an
  uncaught TypeError on every page — removed (unused anyway; all cited excerpts are .ts). Ran a Playwright
  site check at 1280/390px on all 4 written pages after the fix: 0 overflow, 0 JS errors.
  STOP POINT 2 reached: waiting for user review before B3 starts.
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

None. The project is done: all 18 planned pages exist, cited, spot-checked, and committed; the final site
check found 0 defects; the README is written. If the user wants to go further, see plan.md §15 (the full
"Deep dive" depth is additive, not a rebuild).

## Questions for the user

(none open)

## Issues log

(none yet)

## Subagent log

| Date | Task | Result |
|---|---|---|
| 2026-10-30 | Codebase survey (template A) | Reported in plan.md §3. No files changed (read-only). |
