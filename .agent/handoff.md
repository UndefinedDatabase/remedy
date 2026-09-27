# Handoff — F028, round 1

## Session

SESSION 1 of feature F028 · round 1 · rounds so far 1. Context remaining at
handback: comfortable — this round wrote one new module and its test file
from a specification (no repair loop, no red mutation needed a fix-up test,
every gate matched on the first try), leaving ample context had a further
round been required this session.

## Range

Review of `ceb90b8a8`..`HEAD` (`HEAD` is this handback's own commit, `F028
R1 C5`, on `feature/f028-task-injection`).

## Commits

### d7cdc4025 F028 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r1-block.md | 339/0 | copy of this round's block |
| .agent/authored/f028-r1-context.md | 35/0 | copy of the context payload |
| .agent/authored/f028-r1-plan.md | 31/0 | copy of the plan payload |

Measured insertions: 405 (block's own line count 339 + 66), matching the
block's expectation exactly, under the 500-line cap.

### 3e9c5f058 F028 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r1-claim.diff | 162/0 | copy of the claim diff payload |

Matches the block's expected insertions (162) exactly.

### 89ad1f1c0 F028 R1 C2: claim F028, re-head the live review record, book F288 R10, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | 13/13 | rewrite from the context payload |
| .agent/decisions.md | 80/0 | DECISION F028 D1 appended |
| .agent/live_review.md | 23/20 | re-head (heading + intro paragraph + Steps) plus F288 R10's Gate entry appended |
| .agent/plan.md | 18/13 | rewrite from the plan payload |
| docs/roadmap/STATUS.md | 1/1 | F028's line `[ ]` → `[~]` |

Matches the block's expected numstat (13/13, 80/0, 23/20, 18/13, 1/1)
exactly. Applied via `git apply --check` (exit 0) then the real apply
(exit 0) of `claim.diff`, followed by the two payload rewrites.

### a6128ea86 F028 R1 C3a: draft the injection text, gate, id and placement (part 1 of 2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/task_injection.py | 289/0 | new module: S1 constants and exceptions, S2 the draft model, S3 the text, S4 the gate and id, S5 the placement |

### 8d5358bce F028 R1 C3b: the budget check, shortfall seed, fences, prompt and the draft's control file (part 2 of 2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/task_injection.py | 342/0 | S6 the budget check and shortfall seed, S7 the fences and the prompt, S8 the draft and its control file |
| tests/test_no_orphan_modules.py | 2/0 | `ALLOWED_UNWIRED` entry for the new, still-unwired module |

C3a + C3b together are the block's single C3 ("the code"), split by DECISION
of this round under constraint 2: the whole module is 631 insertion lines,
over the 500-line cap by itself, so it is split by SECTION (S1–S5, then
S6–S8) exactly as the F289 R2 C3a/C3b precedent (`doc_staleness.py`, 494 then
322 lines) splits a single new module across two commits. Each half is
independently syntactically valid Python.

### d7f73dadc F028 R1 C4a: test the injection draft pass (part 1 of 2)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_injection.py | 447/0 | new test file: S3–S8 coverage, 43 tests |

### 32e9931d8 F028 R1 C4b: add the mutation tool for the round's red proofs (part 2 of 2)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r1-mutations.py | 209/0 | the G5 mutation (red-proof) tool |

C4a + C4b together are the block's single C4 ("the tests and the tool"),
split under the same 500-line constraint: 447 + 209 = 656 combined, over the
cap; each part alone is well under it.

### F028 R1 C5: rewrite handoff for round 1 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- `git checkout -b feature/f028-task-injection` from `main` at `ceb90b8a8` —
  succeeded (Open PR Gate had already run before this round; `main` was
  already at the merge commit, so no pull).
- `git worktree add --detach .remedy-wt/f028-r1-mut HEAD` (at C4b,
  `32e9931d8`) for G5 — succeeded; `git worktree remove --force
  .remedy-wt/f028-r1-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 61 before the add and 61
  after the remove (step 4's own reading, unchanged).
- `git push -u origin feature/f028-task-injection` after C5 — reported
  under G6 in this round's reply (run after this file is committed).
- No `gh pr create` (the block explicitly forbids it this round: the branch
  opens a pull request at F028's closure, not here), no `gh pr merge`, no
  checkout of `main` after the branch was cut, no branch deletion, no
  force-push, no `git stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `claim.diff`: 162 lines, 18447 bytes, sha256
  `6bbd385903e1ac6bcaf0bc7984ca7ff0499750482d6c07eb1d9576fd809f22d6`.
- `context.md`: 35 lines, 1462 bytes, sha256
  `72fac8a4bb22b544cd25f48eadccdd1a0d0a43a5b2f3f4a4b86b790d396f5683`.
- `plan.md`: 31 lines, 1178 bytes, sha256
  `9c5cdea09c3134af7505405261ba73f8ed58e9e32b6bb34db25532286031cb38`.
- Block: 339 lines, sha256
  `1d3282767f57062812424ab6cfa6459618e91390c48e8fe6106c5c274d803913` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f028-r1-*` payload copy, read back with `git show
<commit>:<path>` from the commit that added it, compared byte-for-byte
(sha256) against its source: all four (block at `d7cdc4025`, plan and
context at `d7cdc4025`, claim.diff at `3e9c5f058`) — MATCH.

### G2 — THE CLAIM
`git show 89ad1f1c0:<path>`, bytes and sha256, each MATCHING the reviewer's
table exactly:
```
docs/roadmap/STATUS.md   bytes=54827    b04a95ce95ad188d7b71b81053613dc0338031914d8b2b05b4fc544f918f6c39
.agent/live_review.md    bytes=309281   cd3ff35d8c4c71ff1bef4dadf8251484b6ea85ab7450899cb019681608909860
.agent/decisions.md      bytes=2250640  56a1d938b0db6bfb7ac41d6c52acb2a20b7356da40395a7fc913a1cf2437ba6f
.agent/plan.md           bytes=1178     9c5cdea09c3134af7505405261ba73f8ed58e9e32b6bb34db25532286031cb38
.agent/context.md        bytes=1462     72fac8a4bb22b544cd25f48eadccdd1a0d0a43a5b2f3f4a4b86b790d396f5683
```
All five MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text at `ceb90b8a` and at
`89ad1f1c0` (C2): `[]` both times — matching the reviewer's reading (empty
at both). At C2 the ledger has exactly one line reading `## Findings` and
exactly one reading `## Steps`; its last line begins `Gate: F288 R10 — the
F288 round 10 entry` — MATCH. F028's STATUS line at C2 reads in full `- [~]
F028 — Task injection` — begins `- [~] F028 — ` as required. `git diff
--name-only 3e9c5f058 89ad1f1c0` names exactly: `.agent/context.md`,
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md` — the table's five paths, no more, no fewer.

### G3 — THE CODE
```
$ bash -c 'python3 -m ruff check packages/orchestration/task_injection.py tests/orchestration/test_task_injection.py tests/test_no_orphan_modules.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```
`place_injected_task`, `shortfall_decision_seed` and the refusal ladder at
the top of `draft_task_injection`, quoted whole from `git show 8d5358bce:
packages/orchestration/task_injection.py` (C3's completed state, C3a+C3b):

```python
def place_injected_task(plan_tasks: Any, files_hint: Any, *,
                        after: str | None = None) -> dict[str, Any]:
    """Where a new task lands: always at the END of the plan, over a list of ``PlannedTask``.

    In order: ``after`` not None and not an id of ``plan_tasks`` raises
    ``TaskInjectionRefused("unknown_task", ...)``; ``after`` given and known is
    ``depends_on=[after]``, basis ``stated``; otherwise every plan task sharing a path with
    ``files_hint``, in plan order, is basis ``content_overlap``; otherwise ``depends_on=[]``,
    basis ``frontier_default``.
    """
    tasks = list(plan_tasks)
    ids = [t.id for t in tasks]
    position = len(tasks)

    if after is not None:
        if after not in ids:
            listing = ", ".join(ids[:10])
            if len(ids) > 10:
                listing += f" and {len(ids) - 10} more"
            raise TaskInjectionRefused(
                "unknown_task",
                f"there is no task {after!r} in this job's plan; its tasks are: {listing}")
        return {
            "depends_on": [after],
            "basis": PLACEMENT_STATED,
            "position": position,
            "rationale": f"placed after {after} because you named it",
        }

    hint_paths = {_norm_path(p) for p in files_hint}
    overlap_ids: list[str] = []
    overlap_paths: set[str] = set()
    for task in tasks:
        task_paths = {_norm_path(p) for p in (task.files_hint or [])}
        shared = task_paths & hint_paths
        if shared:
            overlap_ids.append(task.id)
            overlap_paths |= shared

    if overlap_ids:
        return {
            "depends_on": list(overlap_ids),
            "basis": PLACEMENT_CONTENT_OVERLAP,
            "position": position,
            "rationale": (
                f"placed after {', '.join(overlap_ids)} because they touch the same files: "
                f"{', '.join(sorted(overlap_paths))}"),
        }

    return {
        "depends_on": [],
        "basis": PLACEMENT_FRONTIER_DEFAULT,
        "position": position,
        "rationale": (
            "placed at the end of the plan with no dependency, because no planned task "
            "touches its files"),
    }
```

```python
def shortfall_decision_seed(check: dict[str, Any]) -> dict[str, Any]:
    """The three-option menu a shortfall answers with (DECISION F028 D1 (8))."""
    plan_band = check["plan_band"]
    shrink_band = _SHRINK_BAND.get(plan_band)

    spent = check.get("spent_cost_usd")
    expected = check.get("expected_cost_usd")
    extend_to_usd: float | None = None
    if spent is not None and expected is not None:
        extend_to_usd = float(
            Decimal(repr(round(spent + expected, 6))).quantize(
                Decimal("0.01"), rounding=ROUND_CEILING))

    shrink_label = (
        "the task cannot shrink any further" if shrink_band is None
        else f"shrink the task to the {shrink_band} band")
    option_labels = {
        "extend_budget": "extend the job's budget to cover this task",
        "shrink_task": shrink_label,
        "drop": "drop this task",
    }
    return {
        "question": "the injected task would breach the job's budget; how should it proceed?",
        "options": list(SHORTFALL_OPTIONS),
        "option_labels": [option_labels[option] for option in SHORTFALL_OPTIONS],
        "arithmetic": check["arithmetic"],
        "extend_to_usd": extend_to_usd,
        "shrink_band": shrink_band,
    }
```

```python
def draft_task_injection(
    job: Any,
    text: Any,
    *,
    call_fn: Callable[[str, int], str] | None,
    budgets: Any,
    counters: Any,
    config: Any,
    actor: Any,
    after: str | None = None,
    now: datetime | None = None,
    control_root_path: Path | None = None,
) -> dict[str, Any]:
    """Draft one injected task from ``text``, or answer a refusal. NEVER raises.

    Checks, in order: S3's text, S4's terminal check, ``job.task_plan`` (``no_task_plan``),
    S4's task-cap check, S5's unknown ``after`` (before any planner call), a missing
    ``call_fn`` (``planner_unavailable``), the one structured call (``draft_unparseable``),
    and the candidate ``TaskPlan`` the drafted task would join (``draft_invalid``). A refusal
    writes nothing.
    """
    try:
        validated_text = validate_injection_text(text)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    job_state = getattr(job, "state", "")
    refusal = injection_refusal(job_state, 0)
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    raw_plan = getattr(job, "task_plan", None)
    plan: TaskPlan | None = None
    if isinstance(raw_plan, dict):
        try:
            plan = TaskPlan.model_validate(
                {k: v for k, v in raw_plan.items() if not k.startswith("_")})
        except ValidationError:
            plan = None
    if plan is None:
        return {"outcome": "refused", "code": "no_task_plan",
                "detail": "this job has no readable task plan to inject into"}

    refusal = injection_refusal(job_state, len(plan.tasks))
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    try:
        place_injected_task(plan.tasks, [], after=after)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    if call_fn is None:
        return {"outcome": "refused", "code": "planner_unavailable",
                "detail": "no planner call is available to draft this task"}

    prompt = compose_injection_prompt(validated_text, plan.tasks, after=after)
    outcome = run_structured_call(InjectedTaskDraft, prompt, call_fn)
    if not outcome.ok:
        return {"outcome": "refused", "code": "draft_unparseable",
                "detail": "the planner's draft reply could not be parsed as a task"}
```

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_plan_editing.py tests/orchestration/test_task_veto.py tests/orchestration/test_budget_guard.py tests/orchestration/schemas/test_schemas.py tests/orchestration/test_structured_outputs.py tests/orchestration/test_import_reachability.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1065 passed, 7 skipped in 85.92s (0:01:25)
REAL_EXIT=0
```
The reviewer's own baseline (same selection LESS `test_task_injection.py`,
at `ceb90b8a` before any change) read `1022 passed, 7 skipped` at exit 0.
This run's own new file collects 43 nodes (`--collect-only -q` read `43
tests collected`); 1022 + 43 = 1065, exactly this run's total — no
unexplained difference. The seven skips are the same F252 quarantines
(6 in `test_named_bugs.py`, 1 in `test_agent_tooling.py`), unchanged.

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
`git worktree add --detach .remedy-wt/f028-r1-mut HEAD` (HEAD = C4b,
`32e9931d8`) then `python3 -B .agent/authored/f028-r1-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r1-mut`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1_s3_admits_bel_x07: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestValidateInjectionText::test_text_invalid_control_character']
m2_s4_answers_none_for_a_terminal_job: exit=1 failed=4 nodes=['tests/orchestration/test_task_injection.py::TestInjectionRefusal::test_terminal_states_name_a_follow_up_job[completed]', 'tests/orchestration/test_task_injection.py::TestInjectionRefusal::test_terminal_states_name_a_follow_up_job[failed]', 'tests/orchestration/test_task_injection.py::TestInjectionRefusal::test_terminal_states_name_a_follow_up_job[cancelled]', 'tests/orchestration/test_task_injection.py::TestInjectionRefusal::test_terminal_wins_over_a_full_plan']
m3_next_injected_task_id_always_answers_inj1: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestNextInjectedTaskId::test_smallest_free_id']
m4_s5_ignores_after: exit=1 failed=3 nodes=['tests/orchestration/test_task_injection.py::TestPlaceInjectedTask::test_stated_after_a_known_task', 'tests/orchestration/test_task_injection.py::TestPlaceInjectedTask::test_unknown_after_names_the_first_ten_and_the_rest', 'tests/orchestration/test_task_injection.py::TestDraftTaskInjection::test_unknown_after_refuses_before_any_call_and_writes_nothing']
m5_s5_never_finds_a_content_overlap: exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestPlaceInjectedTask::test_content_overlap_in_plan_order', 'tests/orchestration/test_task_injection.py::TestPlaceInjectedTask::test_leading_dot_slash_normalizes']
m6_xl_reads_as_token_band_high: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestInjectionBudgetCheckAndShortfallSeed::test_band_xl_reads_as_unknown_with_class_default_missing_band']
m7_a_shortfall_answer_carries_the_draft_id_as_its_confirm_token: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestDraftTaskInjection::test_shortfall_answer_has_no_token_and_needs_decision_status']
m8_extend_to_usd_rounds_down: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestInjectionBudgetCheckAndShortfallSeed::test_extend_to_usd_rounds_up_to_the_cent']
m9_read_injection_draft_refuses_only_strictly_after_expires_at: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestDraftTaskInjection::test_read_injection_draft_expiry_boundary']
m10_s7_never_flags_a_deny_glob: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestFenceConflicts::test_deny_glob_is_flagged_with_its_glob']
m11_the_structured_call_runs_with_allow_parse_retry_false: exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestDraftTaskInjection::test_planner_calls_two_after_one_invalid_reply', 'tests/orchestration/test_task_injection.py::TestDraftTaskInjection::test_draft_unparseable_after_two_invalid_replies_writes_nothing']
m12_the_unknown_after_check_runs_after_the_call_instead_of_before_it: exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestDraftTaskInjection::test_unknown_after_refuses_before_any_call_and_writes_nothing']
restored byte-identical: True (packages/orchestration/task_injection.py)
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 12 mutations red with at least one failing node each; no mutation
stayed green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r1-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 61 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r1-block.md`, at `d7cdc4025`) vs
  `.remedy-wt/f028-r1/block.md`: byte-identical, sha256
  `1d3282767f57062812424ab6cfa6459618e91390c48e8fe6106c5c274d803913` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r1-plan.md`, at `d7cdc4025`) vs
  `.remedy-wt/f028-r1-payloads/plan.md`: byte-identical, sha256
  `9c5cdea09c3134af7505405261ba73f8ed58e9e32b6bb34db25532286031cb38` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `context.md` copy (`.agent/authored/f028-r1-context.md`, at `d7cdc4025`)
  vs `.remedy-wt/f028-r1-payloads/context.md`: byte-identical, sha256
  `72fac8a4bb22b544cd25f48eadccdd1a0d0a43a5b2f3f4a4b86b790d396f5683` both
  sides; used to rewrite `.agent/context.md` via `shutil.copyfile` at C2.
- `claim.diff` copy (`.agent/authored/f028-r1-claim.diff`, at `3e9c5f058`)
  vs `.remedy-wt/f028-r1-payloads/claim.diff`: byte-identical, sha256
  `6bbd385903e1ac6bcaf0bc7984ca7ff0499750482d6c07eb1d9576fd809f22d6` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production module and its tests (`task_injection.py`,
`test_task_injection.py`) and the mutation tool (`f028-r1-mutations.py`)
are the WORKER's own authored code against the block's specification S1–S8,
not reviewer-authored text, so no fidelity comparison applies to them.

## Deviations & assumptions

1. C3 was split into C3a/C3b, and C4 was split into C4a/C4b, departing from
   the block's literal single-commit-per-letter sequence. Justification:
   constraint 2's own 500-insertion cap — the whole new module is 631
   insertion lines by itself (over the cap alone), and the test file plus
   the mutation tool together are 447 + 209 = 656 (also over the cap
   combined) — and constraint 2 explicitly names this exact split
   ("C3a and C3b, C4a and C4b") as the required response. C3 was split by
   SECTION (S1–S5 in C3a, S6–S8 in C3b), each half independently
   syntactically valid, mirroring the F289 R2 C3a/C3b precedent for a
   single new module. C4 was split by artifact (the test file in C4a, the
   mutation tool in C4b), mirroring the F288 R1/R2 and F027 R1 C4a/C4b
   precedents.
2. `injection_refusal` is called twice inside `draft_task_injection` — once
   with `plan_task_count=0` (to apply only S4's terminal check, before the
   plan is even parsed) and once with the real task count once the plan is
   read — because the block's own ladder orders the terminal check strictly
   before `no_task_plan`, and the cap check strictly after it, and
   `injection_refusal`'s own signature ties both checks to one call. This
   is a design choice made to satisfy the specified ordering exactly, not
   a change to `injection_refusal`'s tested behaviour: a terminal state
   still refuses `job_terminal` regardless of which count accompanies it
   (a plan_task_count of 0 never independently triggers `plan_full`).
3. `place_injected_task(plan.tasks, [], after=after)` is called once,
   pre-call, purely to trigger S5's unknown-`after` ladder rung before any
   planner call is made (per the block's explicit ordering); its result is
   discarded, and the real placement is computed again after the draft
   returns, over the draft's own `files_hint`. Both calls are pure and
   inexpensive.
4. No test exercises `no_task_plan` or `draft_invalid` through
   `draft_task_injection` directly (only `injection_refusal`'s `plan_full`
   is tested standalone) — the block's test list is an "AT LEAST" list and
   does not name these two paths, and no G5 mutation targets them either.
   Not treated as a gap against this round's DONE-WHEN.

No test went red unexpectedly, no reviewer payload was edited or retyped,
no gate was skipped, and every G5 mutation was caught on the first run —
no fix-up test was required.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3a | deviated | block named one commit "C3"; split into C3a/C3b under constraint 2's 500-line cap (see Deviations §1) |
| C3b | deviated | see C3a |
| C4a | deviated | block named one commit "C4"; split into C4a/C4b under constraint 2's 500-line cap (see Deviations §1) |
| C4b | deviated | see C4a |
| C5 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | all 12 mutations caught, control clean before and after, file restored byte-identical |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 1,
then T002 — the confirmation: the runner folding a confirmed injection into
a running job at its safe points, the plan's edit log, the provenance, the
event and its readers, and the shortfall seed's three answers. Open findings
(by `open_finding_ids` at this round's head): 0. Operator questions open: 0.
