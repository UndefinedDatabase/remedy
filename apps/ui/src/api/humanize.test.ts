import { describe, it, expect } from "vitest";
import { humanizeStreamEvent } from "./humanize";
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";

describe("humanizeStreamEvent over the catalog", () => {
  it("a catalogued kind renders its catalog line and is known", () => {
    const result = humanizeStreamEvent("verification_passed");
    expect(result.line).toBe(STREAM_EVENT_CATALOG["verification_passed"]);
    expect(result.known).toBe(true);
  });

  it("every catalog entry humanizes to its own value", () => {
    const wrong = Object.entries(STREAM_EVENT_CATALOG).filter(
      ([kind, line]) => humanizeStreamEvent(kind).line !== line,
    );
    expect(wrong).toHaveLength(0);
  });

  it("every catalog entry is reported as known", () => {
    const unknown = Object.keys(STREAM_EVENT_CATALOG).filter(
      kind => humanizeStreamEvent(kind).known === false,
    );
    expect(unknown).toHaveLength(0);
  });
});

describe("humanizeStreamEvent generic path", () => {
  it("an uncatalogued kind renders the generic line naming itself", () => {
    const result = humanizeStreamEvent("some_runtime_computed_kind");
    expect(result.line).toBe("some_runtime_computed_kind event");
    expect(result.known).toBe(false);
  });

  it("an uncatalogued kind is never dropped, so the line is non-empty", () => {
    expect(humanizeStreamEvent("x").line.length).toBeGreaterThan(0);
  });

  it("a kind that names an Object.prototype member is not reported as known", () => {
    const result = humanizeStreamEvent("toString");
    expect(result.known).toBe(false);
    expect(result.line).toBe("toString event");
  });

  it("the empty string renders the unknown line rather than a bare ' event'", () => {
    const result = humanizeStreamEvent("");
    expect(result.line).toBe("unknown event");
    expect(result.known).toBe(false);
  });

  it("a non-string kind renders the unknown line", () => {
    for (const kind of [undefined, null, 7, {}, ["tool_use"]]) {
      const result = humanizeStreamEvent(kind);
      expect(result.line).toBe("unknown event");
      expect(result.known).toBe(false);
    }
  });
});
