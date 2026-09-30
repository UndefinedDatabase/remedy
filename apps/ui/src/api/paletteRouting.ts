// T5_F044 T001, DECISION F044 D1 — the bar's routing rule: it is `parse_chat_intent`'s own words,
// in `packages/orchestration/chat_intent.py`'s own order, read here in TypeScript, so the bar and
// the chat never disagree about one line. THE RULE, verbatim: a leading "please " is dropped
// first; then a line ending in "?" or opening with a question word is a question for the chat,
// even when a verb follows ("stop?", "can you stop"); only then is the first word read as a verb,
// and a word is whole only when no letter or digit follows it.

/** Where the bar sends one line of text once it is read. */
export type BarRoute =
  | { readonly kind: "none" }
  | { readonly kind: "chat" }
  | { readonly kind: "command"; readonly command: string }
  | { readonly kind: "palette" };

export const BAR_QUESTION_WORDS: readonly string[] = [
  "what", "why", "how", "when", "where", "which", "who", "did", "does", "do",
  "is", "are", "was", "were", "can", "could", "has", "have",
];

export const BAR_NOTE_OPENERS: readonly string[] = ["tell the builder", "tell it", "note", "steer"];

export const BAR_LEADING_VERBS: Readonly<Record<string, string>> = {
  stop: "job.stop",
  cancel: "job.stop",
  abort: "job.stop",
  pause: "job.pause",
  resume: "job.unpause",
  unpause: "job.unpause",
  continue: "job.unpause",
  veto: "job.veto-task",
  skip: "job.veto-task",
  drop: "job.veto-task",
  rerun: "job.rerun-subtree",
  retry: "job.rerun-subtree",
};

function normalize(text: string): string {
  return text.replace(/\s+/g, " ").trim();
}

function stripLeadingPlease(text: string): string {
  return text.slice(0, 7).toLowerCase() === "please " ? text.slice(7) : text;
}

/** True when `text` starts with `phrase` (case ignored) and no letter, digit or underscore
 *  follows it, so a word counts only when it is whole. */
function startsWithWholePhrase(text: string, phrase: string): boolean {
  if (text.slice(0, phrase.length).toLowerCase() !== phrase) return false;
  const rest = text[phrase.length];
  return rest === undefined || !/[\p{L}\p{N}_]/u.test(rest);
}

function opensWithQuestionWord(text: string): boolean {
  return BAR_QUESTION_WORDS.some((word) => startsWithWholePhrase(text, word));
}

function noteOpenerMatches(text: string): boolean {
  return BAR_NOTE_OPENERS.some((opener) => startsWithWholePhrase(text, opener));
}

export function routeBarText(text: string, focusedTaskId: string): BarRoute {
  const stripped = stripLeadingPlease(normalize(text));
  if (stripped === "") return { kind: "none" };
  if (stripped.endsWith("?") || opensWithQuestionWord(stripped)) return { kind: "chat" };

  const firstWord = stripped.split(" ", 1)[0].toLowerCase();
  if (Object.prototype.hasOwnProperty.call(BAR_LEADING_VERBS, firstWord)) {
    return { kind: "command", command: BAR_LEADING_VERBS[firstWord] };
  }

  if (noteOpenerMatches(stripped)) {
    return { kind: "command", command: focusedTaskId !== "" ? "job.steer" : "chat.send" };
  }

  if (startsWithWholePhrase(stripped, "run again")) {
    return { kind: "command", command: "job.rerun-subtree" };
  }

  return { kind: "palette" };
}
