// T5_F292 T003 — the hunk decisions panel's first markup, rendered with `renderToStaticMarkup`
// (DECISION F292 D7). The read runs in an effect, which a static render never reaches, so this
// pins what the panel shows before the record arrives and for a diff it cannot decide; the
// headless render drives the rest.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { DiffEnvelope } from "../../api/diffViewModel";
import { HunkDecisionPanel } from "./HunkDecisionPanel";

function envelope(overrides: Partial<DiffEnvelope> = {}): DiffEnvelope {
  return {
    version: 1, scope: "task_run", taskId: "T001", source: "task_runs/T001/safe.diff", available: true,
    reason: null, truncated: false, taskRunIds: ["T001"],
    files: [{ path: "src/a.py", oldPath: null, status: "modified", stats: { added: 1, deleted: 1 }, note: null,
      hunks: [{ id: "h1", header: "@@ -1 +1 @@", oldStart: 1, newStart: 1, lines: [] }] }],
    ...overrides,
  };
}

function render(env: DiffEnvelope): string {
  return renderToStaticMarkup(createElement(HunkDecisionPanel, {
    envelope: env, target: { jobId: "0123456789abcdef", serverToken: "token" } }));
}

describe("the hunk decisions panel", () => {
  it("is a region named Hunk decisions that says it is reading the record, with Record disabled until it arrives", () => {
    const markup = render(envelope());
    expect(markup).toMatch(/^<section [^>]*aria-label="Hunk decisions"[^>]*data-ui="hunk-decisions"><h3>Hunk decisions<\/h3>/);
    expect(markup).toContain("Reading the decisions already recorded for this change…");
    expect(markup).toMatch(/<button type="button"[^>]*disabled=""[^>]*title="Reading the decisions already recorded for this change…"[^>]*>Record decisions<\/button>/);
    expect(markup).not.toContain("data-hunk-id");
  });

  it("says why a cut-short diff cannot be decided and offers no Record", () => {
    const markup = render(envelope({ truncated: true }));
    expect(markup).toContain("This change was cut short, so not every hunk can be named; it cannot be decided hunk by hunk.");
    expect(markup).not.toContain("Record decisions");
  });

  it("says no change is available for an absent diff", () => {
    expect(render(envelope({ available: false, files: [] }))).toContain("No change is available to decide.");
  });
});
