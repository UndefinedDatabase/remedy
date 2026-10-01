// T5_F292 T002 — the plan edit request, end to end (DECISION F292 D3).
import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import { describePauseSendResult } from "./pauseSend";
import type { TaskEditSubmitResult } from "./taskEditSend";
import {
  PLAN_EDIT_COMMANDS,
  buildPlanEditRequest,
  describePlanEditResult,
  planDeleteTaskEdit,
  planEditAcceptanceEdit,
  planEditTaskEdit,
  planMergeTasksEdit,
  planReorderEdit,
  planSplitTaskEdit,
  sendPlanEdit,
} from "./planEditSend";

const JOB_ID = "0123456789abcdef";
const TOKEN = "token-abc";
const NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: TOKEN };

function bodyOf(request: DecisionSendRequest | null): Record<string, unknown> {
  return JSON.parse(request!.body);
}

describe("the six edits", () => {
  it("are the door's six command ids in the feature file's order", () => {
    expect(PLAN_EDIT_COMMANDS).toEqual([
      "job.plan-edit-task", "job.plan-delete-task", "job.plan-reorder", "job.plan-merge-tasks",
      "job.plan-split-task", "job.plan-edit-acceptance",
    ]);
  });

  it("each carries the backend's own argument object", () => {
    expect(planEditTaskEdit("T2", { title: "Parse" })).toEqual(
      { command: "job.plan-edit-task", args: { task_id: "T2", fields: { title: "Parse" } } });
    expect(planDeleteTaskEdit("T2")).toEqual({ command: "job.plan-delete-task", args: { task_id: "T2" } });
    expect(planReorderEdit(["T2", "T1"])).toEqual({ command: "job.plan-reorder", args: { order: ["T2", "T1"] } });
    expect(planMergeTasksEdit(["T1", "T3"])).toEqual(
      { command: "job.plan-merge-tasks", args: { task_ids: ["T1", "T3"] } });
    expect(planSplitTaskEdit("T2", [[0, 2], [1]])).toEqual(
      { command: "job.plan-split-task", args: { task_id: "T2", partition: [[0, 2], [1]] } });
  });

  it("an acceptance edit leaves out the index it has not got and the text a remove takes none of", () => {
    expect(planEditAcceptanceEdit("T2", "add", null, "is fast").args).toEqual({ task_id: "T2", op: "add", text: "is fast" });
    expect(planEditAcceptanceEdit("T2", "add", 0, "is fast").args).toEqual(
      { task_id: "T2", op: "add", index: 0, text: "is fast" });
    expect(planEditAcceptanceEdit("T2", "edit", 1, "reads").args).toEqual(
      { task_id: "T2", op: "edit", index: 1, text: "reads" });
    expect(planEditAcceptanceEdit("T2", "remove", 2, "ignored").args).toEqual({ task_id: "T2", op: "remove", index: 2 });
  });

  it("copies its lists, so a later change to the caller's array changes no edit", () => {
    const order = ["T1", "T2"];
    const edit = planReorderEdit(order);
    order.push("T3");
    expect(edit.args.order).toEqual(["T1", "T2"]);
  });
});

describe("buildPlanEditRequest", () => {
  it("builds the exact request, with the version shown as expected_version", () => {
    expect(buildPlanEditRequest(TARGET, planDeleteTaskEdit("T2"), 3, NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: { Authorization: `Bearer ${TOKEN}`, "X-Remedy-CSRF": TOKEN, "Content-Type": "application/json" },
      body: JSON.stringify({
        command: "job.plan-delete-task", client_nonce: NONCE, args: { task_id: "T2", expected_version: 3 } }),
    });
  });

  it("puts expected_version beside every edit's own arguments", () => {
    const body = bodyOf(buildPlanEditRequest(TARGET, planEditTaskEdit("T1", { goal: "g" }), 7, NONCE));
    expect(body.args).toEqual({ task_id: "T1", fields: { goal: "g" }, expected_version: 7 });
  });

  it.each([
    ["no job id", { ...TARGET, jobId: "" }, 1, NONCE],
    ["no token", { ...TARGET, serverToken: "" }, 1, NONCE],
    ["a bad nonce", TARGET, 1, "../x"],
    ["version 0", TARGET, 0, NONCE],
    ["a fractional version", TARGET, 1.5, NONCE],
  ])("is null for %s", (_label, target, version, nonce) => {
    expect(buildPlanEditRequest(target, planDeleteTaskEdit("T2"), version, nonce)).toBeNull();
  });

  it("is null for a command that is not one of the six", () => {
    const edit = { command: "job.stop", args: {} } as unknown as ReturnType<typeof planDeleteTaskEdit>;
    expect(buildPlanEditRequest(TARGET, edit, 1, NONCE)).toBeNull();
  });
});

