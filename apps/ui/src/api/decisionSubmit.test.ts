import { describe, it, expect } from "vitest";
import { submitDecisionSendRequest } from "./decisionSubmit";
import type { DecisionSendFunction, DecisionSendReply } from "./decisionSubmit";
import { buildDecisionSendRequest } from "./decisionSend";
import type { DecisionSendRequest } from "./decisionSend";
import { buildDecisionCardModel } from "./decisionCard";
import type { DecisionInboxEntry } from "./decisionCard";

/** A nonce the server's character class accepts, used wherever a test is about
 *  something other than the nonce. */
const GOOD_NONCE = "ui-a1b2c3d4";

/** The per-run server token `RemedyApp` reads out of the URL, spelled so that
 *  no other part of the request could carry this value by accident. */
const SERVER_TOKEN = "srv-token-9f3c1a";

/** The job whose commands door these requests address. */
const JOB_ID = "job-42";

/** The open card every request here answers. */
function openCardEntry(): DecisionInboxEntry {
  return {
    id: "d-1",
    type: "task_decision",
    status: "open",
    safe_summary: "Two migrations claim the same table",
    payload: { options: ["keep first", "keep second"] },
  };
}

/** The one well-formed request, built through `buildDecisionSendRequest` rather
 *  than typed out here, so these tests pin the SEAM between the builder and the
 *  sender instead of a literal that could drift away from it. */
function openRequest(): DecisionSendRequest {
  const request = buildDecisionSendRequest(
    { jobId: JOB_ID, serverToken: SERVER_TOKEN },
    buildDecisionCardModel(openCardEntry()),
    "keep first",
    GOOD_NONCE,
  );
  if (request === null) {
    throw new Error("an open card with a real answer must build a sendable request");
  }
  return request;
}

/** A send function that RECORDS what it was handed and answers a fixed reply.
 *  The recorded list IS the no-retry assertion: its length is what "exactly
 *  once" means, and no global is touched to obtain it. */
function recordingSend(reply: DecisionSendReply) {
  const calls: DecisionSendRequest[] = [];
  const send: DecisionSendFunction = async (request) => {
    calls.push(request);
    return reply;
  };
  return { calls, send };
}

/** A send function that REJECTS — the shape of an offline browser, a refused
 *  connection or an aborted request. */
function rejectingSend() {
  const calls: DecisionSendRequest[] = [];
  const send: DecisionSendFunction = async (request) => {
    calls.push(request);
    throw new Error("connection refused");
  };
  return { calls, send };
}

describe("submitDecisionSendRequest", () => {
  it("hands the send function the request's own path, method, headers and body, unchanged", async () => {
    const request = openRequest();
    const { calls, send } = recordingSend({ ok: true, status: 200 });
    await submitDecisionSendRequest(request, send);
    expect(calls).toHaveLength(1);
    expect(calls[0]).toBe(request);
    expect(calls[0].path).toBe(request.path);
    expect(calls[0].method).toBe(request.method);
    expect(calls[0].headers).toEqual(request.headers);
    expect(calls[0].body).toBe(request.body);
  });

  it("sends exactly ONCE when the door accepts, because one attempt is the whole policy", async () => {
    const { calls, send } = recordingSend({ ok: true, status: 200 });
    await submitDecisionSendRequest(openRequest(), send);
    expect(calls).toHaveLength(1);
  });

  it("maps a 200 to the accepted outcome, carrying that status", async () => {
    const { send } = recordingSend({ ok: true, status: 200 });
    expect(await submitDecisionSendRequest(openRequest(), send)).toEqual({
      outcome: "accepted",
      status: 200,
    });
  });

  it("maps a 403 to refused CARRYING 403, which is how a card names a credential problem", async () => {
    const { send } = recordingSend({ ok: false, status: 403 });
    expect(await submitDecisionSendRequest(openRequest(), send)).toEqual({
      outcome: "refused",
      status: 403,
    });
  });

  it("maps a 409 to refused CARRYING 409, which is how a card names a decision already answered", async () => {
    const { send } = recordingSend({ ok: false, status: 409 });
    expect(await submitDecisionSendRequest(openRequest(), send)).toEqual({
      outcome: "refused",
      status: 409,
    });
  });

  it("maps a 429 to refused CARRYING 429, so the rate budget is not read as a credential problem", async () => {
    const { send } = recordingSend({ ok: false, status: 429 });
    expect(await submitDecisionSendRequest(openRequest(), send)).toEqual({
      outcome: "refused",
      status: 429,
    });
  });

  it("sends exactly ONCE when the door refuses, which is what no retry means", async () => {
    const { calls, send } = recordingSend({ ok: false, status: 409 });
    await submitDecisionSendRequest(openRequest(), send);
    expect(calls).toHaveLength(1);
  });

  it("maps a rejected send to unreachable with status 0, because there is no response", async () => {
    const { send } = rejectingSend();
    expect(await submitDecisionSendRequest(openRequest(), send)).toEqual({
      outcome: "unreachable",
      status: 0,
    });
  });

  it("does NOT reject when the send rejects, so no click handler leaves an unhandled rejection", async () => {
    const { send } = rejectingSend();
    await expect(submitDecisionSendRequest(openRequest(), send)).resolves.toBeDefined();
  });

  it("sends exactly ONCE when the send rejects, so an offline browser is not hammered", async () => {
    const { calls, send } = rejectingSend();
    await submitDecisionSendRequest(openRequest(), send);
    expect(calls).toHaveLength(1);
  });
});
