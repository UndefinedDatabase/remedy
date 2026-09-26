import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import { describePauseSendResult } from "./pauseSend";
import type { VetoTaskSendReply, VetoTaskSubmitResult } from "./vetoSend";
import {
  JOB_VETO_TASK_COMMAND_ID,
  buildVetoTaskRequest,
  describeVetoTaskResult,
  sendVetoTask,
  submitVetoTaskRequest,
} from "./vetoSend";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const TASK_ID = "task-1";
const REASON = "duplicates T2's work";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: SERVER_TOKEN };

function reply(ok: boolean, status: number, json: () => Promise<unknown>): VetoTaskSendReply {
  return { ok, status, json };
}

describe("buildVetoTaskRequest", () => {
  it("builds the exact request: path, headers and body, the reason unchanged", () => {
    expect(buildVetoTaskRequest(TARGET, TASK_ID, REASON, GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: JOB_VETO_TASK_COMMAND_ID,
        client_nonce: GOOD_NONCE,
        args: { task_id: TASK_ID, reason: REASON },
      }),
    });
  });

  it("names the command job.veto-task", () => {
    const request = buildVetoTaskRequest(TARGET, TASK_ID, REASON, GOOD_NONCE);
    expect(JSON.parse(request!.body).command).toBe("job.veto-task");
  });

  it("is null for an empty task id", () => {
    expect(buildVetoTaskRequest(TARGET, "", REASON, GOOD_NONCE)).toBeNull();
  });

  it("is null for a reason blank after trimming", () => {
    expect(buildVetoTaskRequest(TARGET, TASK_ID, "   ", GOOD_NONCE)).toBeNull();
    expect(buildVetoTaskRequest(TARGET, TASK_ID, "", GOOD_NONCE)).toBeNull();
  });

  it("is null for an unusable nonce", () => {
    expect(buildVetoTaskRequest(TARGET, TASK_ID, REASON, "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildVetoTaskRequest(TARGET, TASK_ID, REASON, GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("submitVetoTaskRequest", () => {
  const REQUEST: DecisionSendRequest = {
    path: "/api/jobs/x/commands", method: "POST", headers: {}, body: "{}",
  };

  it("reads the body on a successful reply", async () => {
    const send = () => Promise.resolve(reply(true, 200, () => Promise.resolve({ outcome: "vetoed", unreachable: [] })));
    const result = await submitVetoTaskRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "accepted", status: 200, body: { outcome: "vetoed", unreachable: [] } });
  });

  it("answers unreachable when the send rejects, without throwing", async () => {
    const send = () => Promise.reject(new Error("offline"));
    const result = await submitVetoTaskRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "unreachable", status: 0, body: null });
  });

  it("answers refused with the status on a non-ok reply", async () => {
    const send = () => Promise.resolve(reply(false, 409, () => Promise.resolve({ error: "task_already_vetoed: the task is already vetoed" })));
    const result = await submitVetoTaskRequest(REQUEST, send);
    expect(result).toEqual({
      outcome: "refused", status: 409, body: { error: "task_already_vetoed: the task is already vetoed" },
    });
  });
});

