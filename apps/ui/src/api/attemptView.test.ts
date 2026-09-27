import { describe, expect, it } from "vitest";
import type { RemedyTaskAttempt, RemedyTaskItem } from "./types";
import { attemptChipText, attemptFactsSentence, taskAttemptRows } from "./attemptView";

function attempt(overrides: Partial<RemedyTaskAttempt> = {}): RemedyTaskAttempt {
  return {
    attempt: 1,
    status: "",
    finalStatus: "",
    reviewerVerdict: "",
    modelOverride: "",
    worktreeCommit: "",
    runId: "",
    rerunId: "",
    endedAt: "",
    testPassed: null,
    ...overrides,
  };
}

function item(overrides: Partial<RemedyTaskItem> = {}): RemedyTaskItem {
  return {
    id: "t1",
    label: "Task",
    state: "current",
    kind: "task",
    checked: false,
    muted: false,
    nodeId: "node-t1",
    ...overrides,
  };
}

describe("attemptChipText", () => {
  it("answers `attempt <n>`", () => {
    expect(attemptChipText(2)).toBe("attempt 2");
    expect(attemptChipText(5)).toBe("attempt 5");
  });
});

describe("taskAttemptRows", () => {
  it("answers [] for an undefined item", () => {
    expect(taskAttemptRows(undefined)).toEqual([]);
  });

  it("answers [] for an item with no attempts and for an item whose attempts is []", () => {
    expect(taskAttemptRows(item())).toEqual([]);
    expect(taskAttemptRows(item({ attempts: [] }))).toEqual([]);
  });

  // DECISION F029 D5 (2) — the closed set of ended words, and the fallback
  // for a status this browser does not name one for.
  it.each([
    ["applied_to_job_workspace", "It was applied"],
    ["passed", "It was applied"],
    ["blocked", "It was blocked"],
    ["failed", "It failed"],
    ["skipped", "It was skipped"],
    ["vetoed", "It was vetoed"],
    ["pending", "It had not run"],
    ["something_else", "It ended as something_else"],
  ])("an earlier row's outcome fact for status %s reads %s", (status, expected) => {
    const rows = taskAttemptRows(item({ attempt: 2, attempts: [attempt({ attempt: 1, status })] }));
    expect(rows[0].facts[0]).toBe(expected);
  });

  it("the verdict fact: 'the reviewer said <verdict>', or 'no review verdict' when empty", () => {
    const withVerdict = taskAttemptRows(item({
      attempt: 2, attempts: [attempt({ attempt: 1, reviewerVerdict: "pass" })],
    }));
    expect(withVerdict[0].facts[1]).toBe("the reviewer said pass");

    const without = taskAttemptRows(item({ attempt: 2, attempts: [attempt({ attempt: 1 })] }));
    expect(without[0].facts[1]).toBe("no review verdict");
  });

  it("the tests fact: passed, failed, or no test result for null", () => {
    const passed = taskAttemptRows(item({
      attempt: 2, attempts: [attempt({ attempt: 1, testPassed: true })],
    }));
    expect(passed[0].facts[2]).toBe("its tests passed");

    const failed = taskAttemptRows(item({
      attempt: 2, attempts: [attempt({ attempt: 1, testPassed: false })],
    }));
    expect(failed[0].facts[2]).toBe("its tests failed");

    const none = taskAttemptRows(item({
      attempt: 2, attempts: [attempt({ attempt: 1, testPassed: null })],
    }));
    expect(none[0].facts[2]).toBe("no test result");
  });

  it("the model fact: 'it ran on <model>', or the job's own model when no override", () => {
    const overridden = taskAttemptRows(item({
      attempt: 2, attempts: [attempt({ attempt: 1, modelOverride: "claude-x" })],
    }));
    expect(overridden[0].facts[3]).toBe("it ran on claude-x");

    const none = taskAttemptRows(item({ attempt: 2, attempts: [attempt({ attempt: 1 })] }));
    expect(none[0].facts[3]).toBe("it ran on the job's own model");
  });

  it("the commit fact: 'commit <first twelve>', or 'no commit' when empty", () => {
    const withCommit = taskAttemptRows(item({
      attempt: 2, attempts: [attempt({ attempt: 1, worktreeCommit: "abcdef0123456789" })],
    }));
    expect(withCommit[0].facts[4]).toBe("commit abcdef012345");

    const none = taskAttemptRows(item({ attempt: 2, attempts: [attempt({ attempt: 1 })] }));
    expect(none[0].facts[4]).toBe("no commit");
  });

  // DECISION F029 D5 (3): a row's changes compare with the row BEFORE it,
  // never the first — proven here by a third attempt reverting to the
  // first's own outcome: its changes must still show a difference, because
  // the row it compares with (the second) differs from it.
  it("a third attempt's changes compare with the SECOND attempt, even when it reverts to the first's own outcome", () => {
    const rows = taskAttemptRows(item({
      attempt: 4,
      attempts: [
        attempt({ attempt: 1, status: "failed" }),
        attempt({ attempt: 2, status: "blocked" }),
        attempt({ attempt: 3, status: "failed" }),
      ],
    }));
    expect(rows).toHaveLength(4);
    expect(rows[0].changes).toEqual([]);
    expect(rows[1].changes).toEqual([
      { label: "Outcome", before: "It failed", after: "It was blocked" },
    ]);
    // The third attempt's own outcome equals the FIRST's, but its changes
    // compare with the SECOND, which differs — so a change is still recorded.
    expect(rows[2].changes).toEqual([
      { label: "Outcome", before: "It was blocked", after: "It failed" },
    ]);
  });

  it("an unchanged fact between two earlier rows earns no entry in changes", () => {
    const rows = taskAttemptRows(item({
      attempt: 3,
      attempts: [
        attempt({ attempt: 1, status: "failed", reviewerVerdict: "fail" }),
        attempt({ attempt: 2, status: "failed", reviewerVerdict: "pass" }),
      ],
    }));
    expect(rows[1].changes).toEqual([
      { label: "Reviewer", before: "the reviewer said fail", after: "the reviewer said pass" },
    ]);
  });

  // DECISION F029 D5 (2): the current row's own present-tense word, for
  // each of the four states the decision names.
  it.each([
    ["pending", "Now waiting to run"],
    ["current", "Now running"],
    ["done", "Now finished"],
    ["blocked", "Now blocked"],
    ["suggested", "Now suggested"],
  ] as const)("the current row's fact for state %s reads %s", (state, expected) => {
    const rows = taskAttemptRows(item({
      state, attempt: 2, attempts: [attempt({ attempt: 1 })],
    }));
    const current = rows[rows.length - 1];
    expect(current.current).toBe(true);
    expect(current.label).toBe("Attempt 2 · current");
    expect(current.facts).toEqual([expected]);
    expect(current.changes).toEqual([]);
  });
});

describe("attemptFactsSentence", () => {
  it("joins with '; ', ends with a full stop, and upper-cases the first letter", () => {
    expect(attemptFactsSentence(["it ran on claude-x", "no commit"])).toBe(
      "It ran on claude-x; no commit.",
    );
  });

  it("a single fact still gets a capital first letter and a full stop", () => {
    expect(attemptFactsSentence(["now running"])).toBe("Now running.");
  });
});
