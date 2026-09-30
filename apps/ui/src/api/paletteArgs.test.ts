// F044 T001 — the palette's argument flow (DECISION F044 D3).
import { describe, expect, it } from "vitest";
import { paletteCommandOf } from "./paletteCommands";
import type { PaletteCommand } from "./paletteCommands";
import { answerArg, argFlowComplete, currentArg, startArgFlow } from "./paletteArgs";

function entry(command: string): PaletteCommand {
  const found = paletteCommandOf(command);
  if (found === null) throw new Error(command);
  return found;
}

describe("the argument flow", () => {
  it("asks a command's arguments in its entry's order", () => {
    const flow = startArgFlow(entry("job.veto-task"));
    expect(flow).toEqual({ entry: entry("job.veto-task"), values: {}, index: 0 });
    expect(currentArg(flow)?.name).toBe("task_id");
    const second = answerArg(flow, "t4");
    expect(second).not.toBeNull();
    expect(currentArg(second!)?.name).toBe("reason");
    expect(argFlowComplete(second!)).toBe(false);
    const done = answerArg(second!, "  it is wrong  ");
    expect(done?.values).toEqual({ task_id: "t4", reason: "it is wrong" });
    expect(argFlowComplete(done!)).toBe(true);
    expect(currentArg(done!)).toBeNull();
  });

  it("is complete at once for a command that asks nothing", () => {
    const flow = startArgFlow(entry("job.pause"));
    expect(argFlowComplete(flow)).toBe(true);
    expect(answerArg(flow, "anything")).toBeNull();
  });

  it("refuses a blank answer to a required argument", () => {
    expect(answerArg(startArgFlow(entry("chat.send")), "   ")).toBeNull();
  });

  it("records a blank answer to an optional argument as no answer at all", () => {
    const done = answerArg(startArgFlow(entry("job.stop")), "  ");
    expect(done?.values).toEqual({});
    expect(argFlowComplete(done!)).toBe(true);
  });

  it("never changes the flow it was given", () => {
    const flow = startArgFlow(entry("job.steer"));
    answerArg(flow, "t1");
    expect(flow.values).toEqual({});
    expect(flow.index).toBe(0);
  });
});
