import { describe, it, expect } from "vitest";
import type { JobDigest } from "./jobDigest";
import type { DigestVisibilityInput, DigestVisibilityReason } from "./digestVisibility";
import { digestVisibility } from "./digestVisibility";

const T0 = 1_700_000_000_000;

/** A complete envelope in one state. The trigger reads only `state`, but the
 *  whole shape is built so the fixture cannot drift from `JobDigest` without the
 *  type checker saying so. */
function digestInState(state: string): JobDigest {
  return {
    version: 1,
    job_id: "job-1",
    state,
    headline: "",
    cost: { value: "", basis: "" },
    ownership: [],
    decisions: { open_count: 0, peak_urgency: 0 },
    primary_action: { label: "", rule_id: "" },
  };
}

/** The quiet baseline: a settled run, never dismissed, nothing has happened.
 *  Each case below overrides exactly the instants it is about, so what a case
 *  changes is what it tests. */
function input(over: Partial<DigestVisibilityInput> = {}): DigestVisibilityInput {
  return {
    digest: digestInState("completed"),
    lastSeenMs: T0,
    dismissedAtMs: null,
    latestActivityMs: null,
    nowMs: T0,
    ...over,
  };
}

/** All seven `RunState` values from `packages/core/models.py`, written as a
 *  TABLE so a state added to that enum has an obvious place to land here. The
 *  instants are the quiet baseline — no activity at all — so this table grades
 *  the SETTLED partition and nothing else.
 *
 *  The three-way partition is the whole point: `pending` and `planned` are
 *  not-yet-started and must not show, `running` is in flight and does not show
 *  on settled grounds, and the remaining four do show. A rule written TWO-WAY —
 *  "terminal means not running" — passes every other case in this file and fails
 *  exactly the first two rows. */
const STATE_TABLE: readonly {
  state: string;
  shows: boolean;
  reason: DigestVisibilityReason;
}[] = [
  { state: "pending", shows: false, reason: "not-yet-started" },
  { state: "planned", shows: false, reason: "not-yet-started" },
  { state: "running", shows: false, reason: "nothing-new" },
  { state: "paused", shows: true, reason: "settled" },
  { state: "completed", shows: true, reason: "settled" },
  { state: "failed", shows: true, reason: "settled" },
  { state: "cancelled", shows: true, reason: "settled" },
];

describe("digestVisibility over the run states", () => {
  for (const row of STATE_TABLE) {
    it(`answers ${row.shows ? "show" : "no show"} (${row.reason}) for ${row.state}`, () => {
      expect(digestVisibility(input({ digest: digestInState(row.state) }))).toEqual({
        show: row.shows,
        reason: row.reason,
      });
    });
  }

  it("covers all seven states of RunState in the table", () => {
    expect(STATE_TABLE.map(row => row.state)).toEqual([
      "pending",
      "planned",
      "running",
      "paused",
      "completed",
      "failed",
      "cancelled",
    ]);
  });

  it("does not show on settled grounds for a state it has never heard of", () => {
    // Claiming a run finished on the strength of a word this client cannot read
    // is the false claim the feature refuses everywhere else.
    expect(digestVisibility(input({ digest: digestInState("quantum-tunnelling") }))).toEqual({
      show: false,
      reason: "nothing-new",
    });
  });

  it("still shows an unknown state on absence grounds when there is real activity", () => {
    expect(
      digestVisibility(
        input({
          digest: digestInState("quantum-tunnelling"),
          latestActivityMs: T0 + 1,
        }),
      ),
    ).toEqual({ show: true, reason: "activity-since-last-seen" });
  });

  it("shows a running job on absence grounds even though it is not settled", () => {
    expect(
      digestVisibility(input({ digest: digestInState("running"), latestActivityMs: T0 + 1 })),
    ).toEqual({ show: true, reason: "activity-since-last-seen" });
  });

  it("never shows a pending job, not even with activity since last-seen", () => {
    expect(
      digestVisibility(input({ digest: digestInState("pending"), latestActivityMs: T0 + 1 })),
    ).toEqual({ show: false, reason: "not-yet-started" });
  });

  it("never shows a planned job, not even with activity since last-seen", () => {
    expect(
      digestVisibility(input({ digest: digestInState("planned"), latestActivityMs: T0 + 1 })),
    ).toEqual({ show: false, reason: "not-yet-started" });
  });
});

