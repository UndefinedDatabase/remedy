# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 51 lands the first group of DECISION F275 D29's P2 and registers `R-0877`, the defect
it repairs. `timeline.append_run_event` and `test_failure_artifact.emit_failure_events`
coerced their `job_id` with `UUID(str(job_id))`, which rejects the sixteen hex characters
`data_paths.mint_job_id` produces — and for an unhyphenated 32-hex id wrote a directory the
reader in the same module never looked in. Both now join the id verbatim, as
`data_paths.run_log_dir` already did. The round 50 PASS verdict is booked here.

## Next Steps

1. P2's remaining groups — the surviving `UUID(...)` coercions over a job or task id that
   are NOT dual-shape normalisers, landed one assignment-connected component per commit as
   DECISION F275 D28 rules for an id widen.
2. P1 — replace the transform's receiver-NAME heuristic with the DECISION F272 D7
   raising-property probe `docs/roadmap/features/T2_F275.md` T002 already orders. The probe
   and its site set exist at `0b009325` in `.agent/f275_t002_flip_inventory.md`; T003
   re-derives them at its own base, as that file says it must.
3. P3 — the `**` splat call-graph pass over the test helper factories.
4. Re-run the dry run, then THE FLIP as the one declared-oversize commit AGENTS.md permits
   per feature, declared with its inseparability reason before review.
5. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
6. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: the session writes the scope report and CONTINUES.
- The open set is 87 by distinct id once this round registers `R-0877`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
