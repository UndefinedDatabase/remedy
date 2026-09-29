// F043 T002 — the term audit's two readings over fixed inputs (DECISION F043 D1).
import { describe, expect, it } from "vitest";
import { auditTermUse, collectDataTerms } from "./terminologyAudit";

describe("collectDataTerms", () => {
  it("reads every data-term value once, sorted", () => {
    const markup = '<div><span class="a" data-term="status.live">LIVE</span>'
      + '<span data-term="phase.job">Job</span><span data-term="status.live">again</span></div>';
    expect(collectDataTerms(markup)).toEqual(["phase.job", "status.live"]);
  });

  it("does not read the tooltip's own data-term-tip attribute", () => {
    expect(collectDataTerms('<span data-term-tip="status.live" role="tooltip">x</span>')).toEqual([]);
  });

  it("reads an attribute written before or after others, and nothing from text", () => {
    const markup = '<span data-term="phase.test" tabindex="0">data-term="phase.fake"</span>'
      + '<span tabindex="0" data-term="phase.build">b</span>';
    expect(collectDataTerms(markup)).toEqual(["phase.build", "phase.test"]);
  });

  it("answers nothing for markup with no term", () => {
    expect(collectDataTerms("<p>plain</p>")).toEqual([]);
  });
});

describe("auditTermUse", () => {
  it("is clean when the used terms and the catalog keys are the same set", () => {
    expect(auditTermUse(["b", "a"], ["a", "b"])).toEqual({ missing: [], dead: [] });
  });

  it("names a used term the catalog lacks as missing", () => {
    expect(auditTermUse(["a", "z.new", "b"], ["a", "b"])).toEqual({ missing: ["z.new"], dead: [] });
  });

  it("names a catalog key nothing uses as dead", () => {
    expect(auditTermUse(["a"], ["c.old", "a", "b.old"])).toEqual({ missing: [], dead: ["b.old", "c.old"] });
  });

  it("reports both directions at once", () => {
    expect(auditTermUse(["x", "a"], ["a", "y"])).toEqual({ missing: ["x"], dead: ["y"] });
  });
});
