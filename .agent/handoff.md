# Handback — F307 round 24: book round 23 with R-1325, R-1327 and R-1328; R-1381 stated, R-1418; R-1403, the self-use generator skips a landed repair

## Session

SESSION 6 of feature F307 · round 24 · rounds so far 24

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2 by `git apply` from the reviewer's cut patch with no hand-retyping, read the staged diff in full against the patch before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~92 % (T001 to T006, T008 to T011, T013 to T017, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1381, R-1414 to R-1417 landed, R-1281's writer part landed, R-1403 under review · the rest open) — Schätzung

## Range

Review of `acbf3311e`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### eb33ff14e F307 R24 C1: book round 23 with R-1325, R-1327 and R-1328, R-1381 stated, R-1418, DECISION F307 D24, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r24.md` | 81/0 | NEW FILE, this round's block, byte copy (81 lines, sha256 `bd3168a893db41f76f9fb11783bf23adfd7242c496b3074f1223746119930351`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D24) |
| `.agent/live_review.md` | 12/0 | prepared slice appended (round 23's Gate verdict PASS; R-1325, R-1327, R-1328 RESOLVED; R-1381 RESOLVED; R-1418 registered) |
| `.agent/plan.md` | 7/7 | replaced with the prepared file |

112 insertions, 7 deletions over 4 files (`git show --shortstat`).

### 66941a8dc F307 R24 C2: the self-use generator skips a finding whose repair has already landed (R-1403)
| Path | +/- | Reason |
|---|---|---|
| `docs/system/self-use-track-v1.md` | 4/1 | paragraph added: a finding whose repair has already landed is skipped too, not only one waiting on something outside the run's control (R-1403, DECISION F307 D24) |
| `packages/orchestration/self_use_generator.py` | 30/2 | `subprocess` import added; `_SUBJECT_FINDING_RE` and `_repaired_since_last_booking` added (reads the subjects of the commits after the ledger file's last changing commit); `_ledger_tier` excludes those ids too |
| `tests/orchestration/test_self_use_generator.py` | 28/0 | new test: a commit after the ledger's last change names a finding's id, so the next generation offers the next-oldest one instead |

62 insertions, 3 deletions over 3 files (`git show --shortstat`); applied from `c2.patch`, not hand-retyped.

### (this commit) F307 R24 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `acbf3311ee62cb0c7d02d0155679516861c71879`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `eb33ff14e`, 112 insertions, byte proofs all held |
| C2 | done | commit `66941a8dc`, 62 insertions, applied from `c2.patch` |
| C3 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 2 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 77`, `exit 0`, `3552 passed, 2 skipped in 35.46s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `10` |
| Gate 6 | done | `git diff --stat 26f09c20d HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r24-worker/` (created this round) holds the digest-verification readings, the C1 byte-proof script, the gate-4 integrity script, the two commit-message files and the selection output.

## Verification

1. Digests, before any write: `digests.txt` sha256 `e4b929d3b0273f6c8f868de8f720c1a7572d6961d4eaa37134002bf7d0e71095` and `block.md` sha256 `bd3168a893db41f76f9fb11783bf23adfd7242c496b3074f1223746119930351` (81 lines) both equal the delivering prompt; the six other listed entries (`c1-.agent__plan.md`, `c1-decisions-append.txt`, `c1-live_review-append.txt`, `c2.patch`, `ruff_touched.py`, `run_selection.py`, `selection.txt`) matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `acbf3311ee62cb0c7d02d0155679516861c71879`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C2, before C3).
4. Gate 2: `python3 .remedy-wt/f307-r24/prep/ruff_touched.py <root>` — `files: packages/orchestration/self_use_generator.py tests/orchestration/test_self_use_generator.py`, `ruff over 2 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r24/prep/run_selection.py <root> .remedy-wt/f307-r24-worker/selection-output.txt` — `paths 77`, `exit 0`, `3552 passed, 2 skipped in 35.46s`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `10`.
8. Gate 6: `git -C <root> diff --stat 26f09c20d HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r24.md` equals `block.md`: 81 lines, sha256 `bd3168a893db41f76f9fb11783bf23adfd7242c496b3074f1223746119930351` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2 was the reviewer's cut patch (`c2.patch`) applied with `git apply --check` then `git apply`, never retyped; the staged diff was read in full before its commit and matched the patch hunk for hunk, touching exactly the three paths `git apply --numstat` named, adding no file.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C3), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

When Remedy picks a finding for its own practice run, it no longer picks one that was already repaired and only waits to be marked as done, so the paid run is spent on real work.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 24's handback and book its verdict, with R-1403, in the next round's first commit.
4. R-1291, the two doctor report shapes.

Operator questions open: 0. Open findings count gate 5 printed: 10.
