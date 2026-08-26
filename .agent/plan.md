# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D13.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R28 records R27's PASS, retires the token blocker as DECISION F031 D13 — the
browser has held the server token since F008 and both write-door headers carry
that one value — and ships `decisionSend.ts`, the pure request a sender issues.

## Next Steps
1. T003's WIRING round: thread the job id and the token from `RemedyApp`'s
   `readUrlState` through the shell to the inbox card, mint the nonce, issue
   the request R28 ships, and wire the resolver R27 ships. That round owns the
   only `fetch` in this seam, and it needs no ruling that is not already made.
2. T003's remainder: the clarification form — whose input must TRIM, since the
   builder refuses only the empty string — and the ruling on
   `NeedsAttentionCard`'s decision branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419 and R-0429
   route there, then closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NOTHING CALLS THE REQUEST BUILDER OR THE RESOLVER YET, exactly as nothing
  called `decisionInboxView` for a round. That is deliberate under DECISION
  F031 D5 — the seam ships tested, the wiring follows — but it means `tsc` and
  review, not a test, are what will catch a mis-wired call site.
- A WHITESPACE-ONLY ANSWER IS STILL BUILT, not refused: `decisionAnswer.ts`
  compares against the empty string exactly, so the form round owes the trim.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `b6ae6f99` and this round leaves it there, minting nothing and
  resolving nothing; R-0419 and R-0429 gain recurrences and stay OPEN.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574,
  R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676,
  R-0677, R-0678, R-0679 and R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
