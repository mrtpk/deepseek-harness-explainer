/* tool-pipeline-stepper.js - step through one tool call's pipeline.
 *
 * Mounts into <x-viz id="tool-pipeline-stepper"> on concepts/tools-and-mcp.html.
 * Vanilla JS, no libraries, no network. Every station's text is fixed (no randomness),
 * so every reader sees the same example: bash({ command: "npm test" }).
 *
 * Sources (at the pinned commit in explainer.json):
 *   packages/core/tools/src/batch.ts:157       settlement.start() appends 'tool/call'
 *   packages/core/tools/src/pipeline.ts:200    prepare() runs the 'tools/pre-execute' waterfall
 *   packages/core/tools/src/pipeline.ts:213    guards run right after pre-execute, denial-only
 *   packages/core/tools/src/contracts.ts:357-361  PreToolDecision: allow | deny | cancel | ask
 *   packages/core/tools/src/pipeline.ts:300    dispatch() runs the 'tools/execute' waterfall
 *   packages/core/tools/src/pipeline.ts:272-275 the wrapped call resolves and runs tool.execute()
 *   packages/core/tools/src/pipeline.ts:488     postExecute() runs the 'tools/post-execute' waterfall
 *   packages/core/tools/src/contracts.ts:367-370  PostToolDecision: accept | block
 *   packages/core/tools/src/batch.ts:146,256    settlement.commit() appends 'tool/result'
 *   packages/jobs/tool-jobs/src/index.ts:286           example pre-execute listener
 *   packages/guard/timeout-policy/src/index.ts:56      example tools/execute wrapper
 *   packages/guard/repeat-tool-reminder/src/index.ts:220  example post-execute listener
 *
 * Left out: approval ("ask") prompts, parallel-call scheduling, PTC nested calls, cancellation.
 *
 * Rules (STYLE.md section 10): IIFE scope; prefixed classes scoped under the mount; colours from the
 * site.css custom properties (dark mode works); real <button> elements (min 40 px); keyboard and touch;
 * an aria-live region; works at 390 px width; deterministic (no randomness is used); a Reset button.
 */
