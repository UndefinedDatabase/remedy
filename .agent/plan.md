# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D12.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R27 ships T003's DEEP-LINK seam at the pure layer: the model learns the task a
decision is about, `decisionFocus.ts` turns that into the graph node the card
will jump to — the resolver `feedFocus.ts` already proved — and the sentence R26
falsified in `decisionCard.ts` is retired at its source.

## Next Steps
1. T003's SENDER round, which needs a design ruling first: the browser holds
   NO bearer token and NO `X-Remedy-CSRF` value today, and how one reaches the
   page is a decision that spans the server and the shell. Rule it, then wire
   the body `decisionAnswer.ts` builds, and wire the resolver R27 ships.
2. T003's remainder: the clarification form — whose input must TRIM, since the
   builder refuses only the empty string — and the ruling on
   `NeedsAttentionCard`'s decision branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist item R-0683 routes there, then closure
   per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NOTHING CALLS THE RESOLVER YET, exactly as nothing called `decisionInboxView`
  for a round. That is deliberate under DECISION F031 D5 — the seam ships
  tested, the wiring follows — but it means `tsc` and review, not a test, are
  what will catch a mis-wired call site.
- A WHITESPACE-ONLY ANSWER IS STILL BUILT, not refused: `decisionAnswer.ts`
  compares against the empty string exactly, so the form round owes the trim.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `beec7b83` and this round leaves it there, minting nothing and
  resolving nothing; R-0377 gains a recurrence and stays OPEN.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601,
  R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678,
  R-0679 and R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
