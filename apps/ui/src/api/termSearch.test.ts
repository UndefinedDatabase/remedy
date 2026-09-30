// F043 T003 — the '?' panel's pure rules (DECISION F043 D3).
import { describe, expect, it } from "vitest";
import { TERM_CATALOG } from "./terminology";
import type { TermEntry } from "./terminology";
import { TERM_PLACES, searchTermEntries, termPlace } from "./termSearch";

function entry(title: string, body: string): TermEntry {
  return { title, body, source: "docs/x.md", anchor: "x" };
}

const SMALL: Readonly<Record<string, TermEntry>> = {
  "b.two": entry("Planned", "Not started yet."),
  "a.one": entry("Planned", "Tasks that have not started."),
  "c.three": entry("Live", "Receiving events as they happen."),
};

describe("searchTermEntries", () => {
  it("keeps every entry for an empty or blank query, sorted by title and then key", () => {
    const want = ["c.three", "a.one", "b.two"];
    expect(searchTermEntries(SMALL, "").map((row) => row.key)).toEqual(want);
    expect(searchTermEntries(SMALL, "   ").map((row) => row.key)).toEqual(want);
  });

  it("matches the title or the body, ignoring case", () => {
    expect(searchTermEntries(SMALL, "LIVE").map((row) => row.key)).toEqual(["c.three"]);
    expect(searchTermEntries(SMALL, "tasks").map((row) => row.key)).toEqual(["a.one"]);
  });

  it("keeps only entries that hold every word of the query", () => {
    expect(searchTermEntries(SMALL, "planned started").map((row) => row.key)).toEqual(["a.one", "b.two"]);
    expect(searchTermEntries(SMALL, "planned events").map((row) => row.key)).toEqual([]);
  });

  it("does not search the key or the source", () => {
    expect(searchTermEntries(SMALL, "three")).toEqual([]);
    expect(searchTermEntries(SMALL, "docs")).toEqual([]);
  });

  it("lists the real catalog whole, and finds the decision inbox by its urgency", () => {
    expect(searchTermEntries(TERM_CATALOG, "").map((row) => row.key).sort()).toEqual(Object.keys(TERM_CATALOG).sort());
    expect(searchTermEntries(TERM_CATALOG, "urgent").map((row) => row.key)).toEqual(["panel.decisions"]);
  });
});

describe("termPlace", () => {
  it("places every catalog entry, so a new family cannot enter the panel without a place", () => {
    const unplaced = Object.keys(TERM_CATALOG).filter((key) => termPlace(key) === "");
    expect(unplaced).toEqual([]);
  });

  it("tells the two entries titled Done apart", () => {
    expect(termPlace("metric.done")).toBe("Metrics bar");
    expect(termPlace("task.done")).toBe("Task list");
  });

  it("answers nothing for a family the table does not name, an inherited name included", () => {
    expect(termPlace("fixture.x")).toBe("");
    expect(termPlace("toString.x")).toBe("");
    expect(Object.keys(TERM_PLACES).sort()).toEqual(["agent", "graph", "metric", "panel", "phase", "status", "task"]);
  });
});
