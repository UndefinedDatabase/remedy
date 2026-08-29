// The completion digest's CARD COPY RULES (T5_F040 T002). `jobDigest.ts` is the
// browser half of the ENVELOPE and `digestVisibility.ts` is the browser half of
// the TRIGGER; this module is the browser half of the WORDS. It is a third file
// rather than a third concern bolted onto either of those for the reason the
// first two were split: `recency.ts`, `actionClass.ts` and `feedFocus.ts` each
// own exactly one rule, and each of the three digest modules has its own purity
// guard already written against it.
//
// WHY IT EXISTS — one collision, ruled as DECISION F040 D10 and nothing wider.
// `docs/ui/design_reference/ux_spec.md` §17 forbids the default UI showing raw
// UUIDs or raw JSON and requires human phrasing. But `primary_action.label` is
// carried verbatim from `recommended_next_action` in
// `packages/orchestration/run_report.py`, which composes it for a MARKDOWN
// artifact: the `open-decision` rule appends a backticked, copy-pasteable CLI
// command carrying a job-id prefix and a `td:` decision id, and `blocked-failed`
// builds its target through `_link`, which returns `[the postmortem](ref)`
// whenever an evidence ref exists. Both are RIGHT where they were written — a
// report is Markdown and a CLI reader wants a command to paste. Only the
// cockpit's render boundary disagrees, and this module IS that boundary.
//
// THE WORDS STAY THE SERVER'S. This module REMOVES what the Markdown surface
// added and changes nothing else: it adds no verb, rephrases no sentence and
// keeps no second rule table keyed on `rule_id`. DECISION F040 D5 makes the
// digest's call to action EQUAL to the report's recommendation, and a client
// that reworded the sentence would break that equality as surely as a second
// rule table would. What is dropped is exactly what Markdown put there.
//
// THE §17 SCREEN HAS ONE HOME AND THIS FILE IS NOT IT. `../copy/humanCopy` owns
// the forbidden-word list, the whole-value identifier test and the length cap;
// `scrubUiText` is IMPORTED from there and applied as the FINAL pass over every
// sentence this module answers. A second copy of that list here would be exactly
// the drift DECISION F040 D2 already spent a round preventing for the urgency
// formula and D4 for the exactness string.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// IT READS NO CLOCK. Nothing here calls Date.now, constructs a date or measures
// elapsed time. Copy is a function of the label it is handed and of nothing
// else, so the same label always answers the same sentence.
// IT KEEPS NO STORAGE. No localStorage key, no sessionStorage key, no
// module-level mutable, nothing memoized between calls.
// IT OPENS NO SOCKET. No fetch, no XMLHttpRequest, no loader: the label has
// already arrived by the time anything here runs.
// IT MINTS NOTHING. No crypto, no id and no nonce of its own — every word that
// survives is a word the server wrote.
//
// `tests/ui_contracts/test_digest_card_copy.py` pins those absences and the
// single-source rule over this file's source, and `digestCardCopy.test.ts` pins
// the sentences.
import { scrubUiText } from "../copy/humanCopy";

/** The digest's OWN state vocabulary, rendered for a human. The keys are the
 *  seven `RunState` members in `packages/core/models.py`, spelled exactly as the
 *  wire spells them, so a state added to that enum has an obvious place to land.
 *
 *  DO NOT REACH FOR `stateLabel` IN `../copy/humanCopy` HERE, however much its
 *  name suggests it. Its vocabulary is the CHECKLIST's — `done`, `current`,
 *  `blocked`, `suggested` — and `RunState` shares none of those spellings, so it
 *  answers "Planned" for `completed`, for `paused`, for `running` and for every
 *  other digest state. It is not a near miss; it is the wrong function. */
const DIGEST_STATE_LABELS: Readonly<Record<string, string>> = {
  "pending": "Waiting to start",
  "planned": "Planned",
  "running": "Running",
  "paused": "Paused",
  "completed": "Completed",
  "failed": "Failed",
  "cancelled": "Cancelled",
};

/** What an unreadable state becomes. A word this client has never heard of is
 *  NOT passed through: §17 forbids showing a raw value, and a state string is a
 *  value the server chose. The repository's own missing-value voice is "not
 *  recorded" (`NOT_RECORDED` in `packages/orchestration/run_report.py`), so the
 *  card says so rather than inventing a state it cannot read. */
const UNREADABLE_STATE_LABEL = "State not recorded";

