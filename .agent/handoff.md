# Handback — F307 round 18: book round 17 with R-1313; T009, the public API's refusals: R-1303, R-1304, R-1308, R-1309 and R-1305

## Session

SESSION 4 of feature F307 · round 18 · rounds so far 18

Context self-assessment: this worker verified every prepared digest before any write, applied C1 through a byte-proof script and C2 to C4 as the prepared patches without a hand edit, read each staged diff before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~76 % (T001 to T006, T008, T010, T011, T014, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414, R-1415 and R-1416 landed, R-1281's writer part landed, T009 under review · the rest open) — Schätzung

## Range

Review of `9d0f2d39a`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 9f9ecd23a F307 R18 C1: book round 17 with R-1313, DECISION F307 D18, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r18.md` | 95/0 | NEW FILE, this round's block, byte copy (95 lines, sha256 `3365c8b48aa6acb60e2d1cf8d725982043d6f7edb3185471ddb98b2b0b1fbc16`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D18) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 17's Gate verdict PASS, R-1313 done) |
| `.agent/plan.md` | 8/8 | replaced with the prepared file |

119 insertions, 8 deletions over 4 files (`git show --shortstat`).

### 1fc1fab05 F307 R18 C2: PATCH, HEAD and OPTIONS under the public API are refused by name with a ledger line, and the server names itself Remedy (R-1303, R-1304)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/ui_server.py` | 13/15 | one `_refuse_public_api_method` for PUT, DELETE, PATCH, HEAD, OPTIONS; `version_string` answers `Remedy` |
| `packages/orchestration/serve_daemon.py` | 6/28 | the public port forwards all seven methods through one method |
| `packages/orchestration/public_api.py` | 12/9 | `public_api_method_refusal` takes the method and names it; version comment |
| `docs/system/public-http-api-v1.md` | 8/6 | the refused methods and the `Server` header |
| `docs/system/api-release-matrix-v1.json` | 12/0 | two value changes of 1.27 |
| `docs/system/structure-ledger-v1.md` | 1/1 | `ui_server.py` row 1826 to 1824 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` lowered by 2 |
| `tests/ui_server/test_public_api.py` | 30/0 | method named, ledger lines, `Server: Remedy` |
| `tests/orchestration/test_serve_daemon.py` | 1/1 | PATCH and OPTIONS added to the not-served parametrization |

84 insertions, 61 deletions over 9 files (`git show --shortstat`).

### 341cb6057 F307 R18 C3: a bad query value gets its own sentence and every route refuses a path value that leaves its place (R-1308, R-1309)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 31/18 | `_path_value_refusal` shared by GET and POST; the query loop gives a declared key its own sentence |
| `docs/system/public-http-api-v1.md` | 4/1 | the query message and `api_path_invalid` on every route |
| `docs/system/api-release-matrix-v1.json` | 12/0 | two value changes of 1.27 |
| `docs/system/structure-ledger-v1.md` | 1/1 | `answer_public_api_post` row 157 to 151 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` lowered by 6 |
| `tests/ui_server/test_public_api.py` | 33/6 | new query and path tests; the two `..%2Fx` tests expect the 400 refusal |

82 insertions, 27 deletions over 6 files (`git show --shortstat`).

### 569be24b1 F307 R18 C4: the changes route says when a job's cost fields refresh (R-1305)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api_routes.py` | 3/1 | the changes route's description |
| `packages/orchestration/client_changes.py` | 5/0 | module docstring: the cost ledger is deliberately not watched |
| `docs/system/public-http-api-v1.md` | 1/1 | generated page row |
| `tests/ui_server/test_public_api.py` | 8/0 | route and page carry the sentence |

17 insertions, 2 deletions over 4 files (`git show --shortstat`).

### (this commit) F307 R18 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `9d0f2d39acfc482d3952f43b32098aebb546143e`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `9f9ecd23a`, 119 insertions, byte proofs all held |
| C2 | done | commit `1fc1fab05`, 84 insertions, patch applied without a hand edit |
| C3 | done | commit `341cb6057`, 82 insertions, patch applied without a hand edit |
| C4 | done | commit `569be24b1`, 17 insertions, patch applied without a hand edit |
| C5 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 8 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 98`, `exit 0`, `4347 passed, 2 skipped in 83.39s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `23` |
| Gate 6 | done | `git diff --stat 202ce9053 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r18-worker/` (created this round) holds the digest check, the C1 byte-proof, the gate-4 script, the five commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `6f65bf65fbe21ff34a04225adce2fb8ca18292e8a94c6f96283f83279f7c9d49` and `block.md` sha256 `3365c8b48aa6acb60e2d1cf8d725982043d6f7edb3185471ddb98b2b0b1fbc16` (95 lines) both equal the delivering prompt; the ten other listed entries matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `9d0f2d39acfc482d3952f43b32098aebb546143e`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C4).
4. Gate 2: `python3 .remedy-wt/f307-r18/prep/ruff_touched.py <root>` — `ruff over 8 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r18/prep/run_selection.py <root> .remedy-wt/f307-r18-worker/selection-output.txt` — `paths 98`, `exit 0`, `4347 passed, 2 skipped in 83.39s (0:01:23)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `23`.
8. Gate 6: `git -C <root> diff --stat 202ce9053 HEAD -- packages apps scripts tests docs` — empty.

## Authored-text proofs

`.agent/authored/f307-r18.md` equals `block.md`: 95 lines, sha256 `3365c8b48aa6acb60e2d1cf8d725982043d6f7edb3185471ddb98b2b0b1fbc16` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing. `c2.patch`, `c3.patch` and `c4.patch` were each applied unchanged after `git apply --check`; gate 6 shows the committed product bytes equal the reviewer's dry run.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C5), each touching only its named paths. No mutation red-proof, no full suite, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently. Two shell calls were refused by the sandbox before running (a heredoc and a `$?` reference) and were re-issued differently; nothing was written by them.

## For the operator, in plain sentences

A program that asks Remedy's web interface for something it does not offer now always gets a short machine-readable refusal saying what was wrong, and every such request is written to the interface's log; the server no longer tells callers which Python version it runs on; and the description of the "what changed" read now says that a job's cost figures refresh when the job itself changes.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 18's handback and book its verdict, with R-1303, R-1304, R-1305, R-1308 and R-1309, in the next round's first commit.
4. T013, R-1282 with `plan_source`.

Operator questions open: 0. Open findings count gate 5 printed: 23.
