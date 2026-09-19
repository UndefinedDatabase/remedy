# Handoff — F271 No more legacy: ownership, reachability, replace-is-delete · Round 5

## Session

SESSION 1 of feature F271 · round 5 · rounds so far 5

Context self-assessment: the worker read the block, AGENTS.md, the closure protocol's preconditions 3, 6 and 7, algorithm steps 1 and 2 with pitfalls (a) to (e), the canonical zip sequence, and F270's round 6 recipe (commit `6b08a96f`, `.agent/selfuse_f270/`, the integrity file, the scripts and summaries under `.remedy-wt/f270-r6/` and `.agent/authored/f270-r6-*`); every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of 10300cdd..HEAD — branch `feature/f271-no-more-legacy`.

## Summary

Round 5 is closure round A.
- C1 books round 4's PASS and rewrites the plan.
- C2 generates self-use item SU-022 and runs it to the approval gate without applying it. The run ended `stopped` with `Stop Reason: budget_exhausted:max_provider_calls`. `describe_self_use_run_defects` returned an empty tuple.
- C3 records the integrity check: passed, 5 checks, 0 failing.
- C4 records evidence job `f271r5e1001` and the review package. The package reads READY_FOR_REVIEW, and its manifest names the accepted HEAD `b54c7fb9`.

## Commits

### 98dd294c F271 R5 C1: book round 4's PASS, rewrite the plan for closure round A, and save the round 5 payload and block copies
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-r5-block.md` | +90 / -0 | Byte copy of the block |
| `.agent/authored/f271-r5-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f271-r5-plan.md` | +24 / -0 | Byte copy of plan.md |
| `.agent/live_review.md` | +2 / -0 | `10300cdd` bytes + ledger.md (Gate F271 R4, VERDICT PASS) |
| `.agent/plan.md` | +7 / -9 | := plan.md |

125 insertions, 9 deletions (`git show --numstat`).

### 5781a607 F271 R5 C2: closure precondition 6 — generate SU-022, run it to the approval gate, record the evidence
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/selfuse_f271/SU-022.md` | +7 / -0 | The job file the runner wrote |
| `.agent/selfuse_f271/entry_and_job_file.txt` | +5 / -0 | SU-022, tier 1 for R-0445, `consumed_by` empty |
| `.agent/selfuse_f271/execution_config.txt` | +7 / -0 | Builder and reviewer both ollama, 2 repair rounds, 3 max rounds, worktree isolation |
| `.agent/selfuse_f271/full_transcript.txt` | +24 / -0 | Job `da3ab3c54d404e25`, stopped |
| `.agent/selfuse_f271/result_state.txt` | +8 / -0 | The run's `result_state` |
| `.agent/selfuse_f271/run_defects.txt` | +3 / -0 | `describe_self_use_run_defects` output: `(empty tuple)` |
| `scripts/self_use_queue.json` | +8 / -0 | The generator's SU-022 entry, `consumed_by` empty |

62 insertions, 0 deletions.

### b54c7fb9 F271 R5 C3: closure precondition 3 — the integrity check reads passed, five checks, none failing
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-integrity-check.txt` | +33 / -0 | `export_integrity_json(run_integrity_checks())` with a final newline, in F270's shape |

33 insertions, 0 deletions.

### 69c6fe6a F271 R5 C4: closure round A — evidence job f271r5e1001 and the review package READY_FOR_REVIEW at the accepted HEAD
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-r5-evidence-summary.txt` | +50 / -0 | The evidence job, in F270's shape |
| `.agent/authored/f271-r5-zip-output.txt` | +33 / -0 | The zip build, in F270's shape |

83 insertions, 0 deletions.

### C5 (this commit) F271 R5 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 125.

## External actions

- `git push origin feature/f271-no-more-legacy` after C3: `10300cdd..b54c7fb9`, not forced. The tip equals origin (G3).
- The self-use run (`run_job` with worktree isolation) created the worktree `.remedy-wt/job-da3ab3c54d404e25` on a new branch, `remedy/job-da3ab3c54d404e25`. Its `git status --porcelain` was empty and its HEAD was `98dd294c` (C1). Following the F268 to F270 precedent, the worker removed it after the run with `git worktree remove --force` and kept the branch. The `remedy/job-*` count was 34 before the run and 35 after it.
- The evidence script `.remedy-wt/f271-r5/create_f271_evidence.py` wrote `.remedy-wt/f271_evidence_round5`, which is not committed.
- `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f271_evidence_round5` ran once and produced one package, READY_FOR_REVIEW on the first attempt. The package was left where the script built it.
- After this commit: `git push origin feature/f271-no-more-legacy`. No pull request is opened this round.

