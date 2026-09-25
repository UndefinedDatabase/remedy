// Goldens for the phase timeline's pure half (T5_F024.md T001, DECISION F024 D1).
// Every expected reading below is a literal, HAND-DERIVED from the phase mapping
// table and the rules in phaseMapping.ts, never computed by the code under test.
import { describe, expect, it } from "vitest";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import {
  GOLDEN_A_JOB_ID,
  GOLDEN_A_ROWS,
  GOLDEN_A_TASKS,
  GOLDEN_B_JOB_ID,
  GOLDEN_B_ROWS,
  GOLDEN_B_TASKS,
  row,
} from "../graph/brainReducer.fixtures";
import type { BrainTaskSeed } from "../graph/brainOntology";
import {
  extractSubGlyphs,
  markerPhaseOf,
  orderedLedger,
  PHASE_MARKER_TABLE,
  readPhases,
  SUB_GLYPH_TABLE,
  timelineSeedOf,
  TIMELINE_PHASES,
} from "./phaseMapping";

const T1: readonly BrainTaskSeed[] = [{ id: "t1", status: "pending", rank: 0 }];

const DEMO_TASKS: readonly BrainTaskSeed[] = [
  { id: "a7a8f67f1b9a4814", status: "pending", rank: 0 },
  { id: "1965fb3f26b64fe7", status: "pending", rank: 1 },
];

describe("the phase mapping table", () => {
  it("names the six stops in the bar's order", () => {
    expect(TIMELINE_PHASES).toEqual(["job", "planning", "build", "test", "review", "finalized"]);
  });

  it("maps the measured writers and nothing for Job or Finalized", () => {
    expect(PHASE_MARKER_TABLE).toEqual({
      planning_started: "planning",
      planning_completed: "planning",
      planning_failed: "planning",
      task_run_started: "build",
      builder_started: "build",
      builder_completed: "build",
      test_run_requested: "test",
      test_run_started: "test",
      test_run_completed: "test",
      test_run_blocked: "test",
      test_run_timed_out: "test",
      verification_passed: "test",
      verification_failed: "test",
      task_round_completed: "review",
    });
  });

  it("marks Review only for a round that carries a reviewer's verdict", () => {
    expect(markerPhaseOf(row(1, "task_round_completed", "t1", "pass"))).toBe("review");
    expect(markerPhaseOf(row(1, "task_round_completed", "t1", "needs_repair"))).toBe("review");
    expect(markerPhaseOf(row(1, "task_round_completed", "t1", "no_review"))).toBeNull();
    expect(markerPhaseOf(row(1, "task_round_completed", "t1", ""))).toBeNull();
  });

  it("marks nothing for an unknown, empty or prototype-named kind", () => {
    expect(markerPhaseOf(row(1, "budget.tick"))).toBeNull();
    expect(markerPhaseOf(row(1, ""))).toBeNull();
    expect(markerPhaseOf(row(1, "toString"))).toBeNull();
    expect(markerPhaseOf(row(1, "job_stopped", "", "stopped"))).toBeNull();
  });
});

