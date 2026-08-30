// THE BROWSER-LOCAL STORAGE EDGE for `DigestVisibilityPort` (T5_F040 T002).
// `digestVisibility.ts` DECLARES the port and IMPLEMENTS nothing; DECISION
// F040 D8 rules that a dismissal and a last-seen instant both persist
// browser-locally, keyed per job, and this module is that persistence,
// nothing else. It is this repository's first localStorage-backed module.
//
// KEY FORMAT: one key per (job, concern) pair, a pure function of the job id
// and a fixed per-concern segment — `remedy:digest:dismissal:<jobId>` and
// `remedy:digest:last-seen:<jobId>`. Two distinct job ids and the two
// concerns therefore always produce four distinct keys: the job id occupies
// its own segment and never collides with the fixed concern segment, and the
// two concern segments ("dismissal", "last-seen") are themselves distinct.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// IT READS NO CLOCK. `writeDismissal`'s `dismissedAtMs` and `writeLastSeen`'s
// `seenAtMs` both arrive as parameters; `Date.now` occurs zero times here.
// The one clock read this feature needs already lives at the dismiss handler
// in `DigestHeroCard.tsx` (constraint 7 of the F040 R11 block), and a second
// read here would be a second edge for a value DECISION F040 D8 already
// assigns one home.
// IT OPENS NO SOCKET. No `fetch`, no `XMLHttpRequest`: this module only ever
// touches the storage object handed to it.
// IT REACHES FOR NO GLOBAL. `browserDigestVisibilityPort`'s one parameter is
// typed against `Pick<Storage, "getItem" | "setItem">` — the DOM lib's own
// `Storage` interface, narrowed to the two methods this module actually
// calls, rather than a bespoke interface invented for this file, since
// `Storage` already has exactly this shape. Narrowing to the two methods
// (rather than requiring all of `Storage`) is what lets a test build the
// smallest fake that satisfies this module without also having to fake
// `removeItem`, `clear`, `key` and `length`, none of which this module calls.
// This is also what makes the module testable without `vi.stubGlobal` — no
// test under `apps/ui/src` patches a global today, and this file does not
// start that pattern: `window` and `localStorage` occur zero times in this
// module's executable source. A REAL binder that closes over
// `window.localStorage` belongs at the MOUNT, in a later round, exactly
// where `browserBrainStreamEnv(window)` binds its own globals for
// `RemedyShell.tsx` to call.
//
// `browserDigestPort.test.ts` pins this module's shape and its rules.

import type { DigestVisibilityPort } from "./digestVisibility";

const DISMISSAL_SEGMENT = "dismissal";
const LAST_SEEN_SEGMENT = "last-seen";

/** The one key-building rule, so the two concerns can never drift into two
 *  different formats. */
function digestStorageKey(concern: string, jobId: string): string {
  return "remedy:digest:" + concern + ":" + jobId;
}

/** A stored string read back as a finite number, or `null` for every other
 *  case — a missing key, an empty string, or a value that does not parse to a
 *  finite number all read as ABSENT, never as `NaN` and never as a thrown
 *  exception. The same "an absence is a state, not an error" posture
 *  `digestVisibility.ts`'s own `DigestDismissal` already takes. */
function readStoredInstant(
  storage: Pick<Storage, "getItem" | "setItem">,
  concern: string,
  jobId: string,
): number | null {
  const raw = storage.getItem(digestStorageKey(concern, jobId));
  if (raw === null) {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
}

/** Stores the given instant as a string under that pair's own key. Reads no
 *  clock of its own — the instant is always the caller's. */
function writeStoredInstant(
  storage: Pick<Storage, "getItem" | "setItem">,
  concern: string,
  jobId: string,
  instantMs: number,
): void {
  storage.setItem(digestStorageKey(concern, jobId), String(instantMs));
}

/** THE FACTORY. Takes its storage injected — never `window.localStorage`
 *  directly — so this module is testable with a small fake and binds to the
 *  real global only at the mount, next round. */
export function browserDigestVisibilityPort(
  storage: Pick<Storage, "getItem" | "setItem">,
): DigestVisibilityPort {
  return {
    readDismissal(jobId: string): number | null {
      return readStoredInstant(storage, DISMISSAL_SEGMENT, jobId);
    },
    writeDismissal(jobId: string, dismissedAtMs: number): void {
      writeStoredInstant(storage, DISMISSAL_SEGMENT, jobId, dismissedAtMs);
    },
    readLastSeen(jobId: string): number | null {
      return readStoredInstant(storage, LAST_SEEN_SEGMENT, jobId);
    },
    writeLastSeen(jobId: string, seenAtMs: number): void {
      writeStoredInstant(storage, LAST_SEEN_SEGMENT, jobId, seenAtMs);
    },
  };
}
