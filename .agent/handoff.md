# Handoff — F028, round 3

## Session

SESSION 1 of feature F028 · round 3 · rounds so far 3. Context remaining at
handback: comfortable — this round wrote roughly 600 lines of production
code across two modules plus roughly 750 lines of tests from a
specification with no repair loop needed (every gate matched on the first
try, all 11 red-proof mutations caught on the first run), leaving ample
context had a further round been required this session.

## Range

Review of `bdb659161`..`HEAD` (`HEAD` is this handback's own commit, `F028
R3 C7`, on `feature/f028-task-injection`).

## Commits

### 1ce006817 F028 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r3-block.md | 259/0 | copy of this round's block |
| .agent/authored/f028-r3-plan.md | 31/0 | copy of the plan payload |
| .agent/authored/f028-r3-records.diff | 67/0 | copy of the records diff payload |

Measured insertions: 357 (block's own line count 259 + 98), matching the
block's expectation exactly, under the 500-line cap.

### ebb4b485a F028 R3 C2: book round 2, resolve R-1076, register R-1077, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 45/0 | DECISION F028 D3 appended |
| .agent/live_review.md | 6/0 | round 2's Gate entry, R-1076's `Done:` paragraph and R-1077's registration appended |
| .agent/plan.md | 9/9 | rewrite from the plan payload |

Matches the block's expected numstat (45/0, 6/0, 9/9) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### 4f4460b23 F028 R3 C3: repair R-1077, answer a shortfall three ways, and carry a budget extension into the fold
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/task_injection.py | 334/39 | S1: `_validate_confirmed_record` (R-1077) wired into `confirmed_injections`; S2: `shortfall_decision_seed`'s question/labels rewritten as a sentence mapping; S3: `INJECTION_ANSWERS_DIRNAME`, `_read_injection_answer`, `_publish_injection_answer`, `answer_injection_shortfall`; S4: `apply_injection_to_job` reordered to compute-then-mutate and gains the budget extension; `draft_task_injection` and `confirm_task_injection` both carry `budget_extend_to_usd` |

334 insertions, under the 500-line cap — no split needed. The block sized
neither C3 nor C4 individually (only C1 and C2), so no expected-insertion
comparison applies here per "WHAT TO REPORT."

### 31047564a F028 R3 C4: re-read the job's budgets after every injection fold
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | 29/4 | S5: `_fold_injections_here` defined after `_job_budgets`'s first binding and before point (a); all four fold points call it instead of `_fold_task_injections` directly, point (d) keeping its length reading around the call |

29 insertions, under the 500-line cap.

### f564160fa F028 R3 C5: test the shortfall answers, the extension and R-1077
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_injection.py | 374/4 | the round-1 `option_labels` index rewrite (the one edit to an existing test); two new S2 label tests; `TestConfirmedRecordFieldValidation` (R-1077, 17 cases); `TestApplyInjectionToJobBudgetExtension` (S4, 4 cases); a parametrized job-untouched-on-error test (7 cases); `TestAnswerInjectionShortfall` (S3, 11 cases); `_confirmed_record`'s new optional `budget_extend_to_usd` kwarg |
| tests/orchestration/test_task_injection_runner.py | 100/1 | `TestConfirmedInjectionMissingAFieldBlocksTheJob` (R-1077 through the full runner); `TestBudgetExtensionReachesThePredictiveCheck` (S5, the extension reaching `predict_next_task_cost` and the job's own record) |

474 insertions total (374 + 100), under the 500-line cap — no split needed.

### d862e2a44 F028 R3 C6: add the round 3 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r3-mutations.py | 248/0 | the G5 mutation (red-proof) tool, 11 mutations (m1–m11) across the two touched production files |

### F028 R3 C7: rewrite handoff for round 3 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 2.
- `git worktree add --detach .remedy-wt/f028-r3-mut d862e2a44` (at C6, G5's
  own ordered worktree) — succeeded; `git worktree remove --force
  .remedy-wt/f028-r3-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 63 before the add and 63
  after the remove (step 4's own reading, unchanged).
- `git push` after C7 — reported under G6 in this round's reply (run after
  this file is committed).
- No `gh pr create` (the block does not order one this round), no `gh pr
  merge`, no checkout of `main`, no branch deletion, no force-push, no `git
  stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `plan.md`: 31 lines, 1168 bytes, sha256
  `4d3ce761c647b0ac8989aacc2de00aa082b6d203c18c47b7bc6046dd414b012e`.
- `records.diff`: 67 lines, 12751 bytes, sha256
  `8c900898eb62dacdfcc3fb1915f91324bfd62f6a677f8fb205fc16cb031ae5d2`.
- Block: 259 lines, sha256
  `2d4ee9a4da1ee8a0d3afde7996fe4633bd2c6f9823db206fddbcf66af64467b3` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f028-r3-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`1ce006817`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r3-block.md byte-identical: True sha256 src=2d4ee9a4da1ee8a0d3afde7996fe4633bd2c6f9823db206fddbcf66af64467b3 sha256 committed=2d4ee9a4da1ee8a0d3afde7996fe4633bd2c6f9823db206fddbcf66af64467b3
.agent/authored/f028-r3-records.diff byte-identical: True sha256 src=8c900898eb62dacdfcc3fb1915f91324bfd62f6a677f8fb205fc16cb031ae5d2 sha256 committed=8c900898eb62dacdfcc3fb1915f91324bfd62f6a677f8fb205fc16cb031ae5d2
.agent/authored/f028-r3-plan.md byte-identical: True sha256 src=4d3ce761c647b0ac8989aacc2de00aa082b6d203c18c47b7bc6046dd414b012e sha256 committed=4d3ce761c647b0ac8989aacc2de00aa082b6d203c18c47b7bc6046dd414b012e
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`ebb4b485a`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md bytes=317562 sha256=9551f5ecff40f5ce794ae75d932cb95ef610c0e032e28a723b297c0b31ced52d
.agent/decisions.md   bytes=2259543 sha256=37251d025f48e5b6410d1005621b43c5a9478d167ce745563ee31d481b0ca045
.agent/plan.md        bytes=1168   sha256=4d3ce761c647b0ac8989aacc2de00aa082b6d203c18c47b7bc6046dd414b012e
```
All three MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text: at `bdb659161`
reads `['R-1076']`; at C2 (`ebb4b485a`) reads `['R-1077']` — MATCH against
the reviewer's stated readings. `git diff --name-only 1ce006817 ebb4b485a`
names exactly: `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md` — the table's three paths, no more, no fewer.

### G3 — THE CODE
```
$ bash -c 'python3 -m ruff check packages/orchestration/task_injection.py packages/orchestration/pingpong_job.py tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```

The whole of `answer_injection_shortfall`, quoted from the diff (C6 state,
`packages/orchestration/task_injection.py`):
```python
def answer_injection_shortfall(
    job: Any,
    draft_id: Any,
    option: Any,
    *,
    actor: Any,
    budgets: Any,
    counters: Any,
    config: Any,
    now: datetime | None = None,
    control_root_path: Path | None = None,
) -> dict[str, Any]:
    """Answer a shortfall draft's decision seed with one of ``SHORTFALL_OPTIONS``. NEVER
    raises for a refusal.

    Checks, in order: S4's terminal check (``job_terminal``); ``read_injection_draft``
    refusing with its own code; a record naming another job (``draft_unknown``); a
    ``status`` other than ``needs_decision`` (``draft_not_in_shortfall``); *option* outside
    ``SHORTFALL_OPTIONS`` (``unknown_option``); an answer already on file for this draft
    (``already_answered``); ``shrink_task`` when the stored seed's ``shrink_band`` is None
    (``cannot_shrink``). A refusal writes nothing.

    Otherwise mints a derived draft id (None for ``drop``) and publishes ONE create-only
    answer file in ``INJECTION_ANSWERS_DIRNAME``, named as a draft file is — a lost race there
    answers ``already_answered`` too. Then: ``drop`` answers ``{"outcome": "dropped",
    "job_id", "draft_id", "answered_at"}`` and nothing more is written. ``shrink_task``
    derives a new draft whose task is the old one at the seed's ``shrink_band``, checked again
    over *budgets*/*counters*/*config*, itself a fresh shortfall (``needs_decision``, a fresh
    seed) when that check still breaches. ``extend_budget`` derives a new draft at the old
    band, ``confirmable``, carrying ``budget_extend_to_usd`` equal to the seed's
    ``extend_to_usd``, its check computed over ``budgets`` with ``max_cost_usd`` raised to
    that figure. Either derived draft keeps the old record's task id, placement,
    ``task_rationale``, ``text``, ``after`` and ``fence_conflicts``, takes the new draft id,
    the answering actor, ``drafted_at`` *now* and a fresh ``expires_at``, and adds
    ``derived_from`` (the old draft id) and ``answer`` (*option*); it is published through
    ``_publish_injection_draft`` (round 1's draft helper) and answered in the shape
    ``draft_task_injection`` answers, plus those two keys and ``budget_extend_to_usd``.
    """
    refusal = injection_refusal(getattr(job, "state", ""), 0)
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    try:
        record = read_injection_draft(
            job.job_id, draft_id, now=now, control_root_path=control_root_path)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    if record.get("job_id") != job.job_id:
        return {"outcome": "refused", "code": "draft_unknown",
                "detail": f"no injection draft {draft_id!r} exists"}

    if record.get("status") != "needs_decision":
        return {"outcome": "refused", "code": "draft_not_in_shortfall",
                "detail": "this injection draft is not awaiting a shortfall decision"}

    if option not in SHORTFALL_OPTIONS:
        return {"outcome": "refused", "code": "unknown_option",
                "detail": f"{option!r} is not a valid shortfall option"}

    if _read_injection_answer(
            job.job_id, draft_id, control_root_path=control_root_path) is not None:
        return {"outcome": "refused", "code": "already_answered",
                "detail": f"injection draft {draft_id!r} was already answered"}

    seed = record.get("decision_seed") or {}
    if option == "shrink_task" and seed.get("shrink_band") is None:
        return {"outcome": "refused", "code": "cannot_shrink",
                "detail": "this task is already at the smallest size; it cannot shrink"}

    now_dt = now if now is not None else datetime.now(timezone.utc)
    bounded_actor = _bounded_actor(actor)
    derived_draft_id = None if option == "drop" else _sp.new_request_id()

    answer_record = {
        "injection_answer_v": 1,
        "job_id": job.job_id,
        "draft_id": draft_id,
        "option": option,
        "actor": bounded_actor,
        "answered_at": now_dt.isoformat(),
        "derived_draft_id": derived_draft_id,
    }
    published = _publish_injection_answer(
        job.job_id, draft_id, answer_record, control_root_path=control_root_path)
    if not published:
        return {"outcome": "refused", "code": "already_answered",
                "detail": f"injection draft {draft_id!r} was already answered"}

    if option == "drop":
        return {"outcome": "dropped", "job_id": job.job_id, "draft_id": draft_id,
                "answered_at": answer_record["answered_at"]}

    task = dict(record["task"])
    placement = record["placement"]
    expires_dt = now_dt + timedelta(seconds=INJECTION_DRAFT_TTL_SECONDS)

    if option == "shrink_task":
        shrink_band = seed["shrink_band"]
        task["est_tokens_band"] = shrink_band
        check = injection_budget_check(budgets, counters, band=shrink_band, config=config)
        shortfall = bool(check["shortfall"])
        budget_extend_to_usd = None
    else:                                                          # extend_budget
        extend_to_usd = seed["extend_to_usd"]
        extended_budgets = budgets.model_copy(update={"max_cost_usd": extend_to_usd})
        check = injection_budget_check(
            extended_budgets, counters, band=task["est_tokens_band"], config=config)
        shortfall = False
        budget_extend_to_usd = extend_to_usd

    derived_answer: dict[str, Any] = {
        "outcome": "shortfall" if shortfall else "drafted",
        "job_id": job.job_id,
        "draft_id": derived_draft_id,
        "confirm_token": None if shortfall else derived_draft_id,
        "task": task,
        "placement": placement,
        "task_rationale": record["task_rationale"],
        "budget_check": check,
        "decision_seed": shortfall_decision_seed(check) if shortfall else None,
        "fence_conflicts": record.get("fence_conflicts", []),
        "drafted_at": now_dt.isoformat(),
        "expires_at": expires_dt.isoformat(),
        "planner_calls": 0,
        "text": record["text"],
        "derived_from": draft_id,
        "answer": option,
        "budget_extend_to_usd": budget_extend_to_usd,
    }

    derived_record = dict(derived_answer)
    derived_record["injection_draft_v"] = 1
    derived_record["status"] = "needs_decision" if shortfall else "confirmable"
    derived_record["actor"] = bounded_actor
    derived_record["after"] = record.get("after")

    _publish_injection_draft(
        job.job_id, derived_draft_id, derived_record, control_root_path=control_root_path)

    return derived_answer
```

`_fold_injections_here`, quoted whole (`packages/orchestration/pingpong_job.py`):
```python
        def _fold_injections_here() -> bool:
            """DECISION F028 D3 (2): fold every confirmed injection, then — when the fold just
            raised the job's own cost limit (DECISION F028 D3 (2) in `apply_injection_to_job`)
            — re-validate `_job_budgets` from the fresh `job.budgets` so the very next safe
            point's reactive and predictive checks enforce the limit the operator just raised,
            not the one this run started with. A budget the fold left corrupt blocks the job
            exactly as the pre-run validation above does.
            """
            nonlocal _job_budgets
            _budgets_before = dict(job.budgets) if job.budgets is not None else None
            if _fold_task_injections(job, _control):
                return True
            if job.budgets != _budgets_before:
                from pydantic import ValidationError as _BudgetValidationError

                from packages.core.models import JobBudgets as _JobBudgets
                try:
                    _job_budgets = _JobBudgets.model_validate(job.budgets)
                except _BudgetValidationError as exc:
                    job.state = JOB_BLOCKED
                    job.error = f"corrupt_budget_state: {exc}"
                    _persist_job(job)
                    return True
            return False
```

Its four call sites, three lines of context each:
```python
        # (a) — before the task loop

        # F028 D2 (3): the injection fold runs at the same point, right after the veto
        # fold — a confirmed injection waiting before this episode started joins task 1.
        if _fold_injections_here():
            return job

        tasks_run = 0
```
```python
            # (b) — every pre-task safe point

            # F028 D2 (3): the injection fold runs again here too, right after the veto
            # fold — a confirmation recorded between two tasks joins the very next one.
            if _fold_injections_here():
                return job

            if task.status == TASK_VETOED:
```
```python
            # (c) — the last statement of the loop body
            # F028 D2 (3): the injection fold's third point — the last statement of the
            # loop body — so a task confirmed while an earlier one ran is folded before the
            # NEXT iteration checks it (never later than one task late).
            if _fold_injections_here():
                return job
```
```python
        # (d) — once after the loop, keeping the length reading around the call
        # task nothing in this run will dispatch, so the job parks PAUSED instead of racing
        # ahead to completion with new work pending.
        _tasks_before_injection_terminal_fold = len(job.tasks)
        if _fold_injections_here():
            return job
        if len(job.tasks) > _tasks_before_injection_terminal_fold:
            job.state = JOB_PAUSED
```

The extension lines of `apply_injection_to_job`, quoted from the diff
(`packages/orchestration/task_injection.py`):
```python
    if "budget_extend_to_usd" in record:
        injection_block["budget_extend_to_usd"] = record["budget_extend_to_usd"]

    log_entry: dict[str, Any] = {
        "version": version + 1,
        "ts": now_dt.isoformat(),
        "actor": actor,
        "command": "plan_add_task",
        "args": {"task": task_dict},
        "before": [t.model_dump() for t in plan.tasks],
        "after": [t.model_dump() for t in new_plan.tasks],
        "injection": injection_block,
    }
    new_body[plan_editing.EDIT_LOG_KEY] = [*body.get(plan_editing.EDIT_LOG_KEY, []), log_entry]

    # DECISION F028 D3 (2) — computed last: raise the job's cost limit, never create or
    # lower one.
    extend_to_usd = record.get("budget_extend_to_usd")
    new_budgets: dict[str, Any] | None = None
    if (extend_to_usd is not None and isinstance(job.budgets, dict)
            and job.budgets.get("max_cost_usd") is not None
            and job.budgets["max_cost_usd"] < extend_to_usd):
        new_budgets = dict(job.budgets)
        new_budgets["max_cost_usd"] = extend_to_usd

    # THE MUTATIONS — everything above is computed; `job` changes only from here on.
    job.tasks.append(fresh)
    job.task_plan = new_body
    if new_budgets is not None:
        job.budgets = new_budgets
```

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/orchestration/test_plan_editing.py tests/orchestration/test_plan_edit_execution.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_manifest.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_worktree_resume_cli.py tests/orchestration/test_job_plan.py tests/orchestration/test_mint_call_sites.py tests/orchestration/test_human_change_one_path.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_unified_store_parity.py tests/orchestration/test_run_manifest_strict_boundaries.py tests/orchestration/test_budget_guard.py tests/orchestration/schemas/test_schemas.py tests/orchestration/test_structured_outputs.py tests/orchestration/test_import_reachability.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1644 passed, 7 skipped in 211.04s (0:03:31)
REAL_EXIT=0
```
The reviewer's own baseline (same selection, at `bdb659161` before any
change) read `1593 passed, 7 skipped` at exit 0. `--collect-only -q` node
counts of the two edited test files:
```
                                bdb659161   C6 (d862e2a44)
test_task_injection.py               67           116
test_task_injection_runner.py         6             8
```
Delta: (116-67) + (8-6) = 49 + 2 = 51. 1593 + 51 = 1644, exactly this run's
total — no unexplained difference. The seven skips are the same F252
quarantines (6 in `test_named_bugs.py`, 1 in `test_agent_tooling.py`),
unchanged.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=161"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0.

### G5 — THE RED PROOFS
`git worktree add --detach .remedy-wt/f028-r3-mut d862e2a44` (C6) then
`python3 -B .agent/authored/f028-r3-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r3-mut`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1_confirmed_injections_accepts_a_record_lacking_text (packages/orchestration/task_injection.py): exit=1 failed=3 nodes=['tests/orchestration/test_task_injection.py::TestConfirmedRecordFieldValidation::test_missing_string_field_raises[text]', 'tests/orchestration/test_task_injection.py::TestConfirmedRecordFieldValidation::test_wrong_type_string_field_raises[text]', 'tests/orchestration/test_task_injection_runner.py::TestConfirmedInjectionMissingAFieldBlocksTheJob::test_missing_text_blocks_with_task_injection_control_error']
m2_apply_injection_to_job_lowers_a_higher_limit_to_the_extension (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestApplyInjectionToJobBudgetExtension::test_never_lowers_an_already_higher_limit']
m3_apply_injection_to_job_creates_a_limit_on_a_job_that_has_none (packages/orchestration/task_injection.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestApplyInjectionToJobBudgetExtension::test_never_lowers_an_already_higher_limit', 'tests/orchestration/test_task_injection.py::TestApplyInjectionToJobBudgetExtension::test_never_creates_a_limit_on_a_job_without_one']
m4_answer_injection_shortfall_skips_the_needs_decision_status_check (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestAnswerInjectionShortfall::test_a_confirmable_draft_answers_draft_not_in_shortfall']
m5_shrink_task_derives_its_draft_at_the_old_band (packages/orchestration/task_injection.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestAnswerInjectionShortfall::test_shrink_task_from_m_to_s_answers_a_confirmable_derived_draft', 'tests/orchestration/test_task_injection.py::TestAnswerInjectionShortfall::test_shrink_task_from_l_to_m_is_still_a_shortfall']
m6_cannot_shrink_is_checked_only_after_the_answer_file_is_published (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestAnswerInjectionShortfall::test_cannot_shrink_when_already_the_smallest_size']
m7_the_extend_budget_draft_carries_budget_extend_to_usd_none (packages/orchestration/task_injection.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestAnswerInjectionShortfall::test_extend_budget_answers_a_confirmable_draft_with_no_shortfall', 'tests/orchestration/test_task_injection_runner.py::TestBudgetExtensionReachesThePredictiveCheck::test_the_extended_limit_reaches_every_predictive_call_and_the_job_records_it']
m8_the_extend_budget_check_is_computed_over_the_old_limit (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestAnswerInjectionShortfall::test_extend_budget_answers_a_confirmable_draft_with_no_shortfall']
m9_confirm_task_injection_drops_budget_extend_to_usd (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection_runner.py::TestBudgetExtensionReachesThePredictiveCheck::test_the_extended_limit_reaches_every_predictive_call_and_the_job_records_it']
m10_the_extend_budget_label_names_no_amount (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestInjectionBudgetCheckAndShortfallSeed::test_question_and_labels_are_exact_sentences_with_a_smaller_band']
m11_fold_injections_here_never_rebinds_job_budgets (packages/orchestration/pingpong_job.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection_runner.py::TestBudgetExtensionReachesThePredictiveCheck::test_the_extended_limit_reaches_every_predictive_call_and_the_job_records_it']
restored byte-identical: True (packages/orchestration/task_injection.py)
restored byte-identical: True (packages/orchestration/pingpong_job.py)
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 11 mutations red with at least one failing node each; no mutation
stayed green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r3-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 63 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r3-block.md`, at `1ce006817`) vs
  `.remedy-wt/f028-r3/block.md`: byte-identical, sha256
  `2d4ee9a4da1ee8a0d3afde7996fe4633bd2c6f9823db206fddbcf66af64467b3` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r3-plan.md`, at `1ce006817`) vs
  `.remedy-wt/f028-r3-payloads/plan.md`: byte-identical, sha256
  `4d3ce761c647b0ac8989aacc2de00aa082b6d203c18c47b7bc6046dd414b012e` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r3-records.diff`, at
  `1ce006817`) vs `.remedy-wt/f028-r3-payloads/records.diff`:
  byte-identical, sha256
  `8c900898eb62dacdfcc3fb1915f91324bfd62f6a677f8fb205fc16cb031ae5d2` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production code (`task_injection.py`, `pingpong_job.py`), its tests
