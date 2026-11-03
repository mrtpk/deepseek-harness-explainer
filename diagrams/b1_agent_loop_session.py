"""Diagram for concepts/agent-loop-and-session.html: how AgentRegistry, the turn/step
loop and the Session log relate.

Used by: src/concepts/agent-loop-and-session.html (<x-diagram name="b1_agent_loop_session" ... />)
Sources (at the pinned commit in explainer.json):
  packages/core/agent/src/index.ts:252       class AgentRegistry extends Service
  packages/core/agent/src/index.ts:416       AgentRegistry.create() delegates to the registered factory
  packages/core/agent-loop/src/index.ts:291  class AgentLoop extends Service implements AgentFactory
  packages/core/agent-loop/src/index.ts:717  AgentLoop.createAgent()
  packages/core/agent-loop/src/index.ts:573  new ReactLoopAgent(...) inside initializeAgent()
  packages/core/agent-loop/src/agent.ts:112  class ReactLoopAgent implements Agent
  packages/core/agent-loop/src/agent.ts:327  private async turn(): one turn, a while(true) loop of steps
  packages/core/agent-loop/src/agent.ts:336  this.session.append('turn/start', ...)
  packages/core/agent-loop/src/agent.ts:361  this.session.append('step/start', ...)
  packages/core/agent-loop/src/agent.ts:388  this.session.append('step/end', ...)
  packages/core/agent-loop/src/agent.ts:422  this.session.append('turn/end', ...)
  packages/core/session/src/index.ts:526     private log: SessionEvent[] = []
  packages/core/session/src/index.ts:829     seq: SessionSeq(this.log.length)
  packages/core/session/src/index.ts:901     this.log.push(event) inside commit()
  packages/core/agent-loop/src/agent.ts:348-358  zero-step exits (blocked, empty first claim)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, INK, MUTE, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "Who creates an Agent, and where does its work go?",
    "AgentRegistry, the agent-loop factory, and the append-only session log",
    params="1 agent  ·  1 session  ·  canvas 1100",
)

# ---- Panel 1: creation -----------------------------------------------------
y0 = 112
P1_H = 180
d.panel(y0, P1_H, 1, "Who creates the live Agent?",
        "AgentRegistry delegates creation to the factory the agent-loop registers.")
bx_y, bw, bh = y0 + 72, 290, 84
d.box(46, bx_y, bw, bh, "AgentRegistry", [
    "core/agent/src/index.ts:252",
    "create(options)",
], col=BLUE)
d.arrow(46 + bw, bx_y + bh / 2, 400 - 2, bx_y + bh / 2, BLUE)
d.arrow_label(46 + bw + 32, bx_y + bh / 2, "delegates to", BLUE)
d.box(400, bx_y, bw, bh, "AgentLoop (factory)", [
    "agent-loop/src/index.ts:291",
    "createAgent()",
], col=AMBER)
d.arrow(400 + bw, bx_y + bh / 2, 754 - 2, bx_y + bh / 2, AMBER)
d.arrow_label(400 + bw + 32, bx_y + bh / 2, "new ReactLoopAgent()", AMBER)
d.box(754, bx_y, bw, bh, "ReactLoopAgent", [
    "agent-loop/src/agent.ts:112",
    "implements Agent",
], col=VIOLET)
d.aside(46, bx_y + bh + 20, [
    "AgentLoop makes one ReactLoopAgent per session (agent-loop/src/index.ts:573).",
])

# ---- Panel 2: the turn/step loop writes the session log --------------------
y1 = y0 + P1_H + 24
P2_H = 232
d.panel(y1, P2_H, 2, "What does the Agent do with one turn?",
        "The loop appends each turn and step boundary to the session log as it runs.")
by = y1 + 72
d.box(46, by, 330, 96, "ReactLoopAgent.turn()", [
    "agent-loop/src/agent.ts:327",
    "while (true) { step() }",
], col=AMBER)
d.aside(46, by + 110, [
    "One turn runs zero or more steps.",
    "Each step is one model call plus its tool calls.",
])

chip_x = 46 + 330 + 70
events = [
    ("turn/start", BLUE, "agent.ts:336"),
    ("step/start", BLUE, "agent.ts:361"),
    ("step/end", BLUE, "agent.ts:388"),
    ("turn/end", BLUE, "agent.ts:422"),
]
chip_y0 = by + 4
for i, (label, col, _src) in enumerate(events):
    cy = chip_y0 + i * 24
    d.chip(chip_x, cy, 118, label, col, h=20)
d.arrow(46 + 330 + 2, by + 48, chip_x - 4, chip_y0 + 38, AMBER)
d.arrow(chip_x + 118 + 4, chip_y0 + 38, 724 - 2, by + 48, BLUE)
d.arrow_label((chip_x + 118 + 724) / 2, by + 34, "session.append(type, data)", BLUE)

d.box(724, by, 330, 96, "Session log", [
    "core/session/src/index.ts:526",
    "log.push(event)  →  :901",
], col=EMERALD)
d.aside(724, by + 110, [
    "The log is append-only: seq = log.length at append time.",
])

y = y1 + P2_H + 24
d.legend(30, y, [
    (BLUE, "AgentRegistry / session events"),
    (AMBER, "AgentLoop / the turn-step loop"),
    (VIOLET, "the Agent interface"),
    (EMERALD, "the session log"),
])
y += 30
y = d.footnotes(30, y, [
    "Simplified: tool execution inside a step, retries, and cancellation are left out.",
    "Every box and arrow above cites the exact file:line in the diagram script's docstring.",
])
d.save(height=y + 14)
