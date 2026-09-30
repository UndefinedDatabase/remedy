// T5_F044 T001, DECISION F044 D1 — the palette's node jump: its targets are the dashboard's task
// list, the rows `handleJump` already reads, each matched over its label, its id and its kind
// through the fuzzy rule, and a jump selects the target's node through the shell's own
// `onSelectNode`, the route a pointer's pick takes.
import type { FuzzyMatch } from "./fuzzyMatch";
import { fuzzyMatch } from "./fuzzyMatch";
import type { RemedyDashboard } from "./types";

export const JUMP_RESULT_LIMIT = 8;

/** One jumpable row: a dashboard task, carried with the node id a jump selects. */
export interface JumpTarget {
  readonly id: string;
  readonly nodeId: string;
  readonly label: string;
  readonly kind: string;
}

/** Which of a target's fields its best match came from. */
export type JumpField = "label" | "id" | "kind";

/** One ranked jump result. */
export interface JumpHit {
  readonly target: JumpTarget;
  readonly field: JumpField;
  readonly match: FuzzyMatch;
}

export function jumpTargetsOf(dashboard: Pick<RemedyDashboard, "tasks">): JumpTarget[] {
  return dashboard.tasks.map((task) => ({
    id: task.id,
    nodeId: task.nodeId,
    label: task.label,
    kind: task.kind,
  }));
}

const FIELD_ORDER: readonly JumpField[] = ["label", "id", "kind"];

function bestHit(target: JumpTarget, query: string): { field: JumpField; match: FuzzyMatch } | null {
  let best: { field: JumpField; match: FuzzyMatch } | null = null;
  for (const field of FIELD_ORDER) {
    const match = fuzzyMatch(query, target[field]);
    if (match !== null && (best === null || match.score > best.match.score)) {
      best = { field, match };
    }
  }
  return best;
}

export function rankJumpTargets(
  targets: readonly JumpTarget[],
  query: string,
  limit: number,
): JumpHit[] {
  if (query.trim() === "") {
    return targets.slice(0, limit).map((target) => ({
      target,
      field: "label" as JumpField,
      match: { score: 0, ranges: [] },
    }));
  }

  const rows: { hit: JumpHit; index: number }[] = [];
  targets.forEach((target, index) => {
    const best = bestHit(target, query);
    if (best !== null) rows.push({ hit: { target, field: best.field, match: best.match }, index });
  });

  rows.sort((a, b) => {
    if (a.hit.match.score !== b.hit.match.score) return b.hit.match.score - a.hit.match.score;
    const labelA = a.hit.target.label;
    const labelB = b.hit.target.label;
    if (labelA.length !== labelB.length) return labelA.length - labelB.length;
    if (labelA !== labelB) return labelA < labelB ? -1 : 1;
    return a.index - b.index;
  });

  return rows.slice(0, limit).map((row) => row.hit);
}
