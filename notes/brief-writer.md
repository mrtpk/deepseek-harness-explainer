# Writer brief (shared by every batch writer of "DeepSeek Harness Explained")

The supervisor's prompt gives you: the batch name, your pages and their scope, the visual (if any), and the
glossary terms you own. This file gives everything else. It is binding.

## This is an OVERVIEW site, not a full study guide
The user asked for an overview, not the nitty-gritty. Single depth, not the skill's usual two-depth
pattern:
- A short beginner start (one sentence, the idea, a diagram).
- Then one compact "More detail" section in prose: how the pieces fit together, what calls what, in what
  order, and the config knobs that change the behaviour. This replaces the skill's full "Deep dive".
- Reading the actual code is a LOW priority for the reader. Do not paste long code excerpts or do a
  line-by-line reading. A short `<x-code>` excerpt is fine when one line or a few lines make the point,
  but prefer saying what the code does in prose, with a `{{cite}}` to back it up.
- Where the repo's own docs go deeper (`docs/subsystems/<name>.md` has a generated "Cordis API" section
  for most subsystems), end the page with a one-line pointer to that doc instead of duplicating it.
- Still: every claim about the code needs a citation. You open the cited lines yourself; "the docs say so"
  is not enough — the docs can be stale.

## Paths
- Explainer folder: /mnt/c/Users/tpesc/Downloads/test-harness/deepseek-harness-explainer (git repo; do not
  commit: the supervisor commits).
- Target repo (READ ONLY, pinned): /mnt/c/Users/tpesc/Downloads/test-harness/deepseek-harness at
  ce7073d51254c26cd63b22a60835b8f948deb447. Never change it.
- Sibling site: none (dsh-superagent-prototype-explainer exists but is empty — nothing to recap).

## Read first, in this order
1. STYLE.md (all of it).
2. plan.md §1-4 (goal, decisions, codebase facts, site structure) and the batch table (plan.md §13; find
   your batch).
3. instructions-svg.md (STYLE.md §10 overrides it: canvas 1100, min text 11).
4. notes/facts.md: [FC] and [S] entries are verified; [W] entries are not. Still open the code and cite it
   yourself.
5. The model page of your page type, once it exists (finished): concepts/agent-loop-and-session.html is
   the reference sample for concept pages; later batches also copy the Phase 1b samples (home, a basics
   page, the tour).
6. ../mrtpk-agent-skills/skills/codebase-explainer/references/writing-and-accuracy.md and page-templates.md.

## Content rules
- Reader: knows TypeScript/Node well. Does not know Cordis (the plugin framework this project is built
  on) or the agent-harness domain (sessions, turns, tool pipelines, subagents, MCP). Do not assume they
  know Claude Code either, though a one-line analogy to it can help on the home page only.
- Every claim about the code: `{{cite path:line}}` or `<x-code>`. Open every cited line yourself. Narrowest
  range. No guesses — if the code does not answer a question, write it on the page as an open question and
  list it in your report.
- Scope: full pages for core runtime, delegation (subagent/jobs/workflow/goal/plan), execution & safety
  (sandbox/shell/fs/terminal/approval), protocols & skills (MCP/skills/ACP/SDKs). Out of scope, mention
  only as "the framework the plugins build on" or a one-liner on the code-map page: `vendor/` (Cordis +
  foundation libs), `native/` (Landlock/flock launcher), `packages/experimental/*`, Swift/C++ files. The
  Python SDK gets one short paragraph: it only launches the compiled `dsh` binary over JSON-RPC-on-stdio;
  it has no in-process harness logic (python/README.md:5-9).
- No sibling site, so no recap links.
- `<x-simplified>` for simplifications. Site text in ASD-STE100 Simplified Technical English (short
  sentences, active voice, one instruction per sentence). Captions start with "Figure: ".
- Add a `<x-quiz>` "Check yourself" block at the end of every concept page and the tour (2-4 questions).
  Not on the code-map or reference pages.
- Diagrams: one script per diagram, Diagram(width=1100), max 3 boxes across, max 3 panels, no text below
  11. Prefix = your batch (diagrams/<batch>_*.py). Keep the total diagram count low (plan.md target:
  5-7 for the whole site) — only add one where a picture genuinely clarifies the architecture.
- Literal tag syntax that is text (`{{cite}}`, `<x-code>`) must be escaped (`&#123;&#123;cite&#125;&#125;`).

## Accuracy lessons
(The supervisor adds each repeated defect type from the fact checks here, with the trap and the correct
place in the code. Start with these.)
1. DEFAULTS: trace each default to where it is finally set (argument parsing, post-init hooks, platform
   code). Do not cite only a config class field.
2. CONDITIONS: write "only when ..." where the code has a condition. No "always", "every", "all" unless you
   checked every path.
3. LINE RANGES: off-by-one is the most common defect. Open each cited range again after you finish the page.
4. COUNTS AND ORDER: "runs N times" or "before X" needs a check of every call site.
5. DOCS: docs are often older than the code. Cite the code. Report each docs-vs-code difference (FAQ material).

## Ownership (parallel work)
- You own only: your page files, src/glossary/<batch>.json, diagrams/<batch>_*.py, and your visual
  assets/viz/<name>.js (shared visual styles only appended to assets/viz/viz.css).
- Search src/glossary/*.json before you add a term. Do not redefine; reuse with {{term id}}.
- Do NOT edit: build.py, assets/site.css, assets/site.js, nav files, other glossary files, notes/*,
  STYLE.md, plan.md, progress.md, other pages.
- Use `python3 build.py --preview` when another page is broken. Your pages must have 0 errors and no
  template or language warnings.

## No subagents
Do NOT start subagents or forks. The user allows 1 running agent at a time; you are it. Do all the work yourself.

## Claims that the code has a bug
Do NOT put a "this looks like a bug" claim on a page. Re-read the control flow twice (is the line inside or
after the loop or if? check the caller and the callee) and report it to the supervisor with exact lines.

## Report (final message only, no report files)
1. Pages written, diagrams, visual, glossary ids added.
2. Build result (errors and warnings for your pages).
3. NEW FACTS for notes/facts.md (each with file:line).
4. FACTS IN facts.md THAT ARE WRONG (with proof).
5. Claims you are less sure of (for the fact checker to check hard).
6. Open questions, docs-vs-code differences, cross-page problems.
