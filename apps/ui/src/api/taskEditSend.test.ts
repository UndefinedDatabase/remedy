import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import { describePauseSendResult } from "./pauseSend";
import type { TaskEditFields } from "./taskSpecView";
import type { TaskEditSendReply, TaskEditSubmitResult } from "./taskEditSend";
import {
  JOB_EDIT_TASK_COMMAND_ID,
  buildTaskEditRequest,
  describeTaskEditResult,
  sendTaskEdit,
  submitTaskEditRequest,
} from "./taskEditSend";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const TASK_ID = "task-1";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: SERVER_TOKEN };
const FIELDS: TaskEditFields = { title: "Renamed" };

function reply(ok: boolean, status: number, json: () => Promise<unknown>): TaskEditSendReply {
  return { ok, status, json };
}

describe("buildTaskEditRequest", () => {
  it("builds the exact request: path, headers and body", () => {
    expect(buildTaskEditRequest(TARGET, TASK_ID, FIELDS, 1, GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: JOB_EDIT_TASK_COMMAND_ID,
        client_nonce: GOOD_NONCE,
        args: { task_id: TASK_ID, fields: FIELDS, expected_version: 1 },
      }),
    });
  });

  it("names the command job.edit-task", () => {
    const request = buildTaskEditRequest(TARGET, TASK_ID, FIELDS, 1, GOOD_NONCE);
    expect(JSON.parse(request!.body).command).toBe("job.edit-task");
  });

  it("is null for a missing job id", () => {
    expect(buildTaskEditRequest({ ...TARGET, jobId: "" }, TASK_ID, FIELDS, 1, GOOD_NONCE)).toBeNull();
  });

  it("is null for a missing token", () => {
    expect(buildTaskEditRequest({ ...TARGET, serverToken: "" }, TASK_ID, FIELDS, 1, GOOD_NONCE)).toBeNull();
  });

  it("is null for an empty task id", () => {
    expect(buildTaskEditRequest(TARGET, "", FIELDS, 1, GOOD_NONCE)).toBeNull();
  });

  it("is null for an unusable nonce", () => {
    expect(buildTaskEditRequest(TARGET, TASK_ID, FIELDS, 1, "not a nonce")).toBeNull();
  });

  it("is null for a version that is not a whole number of at least 1", () => {
    expect(buildTaskEditRequest(TARGET, TASK_ID, FIELDS, 0, GOOD_NONCE)).toBeNull();
    expect(buildTaskEditRequest(TARGET, TASK_ID, FIELDS, -1, GOOD_NONCE)).toBeNull();
    expect(buildTaskEditRequest(TARGET, TASK_ID, FIELDS, 1.5, GOOD_NONCE)).toBeNull();
  });

  it("is null for empty fields", () => {
    expect(buildTaskEditRequest(TARGET, TASK_ID, {}, 1, GOOD_NONCE)).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildTaskEditRequest(TARGET, TASK_ID, FIELDS, 1, GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("submitTaskEditRequest", () => {
  const REQUEST: DecisionSendRequest = {
    path: "/api/jobs/x/commands", method: "POST", headers: {}, body: "{}",
  };

  it("reads the body on a successful reply", async () => {
    const send = () => Promise.resolve(reply(true, 200, () => Promise.resolve({ spec_version: 2 })));
    const result = await submitTaskEditRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "accepted", status: 200, body: { spec_version: 2 } });
  });

  it("answers unreachable when the send rejects, without throwing", async () => {
    const send = () => Promise.reject(new Error("offline"));
    const result = await submitTaskEditRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "unreachable", status: 0, body: null });
  });

  it("answers refused with the status on a non-ok reply", async () => {
    const send = () => Promise.resolve(reply(false, 409, () => Promise.resolve({ current_version: 1 })));
    const result = await submitTaskEditRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "refused", status: 409, body: { current_version: 1 } });
  });
});

