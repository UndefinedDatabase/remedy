# Context — amend0825 dogfooding findings

## Active Branch
feature/amend0825-dogfood-findings, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022.

## Scope
The six findings of the operator collection order amend0825, and nothing else.
Three are repaired in code with regression tests; three are recorded as dated
operator findings in the feature file that owns them. This is not feature work
and claims no STATUS line.

## Do not touch
`validate_job_id`, the promotion blocked-path guard and its all-or-nothing
rule, F232's model-upgrade playbook, and `docs/roadmap/ROADMAP.md`. The
untracked `.agent/STOP` from the stopped F031 R10 round stays on disk.

## Assumptions
- The operator prompt carries the authorization for the alias repoint, for the
  self-merge of this branch's pull request, and for every triage call below.
- A finding whose repair is not surgical, or whose repair no test could prove,
  is recorded rather than half-built. That rule decided findings 3 and 4, and
  decided the residue of finding 2.
- Findings are NOT written to `.agent/candidates.md`: a candidate there blocks
  the next feature claim, and these are feature-owned defects, not closure
  candidates.

## Steps
This order has no round map: it is a single collection order, not a feature
build. The six items, their triage verdicts and the remaining actions live in
the `## Current Step` table of `.agent/plan.md`. `.agent/live_review.md` still
carries the F022 record it held at this branch point and is not touched here;
the F031 record lives on `feature/f031-decision-inbox`.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not F022's and not this
order's: deleting them with the rest of a rewrite is what cost this round a red
CI run, because the state-reader bullet is precisely the rule that was broken.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- A round that emits a new Python event kind adds the matching key in
  `apps/ui/src/api/humanizeCatalog.ts` in the SAME commit and gates
  `tests/ui_contracts/test_humanize_catalog.py`; the two sets are pinned EQUAL
  and neither may move alone (DECISION F022 D1).
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.

This order's own constraints:

- No new STATUS line was registered: every finding had an owning feature file,
  so the registration protocol (Package 1 line, TOTAL_FEATURES pin, README
  counter in one commit) was not entered.
- A test that asserts which model a provider DEFAULTS to reads the id from
  `MODEL_ALIASES`; spelling it makes the test assert a string instead of the
  contract, and an alias repoint then fails a test that nothing broke.
- `remedy plan next` reports F031, not F022. F022 closed on 2026-08-23 with
  pull request #213; the operator's expectation of F022 predates that merge.