## Verification

Each exit code was read through `.remedy-wt/f271-r5/w_run.py`, which writes the output to a file and prints `EXIT <returncode>`.

- **Transport**, before any write: `sha256sum` matched all three digests: block.md `fa63d18efd11fe66ed1868ff8c6545d77f421523b5a08139c79d15648e57aa16`, ledger.md `a652d7d9a65b3b2e71528ab643a9511267be2f23a6ed1c49cb0d16d09fe16d4f`, plan.md `24ad4d5cd7d0a5a340773592d0ece3e62741368faee8f95ada4eb46350aafb0c`.
- **G1** (after C1): `python3 .remedy-wt/f271-r5/w_g1.py`, EXIT 0:
  ```
  payload digests matched: True
  live_review == 10300cdd bytes + ledger.md: True
  .agent/plan.md == plan.md: True
  .agent/authored/f271-r5-ledger.md == payload: True
  .agent/authored/f271-r5-plan.md == payload: True
  .agent/authored/f271-r5-block.md == payload: True
  all: True
  block copy sha256: fa63d18efd11fe66ed1868ff8c6545d77f421523b5a08139c79d15648e57aa16
  ```
- **G2** (after C1): `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py`, EXIT 0: `382 passed in 41.76s` (0 failed).
- **Self-use run**: before it, `next_self_use_item()` printed `None`. `python3 .remedy-wt/f271-r5/run_selfuse.py`, EXIT 0: `generate_and_append_if_empty -> SU-022`, job `da3ab3c54d404e25`, `"state": "stopped"`, `"defects": []`. The `result_state`, verbatim:
  ```
  Job State: stopped
  Stop Reason: budget_exhausted:max_provider_calls
  Stop Source: budget
  Stop Request ID: budget_0938c70cab7ca328
  Stopped At: 2026-09-19T00:51:37.922410+00:00

  Task States:
    T001: stopped (verdict: )
  ```
  `describe_self_use_run_defects` returned the empty tuple, so there is no defect string to quote. As the block ordered, nothing is registered in the ledger.
- **G3** (at C3, after the push): `python3 .remedy-wt/f271-r5/w_g3.py`, EXIT 0:
  ```
  passed: True fail_count: 0 [('handler_import', 'pass'), ('live_review_verdict', 'pass'), ('plan_consistency', 'pass'), ('relevant_untracked', 'pass'), ('high_blockers_open', 'pass')]
  git status --porcelain lines: 0
  HEAD: b54c7fb9519ceeddb37e7988a6304dce8117010d
  origin: b54c7fb9519ceeddb37e7988a6304dce8117010d
  G3: True
  ```
- **G4** (C4, from a clean tree at C3):
  - `git rev-list --ancestry-path --count a4f79a94056283ec59da3cf56624001171f96fbd..b54c7fb9519ceeddb37e7988a6304dce8117010d` printed `20`. `git rev-list --count` over the same range printed `20`. `git merge-base main b54c7fb9` printed `a4f79a94056283ec59da3cf56624001171f96fbd`.
  - `python3 .remedy-wt/f271-r5/create_f271_evidence.py`, EXIT 0: `Collected 131 node IDs after deselection`, `Test results: 131 passed, 0 failed, 0 skipped`, `is_valid_current_run: True`, `validation_errors: []`.
  - `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f271_evidence_round5`, EXIT 0: `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`.
  - `python3 .remedy-wt/f271-r5/verify_zip.py`, EXIT 0: `head_commit: b54c7fb9519ceeddb37e7988a6304dce8117010d`, `base_commit: a4f79a94056283ec59da3cf56624001171f96fbd`, `head_commit == C3: True`, `package_status: READY_FOR_REVIEW`, `sha256: 078c50ba3ce10d8739198ff6242faf84c285df119d52f7b078dce3c9869c39dc`. The sandbox blocked `sha256sum` on the package path (see Deviations).
  - After the zip, `git status --porcelain` printed nothing.

