# Handback — F296 round 4: book round 3, DECISION F296 D4, and T002b — the outcome per task class and tier in the run record, the task's evidence and the cost ledger

## Session

SESSION 1 of feature F296 · round 4 · rounds so far 4

Context self-assessment: this worker verified both prepared digests and every listed digest before any write, copied each prepared file by a script with a byte-for-byte proof, ran its self-review over each commit's staged diff before committing, ran every gate once, and context stayed ample throughout.

Fortschritt: ~65 % (T001a to T002b landed · T003 and the closure open) — Schätzung

## Range

Review of `560bcc45a`..`HEAD` on `feature/f296-tier-escalation`.

## Commits

### 4ae04d7cb F296 R4 C1: book round 3, DECISION F296 D4, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r4.md` | +97/-0 | NEW FILE, this round's block, byte copy, equal to `block.md` by line count and sha256 |
| `.agent/decisions.md` | +12/-0 | DECISION F296 D4: the run record's `tier_ladder`, `tier_outcomes.json` and the ledger's `tier_outcomes` table |
| `.agent/live_review.md` | +2/-0 | round 3's verdict booked (amend0827-process-diet rule 1) |
| `.agent/plan.md` | +11/-10 | rewritten for round 4's scope |

### d428570ac F296 R4 C2: the outcome per task class and tier — the run's tier_ladder, tier_outcomes.json and the ledger's tier_outcomes table
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/tier_escalation.py` | +23/-4 | `TierEscalation.to_json`; `TaskTierLadder.__init__`/`for_run` accept and fill a run's `tier_ladder` record when both roles run on tier models; `after_review` appends each step's json to it |
| `packages/orchestration/pingpong_loop.py` | +9/-9 | `PingPongResult.tier_ladder` field; `run_pingpong` passes `result` to `TaskTierLadder.for_run`; `export_pingpong_json` adds the `tier_ladder` key only when filled; two unrelated lines reformatted to one each to keep `run_pingpong` and the file line-neutral (still 4,909 lines) |
| `packages/orchestration/tier_outcomes.py` | +216/-0 | NEW FILE: `TierOutcomeRow`/`TierOutcomeSummary`, `tier_outcome_rows`, `write_task_tier_outcomes` (writes `tier_outcomes.json` and mirrors it), `record_tier_outcomes`, `rows_from_evidence_file`, `query_tier_outcomes` (for F133), the `tier_outcomes` table and its `meta` schema key |
| `packages/orchestration/job_evidence.py` | +4/-4 | `_write_task_run_evidence` calls `write_task_tier_outcomes` after writing a task's other evidence; file stays at 2,992 lines |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.tier_outcomes` joins the allowlist |

### f1dff2060 F296 R4 C3: the tests of the outcome per task class and tier, and the page
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_tier_outcomes.py` | +180/-0 | NEW FILE: `TestTheRows`, `TestTheLedger`, `TestTheEvidence`, plus the two run-level tests that a run on tier models (switch on or off) records its tiers and a run off tier models records none |
| `docs/system/tier-escalation-v1.md` | +23/-4 | the status banner now names T002b as built; new section "What each tier did, per task class" |
| `docs/README.md` | +1/-1 | the index row's description extended to the evidence file and the cost ledger |

### (this commit) F296 R4 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C4: this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 (preconditions) | done | branch `feature/f296-tier-escalation` at `560bcc45a`, `git status --porcelain` empty, confirmed before any write; Open PR Gate: `gh pr list --state open ...` returned an empty list |
| C1 | done | commit `4ae04d7cb`, byte proofs held for all four paths plus the authored file against `block.md` |
| C2 | done | commit `d428570ac`, byte proofs held for all five paths, self-review run over `git diff --cached` before committing |
| C3 | done | commit `f1dff2060`, byte proofs held for all three paths, self-review run over `git diff --cached` before committing |
| C4 | done | this commit, the handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every line, `absent` for C4 (not yet committed when run), last line `ALL True` |
| Gate 2 | done | exit 0, `All checks passed!` over the five touched Python files |
| Gate 3 | done | exit 0, `11062 passed, 5 skipped in 142.98s`, no FAILED or ERROR line, no leftover-process line |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | printed `6`, matching the required count |
| Push | done | reported in the session reply |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]` before any write, so the Open PR Gate needed no merge and no report. `git push origin feature/f296-tier-escalation` ran once after this commit; its result is reported in the session reply. No PR is opened this round (the block does not ask for one). No fetch, pull, merge or provider call. The scratch folder `.remedy-wt/f296-r4-worker/` holds the digest checker, the copy-and-verify scripts, the commit-message files, and the gate-3 output file.

## Verification

