# Handoff — F038, round 2 (book round 1 and R-1091's resolution, record DECISION F038 D3,
rewrite the spec's two scope paragraphs, and land T001's project scope and the node scope's
prompt-trace items)

## Session

SESSION 1 of feature F038 · round 2 · rounds so far 2. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, both
payloads and the records diff before writing anything, read every named source file whole
(`chat_evidence.py`, `test_chat_evidence.py`, `RemyProject`, `list_job_plans_safe`,
`list_decisions`/`open_decisions`, `detect_patterns`/`ProjectPattern`,
`build_index`/`proposed_feature`/`RoadmapGrammarError`, `build_job_digest`,
`list_missions_safe`/`create_mission`, the dossier state functions and `MissionDossier`/
`DossierItem`, `query_cost`/`CostRow`/`CallRecord`/`record_call`, `run_dir` and
`PromptTraceEntry`) before touching it, verified every payload and every committed copy for
real, applied `records.diff`, wrote and ran the new project-scope code and its tests against
real writers, split C4 under the 500-insertion cap, wrote a fresh 11-mutation red-proof tool
and ran it for real in a disposable worktree, ran the pinned serial test selection and the
integrity check to completion, and ran every gate (G1–G5) for real before writing this
handback.

## Range

Review of `733d5db69..HEAD` (`HEAD` is this handback's own commit, `F038 R2 C5`, on
`feature/f038-grounded-chat`).

## Commits

### 15afcb121 F038 R2 C1a: copy round 2 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r2-block.md | 327/0 | copy of the block, verified line count (327) and sha256 |
| .agent/authored/f038-r2-plan.md | 30/0 | copy of the reviewer's plan.md payload |

357 insertions total, exactly the block's own note: 327-line block + 30, under the 500-line cap.

### 6e2abcb14 F038 R2 C1b: copy round 2 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r2-records.diff | 105/0 | copy of the reviewer's records.diff payload |

Measured 105 insertions, exactly the block's expected reading.

### 2b5185aad F038 R2 C2: book round 1 and R-1091's resolution, record D3, update the spec's sets
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 51/0 | `git apply records.diff` — appends DECISION F038 D3 |
| .agent/live_review.md | 4/0 | `git apply records.diff` — books round 1's Gate entry and R-1091's Done paragraph |
| .agent/plan.md | 8/11 | rewritten to plan.md payload by `shutil.copyfile` |
| docs/roadmap/design/grounded-chat-spec.md | 15/8 | `git apply records.diff` — rewrites section 2's two scope paragraphs |

Measured numstat matches the block's table exactly: 51/0, 4/0, 8/11, 15/8.

### e2c2e67cf F038 R2 C3: collect the project scope and the node scope's prompt traces
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_evidence.py | 285/13 | S1–S5: both scopes named, twelve anchor kinds, the prompt-trace collector wired into the node scope, and the project-scope collector (record, roadmap, decisions, patterns, dossiers, ledger, jobs) plus `project_evidence_set` |
| tests/test_no_orphan_modules.py | 2/2 | S6: the `ALLOWED_UNWIRED` reason now names "the node and project scopes" |

No insertion count was expected by the block for C3; measured 287 total, under the cap.

### dbde58322 F038 R2 C4a: test the project scope and the prompt items
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_evidence.py | 306/8 | renamed the eleven/eight-item tests to twelve/nine, widened the anchor-kind and scope-refusal assertions, and added the eight NEW TESTS the block orders (prompt trace + junk lines, trace_empty, empty project, roadmap grammar (4 sub-cases), linked-job filtering/decision-grouping/pattern, mission dossier, ledger measured/unmeasured, `project_evidence_set` determinism) |

No insertion count was expected by the block for C4; measured 306 for this half.

### 80a0e160b F038 R2 C4b: add the mutation red-proof tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r2-mutations.py | 219/0 | the G5 tool: 11 mutations (n1–n11) against `chat_evidence.py`, run against `tests/orchestration/test_chat_evidence.py` only |

No insertion count was expected by the block for C4; measured 219 for this half. C4a + C4b =
525 insertions, which is why constraint 2 split it (declared below).

