# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D11.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R26 OPENS T003 at the layer a test can reach: `decisionAnswer.ts` turns a card
plus a typed answer into the exact body `/api/jobs/<id>/commands` accepts and
refuses four the door would refuse anyway, while R-0682's `role="group"` lands
on both chip rows.

## Next Steps
1. T003's sender round wires that body to the door — the CSRF header, the
   bearer token, the nonce the browser mints, and the answer affordances the
   card currently ships DISABLED.
2. T003's remainder: the clarification form, the deep links into graph focus,
   and the ruling on `NeedsAttentionCard`'s decision branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist item R-0683 routes there, then closure
   per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE BUILDER IS PURE AND THE DOOR IS NOT. Every refusal it makes is a SECOND
  copy of a rule `ui_server.py` already enforces — the nonce character class
  most of all — so the two can drift. It refuses early to spare the operator a
  round trip, never to replace the server's check.
- NO TEST REACHES THE MARKUP under DECISION F031 D5, so `role="group"` is
  pinned by review alone; this round adds no `tests/ui_contracts/` pin, and
  this line records that gap rather than implying coverage.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 240 at `92b323e3`, and this round's C2 lowers it to 239 by resolving
  R-0682 and minting nothing, in the commit order the R26 block's constraint 4
  fixes.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and
  R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
