# Handback — F307 round 25: book round 24 with R-1403; R-1411 and R-1419, the data root guard

## Session

SESSION 6 of feature F307 · round 25 · rounds so far 25

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2 by `git apply` from the reviewer's cut patch with no hand-retyping, read the staged diff in full against the patch before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~93 % (T001 to T017, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1381, R-1403, R-1414 to R-1417 landed, R-1281's writer part landed, R-1411 and R-1419 under review · the rest open) — Schätzung

## Range

Review of `c567ff112`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 59d1662c4 F307 R25 C1: book round 24 with R-1403, R-1419, DECISION F307 D25, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r25.md` | 83/0 | NEW FILE, this round's block, byte copy (83 lines, sha256 `604741ede974251320538b242ddab6618655afa5bc8c216d73c944c6ccd3a103`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D25) |
| `.agent/live_review.md` | 6/0 | prepared slice appended (round 24's Gate verdict PASS; R-1403 RESOLVED; R-1419 registered) |
| `.agent/plan.md` | 7/6 | replaced with the prepared file |

108 insertions, 6 deletions over 4 files (`git show --shortstat`).

### a39eab1c4 F307 R25 C2: the data root guard reads its two levels and excuses a foreign supervisor's own folders (R-1411, R-1419)
| Path | +/- | Reason |
|---|---|---|
| `tests/conftest.py` | 49/5 | `_data_root_fingerprint` takes `os.fspath(root)` first (R-1419); `SUPERVISOR_OWN_CLASSES`, `_foreign_supervisor_answers` and `_data_root_guard_verdict` added; `pytest_configure` records whether a foreign supervisor answers, `pytest_sessionfinish` excuses its own classes and prints an `R-1411:` notice when it does (R-1411) |
| `tests/regression/test_data_root_guard.py` | 46/2 | imports extended; four new tests: the supervisor's own folders are excused only while a foreign one serves, a record the run wrote still fails beside a foreign supervisor, a `Path` root reads two levels too, a root no supervisor serves has no foreign supervisor |
| `tests/regression/test_data_root_guard_supervisor.py` | 75/0 | NEW FILE: a real child pytest run beside a unix-socket listener standing in for the installed service's supervisor, proving the excuse and the still-failing case end to end |

170 insertions, 7 deletions over 3 files (`git show --shortstat`); applied from `c2.patch`, not hand-retyped.

### (this commit) F307 R25 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `c567ff112f2559f0f3b7139b3221909867506b71`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `59d1662c4`, 108 insertions, byte proofs all held |
| C2 | done | commit `a39eab1c4`, 170 insertions, applied from `c2.patch` |
| C3 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 3 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 392`, `exit 0`, `13200 passed, 7 skipped in 290.77s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `10` |
| Gate 6 | done | `git diff --stat 8d13d4a33 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r25-worker/` (created this round) holds the digest-verification readings, the C1 byte-proof script, the gate-4 integrity script, the two commit-message files and the selection output.

## Verification

1. Digests, before any write: `digests.txt` sha256 `e502c35168a9c0c1dcbe0faf195924c0066877083c151675211b32fa2da479f1` and `block.md` sha256 `604741ede974251320538b242ddab6618655afa5bc8c216d73c944c6ccd3a103` (83 lines) both equal the delivering prompt; the six other listed entries (`c1-.agent__plan.md`, `c1-decisions-append.txt`, `c1-live_review-append.txt`, `c2.patch`, `ruff_touched.py`, `run_selection.py`, `selection.txt`) matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `c567ff112f2559f0f3b7139b3221909867506b71`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C2, before C3).
4. Gate 2: `python3 .remedy-wt/f307-r25/prep/ruff_touched.py <root>` — `files: tests/conftest.py tests/regression/test_data_root_guard.py tests/regression/test_data_root_guard_supervisor.py`, `ruff over 3 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r25/prep/run_selection.py <root> .remedy-wt/f307-r25-worker/selection-output.txt` — `paths 392`, `exit 0`, `13200 passed, 7 skipped in 290.77s (0:04:50)`. SKIPPED: `tests/orchestration/test_builder_bridge_smoke.py:118` (Ollama smoke, opt-in), `tests/orchestration/test_real_ollama_smoke.py:96,100,134` (Ollama smoke, opt-in, 3 lines), `tests/regression/test_f293_acceptance.py:195` (main holds F293), `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line; the full output was also scanned for lines starting `R-1411:`, `R-0803:` or `R-1419:` — none found, so the foreign-supervisor branch never fired on this run (no supervisor answered the test roots used).
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `10`.
8. Gate 6: `git -C <root> diff --stat 8d13d4a33 HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r25.md` equals `block.md`: 83 lines, sha256 `604741ede974251320538b242ddab6618655afa5bc8c216d73c944c6ccd3a103` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2 was the reviewer's cut patch (`c2.patch`) applied with `git apply --check` then `git apply`, never retyped; the staged diff was read in full before its commit and matched the patch hunk for hunk, touching exactly the three paths `git apply --numstat` named, adding one file.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C3), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

On the operator's machine a test run no longer fails because Remedy's own background service wrote its request log or a project record while the tests ran; a test that wrongly writes Remedy's real data still fails, and the check now looks one folder deeper, as it always said it did.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 25's handback and book its verdict, with R-1411 and R-1419, in the next round's first commit.
4. R-1291, the two doctor report shapes.

Operator questions open: 0. Open findings count gate 5 printed: 10.
