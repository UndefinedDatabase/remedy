// DECISION F028 D6 (2) — AN INJECTED TASK'S CHIP, as ONE pure function over the
// task item S1 above already carries. It is built exactly as `taskSpecView.ts`'s
// `versionChipLabel` is built, and for the same reason: the shipped vitest
// config collects `src/**/*.test.ts` only and no DOM harness exists, so a rule
// written inside a component would ship untested.
//
// THE WORDS, NOT THE RAW VALUE. `ux_spec.md` §17 forbids raw ids and metadata
// in the default view, so this module never hands a component the string
// `human_injected` itself — only the words a chip may show, or `null` for a
// task the operator did not add.

/** The one origin value the dashboard's task item carries that this chip
 *  answers for — `task_injection.ORIGIN_HUMAN_INJECTED` on the server,
 *  mirrored here rather than renamed on the way out, the same rule
 *  `vetoSend.ts`'s `JOB_VETO_TASK_COMMAND_ID` follows. */
export const INJECTED_TASK_ORIGIN = "human_injected";

/** The words a task-list row and the detail popover both show for an
 *  injected task's pill. */
export const ORIGIN_CHIP_TEXT = "Added by you";

/** The pill's title attribute — the one sentence an operator reads on hover,
 *  identical in both mounts so the chip means the same thing everywhere it
 *  appears. */
export const ORIGIN_CHIP_TITLE = "You added this task while the job was running.";

/** THE CHIP: `ORIGIN_CHIP_TEXT` for a task whose `origin` is exactly
 *  `INJECTED_TASK_ORIGIN`, `null` otherwise — including for a missing task, a
 *  missing `origin` and any other origin value this browser does not yet
 *  name a chip for. Total over `null | undefined` so a caller need not guard
 *  before it calls. */
export function taskOriginChip(task: { origin?: string } | null | undefined): string | null {
  return task?.origin === INJECTED_TASK_ORIGIN ? ORIGIN_CHIP_TEXT : null;
}

// A reader looking here for a colour, a mark or a state is looking for
// something this module deliberately does not have: provenance is not a
// state (DECISION F028 D6's ALTERNATIVES), so this file answers words for a
// pill, never a `RemedyState` and never a token.
