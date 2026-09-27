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

/** DECISION F028 D7 (3) — the word the CANVAS chip carries for an injected
 *  task, short because the chip itself is small (graph_spec §4's synapse-
 *  scale text). `buildForceBrainModel.ts`'s `taskChipOf` reads it, never the
 *  list/popover's own `ORIGIN_CHIP_TEXT` above — the two surfaces are sized
 *  for different amounts of text and are never assumed to agree. */
export const ORIGIN_CANVAS_CHIP_TEXT = "added";

// A reader looking here for a colour, a mark or a state is looking for
// something this module deliberately does not have: provenance is not a
// state (DECISION F028 D6's ALTERNATIVES), so this file answers words for a
// pill, never a `RemedyState` and never a token.

// ---------------------------------------------------------------------------
// DECISION F028 D7 (2) — THE DRAFT VIEW: the one PURE function that turns a
// sent command's 200 body into every sentence and list `AddTaskSheet.tsx`
// shows, built exactly as `taskOriginChip` above is built and for the same
// reason: the shipped vitest config collects `src/**/*.test.ts` only and no
// DOM harness exists, so a rule written inside the sheet itself would ship
// untested. It reads the wire body `packages/orchestration/task_injection.py`
// answers DEFENSIVELY: every field is read by its own type, never assumed,
// so a missing or mistyped one answers the empty string or the empty list
// rather than throwing — the sheet must never crash on an odd body.
// ---------------------------------------------------------------------------

/** One option a shortfall's decision seed offers, in the seed's own order. */
export interface InjectDraftOption {
  option: string;
  label: string;
}

/** `injectDraftView`'s own answer: everything `AddTaskSheet.tsx` reads to
 *  show a draft or a shortfall, and nothing it has to compute itself. */
export interface InjectDraftView {
  kind: "drafted" | "shortfall";
  draftId: string;
  /** `null` for a shortfall (DECISION F028 D3 (1) — a shortfall draft is not
   *  yet confirmable); the defensive empty string for a `drafted` body whose
   *  own `confirm_token` is missing or mistyped. */
  confirmToken: string | null;
  title: string;
  goal: string;
  acceptance: string[];
  size: string;
  placement: string;
  cost: string;
  fenceWarnings: string[];
  expiresAt: string;
  question: string;
  options: InjectDraftOption[];
}

function readString(value: unknown): string {
  return typeof value === "string" ? value : "";
}

function readStringList(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((entry): entry is string => typeof entry === "string") : [];
}

function readRecord(value: unknown): Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

/** The first letter upper-cased and a full stop added — `place_injected_task`'s
 *  own rationale strings carry neither. The empty string stays empty: a
 *  sentence with nothing in it is not a sentence with a stray period. */
function sentenceOf(raw: string): string {
  if (raw === "") return "";
  const capitalized = raw.slice(0, 1).toUpperCase() + raw.slice(1);
  return capitalized.endsWith(".") ? capitalized : `${capitalized}.`;
}

/** THE DRAFT VIEW (DECISION F028 D7 (2)): `null` unless `answer.outcome` is
 *  `drafted` or `shortfall` — a `confirmed`, a `dropped` body and every
 *  refusal all answer `null`, which `AddTaskSheet.tsx` reads as "nothing to
 *  review", showing the send's own sentence instead. */
export function injectDraftView(answer: Record<string, unknown> | null): InjectDraftView | null {
  if (answer === null) {
    return null;
  }
  const outcome = answer.outcome;
  if (outcome !== "drafted" && outcome !== "shortfall") {
    return null;
  }
  const kind = outcome;
  const task = readRecord(answer.task);
  const placement = readRecord(answer.placement);
  const budgetCheck = readRecord(answer.budget_check);
  const decisionSeed = kind === "shortfall" ? readRecord(answer.decision_seed) : {};
  const band = readString(task.est_tokens_band);
  const arithmetic = readString(budgetCheck.arithmetic);
  const optionLabels = readRecord(decisionSeed.option_labels);
  const options = readStringList(decisionSeed.options).map((option) => ({
    option,
    label: readString(optionLabels[option]),
  }));
  const fenceConflicts = Array.isArray(answer.fence_conflicts) ? answer.fence_conflicts : [];
  const fenceWarnings = fenceConflicts
    .map((entry) => readString(readRecord(entry).path))
    .filter((path) => path !== "")
    .map((path) => `${path} is outside what this job may change.`);

  return {
    kind,
    draftId: readString(answer.draft_id),
    confirmToken: kind === "shortfall" ? null : readString(answer.confirm_token),
    title: readString(task.title),
    goal: readString(task.goal),
    acceptance: readStringList(task.acceptance),
    size: band === "" ? "" : `Size: ${band}.`,
    placement: sentenceOf(readString(placement.rationale)),
    cost: arithmetic === "" ? "" : `Cost check: ${arithmetic}.`,
    fenceWarnings,
    expiresAt: readString(answer.expires_at),
    question: kind === "shortfall" ? readString(decisionSeed.question) : "",
    options: kind === "shortfall" ? options : [],
  };
}
