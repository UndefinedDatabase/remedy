import { describe, expect, it } from "vitest";
import {
  taskTitleOf, taskVetoAction, taskVetoEntry, vetoAnswerSentence, vetoHoverText, vetoingEntriesOf,
} from "./vetoView";
import type { RemedyDashboard, RemedyTaskItem, RemedyVetoEntry, RemedyVetoes } from "./types";

function entry(overrides: Partial<RemedyVetoEntry> = {}): RemedyVetoEntry {
  return {
    taskId: "t1",
    reason: "duplicates T2",
    actor: "operator",
    requestedAt: "2026-09-26T00:00:00Z",
    requestId: "req-1",
    statusAtVeto: "pending",
    unreachableTaskIds: [],
    answer: "",
    ...overrides,
  };
}

function vetoes(overrides: Partial<RemedyVetoes> = {}): RemedyVetoes {
  return {
    tasks: [],
    vetoableTaskIds: [],
    unreachableTaskIds: [],
    error: "",
    ...overrides,
  };
}

function task(id: string, label = id): RemedyTaskItem {
  return { id, label, state: "pending", kind: "task", checked: false, muted: false, nodeId: `node-${id}` };
}

function dashboard(overrides: Partial<RemedyDashboard> = {}): RemedyDashboard {
  return {
    tasks: [],
    vetoes: vetoes(),
    ...overrides,
  } as RemedyDashboard;
}

describe("taskVetoEntry", () => {
  it("finds the entry recorded against a task", () => {
    const e = entry({ taskId: "t1" });
    expect(taskVetoEntry(vetoes({ tasks: [e] }), "t1")).toBe(e);
  });

  it("is null for a task never vetoed", () => {
    expect(taskVetoEntry(vetoes({ tasks: [entry({ taskId: "t1" })] }), "t9")).toBeNull();
  });
});

describe("vetoingEntriesOf", () => {
  it("finds every entry whose own unreachable set names the task, in section order", () => {
    const e1 = entry({ taskId: "t1", unreachableTaskIds: ["t3"] });
    const e2 = entry({ taskId: "t2", unreachableTaskIds: ["t3"] });
    expect(vetoingEntriesOf(vetoes({ tasks: [e1, e2] }), "t3")).toEqual([e1, e2]);
  });

  it("is empty for a task no veto names", () => {
    const e1 = entry({ taskId: "t1", unreachableTaskIds: ["t3"] });
    expect(vetoingEntriesOf(vetoes({ tasks: [e1] }), "t9")).toEqual([]);
  });
});

describe("taskTitleOf", () => {
  it("reads the task's label", () => {
    expect(taskTitleOf(dashboard({ tasks: [task("t1", "Build the thing")] }), "t1")).toBe("Build the thing");
  });

  it("falls back to the bare id for a task this dashboard never named", () => {
    expect(taskTitleOf(dashboard({ tasks: [] }), "t9")).toBe("t9");
  });
});

describe("taskVetoAction", () => {
  it("names the task id when the section names it vetoable and carries no error", () => {
    const d = dashboard({ vetoes: vetoes({ vetoableTaskIds: ["t1"] }) });
    expect(taskVetoAction(d, "t1")).toEqual({ taskId: "t1" });
  });

  it("is null for a task the section does not name vetoable", () => {
    const d = dashboard({ vetoes: vetoes({ vetoableTaskIds: ["t2"] }) });
    expect(taskVetoAction(d, "t1")).toBeNull();
  });

  it("is null when the section's own read failed, even for a task it still names vetoable", () => {
    const d = dashboard({ vetoes: vetoes({ vetoableTaskIds: ["t1"], error: "boom" }) });
    expect(taskVetoAction(d, "t1")).toBeNull();
  });
});

describe("vetoHoverText", () => {
  it("names the reason verbatim for a vetoed task, HTML and all", () => {
    const reason = "breaks <b>everything</b> & costs too much";
    const d = dashboard({ vetoes: vetoes({ tasks: [entry({ taskId: "t1", reason })] }) });
    expect(vetoHoverText(d, "t1")).toBe(`Vetoed: ${reason}`);
  });

  it("names every vetoing task's title, joined by \", \", in section order", () => {
    const d = dashboard({
      tasks: [task("t1", "Build the API"), task("t2", "Wire the client")],
      vetoes: vetoes({
        tasks: [
          entry({ taskId: "t1", unreachableTaskIds: ["t3"] }),
          entry({ taskId: "t2", unreachableTaskIds: ["t3"] }),
        ],
      }),
    });
    expect(vetoHoverText(d, "t3")).toBe("Unreachable due to veto of Build the API, Wire the client");
  });

  it("a vetoed task's text wins over an unreachable reading of the same task", () => {
    const d = dashboard({
      tasks: [task("t1", "Alpha")],
      vetoes: vetoes({
        tasks: [
          entry({ taskId: "t1", reason: "duplicate work", unreachableTaskIds: ["t1"] }),
        ],
      }),
    });
    expect(vetoHoverText(d, "t1")).toBe("Vetoed: duplicate work");
  });

  it("is null for a task that is neither vetoed nor unreachable", () => {
    expect(vetoHoverText(dashboard(), "t9")).toBeNull();
  });
});

describe("vetoAnswerSentence", () => {
  it("an empty answer is still waiting in the inbox", () => {
    expect(vetoAnswerSentence("")).toBe("A replan proposal is waiting in the decision inbox.");
  });

  it("replan_follow_up", () => {
    expect(vetoAnswerSentence("replan_follow_up")).toBe("Answered: replan the remaining work as a new job.");
  });

  it("accept_reduced_scope", () => {
    expect(vetoAnswerSentence("accept_reduced_scope")).toBe("Answered: accept the smaller scope.");
  });

  it("any other value reads as answered, honestly", () => {
    expect(vetoAnswerSentence("something_else")).toBe("Answered.");
  });
});
