# Handback — F296 round 2: book round 1, DECISION F296 D2, the tier escalation's keys, its ladder, the loop's two calls, its tests and its page

## Session

SESSION 1 of feature F296 · round 2 · rounds so far 2

Context self-assessment: this worker verified both prepared digests and every listed digest before any write, copied each prepared file by a script with a byte-for-byte proof, ran its self-review over each commit's staged diff before committing, ran every gate once, and context stayed ample throughout.

Fortschritt: ~35 % (T001a to T001c landed · T002a to T003 open) — Schätzung

## Range

Review of `c3eaeeeb6`..`HEAD` on `feature/f296-tier-escalation`.

## Commits

### e704bdecb F296 R2 C1: book round 1, DECISION F296 D2, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r2.md` | +98/-0 | NEW FILE, this round's block, byte copy, equal to `block.md` by line count and sha256 |
| `.agent/decisions.md` | +12/-0 | DECISION F296 D2: the trigger and the step |
| `.agent/live_review.md` | +2/-0 | round 1's verdict booked (amend0827-process-diet rule 1) |
| `.agent/plan.md` | +10/-9 | rewritten for round 2's scope |

### 62531cd40 F296 R2 C2: the tier escalation — three model_escalation keys, TaskTierLadder, and the loop's two calls
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/environment.md` | +3/-0 | the three `model_escalation` env-var rows |
| `packages/orchestration/config_keys_model_routing.py` | +45/-0 | the three config keys, after the failover cooldown |
| `packages/orchestration/pingpong_loop.py` | +16/-16 | `TaskTierLadder` built after the providers, called at `start_round` and `after_review`, `resumes` replacing the two fixed resume checks, the actor binding reading the ladder; line-neutral by joining five multi-line statements |
| `packages/orchestration/tier_escalation.py` | +275/-0 | NEW FILE: `TierModel`, `EscalationPolicy`, `parse_escalation_tiers`, `resolve_escalation_policy`, the trigger functions, `TaskTierLadder` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | the new module's entry |

### 824b474b0 F296 R2 C3: the tier escalation's tests, its page and its index rows
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_tier_escalation.py` | +371/-0 | NEW FILE: the pure decision, then three real `run_pingpong` runs (escalates on repeated failure, never on an unreachable provider, nothing with the switch off) |
| `docs/system/tier-escalation-v1.md` | +69/-0 | NEW FILE: the trigger, the step and the loop's call, what never moves a task, the configuration table |
| `docs/README.md` | +2/-0 | the quick-find row and the system-docs table row for the new page |

### (this commit) F296 R2 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C4: this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 (preconditions) | done | branch `feature/f296-tier-escalation` at `c3eaeeeb6`, `git status --porcelain` empty, confirmed before any write; Open PR Gate: `gh pr list --state open ...` returned an empty list |
| C1 | done | commit `e704bdecb`, byte proofs held for all four paths plus the authored file against `block.md` |
| C2 | done | commit `62531cd40`, byte proofs held for all five paths, self-review run over `git diff --cached` before committing |
| C3 | done | commit `824b474b0`, byte proofs held for all three paths, self-review run over `git diff --cached` before committing |
| C4 | done | this commit, the handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every line, `absent` for C4 (not yet committed when run), last line `ALL True` |
| Gate 2 | done | exit 0, `All checks passed!` over the four touched Python files |
| Gate 3 | done | exit 0, `8751 passed, 2 skipped in 87.89s`, no FAILED or ERROR line, no leftover-process line |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | printed `6`, matching the required count |
| Push | pending | reported in the session reply |

## External actions