describe("phase boundaries per fixture", () => {
  it("golden A: build, a verdict, a late test and the task's pass", () => {
    expect(readPhases(GOLDEN_A_JOB_ID, GOLDEN_A_TASKS, GOLDEN_A_ROWS)).toEqual({
      current: "finalized",
      lastSeq: 4,
      spans: [
        { phase: "job", startSeq: 1, endSeq: 1 },
        { phase: "planning", startSeq: 1, endSeq: 1 },
        { phase: "build", startSeq: 1, endSeq: 2 },
        { phase: "test", startSeq: 2, endSeq: 2 },
        { phase: "review", startSeq: 2, endSeq: 4 },
        { phase: "finalized", startSeq: 4, endSeq: null },
      ],
    });
  });

  it("golden B: a stop, a repair and an open decision never finalize", () => {
    expect(readPhases(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, GOLDEN_B_ROWS)).toEqual({
      current: "review",
      lastSeq: 9,
      spans: [
        { phase: "job", startSeq: 1, endSeq: 1 },
        { phase: "planning", startSeq: 1, endSeq: 1 },
        { phase: "build", startSeq: 1, endSeq: 2 },
        { phase: "test", startSeq: 2, endSeq: 2 },
        { phase: "review", startSeq: 2, endSeq: null },
      ],
    });
  });

  it("the demo recording finalizes at the second task's completion", () => {
    expect(readPhases(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows())).toEqual({
      current: "finalized",
      lastSeq: 7,
      spans: [
        { phase: "job", startSeq: 0, endSeq: 0 },
        { phase: "planning", startSeq: 0, endSeq: 0 },
        { phase: "build", startSeq: 0, endSeq: 1 },
        { phase: "test", startSeq: 1, endSeq: 1 },
        { phase: "review", startSeq: 1, endSeq: 7 },
        { phase: "finalized", startSeq: 7, endSeq: null },
      ],
    });
  });

  it("the demo recording's prefix to seq 3 is still in Review with one task open", () => {
    expect(readPhases(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows().slice(0, 4))).toEqual({
      current: "review",
      lastSeq: 3,
      spans: [
        { phase: "job", startSeq: 0, endSeq: 0 },
        { phase: "planning", startSeq: 0, endSeq: 0 },
        { phase: "build", startSeq: 0, endSeq: 1 },
        { phase: "test", startSeq: 1, endSeq: 1 },
        { phase: "review", startSeq: 1, endSeq: null },
      ],
    });
  });

  it("a planned job walks Planning, Build and Test and stops at a failure", () => {
    const rows = [
      row(0, "planning_started"),
      row(1, "planning_completed", "", "changed"),
      row(2, "task_run_started", "t1"),
      row(3, "verification_failed", "t1", "fail"),
      row(4, "task_run_failed", "t1", "fail"),
    ];
    expect(readPhases("job-p", T1, rows)).toEqual({
      current: "test",
      lastSeq: 4,
      spans: [
        { phase: "job", startSeq: 0, endSeq: 0 },
        { phase: "planning", startSeq: 0, endSeq: 2 },
        { phase: "build", startSeq: 2, endSeq: 3 },
        { phase: "test", startSeq: 3, endSeq: null },
      ],
    });
  });

  it("a ledger with rows but no marker is honest: Job alone", () => {
    expect(readPhases("job-s", T1, [row(0, ""), row(1, "")])).toEqual({
      current: "job",
      lastSeq: 1,
      spans: [{ phase: "job", startSeq: 0, endSeq: null }],
    });
  });

  it("an empty ledger reaches no phase", () => {
    expect(readPhases("job-e", T1, [])).toEqual({ current: "job", spans: [], lastSeq: null });
  });

  it("a pass without a review round fills the skipped phases at the pass", () => {
    const rows = [row(0, "task_run_started", "t1"), row(1, "task_run_completed", "t1", "pass")];
    expect(readPhases("job-n", T1, rows)).toEqual({
      current: "finalized",
      lastSeq: 1,
      spans: [
        { phase: "job", startSeq: 0, endSeq: 0 },
        { phase: "planning", startSeq: 0, endSeq: 0 },
        { phase: "build", startSeq: 0, endSeq: 1 },
        { phase: "test", startSeq: 1, endSeq: 1 },
        { phase: "review", startSeq: 1, endSeq: 1 },
        { phase: "finalized", startSeq: 1, endSeq: null },
      ],
    });
  });

  it("a marker after the pass moves Finalized to that marker", () => {
    const rows = [
      row(0, "task_run_started", "t1"),
      row(1, "task_run_completed", "t1", "pass"),
      row(2, "verification_passed", "t1", "pass"),
    ];
    expect(readPhases("job-m", T1, rows)).toEqual({
      current: "finalized",
      lastSeq: 2,
      spans: [
        { phase: "job", startSeq: 0, endSeq: 0 },
        { phase: "planning", startSeq: 0, endSeq: 0 },
        { phase: "build", startSeq: 0, endSeq: 2 },
        { phase: "test", startSeq: 2, endSeq: 2 },
        { phase: "review", startSeq: 2, endSeq: 2 },
        { phase: "finalized", startSeq: 2, endSeq: null },
      ],
    });
  });

  it("Finalized is withdrawn when a task starts again, and the earlier prefix keeps it", () => {
    const rows = [
      row(0, "task_run_started", "t1"),
      row(1, "task_round_completed", "t1", "pass"),
      row(2, "task_run_completed", "t1", "pass"),
      row(3, "task_run_started", "t1"),
    ];
    expect(readPhases("job-r", T1, rows.slice(0, 3)).current).toBe("finalized");
    expect(readPhases("job-r", T1, rows)).toEqual({
      current: "review",
      lastSeq: 3,
      spans: [
        { phase: "job", startSeq: 0, endSeq: 0 },
        { phase: "planning", startSeq: 0, endSeq: 0 },
        { phase: "build", startSeq: 0, endSeq: 1 },
        { phase: "test", startSeq: 1, endSeq: 1 },
        { phase: "review", startSeq: 1, endSeq: null },
      ],
    });
  });

  it("reads the same phases from shuffled rows with repeated seqs", () => {
    const shuffled = [GOLDEN_A_ROWS[3], GOLDEN_A_ROWS[1], row(2, "job_stopped"), GOLDEN_A_ROWS[0], GOLDEN_A_ROWS[2]];
    expect(readPhases(GOLDEN_A_JOB_ID, GOLDEN_A_TASKS, shuffled)).toEqual(
      readPhases(GOLDEN_A_JOB_ID, GOLDEN_A_TASKS, GOLDEN_A_ROWS),
    );
  });
});

