import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import { describePauseSendResult } from "./pauseSend";
import type { InjectSendReply, InjectSubmitResult } from "./injectSend";
import {
  INJECT_DRAFT_DEADLINE_MS,
  INJECT_SHORTFALL_OPTIONS,
  INJECT_STEP_DEADLINE_MS,
  JOB_INJECT_ANSWER_COMMAND_ID,
  JOB_INJECT_COMMAND_ID,
  JOB_INJECT_CONFIRM_COMMAND_ID,
  buildInjectAnswerRequest,
  buildInjectConfirmRequest,
  buildInjectDraftRequest,
  describeInjectResult,
  injectAnswerOf,
  sendInjectAnswer,
  sendInjectConfirm,
  sendInjectDraft,
  submitInjectRequest,
} from "./injectSend";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const TEXT = "add a smoke test for the new endpoint";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: SERVER_TOKEN };

function reply(ok: boolean, status: number, json: () => Promise<unknown>): InjectSendReply {
  return { ok, status, json };
}

describe("the three deadlines", () => {
  it("the draft waits on the planner's call", () => {
    expect(INJECT_DRAFT_DEADLINE_MS).toBe(120000);
  });

  it("a confirm or an answer takes the shared step bound", () => {
    expect(INJECT_STEP_DEADLINE_MS).toBe(20000);
  });
});

