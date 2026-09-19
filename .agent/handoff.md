# Handoff — F271 No more legacy: ownership, reachability, replace-is-delete · Round 3

## Session

SESSION 1 of feature F271 · round 3 · rounds so far 3

Context self-assessment: the worker read the block, AGENTS.md, `docs/roadmap/features/T2_F271.md`, DECISION F271 D3, the ledger and plan payloads and the whole of `prototype_final.diff` once each, and every figure below comes from a command run in this round.

## Range

Review of 8bacb0fc..HEAD — branch `feature/f271-no-more-legacy`.

## Summary

- C1 is the bookkeeping. It saves the four payload copies, sets `.agent/plan.md` to plan.md, appends ledger.md to `.agent/live_review.md` (the F271 R2 gate entry and `Done: R-0982`), and appends DECISION F271 D3 to `.agent/decisions.md`.
- C2 is the R-0982 deletion (D3 (3)). It deletes `packages/orchestration/patch_revert.py` and the five `TestPatchRevert` tests that exercised only that module. `test_brain_has_patch_revert_node` now plants the event itself and asserts the `ET_REVERTED_BY` edge. C2 also drops the `ALLOWED_UNWIRED` entry and the section 12q snapshot-directory check in `scripts/remedy_smoke.sh`.
- C3 is T002's doctor part (D3 (2)). It adds the `_plant_dead_command` helper and two tests to `TestDoctorCoreDeadCommands`, one for JSON mode and one for text mode. It also rewrites the `_cmd_doctor_core` comment, which is only a comment, so that it names the tests.
- C4 is T002's closure part (D3 (1)). It adds precondition 7 to `docs/roadmap/STATUS_closure_protocol.md`, which cites AGENTS.md's Scope Control rule "Replacing is deleting".
- C5 is this handoff.

## Commits

### 2395382b F271 R3 C1: book F271 round 2's verdict and Done R-0982, land DECISION F271 D3, save the round 3 payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-r3-block.md` | +92 / -0 | Byte copy of the block |
| `.agent/authored/f271-r3-decisions.md` | +40 / -0 | Byte copy |
| `.agent/authored/f271-r3-ledger.md` | +4 / -0 | Byte copy |
| `.agent/authored/f271-r3-plan.md` | +26 / -0 | Byte copy |
| `.agent/decisions.md` | +40 / -0 | `8bacb0fc` bytes + decisions.md (DECISION F271 D3) |
| `.agent/live_review.md` | +4 / -0 | `8bacb0fc` bytes + ledger.md |
| `.agent/plan.md` | +9 / -10 | := plan.md |

215 insertions, 10 deletions (`git show --numstat`).

### 3c566f86 F271 R3 C2: delete patch_revert with the five tests only it served, its allowance and the smoke snapshot check, resolving R-0982 under DECISION F271 D3
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/patch_revert.py` | +0 / -290 | deleted (D3 (3)) |
| `scripts/remedy_smoke.sh` | +0 / -7 | 12q loses the `patch_snapshots/<intent>` check |
| `tests/orchestration/test_source_apply.py` | +20 / -134 | five tests deleted; brain test plants the event and asserts the edge |
| `tests/test_no_orphan_modules.py` | +0 / -2 | the R-0982 `ALLOWED_UNWIRED` entry goes |

20 insertions, 433 deletions.

### 55ff1c3a F271 R3 C3: T002 planted-dead-command tests for doctor core in JSON and text mode, and the doctor comment naming them
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/worker_facade_cmd.py` | +3 / -3 | comment only |
| `tests/cli/test_worker_facade_cmd.py` | +41 / -2 | `_plant_dead_command` helper, two planted tests, class docstring |

44 insertions, 5 deletions.

