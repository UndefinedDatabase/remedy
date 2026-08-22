import { describe, it, expect } from "vitest";
import {
  BRAIN_BACKOFF_CAP_MS, BRAIN_RECENT_LIMIT, brainBackoffDelayMs, degradeBrainStream,
  failBrainStream, initialBrainStreamState, openBrainStream, receiveBrainFrame,
  repairBrainGap, resumeEventId,
} from "./brainStream";
import type { BrainStreamState } from "./brainStream";

/** Drive a state through a run of seqs, as the transport would deliver them. */
function drive(state: BrainStreamState, seqs: number[]): BrainStreamState {
  return seqs.reduce((s, seq) => receiveBrainFrame(s, { seq, event: { seq } }, seq * 10), state);
}

describe("initialBrainStreamState", () => {
  it("holds nothing and does not claim to be live", () => {
    const s = initialBrainStreamState();
    expect(s.lastSeq).toBeNull();
    expect(s.status).toBe("reconnecting");
    expect(s.gapDetected).toBe(false);
  });
});

describe("resumeEventId", () => {
  it("sends no header before the first frame", () => {
    expect(resumeEventId(initialBrainStreamState())).toBeNull();
  });
  it("sends the last seq HELD, not the next one wanted", () => {
    // The server adds the one, so a next-wanted seq would skip an event.
    expect(resumeEventId(drive(initialBrainStreamState(), [0, 1, 2]))).toBe("2");
  });
  it("zero is a position and is still sent", () => {
    // The client half of the server-side rule that zero is not an absence.
    expect(resumeEventId(drive(initialBrainStreamState(), [0]))).toBe("0");
  });
});

describe("receiveBrainFrame", () => {
  it("a contiguous run reports no gap and ends live", () => {
    const s = drive(openBrainStream(initialBrainStreamState()), [0, 1, 2, 3]);
    expect(s.lastSeq).toBe(3);
    expect(s.gapDetected).toBe(false);
    expect(s.status).toBe("live");
  });
  it("the first frame of a fresh client is never a gap", () => {
    // A resume from a cursor starts mid-ledger; that is not a discontinuity.
    expect(drive(initialBrainStreamState(), [7]).gapDetected).toBe(false);
  });
  it("a hole in the sequence is detected", () => {
    expect(drive(initialBrainStreamState(), [0, 1, 4]).gapDetected).toBe(true);
  });
  it("a replayed frame is dropped and does not move the held position", () => {
    const s = drive(initialBrainStreamState(), [0, 1, 1]);
    expect(s.lastSeq).toBe(1);
    expect(s.gapDetected).toBe(false);
  });
  it("a detected gap stays set while later frames arrive cleanly", () => {
    expect(drive(initialBrainStreamState(), [0, 3, 4, 5]).gapDetected).toBe(true);
  });
  it("frames over the fallback stay labelled delayed", () => {
    const s = drive(degradeBrainStream(initialBrainStreamState()), [0, 1]);
    expect(s.status).toBe("delayed");
    expect(s.lastSeq).toBe(1);
  });
});

describe("repairBrainGap", () => {
  it("a snapshot clears the discontinuity and sets the held position", () => {
    const fixed = repairBrainGap(drive(initialBrainStreamState(), [0, 4]), 9);
    expect(fixed.gapDetected).toBe(false);
    expect(fixed.lastSeq).toBe(9);
    expect(resumeEventId(fixed)).toBe("9");
  });
});

describe("the status surface", () => {
  it("moves through live, reconnecting and delayed and back to live", () => {
    let s = openBrainStream(initialBrainStreamState());
    expect(s.status).toBe("live");
    s = failBrainStream(s);
    expect(s.status).toBe("reconnecting");
    s = degradeBrainStream(s);
    expect(s.status).toBe("delayed");
    s = openBrainStream(s);
    expect(s.status).toBe("live");
  });
  it("a successful open resets the attempt count", () => {
    const s = openBrainStream(failBrainStream(failBrainStream(initialBrainStreamState())));
    expect(s.attempt).toBe(0);
  });
  it("each drop counts one attempt", () => {
    expect(failBrainStream(failBrainStream(initialBrainStreamState())).attempt).toBe(2);
  });
});

describe("brainBackoffDelayMs", () => {
  it("the first attempt does not wait", () => {
    expect(brainBackoffDelayMs(0)).toBe(0);
  });
  it("doubles from the base delay", () => {
    expect([1, 2, 3, 4].map((n) => brainBackoffDelayMs(n))).toEqual([250, 500, 1000, 2000]);
  });
  it("is capped so a long outage keeps retrying", () => {
    // The LITERAL is the gate. Asserting only against the imported constant
    // tracks any change to it and therefore pins nothing — the cap could be
    // raised to a minute and this test would stay green (finding R-0623).
    expect(BRAIN_BACKOFF_CAP_MS).toBe(8000);
    expect(brainBackoffDelayMs(20)).toBe(8000);
  });
  it("never decreases as attempts grow", () => {
    const d = [0, 1, 2, 3, 4, 5, 6, 7, 8].map((n) => brainBackoffDelayMs(n));
    expect(d).toEqual([...d].sort((a, b) => a - b));
  });
});

describe("the recent ring", () => {
  it("a fresh client holds no rows and has dropped none", () => {
    const s = initialBrainStreamState();
    expect(s.recent).toEqual([]);
    expect(s.recentDropped).toBe(0);
  });

  it("each accepted frame appends one projected row, oldest first", () => {
    const s = drive(initialBrainStreamState(), [4, 5, 6]);
    expect(s.recent.map((r) => r.seq)).toEqual([4, 5, 6]);
    expect(s.recentDropped).toBe(0);
  });

  it("a replayed frame appends nothing and returns the identical state", () => {
    const s = drive(initialBrainStreamState(), [1, 2]);
    const again = receiveBrainFrame(s, { seq: 2, event: { seq: 2 } }, 999);
    expect(again).toBe(s);
    expect(again.recent).toBe(s.recent);
    expect(again.recent.map((r) => r.seq)).toEqual([1, 2]);
  });

  it("the ring never grows past BRAIN_RECENT_LIMIT, dropping the OLDEST", () => {
    const seqs = Array.from({ length: BRAIN_RECENT_LIMIT + 5 }, (_, i) => i + 1);
    const s = drive(initialBrainStreamState(), seqs);
    expect(s.recent.length).toBe(BRAIN_RECENT_LIMIT);
    expect(s.recentDropped).toBe(5);
    expect(s.recent[0].seq).toBe(6);
    expect(s.recent[s.recent.length - 1].seq).toBe(BRAIN_RECENT_LIMIT + 5);
  });

  it("the row carries the humanized projection, not the raw envelope", () => {
    const s = receiveBrainFrame(initialBrainStreamState(), {
      seq: 3, event: { event: "task_run_started", outcome: "ok" },
    }, 1234);
    expect(s.recent[0].kind).toBe("task_run_started");
    expect(s.recent[0].known).toBe(true);
    expect(s.recent[0].outcome).toBe("ok");
  });

  it("the row carries the arrival stamp the transport handed in", () => {
    const s = receiveBrainFrame(initialBrainStreamState(), {
      seq: 3, event: { event: "task_run_started" },
    }, 1234);
    expect(s.recent[0].receivedAtMs).toBe(1234);
  });

  it("each row keeps its OWN stamp as the ring fills", () => {
    const s = drive(initialBrainStreamState(), [1, 2, 3]);
    expect(s.recent.map((r) => r.receivedAtMs)).toEqual([10, 20, 30]);
  });
});
