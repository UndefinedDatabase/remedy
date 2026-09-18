# Handoff — F268 remedy do: the one-command start · Round 12 (closure: repair 1 and round A)

## Session

SESSION 2 of feature F268 · round 12 · rounds so far 12

## Range

Review of 205b10a5..HEAD — branch `feature/f268-remedy-do`.

## Summary

Round 12 did the following:

- C1 booked round 11's PASS.
- C2 repaired all three bad nodes of the closure suite (repair round 1 of at most three). The bad set shrank from 3 to 0 and no node became newly bad in the files the block named.
- C3 to C5 ran closure round A:
  - the self-use item (precondition 6)
  - the integrity check (precondition 3)
  - the evidence job (algorithm step 1)
  - the review zip (algorithm step 2)

The package is READY_FOR_REVIEW. Its manifest's `committed_review_subject.head_commit` equals C4.

**Values round B quotes, spelled exactly as the tools printed them:**

1. Evidence job id: `f268r12e1001`
2. Package filename: `remedy-review-20260918-140632-READY_FOR_REVIEW.zip`
3. SHA-256: `2c4ed9fa9d3c2e762dbf19a069cc378dfc7c46d973f9334e656f4dc9e873d86a`
4. Package path: `NOT ARCHIVED` (the package was not moved and stays where `make_review_zip.sh` built it, `REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips`)
5. Accepted HEAD: `5883bccb2b2d4362815215c6a24a71b67f9016f9`
6. Self-use item id: `SU-019`

**Self-use defects.** `describe_self_use_run_defects` returned these strings for the run's `JobPlan` (job `fcba47b830c24c89`, state `blocked`), verbatim. The reviewer registers them. No finding was written into `.agent/live_review.md` and `consumed_by` is not set.

1. `job fcba47b830c24c89 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`
2. `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`

**Observation for the reviewer (not registered).** Tier 1 of `generate_and_append_if_empty` produced SU-019 from R-0445. That is the same finding F266's SU-018 already carried (`consumed_by: "F266"`), because R-0445 is still open in the ledger. SU-019's text is identical to SU-018's. So each closure keeps regenerating R-0445 until it gets a `Done:` line.

## Commits

### 12068ead F268 R12 C1: bookkeeping — book round 11's verdict, round 12 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r12-block.md` | +102 / -0 | Byte copy of the block |
| `.agent/authored/f268-r12-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f268-r12-plan.md` | +23 / -0 | Byte copy of plan.md |
| `.agent/live_review.md` | +2 / -0 | `205b10a5` bytes + ledger.md (Gate F268 R11 PASS) |
| `.agent/plan.md` | +6 / -7 | := plan.md |

### fa8f9703 F268 R12 C2: repair 1 — the three segment-manifest wiring guards read do_sequence, where round 1 moved the call sites
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_prompt_trace.py` | +8 / -8 | Changes, by design: <br>• The three `TestSegmentManifest` guards now import `packages.orchestration.do_sequence as do_sequence` instead of `apps.cli.commands.do_cmd as do_cmd`. <br>• Every asserted string is unchanged. <br>• Two docstrings no longer say "CLI": the first guard's (":262") and the builder guard's reference to "the CLI guards above" (":390"). Both now name `do_sequence`. |

### 1be1950d F268 R12 C3: closure precondition 6 — generate SU-019, run it to the approval gate, record the evidence
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/selfuse_f268/SU-019.md` | +7 / -0 | The job file `plan_next_self_use_item` rendered |
| `.agent/selfuse_f268/entry_and_job_file.txt` | +5 / -0 | Queue entry and job-file path |
| `.agent/selfuse_f268/execution_config.txt` | +7 / -0 | Providers (ollama / ollama), rounds, isolation |
| `.agent/selfuse_f268/full_transcript.txt` | +24 / -0 | Job and task summary |
| `.agent/selfuse_f268/result_state.txt` | +8 / -0 | Job and task states |
| `.agent/selfuse_f268/run_defects.txt` | +4 / -0 | The two `describe_self_use_run_defects` strings |
| `scripts/self_use_queue.json` | +8 / -0 | SU-019 appended by the generator, `consumed_by: ""` |

