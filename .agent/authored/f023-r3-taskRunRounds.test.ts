import { describe, expect, it } from "vitest";
import { loadTaskRunRounds } from "./remedyApi";
import { TASK_RUN_ROUNDS_VERSION, decodeTaskRunRounds, taskRunRoundsPath } from "./taskRunRounds";

// The server's envelope for one task, as tests/ui_server/test_task_run_rounds.py
// pins it: snake_case on the wire, camelCase after decoding.
const ENVELOPE = {
  version: 1, job_id: "job-1", task_id: "T001", available: true, reason: null,
  run_id: "0123456789abcdef", retries_used: 1,
  rounds: [
    {
      round: 1, kind: "initial", started_at: "2026-09-25T10:00:00+00:00",
      finished_at: "2026-09-25T10:01:30.250000+00:00", duration_ms: 90250, test_passed: false,
      builder: { duration_ms: 61000, tokens_used: 1834 },
      reviewer: { verdict: "needs_repair", duration_ms: 22000, parse_retried: true },
    },
    {
      round: 2, kind: "repair", started_at: null, finished_at: null, duration_ms: null, test_passed: null,
      builder: null, reviewer: null,
    },
  ],
};

describe("taskRunRoundsPath", () => {
  it("addresses the seven-segment route with every value encoded", () => {
    expect(taskRunRoundsPath({ jobId: "job 1", taskId: "T/001", token: "a&b" }))
      .toBe("/api/jobs/job%201/task-runs/T%2F001/rounds?token=a%26b");
    expect(taskRunRoundsPath({ jobId: "j", taskId: "T001", token: "t", baseUrl: "http://h:1" }))
      .toBe("http://h:1/api/jobs/j/task-runs/T001/rounds?token=t");
  });
});

describe("decodeTaskRunRounds", () => {
  it("reads the envelope's version", () => {
    expect(TASK_RUN_ROUNDS_VERSION).toBe(1);
  });

  it("decodes every field of an available envelope", () => {
    expect(decodeTaskRunRounds(ENVELOPE, "T001")).toEqual({
      available: true, reason: null, taskId: "T001", runId: "0123456789abcdef", retriesUsed: 1,
      rounds: [
        {
          round: 1, kind: "initial", startedAt: "2026-09-25T10:00:00+00:00",
          finishedAt: "2026-09-25T10:01:30.250000+00:00", durationMs: 90250, testPassed: false,
          builder: { durationMs: 61000, tokensUsed: 1834 },
          reviewer: { verdict: "needs_repair", durationMs: 22000, parseRetried: true },
        },
        {
          round: 2, kind: "repair", startedAt: null, finishedAt: null, durationMs: null, testPassed: null,
          builder: null, reviewer: null,
        },
      ],
    });
  });

  it("keeps the server's reason when the envelope is unavailable, and no rounds", () => {
    const env = { ...ENVELOPE, available: false, reason: "no_run_recorded", run_id: null, rounds: ENVELOPE.rounds };
    expect(decodeTaskRunRounds(env, "T001")).toEqual({
      available: false, reason: "no_run_recorded", taskId: "T001", runId: null, retriesUsed: 1, rounds: [],
    });
  });

  it("answers unreadable for another version, another task, or no envelope at all", () => {
    for (const payload of [{ ...ENVELOPE, version: 2 }, { ...ENVELOPE, task_id: "T002" }, null, "text", [ENVELOPE]]) {
      const decoded = decodeTaskRunRounds(payload, "T001");
      expect([decoded.available, decoded.reason, decoded.rounds]).toEqual([false, "unreadable", []]);
    }
  });

  it("drops malformed values to null rather than trusting them", () => {
    const env = { ...ENVELOPE, retries_used: -1, rounds: [{ round: 1.5, duration_ms: "90s", builder: { tokens_used: -3 } }, 7] };
    const decoded = decodeTaskRunRounds(env, "T001");
    expect(decoded.retriesUsed).toBeNull();
    expect(decoded.rounds).toEqual([{
      round: null, kind: null, startedAt: null, finishedAt: null, durationMs: null, testPassed: null,
      builder: { durationMs: null, tokensUsed: null }, reviewer: null,
    }]);
  });
});

describe("loadTaskRunRounds", () => {
  it("fetches the route's path and decodes what arrives", async () => {
    const asked: string[] = [];
    const result = await loadTaskRunRounds({ jobId: "job-1", taskId: "T001", token: "t" }, async (path) => {
      asked.push(path);
      return ENVELOPE;
    });
    expect(asked).toEqual(["/api/jobs/job-1/task-runs/T001/rounds?token=t"]);
    expect([result.available, result.rounds.length]).toEqual([true, 2]);
  });

  it("never throws: a failed fetch is the unreadable shape", async () => {
    const result = await loadTaskRunRounds({ jobId: "j", taskId: "T001", token: "t" }, async () => {
      throw new Error("403");
    });
    expect([result.available, result.reason, result.taskId]).toEqual([false, "unreadable", "T001"]);
  });
});