describe("describeVetoTaskResult", () => {
  it("no other task depended on it", () => {
    const message = describeVetoTaskResult({ outcome: "accepted", status: 200, body: { outcome: "vetoed", unreachable: [] } });
    expect(message.sentence).toBe(
      "Vetoed. No other task depended on it. A replan proposal is waiting in the decision inbox.");
    expect(message.tone).toBe("ok");
  });

  it("exactly one dependent task, singular wording", () => {
    const message = describeVetoTaskResult(
      { outcome: "accepted", status: 200, body: { outcome: "vetoed", unreachable: ["t2"] } });
    expect(message.sentence).toBe(
      "Vetoed. 1 task that depends on it will not run. A replan proposal is waiting in the decision inbox.");
  });

  it("more than one dependent task, plural wording with the count", () => {
    const message = describeVetoTaskResult(
      { outcome: "accepted", status: 200, body: { outcome: "vetoed", unreachable: ["t2", "t3", "t4"] } });
    expect(message.sentence).toBe(
      "Vetoed. 3 tasks that depend on it will not run. A replan proposal is waiting in the decision inbox.");
  });

  it("an outcome other than vetoed reads as unconfirmed", () => {
    const message = describeVetoTaskResult({ outcome: "accepted", status: 200, body: { outcome: "something_else" } });
    expect(message.sentence).toBe("The job answered, but did not confirm the veto.");
    expect(message.tone).toBe("warn");
  });

  it.each([
    ["job_not_vetoable", "Not vetoed: this job has already finished."],
    ["task_already_vetoed", "Not vetoed: this task is already vetoed."],
    ["task_not_vetoable", "Not vetoed: this task can no longer be vetoed."],
    ["unknown_task", "Not vetoed: this job has no such task."],
  ])("409 code %s", (code, sentence) => {
    const message = describeVetoTaskResult(
      { outcome: "refused", status: 409, body: { error: `${code}: some detail` } });
    expect(message.sentence).toBe(sentence);
    expect(message.tone).toBe("warn");
  });

  it("echoes an unrecognised 409 code verbatim", () => {
    const message = describeVetoTaskResult(
      { outcome: "refused", status: 409, body: { error: "some_new_code: a new refusal" } });
    expect(message.sentence).toBe("Not vetoed: some_new_code: a new refusal.");
    expect(message.tone).toBe("warn");
  });

  it("a 400 on field reason names the door's own detail", () => {
    const message = describeVetoTaskResult(
      { outcome: "refused", status: 400, body: { field: "reason", error: "a veto reason is required and must not be empty or blank" } });
    expect(message.sentence).toBe("Not vetoed: a veto reason is required and must not be empty or blank.");
    expect(message.tone).toBe("warn");
  });

  it("words every other refusal exactly as describePauseSendResult words its own", () => {
    const statuses: VetoTaskSubmitResult[] = [
      { outcome: "refused", status: 400, body: { field: "args" } },
      { outcome: "refused", status: 403, body: null },
      { outcome: "refused", status: 429, body: null },
      { outcome: "refused", status: 500, body: null },
      { outcome: "refused", status: 418, body: null },
    ];
    for (const result of statuses) {
      expect(describeVetoTaskResult(result)).toEqual(describePauseSendResult(result));
    }
  });

  it("reuses the pause door's own unreachable sentence and tone", () => {
    const message = describeVetoTaskResult({ outcome: "unreachable", status: 0, body: null });
    expect(message.tone).toBe("warn");
    expect(message.sentence).toContain("No answer came back");
  });
});

describe("sendVetoTask", () => {
  it("sends exactly once and reports the door's answer", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      return Promise.resolve(
        { outcome: "accepted", status: 200, body: { outcome: "vetoed", unreachable: [] } } as VetoTaskSubmitResult);
    };
    const answer = await sendVetoTask(TARGET, TASK_ID, REASON, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(answer.sentence).toContain("Vetoed. No other task depended on it.");
  });

  it("never reaches the network when no nonce can be minted", async () => {
    const submit = () => Promise.resolve(
      { outcome: "accepted", status: 200, body: null } as VetoTaskSubmitResult);
    const answer = await sendVetoTask(TARGET, TASK_ID, REASON, {
      mintNonce: () => null, submit, deadline: () => new Promise(() => {}),
    });
    expect(answer.tone).toBe("warn");
  });

  it("never reaches the network when the reason is blank", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve(
        { outcome: "accepted", status: 200, body: null } as VetoTaskSubmitResult);
    };
    const answer = await sendVetoTask(TARGET, TASK_ID, "   ", {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(answer.tone).toBe("warn");
  });

  it("answers unreachable when the deadline wins", async () => {
    const answer = await sendVetoTask(TARGET, TASK_ID, REASON, {
      mintNonce: () => GOOD_NONCE,
      submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve(),
    });
    expect(answer.sentence).toContain("No answer came back");
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const answer = await sendVetoTask(TARGET, TASK_ID, REASON, {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: () => new Promise(() => {}),
    });
    expect(answer.tone).toBe("warn");
  });
});
