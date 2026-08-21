// The React half of the brain stream, and deliberately the ONLY part of it that
// is React at all: every rule this client has lives in brainStream.ts,
// brainStreamDriver.ts, brainStreamRunner.ts and brainStreamSession.ts, where
// the node-environment vitest can reach it. What is left here — subscribe to a
// store, start it, close it on unmount — is gated by a tests/ui_contracts/
// source contract, the style this repository uses for every React component.
import { useEffect, useMemo, useRef, useSyncExternalStore } from "react";
import { createBrainStreamSession } from "./brainStreamSession";
import type { BrainStreamHostDeps } from "./brainStreamHost";
import type { BrainStreamView } from "./brainStreamRunner";

/** Subscribe the cockpit to one job's event stream.
 *
 *  The session is keyed on `jobId` ALONE. `makeDeps` is read through a ref
 *  instead of a dependency, because a caller that writes its deps inline hands
 *  a new function every render, and a memo that honoured that identity would
 *  tear down the stream and open a fresh EventSource on every parent render. */
export function useBrainStream(
  jobId: string,
  makeDeps: (jobId: string) => BrainStreamHostDeps,
): BrainStreamView {
  const latestMakeDeps = useRef(makeDeps);
  useEffect(() => { latestMakeDeps.current = makeDeps; }, [makeDeps]);

  const session = useMemo(() => createBrainStreamSession(latestMakeDeps.current(jobId)), [jobId]);

  // Closing on unmount is the whole reason the session exposes `close`: React
  // remounts components freely, and a cleanup that only forgot the session
  // would leave its EventSource open for the lifetime of the page.
  useEffect(() => {
    session.start();
    return () => { session.close(); };
  }, [session]);

  return useSyncExternalStore(session.subscribe, session.view, session.view);
}
