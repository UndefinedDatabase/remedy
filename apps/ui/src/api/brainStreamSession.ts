// The knot neither half can tie alone: the host dispatches INTO a runner that
// does not exist when the host is built, and the runner drives a host it must
// already hold. Tying it here rather than inside the React hook keeps the whole
// composition — start, subscribe, close — under the node-environment vitest,
// for the same reason the driver and the runner are not React either.
import { createBrainStreamHost } from "./brainStreamHost";
import type { BrainStreamHostDeps } from "./brainStreamHost";
import { createBrainStreamRunner } from "./brainStreamRunner";
import type { BrainStreamView } from "./brainStreamRunner";

/** Exactly what `useSyncExternalStore` needs, plus the lifetime a socket owner
 *  owes its caller. */
export interface BrainStreamSession {
  subscribe(listener: () => void): () => void;
  view(): BrainStreamView;
  start(): void;
  /** Stop the runner AND close the socket. Stopping alone silences the client
   *  while leaving its EventSource open, so a remounting cockpit would leak one
   *  connection per mount. */
  close(): void;
}

/** Compose the real adapter with the runner store. Building a session opens
 *  nothing: only `start` connects, so a session created during a render React
 *  then discards costs a closure and never a socket. */
export function createBrainStreamSession(deps: BrainStreamHostDeps): BrainStreamSession {
  const host = createBrainStreamHost((event) => { runner.dispatch(event); }, deps);
  const runner = createBrainStreamRunner(host);
  return {
    subscribe: runner.subscribe,
    view: runner.view,
    start: runner.start,
    close(): void {
      runner.stop();
      host.close();
    },
  };
}
