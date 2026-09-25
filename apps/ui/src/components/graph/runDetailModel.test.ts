import { describe, expect, it } from "vitest";
import type { TaskRunRounds } from "../../api/taskRunRounds";
import type { RemedyPromptTraceItem } from "../../api/types";
import { rebuildBrainModel } from "./brainReducer";
import { row } from "./brainReducer.fixtures";
import {
  RUN_FACT_EARLIER, RUN_FACT_LOADING, RUN_FACT_NO_ROUND, RUN_FACT_NO_RUN, RUN_FACT_REVIEWER_TOKENS,
  RUN_FACT_RUNNING, RUN_FACT_TEST_TIMING, RUN_FACT_TEST_TOKENS, RUN_FACT_UNREADABLE,
  formatDurationMs, formatTokens, runDetailOf, runPlaceOf,
} from "./runDetailModel";

// One task's ledger: a builder run at seq 1 whose rounds end needs_repair (seq
// 2), with no review (seq 3, which the reducer draws nothing for) and pass
// (seq 4), then the run completes and a test passes. ROWS_AGAIN adds a second
// builder run at seq 7. Every expected value below is read off these rows and
// the report under them by hand, never computed by the code under test.
const ROWS = [
  row(1, "task_run_started", "t1"),
  row(2, "task_round_completed", "t1", "needs_repair"),
  row(3, "task_round_completed", "t1", "no_review"),
  row(4, "task_round_completed", "t1", "pass"),
  row(5, "task_run_completed", "t1", "pass"),
  row(6, "verification_passed", "t1", "pass"),
];
const ROWS_AGAIN = [...ROWS, row(7, "task_run_started", "t1")];

const REPORT: TaskRunRounds = {
  available: true, reason: null, taskId: "t1", runId: "0123456789abcdef", retriesUsed: 1,
  rounds: [
    { round: 1, kind: "initial", startedAt: null, finishedAt: null, durationMs: 90250, testPassed: false,
      builder: { durationMs: 61000, tokensUsed: 1834 },
      reviewer: { verdict: "needs_repair", durationMs: 22000, parseRetried: true } },
    { round: 2, kind: "repair", startedAt: null, finishedAt: null, durationMs: 29000, testPassed: true,
      builder: { durationMs: 20000, tokensUsed: 900 }, reviewer: null },
    { round: 3, kind: "repair", startedAt: null, finishedAt: null, durationMs: 10000, testPassed: true,
      builder: { durationMs: 7000, tokensUsed: null },
      reviewer: { verdict: "pass", durationMs: 8000, parseRetried: false } },
  ],
};

function prompt(id: string, role: RemedyPromptTraceItem["role"], round: number, taskId = "t1"): RemedyPromptTraceItem {
  return {
    id, taskId, runId: "r", round, role, promptKind: "review", provider: "p", providerKind: "k",
    promptSha256: "", promptChars: 0, promptTokensEstimated: 0, contextCategories: [], changedFilesSafe: [],
    safeDiffFiles: [], evidenceRef: "", redactedPreview: "", redactedPreviewTruncated: false,
  };
}
const PROMPTS = [
  prompt("b2", "builder", 2), prompt("b1", "builder", 1), prompt("v1", "reviewer", 1),
  prompt("v3", "reviewer", 3), prompt("other", "reviewer", 1, "t2"),
];

function nodeOf(rows: typeof ROWS, id: string) {
  const model = rebuildBrainModel("job-d", [{ id: "t1", status: "pending", rank: 0 }], rows);
  const node = model.nodes.find((n) => n.id === id);
  if (!node) throw new Error(`no node ${id}`);
  return node;
}

function detail(id: string, rounds: TaskRunRounds | null = REPORT, rows = ROWS) {
  return runDetailOf({ node: nodeOf(rows, id), rows, rounds, promptItems: PROMPTS });
}

describe("formatting", () => {
  it("writes durations in the unit a reader expects", () => {
    expect([850, 4200, 9949, 22000, 38000, 59600, 125000, 129250].map(formatDurationMs))
      .toEqual(["850 ms", "4.2 s", "9.9 s", "22 s", "38 s", "1 min 0 s", "2 min 5 s", "2 min 9 s"]);
  });

  it("writes token counts with thousands separators", () => {
    expect([0, 900, 2734, 1234567].map(formatTokens)).toEqual(["0", "900", "2,734", "1,234,567"]);
  });
});

