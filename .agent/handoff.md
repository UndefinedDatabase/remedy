# Handback — F199 round 4: book round 3, repair R-1267 and R-1268, and T002 the local crash report and the check crash_reports

## Session

SESSION 1 of feature F199 · round 4 · rounds so far 4

Context self-assessment: the block and the modules it named were enough to write the report, the check and the tests without a second look; I could not run any test but gate 3, so the new tests were written against the code's text and gate 3 was the first time they ran.

Fortschritt: ~65 % (T001 and T002 complete · T003 and the closure open) — Schätzung

## Range

Review of `19bc8f46d`..HEAD (round 4: C1 to C6, then C7; this handback is C7).

## Commits

### a41203b51 F199 R4 C1: book round 3, register R-1267 and R-1268, save the round 4 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f199-r4.md` | +218/-0 | NEW FILE, byte copy of `block.md` (218 lines, sha256 `d9377333ce0c16f1c11d5fbdbf19061f11a981f2e233e23792991a02811f61c8`) |
| `.agent/live_review.md` | +6/-0 | byte copy of `dry-live_review.md` |
| `.agent/plan.md` | +7/-8 | byte copy of `dry-plan.md` |

### 665417afe F199 R4 C2: an unreadable snapshot manifest fails its check, and the page states the worktree levels (R-1267, R-1268)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/self_health.py` | +5/-1 | `_snapshot_problems` answers "its manifest cannot be read" on AttributeError or TypeError |
| `tests/orchestration/test_self_health.py` | +10/-0 | a manifest that is the JSON list `[1, 2]` fails the check, folder named |
| `docs/system/self-health-v1.md` | +2/-1 | `worktrees` WARN-when reads only the gone folder; one sentence says an unreadable repository is named and changes no level |

### eb74a80e2 F199 R4 C3: the local crash report and its data-root class (T002)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/crash_report.py` | +147/-0 | NEW FILE: constants, `crash_reports_dir`, `remedy_version`, `config_digest`, `render_crash_report`, `write_crash_report`, `install_thread_crash_hook`, `recent_crash_reports` |
| `packages/orchestration/data_paths.py` | +3/-0 | `DURABLE_CLASSES` gains `crash`, last |

### ce8b5701d F199 R4 C4: a crash writes its report at the catch-all and in the supervisor, and the check crash_reports (T002)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/grouped.py` | +13/-0 | `_dispatch` writes the report, `--json` carries `crash_report`, text prints one more stderr line, docstring names D1 |
| `apps/cli/commands/serve_cmd.py` | +5/-0 | thread hook installed around `run_supervisor`, restored in a `finally` |
| `packages/orchestration/self_health.py` | +28/-0 | `CRASH_HINT`, `check_crash_reports`, added last to `run_health_checks` |
| `apps/cli/command_catalog_doctor.py` | +2/-2 | description names the recent crash reports |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.crash_report` in its sorted place (lazy import joins the closure) |

### b90388e68 F199 R4 C5: the crash report's tests with planted secrets (T002)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_crash_report.py` | +162/-0 | NEW FILE: planted-secret fixture, header lines, unwritable folder, digest unavailable, thread hook (report, previous hook, restore, SystemExit), recent reports |
| `tests/orchestration/test_self_health.py` | +27/-2 | `check_crash_reports` PASS and WARN; the set test answers eight |
| `tests/cli/test_doctor_health_cmd.py` | +3/-3 | counts become eight (9 lines, `1 of 8`) |
| `tests/cli/test_json_envelope.py` | +33/-0 | text and `--json` cases write one report and name it; SystemExit and KeyboardInterrupt leave the folder empty |

### 06e59122f F199 R4 C6: the self-health page describes the crash report

| Path | +/- | Reason |
|---|---|---|
| `docs/system/self-health-v1.md` | +20/-6 | banner, `crash_reports` row, example line, `1 of 8`, section "The crash report", "Not yet" keeps the health route |
| `docs/README.md` | +1/-1 | the system-table row names eight checks and the crash report |

### (this commit) F199 R4 C7: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this handback |

## External actions

- `git push origin feature/f199-self-health` runs after this commit; its result is in the session's final reply. No pull request opened, no worktree added.

