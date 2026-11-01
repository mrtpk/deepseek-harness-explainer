"""Diagram for index.html: the home-page system map.

Used by: src/index.html (<x-diagram name="b2_home_system_map" ... />)
Sources (at the pinned commit in explainer.json):
  README.md:5-9                         dsh is an agent harness built on Cordis ("everything is a plugin")
  README.md:27                          dsh web serves the browser UI at http://127.0.0.1:3080
  docs/architecture.md:53                Desktop (Electron) loads the Web client's packaged assets
  apps/cli/src/bin.ts:26-42             runCli() parses argv, then boots a profile
  docs/architecture.md:17               a profile lists the bundles it stacks (web, headless, sdk, sdk-minimal, acp)
  docs/architecture.md:19,25            a bundle is a patchable distribution format; layers apply in order
  apps/cli/src/profile-boot.ts:224-236,313-323   composeProfile() stacks the layers, then boot() mounts them
  docs/architecture.md:57-65            core package table: session, tools, agent, agent-loop, llm
  docs/architecture.md:154              "Manage background jobs: register on ctx.jobs"
  docs/architecture.md:138              subagent providers vary behind one interface
  docs/subsystems/workflow.md:5         the workflow seam lets an agent run a script that starts subagents
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, TEAL, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "How does one dsh run come together?",
    "From the command you type to the parts that answer it",
    params="3 surfaces  ·  1 profile boot  ·  canvas 1100",
)

# ---- Panel 1: the three surfaces -------------------------------------------
y0 = 112
P1_H = 176
d.panel(y0, P1_H, 1, "How do you start dsh?",
        "Three surfaces; each one boots a named profile.")
bx_y, bw, bh = y0 + 72, 290, 78
d.box(46, bx_y, bw, bh, "CLI", [
    "apps/cli/src/bin.ts",
    "dsh --profile <name>",
], col=BLUE)
d.box(400, bx_y, bw, bh, "Web", [
    "packages/bundle/web-app",
    "http://127.0.0.1:3080",
], col=BLUE)
d.box(754, bx_y, bw, bh, "Desktop", [
    "apps/desktop (Electron)",
    "loads Web's own assets",
], col=BLUE)
d.aside(46, bx_y + bh + 20, [
    "Each surface hands a profile name to the same profile boot (Panel 2).",
])

# ---- Panel 2: profile and bundle boot --------------------------------------
y1 = y0 + P1_H + 24
P2_H = 176
d.panel(y1, P2_H, 2, "How does a profile become a running tree?",
        "A profile stacks bundle layers; boot() mounts the result.")
by = y1 + 72
d.box(46, by, bw, bh, "Profile", [
    "web · headless · sdk",
    "architecture.md:17",
], col=AMBER)
d.arrow(46 + bw, by + bh / 2, 400 - 2, by + bh / 2, AMBER)
d.arrow_label(46 + bw + 32, by + bh / 2, "stacks bundle layers", AMBER)
d.box(400, by, bw, bh, "Bundle layers", [
    "cordis.patch.yml stack",
    "architecture.md:19,25",
], col=AMBER)
d.arrow(400 + bw, by + bh / 2, 754 - 2, by + bh / 2, AMBER)
d.arrow_label(400 + bw + 32, by + bh / 2, "boot() mounts", AMBER)
d.box(754, by, bw, bh, "Mounted tree", [
    "profile-boot.ts:313-323",
    "one Cordis context",
], col=AMBER)

# ---- Panel 3: core runtime and delegation -----------------------------------
y2 = y1 + P2_H + 24
P3_H = 166
d.panel(y2, P3_H, 3, "What runs inside the mounted tree?",
        "The core runtime answers one step; it can delegate the rest.")
cy = y2 + 72
cw = 460
d.box(46, cy, cw, 86, "Core runtime", [
    "agent loop + session log",
    "tools + LLM adapter seam",
], col=TEAL)
d.arrow(46 + cw, cy + 43, 584 - 2, cy + 43, TEAL)
d.arrow_label((46 + cw + 584) / 2, cy + 43, "delegates background work", TEAL)
d.box(584, cy, cw, 86, "Delegation", [
    "subagents · jobs · workflow",
    "architecture.md:138,154",
], col=VIOLET)

legend_y = y2 + P3_H + 24
d.legend(30, legend_y, [
    (BLUE, "entry surface"),
    (AMBER, "profile / bundle boot"),
    (TEAL, "core runtime"),
    (VIOLET, "delegation"),
])
y = legend_y + 40
y = d.footnotes(30, y, [
    "Simplified: config patch overlays (--patch), HMR and the sandbox/approval layer are left out.",
    "Every box cites its exact file:line in the diagram script's docstring.",
])
d.save(height=y + 14)
