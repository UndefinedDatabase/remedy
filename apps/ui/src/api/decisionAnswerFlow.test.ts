import { describe, it, expect } from "vitest";
import { answerDecisionCard } from "./decisionAnswerFlow";
import type { DecisionAnswerFlowDeps } from "./decisionAnswerFlow";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { DecisionSubmitResult } from "./decisionSubmit";
import { buildDecisionCardModel } from "./decisionCard";
import type { DecisionCardModel, DecisionInboxEntry } from "./decisionCard";
import {
  describeDecisionSubmitResult,
  describeUnsendableDecisionAnswer,
} from "./decisionOutcome";

/** The per-run server token `RemedyApp` reads out of the URL, spelled so that no
 *  other part of the request could carry this value by accident. */
const SERVER_TOKEN = "srv-token-9f3c1a";

/** The job whose commands door this flow addresses. */
const JOB_ID = "job-42";

/** A nonce the server's character class accepts, for the tests that are about
 *  something other than minting. */
const GOOD_NONCE = "ui-a1b2c3d4";

/** The answer the operator chose in every test that gets as far as sending. */
const CHOSEN_ANSWER = "keep first";

/** The status `decisionSubmit.ts` fixes for "there was no response at all". */
const NO_RESPONSE_STATUS = 0;

function sendTarget(): DecisionSendTarget {
  return { jobId: JOB_ID, serverToken: SERVER_TOKEN };
}

/** The open card every test here answers, built through the shipped model
 *  builder rather than typed out, so these tests pin the SEAM between the model
 *  and the flow instead of a literal that could drift away from it. */
function openCard(): DecisionCardModel {
  const entry: DecisionInboxEntry = {
    id: "d-1",
    type: "task_decision",
    status: "open",
    safe_summary: "Two migrations claim the same table",
    payload: { options: ["keep first", "keep second"] },
  };
  return buildDecisionCardModel(entry);
}

/** A submit seam that RECORDS whether it was reached and answers a fixed
 *  result. The recorded list IS the "never touched the network" assertion, and
 *  no global is patched to obtain it. */
function recordingSubmit(result: DecisionSubmitResult) {
  const calls: DecisionSendRequest[] = [];
  const submit = async (request: DecisionSendRequest) => {
    calls.push(request);
    return result;
  };
  return { calls, submit };
}

/** A submit seam that NEVER SETTLES — the shape of a run that took the request
 *  and said nothing back. */
function neverSettlingSubmit() {
  const calls: DecisionSendRequest[] = [];
  const submit = async (request: DecisionSendRequest) => {
    calls.push(request);
    return new Promise<DecisionSubmitResult>(() => {});
  };
  return { calls, submit };
}

/** A deadline that is already over when it is asked. */
function deadlineNow(): Promise<void> {
  return Promise.resolve();
}

/** A deadline that never arrives, so the submit decides the outcome. */
function deadlineNever(): Promise<void> {
  return new Promise<void>(() => {});
}

/** A deadline seam that RECORDS whether it was asked at all. */
function recordingDeadline() {
  const asked: number[] = [];
  const deadline = () => {
    asked.push(asked.length);
    return deadlineNever();
  };
  return { asked, deadline };
}

/** The seams a test does not care about, so each test states only what it is
 *  about. Minting and building succeed; nothing settles by itself. */
function workingSeams(extra: DecisionAnswerFlowDeps = {}): DecisionAnswerFlowDeps {
  return {
    mintNonce: () => GOOD_NONCE,
    deadline: deadlineNever,
    ...extra,
  };
}

