// T5_F292 T003, DECISION F292 D6: the rules of the hunk controls — which hunks a person may
// decide, the draft they start from, and the one decision a send records. The write door
// answers every refused hunk decision with the same fixed sentence and never its reason
// (DECISIONS F009 D18 and D22), so every refusal these rules can see coming is stated here,
// before the send: a change that cannot be named hunk by hunk, a hunk without an id, a decision
// that decides nothing, and a rejection without a reason. Pure: no fetch, clock, storage or DOM.
import type { DiffEnvelope } from "./diffViewModel";
import { UNIDENTIFIED_HUNK_ID_PREFIX } from "./diffViewModel";
import type { HunkDecisions, HunkState } from "./hunkDecisions";

/** One hunk's decision as the person is making it. */
export interface HunkDraftEntry {
  state: HunkState;
  reason: string;
}

/** Every decidable hunk of the diff, by id, in no particular key order; the diff gives the order. */
export type HunkDraft = Readonly<Record<string, HunkDraftEntry>>;

/** The arguments `patch.approve-hunks` takes: the task run (left out for the job's own diff), the
 *  approved hunk ids and the rejected ones with their reasons, each in the diff's order. */
export interface HunkDecisionArgs {
  task_run?: string;
  approved: string[];
  rejected: { id: string; reason: string }[];
}

/** Why no hunk of this diff can be decided, or `null` when they can: no diff is there, or the
 *  diff was cut short, which the recorder refuses because it cannot name every hunk. */
export function hunkControlsBlocked(envelope: DiffEnvelope): string | null {
  if (!envelope.available) return "No change is available to decide.";
  if (envelope.truncated) {
    return "This change was cut short, so not every hunk can be named; it cannot be decided hunk by hunk.";
  }
  return null;
}

/** Whether one hunk can be decided: a hunk the server sent no id for has a placeholder id the
 *  browser made up, which the recorder would refuse as unknown. */
export function hunkIsDecidable(hunkId: string): boolean {
  return !hunkId.startsWith(UNIDENTIFIED_HUNK_ID_PREFIX);
}

/** The decidable hunk ids of the diff, in its order. */
export function decidableHunkIds(envelope: DiffEnvelope): string[] {
  return envelope.files.flatMap((file) => file.hunks.map((hunk) => hunk.id)).filter(hunkIsDecidable);
}

/** The draft a person starts from: each decidable hunk as the record has it, or pending. A
 *  recorded row for a hunk this diff does not show is left out, because sending it would be
 *  refused as unknown. */
export function hunkDraftOf(envelope: DiffEnvelope, recorded: HunkDecisions): HunkDraft {
  const rows = new Map(recorded.hunks.map((row) => [row.id, row]));
  const draft: Record<string, HunkDraftEntry> = {};
  for (const id of decidableHunkIds(envelope)) {
    const row = rows.get(id);
    draft[id] = row === undefined ? { state: "pending", reason: "" } : { state: row.state, reason: row.reason };
  }
  return draft;
}

/** Whether the draft differs from what is recorded, hunk by hunk, the reasons compared trimmed. */
export function hunkDraftChanged(envelope: DiffEnvelope, recorded: HunkDecisions, draft: HunkDraft): boolean {
  const start = hunkDraftOf(envelope, recorded);
  return decidableHunkIds(envelope).some((id) => draft[id]?.state !== start[id]?.state
    || (draft[id]?.state === "rejected" && draft[id].reason.trim() !== start[id].reason.trim()));
}

/** The one decision a send records, or the reason it cannot be sent. Every decidable hunk the
 *  draft leaves pending stays pending in the record, because a decision replaces the record
 *  whole. */
export function hunkDecisionArgs(envelope: DiffEnvelope, draft: HunkDraft): { args: HunkDecisionArgs } | { problem: string } {
  const ids = decidableHunkIds(envelope);
  const approved = ids.filter((id) => draft[id]?.state === "approved");
  const rejected = ids.filter((id) => draft[id]?.state === "rejected").map((id) => ({ id, reason: draft[id].reason.trim() }));
  if (approved.length === 0 && rejected.length === 0) return { problem: "Decide at least one hunk before recording." };
  if (rejected.some((entry) => entry.reason === "")) return { problem: "Give each rejected hunk a reason." };
  const args: HunkDecisionArgs = { approved, rejected };
  if (envelope.taskId.trim() !== "") args.task_run = envelope.taskId;
  return { args };
}

/** How many hunks the draft approves, rejects and leaves pending, in words. */
export function hunkTally(envelope: DiffEnvelope, draft: HunkDraft): string {
  const ids = decidableHunkIds(envelope);
  const count = (state: HunkState) => ids.filter((id) => draft[id]?.state === state).length;
  return `${count("approved")} approved, ${count("rejected")} rejected, ${count("pending")} pending`;
}
