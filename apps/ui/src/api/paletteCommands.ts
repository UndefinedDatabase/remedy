// T5_F044 T001, DECISION F044 D1 — the palette's command list: one entry per command of
// `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py`, the write door's exposed set, less the
// two continuation steps that only continue the add-task sheet's conversation, which that sheet
// already owns. `tests/ui_contracts/test_palette_contract.py` holds this list to that set, to the
// chat's titles and to the chat's required arguments, so drift on either side goes red.
//
// Remedy deliberately does not send a command whose arguments the palette cannot ask for
// honestly: the six plan edits and the hunk approval open the surfaces that ask for them
// (T5_F292 T003, DECISION F292 D8) — the plan view, and the hunk decisions of the job's own diff.

export type PaletteArgKind = "task" | "text";
export type PaletteFlow = "send" | "surface";

export interface PaletteArg {
  readonly name: string;
  readonly kind: PaletteArgKind;
  readonly required: boolean;
  readonly prompt: string;
}

export interface PaletteCommand {
  readonly command: string;
  readonly title: string;
  readonly flow: PaletteFlow;
  readonly surface: string;
  readonly args: readonly PaletteArg[];
}

export const PALETTE_COMMANDS: readonly PaletteCommand[] = [
  {
    command: "job.stop",
    title: "Stop the job",
    flow: "send",
    surface: "",
    args: [
      { name: "reason", kind: "text", required: false, prompt: "Why stop? (optional)" },
    ],
  },
  {
    command: "job.pause",
    title: "Pause the job",
    flow: "send",
    surface: "",
    args: [],
  },
  {
    command: "job.unpause",
    title: "Resume the job",
    flow: "send",
    surface: "",
    args: [],
  },
  {
    command: "decision.resolve",
    title: "Answer the decision",
    flow: "surface",
    surface: "decision-inbox-card",
    args: [],
  },
  {
    command: "patch.approve-hunks",
    title: "Approve or reject the hunks of a change",
    flow: "surface",
    surface: "hunk-decisions",
    args: [],
  },
  {
    command: "chat.send",
    title: "Send a message to the job",
    flow: "send",
    surface: "",
    args: [
      { name: "message", kind: "text", required: true, prompt: "Your message to the job" },
    ],
  },
  {
    command: "job.plan-edit-task",
    title: "Edit a planned task",
    flow: "surface",
    surface: "plan-view",
    args: [],
  },
  {
    command: "job.plan-delete-task",
    title: "Delete a planned task",
    flow: "surface",
    surface: "plan-view",
    args: [],
  },
  {
    command: "job.plan-reorder",
    title: "Reorder the plan",
    flow: "surface",
    surface: "plan-view",
    args: [],
  },
  {
    command: "job.plan-merge-tasks",
    title: "Merge planned tasks",
    flow: "surface",
    surface: "plan-view",
    args: [],
  },
  {
    command: "job.plan-split-task",
    title: "Split a planned task",
    flow: "surface",
    surface: "plan-view",
    args: [],
  },
  {
    command: "job.plan-edit-acceptance",
    title: "Edit a planned task's acceptance",
    flow: "surface",
    surface: "plan-view",
    args: [],
  },
  {
    command: "job.edit-task",
    title: "Edit a task",
    flow: "surface",
    surface: "task-edit-form",
    args: [
      { name: "task_id", kind: "task", required: true, prompt: "Which task?" },
    ],
  },
  {
    command: "job.veto-task",
    title: "Veto the task",
    flow: "send",
    surface: "",
    args: [
      { name: "task_id", kind: "task", required: true, prompt: "Which task?" },
      { name: "reason", kind: "text", required: true, prompt: "Why veto it?" },
    ],
  },
  {
    command: "job.steer",
    title: "Send a note to the task's builder",
    flow: "send",
    surface: "",
    args: [
      { name: "task_id", kind: "task", required: true, prompt: "Which task?" },
      { name: "message", kind: "text", required: true, prompt: "Your note to its builder" },
    ],
  },
  {
    command: "job.inject",
    title: "Add a task to the plan",
    flow: "surface",
    surface: "add-task-sheet",
    args: [],
  },
  {
    command: "job.rerun-subtree",
    title: "Rerun the task and the tasks after it",
    flow: "send",
    surface: "",
    args: [
      { name: "task_id", kind: "task", required: true, prompt: "Which task?" },
    ],
  },
  {
    command: "job.preview-start",
    title: "Start the app preview",
    flow: "send",
    surface: "",
    args: [],
  },
  {
    command: "job.preview-stop",
    title: "Stop the app preview",
    flow: "send",
    surface: "",
    args: [],
  },
];

/** The two continuation steps of the add-task sheet's own conversation: never listed, since the
 *  sheet that started the conversation owns them. */
export const PALETTE_CONTINUATION_COMMANDS: readonly string[] = ["job.inject-confirm", "job.inject-answer"];

export function paletteCommandOf(command: string): PaletteCommand | null {
  return PALETTE_COMMANDS.find((entry) => entry.command === command) ?? null;
}
