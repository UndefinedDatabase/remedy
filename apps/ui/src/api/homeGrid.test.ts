// F042 T003, DECISION F042 D4 — the reviewer's acceptance of the home grid's rules: which
// projects a page shows, and every word and tone one project's card carries, from the list
// entry and the summary card `project_summary` composes.
import { describe, expect, it } from "vitest";
import {
  DEGRADED_LINE,
  HOME_PAGE_SIZE,
  NO_FOLDER_HINT,
  NO_JOBS_LINE,
  NO_PROJECTS_LINE,
  SUMMARY_UNAVAILABLE_LINE,
  costTodayLine,
  homePage,
  projectCardOf,
  resultToneOf,
} from "./homeGrid";
import { decodeProjectSummary } from "./projectScope";
import type { ProjectEntry, ProjectSummary } from "./projectScope";

const entry: ProjectEntry = {
  id: "id-alpha", slug: "alpha", name: "Alpha", repo_path: "/work/alpha", repo_reachable: true, fix_it: null,
};
const summary: ProjectSummary = decodeProjectSummary({
  version: 1, project_id: "id-alpha", slug: "alpha", jobs: { active: 2, total: 3 },
  last_result: { job_id: "j1", title: "alpha newest", state: "blocked", headline: "The run is blocked." },
  cost_today: { day: "2026-09-29", value_usd: 0.25, basis: "actual", calls: 1 },
  decisions: { open_count: 5, peak_urgency: 3600 }, degraded: false,
})!;

describe("homePage", () => {
  const items = Array.from({ length: 30 }, (_, i) => `p${i + 1}`);

  it("shows twelve to a page", () => {
    expect(HOME_PAGE_SIZE).toBe(12);
    expect(homePage(items, 1)).toEqual({ items: items.slice(0, 12), page: 1, pages: 3 });
    expect(homePage(items, 3)).toEqual({ items: items.slice(24), page: 3, pages: 3 });
  });

  it("clamps a page out of range and reads an empty list as one empty page", () => {
    expect(homePage(items, 9).page).toBe(3);
    expect(homePage(items, 0).page).toBe(1);
    expect(homePage([], 1)).toEqual({ items: [], page: 1, pages: 1 });
  });
});

describe("resultToneOf", () => {
  it("draws each state in its family", () => {
    expect(["completed", "done", "running", "blocked", "failed", "cancelled", "planned", "paused", ""].map(resultToneOf))
      .toEqual(["done", "done", "current", "blocked", "blocked", "blocked", "open", "open", "none"]);
  });
});

describe("costTodayLine", () => {
  it("names the figure and its basis, and never an unmeasured zero", () => {
    expect(costTodayLine({ day: "d", value_usd: 0.25, basis: "actual", calls: 1 })).toBe("Cost today: $0.25");
    expect(costTodayLine({ day: "d", value_usd: 0.5, basis: "lower_bound", calls: 2 })).toBe("Cost today: at least $0.50");
    expect(costTodayLine({ day: "d", value_usd: null, basis: "absent", calls: 0 })).toBe("Cost today: not measured");
    expect(costTodayLine({ day: "d", value_usd: 0, basis: "absent", calls: 0 })).toBe("Cost today: not measured");
  });
});

describe("projectCardOf", () => {
  it("draws a project's card from its entry and its summary", () => {
    expect(projectCardOf(entry, summary)).toEqual({
      slug: "alpha", name: "Alpha", folderHint: "/work/alpha", reachable: true, fixIt: null,
      activeChip: "2 active", resultLine: "The run is blocked.", resultTone: "blocked",
      costLine: "Cost today: $0.25", decisionsChip: "5 open decisions", urgent: true, degraded: false,
    });
  });

  it("says a project with no job has none, and counts one decision in the singular", () => {
    const card = projectCardOf(entry, { ...summary, last_result: null, decisions: { open_count: 1, peak_urgency: 0 } });
    expect([card.resultLine, card.resultTone, card.decisionsChip, card.urgent]).toEqual([NO_JOBS_LINE, "none", "1 open decision", false]);
  });

  it("carries a moved folder's fix-it and a missing folder's hint", () => {
    const moved = projectCardOf({ ...entry, repo_reachable: false, fix_it: "Run: remedy project attach" }, summary);
    expect([moved.reachable, moved.fixIt]).toEqual([false, "Run: remedy project attach"]);
    expect(projectCardOf({ ...entry, repo_path: null }, summary).folderHint).toBe(NO_FOLDER_HINT);
  });

  it("says when some job records could not be read", () => {
    expect(projectCardOf(entry, { ...summary, degraded: true }).degraded).toBe(true);
    expect(DEGRADED_LINE).toBe("Some job records could not be read.");
  });

  it("draws an unreadable summary as its own absence and never as zeros", () => {
    expect(projectCardOf(entry, null)).toEqual({
      slug: "alpha", name: "Alpha", folderHint: "/work/alpha", reachable: true, fixIt: null,
      activeChip: "", resultLine: SUMMARY_UNAVAILABLE_LINE, resultTone: "none", costLine: "",
      decisionsChip: "", urgent: false, degraded: false,
    });
  });

  it("invites remedy init when no project is registered", () => {
    expect(NO_PROJECTS_LINE).toBe("No projects yet. Run remedy init in a project's folder to add it.");
  });
});
