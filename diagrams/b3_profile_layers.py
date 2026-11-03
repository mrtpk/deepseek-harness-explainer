"""Diagram for learn/profiles-and-bundles.html: how a profile's bundles and
patch layers stack into one running dsh plugin tree.

Used by: src/learn/profiles-and-bundles.html (<x-diagram name="b3_profile_layers" ... />)
Sources (at the pinned commit in explainer.json):
  packages/util/official-bundles/src/bundles.ts:14-19   PROFILE_TEMPLATES: web and headless bundle lists
  packages/bundle/headless/package.json:39-42           dsh.bundle.patch -> ./cordis.patch.yml
  packages/boot/app-boot/src/profile-context.ts:75-80   readProfilePatches(): layer order
  apps/cli/src/profile-boot.ts:73-75                    homePatchPath(): $DSH_HOME/cordis.patch.yml
  apps/cli/src/args.ts:170                              --patch <path> overlay option (repeatable)
  packages/boot/app-boot/src/profile.ts:755-762         composeEntries(): patches apply over an empty entry list
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, EMERALD, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "How is one running dsh tree assembled?",
    "A profile stacks bundles; patch layers then overlay on top, in a fixed order",
    params="2 example profiles  ·  4 patch layers  ·  canvas 1100",
)

# ---- Panel 1: a profile stacks named bundles --------------------------------
y0 = 112
P1_H = 172
d.panel(y0, P1_H, 1, "Which bundles does a profile stack?",
        "Two shipped profiles, read from one bundle-list table.")
bx_y, bw, bh = y0 + 70, 460, 80
d.box(60, bx_y, bw, bh, "profile: web", [
    "dsh-base, dsh-web-app",
    "bundles.ts:14-16",
], col=BLUE)
d.box(580, bx_y, bw, bh, "profile: headless", [
    "dsh-base, dsh-headless",
    "bundles.ts:17-19",
], col=BLUE)
d.aside(60, bx_y + bh + 18, [
    "Each bundle names its own patch file in package.json's dsh.bundle.patch (headless/package.json:39-42).",
])

# ---- Panel 2: patch layers stack in a fixed order ---------------------------
y1 = y0 + P1_H + 24
P2_H = 430
d.panel(y1, P2_H, 2, "In what order do patch layers apply?",
        "Layers apply over an empty entry list; a later layer can replace or add a row by id.")

lx, lw, lh, gap = 275, 550, 46, 62
ly = y1 + 68
layers = [
    ("1. Bundle patches", "dsh-base, dsh-headless rows", "profile-context.ts:76", BLUE),
    ("2. Profile's own cordis.patch.yml", "per-profile tweak layer", "profile-context.ts:77", VIOLET),
    ("3. $DSH_HOME/cordis.patch.yml", "machine-local, outranks #2", "profile-boot.ts:73-75", AMBER),
    ("4. --patch overlays", "argv order, applied last", "args.ts:170", EMERALD),
]
for i, (title, note, cite, col) in enumerate(layers):
    y = ly + i * gap
    d.box(lx, y, lw, lh, title, [note, cite], col=col, tsize=13, mono_size=10.8)
    if i < len(layers) - 1:
        d.arrow(lx + lw / 2, y + lh, lx + lw / 2, y + gap - 2, col)

result_y = ly + len(layers) * gap + 6
d.arrow(lx + lw / 2, result_y - 8, lx + lw / 2, result_y + 2, EMERALD)
d.box(lx, result_y + 4, lw, 54, "Composed entry list (mounted tree)", [
    "composeEntries(): profile.ts:755-762",
], col=AMBER, fill="#fff")
d.aside(lx, result_y + 4 + 54 + 16, [
    "A patch names a row by id: it replaces that row's whole config, or inserts a new row (architecture.md:25).",
])

legend_y = y1 + P2_H + 24
d.legend(30, legend_y, [
    (BLUE, "profile bundle list / bundle layer"),
    (VIOLET, "profile's own patch"),
    (AMBER, "home patch / result"),
    (EMERALD, "--patch overlay"),
])
y = legend_y + 40
y = d.footnotes(30, y, [
    "Simplified: presets, HMR reload, skipped-bundle handling, and the optional telemetry-off patch are left out.",
    "Every box cites its exact file:line in the diagram script's docstring.",
])
d.save(height=y + 14)
