/**
 * The task detail's "Who did what" section (F035 T003, DECISION F035 D5).
 *
 * The section renders the ledger `packages/orchestration/ownership.py` builds and
 * `packages/orchestration/ownership_phrases.py` words into one plain sentence each, as the
 * browser's `ownership` route serves them (`GET /api/jobs/<job_id>/ownership`). This module
 * decodes that view, builds its path, labels each action with one short chip word, and answers
 * the entries that belong to one task — those it names directly, or names as a consequence.
 *
 * IT OPENS NO SOCKET, READS NO CLOCK AND KEEPS NO STORAGE: the one read goes through
 * `loadOwnershipView` in `remedyApi.ts`, and the section owns nothing but what it is handed.
 *
 * THE DECODER REFUSES WHOLE. An entry, actor or consequence it cannot read makes the whole view
 * unreadable rather than silently shorter — a history that quietly drops one action would say
 * less than the job actually did, and this surface exists to say exactly what happened.
 */

/** One actor, as `ownership_actor` in `packages/orchestration/ownership.py` records it. */
export interface OwnershipActor {
  kind: string;
  door: string;
  recordedAs: string;
  tokenNumber: number;
  autoApproved: boolean;
}

/** What one entry caused, as `_CONSEQUENCE_KEYS` in `ownership.py` shapes it. */
export interface OwnershipConsequence {
  kind: string;
  taskIds: string[];
  ref: string;
}

/** One ledger entry with its rendered sentence, as `ownership_view` in `ownership_phrases.py`
 *  answers it — the ledger's own dict, minus `detail`, plus `sentence`. */
export interface OwnershipEntry {
  recordRef: string;
  ts: string;
  actor: OwnershipActor;
  action: string;
  taskId: string;
  text: string;
  consequence: OwnershipConsequence;
  sentence: string;
}

/** The whole view `ownership_view` answers: every entry, or none with a reason. */
export interface OwnershipView {
  schema: string;
  jobId: string;
  entries: OwnershipEntry[];
  error: string;
}

const OWNERSHIP_SCHEMA = "remedy.ownership.v1";

function recordOf(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>) : null;
}

