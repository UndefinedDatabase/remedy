# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record, the round map and the finding-id ceiling.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the file-based decision queue, live via
decision.requested and decision.resolved events driving the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every producing type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R2 records the F031 R1 verdict — PASS on all thirteen gates, each re-run by the
reviewer — and registers the two recurrences that review surfaced, R-0632 and
R-0676, both reviewer-block defects and neither a new id.

## Next Steps
1. R3 takes the decision-inbox inventory in the source and MEASURES each part:
   the file-based queue store and its CLI, every producer that writes a
   decision, the DAG module's blocked-subtree entry point, and the decision
   event kinds the stream carries today on the Python and the TypeScript side.
2. R3 also settles whether F050 and F051 are built, since F031 depends on both.
3. T001 follows the feature file's Task slicing once that inventory is on disk.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236 measured at `ae5e989d`. R1's plan and handback each
  called a twelve-id set "open" unqualified, which D10 forbids and which the
  R-0632 recurrence this round records.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0625, R-0672, R-0674, R-0675, R-0676, R-0677 and R-0632. R-0495 and
  R-0574 are the two Highs, both inherited from the closed F085 and F086.
- The record now holds `Gate: R19` from F022 as its seed entry. If F031 reaches
  its own R19, that key collides and the ledger gains two paragraphs answering
  to one key — the §3 item 26 defect. A round before then renames the seed or
  the scheme; this bullet is the reminder, measured at `ae5e989d`.
