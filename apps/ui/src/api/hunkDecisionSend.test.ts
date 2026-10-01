// T5_F292 T003 — the hunk decision request, end to end (DECISION F292 D6).
import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import { describePauseSendResult } from "./pauseSend";
import type { TaskEditSubmitResult } from "./taskEditSend";
import {
  HUNK_DECISION_COMMAND_ID,
  buildHunkDecisionRequest,
  describeHunkDecisionResult,
  sendHunkDecision,
} from "./hunkDecisionSend";

const TARGET = { jobId: "0123456789abcdef", serverToken: "token-abc" };
const NONCE = "ui-a1b2c3d4";
const ARGS = { approved: ["h1"], rejected: [{ id: "h2", reason: "too broad" }] };

describe("buildHunkDecisionRequest", () => {
  it("builds the exact request for patch.approve-hunks", () => {
    expect(HUNK_DECISION_COMMAND_ID).toBe("patch.approve-hunks");
    expect(buildHunkDecisionRequest(TARGET, { ...ARGS, task_run: "T001" }, NONCE)).toEqual({
      path: "/api/jobs/0123456789abcdef/commands",
      method: "POST",
      headers: { Authorization: "Bearer token-abc", "X-Remedy-CSRF": "token-abc", "Content-Type": "application/json" },
      body: JSON.stringify({ command: "patch.approve-hunks", client_nonce: NONCE,
        args: { approved: ["h1"], rejected: [{ id: "h2", reason: "too broad" }], task_run: "T001" } }),
    });
  });
  it.each([
    ["no job id", { ...TARGET, jobId: "" }, ARGS, NONCE],
    ["no token", { ...TARGET, serverToken: "" }, ARGS, NONCE],
    ["a bad nonce", TARGET, ARGS, "../x"],
    ["a decision that decides nothing", TARGET, { approved: [], rejected: [] }, NONCE],
  ])("is null for %s", (_label, target, args, nonce) => {
    expect(buildHunkDecisionRequest(target, args, nonce)).toBeNull();
  });
});

describe("describeHunkDecisionResult", () => {
  it("an accepted decision names its counts", () => {
    expect(describeHunkDecisionResult({ outcome: "accepted", status: 200,
      body: { command: "patch.approve-hunks", outcome: "accepted", attempt_key: "job:workspace.diff", approved: 1, rejected: 1, pending: 1 } }))
      .toEqual({ message: { tone: "ok", sentence: "Recorded: 1 approved, 1 rejected, 1 pending." }, recorded: true });
  });
  it("an accepted answer without counts says so rather than inventing them", () => {
    expect(describeHunkDecisionResult({ outcome: "accepted", status: 200, body: null }).message.sentence)
      .toBe("Recorded: ? approved, ? rejected, ? pending.");
  });
  it("the door's one refusal says the server refused it and how to try again, and invents no reason", () => {
    expect(describeHunkDecisionResult({ outcome: "refused", status: 409, body: { error: "hunk decision was refused" } }))
      .toEqual({ message: { tone: "error", sentence:
        "Not recorded: the server refused this decision for this change. Close the change, open it again and decide again." },
        recorded: false });
  });
  it.each([
    ["a 400", { outcome: "refused", status: 400, body: null }],
    ["a 403", { outcome: "refused", status: 403, body: null }],
    ["a 500", { outcome: "refused", status: 500, body: null }],
    ["no answer", { outcome: "unreachable", status: 0, body: null }],
  ] as [string, TaskEditSubmitResult][])("%s is worded as the pause door words it", (_label, result) => {
    expect(describeHunkDecisionResult(result)).toEqual({ message: describePauseSendResult(result), recorded: false });
  });
});

describe("sendHunkDecision", () => {
  it("sends one request and reports it recorded", async () => {
    const sent: DecisionSendRequest[] = [];
    const outcome = await sendHunkDecision(TARGET, ARGS, {
      mintNonce: () => NONCE,
      submit: async (request) => { sent.push(request); return { outcome: "accepted", status: 200, body: { approved: 1, rejected: 1, pending: 0 } }; },
      deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(JSON.parse(sent[0].body).args).toEqual(ARGS);
    expect(outcome).toEqual({ message: { tone: "ok", sentence: "Recorded: 1 approved, 1 rejected, 0 pending." }, recorded: true });
  });
  it("touches no network when no nonce can be minted or nothing is decided", async () => {
    let calls = 0;
    const submit = async () => { calls += 1; return { outcome: "accepted", status: 200, body: null } as TaskEditSubmitResult; };
    const unsendable = { message: { tone: "warn", sentence: "This decision cannot be sent as it stands." }, recorded: false };
    expect(await sendHunkDecision(TARGET, ARGS, { mintNonce: () => null, submit })).toEqual(unsendable);
    expect(await sendHunkDecision(TARGET, { approved: [], rejected: [] }, { mintNonce: () => NONCE, submit })).toEqual(unsendable);
    expect(calls).toBe(0);
  });
  it("a send that never answers before the deadline, or throws, is unreachable", async () => {
    const unreachable = describeHunkDecisionResult({ outcome: "unreachable", status: 0, body: null });
    expect(await sendHunkDecision(TARGET, ARGS, { mintNonce: () => NONCE, submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve() })).toEqual(unreachable);
    expect(await sendHunkDecision(TARGET, ARGS, { mintNonce: () => NONCE, submit: () => Promise.reject(new Error("down")),
      deadline: () => new Promise(() => {}) })).toEqual(unreachable);
  });
});