### b1d0f9f8 F271 R3 C4: T002 closure precondition 7, no new module outside the reachable set unless its feature file names it, citing the rule Replacing is deleting
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS_closure_protocol.md` | +10 / -0 | precondition 7 |

10 insertions, 0 deletions.

### C5 (this commit) F271 R3 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 215.

## External actions

- `git worktree add --detach .remedy-wt/f271-r3-g5wt b1d0f9f8` for G5, then `git worktree remove .remedy-wt/f271-r3-g5wt`. Afterwards `git worktree list` shows the primary checkout alone: `/home/decodeux/Repos/remedy  b1d0f9f8 [feature/f271-no-more-legacy]`.
- `git push` after C5, not forced. No pull request is opened.
- No evidence job and no zip.

## Verification

All gates below ran at C4 (`b1d0f9f8`) before C5. Each exit code was read through `.remedy-wt/f271-r3/w_run.py`, which prints `EXIT <returncode>` for the command it runs.

- **Transport**, before any write: `sha256sum` matched the block's `38bfb15e6047d2ddb2f1214a904df1b162bc62af0737fd2b05881d79a43cce6e` and all four payload digests: plan.md `e8f54864…`, ledger.md `4897747e…`, decisions.md `5e937e42…` and prototype_final.diff `63ba2a7f…`. `git apply --check --index` on the prototype passed at `8bacb0fc`.
- **G1**: `python3 .remedy-wt/f271-r3/w_g1.py` printed `12 checks, all True: True` (exit 0). The checks are:
  - the five digests;
  - `.agent/plan.md` equals plan.md;
  - `.agent/live_review.md` equals its `8bacb0fc` bytes + ledger.md;
  - `.agent/decisions.md` equals its `8bacb0fc` bytes + decisions.md;
  - each of the four `.agent/authored/f271-r3-*` copies equals its payload.
- **G2**: `python3 .remedy-wt/f271-r3/w_g2.py` exited 0.
  - `git diff --binary 8bacb0fc b1d0f9f8 -- . ':!.agent' | git patch-id --stable` gives first field `0122492bf6ec20f8acd3ad95e1aeb2542cb51b85`. `git patch-id --stable < prototype_final.diff` gives the same field.
  - `git show --numstat --format=` of C2, C3 and C4 lists exactly the paths the Bundle names (`paths match Bundle: True` for each; tables above).
- **G3**: `git status --porcelain` was empty before and after the run. The twelve-target command, as ordered, ran serially in the primary checkout and printed `706 passed in 116.29s (0:01:56)` (exit 0, 0 failed). `bash -n scripts/remedy_smoke.sh` exited 0.
- **G4**: `python3 -m ruff check apps/cli/commands/worker_facade_cmd.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_source_apply.py tests/test_no_orphan_modules.py` printed `All checks passed!` (exit 0). The ordered `git grep` (exit 0) printed exactly the three lines D3 accepts:
  - `apps/cli/commands/patch.py:175:def _cmd_revert_patch_intent(`
  - `apps/cli/commands/patch.py:407:    "patch.revert": lambda args: _cmd_revert_patch_intent(`
  - ``docs/system/snapshot-rollback-v1.md:181:| `patch_apply.py` | Mandatory snapshot replaces `store_pre_apply_snapshot()`. `DurableApplyRecord` saved after apply. `snapshot_id` + `snapshot_verified` in artifact apply record. Legacy snapshot call removed (Step 1141). |``
- **G5**: disposable worktree `.remedy-wt/f271-r3-g5wt` at `b1d0f9f8`, driven by `.remedy-wt/f271-r3/w_g5.py`. Every run was `python3 -B -m pytest -q -p no:cacheprovider -rf <file> -k <selector>` from the worktree root. `__pycache__` was purged before each run; the purge found 0 directories each time. Before each run the script printed the imported module path, which was always inside the worktree (`.../.remedy-wt/f271-r3-g5wt/apps/cli/commands/worker_facade_cmd.py`, or `.../packages/orchestration/project_brain.py` for (c)). Each target line counted 1 before it was mutated. Each change was reverted before the next, and after each revert the worktree's `git status --porcelain` was empty.
  - Control, unmutated, `-k TestDoctorCoreDeadCommands`: `4 passed, 37 deselected in 8.15s`, exit 0.
  - (a) `"dead_commands": dead_commands,` → `"dead_commands": [],`: `1 failed, 3 passed, 37 deselected in 8.24s`, exit 1, `FAILED tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadCommands::test_json_mode_lists_exactly_the_planted_command`.
  - (b) `for cid in dead_commands:` → `for cid in []:`: `1 failed, 3 passed, 37 deselected in 8.23s`, exit 1, `FAILED tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadCommands::test_text_mode_lists_the_planted_command_in_the_section`.
  - Brain control, unmutated, `tests/orchestration/test_source_apply.py -k test_brain_has_patch_revert_node`: `1 passed, 28 deselected in 0.32s`, exit 0.
  - (c) in `project_brain.py`, `"patch_intent_reverted"` → `"patch_intent_reverted_x"`: `1 failed, 28 deselected in 0.34s`, exit 1, `FAILED tests/orchestration/test_source_apply.py::TestPatchRevert::test_brain_has_patch_revert_node`.
  - No change stayed green.
- **G6** comes after the push, so the round report carries it.
- Full suite not run (amend0917-throughput).

## Authored-text proofs

- The byte copies are at `.agent/authored/f271-r3-*`, four files. Each is `True` against its payload (G1). The block copy's digest is `38bfb15e6047d2ddb2f1214a904df1b162bc62af0737fd2b05881d79a43cce6e`.
- `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md` were each built from payload bytes, or from `git show 8bacb0fc:` bytes plus the payload. Each byte check is `True` (G1).
- The code and doc text of C2 to C4 match the prototype byte for byte, as the patch-id shows (G2).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `2395382b` |
| C2 R-0982 deletion (D3 (3)) | done | `3c566f86`; G4 grep leaves only the three accepted lines; G5 (c) red |
| C3 T002 doctor planted command (D3 (2)) | done | `55ff1c3a`; G5 (a) and (b) red |
| C4 T002 precondition 7 (D3 (1)) | done | `b1d0f9f8` |
| C5 handoff | done | This commit |

## Open findings

This count is by distinct id on the committed `.agent/live_review.md` at C4. `^- R-\d+ — ` matches 136 ids and `^Done: R-\d+ — ` matches 6. All 6 are among the 136, so 130 are open: round 2's 131 minus R-0982, which is now Done.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, C4, C5, then the push). No extra commit.
- **Prototype:** `git apply --index` put the whole prototype on the index once, at `8bacb0fc` + C1. C2, C3 and C4 each committed their path subset with `git commit -- <paths>`. Nothing in the prototype was changed, and the worker found no defect in it.
- **G5 extra control:** the block orders one unmutated control, for the doctor tests. The worker also ran the brain test unmutated before mutation (c), so that (c)'s red has a green control from the same selection. This adds a run and changes nothing.
- **Driver scripts:** the gates ran through gitignored scratch in `.remedy-wt/f271-r3/`: `w_c1.py`, `w_g1.py`, `w_g2.py`, `w_g5.py`, `w_openset.py` and `w_run.py`. The bash guard rejects the inline forms. The G3 output was piped to `tail`. The exit code is still real, because `w_run.py` prints the pytest process's own return code.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The review of round 3.

Operator questions open: 5