(function () {
  "use strict";

  var VIZ_ID = "tool-pipeline-stepper";

  var STATIONS = [
    {
      kind: "event", title: "tool/call logged", where: "tools/src/batch.ts:157,247",
      lede: "The model's call is appended to the session log before the pipeline runs.",
      detail: 'bash({ command: "npm test" }) is logged, durable and replayable, before any policy runs.',
      part: "event"
    },
    {
      kind: "stage", title: "tools/pre-execute", where: "tools/src/pipeline.ts:200",
      lede: "Listeners vote allow, deny, cancel, or ask, before the call may run.",
      detail: "@deepseek-ai/dsh-tool-jobs reads a per-call output-size budget here (tool-jobs/src/index.ts:286). " +
        "Right after, registered guards get one more look: a guard can only add a denial, never undo one (pipeline.ts:213).",
      part: "pre"
    },
    {
      kind: "stage", title: "tools/execute", where: "tools/src/pipeline.ts:300",
      lede: "An around-dispatch wrapper runs, then the tool's own body runs.",
      detail: "@deepseek-ai/dsh-tool-call-timeout-policy wraps dispatch with a cooperative timeout " +
        "(timeout-policy/src/index.ts:56). The wrapped call resolves bash's definition and calls its execute() (pipeline.ts:272-275).",
      part: "exec"
    },
    {
      kind: "stage", title: "tools/post-execute", where: "tools/src/pipeline.ts:488",
      lede: "Listeners accept, replace, or block the normalized result.",
      detail: "@deepseek-ai/dsh-repeat-tool-reminder adds a nudge message if this exact call repeats " +
        "(repeat-tool-reminder/src/index.ts:220). A listener may replace content or a success value, never both (pipeline.ts:501-502).",
      part: "post"
    },
    {
      kind: "event", title: "tool/result logged", where: "tools/src/batch.ts:146,256",
      lede: "The final, accepted result is appended to the session log.",
      detail: "The model sees this tool/result on its next step. tool/call and tool/result are singular, durable session events " +
        "- distinct from the three plural tools/* waterfalls above, which are live extension points, not log entries.",
      part: "event"
    }
  ];

  var PART_COLOR = {
    event: "var(--mute)",
    pre: "var(--viz-c1)",
    exec: "var(--viz-c4)",
    post: "var(--viz-c3)"
  };

  var CSS = [
    ".tps-root{font-family:var(--sans);color:var(--ink)}",
    ".tps-rail{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px;padding:0;list-style:none}",
    ".tps-btn-station{min-width:40px;min-height:40px;padding:4px 10px;border:1px solid var(--line);",
    "  border-radius:6px;background:var(--surface);font:600 12.5px var(--sans);color:var(--ink);cursor:pointer;",
    "  text-align:left;line-height:1.2}",
    ".tps-btn-station[aria-current=step]{border-color:var(--tps-c,var(--blue));box-shadow:inset 0 -3px 0 var(--tps-c,var(--blue))}",
    ".tps-btn-num{display:inline-block;min-width:16px;font:700 12.5px var(--mono)}",
    ".tps-card{border-left:4px solid var(--tps-c,var(--line));padding:10px 16px;margin:0 0 12px;",
    "  background:var(--panel-bg);border-radius:0 8px 8px 0}",
    ".tps-kind{display:inline-block;font:700 10.5px var(--mono);letter-spacing:.04em;",
    "  text-transform:uppercase;color:var(--tps-c,var(--mute));margin:0 0 4px}",
    ".tps-title{margin:0 0 2px;font-weight:700;font-size:17px}",
    ".tps-where{margin:0 0 8px;font:12.5px var(--mono);color:var(--mute);overflow-wrap:anywhere}",
    ".tps-lede{margin:0 0 6px;font-size:14.5px}",
    ".tps-detail{margin:0;font-size:13.5px;color:var(--mute)}",
    ".tps-ctrl{display:flex;flex-wrap:wrap;gap:8px}",
    ".tps-btn{min-height:40px;padding:0 16px;border:1px solid var(--line);border-radius:6px;",
    "  background:var(--surface);color:var(--ink);font:600 14.5px var(--sans);cursor:pointer}",
    ".tps-btn:disabled{opacity:.45;cursor:default}",
    ".tps-live{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}",
    "@media (max-width:460px){.tps-btn-station{flex:1 1 40%}}"
  ].join("\n");

  function injectCss() {
    if (document.getElementById("tps-style")) return;
    var st = document.createElement("style");
    st.id = "tps-style";
    st.textContent = CSS;
    document.head.appendChild(st);
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function Viz(mount) {
    this.mount = mount;
    mount.innerHTML = ""; // removes the .viz-fallback text
    var root = el("div", "tps-root");

    this.rail = el("ol", "tps-rail");
    var self = this;
    this.stationBtns = STATIONS.map(function (s, i) {
      var li = el("li");
      var b = el("button", "tps-btn-station");
      b.type = "button";
      var num = el("span", "tps-btn-num", String(i + 1) + ". ");
      b.appendChild(num);
      b.appendChild(document.createTextNode(s.title));
      b.setAttribute("aria-label", "Station " + (i + 1) + " of " + STATIONS.length + ": " + s.title);
      b.addEventListener("click", function () { self.go(i); });
      li.appendChild(b);
      self.rail.appendChild(li);
      return b;
    });

    this.card = el("div", "tps-card");
    this.kindEl = el("p", "tps-kind");
    this.titleEl = el("p", "tps-title");
    this.whereEl = el("p", "tps-where");
    this.ledeEl = el("p", "tps-lede");
    this.detailEl = el("p", "tps-detail");
    [this.kindEl, this.titleEl, this.whereEl, this.ledeEl, this.detailEl].forEach(function (e) {
      self.card.appendChild(e);
    });

    var ctrl = el("div", "tps-ctrl");
    this.prev = el("button", "tps-btn", "← Previous");
    this.next = el("button", "tps-btn", "Next →");
    var rst = el("button", "tps-btn", "Reset");
    [this.prev, this.next, rst].forEach(function (b) { b.type = "button"; ctrl.appendChild(b); });

    this.live = el("div", "tps-live");
    this.live.setAttribute("aria-live", "polite");

    this.prev.addEventListener("click", function () { self.go(self.i - 1); });
    this.next.addEventListener("click", function () { self.go(self.i + 1); });
    rst.addEventListener("click", function () { self.go(0); });

    root.appendChild(this.rail);
    root.appendChild(this.card);
    root.appendChild(ctrl);
    root.appendChild(this.live);
    mount.appendChild(root);

    this.go(0, true);
  }

  Viz.prototype.go = function (i, quiet) {
    if (i < 0 || i >= STATIONS.length) return;
    this.i = i;
    var s = STATIONS[i];
    var col = PART_COLOR[s.part] || "var(--line)";
    this.card.style.setProperty("--tps-c", col);
    this.kindEl.textContent = s.kind === "event" ? "Durable session event" : "Live pipeline stage";
    this.kindEl.style.setProperty("--tps-c", col);
    this.titleEl.textContent = (i + 1) + ". " + s.title;
    this.whereEl.textContent = s.where;
    this.ledeEl.textContent = s.lede;
    this.detailEl.textContent = s.detail;
    this.stationBtns.forEach(function (b, k) {
      b.style.setProperty("--tps-c", PART_COLOR[STATIONS[k].part] || "var(--line)");
      if (k === i) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
    });
    this.prev.disabled = i === 0;
    this.next.disabled = i === STATIONS.length - 1;
    if (!quiet) {
      this.live.textContent = "Station " + (i + 1) + " of " + STATIONS.length + ": " + s.title + ". " + s.lede;
    }
  };

  function init() {
    injectCss();
    var mounts = document.querySelectorAll('[data-viz="' + VIZ_ID + '"]');
    Array.prototype.forEach.call(mounts, function (m) { new Viz(m); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