describe("answerDecisionCard", () => {
  it("says the answer was recorded when the door accepts", async () => {
    const { submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({ submit }),
    );
    expect(message).toEqual(
      describeDecisionSubmitResult({ outcome: "accepted", status: 200 }),
    );
  });

  it("carries a refusal's status into the sentence chooser, so a rate limit is not read as a credential problem", async () => {
    const { submit } = recordingSubmit({ outcome: "refused", status: 429 });
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({ submit }),
    );
    expect(message).toEqual(
      describeDecisionSubmitResult({ outcome: "refused", status: 429 }),
    );
    expect(message.tone).toBe("warn");
  });

  it("hands the submit the request the builder built, unchanged", async () => {
    const built: DecisionSendRequest = {
      path: "/api/jobs/job-42/commands",
      method: "POST",
      headers: { Authorization: "Bearer srv-token-9f3c1a" },
      body: "{}",
    };
    const { calls, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({ buildRequest: () => built, submit }),
    );
    expect(calls).toHaveLength(1);
    expect(calls[0]).toBe(built);
  });

  it("hands the builder the target, the card, the answer and the minted nonce, unchanged", async () => {
    const target = sendTarget();
    const model = openCard();
    const seen: unknown[][] = [];
    const { submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    await answerDecisionCard(
      target,
      model,
      CHOSEN_ANSWER,
      workingSeams({
        buildRequest: (
          builtTarget: DecisionSendTarget,
          builtModel: DecisionCardModel,
          answerText: string,
          clientNonce: string,
        ) => {
          seen.push([builtTarget, builtModel, answerText, clientNonce]);
          return { path: "/p", method: "POST", headers: {}, body: answerText };
        },
        submit,
      }),
    );
    expect(seen).toHaveLength(1);
    expect(seen[0]).toEqual([target, model, CHOSEN_ANSWER, GOOD_NONCE]);
    expect(seen[0][0]).toBe(target);
    expect(seen[0][1]).toBe(model);
  });

  it("stops at a nonce that cannot be minted and NEVER reaches the network", async () => {
    const { calls, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      { mintNonce: () => null, submit, deadline: deadlineNever },
    );
    expect(message).toEqual(describeUnsendableDecisionAnswer());
    expect(calls).toHaveLength(0);
  });

  it("stops at a request that cannot be built and NEVER reaches the network", async () => {
    const { calls, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({ buildRequest: () => null, submit }),
    );
    expect(message).toEqual(describeUnsendableDecisionAnswer());
    expect(calls).toHaveLength(0);
  });

  it("refuses a blank answer through the SHIPPED builder, one round trip before the door", async () => {
    const { calls, submit } = recordingSubmit({ outcome: "accepted", status: 200 });
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      "   ",
      workingSeams({ submit }),
    );
    expect(message).toEqual(describeUnsendableDecisionAnswer());
    expect(calls).toHaveLength(0);
  });

  it("never asks the deadline when nothing was sendable, because no wait was started", async () => {
    const { asked, deadline } = recordingDeadline();
    await answerDecisionCard(sendTarget(), openCard(), CHOSEN_ANSWER, {
      mintNonce: () => null,
      deadline,
    });
    expect(asked).toHaveLength(0);
  });

  it("still answers when the submit NEVER settles, because the deadline bounds the wait", async () => {
    const { calls, submit } = neverSettlingSubmit();
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({ submit, deadline: deadlineNow }),
    );
    expect(message).toEqual(
      describeDecisionSubmitResult({
        outcome: "unreachable",
        status: NO_RESPONSE_STATUS,
      }),
    );
    expect(calls).toHaveLength(1);
  });

  it("reuses the unreachable sentence when the deadline wins, rather than inventing a fourth outcome", async () => {
    const { submit } = neverSettlingSubmit();
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({ submit, deadline: deadlineNow }),
    );
    expect(message.tone).toBe("warn");
    expect(message.sentence).toBe(
      describeDecisionSubmitResult({
        outcome: "unreachable",
        status: NO_RESPONSE_STATUS,
      }).sentence,
    );
  });

  it("lets a submit that settles FIRST win the race, even though a deadline was started", async () => {
    const { asked, deadline } = recordingDeadline();
    const { submit } = recordingSubmit({ outcome: "refused", status: 409 });
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({ submit, deadline }),
    );
    expect(message).toEqual(
      describeDecisionSubmitResult({ outcome: "refused", status: 409 }),
    );
    expect(asked).toHaveLength(1);
  });

  it("does NOT reject when a submit seam rejects, so no click handler leaves an unhandled rejection", async () => {
    const message = await answerDecisionCard(
      sendTarget(),
      openCard(),
      CHOSEN_ANSWER,
      workingSeams({
        submit: async () => {
          throw new Error("connection refused");
        },
      }),
    );
    expect(message).toEqual(
      describeDecisionSubmitResult({
        outcome: "unreachable",
        status: NO_RESPONSE_STATUS,
      }),
    );
  });

  it("runs on its own defaults with the deps argument omitted entirely", async () => {
    const message = await answerDecisionCard(sendTarget(), openCard(), "   ");
    expect(message).toEqual(describeUnsendableDecisionAnswer());
  });
});
