# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- R-0200 (registered in F079, deferred unbuilt): closure evidence
  cannot yet prove a specified verb was actually CALLED — the
  gate-tooling half of the F070 acceptance gap. The reviewer-practice
  half is landed (docs/agents/reviewer_conventions.md,
  specified-route-exercised rule). Any build order should cite that
  rule. Source: F075 R4 diagnosis → F079 R1 registration → deferred
  through F079 closure · 2026-08-06.
- R-0202 (registered in F079, deferred unbuilt): the mid-run UI
  rebuild class — REMEDY_UI_NO_AUTO_BUILD=1 was once ignored by a
  spawned server/build path (R-0169, F069 R2; recurred F075 R12).
  Did NOT recur in the F079 R3 gate (dist hashes identical on both
  sides), but one clean gate is not the env-var hunt; the mechanism
  is still unexplained. integration_gate.md carries the operational
  mitigation. Source: F075 R12 gate → F079 R1 registration ·
  2026-08-06.
- xdist flake, single id: tests/orchestration/
  test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogical
  Identity::test_different_execution_identities_same_logical_hash
  failed once in the reviewer's parallel full-suite run at F079 R3,
  passed serially (file: 11/11) and the file is untouched by F079
  (0 commits in range). F135 flaky-detector territory; 1 id, far
  under the 10-id flake-debt threshold. Source: F079 R3 gate,
  reviewer run · 2026-08-06.
