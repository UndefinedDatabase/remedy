// F038 T003, DECISION F038 D12 — the evidence panel's Chat tab: the grounded chat, replacing
// the placeholder `EVIDENCE_CHAT_NOT_YET` named. A line asks the chat route about the focused
// run's task, or about the whole project when "Ask about the whole project" is ticked; an
// answer shows every sentence with numbered chips linking to its evidence items, or a visible
// unsupported mark; a card is sent through the write door only when Confirm is pressed.
//
// `ChatTurnBlock` IS PURE and owns every rendering rule this feature has: which mark a
// sentence carries, whether Confirm shows, what an evidence item reads. It is exported apart
// from `EvidenceChatTab` so `evidenceChatAudit.test.ts` can render it with
// `react-dom/server`'s `renderToStaticMarkup` — the one DOM surface this repository's vitest
// config can reach (DECISION F031 D5: no DOM harness exists for a mounted component). Every
// OTHER rule — what a sentence means, what a card sends — lives in `../../api/chatTurn.ts`,
// which this file only calls.
//
// IT READS ONLY THROUGH `loadChatTurn` AND SENDS ONLY THROUGH `sendChatCard`: no `fetch(`
// appears anywhere in this file, exactly as `DiffTab` and `OwnershipTab` in
// `EvidencePanel.tsx` read only through their own doors.
import { useRef, useState } from "react";
import { loadChatTurn } from "../../api/remedyApi";
import {
  chatEvidenceTab, chatEvidenceTabLabel, chatScopeLabel, chatSentenceMark, chatSentenceText,
  chatUnavailableLine, sendChatCard,
} from "../../api/chatTurn";
import type { ChatCardView, ChatTurnView } from "../../api/chatTurn";
import type { DecisionOutcomeMessage } from "../../api/decisionOutcome";
import type { DecisionSendTarget } from "../../api/decisionSend";
import type { EvidenceTab } from "./semanticZoom";
import styles from "./EvidenceChatTab.module.css";

const CHAT_PENDING_LINE = "Asking…";
const CHAT_UNREADABLE_LINE = "This answer could not be read.";

/** One asked line and what the chat route answered: `view` is `undefined` while the read is
 *  in flight and `null` when the route's answer could not be decoded. Pure — it renders
 *  exactly what it is handed and reads no clock, no storage and no network of its own.
 *  `sending` (default false) is the tab's own send-in-flight flag: while it is true Confirm
 *  is not rendered, so a card can never be sent twice by a second click racing the first. */
