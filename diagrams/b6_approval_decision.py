"""Diagram for concepts/approval-and-interaction.html: how one approval question
is asked and audited, and who gets to answer it.

Used by: src/concepts/approval-and-interaction.html (<x-diagram name="b6_approval_decision" ... />)
Sources (at the pinned commit in explainer.json):
  packages/core/tools/src/contracts.ts:357-361        PreToolDecision 'ask' (from a tools/pre-execute listener)
  packages/core/tools/src/pipeline.ts:449-471          serviceAsk() calls approval.request(), maps the outcome back
  packages/interaction/user-approval/src/index.ts:242-261   request(): audit pair around the decision
  packages/interaction/user-approval/src/index.ts:293-318   decide(): 'never' short-circuits before any answerer runs
  packages/acp/acp/src/index.ts:158-176                one ACP answerer example (session/request_permission)
  packages/client/ui-approval/src/client/index.ts:107  browser UI answerer
  packages/sdk/server/src/server.ts:130-148            SDK answerer (only when approvalRequests is on)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "How is one approval question decided?",
    "ctx.approval audits the ask and the outcome; the session's policy decides who, if anyone, is asked",
    params="1 audit pair  ·  2 policies  ·  canvas 1100",
)

# ---- Panel 1: the request lifecycle ------------------------------------------
y0 = 112
P1_H = 170
d.panel(y0, P1_H, 1, "What happens when a tool call needs a yes?",
        "pipeline.ts:449-471 calls ctx.approval.request(); the outcome maps back to allow or deny.")

cw, ch, gap = 326, 108, 20
cx = 46
d.step_card(cx, y0 + 50, cw, ch, 1, "pre-execute listener: kind 'ask'", BLUE,
            rows=[("from", "contracts.ts:357-361")])
cx += cw + gap
d.step_card(cx, y0 + 50, cw, ch, 2, "approval/asked -> decide() -> approval/decided", AMBER,
            rows=[("audit", "index.ts:242-261")])
cx += cw + gap
d.step_card(cx, y0 + 50, cw, ch, 3, "outcome maps back to allow / deny", VIOLET,
            rows=[("only", "allowed-once proceeds")])
d.arrow(46 + cw, y0 + 104, 46 + cw + gap, y0 + 104, BLUE)
d.arrow(46 + 2 * cw + gap, y0 + 104, 46 + 2 * cw + 2 * gap, y0 + 104, AMBER)

# ---- Panel 2: who answers -----------------------------------------------------
y1 = y0 + P1_H + 24
P2_H = 212
d.panel(y1, P2_H, 2, "Who gets asked, and when does nobody?",
        "'never' decides before dispatch; 'ask' runs a waterfall of composed answerers.")

lane_y = y1 + 44
lane_h = P2_H - 56
d.lane(46, lane_y, 300, lane_h, AMBER, 'policy: "never"', [
    "index.ts:301",
])
d.box(66, lane_y + 78, 260, 70, "rejected", ["deterministic, no answerer runs", "(CI / unattended stance)"], col=AMBER, mono_size=10)

d.lane(366, lane_y, 694, lane_h, EMERALD, 'policy: "ask" -> waterfall', [
    "first composed answerer to return an outcome decides (cordis-primer.md:22)",
])
bw = 210
for i, (title, note) in enumerate([
    ("browser UI", "ui-approval"),
    ("ACP bridge", "session/request_permission"),
    ("SDK bridge", "approval/request (opt-in)"),
]):
    bx = 386 + i * (bw + 15)
    d.box(bx, lane_y + 78, bw, 70, title, [note], col=EMERALD, mono_size=10)

y = y1 + P2_H + 24
d.legend(30, y, [
    (AMBER, "fail-closed: no answerer ever runs"),
    (EMERALD, "exactly one answerer's outcome wins"),
])
y += 30
y = d.footnotes(30, y, [
    "No claiming answerer, a throwing answerer or an unknown value gives 'unavailable'. Callers deny it (index.ts:306-318).",
    "Simplified: cancellation races, scope-filtered dispatch, and the sandbox-escalation retry are left out of this picture.",
])
d.save(height=y + 14)
