# Handback — F307 round 17: book round 16 with R-1279; R-1313, a `remedy.toml` that cannot be read answered `config_invalid` with exit code 2, at interface 1.27

## Session

SESSION 4 of feature F307 · round 17 · rounds so far 17

Context self-assessment: this worker verified every prepared digest before any write, applied C1 through a byte-proof script and C2 as the prepared patch without a hand edit, read each staged diff before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~72 % (T001 to T006, T010, T011, T014, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414, R-1415 and R-1416 landed, R-1281's writer part landed, R-1313 under review · the rest open) — Schätzung

## Range

Review of `2ab710265`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### d1e3cb340 F307 R17 C1: book round 16 with R-1279, DECISION F307 D17, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r17.md` | 84/0 | NEW FILE, this round's block, byte copy (84 lines, sha256 `0cbef0c8a6fa53e256038463366737cb462d0282964b72753e1fd153059ebab6`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D17) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 16's Gate verdict PASS, R-1279 done) |
| `.agent/plan.md` | 8/8 | replaced with the prepared file |

108 insertions, 8 deletions over 4 files (`git show --shortstat`).

### 5e856d993 F307 R17 C2: a remedy.toml that cannot be read is answered config_invalid with exit code 2 and no crash report, at 1.27 (R-1313)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/grouped.py` | 7/0 | `_dispatch` answers `BudgetConfigError` from the logging setup with `config_invalid`, exit code 2, no crash report |
| `apps/cli/exit_codes.py` | 5/4 | exit code 2's meaning names the file |
| `apps/cli/client_interface.py` | 4/3 | `CLIENT_INTERFACE_VERSION` 1.26 to 1.27 |
| `packages/orchestration/public_api.py` | 3/2 | `PUBLIC_API_VERSION` 1.26 to 1.27 |
| `docs/guides/exit-codes.md` | 1/1 | code 2 row equals the code |
| `docs/system/machine-client-contract-v1.md` | 5/2 | since-1.27 paragraph; generated version and code 2 row |
| `docs/system/public-http-api-v1.md` | 1/1 | generated page, version 1.27 |
| `docs/system/api-release-matrix-v1.json` | 16/2 | `current` 1.27 and the 1.27 value change |
| `docs/README.md` | 2/2 | version range 1.17-1.27 |
| `tests/cli/test_json_envelope.py` | 32/3 | malformed-file tests: JSON and text answers, exit 2, no crash report |
| `tests/cli/test_client_interface.py` | 1/1 | version pin |
| `tests/ui_server/test_public_api.py` | 9/9 | version pins |

86 insertions, 30 deletions over 12 files (`git show --shortstat`).

### (this commit) F307 R17 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `2ab710265c27922b0ea10ce692c1030dbad55faf`, tree clean, no pull run |
| C1 | done | commit `d1e3cb340`, 108 insertions, byte proofs all held |
| C2 | done | commit `5e856d993`, 86 insertions, patch applied without a hand edit |
| C3 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 7 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 201`, `exit 0`, `7940 passed, 2 skipped in 183.39s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `24` |
| Gate 6 | done | `git diff --stat 6e9f3c48b HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r17-worker/` (created this round) holds the C1 byte-proof, gate-4 script, the two commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `a13d208c7627ed95572b5c4f91f965922330a67d782a6677a228780e0edcbe8d` and `block.md` sha256 `0cbef0c8a6fa53e256038463366737cb462d0282964b72753e1fd153059ebab6` (84 lines) both equal the delivering prompt; the seven other files listed matched their digests.
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `2ab710265c27922b0ea10ce692c1030dbad55faf`; tree clean; no `.agent/STOP`.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C2).
4. Gate 2: `python3 .remedy-wt/f307-r17/prep/ruff_touched.py <root>` — exit 0, `ruff over 7 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r17/prep/run_selection.py <root> .remedy-wt/f307-r17-worker/selection-output.txt` — `paths 201`, `exit 0`, `7940 passed, 2 skipped in 183.39s (0:03:03)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line in the printed summary.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — exit 0, `24`.
8. Gate 6: `git -C <root> diff --stat 6e9f3c48b HEAD -- packages apps scripts tests docs` — empty.

## Authored-text proofs

`.agent/authored/f307-r17.md` equals `block.md`: 84 lines, sha256 `0cbef0c8a6fa53e256038463366737cb462d0282964b72753e1fd153059ebab6` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing. `c2.patch` was applied unchanged after `git apply --check`, its digest matching; gate 6 shows the committed product bytes equal the reviewer's dry run.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C3), each touching only its named paths. No mutation red-proof, no full suite, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently. Two shell calls were refused by the sandbox before running (a compound command) and were re-issued as single commands; nothing was written by them.

## For the operator, in plain sentences

When the settings file cannot be read, Remedy now says the settings file is broken and exits with the code for a wrong invocation, instead of reporting a crash of its own and leaving a crash report behind. The published interface version for programs that drive Remedy rises by one step, because they now receive that different answer.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 17's handback and book its verdict, with R-1313, in the next round's first commit.
4. T009, the public API: R-1303, R-1304, R-1305, R-1308 and R-1309.

Operator questions open: 0. Open findings count gate 5 printed: 24.
