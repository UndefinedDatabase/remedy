import { describe, it, expect } from "vitest";
import { buildDecisionSendRequest } from "./decisionSend";
import { buildDecisionResolveCommand, jobCommandsPath } from "./decisionAnswer";
import { buildDecisionCardModel } from "./decisionCard";
import type { DecisionInboxEntry } from "./decisionCard";

/** A nonce the server's character class accepts, used wherever a test is about
 *  something other than the nonce. */
const GOOD_NONCE = "ui-a1b2c3d4";

/** The per-run server token `RemedyApp` reads out of the URL, spelled so that
 *  no other part of the request could carry this value by accident. */
const SERVER_TOKEN = "srv-token-9f3c1a";

/** The job whose commands door this request addresses. */
const JOB_ID = "job-42";

/** Every model here is built through `buildDecisionCardModel` rather than by
 *  hand, so these tests pin the SEAM between the endpoint's payload and the
 *  request that answers it — not a literal someone typed twice. */
function modelFrom(entry: DecisionInboxEntry) {
  return buildDecisionCardModel(entry);
}

/** The open card every accepted-request test answers. */
function openCardEntry(): DecisionInboxEntry {
  return {
    id: "d-1",
    type: "task_decision",
    status: "open",
    safe_summary: "Two migrations claim the same table",
    payload: { options: ["keep first", "keep second"] },
  };
}

/** The addressed job and the credential that opens its door, as the ONE value
 *  the builder takes. Rebuilt per call so no test can mutate another's target. */
function sendTarget() {
  return { jobId: JOB_ID, serverToken: SERVER_TOKEN };
}

/** The one well-formed call, so a test about headers does not restate a call
 *  about the body. */
function openRequest() {
  return buildDecisionSendRequest(
    sendTarget(),
    modelFrom(openCardEntry()),
    "keep first",
    GOOD_NONCE,
  );
}

describe("buildDecisionSendRequest", () => {
  it("addresses the job's own commands path, with no host and no query", () => {
    const request = openRequest();
    expect(request?.path).toBe(jobCommandsPath(JOB_ID));
    expect(request?.path).toBe("/api/jobs/job-42/commands");
  });

  it("answers POST, the method the command door reads a body from", () => {
    expect(openRequest()?.method).toBe("POST");
  });

  it("carries a body that parses back to the command the builder builds", () => {
    const request = openRequest();
    expect(request).not.toBeNull();
    expect(JSON.parse(request!.body)).toEqual(
      buildDecisionResolveCommand(modelFrom(openCardEntry()), "keep first", GOOD_NONCE),
    );
  });

  it("carries the token in BOTH token headers, as ONE secret per DECISION F009 D11", () => {
    const request = openRequest();
    expect(request).not.toBeNull();
    const headers = request!.headers;
    expect(headers["Authorization"]).toBe(`Bearer ${SERVER_TOKEN}`);
    expect(headers["X-Remedy-CSRF"]).toBe(SERVER_TOKEN);
    expect(headers["Authorization"].replace("Bearer ", "")).toBe(headers["X-Remedy-CSRF"]);
  });

  it("puts the Bearer scheme on the authorization header ONLY", () => {
    const request = openRequest();
    expect(request).not.toBeNull();
    expect(request!.headers["Authorization"].startsWith("Bearer ")).toBe(true);
    expect(request!.headers["X-Remedy-CSRF"]).not.toContain("Bearer");
  });

  it("declares a JSON content type, because the body IS JSON", () => {
    expect(openRequest()?.headers["Content-Type"]).toBe("application/json");
  });

  it("keeps the token out of the path entirely, because a query string reaches logs", () => {
    const request = openRequest();
    expect(request).not.toBeNull();
    expect(request!.path).not.toContain(SERVER_TOKEN);
    expect(request!.path).not.toContain("?");
  });

  it("refuses an empty token, which is a request the door answers 403", () => {
    expect(
      buildDecisionSendRequest(
        { jobId: JOB_ID, serverToken: "" },
        modelFrom(openCardEntry()),
        "keep first",
        GOOD_NONCE,
      ),
    ).toBeNull();
  });

  it("refuses an empty job id, because it addresses no job", () => {
    expect(
      buildDecisionSendRequest(
        { jobId: "", serverToken: SERVER_TOKEN },
        modelFrom(openCardEntry()),
        "keep first",
        GOOD_NONCE,
      ),
    ).toBeNull();
  });

  it("reads the job and the token from NAMED fields, so their ORDER cannot matter", () => {
    // The swap finding R-0684 describes is stopped by `tsc`, not by this test:
    // with one named object there is no positional pair left to transpose. What
    // a test CAN pin is that writing the two fields the other way round builds
    // the very same request, and still keeps the credential out of the path.
    const reversed = buildDecisionSendRequest(
      { serverToken: SERVER_TOKEN, jobId: JOB_ID },
      modelFrom(openCardEntry()),
      "keep first",
      GOOD_NONCE,
    );
    expect(reversed).toEqual(openRequest());
    expect(reversed?.path).not.toContain(SERVER_TOKEN);
  });

  it("propagates the body builder's refusal as null, never as a request with no body", () => {
    const resolved = modelFrom({ ...openCardEntry(), status: "resolved" });
    expect(resolved.isOpen).toBe(false);
    expect(buildDecisionResolveCommand(resolved, "keep first", GOOD_NONCE)).toBeNull();
    expect(
      buildDecisionSendRequest(sendTarget(), resolved, "keep first", GOOD_NONCE),
    ).toBeNull();
  });

  it("propagates the blank-answer refusal, so no whitespace answer is sendable", () => {
    expect(buildDecisionResolveCommand(modelFrom(openCardEntry()), "   ", GOOD_NONCE)).toBeNull();
    expect(
      buildDecisionSendRequest(sendTarget(), modelFrom(openCardEntry()), "   ", GOOD_NONCE),
    ).toBeNull();
  });
});

