# Handback — F307 round 3: book round 2, R-1375, R-1376 and R-1412; T004's refactor and behaviour commits

## Session

SESSION 1 of feature F307 · round 3 · rounds so far 3

Context self-assessment: this worker verified every prepared digest, byte-copied the prepared files, self-reviewed each diff before committing, ran each gate once and wrote this handback from what it read; context is ample and nothing was lost.

Fortschritt: ~18 % (T001 to T004 landed · T005 to T021 open) — Schätzung

## Range

Review of `ada52bd01`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 28e72daf8 F307 R3 C1: book round 2, R-1375, R-1376 and R-1412, DECISION F307 D4, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r3.md` | 114/0 | NEW FILE, this round's block, byte copy (114 lines, sha256 `86f24596cdeeaba02870bb102b46567c7d58f62834faeee8794e7508236df342`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy (DECISION F307 D4) |
| `.agent/live_review.md` | 8/0 | prepared file, byte copy (round 2's verdict and its three resolutions booked: R-1375, R-1376, R-1412) |
| `.agent/plan.md` | 7/7 | prepared file, byte copy |
| `docs/roadmap/features/T2_F307.md` | 5/4 | prepared file, byte copy (T004 and T005 lines updated; R-1278 and R-1287 move to T005) |

### 158e2f072 F307 R3 C2: one failover link loop, its keys spelled once, no test-only names in production (R-1310, R-1294)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config_keys_model_routing.py` | 9/3 | prepared file, byte copy (R-1310: failover keys and cooldown default spelled once) |
| `packages/orchestration/model_failover.py` | 67/153 | prepared file, byte copy (R-1310, R-1294: one link loop, one disclosure builder, a module docstring; properties with no production reader removed) |
| `packages/orchestration/structured_log.py` | 0/10 | prepared file, byte copy (R-1294: `LOG_FIELD_NAMES` and `current_log_context` deleted, no production reader) |
| `tests/orchestration/test_model_failover.py` | 12/7 | prepared file, byte copy (reads the deleted properties through a private-field helper) |
| `tests/orchestration/test_role_provider_factory.py` | 7/7 | prepared file, byte copy (same) |
| `tests/orchestration/test_structured_log.py` | 13/2 | prepared file, byte copy (keeps its own copy of the deleted names, R-1294) |
| `tests/test_run_log.py` | 4/2 | prepared file, byte copy (reads the public context variables directly) |

### 0aacb7b75 F307 R3 C3: a failing backup serves nothing and a link names a provider Remedy can create (R-1286, R-1288)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | 4/4 | prepared file, byte copy (R-1288: reads `ROLE_PROVIDER_NAMES` instead of its own copy) |
| `docs/system/model-failover-v1.md` | 14/9 | prepared file, byte copy (documents both behaviour changes) |
| `packages/orchestration/model_failover.py` | 20/7 | prepared file, byte copy (R-1286: a link that answers with a failure serves nothing, holds nothing; R-1288: a chain link naming an unknown provider is refused when the table is read) |
| `packages/orchestration/provider_names.py` | 11/0 | NEW FILE, prepared file, byte copy (`ROLE_PROVIDER_NAMES`, R-1288) |
| `tests/cli/test_do_cmd_summary.py` | 2/2 | prepared file, byte copy |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | prepared file, byte copy (new module listed) |
| `tests/orchestration/test_model_failover.py` | 70/4 | prepared file, byte copy (new tests for R-1286 and R-1288) |
| `tests/orchestration/test_role_provider_factory.py` | 1/1 | prepared file, byte copy (fixture provider renamed to a real one) |

### (this commit) F307 R3 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD `ada52bd01` equal to `origin/feature/f307-findings-paydown-v9`, tree clean |
| C1 | done | records commit `28e72daf8` |
| C2 | done | refactor commit `158e2f072` |
| C3 | done | behaviour commit `0aacb7b75` |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every counted line, `absent C4` (not yet counted), last line `ALL True` |
| Gate 2 | done | `ruff check` printed `All checks passed!` |
| Gate 3 | done | 85 paths, exit 0, `3804 passed, 2 skipped in 36.99s`, two SKIPPED lines, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `51` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own, no provider call, no rotation.