function textOf(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function actorOf(value: unknown): OwnershipActor | null {
  const actor = recordOf(value);
  if (actor === null) return null;
  const kind = textOf(actor["kind"]);
  const door = textOf(actor["door"]);
  const recordedAs = textOf(actor["recorded_as"]);
  const tokenNumber = actor["token_number"];
  const autoApproved = actor["auto_approved"];
  if (kind === null || door === null || recordedAs === null
      || typeof tokenNumber !== "number" || typeof autoApproved !== "boolean") {
    return null;
  }
  return { kind, door, recordedAs, tokenNumber, autoApproved };
}

function consequenceOf(value: unknown): OwnershipConsequence | null {
  const consequence = recordOf(value);
  if (consequence === null) return null;
  const kind = textOf(consequence["kind"]);
  const ref = textOf(consequence["ref"]);
  const rawTaskIds = consequence["task_ids"];
  if (kind === null || ref === null || !Array.isArray(rawTaskIds)) return null;
  const taskIds = rawTaskIds.map(textOf);
  if (taskIds.some((t) => t === null)) return null;
  return { kind, taskIds: taskIds as string[], ref };
}

function entryOf(value: unknown): OwnershipEntry | null {
  const entry = recordOf(value);
  if (entry === null) return null;
  const recordRef = textOf(entry["record_ref"]);
  const ts = textOf(entry["ts"]);
  const actor = actorOf(entry["actor"]);
  const action = textOf(entry["action"]);
  const taskId = textOf(entry["task_id"]);
  const text = textOf(entry["text"]);
  const consequence = consequenceOf(entry["consequence"]);
  const sentence = textOf(entry["sentence"]);
  if (recordRef === null || ts === null || actor === null || action === null || taskId === null
      || text === null || consequence === null || sentence === null) {
    return null;
  }
  return { recordRef, ts, actor, action, taskId, text, consequence, sentence };
}

/** The ownership route's envelope, or `null` when any part of it cannot be read. Never throws. */
export function decodeOwnershipView(raw: unknown): OwnershipView | null {
  const payload = recordOf(raw);
  if (payload === null) return null;
  const schema = textOf(payload["schema"]);
  const jobId = textOf(payload["job_id"]);
  const rawEntries = payload["entries"];
  const error = textOf(payload["error"]);
  if (schema !== OWNERSHIP_SCHEMA || jobId === null || !Array.isArray(rawEntries) || error === null) {
    return null;
  }
  const entries = rawEntries.map(entryOf);
  if (entries.some((e) => e === null)) return null;
  return { schema, jobId, entries: entries as OwnershipEntry[], error };
}

/** The job's ownership route, with the token the cockpit already carries. */
export function ownershipViewPath(request: { jobId: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl ?? "";
  return `${base}/api/jobs/${encodeURIComponent(request.jobId)}/ownership`
    + `?token=${encodeURIComponent(request.token)}`;
}

/** The short chip word for each action the phrase catalog words (F035 T002, DECISION F035 D3).
 *  Every key here is one of that catalog's own actions; `ownershipChipWord` answers "Action"
 *  for anything else, so a future action this chip never learned still reads as something. */
export const OWNERSHIP_CHIP_WORDS: Record<string, string> = {
  task_vetoed: "Veto",
  veto_answered: "Veto answer",
  task_injected: "Added",
  subtree_rerun: "Rerun",
  plan_edited: "Plan edit",
  task_edited: "Edit",
  steering_sent: "Steering",
  note_sent: "Note",
  job_paused: "Pause",
  task_paused: "Pause",
  job_resumed: "Resume",
  task_resumed: "Resume",
  job_stopped: "Stop",
  hunk_approved: "Hunk approved",
  hunk_rejected: "Hunk rejected",
  decision_answered: "Answer",
  clarification_answered: "Plan question",
  plan_approved: "Approval",
  plan_rejected: "Rejection",
};

/** The chip word for one entry's action, or the generic fallback. */
export function ownershipChipWord(action: string): string {
  return OWNERSHIP_CHIP_WORDS[action] ?? "Action";
}

/** The one line the section shows for a view that could not be read; never the server's own
 *  error text (`ux_spec.md` §17 forbids raw internals in copy). */
export const OWNERSHIP_UNREADABLE_LINE = "Who did what could not be read for this job.";

/** The one line the evidence panel's ownership tab shows for a job with no entry at all. */
export const OWNERSHIP_EMPTY_LINE = "No action is recorded for this job yet.";

/** One state of the evidence panel's ownership tab (DECISION F035 D6): loading while the read is
 *  in flight, the fixed unreadable line for a `null` view or one whose `error` is not "", the
 *  fixed empty line for a view with no entry, or every entry in the view's own order. PURE, so
 *  the tab's four readings are goldened here rather than through a render. */
export type OwnershipPanelState =
  | { kind: "loading" }
  | { kind: "unreadable"; line: string }
  | { kind: "empty"; line: string }
  | { kind: "entries"; entries: OwnershipEntry[] };

/** The ownership tab's one state function. */
export function ownershipPanelState(view: OwnershipView | null, loaded: boolean): OwnershipPanelState {
  if (!loaded) return { kind: "loading" };
  if (view === null || view.error !== "") return { kind: "unreadable", line: OWNERSHIP_UNREADABLE_LINE };
  if (view.entries.length === 0) return { kind: "empty", line: OWNERSHIP_EMPTY_LINE };
  return { kind: "entries", entries: view.entries };
}

/** The entries that belong to one task: those it names directly, or that name it as a
 *  consequence, in the view's own order. `""` names no task, so it answers none. */
export function ownershipEntriesForTask(view: OwnershipView, taskId: string): OwnershipEntry[] {
  if (taskId === "") return [];
  return view.entries.filter((entry) =>
    entry.taskId === taskId || entry.consequence.taskIds.includes(taskId));
}

/** The run-log events whose frame means the ownership view is worth reading again — every
 *  event a ledger class of `packages/orchestration/ownership.py` reads. */
export const OWNERSHIP_REFRESH_EVENTS = [
  "task_vetoed",
  "veto_proposal_answered",
  "task_injected",
  "subtree_rerun_prepared",
  "plan_approved",
  "job_paused",
  "task_paused",
  "job_resumed",
  "task_resumed",
  "job_stopped",
  "steering_message_received",
  "steering_message_consumed",
  "task_decision_answered",
] as const;

/** The newest stream position announcing one of `OWNERSHIP_REFRESH_EVENTS`, or 0; a change
 *  means "read again" — the rule `lessonsRefreshKey` applies to its own one kind. */
export function ownershipRefreshKey(recent: readonly { seq: number; kind: string }[]): number {
  const kinds: readonly string[] = OWNERSHIP_REFRESH_EVENTS;
  return recent.reduce(
    (newest, row) => (kinds.includes(row.kind) && row.seq > newest ? row.seq : newest), 0);
}
