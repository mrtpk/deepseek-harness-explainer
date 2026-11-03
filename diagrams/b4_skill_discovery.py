"""Diagram for concepts/skills.html: where a skill is discovered from, and how it reaches
the model inside a session.

Used by: src/concepts/skills.html (<x-diagram name="b4_skill_discovery" ... />)
Sources (at the pinned commit in explainer.json):
  packages/skill/skill/src/index.ts:356          class SkillRegistry (ctx.skills)
  packages/skill/skill-filesystem/src/index.ts:35-39   rank constants (100..500)
  packages/skill/skill-filesystem/src/index.ts:251-271 roots pushed in rank order
  packages/skill/skill/src/index.ts:28           BUNDLED_SKILL_RANK = 600
  packages/skill/skill/src/index.ts:345-352      rank decides duplicates only within one layer
  packages/skill/tool-skill/src/index.ts:217-255 agent/pre-step injects the skill catalog
  packages/skill/tool-skill/src/index.ts:84-160  the model-facing "skill" tool
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "Which skill wins, and how does the model load it?",
    "Local roots rank into one registry; a session catalog loads one skill body on demand",
    params="6 root kinds  ·  1 registry  ·  canvas 1100",
)

# ---- Panel 1: ranked local roots --------------------------------------------
y0 = 112
P1_H = 180
d.panel(y0, P1_H, 1, "Which root wins a duplicate skill name?",
        "In one registry layer, the lower rank wins. The provider scans the roots in this order.")
roots = [
    ("100  project-dsh", ".dsh/skills"),
    ("200  project-agents", ".agents/skills"),
    ("300  custom", "Config.customSkillDirs"),
    ("400  user-dsh", "<dshHome>/skills"),
    ("500  user-agents", "<agentsHome>/skills"),
]
cw = (1040 - 46 - 4 * 10) / 5
for i, (rank, path) in enumerate(roots):
    cx = 46 + i * (cw + 10)
    d.box(cx, y0 + 68, cw, 64, rank, [path], col=BLUE, tsize=12, mono_size=10.5)
d.aside(46, y0 + 142, [
    "skill-filesystem/src/index.ts:35-39,251-271  ·  a 6th rank (600, bundled) is opt-in and not shown here.",
])

# ---- Panel 2: one skill reaching the model ----------------------------------
y1 = y0 + P1_H + 24
P2_H = 196
d.panel(y1, P2_H, 2, "How does a skill reach the model?",
        "Discovery gives a catalog message. The model loads one full body on demand.")
cy = y1 + 70
cw2 = 330
gap = (1080 - 46 - 3 * cw2) / 2
xs = [46, 46 + cw2 + gap, 46 + 2 * cw2 + 2 * gap]
d.step_card(xs[0], cy, cw2, 118, 1, "Discover", AMBER, tag="skill-filesystem", rows=[
    ("via", "ctx.skills.snapshot()"),
])
d.step_card(xs[1], cy, cw2, 118, 2, "Inject catalog", VIOLET, tag="tool-skill.ts:217", rows=[
    ("at", "agent/pre-step"),
    ("as", "name + description only"),
])
d.step_card(xs[2], cy, cw2, 118, 3, "Load on demand", EMERALD, tag="tool-skill.ts:84", rows=[
    ("tool", 'skill({ name })'),
    ("via", "ctx.skills.get()"),
])
for i in range(2):
    ax = xs[i] + cw2
    d.arrow(ax, cy + 55, xs[i + 1] - 2, cy + 55, BLUE)

y = y1 + P2_H + 24
d.legend(30, y, [
    (BLUE, "ranked local roots"),
    (AMBER, "discovery"),
    (VIOLET, "the session catalog"),
    (EMERALD, "a loaded skill body"),
])
y += 30
y = d.footnotes(30, y, [
    "Simplified: remote and embedded providers, invocation-policy flags and watcher invalidation are not shown.",
    "Every box and card above cites the exact file:line in the diagram script's docstring.",
])
d.save(height=y + 14)