Closure values, spelled exactly as the tools printed them:
1. Evidence job id: `f271r5e1001`
2. Package filename: `remedy-review-20260919-025357-READY_FOR_REVIEW.zip`
3. SHA-256: `078c50ba3ce10d8739198ff6242faf84c285df119d52f7b078dce3c9869c39dc`
4. Package path: `/home/decodeux/Repos/remedy-history/zips` (NOT ARCHIVED; the package was left where it was built)
5. Accepted HEAD: `b54c7fb9519ceeddb37e7988a6304dce8117010d`
6. Self-use item id: `SU-022`

## Authored-text proofs

- The copies `.agent/authored/f271-r5-{ledger.md,plan.md,block.md}` equal their payloads byte for byte (G1). The block copy's sha256 is `fa63d18efd11fe66ed1868ff8c6545d77f421523b5a08139c79d15648e57aa16`.
- `.agent/live_review.md` was built by python from `git show 10300cdd:` bytes plus ledger.md, and `.agent/plan.md` from plan.md alone. Both byte checks are `True` (G1).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `98dd294c`, the block copy included |
| C2 self-use item | done | `5781a607`: SU-022 stopped on `budget_exhausted:max_provider_calls`, the defect tuple empty, `consumed_by` not set |
| C3 integrity check | done | `b54c7fb9`: passed, 5 checks, 0 failing, pushed |
| C4 evidence job and zip | done | `69c6fe6a`: `f271r5e1001`, READY_FOR_REVIEW on the first attempt |
| C5 handoff and push | done | This commit, then the push |
| G1, G2, G3, G4 | done | All EXIT 0 |

## Open findings

This count is by distinct id on the committed `.agent/live_review.md` at C4, from `python3 .remedy-wt/f271-r4/w_count.py`: `registered 136 done 6 done within registered 6 open 130`. That is the same as at round 4, since this round registers no finding.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1, C2, C3, the push, C4, C5, the push. There is no extra commit.
- **Package hash tool:** the sandbox refused `sha256sum` on `/home/decodeux/Repos/remedy-history/zips/...`, because that path is outside the allowed working directory. The digest came from Python's `hashlib.sha256` over the package bytes in `verify_zip.py`. It equals the `final_sha256` the zip script printed.
- **Integrity file:** `export_integrity_json` output with a final newline added, which matches the trailing bytes of F270's `.agent/authored/f270-integrity-check.txt`.
- **Evidence run id:** `vr-1113`, one past F270's `vr-1112`. The block does not name a run id, and `vr-1113` matches `^vr-\d{4,}$`.
- **Evidence partition:** the producer split the 15 authoritative files as T001=5, T002=5, T003=5, even though `step_range` is `T001-T002`. F269 and F270 show the same pattern. This is how the producer behaves; the worker did not change it.
- **Observation, not registered:** SU-022 is again the R-0445 tier-1 item, the fourth in a row after SU-020 and SU-021, because R-0445 is still the oldest open Medium or Low finding. The run stopped on the provider-call budget. It did not reach the completion gate the way F270's run did, and `describe_self_use_run_defects` returns nothing for a `stopped` job, even one stopped by its budget. The reviewer can decide whether that empty tuple is a blind spot.
- **Scratch:** all scratch files are gitignored and sit under `.remedy-wt/f271-r5/`: `w_c1.py`, `w_g1.py`, `w_g3.py`, `w_run.py`, `run_selfuse.py`, `integrity.py`, `create_f271_evidence.py`, `verify_zip.py`, and the output captures `g1.txt`, `g2.txt`, `g3.txt`, `queue_probe.txt`, `selfuse_out.txt`, `integrity_out.txt`, `evidence_out.txt`, `zip_out.txt` and `verify_zip.txt`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The review of round 5.
3. Closure round B: the verdict bookings, the self-use result (SU-022 has no defect string to register), the ledger rotation, the closure commit with the STATUS line, the README counters and SU-022's `consumed_by` set to F271, and then the pull request.

Operator questions open: 5
