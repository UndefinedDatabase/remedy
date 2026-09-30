// F044 T001 — the palette's node jump (DECISION F044 D1). Expected scores are the fuzzy rule's,
// computed by hand.
import { describe, expect, it } from "vitest";
import type { RemedyTaskItem } from "./types";
import { JUMP_RESULT_LIMIT, jumpTargetsOf, rankJumpTargets } from "./paletteJump";
import type { JumpTarget } from "./paletteJump";

function task(id: string, label: string, kind: RemedyTaskItem["kind"]): RemedyTaskItem {
  return { id, label, state: "pending", kind, checked: false, muted: false, nodeId: `task:${id}` };
}

const TARGETS: JumpTarget[] = [
  { id: "t1", nodeId: "task:t1", label: "Fix error handling", kind: "task" },
  { id: "t2", nodeId: "task:t2", label: "Write tests", kind: "test" },
  { id: "review-7", nodeId: "task:review-7", label: "Check the diff", kind: "review" },
  { id: "t4", nodeId: "task:t4", label: "Errata", kind: "task" },
];

describe("jumpTargetsOf", () => {
  it("answers one target per task, in the dashboard's order, with the task's own node id", () => {
    const tasks = [task("t2", "Write tests", "test"), task("t1", "Fix error handling", "task")];
    expect(jumpTargetsOf({ tasks })).toEqual([
      { id: "t2", nodeId: "task:t2", label: "Write tests", kind: "test" },
      { id: "t1", nodeId: "task:t1", label: "Fix error handling", kind: "task" },
    ]);
  });
});

describe("rankJumpTargets", () => {
  it("lists label matches best first and drops the rest", () => {
    const hits = rankJumpTargets(TARGETS, "err", 10);
    expect(hits.map((hit) => [hit.target.id, hit.field, hit.match.score])).toEqual([
      ["t4", "label", 1500],
      ["t1", "label", 1496],
    ]);
    expect(hits[1].match.ranges).toEqual([[4, 7]]);
  });

  it("matches the id, the id winning a tie with the kind", () => {
    const hits = rankJumpTargets(TARGETS, "review", 10);
    expect(hits.map((hit) => [hit.target.id, hit.field, hit.match.score, hit.match.ranges])).toEqual([
      ["review-7", "id", 1500, [[0, 6]]],
    ]);
  });

  it("matches the kind when it scores higher than the label", () => {
    const hits = rankJumpTargets(TARGETS, "test", 10);
    expect(hits.map((hit) => [hit.target.id, hit.field, hit.match.score])).toEqual([["t2", "kind", 1500]]);
  });

  it("breaks a score tie by the shorter label, and cuts at the limit after sorting", () => {
    expect(rankJumpTargets(TARGETS, "t", 10).map((hit) => [hit.target.id, hit.field, hit.match.score])).toEqual([
      ["t4", "id", 1500],
      ["t2", "id", 1500],
      ["t1", "id", 1500],
      ["review-7", "label", 1494],
    ]);
    expect(rankJumpTargets(TARGETS, "t", 1).map((hit) => hit.target.id)).toEqual(["t4"]);
  });

  it("lists the first targets in their own order for an empty or blank query", () => {
    for (const query of ["", "   "]) {
      expect(rankJumpTargets(TARGETS, query, 2)).toEqual([
        { target: TARGETS[0], field: "label", match: { score: 0, ranges: [] } },
        { target: TARGETS[1], field: "label", match: { score: 0, ranges: [] } },
      ]);
    }
  });

  it("lists at most JUMP_RESULT_LIMIT rows in the palette", () => {
    expect(JUMP_RESULT_LIMIT).toBe(8);
  });
});