(two files) and the mutation tool (`f028-r3-mutations.py`) are the
WORKER's own authored code against the block's specification S1–S5, not
reviewer-authored text, so no fidelity comparison applies to them.

## Deviations & assumptions

1. `apply_injection_to_job` gains `injection_block["budget_extend_to_usd"]`
   ONLY when the input `record` itself carries that key at all (`if
   "budget_extend_to_usd" in record:`), rather than unconditionally
   `record.get("budget_extend_to_usd")` (which would always be at least
   `None`). Justification: S1 and S4 both frame this field as "when
   present" throughout the spec, and the round's own claim that the
   `option_labels` index rewrite is "the only edit this round makes to a
   test round 1 wrote" is verifiable evidence that no round-2 test needed
   editing — `TestApplyInjectionToJob::test_appends_provenance_...`
   (`a49858dda`, round 2) asserts the `injection` block's exact 9-key
   shape via `_confirmed_record()`, which never carries the key. The
   unconditional reading would have broken that exact-equality assertion,
   forcing either a second test edit (contradicting the round's own
   "only edit" claim) or an undeclared silent break. The conditional
   reading satisfies the letter of S4 ("gains ... the record's value"), is
   symmetric with S1's own "when present" validation rule for the same
   field, and left that round-2 test green with zero edits — confirmed by
   the full G4 run above. `confirm_task_injection` (S4) always writes the
   key (`None` when the draft named no extension), so every record
   reaching `apply_injection_to_job` through the real confirm→fold path
   carries it either way; only a hand-built test record omitting the key
   entirely (as round 2's builder does by default) takes the "absent"
   branch, and the new round-3 tests exercise the "present" branch
   directly via `_confirmed_record(budget_extend_to_usd=...)`.
2. `_confirmed_record()` (the shared test builder in
   `test_task_injection.py`) gained one new optional keyword,
   `budget_extend_to_usd`, defaulting to a sentinel that omits the key
   entirely — preserving every existing call's exact prior output byte for
   byte. This is an additive extension to a helper, not an edit to an
   existing test's assertions; no existing test's behavior changed.
3. `answer_injection_shortfall`'s `extend_budget` branch hardcodes
   `shortfall = False` (and therefore `status = "confirmable"`,
   `decision_seed = None`) rather than branching on the freshly computed
   check's own `shortfall` reading, unlike the `shrink_task` branch which
   does branch on it. Justification: S3 states plainly "extend_budget
   publishes a derived draft at the old band, status confirmable" with no
   conditional language, unlike the explicit "a shortfall making it
   needs_decision" clause given for `shrink_task`; the seed's
   `extend_to_usd` is itself computed by `ROUND_CEILING` specifically to
   guarantee the extended check clears, so the two readings coincide in
   every real run — confirmed by `test_extend_budget_answers_a_confirmable_draft_with_no_shortfall`,
   which independently asserts the computed check's `shortfall` reads
   `False`.
4. Test-file line/byte/sha256 measurements in this handback were taken with
   a small Python helper script under `.remedy-wt/f028-r3-worker/`
   (gitignored, this round's own scratch directory) rather than shell
   pipelines the sandbox denies (`wc`, command substitution) — per the
   block's own "THIS SANDBOX REFUSES SHAPES" section, which names exactly
   this workaround (`python3 - <<'PY'` for counting/hashing/copying).

No test went red unexpectedly, no reviewer payload was edited or retyped,
no gate was skipped, and every G5 mutation was caught on the first run — no
fix-up test was required.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | both test files fit in one commit under the 500-line cap (374+100=474); no split needed |
| C6 | done | |
| C7 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | all 11 mutations caught, both controls clean, both files restored byte-identical |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| R-1077 | done | repaired at C3 (`4f4460b23`): `_validate_confirmed_record` closes the hole in `confirmed_injections`, and `apply_injection_to_job` is reordered so every value it reads is computed before `job` is mutated; its cases pinned in `TestConfirmedRecordFieldValidation` and the job-untouched parametrized test at C5 (`f564160fa`); the repair awaits review before it can be marked `Done:` in the ledger |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 3,
then the run-log event of a folded injection with its readers and `remedy
job inject`. Open findings (by `open_finding_ids` at this round's head): 1
(R-1077, its repair awaiting review). Operator questions open: 0.
