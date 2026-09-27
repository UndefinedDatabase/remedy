# Handoff — F035, round 2 (T001's second half: hunk decisions, decision answers,
clarification answers and plan approval join the ownership ledger, and the ledger is written at
the end of every `run_job`)

## Session

SESSION 1 of feature F035 · round 2 · rounds so far 2. Context remaining at handback:
comfortable — the round read AGENTS.md, the block, the two payloads and the handback template
once, read every source module the block named whole or by search, wrote the four new readers
and the run-end write with their tests, ran the full gate selection twice and the mutation tool
twice, and still has a large majority of its context budget left.

## Range

Review of `d4495f2a2`..`HEAD` (`HEAD` is this handback's own commit, `F035 R2 C5`, on
`feature/f035-ownership-ledger`).

## Commits

### 47e14e6ae F035 R2 C1: copy round 2 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r2-block.md | 288/0 | verbatim copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f035-r2-booking.diff | 59/0 | verbatim copy of the booking.diff payload |
| .agent/authored/f035-r2-plan.md | 30/0 | verbatim copy of the plan.md payload |

Measured insertions: 377 (288+59+30). Block expected the block's own line count (288) plus 89 =
377. Match, under the 500-line cap.

### a21d919d3 F035 R2 C2: book round 1, record D2, log one prose slip, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 32/0 | DECISION F035 D2 appended by `git apply booking.diff` |
| .agent/live_review.md | 2/0 | round 1's Gate entry appended by `git apply booking.diff` |
| .agent/plan.md | 9/9 | rewritten to the plan.md payload |
| .agent/prose_slips.md | 1/0 | one prose-slip line appended by `git apply booking.diff` |

Measured numstat: 32/0, 2/0, 9/9, 1/0 — equal to the block's G2 expectation exactly.

### 0b08a08c5 F035 R2 C3: read hunks, answers, clarifications and approvals, and write the ledger at run end
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ownership.py | 180/5 | S1-S4: `_hunk_decision_entries`, `_decision_answer_entries`, `_clarification_entries`, `_plan_approval_actor_text`, `_plan_approval_body_entries`; `_run_log_entries` gains the `plan_approved` branch and its dedupe key moves to `(name, ref)` |
| packages/orchestration/pingpong_job.py | 46/0 | `_write_ownership_ledger_at_run_end` and `_writes_ownership_ledger`, the decorator applied to `run_job` |
| tests/orchestration/import_reachability_allowlist.txt | 1/0 | `packages.orchestration.ownership` added in its sorted place |
| tests/test_no_orphan_modules.py | 0/3 | `ownership.py`'s `ALLOWED_UNWIRED` entry removed |

Measured insertions: 227 (180+46+1+0). The block states no expectation for C3; this is what was
measured. Both guards (`test_no_orphan_modules.py`, `test_import_reachability.py`) were run
standalone before this commit and named no other module.

### 5864aa1f3 F035 R2 C4: test the remaining ownership classes and the run-end write, add the mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r2-mutations.py | 132/0 | the G5 red-proof tool, authored this round |
| tests/orchestration/test_ownership_ledger.py | 239/1 | `TestHunkDecisions`, `TestDecisionAnswers`, `TestClarifications`, `TestPlanApproval`, plus the shared hunk-diff fixture and the run-log timestamp rewriter |
| tests/orchestration/test_pingpong_job_ownership.py | 96/0 | new file: the real-`run_job` write-path tests |

Measured insertions: 467 (132+239+96). The block states no expectation for C4; this is what was
measured, under the 500-line cap.

### c7818a235 F035 R2 C4b: strengthen the pending-hunk test against a relabeled leak (DEVIATION — see below)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_ownership_ledger.py | 3/3 | `test_approved_entry_and_no_entry_for_the_pending_row` now asserts the ledger's WHOLE entry list rather than an action-filtered view |

Not one of the block's named commits (C1-C5); constraint 4 permits correcting a test this round
itself wrote before C5, declared here and in Deviations below.

### This commit F035 R2 C5: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback, per `docs/agents/handback_template.md` |

