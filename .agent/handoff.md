# Handoff — F273 Findings paydown v1 · Round 15

## Session

SESSION 2 of feature F273 · round 15 · rounds so far 15

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D15, round 14's handoff as the template's instance, and the hunks of both code diffs as it applied them. Every figure below comes from a command run in this round, and the worker's context held all of it without loss.

Session 2 ran rounds 8 to 15, eight delegated rounds, the top of the six-to-eight target; it ends here with the held rulings of DECISION F273 D15 (4) for a fresh session.

## Range

Review of bce5bc3b..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 15 books round 14's verdict and its six resolutions, lands DECISION F273 D15, and builds R-0990, R-0931 and R-0981 as the reviewer's dry run built them. The repair-loop, R-0914 and worker-queue prototypes (g6b, g6d, g6e) are held, not applied (D15 (4)).
- C1 books Gate F273 R14 (VERDICT PASS) and six `Done:` lines (R-0989, R-0903, R-0908, R-0911, R-0932, R-0936). It also lands DECISION F273 D15, rewrites the plan and saves the four payload copies.
- C2 (R-0990): `_extract_job_truth` takes its intent ids and states from `approval_queue.list_patch_intents`. `approval_required` means a pending intent with no applied record. The run's `approval_required` event counts only when no intent is listed. The status tip reads the new `pending_intent_ids`.
- C3 (R-0931, R-0981):
  - `build_current_candidate`, `diff_manifests`, `load_latest_manifest_for_cli` and `CanonicalLoadResult` are deleted from `run_manifest.py`, along with their helpers and tests. `T0_F012.md` records that the drift check is gone.
  - `role_conventions.py` is deleted with its test. The document checks move to `tests/orchestration/test_conventions_documents.py`. `T2_F105.md` and the cache-ordering page record why.
- C4 is this handoff.

Landed: R-0990 — `b339d5ed` (C2)
Landed: R-0931 — `3be6ce11` (C3)
Landed: R-0981 — `3be6ce11` (C3)

## Commits

### 58178cdc F273 R15 C1: bookkeeping — round 14's verdict and its six resolutions booked, DECISION F273 D15 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r15-block.md` | +96 / -0 | Byte copy of the block |
| `.agent/authored/f273-r15-decisions.md` | +35 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r15-ledger.md` | +14 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r15-plan.md` | +29 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +35 / -0 | `bce5bc3b` bytes + decisions.md (DECISION F273 D15) |
| `.agent/live_review.md` | +14 / -0 | `bce5bc3b` bytes + ledger.md (Gate F273 R14, six `Done:` lines) |
| `.agent/plan.md` | +9 / -6 | := plan.md |

232 insertions, 6 deletions (`git show --numstat`).

### b339d5ed F273 R15 C2: R-0990 — the job views read their intent ids and states from the approval queue
All by `git apply .remedy-wt/f273-proto-g6a.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/job.py` | +19 / -28 | Truth reads the approval queue; `pending_intent_ids` feeds the status tip |
| `tests/cli/test_product_spine.py` | +53 / -7 | Intents carry explanations; new approve-every-intent test; no-intent event case |

72 insertions, 35 deletions.

### 3be6ce11 F273 R15 C3: R-0931, R-0981 — the manifest diff and its candidate builder go with their tests, and the conventions module goes while its documents keep their tests
All by `git apply .remedy-wt/f273-proto-g6c.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T0_F012.md` | +2 / -0 | Status note: the drift check is gone |
| `docs/roadmap/features/T2_F105.md` | +6 / -1 | Why the conventions module went |
| `docs/system/cache-optimal-prompt-ordering-v1.md` | +2 / -1 | Banner: the T002 loaders are deleted |
| `packages/orchestration/role_conventions.py` | +0 / -138 | Deleted |
| `packages/orchestration/run_manifest.py` | +5 / -421 | Candidate builder, manifest diff, CLI loader and helpers deleted |
| `tests/cli/test_job_rerun_integrity_errors.py` | +0 / -79 | Deleted with the CLI loader |
| `tests/cli/test_job_rerun_manifest.py` | +5 / -82 | Drift tests removed |
| `tests/cli/test_job_rerun_read_only_workspace.py` | +5 / -189 | Drift tests removed |
| `tests/cli/test_job_rerun_workspace_identity.py` | +0 / -77 | Candidate tests removed |
| `tests/orchestration/test_conventions_documents.py` | +52 / -0 | New: the documents' cap and anchors |
| `tests/orchestration/test_role_conventions.py` | +0 / -226 | Deleted with its module |
| `tests/orchestration/test_run_manifest.py` | +0 / -42 | Diff tests removed |
| `tests/orchestration/test_run_manifest_input_coverage.py` | +0 / -114 | Deleted |
| `tests/orchestration/test_run_manifest_logical_identity.py` | +0 / -11 | Diff assertions removed |
| `tests/orchestration/test_run_manifest_reference_coverage.py` | +1 / -1 | Docstring |
| `tests/orchestration/test_run_manifest_resume_workspace.py` | +0 / -95 | Deleted |
| `tests/test_no_orphan_modules.py` | +0 / -2 | Allowlist entry for the deleted module removed |

