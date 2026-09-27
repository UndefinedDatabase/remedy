import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import type { DecisionSubmitResult } from "./decisionSubmit";
import {
  STEERING_ENDED_STATES,
  STEERING_MAX_CHARS,
  STEER_TASK_COMMAND,
  buildChatSendRequest,
  buildSteerTaskRequest,
  describeChatSendResult,
  describeSteerTaskResult,
  describeUnsendableChatMessage,
  normalizeSteeringMessage,
  sendSteeringMessage,
  sendSteeringNote,
  steeringIsOpen,
} from "./steeringSend";
import type { SteerTaskSubmitResult } from "./steeringSend";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: SERVER_TOKEN };
const TASK_ID = "task-1";

/** A submit that records every request it was handed and answers `result`. */
function recordingSubmit(result: DecisionSubmitResult) {
  const sent: DecisionSendRequest[] = [];
  const submit = (request: DecisionSendRequest) => {
    sent.push(request);
    return Promise.resolve(result);
  };
  return { sent, submit };
}

/** `recordingSubmit`'s own shape, over a `SteerTaskSubmitResult` — the body the
 *  task-addressed submit reads back that the job-wide one does not. */
function recordingSteerSubmit(result: SteerTaskSubmitResult) {
  const sent: DecisionSendRequest[] = [];
  const submit = (request: DecisionSendRequest) => {
    sent.push(request);
    return Promise.resolve(result);
  };
  return { sent, submit };
}

const neverSettles = () => new Promise<DecisionSubmitResult>(() => {});
const neverSettlesSteer = () => new Promise<SteerTaskSubmitResult>(() => {});
const settledDeadline = () => Promise.resolve();
const pendingDeadline = () => new Promise<void>(() => {});

describe("normalizeSteeringMessage", () => {
  it("trims the message", () => {
    expect(normalizeSteeringMessage("  Keep it small.  ")).toBe("Keep it small.");
  });

  it("refuses a message that is empty, blank or carries a NUL", () => {
    expect(normalizeSteeringMessage("")).toBeNull();
    expect(normalizeSteeringMessage("   \n ")).toBeNull();
    expect(normalizeSteeringMessage("a\u0000b")).toBeNull();
  });

  it("takes the limit exactly and refuses one character past it", () => {
    expect(normalizeSteeringMessage("x".repeat(STEERING_MAX_CHARS))).not.toBeNull();
    expect(normalizeSteeringMessage("x".repeat(STEERING_MAX_CHARS + 1))).toBeNull();
  });

  it("counts an emoji as one character, as the server does", () => {
    const atLimit = "😀".repeat(STEERING_MAX_CHARS);
    expect(normalizeSteeringMessage(atLimit)).toBe(atLimit);
  });
});

describe("steeringIsOpen", () => {
  it("closes for every ended state and only for those", () => {
    for (const state of STEERING_ENDED_STATES) {
      expect(steeringIsOpen(state)).toBe(false);
    }
    for (const state of ["running", "paused", "stopped", "planned", "blocked", "unknown", ""]) {
      expect(steeringIsOpen(state)).toBe(true);
    }
  });

  it("ignores case and surrounding space", () => {
    expect(steeringIsOpen(" Completed ")).toBe(false);
  });
});

describe("buildChatSendRequest", () => {
  it("builds the exact request the door accepts", () => {
    expect(buildChatSendRequest(TARGET, "  Use pnpm.  ", GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: "chat.send",
        client_nonce: GOOD_NONCE,
        args: { message: "Use pnpm." },
      }),
    });
  });

  it("answers null for a missing job, token, message or usable nonce", () => {
    expect(buildChatSendRequest({ ...TARGET, jobId: "" }, "Hi.", GOOD_NONCE)).toBeNull();
    expect(buildChatSendRequest({ ...TARGET, serverToken: "" }, "Hi.", GOOD_NONCE)).toBeNull();
    expect(buildChatSendRequest(TARGET, "   ", GOOD_NONCE)).toBeNull();
    expect(buildChatSendRequest(TARGET, "Hi.", "not a nonce")).toBeNull();
  });

  it("never puts the token in the path", () => {
    const request = buildChatSendRequest(TARGET, "Hi.", GOOD_NONCE);
    expect(request?.path.includes(SERVER_TOKEN)).toBe(false);
  });
});