### 5883bccb F268 R12 C4: closure precondition 3 — the integrity check reads passed, five checks, zero failures
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-integrity-check.txt` | +33 / -0 | `export_integrity_json(run_integrity_checks())`, F266's shape |

### 4ef52e4d F268 R12 C5: closure steps 1 and 2 — evidence job f268r12e1001 and a READY_FOR_REVIEW package at 5883bccb
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r12-evidence-summary.txt` | +53 / -0 | Evidence job summary, F266's shape |
| `.agent/authored/f268-r12-zip-output.txt` | +33 / -0 | Zip build output, F266's shape |

### C6 (this commit) F268 R12 C6: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 135.

## External actions

- `git worktree add .remedy-wt/f268-r12-mut fa8f9703`, for the G2 mutation. Removed afterwards with `git worktree remove --force`.
- The self-use run (`run_job`, isolation worktree) created the worktree `.remedy-wt/job-fcba47b830c24c89` on the new branch `remedy/job-fcba47b830c24c89`.
  - Its cleanup status was `retained`.
  - I removed that worktree with `git worktree remove --force` after C3 so that G6 reads one row.
  - The branch was kept.
- `git push origin feature/f268-remedy-do` after C4: pushed C1 to C4, and the tip equalled origin at `5883bccb`.
- `git push` after C5: tip `4ef52e4d` equals origin.
- `git push` after C6 (this commit).
- `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f268_evidence_round12`: one attempt, READY_FOR_REVIEW.
- No PR and no gh action.

## Verification

- **G1** (after C2), exit 0:
  - Transport: the block's digest was `2ccd13cd41fe2067574c89d1cc94af9ad4a9abf16eb4fa28e0e0cb7d08d7e61e`. ledger.md was `9b923d5cd901d312eae80588c23ba31c710917cb8a198e1f17b58b40750bc536` and plan.md was `5c6363bf86c68c2b4b86a790e5f6b7506088bd502419bfda44db396dfbb39062`. All three matched.
  - The python byte check printed `True` for `.agent/live_review.md` == `git show 205b10a5:.agent/live_review.md` + ledger.md.
  - It printed `True` for `.agent/plan.md` == plan.md.
- **G2** `python3 -m pytest -q -p no:cacheprovider` over the three node ids in `f268-closure-suite.txt`, exit 0: `3 passed in 0.27s`.
  - Over `tests/orchestration/test_prompt_trace.py tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py`, exit 0: `121 passed in 63.57s (0:01:03)`, so 0 failed.
  - Mutation red-proof in the worktree `.remedy-wt/f268-r12-mut` at `fa8f9703`:
    - `find … -name __pycache__` found none, since the checkout was fresh. Runs used `python3 -B`.
    - The imported module was `/home/decodeux/Repos/remedy/.remedy-wt/f268-r12-mut/packages/orchestration/do_sequence.py` in both the control and the mutated run.
    - Control: `test_every_cli_call_site_hands_its_composition_down` gave `1 passed in 0.30s`.
    - Mutation: `composed=plan_composed,` (1 occurrence) became `composed=None,`, and `git diff --stat` showed `1 insertion(+), 1 deletion(-)`. Result: `FAILED …::test_every_cli_call_site_hands_its_composition_down`, `tests/orchestration/test_prompt_trace.py:336: AssertionError`, `1 failed in 0.29s`.
    - The worktree was removed.
- **G3** `python3 -m ruff check tests/orchestration/test_prompt_trace.py`, exit 0: `All checks passed!`
- **G4** (after C4):
  - `run_integrity_checks()`: `passed True fail_count 0`. All five checks read PASS: `handler_import` (handlers=147), `live_review_verdict`, `plan_consistency` (unchecked=0), `relevant_untracked` (untracked=0, relevant=0) and `high_blockers_open` (no open blocker/high findings).
  - `git status --porcelain` was empty.
  - `git rev-parse HEAD origin/feature/f268-remedy-do` printed `5883bccb2b2d4362815215c6a24a71b67f9016f9` twice.
