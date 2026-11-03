"""Diagram for concepts/sandbox-and-execution.html: how one capability call's
file-effect policy is resolved, and how the shell, terminal and fs families
enforce it differently.

Used by: src/concepts/sandbox-and-execution.html (<x-diagram name="b6_sandbox_execution" ... />)
Sources (at the pinned commit in explainer.json):
  packages/sandbox/sandbox-policy/src/index.ts:197-205   SandboxPolicyService.resolve() precedence
  packages/sandbox/sandbox/src/index.ts:30               SandboxMode union
  packages/shell/bash-sandbox/src/index.ts:187-189       confine(): wraps argv through ctx.sandbox
  packages/terminal/terminal-bash/src/index.ts:97-106    spawnArgv(): the PTY shell is confined the same way
  packages/fs/fs-sandbox/src/index.ts:156-178            checkedTarget(): path containment, no ctx.sandbox call
  docs/subsystems/sandbox.md:23                          danger-full-access bypasses ctx.sandbox entirely
  packages/bundle/base/cordis.patch.yml:243-247          base bundle mode: DSH_PERMISSION_MODE ?? 'workspace-write'
                                                         (schema default read-only: sandbox-policy/src/index.ts:137)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, NEUTRAL, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "What decides one call's file-effect policy, and who enforces it?",
    "ctx.sandboxPolicy resolves one mode per call; three capability families enforce it two different ways",
    params="1 policy resolver  ·  3 capability families  ·  canvas 1100",
)

# ---- Panel 1: resolving the policy -------------------------------------------
y0 = 112
P1_H = 214
d.panel(y0, P1_H, 1, "Which mode wins for one call?",
        "Precedence, highest first (sandbox-policy/src/index.ts:200).")

bw, bh, gap = 320, 64, 30
bx = 46
for i, (title, lines, col) in enumerate([
    ("explicit approved mode", ["an approved escalation retry"], AMBER),
    ("session's sandbox/mode event", ["the last logged override"], BLUE),
    ("deployment default", ['config "mode" (base: workspace-write)'], NEUTRAL),
]):
    x = bx + i * (bw + gap)
    d.box(x, y0 + 56, bw, bh, title, lines, col=col, mono_size=10.5)
    d.arrow(x + bw / 2, y0 + 120, 550, y0 + 166, col)

d.box(390, y0 + 166, 320, 36, "ctx.sandboxPolicy.resolve()", [], col=VIOLET, tsize=12.5)
d.text(550, y0 + 210, '{ mode, workspaceRoot }  ->  one SandboxExecutionPolicy for this call', 11.5, "#374151", anchor="middle")

# ---- Panel 2: enforcement differs by family ----------------------------------
y1 = y0 + P1_H + 24
P2_H = 196
d.panel(y1, P2_H, 2, "How does each family enforce that policy?",
        "Shell and terminal wrap a subprocess; fs checks the path itself.")

lane_y = y1 + 44
lane_h = P2_H - 56
d.lane(46, lane_y, 620, lane_h, BLUE, "shell + terminal: wrap the subprocess", [
    "bash-sandbox:187-189, terminal-bash:97-106",
])
d.box(66, lane_y + 78, 270, 56, "ctx.sandbox.confine(argv, policy)", ["kernel backend: bwrap / Landlock / Seatbelt / ACL"], col=BLUE, mono_size=10)
d.box(356, lane_y + 78, 280, 56, "returns a replacement argv", ["caller spawns THAT argv instead"], col=BLUE, mono_size=10.5)
d.arrow(336, lane_y + 106, 356, lane_y + 106, BLUE)

d.lane(686, lane_y, 374, lane_h, EMERALD, "fs: checks the path itself", [
    "fs-sandbox/src/index.ts:156-178",
])
d.box(706, lane_y + 78, 334, 56, "canonicalize + containment check", ["no ctx.sandbox call; trusted-code fence"], col=EMERALD, mono_size=10)

y = y1 + P2_H + 24
d.legend(30, y, [
    (BLUE, "wraps a subprocess (kernel boundary)"),
    (EMERALD, "checks a path (trusted-code fence, not a kernel boundary)"),
])
y += 30
y = d.footnotes(30, y, [
    "danger-full-access skips this entirely: a consumer spawns its original argv and never calls ctx.sandbox (docs/subsystems/sandbox.md:23).",
    "Simplified: enforcement completeness (full/partial) and the approval-gated escalation retry are left out of this picture.",
])
d.save(height=y + 14)
