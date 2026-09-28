import { describe, expect, it } from "vitest";
import type { DecisionSendRequest } from "./decisionSend";
import type { DecisionSubmitResult } from "./decisionSubmit";
import {
  CHAT_NOT_IN_EVIDENCE,
  buildChatCardSendRequest,
  chatEvidenceTab,
  chatScopeLabel,
  chatSentenceMark,
  chatSentenceText,
  chatTurnPath,
  decodeChatTurn,
  describeChatCardResult,
  describeUnsendableChatCard,
  sendChatCard,
} from "./chatTurn";
import type { ChatAnswerSentenceView, ChatAnswerView, ChatCardView } from "./chatTurn";

const JOB_ID = "0123456789abcdef";
const SERVER_TOKEN = "token-abc";
const GOOD_NONCE = "ui-a1b2c3d4";
const TARGET = { jobId: JOB_ID, serverToken: SERVER_TOKEN };

/** A submit that records every request it was handed and answers `result`, exactly the shape
 *  `steeringSend.test.ts`'s own `recordingSubmit` takes: a counting stub without `vi.fn`. */
function recordingSubmit(result: DecisionSubmitResult) {
  const sent: DecisionSendRequest[] = [];
  const submit = (request: DecisionSendRequest) => {
    sent.push(request);
    return Promise.resolve(result);
  };
  return { sent, submit };
}

function sentence(fields: Partial<ChatAnswerSentenceView> = {}): ChatAnswerSentenceView {
  return { text: "Tests passed [1].", citations: [1], supported: true, problem: "", ...fields };
}

const RAW_ANSWER = {
  available: true,
  kind: "answer",
  scope: "node",
  subject: "task-1",
  question: "Did the tests pass?",
  generator: "mechanical",
  sentences: [
    { text: "Tests passed [1].", citations: [1], supported: true, problem: "" },
  ],
  evidence: [
    { number: 1, kind: "node", ref: "task-1", text: "Task task-1: Write the README" },
  ],
  omitted: 0,
};

const RAW_CARD = {
  available: true,
  kind: "card",
  verb: "job.pause",
  title: "Pause the job",
  lines: ["Job: job-1", "Command: job.pause"],
  args: {},
  missing: [],
  confirmable: true,
};

describe("decodeChatTurn", () => {
  it("reads an answer", () => {
    expect(decodeChatTurn(RAW_ANSWER)).toEqual({
      kind: "answer",
      scope: "node",
      subject: "task-1",
      question: "Did the tests pass?",
      generator: "mechanical",
      sentences: [{ text: "Tests passed [1].", citations: [1], supported: true, problem: "" }],
      evidence: [{ number: 1, kind: "node", ref: "task-1", text: "Task task-1: Write the README" }],
      omitted: 0,
    });
  });

  it("reads a card exactly", () => {
    expect(decodeChatTurn(RAW_CARD)).toEqual({
      kind: "card",
      verb: "job.pause",
      title: "Pause the job",
      lines: ["Job: job-1", "Command: job.pause"],
      args: {},
      missing: [],
      confirmable: true,
    });
  });

  it("reads an unavailable turn", () => {
    expect(decodeChatTurn({ available: false, reason: "empty_text" }))
      .toEqual({ kind: "unavailable", reason: "empty_text" });
  });

  it("refuses a citation beyond the evidence", () => {
    const raw = { ...RAW_ANSWER, sentences: [{ text: "x [2].", citations: [2], supported: true, problem: "" }] };
    expect(decodeChatTurn(raw)).toBeNull();
  });

  it("refuses a misnumbered evidence item", () => {
    const raw = { ...RAW_ANSWER, evidence: [{ number: 2, kind: "node", ref: "task-1", text: "x" }] };
    expect(decodeChatTurn(raw)).toBeNull();
  });
});

describe("chatTurnPath", () => {
  it("quotes the text and omits the task for the project", () => {
    expect(chatTurnPath({ jobId: JOB_ID, token: SERVER_TOKEN, text: "a b?", taskId: "" }))
      .toBe(`/api/jobs/${JOB_ID}/chat?token=${SERVER_TOKEN}&text=a%20b%3F`);
  });

  it("carries the task when it names one", () => {
    expect(chatTurnPath({ jobId: JOB_ID, token: SERVER_TOKEN, text: "hi", taskId: "task-1" }))
      .toBe(`/api/jobs/${JOB_ID}/chat?token=${SERVER_TOKEN}&text=hi&task=task-1`);
  });
});

describe("chatSentenceText", () => {
  it("drops [1]", () => {
    expect(chatSentenceText(sentence({ text: "Tests passed [1]." }))).toBe("Tests passed.");
  });

  it("drops [1][2]", () => {
    expect(chatSentenceText(sentence({ text: "Two items [1][2]." }))).toBe("Two items.");
  });
});

