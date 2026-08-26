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

/** The one well-formed call, so a test about headers does not restate a call
 *  about the body. */
function openRequest() {
  return buildDecisionSendRequest(
    JOB_ID,
    SERVER_TOKEN,
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
      buildDecisionSendRequest(JOB_ID, "", modelFrom(openCardEntry()), "keep first", GOOD_NONCE),
    ).toBeNull();
  });

  it("refuses an empty job id, because it addresses no job", () => {
    expect(
      buildDecisionSendRequest("", SERVER_TOKEN, modelFrom(openCardEntry()), "keep first", GOOD_NONCE),
    ).toBeNull();
  });

  it("propagates the body builder's refusal as null, never as a request with no body", () => {
    const resolved = modelFrom({ ...openCardEntry(), status: "resolved" });
    expect(resolved.isOpen).toBe(false);
    expect(buildDecisionResolveCommand(resolved, "keep first", GOOD_NONCE)).toBeNull();
    expect(
      buildDecisionSendRequest(JOB_ID, SERVER_TOKEN, resolved, "keep first", GOOD_NONCE),
    ).toBeNull();
  });
});