describe("buildInjectDraftRequest", () => {
  it("builds the exact request with no after", () => {
    expect(buildInjectDraftRequest(TARGET, TEXT, undefined, GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: JOB_INJECT_COMMAND_ID,
        client_nonce: GOOD_NONCE,
        args: { text: TEXT },
      }),
    });
  });

  it("carries after only when it is a non-empty string", () => {
    const request = buildInjectDraftRequest(TARGET, TEXT, "T003", GOOD_NONCE);
    expect(JSON.parse(request!.body).args).toEqual({ text: TEXT, after: "T003" });
  });

  it("drops an empty-string after rather than sending it", () => {
    const request = buildInjectDraftRequest(TARGET, TEXT, "", GOOD_NONCE);
    expect(JSON.parse(request!.body).args).toEqual({ text: TEXT });
  });

  it("names the command job.inject", () => {
    const request = buildInjectDraftRequest(TARGET, TEXT, undefined, GOOD_NONCE);
    expect(JSON.parse(request!.body).command).toBe("job.inject");
  });

  it("is null for text blank after trimming", () => {
    expect(buildInjectDraftRequest(TARGET, "   ", undefined, GOOD_NONCE)).toBeNull();
    expect(buildInjectDraftRequest(TARGET, "", undefined, GOOD_NONCE)).toBeNull();
  });

  it("is null for an unusable nonce", () => {
    expect(buildInjectDraftRequest(TARGET, TEXT, undefined, "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildInjectDraftRequest(TARGET, TEXT, undefined, GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("buildInjectConfirmRequest", () => {
  it("builds the exact request", () => {
    expect(buildInjectConfirmRequest(TARGET, "draft-1", GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: JOB_INJECT_CONFIRM_COMMAND_ID,
        client_nonce: GOOD_NONCE,
        args: { confirm_token: "draft-1" },
      }),
    });
  });

  it("names the command job.inject-confirm", () => {
    const request = buildInjectConfirmRequest(TARGET, "draft-1", GOOD_NONCE);
    expect(JSON.parse(request!.body).command).toBe("job.inject-confirm");
  });

  it("is null for an empty token", () => {
    expect(buildInjectConfirmRequest(TARGET, "", GOOD_NONCE)).toBeNull();
  });

  it("is null for an unusable nonce", () => {
    expect(buildInjectConfirmRequest(TARGET, "draft-1", "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildInjectConfirmRequest(TARGET, "draft-1", GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("buildInjectAnswerRequest", () => {
  it("builds the exact request", () => {
    expect(buildInjectAnswerRequest(TARGET, "draft-1", "extend_budget", GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: JOB_INJECT_ANSWER_COMMAND_ID,
        client_nonce: GOOD_NONCE,
        args: { draft_id: "draft-1", option: "extend_budget" },
      }),
    });
  });

  it("names the command job.inject-answer", () => {
    const request = buildInjectAnswerRequest(TARGET, "draft-1", "drop", GOOD_NONCE);
    expect(JSON.parse(request!.body).command).toBe("job.inject-answer");
  });

  it("accepts every option INJECT_SHORTFALL_OPTIONS names", () => {
    for (const option of INJECT_SHORTFALL_OPTIONS) {
      expect(buildInjectAnswerRequest(TARGET, "draft-1", option, GOOD_NONCE)).not.toBeNull();
    }
  });

  it("is null for an empty draft id", () => {
    expect(buildInjectAnswerRequest(TARGET, "", "drop", GOOD_NONCE)).toBeNull();
  });

  it("is null for an option outside the three", () => {
    expect(buildInjectAnswerRequest(TARGET, "draft-1", "cancel", GOOD_NONCE)).toBeNull();
    expect(buildInjectAnswerRequest(TARGET, "draft-1", "", GOOD_NONCE)).toBeNull();
  });

  it("is null for an unusable nonce", () => {
    expect(buildInjectAnswerRequest(TARGET, "draft-1", "drop", "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildInjectAnswerRequest(TARGET, "draft-1", "drop", GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("submitInjectRequest", () => {
  const REQUEST: DecisionSendRequest = {
    path: "/api/jobs/x/commands", method: "POST", headers: {}, body: "{}",
  };

  it("reads the body on a successful reply", async () => {
    const send = () => Promise.resolve(reply(true, 200, () => Promise.resolve({ outcome: "drafted" })));
    const result = await submitInjectRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "accepted", status: 200, body: { outcome: "drafted" } });
  });

  it("answers unreachable when the send rejects, without throwing", async () => {
    const send = () => Promise.reject(new Error("offline"));
    const result = await submitInjectRequest(REQUEST, send);
    expect(result).toEqual({ outcome: "unreachable", status: 0, body: null });
  });

  it("answers refused with the status on a non-ok reply", async () => {
    const send = () => Promise.resolve(reply(false, 409, () => Promise.resolve({ error: "draft_expired: it expired" })));
    const result = await submitInjectRequest(REQUEST, send);
    expect(result).toEqual({
      outcome: "refused", status: 409, body: { error: "draft_expired: it expired" },
    });
  });
});

describe("describeInjectResult", () => {
  it("drafted", () => {
    const message = describeInjectResult({ outcome: "accepted", status: 200, body: { outcome: "drafted" } });
    expect(message.tone).toBe("ok");
    expect(message.sentence).toBe("Drafted. Review it, then confirm to add this task to the plan.");
  });

  it("shortfall", () => {
    const message = describeInjectResult({ outcome: "accepted", status: 200, body: { outcome: "shortfall" } });
    expect(message.tone).toBe("warn");
    expect(message.sentence).toBe(
      "This draft would put the job over budget. Choose how to proceed before it can be confirmed.");
  });

  it("confirmed", () => {
    const message = describeInjectResult({ outcome: "accepted", status: 200, body: { outcome: "confirmed" } });
    expect(message.tone).toBe("ok");
    expect(message.sentence).toBe("Added. This task joins the plan and the job may start it next.");
  });

  it("dropped", () => {
    const message = describeInjectResult({ outcome: "accepted", status: 200, body: { outcome: "dropped" } });
    expect(message.tone).toBe("ok");
    expect(message.sentence).toBe("Dropped. This draft will not be added.");
  });

  it("an outcome other than the four reads as unconfirmed", () => {
    const message = describeInjectResult({ outcome: "accepted", status: 200, body: { outcome: "something_else" } });
    expect(message.tone).toBe("warn");
    expect(message.sentence).toBe("The job answered, but did not confirm the injection.");
  });

  it.each([
    ["job_terminal", "Not added: this job has already finished."],
    ["no_task_plan", "Not added: this job has no task plan to add a task to."],
    ["plan_full", "Not added: the plan is already at its task cap."],
    ["planner_unavailable", "Not drafted: no planner is available right now."],
    ["budget_unreadable", "Not drafted: this job's budget state cannot be read."],
    ["draft_unparseable", "Not drafted: the planner's reply could not be read as a task."],
    ["draft_invalid", "Not drafted: the drafted task cannot be added to this job's plan."],
    ["unknown_task", "Not added: this job has no such task."],
    ["draft_unknown", "Not confirmed: this draft no longer exists."],
    ["draft_expired", "Not confirmed: this draft has expired."],
    ["draft_needs_decision", "Not confirmed: this draft is over budget and needs a decision first."],
    ["already_confirmed", "Not confirmed: this draft has already been confirmed."],
    ["draft_stale", "Not confirmed: this draft no longer matches the job's plan."],
    ["draft_not_in_shortfall", "Not answered: this draft is not waiting on a shortfall decision."],
    ["already_answered", "Not answered: this draft's shortfall has already been answered."],
    ["cannot_shrink", "Not answered: this draft cannot be shrunk any further."],
  ])("409 code %s", (code, sentence) => {
    const message = describeInjectResult(
      { outcome: "refused", status: 409, body: { error: `${code}: some detail` } });
    expect(message.sentence).toBe(sentence);
    expect(message.tone).toBe("warn");
  });

  it("echoes an unrecognised 409 code verbatim", () => {
    const message = describeInjectResult(
      { outcome: "refused", status: 409, body: { error: "some_new_code: a new refusal" } });
    expect(message.sentence).toBe("Not done: some_new_code: a new refusal.");
    expect(message.tone).toBe("warn");
  });

  it("a 400 on field text names the door's own detail", () => {
    const message = describeInjectResult(
      { outcome: "refused", status: 400,
        body: { field: "text", error: "an injected task's text is required and must not be empty or blank" } });
    expect(message.sentence).toBe(
      "Not drafted: an injected task's text is required and must not be empty or blank.");
    expect(message.tone).toBe("warn");
  });

  it("words every other refusal exactly as describePauseSendResult words its own", () => {
    const statuses: InjectSubmitResult[] = [
      { outcome: "refused", status: 400, body: { field: "args" } },
      { outcome: "refused", status: 403, body: null },
      { outcome: "refused", status: 429, body: null },
      { outcome: "refused", status: 500, body: null },
      { outcome: "refused", status: 418, body: null },
    ];
    for (const result of statuses) {
      expect(describeInjectResult(result)).toEqual(describePauseSendResult(result));
    }
  });

  it("reuses the pause door's own unreachable sentence and tone", () => {
    const message = describeInjectResult({ outcome: "unreachable", status: 0, body: null });
    expect(message.tone).toBe("warn");
    expect(message.sentence).toContain("No answer came back");
  });
});

describe("injectAnswerOf", () => {
  it("answers the 200 body as an object", () => {
    const body = { outcome: "drafted", confirm_token: "draft-1" };
    expect(injectAnswerOf({ outcome: "accepted", status: 200, body })).toBe(body);
  });

  it("is null for a refused result", () => {
    expect(injectAnswerOf({ outcome: "refused", status: 409, body: { error: "x: y" } })).toBeNull();
  });

  it("is null for an unreachable result", () => {
    expect(injectAnswerOf({ outcome: "unreachable", status: 0, body: null })).toBeNull();
  });
});

describe("sendInjectDraft", () => {
  it("sends exactly once and reports the door's answer, plus the 200 body", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      return Promise.resolve(
        { outcome: "accepted", status: 200, body: { outcome: "drafted", confirm_token: "draft-1" } } as InjectSubmitResult);
    };
    const outcome = await sendInjectDraft(TARGET, TEXT, undefined, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(outcome.message.sentence).toContain("Drafted.");
    expect(outcome.answer).toEqual({ outcome: "drafted", confirm_token: "draft-1" });
  });

  it("never reaches the network when no nonce can be minted", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve({ outcome: "accepted", status: 200, body: null } as InjectSubmitResult);
    };
    const outcome = await sendInjectDraft(TARGET, TEXT, undefined, {
      mintNonce: () => null, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(outcome.message.tone).toBe("warn");
    expect(outcome.answer).toBeNull();
  });

  it("never reaches the network when the text is blank", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve({ outcome: "accepted", status: 200, body: null } as InjectSubmitResult);
    };
    const outcome = await sendInjectDraft(TARGET, "   ", undefined, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(outcome.message.tone).toBe("warn");
  });

  it("answers unreachable when the deadline wins", async () => {
    const outcome = await sendInjectDraft(TARGET, TEXT, undefined, {
      mintNonce: () => GOOD_NONCE,
      submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve(),
    });
    expect(outcome.message.sentence).toContain("No answer came back");
    expect(outcome.answer).toBeNull();
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const outcome = await sendInjectDraft(TARGET, TEXT, undefined, {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: () => new Promise(() => {}),
    });
    expect(outcome.message.tone).toBe("warn");
  });
});

describe("sendInjectConfirm", () => {
  it("sends exactly once and reports the door's answer", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      return Promise.resolve(
        { outcome: "accepted", status: 200, body: { outcome: "confirmed" } } as InjectSubmitResult);
    };
    const outcome = await sendInjectConfirm(TARGET, "draft-1", {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(JSON.parse(sent[0].body).command).toBe("job.inject-confirm");
    expect(outcome.message.sentence).toContain("Added.");
  });

  it("never reaches the network when the token is empty", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve({ outcome: "accepted", status: 200, body: null } as InjectSubmitResult);
    };
    const outcome = await sendInjectConfirm(TARGET, "", {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(outcome.message.tone).toBe("warn");
  });

  it("answers unreachable when the deadline wins", async () => {
    const outcome = await sendInjectConfirm(TARGET, "draft-1", {
      mintNonce: () => GOOD_NONCE,
      submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve(),
    });
    expect(outcome.message.sentence).toContain("No answer came back");
  });
});

describe("sendInjectAnswer", () => {
  it("sends exactly once and reports the door's answer", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      return Promise.resolve(
        { outcome: "accepted", status: 200, body: { outcome: "dropped" } } as InjectSubmitResult);
    };
    const outcome = await sendInjectAnswer(TARGET, "draft-1", "drop", {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(JSON.parse(sent[0].body).command).toBe("job.inject-answer");
    expect(outcome.message.sentence).toContain("Dropped.");
  });

  it("never reaches the network when the option is outside the three", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve({ outcome: "accepted", status: 200, body: null } as InjectSubmitResult);
    };
    const outcome = await sendInjectAnswer(TARGET, "draft-1", "cancel", {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(outcome.message.tone).toBe("warn");
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const outcome = await sendInjectAnswer(TARGET, "draft-1", "drop", {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: () => new Promise(() => {}),
    });
    expect(outcome.message.tone).toBe("warn");
  });
});
