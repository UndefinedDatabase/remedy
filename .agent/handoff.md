# Handback — F080 R3 (closure part 1) — BLOCKED at the review zip

Branch: feature/f080-roadmap-mirror @ bd73aaa673eff20469daf199f698ce6abccf635a,
pushed, worktree clean. Parts A, B and C are done and green. Part D is
half done: the evidence bundle built clean, **the review zip build
FAILED**. Per STATUS_closure_protocol.md step 2 a failing zip is a
CLOSURE BLOCKER, so F080 does NOT close this round. No STATUS edit, no
README edit, no PR — as instructed, and now also because closure is
blocked.

## THE BLOCKER (raw)
    $ bash scripts/make_review_zip.sh --evidence-dir <scratch>/remedy-job-evidence-f080-closure
    UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
    Evidence refresh completed for staged copy.
    Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
    WARNING: Evidence validation failed (is_valid_current_run=false).
    Zip will be built anyway — reviewer will see validation status in manifest.
    REVIEW_ZIP_ERROR: ReviewSubjectError: review_subject commit[4] subject is missing, too long, or carries a secret/path/control

    REVIEW_ZIP_ERROR: coordinator failed to build/publish the review ZIP (exit 2).
    No public intermediate ZIP was created; nothing to clean up.
    EXIT=2
No zip was published; nothing to record as package/SHA-256.

### Diagnosis (mechanical, reproducible)
commit[4] of the base..HEAD chain (0-indexed) is **1e1f4352**, subject:

    feat(f080): remedy plan status / plan next (T001)

    $ python3 -c "from packages.orchestration.run_manifest import _contains_local_path; \
                  print(_contains_local_path('feat(f080): remedy plan status / plan next (T001)'))"
    True
    probe : 'feat(f080): remedy plan status / plan next (T001)'
    scrub : 'feat(f080): remedy plan status [path]/path plan next (T001)'