## External actions

- `git apply --check .remedy-wt/f035-r2-payloads/booking.diff` — exit 0.
- `git apply .remedy-wt/f035-r2-payloads/booking.diff` — exit 0.
- `git worktree add --detach .remedy-wt/f035-r2-mut HEAD` at C4 (`5864aa1f3`) — succeeded; ran
  the mutation tool (found m1 green, see Deviations); `git worktree remove --force
  .remedy-wt/f035-r2-mut` and `git worktree prune` — both succeeded.
- `git worktree add --detach .remedy-wt/f035-r2-mut HEAD` again at C4b (`c7818a235`) after the
  fix — succeeded; ran the mutation tool (all 12 caught); `git worktree remove --force
  .remedy-wt/f035-r2-mut` and `git worktree prune` — both succeeded.
- `git push` — reported in the reply per the block (G6 cannot go in this file, written before
  the push).
- No PR created or merged — the block orders none, and none was created.

## Verification

G1 TRANSPORT — payloads measured against the PAYLOADS table before use:
```
booking.diff: 59 lines, 12611 bytes, sha256 d02e9e26723e95da0f9d99d54663f28ff59df825019b18cb24b0937bff06ea31 — MATCH
plan.md:      30 lines, 1005 bytes,  sha256 52093632b817b7241f483738cae2a41b5c5d49c5042f3dde884d967c882de79b — MATCH
```
Copies at C1, read back with `git show <C1>:<path>` and compared byte-for-byte (`cmp`) against
the source: `.agent/authored/f035-r2-block.md` vs `.remedy-wt/f035-r2/block.md` — IDENTICAL;
`.agent/authored/f035-r2-plan.md` vs the plan.md payload — IDENTICAL;
`.agent/authored/f035-r2-booking.diff` vs the booking.diff payload — IDENTICAL.

G2 THE BOOKING — at C2 (`a21d919d3`), `git show <C2>:<path> | wc -c` and `sha256sum`:
```
.agent/decisions.md   2328299 bytes  bf8e0fd805735352f9e4f2028463bcf8e0e240923e86a22b8364950ea360f01b — MATCH
.agent/live_review.md  302813 bytes  79edb1951b5601457ec4ae75ca6131861ee14e50f05ab6b709dae84baa33ece9 — MATCH
.agent/plan.md            1005 bytes 52093632b817b7241f483738cae2a41b5c5d49c5042f3dde884d967c882de79b — MATCH
.agent/prose_slips.md   374918 bytes 8f22b48d6f0b64a674144895411083c298abf07c55e81dbe21260c773a8321b2 — MATCH
```
`scripts.rotate_live_review.open_finding_ids` over the C2 ledger text: `[]` (empty, as the
reviewer read). The ledger's last non-blank line at C2 begins `Gate: F035 R1 — ` (confirmed by
direct read).

