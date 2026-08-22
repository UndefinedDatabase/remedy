// One activity-feed row, projected from one brain-stream frame. T002's rows
// render THIS and never the raw envelope, so the naming trap below is resolved
// once here instead of in every component that reads a stream event.
import { humanizeStreamEvent } from "./humanize";
import type { BrainStreamFrame } from "./brainStream";

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
  return {
    seq: frame.seq,
    receivedAtMs,
    kind,
    line: humanized.line,
    known: humanized.known,
    timestamp: stringField(envelope, "timestamp"),
    outcome: stringField(envelope, "outcome"),
    taskId: stringField(envelope, "task_id"),
  };
}
