# Handoff — F028, round 5

## Session

SESSION 1 of feature F028 · round 5 · rounds so far 5. Context remaining at
handback: comfortable — this round wrote one new module-level function, one
new HTTP dispatch method, three new door guard checks, one new run-log
event write site, and roughly 400 lines of new tests plus a 262-line
mutation tool, with zero self-caught implementation bugs in the production
code and every gate matching cleanly on the first run.

## Range

Review of `6814c6865`..`HEAD` (`HEAD` is this handback's own commit, `F028
R5 C7`, on `feature/f028-task-injection`).

## Commits

### 6e2a9b37a F028 R5 C1: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r5-block.md | 266/0 | copy of this round's block |
| .agent/authored/f028-r5-plan.md | 30/0 | copy of the plan payload |
| .agent/authored/f028-r5-records.diff | 71/0 | copy of the records diff payload |

Measured insertions: 367 (block's own line count 266 + 101), matching the
block's expectation exactly, under the 500-line cap.

### e4796697c F028 R5 C2: book round 4, register R-1078, record D5 and two prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 41/0 | DECISION F028 D5 appended |
| .agent/live_review.md | 4/0 | round 4's Gate entry and R-1078's registration appended |
| .agent/plan.md | 9/9 | rewrite from the plan payload |
| .agent/prose_slips.md | 2/0 | two round-4 prose slips appended |

Matches the block's expected numstat (41/0, 4/0, 9/9, 2/0) exactly. Applied
via `git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### 6489fdedb F028 R5 C3: repair R-1078 and resolve an after reference for the door
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job_inject_cmd.py | 13/4 | S1 (R-1078's repair): `--yes` over a shortfall never calls `emit_ok`; under `--json` it calls only `fail("draft_needs_decision", ...)` carrying `draft_id`, `decision_seed` and `budget_check`; without `--json` it still prints the seed first, then fails the same way |
| packages/orchestration/task_injection.py | 30/0 | S2: `resolve_after_ref(job, ref)` added and exported — the door's own `after` resolver, never the command line's `_resolve_after` |

43 insertions total, under the 500-line cap — no split needed. The block
sized neither C3 nor C4 individually (only C1 and C2), so no
expected-insertion comparison applies here per "WHAT TO REPORT."

### 3741c8a71 F028 R5 C4: accept job.inject, job.inject-confirm and job.inject-answer at the write door
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 4/0 | S3: the three ids join `UI_EXPOSED_COMMANDS`, after `job.veto-task`, under one comment naming DECISION F028 D5 |
| packages/orchestration/ui_server.py | 117/0 | S3: the three `JOB_INJECT_*` constants, `_handle_command_submission`'s new branch (the veto branch's body, `_dispatch_injection` in place of its dispatch call), `_dispatch_injection` itself, and `_read_command_payload`'s three new field checks |
| tests/ui_server/test_command_channel.py | 31/2 | S4: the sorted-ids literal gains the three ids; `DOOR_METHODS` gains `_dispatch_injection`; `ALLOWED_IMPORTS` gains the nine `task_injection` name pairs the two door methods import, each commented `# F028 D5`; `test_every_exposed_command_reaches_the_answer_its_effect_gives` gains the three new branches and one docstring sentence per id |

152 insertions total, under the 500-line cap — no split needed.

### fcc05c338 F028 R5 C5: write task_injected when the runner folds an injection
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanizeCatalog.ts | 1/0 | S5: `STREAM_EVENT_CATALOG` gains `task_injected` between `task_gate_evaluated` and `task_lesson_written` |
| packages/orchestration/event_names.py | 1/0 | S5: `EVENT_NAMES` gains `task_injected` between `task_decision_answered` and `task_lesson_written` |
| packages/orchestration/pingpong_job.py | 28/0 | S5: `_fold_task_injections` collects one event dict per folded record (applied or inert) and, AFTER `_persist_job`, writes each through `RunLogWriter(job.job_id).log("task_injected", ...)` |

30 insertions total, under the 500-line cap — no split needed.

### e17f1ce45 F028 R5 C6: test the door's injection commands, the event and the resolver
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_inject.py | 21/0 | R-1078's repair test: `--yes --json` over a shortfall leaves stdout parseable as exactly one JSON document, `draft_needs_decision` carrying the draft id and the seed |
| tests/orchestration/test_task_injection.py | 35/0 | `TestResolveAfterRef`, S2's four answers (None, a planned id unchanged, an entry id resolved, an unmatched ref unchanged) |
| tests/orchestration/test_task_injection_runner.py | 75/0 | `TestTaskInjectedEvent`: an applied fold writes one event naming the new entry's task id; an inert fold writes one naming its reason; a second run writes none |
| tests/ui_server/test_command_dispatch.py | 242/0 | NEW `TestInjectionDispatchEffects`, built as `TestVetoTaskDispatchEffects` is: a drafted `job.inject` (actor, one draft file), `after` by entry id reaching the planned id, `job.inject-confirm` (one file, second is 409 `already_confirmed`), `job.inject-answer` `drop` over a shortfall, a bad text/option 400 with no control file, a terminal job 409 `job_terminal` |

373 insertions total. **DECLARED DEVIATION (constraint 2 split):** the
block's bundle names one C6 carrying both the four test files and the
mutation tool; 373 (tests) + 262 (tool) = 635 would exceed the 500-line
cap, so this round split it into C6 (this commit, tests only) and C6b
(the tool alone), per constraint 2's own instruction to split and name
each part with its own subject. The selection of G4 stays green after
both parts (verified below).

### 1a3c4a465 F028 R5 C6b: add the round 5 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r5-mutations.py | 262/0 | the G5 mutation (red-proof) tool, 9 mutations (m1–m9) across the four touched production files |

### F028 R5 C7: rewrite handoff for round 5 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 4.
- `git worktree add --detach .remedy-wt/f028-r5-base-count 6814c686` (to
  measure base `--collect-only` node counts for G4's accounting) —
  succeeded; `git worktree remove --force
  .remedy-wt/f028-r5-base-count` and `git worktree prune` afterwards —
  both succeeded, `git worktree list | wc -l` read 65 before and after.
- `git worktree add --detach .remedy-wt/f028-r5-mut 1a3c4a465` (at C6b,
  G5's own ordered worktree) — succeeded; `git worktree remove --force
  .remedy-wt/f028-r5-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 65 before the add and 65
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
- `plan.md`: 30 lines, 1068 bytes, sha256
  `ea6ff390bddb5c46d3030febe9f9ea4ae399426aaf1d04cbe09c118419750265`.
- `records.diff`: 71 lines, 13248 bytes, sha256
  `074a99b06ed1a9a9b18e8f1e4cc924d29a5c45a49e76fb0093f741b749f9e8c2`.
- Block: 266 lines, sha256
  `57a984efa3ba0fa1788bd2a33ddc1d63c17344894216589a6dc52141e84a275a` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f028-r5-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`6e2a9b37a`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r5-block.md MATCH sha=57a984efa3ba0fa1788bd2a33ddc1d63c17344894216589a6dc52141e84a275a
.agent/authored/f028-r5-records.diff MATCH sha=074a99b06ed1a9a9b18e8f1e4cc924d29a5c45a49e76fb0093f741b749f9e8c2
.agent/authored/f028-r5-plan.md MATCH sha=ea6ff390bddb5c46d3030febe9f9ea4ae399426aaf1d04cbe09c118419750265
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`e4796697c`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md bytes=324718 sha256=5d5ee90fbaf255e3ee9befcb173084925160b6361d4d9ac13b1e039b8897f653
.agent/decisions.md   bytes=2266429 sha256=13170b346f8391108eb1caf8109ad1b578b754818d03de035ff0df3a6e615eaf
.agent/prose_slips.md bytes=373059 sha256=004c013e1b9fa07327841c8233ab268e2b3db59f6f48bdbddcac7767240896c4
.agent/plan.md        bytes=1068   sha256=ea6ff390bddb5c46d3030febe9f9ea4ae399426aaf1d04cbe09c118419750265
```
All four MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text: at `6814c686`
reads `[]`; at C2 (`e4796697c`) reads `['R-1078']` — MATCH against the
reviewer's stated readings. `git diff --name-only 6e2a9b37a e4796697c`
names exactly: `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md` — the table's four paths, no
more, no fewer.

### G3 — THE CODE
```
$ bash -c 'python3 -m ruff check apps/cli/commands/job_inject_cmd.py packages/orchestration/task_injection.py packages/orchestration/ui_server.py apps/cli/command_catalog.py packages/orchestration/pingpong_job.py packages/orchestration/event_names.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/cli/test_job_inject.py tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```

`_dispatch_injection`, quoted whole (C6b state, `packages/orchestration/ui_server.py`):
```python
    def _dispatch_injection(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run one of `job.inject`, `job.inject-confirm` or `job.inject-answer` and build
        the body DECISION F028 D5 (1) rules for it.

        None of the three effects ever raises for a refusal; each one's own `code` and
        `detail` ride in the returned dict unchanged, exactly as `_dispatch_veto_task`'s
        does. `job.inject` and `job.inject-answer` first read the job's budget state
        through `injection_budget_inputs`, DECISION F028 D4 (3)'s shared helper — a
        `TaskInjectionRefused` there is a refusal like any other, not a raised error.
        `job.inject`'s `after` argument is resolved to a planned id by `resolve_after_ref`,
        never by the command line's own resolver, which writes to the terminal.
        """
        from packages.orchestration.task_injection import (
            TaskInjectionRefused,
            answer_injection_shortfall,
            confirm_task_injection,
            draft_task_injection,
            injection_budget_inputs,
            injection_call_fn,
            resolve_after_ref,
        )

        args = payload["args"]
        command = payload["command"]
        actor = token_fingerprint(self._supplied_bearer_token())

        if command == JOB_INJECT_CONFIRM_COMMAND_ID:
            result = confirm_task_injection(job, args["confirm_token"], actor=actor)
            return {"command": command, **result}

        try:
            budgets, counters, config = injection_budget_inputs(job)
        except TaskInjectionRefused as exc:
            return {"command": command, "outcome": "refused", "code": exc.code,
                    "detail": exc.detail}

        if command == JOB_INJECT_COMMAND_ID:
            result = draft_task_injection(
                job, args["text"], call_fn=injection_call_fn(), budgets=budgets,
                counters=counters, config=config, actor=actor,
                after=resolve_after_ref(job, args.get("after")))
        else:                                           # JOB_INJECT_ANSWER_COMMAND_ID
            result = answer_injection_shortfall(
                job, args["draft_id"], args["option"], actor=actor, budgets=budgets,
                counters=counters, config=config)
        return {"command": command, **result}
```

The new branch of `_handle_command_submission`, quoted whole:
```python
        # DECISION F028 D5 maps `job.inject`, `job.inject-confirm` and `job.inject-answer` to
        # `_dispatch_injection`, run with this door's own token fingerprint as the actor.
        # D18's order is unchanged: effect, then the audit line, then the publication. As
        # `job.veto-task`'s branch above, the effect's own refusal `code` and `detail` ride
        # on the wire — `_read_command_payload` already checked each command's own argument
        # shapes before the job was read.
        if payload["command"] in JOB_INJECT_COMMAND_IDS:
            try:
                accepted_body = self._dispatch_injection(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(
                    409, f"{accepted_body['code']}: {accepted_body['detail']}"))
                return
            # D18, clause three: both writes below fail SOFT. The injection is already
            # durable, so refusing after the fact would report an injection that really
            # was requested as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
```

The new checks of `_read_command_payload`, quoted whole:
```python
        # DECISION F028 D5: an injection command names its own fields' shapes, refused
        # BEFORE the job is read, for R-0685's reason above.
        if command == JOB_INJECT_COMMAND_ID:
            from packages.orchestration.task_injection import (
                TaskInjectionRefused,
                validate_injection_text,
            )

            try:
                validate_injection_text(args.get("text"))
            except TaskInjectionRefused as exc:
                return None, _command_field_error("text", exc.detail)
            after = args.get("after")
            if after is not None and (not isinstance(after, str) or not after):
                return None, _command_field_error(
                    "after", "after must be a non-empty string when given")
        if command == JOB_INJECT_CONFIRM_COMMAND_ID:
            confirm_token = args.get("confirm_token")
            if not isinstance(confirm_token, str) or not confirm_token:
                return None, _command_field_error(
                    "confirm_token", "confirm_token must be a non-empty string")
        if command == JOB_INJECT_ANSWER_COMMAND_ID:
            from packages.orchestration.task_injection import SHORTFALL_OPTIONS

            draft_id = args.get("draft_id")
            if not isinstance(draft_id, str) or not draft_id:
                return None, _command_field_error(
                    "draft_id", "draft_id must be a non-empty string")
            if args.get("option") not in SHORTFALL_OPTIONS:
                return None, _command_field_error(
                    "option", f"option must be one of {', '.join(SHORTFALL_OPTIONS)}")
```

The event write of `_fold_task_injections`, quoted whole (the changed
function body, C6b state, `packages/orchestration/pingpong_job.py`):
```python
    from packages.orchestration import task_injection as _ti

    try:
        records = _ti.confirmed_injections(job.job_id, control_root_path=control_root_path)
    except _ti.TaskInjectionError as exc:
        job.state = JOB_BLOCKED
        job.error = f"task_injection_control_error: {exc}"
        _persist_job(job)
        return True

    task_injections = job.metadata.setdefault("task_injections", {})
    changed = False
    folded_events: list[dict[str, Any]] = []

    for record in records:
        draft_id = record["draft_id"]
        if draft_id in task_injections:
            continue                                          # already folded

        planned_id = record["task"]["id"]
        basis = record["placement"]["basis"]
        actor = record["actor"]
        confirmed_unseen = record.get("confirmed_unseen", False)

        try:
            applied = _ti.apply_injection_to_job(job, record)
        except _ti.TaskInjectionRefused as exc:
            task_injections[draft_id] = {
                "inert": exc.detail,
                "folded_at": datetime.now(timezone.utc).isoformat(),
            }
            changed = True
            folded_events.append({
                "outcome": "inert", "task_id": "", "draft_id": draft_id,
                "planned_id": planned_id, "basis": basis, "actor": actor,
                "confirmed_unseen": confirmed_unseen, "reason": exc.detail,
            })
            continue

        task_injections[draft_id] = applied
        changed = True
        folded_events.append({
            "outcome": "applied", "task_id": applied["task_id"], "draft_id": draft_id,
            "planned_id": planned_id, "basis": basis, "actor": actor,
            "confirmed_unseen": confirmed_unseen,
        })

    if changed:
        _persist_job(job)

    # DECISION F028 D5 (2): the event is written AFTER `_persist_job` — a crash between the
    # save and this write loses the event and never duplicates it, since the record already
    # on disk (`task_injections[draft_id]` above) is what keeps this record from being
    # folded, and therefore its event written, a second time.
    if folded_events:
        from packages.orchestration.run_log import RunLogWriter

        writer = RunLogWriter(job.job_id)
        for event in folded_events:
            writer.log("task_injected", **event)

    return False
```

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/cli/test_job_inject.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_sse_stream.py tests/orchestration/test_event_names.py tests/ui_contracts/test_humanize_catalog.py tests/ui_contracts/test_veto_controls_contract.py tests/orchestration/test_teacher_narration.py tests/ui_contracts/test_phase_mapping.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/test_command_catalog.py tests/orchestration/test_dead_command_check.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1514 passed, 7 skipped in 108.86s (0:01:48)
REAL_EXIT=0
```
The reviewer's own baseline at `6814c686` read `1500 passed, 7 skipped` at
exit 0 — matching the reviewer's stated reading exactly. `--collect-only -q`
node counts of the five edited test files:
```
                                     6814c686   C6b (1a3c4a465)
test_job_inject.py                     16            17
test_task_injection.py                136           140
test_task_injection_runner.py           8            11
test_command_channel.py               110           110
test_command_dispatch.py               49            55
```
Delta from the five edited files: (17-16)+(140-136)+(11-8)+(110-110)+(55-49)
= 1+4+3+0+6 = 14. `1514-1500 = 14` exactly — no unexplained difference.
`test_command_channel.py` gained zero nodes because S4 only edits existing
tests, per the block's own instruction; the count confirms no stray new
test slipped in there. The seven skips are the same F252 quarantines (6 in
`test_named_bugs.py`, 1 in `test_agent_tooling.py`), unchanged.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
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
`git worktree add --detach .remedy-wt/f028-r5-mut 1a3c4a465` (C6b) then
`python3 -B .agent/authored/f028-r5-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r5-mut`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1_yes_json_over_a_shortfall_emits_ok_before_fail_again (apps/cli/commands/job_inject_cmd.py): exit=1 failed=1 nodes=['tests/cli/test_job_inject.py::TestInjectYes::test_yes_json_over_a_shortfall_prints_exactly_one_json_document']
m2_resolve_after_ref_never_maps_an_entry_id_to_its_planned_id (packages/orchestration/task_injection.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestResolveAfterRef::test_an_entrys_own_task_id_resolves_to_its_planned_id', 'tests/ui_server/test_command_dispatch.py::TestInjectionDispatchEffects::test_after_by_the_entry_id_reaches_the_drafts_depends_on_as_the_planned_id']
m3_the_doors_job_inject_check_never_calls_validate_injection_text (packages/orchestration/ui_server.py): exit=1 failed=3 nodes=['tests/ui_server/test_command_dispatch.py::TestInjectionDispatchEffects::test_a_bad_text_is_400_and_a_bad_option_is_400_with_no_control_file_written', 'tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_every_exposed_command_reaches_the_answer_its_effect_gives', 'tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_imports_exactly_the_allowed_set']
m4_the_doors_option_check_admits_any_string (packages/orchestration/ui_server.py): exit=1 failed=1 nodes=['tests/ui_server/test_command_dispatch.py::TestInjectionDispatchEffects::test_a_bad_text_is_400_and_a_bad_option_is_400_with_no_control_file_written']
m5_dispatch_injection_passes_after_unresolved (packages/orchestration/ui_server.py): exit=1 failed=1 nodes=['tests/ui_server/test_command_dispatch.py::TestInjectionDispatchEffects::test_after_by_the_entry_id_reaches_the_drafts_depends_on_as_the_planned_id']
m6_dispatch_injection_names_the_actor_cli (packages/orchestration/ui_server.py): exit=1 failed=1 nodes=['tests/ui_server/test_command_dispatch.py::TestInjectionDispatchEffects::test_a_drafted_injection_answers_200_and_writes_one_draft_file_naming_the_actor']
m7_the_injection_branch_answers_a_refusal_with_200 (packages/orchestration/ui_server.py): exit=1 failed=2 nodes=['tests/ui_server/test_command_dispatch.py::TestInjectionDispatchEffects::test_confirm_answers_200_with_one_confirmation_file_and_a_second_is_409', 'tests/ui_server/test_command_dispatch.py::TestInjectionDispatchEffects::test_a_terminal_job_is_409_naming_job_terminal']
m8_the_fold_writes_no_event_for_an_applied_record (packages/orchestration/pingpong_job.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection_runner.py::TestTaskInjectedEvent::test_an_applied_fold_writes_one_event_naming_the_new_entrys_task_id', 'tests/orchestration/test_task_injection_runner.py::TestTaskInjectedEvent::test_a_second_run_writes_no_further_event']
m9_the_fold_writes_the_event_for_an_inert_record_with_outcome_applied (packages/orchestration/pingpong_job.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection_runner.py::TestTaskInjectedEvent::test_an_inert_fold_writes_one_event_naming_its_reason']
restored byte-identical: True (apps/cli/commands/job_inject_cmd.py)
restored byte-identical: True (packages/orchestration/task_injection.py)
restored byte-identical: True (packages/orchestration/ui_server.py)
restored byte-identical: True (packages/orchestration/pingpong_job.py)
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 9 mutations red with at least one failing node each; no mutation
stayed green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r5-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 65 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r5-block.md`, at `6e2a9b37a`) vs
  `.remedy-wt/f028-r5/block.md`: byte-identical, sha256
  `57a984efa3ba0fa1788bd2a33ddc1d63c17344894216589a6dc52141e84a275a` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r5-plan.md`, at `6e2a9b37a`) vs
  `.remedy-wt/f028-r5-payloads/plan.md`: byte-identical, sha256
  `ea6ff390bddb5c46d3030febe9f9ea4ae399426aaf1d04cbe09c118419750265` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r5-records.diff`, at
  `6e2a9b37a`) vs `.remedy-wt/f028-r5-payloads/records.diff`:
  byte-identical, sha256
  `074a99b06ed1a9a9b18e8f1e4cc924d29a5c45a49e76fb0093f741b749f9e8c2` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production code (`task_injection.py`, `job_inject_cmd.py`,
`ui_server.py`, `command_catalog.py`, `pingpong_job.py`, `event_names.py`,
`humanizeCatalog.ts`), its tests (four files) and the mutation tool
(`f028-r5-mutations.py`) are the WORKER's own authored code against the
block's specification S1–S5, not reviewer-authored text, so no fidelity
comparison applies to them.

## Deviations & assumptions

1. **C6 split into C6 and C6b (constraint 2).** The block's bundle lists
   one C6 carrying "the four test files of THE TESTS and
   `.agent/authored/f028-r5-mutations.py`". Measured before committing:
   the four test files alone total 373 insertions; the mutation tool alone
   totals 262. Combined (635) would exceed the 500-line cap, so this round
   split the commit into C6 (the four test files, 373 insertions, subject
   "F028 R5 C6: test the door's injection commands, the event and the
   resolver") and C6b (the tool alone, 262 insertions, subject "F028 R5
   C6b: add the round 5 mutation tool"), per constraint 2's own instruction
   that a commit reaching 500 is split into parts with their own subjects,
   each leaving the selection of G4 green. G4 was run once, after both
   parts landed (C6b is HEAD for every gate below G3), and reads green;
   this is declared here as constraint 2 orders, in addition to the two
   per-commit tables above already showing the split.
2. **`resolve_after_ref`'s placement in `task_injection.py`.** The block
   names no exact line for the new function; it was placed directly after
   `injection_call_fn` (DECISION F028 D4 (3)'s other shared door/CLI
   helper), grouping the three functions the door and the command line
   both read under one comment block, rather than beside the (unrelated)
   S5 placement logic.
3. **Event field naming in `_fold_task_injections`.** S5 orders
   `log("task_injected", outcome=..., task_id=..., draft_id=...,
   planned_id=..., basis=..., actor=..., confirmed_unseen=...)`. The
   confirmed-injection record's own `task["id"]` is read as `planned_id`
   for BOTH outcomes (applied and inert) — the planned id that WOULD have
   joined the plan, since a confirmed record's `task` dict is fixed before
   the apply is attempted and does not change between the two outcomes.
   For an applied record, `task_id` is `apply_injection_to_job`'s returned
   `applied["task_id"]` (the fresh `TaskEntry`'s own runtime id, per
   `confirm_task_injection`'s own docstring distinguishing the two); for an
   inert record it is the empty string per S5's own text. `RunLogWriter
   .log`'s `outcome` and `task_id` are its own named keyword parameters;
   `draft_id`, `planned_id`, `basis`, `actor`, `confirmed_unseen` and (for
   inert only) `reason` fall through to `**metadata`, exactly as the
   existing `_write_task_vetoed_event` in `task_veto.py` passes `actor`
   the same way.
4. **Test-file/payload line/byte/sha256 measurements, the base
   `--collect-only` counts and the mutation-occurrence checks** were done
   with small Python helper scripts written to `.remedy-wt/f028-r5-worker/`
   and run via `python3 <script>` rather than shell pipelines the sandbox
   denies (heredocs containing a brace-with-quote, `for` loops with simple
   variable expansion, command substitution) — per the block's own "THIS
   SANDBOX REFUSES SHAPES" section. The base node counts were measured in
   a disposable worktree at `6814c686` (`git worktree add --detach
   .remedy-wt/f028-r5-base-count 6814c686`), removed immediately after use.

No test went red unexpectedly, no reviewer payload was edited or retyped,
no gate was skipped, and every G5 mutation was caught on the first run —
no fix-up test was required.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | repairs R-1078 |
| C4 | done | |
| C5 | done | |
| C6 | deviated | split into C6 (four test files, 373 insertions) and C6b (mutation tool, 262 insertions) under constraint 2 — combined would have reached 635 insertions; declared in Deviations §1 |
| C6b | done | see C6's note |
| C7 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | 1514 passed, 7 skipped, exit 0; the 14-node delta from the reviewer's 1500 baseline fully accounted for across the five edited test files |
| G5 | done | all 9 mutations caught, both controls clean, all four files restored byte-identical |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| R-1078 | done | repaired in C3 (`6489fdedb`); test in C6 (`e17f1ce45`); red-proved by G5's m1 |
| S1 | done | R-1078's repair in `job_inject_cmd.py` |
| S2 | done | `resolve_after_ref` in `task_injection.py` |
| S3 | done | the three door constants, `_handle_command_submission`'s branch, `_dispatch_injection`, `_read_command_payload`'s checks, the catalog registration |
| S4 | done | the sorted-ids literal, `DOOR_METHODS`, `ALLOWED_IMPORTS`, the three new branches and docstring sentences in `test_command_channel.py` |
| S5 | done | `_fold_task_injections`'s event write, `EVENT_NAMES`, `STREAM_EVENT_CATALOG` |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 5,
then the send module, the Add Task sheet and the provenance chip. Open
findings (by `open_finding_ids` at this round's head): 1 (R-1078, its
repair awaiting review). Operator questions open: 0.
