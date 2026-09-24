import { describe, expect, it } from "vitest";
import {
  brainLedgerLive,
  brainLedgerPage,
  brainLedgerPrefix,
  brainLedgerReceived,
  brainLedgerRequest,
  emptyBrainLedger,
  initialBrainLedgerLoad,
  mergeBrainRows,
  nextBrainLedgerCursor,
} from "./brainLedger";
import type { BrainLedger, BrainLedgerLoad } from "./brainLedger";
import { rebuildBrainModel } from "./brainReducer";
import { dashboardBrainSeeds } from "./brainView";
import { row } from "./brainReducer.fixtures";
import { BRAIN_DEMO_FRAMES, BRAIN_DEMO_JOB_ID, BRAIN_DEMO_TASKS, brainDemoRows } from "./brainDemoRecording";

/** `BrainEventRow` fields alone, so a `toEqual` against `row(...)` is not
 *  defeated by the extra fields `feedRowOf` puts on a real `FeedRow`. */
function eventFields(rows: readonly { seq: number; kind: string; outcome: string; taskId: string }[]) {
  return rows.map(({ seq, kind, outcome, taskId }) => ({ seq, kind, outcome, taskId }));
}

describe("mergeBrainRows", () => {
  it("sorts the merged rows by seq", () => {
    const merged = mergeBrainRows(emptyBrainLedger(), [row(2, "task_run_started", "t1"), row(0, "task_run_started", "t1"), row(1, "task_run_started", "t1")], null);
    expect(merged.rows.map((r) => r.seq)).toEqual([0, 1, 2]);
  });

  it("dedupes by seq with the already-held row winning", () => {
    const held = row(0, "task_run_started", "t1");
    const ledger: BrainLedger = { rows: [held], known: 1 };
    const merged = mergeBrainRows(ledger, [row(0, "task_run_started", "t2")], null);
    expect(merged.rows).toEqual([held]);
    expect(merged.rows[0]).toBe(held);
  });

  it("raises known to one past the highest seq now held", () => {
    const merged = mergeBrainRows(emptyBrainLedger(), [row(4, "task_run_started", "t1")], null);
    expect(merged.known).toBe(5);
  });

  it("raises known to the caller's knownLength when that is higher", () => {
    const merged = mergeBrainRows(emptyBrainLedger(), [row(0, "task_run_started", "t1")], 10);
    expect(merged.known).toBe(10);
  });

  it("returns the SAME object when nothing changed", () => {
    const ledger = mergeBrainRows(emptyBrainLedger(), [row(0, "task_run_started", "t1")], null);
    expect(mergeBrainRows(ledger, [row(0, "task_run_started", "t1")], null)).toBe(ledger);
    expect(mergeBrainRows(ledger, [], null)).toBe(ledger);
    expect(mergeBrainRows(ledger, [], 1)).toBe(ledger);
  });
});

describe("brainLedgerPrefix", () => {
  it("stops at the first hole", () => {
    const ledger: BrainLedger = { rows: [row(0, "a"), row(1, "a"), row(3, "a")], known: 4 };
    expect(brainLedgerPrefix(ledger).map((r) => r.seq)).toEqual([0, 1]);
  });

  it("is empty when seq 0 itself is missing", () => {
    const ledger: BrainLedger = { rows: [row(1, "a"), row(2, "a")], known: 3 };
    expect(brainLedgerPrefix(ledger)).toEqual([]);
  });
});

describe("nextBrainLedgerCursor", () => {
  it("is 0 before any read", () => {
    expect(nextBrainLedgerCursor(emptyBrainLedger())).toBe(0);
  });

  it("is the first missing seq inside [0, known)", () => {
    const ledger: BrainLedger = { rows: [row(0, "a"), row(1, "a"), row(3, "a"), row(4, "a")], known: 5 };
    expect(nextBrainLedgerCursor(ledger)).toBe(2);
  });

  it("is null once every seq the client knows about is held", () => {
    const ledger: BrainLedger = { rows: [row(0, "a"), row(1, "a"), row(2, "a")], known: 3 };
    expect(nextBrainLedgerCursor(ledger)).toBeNull();
  });
});

describe("brainLedgerPage", () => {
  it("reads rows and cursor from a payload shaped like _build_events_since_json's", () => {
    const payload = {
      version: 1,
      job_id: "job-x",
      cursor: "3",
      events: [
        { seq: 0, event: "task_run_started", timestamp: "t0", outcome: "", task_id: "t1" },
        { seq: 1, event: "task_round_completed", timestamp: "t1", outcome: "pass", task_id: "t1" },
      ],
    };
    const page = brainLedgerPage(payload);
    expect(eventFields(page.rows)).toEqual([
      row(0, "task_run_started", "t1"),
      row(1, "task_round_completed", "t1", "pass"),
    ]);
    expect(page.known).toBe(3);
  });

  it("reads null known for a malformed, missing or absent cursor", () => {
    expect(brainLedgerPage({ cursor: "not a number", events: [] }).known).toBeNull();
    expect(brainLedgerPage({ events: [] }).known).toBeNull();
    expect(brainLedgerPage(null)).toEqual({ rows: [], known: null });
  });
});