describe("describeTaskEditResult", () => {
  it("says the new version was saved", () => {
    const message = describeTaskEditResult({ outcome: "accepted", status: 200, body: { spec_version: 2 } });
    expect(message.sentence).toBe("Saved as v2.");
    expect(message.tone).toBe("ok");
  });

  it("adds the relaunch sentence naming the job when the body's state is failed", () => {
    const message = describeTaskEditResult(
      { outcome: "accepted", status: 200, body: { spec_version: 2, state: "failed" } },
      JOB_ID,
    );
    expect(message.sentence).toBe(
      `Saved as v2. Relaunch the job to run it: remedy job run ${JOB_ID}.`);
  });

  it("drops the relaunch command when no jobId is given", () => {
    const message = describeTaskEditResult(
      { outcome: "accepted", status: 200, body: { spec_version: 2, state: "failed" } },
    );
    expect(message.sentence).toBe("Saved as v2. Relaunch the job to run it.");
  });

  it("does not add the relaunch sentence for a waiting or paused task", () => {
    expect(describeTaskEditResult(
      { outcome: "accepted", status: 200, body: { spec_version: 2, state: "waiting" } },
    ).sentence).toBe("Saved as v2.");
    expect(describeTaskEditResult(
      { outcome: "accepted", status: 200, body: { spec_version: 3, state: "paused" } },
    ).sentence).toBe("Saved as v3.");
  });

  it("asks the operator to reopen the task on a stale version", () => {
    const message = describeTaskEditResult(
      { outcome: "refused", status: 409, body: { current_version: 4 } },
    );
    expect(message.sentence).toBe(
      "Not saved: this task changed since you opened it. Close it and edit again.");
    expect(message.tone).toBe("error");
  });

  it("shows the backend's own detail for any other 409", () => {
    const message = describeTaskEditResult(
      { outcome: "refused", status: 409, body: { error: "x", detail: "the task is not open for a runtime edit" } },
    );
    expect(message.sentence).toBe("Not saved: the task is not open for a runtime edit.");
    expect(message.tone).toBe("error");
  });

  it("words every other refusal exactly as describePauseSendResult words its own", () => {
    const statuses: TaskEditSubmitResult[] = [
      { outcome: "refused", status: 400, body: null },
      { outcome: "refused", status: 403, body: null },
      { outcome: "refused", status: 429, body: null },
      { outcome: "refused", status: 500, body: null },
      { outcome: "refused", status: 418, body: null },
    ];
    for (const result of statuses) {
      expect(describeTaskEditResult(result)).toEqual(describePauseSendResult(result));
    }
  });

  it("reuses the pause door's own unreachable sentence and tone", () => {
    const message = describeTaskEditResult({ outcome: "unreachable", status: 0, body: null });
    expect(message.tone).toBe("warn");
    expect(message.sentence).toContain("No answer came back");
  });
});

describe("sendTaskEdit", () => {
  it("sends exactly once and reports the door's answer", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      return Promise.resolve(
        { outcome: "accepted", status: 200, body: { spec_version: 2 } } as TaskEditSubmitResult);
    };
    const answer = await sendTaskEdit(TARGET, TASK_ID, FIELDS, 1, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(answer.sentence).toBe("Saved as v2.");
  });

  it("passes the target's job id into the relaunch sentence", async () => {
    const submit = () => Promise.resolve(
      { outcome: "accepted", status: 200, body: { spec_version: 2, state: "failed" } } as TaskEditSubmitResult);
    const answer = await sendTaskEdit(TARGET, TASK_ID, FIELDS, 1, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(answer.sentence).toBe(
      `Saved as v2. Relaunch the job to run it: remedy job run ${JOB_ID}.`);
  });

  it("never reaches the network when no nonce can be minted", async () => {
    const submit = () => Promise.resolve(
      { outcome: "accepted", status: 200, body: null } as TaskEditSubmitResult);
    const answer = await sendTaskEdit(TARGET, TASK_ID, FIELDS, 1, {
      mintNonce: () => null, submit, deadline: () => new Promise(() => {}),
    });
    expect(answer.tone).toBe("warn");
  });

  it("never reaches the network when fields is empty", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve(
        { outcome: "accepted", status: 200, body: null } as TaskEditSubmitResult);
    };
    const answer = await sendTaskEdit(TARGET, TASK_ID, {}, 1, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(answer.tone).toBe("warn");
  });

  it("answers unreachable when the deadline wins", async () => {
    const answer = await sendTaskEdit(TARGET, TASK_ID, FIELDS, 1, {
      mintNonce: () => GOOD_NONCE,
      submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve(),
    });
    expect(answer.sentence).toContain("No answer came back");
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const answer = await sendTaskEdit(TARGET, TASK_ID, FIELDS, 1, {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: () => new Promise(() => {}),
    });
    expect(answer.tone).toBe("warn");
  });
});
