"""Diagram for concepts/acp-sdk-and-clients.html: the three protocol seams a
client can use to reach a dsh runtime, and how the Python SDK is just a
subprocess launcher over one of them.

Used by: src/concepts/acp-sdk-and-clients.html (<x-diagram name="b6_acp_sdk_clients" ... />)
Sources (at the pinned commit in explainer.json):
  packages/acp/acp/README.md:11                 dsh-acp: automation-only ACP server, JSON-RPC over stdio
  packages/sdk/protocol/README.md:12,34         dsh-sdk-protocol: newline-delimited JSON-RPC, 1 message per line
  packages/sdk/server/README.md:11               dsh-sdk-jsonrpc-server serves that protocol over stdio
  packages/client/connection/README.md:12,34     dsh-client-connection: Remote RPC over HTTP POST + a Mux WebSocket
  packages/client/connection/README.md:30        a desktop page supplies its own streamBaseUrl to the same carrier
  apps/desktop/src/main.ts:790                   Desktop actually does this (returns { streamBaseUrl })
  python/README.md:5                              the Python SDK drives dsh as a subprocess, over stdio JSON-RPC
  python/sdk/README.md (Start a runtime)          "no separate application entrypoint"; launches dsh --profile sdk
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import AMBER, BLUE, NEUTRAL, VIOLET, Diagram  # noqa: E402

d = Diagram(width=1100)
d.header(
    "How does a client reach a dsh runtime?",
    "Three separate protocol seams, each served by its own plugin",
    params="3 protocol seams  ·  1 shared runtime  ·  canvas 1100",
)

# ---- Panel 1: three seams into one runtime -----------------------------------
y0 = 112
P1_H = 230
d.panel(y0, P1_H, 1, "Which protocol does a client speak?",
        "Each seam is a different plugin; none of them calls another.")

bw, bh, gap = 320, 86, 30
bx = 46
cols = [BLUE, AMBER, VIOLET]
titles = [
    ("ACP server", ["dsh-acp, generic protocol", "automation only (acp/README.md:11)"]),
    ("SDK jsonrpc-server", ["dsh's own wire protocol", "Node + Python SDK clients"]),
    ("Web/Desktop connection", ["Remote RPC: HTTP POST", "+ one Mux WebSocket"]),
]
for i, (title, lines) in enumerate(titles):
    x = bx + i * (bw + gap)
    d.box(x, y0 + 56, bw, bh, title, lines, col=cols[i], mono_size=10.5)
    d.arrow(x + bw / 2, y0 + 142, x + bw / 2, y0 + 190, cols[i])

d.box(230, y0 + 190, 640, 34, "dsh agent / session runtime", [], col=NEUTRAL, tsize=13)

# ---- Panel 2: the Python SDK is a launcher, not a 4th seam -------------------
y1 = y0 + P1_H + 24
P2_H = 150
d.panel(y1, P2_H, 2, "Where does the Python SDK fit in?",
        "It has no protocol of its own: it starts the SDK seam's own server.")

d.box(66, y1 + 60, 300, 64, "Python SDK process", ["deepseek_harness package"], col=AMBER, mono_size=10.5)
d.arrow(366, y1 + 92, 470, y1 + 92, AMBER)
d.box(472, y1 + 60, 420, 64, 'bundled "dsh --profile sdk" binary', ["no in-process harness logic (python/README.md:5)"], col=AMBER, mono_size=10)

y = y1 + P2_H + 24
y = d.legend(30, y, [
    (BLUE, "ACP: generic automation protocol"),
    (AMBER, "SDK: dsh's own wire protocol"),
    (VIOLET, "Web/Desktop: Remote RPC"),
])
y += 30
y = d.footnotes(30, y, [
    "Desktop supplies its own HTTP origin (streamBaseUrl) to the same browser connection carrier (connection/README.md:30, desktop/src/main.ts:790).",
    "Simplified: MCP server mounting, session persistence, and per-protocol approval bridging are left out of this picture.",
])
d.save(height=y + 14)
