import { describe, expect, it } from "vitest";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { PauseSubmitResult } from "./pauseSend";
import {
  JOB_PREVIEW_START_COMMAND_ID,
  JOB_PREVIEW_STOP_COMMAND_ID,
  buildPreviewSendRequest,
  describePreviewSendResult,
  sendPreviewCommand,
} from "./previewSend";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET: DecisionSendTarget = { jobId: JOB_ID, serverToken: SERVER_TOKEN };

describe("buildPreviewSendRequest", () => {
  it("builds the start request with empty args", () => {
    expect(buildPreviewSendRequest(TARGET, JOB_PREVIEW_START_COMMAND_ID, GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: JOB_PREVIEW_START_COMMAND_ID,
        client_nonce: GOOD_NONCE,
        args: {},
      }),
    });
  });

  it("builds the stop request with empty args", () => {
    const request = buildPreviewSendRequest(TARGET, JOB_PREVIEW_STOP_COMMAND_ID, GOOD_NONCE);
    expect(JSON.parse(request!.body)).toEqual({
      command: JOB_PREVIEW_STOP_COMMAND_ID,
      client_nonce: GOOD_NONCE,
      args: {},
    });
  });

  it("answers null for a missing job, a missing token or an unusable nonce", () => {
    expect(buildPreviewSendRequest({ ...TARGET, jobId: "" }, JOB_PREVIEW_START_COMMAND_ID, GOOD_NONCE)).toBeNull();
    expect(buildPreviewSendRequest({ ...TARGET, serverToken: "" }, JOB_PREVIEW_START_COMMAND_ID, GOOD_NONCE)).toBeNull();
    expect(buildPreviewSendRequest(TARGET, JOB_PREVIEW_START_COMMAND_ID, "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildPreviewSendRequest(TARGET, JOB_PREVIEW_START_COMMAND_ID, GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("describePreviewSendResult", () => {
  function accepted(body: Record<string, unknown> | null): PauseSubmitResult {
    return { outcome: "accepted", status: 200, body };
  }

  it("names starting the app for an accepted start", () => {
    const message = describePreviewSendResult(JOB_PREVIEW_START_COMMAND_ID, accepted({ outcome: "accepted", state: "starting" }));
    expect(message).toEqual({ tone: "ok", sentence: "Starting the app. The link appears once the app answers." });
  });

  it("names stopping the app for an accepted stop", () => {
    const message = describePreviewSendResult(JOB_PREVIEW_STOP_COMMAND_ID, accepted({ outcome: "accepted", state: "stopped" }));
    expect(message).toEqual({ tone: "ok", sentence: "Stopping the app." });
  });

  it("answers the unrecognised-outcome sentence for any other body, for both commands", () => {
    const expected = { tone: "warn", sentence: "The job answered, but not in a way this page understands." };
    expect(describePreviewSendResult(JOB_PREVIEW_START_COMMAND_ID, accepted({ outcome: "something_else" }))).toEqual(expected);
    expect(describePreviewSendResult(JOB_PREVIEW_STOP_COMMAND_ID, accepted(null))).toEqual(expected);
  });

  it("maps every refusal status to its own sentence and describeChatSendResult's own tone, for both commands", () => {
    const cases: [number, string, string][] = [
      [400, "error", "This request could not be read, so the app was neither started nor stopped."],
      [403, "error", "This dashboard was not allowed to start or stop the app. Open the dashboard again from a fresh link."],
      [429, "warn", "Too many requests arrived at once. Wait a moment, then try again."],
      [500, "warn", "The job could not record this request. Try again in a moment."],
      [418, "error", "The job refused this request, so nothing was recorded."],
    ];
    for (const [status, tone, sentence] of cases) {
      const result: PauseSubmitResult = { outcome: "refused", status, body: null };
      expect(describePreviewSendResult(JOB_PREVIEW_START_COMMAND_ID, result)).toEqual({ tone, sentence });
      expect(describePreviewSendResult(JOB_PREVIEW_STOP_COMMAND_ID, result)).toEqual({ tone, sentence });
    }
  });

  it("reuses steering's own unreachable sentence and tone, for both commands", () => {
    const result: PauseSubmitResult = { outcome: "unreachable", status: 0, body: null };
    const message = describePreviewSendResult(JOB_PREVIEW_START_COMMAND_ID, result);
    expect(message.tone).toBe("warn");
    expect(message.sentence).toContain("No answer came back");
    expect(describePreviewSendResult(JOB_PREVIEW_STOP_COMMAND_ID, result)).toEqual(message);
  });

  it("answers a fresh object every call", () => {
    const result = accepted({ outcome: "accepted" });
    expect(describePreviewSendResult(JOB_PREVIEW_START_COMMAND_ID, result))
      .not.toBe(describePreviewSendResult(JOB_PREVIEW_START_COMMAND_ID, result));
  });
});

describe("sendPreviewCommand", () => {
  it("sends exactly once and reports the door's answer", async () => {
    const sent: DecisionSendRequest[] = [];
    const submit = (request: DecisionSendRequest) => {
      sent.push(request);
      return Promise.resolve({ outcome: "accepted", status: 200, body: { outcome: "accepted" } } as PauseSubmitResult);
    };
    const answer = await sendPreviewCommand(TARGET, JOB_PREVIEW_START_COMMAND_ID, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(sent).toHaveLength(1);
    expect(sent[0].body).toBe(JSON.stringify({ command: JOB_PREVIEW_START_COMMAND_ID, client_nonce: GOOD_NONCE, args: {} }));
    expect(answer.sentence).toContain("Starting the app");
  });

  it("never reaches the network when no nonce can be minted", async () => {
    const submit = () => Promise.resolve({ outcome: "accepted", status: 200, body: null } as PauseSubmitResult);
    const answer = await sendPreviewCommand(TARGET, JOB_PREVIEW_START_COMMAND_ID, {
      mintNonce: () => null, submit, deadline: () => new Promise(() => {}),
    });
    expect(answer).toEqual({ tone: "warn", sentence: "This action cannot be sent as the page stands." });
  });

  it("never reaches the network when the builder refuses the request", async () => {
    let called = false;
    const submit = () => {
      called = true;
      return Promise.resolve({ outcome: "accepted", status: 200, body: null } as PauseSubmitResult);
    };
    const answer = await sendPreviewCommand({ jobId: "", serverToken: SERVER_TOKEN }, JOB_PREVIEW_START_COMMAND_ID, {
      mintNonce: () => GOOD_NONCE, submit, deadline: () => new Promise(() => {}),
    });
    expect(called).toBe(false);
    expect(answer).toEqual({ tone: "warn", sentence: "This action cannot be sent as the page stands." });
  });

  it("answers unreachable when the deadline wins", async () => {
    const answer = await sendPreviewCommand(TARGET, JOB_PREVIEW_STOP_COMMAND_ID, {
      mintNonce: () => GOOD_NONCE,
      submit: () => new Promise(() => {}),
      deadline: () => Promise.resolve(),
    });
    expect(answer.sentence).toContain("No answer came back");
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const answer = await sendPreviewCommand(TARGET, JOB_PREVIEW_START_COMMAND_ID, {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: () => new Promise(() => {}),
    });
    expect(answer.tone).toBe("warn");
    expect(answer.sentence).toContain("No answer came back");
  });
});