## Verification

Preconditions: branch `feature/f199-self-health`, HEAD `19bc8f46d`, `git status --porcelain` empty. Digests of `block.md` (218 lines), `run_selection.py`, `selection.txt` and the two `dry-*` files matched.

Gate 1: `git -C /home/decodeux/Repos/remedy status --porcelain` — empty.

Gate 2: the ordered `python3 -m ruff check` over the ten paths — `All checks passed!`

Gate 3 (HEAD `06e59122f`, run once): exit 0, `4293 passed, 3 skipped in 46.07s`; no FAILED, ERROR, `absent in tree:` or `process(es) behind` line (the saved output was searched). SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine F252), `tests/test_install_smoke.py:175` (opt-in install smoke), `tests/test_repair_context_reviewer_memory.py:257` (UI source not found).

Gate 4: `python3 -m apps.cli.main integrity check --json` — `fail_count` 0, `ok` true.

Gate 5: `open_finding_ids` -> `['R-1235', 'R-1246', 'R-1251', 'R-1252', 'R-1267', 'R-1268']`.

Gate 6: `python3 -m apps.cli.main doctor health`:
```
Remedy health: PASS
  [PASS] config: every configured value has its declared type
  [PASS] ledgers: 2 of 2 token ledgers passed SQLite's integrity check
  [PASS] snapshots: 20 of 20 newest workspace snapshots passed their hash check
  [PASS] worktrees: 12 repositories checked; no worktree is prunable
  [PASS] providers: reachable: claude-cli, ollama; not reachable: claude; no provider was called
  [PASS] staging_copies: 0.0 GB of staging copies can be freed, below the warning level of 5 GB
  [PASS] disk: 1186442829824 bytes free; no floor is configured (budget.min_free_disk_bytes)
  [PASS] crash_reports: no crash report in the last 7 days
```

## Authored-text proofs

C1's two `dry-*` files were copied over their paths; `git diff --cached --numstat` named exactly three paths with `218 0`, `6 0`, `7 8`. The block copy `.agent/authored/f199-r4.md` has 218 lines and sha256 `d9377333ce0c16f1c11d5fbdbf19061f11a981f2e233e23792991a02811f61c8`, equal to the delivering prompt.

## Deviations & assumptions

1. The block's commit order and paths were followed; the reachability allowlist line in C4 was the block's conditional path and I judged it needed (a function-body import joins the closure). Gate 3 passed with it.
2. `write_crash_report` computes the version and the digest inside its guarded block, so any OSError, ValueError or TypeError from them also gives `None`; the block names those classes only for the file work.
3. `render_crash_report` treats a naive `when` as UTC.
4. No red-proof and no test run other than gate 3 were done; the new tests ran for the first time in gate 3 and were green.

## For the operator, in plain sentences

When a Remedy command or the background service stops on an error nobody expected, Remedy now writes a short report on this machine. It holds the error and where it happened, with passwords and keys removed, and Remedy says where the file is. It never sends the report anywhere. The health command warns for a week after such a report.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. Phase 1 rule 2: the Open PR Gate.
3. The next round's first commit books round 4's verdict.
4. T003, the supervisor's health route.

Operator questions open: 0.
Open findings: 6 — R-1235, R-1246, R-1251 and R-1252 owned by F306, R-1267 and R-1268 owned by F199 (their repairs landed this round, awaiting review).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | three paths, numstat as ordered; block copy 218 lines and digest equal |
| C2 | done | manifest repair, its test, the page's worktree levels |
| C3 | done | crash_report module and the `crash` class |
| C4 | done | catch-all, supervisor hook, check, description, allowlist line |
| C5 | done | tests with planted secrets; counts at eight |
| C6 | done | page and index row |
| C7 | done | this handback |
| Gate 1 | passed | status empty |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | exit 0, `4293 passed, 3 skipped`, first run |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | exact open-finding set |
| Gate 6 | passed | exit 0, all eight checks PASS |
| R-1267 | done | repair landed in C2, awaiting review |
| R-1268 | done | repair landed in C2, awaiting review |
| T002 | done | the report, the check, tests and page |
