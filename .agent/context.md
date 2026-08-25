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

## Constraints
- No new STATUS line was registered: every finding had an owning feature file,
  so the registration protocol (Package 1 line, TOTAL_FEATURES pin, README
  counter in one commit) was not entered.
- `remedy plan next` reports F031, not F022. F022 closed on 2026-08-23 with
  pull request #213; the operator's expectation of F022 predates that merge.
