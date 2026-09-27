// THE ATTEMPT VIEW (DECISION F029 D5): pure functions of a task item that
// decide what the graph's chip and the popover's Attempts list show. Nothing
// here reaches a fetch, a clock or a DOM — every answer is a function of the
// item alone, exactly as `taskSpecView.ts` reads a task's spec and version
// chain and for the same reason: the shipped vitest config collects
// `src/**/*.test.ts` only and no DOM harness exists, so a rule written
// inside a component or the graph builder would ship untested.

/** DECISION F029 D5 (1) — the CANVAS chip's own fragment for a task on its
 *  second or later attempt: short, because the chip itself is small
 *  (graph_spec §4's synapse-scale text), exactly the size
 *  `ORIGIN_CANVAS_CHIP_TEXT` in `injectView.ts` is built for. `taskChipOf` in
 *  `buildForceBrainModel.ts` is the one caller, joining this after `v<n>`
 *  and "added" when they apply. */
export function attemptChipText(n: number): string {
  return `attempt ${n}`;
}
