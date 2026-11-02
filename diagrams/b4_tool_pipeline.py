"""Diagram for concepts/tools-and-mcp.html: where tool definitions come from, and the
fixed pipeline order one tool call runs through.

Used by: src/concepts/tools-and-mcp.html (<x-diagram name="b4_tool_pipeline" ... />)
Sources (at the pinned commit in explainer.json):
  packages/core/tools/src/index.ts:128      ToolsService.register() (first-party plugins)
  packages/mcp/mcp-client/src/tools.ts:150  ctx.tools.register(definition) (one per MCP server)
  packages/mcp/mcp-client/src/tools.ts:82   publicToolName(): "mcp__<serverName>__<rawName>"
  docs/architecture.md:99                   tool/call* -> tools/pre-execute -> tools/execute
                                             -> tools/post-execute -> tool/result*
  packages/core/tools/src/batch.ts:157      settlement.start() appends 'tool/call'
  packages/core/tools/src/pipeline.ts:200   prepare() runs the 'tools/pre-execute' waterfall
  packages/core/tools/src/pipeline.ts:300   dispatch() runs the 'tools/execute' waterfall
  packages/core/tools/src/pipeline.ts:488   postExecute() runs the 'tools/post-execute' waterfall
  packages/core/tools/src/batch.ts:146,256  settlement.commit() appends 'tool/result'
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, NEUTRAL, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "Where do tool definitions come from, and what order do calls run in?",
    "Two registration sources feed one registry; every call runs the same three-stage pipeline",
    params="1 registry  ·  3 live stages  ·  canvas 1100",
)

# ---- Panel 1: registration sources -----------------------------------------
y0 = 112
P1_H = 168
d.panel(y0, P1_H, 1, "Who registers a tool?",
        "A first-party plugin and an MCP client both call ctx.tools.register().")
bx_y, bw, bh = y0 + 66, 300, 84
d.box(46, bx_y, bw, bh, "First-party tool plugin", [
    "core/tools/src/index.ts:128",
    'name: "bash", "read", ...',
], col=BLUE)
d.box(46, bx_y + bh + 14, bw, 44, "MCP client (per server)", [
    "mcp-client/src/tools.ts:150,82",
], col=VIOLET)
d.arrow(46 + bw, bx_y + bh / 2, 460 - 2, y0 + 110, BLUE)
d.arrow(46 + bw, bx_y + bh + 14 + 22, 460 - 2, y0 + 128, VIOLET)
d.box(460, y0 + 70, 300, 80, "ctx.tools (ToolsService)", [
    "core/tools/src/index.ts:99",
    "the tool registry",
], col=AMBER)
d.aside(800, y0 + 78, [
    'MCP tools get a namespaced',
    'name: mcp__<server>__<tool>.',
])

# ---- Panel 2: the pipeline --------------------------------------------------
y1 = y0 + P1_H + 24
P2_H = 196
d.panel(y1, P2_H, 2, "What order does one call run in?",
        "The same fixed order for every call (docs/architecture.md:99).")
chips = [
    ("tool/call", NEUTRAL, "batch.ts:157", True),
    ("tools/pre-execute", BLUE, "pipeline.ts:200", False),
    ("tools/execute", AMBER, "pipeline.ts:300", False),
    ("tools/post-execute", EMERALD, "pipeline.ts:488", False),
    ("tool/result", NEUTRAL, "batch.ts:146", True),
]
cw = 190
gap = (1040 - 46 - len(chips) * cw) / (len(chips) - 1)
cy = y1 + 76
for i, (label, col, src, _durable) in enumerate(chips):
    cx = 46 + i * (cw + gap)
    d.chip(cx, cy, cw, label, col, h=36)
    d.text(cx + cw / 2, cy + 54, src, 11, col, anchor="middle", mono=True)
    if i < len(chips) - 1:
        d.arrow(cx + cw + 2, cy + 18, cx + cw + gap - 2, cy + 18, BLUE)
d.aside(46, cy + 76, [
    "tool/call and tool/result (singular) are durable session events logged before and after the pipeline.",
    "tools/pre-execute, tools/execute and tools/post-execute (plural) are live waterfalls: plugins join any of the three.",
])

y = y1 + P2_H + 24
y = d.legend(30, y, [
    (NEUTRAL, "durable session event"),
    (BLUE, "pre-execute: allow / deny / ask"),
    (AMBER, "execute: run the tool body"),
    (EMERALD, "post-execute: accept / block"),
])
y += 30
y = d.footnotes(30, y, [
    "Simplified: approval prompts, guards, and parallel-call scheduling are left out (see the interactive visual below).",
    "Every box, chip and arrow above cites the exact file:line in the diagram script's docstring.",
])
d.save(height=y + 14)
