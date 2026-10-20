# Handback — F312 round 3 (book round 2, DECISION F312 D4, the answer path, R-1378)

## Session

SESSION 1 of feature F312 · round 3 · rounds so far 3

Context self-assessment: the session verified every prepared file's digest with a Python sha256
reader before use, kept C2's code and C3's tests in separate commits exactly as the block ordered,
hit no pre-existing red test, and all six gates passed on the first run.

State block:
Feature F312 (`[~]` in STATUS since round 1's C1), branch `feature/f312-scope-kinds`, base
`38bfa1c37` (round 2's handback). Head: this commit (C4), after C1 to C3.
Fortschritt: ~85 % (T001 to T003 and the answer path landed · the closure open) — Schätzung

## Range

Review of `38bfa1c37`..HEAD (C1 to C3 below, then this commit, C4, which also carries this
handback).

## Commits

### f678daca6 F312 R3 C1: book round 2, register R-1378, the D3 addendum and DECISION F312 D4, the plan
178 insertions, 11 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f312-r3.md` | +151 (new file) | byte copy of the block |
| `.agent/decisions.md` | +14 | byte copy of the prepared decisions (the DECISION F312 D3 addendum and DECISION F312 D4 appended) |
| `.agent/live_review.md` | +4 | byte copy of the prepared ledger (round 2's booking, R-1378 registered) |
| `.agent/plan.md` | +8/-11 | byte copy of the prepared plan |
| `.agent/prose_slips.md` | +1 | byte copy of the prepared slips (one line appended) |

### 04d5253ac F312 R3 C2: an answer to the scope question makes the named files the job's tasks
65 insertions, 5 deletions.
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/do-run-v1.md` | +3 | the answer-path sentences inserted right after their anchor |
| `packages/orchestration/do_sequence.py` | +1/-1 | `_first_pass_task_plan` hands `prompt_traces` on to `second_pass_task_plan` |
| `packages/orchestration/escalation.py` | +2 | `answer_task_decision` hands the record to `scope_question.apply_scope_answer` after `_record_answer_on_task`, return value unchanged |
| `packages/orchestration/scope_question.py` | +59/-4 | `apply_scope_answer` (DECISION F312 D4); `second_pass_task_plan` and `raise_scope_question` gain `prompt_traces`, written to the job's `prompt_trace.jsonl` before `ScopeQuestionRaised` (R-1378) |

### e05af1b12 F312 R3 C3: the answer path and the question's traces, tested
225 insertions (no deletions).
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_scope_question.py` | +163 (extended) | `apply_scope_answer` plans the job with both names as tasks in order (direct and through `answer_task_decision`); junk/repeats keep only the one safe name; an answer naming no usable file leaves the job stopped; a task decision on an unrelated job is unchanged by the hook; R-1378's prompt trace holds at least two `task_plan` rows |
| `tests/regression/test_lab_orders_20261020.py` | +62 (extended) | the second lab order's stopped question job answered and resumed through the CLI door (`decision resolve` then `job resume --yes`, fake builder chain, no real model or network) |

### this commit (C4) F312 R3 C4: handback
1 file.
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file (a handoff cannot table its own commit) |

## External actions

The push is run after this commit, so its outcome is reported in the final reply only. Before this
commit: no push, no `gh` command besides the read-only `gh pr list` of the Open PR Gate (empty, no
open PR), no pull request opened this round.

## Verification

1. Gate 1: `git status --porcelain` — empty. `python3 .remedy-wt/f312-r3/prep/verify.py .`:
   ```
   True	f678daca6 single parent equal to the commit before it
   True	04d5253ac single parent equal to the commit before it
   True	e05af1b12 single parent equal to the commit before it
   True	every commit carries an F312 R3 Cn subject: 3 of 3
   True	C1 paths exactly ['.agent/authored/f312-r3.md', '.agent/decisions.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md']: ['.agent/authored/f312-r3.md', '.agent/decisions.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md']
   True	C2 paths inside its set: ['docs/guides/do-run-v1.md', 'packages/orchestration/do_sequence.py', 'packages/orchestration/escalation.py', 'packages/orchestration/scope_question.py']
   True	C3 paths all under tests/: ['tests/orchestration/test_scope_question.py', 'tests/regression/test_lab_orders_20261020.py']
   absent	C4
   True	C1 .agent/authored/f312-r3.md equals block.md
   True	C1 .agent/live_review.md equals dry-live_review.md
   True	C1 .agent/decisions.md equals dry-decisions.md
   True	C1 .agent/prose_slips.md equals dry-prose_slips.md
   True	C1 .agent/plan.md equals dry-plan.md
   True	C2 scope_question.py defines apply_scope_answer once
   True	C2 answer_task_decision hands the record to apply_scope_answer
   True	C2 the question's job writes its prompt traces (R-1378)
   True	C2 do_sequence.py stays under 1000 lines: 982
   True	C2 the guide sentences stand right after their anchor
   True	C2 the guide is the base plus the sentences and nothing else
   True	C2 leaves order_scope.py byte-identical (do not touch)
   ALL True
   ```
2. Gate 2: `python3 -m ruff check` over every Python file C2 and C3 touched
   (`packages/orchestration/scope_question.py`, `packages/orchestration/escalation.py`,
   `packages/orchestration/do_sequence.py`, `tests/orchestration/test_scope_question.py`,
   `tests/regression/test_lab_orders_20261020.py`): exit 0, `All checks passed!`.
3. Gate 3: `python3 .remedy-wt/f312-r3/prep/run_selection.py . .remedy-wt/f312-r3-worker/selection-output.txt`:
   `paths 85`, `exit 0`, `3879 passed, 2 skipped in 58.64s`; no FAILED or ERROR line, no
   "process(es) behind" line. SKIPPED lines:
   - `SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.`
   - `SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access`
4. Gate 4: `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing
   check `high_blockers_open`: `"13 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345,
   R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362, R-1369"` — the thirteen of DECISION
   F310 D7, no other.
5. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `89`.
6. Gate 6: `python3 -c "from pathlib import Path; print(len(Path('packages/orchestration/do_sequence.py').read_text().splitlines()))"` — `982`.

## Authored-text proofs

Byte copy of `block.md` to `.agent/authored/f312-r3.md` at C1, proved by a sha256 equality in the
copy script (151 lines, sha256 `deef29f803659a68ed1e9732826a3d5fa0504f38dfcde436810ec812f5f1a5fb`,
matching the prompt's stated digest and line count exactly) and confirmed again by `verify.py`'s
`C1 .agent/authored/f312-r3.md equals block.md` line above. The other four C1 copies
(`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`) are
prepared-file byte copies, each proved equal by sha256 in the copy script and again by `verify.py`.
No reviewer amendment was issued this round, so no further authored-text copy applies.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | f678daca6 |
| C2 | done | 04d5253ac |
| C3 | done | e05af1b12 |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 3879 passed, 2 skipped |
| Gate 4 | done | fail_count 1 on the standing thirteen |
| Gate 5 | done | 89 |
| Gate 6 | done | 982 |
| C4 | done | this commit |

## Deviations & assumptions

- None of C1 to C3 was amended; each landed on its first attempt with no pre-existing test going
  red.
- DECISION F312 D4 and the block's C2.1 both state that an applied answer clears `job.task_plan`,
  `job.stop_reason` and `job.finished_at`; the block's own words for all three are "becomes None" /
  "None", so `apply_scope_answer` sets the Python value `None` on `stop_reason` and `finished_at`
  (both otherwise typed and conventionally emptied to `""` elsewhere in `JobPlan`, per the class's
  own "absent is spelled `""` for a string" comment, which documents only the eight fields F272 T002
  added and does not cover these two older F011 fields). Followed literally as written; nothing in
  gate 3's selection reads either field as a string afterward (`self_use_findings.py`'s
  `stop_reason.strip()` reader is outside the selection). Flagging this for the reviewer rather than
  silently choosing `""` to match the sibling fields' convention.
- `remedy job resume` on the freshly-planned job built by `apply_scope_answer` carries no persisted
  `execution_config` (nothing ran it through the ping-pong engine yet), so it takes the single-pass
  local runner (`_cmd_job_run_cycles` with the F046 rollout default of one cycle, which defers to
  `_cmd_run_next_task_local`), not a builder-provider CLI flag — `job resume` takes no such flag.
  C3.4's CLI-door test fakes that runner's builder chain exactly as
  `tests/test_run_log_cli.py::TestRunNextTaskLocalSuccess` fakes it (`OllamaBuilder`, `run_next_task`,
  `annotate_task_result`, `materialize_task_output`, `verify_task_output`, `finalize_task`), so no
  real model or network is reached; confirmed `job resume` does not refuse the freshly-planned job
  before writing the test this way.
- `docs/README.md` is untouched: `docs/guides/do-run-v1.md` already carries its index entry from an
  earlier feature; this round only extends its existing content, neither adding nor renaming a doc.
- The records of the operator's failed lab job were not read: the data root is not readable in this
  session, per DECISION F312 D1; the finding's text and the code are the evidence, as the block and
  the DECISION both state.

## For the operator, in plain sentences

Answering the question Remedy asks after refusing a plan twice now actually does something: naming
the files you meant, separated by commas, turns those files into the job's work items and lets the
job run immediately, with no further planning call spent. Naming nothing useful — a path outside
the project, or nothing at all — leaves the job exactly as it was, so the request can be given again
with its files spelled out. The two planning attempts a job spent before it had to ask are no longer
thrown away; they are kept beside the job so a person reviewing it later can see what was tried.
Both ways of answering were proven end to end: directly in code, and through the actual command line
a person types, including the follow-up command that starts the job's work.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`); the Open PR Gate; book round 3's verdict in the next
round's first commit; the closure's integration-gate round.
Operator questions open: 1. Open findings: 89 (gate 5, `open_finding_ids`, read at C1's ledger).
