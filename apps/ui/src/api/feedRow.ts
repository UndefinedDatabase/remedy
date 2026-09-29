// One activity-feed row, projected from one brain-stream frame. T002's rows
// render THIS and never the raw envelope, so the naming trap below is resolved
// once here instead of in every component that reads a stream event.
import { humanizeStreamEvent } from "./humanize";
import type { BrainStreamFrame } from "./brainStream";
import { readSteeringAck, steeringAckLine } from "./steeringAck";
import { readSteeringNote } from "./steeringNote";
import { budgetTickFiguresOf } from "./budgetTick";
import type { BudgetTickFigures } from "./costMetric";

/** What one activity-feed row shows. `seq` is the ledger position the row
 *  carries and jumps to; `known` is what a dev console note counts.
 *  `receivedAtMs` is the arrival instant the host stamped from the injected
 *  clock (R23). The recency dot subtracts it from that SAME clock, which the
 *  envelope's own `timestamp` could not serve: it is a server-clock string
 *  ui_server.py passes through unparsed, empty where the run log has none, so
 *  a server running behind would render as a dead agent. */
export interface FeedRow {
  seq: number;
  receivedAtMs: number;
  kind: string;
  line: string;
  known: boolean;
  timestamp: string;
  outcome: string;
  /** The task this event belongs to, or "" when it belongs to none. Carried by
   *  the envelope since DECISION F021 D2; `feedFocus.ts` turns it into the
   *  graph node a row click jumps to. */
  taskId: string;
  /** The attempt (one execution of a task, one test run, or one long-run
   *  cycle) this row belongs to, or "" when the envelope carries none.
   *  DECISION F288 D3 (2). */
  attemptId?: string;
  /** `plan_approved`'s approved task ids, in plan order, or `[]` for every
   *  other row. DECISION F288 D3 (2). */
  planTaskIds?: readonly string[];
  /** "operator" for a steering note's own row, absent for every other row: the
   *  feed shows the note as the operator's own line rather than the catalog's
   *  third-person description of it. DECISION F030 D3. */
  author?: "operator";
  /** A `budget.tick` frame's own figures, carried opaque, absent on every
   *  other row — never `undefined` on a present key, so a card can tell "no
   *  tick yet" from "a tick with nothing in it" (DECISION F039 D5 (3)). */
  budget?: BudgetTickFigures;
}

// The naming trap this module exists to resolve, measured at `f5f01585` in
// `_safe_event_summary` (packages/orchestration/ui_server.py): a frame's
// `event` field holds the whole SAFE ENVELOPE — seq, event, timestamp and
// outcome — and the envelope's OWN `event` field is the kind string. The kind
// is therefore `frame.event.event`, which reads like a typo and is not one.
function envelopeOf(frame: BrainStreamFrame): Record<string, unknown> {
  return typeof frame.event === "object" && frame.event !== null
    ? frame.event as Record<string, unknown>
    : {};
}

/** Read one envelope field as a string, defaulting to "" for anything else.
 *  The envelope is parsed JSON from a server this client does not control, so
 *  every field is CHECKED rather than asserted. */
function stringField(envelope: Record<string, unknown>, name: string): string {
  const value = envelope[name];
  return typeof value === "string" ? value : "";
}

/** `plan_approved`'s `plan.task_ids`, in order, dropping any non-string entry;
 *  `[]` when `plan` is absent, not an object, or its `task_ids` not an array.
 *  DECISION F288 D3 (2). */
function planTaskIdsOf(envelope: Record<string, unknown>): readonly string[] {
  const plan = envelope["plan"];
  if (typeof plan !== "object" || plan === null) {
    return [];
  }
  const taskIds = (plan as Record<string, unknown>)["task_ids"];
  if (!Array.isArray(taskIds)) {
    return [];
  }
  return taskIds.filter((value): value is string => typeof value === "string");
}

/** Project one frame into the row a feed renders. Total by construction: every
 *  frame yields a row, because an event the catalog cannot name still happened
 *  and a feed that dropped it would tell a story with holes in it. */
export function feedRowOf(
  frame: BrainStreamFrame,
  receivedAtMs: number,
): FeedRow {
  const envelope = envelopeOf(frame);
  const kind = stringField(envelope, "event");
  const humanized = humanizeStreamEvent(kind);
  // F264 T003: a steering acknowledgement shows WHAT was understood and FROM WHICH ROUND,
  // the two halves an acknowledgement is useless without, rather than the catalog's
  // generic line; a frame whose field is malformed keeps the catalog line.
  const ack = readSteeringAck(envelope);
  // F030 T003: a steering note shows the operator's OWN text, verbatim, as the operator's
  // own row — never the catalog's third-person description of the fact it was recorded.
  const note = readSteeringNote(envelope);
  // DECISION F039 D5 (3): a budget tick's figures ride on their OWN row, absent
  // rather than `undefined` on every other kind, so a card can read "cost so far".
  const budget = budgetTickFiguresOf(frame);
  return {
    seq: frame.seq,
    receivedAtMs,
    kind,
    line: note ? note.text : ack ? steeringAckLine(ack) : humanized.line,
    known: humanized.known,
    timestamp: stringField(envelope, "timestamp"),
    outcome: stringField(envelope, "outcome"),
    taskId: stringField(envelope, "task_id"),
    attemptId: stringField(envelope, "attempt_id"),
    planTaskIds: planTaskIdsOf(envelope),
    ...(note ? { author: "operator" as const } : {}),
    ...(budget !== null ? { budget } : {}),
  };
}