describe("digestVisibility and a dismissal", () => {
  it("holds a dismissal when nothing at all has happened since", () => {
    expect(digestVisibility(input({ dismissedAtMs: T0 }))).toEqual({
      show: false,
      reason: "dismissed",
    });
  });

  it("holds a dismissal when the newest activity is older than it", () => {
    expect(
      digestVisibility(input({ dismissedAtMs: T0, latestActivityMs: T0 - 1 })),
    ).toEqual({ show: false, reason: "dismissed" });
  });

  it("holds a dismissal when the activity is EXACTLY the dismissal instant", () => {
    // Not newer, so it is activity the operator was already looking at when the
    // card was dismissed. This boundary is the difference between "persists"
    // and "re-arms on the same event".
    expect(
      digestVisibility(input({ dismissedAtMs: T0, latestActivityMs: T0 })),
    ).toEqual({ show: false, reason: "dismissed" });
  });

  it("re-arms on activity strictly after the dismissal", () => {
    expect(
      digestVisibility(input({ dismissedAtMs: T0, latestActivityMs: T0 + 1 })),
    ).toEqual({ show: true, reason: "settled" });
  });

  it("re-arms into the absence answer for a job that is not settled", () => {
    expect(
      digestVisibility(
        input({
          digest: digestInState("running"),
          dismissedAtMs: T0,
          latestActivityMs: T0 + 1,
          lastSeenMs: T0,
        }),
      ),
    ).toEqual({ show: true, reason: "activity-since-last-seen" });
  });

  it("holds a dismissal over a not-yet-started job as well", () => {
    expect(
      digestVisibility(input({ digest: digestInState("pending"), dismissedAtMs: T0 })),
    ).toEqual({ show: false, reason: "dismissed" });
  });
});

describe("digestVisibility and the absence rule", () => {
  it("shows when the activity is strictly after last-seen", () => {
    expect(
      digestVisibility(
        input({ digest: digestInState("running"), lastSeenMs: T0, latestActivityMs: T0 + 1 }),
      ),
    ).toEqual({ show: true, reason: "activity-since-last-seen" });
  });

  it("does not show when the activity is EXACTLY last-seen", () => {
    expect(
      digestVisibility(
        input({ digest: digestInState("running"), lastSeenMs: T0, latestActivityMs: T0 }),
      ),
    ).toEqual({ show: false, reason: "nothing-new" });
  });

  it("does not show when the activity is older than last-seen", () => {
    expect(
      digestVisibility(
        input({ digest: digestInState("running"), lastSeenMs: T0, latestActivityMs: T0 - 1 }),
      ),
    ).toEqual({ show: false, reason: "nothing-new" });
  });

  it("shows on any activity when last-seen is null, which means never seen", () => {
    expect(
      digestVisibility(
        input({ digest: digestInState("running"), lastSeenMs: null, latestActivityMs: 0 }),
      ),
    ).toEqual({ show: true, reason: "activity-since-last-seen" });
  });

  it("does not show when last-seen is null and nothing has happened either", () => {
    expect(
      digestVisibility(
        input({ digest: digestInState("running"), lastSeenMs: null, latestActivityMs: null }),
      ),
    ).toEqual({ show: false, reason: "nothing-new" });
  });

  it("answers nothing-new as the default rather than as an inferred fallback", () => {
    expect(digestVisibility(input({ digest: digestInState("running") }))).toEqual({
      show: false,
      reason: "nothing-new",
    });
  });
});

describe("digestVisibility with no digest and with a skewed clock", () => {
  it("never shows a null digest, whatever the instants say", () => {
    expect(
      digestVisibility(
        input({ digest: null, lastSeenMs: null, latestActivityMs: T0 + 60_000 }),
      ),
    ).toEqual({ show: false, reason: "no-digest" });
  });

  it("never shows a null digest even when a dismissal is in force", () => {
    expect(digestVisibility(input({ digest: null, dismissedAtMs: T0 }))).toEqual({
      show: false,
      reason: "no-digest",
    });
  });

  it("still counts activity stamped in the future as activity", () => {
    // The stamp is an hour ahead of `nowMs`. No branch compares anything with
    // `nowMs`, so skew cannot hide the news: over-reporting costs a click,
    // under-reporting costs the report.
    expect(
      digestVisibility(
        input({
          digest: digestInState("running"),
          lastSeenMs: T0,
          latestActivityMs: T0 + 3_600_000,
          nowMs: T0,
        }),
      ),
    ).toEqual({ show: true, reason: "activity-since-last-seen" });
  });

  it("re-arms a dismissal on a future stamp too", () => {
    expect(
      digestVisibility(
        input({ dismissedAtMs: T0, latestActivityMs: T0 + 3_600_000, nowMs: T0 }),
      ),
    ).toEqual({ show: true, reason: "settled" });
  });

  it("answers the same for any nowMs, because no branch reads it", () => {
    const base = input({ digest: digestInState("running"), latestActivityMs: T0 + 1 });
    const early = digestVisibility({ ...base, nowMs: 0 });
    const late = digestVisibility({ ...base, nowMs: T0 + 10_000_000 });
    expect(early).toEqual(late);
    expect(early).toEqual({ show: true, reason: "activity-since-last-seen" });
  });
});
