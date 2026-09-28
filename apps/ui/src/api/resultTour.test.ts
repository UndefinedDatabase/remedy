import { describe, it, expect } from "vitest";
import {
  MAX_TOUR_STOPS,
  TOUR_ANCHOR_KINDS,
  TOUR_EMPTY_LINE,
  TOUR_UNREADABLE_LINE,
  decodeTourView,
  tourAnchorLabel,
  tourCanShow,
  tourDiffRowKey,
  tourGeneratorLabel,
  tourNeighbours,
  tourPanelState,
  tourProgress,
  tourStepLabel,
  tourViewPath,
} from "./resultTour";
import { diffEnvelopePath, loadTourView } from "./remedyApi";

function stop(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    title: "How the run ended",
    body: "State: completed.",
    anchor: { kind: "evidence", ref: "report.md" },
    ...overrides,
  };
}

function tour(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    schema: "remedy.tour.v1",
    job_id: "job-1",
    generator: "fallback",
    stops: [stop()],
    dropped: [],
    ...overrides,
  };
}

function view(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return { stored: true, version: 1, tour: tour(), error: "", ...overrides };
}

describe("decodeTourView", () => {
  it("reads a wire-shaped view", () => {
    const decoded = decodeTourView(view())!;
    expect(decoded.stored).toBe(true);
    expect(decoded.version).toBe(1);
    expect(decoded.error).toBe("");
    expect(decoded.tour).toEqual({
      schema: "remedy.tour.v1", jobId: "job-1", generator: "fallback",
      stops: [{ title: "How the run ended", body: "State: completed.",
        anchor: { kind: "evidence", ref: "report.md" } }],
      dropped: [],
    });
  });

  it("reads a view with an error and no stored tour", () => {
    const decoded = decodeTourView(view({ stored: false, version: 0, error: "boom" }))!;
    expect(decoded.stored).toBe(false);
    expect(decoded.version).toBe(0);
    expect(decoded.error).toBe("boom");
  });

  it.each([
    ["no object", null],
    ["a list", []],
    ["a wrong schema", view({ tour: tour({ schema: "remedy.tour.v2" }) })],
    ["an unknown anchor kind", view({
      tour: tour({ stops: [stop({ anchor: { kind: "unknown", ref: "x" } })] }) })],
    ["an empty anchor ref", view({
      tour: tour({ stops: [stop({ anchor: { kind: "node", ref: "" } })] }) })],
    ["nine stops", view({
      tour: tour({ stops: Array.from({ length: 9 }, () => stop()) }) })],
    ["a negative version", view({ version: -1 })],
    ["a fractional version", view({ version: 1.5 })],
    ["a missing dropped entry key", view({
      tour: tour({ dropped: [{ title: "x" }] }) })],
  ])("refuses the whole view for %s", (_label, raw) => {
    expect(decodeTourView(raw)).toBeNull();
  });

  it("accepts exactly MAX_TOUR_STOPS stops", () => {
    const decoded = decodeTourView(view({
      tour: tour({ stops: Array.from({ length: MAX_TOUR_STOPS }, () => stop()) }) }));
    expect(decoded?.tour.stops.length).toBe(MAX_TOUR_STOPS);
  });
});

describe("tourViewPath", () => {
  it("builds the route with the job id and token encoded", () => {
    expect(tourViewPath({ jobId: "a/b", token: "t&k" }))
      .toBe("/api/jobs/a%2Fb/tour?token=t%26k");
  });
});

describe("tourPanelState", () => {
  const stopsView = decodeTourView(view())!;
  const emptyView = decodeTourView(view({ tour: tour({ stops: [] }) }))!;

  it("reads loading while not loaded, whatever the view", () => {
    expect(tourPanelState(null, false)).toEqual({ kind: "loading" });
    expect(tourPanelState(stopsView, false)).toEqual({ kind: "loading" });
  });

  it("reads unreadable for a loaded null view", () => {
    expect(tourPanelState(null, true)).toEqual({ kind: "unreadable", line: TOUR_UNREADABLE_LINE });
  });

  it("reads empty for a loaded view with no stops", () => {
    expect(tourPanelState(emptyView, true)).toEqual({ kind: "empty", line: TOUR_EMPTY_LINE });
  });

  it("reads stops, in the tour's own order, for a loaded view with stops", () => {
    expect(tourPanelState(stopsView, true)).toEqual({ kind: "stops", stops: stopsView.tour.stops });
  });
});

