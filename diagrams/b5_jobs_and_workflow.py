"""Diagram for concepts/jobs-workflow-goal-plan.html: the background-job status
lifecycle, and how a workflow script's agent() calls reach the same subagent seam.

Used by: src/concepts/jobs-workflow-goal-plan.html (<x-diagram name="b5_jobs_and_workflow" ... />)
Sources (at the pinned commit in explainer.json):
  packages/jobs/jobs/src/view.ts:15-19         JobStatus union; running, optional stopping, one terminal state
  packages/jobs/jobs-local/src/index.ts:484-493,694-707   stopping on kill() or teardown
  packages/jobs/jobs/src/index.ts:88-100,113   JobRegistry (ctx.jobs), abstract start()
  packages/workflow/workflow/src/index.ts:157,168   WorkflowEngine (ctx.workflowEngine), abstract start()
  packages/workflow/workflow-ptc/src/index.ts:3,167     the script process gets the calling session's file policy
  packages/workflow/workflow-ptc/src/host.ts:200-220    each agent() call becomes subagents.startActivation()
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, NEUTRAL, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "Job states, and what starts a workflow's children",
    "Two independent, optional capabilities beside the agent loop",
    params="5 job states  ·  1 sandboxed script  ·  canvas 1100",
)

# ---- Panel 1: job status lifecycle ------------------------------------------
y0 = 112
P1_H = 150
d.panel(y0, P1_H, 1, "What are the job states?",
        "ctx.jobs tracks one producer-owned execution per id (jobs/src/view.ts:19).")
states = [
    ("running", BLUE, False),
    ("stopping", AMBER, False),
    ("completed", EMERALD, True),
    ("killed", NEUTRAL, True),
    ("failed", VIOLET, True),
]
cw = 170
gap = (1040 - 46 - len(states) * cw) / (len(states) - 1)
cy = y0 + 70
for i, (label, col, terminal) in enumerate(states):
    cx = 46 + i * (cw + gap)
    d.chip(cx, cy, cw, label, col, h=34)
    if i == 0:
        d.arrow(cx + cw + 2, cy + 17, cx + cw + gap - 2, cy + 17, BLUE)
d.aside(46, cy + 52, [
    "running -> stopping after a kill() request or a teardown (jobs-local/src/index.ts:484-493, 694-707).",
    "running or stopping -> exactly one terminal state: completed, killed or failed (view.ts:15-19).",
])

# ---- Panel 2: workflow script starts subagents -------------------------------
y1 = y0 + P1_H + 24
P2_H = 196
d.panel(y1, P2_H, 2, "How does a workflow script start children?",
        "Every agent() call in the script runs through the same subagent seam.")
d.box(46, y1 + 60, 260, 76, "Model-written script", [
    "{ script, meta, args }", "workflow/src/index.ts:168",
], col=BLUE, mono_size=10.5)
d.arrow(306, y1 + 98, 404, y1 + 98, BLUE)
d.box(406, y1 + 60, 300, 76, "sandboxed Node process", [
    "workflow-ptc/index.ts:3,167", "one agent() call = 1 child",
], col=AMBER, mono_size=10.5)
d.arrow(706, y1 + 98, 804, y1 + 98, AMBER)
d.box(806, y1 + 60, 220, 76, "ctx.subagents", [
    "host.ts:200-220", 'delivery: "caller"',
], col=EMERALD, mono_size=10.5)
d.text(46, y1 + P2_H - 14, "The delegation tool uses the same seam. The script is one more caller.",
       11.5, "#6b7280")

y = y1 + P2_H + 24
d.legend(30, y, [
    (BLUE, "running / caller-written"),
    (AMBER, "in-flight / sandbox boundary"),
    (EMERALD, "terminal (completed) / subagent seam"),
])
y += 30
y = d.footnotes(30, y, [
    "Simplified: goals and plan mode add no new process boundary, so they are not drawn here (see the text below).",
    "The job ring, the workflow's phase/log events, and capacity caps are left out of this picture.",
])
d.save(height=y + 14)
