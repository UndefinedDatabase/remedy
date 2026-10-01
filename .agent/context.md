# Context — F292 Plan view and hunk decisions in the cockpit

## Active Branch
feature/f292-plan-view-hunk-decisions, cut from `main` at `2d138e90f`
(the merge commit of pull request 306, F294 Test load diet, part two).

## Scope
F292 (Tier 5, registered by DECISION F044 D5): a plan view in the cockpit that shows the stored
plan with its version, its approval state and each planned task's dependencies and acceptance, and
offers the six plan edits against the version it shows; hunk approve and reject controls in the
diff view; and the palette's seven form entries opening these surfaces, per
`docs/roadmap/features/T5_F292.md`. DECISION F292 D1 fixes the plan read and the round order.

## Do not touch
The write door's argument checks and refusal codes; the plan's own validation; the diff view's
reading of the envelope (feature file, "Do not touch"). The UI follows
`docs/ui/design_reference/` and the shared `--remedy-*` tokens.

## Active assumptions
- The plan view and `remedy job plan-show --json` read one builder, `plan_editing.plan_view`.
- Every UI round renders its surface headless and reads every new style it adds.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