describe("tourNeighbours", () => {
  it("answers null past both ends", () => {
    expect(tourNeighbours(3, 0)).toEqual({ previous: null, next: 1 });
    expect(tourNeighbours(3, 1)).toEqual({ previous: 0, next: 2 });
    expect(tourNeighbours(3, 2)).toEqual({ previous: 1, next: null });
  });

  it("answers null at both ends for a single stop", () => {
    expect(tourNeighbours(1, 0)).toEqual({ previous: null, next: null });
  });
});

describe("tourStepLabel", () => {
  it("labels the step one-based", () => {
    expect(tourStepLabel(5, 0)).toBe("Stop 1 of 5");
    expect(tourStepLabel(5, 4)).toBe("Stop 5 of 5");
  });
});

describe("tourProgress", () => {
  it("marks every stop done, current or ahead", () => {
    expect(tourProgress(3, 1)).toEqual(["done", "current", "ahead"]);
    expect(tourProgress(3, 0)).toEqual(["current", "ahead", "ahead"]);
    expect(tourProgress(3, 2)).toEqual(["done", "done", "current"]);
  });
});

describe("tourAnchorLabel", () => {
  it("labels every anchor kind", () => {
    expect(tourAnchorLabel({ kind: "node", ref: "T1" })).toBe("Task T1");
    expect(tourAnchorLabel({ kind: "diff", ref: "a.py" })).toBe("Changed file a.py");
    expect(tourAnchorLabel({ kind: "evidence", ref: "report.md" })).toBe("Evidence file report.md");
    expect(tourAnchorLabel({ kind: "command", ref: "pytest" })).toBe("Command pytest");
  });

  it("names every kind in TOUR_ANCHOR_KINDS", () => {
    expect(TOUR_ANCHOR_KINDS).toEqual(["node", "diff", "evidence", "command"]);
  });
});

describe("tourGeneratorLabel", () => {
  it("credits the summary model when it wrote the tour", () => {
    expect(tourGeneratorLabel("summary-role"))
      .toBe("Written by the summary model and checked against the job's records");
  });

  it("reads mechanical for any other generator", () => {
    expect(tourGeneratorLabel("fallback")).toBe("Built from the job's records");
    expect(tourGeneratorLabel("")).toBe("Built from the job's records");
  });
});

describe("tourCanShow", () => {
  it("holds for a node and a diff anchor", () => {
    expect(tourCanShow({ kind: "node", ref: "T1" })).toBe(true);
    expect(tourCanShow({ kind: "diff", ref: "a.py" })).toBe(true);
  });

  it("fails for an evidence and a command anchor", () => {
    expect(tourCanShow({ kind: "evidence", ref: "report.md" })).toBe(false);
    expect(tourCanShow({ kind: "command", ref: "pytest" })).toBe(false);
  });
});

describe("tourDiffRowKey", () => {
  const summaries = [
    { path: "a.py", rowKey: "file:0" },
    { path: "b.py", rowKey: "file:1" },
    { path: "a.py", rowKey: "file:2" },
  ];

  it("answers the FIRST matching summary's key", () => {
    expect(tourDiffRowKey(summaries, "a.py")).toBe("file:0");
  });

  it("answers null when no summary names the path", () => {
    expect(tourDiffRowKey(summaries, "c.py")).toBeNull();
  });
});

describe("diffEnvelopePath's job scope", () => {
  it("reads the job's whole diff for an empty task id", () => {
    expect(diffEnvelopePath({ jobId: "j1", token: "tok", taskId: "" }))
      .toBe("/api/jobs/j1/diff?token=tok");
  });
});

describe("loadTourView", () => {
  it("reads the route through the injected fetcher", async () => {
    const asked: string[] = [];
    const decoded = await loadTourView({ jobId: "j1", token: "tok" }, async (path) => {
      asked.push(path);
      return view();
    });
    expect(asked).toEqual(["/api/jobs/j1/tour?token=tok"]);
    expect(decoded?.tour.stops.length).toBe(1);
  });

  it("answers null, never throws, when the fetcher rejects", async () => {
    const decoded = await loadTourView({ jobId: "j1", token: "tok" }, async () => {
      throw new Error("offline");
    });
    expect(decoded).toBeNull();
  });
});
