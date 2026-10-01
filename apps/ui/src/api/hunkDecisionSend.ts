// THE HUNK DECISION REQUEST, END TO END (T5_F292 T003, DECISION F292 D6): `patch.approve-hunks`
// at the write door, which RECORDS the decision on the job and applies nothing (DECISION F033
// D4). It composes `taskEditSend.ts` and `pauseSend.ts` for the token headers, the nonce, the one
// submit and every status that carries no hunk-decision meaning.
//
// WHAT IS ITS OWN: the command id, the request, and two sentences. An accepted decision says how
// many hunks it approved, rejected and left pending, read off the door's own answer. A 409 is the
// door's one fixed refusal, `COMMAND_HUNK_DECISION_STATE_MESSAGE` in `ui_server.py`, which
// withholds the reason on purpose (DECISIONS F009 D18 and D22), so the sentence says plainly that
// the server refused the decision and how to try again, and invents no reason.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { HunkDecisionArgs } from "./hunkDecisionView";
import { describePauseSendResult } from "./pauseSend";
import { submitTaskEditRequest } from "./taskEditSend";
import type { TaskEditSubmitResult } from "./taskEditSend";

/** The command id, in the door's spelling (`HUNK_APPROVE_COMMAND_ID` in `ui_server.py`). */
export const HUNK_DECISION_COMMAND_ID = "patch.approve-hunks";

/** THE BUILDER: the exact request the commands endpoint accepts for one decision, or `null` when
 *  it would be unsendable — an empty job id or token, a nonce outside the door's class, or a
 *  decision that decides no hunk, which the recorder refuses as empty. */
export function buildHunkDecisionRequest(
  target: DecisionSendTarget,
  args: HunkDecisionArgs,
  clientNonce: string,
): DecisionSendRequest | null {
  if (target.jobId === "" || target.serverToken === "" || !isUsableCommandNonce(clientNonce)
      || (args.approved.length === 0 && args.rejected.length === 0)) {
    return null;
  }
  return {
    path: jobCommandsPath(target.jobId),
    method: "POST",
    headers: {
      Authorization: `Bearer ${target.serverToken}`,
      "X-Remedy-CSRF": target.serverToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ command: HUNK_DECISION_COMMAND_ID, client_nonce: clientNonce, args }),
  };
}

const REFUSED_SENTENCE =
  "Not recorded: the server refused this decision for this change. Close the change, open it again and decide again.";

/** One send's answer in words, and whether the decision was recorded. */
export interface HunkDecisionOutcome {
  message: DecisionOutcomeMessage;
  recorded: boolean;
}

function count(body: Record<string, unknown> | null, key: string): string {
  const value = body?.[key];
  return typeof value === "number" ? String(value) : "?";
}

/** THE MAPPING. An accepted decision names its counts; a 409 is the door's one fixed refusal;
 *  every other status is worded as the pause door words it. */
export function describeHunkDecisionResult(result: TaskEditSubmitResult): HunkDecisionOutcome {
  if (result.outcome === "accepted") {
    const body = result.body;
    return {
      message: { tone: "ok", sentence: `Recorded: ${count(body, "approved")} approved, ${count(body, "rejected")} rejected, ${count(body, "pending")} pending.` },
      recorded: true,
    };
  }
  if (result.outcome === "refused" && result.status === 409) {
    return { message: { tone: "error", sentence: REFUSED_SENTENCE }, recorded: false };
  }
  return { message: describePauseSendResult(result), recorded: false };
}

const HUNK_DECISION_DEADLINE_MS = 20000;
const UNREACHABLE: TaskEditSubmitResult = { outcome: "unreachable", status: 0, body: null };

/** Every seam optional and defaulting to the shipped function, as `taskEditSend.ts` takes. */
export interface HunkDecisionSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<TaskEditSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitForHunkDecisionDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, HUNK_DECISION_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, stopping at the first step that answers
 *  `null`. Neither `null` path touches the network. */
export async function sendHunkDecision(
  target: DecisionSendTarget,
  args: HunkDecisionArgs,
  deps: HunkDecisionSendDeps = {},
): Promise<HunkDecisionOutcome> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitTaskEditRequest(request));
  const deadline = deps.deadline ?? waitForHunkDecisionDeadline;
  const unsendable: HunkDecisionOutcome = {
    message: { tone: "warn", sentence: "This decision cannot be sent as it stands." }, recorded: false };

  const clientNonce = mintNonce();
  if (clientNonce === null) return unsendable;
  const request = buildHunkDecisionRequest(target, args, clientNonce);
  if (request === null) return unsendable;
  try {
    const settled = await Promise.race([submit(request), deadline().then(() => null)]);
    return describeHunkDecisionResult(settled ?? UNREACHABLE);
  } catch {
    return describeHunkDecisionResult(UNREACHABLE);
  }
}