describe("the timeline seed", () => {
  it("resets every status to pending and keeps the rest", () => {
    const tasks: BrainTaskSeed[] = [
      { id: "t1", status: "completed", rank: 0, title: "Deliver a" },
      { id: "t2", status: "failed", rank: 1 },
    ];
    expect(timelineSeedOf(tasks)).toEqual([
      { id: "t1", status: "pending", rank: 0, title: "Deliver a" },
      { id: "t2", status: "pending", rank: 1 },
    ]);
    expect(tasks[0].status).toBe("completed");
  });

  it("does not let today's statuses finalize the start of the ledger", () => {
    const done: BrainTaskSeed[] = [{ id: "t1", status: "completed", rank: 0 }];
    expect(readPhases("job-d", done, [row(0, "budget.tick")])).toEqual({
      current: "job",
      lastSeq: 0,
      spans: [{ phase: "job", startSeq: 0, endSeq: null }],
    });
  });

  it("orders the ledger by seq with the first of a repeated seq kept", () => {
    const first = row(2, "task_run_started", "t1");
    expect(orderedLedger([row(5, "budget.tick"), first, row(2, "job_stopped")])).toEqual([
      first,
      row(5, "budget.tick"),
    ]);
  });
});

describe("sub-glyph extraction", () => {
  it("maps the kinds the kind alone decides", () => {
    expect(SUB_GLYPH_TABLE).toEqual({
      task_needs_decision: "decision",
      task_decision_answered: "decision",
      task_run_failed: "failure",
      verification_failed: "failure",
      planning_failed: "failure",
      test_run_timed_out: "failure",
      cycle_healed: "heal",
      job_stopped: "stop",
    });
  });

  it("a healed verify cycle is a heal whatever came before it", () => {
    expect(extractSubGlyphs([row(4, "cycle_healed")])).toEqual([
      { seq: 4, glyph: "heal", kind: "cycle_healed", taskId: "", line: "cycle_healed event" },
    ]);
  });

  it("golden B: two failed rounds, a stop, the heal and a decision, with humanized lines", () => {
    expect(extractSubGlyphs(GOLDEN_B_ROWS)).toEqual([
      { seq: 2, glyph: "failure", kind: "task_round_completed", taskId: "t1", line: "A review round of a task finished." },
      { seq: 3, glyph: "failure", kind: "task_round_completed", taskId: "t1", line: "A review round of a task finished." },
      { seq: 4, glyph: "stop", kind: "job_stopped", taskId: "", line: "The job stopped." },
      { seq: 6, glyph: "heal", kind: "task_round_completed", taskId: "t1", line: "A review round of a task finished." },
      { seq: 9, glyph: "decision", kind: "task_needs_decision", taskId: "t2", line: "task_needs_decision event" },
    ]);
  });

  it("the demo recording: each task's repair round and its heal", () => {
    expect(extractSubGlyphs(brainDemoRows()).map((g) => [g.seq, g.glyph, g.taskId])).toEqual([
      [1, "failure", "a7a8f67f1b9a4814"],
      [2, "heal", "a7a8f67f1b9a4814"],
      [5, "failure", "1965fb3f26b64fe7"],
      [6, "heal", "1965fb3f26b64fe7"],
    ]);
  });

  it("a pass heals only the task whose round failed, and only once", () => {
    const rows = [
      row(0, "task_round_completed", "t1", "fail"),
      row(1, "task_round_completed", "t2", "pass"),
      row(2, "task_round_completed", "t1", "pass"),
      row(3, "task_round_completed", "t1", "pass"),
    ];
    expect(extractSubGlyphs(rows).map((g) => [g.seq, g.glyph])).toEqual([
      [0, "failure"],
      [2, "heal"],
    ]);
  });

  it("golden A has nothing to mark, and a failed planned job marks both failures", () => {
    expect(extractSubGlyphs(GOLDEN_A_ROWS)).toEqual([]);
    const rows = [
      row(0, "planning_failed", "", "error"),
      row(1, "verification_failed", "t1", "fail"),
      row(2, "task_run_failed", "t1", "fail"),
    ];
    expect(extractSubGlyphs(rows)).toEqual([
      { seq: 0, glyph: "failure", kind: "planning_failed", taskId: "", line: "Planning failed." },
      { seq: 1, glyph: "failure", kind: "verification_failed", taskId: "t1", line: "Verification failed." },
      { seq: 2, glyph: "failure", kind: "task_run_failed", taskId: "t1", line: "A task failed." },
    ]);
  });
});
