// F043 T001 and T002 — THE TERM AUDIT over rendered surfaces (DECISION F043 D1). The surfaces
// are rendered with `react-dom/server`'s `renderToStaticMarkup`, the one DOM surface this
// repository's vitest config reaches (a node environment with no DOM library, as
// `evidenceChatAudit.test.ts` records), and their `data-term` attributes are read back with the
// audit's own reader. Both directions must be clean over the real components, and each drift
// fixture must turn its direction red. Hover, focus and placement need a browser; the round's
// render harness proves them.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { buildDecisionCardModel } from "../../api/decisionCard";
import type { FeedRow } from "../../api/feedRow";
import { normalizeApiFailure } from "../../api/remedyApi";
import type { RemedyMetric, RemedyState, RemedyTaskItem } from "../../api/types";
import { TERM_CATALOG } from "../../api/terminology";
import { auditTermUse, collectDataTerms } from "../../api/terminologyAudit";
import { TopMetricsBar } from "../metrics/TopMetricsBar";
import { LiveStatusPill } from "../panels/LiveStatusPill";
import { RightLivePanel } from "../panels/RightLivePanel";
import { PhaseTimeline } from "../timeline/PhaseTimeline";
import { TIMELINE_PHASES } from "../timeline/phaseMapping";
import { PHASE_LABELS } from "../timeline/timelineView";
import type { TimelineScrub } from "../timeline/useTimelineScrub";
import { Term } from "./Term";

/** A scrubber over an empty ledger, LIVE: every phase shows its label and nothing else moves. */
const EMPTY_SCRUB: TimelineScrub = {
  state: { mode: "live", position: -1, head: -1, queued: 0 },
  view: {
    segments: TIMELINE_PHASES.map((phase) => ({
      phase, label: PHASE_LABELS[phase], state: "future", compact: false, fill: 0,
    })),
    glyphs: [],
    readout: "No events yet",
  },
  whole: { current: "job", spans: [], lastSeq: null },
  stops: [],
  scrubbedModel: null,
  notice: null,
  scrubTo: () => {},
  onKey: () => false,
  goLive: () => {},
};

function task(id: string, state: RemedyState, applyStatus?: string): RemedyTaskItem {
  return {
    id, label: `Task ${id}`, state, kind: "task", checked: state === "done", muted: false, nodeId: `node-${id}`,
    ...(applyStatus === undefined ? {} : { applyStatus }),
  };
}

/** A running job whose right panel shows every card with a term: a task in each state the list
 *  words differently, one open decision, and an action a moment ago, so the NowCard's Live badge
 *  shows. Built on the dashboard `normalizeApiFailure` answers, the cockpit's own empty shape. */
function panelFixture() {
  const base = normalizeApiFailure("job-1", []);
  const recent: FeedRow[] = [{
    seq: 1, receivedAtMs: Date.now(), kind: "builder_started", line: "The builder started.", known: true,
    timestamp: "", outcome: "", taskId: "",
  }];
  return {
    dashboard: {
      ...base,
      live: { ...base.live, running: true },
      tasks: [task("a", "done"), task("b", "current"), task("c", "blocked"), task("d", "pending"),
        task("e", "done", "partial")],
      decisionInbox: [buildDecisionCardModel({
        id: "d-1", status: "open", type: "clarification", age_seconds: 60, blocked_count: 1,
      })],
    },
    recent,
  };
}

/** The metrics bar's eight tiles: the six plain ones, which carry a term, and the token tile,
 *  whose own breakdown tooltip is the one it keeps this round. */
const METRICS: RemedyMetric[] = [
  { key: "open", label: "Open", value: 1 },
  { key: "planned", label: "Planned", value: 1 },
  { key: "done", label: "Done", value: 2 },
  { key: "progress", label: "Progress", value: 40, suffix: "%" },
  { key: "tests", label: "Tests", value: 3, state: "pass" },
  { key: "proof", label: "Proof", value: 1, suffix: "/2" },
  { key: "tokens", label: "Tokens", value: 1200, tooltip: { builder: 1200 } },
];

