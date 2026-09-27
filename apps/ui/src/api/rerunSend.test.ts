import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import { describePauseSendResult } from "./pauseSend";
import type { RerunSubtreeSendReply, RerunSubtreeSubmitResult } from "./rerunSend";
import {
  JOB_RERUN_SUBTREE_COMMAND_ID,
  RERUN_DEADLINE_MS,
  buildRerunSubtreeRequest,
  describeRerunResult,
  rerunAnswerOf,
  sendRerunSubtree,
  submitRerunSubtreeRequest,
} from "./rerunSend";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const TASK_ID = "aaaaaaaa";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: SERVER_TOKEN };

function reply(ok: boolean, status: number, json: () => Promise<unknown>): RerunSubtreeSendReply {
  return { ok, status, json };
}

describe("RERUN_DEADLINE_MS", () => {
  it("is longer than every other send in this cockpit", () => {
    expect(RERUN_DEADLINE_MS).toBe(60000);
  });
});

describe("buildRerunSubtreeRequest", () => {
  it("names the command job.rerun-subtree and always sends task_id", () => {
    const request = buildRerunSubtreeRequest(TARGET, TASK_ID, {}, GOOD_NONCE);
    const body = JSON.parse(request!.body);
    expect(body.command).toBe(JOB_RERUN_SUBTREE_COMMAND_ID);
    expect(body.args).toEqual({ task_id: TASK_ID });
  });

  it("sends the trimmed model when it is not blank", () => {
    const request = buildRerunSubtreeRequest(TARGET, TASK_ID, { model: "  gpt-5  " }, GOOD_NONCE);
    expect(JSON.parse(request!.body).args).toEqual({ task_id: TASK_ID, model: "gpt-5" });
  });

  it("sends no model for a blank one", () => {
    const request = buildRerunSubtreeRequest(TARGET, TASK_ID, { model: "   " }, GOOD_NONCE);
    expect(JSON.parse(request!.body).args).toEqual({ task_id: TASK_ID });
  });

  it("sends no model when none is given", () => {
    const request = buildRerunSubtreeRequest(TARGET, TASK_ID, { confirmCost: true }, GOOD_NONCE);
    expect(JSON.parse(request!.body).args).toEqual({ task_id: TASK_ID, confirm_cost: true });
  });

  it("sends confirm_cost true only when it is true", () => {
    const withoutIt = buildRerunSubtreeRequest(TARGET, TASK_ID, { confirmCost: false }, GOOD_NONCE);
    expect(JSON.parse(withoutIt!.body).args).toEqual({ task_id: TASK_ID });
  });

  it("sends every combination of model and confirmation together", () => {
    const request = buildRerunSubtreeRequest(
      TARGET, TASK_ID, { model: "gpt-5", confirmCost: true }, GOOD_NONCE);
    expect(JSON.parse(request!.body).args).toEqual({
      task_id: TASK_ID, model: "gpt-5", confirm_cost: true,
    });
  });

  it("is null for an empty task id", () => {
    expect(buildRerunSubtreeRequest(TARGET, "", {}, GOOD_NONCE)).toBeNull();
  });

  it("is null for an unusable nonce", () => {
    expect(buildRerunSubtreeRequest(TARGET, TASK_ID, {}, "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildRerunSubtreeRequest(TARGET, TASK_ID, {}, GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("submitRerunSubtreeRequest", () => {
  const REQUEST: DecisionSendRequest = {
    path: "/api/jobs/x/commands", method: "POST", headers: {}, body: "{}",
  };

  it("reads the body on a successful 200 reply", async () => {
    const send = () => Promise.resolve(
      reply(true, 200, () => Promise.resolve({ outcome: "prepared", run_command: "remedy job run x" })));
    const result = await submitRerunSubtreeRequest(REQUEST, send);
    expect(result).toEqual({
      outcome: "accepted", status: 200,
      body: { outcome: "prepared", run_command: "remedy job run x" },
    });
  });

  it("answers unreachable when the send rejects, without throwing", async () => {
    const send = () => Promise.reject(new Error("offline"));
    const result = await submitRerunSubtreeRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "unreachable", status: 0, body: null });
  });

  it("answers refused with the status on a non-ok reply", async () => {
    const send = () => Promise.resolve(
      reply(false, 409, () => Promise.resolve({ error: "job_terminal: this job has already finished" })));
    const result = await submitRerunSubtreeRequest(REQUEST, send);
    expect(result).toEqual({
      outcome: "refused", status: 409, body: { error: "job_terminal: this job has already finished" },
    });
  });
});

describe("describeRerunResult", () => {
  it("a 409's sentence is the detail after the prefix, verbatim", () => {
    const message = describeRerunResult(
      { outcome: "refused", status: 409, body: { error: "job_terminal: this job has already finished" } });
    expect(message.tone).toBe("warn");
    expect(message.sentence).toBe("this job has already finished");
  });

  it("echoes a 409 with no ': ' separator whole", () => {
    const message = describeRerunResult({ outcome: "refused", status: 409, body: { error: "no separator here" } });
    expect(message.sentence).toBe("no separator here");
  });

  it("reuses pauseSend.ts's own unreachable sentence and tone", () => {
    const result: RerunSubtreeSubmitResult = { outcome: "unreachable", status: 0, body: null };
    expect(describeRerunResult(result)).toEqual(describePauseSendResult(result));
  });
});

describe("rerunAnswerOf", () => {
  it("answers the 200 body as an object", () => {
    const body = { outcome: "prepared", run_command: "remedy job run x" };
    expect(rerunAnswerOf({ outcome: "accepted", status: 200, body })).toBe(body);
  });

  it("is null for a refused result", () => {
    expect(rerunAnswerOf({ outcome: "refused", status: 409, body: { error: "x: y" } })).toBeNull();
  });

  it("is null for an unreachable result", () => {
    expect(rerunAnswerOf({ outcome: "unreachable", status: 0, body: null })).toBeNull();
  });
});

describe("sendRerunSubtree", () => {
  it("sends exactly once and reports the door's answer, plus the 200 body", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      const result: RerunSubtreeSubmitResult = {
        outcome: "accepted", status: 200, body: { outcome: "prepared", run_command: "remedy job run x" },
      };
      return Promise.resolve(result);
    };
    const outcome = await sendRerunSubtree(TARGET, TASK_ID, { model: "gpt-5" }, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(JSON.parse(sent[0].body).command).toBe(JOB_RERUN_SUBTREE_COMMAND_ID);
    expect(outcome.answer).toEqual({ outcome: "prepared", run_command: "remedy job run x" });
  });

  it("answers unreachable when the deadline wins", async () => {
    const outcome = await sendRerunSubtree(TARGET, TASK_ID, {}, {
      mintNonce: () => GOOD_NONCE,
      submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve(),
    });
    expect(outcome.message.sentence).toContain("No answer came back");
    expect(outcome.answer).toBeNull();
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const outcome = await sendRerunSubtree(TARGET, TASK_ID, {}, {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: () => new Promise(() => {}),
    });
    expect(outcome.message.tone).toBe("warn");
    expect(outcome.answer).toBeNull();
  });

  it("never reaches the network when no nonce can be minted", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve({ outcome: "accepted", status: 200, body: null } as RerunSubtreeSubmitResult);
    };
    const outcome = await sendRerunSubtree(TARGET, TASK_ID, {}, {
      mintNonce: () => null, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(outcome.message.tone).toBe("warn");
    expect(outcome.answer).toBeNull();
  });
});
