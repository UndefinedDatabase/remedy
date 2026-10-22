# Handback — F074 round 2: book round 1, land T003 — the trust view and the plan view's calibrated bands

## Session

SESSION 1 of feature F074 · round 2 · rounds so far 2

Context self-assessment: this worker checked both prompt digests and every prepared file's digest before any write, copied every file by a script with a byte proof, ran each gate exactly once, and context stayed ample throughout.

Fortschritt: ~65 % (T001 to T003 landed · the closure open) — Schätzung

## Range

Review of `be58f7854`..`HEAD` on `feature/f074-estimate-calibration`.

## Commits

### 233bd6709 F074 R2 C1: book round 1, one prose slip, DECISION F074 D2, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f074-r2.md` | +99/-0 | NEW FILE, this round's block, byte copy of `block.md` (sha256 `37a794b0...6d24ac4ed`) |
| `.agent/decisions.md` | +12/-0 | DECISION F074 D2 appended |
| `.agent/live_review.md` | +2/-0 | round 1's verdict booked |
| `.agent/plan.md` | +4/-6 | rewritten for F074 round 2 |
| `.agent/prose_slips.md` | +1/-0 | round 1's handback overclaim ("whole test collection passed") recorded |

### 89bd8a989 F074 R2 C2: stats calibration, the trust view of the estimate calibration, and the calibrated midpoint beside a band in job plan-show
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_stats.py` | +21/-0 | `stats.calibration` catalog entry |
| `apps/cli/commands/__init__.py` | +2/-1 | `stats_calibration_cmd` wired into `collect_all_handlers` |
| `apps/cli/commands/job_plan_cmd.py` | +19/-1 | `_calibrated_band_notes`, the band annotation in `_cmd_plan_show` |
| `apps/cli/commands/stats_calibration_cmd.py` | +108/-0 | NEW FILE, T003: `remedy stats calibration` handler, text and JSON rendering |
| `packages/orchestration/budget_resolution.py` | +34/-12 | `_calibration_settings` factored out, `resolve_calibration_settings` added |
| `packages/orchestration/estimate_calibration.py` | +8/-0 | `calibrated_band_note` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `apps.cli.commands.stats_calibration_cmd` line |

### 30456cea1 F074 R2 C3: the trust view's tests and the plan view's, and the calibration page completed
| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +1/-1 | the index row for `estimate-calibration-v1.md` updated for T003 |
| `docs/system/estimate-calibration-v1.md` | +24/-3 | the trust view and plan's bands sections, status banner updated |
| `tests/cli/test_job_plan_cmd.py` | +60/-0 | `TestPlanShowCalibratedBands`: calibrated midpoint, thin class, malformed setting, JSON unchanged |
| `tests/cli/test_stats_calibration_cmd.py` | +162/-0 | NEW FILE, T003 tests: catalog, text rendering, JSON, snapshot reuse, config override, no-ledger, no-window, no-project, malformed setting |

## Item status

| Item | Status | Reason |
|---|---|---|
| Both prompt digests checked (`block.md`, `digests.txt`) | done | both matched before any read |
| Every prepared file's digest checked | done | 21 of 21 matched |
| Preconditions | done | clean status, correct branch, HEAD `be58f7854` equal to origin |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| C4 (this handback) | done | |
| Push | done | see External actions |
| Pull request | skipped | the block orders no PR this round |

## External actions

- `git push origin feature/f074-estimate-calibration`: outcome in the worker's reply (written after this file is committed).
- No merge, no PR create, no stash, no provider call, no rebase, no amend, no force push.

## Verification

Gate 1a: `git status --porcelain` (through `git -C <repository root>`) — empty output.

Gate 1b: `python3 .remedy-wt/f074-r2/prep/verify.py .` — every line `True` (including every C1-C3 path-set and byte-equality check, `absent C4` before this commit existed), last line `ALL True`.

Gate 2: `python3 .remedy-wt/f074-r2/prep/ruff_touched.py .` — `ruff over 8 files: exit 0`, `All checks passed!`

Gate 3: `python3 .remedy-wt/f074-r2/prep/run_selection.py . .remedy-wt/f074-r2-worker/selection-output.txt` — `paths 201`, `exit 0`, `9132 passed, 2 skipped in 82.71s (0:01:22)`. No FAILED, ERROR or "process(es) behind" line. The two SKIPPED lines, verbatim:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Gate 4: `python3 -m apps.cli.main integrity check --json` — `"fail_count": 0`, `"ok": true`, `"passed": true`; `handler_import` pass (handlers=196), `live_review_verdict` pass (last Gate verdict PASS), `plan_consistency` pass (unchecked=0, context_complete=False), `relevant_untracked` pass (untracked=0, relevant=0), `repo_root_hygiene` pass, `high_blockers_open` pass (no open blocker/high findings).

Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `7`.

## Authored-text proofs

`.agent/authored/f074-r2.md`: `wc -l` reads `99`, `sha256sum` reads `37a794b033562d100d3edabc1328afbb222f713e185ab0a02e1b1926d24ac4ed`, equal to both `block.md` and the digest the delivering prompt named.

Every C1-C3 prepared file was copied by a Python byte copy and proven equal over bytes at copy time by comparing the destination's re-read bytes against the source's; `verify.py` at gate 1 re-proved every one of them plus the whole-digest-list check, and reported `True` throughout.

## Deviations & assumptions

None. The block's ordered commit sequence (C1 through C4, gates 1-5, the push) was followed exactly; no extra commit, no dropped commit, no reordering.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2, the Open PR Gate.
3. Book round 2's verdict in the next round's first commit.
4. The closure's integration gate: the one full suite and a self-use run.

Operator questions open: 0. Open findings: 7.

## For the operator, in plain sentences

Remedy can now show what its cost estimates rest on: for each kind of task, how many past tasks were measured, what they actually used, which kinds are measured well enough to be trusted, and how old that measurement is. When a stored plan is shown, a task whose kind is measured well enough now also shows the typical size such tasks have used. This round ran its own selection of tests rather than the whole test collection; a code-quality check and a repository-health check both passed as well. The branch has been pushed for review; no pull request was opened this round, as the plan for this step did not call for one.