- **G5** (C5, from a clean tree at C4):
  - Fork point `git rev-parse 8e075bbe` = `8e075bbeb5ef572b4f92738c4c4a07847c642f63`. `git rev-list --ancestry-path 8e075bbe..5883bccb… --count` gave `67` and `git rev-list 8e075bbe..5883bccb… --count` gave `67`. There are no merges in the range, and `git merge-base HEAD origin/main` = `8e075bbe…`.
  - Evidence script, exit 0: `Collected 251 node IDs after deselection`, `Test results: 251 passed, 0 failed, 0 skipped`, `is_valid_current_run: True` and `validation_errors: []`.
  - Summary: `authority_count 61`, `commit_count 67`, verdict `PASS_WITH_RISKS`, `total_passed 251`.
  - Zip script: `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, member_count 4451.
  - Read out of the package's `.review_zip_manifest.json` → `committed_review_subject`: `head_commit 5883bccb2b2d4362815215c6a24a71b67f9016f9` (`== C4: True`) and `base_commit 8e075bbeb5ef572b4f92738c4c4a07847c642f63`.
  - Package SHA-256 `2c4ed9fa9d3c2e762dbf19a069cc378dfc7c46d973f9334e656f4dc9e873d86a`, computed by python `hashlib.sha256` over the file; see Deviations. It equals the zip script's own `final_sha256`.
- **G6** after the C6 push: the round report carries it. After the C5 push, `git rev-parse HEAD origin/…` printed `4ef52e4d843afaed9dcfd4484157c1bc49f792f4` twice. The `remedy/job-*` branch count was `31` before C3 and `32` after the self-use run.

## Authored-text proofs

- Byte copies are at `.agent/authored/f268-r12-{block,ledger,plan}.md`. Their sha256 values equal the payload digests above. The block copy's digest is `2ccd13cd41fe2067574c89d1cc94af9ad4a9abf16eb4fa28e0e0cb7d08d7e61e`.
- `.agent/live_review.md` and `.agent/plan.md`: byte checks `True` (G1).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `12068ead` |
| C2 repair 1 | done | `fa8f9703`; bad set 3 → 0 |
| C3 self-use item | done | `1be1950d`; SU-019, job `fcba47b830c24c89` blocked at `repair_exhausted` |
| C4 integrity check | done | `5883bccb`; passed |
| C5 evidence job and zip | done | `4ef52e4d`; READY_FOR_REVIEW |
| C6 handoff | done | This commit |

## Open findings

125 open by distinct id, from `.remedy-wt/f268-r4/count.py`: HEAD has 140 registrations and 15 `Done:` ids. This is unchanged. This round opens and resolves no finding; the two self-use defect strings wait for the reviewer.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1 to C6). No extra repair commit.
- **The evidence script's first run was discarded.** F266's collect-only parser drops every line containing "passed", "failed", "skipped", "error" or "==". That dropped five real node ids whose test names contain those words, which gave 246 ids against 251 passed (pitfall (a)).
  - The five were `test_an_unknown_project_exits_1_with_the_init_step_failed_and_no_mission`, `test_a_cockpit_that_does_not_come_up_is_skipped_and_the_walk_ends_at_apply`, `test_a_job_whose_cost_mirror_failed_is_named_not_counted_as_zero`, `test_missing_job_returns_error` and `test_the_finalize_step_leaves_no_error_file`.
  - The parser now keeps every `tests/…::…` line and exits if the count differs from pytest's `N tests collected`.
  - The script now also prints `is_valid_current_run` and `validation_errors` from `scripts/build_review_manifest.py::validate_evidence_candidate`.
  - The bundle was rebuilt before any zip was attempted. No zip was built from the discarded bundle.
- **Test count.** The block stated `208 passed` for the seven files other than `test_prompt_trace.py`. The run read 251 over eight files, which is consistent with `test_prompt_trace.py`'s 43.
- **SHA-256 via python.** The shell guard refuses `sha256sum` on a path outside the repository, so the digest was taken with `hashlib.sha256`. It is identical to the zip script's printed `final_sha256`.
- **Package manifest member.** `committed_review_subject` lives in the package's `.review_zip_manifest.json`.
- **Self-use job worktree removed.** `run_job` left `.remedy-wt/job-fcba47b830c24c89` retained. It was removed so that G6's `git worktree list` reads one row. The `remedy/job-fcba47b830c24c89` branch is kept (count 31 → 32).
- **`execution_config.txt` fields.** The file records the `ExecutionConfig` fields the run returned. `builder_model` and `reviewer_model` are empty in the JobPlan. F266's `Timeout` and `Context Strategy` lines were omitted because the JobPlan carries no such field.
- **The shell guard refuses `$?`.** Exit codes are therefore the tool's own report; no gate returned non-zero except the deliberate mutation run.

## Next

Reviewer: review round 12 and book its verdict. Register the two self-use defect strings under the standard rules. Then closure round B: `consumed_by` for SU-019, the ledger rotation, the finding owners, and the STATUS line and README in one commit, followed by the PR.