describe("runPlaceOf", () => {
  it("counts every round the ledger logged, the unreviewed one included", () => {
    expect(runPlaceOf({ kind: "review_run", seq: 2 }, "t1", ROWS)).toEqual({ startSeq: 1, round: 1, latest: true });
    expect(runPlaceOf({ kind: "review_run", seq: 4 }, "t1", ROWS)).toEqual({ startSeq: 1, round: 3, latest: true });
    expect(runPlaceOf({ kind: "builder_run", seq: 1 }, "t1", ROWS)).toEqual({ startSeq: 1, round: null, latest: true });
  });

  it("knows a run is no longer the latest once the task started again", () => {
    expect(runPlaceOf({ kind: "review_run", seq: 4 }, "t1", ROWS_AGAIN)).toEqual({ startSeq: 1, round: 3, latest: false });
    expect(runPlaceOf({ kind: "builder_run", seq: 7 }, "t1", ROWS_AGAIN)).toEqual({ startSeq: 7, round: null, latest: true });
  });
});

describe("runDetailOf — the latest run's report is at hand", () => {
  it("a review run in round 1: its verdict, the reviewer's time and the re-asked reply", () => {
    expect(detail("run:t1:2")).toEqual({
      title: "Review run", verdict: "Needs repair", taskId: "t1", round: 1,
      tokens: { missing: RUN_FACT_REVIEWER_TOKENS },
      duration: { value: "22 s" },
      retries: { value: "Asked again once: the first reply could not be read" },
      promptItemId: "v1",
    });
  });

  it("a review run in round 3, after a round with no review", () => {
    expect(detail("run:t1:4")).toEqual({
      title: "Review run", verdict: "Passed", taskId: "t1", round: 3,
      tokens: { missing: RUN_FACT_REVIEWER_TOKENS },
      duration: { value: "8.0 s" },
      retries: { value: "None" },
      promptItemId: "v3",
    });
  });

  it("the builder run: its tokens summed where recorded, its rounds' time, its repairs and retries", () => {
    expect(detail("run:t1:1")).toEqual({
      title: "Builder run", verdict: "Passed", taskId: "t1", round: null,
      tokens: { value: "2,734 (the builder, as the provider reported)" },
      duration: { value: "2 min 9 s" },
      retries: { value: "2 repair rounds, 1 provider retry" },
      promptItemId: "b1",
    });
  });

  it("a test run says it makes no model call and is not timed on its own", () => {
    expect(detail("run:t1:6")).toEqual({
      title: "Test run", verdict: "Passed", taskId: "t1", round: null,
      tokens: { value: RUN_FACT_TEST_TOKENS },
      duration: { missing: RUN_FACT_TEST_TIMING },
      retries: { value: "None" },
      promptItemId: null,
    });
  });

  it("a round the report has no entry for is said so, never guessed", () => {
    const withoutRound1 = { ...REPORT, rounds: REPORT.rounds.slice(1) };
    const d = detail("run:t1:2", withoutRound1);
    expect([d.tokens, d.duration, d.retries]).toEqual([
      { missing: RUN_FACT_NO_ROUND }, { missing: RUN_FACT_NO_ROUND }, { missing: RUN_FACT_NO_ROUND },
    ]);
  });
});

describe("runDetailOf — every reason a fact is not shown", () => {
  const facts = (d: ReturnType<typeof detail>) => [d.tokens, d.duration, d.retries];

  it("while the report loads", () => {
    expect(facts(detail("run:t1:2", null))).toEqual(Array(3).fill({ missing: RUN_FACT_LOADING }));
  });

  it("when the task has not finished a run, or its report cannot be read", () => {
    const noRun: TaskRunRounds = { ...REPORT, available: false, reason: "no_run_recorded", rounds: [] };
    const broken: TaskRunRounds = { ...REPORT, available: false, reason: "run_report_unreadable", rounds: [] };
    expect(facts(detail("run:t1:2", noRun))).toEqual(Array(3).fill({ missing: RUN_FACT_NO_RUN }));
    expect(facts(detail("run:t1:2", broken))).toEqual(Array(3).fill({ missing: RUN_FACT_UNREADABLE }));
  });

  it("for a run the task has since started again, whose report is gone", () => {
    expect(facts(detail("run:t1:1", REPORT, ROWS_AGAIN))).toEqual(Array(3).fill({ missing: RUN_FACT_EARLIER }));
    expect(facts(detail("run:t1:4", REPORT, ROWS_AGAIN))).toEqual(Array(3).fill({ missing: RUN_FACT_EARLIER }));
  });

  it("for a run still going, whatever the report says", () => {
    const d = detail("run:t1:7", REPORT, ROWS_AGAIN);
    expect([d.verdict, ...facts(d)]).toEqual(["Running", ...Array(3).fill({ missing: RUN_FACT_RUNNING })]);
  });
});
