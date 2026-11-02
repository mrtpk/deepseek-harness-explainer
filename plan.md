# DeepSeek Harness Explainer — Plan

Status: **APPROVED (scaled-down, overview scope) — 2026-11-01.**
Date: 2026-11-01
Source repo: `../deepseek-harness` at commit `ce7073d5` (https://github.com/deepseek-ai/deepseek-harness)

---

## 1. Goal

Make a static website that gives a beginner an OVERVIEW of how deepseek-harness (`dsh`) works.
The reader must come away able to explain how the pieces fit together and how a task flows
through the system. Reading the actual code line by line is a low priority for the reader.
This is a short site, not a full study guide.

## 2. Decisions (approved by the user, 2026-11-01)

| Topic | Decision |
|---|---|
| Reader | Knows TypeScript/Node. Does not know Cordis or this project's domain (agent harnesses). |
| Depth of detail | Single explanatory depth, not the skill's full two-depth pattern. Each page: short beginner start, a diagram, then a compact "More detail" section that explains mechanism and sequencing in prose. Every claim still cites `file:line`, but pages use short code excerpts only where one clarifies a point — no full file reads. Pages link to the repo's own `docs/subsystems/*.md` for readers who want to study the code itself. |
| Hosting | Local files for now (`file://`, double-click `site/index.html`). CDN libraries OK (cdnjs, Google Fonts). |
| Structure | Home + 3 basics pages + 9 concept pages (grouped by capability family, not one page per package) + 1 guided tour + 1 code-map page + 1 reference page. Not one page per file. |
| Location | `deepseek-harness-explainer/`, next to the `deepseek-harness` checkout. The target repo stays unchanged. |
| Site language | ASD-STE100 Simplified Technical English (`language_style: ste` in explainer.json). |
| Scope | Full pages for: core runtime (agent loop, session, tools, LLM seam), delegation (subagent, jobs, workflow, goal, plan), execution/safety (sandbox, shell/fs/terminal, approval), protocols/skills (MCP, skills, ACP, SDKs). Out of scope / interface-only mention: `vendor/` (Cordis + foundation libs — explained only as "the framework the plugins build on"), `native/` (Landlock/flock launcher), `packages/experimental/*` (one line each on the code-map page), Swift/C++ files. Python SDK gets one short paragraph (it only launches the compiled `dsh` binary; no in-process logic). |
| Name | "DeepSeek Harness Explained" |
| Look | Light article look (light always; dark only by toggle). Diagrams follow `instructions-svg.md` + STYLE.md §10. Diagrams only where they clarify architecture — expect about 5-7 total, not one per page. |
| Interactive visuals | One: a tool-execution-pipeline stepper (pre-execute → execute → post-execute) on the tools-and-mcp concept page. |
| Quizzes | A short "Check yourself" (`<x-quiz>`) at the end of each concept page and the tour. Not on reference/code-map pages. |
| Code version | Commit `ce7073d51254c26cd63b22a60835b8f948deb447` (2026-10-30, HEAD at survey time). Version line on every page, full SHA in the footer, home section `#code-version`. |
| Fact-check | Light: the supervisor spot-checks citations and the higher-risk claims (defaults, call order, "always" vs "only when") per batch. No separate fact-checker subagent. This is a deliberate scope cut from the skill default — logged here, and in the README as a check that was skipped. |
| Checkpoint | Stop after the foundation + first sample batch (home, one basics page, the tour). The user reviews look and depth before the rest is written. |
| Budget | 1 subagent at a time, sequential batches. Default model/effort. |
| Git | Commit per stage; push only when the user asks; author Thomas Paul <contact@thomaspaul.dev> (repo-local). |
| Sibling site | None. `dsh-superagent-prototype-explainer` exists as a folder but is empty — no basics to reuse. |

Add the date when a decision changes: "**Changed <date>:** ...".

## 3. Facts about the codebase (from the survey, 2026-10-30)

- Size: ~6,781 TypeScript/TSX files, ~1.48M lines (the product). Also ~80 Python files (thin client SDK,
  not core runtime), 52 Swift files (one experimental macOS helper, isolated), 4 C files (555 lines, a
  Landlock/flock native launcher), ~4,911 Markdown files (half are `.zh.md` Chinese doc mirrors).
- What it runs on: Node.js >=24.9, TypeScript, ESM, pnpm workspaces (AGENTS.md:84). `dsh web` serves a
  browser UI at `http://127.0.0.1:3080` (README.md:27). Desktop is Electron, reusing the Web client's
  assets unmodified (docs/architecture.md:51-53).
- It is an AI coding-agent harness/runtime shaped like Claude Code: sessions, turn/step loop, tool
  pipeline, subagents, MCP, skills, sandboxed shell/fs, approval policy, headless/CLI + Web/Desktop GUI.
  Built on an "everything-is-a-plugin" framework called Cordis (README.md:5-9, docs/architecture.md:9-11).
  It even ships a subagent provider for the Claude Code product: it calls the official Claude Agent SDK
  (not the host's installed `claude` binary — the package README says it "never falls back to the host
  `claude` executable", packages/subagent/subagent-claude-code/README.md:12) and an experimental Claude
  Code "mods" compatibility bridge (docs/subsystems/claude-code-mods.md). **Correction, 2026-11-02:** the
  original survey (below, unchanged for the record) said this provider "shells out to the real Claude Code
  binary" — the B5 writer traced the code and found that wrong; see concepts/subagents-and-delegation.html
  and progress.md's B5 log entry.
- History: 24,922 commits in under 5 months (HEAD 2026-10-30, first commit 2026-06-10). No submodules;
  Cordis and its foundation libs are vendored by source copy under `vendor/` (vendor/README.md:1-5).
- Good docs in the repo: `docs/architecture.md`, `AGENTS.md` (package one-liners), `packages/README.md`
  (package-group table), `docs/glossary.md` (domain terms), `docs/subsystems/*.md` (~70 files, one per
  subsystem, each with a generated "Cordis API" section), `docs/agent-lifecycle.md` (generated Mermaid
  sequence diagram of one turn), `docs/tool-execution-pipeline.md`, `docs/capability-seams.md`,
  `docs/module-graph.md` (more Mermaid diagrams), `docs/config-catalog.md`, `docs/tool-catalog.md`
  (generated reference catalogs). These are reused as "more detail" links, not duplicated.
- Comments in another language: code comments are English. Chinese appears only in parallel `.zh.md`
  doc mirrors and locale test fixtures, not in product source.

## 4. Site structure (16 pages + glossary)

```
deepseek-harness-explainer/
  index.html     Home: what dsh is, system map, "Start here", code version
  learn/         PART 1 — Basics (3 pages)
  concepts/      PART 2 — Concepts (9 pages, grouped by capability family)
  tours/         PART 3 — Guided tour (1)
  code/          PART 4 — Folder tree + central-files page
  reference/     PART 5 — Generated config/env table, glossary
```

### Part 1 — Learn the basics
1. `plugins-and-cordis`: everything-is-a-plugin; Cordis services, effects, events (docs/cordis-primer.md,
   vendor/cordis/)
2. `profiles-and-bundles`: how a running `dsh` tree is assembled from a profile + stacked bundle/patch
   layers (docs/architecture.md:13-47, packages/boot/app-boot, packages/bundle/*)
3. `session-and-loop-vocabulary`: turn / step / round, the session event log, an exchange
   (docs/glossary.md, docs/architecture.md:79-118)

### Part 2 — Concepts
- **Core runtime:** `agent-loop-and-session` (AgentRegistry, ReactLoopAgent, Session log) ·
  `llm-and-system-prompt` (ctx.llm adapter seam, provider adapters, prompt assembly)
- **Tools & extensibility:** `tools-and-mcp` (tool registry/pipeline + MCP external servers; the one
  interactive visual) · `skills` (skill catalog/loader)
- **Delegation & background work:** `subagents-and-delegation` (subagent manager, the Claude Code
  subagent provider) · `jobs-workflow-goal-plan` (background jobs, the workflow/PTC engine, goals, plan
  mode)
- **Execution & safety:** `sandbox-and-execution` (sandbox seam, shell/fs/terminal capability families) ·
  `approval-and-interaction` (human-in-the-loop approval policy)
- **Protocols & clients:** `acp-sdk-and-clients` (ACP server, Node/Python SDKs, how Web/Desktop connect)

### Part 3 — Guided tour
1. **Life of a headless task** — `dsh --profile headless "task"` to stdout (9 stops, from the survey §3:
   bin.ts → profile-boot.ts → headless bundle → agent creation → turn/step loop → tool execution →
   idle/subagent wait → session flush → stdout)

### Part 4 — Code map
- Folder tree (`tools/gen_folder_tree.py`) covering the whole repo, including one-line mentions of
  out-of-scope folders (`vendor/`, `native/`, `packages/experimental/*`).
- One page listing the ~18 central files from the survey §6, each with a one-line role and a link to its
  concept page.

### Part 5 — Reference
- One generated page: the main env vars, config-file layering (`cordis.yml` + `cordis.patch.yml`), and
  CLI flags from `apps/cli/src/args.ts`, with a pointer to the repo's own `docs/config-catalog.md` and
  `docs/tool-catalog.md` for the full generated tables (not duplicated here).
- Glossary (generated by build.py; seeded from `docs/glossary.md`).

## 5. Page design

Templates: STYLE.md §4, adapted for single-depth pages (see Decisions above — "More detail" replaces the
full "Deep dive" pattern; keep the `<x-deepdive>` tag available for the rare page that needs it).

### Interactive visual (1)
- `tool-pipeline-stepper`: the reader steps through `tools/pre-execute → tools/execute → tools/post-execute`
  for one tool call, seen on the `tools-and-mcp` concept page.

## 6. Technology

Static HTML, `build.py` (standard library only), `explainer.json` for project values, SVG diagrams from
Python scripts with `svglib.py`, Prism (incl. `prism-typescript`) from cdnjs, Inter from Google Fonts.
Output `site/` opens from disk.

## 7. Writing rules

See STYLE.md §6-7, as adapted for single-depth pages. Every claim about the code cites `file:line` at
`ce7073d5`. No full-file code reading — short excerpts only where they clarify a specific point.

## 8. How the supervisor works

Supervisor + 1 subagent at a time. Writer → supervisor spot-check (light; see Decisions) → commit per
batch. `progress.md` is updated after every event. The target repo is never changed. No push without a
user request. Open questions go to `progress.md` "Questions for the user".

## 9. Definition of done

- All 16 planned pages exist (or are deferred by the user) and `python3 build.py` has 0 errors.
- Every concept page and the tour has a diagram, at least one short code excerpt, a "More detail" section
  and a "Check yourself" quiz.
- Every batch has a supervisor spot-check logged in `notes/facts.md`. The FINAL-PASS TODO list is empty.
- Site check at 1280 and 390 px: no overflow, no JS errors, no broken links; the one visual works.
- A beginner can follow Home → Basics → the tour with no dead end.
- README states plainly that fact-checking was a light, supervisor-only spot-check, not a full
  per-claim adversarial pass.

## 10. Risks

| Risk | What we do |
|---|---|
| Wrong explanations slip through (lighter fact-check) | Spot-check the higher-risk claims every batch (defaults, call order, "always" vs "only when"); writer still opens every cited line itself; the gap is disclosed in the README |
| Pages differ in style | One template, STYLE.md, Phase 1 samples given to every writer |
| Out-of-scope code | Explain the interface only, and say so on the page |
| 20k-file repo is too big to survey exhaustively | Scope is fixed to the ~18 central files and ~21 concepts from the survey; everything else gets at most a code-map mention |

## 11. Answers from the user (2026-11-01)

1. Target: `./deepseek-harness`, output to `deepseek-harness-explainer/`. Overview only, no nitty-gritty.
2. Depth: understand how it works; cite code; reading the code itself is low priority → single-depth pages.
3. Fact-check: light (supervisor spot-check), not a full fact-checker subagent.
4. Structure: approved 16-page overview scope, but add quizzes and one interactive visual.
5. Budget: 1 subagent at a time.

## 12. Phase 1 in detail (the review package)

| Step | Work | Who |
|---|---|---|
| 1a | Tooling, STYLE.md (adapted for single-depth), nav files with all 16 planned pages, core glossary (~25 terms from docs/glossary.md), one sample concept page (`agent-loop-and-session`) with every tag in use | 1 subagent |
| 1b | Samples, one at a time: home page + system map; one basics page (`plugins-and-cordis`); the tour (`life-of-a-headless-task`) | 3 subagents, sequential |
| 1c | Supervisor spot-check of the sample pages; a quick site check | supervisor |
| 1d | **Stop. Show the user the sample pages.** | supervisor |

## 13. Full build (after user approval)

Pipeline per batch: writer → `build.py` 0 errors → supervisor spot-check (light) → commit.

| Batch | Pages | Interactive visual |
|---|---|---|
| B1 Foundation | STYLE.md, nav, core glossary, 1 sample concept page | – |
| B2 Samples | home, `plugins-and-cordis`, tour `life-of-a-headless-task` | – |
| B3 Remaining basics | `profiles-and-bundles`, `session-and-loop-vocabulary` | – |
| B4 Core runtime + tools | `agent-loop-and-session` (full), `llm-and-system-prompt`, `tools-and-mcp`, `skills` | tool-pipeline-stepper |
| B5 Delegation | `subagents-and-delegation`, `jobs-workflow-goal-plan` | – |
| B6 Execution & protocols | `sandbox-and-execution`, `approval-and-interaction`, `acp-sdk-and-clients` | – |
| B7 Code map + reference | folder tree, central-files page, reference page | – |

Waves: all sequential (budget = 1 at a time). Order: B1 → B2 → **stop point 2** → B3 → B4 → B5 → B6 → B7 → F.

## 14. Deferred pages

(none)

## 15. Future work: adding the skill's full "Deep dive" depth

Not planned now. The user asked for an overview (§2 Depth of detail); this is a note for later, if the
user wants to go deeper after the overview site is done.

**Feasible, additive, no rebuild needed.** The page template and the `<x-deepdive>` tag the skill normally
uses for full depth already exist in the starter kit; this project just isn't using them except for one
tricky nuance per page. Adding full depth later means expanding each page's "More detail" section, not
rewriting it.

**What a full deep dive adds, per page:**
- Exact types and shapes: interfaces, config schemas, event payloads (not just that a field exists).
- Every edge case and condition, traced through every call site (not one flagged nuance).
- Env vars and CLI flags relevant to that concept, beyond the site-wide reference page.
- A worked example with real numbers (for example an actual session-log trace or tool-call batch).
- Line-by-line reading of the key functions, with longer `<x-code>` excerpts.

**What the current overview site's reader misses, as a result:** exact edge cases and full call-order
guarantees (claims are written conservatively, "only when ...", not exhaustively proven); exact types and
schema shapes; line-by-line code reading; worked numeric examples; most env vars/flags per individual
concept (only the main ones are on the site-wide reference page); and the rigor of a dedicated adversarial
fact-check (this build uses a supervisor spot-check, §2 Fact-check — disclosed in the README).

**Cost if done later:** one batch per 3-4 concept pages (the 9 concept pages + the tour = about 3 batches),
each a writer pass to expand "More detail" into a full deep dive, then a **full** fact-check of the new
material (not the light spot-check this build used — deep-dive claims are exactly what needs adversarial
checking: defaults, edge cases, call order). The code-map and reference pages would not need this; they
are already reference-style.
