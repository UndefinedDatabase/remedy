// The React half of the ledger, deliberately thin: every rule — merge,
// prefix, cursor arithmetic, stall and retry — lives in brainLedger.ts,
// where the node-environment vitest can reach it. What is left here is
// state, two effects and the one path builder both transports share:
// `readPage` is built from `eventsSincePath` (brainStreamDeps.ts) by
// RemedyShell.tsx and handed down through BrainGraphStage.tsx.
import { useEffect, useRef, useState } from "react";
import {
  brainLedgerLive,
  brainLedgerReceived,
  brainLedgerRequest,
  initialBrainLedgerLoad,
} from "./brainLedger";
import type { BrainLedger, BrainLedgerLoad } from "./brainLedger";
import type { BrainEventRow } from "./brainOntology";

export function useBrainLedger(
  jobId: string,
  liveRows: readonly BrainEventRow[],
  readPage: (cursor: number) => Promise<unknown>,
): BrainLedger {
  // Guards a read in flight, and dropping a response whose job has moved on.
  // Both live in a REF rather than state: a state flip would change the
  // request effect's own key below and cancel the read it is meant to guard.
  const inFlightCursorRef = useRef<number | null>(null);
  const currentJobRef = useRef(jobId);

  const [held, setHeld] = useState<{ jobId: string; load: BrainLedgerLoad }>(
    () => ({ jobId, load: initialBrainLedgerLoad() }),
  );
  // A different job starts over: the previous job's rows, cursor and
  // in-flight guard all belong to a ledger this render has already left
  // behind. Adjusting state WHILE RENDERING (React's own escape hatch for a
  // key change) bails this render out before the effects below can act on
  // the stale load against the new job.
  let state = held;
  if (held.jobId !== jobId) {
    state = { jobId, load: initialBrainLedgerLoad() };
    inFlightCursorRef.current = null;
    setHeld(state);
  }

  useEffect(() => { currentJobRef.current = jobId; }, [jobId]);

  useEffect(() => {
    setHeld((current) => {
      const next = brainLedgerLive(current.load, liveRows);
      return next === current.load ? current : { jobId: current.jobId, load: next };
    });
  }, [liveRows]);

  const cursor = brainLedgerRequest(state.load);
  useEffect(() => {
    if (cursor === null || inFlightCursorRef.current === cursor) return;
    inFlightCursorRef.current = cursor;
    const requestedJob = jobId;
    readPage(cursor).then(
      (payload) => {
        inFlightCursorRef.current = null;
        if (currentJobRef.current !== requestedJob) return;
        setHeld((current) => ({ jobId: current.jobId, load: brainLedgerReceived(current.load, cursor, payload) }));
      },
      () => {
        inFlightCursorRef.current = null;
        if (currentJobRef.current !== requestedJob) return;
        setHeld((current) => ({ jobId: current.jobId, load: brainLedgerReceived(current.load, cursor, null) }));
      },
    );
  }, [cursor, jobId, readPage]);

  return state.load.ledger;
}
