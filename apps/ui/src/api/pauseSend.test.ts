import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import type { PauseSendReply, PauseSubmitResult } from "./pauseSend";
import {
  JOB_PAUSE_COMMAND_ID,
  JOB_UNPAUSE_COMMAND_ID,
  buildPauseSendRequest,
  describePauseSendResult,
  sendPauseCommand,
  submitPauseSendRequest,
} from "./pauseSend";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const TASK_ID = "task-1";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: SERVER_TOKEN };

function reply(ok: boolean, status: number, json: () => Promise<unknown>): PauseSendReply {
  return { ok, status, json };
}

describe("buildPauseSendRequest", () => {
  it("builds the job scope request with empty args", () => {
    expect(buildPauseSendRequest(TARGET, JOB_PAUSE_COMMAND_ID, undefined, GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: JOB_PAUSE_COMMAND_ID,
        client_nonce: GOOD_NONCE,
        args: {},
      }),
    });
  });

  it("builds the task scope request naming the task", () => {
    const request = buildPauseSendRequest(TARGET, JOB_UNPAUSE_COMMAND_ID, TASK_ID, GOOD_NONCE);
    expect(JSON.parse(request!.body)).toEqual({
      command: JOB_UNPAUSE_COMMAND_ID,
      client_nonce: GOOD_NONCE,
      args: { task: TASK_ID },
    });
  });

  it("answers null for a missing job, token, an empty task id or an unusable nonce", () => {
    expect(buildPauseSendRequest({ ...TARGET, jobId: "" }, JOB_PAUSE_COMMAND_ID, undefined, GOOD_NONCE)).toBeNull();
    expect(buildPauseSendRequest({ ...TARGET, serverToken: "" }, JOB_PAUSE_COMMAND_ID, undefined, GOOD_NONCE)).toBeNull();
    expect(buildPauseSendRequest(TARGET, JOB_PAUSE_COMMAND_ID, "", GOOD_NONCE)).toBeNull();
    expect(buildPauseSendRequest(TARGET, JOB_PAUSE_COMMAND_ID, undefined, "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildPauseSendRequest(TARGET, JOB_PAUSE_COMMAND_ID, undefined, GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("submitPauseSendRequest", () => {
  const REQUEST: DecisionSendRequest = {
    path: "/api/jobs/x/commands", method: "POST", headers: {}, body: "{}",
  };

  it("reads the body on a successful reply", async () => {
    const send = () => Promise.resolve(reply(true, 200, () => Promise.resolve({ outcome: "requested" })));
    const result = await submitPauseSendRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "accepted", status: 200, body: { outcome: "requested" } });
  });

  it("answers a null body when the reply is not JSON", async () => {
    const send = () => Promise.resolve(reply(true, 200, () => Promise.reject(new Error("bad json"))));
    const result = await submitPauseSendRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "accepted", status: 200, body: null });
  });

  it("answers a null body when the parsed JSON is not an object", async () => {
    const send = () => Promise.resolve(reply(true, 200, () => Promise.resolve("not an object")));
    const result = await submitPauseSendRequest(REQUEST, send);
    expect(result.body).toBeNull();
  });

  it("answers unreachable when the send rejects, without throwing", async () => {
    const send = () => Promise.reject(new Error("offline"));
    const result = await submitPauseSendRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "unreachable", status: 0, body: null });
  });

  it("answers refused with the status on a non-ok reply", async () => {
    const send = () => Promise.resolve(reply(false, 409, () => Promise.resolve({ outcome: "refused" })));
    const result = await submitPauseSendRequest(REQUEST, send);
    expect(result.outcome).toBe("refused");
    expect(result.status).toBe(409);
  });
});

describe("describePauseSendResult", () => {
  function accepted(body: Record<string, unknown> | null): PauseSubmitResult {
    return { outcome: "accepted", status: 200, body };
  }

  it("gives every named outcome word its own sentence", () => {
    expect(describePauseSendResult(accepted({ outcome: "requested" })).sentence).toContain("Pause requested");
    expect(describePauseSendResult(accepted({ outcome: "paused" })).sentence).toContain("This task is paused");
    expect(describePauseSendResult(accepted({ outcome: "released" })).sentence).toContain("released");
    expect(describePauseSendResult(accepted({ outcome: "withdrawn" })).sentence).toContain("taken back");
    expect(describePauseSendResult(accepted({ outcome: "not_paused" })).sentence)
      .toBe("Nothing was paused, so nothing changed.");
    expect(describePauseSendResult(accepted({ outcome: "something_else" })).sentence)
      .toBe("The job answered, but not in a way this page understands.");
  });

  it("names the relaunch command in the parked sentence", () => {
    const message = describePauseSendResult(accepted({ outcome: "parked", next: "remedy job run abc123" }));
    expect(message.sentence).toBe("This job is paused and saved. To continue it, run: remedy job run abc123");
  });

  it("says an ended job cannot be paused or resumed on a 409", () => {
    const message = describePauseSendResult({ outcome: "refused", status: 409, body: null });
    expect(message.sentence).toBe("This job has ended, so it cannot be paused or resumed.");
    expect(message.tone).toBe("error");
  });

  it("maps every refusal status to the same tone describeChatSendResult gives it", () => {
    const tones: [number, string][] = [
      [400, "error"], [403, "error"], [409, "error"], [429, "warn"], [500, "warn"], [418, "error"],
    ];
    for (const [status, tone] of tones) {
      expect(describePauseSendResult({ outcome: "refused", status, body: null }).tone).toBe(tone);
    }
  });

  it("reuses steering's own unreachable sentence and tone", () => {
    const message = describePauseSendResult({ outcome: "unreachable", status: 0, body: null });
    expect(message.tone).toBe("warn");
    expect(message.sentence).toContain("No answer came back");
  });

  it("answers a fresh object every call", () => {
    const result: PauseSubmitResult = accepted({ outcome: "requested" });
    expect(describePauseSendResult(result)).not.toBe(describePauseSendResult(result));
  });
});

describe("sendPauseCommand", () => {
  it("sends exactly once and reports the door's answer", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      return Promise.resolve({ outcome: "accepted", status: 200, body: { outcome: "requested" } } as PauseSubmitResult);
    };
    const answer = await sendPauseCommand(TARGET, JOB_PAUSE_COMMAND_ID, undefined, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(answer.sentence).toContain("Pause requested");
  });

  it("never reaches the network when no nonce can be minted", async () => {
    const submit = () => Promise.resolve({ outcome: "accepted", status: 200, body: null } as PauseSubmitResult);
    const answer = await sendPauseCommand(TARGET, JOB_PAUSE_COMMAND_ID, undefined, {
      mintNonce: () => null, submit, deadline: () => new Promise(() => {}),
    });
    expect(answer.tone).toBe("warn");
  });

  it("answers unreachable when the deadline wins", async () => {
    const answer = await sendPauseCommand(TARGET, JOB_UNPAUSE_COMMAND_ID, TASK_ID, {
      mintNonce: () => GOOD_NONCE,
      submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve(),
    });
    expect(answer.sentence).toContain("No answer came back");
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const answer = await sendPauseCommand(TARGET, JOB_PAUSE_COMMAND_ID, undefined, {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: () => new Promise(() => {}),
    });
    expect(answer.tone).toBe("warn");
  });
});
