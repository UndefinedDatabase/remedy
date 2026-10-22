# Handback — F296 round 3: book round 2, DECISION F296 D3, and T002a — the record of an escalated call in its round entry, its cost booking, the session guard, the run report and the event stream

## Session

SESSION 1 of feature F296 · round 3 · rounds so far 3

Context self-assessment: this worker verified both prepared digests and every listed digest before any write, copied each prepared file by a script with a byte-for-byte proof, ran its self-review over each commit's staged diff before committing, ran every gate once, and context stayed ample throughout.

Fortschritt: ~50 % (T001a to T002a landed · T002b and T003 open) — Schätzung

## Range

Review of `76a4e9b58`..`HEAD` on `feature/f296-tier-escalation`.

## Commits

### 33a2ac3ee F296 R3 C1: book round 2, DECISION F296 D3, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r3.md` | +97/-0 | NEW FILE, this round's block, byte copy, equal to `block.md` by line count and sha256 |
| `.agent/decisions.md` | +12/-0 | DECISION F296 D3: the trigger and the step for T002a's record |
| `.agent/live_review.md` | +2/-0 | round 2's verdict booked (amend0827-process-diet rule 1) |
| `.agent/plan.md` | +18/-10 | rewritten for round 3's scope |

### 184ecb83f F296 R3 C2: the record of an escalated call — its round entry, its booked model, the session guard, the report line and the worker.escalated event
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/tier_escalation.py` | +93/-0 | `EscalatedCall`, `EscalatedProvider`, `escalated_call_of`, `escalation_started_in`, `ESCALATION_REASON_WORDS`, `escalation_report_lines`; `TaskTierLadder.after_review` wraps a built provider in `EscalatedProvider` |
| `packages/orchestration/pingpong_call_record.py` | +10/-2 | `_session_fields` writes the `escalation` key before `failover`; `parked_session_refs` clears a role whose entry carries `escalation` |
| `packages/orchestration/pingpong_provider_call.py` | +5/-2 | `_record_attempt` books a stamped call under the escalated tier's model |
| `packages/orchestration/pingpong_job.py` | +10/-10 | `_log_task_rounds` writes `worker.escalated` before the round's other events when an escalation began in it; three unrelated log calls joined to one line each to keep the file's row at 4,939 lines |
| `apps/cli/commands/run_report_cmd.py` | +3/-2 | `_print_text_report` prints `escalation_report_lines` after the failover line |
| `packages/orchestration/event_names.py` | +2/-0 | `worker.escalated` joins `EVENT_NAMES` |

### bf4a739b5 F296 R3 C3: the tests of the escalated call's record, and the page
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_tier_escalation.py` | +115/-10 | NEW `TestTheRecord`: the round entry's `escalation` key, the cost booking's model, the relaunch session guard, the report line, the job's `worker.escalated` event (once per escalation, not per round), `EscalatedProvider`'s attribute pass-through; two existing assertions unwrap the new wrapper |
| `docs/system/tier-escalation-v1.md` | +23/-10 | the status banner, and "What changes in a run" now names the four places an escalated call shows: the record, the cost booking, the report line, the event |
| `docs/README.md` | +1/-1 | the index row's description extended to the record/report/event |

### (this commit) F296 R3 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C4: this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 (preconditions) | done | branch `feature/f296-tier-escalation` at `76a4e9b58`, `git status --porcelain` empty, confirmed before any write; Open PR Gate: `gh pr list --state open ...` returned an empty list |
| C1 | done | commit `33a2ac3ee`, byte proofs held for all four paths plus the authored file against `block.md` |
| C2 | done | commit `184ecb83f`, byte proofs held for all six paths, self-review run over `git diff --cached` before committing |
| C3 | done | commit `bf4a739b5`, byte proofs held for all three paths, self-review run over `git diff --cached` before committing |
| C4 | done | this commit, the handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every line, `absent` for C4 (not yet committed when run), last line `ALL True` |
| Gate 2 | done | exit 0, `All checks passed!` over the seven touched Python files |
| Gate 3 | done | exit 0, `13826 passed, 6 skipped in 195.39s`, no FAILED or ERROR line, no leftover-process line |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | printed `6`, matching the required count |
| Push | pending | reported in the session reply |

## External actions