### <C5-sha> F038 R2 C5: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f038-r2-mut 80a0e160b` — added the disposable G5
  worktree at C4b. Outcome: `Preparing worktree (detached HEAD 80a0e160b)`.
- `python3 -B .agent/authored/f038-r2-mutations.py .../f038-r2-mut` — ran the 11-mutation
  red-proof tool. Outcome: all 11 caught, both controls exit 0, `restored byte-identical: True`
  on every mutation, `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove --force .remedy-wt/f038-r2-mut` — removed the G5 worktree. Outcome:
  exit 0.
- `git worktree prune` — outcome: exit 0.
- `git push origin feature/f038-grounded-chat` — reported under G6 below (run after this file's
  own commit, so its outcome is reported there rather than tabled here, per the handback
  template's self-reference exception).

## Verification

### BEFORE ANYTHING ELSE
1. `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, exit 2. Absent.
2. `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty, exit 0.
   `git branch --show-current` → `feature/f038-grounded-chat`. `git log --oneline -1` →
   `733d5db69 F038 R1 C6: rewrite handoff for round 1`.
3. Block bytes: measured line count 327, sha256
   `5746845efe51ee6afed981c86c4637ca1e700ba15e6dcc847ff290aa47f0a1e2`; both equal the two
   readings the delegation message stated.
4. `git worktree list | wc -l` → `64`.

### PAYLOADS
| file | measured lines | measured bytes | measured sha256 | matches table |
|---|---|---|---|---|
| records.diff | 105 | 13552 | f8c89e25ef3e44c9dee183e9ac0337478aada610d31c7b59f6c110eea6d072ea | yes |
| plan.md | 30 | 992 | bcb8cca73a353e29155d1d7eebcf64dab77b0504e644a13f4ddb3052095c2219 | yes |

### G1 TRANSPORT
`git apply --check .remedy-wt/f038-r2-payloads/records.diff` → exit 0. Real `git apply` → exit 0.
Each `.agent/authored/f038-r2-*` copy compared byte-for-byte against its source, read back with
`git show <commit>:<path>`:
- `15afcb121:.agent/authored/f038-r2-block.md` == `.remedy-wt/f038-r2/block.md` — MATCH (24675 bytes both).
- `15afcb121:.agent/authored/f038-r2-plan.md` == `.remedy-wt/f038-r2-payloads/plan.md` — MATCH (992 bytes both).
- `6e2abcb14:.agent/authored/f038-r2-records.diff` == `.remedy-wt/f038-r2-payloads/records.diff` — MATCH (13552 bytes both).

### G2 THE RECORDS
sha256 of each file read with `git show 2b5185aad:<path>`:
| path | bytes | sha256 | matches reviewer's reading |
|---|---|---|---|
| .agent/decisions.md | 2382330 | d4b172c0f51fe848cd385753ebb4044a40353e53ac1e1c0db015429ebc5c62e2 | yes |
| .agent/live_review.md | 312479 | 2092ebf2ecece86924a54d63527c96efd2aa62b2b8244eaa493a988352b9ec2b | yes |
| docs/roadmap/design/grounded-chat-spec.md | 5261 | d4075ecf42cbd4c32cc327c61ab65fccba37cee1928f1da7ef8b65b62acf6f9e | yes |
| .agent/plan.md | 992 | bcb8cca73a353e29155d1d7eebcf64dab77b0504e644a13f4ddb3052095c2219 | yes |

`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s text:
at `733d5db69` → `['R-1091']`; at `2b5185aad` → `[]`. Both match the reviewer's stated readings.

`git diff --name-only 6e2abcb14 2b5185aad` →
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
docs/roadmap/design/grounded-chat-spec.md
```
Names exactly the four paths of the table above.

### G3 THE CODE
`python3 -m ruff check packages/orchestration/chat_evidence.py
tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py` at C4b → `All checks
passed!`, exit 0.

Quoted from `git show e2c2e67cf` (C3):

Module docstring:
```
"""F038 T001 — the grounded chat's evidence: the item, its problems, the composer
that keeps an ordered prefix under the token cap, the node scope's collector of one
task's own records and its prompt trace, and the project scope's collector of one
registry project's own records (DECISION F038 D1, DECISION F038 D3).

Remedy deliberately does not let a scope's evidence reach past its own records: the
node scope answers only from one task's own record, its own rounds, its own prompt
trace, its own diff and its own run-log events — never another task's, and never the
whole job's; the project scope answers only from one registered project's own record,
its linked jobs and its own missions — never another project's.
"""
```

The whole prompt-trace function of S2:
```python
def _prompt_trace_items(task: Any, task_id: str) -> list[ChatEvidenceItem]:
    """S2: the task's own prompt trace, one item per entry — metadata only, never
    the prompt text. Directly after the rounds and before the diff."""
    run_id = getattr(task, "run_id", None)
    if not isinstance(run_id, str) or not _RUN_ID_RE.match(run_id):
        return [
            make_chat_item(
                "node", task_id, "Prompt trace: not recorded (no_run_recorded)"
            )
        ]
    trace_path = run_dir(run_id) / "prompt_trace.jsonl"
    try:
        text = trace_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [
            make_chat_item("node", task_id, "Prompt trace: not recorded (trace_missing)")
        ]
    except (OSError, UnicodeDecodeError):
        return [
            make_chat_item(
                "node", task_id, "Prompt trace: not recorded (trace_unreadable)"
            )
        ]

    items: list[ChatEvidenceItem] = []
    for line in text.splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(entry, dict):
            continue
        round_number = entry.get("round")
        role = entry.get("role") or CHAT_NOT_RECORDED
        prompt_kind = entry.get("prompt_kind") or CHAT_NOT_RECORDED
        provider = entry.get("provider") or CHAT_NOT_RECORDED
        configured_model = entry.get("configured_model") or CHAT_NOT_RECORDED
        tokens_estimated = entry.get("prompt_tokens_estimated")
        text_line = (
            f"Prompt for round {round_number}, {role} ({prompt_kind}): "
            f"{tokens_estimated} tokens estimated; provider {provider}; "
            f"model {configured_model}"
        )
        items.append(
            make_chat_item("prompt", f"{task_id}#{round_number}/{role}", text_line)
        )
    if not items:
        return [
            make_chat_item("node", task_id, "Prompt trace: not recorded (trace_empty)")
        ]
    return items
```

The whole of `collect_project_evidence`:
```python
def collect_project_evidence(project: Any) -> list[ChatEvidenceItem]:
    """One registry project's own evidence (DECISION F038 D3): its record, its
    repository's roadmap position, its linked jobs' open decisions and patterns,
    its missions' dossiers, its token ledger's totals and one digest per linked
    job, newest first.
    """
    pid = str(project.id)
    all_jobs, _degraded, _skipped = list_job_plans_safe()
    linked_ids = set(project.job_ids)
    jobs = [job for job in all_jobs if str(job.job_id) in linked_ids]
    events_by_job_id = {
        str(job.job_id): load_run_events(resolve_data_root(), str(job.job_id))
        for job in jobs
    }
    return [
        _project_record_item(project, pid, len(jobs)),
        *_project_roadmap_items(project, pid),
        *_project_decision_items(jobs, events_by_job_id),
        *_project_pattern_items(jobs, events_by_job_id),
        *_project_dossier_items(project, pid),
        *_project_ledger_items(pid),
        *_project_job_items(jobs, pid, events_by_job_id),
    ]
```

### G4 THE TESTS
Serial run, at C4b, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -4; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
Output:
```
764 passed, 6 skipped in 89.84s (0:01:29)
REAL_EXIT=0
```
The six skips are the F252 quarantine in `tests/regression/test_named_bugs.py` (five `- ` lines
plus one collapsed in `tail -4`; all six read `D3 quarantine (F252)`), matching the reviewer's
baseline reading exactly.

Node count of `tests/orchestration/test_chat_evidence.py` by `--collect-only -q`:
- at `733d5db69`: 14 tests (measured by extracting `git show 733d5db69:tests/orchestration/test_chat_evidence.py` into a scratch file and collecting it).
- at C4b: 22 tests.
Difference: +8 nodes, exactly the eight NEW TESTS this round adds. 756 (reviewer's baseline) + 8
= 764, accounting for the whole difference; no other test file's collection changed.

`python3 -m apps.cli.main integrity check --json`:
```json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0 — R-1091 is resolved at C2, exit 0.

### G5 THE RED PROOFS
`git worktree add --detach .remedy-wt/f038-r2-mut 80a0e160b` → exit 0.
`python3 -B .agent/authored/f038-r2-mutations.py .../.remedy-wt/f038-r2-mut` → whole output:
```
control (before): exit=0 failed=0 nodes=[]
n1 a prompt item's text carries the entry's prompt_text_redacted: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_prompt_trace_with_junk_lines_yields_exactly_the_recorded_entries'] caught=True
  restored byte-identical: True
n2 a trace line that parses to something not a dict is not skipped: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_prompt_trace_with_junk_lines_yields_exactly_the_recorded_entries'] caught=True
  restored byte-identical: True
n3 the project scope takes every job, linked or not: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_project_scope_filters_to_linked_jobs_and_groups_their_decisions'] caught=True
  restored byte-identical: True
n4 the linked jobs come oldest first: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_project_scope_filters_to_linked_jobs_and_groups_their_decisions'] caught=True
  restored byte-identical: True
n5 a decision's ref is its id alone, without its job: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_project_scope_filters_to_linked_jobs_and_groups_their_decisions'] caught=True
  restored byte-identical: True
n6 the roadmap is read from Remedy's own repository instead of the project's: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_the_roadmap_position_reads_status_by_its_own_grammar'] caught=True
  restored byte-identical: True
n7 an in-progress feature reads as the next open feature: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_the_roadmap_position_reads_status_by_its_own_grammar'] caught=True
  restored byte-identical: True
n8 a resolved dossier risk is listed: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_missions_dossier_yields_its_goal_next_step_and_open_risks'] caught=True
  restored byte-identical: True
n9 an unmeasured ledger figure reads 0: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_the_token_ledger_reads_measured_figures_and_names_the_unmeasured'] caught=True
  restored byte-identical: True
n10 the job items come before the decisions: exit=1 failed=2 nodes=['tests/orchestration/test_chat_evidence.py::test_a_project_with_nothing_linked_yields_exactly_the_five_items', 'tests/orchestration/test_chat_evidence.py::test_project_scope_filters_to_linked_jobs_and_groups_their_decisions'] caught=True
  restored byte-identical: True
n11 the prompt items come after the diff: exit=1 failed=2 nodes=['tests/orchestration/test_chat_evidence.py::test_a_fully_recorded_task_yields_exactly_the_twelve_items_in_order', 'tests/orchestration/test_chat_evidence.py::test_a_task_with_nothing_recorded_yields_exactly_the_nine_items'] caught=True
  restored byte-identical: True
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation caught with at least one failing node; both unmutated controls read exit 0; every
mutation restored byte-identical. No mutation stayed green, so no post-hoc test addition was
needed (constraint 4's "add the test that catches it" branch did not fire — see Deviations for
the one test strengthened proactively, before this run, to make n10 catchable).
`git worktree remove --force .remedy-wt/f038-r2-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list | wc -l` → `64`.

## Authored-text proofs

- `.agent/authored/f038-r2-block.md` (added at `15afcb121`) == `.remedy-wt/f038-r2/block.md`,
  byte for byte (24675 bytes both). MATCH.
- `.agent/authored/f038-r2-plan.md` (added at `15afcb121`) == `.remedy-wt/f038-r2-payloads/plan.md`,
  byte for byte (992 bytes both). MATCH.
- `.agent/authored/f038-r2-records.diff` (added at `6e2abcb14`) ==
  `.remedy-wt/f038-r2-payloads/records.diff`, byte for byte (13552 bytes both). MATCH.
- `.agent/plan.md` after C2 (`2b5185aad`) == `.remedy-wt/f038-r2-payloads/plan.md`, byte for byte
  (sha256 `bcb8cca73a35...2219` both, confirmed under G2). MATCH.
- `records.diff` applied via `git apply` (not retyped); `.agent/decisions.md`,
  `.agent/live_review.md` and `docs/roadmap/design/grounded-chat-spec.md` after C2 match the
  reviewer's stated sha256 exactly (G2 table above). MATCH.

## Deviations & assumptions

1. **C4 split into C4a/C4b (constraint 2).** The block's BUNDLE names one commit "C4 — THE TESTS
   AND THE TOOL". Staged together, `tests/orchestration/test_chat_evidence.py` (306 insertions)
   and `.agent/authored/f038-r2-mutations.py` (219 insertions) total 525 insertions, at/over the
   500-insertion cap. Split into `C4a` (tests, 306 insertions) and `C4b` (the tool, 219
   insertions), each under the cap, with subjects `F038 R2 C4a: test the project scope and the
   prompt items` and `F038 R2 C4b: add the mutation red-proof tool`, both declaring the split in
   their commit body. This is the split constraint 2 itself anticipates ("C4a and C4b").
2. **A test this round wrote was corrected before any commit (constraint 4).**
   `test_project_scope_filters_to_linked_jobs_and_groups_their_decisions` was first written
   assuming a linked job's one failing `test_run_completed` event derives exactly one
   `HumanDecision` (the `tf:` test-failure branch of `decision_queue.list_decisions`). Measured
   against the real writer before committing: (a) a job whose `metadata` carries no
   `target_repo` also derives a `sr:derived_no_repo` stop-reason decision
   (`stop_reasons.derive_stop_reasons`), and (b) even with `target_repo` set, the same failing
   test event ALSO derives a `sr:derived_test_fail` stop-reason decision from the same module's
   test-failure branch — two decisions per job, not one. Fixed `_make_project_job`'s default
   metadata to `{"target_repo": "/tmp/repo"}` (avoiding (a), matching the codebase's own
   `test_decision_inbox.py` fixture convention) and widened the assertion to expect both `sr:`
   and `tf:` decisions per job, in that order. Nothing wrong was ever committed — this was
   corrected during authoring, before C4a.
3. **One test assertion added proactively, not after an observed green mutation.** While
   designing mutation n10 ("the job items come before the decisions"), I noticed
   `test_project_scope_filters_to_linked_jobs_and_groups_their_decisions` only checked the
   `job` and `decision` kind sublists independently, which would not catch a reordering of the
   two groups relative to each other. Added an explicit order assertion (last decision index <
   first job index) to that same test before ever running the mutation tool, so n10 was caught
   on its first and only run (see G5 output — no mutation read green at any point, so
   constraint 4's "add the test that catches it" branch, which presumes an observed green
   mutation, never fired in the literal sense; this is declared regardless, since it is a test
   addition made specifically to secure a mutation's catch).
4. No payload was repaired, edited or retyped. No existing test outside the five named in the
   block was touched. No file outside the round's tracked path set (constraint 3) was touched —
   confirmed by `git diff --name-only 733d5db69` at the branch tip (see below).

## Tracked path set (constraint 3)

`git diff --name-only 733d5db69` at the branch tip after C5:
```
.agent/authored/f038-r2-block.md
.agent/authored/f038-r2-mutations.py
.agent/authored/f038-r2-plan.md
.agent/authored/f038-r2-records.diff
.agent/decisions.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
docs/roadmap/design/grounded-chat-spec.md
packages/orchestration/chat_evidence.py
tests/orchestration/test_chat_evidence.py
tests/test_no_orphan_modules.py
```
Exactly the block's constraint-3 set, no more and no less.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1 (STOP check) | done | |
| BEFORE ANYTHING ELSE 2 (repo state) | done | |
| BEFORE ANYTHING ELSE 3 (block bytes) | done | |
| BEFORE ANYTHING ELSE 4 (worktree count) | done | |
| PAYLOADS verification | done | |
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | deviated | split into C4a and C4b under the 500-insertion cap (constraint 2) |
| C5 | done | this commit |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | all 11 mutations caught first run |
| G6 TREE AND PUSH | done | reported in the round reply, not tabled here (cannot precede this commit) |

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk. (2) The
review of round 2. (3) T001's grounded answer: the citation check, the unsupported marker and
the canary suite. Open-findings count: 0. Operator-questions count: 1 (Q6, empty paydown waits
one feature).