Chain: review_subject.validate_review_commit_schema → _metadata_is_safe
→ run_manifest._contains_local_path → failure_postmortem.safe_text. The
` / ` between two words is read as a local path, so the subject fails
the packaging metadata scan. This is exactly the AGENTS.md
commit-subject rule ("no leading-slash tokens, absolute paths… the
evidence-packaging metadata scanner rejects such subjects and blocks
closure. Learned 2026-07-23: one such subject blocked the F081 closure
for several rounds"). The subject is MINE, written in R1 — no round
prompt authored it. All 15 other subjects in the range pass.

### Why I did not fix it myself
The only fix is rewording 1e1f4352, i.e. rewriting reviewed history
(commits 5-16 all get new shas) and force-pushing. That invalidates the
R1 range 1da1b07a..6787d6cf, the R2 range 6787d6cf..84cd2797 and
LAST_REVIEWED_SHA 84cd2797, all of which the live review cites, and
force-push is outside the guardrails. Operator/reviewer decision.
Once a decision exists: reword → rebuild the bundle at the new HEAD
(the bundle pins bd73aaa6) → rebuild the zip → R4.

## Changed files per commit
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 1b79d42e | .agent/live_review.md | +75/-30 | authored R2 PASS verdict persisted |
| 1b79d42e | docs/roadmap/features/T2_F083.md | +11/-0 | R-0205 class routed (DECISION D3) |
| 1b79d42e | .agent/plan.md, .agent/context.md | rewrite | R3 closure-part-1 state |
| 1b79d42e | .agent/authored/f080-r3-{1,2,3}.md | +174 | receipts (see deviation below) |
| bd73aaa6 | docs/roadmap/features/T1_F080.md | +59/-0 | Built State — precondition 4 |
| (final) | .agent/plan.md, .agent/handoff.md | rewrite | blocker + this handback |

Deviation (declared): `git add -A` on the Part A commit swept
.agent/authored/f080-r3-2.md in one commit EARLY — it is applied in
Part B (bd73aaa6), not Part A. The receipt content and hash are
unaffected; only its commit placement deviates from "commit each
receipt with the commit that applies it". Not fixable without history
rewrite.

## Authored-text receipts (R-0148) — all three matched first try
| File | Computed sha256 | Match |
|---|---|---|
| f080-r3-1.md | b9de06f542caa5fafbce5049763ca94a7d53fa49846d7e4219be13475290f3cf | yes |
| f080-r3-2.md | 02587bf4cc196c1fb71a6f3bc59963254709020ae9beda6dc253ea07c052d839 | yes |
| f080-r3-3.md | ed4a78a7bbb434e184ceaba712a8c99e73642e2160968713fb47774b003b0c89 | yes |
No wrap damage this round; no recovery needed.

## Verification transcripts
    # PART A
    python3 -m pytest tests/docs/ -q                                -> 0 · 293 passed in 0.19s
    python3 -m pytest tests/ui_server/test_dashboard_contract.py -q -> 0 · 70 passed in 3.45s
    python3 -m pytest tests/regression/test_resource_safety.py -q   -> 0 · 21 passed in 10.83s
    # PART B
    python3 -m pytest tests/docs/ -q                   -> 0 · 293 passed in 0.19s
    python3 -m pytest tests/cli/test_golden_path.py -q -> 0 · 42 passed in 15.20s
    # PART C — closure preconditions
    git status --porcelain    -> empty
    git push                  -> 84cd2797..bd73aaa6  feature/f080-roadmap-mirror
    remedy integrity check --json -> exit 0, passed=true, fail_count=0, check_count=5
        handler_import pass (handlers=325) · live_review_verdict pass ·
        plan_consistency pass (unchecked=0) · relevant_untracked pass
        (untracked=0, relevant=0) · high_blockers_open pass
    python3 -m pytest tests/docs/ -q                   -> 0 · 293 passed in 0.19s
    python3 -m pytest tests/cli/test_golden_path.py -q -> 0 · 42 passed in 16.62s
    # PART D — bundle inputs, all run at the accepted HEAD
    python3 -m pytest --collect-only -q                -> 0 · 15960 tests collected
    REMEDY_UI_NO_AUTO_BUILD=1 pytest -n auto -q  (1st) -> 1 · 1 failed, 15940 passed, 19 skipped, 126.68s
    REMEDY_UI_NO_AUTO_BUILD=1 pytest -n auto -q  (2nd) -> 0 · 15941 passed, 19 skipped, 156.03s
    pytest tests/orchestration/test_roadmap_index.py -q            -> 0 · 30 passed
    pytest tests/orchestration/test_feature_mission_adapter.py -q  -> 0 · 29 passed
    pytest tests/cli/test_plan_cli.py -q                           -> 0 · 21 passed
    pytest tests/docs/ -q                                          -> 0 · 293 passed
    pytest tests/cli/test_golden_path.py -q                        -> 0 · 42 passed

### The one red, attributed (integration_gate.md step 4)
The FIRST full-suite re-run at the accepted HEAD failed one id:
`tests/ui_server/test_live_state.py::TestUIServerIntegration::test_server_starts_and_writes_info`.
Captured stderr names the cause outright: "ERROR: React UI not built."
— the R-0169 mid-run UI rebuild racing the UI server, i.e. the class
this feature already carries as R-0202 (routed to T2_F085). The same id
sits in the base_failed lists of the F056, F069 and F075 gates with the
same attribution. Serial proof, all at this HEAD:
    pytest <the exact node id> -q                       -> 0 · 1 passed in 0.18s
    pytest tests/ui_server/test_live_state.py -q        -> 0 · 42 passed in 1.94s
    pytest tests/ui_server/test_live_state.py -n auto -q -> 0 · 42 passed in 1.04s
    full suite re-run                                   -> 0 · 15941 passed, 19 skipped
Serial-pass ⇒ flake/environment class: recorded, not a blocker, and NOT
a new finding — it is R-0202's known class. The bundle's numbers come
from the GREEN run, so nothing claims a passing count from a red run.

## Closure preconditions 1-5 (STATUS_closure_protocol.md)
1. Every step has a PASS round; verdicts R1 PASS, R2 PASS; findings
   R-0200/R-0202/R-0204/R-0205 all Resolved or routed — live_review.md.
2. Full suite green, re-confirmed at the accepted HEAD: exit 0, 15941
   passed, 19 skipped (raw above); the dedicated R2 integration gate
   PASSed with zero branch-only failures (.agent/gate_f080_r2/).
3. `remedy integrity check --json` → passed=true, fail_count=0,
   untracked=0, relevant=0.
4. Built State current in docs/roadmap/features/T1_F080.md as of
   commit bd73aaa6 (a content commit, not the closure commit).
5. Working tree clean, branch pushed, worker idle.
All five hold. The blocker is packaging, not the feature.

## Evidence bundle — BUILT and reusable (only the zip is missing)
- Evidence job id: **f080-closure**
- Producer: `job_evidence.create_manual_completion_bundle(review_feature_id="f080", …)`
- Location (OUTSIDE the repo, never committed, per DECISION 2026-08-01):
  `<session scratch>/remedy-job-evidence-f080-closure` (2.6 MB)
- Summary: head bd73aaa673eff20469daf199f698ce6abccf635a, authority 16
  files, partition T001 6 / T002 6 / T003 4, commit_count 16,
  verdict PASS_WITH_RISKS, manual_completion True, total_passed 16356.
- Gate set present and coherent: final_verifier_report PASS_WITH_RISKS,
  fresh_evidence_gate PASS, artifact_contract_gate PASS,
  change_provenance_gate PASS, runtime_integration_gate PASS,
  manifest_integrity ok, postmortem_integrity ok, commit_execution_gate
  NEEDS_HUMAN_APPROVAL, verification_tests + token_truth written.
- Every producer pitfall satisfied at authoring time: run_ids
  vr-0001..vr-0006 (`^vr-\d{4,}$`); output_hash left to the producer's
  sha256(stdout_summary); full-length base_commit
  1da1b07a427c4518f21b5698dacfd5ab37f55c4a; node ids from
  `--collect-only` with len(node_ids) == selected == passed+skipped for
  every run (15960 / 30 / 29 / 21 / 293 / 42); every test_files entry
  asserted to be an existing FILE before the call.
- Caveat for R4: the bundle pins HEAD bd73aaa6. If the blocker is
  resolved by rewording 1e1f4352, the bundle must be rebuilt at the new
  HEAD (the build script is in session scratch as build_bundle.py).

## Values R4 needs (all present except the package)
- accepted HEAD (full): bd73aaa673eff20469daf199f698ce6abccf635a
- base: 1da1b07a427c4518f21b5698dacfd5ab37f55c4a
- evidence job: f080-closure
- package + SHA-256: **NOT AVAILABLE — zip build failed (see above)**

## Open findings
- 1 blocking: the commit-subject packaging blocker above. No R-id spent
  — per the closure protocol, findings raised during a closure round are
  CANDIDATES; the reviewer registers or resolves it next round. Not
  written to .agent/candidates.md because that file is a CLOSURE-COMMIT
  vehicle and this round has no closure commit.
- Next free id: R-0206.

## Next expected action
Reviewer/operator rules on the reword-and-force-push question, then a
repair round: reword → rebuild bundle → rebuild zip → R4 closure.

## Item status
| Item | Status | Reason |
|---|---|---|
| Part A verdict + R-0205 routing | done | commit 1b79d42e, all three receipts matched |
| Part B Built State | done | commit bd73aaa6, both gates green |
| Part C preconditions | done | 1-5 all hold, evidence recorded above |
| Part D evidence job | done | f080-closure, full gate set, green numbers |
| Part D review zip | BLOCKED | ReviewSubjectError on commit[4] subject; raw error recorded |
| Handback | done | clean worktree, pushed, this file |
