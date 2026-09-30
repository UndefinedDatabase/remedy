// F044 T001 — the palette's send (DECISION F044 D3). The network is never reached: each sender's
// own seams are replaced, and the request the door would receive is read back.
import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import { paletteCommandOf } from "./paletteCommands";
import type { PaletteCommand } from "./paletteCommands";
import { answerArg, startArgFlow } from "./paletteArgs";
import type { PaletteArgFlow } from "./paletteArgs";
import { PALETTE_RERUN_CONFIRM_ELSEWHERE, sendPaletteCommand } from "./paletteSend";

const TARGET = { jobId: "job-1", serverToken: "tok" };

function entry(command: string): PaletteCommand {
  const found = paletteCommandOf(command);
  if (found === null) throw new Error(command);
  return found;
}

function flowOf(command: string, answers: string[]): PaletteArgFlow {
  let flow = startArgFlow(entry(command));
  for (const answer of answers) {
    const next = answerArg(flow, answer);
    if (next === null) throw new Error(answer);
    flow = next;
  }
  return flow;
}

describe("sendPaletteCommand through the chat's card sender", () => {
  it("sends the command with the flow's arguments and says it was sent", async () => {
    const sent: DecisionSendRequest[] = [];
    const message = await sendPaletteCommand(TARGET, flowOf("job.veto-task", ["t4", "wrong"]), {
      card: { mintNonce: () => "nonce-1", submit: async (request) => { sent.push(request); return { outcome: "accepted", status: 200 }; } },
    });
    expect(message).toEqual({ tone: "ok", sentence: "Sent: job.veto-task." });
    expect(sent.length).toBe(1);
    expect(sent[0].path).toBe("/api/jobs/job-1/commands");
    expect(JSON.parse(sent[0].body)).toEqual({
      command: "job.veto-task", client_nonce: "nonce-1", args: { task_id: "t4", reason: "wrong" },
    });
  });

  it("sends no empty argument for an optional one left blank", async () => {
    const sent: DecisionSendRequest[] = [];
    await sendPaletteCommand(TARGET, flowOf("job.stop", [""]), {
      card: { mintNonce: () => "nonce-2", submit: async (request) => { sent.push(request); return { outcome: "accepted", status: 200 }; } },
    });
    expect(JSON.parse(sent[0].body)).toEqual({ command: "job.stop", client_nonce: "nonce-2", args: {} });
  });

  it("speaks the card's own words for a refusal", async () => {
    const message = await sendPaletteCommand(TARGET, flowOf("job.pause", []), {
      card: { mintNonce: () => "nonce-3", submit: async () => ({ outcome: "refused", status: 409 }) },
    });
    expect(message).toEqual({ tone: "error", sentence: "The job refused it in its current state, so nothing was done." });
  });
});

describe("sendPaletteCommand for a rerun", () => {
  function rerunWith(body: Record<string, unknown>) {
    const sent: DecisionSendRequest[] = [];
    const promise = sendPaletteCommand(TARGET, flowOf("job.rerun-subtree", ["t2"]), {
      rerun: {
        mintNonce: () => "nonce-4",
        submit: async (request) => { sent.push(request); return { outcome: "accepted", status: 200, body }; },
      },
    });
    return { sent, promise };
  }

  it("goes through the rerun's own sender with the task", async () => {
    const { sent, promise } = rerunWith({ outcome: "prepared", root_task_id: "t2", subtree: ["t2", "t3"], run_command: "remedy job run job-1" });
    const message = await promise;
    expect(JSON.parse(sent[0].body)).toEqual({ command: "job.rerun-subtree", client_nonce: "nonce-4", args: { task_id: "t2" } });
    expect(message).toEqual({
      tone: "ok",
      sentence: "Task t2 and 1 task after it were reset to run again. Run it with: remedy job run job-1",
    });
  });

  it("says where to confirm a rerun whose cost needs confirming", async () => {
    const { promise } = rerunWith({ outcome: "needs_confirmation", subtree: ["t2"] });
    const message = await promise;
    expect(PALETTE_RERUN_CONFIRM_ELSEWHERE).toBe("Confirm it from the run's detail.");
    expect(message).toEqual({
      tone: "warn",
      sentence: "The cost of rerunning task t2 and 0 tasks after it cannot be estimated in advance. Confirm it from the run's detail.",
    });
  });
});