describe("describePlanEditResult", () => {
  const refused = (status: number, body: Record<string, unknown> | null): TaskEditSubmitResult =>
    ({ outcome: "refused", status, body });

  it("an accepted edit names the plan's new version", () => {
    expect(describePlanEditResult({ outcome: "accepted", status: 200, body: { version: 4, outcome: "accepted" } }))
      .toEqual({ message: { tone: "ok", sentence: "Saved as version 4." }, version: 4 });
  });

  it("an accepted answer with no version says so and carries none", () => {
    expect(describePlanEditResult({ outcome: "accepted", status: 200, body: null }))
      .toEqual({ message: { tone: "ok", sentence: "Saved as version ?." }, version: null });
  });

  it("a stale version, a 409 with only current_version, asks to look again", () => {
    expect(describePlanEditResult(refused(409, { error: "x", current_version: 5 })).message).toEqual({
      tone: "error", sentence: "Not saved: the plan changed since you opened it. Look at it again and redo the edit." });
  });

  it("a plan that fails revalidation says the reason, though it carries current_version too", () => {
    expect(describePlanEditResult(refused(409, { error: "x", detail: "the plan has a cycle", current_version: 2 })).message)
      .toEqual({ tone: "error", sentence: "Not saved: the plan has a cycle." });
  });

  it("a closed plan says the reason", () => {
    expect(describePlanEditResult(refused(409, { error: "x", detail: "the plan is approved" })).message)
      .toEqual({ tone: "error", sentence: "Not saved: the plan is approved." });
  });

  it("an edit the plan cannot take, a 400 on args, says the reason", () => {
    expect(describePlanEditResult(refused(400, { error: "x", field: "args", detail: "the edit changes nothing" })).message)
      .toEqual({ tone: "error", sentence: "Not saved: the edit changes nothing." });
  });

  it.each([
    ["a 400 on another field", refused(400, { error: "x", field: "expected_version" })],
    ["a 409 with neither", refused(409, { error: "x" })],
    ["a 403", refused(403, null)],
    ["a 429", refused(429, null)],
    ["a 500", refused(500, { error: "x", detail: "hidden" })],
    ["no answer", { outcome: "unreachable", status: 0, body: null } as TaskEditSubmitResult],
  ])("%s is worded as the pause door words it", (_label, result) => {
    expect(describePlanEditResult(result)).toEqual({ message: describePauseSendResult(result), version: null });
  });
});

describe("sendPlanEdit", () => {
  it("sends one request against the version shown and reports the version it landed as", async () => {
    const sent: DecisionSendRequest[] = [];
    const outcome = await sendPlanEdit(TARGET, planDeleteTaskEdit("T2"), 3, {
      mintNonce: () => NONCE,
      submit: async (request) => { sent.push(request); return { outcome: "accepted", status: 200, body: { version: 4 } }; },
      deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(bodyOf(sent[0]).args).toEqual({ task_id: "T2", expected_version: 3 });
    expect(outcome).toEqual({ message: { tone: "ok", sentence: "Saved as version 4." }, version: 4 });
  });

  it("touches no network when no nonce can be minted or the request is unsendable", async () => {
    let calls = 0;
    const submit = async () => { calls += 1; return { outcome: "accepted", status: 200, body: null } as TaskEditSubmitResult; };
    const unsendable = { message: { tone: "warn", sentence: "This edit cannot be sent as it stands." }, version: null };
    expect(await sendPlanEdit(TARGET, planDeleteTaskEdit("T2"), 3, { mintNonce: () => null, submit })).toEqual(unsendable);
    expect(await sendPlanEdit(TARGET, planDeleteTaskEdit("T2"), 0, { mintNonce: () => NONCE, submit })).toEqual(unsendable);
    expect(calls).toBe(0);
  });

  it("a send that never answers before the deadline, or that throws, is unreachable", async () => {
    const unreachable = describePlanEditResult({ outcome: "unreachable", status: 0, body: null });
    expect(await sendPlanEdit(TARGET, planDeleteTaskEdit("T2"), 3, {
      mintNonce: () => NONCE, submit: () => new Promise(() => {}), deadline: () => Promise.resolve(),
    })).toEqual(unreachable);
    expect(await sendPlanEdit(TARGET, planDeleteTaskEdit("T2"), 3, {
      mintNonce: () => NONCE, submit: () => Promise.reject(new Error("down")), deadline: () => new Promise(() => {}),
    })).toEqual(unreachable);
  });
});
