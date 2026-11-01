"""Diagram for learn/plugins-and-cordis.html: a plugin joining a Cordis context,
then two plugins cooperating through a typed event.

Used by: src/learn/plugins-and-cordis.html (<x-diagram name="b2_plugins_cordis" ... />)
Sources (at the pinned commit in explainer.json):
  packages/bundle/headless/src/index.ts:42   export const name = 'headless-runner'
  packages/bundle/headless/src/index.ts:45   export const inject = ['agentDefaultModel', 'agents', 'sessions']
  packages/bundle/headless/src/index.ts:456  export function apply(ctx: Context, config: Config)
  docs/architecture.md:57-65                 core package table: ctx.sessions, ctx.tools, ctx.agents, ctx.llm
  docs/cordis-primer.md:13                   registrations are reversible effects (ctx.effect() / ctx.on())
  packages/core/agent/src/index.ts:384       this.ctx.effect(() => {...}) inside setFactory()
  packages/core/tools/src/pipeline.ts:199-201  this.ctx.waterfall(carrier, 'tools/pre-execute', exec, ...)
  docs/cordis-primer.md:29-30                a waterfall listener must call next() to delegate
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "How does one plugin join dsh, and talk to another?",
    "A plugin claims a context, then cooperates through a typed event",
    params="1 context  ·  1 event  ·  canvas 1100",
)

# ---- Panel 1: a plugin joins the context ------------------------------------
y0 = 112
P1_H = 180
d.panel(y0, P1_H, 1, "How does a plugin join dsh?",
        "Cordis calls apply(ctx); the plugin registers effects on that context.")
bx_y, bw, bh = y0 + 72, 290, 84
d.box(46, bx_y, bw, bh, "headless-runner", [
    "name = 'headless-runner'",
    "bundle/headless/index.ts:42",
], col=BLUE)
d.arrow(46 + bw, bx_y + bh / 2, 400 - 2, bx_y + bh / 2, BLUE)
d.arrow_label(46 + bw + 32, bx_y + bh / 2, "apply(ctx)", BLUE)
d.box(400, bx_y, bw, bh, "Context (ctx)", [
    "ctx.sessions  ctx.tools",
    "ctx.agents  ctx.llm",
], col=AMBER)
d.arrow(400 + bw, bx_y + bh / 2, 754 - 2, bx_y + bh / 2, AMBER)
d.arrow_label(400 + bw + 32, bx_y + bh / 2, "ctx.effect() / ctx.on()", AMBER)
d.box(754, bx_y, bw, bh, "Reversible effect", [
    "unwinds on unload",
    "cordis-primer.md:13",
], col=VIOLET)
d.aside(46, bx_y + bh + 20, [
    "A plugin never imports another plugin directly; it only claims services by key, through ctx.",
])

# ---- Panel 2: two plugins cooperate through a typed event -------------------
y1 = y0 + P1_H + 24
P2_H = 220
d.panel(y1, P2_H, 2, "How do two plugins cooperate?",
        "One service dispatches a typed event; listeners run in registration order.")
by = y1 + 72
d.box(46, by, 310, 96, "ctx.tools (service)", [
    "pipeline.ts:199-201",
    "ctx.waterfall(name, exec, ...)",
], col=AMBER)
d.aside(46, by + 110, [
    "A waterfall listener must call next() to delegate, or return to decide the result.",
])

chip_x = 46 + 310 + 60
d.chip(chip_x, by + 4, 190, "tools/pre-execute", BLUE, h=22)
d.chip(chip_x, by + 34, 190, "waterfall · ordered", BLUE, h=22)
d.arrow(46 + 310 + 2, by + 48, chip_x - 4, by + 15, AMBER)
d.arrow(chip_x + 190 + 4, by + 15, 744 - 2, by + 48, BLUE)
d.arrow_label((chip_x + 190 + 744) / 2, by + 10, "ctx.on(name, listener)", BLUE)

d.box(744, by, 310, 96, "Listener plugin", [
    "registered with ctx.on()",
    "cordis-primer.md:29-30",
], col=VIOLET)

legend_y = y1 + P2_H + 24
d.legend(30, legend_y, [
    (BLUE, "plugin / event"),
    (AMBER, "context and services"),
    (VIOLET, "effect / listener"),
])
y = legend_y + 40
y = d.footnotes(30, y, [
    "Simplified: Cordis has 5 dispatch modes (emit, waterfall, parallel, serial, bail); only waterfall is shown.",
    "Every box cites its exact file:line in the diagram script's docstring.",
])
d.save(height=y + 14)
