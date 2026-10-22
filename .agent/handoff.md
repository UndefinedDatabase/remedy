# Handback — F307 round 28: book round 27 with R-1291, DECISION F307 D28, the plan; T021 (`run_job`'s step (3)) begun

## Session

SESSION 6 of feature F307 · round 28 · rounds so far 28

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2 by `git apply --check --index` then `git apply --index` from the reviewer's cut patch with no hand-retyping, read the staged diff in full against the patch before committing, and ran each gate once; context is ample and nothing was lost.

Session end (the reviewer, after its verdict on round 28): this session ran seven delegated rounds, 22 to 28, and ends because the next work, F307's closure sequence, is planned as a session of its own (DECISION F307 D28). It worked T016 to T021: it booked R-1332 and resolved R-1331, R-1325, R-1327, R-1328, R-1381, R-1403, R-1411, R-1419, R-1330 and R-1291; it registered R-1418 for the next paydown and R-1419, which it repaired, and decided to carry R-1326 (DECISION F307 D28 (2)). No prose slip was written. Context self-assessment: every product commit was built by script in the disposable dry tree, run and red-proved there, and the worker's commit compared by bytes; two of the session's own transforms failed in the dry tree first (a leftover `__pycache__` folder that nested a moved folder, and a pinned scrubber rule), and neither reached the branch.