describe("describeChatSendResult", () => {
  it("maps each answer the door gives to its tone", () => {
    const tones = [
      [{ outcome: "accepted", status: 200 }, "ok"],
      [{ outcome: "unreachable", status: 0 }, "warn"],
      [{ outcome: "refused", status: 400 }, "error"],
      [{ outcome: "refused", status: 403 }, "error"],
      [{ outcome: "refused", status: 409 }, "error"],
      [{ outcome: "refused", status: 429 }, "warn"],
      [{ outcome: "refused", status: 500 }, "warn"],
      [{ outcome: "refused", status: 418 }, "error"],
    ] as const;
    for (const [result, tone] of tones) {
      expect(describeChatSendResult(result).tone).toBe(tone);
    }
  });

  it("says an ended job did not record the message", () => {
    expect(describeChatSendResult({ outcome: "refused", status: 409 }).sentence)
      .toContain("has ended");
  });

  it("names no status number, header or path in any sentence", () => {
    const statuses = [0, 200, 400, 403, 409, 429, 500, 418];
    const sentences = statuses.map((status) => describeChatSendResult({
      outcome: status === 200 ? "accepted" : status === 0 ? "unreachable" : "refused", status,
    }).sentence).concat(describeUnsendableChatMessage().sentence);
    for (const sentence of sentences) {
      expect(sentence).not.toMatch(/\b(200|400|403|409|429|500|418)\b|X-Remedy|\/api\//);
    }
  });

  it("answers a fresh object every call", () => {
    const result: DecisionSubmitResult = { outcome: "accepted", status: 200 };
    expect(describeChatSendResult(result)).not.toBe(describeChatSendResult(result));
  });
});

describe("sendSteeringMessage", () => {
  it("sends exactly once and reports acceptance", async () => {
    const { sent, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const answer = await sendSteeringMessage(TARGET, "Keep it small.", {
      mintNonce: () => GOOD_NONCE, submit, deadline: pendingDeadline,
    });
    expect(sent).toHaveLength(1);
    expect(JSON.parse(sent[0].body).args.message).toBe("Keep it small.");
    expect(answer.tone).toBe("ok");
  });

  it("never reaches the network for an unsendable message or a failed nonce", async () => {
    const { sent, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const blank = await sendSteeringMessage(TARGET, "   ", {
      mintNonce: () => GOOD_NONCE, submit, deadline: pendingDeadline,
    });
    const noNonce = await sendSteeringMessage(TARGET, "Hi.", {
      mintNonce: () => null, submit, deadline: pendingDeadline,
    });
    expect(sent).toHaveLength(0);
    expect(blank).toEqual(describeUnsendableChatMessage());
    expect(noNonce).toEqual(describeUnsendableChatMessage());
  });

  it("answers unreachable when the deadline wins", async () => {
    const answer = await sendSteeringMessage(TARGET, "Hi.", {
      mintNonce: () => GOOD_NONCE, submit: neverSettles, deadline: settledDeadline,
    });
    expect(answer).toEqual(describeChatSendResult({ outcome: "unreachable", status: 0 }));
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const answer = await sendSteeringMessage(TARGET, "Hi.", {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: pendingDeadline,
    });
    expect(answer.tone).toBe("warn");
  });
});

describe("buildSteerTaskRequest", () => {
  it("builds the exact request the door accepts", () => {
    expect(buildSteerTaskRequest(TARGET, TASK_ID, "  Use pnpm.  ", GOOD_NONCE)).toEqual({
      path: `/api/jobs/${JOB_ID}/commands`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${SERVER_TOKEN}`,
        "X-Remedy-CSRF": SERVER_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: STEER_TASK_COMMAND,
        client_nonce: GOOD_NONCE,
        args: { task_id: TASK_ID, message: "Use pnpm." },
      }),
    });
  });

  it("names the write door's own command id", () => {
    expect(STEER_TASK_COMMAND).toBe("job.steer");
  });

  it("answers null for an empty task id, an unsendable message or an unusable nonce", () => {
    expect(buildSteerTaskRequest(TARGET, "", "Hi.", GOOD_NONCE)).toBeNull();
    expect(buildSteerTaskRequest(TARGET, TASK_ID, "   ", GOOD_NONCE)).toBeNull();
    expect(buildSteerTaskRequest(TARGET, TASK_ID, "Hi.", "not a nonce")).toBeNull();
  });

  it("normalises the message the same way buildChatSendRequest does", () => {
    const atLimit = "x".repeat(STEERING_MAX_CHARS);
    expect(buildSteerTaskRequest(TARGET, TASK_ID, atLimit, GOOD_NONCE)).not.toBeNull();
    expect(buildSteerTaskRequest(TARGET, TASK_ID, atLimit + "x", GOOD_NONCE)).toBeNull();
  });
});

describe("describeSteerTaskResult", () => {
  it("names the task by id on acceptance", () => {
    const message = describeSteerTaskResult({ outcome: "accepted", status: 200, body: null }, TASK_ID);
    expect(message.tone).toBe("ok");
    expect(message.sentence).toBe(
      `Your note was recorded. Task ${TASK_ID} reads it at the start of its next round.`);
  });

  it("names each of the three 409 codes in plain words", () => {
    const cases: [string, string][] = [
      ["job_not_steerable", "already finished"],
      ["task_not_steerable", "no longer be steered"],
      ["unknown_task", "no such task"],
    ];
    for (const [code, phrase] of cases) {
      const message = describeSteerTaskResult(
        { outcome: "refused", status: 409, body: { error: `${code}: some detail` } }, TASK_ID);
      expect(message.sentence).toContain(phrase);
    }
  });

  it("echoes an unrecognised 409 code's raw string", () => {
    const message = describeSteerTaskResult(
      { outcome: "refused", status: 409, body: { error: "something_else: detail" } }, TASK_ID);
    expect(message.sentence).toContain("something_else: detail");
  });

  it("falls back to describeChatSendResult's own 409 sentence with no body", () => {
    const message = describeSteerTaskResult({ outcome: "refused", status: 409, body: null }, TASK_ID);
    expect(message).toEqual(describeChatSendResult({ outcome: "refused", status: 409 }));
  });

  it("reuses describeChatSendResult's sentences for 400, 403, 429 and 500", () => {
    for (const status of [400, 403, 429, 500]) {
      const message = describeSteerTaskResult({ outcome: "refused", status, body: null }, TASK_ID);
      expect(message).toEqual(describeChatSendResult({ outcome: "refused", status }));
    }
  });

  it("reuses describeChatSendResult's unreachable sentence", () => {
    const message = describeSteerTaskResult({ outcome: "unreachable", status: 0, body: null }, TASK_ID);
    expect(message).toEqual(describeChatSendResult({ outcome: "unreachable", status: 0 }));
  });
});

describe("sendSteeringNote", () => {
  it("sends exactly once, addressed to the task, and reports acceptance", async () => {
    const { sent, submit } = recordingSteerSubmit({ outcome: "accepted", status: 200, body: null });
    const answer = await sendSteeringNote(TARGET, TASK_ID, "Keep it small.", {
      mintNonce: () => GOOD_NONCE, submit, deadline: pendingDeadline,
    });
    expect(sent).toHaveLength(1);
    const body = JSON.parse(sent[0].body);
    expect(body.command).toBe(STEER_TASK_COMMAND);
    expect(body.args).toEqual({ task_id: TASK_ID, message: "Keep it small." });
    expect(answer.tone).toBe("ok");
  });

  it("never reaches the network for an unsendable message, an empty task or a failed nonce", async () => {
    const { sent, submit } = recordingSteerSubmit({ outcome: "accepted", status: 200, body: null });
    const blank = await sendSteeringNote(TARGET, TASK_ID, "   ", {
      mintNonce: () => GOOD_NONCE, submit, deadline: pendingDeadline,
    });
    const noTask = await sendSteeringNote(TARGET, "", "Hi.", {
      mintNonce: () => GOOD_NONCE, submit, deadline: pendingDeadline,
    });
    const noNonce = await sendSteeringNote(TARGET, TASK_ID, "Hi.", {
      mintNonce: () => null, submit, deadline: pendingDeadline,
    });
    expect(sent).toHaveLength(0);
    expect(blank).toEqual(describeUnsendableChatMessage());
    expect(noTask).toEqual(describeUnsendableChatMessage());
    expect(noNonce).toEqual(describeUnsendableChatMessage());
  });

  it("answers unreachable when the deadline wins", async () => {
    const answer = await sendSteeringNote(TARGET, TASK_ID, "Hi.", {
      mintNonce: () => GOOD_NONCE, submit: neverSettlesSteer, deadline: settledDeadline,
    });
    expect(answer).toEqual(describeChatSendResult({ outcome: "unreachable", status: 0 }));
  });

  it("answers unreachable when an injected submit rejects", async () => {
    const answer = await sendSteeringNote(TARGET, TASK_ID, "Hi.", {
      mintNonce: () => GOOD_NONCE,
      submit: () => Promise.reject(new Error("offline")),
      deadline: pendingDeadline,
    });
    expect(answer.tone).toBe("warn");
  });
});