describe("chatSentenceMark", () => {
  it("reads cited", () => {
    expect(chatSentenceMark(sentence({ supported: true, citations: [1] }))).toBe("cited");
  });

  it("reads unsupported without a citation", () => {
    expect(chatSentenceMark(sentence({ supported: false, citations: [] }))).toBe("unsupported");
  });

  it("reads unsupported WITH a citation", () => {
    expect(chatSentenceMark(sentence({ supported: false, citations: [1] }))).toBe("unsupported");
  });

  it("reads absence", () => {
    expect(chatSentenceMark(sentence({ supported: true, citations: [], text: CHAT_NOT_IN_EVIDENCE })))
      .toBe("absence");
  });
});

function answerView(fields: Partial<ChatAnswerView> = {}): ChatAnswerView {
  return {
    kind: "answer", scope: "node", subject: "task-1", question: "q", generator: "mechanical",
    sentences: [sentence()], evidence: [], omitted: 0, ...fields,
  };
}

describe("chatScopeLabel", () => {
  it("names the task, the project, or that none is registered", () => {
    expect(chatScopeLabel(answerView({ scope: "node", subject: "task-1" }))).toBe("About task task-1");
    expect(chatScopeLabel(answerView({ scope: "project", subject: "proj-1" })))
      .toBe("About project proj-1");
    expect(chatScopeLabel(answerView({ scope: "project", subject: "" })))
      .toBe("No project is registered for this job.");
  });
});

describe("chatEvidenceTab", () => {
  it("maps a diff item to diff and a prompt item to prompt, else null", () => {
    expect(chatEvidenceTab("diff")).toBe("diff");
    expect(chatEvidenceTab("prompt")).toBe("prompt");
    expect(chatEvidenceTab("node")).toBeNull();
  });
});

describe("buildChatCardSendRequest", () => {
  const completeCard: ChatCardView = {
    kind: "card", verb: "job.steer", title: "Send a note to the task's builder",
    lines: ["Job: job-1", "Task: task-1", "Message: use tabs"],
    args: { task_id: "task-1", message: "use tabs" }, missing: [], confirmable: true,
  };

  it("builds the request's path and whole parsed body", () => {
    const request = buildChatCardSendRequest(TARGET, completeCard, GOOD_NONCE);
    expect(request?.path).toBe(`/api/jobs/${JOB_ID}/commands`);
    expect(request?.method).toBe("POST");
    expect(request?.headers).toEqual({
      Authorization: `Bearer ${SERVER_TOKEN}`,
      "X-Remedy-CSRF": SERVER_TOKEN,
      "Content-Type": "application/json",
    });
    expect(JSON.parse(request?.body ?? "")).toEqual({
      command: "job.steer", client_nonce: GOOD_NONCE,
      args: { task_id: "task-1", message: "use tabs" },
    });
  });

  it("refuses a card that is not confirmable, has a missing entry, an empty verb, or an unusable nonce", () => {
    expect(buildChatCardSendRequest(TARGET, { ...completeCard, confirmable: false }, GOOD_NONCE)).toBeNull();
    expect(buildChatCardSendRequest(TARGET, { ...completeCard, missing: ["message"] }, GOOD_NONCE)).toBeNull();
    expect(buildChatCardSendRequest(TARGET, { ...completeCard, verb: "" }, GOOD_NONCE)).toBeNull();
    expect(buildChatCardSendRequest(TARGET, completeCard, "bad nonce")).toBeNull();
    expect(buildChatCardSendRequest({ jobId: "", serverToken: SERVER_TOKEN }, completeCard, GOOD_NONCE)).toBeNull();
    expect(buildChatCardSendRequest({ jobId: JOB_ID, serverToken: "" }, completeCard, GOOD_NONCE)).toBeNull();
  });
});

describe("describeChatCardResult", () => {
  it("names the verb on acceptance and composes the refusal vocabulary otherwise", () => {
    expect(describeChatCardResult({ outcome: "accepted", status: 200 }, "job.pause"))
      .toEqual({ tone: "ok", sentence: "Sent: job.pause." });
    expect(describeChatCardResult({ outcome: "unreachable", status: 0 }, "job.pause").tone).toBe("warn");
  });
});

describe("sendChatCard", () => {
  const incompleteCard: ChatCardView = {
    kind: "card", verb: "job.steer", title: "Send a note",
    lines: ["Needs: message."], args: {}, missing: ["message"], confirmable: false,
  };
  const completeCard: ChatCardView = {
    kind: "card", verb: "job.pause", title: "Pause the job",
    lines: ["Job: job-1", "Command: job.pause"], args: {}, missing: [], confirmable: true,
  };

  it("an incomplete card sends nothing", async () => {
    const { sent, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const outcome = await sendChatCard(TARGET, incompleteCard, { mintNonce: () => GOOD_NONCE, submit });
    expect(sent).toEqual([]);
    expect(outcome).toEqual(describeUnsendableChatCard());
  });

  it("a complete card sends once with the accepted sentence", async () => {
    const { sent, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const outcome = await sendChatCard(TARGET, completeCard, { mintNonce: () => GOOD_NONCE, submit });
    expect(sent.length).toBe(1);
    expect(outcome).toEqual({ tone: "ok", sentence: "Sent: job.pause." });
  });
});