describe("the loader", () => {
  it("request, then received fills it, then request is null", () => {
    const load = initialBrainLedgerLoad();
    const cursor = brainLedgerRequest(load);
    expect(cursor).toBe(0);
    const payload = {
      cursor: "3",
      events: [
        { seq: 0, event: "task_run_started", timestamp: "", outcome: "", task_id: "t1" },
        { seq: 1, event: "task_round_completed", timestamp: "", outcome: "pass", task_id: "t1" },
        { seq: 2, event: "task_run_completed", timestamp: "", outcome: "pass", task_id: "t1" },
      ],
    };
    const filled = brainLedgerReceived(load, cursor as number, payload);
    expect(brainLedgerPrefix(filled.ledger)).toHaveLength(3);
    expect(brainLedgerRequest(filled)).toBeNull();
  });

  it("an empty or failed read at cursor c stalls c", () => {
    const afterGap = mergeBrainRows(
      emptyBrainLedger(),
      [row(0, "a"), row(1, "a"), row(5, "a"), row(6, "a"), row(7, "a")],
      null,
    );
    const load: BrainLedgerLoad = { ledger: afterGap, stalled: null };
    const cursor = brainLedgerRequest(load);
    expect(cursor).toBe(2);

    const stalledByEmpty = brainLedgerReceived(load, cursor as number, { cursor: "8", events: [] });
    expect(stalledByEmpty.stalled).toBe(2);
    expect(brainLedgerRequest(stalledByEmpty)).toBeNull();

    const stalledByFailure = brainLedgerReceived(load, cursor as number, null);
    expect(stalledByFailure.stalled).toBe(2);
    expect(brainLedgerRequest(stalledByFailure)).toBeNull();
  });

  it("a live row that changes the ledger clears the stall", () => {
    const afterGap = mergeBrainRows(
      emptyBrainLedger(),
      [row(0, "a"), row(1, "a"), row(5, "a"), row(6, "a"), row(7, "a")],
      null,
    );
    const stalled: BrainLedgerLoad = { ledger: afterGap, stalled: 2 };
    const cleared = brainLedgerLive(stalled, [row(2, "a")]);
    expect(cleared.stalled).toBeNull();
    expect(brainLedgerRequest(cleared)).toBe(3);
  });
});

describe("THE GAP SCENARIO (brainDemoRecording)", () => {
  it("holds the prefix at the state before the hole, then matches the whole model once it is filled", () => {
    const demoRows = brainDemoRows();
    const seeds = dashboardBrainSeeds(BRAIN_DEMO_TASKS);

    let load = brainLedgerLive(initialBrainLedgerLoad(), [...demoRows.slice(0, 2), ...demoRows.slice(5, 8)]);
    expect(eventFields(brainLedgerPrefix(load.ledger))).toEqual(eventFields(demoRows.slice(0, 2)));
    expect(brainLedgerRequest(load)).toBe(2);

    // While the hole is open the model holds nothing born at seq 5 or later.
    const modelWhileOpen = rebuildBrainModel(BRAIN_DEMO_JOB_ID, seeds, brainLedgerPrefix(load.ledger));
    expect(modelWhileOpen.nodes.some((n) => n.seq >= 5)).toBe(false);

    const page = { cursor: "8", events: BRAIN_DEMO_FRAMES.slice(2, 5).map((f) => f.event) };
    load = brainLedgerReceived(load, 2, page);

    const filledPrefix = brainLedgerPrefix(load.ledger);
    expect(filledPrefix).toHaveLength(8);
    const filledModel = rebuildBrainModel(BRAIN_DEMO_JOB_ID, seeds, filledPrefix);
    const wholeModel = rebuildBrainModel(BRAIN_DEMO_JOB_ID, seeds, demoRows);
    expect(filledModel).toEqual(wholeModel);
  });
});

describe("THE MID-LEDGER JOIN (brainDemoRecording)", () => {
  it("requests from the start and holds no prefix until a page from cursor 0 fills it", () => {
    const demoRows = brainDemoRows();
    let load = brainLedgerLive(initialBrainLedgerLoad(), demoRows.slice(4, 8));
    expect(brainLedgerRequest(load)).toBe(0);
    expect(brainLedgerPrefix(load.ledger)).toEqual([]);

    const page = { cursor: "8", events: BRAIN_DEMO_FRAMES.slice(0, 4).map((f) => f.event) };
    load = brainLedgerReceived(load, 0, page);
    expect(brainLedgerPrefix(load.ledger)).toHaveLength(8);
  });
});