/** What a call to action reduced to nothing becomes. It is a MISSING-VALUE
 *  MARKER and not a call to action: it names no target, adds no verb and asks
 *  for nothing, because a client that invented an instruction here would be
 *  writing the CTA that DECISION F040 D5 reserves for the server. It is passed
 *  as `scrubUiText`'s OWN fallback parameter rather than tested for separately,
 *  so this module has one empty-case path and not two — `scrubUiText` already
 *  answers its fallback for an empty string, for a forbidden word and for a
 *  whole-value identifier, and all three deserve the same answer. */
const CTA_FALLBACK = "No recommendation recorded";

/** A markdown link, `[text](ref)`, as `_link` in `run_report.py` emits it.
 *  Global: a sentence may carry more than one, and the ref goes with the
 *  brackets rather than being shown as a bare URL. */
const MARKDOWN_LINK = /\[([^\]]*)\]\((?:[^)]*)\)/g;

/** A trailing backticked command together with the `: ` that introduces it, as
 *  the `open-decision` rule appends it. Anchored at the END on purpose: this
 *  removes the paste-me artifact the report adds and leaves the human sentence
 *  that precedes it untouched. The colon is optional so a label that ends in a
 *  bare backticked run is stripped too. */
const TRAILING_COMMAND = /\s*:?\s*`[^`]*`\s*$/;

/** WHY: the hero card says what state the run is in, and the digest's states are
 *  `RunState`'s rather than the checklist's — see the map above for the trap. */
export function digestStateLabel(state: string): string {
  const key = String(state ?? "").trim().toLowerCase();
  return Object.prototype.hasOwnProperty.call(DIGEST_STATE_LABELS, key)
    ? DIGEST_STATE_LABELS[key]
    : UNREADABLE_STATE_LABEL;
}

/** WHY: the server's call to action is written for a Markdown report, and the
 *  cockpit may not show its markup or the identifiers inside it (DECISION F040
 *  D10) — so the markup comes out and the sentence stays the server's.
 *
 *  THE ORDER IS THE RULE, and it is three steps and no more:
 *  1. unwrap every markdown link to its own link text, so `[the postmortem](ref)`
 *     becomes `the postmortem` and the ref is not shown at all;
 *  2. drop a trailing backticked command with its introducing `: `, so
 *     "Answer the open decision: `remedy …`" becomes "Answer the open decision"
 *     — which is the sentence the same rule already emits when no answer command
 *     exists, so the two forms of that rule converge rather than diverge;
 *  3. hand the result to `scrubUiText`, which owns §17's forbidden-word list,
 *     the whole-value identifier test and the length cap.
 *
 *  A LABEL WITH NEITHER MARKUP NOR A COMMAND PASSES THROUGH UNCHANGED except for
 *  that final screen — three of the five rules in `recommended_next_action` are
 *  in exactly that shape, and none of them is improved by being touched.
 *
 *  THE IN-PAGE AFFORDANCE IS NOT THIS MODULE'S JOB. The dropped command is what
 *  `rule_id` was kept in the envelope for: DECISION F040 D5 keeps routing out of
 *  the wire and lets the client decide the affordance, so the card offers a
 *  button where the report offered a paste. */
export function digestCtaText(label: string): string {
  const unlinked = String(label ?? "").replace(MARKDOWN_LINK, "$1");
  const uncommanded = unlinked.replace(TRAILING_COMMAND, "");
  return scrubUiText(uncommanded, CTA_FALLBACK);
}

/** WHY: the closed set of `rule_id` values the envelope can carry, so the card
 *  can bind an affordance per rule and a guard can notice a SIXTH one.
 *
 *  These are the five ids `recommended_next_action` in
 *  `packages/orchestration/run_report.py` returns, in that function's own
 *  first-match-wins order. They are listed and not derived because the wire
 *  carries the id as a string and the client has no other way to know the set;
 *  `tests/ui_contracts/test_digest_card_copy.py` parses the ids back out of that
 *  function and fails if this tuple and the report ever disagree. Note that only
 *  four of the five are reached by the goldens under
 *  `tests/orchestration/fixtures/job_digest/golden/` — the rule table, not the
 *  fixtures, is the vocabulary. */
export const DIGEST_CTA_RULE_IDS = [
  "open-decision",
  "stopped-by-operator",
  "blocked-failed",
  "all-green",
  "indeterminate",
] as const;