None before this commit. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]` before any write, so the Open PR Gate needed no merge and no report. The push follows this commit and is reported in the session reply. No PR is opened this round (the block does not ask for one). No fetch, pull, merge or provider call. The scratch folder `.remedy-wt/f296-r2-worker/` holds the digest checker, the copy-and-verify script, the commit-message files, the gate-3 output file, and this handback's supporting checks.

## Verification

1. Digests before any write: `block.md` (98 lines) and `digests.txt` matched the two hashes given in the delivering prompt; every one of the seventeen files listed in `digests.txt` matched its sha256 (checked with a script run under `python3 -I`, last line `ALL_FILES_OK: True`).
2. Preconditions: `git branch --show-current` read `feature/f296-tier-escalation`, `git rev-parse HEAD` read `c3eaeeeb6784020949df6498e4681f97f6730202`, `git status --porcelain` printed nothing — all before any write. `.agent/STOP` did not exist. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]`.
3. C1: all four named paths plus the new `.agent/authored/f296-r2.md` copied by a script, then compared byte-for-byte (`hashlib.sha256` and raw equality) against the prepared source; `.agent/authored/f296-r2.md` read 98 lines and sha256 `60099c489746531ab8b3d1a55355e9833753141671676a53f5b92418dfb8ac05`, equal to `block.md`'s own on both counts. `git diff --cached --numstat` showed exactly the four named paths, 122 insertions and 9 deletions.
4. C2: all five named paths copied and compared byte-for-byte the same way; `git diff --cached --stat` and the full diff were read as the self-review this round's block requires — `pingpong_loop.py` landed at 16 insertions and 16 deletions (line-neutral, five multi-line statements joined), the new `tier_escalation.py` imports and a plain-Python import smoke-check both succeeded.
5. C3: all three named paths copied and compared byte-for-byte the same way; `git diff --cached --numstat` showed exactly the three named paths, 442 insertions, 0 deletions; the new test file and the new docs page were read in full before committing.
6. Gate 1: `git status --porcelain` (through `git -C` on the primary checkout) printed nothing. `python3 .remedy-wt/f296-r2/prep/verify.py <repository root>` printed one `True` line per check (19 of them), one `absent` line for the not-yet-committed handback commit, and `ALL True` last.
7. Gate 2: `python3 .remedy-wt/f296-r2/prep/ruff_touched.py <repository root>` printed `files: packages/orchestration/config_keys_model_routing.py packages/orchestration/pingpong_loop.py packages/orchestration/tier_escalation.py tests/orchestration/test_tier_escalation.py`, `ruff over 4 files: exit 0`, `All checks passed!`.
8. Gate 3: `python3 .remedy-wt/f296-r2/prep/run_selection.py <repository root> .remedy-wt/f296-r2-worker/selection-output.txt` ran pytest once over 208 paths (the round's selection plus every `tests/test_*.py`). Printed `paths 208`, `exit 0`, `8751 passed, 2 skipped in 87.89s (0:01:27)`. The two skipped lines read: an install-smoke test that is opt-in and needs network access, and an agent-tooling test quarantined under an earlier decision with its own backlog note. A direct grep of the full saved output confirmed zero `FAILED`/`ERROR` lines and zero `process(es) behind` lines.
9. Gate 4: `python3 -m apps.cli.main integrity check --json` (from the primary checkout) returned six checks, all `pass` (handler import, live-review verdict, plan consistency, relevant-untracked, repo-root hygiene, open high-severity findings), with `"fail_count": 0`.
10. Gate 5: the open-finding-id lookup over `.agent/live_review.md` printed `6`, matching the count the block requires.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: all four files of C1 plus `.agent/authored/f296-r2.md` (additionally proved equal to the prompt's own `block.md` by line count and sha256), all five files of C2, and all three files of C3.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1, C2, C3, then this C4), each commit touching only its named paths. No amend, rebase, force-push or `--no-verify` was used. `.data` was never read by this worker. No mutation red-proof and no full-suite run were attempted; `REMEDY_TEST_MAX_WORKERS` was never set; each gate ran exactly once and never alongside another test command. A `python3 -I` smoke import of `pingpong_loop.py` failed on a missing `pydantic` under full isolation; this is an artifact of `-I` excluding site-packages, not a defect of this round's edits — a plain `python3` import of both new and touched modules succeeded, and gate 3's full run of the loop's tests passed.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 2's verdict in the next round's first commit.
4. T002a: the escalation in the call evidence, the run report's line and the `worker.escalated` event.

Operator questions open: 0. Open findings: 6.

## For the operator, in plain sentences

This session continued the work that teaches the system running a task's repair rounds to hand the next round to a stronger helper when a cheaper one keeps failing. It added the three settings that turn this on and describe which model serves which strength level, the piece of code that decides when a task should move up and carries out that move, and wired it into the two places inside the main repair loop where a round starts and where a repair decision is made. It then added the tests that check this decision and three real sample runs, and a page describing the new behavior for future readers. The whole relevant set of automated checks passed after this step, and no outstanding problem was left behind by it.

A pull request will be opened once more of this feature's work has landed; it is not opened yet.
