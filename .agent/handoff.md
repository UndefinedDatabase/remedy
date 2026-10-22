# Handback — F113 round 1: claim F113, book F296 round 7, write the slice list, land T001 and T002

## Session

SESSION 1 of feature F113 · round 1 · rounds so far 1

Context self-assessment: this worker verified the block and manifest digests before any write, copied each prepared file by a script with a byte-for-byte proof, ran each gate once after C3, and context stayed ample throughout.

Fortschritt: ~35 % (T001 and T002 landed · T003a to T003c open) — Schätzung

## Range

Review of `3af211790`..`HEAD` on `feature/f113-local-side-roles`.

## Commits

### 6db0605c2 F113 R1 C1: claim F113, book F296 R7, re-head the ledger, DECISION F113 D1, the slice list
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f113-r1.md` | +105/-0 | NEW FILE, this round's block, byte copy equal to `block.md` (105 lines, sha256 `030d9d5d...313f78`) |
| `.agent/context.md` | +9/-7 | rewritten for F113 |
| `.agent/decisions.md` | +12/-0 | DECISION F113 D1 |
| `.agent/live_review.md` | +17/-14 | re-headed, F296 round 7 booked |
| `.agent/plan.md` | +12/-10 | rewritten for F113 round 1 |
| `docs/roadmap/STATUS.md` | +1/-1 | F113 `[ ]` to `[~]` |
| `docs/roadmap/features/T3_F113.md` | +18/-0 | the slice list |

### 99930b2d1 F113 R1 C2: local endpoints and side roles — the two local_routing keys, the probe, the core-never-local refusal, the fallback and the summary role's three call sites
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/local_endpoints.py` | +196/-0 | NEW FILE, endpoint table, probe at first use, the call |
| `packages/orchestration/side_role_routing.py` | +146/-0 | NEW FILE, side-role table, core-role refusal, fallback |
| `packages/orchestration/config_keys_model_routing.py` | +35/-0 | the two `local_routing` keys |
| `packages/orchestration/artifact_summary.py` | +18/-6 | route field, call site follows the route |
| `packages/orchestration/result_tour.py` | +7/-7 | call site follows the route |
| `packages/orchestration/chat_answer.py` | +5/-3 | call site follows the route |
| `tests/orchestration/import_reachability_allowlist.txt` | +2/-0 | the two new modules |
| `docs/guides/environment.md` | +2/-0 | the two keys |

Total 411 insertions, under 500.

### f2722ad6c F113 R1 C3: the tests of the endpoints and the side roles, their page and its index rows
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_local_endpoints.py` | +212/-0 | NEW FILE |
| `tests/orchestration/test_side_role_routing.py` | +216/-0 | NEW FILE |
| `docs/system/local-side-roles-v1.md` | +56/-0 | NEW FILE, the system page |
| `docs/README.md` | +2/-0 | the page's two index rows |

### (this commit) F113 R1 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch `feature/f113-local-side-roles` created from clean `main` at `3af211790` |
| C1 | done | commit `6db0605c2`; seven paths byte-proved equal to their `c1-` source; block copy 105 lines, sha256 equal to `block.md` |
| C2 | done | commit `99930b2d1`; eight paths byte-proved equal; 411 insertions |
| C3 | done | commit `f2722ad6c`; four paths byte-proved equal; 486 insertions |
| C4 | done | this commit |
| Gate 1 | done | status porcelain empty; `verify.py .` ended `ALL True` (C4 `absent`, as it was not yet committed) |
| Gate 2 | done | `ruff_touched.py .` over 8 files, exit 0, `All checks passed!` |
| Gate 3 | done | exit 0, `7846 passed, 5 skipped, 1 warning in 83.40s`, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `integrity check --json` exit 0, `fail_count` 0 |
| Gate 5 | done | printed `7` |
| Push | pending | runs after this commit; its result is reported in the session reply |

## External actions

None yet: no push, no pull request, no gh command ran as of this commit. `git push -u origin feature/f113-local-side-roles` runs right after this commit; its result is reported in the session reply. No pull request is opened by this round.

## Verification

1. Digests before any write: `block.md` 105 lines, sha256 `030d9d5d7e26f23fb31d68fe93f361c58b0cd5c0804286efc6e28fb4e0313f78`; `digests.txt` sha256 `7767c77ce20e79e31926fede4c8b600fc73e10bf1d8487dad8cd070b46b3220c`; every listed file `True`, `BAD 0`.
2. C0: `git rev-parse HEAD` read `3af2117906ec...`, `git status --porcelain` empty before the branch was created.
3. Gate 1: `git status --porcelain` empty after C3; `python3 .remedy-wt/f113-r1/prep/verify.py .` exit 0, every line `True`, `absent` for C4, last line `ALL True`.
4. Gate 2: `python3 .remedy-wt/f113-r1/prep/ruff_touched.py .` exit 0: `ruff over 8 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f113-r1/prep/run_selection.py . .remedy-wt/f113-r1-worker/selection-output.txt` exit 0 (169 paths): `7846 passed, 5 skipped, 1 warning in 83.40s (0:01:23)`. Skipped lines: `tests/orchestration/test_model_routing.py:455` (3, covered by the violating fixture above), `tests/test_agent_tooling.py:43` (1, D12 quarantine, F252), `tests/test_install_smoke.py:175` (1, opt-in install smoke).
6. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0; six checks `pass`, `"fail_count": 0`, `"ok": true`.
7. Gate 5: `r.open_finding_ids(...)` over `.agent/live_review.md` printed `7`.

## Authored-text proofs

All prepared files of C1, C2 and C3 (19 paths) were proved equal over bytes by a script that copies and then compares, and `verify.py` re-proved them after C3. The saved block `.agent/authored/f113-r1.md` equals `block.md` (105 lines, same sha256).

## Deviations & assumptions

None. C1, C2, C3 landed in the ordered sequence, each touching only its named paths. No amend, rebase, force-push or `--no-verify`. No mutation proofs, no full suite, no `REMEDY_TEST_MAX_WORKERS`; each gate ran once. The working directory was never changed; commands needing the repository root ran through a script under `.remedy-wt/f113-r1-worker/` that passes `cwd=`.

## For the operator, in plain sentences

Remedy can now send its written summaries to a model server running on your own machine, so producing them stops costing paid tokens. You name the server in your project settings and say which side jobs may use it. Remedy refuses to send the jobs that build, review or plan to such a server, and says which rule it applied. If the server does not answer, the summary is written by the model that wrote it before, and the summary says why it fell back. A project that names no server sees no change. What is still missing is the cost record for these calls, the quality check that switches a server off when its summaries are poor, and the end-to-end demonstration.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 1's verdict in the next round's first commit.
4. T003a: the cost ledger records a side-role call with its basis.

Operator questions open: 0. Open findings: 7.