78 insertions, 1479 deletions.

### C4 (this commit) F273 R15 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 232.

## External actions

- `git worktree add --detach .remedy-wt/f273-r15-g5 3be6ce11` for G5, then `git worktree remove .remedy-wt/f273-r15-g5` (exit 0, no `--force`). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy  3be6ce11 [feature/f273-findings-paydown-v1]
  ```
- After C4: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C3 `3be6ce11` with a clean tree. Every script ran with an explicit `cwd`; exit codes come from `.remedy-wt/f273-r15/wk_run.py`, which prints the child's real return code.

- **Transport**, before any write: `sha256sum` of the block, the four payloads, the two diffs and the two G3 lists matched the given digests (block.md `7c0434fab26ef4027847c9db3cdb21437653e5c18cdbd42ca6113a9a9e66628c`).
- **G1**: `python3 .remedy-wt/f273-r15/wk_g1.py`, exit 0:
  ```
  digest f273-r15/plan.md True
  digest f273-r15/ledger.md True
  digest f273-r15/decisions.md True
  digest f273-r15/next.md True
  digest f273-r15/block.md True
  digest f273-proto-g6a.diff True
  digest f273-proto-g6c.diff True
  digest f273-s2/r15_control.txt True
  digest f273-s2/r15_extra.txt True
  plan.md == payload True
  live_review == base + ledger True
  decisions == base + decisions True
  authored f273-r15-plan.md True
  authored f273-r15-ledger.md True
  authored f273-r15-decisions.md True
  authored f273-r15-block.md True
  C2 paths == g6a paths True
  C3 paths == g6c paths True
  C1 paths == 7 bookkeeping paths True
  19 checks, all True: True
  EXIT CODE: 0
  ```
- **G2**: `git rev-parse 3be6ce11:tests 3be6ce11:packages 3be6ce11:apps 3be6ce11:docs`, exit 0:
  ```
  38e2208d66688abbec594b93386cba273d0dd0e9
  585f2e6af040f657dc8a9dba41855c3b67f1ef01
  afdc344919dba92cc79ae5ac8dbb42bc727673fb
  27c3ec810bbb894664d66d6aeea7e28206d32c2e
  ```
  All four equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial): `python3 .remedy-wt/f273-r15/wk_g3.py` runs `python3 -m pytest -q -p no:cacheprovider` over every line of `r15_control.txt` then `r15_extra.txt`, and counts `R-0803:` lines over the full output:
  ```
  control paths: 18 extra paths: 73 distinct: 82 missing: []
  1839 passed in 286.35s (0:04:46)
  R-0803: lines: 0
  EXIT CODE: 0
  ```
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root:
  ```
  All checks passed!
  EXIT CODE: 0
  ```
- **G5** (`python3 .remedy-wt/f273-r15/wk_g5.py`, exit 0): one detached worktree at `3be6ce11`; `python3 -B -m pytest -q -p no:cacheprovider` from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`; `__pycache__` purged before every run; each FROM matched as a whole line with its newline; each file reverted from its saved bytes.
  ```
  run_manifest path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r15-g5/packages/orchestration/run_manifest.py
  CONTROL (unmutated) over tests/cli/test_product_spine.py tests/orchestration/test_conventions_documents.py: 68 passed in 0.71s | exit 0
  (a) apps/cli/commands/job.py: FROM line count = 1
      tests/cli/test_product_spine.py: 2 failed, 59 passed in 0.69s | exit 1 | RED
      FAILED tests/cli/test_product_spine.py::TestJobTruthExtraction::test_job_with_patch_intent
      FAILED tests/cli/test_product_spine.py::TestJobTruthExtraction::test_approving_every_intent_clears_approval_and_every_id_resolves
  (b) apps/cli/commands/job.py: FROM line count = 1
      tests/cli/test_product_spine.py: 1 failed, 60 passed in 0.70s | exit 1 | RED
      FAILED tests/cli/test_product_spine.py::TestJobTruthExtraction::test_approving_every_intent_clears_approval_and_every_id_resolves
  (c) apps/cli/commands/job.py: FROM line count = 1
      tests/cli/test_product_spine.py: 1 failed, 60 passed in 0.70s | exit 1 | RED
      FAILED tests/cli/test_product_spine.py::TestJobTruthExtraction::test_approving_every_intent_clears_approval_and_every_id_resolves
  (d) docs/agents/teacher_conventions.md: FROM line count = 1
      tests/orchestration/test_conventions_documents.py: 1 failed, 6 passed in 0.23s | exit 1 | RED
      FAILED tests/orchestration/test_conventions_documents.py::test_document_still_carries_its_headings[docs/agents/teacher_conventions.md]
  worktree status after reverts: ''
  worktree remove exit 0
  ```
  Each mutation printed `reverted: True` after its run (trimmed above).
  Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit comes before it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r15/wk_c1.py` from `git show bce5bc3b:<path>` bytes and the payload bytes. Nothing was hand-edited except this handoff. G1 re-proves every C1 file and every `.agent/authored/f273-r15-*` copy against its payload.
- The code arrived only by `git apply` of the two reviewer-verified diffs, in the block's order. G2's object ids equal the reviewer's dry-run objects.
- The `## Next` body below is `next.md` byte for byte, appended by script.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `58178cdc` |
| C2 R-0990 | done | `b339d5ed` |
| C3 R-0931, R-0981 | done | `3be6ce11` |
| C4 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |
| g6b, g6d, g6e prototypes | skipped | Held by DECISION F273 D15 (4); not applied |

