# Handoff — F273 Findings paydown v1 · Round 16

## Session

SESSION 3 of feature F273 · round 16 · rounds so far 16

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D16, the handback template, round 15's handoff as the template's instance and every hunk of the three diffs as it applied them, and held all of it without loss; every figure below comes from a command run in this round.

## Range

Review of b22fe3bc..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 16 books round 15's verdict and three resolutions, registers R-0991, lands DECISION F273 D16, and builds R-0918, R-0923, R-0924, R-0925, R-0926, R-0991, R-0912, R-0940 and R-0954 as the reviewer's dry run built them.
- C1 books Gate F273 R15 (VERDICT PASS) and three `Done:` lines (R-0990, R-0931, R-0981), registers R-0991, lands DECISION F273 D16, rewrites the plan and saves the four payload copies.
- C2 (R-0918, R-0923, R-0924, R-0925, R-0926, R-0991): `repair_loop.py` and `repair_request_builder.py` are deleted with their tests; the attempt store's readers in `mission_readiness.py` and `self_dogfood.py` and the cockpit's `repair` and `repair_request` sections go with them, and the edited readiness and self-dogfood lines gain pinning tests. The humanize-catalog contract recovers names passed to a module's own forwarding helpers, to a fixed point, and counts `emit_important_event`; `contract_decision` and `repair_loop_stopped` stay, and 23 newly visible names gain catalog entries.
- C3 (R-0912): `_task_evidence_dir` raises `UnsafeTaskIdError` (a `ValueError` carrying the id); `job evidence` catches it and exits 1 with one line naming the id. Two CLI tests: a job whose task carries the minted default exports, and an unsafe id is refused by name.
- C4 (R-0940, R-0954, R-0924's Acceptance line): two worker-step rules in `docs/agents/self_drive_protocol.md`, and R-0924's Acceptance line in `T2_F273.md` gains the deleted-store branch (DECISION F273 D16 (2)).
- C5 is this handoff.

Landed: R-0918 — `12a6e591` (C2)
Landed: R-0923 — `12a6e591` (C2)
Landed: R-0924 — `12a6e591` (C2), its Acceptance line amended at `1d66099a` (C4)
Landed: R-0925 — `12a6e591` (C2)
Landed: R-0926 — `12a6e591` (C2)
Landed: R-0991 — `12a6e591` (C2)
Landed: R-0912 — `f939c117` (C3)
Landed: R-0940 — `1d66099a` (C4)
Landed: R-0954 — `1d66099a` (C4)

## Commits

### a2ee6ef6 F273 R16 C1: bookkeeping — round 15's verdict and its three resolutions booked, R-0991 registered, DECISION F273 D16 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r16-block.md` | +112 / -0 | Byte copy of the block |
| `.agent/authored/f273-r16-decisions.md` | +35 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r16-ledger.md` | +10 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r16-plan.md` | +32 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +35 / -0 | `b22fe3bc` bytes + decisions.md (DECISION F273 D16) |
| `.agent/live_review.md` | +10 / -0 | `b22fe3bc` bytes + ledger.md (Gate F273 R15, three `Done:` lines, R-0991) |
| `.agent/plan.md` | +16 / -13 | := plan.md |

250 insertions, 13 deletions (`git show --numstat`).

### 12a6e591 F273 R16 C2: R-0918, R-0923, R-0924, R-0925, R-0926, R-0991 — the repair loop and the repair request builder go whole with their readers and cockpit sections, and the catalog contract reads forwarding helpers
All by `git apply .remedy-wt/f273-proto-g7a2.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/humanizeCatalog.ts` | +25 / -0 | Entries for the names the helper-aware walk finds |
| `docs/guides/do-run-v1.md` | +2 / -2 | `DoRunNextAction` no longer has a production importer |
| `docs/system/operator-cockpit-v1.md` | +6 / -3 | `repair` and `repair_request` sections deleted |
| `docs/system/repair-loop-v1.md` | +12 / -7 | Status: module deleted; a repair is only a phase of a run; no post-apply attempt state |
| `docs/system/repair-request-builder-v0.md` | +3 / -0 | Status: module deleted |
| `docs/system/run-contract-v1.md` | +1 / -5 | The repair-loop integration is gone |
| `packages/orchestration/decision_queue.py` | +1 / -2 | Comment |
| `packages/orchestration/do_run.py` | +4 / -3 | Docstring |
| `packages/orchestration/mission_readiness.py` | +6 / -56 | Attempt-store reader and the repair items/capabilities/risks deleted |
| `packages/orchestration/repair_loop.py` | +0 / -1287 | Deleted |
| `packages/orchestration/repair_request_builder.py` | +0 / -602 | Deleted |
| `packages/orchestration/self_dogfood.py` | +16 / -29 | Attempt-store reader deleted; the gap cites the failure artifact |
| `packages/orchestration/test_execution_service.py` | +2 / -2 | Docstring |
| `packages/orchestration/ui_server.py` | +0 / -74 | Cockpit `repair` and `repair_request` sections deleted |
| `pyproject.toml` | +0 / -1 | Deleted module's mypy entry |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -2 | Deleted modules |
| `tests/orchestration/test_mission_readiness.py` | +32 / -16 | Pins `failure_resolved` and `human_decision_needed` |
| `tests/orchestration/test_repair_loop_v1.py` | +0 / -308 | Deleted with its module |
| `tests/orchestration/test_repair_request_builder.py` | +0 / -225 | Deleted with its module |
| `tests/orchestration/test_run_contract.py` | +0 / -8 | Guard over the deleted module removed |
| `tests/orchestration/test_self_dogfood.py` | +9 / -0 | Pins the gap's `source_type` |
| `tests/orchestration/test_test_failure_repair.py` | +3 / -332 | Repair-loop tests removed |
| `tests/ui_contracts/test_humanize_catalog.py` | +100 / -25 | Helper-aware walk and its test |
| `tests/ui_server/test_dashboard_cockpit_truth.py` | +2 / -18 | The two sections are asserted absent |

224 insertions, 3007 deletions.

### f939c117 F273 R16 C3: R-0912 — job evidence refuses an unsafe persisted task id by name and exits 1
All by `git apply .remedy-wt/f273-proto-g7d1.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +15 / -5 | Catches `UnsafeTaskIdError`, exits 1 naming the id |
| `packages/orchestration/job_evidence.py` | +16 / -7 | `UnsafeTaskIdError` carries the id |
| `tests/orchestration/test_job_evidence.py` | +43 / -0 | Minted-default export and by-name refusal CLI tests |

74 insertions, 12 deletions.

### 1d66099a F273 R16 C4: R-0940, R-0954 — two worker-step rules in the self-drive protocol, and R-0924's Acceptance line gains the deleted-store branch
All by `git apply .remedy-wt/f273-s3/r16_docs.diff`.
| Path | +/- | Reason |
|------|-----|--------|
| `docs/agents/self_drive_protocol.md` | +7 / -0 | R-0954 block-copy check; R-0940 disposable-worktree rule |
| `docs/roadmap/features/T2_F273.md` | +2 / -1 | R-0924 Acceptance line, D16 branch |

9 insertions, 1 deletion.

### C5 (this commit) F273 R16 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 250.

## External actions

- `git worktree add --detach .remedy-wt/f273-r16-g5 1d66099a` for G5, then `git worktree remove .remedy-wt/f273-r16-g5` (exit 0, no `--force`) as the step's last action. `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                         1d66099a [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-s3-r16  5fbee8b9 (detached HEAD)
  ```
  The second entry is not this round's: it existed, detached at `5fbee8b9`, before the round started, and the worker left it alone.
- The branch `remedy/job-81ec65896729405c` exists in this repository. A research helper's probe created it (2026-09-19 17:39, before this round); nobody may delete it without the operator. `git branch --list 'remedy/job-*'` reads 37 branches after the gates, 36 plus that one.
- After C5: `git push`. No pull request is opened.

## Verification

G1 to G5 ran at C4 `1d66099a` with a clean tree. Every script ran with an explicit `cwd`; exit codes come from `.remedy-wt/f273-r16/wk_run.py`, which prints the child's real return code, or from the script's own `EXIT CODE:` line.

- **Transport**, before any write: `sha256sum` of the block, the five payloads and the three diffs matched the given digests. The block file read 112 lines.
- **Block copy (R-0954)**, before C1: `.remedy-wt/f273-r16/wk_c1.py` read the saved `.agent/authored/f273-r16-block.md` back:
  ```
  saved block copy sha256: c7ff4fb323405f29eabc5ef53fa21dbb97e46b74722b0a557f691b226cce2ae8
  saved block copy lines: 112
  equals given sha256: True equals given line count 112: True
  ```
- **G1**: `python3 .remedy-wt/f273-r16/wk_g1.py`, exit 0:
  ```
  digest f273-r16/plan.md True
  digest f273-r16/ledger.md True
  digest f273-r16/decisions.md True
  digest f273-r16/next.md True
  digest f273-r16/targets.txt True
  digest f273-r16/block.md True
  digest f273-proto-g7a2.diff True
  digest f273-proto-g7d1.diff True
  digest f273-s3/r16_docs.diff True
  plan.md == payload True
  live_review == base + ledger True
  decisions == base + decisions True
  authored f273-r16-plan.md True
  authored f273-r16-ledger.md True
  authored f273-r16-decisions.md True
  authored f273-r16-block.md True
  C2 paths == g7a2 paths True
  C3 paths == g7d1 paths True
  C4 paths == r16_docs paths True
  C1 paths == 7 bookkeeping paths True
  20 checks, all True: True
  EXIT CODE: 0
  ```
- **G2**: `git rev-parse 1d66099a:tests 1d66099a:packages 1d66099a:apps 1d66099a:docs`, exit 0:
  ```
  59a351fcfd1565731e63d03b2f2c31cc6fee3ddc
  43a6fc081dca24c6284dd5aa0e752677d7af2239
  c3ce5c3eaf7e2ad5920469e0a197f763f8c46be8
  82ebd05ea4af375724587e153c0bd49859876257
  ```
  All four equal the reviewer's dry-run objects.
- **G3** (primary checkout, serial): `python3 .remedy-wt/f273-r16/wk_g3.py` runs `python3 -m pytest -q -p no:cacheprovider` over every line of `targets.txt` and counts `R-0803:` lines over the full output:
  ```
  target paths: 19 distinct: 19 missing: []
  2063 passed, 5 skipped in 217.15s (0:03:37)
  R-0803: lines: 0
  EXIT CODE: 0
  ```
- **G4**: `python3 -m ruff check . --output-format concise` from the primary checkout's root:
  ```
  All checks passed!
  EXIT CODE: 0
  ```
- **G5** (`python3 .remedy-wt/f273-r16/wk_g5.py`, exit 0): one detached worktree at `1d66099a`; `python3 -B -m pytest -q -p no:cacheprovider` from its root; env carries `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`; `__pycache__` purged before every run; each FROM matched as a whole line with its newline; each file reverted from its saved bytes.
  ```
  ui_server path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r16-g5/packages/orchestration/ui_server.py
  CONTROL (unmutated) over tests/ui_contracts/test_humanize_catalog.py tests/orchestration/test_mission_readiness.py tests/orchestration/test_self_dogfood.py tests/orchestration/test_job_evidence.py: 147 passed in 29.78s | exit 0
  (a) tests/ui_contracts/test_humanize_catalog.py: FROM line count = 1
      tests/ui_contracts/test_humanize_catalog.py: 2 failed, 9 passed in 1.07s | exit 1 | RED
          FAILED tests/ui_contracts/test_humanize_catalog.py::TestDerivation::test_the_walk_finds_a_name_only_a_helper_emits
          FAILED tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary
  (b) packages/orchestration/mission_readiness.py: FROM line count = 1
      tests/orchestration/test_mission_readiness.py: 1 failed, 19 passed in 0.35s | exit 1 | RED
          FAILED tests/orchestration/test_mission_readiness.py::TestReadinessTruth::test_failure_resolved_reads_the_unresolved_failures
  (c) packages/orchestration/mission_readiness.py: FROM line count = 1
      tests/orchestration/test_mission_readiness.py: 1 failed, 19 passed in 0.36s | exit 1 | RED
          FAILED tests/orchestration/test_mission_readiness.py::TestReadinessTruth::test_human_decision_needed_reads_the_pending_intents
  (d) packages/orchestration/self_dogfood.py: FROM line count = 1
      tests/orchestration/test_self_dogfood.py: 1 failed, 16 passed in 0.31s | exit 1 | RED
          FAILED tests/orchestration/test_self_dogfood.py::TestInspection::test_unresolved_failure_item_cites_the_failure_artifact
  (e) apps/cli/commands/do_cmd.py: FROM line count = 1
      tests/orchestration/test_job_evidence.py: 1 failed, 98 passed in 20.83s | exit 1 | RED
          FAILED tests/orchestration/test_job_evidence.py::TestSafeTaskIdHelper::test_job_evidence_command_refuses_an_unsafe_task_id_by_name
  worktree status after reverts: ''
  worktree remove exit 0
  ```
  Each mutation printed `reverted: True` after its run (trimmed above). Every mutation went red; none stayed green.
- **G6** runs after the push and is reported in the round report, because this commit comes before it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file in C1 was built by `python3 .remedy-wt/f273-r16/wk_c1.py` from `git show b22fe3bc:<path>` bytes and the payload bytes. Nothing was hand-edited except this handoff. G1 re-proves every C1 file and every `.agent/authored/f273-r16-*` copy against its payload.
- The code and docs arrived only by `git apply` of the three reviewer-verified diffs, in the block's order. G2's object ids equal the reviewer's dry-run objects.
- The `## Next` body below is `next.md` byte for byte, appended by script.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping (Gate F273 R15, R-0990, R-0931, R-0981 `Done:`, R-0991 registered, D16) | done | `a2ee6ef6` |
| R-0918 | done | `12a6e591` (C2) |
| R-0923 | done | `12a6e591` (C2) |
| R-0924 | done | `12a6e591` (C2); Acceptance line at `1d66099a` (C4) |
| R-0925 | done | `12a6e591` (C2) |
| R-0926 | done | `12a6e591` (C2) |
| R-0991 | done | `12a6e591` (C2) |
| R-0912 | done | `f939c117` (C3) |
| R-0940 | done | `1d66099a` (C4) |
| R-0954 | done | `1d66099a` (C4) |
| C5 handoff + push | done | This commit, then the push |
| G1 to G5 | done | All green as above |
| G6 | done | After the push; in the round report |
| R-0977 | skipped | Not in this bundle; held by DECISION F273 D16 (6) |

## Open findings

Measured by `.remedy-wt/f273-r16/wk_count.py`. It loads `scripts/rotate_live_review.py` by path, registers it in `sys.modules`, and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `a2ee6ef6` (C1 onwards; C2 to C4 do not touch it; the same at `1d66099a`): **55 open**;
- at `b22fe3bc`: 57 open.

C1's three `Done:` lines close three distinct ids and it registers R-0991: 57 - 3 + 1 = 55. The nine ids landed this round are still open in the ledger.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C5, then the push. No extra commit.
- **G5 control scope:** the control ran over exactly the four files U, M, S and J.
- **G5 worktree:** made with `--detach`, so no branch was created.
- **Pre-existing worktree:** `.remedy-wt/f273-s3-r16` (detached at `5fbee8b9`) was registered before the round and appears in `git worktree list`; the worker did not create, use or remove it.
- **Payload copies:** the four files the block names for C1 (plan, ledger, decisions, block) went to `.agent/authored/`. `next.md` is not copied; it lives in this handoff's `## Next`.
- **Operator questions:** the count below is the number of `### Q<n>` headings in `.agent/operator_questions.md` (Q1, Q2, Q4, Q5, Q7).
- **Scratch:** gitignored under `.remedy-wt/f273-r16/`: `wk_c1.py`, `wk_g1.py`, `wk_g3.py`, `wk_g5.py`, `wk_count.py`, `wk_run.py`, `wk_c5.py`, `handoff_head.md`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 16 over `b22fe3bc`..the round 16
   handoff commit, booked as `Gate: F273 R16` with `Done:` lines for R-0918, R-0923, R-0924,
   R-0925, R-0926, R-0991, R-0912, R-0940 and R-0954 in the next round's first commit.
2. R-0914: delete `attest_operator_repair` and the export's attestation overlay that only it fed,
   keeping `create_manual_completion_bundle` and everything it reaches, with `manual_attestation.py`;
   its Acceptance line is amended by DECISION in the same round.
3. The worker queue (R-0927, R-0928) without raising `_COUPLING_CEILING`: the dead-name readers go
   with their emitters, and the permission guard over `apply_structured_patch` is re-pointed, not
   dropped.
4. R-0977 with the `__pycache__` handoff-coverage defect DECISION F273 D16 (6) names, then a
   measured owner for every other open id, then closure.

Operator questions open: 5
