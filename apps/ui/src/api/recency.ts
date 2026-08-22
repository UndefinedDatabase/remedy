// How fresh the newest ACTION is, as a PURE function of two numbers. T5_F021
// gives the NowCard an activity dot that pulses on recency and fades to idle
// after a quiet window; Remedy deliberately keeps the RULE separate from the
// clock, so the fade is testable without waiting and without faking time. The
// caller passes `nowMs`; this module never reads a clock itself.

/** Inside this many ms of the newest action the dot pulses: the agent is
 *  visibly doing something right now. */
export const FRESH_WINDOW_MS = 5000;

/** After this many ms of quiet the dot is idle. Between the two windows it
 *  fades, which is the motion the design reference asks for. */
export const QUIET_WINDOW_MS = 30000;

/** What the dot shows. `none` is the pre-stream state, before any action has
 *  arrived at all, and is NOT the same as `idle`, which means the agent acted
 *  and then went quiet. */
export type RecencyLevel = "none" | "fresh" | "fading" | "idle";

/** The dot's level for a newest action stamped `lastActionAtMs`, seen at
 *  `nowMs`. A null stamp means nothing has acted yet. */
export function recencyLevel(lastActionAtMs: number | null, nowMs: number): RecencyLevel {
  if (lastActionAtMs === null) {
    return "none";
  }
  const elapsed = nowMs - lastActionAtMs;
  // A stamp in the future means the clocks disagree, not that the agent is
  // idle. Remedy reports fresh rather than idle here on purpose: under skew the
  // honest failure is to over-report life, never to declare a working agent dead.
  if (elapsed < FRESH_WINDOW_MS) {
    return "fresh";
  }
  if (elapsed < QUIET_WINDOW_MS) {
    return "fading";
  }
  return "idle";
}

/** Whether the card may call itself live. This is the single source R21 gives
 *  BOTH the badge and the dot, so the two can never disagree -- the defect
 *  R-0652 recorded was exactly a badge with a liveness rule of its own. */
export function isLiveByRecency(level: RecencyLevel): boolean {
  return level === "fresh" || level === "fading";
}