1. Digests before any write: `block.md` (97 lines) and `digests.txt` matched the two hashes given in the delivering prompt; every one of the seventeen files listed in `digests.txt` matched its sha256 (checked with a script, last line `ALL_MATCH: True`).
2. Preconditions: `git branch --show-current` read `feature/f296-tier-escalation`, `git rev-parse HEAD` read `560bcc45a6afc2e2e5cdb275dd26064f5ed2ce27`, `git status --porcelain` printed nothing — all before any write. `.agent/STOP` did not exist. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]`.
3. C1: all four named paths plus the new `.agent/authored/f296-r4.md` copied by a script, then compared byte-for-byte (`hashlib.sha256` and raw equality) against the prepared source; `.agent/authored/f296-r4.md` read 97 lines and sha256 `b9adb077f8d17fce627667d9867935b3d28d5ad9ad6739742e3eddab7897b9c9`, equal to `block.md`'s own on both counts. `git diff --cached --stat` showed exactly the four named paths.
4. C2: all five named paths copied and compared byte-for-byte the same way; `git diff --cached --stat` and the full diff were read as the self-review this round's block requires — `pingpong_loop.py` landed at 9 insertions and 9 deletions (line-neutral, two lines reformatted to compensate for the new field and the two call-site edits; file stays at 4,909 lines) and `job_evidence.py` at 4 insertions and 4 deletions (file stays at 2,992 lines); the new module and the ladder's record-filling matched DECISION F296 D4's text.
5. C3: all three named paths copied and compared byte-for-byte the same way; the new test module (`TestTheRows`, `TestTheLedger`, `TestTheEvidence`, and the two run-level tests) and the updated docs page were read in full before committing.
6. Gate 1: `git status --porcelain` (through `git -C` on the primary checkout) printed nothing. `python3 .remedy-wt/f296-r4/prep/verify.py <repository root>` printed one `True` line per check (18 of them), one `absent` line for the not-yet-committed handback commit, and `ALL True` last.
7. Gate 2: `python3 .remedy-wt/f296-r4/prep/ruff_touched.py <repository root>` printed `files: packages/orchestration/job_evidence.py packages/orchestration/pingpong_loop.py packages/orchestration/tier_escalation.py packages/orchestration/tier_outcomes.py tests/orchestration/test_tier_outcomes.py`, `ruff over 5 files: exit 0`, `All checks passed!`.
8. Gate 3: `python3 .remedy-wt/f296-r4/prep/run_selection.py <repository root> .remedy-wt/f296-r4-worker/selection-output.txt` ran pytest once over 294 paths (the round's selection plus every `tests/test_*.py`). Printed `paths 294`, `exit 0`, `11062 passed, 5 skipped in 142.98s (0:02:22)`. The five skipped lines read: three opt-in Ollama/network smoke tests, one opt-in install-smoke test, and one agent-tooling test quarantined under an earlier decision (D12, F252) with its own backlog note. A direct read of the script's own filtered output confirmed zero `FAILED`/`ERROR` lines and zero `process(es) behind` lines.
9. Gate 4: `python3 -m apps.cli.main integrity check --json` (from the primary checkout) returned six checks, all `pass` (handler import, live-review verdict, plan consistency, relevant-untracked, repo-root hygiene, open high-severity findings), with `"fail_count": 0`.
10. Gate 5: the open-finding-id lookup over `.agent/live_review.md` printed `6`, matching the count the block requires.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: all four files of C1 plus `.agent/authored/f296-r4.md` (additionally proved equal to the prompt's own `block.md` by line count and sha256), all five files of C2, and all three files of C3.

## Deviations & assumptions

One. Gate 4's command (`python3 -m apps.cli.main integrity check --json`) was first tried as `python3 -I -m apps.cli.main integrity check --json`, following this prompt's general note that Python reading untrusted downloaded content should run with `-I`; that note does not apply here (the command runs the trusted, already-checked-out repository's own CLI, not downloaded data), and `-I` broke module resolution for `apps.cli.main` (`ModuleNotFoundError: No module named 'apps'`) by dropping the repository root from `sys.path`. The command was re-run once, without `-I`, from the primary checkout's working directory, and produced the correct, decisive result (`fail_count` 0). No other deviation. The commit sequence landed exactly as ordered (C1, C2, C3, then this C4), each commit touching only its named paths. No amend, rebase, force-push or `--no-verify` was used. `.data` was never read by this worker. No mutation red-proof and no full-suite run were attempted; `REMEDY_TEST_MAX_WORKERS` was never set; each gate ran exactly once and never alongside another test command.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 4's verdict in the next round's first commit.
4. T003: the benchmark and the default.

Operator questions open: 0. Open findings: 6.

## For the operator, in plain sentences

This session first recorded the previous round's result and a short decision note about the new step, the way this project keeps its own history honest. It then taught the system to keep a record of what each tier of helper model did for every task it worked on: which tier it ran on, how many rounds it took, how often a call needed a retry, what it cost, and how that stretch ended, whether by being handed up to a stronger helper or by the task finishing on that tier. That record is written next to the rest of a task's evidence and copied into the project's running cost ledger, so a later feature can look across many finished jobs and see which kind of task a cheaper helper handles well and which kind it tends to hand up. A new set of tests checks all of this against both built-up examples and a real run, and the guide page for this feature was updated to describe it. Every relevant automated check, including the whole targeted test run, passed cleanly, and nothing was left broken.

A pull request will be opened once more of this feature's work has landed; it is not opened yet.
