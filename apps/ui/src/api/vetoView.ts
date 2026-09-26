// THE VETO'S VIEW (DECISION F027 D8): everything the page reads off the
// dashboard's own `vetoes` section, as PURE functions — no `fetch(`, no DOM, no
// clock. The canvas's hover text, the popover's Veto and Unreachable sections,
// and the "Veto task" form's own eligibility all read this module rather than
// re-deriving a rule against `RemedyVetoes` or `RemedyVetoEntry` a second time.
//
// THE TWO READING DIRECTIONS. `taskVetoEntry` answers the ONE entry a vetoed
// task owns; `vetoingEntriesOf` answers every entry that named a task as
// unreachable, which may be more than one when two vetoes both cut the same
// downstream task off. Both read `vetoes.tasks` in the section's own order —
// plan order, `RemedyVetoes`' own comment says — so a caller that lists
// several titles lists them in that same order, never re-sorted.
//
// A VETOED TASK'S HOVER TEXT WINS. A task can never be both vetoed and
// unreachable at once (the backend's own gate refuses a second veto of an
// already-vetoed task), but `vetoHoverText` still checks vetoed first, because
// that is the more specific fact when both could somehow be read.
import type { RemedyDashboard, RemedyVetoEntry, RemedyVetoes } from "./types";

/** The one veto entry recorded against `taskId`, or `null` when that task was
 *  never vetoed. */
export function taskVetoEntry(vetoes: RemedyVetoes, taskId: string): RemedyVetoEntry | null {
  return vetoes.tasks.find((entry) => entry.taskId === taskId) ?? null;
}

/** Every entry whose OWN unreachable set names `taskId` — the veto or vetoes
 *  that made this task unreachable — in the section's own order. */
export function vetoingEntriesOf(vetoes: RemedyVetoes, taskId: string): RemedyVetoEntry[] {
  return vetoes.tasks.filter((entry) => entry.unreachableTaskIds.includes(taskId));
}

/** A task's own display title, read from `dashboard.tasks`, or the bare id
 *  itself when this dashboard never named that task — the same fallback
 *  `selectionTaskIdOf`'s callers already accept for an id this page has never
 *  seen. */
export function taskTitleOf(dashboard: RemedyDashboard, taskId: string): string {
  return dashboard.tasks.find((t) => t.id === taskId)?.label ?? taskId;
}

/** Everything the "Veto task" form needs to know it may open: just the task id
 *  it acts on — `taskEditAction`'s own shape, named for the same reason: a
 *  form mounted from this action never re-derives eligibility itself. */
export interface TaskVetoAction {
  taskId: string;
}

/** `null` when the section's own read failed (`error` is not `""`) or this
 *  task is not in `vetoableTaskIds` — a task already vetoed, one the job's
 *  current state no longer allows a veto against, or one this section never
 *  named at all. */
export function taskVetoAction(dashboard: RemedyDashboard, taskId: string): TaskVetoAction | null {
  const vetoes = dashboard.vetoes;
  if (vetoes.error !== "" || !vetoes.vetoableTaskIds.includes(taskId)) {
    return null;
  }
  return { taskId };
}

/** The live canvas's own hover text for one task node, or `null` for a task
 *  that is neither vetoed nor unreachable — every other node, as today. A
 *  vetoed task's reason rides VERBATIM, exactly as `record_task_veto` stored
 *  it; an unreachable task names every vetoing task's TITLE, joined by
 *  `", "`, in the section's own order. */
export function vetoHoverText(dashboard: RemedyDashboard, taskId: string): string | null {
  const vetoed = taskVetoEntry(dashboard.vetoes, taskId);
  if (vetoed) {
    return `Vetoed: ${vetoed.reason}`;
  }
  const vetoing = vetoingEntriesOf(dashboard.vetoes, taskId);
  if (vetoing.length > 0) {
    const titles = vetoing.map((entry) => taskTitleOf(dashboard, entry.taskId));
    return `Unreachable due to veto of ${titles.join(", ")}`;
  }
  return null;
}

const REPLAN_WAITING_SENTENCE = "A replan proposal is waiting in the decision inbox.";
const REPLAN_FOLLOW_UP_SENTENCE = "Answered: replan the remaining work as a new job.";
const ACCEPT_REDUCED_SCOPE_SENTENCE = "Answered: accept the smaller scope.";
const ANSWERED_SENTENCE = "Answered.";

/** THE VETO ENTRY'S OWN `answer` FIELD, worded: `""` means the replan
 *  proposal this veto filed is still sitting in the decision inbox unanswered;
 *  the two options `veto_proposal.py`'s own `task_veto.REPLAN_PROPOSAL_OPTIONS`
 *  offers each get their own sentence; any other value — an answer this page does not name one by
 *  one — still reads as answered, honestly, rather than as the empty case. */
export function vetoAnswerSentence(answer: string): string {
  if (answer === "") {
    return REPLAN_WAITING_SENTENCE;
  }
  if (answer === "replan_follow_up") {
    return REPLAN_FOLLOW_UP_SENTENCE;
  }
  if (answer === "accept_reduced_scope") {
    return ACCEPT_REDUCED_SCOPE_SENTENCE;
  }
  return ANSWERED_SENTENCE;
}
