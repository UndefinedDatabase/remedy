import { describe, it, expect } from "vitest";
import {
  describeDecisionSubmitResult,
  describeUnsendableDecisionAnswer,
} from "./decisionOutcome";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import type { DecisionSubmitResult } from "./decisionSubmit";

/** THE VOCABULARY, SPELLED OUT BY THE TEST rather than imported. The module
 *  keeps every sentence private on purpose, and a test that read the constant
 *  would pass whatever the constant became — these literals are what actually
 *  pins the words an operator will read. */
const ACCEPTED = "Your answer was recorded.";
const UNREACHABLE =
  "No answer came back, so this may not have reached the run. You can send it again.";
const RATE_LIMITED =
  "Too many answers arrived at once. Wait a moment, then send this one again.";
const CREDENTIAL =
  "This dashboard was not allowed to answer, so nothing was recorded. Open the dashboard again from a fresh link.";
const MALFORMED = "The run could not read this answer, so nothing was recorded.";
const CLOSED = "This decision is no longer open. It may already have been answered.";
const UNDISPATCHED = "This run cannot take answers from the dashboard.";
const UNRECOGNISED_REFUSAL = "The run refused this answer, so nothing was recorded.";
const UNSENDABLE = "This answer cannot be sent as it stands. Check it, then try again.";

/** The status `decisionSubmit.ts` fixes for "there was no response at all". */
const NO_RESPONSE_STATUS = 0;

/** A refusal at one status, written once so each case below reads as the status
 *  it is about and nothing else. */
function refusedAt(status: number): DecisionSubmitResult {
  return { outcome: "refused", status };
}

describe("describeDecisionSubmitResult", () => {
  it("calls an accepted answer recorded, in the calm tone", () => {
    expect(describeDecisionSubmitResult({ outcome: "accepted", status: 200 })).toEqual({
      tone: "ok",
      sentence: ACCEPTED,
    });
  });

  it("warns rather than errors when nothing was heard back, because sending again may work", () => {
    expect(
      describeDecisionSubmitResult({
        outcome: "unreachable",
        status: NO_RESPONSE_STATUS,
      }),
    ).toEqual({ tone: "warn", sentence: UNREACHABLE });
  });

  it("warns over the rate budget, which is the one refusal that clears by waiting", () => {
    expect(describeDecisionSubmitResult(refusedAt(429))).toEqual({
      tone: "warn",
      sentence: RATE_LIMITED,
    });
  });

  it("errors on a rejected credential and points at a fresh link rather than at retrying", () => {
    expect(describeDecisionSubmitResult(refusedAt(403))).toEqual({
      tone: "error",
      sentence: CREDENTIAL,
    });
  });

  it("errors on a body the run could not read, and says nothing was recorded", () => {
    expect(describeDecisionSubmitResult(refusedAt(400))).toEqual({
      tone: "error",
      sentence: MALFORMED,
    });
  });

  it("errors on a decision that is no longer open, because answering again cannot help", () => {
    expect(describeDecisionSubmitResult(refusedAt(409))).toEqual({
      tone: "error",
      sentence: CLOSED,
    });
  });

  it("errors on a command this run does not dispatch, which no retry will change", () => {
    expect(describeDecisionSubmitResult(refusedAt(501))).toEqual({
      tone: "error",
      sentence: UNDISPATCHED,
    });
  });

  it("falls back to a sentence that claims nothing about a refusal it cannot name", () => {
    expect(describeDecisionSubmitResult(refusedAt(418))).toEqual({
      tone: "error",
      sentence: UNRECOGNISED_REFUSAL,
    });
  });

  it("gives every unlisted refusal the same unrecognised sentence, high or low", () => {
    const low = describeDecisionSubmitResult(refusedAt(302));
    const high = describeDecisionSubmitResult(refusedAt(503));
    expect(low).toEqual({ tone: "error", sentence: UNRECOGNISED_REFUSAL });
    expect(high).toEqual(low);
  });

  it("ignores the status entirely once the door has accepted", () => {
    expect(describeDecisionSubmitResult({ outcome: "accepted", status: 429 })).toEqual({
      tone: "ok",
      sentence: ACCEPTED,
    });
  });

  it("hands out a FRESH message each call, so no caller can edit the vocabulary", () => {
    const first = describeDecisionSubmitResult(refusedAt(409));
    const second = describeDecisionSubmitResult(refusedAt(409));
    expect(first).toEqual(second);
    expect(first).not.toBe(second);
    first.sentence = "edited";
    expect(describeDecisionSubmitResult(refusedAt(409)).sentence).toBe(CLOSED);
  });

  it("puts no status number, header name or URL into any sentence it can answer", () => {
    const everySentence = [
      describeDecisionSubmitResult({ outcome: "accepted", status: 200 }),
      describeDecisionSubmitResult({ outcome: "unreachable", status: NO_RESPONSE_STATUS }),
      describeDecisionSubmitResult(refusedAt(400)),
      describeDecisionSubmitResult(refusedAt(403)),
      describeDecisionSubmitResult(refusedAt(409)),
      describeDecisionSubmitResult(refusedAt(429)),
      describeDecisionSubmitResult(refusedAt(501)),
      describeDecisionSubmitResult(refusedAt(418)),
      describeUnsendableDecisionAnswer(),
    ].map((message: DecisionOutcomeMessage) => message.sentence);
    for (const sentence of everySentence) {
      expect(sentence).not.toMatch(/[0-9]/);
      expect(sentence).not.toMatch(/http|\/api\/|X-Remedy|Authorization|fetch/);
    }
  });

  it("says something DIFFERENT for every branch, so no two states read alike", () => {
    const sentences = [
      describeDecisionSubmitResult({ outcome: "accepted", status: 200 }).sentence,
      describeDecisionSubmitResult({ outcome: "unreachable", status: NO_RESPONSE_STATUS })
        .sentence,
      describeDecisionSubmitResult(refusedAt(400)).sentence,
      describeDecisionSubmitResult(refusedAt(403)).sentence,
      describeDecisionSubmitResult(refusedAt(409)).sentence,
      describeDecisionSubmitResult(refusedAt(429)).sentence,
      describeDecisionSubmitResult(refusedAt(501)).sentence,
      describeDecisionSubmitResult(refusedAt(418)).sentence,
      describeUnsendableDecisionAnswer().sentence,
    ];
    expect(new Set(sentences).size).toBe(sentences.length);
  });
});

describe("describeUnsendableDecisionAnswer", () => {
  it("warns about an answer that never reached the wire, because editing it can help", () => {
    expect(describeUnsendableDecisionAnswer()).toEqual({
      tone: "warn",
      sentence: UNSENDABLE,
    });
  });

  it("says something no sent result says, so an unsent answer is never mistaken for a refusal", () => {
    const unsendable = describeUnsendableDecisionAnswer().sentence;
    expect(unsendable).not.toBe(UNRECOGNISED_REFUSAL);
    expect(unsendable).not.toBe(UNREACHABLE);
  });

  it("hands out a FRESH message each call, so no caller can edit the vocabulary", () => {
    const first = describeUnsendableDecisionAnswer();
    const second = describeUnsendableDecisionAnswer();
    expect(first).toEqual(second);
    expect(first).not.toBe(second);
  });
});