## Verification

1. Digests: `python3 .remedy-wt/f307-r3-worker/check_digests.py` over the 24 lines of `digests.txt` — every line `OK`, last line `ALL_OK`.
2. Gate 1: `git status --porcelain` (through `git -C`) — empty. `python3 .remedy-wt/f307-r3/prep/verify.py .` — every counted line `True` (single-parent checks on all three commits, the Cn-subject count 3 of 3, the branch check, every C1, C2 and C3 path-set and per-path equality check, and "the saved block equals block.md"); one line `absent C4` (not yet counted, C4 did not exist when the gate ran); last line `ALL True`.
3. Gate 2: `python3 -m ruff check packages/orchestration/model_failover.py packages/orchestration/config_keys_model_routing.py packages/orchestration/structured_log.py packages/orchestration/provider_names.py apps/cli/commands/do_cmd.py tests/orchestration/test_model_failover.py tests/orchestration/test_role_provider_factory.py tests/orchestration/test_structured_log.py tests/test_run_log.py tests/cli/test_do_cmd_summary.py` — `All checks passed!`.
4. Gate 3: `python3 .remedy-wt/f307-r3/prep/run_selection.py . .remedy-wt/f307-r3-worker/selection-output.txt` — `paths 85`, `exit 0`, `3804 passed, 2 skipped in 36.99s`. SKIPPED lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (install smoke is opt-in). No FAILED, no ERROR, no `process(es) behind` line.
5. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0 — `fail_count` 0; all six checks pass: `handler_import` ("handlers=194"), `live_review_verdict` ("last Gate verdict PASS"), `plan_consistency` ("unchecked=0, context_complete=False"), `relevant_untracked` ("untracked=0, relevant=0"), `repo_root_hygiene` ("no reviewer scratch, evidence dir or archive at the root"), `high_blockers_open` ("no open blocker/high findings").
6. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `51`.

## Authored-text proofs

C1's five prepared files, C2's seven prepared files and C3's eight prepared files are byte copies of the prepared files; each was proved equal by a sha256 comparison right after the copy, before staging, and `verify.py` re-proved every one of them (`True`). `.agent/authored/f307-r3.md` equals `block.md`: 114 lines, sha256 `86f24596cdeeaba02870bb102b46567c7d58f62834faeee8794e7508236df342` on both sides.

## Deviations & assumptions

None. The commit sequence, paths and gate commands followed the block exactly; no file outside the named paths per commit was touched. The prep directory also holds six files not listed in `digests.txt` (`src-decisions.md`, `src-ledger.md`, `src-model_failover.py`, `src-plan.md`, `src-provider_names.py`, `src-test-failover-c3.py`); since the block names `digests.txt` as the list of every prepared file to use, and these six are absent from it, they were left untouched and unread for content.

## For the operator, in plain sentences

This round booked the previous round's closing verdict and its three resolutions into the running record, recorded one decision describing how the remaining work splits across two upcoming steps, and updated the running plan to match. It then carried out the planned cleanup of the failover module: the configuration keys it reads are now spelled in exactly one place, one loop now handles both ways the module walks its backup chain, and several names that only tests had ever read were removed from the production module, with the tests updated to reach what they need another way. No behaviour changed in that step. The following step changed two real behaviours: a backup model that answers with a failure of its own is no longer reported as having served the call, and does not keep the usual model sidelined; and a backup chain naming a provider Remedy cannot build is now refused as soon as the configuration is read, with the same list of known names used by the command line. All five required checks ran once each and came back exactly as expected. No question waits for the operator.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 3's verdict in the next round's first commit.
4. T005: the boundary of pingpong_loop's provider call, then R-1276, R-1277, R-1278, R-1287 and R-1289.

Operator questions open: 0. Open findings count gate 5 printed: 51.
