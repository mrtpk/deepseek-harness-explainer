"""Diagram for concepts/llm-and-system-prompt.html: ctx.llm's adapter seam, and how one
step builds the request it streams through that seam.

Used by: src/concepts/llm-and-system-prompt.html (<x-diagram name="b4_llm_adapter_seam" ... />)
Sources (at the pinned commit in explainer.json):
  packages/llm/llm/src/index.ts:401        LlmRuntime.registerAdapter(providers, adapter)
  packages/llm/llm/src/index.ts:1170       LlmRuntime.stream() -> streamWithRegistration()
  packages/llm/llm-deepseek/src/host.ts:81 ctx.llm.registerAdapter([provider], adapter)
  packages/llm/llm-deepseek/src/adapter.ts:22  class DeepSeekAdapter extends LlmAdapter
  packages/core/agent-loop/src/agent.ts:294 ctx.systemPrompt.assemble(...)
  packages/core/agent-loop/src/agent.ts:442 renderPrompt(assembly)
  packages/core/agent-loop/src/agent.ts:453-461 systemPrompt.project() -> append('system/message', ...)
  packages/core/agent-loop/src/agent.ts:656-728 buildRequest(): request/header, deriveMessages()
  packages/core/agent-loop/src/agent.ts:644 preparedCall = ctx.llm.prepareCall(...)
  packages/core/agent-loop/src/agent.ts:490 preparedCall?.stream(request) ?? this.loopCtx.llm.stream(request)
  packages/llm/llm/src/index.ts:1010       a prepared call also runs the llm/stream waterfall
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "What does ctx.llm route to, and what does it send?",
    "The provider-adapter seam, and the three steps that build one request",
    params="1 request  ·  1 adapter route  ·  canvas 1100",
)

# ---- Panel 1: the adapter seam ---------------------------------------------
y0 = 112
P1_H = 170
d.panel(y0, P1_H, 1, "Who streams the model call?",
        "ctx.llm selects the adapter registered for the request's provider name.")
bx_y, bw, bh = y0 + 70, 290, 80
d.box(46, bx_y, bw, bh, "AgentLoop.step()", [
    "agent-loop/src/agent.ts:490",
    "preparedCall.stream(request)",
], col=AMBER)
d.arrow(46 + bw, bx_y + bh / 2, 400 - 2, bx_y + bh / 2, AMBER)
d.arrow_label(46 + bw + 24, bx_y + bh / 2 - 12, "stream(request)", AMBER)
d.box(400, bx_y, bw, bh, "LlmRuntime (ctx.llm)", [
    "llm/src/index.ts:401",
    "registerAdapter(providers, .)",
], col=BLUE)
d.arrow(400 + bw, bx_y + bh / 2, 754 - 2, bx_y + bh / 2, BLUE)
d.arrow_label(400 + bw + 24, bx_y + bh / 2 - 12, "registered route", BLUE)
d.box(754, bx_y, bw, bh, "DeepSeekAdapter", [
    "llm-deepseek/src/adapter.ts:22",
    "extends LlmAdapter",
], col=VIOLET)
d.aside(46, bx_y + bh + 18, [
    "Any provider adapter can go here. Only its stream() method is required.",
])

# ---- Panel 2: building the request -----------------------------------------
y1 = y0 + P1_H + 24
P2_H = 232
d.panel(y1, P2_H, 2, "How does one step build that request?",
        "Three sub-steps run before the request is frozen and streamed.")
cy = y1 + 70
cw = 330
gap = (1080 - 46 - 3 * cw) / 2
xs = [46, 46 + cw + gap, 46 + 2 * cw + 2 * gap]
d.step_card(xs[0], cy, cw, 130, 1, "Assemble", BLUE, tag="agent.ts:294", rows=[
    ("in", "sections + tools + ctx"),
    ("via", "ctx.systemPrompt"),
])
d.step_card(xs[1], cy, cw, 130, 2, "Render & commit", AMBER, tag="agent.ts:442,453", rows=[
    ("out", "rendered prompt text"),
    ("logs", "system/message"),
])
d.step_card(xs[2], cy, cw, 130, 3, "Build & stream", EMERALD, tag="agent.ts:656,490", rows=[
    ("logs", "request/header"),
    ("sends", "preparedCall.stream()"),
])
for i in range(2):
    ax = xs[i] + cw
    d.arrow(ax, cy + 65, xs[i + 1] - 2, cy + 65, BLUE)
d.aside(46, cy + 146, [
    "deriveMessages() turns the session log into the model-visible history sent with the request (agent.ts:728).",
])

y = y1 + P2_H + 24
d.legend(30, y, [
    (AMBER, "the agent loop"),
    (BLUE, "ctx.llm / assembly"),
    (VIOLET, "a provider adapter"),
    (EMERALD, "building the frozen request"),
])
y += 30
y = d.footnotes(30, y, [
    "Simplified: retries, image attachments and reasoning-effort controls are not shown.",
    "Every box and arrow above cites the exact file:line in the diagram script's docstring.",
])
d.save(height=y + 14)
