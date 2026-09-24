// The job's own event LEDGER, merged from two sources into one: pages of
// `events-since` read from the server and the live stream's ring. No React,
// no DOM, no URL — `useBrainLedger.ts` is the thin binding that calls this
// from a component; every rule that decides what the graph is ALLOWED to
// draw lives here, where the node-environment vitest can reach it.
//
// DECISION F019 D5: the graph folds only the CONTIGUOUS PREFIX the client
// holds in full — every seq from 0 up to the first one it does not have —
// never the rows past a hole. A hole is a live frame that skipped a seq, a
// stream that joined mid-ledger, or a tab that slept through part of it; it
// is filled by paging `events-since` from the first missing seq, and until
// it is filled the graph shows the state before the hole rather than a state
// the ledger has not fully told it (no ghost: graph_spec §8).
import { framesOf } from "../../api/brainStreamDeps";
import { feedRowOf } from "../../api/feedRow";
import type { BrainEventRow } from "./brainOntology";

/** The rows this client holds, one per seq, sorted by seq; `known` is the
 *  ledger length the client knows exists — from a page's `cursor`, or from a
 *  held row's own seq + 1 — and is `null` before anything has been read. */
export interface BrainLedger {
  rows: readonly BrainEventRow[];
  known: number | null;
}

/** A client that has read nothing yet and knows nothing about the ledger's
 *  length. */
export function emptyBrainLedger(): BrainLedger {
  return { rows: [], known: null };
}

/** The max of three optional numbers, `null` only while all three are
 *  absent — the rule `known` follows below, named once so the three call
 *  sites (old `known`, a page's `knownLength`, a held row's own length)
 *  cannot drift apart. */
function maxKnown(a: number | null, b: number | null, c: number | null): number | null {
  let result: number | null = null;
  for (const value of [a, b, c]) {
    if (value === null) continue;
    result = result === null ? value : Math.max(result, value);
  }
  return result;
}

/** Merge a page or a live batch into the ledger. Rows are unique by seq with
 *  the ALREADY-HELD row winning — the same "first wins" rule
 *  `rebuildBrainModel` applies to a set of rows with a duplicate seq — sorted
 *  by seq afterward. `known` rises to the max of the ledger's own `known`,
 *  the caller's `knownLength` and one past the highest seq now held. Returns
 *  the SAME object when nothing changed (no new seq, same `known`), which is
 *  what lets a reader compare the ledger by reference. */
export function mergeBrainRows(
  ledger: BrainLedger,
  rows: readonly BrainEventRow[],
  knownLength: number | null,
): BrainLedger {
  const bySeq = new Map<number, BrainEventRow>();
  for (const row of ledger.rows) bySeq.set(row.seq, row);
  let added = false;
  for (const row of rows) {
    if (bySeq.has(row.seq)) continue;
    bySeq.set(row.seq, row);
    added = true;
  }
  let maxHeldSeq = -1;
  for (const seq of bySeq.keys()) maxHeldSeq = Math.max(maxHeldSeq, seq);
  const fromHeld = maxHeldSeq >= 0 ? maxHeldSeq + 1 : null;
  const known = maxKnown(ledger.known, knownLength, fromHeld);
  if (!added && known === ledger.known) return ledger;
  const nextRows = [...bySeq.values()].sort((a, b) => a.seq - b.seq);
  return { rows: nextRows, known };
}

/** The rows whose seqs run 0, 1, 2, … without a hole, stopping at the first
 *  missing one — empty when seq 0 itself is missing. `ledger.rows` is always
 *  sorted and unique by seq (an invariant `mergeBrainRows` keeps), so a
 *  single ascending walk finds the break. */
export function brainLedgerPrefix(ledger: BrainLedger): BrainEventRow[] {
  const prefix: BrainEventRow[] = [];
  let next = 0;
  for (const row of ledger.rows) {
    if (row.seq !== next) break;
    prefix.push(row);
    next += 1;
  }
  return prefix;
}

/** The next `events-since` cursor to read: `0` before anything is known;
 *  else the smallest seq in `[0, known)` not yet held; `null` once every seq
 *  the client knows about is held. */
export function nextBrainLedgerCursor(ledger: BrainLedger): number | null {
  if (ledger.known === null) return 0;
  const held = new Set(ledger.rows.map((row) => row.seq));
  for (let seq = 0; seq < ledger.known; seq += 1) {
    if (!held.has(seq)) return seq;
  }
  return null;
}

/** The events-since envelope's `cursor`, read as a finite length ≥ 0 — the
 *  ledger's own length, unlike `snapshotSeqOf` (brainStreamDeps.ts), which
 *  turns that same field into a POSITION and refuses an empty ledger. A
 *  malformed or missing cursor yields `null` rather than a guessed length. */
function knownLengthOf(payload: unknown): number | null {
  if (payload === null || typeof payload !== "object") return null;
  const cursor = (payload as { cursor?: unknown }).cursor;
  const length = typeof cursor === "string" ? Number(cursor) : cursor;
  return typeof length === "number" && Number.isFinite(length) && length >= 0 ? length : null;
}

/** One `events-since` page, turned into ledger rows through the one frame
 *  parser (`feedRowOf`, DECISION F019 D1 (2)) and the ledger length its
 *  `cursor` carries. */
export function brainLedgerPage(payload: unknown): { rows: BrainEventRow[]; known: number | null } {
  const rows = framesOf(payload).map((frame) => feedRowOf(frame, 0));
  return { rows, known: knownLengthOf(payload) };
}

/** The loader's own pure state: the ledger merged so far, and the cursor a
 *  read has already come back empty or failed for (`stalled`) — the request
 *  rule below refuses to re-issue that SAME cursor until a live frame proves
 *  the ledger has moved. */
export interface BrainLedgerLoad {
  ledger: BrainLedger;
  stalled: number | null;
}

export function initialBrainLedgerLoad(): BrainLedgerLoad {
  return { ledger: emptyBrainLedger(), stalled: null };
}

/** The next cursor a caller should read, or `null` when the ledger is
 *  complete OR when that cursor is the one already known to answer empty
 *  (`stalled`) — asking it again would only stall a second time. */
export function brainLedgerRequest(load: BrainLedgerLoad): number | null {
  const cursor = nextBrainLedgerCursor(load.ledger);
  if (cursor === null || cursor === load.stalled) return null;
  return cursor;
}

/** Apply the response to a read issued for `cursor`. `payload === null`
 *  means the read failed and merges nothing; either way, an unchanged ledger
 *  stalls this cursor and a changed one clears the stall (a fresh cursor is
 *  free to be requested again next time). */
export function brainLedgerReceived(
  load: BrainLedgerLoad,
  cursor: number,
  payload: unknown | null,
): BrainLedgerLoad {
  const page = payload === null ? { rows: [], known: null } : brainLedgerPage(payload);
  const ledger = mergeBrainRows(load.ledger, page.rows, page.known);
  const stalled = ledger === load.ledger ? cursor : null;
  if (ledger === load.ledger && stalled === load.stalled) return load;
  return { ledger, stalled };
}

/** Fold the live ring's rows into the ledger. A new frame is the retry
 *  signal after a failed or empty read, so a ledger the live rows actually
 *  changed clears any stall; one they did not leaves it exactly as it was. */
export function brainLedgerLive(load: BrainLedgerLoad, rows: readonly BrainEventRow[]): BrainLedgerLoad {
  const ledger = mergeBrainRows(load.ledger, rows, null);
  if (ledger === load.ledger) return load;
  return { ledger, stalled: null };
}
