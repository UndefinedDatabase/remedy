# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D7.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R12 upgrades `task_decision`, the eighth and last producing type, and ends
T002. It is the only branch whose options are not known when the code is
written — they come from the escalation record — so its outcomes are BUILT per
option and the same code must satisfy rule (g) when the record offers choices
and rule (h) when it offers none. It is also the branch that drops the record's
`impact`, which amendment A3 carried forward to T002, and this round uses it.
When the type joins the set the emit gate is fully live.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R11 verdict | ordered | the record is touched first |
| C3 the triple, the gate entry and the comment | ordered | S2 to S6 |
| C4 the tests | ordered | S7 |
| C5 the handback | ordered | |

## Next Steps
1. T003: card enrichment and the chip deep links. It is the first F032 work to
   touch `apps/`, so it is the first round bound by the canonical design
   reference in `docs/ui/design_reference/`, and its rounds carry the
   assumption_log obligation that comes with it.
2. The integration gate — the full suite, run per docs/agents/integration_gate.md.
3. The closure sequence: evidence job, a fresh review zip, the STATUS line and
   the pull request, per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Built outcomes are keyed with values the code never chose, so an option
  string that is itself a member of `BOILERPLATE_PHRASES` would be a legal key
  with an illegal-looking outcome; the text is built around the option rather
  than from it, which is what keeps rule (f) clear of the key.
- All eight producing types are enforced from this round on, so any later
  change that regresses a triple raises instead of rendering. That is the
  intent, and it is what the constant was created to reach.