G3 THE CODE — at C4:
```
$ python3 -m ruff check packages/orchestration/ownership.py packages/orchestration/pingpong_job.py \
    tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py \
    tests/test_no_orphan_modules.py
All checks passed!
REAL_EXIT=0
```
`_write_ownership_ledger_at_run_end`, `_writes_ownership_ledger`, the decorator line and the
`def run_job(` line under it, quoted from `git show 0b08a08c5:packages/orchestration/pingpong_job.py`:
```python
def _write_ownership_ledger_at_run_end(job: Any) -> None:
    """Save `ownership.json` into `job`'s evidence export, DECISION F035 D2. Returns at once
    for anything that is not a `JobPlan` with a real `job_dir` on disk — a `job_not_found`
    placeholder from `run_job` below never had one. An `OwnershipError` building the ledger or
    an `OSError` writing it is logged and swallowed: a ledger write must never fail the run it
    describes, and the job `run_job` already returned is the one that matters."""
    import logging

    from packages.common.secure_fs import durable_write_json
    from packages.orchestration.data_paths import job_dir, job_evidence_export_dir
    from packages.orchestration.ownership import (
        OWNERSHIP_FILENAME,
        OwnershipError,
        build_ownership_ledger,
    )

    if not isinstance(job, JobPlan):
        return
    if not job_dir(job.job_id).is_dir():
        return
    try:
        ledger = build_ownership_ledger(job)
        export_dir = job_evidence_export_dir(job.job_id)
        export_dir.mkdir(parents=True, exist_ok=True)
        durable_write_json(export_dir / OWNERSHIP_FILENAME, ledger)
    except (OwnershipError, OSError) as exc:
        logging.getLogger(__name__).warning(
            "ownership ledger write failed for job %s: %s", job.job_id, exc)


def _writes_ownership_ledger(fn):
    """Wrap `run_job` so every invocation ends by saving the ownership ledger, DECISION F035
    D2. `fn`'s own return value is unchanged — the save is a side effect after it runs, never a
    second source of truth for the job `run_job` returns."""

    @functools.wraps(fn)
    def _wrapped(*args, **kwargs):
        job = fn(*args, **kwargs)
        _write_ownership_ledger_at_run_end(job)
        return job

    return _wrapped


@_writes_ownership_ledger
def run_job(
```
Reader (g)'s new dedupe key, quoted from the same commit's `ownership.py`:
```python
        ref = request_id if request_id else raw_ts
        key = (name, ref)
```