describe("buildDecisionSendRequest clarification answers", () => {
  /** The pending flight-plan approval this form exists for, carrying one open
   *  question on the same card. It is the entry `decisionAnswer.ts`'s own
   *  clarification tests use, so both layers pin the same seam rather than two
   *  literals that could drift apart. */
  function pendingPlanEntry(): DecisionInboxEntry {
    return {
      id: "fp:approval",
      type: "flight_plan_approval",
      status: "open",
      safe_summary: "Flight plan awaiting approval (1 open question).",
      payload: {
        options: ["approve", "reject"],
        clarifications: [{ id: "q1", question: "Which store?", default_answer: "postgres" }],
      },
      answerable_by_decision_resolve: true,
    };
  }

  /** One approval request, built with whatever map the caller chose to pass —
   *  or with none at all, which is what every call site written before this
   *  form passes. */
  function planRequest(clarificationAnswers?: Record<string, string>) {
    return buildDecisionSendRequest(
      sendTarget(),
      modelFrom(pendingPlanEntry()),
      "approve",
      GOOD_NONCE,
      clarificationAnswers,
    );
  }

  /** The `args` object the request's SERIALISED body parses back to. Read
   *  through the body rather than through the command builder, because what is
   *  under test here is what this module actually put on the wire. */
  function sentArgs(request: ReturnType<typeof planRequest>) {
    expect(request).not.toBeNull();
    return JSON.parse(request!.body).args as Record<string, unknown>;
  }

  it("sends NO answers key at all when the caller passes no fifth argument", () => {
    const args = sentArgs(planRequest());
    expect(Object.keys(args).sort()).toEqual(["answer", "decision_id"]);
    expect(args["answers"]).toBeUndefined();
  });

  it("forwards a filled map under the server's own args key, with its value TRIMMED", () => {
    const args = sentArgs(planRequest({ q1: "  sqlite\n" }));
    expect(Object.keys(args).sort()).toEqual(["answer", "answers", "decision_id"]);
    expect(args["answers"]).toEqual({ q1: "sqlite" });
  });

  it("sends NO answers key for a map whose every value is blank after trimming", () => {
    const args = sentArgs(planRequest({ q1: "   ", q2: "\n\t", q3: "" }));
    expect(Object.keys(args)).not.toContain("answers");
    expect(args["answers"]).toBeUndefined();
  });

  it("lets the map reach the BODY alone, never the path and never the headers", () => {
    // The transposition finding R-0684 is about a value landing in a part of
    // the request that was never meant to carry it, and the path and the
    // headers are exactly those parts one layer up from where it was found.
    const request = planRequest({ q1: "sqlite" });
    expect(request).not.toBeNull();
    expect(request!.path).toBe(jobCommandsPath(JOB_ID));
    expect(request!.path).toBe(planRequest()?.path);
    expect(request!.headers).toEqual(planRequest()?.headers);
    for (const carried of ["q1", "sqlite"]) {
      expect(request!.path).not.toContain(carried);
      expect(JSON.stringify(request!.headers)).not.toContain(carried);
      expect(request!.body).toContain(carried);
    }
  });
});
