import { describe, it, expect } from "vitest";
import { feedRowOf as projectRow } from "./feedRow";
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";

// The cases below predate the arrival stamp and assert nothing about it, so
// they call through a shim supplying a fixed one. The stamp's own contract is
// the last case in this file, which calls `projectRow` directly.
function feedRowOf(frame: { seq: number; event: unknown }) {
  return projectRow(frame, 0);
}

/** A frame as `framesOf` builds one: the envelope IS the frame's event field. */
function frameOf(seq: number, envelope: unknown) {
  return { seq, event: envelope };
}

describe("feedRowOf over a well-formed envelope", () => {
  it("carries the frame's own seq rather than any envelope field", () => {
    const row = feedRowOf(frameOf(41, { seq: 7, event: "task_run_started" }));
    expect(row.seq).toBe(41);
  });

  it("resolves the kind from the envelope's own event field", () => {
    const row = feedRowOf(frameOf(1, { event: "task_run_started" }));
    expect(row.kind).toBe("task_run_started");
    expect(row.line).toBe(STREAM_EVENT_CATALOG["task_run_started"]);
    expect(row.known).toBe(true);
  });

  it("carries timestamp and outcome through unchanged", () => {
    const row = feedRowOf(frameOf(2, {
      event: "task_run_started", timestamp: "2026-08-22T10:00:00Z", outcome: "ok",
    }));
    expect(row.timestamp).toBe("2026-08-22T10:00:00Z");
    expect(row.outcome).toBe("ok");
  });
});

describe("feedRowOf on envelopes the client does not control", () => {
  it("an uncatalogued kind still yields a row, on the generic line", () => {
    const row = feedRowOf(frameOf(3, { event: "some_runtime_computed_kind" }));
    expect(row.line).toBe("some_runtime_computed_kind event");
    expect(row.known).toBe(false);
    expect(row.seq).toBe(3);
  });

  it("a non-object event field yields a row rather than throwing", () => {
    for (const broken of [null, "a string", 7, undefined]) {
      const row = feedRowOf(frameOf(4, broken));
      expect(row.kind).toBe("");
      expect(row.line).toBe("unknown event");
      expect(row.known).toBe(false);
    }
  });

  it("missing string fields read as the empty string, never undefined", () => {
    const row = feedRowOf(frameOf(5, { event: "task_run_started" }));
    expect(row.timestamp).toBe("");
    expect(row.outcome).toBe("");
  });

  it("a non-string field is rejected rather than coerced", () => {
    const row = feedRowOf(frameOf(6, { event: 42, timestamp: 1, outcome: [] }));
    expect(row.kind).toBe("");
    expect(row.timestamp).toBe("");
    expect(row.outcome).toBe("");
  });

  it("a kind colliding with an Object prototype member is not reported known", () => {
    const row = feedRowOf(frameOf(7, { event: "constructor" }));
    expect(row.known).toBe(false);
    expect(row.line).toBe("constructor event");
  });

  it("carries the arrival stamp the caller supplies, unchanged", () => {
    const row = projectRow(frameOf(8, { event: "task_run_started" }), 1717);
    expect(row.receivedAtMs).toBe(1717);
  });
});