Fortschritt: ~97 % (T001 to T020, R-1280, R-1290, R-1291, R-1292, R-1297, R-1298, R-1301, R-1330, R-1381, R-1403, R-1411, R-1414 to R-1417, R-1419 landed, R-1281's writer part landed, T021 under review · the closure open) — Schätzung

## Range

Review of `781b547c3`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 7d14bcf81 F307 R28 C1: book round 27 with R-1291, DECISION F307 D28, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r28.md` | 81/0 | NEW FILE, this round's block, byte copy (81 lines, sha256 `bdd409464a8b62bd1fdf3826320ac2b3e65141c1e4fffd40fc547c1e8885ec07`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D28) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 27's Gate verdict PASS; R-1291 RESOLVED) |
| `.agent/plan.md` | 8/11 | replaced with the prepared file |

105 insertions, 11 deletions over 4 files (`git show --shortstat`).

### 4101d0968 F307 R28 C2: the final job review becomes a function of its own, structural step (3) of run_job begun
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 4/3 | step (3) begun, recorded; `run_job` row lowered 1434 → 1381; `pingpong_job.py` row lowered 4943 → 4939 |
| `packages/orchestration/pingpong_job.py` | 50/54 | the final job review moves verbatim into `_write_final_job_review(job)`, a module-level function; the call site in `run_job` becomes one line |
| `tests/test_structure_ratchet.py` | 2/2 | `MAX_FUNCTION_LINES` lowered 28601 → 28548, `MAX_FILE_LINES` lowered 63067 → 63063, the ratchet following the drop |

56 insertions, 59 deletions over 3 files (`git show --shortstat`); applied from `c2.patch` via `git apply --check --index` then `git apply --index`, never hand-retyped; the staged diff matched the patch exactly (only the two abbreviated-vs-full blob-hash `index` lines differed, same blobs) before commit.

### (this commit) F307 R28 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `781b547c34007b5c82dddbae26af014c75298b04`, tree clean, no pull run, no `.agent/STOP`, no open PR (`gh pr list` empty) |
| C1 | done | commit `7d14bcf81`, 105 insertions/11 deletions, byte proofs all held |
| C2 | done | commit `4101d0968`, 56 insertions/59 deletions over 3 files, applied from `c2.patch` |
| C3 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 2 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 386`, `exit 0`, `12952 passed, 6 skipped in 208.12s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `6` |
| Gate 6 | done | `git diff --stat 436673749 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, no open PR (Open PR Gate passed, no merge needed). Push follows this commit and is reported in the session reply. `.remedy-wt/f307-r28-worker/` (created this round) holds the digest-verification script, the C1 byte-proof script, the gate-4 integrity script, the two commit-message files for C1/C2, and the selection output.

## Verification

1. Digests, before any write: `digests.txt` sha256 `3dcfec94e1784afc156f6ecea91c1786b0e2646799e2b17f0276242b6c92c30a` and `block.md` sha256 `bdd409464a8b62bd1fdf3826320ac2b3e65141c1e4fffd40fc547c1e8885ec07` (81 lines) both equal the delivering prompt; the six other listed entries (`c1-.agent__plan.md`, `c1-decisions-append.txt`, `c1-live_review-append.txt`, `c2.patch`, `ruff_touched.py`, `run_selection.py`, `selection.txt`) matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `781b547c34007b5c82dddbae26af014c75298b04`; tree clean; `gh pr list --state open ...` returned `[]`.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C2, before C3).
4. Gate 2: `python3 .remedy-wt/f307-r28/prep/ruff_touched.py <root>` — `files:` lists 2 Python files changed since the base (`packages/orchestration/pingpong_job.py`, `tests/test_structure_ratchet.py`), `ruff over 2 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r28/prep/run_selection.py <root> .remedy-wt/f307-r28-worker/selection-output.txt` — `paths 386`, `exit 0`, `12952 passed, 6 skipped in 208.12s (0:03:28)`. SKIPPED: `tests/orchestration/test_builder_bridge_smoke.py:118` (opt-in, `REMEDY_SMOKE_OLLAMA=1`), `tests/orchestration/test_real_ollama_smoke.py:96,100,134` (opt-in, `REMEDY_REAL_OLLAMA_SMOKE=1`), `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR, `process(es) behind`, `R-1411:` or `R-0803:` line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `6`.
8. Gate 6: `git -C <root> diff --stat 436673749 HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r28.md` equals `block.md`: 81 lines, sha256 `bdd409464a8b62bd1fdf3826320ac2b3e65141c1e4fffd40fc547c1e8885ec07` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2 was the reviewer's cut patch (`c2.patch`) applied with `git apply --check --index` then `git apply --index`, never retyped; the staged diff was read in full before commit and matched the patch exactly (modulo abbreviated blob-hash `index` lines, same blobs), with no file added or changed outside the patch.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1, C2), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## Reviewer verdict of round 28 (carried here under amend0827 rule 1)

VERDICT PASS. Book this paragraph byte for byte, preceded by one empty line, at the end of
`.agent/live_review.md` in the next round's first commit:

Gate: F307 R28 — the F307 round 28 entry, over `781b547c3`..`700eeffbf` (3 commits, each single-parent; insertions by `git show --shortstat`: `7d14bcf81` 105, `4101d0968` 56, `700eeffbf` 39). VERDICT PASS, verified by dry run, bytes identical: the product tree of `4101d0968` equals the reviewer's dry-run commit `436673749`, the ledger and the decisions file each equal their pre-image plus the prepared slice, and the plan and the saved block equal the prepared files. C2 moves the final job review verbatim into `_write_final_job_review`, with two list literals and one call joined; `run_job` fell from 1434 to 1381 lines and `pingpong_job.py` from 4943 to 4939, the rows and both pins with them. In a disposable worktree at `436673749`, two mutations turned `tests/orchestration/test_pingpong_integration.py` red: `run_job` no longer calling the review (three tests), and the review writing no blocking record (one test). The selection, 386 paths, read `12952 passed, 6 skipped` with exit 0, the worker's one run the same; ruff read clean over the 2 Python files, the integrity check `fail_count` 0, and the open set 6 ids.

## For the operator, in plain sentences

Nothing a person sees changes; the largest part of Remedy's job runner got smaller, and this batch of repairs is ready to be closed in the next working session.

This working session finished the remaining repairs of this batch but one. When a job stops because one of its steps could not be finished, a person can now try that step again, and the job's overview offers it. The overview also says how many uncommitted files a job started from and names them for programs. Remedy's own practice run no longer picks a repair that was already made, and the tests no longer fail because Remedy's background service wrote its logs while they ran. Remedy's two health commands now report in the same way, and the part that answers programs over the network has a name that says so. Choosing the models of a project in its own settings file was moved to the next batch, because it needs a larger part of the job runner reshaped first. The next working session closes this batch.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Round 28 is reviewed (PASS): book the paragraph of the section "Reviewer verdict of round 28" above
   in the next round's first commit.
4. The closure sequence of F307, per `docs/roadmap/STATUS_closure_protocol.md`: the one full suite, the
   evidence package, the Built State, the next findings paydown registered with R-1246, R-1326, R-1351,
   R-1353, R-1418 and R-1281's rest, the ledger rotation and the STATUS flip. Session 7 of F307 begins;
   the soft limit is 8 sessions.

Operator questions open: 0. Open findings count gate 5 printed: 6.
