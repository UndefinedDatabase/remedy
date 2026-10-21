# Handback — F307 round 4: book round 3 and four resolutions, DECISION F307 D5, T014, R-1280

## Session

SESSION 1 of feature F307 · round 4 · rounds so far 4

Context self-assessment: this worker verified every prepared digest, byte-copied the prepared files, self-reviewed each diff before committing, ran each gate once (apart from one disclosed duplicate ruff invocation) and wrote this handback from what it read; context is ample and nothing was lost.

Fortschritt: ~24 % (T001 to T004, T014 and R-1280 landed · the rest open) — Schätzung

## Range

Review of `573ef796e`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 93438e281 F307 R4 C1: book round 3, R-1286, R-1288, R-1294 and R-1310, DECISION F307 D5, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r4.md` | 107/0 | NEW FILE, this round's block, byte copy (107 lines, sha256 `48f7d520eb3204bcb388d5d50dd2acf1aeeed8237981db4d6a9f69540c3dcc7b`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy (DECISION F307 D5) |
| `.agent/live_review.md` | 10/0 | prepared file, byte copy (round 3's verdict and its four resolutions booked: R-1286, R-1288, R-1294, R-1310) |
| `.agent/plan.md` | 7/6 | prepared file, byte copy |
| `docs/roadmap/features/T2_F307.md` | 3/0 | prepared file, byte copy (the round-4-on slice order recorded under the slice list) |

### 843db401e F307 R4 C2: a lock with no packages, a race test that cannot pass empty, two records corrected (R-1302, R-1306, R-1307, R-1319)
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F297.md` | 2/2 | prepared file, byte copy (R-1307: SU-056's record corrected to say it paused) |
| `packages/orchestration/repo_catalog_plausibility.py` | 2/0 | prepared file, byte copy (R-1302: a TOML lock with no `[[package]]` table reads as no names) |
| `tests/cli/test_rehearsal.py` | 6/6 | prepared file, byte copy (R-1319: docstring corrected to say what the counter test guards) |
| `tests/orchestration/test_dod_runners.py` | 5/1 | prepared file, byte copy (R-1306: the port-race test fails when neither racer passed) |
| `tests/orchestration/test_repo_catalog_plausibility.py` | 9/0 | prepared file, byte copy (new test for R-1302) |

### 8989215a3 F307 R4 C3: a private key hides only its part of a crash report or a log line (R-1280)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/crash_report.py` | 9/7 | prepared file, byte copy (R-1280: command, error and each traceback entry redacted on their own) |
| `packages/orchestration/structured_log.py` | 5/4 | prepared file, byte copy (R-1280: `TextLogFormatter` redacts the message and the exception on their own) |
| `tests/orchestration/test_crash_report.py` | 32/0 | prepared file, byte copy (new tests for R-1280) |
| `tests/orchestration/test_structured_log.py` | 10/0 | prepared file, byte copy (new test for R-1280) |

### (this commit) F307 R4 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD `573ef796e` equal to `origin/feature/f307-findings-paydown-v9`, tree clean |
| C1 | done | records commit `93438e281` |
| C2 | done | T014 repair commit `843db401e` |
| C3 | done | R-1280 repair commit `8989215a3` |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every counted line, `absent C4` (not yet counted), last line `ALL True` |
| Gate 2 | done | `ruff check` printed `All checks passed!`, exit 0 |
| Gate 3 | done | 80 paths, exit 0, `3612 passed, 2 skipped in 40.52s`, two SKIPPED lines, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `47` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own, no provider call, no rotation.

## Verification

1. Digests: a python check over the 18 lines of `digests.txt` — every prepared file's sha256 read `OK` against the listed digest, last line `ALL_OK`. `block.md` and `digests.txt` themselves were also hashed first and matched the values given in the delivering prompt.
2. C0: `git branch --show-current` read `feature/f307-findings-paydown-v9`; `git rev-parse HEAD` and `git rev-parse origin/feature/f307-findings-paydown-v9` both read `573ef796e...`; `git status --porcelain` was empty before any write.
3. Gate 1: `git status --porcelain` (through `git -C`) — empty. `python3 .remedy-wt/f307-r4/prep/verify.py .` — every counted line `True` (single-parent checks on all three commits, the Cn-subject count 3 of 3, the branch check, every C1, C2 and C3 path-set and per-path equality check, and "the saved block equals block.md"); one line `absent C4` (not yet counted, C4 did not exist when the gate ran); last line `ALL True`.
4. Gate 2: `python3 -m ruff check packages/orchestration/repo_catalog_plausibility.py packages/orchestration/crash_report.py packages/orchestration/structured_log.py tests/orchestration/test_repo_catalog_plausibility.py tests/orchestration/test_dod_runners.py tests/cli/test_rehearsal.py tests/orchestration/test_crash_report.py tests/orchestration/test_structured_log.py`, run from the primary checkout — `All checks passed!`, exit 0.
5. Gate 3: `python3 .remedy-wt/f307-r4/prep/run_selection.py . .remedy-wt/f307-r4-worker/selection-output.txt` — `paths 80`, `exit 0`, `3612 passed, 2 skipped in 40.52s`. SKIPPED lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (install smoke is opt-in). No FAILED, no ERROR, no `process(es) behind` line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0 — `fail_count` 0; all six checks pass: `handler_import` ("handlers=194"), `live_review_verdict` ("last Gate verdict PASS"), `plan_consistency` ("unchecked=0, context_complete=False"), `relevant_untracked` ("untracked=0, relevant=0"), `repo_root_hygiene` ("no reviewer scratch, evidence dir or archive at the root"), `high_blockers_open` ("no open blocker/high findings").
7. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `47`.

## Authored-text proofs

C1's five prepared files, C2's five prepared files and C3's four prepared files are byte copies of the prepared files; each was proved equal by a sha256 comparison right after the copy, before staging, and `verify.py` re-proved every one of them (`True`). `.agent/authored/f307-r4.md` equals `block.md`: 107 lines, sha256 `48f7d520eb3204bcb388d5d50dd2acf1aeeed8237981db4d6a9f69540c3dcc7b` on both sides.

## Deviations & assumptions

One disclosed deviation, with no effect on any gate's result: before running Gate 2's exact command (relative paths, cwd at the repository root, matching the block literally), this worker first ran an equivalent `ruff check` invocation using absolute file paths as a sanity check, before settling on the literal cwd-anchored form for the recorded gate run. That is a second invocation of the same check rather than the single run the block calls for; both runs printed `All checks passed!` with no difference in outcome. No other command was repeated, and no mutation or full-suite run was attempted.

The prep directory also holds files not listed in `digests.txt` (several `src-*` sources). Since the block names `digests.txt` as the list of every prepared file to use, and those are absent from it, they were left untouched and unread for content.

No other deviation. The commit sequence, paths and gate commands followed the block exactly; no file outside the named paths per commit was touched.

## For the operator, in plain sentences

This round booked the previous round's closing verdict and the four resolutions it carried into the running record, and recorded a decision that reorders the remaining work so the steps touching no function or file the structure ledger lists run before the steps that need a boundary drawn first. It then repaired four small defects: a dependency lock file with no packages now reads as holding none instead of failing; a test that races two startup attempts now requires that at least one of them actually succeeds, instead of silently passing when both fail; a test's own docstring was corrected to describe the real reason a counter has to start before its mocks are installed; and a past record was corrected to say a self-use step paused rather than finished. Finally, a crash report and a plain-text log line each now hide only the one part of themselves that carries a secret, so a private key found in a command, an error or one frame of a traceback no longer erases the rest of the report or the rest of the line around it. All five required checks ran once each (with one harmless duplicate check noted above) and came back exactly as expected. No question waits for the operator.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 4's verdict in the next round's first commit.
4. T007's module-local half: R-1290 and R-1292.

Operator questions open: 0. Open findings count gate 5 printed: 47.