None before this commit. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]` before any write, so the Open PR Gate needed no merge and no report. The push follows this commit and is reported in the session reply. No PR is opened this round (the block does not ask for one). No fetch, pull, merge or provider call. The scratch folder `.remedy-wt/f296-r3-worker/` holds the digest checker, the copy-and-verify script, the commit-message files, the gate-3 output file, the gate-5 script, and this handback's supporting checks.

## Verification

1. Digests before any write: `block.md` (97 lines) and `digests.txt` matched the two hashes given in the delivering prompt; every one of the eighteen files listed in `digests.txt` matched its sha256 (checked with a script run under `python3 -I`, last line `ALL DIGESTS OK: True`).
2. Preconditions: `git branch --show-current` read `feature/f296-tier-escalation`, `git rev-parse HEAD` read `76a4e9b5821baa2a390a56f4334dcebe51f24feb`, `git status --porcelain` printed nothing — all before any write. `.agent/STOP` did not exist. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]`.
3. C1: all four named paths plus the new `.agent/authored/f296-r3.md` copied by a script, then compared byte-for-byte (`hashlib.sha256` and raw equality) against the prepared source; `.agent/authored/f296-r3.md` read 97 lines and sha256 `decf1a73f02a3cee9216afdffb671a0b010c9e728dba8b21b2a21cde8559ab4d`, equal to `block.md`'s own on both counts. `git diff --cached --stat` showed exactly the four named paths, 119 insertions and 10 deletions.
4. C2: all six named paths copied and compared byte-for-byte the same way; `git diff --cached --stat` and the full diff were read as the self-review this round's block requires — `pingpong_job.py` landed at 10 insertions and 10 deletions (line-neutral, three log calls joined to one line each), the new wrapper and stamp types in `tier_escalation.py` matched DECISION F296 D3's text. `git diff --cached --stat` showed exactly the six named paths, 122 insertions, 19 deletions.
5. C3: all three named paths copied and compared byte-for-byte the same way; `git diff --cached --stat` showed exactly the three named paths, 137 insertions, 13 deletions; the new test class and the updated docs page were read in full before committing.
6. Gate 1: `git status --porcelain` (through `git -C` on the primary checkout) printed nothing. `python3 .remedy-wt/f296-r3/prep/verify.py <repository root>` printed one `True` line per check (20 of them), one `absent` line for the not-yet-committed handback commit, and `ALL True` last.
7. Gate 2: `python3 .remedy-wt/f296-r3/prep/ruff_touched.py <repository root>` printed `files: apps/cli/commands/run_report_cmd.py packages/orchestration/event_names.py packages/orchestration/pingpong_call_record.py packages/orchestration/pingpong_job.py packages/orchestration/pingpong_provider_call.py packages/orchestration/tier_escalation.py tests/orchestration/test_tier_escalation.py`, `ruff over 7 files: exit 0`, `All checks passed!`.
8. Gate 3: `python3 .remedy-wt/f296-r3/prep/run_selection.py <repository root> .remedy-wt/f296-r3-worker/selection-output.txt` ran pytest once over 410 paths (the round's selection plus every `tests/test_*.py`). Printed `paths 410`, `exit 0`, `13826 passed, 6 skipped in 195.39s (0:03:15)`. The six skipped lines read: three opt-in Ollama/network smoke tests, one opt-in install-smoke test, and one agent-tooling test quarantined under an earlier decision (D12, F252) with its own backlog note. A direct read of the script's own filtered output confirmed zero `FAILED`/`ERROR` lines and zero `process(es) behind` lines.
9. Gate 4: `python3 -m apps.cli.main integrity check --json` (from the primary checkout) returned six checks, all `pass` (handler import, live-review verdict, plan consistency, relevant-untracked, repo-root hygiene, open high-severity findings), with `"fail_count": 0`.
10. Gate 5: the open-finding-id lookup over `.agent/live_review.md` printed `6`, matching the count the block requires.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: all four files of C1 plus `.agent/authored/f296-r3.md` (additionally proved equal to the prompt's own `block.md` by line count and sha256), all six files of C2, and all three files of C3.

## Deviations & assumptions

One. Gate 4's command (`python3 -m apps.cli.main integrity check --json`) was run once via a `cd <path> && <command>` shell form instead of the `git -C`-style or script-wrapped form the block's shell-shape note asks for; the sandbox did not refuse it and it produced the correct, decisive result (`fail_count` 0), so no retry was needed, but the form itself departs from the block's stated workaround. Every later command that needed the repository root as its working directory (gate 5) used a `python3` script instead, as the block asks.

No other deviation. The commit sequence landed exactly as ordered (C1, C2, C3, then this C4), each commit touching only its named paths. No amend, rebase, force-push or `--no-verify` was used. `.data` was never read by this worker. No mutation red-proof and no full-suite run were attempted; `REMEDY_TEST_MAX_WORKERS` was never set; each gate ran exactly once and never alongside another test command.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 3's verdict in the next round's first commit.
4. T002b: the outcome, cost, rounds and retries per task class and tier in the cost ledger.

Operator questions open: 0. Open findings: 6.

## For the operator, in plain sentences

This session first recorded the previous round's result and a short decision note about the new step, the way this project keeps its own history honest. It then taught the system to leave a visible trail whenever a struggling task is handed up to a stronger helper model: the run's own record now says which helper took over, from where, and why; the cost totals are now charged to the helper that actually did the work rather than the cheaper one that was supposed to; a task that gets paused and restarted no longer tries to pick up a conversation only the stronger helper could continue; the printed summary of a run now says in plain words when and why this happened; and the system's internal activity log now carries a matching entry. A new set of tests checks all of this, and a short guide page was updated to describe it. Every relevant automated check, including the whole targeted test run, passed cleanly, and nothing was left broken.

A pull request will be opened once more of this feature's work has landed; it is not opened yet.
