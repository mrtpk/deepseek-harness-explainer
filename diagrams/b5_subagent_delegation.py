"""Diagram for concepts/subagents-and-delegation.html: how a parent picks a named
provider, and why some children keep a durable session while others run once.

Used by: src/concepts/subagents-and-delegation.html (<x-diagram name="b5_subagent_delegation" ... />)
Sources (at the pinned commit in explainer.json):
  packages/subagent/subagent/src/index.ts:271-286   SubagentRuntime.startActivation()
  packages/subagent/subagent/src/index.ts:600-607   expectProvider() looks the name up in the registry
  packages/subagent/subagent/src/types.ts:313-356   SubagentProvider: optional start() / prepareContinuable()
  packages/subagent/subagent-spawn-in-process/src/index.ts:50   prepareContinuable() -> local, durable
  packages/subagent/subagent-fork-in-process/src/index.ts:72    prepareContinuable() -> local, durable
  packages/subagent/subagent-claude-code/src/index.ts:73-116    start() only -> one-shot, external
  packages/subagent/subagent-claude-code/README.md:12            never falls back to the host `claude` executable
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, NEUTRAL, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "How does a parent delegate to a child, by name?",
    "ctx.subagents is a named-provider registry; providers differ in whether the child keeps a session",
    params="1 registry  ·  2 provider families  ·  canvas 1100",
)

# ---- Panel 1: naming a provider ---------------------------------------------
y0 = 112
P1_H = 150
d.panel(y0, P1_H, 1, "How does startActivation() pick a backend?",
        "The caller names a provider; the registry looks it up by that name.")
d.box(46, y0 + 60, 260, 68, "Parent Agent", [
    'subagents.startActivation(', '{ provider: "spawn" })',
], col=BLUE, mono_size=10.5)
d.arrow(306, y0 + 94, 404, y0 + 94, BLUE)
d.box(406, y0 + 60, 260, 68, "ctx.subagents", [
    "index.ts:271-286", "registry by name",
], col=AMBER)
d.arrow(666, y0 + 94, 764, y0 + 94, AMBER)
d.box(766, y0 + 60, 260, 68, "named provider", [
    "index.ts:600-607", 'e.g. "spawn", "claude-code"',
], col=VIOLET)

# ---- Panel 2: local vs external ---------------------------------------------
y1 = y0 + P1_H + 24
P2_H = 232
d.panel(y1, P2_H, 2, "Does the child keep a session, or run once?",
        "Method presence on the provider decides it (types.ts:340,355).")

lane_y = y1 + 44
lane_h = P2_H - 56
d.lane(46, lane_y, 500, lane_h, EMERALD, "Local: prepareContinuable()", [
    "spawn-in-process:50, fork-in-process:72",
])
d.box(66, lane_y + 78, 220, 60, "spawn", ["in-process, fresh"], col=EMERALD, mono_size=10.5)
d.box(306, lane_y + 78, 220, 60, "fork", ["in-process, seeded"], col=EMERALD, mono_size=10.5)
d.text(66, lane_y + lane_h - 14, "-> durable, resumable child session (can accept later messages)",
       11.5, EMERALD, mono=False)

d.lane(566, lane_y, 494, lane_h, VIOLET, "External: start() only", [
    "claude-code:73-116, codex, acp, dsh-sdk",
])
d.box(586, lane_y + 78, 220, 60, "claude-code", ["official Claude Agent SDK"], col=VIOLET, mono_size=10.5)
d.box(826, lane_y + 78, 220, 60, "codex / acp / dsh-sdk", ["each its own transport"], col=VIOLET, mono_size=10.5)
d.text(586, lane_y + lane_h - 14, "-> one execution; no follow-up input, no resume",
       11.5, VIOLET, mono=False)

y = y1 + P2_H + 24
y = d.legend(30, y, [
    (EMERALD, "local provider: durable child"),
    (VIOLET, "external provider: one-shot child"),
])
y += 30
y = d.footnotes(30, y, [
    'The Claude Code provider spawns the SDK\'s own platform-pinned CLI, under dsh\'s subprocess owner —',
    'never the host\'s installed "claude" executable (subagent-claude-code/src/run.ts:370-375, README.md:12).',
    "Simplified: capacity limits, depth caps, and tool-restriction policy are left out of this picture.",
])
d.save(height=y + 14)