export function ChatTurnBlock({
  question, view, turnKey, outcome, sending = false, onConfirm, onOpenTab,
}: {
  question: string;
  view: ChatTurnView | null | undefined;
  turnKey: string;
  outcome: DecisionOutcomeMessage | null;
  sending?: boolean;
  onConfirm: () => void;
  onOpenTab: (tab: EvidenceTab) => void;
}) {
  if (question === "") return null;
  return (
    <div className={styles.turn} data-ui="chat-turn">
      <p className={styles.question} data-ui="chat-question">{question}</p>
      {view === undefined && <p className={styles.pending} data-ui="chat-pending">{CHAT_PENDING_LINE}</p>}
      {view === null && <p className={styles.unreadable} data-ui="chat-unreadable">{CHAT_UNREADABLE_LINE}</p>}
      {view !== undefined && view !== null && view.kind === "unavailable" && (
        <p className={styles.unavailable} data-ui="chat-unavailable">{chatUnavailableLine(view.reason)}</p>
      )}
      {view !== undefined && view !== null && view.kind === "answer" && (
        <>
          <span className={styles.scopeChip} data-ui="chat-scope">{chatScopeLabel(view)}</span>
          {view.sentences.map((sentence, index) => {
            const mark = chatSentenceMark(sentence);
            return (
              <p key={index} className={styles.sentence} data-ui="chat-sentence" data-mark={mark}>
                {chatSentenceText(sentence)}
                {mark === "cited" && sentence.citations.map((n) => (
                  <a key={n} className={styles.chip} data-ui="chat-chip" href={`#chat-${turnKey}-ev-${n}`}>
                    {`[${n}]`}
                  </a>
                ))}
                {mark === "unsupported" && (
                  <span className={styles.unsupportedMark} data-ui="chat-unsupported" title={sentence.problem}>
                    unsupported
                  </span>
                )}
              </p>
            );
          })}
          <div className={styles.evidenceList} data-ui="chat-evidence">
            {view.evidence.map((item) => {
              const tab = chatEvidenceTab(item.kind);
              return (
                <div
                  key={item.number}
                  id={`chat-${turnKey}-ev-${item.number}`}
                  className={styles.evidenceItem}
                  data-ui="chat-evidence-item"
                >
                  <span>{`[${item.number}] ${item.kind} ${item.ref} — ${item.text}`}</span>
                  {tab !== null && (
                    <button type="button" className={styles.openTab} onClick={() => onOpenTab(tab)}>
                      {chatEvidenceTabLabel(tab)}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </>
      )}
      {view !== undefined && view !== null && view.kind === "card" && (
        <>
          <strong className={styles.cardTitle} data-ui="chat-card">{view.title}</strong>
          <ul className={styles.cardLines}>
            {view.lines.map((line, index) => <li key={index}>{line}</li>)}
          </ul>
          {!sending && chatCardCanConfirm(view, outcome) && (
            <button type="button" className={styles.confirm} data-ui="chat-card-confirm" onClick={onConfirm}>
              Confirm
            </button>
          )}
          <p className={styles.outcome} role="status">{outcome !== null ? outcome.sentence : ""}</p>
        </>
      )}
    </div>
  );
}

/** Confirm shows only while the card is confirmable, misses nothing, and has not already been
 *  sent with tone `ok` — pressing it again after a successful send would replay a write. */
function chatCardCanConfirm(card: ChatCardView, outcome: DecisionOutcomeMessage | null): boolean {
  return card.confirmable && card.missing.length === 0 && !(outcome !== null && outcome.tone === "ok");
}

/** One asked line, its answer or card, the outcome of confirming it, if any, and whether its
 *  send is in flight right now. */
interface ChatTurnRecord {
  key: string;
  question: string;
  view: ChatTurnView | null | undefined;
  outcome: DecisionOutcomeMessage | null;
  sending: boolean;
}

/** The tab itself: the log of turns above the form that asks the next one (F038 T003). It
 *  reads only through `loadChatTurn` and sends only through `sendChatCard`. */
export function EvidenceChatTab({ jobId, token, taskId, onTab }: {
  jobId: string;
  token: string;
  taskId: string;
  onTab: (tab: EvidenceTab) => void;
}) {
  const [wholeProject, setWholeProject] = useState(false);
  const [text, setText] = useState("");
  const [turns, setTurns] = useState<ChatTurnRecord[]>([]);
  const nextKey = useRef(0);
  const target: DecisionSendTarget = { jobId, serverToken: token };

  const ask = async () => {
    const question = text.trim();
    if (question === "") return;
    const key = String(nextKey.current);
    nextKey.current += 1;
    setTurns((sofar) => [...sofar, { key, question, view: undefined, outcome: null, sending: false }]);
    setText("");
    const scopeTaskId = wholeProject ? "" : taskId;
    const view = await loadChatTurn({ jobId, token, text: question, taskId: scopeTaskId });
    setTurns((sofar) => sofar.map((turn) => (turn.key === key ? { ...turn, view } : turn)));
  };

  const confirm = async (key: string, card: ChatCardView) => {
    setTurns((sofar) => sofar.map((turn) => (turn.key === key ? { ...turn, sending: true } : turn)));
    const outcome = await sendChatCard(target, card);
    setTurns((sofar) => sofar.map((turn) => (
      turn.key === key ? { ...turn, outcome, sending: false } : turn
    )));
  };

  return (
    <div className={styles.tab} data-ui="chat-tab">
      {turns.map((turn) => (
        <ChatTurnBlock
          key={turn.key}
          question={turn.question}
          view={turn.view}
          turnKey={turn.key}
          outcome={turn.outcome}
          sending={turn.sending}
          onConfirm={() => {
            if (turn.view !== undefined && turn.view !== null && turn.view.kind === "card") {
              void confirm(turn.key, turn.view);
            }
          }}
          onOpenTab={onTab}
        />
      ))}
      <div className={styles.form}>
        <label className={styles.wholeProjectLabel}>
          <input
            type="checkbox"
            checked={wholeProject}
            onChange={(event) => setWholeProject(event.target.checked)}
          />
          Ask about the whole project
        </label>
        <input
          className={styles.input}
          type="text"
          aria-label="Ask the chat"
          placeholder={wholeProject ? "Ask about the whole project" : `Ask about task ${taskId}`}
          value={text}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") void ask();
          }}
        />
        <button type="button" className={styles.ask} onClick={() => void ask()}>
          Ask
        </button>
      </div>
    </div>
  );
}