function renderPanel(): string {
  const { dashboard, recent } = panelFixture();
  return renderToStaticMarkup(createElement(RightLivePanel, {
    dashboard, serverToken: "token", onSelectNode: () => {}, recent,
  }));
}

/** The terms whose surface a node test cannot render: `BrainGraphStage` imports the force-graph
 *  library, which reads `window` as it loads. Each is held to a literal use in its source file
 *  here, and the round's render harness shows it in a real browser (DECISION F043 D2). */
const BROWSER_ONLY_TERMS: ReadonlyArray<readonly [string, string]> = [
  ["graph.scrubbed", "components/graph/BrainGraphStage.tsx"],
];

const FS_MODULE = "node:fs";
const URL_MODULE = "node:url";
type FsModule = { readFileSync: (path: string, encoding: string) => string };
type UrlModule = { fileURLToPath: (url: URL) => string };

/** A file's text, by its path under `apps/ui/src`, which is two levels above this file. */
async function uiSource(relative: string): Promise<string> {
  const fs = (await import(FS_MODULE)) as FsModule;
  const url = (await import(URL_MODULE)) as UrlModule;
  return fs.readFileSync(url.fileURLToPath(new URL(`../../${relative}`, import.meta.url)), "utf8");
}

/** Every surface this feature has put a term on, in each state that shows a different term. */
function renderSurfaces(): string {
  return [
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: false })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true, streamStatus: "delayed" })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true, streamStatus: "reconnecting" })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true, replay: true })),
    renderToStaticMarkup(createElement(PhaseTimeline, { scrub: EMPTY_SCRUB })),
    renderPanel(),
    renderToStaticMarkup(createElement(TopMetricsBar, { metrics: METRICS })),
  ].join("\n");
}

describe("the Term component's markup", () => {
  it("writes its key, takes keyboard focus, and shows no tooltip until asked", () => {
    const markup = renderToStaticMarkup(createElement(Term, { term: "status.live", children: "LIVE" }));
    expect(markup).toMatch(/^<span [^>]*data-term="status\.live"[^>]*>LIVE<\/span>$/);
    expect(markup).toContain('tabindex="0"');
    expect(markup).not.toContain('role="tooltip"');
    expect(markup).not.toContain("aria-describedby");
  });

  it("still writes the key of a term the catalog lacks, and offers it no focus", () => {
    const markup = renderToStaticMarkup(createElement(Term, { term: "fixture.unlisted", children: "x" }));
    expect(collectDataTerms(markup)).toEqual(["fixture.unlisted"]);
    expect(markup).not.toContain("tabindex");
  });
});

describe("the term audit over the shipped surfaces", () => {
  it("finds exactly the terms the surfaces are built with", () => {
    expect(collectDataTerms(renderSurfaces())).toEqual([
      "agent.live",
      "blocked.task",
      "metric.done",
      "metric.open",
      "metric.planned",
      "metric.progress",
      "metric.proof",
      "metric.tests",
      "panel.activity",
      "panel.agent_now",
      "panel.decisions",
      "panel.tasks",
      "phase.build",
      "phase.finalized",
      "phase.job",
      "phase.planning",
      "phase.review",
      "phase.test",
      "status.delayed",
      "status.idle",
      "status.live",
      "status.reconnecting",
      "status.replay",
      "task.done",
      "task.in_progress",
      "task.partially_applied",
      "task.planned",
    ]);
  });

  it("uses each browser-only term in its own source file", async () => {
    for (const [term, file] of BROWSER_ONLY_TERMS) {
      expect(await uiSource(file), term).toContain(`<Term term="${term}">`);
    }
  });

  it("is clean in both directions against the catalog", () => {
    const used = [...collectDataTerms(renderSurfaces()), ...BROWSER_ONLY_TERMS.map(([term]) => term)];
    expect(auditTermUse(used, Object.keys(TERM_CATALOG))).toEqual({
      missing: [],
      dead: [],
    });
  });

  it("puts each pill label and each phase label inside its term", () => {
    const pill = renderToStaticMarkup(createElement(LiveStatusPill, { live: true, replay: true }));
    expect(pill).toMatch(/<span [^>]*data-term="status\.replay"[^>]*>REPLAY<\/span>/);
    const timeline = renderToStaticMarkup(createElement(PhaseTimeline, { scrub: EMPTY_SCRUB }));
    for (const phase of TIMELINE_PHASES) {
      const pattern = new RegExp(`data-term="phase\\.${phase}"[^>]*><span[^>]*>${PHASE_LABELS[phase]}</span></span>`);
      expect(timeline, phase).toMatch(pattern);
    }
    expect(timeline).not.toContain(" title=\"");
  });
});

