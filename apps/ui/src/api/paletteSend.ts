// T5_F044 T001, DECISION F044 D3 — the palette's send: a complete argument flow becomes the one
// request the write door accepts, through the SAME senders the rest of this cockpit already
// composes rather than a fetch of its own. A `job.rerun-subtree` flow needs its OWN sender because
// its 200 body is not a plain acceptance — `rerunSend.ts`'s `sendRerunSubtree` reads a cost that
// needs confirming or a prepared run command back off the wire, through `rerunView.ts`'s
// `rerunAnswerView`, and the palette asks no confirmation of its own, so a rerun whose cost is not
// yet confirmed is told, in words, where to confirm it instead. Every other command's flow is a
// plain command with plain arguments, exactly what a confirmed chat card already sends, so it goes
// through `chatTurn.ts`'s `sendChatCard` — the palette and the chat send the same commands in the
// same words.
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import type { DecisionSendTarget } from "./decisionSend";
import type { ChatCardSendDeps } from "./chatTurn";
import { sendChatCard } from "./chatTurn";
import type { RerunSubtreeSendDeps } from "./rerunSend";
import { sendRerunSubtree } from "./rerunSend";
import { rerunAnswerView } from "./rerunView";
import type { PaletteArgFlow } from "./paletteArgs";

const RERUN_COMMAND = "job.rerun-subtree";
const RERUN_TASK_ARG = "task_id";

/** The palette asks no confirmation of its own: a rerun whose cost needs confirming is told, in
 *  words, where that confirmation lives instead. */
export const PALETTE_RERUN_CONFIRM_ELSEWHERE = "Confirm it from the run's detail.";

/** Every seam optional and defaulting to the shipped sender each command's flow reaches for. */
export interface PaletteSendDeps {
  card?: ChatCardSendDeps;
  rerun?: RerunSubtreeSendDeps;
}

/** THE RERUN'S OWN WORDS: `rerunAnswerView`'s sentence, plus the run command for a prepared
 *  answer or `PALETTE_RERUN_CONFIRM_ELSEWHERE` for one that still needs confirming. */
function rerunOutcomeMessage(
  view: ReturnType<typeof rerunAnswerView>,
  fallback: DecisionOutcomeMessage,
): DecisionOutcomeMessage {
  if (view === null) return fallback;
  if (view.kind === "prepared") {
    return { tone: "ok", sentence: `${view.sentence} Run it with: ${view.runCommand}` };
  }
  return { tone: "warn", sentence: `${view.sentence} ${PALETTE_RERUN_CONFIRM_ELSEWHERE}` };
}

/** THE FLOW: a complete command flow sent through its own sender — a rerun through
 *  `sendRerunSubtree`, every other command through `sendChatCard`. */
export async function sendPaletteCommand(
  target: DecisionSendTarget,
  flow: PaletteArgFlow,
  deps: PaletteSendDeps = {},
): Promise<DecisionOutcomeMessage> {
  if (flow.entry.command === RERUN_COMMAND) {
    const taskId = flow.values[RERUN_TASK_ARG] ?? "";
    const outcome = await sendRerunSubtree(target, taskId, {}, deps.rerun);
    return rerunOutcomeMessage(rerunAnswerView(outcome.answer), outcome.message);
  }
  return sendChatCard(
    target,
    {
      kind: "card",
      verb: flow.entry.command,
      title: flow.entry.title,
      lines: [],
      args: { ...flow.values },
      missing: [],
      confirmable: true,
    },
    deps.card,
  );
}
