// F044 T001 — the palette's command list (DECISION F044 D1). The whole list is pinned literally;
// `tests/ui_contracts/test_palette_contract.py` pins it against the write door's exposed set and
// the chat's titles and arguments.
import { describe, expect, it } from "vitest";
import { PALETTE_COMMANDS, PALETTE_CONTINUATION_COMMANDS, paletteCommandOf } from "./paletteCommands";

const TASK = { name: "task_id", kind: "task", required: true, prompt: "Which task?" };

describe("PALETTE_COMMANDS", () => {
  it("lists every entry exactly as DECISION F044 D1 wrote it, with DECISION F292 D8's surfaces", () => {
    expect(PALETTE_COMMANDS).toEqual([
      { command: "job.stop", title: "Stop the job", flow: "send", surface: "",
        args: [{ name: "reason", kind: "text", required: false, prompt: "Why stop? (optional)" }] },
      { command: "job.pause", title: "Pause the job", flow: "send", surface: "", args: [] },
      { command: "job.unpause", title: "Resume the job", flow: "send", surface: "", args: [] },
      { command: "decision.resolve", title: "Answer the decision", flow: "surface", surface: "decision-inbox-card", args: [] },
      { command: "patch.approve-hunks", title: "Approve or reject the hunks of a change", flow: "surface", surface: "hunk-decisions", args: [] },
      { command: "chat.send", title: "Send a message to the job", flow: "send", surface: "",
        args: [{ name: "message", kind: "text", required: true, prompt: "Your message to the job" }] },
      { command: "job.plan-edit-task", title: "Edit a planned task", flow: "surface", surface: "plan-view", args: [] },
      { command: "job.plan-delete-task", title: "Delete a planned task", flow: "surface", surface: "plan-view", args: [] },
      { command: "job.plan-reorder", title: "Reorder the plan", flow: "surface", surface: "plan-view", args: [] },
      { command: "job.plan-merge-tasks", title: "Merge planned tasks", flow: "surface", surface: "plan-view", args: [] },
      { command: "job.plan-split-task", title: "Split a planned task", flow: "surface", surface: "plan-view", args: [] },
      { command: "job.plan-edit-acceptance", title: "Edit a planned task's acceptance", flow: "surface", surface: "plan-view", args: [] },
      { command: "job.edit-task", title: "Edit a task", flow: "surface", surface: "task-edit-form", args: [TASK] },
      { command: "job.veto-task", title: "Veto the task", flow: "send", surface: "",
        args: [TASK, { name: "reason", kind: "text", required: true, prompt: "Why veto it?" }] },
      { command: "job.steer", title: "Send a note to the task's builder", flow: "send", surface: "",
        args: [TASK, { name: "message", kind: "text", required: true, prompt: "Your note to its builder" }] },
      { command: "job.inject", title: "Add a task to the plan", flow: "surface", surface: "add-task-sheet", args: [] },
      { command: "job.rerun-subtree", title: "Rerun the task and the tasks after it", flow: "send", surface: "", args: [TASK] },
      { command: "job.preview-start", title: "Start the app preview", flow: "send", surface: "", args: [] },
      { command: "job.preview-stop", title: "Stop the app preview", flow: "send", surface: "", args: [] },
    ]);
  });

  it("names a surface for, and only for, a surface entry", () => {
    for (const entry of PALETTE_COMMANDS) {
      expect(entry.surface !== "", entry.command).toBe(entry.flow === "surface");
    }
  });

  it("opens the plan view for the six plan edits and the hunk decisions for the hunk approval, asking nothing", () => {
    const opened = PALETTE_COMMANDS.filter((row) => row.surface === "plan-view" || row.surface === "hunk-decisions");
    expect(opened.map((row) => [row.command, row.surface])).toEqual([
      ["patch.approve-hunks", "hunk-decisions"], ["job.plan-edit-task", "plan-view"],
      ["job.plan-delete-task", "plan-view"], ["job.plan-reorder", "plan-view"], ["job.plan-merge-tasks", "plan-view"],
      ["job.plan-split-task", "plan-view"], ["job.plan-edit-acceptance", "plan-view"],
    ]);
    for (const entry of opened) expect(entry.args, entry.command).toEqual([]);
  });

  it("holds no command, title or argument name twice", () => {
    const commands = PALETTE_COMMANDS.map((entry) => entry.command);
    const titles = PALETTE_COMMANDS.map((entry) => entry.title);
    expect(new Set(commands).size).toBe(commands.length);
    expect(new Set(titles).size).toBe(titles.length);
    for (const entry of PALETTE_COMMANDS) {
      const names = entry.args.map((arg) => arg.name);
      expect(new Set(names).size, entry.command).toBe(names.length);
    }
  });
});

describe("PALETTE_CONTINUATION_COMMANDS", () => {
  it("is the add-task sheet's two continuation steps, none of them listed", () => {
    expect(PALETTE_CONTINUATION_COMMANDS).toEqual(["job.inject-confirm", "job.inject-answer"]);
    for (const command of PALETTE_CONTINUATION_COMMANDS) {
      expect(paletteCommandOf(command)).toBeNull();
    }
  });
});

describe("paletteCommandOf", () => {
  it("answers the entry of a listed command", () => {
    expect(paletteCommandOf("job.pause")).toBe(PALETTE_COMMANDS[1]);
    expect(paletteCommandOf("job.preview-stop")?.title).toBe("Stop the app preview");
  });

  it("answers null for anything else, a prototype member included", () => {
    expect(paletteCommandOf("")).toBeNull();
    expect(paletteCommandOf("job.delete")).toBeNull();
    expect(paletteCommandOf("toString")).toBeNull();
  });
});
