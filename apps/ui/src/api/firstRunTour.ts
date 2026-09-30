// The first-run tour's content and its one stored fact (T5_F043 T003, DECISION F043 D4): six
// steps over the shell's own regions, and the once-per-browser record that keeps it from
// returning once it has been seen.

/** One step of the first-run tour: a title, a body and the region it points at, by `data-ui`. */
export interface FirstRunStep {
  readonly title: string;
  readonly body: string;
  readonly target: string;
}

// The sixth step stands in for the command palette until one exists (DECISION F043 D1 (5));
// it points at the Terms button instead, which is also where the tour can be started again.
export const FIRST_RUN_STEPS: readonly FirstRunStep[] = [
  {
    title: "The graph",
    body: "Every task of this job is a dot joined to the job at the centre. A dot changes colour as its task is planned, runs, and passes or fails. Choose one to see what it did.",
    target: "brain-graph-stage",
  },
  {
    title: "The timeline",
    body: "The job's phases, from its first event to the end. Drag along it to see the job as it stood earlier; LIVE brings you back.",
    target: "phase-timeline",
  },
  {
    title: "What is happening now",
    body: "The newest real action of the job's agents, and below it every event in plain words.",
    target: "right-live-panel",
  },
  {
    title: "Decisions",
    body: "Questions Remedy cannot answer for itself wait here for you, the most urgent first.",
    target: "decision-inbox-card",
  },
  {
    title: "A note for the job",
    body: "Write a note here and the builder reads it at its next round.",
    target: "chat-input-row",
  },
  {
    title: "Every word explained",
    body: "Hover an underlined word to see what it means, or press ? for the list of every term. You can start this tour again from there.",
    target: "terms-button",
  },
];

/** Where the once-per-browser record lives. */
export const FIRST_RUN_TOUR_KEY = "remedy:first-run-tour";

/** The one value the key ever holds: the tour was seen. */
export const FIRST_RUN_TOUR_SEEN = "seen";

/** The storage this module needs, and nothing more. */
export type FirstRunTourStorage = Pick<Storage, "getItem" | "setItem">;

/** Whether the tour should open on its own: `false` without a storage, `true` only when the
 *  storage holds no record of it yet, `false` when the storage throws. */
export function firstRunTourDue(storage: FirstRunTourStorage | null): boolean {
  if (storage === null) return false;
  try {
    return storage.getItem(FIRST_RUN_TOUR_KEY) === null;
  } catch {
    return false;
  }
}

/** Records the tour as seen; does nothing without a storage, and swallows a throw. */
export function markFirstRunTourSeen(storage: FirstRunTourStorage | null): void {
  if (storage === null) return;
  try {
    storage.setItem(FIRST_RUN_TOUR_KEY, FIRST_RUN_TOUR_SEEN);
  } catch {
    // The storage is unavailable; there is nothing to record.
  }
}

/** The step label the tour's card shows, one-based. */
export function firstRunStepLabel(count: number, current: number): string {
  return `Step ${current + 1} of ${count}`;
}