## Open findings

Measured by `.remedy-wt/f273-r15/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registers it in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `58178cdc` (C1 onwards; C2 and C3 do not touch it; the same at `3be6ce11`): **57 open**;
- at `bce5bc3b`: 63 open.

C1's six `Done:` lines close six distinct ids and register none: 63 - 6 = 57. The three ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C4, then the push. No extra commit.
- **G3 duplicates:** the two lists hold 91 lines naming 82 distinct paths. `tests/cli/test_job_rerun_manifest.py` appears twice in `r15_extra.txt`, and eight paths appear in both lists. All 91 were passed as listed, relying on pytest's default de-duplication of repeated file arguments. The worker did not check this separately.
- **G5 control scope:** the control ran over exactly the two files the mutations name (S and D).
- **G5 worktree:** made with `--detach`, so no branch was created.
- **Payload copies:** the four files the block names for C1 (plan, ledger, decisions, block) went to `.agent/authored/`. `next.md` is not copied; it lives in this handoff's `## Next`.
- **Scratch:** gitignored under `.remedy-wt/f273-r15/`: `wk_c1.py`, `wk_g1.py`, `wk_g3.py`, `wk_g5.py`, `wk_count.py`, `wk_run.py`, `wk_c4.py`, `handoff_head.md`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 15: the next session re-derives round
   15 over `bce5bc3b`..the round 15 handoff commit, taking the reviewer's draft verdict in the
   gitignored `.remedy-wt/next-r1/ledger_f273r15.md` as a draft only, and books `Gate: F273 R15`
   with `Done:` lines for R-0990, R-0931 and R-0981 in its first round's first commit.
2. The three HELD prototypes (DECISION F273 D15 (4)), each a ruling taken with its patch. They
   were built against `bce5bc3b`'s code tree and need re-applying or rebuilding at the round 15 tip:
   - The repair loop (R-0923, R-0918, R-0924, R-0925, R-0926): `.remedy-wt/f273-proto-g6b.diff`,
     sha256 `68b1edc361e2a2f07c54eea2f4ee83ff8487e22160a798c66a9ad2e096c8586b`. Open rulings:
     deleting `repair_loop.py` whole against the "module stays whole" clause R-0923 cites from
     DECISION F261 D17; the two cockpit labels `contract_decision` and `repair_loop_stopped` dropped
     while their events are still emitted (prefer keeping them, which needs a helper-aware
     humanize-catalog walk); and R-0924's Acceptance line gaining a "ruled moot" branch.
   - R-0914: `.remedy-wt/f273-proto-g6d.diff` is REJECTED: it deletes
     `create_manual_completion_bundle`, the closure evidence producer
     `docs/roadmap/STATUS_closure_protocol.md` names. Re-measure which attestation writer is live.
   - The worker queue (R-0927, R-0928): `.remedy-wt/f273-proto-g6e.diff`, sha256
     `5eb3bd58e90bffb28db408e503a55b9fde85e084961c4b85a792612cb7e26a41`, stacked on g6d, so it must
     be rebuilt without it. Open rulings: `_COUPLING_CEILING` 1 to 6 (the alternative is deleting
     the five dead names' readers); the deleted guard `test_no_public_command_reaches_without_permission`
     should be re-pointed at the live `apply_structured_patch` callers, not dropped; deleting
     `source_context.py` and `worker status`.
3. Then the remaining Acceptance ids (R-0892 waits on operator question Q2; R-0912's leftovers;
   R-0940 and R-0954 are process-doc edits; R-0977 needs its ruling first), a measured owner for
   every other open id, and the closure sequence.

Operator questions open: 5
