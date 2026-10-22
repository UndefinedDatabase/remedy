# Handback — F296 round 1: claim F296, book F307's round 32, write the slice list, take step (1) of `run_pingpong`'s boundary

## Session

SESSION 1 of feature F296 · round 1 · rounds so far 1

Context self-assessment: this worker verified both prepared digests and every listed digest before any write, copied each prepared file by a script with a byte-for-byte proof, ran every gate once, and context stayed ample throughout.

Fortschritt: ~10 % (T001a landed · T001b to T003 open) — Schätzung

## Range

Review of `eb7aa432b`..`HEAD` on `feature/f296-tier-escalation`.

## Commits

### 8e7799850 F296 R1 C1: claim F296, book F307 R32, re-head the ledger, DECISION F296 D1, the slice list
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r1.md` | +94/-0 | NEW FILE, this round's block, byte copy |
| `.agent/context.md` | +7/-6 | rewritten for F296's scope |
| `.agent/decisions.md` | +12/-0 | DECISION F296 D1 |
| `.agent/live_review.md` | +21/-19 | re-headed to F296, F307 round 32 booked |
| `.agent/plan.md` | +14/-13 | rewritten for F296's round 1 |
| `docs/roadmap/STATUS.md` | +1/-1 | F296's line `[ ]` to `[~]` |
| `docs/roadmap/features/T3_F296.md` | +19/-0 | the slice list |

### f3813280e F296 R1 C2: run_pingpong step (1) — the target snapshot check is one function its four places call
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +3/-2 | the function's and the file's rows fall by the step's measure |
| `packages/orchestration/pingpong_loop.py` | +24/-36 | `_record_target_mutation` extracted, called at all four places |
| `tests/test_structure_ratchet.py` | +2/-2 | the two pins lowered by the same counts |

### (this commit) F296 R1 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C3: this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch `feature/f296-tier-escalation` created from `main` at `eb7aa432b`, confirmed before any write |
| C1 | done | commit `8e7799850`, byte proofs held for all seven paths, numstat matches |
| C2 | done | commit `f3813280e`, byte proofs held for all three paths, self-review run before commit |
| C3 | done | this commit, the handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every line, `absent` for C3 (not yet committed when run), last line `ALL True` |
| Gate 2 | done | exit 0, `All checks passed!` over the two touched Python files |
| Gate 3 | done | exit 0, `7179 passed, 2 skipped in 81.14s`, no FAILED or ERROR line, no leftover-process line |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | printed `6`, matching the required count |
| Push | pending | reported in the session reply |

## External actions

None before this commit. The push follows it and is reported in the session reply. No PR is opened this round (the block does not ask for one). No fetch, pull, merge or provider call. The scratch folder `.remedy-wt/f296-r1-worker/` holds the digest checkers, the copy and proof scripts, the commit-message files and this handback's supporting checks.

## Verification

1. Digests before any write: `block.md` (94 lines) and `digests.txt` matched the two hashes given in the delivering prompt; every one of the fifteen files listed in `digests.txt` matched its sha256 (checked with a script run under `python3 -I`, last line `ALL_OK True`).
2. Preconditions: `git status --porcelain` empty, `git branch --show-current` read `main`, `git rev-parse HEAD` read `eb7aa432b15331cc8e777b34306bcb144fb5a8fe` before the branch was created. `gh pr list --state open ...` returned an empty list, so the Open PR Gate needed no merge.
3. C1: all seven prepared files copied by a script, then compared byte-for-byte (`hashlib.sha256` and raw equality) against the prepared source; `.agent/authored/f296-r1.md` read 94 lines and sha256 `df2795839931b04b34abea678d42ddf79974e23d55555ff3c756f8e3dc62a567`, equal to `block.md`'s own.
4. C2: all three prepared files copied and compared byte-for-byte the same way; `git diff --cached --stat` showed exactly the three named paths at 29 insertions and 40 deletions, read before committing as the self-review this round's block requires.
5. Gate 1: `git status --porcelain` (through `git -C` on the primary checkout) printed nothing. `python3 .remedy-wt/f296-r1/prep/verify.py <repository root>` printed one `True` line per check (17 of them), one `absent` line for the not-yet-committed handback commit, and `ALL True` last.
6. Gate 2: `python3 .remedy-wt/f296-r1/prep/ruff_touched.py <repository root>` printed `files: packages/orchestration/pingpong_loop.py tests/test_structure_ratchet.py`, `ruff over 2 files: exit 0`, `All checks passed!`.
7. Gate 3: `python3 .remedy-wt/f296-r1/prep/run_selection.py <repository root> .remedy-wt/f296-r1-worker/selection-output.txt` ran pytest once over 176 paths (the round's selection plus every `tests/test_*.py`). Printed `paths 176`, `exit 0`, `7179 passed, 2 skipped in 81.14s (0:01:21)`. The two skipped lines read: an install-smoke test that is opt-in and needs network access, and an agent-tooling test quarantined under an earlier decision with its own backlog note. No FAILED, ERROR or leftover-process line appeared.
8. Gate 4: `python3 -m apps.cli.main integrity check --json` (from the primary checkout) returned six checks, all `pass` (an import check, a review-verdict check, a plan-consistency check, an untracked-files check, a repository-hygiene check, and a check for open high-severity findings), with `"fail_count": 0`.
9. Gate 5: the open-finding-id lookup over `.agent/live_review.md` printed `6`, matching the count the block requires.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: all seven files of C1 and all three files of C2. `.agent/authored/f296-r1.md` additionally proved equal to the prompt's own `block.md` by line count and sha256.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C0, C1, C2, then this C3), each commit touching only its named paths. No amend, rebase, force-push or `--no-verify` was used. `.data` was never read by this worker. No mutation red-proof and no full-suite run were attempted; `REMEDY_TEST_MAX_WORKERS` was never set; each gate ran exactly once and never alongside another test command.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 1's verdict in the next round's first commit.
4. T001b and T001c: the escalation module, its configuration keys and the loop's call.

Operator questions open: 0. Open findings: 6.

## For the operator, in plain sentences

This session started a new piece of work: teaching the system that runs a task's repair rounds to hand the next round to a stronger helper when a cheaper one keeps failing, instead of staying on the cheaper one forever. This first step did not change what a person sees. It took one small, repeated piece of internal bookkeeping that was written out four separate times inside the part of the code that runs those rounds, and turned it into a single shared piece, so the upcoming change can be added without that code growing any longer than it already is. The whole relevant set of automated checks passed after this step, and no outstanding problem was left behind by it.

A pull request will be opened once more of this feature's work has landed; it is not opened yet.
