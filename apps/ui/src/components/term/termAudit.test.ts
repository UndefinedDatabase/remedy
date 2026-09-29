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
import { TERM_CATALOG } from "../../api/terminology";
import { auditTermUse, collectDataTerms } from "../../api/terminologyAudit";
import { LiveStatusPill } from "../panels/LiveStatusPill";
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

/** Every surface this feature has put a term on, in each state that shows a different term. */
function renderSurfaces(): string {
  return [
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: false })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true, streamStatus: "delayed" })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true, streamStatus: "reconnecting" })),
    renderToStaticMarkup(createElement(LiveStatusPill, { live: true, replay: true })),
    renderToStaticMarkup(createElement(PhaseTimeline, { scrub: EMPTY_SCRUB })),
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
    ]);
  });

  it("is clean in both directions against the catalog", () => {
    expect(auditTermUse(collectDataTerms(renderSurfaces()), Object.keys(TERM_CATALOG))).toEqual({
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

describe("the drift fixtures", () => {
  it("a term rendered without a catalog entry turns the first direction red", () => {
    const drifted = `${renderSurfaces()}\n${renderToStaticMarkup(createElement(Term, { term: "fixture.unlisted", children: "new" }))}`;
    expect(auditTermUse(collectDataTerms(drifted), Object.keys(TERM_CATALOG))).toEqual({
      missing: ["fixture.unlisted"],
      dead: [],
    });
  });

  it("a catalog key no surface renders turns the second direction red", () => {
    const keys = [...Object.keys(TERM_CATALOG), "fixture.dead"];
    expect(auditTermUse(collectDataTerms(renderSurfaces()), keys)).toEqual({
      missing: [],
      dead: ["fixture.dead"],
    });
  });
});