describe("the terms of the right panel and the metrics bar", () => {
  it("puts every task row's state word in its term, taking no focus inside the row's button", () => {
    const rows = renderPanel().match(/<button [^>]*class="[^"]*taskRow[^"]*"[^>]*>.*?<\/button>/gs) ?? [];
    const words = rows.map((row) => {
      const found = row.match(/<span [^>]*data-term="([^"]+)"[^>]*>([^<]+)<\/span><\/span><\/button>$/);
      return found === null ? null : [found[1], found[2]];
    });
    expect(words).toEqual([
      ["task.done", "Done"],
      ["task.in_progress", "In Progress"],
      ["blocked.task", "Blocked"],
      ["task.planned", "Planned"],
      ["task.partially_applied", "Partially applied"],
    ]);
    for (const row of rows) expect(row).not.toContain("tabindex");
  });

  it("gives each card's heading its term and the NowCard's Live badge its own", () => {
    const panel = renderPanel();
    expect(panel).toMatch(/<h2><span [^>]*data-term="panel\.agent_now"[^>]*>Agent is doing now<\/span><\/h2>/);
    expect(panel).toMatch(/<h2><span [^>]*data-term="panel\.decisions"[^>]*>Decision inbox<\/span><\/h2>/);
    expect(panel).toMatch(/<h2><span [^>]*data-term="panel\.activity"[^>]*>Activity<\/span><\/h2>/);
    expect(panel).toMatch(/<h2><span [^>]*data-term="panel\.tasks"[^>]*>Tasks<\/span><\/h2>/);
    expect(panel).toMatch(/<span [^>]*data-term="agent\.live"[^>]*>Live<\/span>/);
  });

  it("gives the six plain metrics' labels their terms and leaves the token tile's label bare", () => {
    const bar = renderToStaticMarkup(createElement(TopMetricsBar, { metrics: METRICS }));
    for (const [key, label] of [["open", "Open"], ["planned", "Planned"], ["done", "Done"],
      ["progress", "Progress"], ["tests", "Tests"], ["proof", "Proof"]]) {
      expect(bar, key).toMatch(new RegExp(`<span [^>]*data-term="metric\\.${key}"[^>]*>${label}</span>`));
    }
    expect(bar).toMatch(/<div class="[^"]*label[^"]*">Tokens<\/div>/);
  });

  it("a term inside a control writes its key and takes no focus", () => {
    const markup = renderToStaticMarkup(createElement(Term, { term: "task.done", insideControl: true, children: "Done" }));
    expect(collectDataTerms(markup)).toEqual(["task.done"]);
    expect(markup).not.toContain("tabindex");
  });
});

describe("the drift fixtures", () => {
  it("a term rendered without a catalog entry turns the first direction red", () => {
    const drifted = `${renderSurfaces()}\n${renderToStaticMarkup(createElement(Term, { term: "fixture.unlisted", children: "new" }))}`;
    const used = [...collectDataTerms(drifted), ...BROWSER_ONLY_TERMS.map(([term]) => term)];
    expect(auditTermUse(used, Object.keys(TERM_CATALOG))).toEqual({
      missing: ["fixture.unlisted"],
      dead: [],
    });
  });

  it("a catalog key no surface renders turns the second direction red", () => {
    const keys = [...Object.keys(TERM_CATALOG), "fixture.dead"];
    const used = [...collectDataTerms(renderSurfaces()), ...BROWSER_ONLY_TERMS.map(([term]) => term)];
    expect(auditTermUse(used, keys)).toEqual({
      missing: [],
      dead: ["fixture.dead"],
    });
  });
});
