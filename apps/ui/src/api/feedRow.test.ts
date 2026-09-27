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


describe("feedRowOf on a steering acknowledgement", () => {
  const understood = "the builder follows “Use pnpm.” from round 2 of task task-1 on";

  it("shows the round and the restatement instead of the catalog line", () => {
    const row = feedRowOf(frameOf(9, {
      event: "steering_message_consumed", task_id: "task-1",
      steering: { message_id: "sm-0001", round_number: 2, understood },
    }));
    expect(row.line).toBe(`Steering taken in at round 2: ${understood}.`);
    expect(row.known).toBe(true);
    expect(row.taskId).toBe("task-1");
  });

  it("keeps the catalog line when the acknowledgement field is malformed", () => {
    const row = feedRowOf(frameOf(10, {
      event: "steering_message_consumed", steering: { message_id: "sm-0001" },
    }));
    expect(row.line).toBe(STREAM_EVENT_CATALOG["steering_message_consumed"]);
  });
});

describe("feedRowOf's attemptId (DECISION F288 D3 (2))", () => {
  it("reads attempt_id from the envelope", () => {
    const row = feedRowOf(frameOf(11, {
      event: "task_run_started", attempt_id: "cycle-1",
    }));
    expect(row.attemptId).toBe("cycle-1");
  });

  it("is the empty string when absent", () => {
    const row = feedRowOf(frameOf(12, { event: "task_run_started" }));
    expect(row.attemptId).toBe("");
  });

  it("is the empty string when not a string", () => {
    const row = feedRowOf(frameOf(13, {
      event: "task_run_started", attempt_id: 42,
    }));
    expect(row.attemptId).toBe("");
  });
});

describe("feedRowOf on a steering note (DECISION F030 D3)", () => {
  it("shows the operator's own text, verbatim, as the operator's own row", () => {
    const row = feedRowOf(frameOf(19, {
      event: "steering_message_received", task_id: "task-1",
      note: { message_id: "sm-0002", text: "watch the budget", channel: "cli",
              task_id: "task-1" },
    }));
    expect(row.line).toBe("watch the budget");
    expect(row.author).toBe("operator");
    expect(row.taskId).toBe("task-1");
  });

  it("keeps the catalog line and gets no author when the note field is malformed", () => {
    const row = feedRowOf(frameOf(20, {
      event: "steering_message_received", note: { message_id: "sm-0003" },
    }));
    expect(row.line).toBe(STREAM_EVENT_CATALOG["steering_message_received"]);
    expect(row.author).toBeUndefined();
  });

  it("gives every other row no author", () => {
    const row = feedRowOf(frameOf(21, { event: "task_run_started" }));
    expect(row.author).toBeUndefined();
  });
});

describe("feedRowOf's planTaskIds (DECISION F288 D3 (2))", () => {
  it("keeps the order of plan.task_ids' string entries", () => {
    const row = feedRowOf(frameOf(14, {
      event: "plan_approved", plan: { task_ids: ["task-1", "task-2"] },
    }));
    expect(row.planTaskIds).toEqual(["task-1", "task-2"]);
  });

  it("drops non-string entries while keeping the rest in order", () => {
    const row = feedRowOf(frameOf(15, {
      event: "plan_approved", plan: { task_ids: ["task-1", 7, "task-2", null] },
    }));
    expect(row.planTaskIds).toEqual(["task-1", "task-2"]);
  });

  it("is [] when plan is absent", () => {
    const row = feedRowOf(frameOf(16, { event: "task_run_started" }));
    expect(row.planTaskIds).toEqual([]);
  });

  it("is [] when plan is not an object", () => {
    const row = feedRowOf(frameOf(17, { event: "plan_approved", plan: "nope" }));
    expect(row.planTaskIds).toEqual([]);
  });

  it("is [] when plan.task_ids is not an array", () => {
    const row = feedRowOf(frameOf(18, {
      event: "plan_approved", plan: { task_ids: "task-1" },
    }));
    expect(row.planTaskIds).toEqual([]);
  });
});
