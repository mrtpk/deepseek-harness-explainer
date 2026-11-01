"""Overview diagram for tours/life-of-a-headless-task.html: the 9 stops of one
`dsh --profile headless "task"` run, grouped into three stages.

Used by: src/tours/life-of-a-headless-task.html (<x-diagram name="b2_headless_tour" ... />)
Sources (at the pinned commit in explainer.json; see the page for the full citations):
  apps/cli/src/args.ts:146-216                  parseDshArgs()
  apps/cli/src/profile-boot.ts:224-236,313-323  composeProfile(), runProfile()
  packages/bundle/headless/cordis.patch.yml:14-26  insert headless-startup, headless-runner
  packages/bundle/headless/src/index.ts:389-394 agents.create(...)
  packages/core/agent-loop/src/agent.ts:179-181 followup(input)
  packages/core/agent-loop/src/agent.ts:230-250 wakeDriver() starts kick()
  packages/core/agent-loop/src/agent.ts:590-593 this.loopCtx.tools.execute(...)
  packages/bundle/headless/src/index.ts:424-431 whenIdle() / waitForChildren() loop
  packages/bundle/headless/src/index.ts:435,438 sessions.flush(), stdout.write()
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "Life of one headless task, stop by stop",
    "dsh --profile headless \"task\"  ·  9 stops in 3 stages",
    params="canvas 1100",
)

x_positions = [46, 400, 754]
bw, bh = 290, 92

# ---- Stage 1: start the run -------------------------------------------------
y0 = 112
d.panel(y0, 176, 1, "How does the run start?",
        "The launcher parses argv, boots the profile, and mounts the headless bundle.")
by = y0 + 68
cards1 = [
    ("bin.ts / args.ts", [("at", "args.ts:146-216"), ("do", "parseDshArgs()")]),
    ("profile-boot.ts", [("at", "profile-boot.ts:313-323"), ("do", "composeProfile(), boot()")]),
    ("headless bundle", [("at", "cordis.patch.yml:14-26"), ("do", "insert headless-runner")]),
]
for i, (x, (title, rows)) in enumerate(zip(x_positions, cards1)):
    d.step_card(x, by, bw, bh, i + 1, title, BLUE, rows=rows)
for i, label in enumerate(["--profile headless \"task\"", "boot() mounts the stack"]):
    x1 = x_positions[i] + bw
    x2 = x_positions[i + 1]
    d.arrow(x1, by + bh / 2, x2 - 2, by + bh / 2, BLUE)
    d.arrow_label((x1 + x2) / 2, by + bh / 2, label, BLUE)

# ---- Stage 2: run the task ---------------------------------------------------
y1 = y0 + 176 + 24
P2_H = 204
d.panel(y1, P2_H, 2, "How does the task reach the model?",
        "The runner creates an Agent, hands it the task, and wakes its turn/step loop.")
by = y1 + 68
cards2 = [
    ("AgentRegistry.create()", [("at", "headless/index.ts:389"), ("do", "builds one Agent")]),
    ("agent.followup()", [("at", "agent-loop/agent.ts:179"), ("do", "queues next-turn input")]),
    ("turn/step loop", [("at", "agent-loop/agent.ts:230"), ("do", "wakeDriver() -> kick()")]),
]
for i, (x, (title, rows)) in enumerate(zip(x_positions, cards2)):
    d.step_card(x, by, bw, bh, i + 4, title, AMBER, rows=rows)
for i, label in enumerate(["one fresh Session", "wakeup = true"]):
    x1 = x_positions[i] + bw
    x2 = x_positions[i + 1]
    d.arrow(x1, by + bh / 2, x2 - 2, by + bh / 2, AMBER)
    d.arrow_label((x1 + x2) / 2, by + bh / 2, label, AMBER)
d.aside(46, by + bh + 20, [
    "The turn/step loop itself is the subject of a separate page (see the link under the diagram).",
])

# ---- Stage 3: finish the run --------------------------------------------------
y2 = y1 + P2_H + 24
d.panel(y2, 176, 3, "How does the run end?",
        "Tools run, the runner waits for quiet, then flushes the log and prints the result.")
by = y2 + 68
cards3 = [
    ("tools.execute()", [("at", "agent-loop/agent.ts:590"), ("do", "pre- / execute / post-")]),
    ("whenIdle + children", [("at", "headless/index.ts:424-431"), ("do", "waits for subagents")]),
    ("flush + stdout", [("at", "headless/index.ts:435,438"), ("do", "sessions.flush(), write")]),
]
for i, (x, (title, rows)) in enumerate(zip(x_positions, cards3)):
    d.step_card(x, by, bw, bh, i + 7, title, EMERALD, rows=rows)
for i, label in enumerate(["no tool work owed", "idle, no live children"]):
    x1 = x_positions[i] + bw
    x2 = x_positions[i + 1]
    d.arrow(x1, by + bh / 2, x2 - 2, by + bh / 2, EMERALD)
    d.arrow_label((x1 + x2) / 2, by + bh / 2, label, EMERALD)

legend_y = y2 + 176 + 24
d.legend(30, legend_y, [
    (BLUE, "stage 1 · start the run"),
    (AMBER, "stage 2 · run the task"),
    (EMERALD, "stage 3 · finish the run"),
])
y = legend_y + 40
y = d.footnotes(30, y, [
    "Simplified: --json mode, --session-id resume, and error/cancellation paths are left out.",
    "Each stop's exact file:line is cited on the page, not just in this diagram's docstring.",
])
d.save(height=y + 14)
