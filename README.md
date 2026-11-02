# DeepSeek Harness Explained

A static website that teaches the [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
codebase step by step.
`dsh` is an AI coding-agent harness and runtime, shaped like Claude Code (sessions, a turn/step loop, a
tool pipeline, subagents, MCP, skills, a sandbox, an approval policy), built on an "everything-is-a-plugin"
framework called Cordis.

The site is for a reader who knows TypeScript and Node well, but knows little about Cordis or the
agent-harness domain (sessions, turns, tool pipelines, subagents, MCP, skills).

> **Status:** complete overview site, 18 pages. No page was deferred.
>
> This is an **overview**, not the skill's usual full two-depth study guide. Each page gives a short
> beginner start, then one compact "More detail" section — how the pieces fit together, what calls what,
> in what order, and the main config knobs. Reading the actual source is a low priority for this site;
> citations back every claim, but long code excerpts and line-by-line reading are mostly out of scope.
> See [`plan.md`](plan.md) section 15 for what a later, deeper pass would add.
>
> **Fact-check scope:** every page's writer opened and cited the code itself, but the check behind each
> batch was a **light, supervisor-only spot-check** of a sample of claims per batch — not a full,
> per-claim adversarial fact-check pass. See [`progress.md`](progress.md) for exactly what was checked,
> batch by batch, and plan.md section 15 for what a full fact-check pass would additionally need to cover.

## Code version

The site explains one exact version of deepseek-harness:

| | |
|---|---|
| Commit | [`ce7073d51254c26cd63b22a60835b8f948deb447`](https://github.com/deepseek-ai/deepseek-harness/tree/ce7073d51254c26cd63b22a60835b8f948deb447) |
| Date | 2026-10-30 |

All code excerpts and `file:line` links point to this commit. Line numbers can be different in newer
versions.

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
git checkout ce7073d51254c26cd63b22a60835b8f948deb447
```

## Read the site

Open `site/index.html` in a browser. The site works from disk (`file://`), with no server.
It needs an internet connection only for the Inter font and for code colours (Prism from cdnjs).
Without it, the site uses a system font and plain code.

| Part | Folder | What it contains |
|---|---|---|
| Learn the basics | `learn/` | Plugins and Cordis; profiles and bundles; turn/step/round/exchange vocabulary |
| Concepts | `concepts/` | 9 pages, grouped: core runtime, tools and extensibility, delegation and background work, execution and safety, protocols and clients |
| Guided tour | `tours/` | "Life of a headless task": `dsh --profile headless "task"` to stdout, 9 stops |
| Code map | `code/` | The full folder tree, and the ~18 files most central to the concepts above |
| Reference | `reference/` | Main env vars, config-file layering, CLI flags; the glossary |

Press `/` to search. Point to a dotted word to see its glossary definition. The one interactive visual
(a click-through tool-call pipeline stepper) is on `concepts/tools-and-mcp.html`.

## Build the site

Requirements: Python 3.11 or newer (standard library only), and a checkout of deepseek-harness at the
commit above, at the path `repo_path` in `explainer.json` (default: a folder next to this one).

```
parent/
  deepseek-harness/              # git checkout at ce7073d5 (read only)
  deepseek-harness-explainer/    # this repository
```

```bash
python3 tools/gen_folder_tree.py   # update the code-map folder tree
python3 build.py                   # build site/ from src/
python3 build.py --strict          # also stop on warnings
python3 build.py --preview         # write site/ even when a page has errors
python3 build.py --force-diagrams  # run all diagram scripts again
```

The build reads code excerpts directly from the checkout, so each excerpt is exact.
It stops with an error if the checkout is at a different commit, or if a link, a code citation or a
glossary term is wrong.

## Repository layout

| Path | Contents |
|---|---|
| `explainer.json` | Project name, target repo path and URL, pinned commit, language style |
| `src/` | Page sources, navigation (`src/nav/`) and glossary (`src/glossary/`) |
| `diagrams/` | One Python script for each SVG diagram, and the shared helper `svglib.py` |
| `assets/` | Site CSS and JavaScript, and the interactive visual (`assets/viz/`) |
| `tools/` | Generators for reference tables and the folder tree |
| `notes/brief-writer.md`, `notes/brief-factcheck.md` | The shared briefs given to every batch writer, and the supervisor's own spot-check checklist |
| `build.py` | The site generator |
| `site/` | The built site. Do not edit it |
| `STYLE.md`, `instructions-svg.md` | The writer's guide and the diagram style guide |
| `plan.md`, `progress.md` | The project plan and the full build log, batch by batch |

## How the content is made

- The pages are written in ASD-STE100 Simplified Technical English (short sentences, active voice, one
  instruction per sentence).
- Every claim about the code has a `file:line` citation at the pinned commit, opened by the page's own
  writer.
- After each batch of pages, the supervisor spot-checked a sample of its higher-risk claims (defaults,
  call order, "always" vs "only when") directly against the code. See `progress.md`'s batch-by-batch log
  for exactly what was checked and what, if anything, was found and fixed.
- Out of scope: `vendor/` (Cordis itself and its foundation libraries — explained only as the framework the
  product is built on), `native/` (the Landlock/flock launcher), `packages/experimental/*`, and the Swift
  and C++ files (one experimental macOS helper). The Python SDK gets one short paragraph only: it launches
  the compiled `dsh` binary over JSON-RPC-on-stdio and has no in-process harness logic of its own.

The pages were written with Claude Code and reviewed against the source code.
This site is not an official project of the DeepSeek Harness authors.
