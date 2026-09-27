// THE REST OF A SUBTREE RERUN, AS SENTENCES (DECISION F029 D6 (2)): the words
// a `job.rerun-subtree` 200 body becomes, once `rerunSend.ts`'s
// `rerunAnswerOf` has pulled it off the wire. `needs_confirmation` and
// `prepared` are the only two outcomes that body ever carries
// (`subtree_rerun.rerun_subtree_command`, DECISION F029 D4); every other
// value — including one this page does not recognise — answers `null`, so a
// caller never prints a sentence for a shape it did not check.
//
// READ DEFENSIVELY, LIKE EVERY OTHER VIEW IN THIS COCKPIT: a `subtree` that
// is not an array reads as empty, a `root_task_id` (or a `subtree[0]`) that
// is not a string reads as "", and an estimate whose `band_usd_high` is not a
// number reads as "cannot be estimated" rather than printing `NaN`. A body
// with every field missing still answers a sentence, never throws.
export interface RerunAnswerView {
  kind: "needs_confirmation" | "prepared";
  sentence: string;
  /** The command that runs the rerun — only a `prepared` answer carries one. */
  runCommand: string;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isFiniteNumber(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

/** The subtree the answer names, or `[]` for anything that is not an array —
 *  `rerun_subtree_command`'s own `subtree` key, the root and every task that
 *  depends on it, in plan order (`subtree_rerun.rerun_subtree_ids`). */
function subtreeOf(answer: Record<string, unknown>): readonly unknown[] {
  return Array.isArray(answer.subtree) ? answer.subtree : [];
}

/** The subtree's first id, or "" — the root a `needs_confirmation` answer
 *  names only through its `subtree`, since that body carries no
 *  `root_task_id` field of its own. */
function firstIdOf(subtree: readonly unknown[]): string {
  const first = subtree[0];
  return typeof first === "string" ? first : "";
}

function pluralSuffix(n: number): string {
  return n === 1 ? "" : "s";
}

/** The estimate sentence: priced when `band_usd_high` (and its two
 *  companions) are numbers, else the honest "cannot be estimated" fallback —
 *  DECISION F029 D3's own posture, that an unpriceable band is never shown
 *  as a number. */
function estimateSentence(answer: Record<string, unknown>, root: string, n: number): string {
  const estimate = answer.estimate;
  const low = isRecord(estimate) ? estimate.band_usd_low : undefined;
  const high = isRecord(estimate) ? estimate.band_usd_high : undefined;
  const threshold = answer.confirm_above_usd;
  if (isFiniteNumber(low) && isFiniteNumber(high) && isFiniteNumber(threshold)) {
    return `Rerunning task ${root} and ${n} task${pluralSuffix(n)} after it is estimated at `
      + `$${low.toFixed(2)} to $${high.toFixed(2)}, above the $${threshold.toFixed(2)} you asked `
      + "to confirm.";
  }
  return `The cost of rerunning task ${root} and ${n} task${pluralSuffix(n)} after it cannot be `
    + "estimated in advance.";
}

/** THE MAPPING: a `job.rerun-subtree` 200 body becomes the one sentence to
 *  show about it, or `null` for anything this control does not itself
 *  narrate — a refusal or an unreachable server, which `rerunSend.ts`'s
 *  `describeRerunResult` already speaks for. */
export function rerunAnswerView(answer: Record<string, unknown> | null): RerunAnswerView | null {
  if (answer === null) {
    return null;
  }
  if (answer.outcome === "needs_confirmation") {
    const subtree = subtreeOf(answer);
    const root = firstIdOf(subtree);
    const n = Math.max(subtree.length - 1, 0);
    return { kind: "needs_confirmation", sentence: estimateSentence(answer, root, n), runCommand: "" };
  }
  if (answer.outcome === "prepared") {
    const subtree = subtreeOf(answer);
    const root = typeof answer.root_task_id === "string" ? answer.root_task_id : "";
    const n = Math.max(subtree.length - 1, 0);
    const runCommand = typeof answer.run_command === "string" ? answer.run_command : "";
    return {
      kind: "prepared",
      sentence: `Task ${root} and ${n} task${pluralSuffix(n)} after it were reset to run again.`,
      runCommand,
    };
  }
  return null;
}
