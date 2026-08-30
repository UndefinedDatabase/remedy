import { describe, it, expect } from "vitest";
import { decodeJobDigest } from "./jobDigest";
import { browserDigestVisibilityPort } from "./browserDigestPort";
import { digestVisibility } from "./digestVisibility";
import { digestCtaText } from "./digestCardCopy";

// The feature file's own end-to-end script (T5_F040.md, Task slicing, T003):
// finish a fake job while the UI is away, reopen, the hero shows the right
// CTA, dismiss it, and it does not re-show — then new activity re-arms it.
// This file is the one place all four T002 client seams are chained together,
// because none of their own test files exercises the COMPOSITION the
// feature's Acceptance describes.
//
// Shaped after `tests/orchestration/fixtures/job_digest/golden/
// blocked_with_decisions.json` (hand-copied per the convention
// `jobDigest.test.ts` already establishes, so the fixture and the wire cannot
// drift apart in this file's imagination) — a settled, decision-blocked job
// whose `primary_action.label` carries the real backticked CLI command the
// `open-decision` rule of `recommended_next_action` appends in
// `packages/orchestration/run_report.py`.
const ENVELOPE = {
  version: 1,
  job_id: "e2e-job-1",
  state: "paused",
  headline: "The run is paused and its terminal status is blocked.",
  cost: { value: "not-measured", basis: "absent" },
  ownership: [] as string[],
  decisions: { open_count: 2, peak_urgency: 2400 },
  primary_action: {
    label:
      'Answer the open decision: `remedy decision resolve e2e-job- td:d1 --reason "postgres"`',
    rule_id: "open-decision",
  },
};

// A minimal in-memory `Storage`, narrowed to the two methods
// `browserDigestVisibilityPort` actually calls — the same narrowing the
// port's own module documents, so this fake needs no `removeItem`, `clear`,
// `key` or `length`.
function fakeStorage(): Pick<Storage, "getItem" | "setItem"> {
  const map = new Map<string, string>();
  return {
    getItem: (key: string) => (map.has(key) ? map.get(key)! : null),
    setItem: (key: string, value: string) => {
      map.set(key, value);
    },
  };
}

const T_AWAY = 1_700_000_000_000; // the UI's last known-open instant
const T_FINISH = T_AWAY + 60_000; // the job finishes while the UI is away
const T_REOPEN = T_AWAY + 300_000; // the operator reopens the UI

describe("the completion digest, end to end (T5_F040 T003)", () => {
  it("shows the right CTA on reopen, holds through a dismissal, and re-arms on new activity", () => {
    const digest = decodeJobDigest(ENVELOPE);
    expect(digest).not.toBeNull();
    const jobId = digest!.job_id;

    const port = browserDigestVisibilityPort(fakeStorage());
    port.writeLastSeen(jobId, T_AWAY);

    // Reopen: the job finished while away, and it is SETTLED (`paused`), so
    // it shows on those grounds regardless of the last-seen instant.
    const onReopen = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_FINISH,
      nowMs: T_REOPEN,
    });
    expect(onReopen).toEqual({ show: true, reason: "settled" });

    // The CTA equals the report's own recommendation with the report's
    // Markdown removed and nothing else changed (DECISION F040 D10).
    expect(digestCtaText(digest!.primary_action.label)).toBe(
      "Answer the open decision",
    );

    // Dismiss at the reopen instant.
    port.writeDismissal(jobId, T_REOPEN);
    port.writeLastSeen(jobId, T_REOPEN);

    // No re-show: no activity has happened since the dismissal.
    const afterDismissal = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_FINISH,
      nowMs: T_REOPEN + 60_000,
    });
    expect(afterDismissal).toEqual({ show: false, reason: "dismissed" });

    // The exact dismissal instant itself does not re-arm the card either —
    // the Acceptance's "persists" half of "Dismissal persists; new activity
    // re-arms".
    const atTheBoundary = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_REOPEN,
      nowMs: T_REOPEN + 60_000,
    });
    expect(atTheBoundary).toEqual({ show: false, reason: "dismissed" });

    // New activity strictly after the dismissal re-arms it — the
    // Acceptance's "re-arms" half.
    const T_NEW_ACTIVITY = T_REOPEN + 120_000;
    const reArmed = digestVisibility({
      digest,
      lastSeenMs: port.readLastSeen(jobId),
      dismissedAtMs: port.readDismissal(jobId),
      latestActivityMs: T_NEW_ACTIVITY,
      nowMs: T_NEW_ACTIVITY + 1,
    });
    expect(reArmed).toEqual({ show: true, reason: "settled" });
  });
});