G4 THE TESTS — SERIALLY, at C4b (`c7818a235`), the block's full selection:
```
$ python3 -m pytest -q -p no:cacheprovider -rs <the block's 34-path selection>
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1326 passed, 1 skipped in 105.27s
REAL_EXIT=0
```
Accounting for 1326: the reviewer's own baseline at `d4495f2a` (this selection LESS
`test_pingpong_job_ownership.py` and LESS `test_command_channel.py`) read 1203 passed, 1
skipped. `--collect-only -q` node counts, measured fresh: `test_ownership_ledger.py` 42 (was 33
at round 1, +9 this round's S1-S4 classes); `test_pingpong_job_ownership.py` 4 (new file);
`test_command_channel.py` 110 (excluded from the reviewer's baseline, included here). 1203 - 33 +
42 + 4 + 110 = 1326. Match, real exit 0.

Then:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks read `pass`.

G5 THE RED PROOFS — run TWICE. FIRST run, over C4 (`5864aa1f3`), `git worktree add --detach
.remedy-wt/f035-r2-mut 5864aa1f3`, then `python3 -B .agent/authored/f035-r2-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f035-r2-mut`:
```
control (before): exit=0 failed=0 ids=[]
m1: a pending hunk row yields an entry: exit=0 failed=0 ids=[]              <- GREEN, not caught
m2..m12: all exit=1 failed=1 (m10 failed=3), each naming a failing node
control (after): exit=0 failed=0 ids=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False
```
m1 relabels a pending row's `action` instead of dropping it; the round's own test filtered the
ledger by `action in ("hunk_approved", "hunk_rejected")` before checking there was exactly one
entry, so a relabeled leak was invisible to it. Per constraint 4, fixed in C4b (see Commits and
Deviations) and the tool re-run. `git worktree remove --force .remedy-wt/f035-r2-mut` and `git
worktree prune` — both succeeded; `git worktree list | wc -l` read 61 (equal to step 4's
reading) and `git branch --list 'remedy/*' | wc -l` read 197 (unchanged).

SECOND run, over C4b (`c7818a235`), same worktree recipe:
```
control (before): exit=0 failed=0 ids=[]
m1: exit=1 failed=1 ids=['...TestHunkDecisions::test_approved_entry_and_no_entry_for_the_pending_row']
m2: exit=1 failed=1 ids=['...TestHunkDecisions::test_rejected_entry_reason_verbatim_its_landing_and_no_door']
m3: exit=1 failed=1 ids=['...TestDecisionAnswers::test_human_and_default_answers_and_no_entry_for_an_open_one']
m4: exit=1 failed=1 ids=['...TestDecisionAnswers::test_human_and_default_answers_and_no_entry_for_an_open_one']
m5: exit=1 failed=1 ids=['...TestClarifications::test_human_default_and_planner_and_none_for_unresolved']
m6: exit=1 failed=1 ids=['...TestClarifications::test_human_default_and_planner_and_none_for_unresolved']
m7: exit=1 failed=1 ids=['...TestPlanApproval::test_auto_yes_mode_event_is_auto_approved_with_the_audits_reason_as_text']
m8: exit=1 failed=1 ids=['...TestPlanApproval::test_two_events_with_no_request_id_yield_two_entries']
m9: exit=1 failed=1 ids=['...TestPlanApproval::test_a_rejected_plans_entry']
m10: exit=1 failed=3 ids=['...test_completed_job_writes_ownership_json_matching_the_returned_job', '...test_an_ownershiperror_in_the_write_leaves_the_run_untouched_writes_no_file_and_logs_one_warning', '...test_run_job_is_wrapped']
m11: exit=1 failed=1 ids=['...test_an_ownershiperror_in_the_write_leaves_the_run_untouched_writes_no_file_and_logs_one_warning']
m12: exit=1 failed=1 ids=['...test_an_unknown_job_id_writes_no_file']
control (after): exit=0 failed=0 ids=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
`git worktree remove --force .remedy-wt/f035-r2-mut` and `git worktree prune` — both succeeded;
`git worktree list | wc -l` read 61 (equal to step 4's reading, unchanged) and `git branch
--list 'remedy/*' | wc -l` read 197 (unchanged).

## Authored-text proofs

`.agent/authored/f035-r2-block.md`, `.agent/authored/f035-r2-plan.md` and
`.agent/authored/f035-r2-booking.diff`, each `cmp`'d byte-for-byte at C1 against its payload
source — all IDENTICAL (see G1 above). `booking.diff`'s own effect on `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` and `.agent/prose_slips.md`, read at C2 by size and
sha256 — all equal to the reviewer's simulation tree (see G2 above).

## Deviations & assumptions

1. G5's FIRST run (over C4, `5864aa1f3`) found mutation m1 GREEN: a pending hunk row relabeled
   under a different `action` string, rather than dropped, was invisible to
   `test_approved_entry_and_no_entry_for_the_pending_row`, which filtered the ledger by
   `action in ("hunk_approved", "hunk_rejected")` before asserting there was exactly one entry.
   Per constraint 4 ("a test this round itself wrote that is wrong may be corrected before C5,
   and the correction is declared"), the assertion was strengthened to unpack the ledger's WHOLE
   entry list for that job, and the fix landed as an extra commit, C4b (`c7818a235`), not named
   among the block's C1-C5. G5 was re-run over C4b and read `ALL MUTATIONS CAUGHT AND RESTORED
   CLEANLY: True`. Nothing on disk at the branch tip is wrong; the production code
   (`ownership.py`, `pingpong_job.py`) was never touched by this fix.
2. No other deviations. Every commit stayed under the 500-line insertion cap, so constraint 2's
   split naming (C3a/C3b, C4a/C4b) was not needed for size — C4b's name reuses that convention
   only because it is a second commit against the same file as C4, not because C4 was oversize.

## Next

Per AGENTS.md Phase 1 rule 1 (read `.agent/STOP` from disk) and the block's ordering: the review
of round 2, then T002 — the phrase catalog, the report's Ownership section with its goldens, and
the digest's `ownership` sentences. Open findings: 0. Operator questions: 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| Step 1 (`.agent/STOP` check) | done | |
| Step 2 (primary checkout, branch, HEAD) | done | |
| Step 3 (block byte verification) | done | |
| Step 4 (worktree count) | done | |
| Payload verification (2 payloads) | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C4b | deviated | correction to this round's own test after G5 caught mutation m1 green; see Deviations 1 |
| C5 (this handback) | done | |
| G1 Transport | done | |
| G2 The booking | done | |
| G3 The code | done | |
| G4 The tests | done | |
| G5 The red proofs | done | first run found m1 green; fixed in C4b; second run read ALL CAUGHT True |
| G6 Tree and push | done | reported in the reply, not this file (block: "cannot go in C5") |
