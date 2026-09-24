// This module owns WHEN a node appears — the stagger and order a birth
// animates in — and nothing about HOW it is painted (scale-in spring, edge
// draw-in, the glow pulse): that stays the renderer's job (graph_spec §11-
// §12; motion_spec.md "node birth"; DECISION F019 D1). Pure and total: no
// DOM, no random draws, no Date — scheduleBrainBirths is a function of its
// two layouts and a boolean.
import type { BrainLayoutData } from "./forceBrainTypes";

/** Birth spring duration, `--remedy-dur-birth` (graph_spec §12; tests/
 *  ui_contracts/test_brain_motion_tokens.py pins this against the token). */
export const BRAIN_BIRTH_MS = 420;
/** Birth duration under reduced motion — a plain fade, no spring (graph_spec
 *  §12: "Reduced motion: births = 180ms fade"). */
export const BRAIN_BIRTH_REDUCED_MS = 180;
/** Gap between the start of consecutive births in the same wave (graph_spec
 *  §11: "max 3 concurrent staggered 90ms"). */
export const BRAIN_BIRTH_STAGGER_MS = 90;
/** How many births may be in flight at once before the next one waits for an
 *  earlier one to finish (graph_spec §11, the "calm rule"). */
export const BRAIN_BIRTH_MAX_CONCURRENT = 3;

/** One node's entrance: when it starts, how long it takes, and whether it is
 *  a plain fade (reduced motion) instead of the spring scale-in. */
export interface BrainBirth {
  id: string;
  delayMs: number;
  durationMs: number;
  fade: boolean;
}

/** The births between two layouts, in the order they should animate
 *  (graph_spec §11: "births animate in data order"). A first paint
 *  (`previous === null`) renders at rest — no births — so a fresh screenshot
 *  is stable; a node present in both layouts is never re-born; a node that
 *  disappeared births nothing. Birth i's delay is the LATER of its own
 *  stagger slot and the moment the birth `BRAIN_BIRTH_MAX_CONCURRENT` before
 *  it finishes, which is what keeps at most that many animating at once. */
export function scheduleBrainBirths(
  previous: BrainLayoutData | null,
  next: BrainLayoutData,
  reducedMotion: boolean,
): BrainBirth[] {
  if (previous === null) return [];
  const previousIds = new Set(previous.nodes.map((n) => n.id));
  const born = next.nodes.filter((n) => !previousIds.has(n.id));
  const durationMs = reducedMotion ? BRAIN_BIRTH_REDUCED_MS : BRAIN_BIRTH_MS;

  const delays: number[] = [];
  born.forEach((_, i) => {
    const staggerSlot = i * BRAIN_BIRTH_STAGGER_MS;
    const concurrencyFloor = i >= BRAIN_BIRTH_MAX_CONCURRENT
      ? delays[i - BRAIN_BIRTH_MAX_CONCURRENT] + durationMs
      : 0;
    delays.push(Math.max(staggerSlot, concurrencyFloor));
  });

  return born.map((n, i) => ({
    id: n.id, delayMs: delays[i], durationMs, fade: reducedMotion,
  }));
}
