# Handback — amend1014-do-golden-path-now: the `remedy do` golden path is repaired; the real acceptance run reached the builder and stopped on a provider limit

## Session

Operator amendment amend1014-do-golden-path-now · branch `feature/do-golden-path` (from `main` at
`e688b30f3`) · code commits C1 to C10, `9e88a356e`..`b6741dfbb` · the pull request is open and
**not merged**. The interrupted F078 feature was already committed and pushed on
`feature/f078-autonomy-levels` (clean tree, `9d3187143`, no pull request); nothing of it was
reset, restored, stashed or touched. The Open PR Gate found no open pull request. `.agent/STOP`
(the operator's stop file) is untracked and was left alone.

## State: what the command does now

`remedy do "<the incident order>" --repo .` on a committed one-file repository, with no flag:
first output at 0.34 s, deterministic study, the one-milestone plan with a deterministic DoD, one
job and one task for `README.md`, **zero planning or study provider calls**, the cockpit URL
printed before the builder starts, progress lines on stderr with a heartbeat every ten seconds, a
stop before apply, the target untouched. `--yes` of `do` is deleted; `--run-unattended` replaces it.

## Real acceptance run — the honest result

Command, exactly the human one apart from the path, at commit `b6741dfbb`, a fresh committed
repository holding only `README.md` (`# Test\n`), isolated data root, the default configuration
(`builder`, `reviewer`, `planner` and `study` all `ollama`, model `muse-glimmer:latest`):

```
remedy do "Add one concise project-description paragraph below the existing heading in README.md. Change no other files." --repo .
```

| Measure | Result |
|---|---|
| Time to first visible output | 0.341 s after launch; the first provider call can happen only after `run started`, at 1.06 s |
| Phase durations | init 0.0 s · study 0.0 s · plan 0.1 s · shape 0.0 s · ui 0.5 s · run 135.7 s |
| Resolved provider per call | builder `ollama` ×3, reviewer `ollama` ×3 (rounds 1 to 3; `provider_evidence.json`, `prompt_trace.jsonl`) |
| Provider calls by role | planning 0 · study 0 · intake 0 · DoD 0 · builder 3 · reviewer 3. No mission-level prompt trace exists. |
| Jobs and tasks | 1 job, 1 task, deliverable `README.md` (no synthetic inspection task) |
| Cockpit | URL printed at 1.06 s after launch, 6 ms before `run started`; HTTP 200 on the URL after the run failed (checked on the first run); `remedy ui stop` clean |
| Final state | `blocked`: `task_..._gate_failed: final_status=repair_exhausted; no_file_changed; reviewer_verdict=fail` |
| Target `git status` before / after | both empty; `README.md` still `# Test`; one commit |
| Generated diff | **none** (`result.diff` is 0 bytes) |

**This is a failed acceptance on the criterion "an actual README diff in Remedy's isolated
workspace".** Cause, measured: the builder's reply described the edit and printed the new file in
prose (`files_changed: []`, `parse_source: heuristic_fallback`), and the reviewer correctly failed
a claimed change that is not in the staged diff. The `no_file_changed` gate fired on the one REAL
task, not on an inspection task. I found no code path that applies an Ollama builder's text to the
workspace: `OllamaPingPongProvider.build` returns text, `pingpong_loop` writes a builder's changes
into staging only for the fake provider, and a writing provider (claude-cli) edits the workspace
itself. So with the all-Ollama default, no order can produce a diff; that predates this amendment,
and repairing it is a provider rewrite the amendment forbids. I did not run claude-cli, because
the order says no Claude process was expected and it spends usage nobody authorized.
**Operator question (one):** should a follow-up feature let the Ollama builder's structured reply
be applied to the workspace, or should `remedy do`'s default builder be a writing provider?

A second, labelled **fake-provider** run of the same command (`--builder-provider fake
--reviewer-provider fake`, commit `e5ca409a0`) shows the rest of the path: one job, one task,
cockpit before the run, `run done — 1.1 s`, apply stopped, target `git status` empty, and a diff in
the job workspace (`docs/README.md`, the fake builder's fixed output, not a real paragraph).

## Provider calls for the incident, before and after

| | Before (the incident, as the order measured it) | After (this branch) |
|---|---|---|
| Study narration | 3 | 0 |
| Mission plan | 1 | 0 |
| Milestone DoD compilation | 3 | 0 |
| Intake | 1 | 0 |
| Task plan | 1 | 0 |
| Builder | 1 | 1 per round (3 in the real run, as no round changed a file) |
| Reviewer | 1 | 1 per round (3) |
| Total | 11 sequential, about 7.5 minutes | 6 in the real run; 2 on a first-round pass |

## Item-status table

| Item | Status | Reason |
|---|---|---|
| D1 lane | done | `do_lane.py` `select_do_lane`, pure, table-tested (13 rows plus properties), no model; bounded lane studies a tiny repository from facts, plans and compiles the DoD deterministically, shapes one job and one task, calls no planner |
| D2 one deliverable, one task | done | verbs verify, confirm, locate, find, identify, assess, audit; `coalesce_deliverable_tasks` merges by the same file, last task's title, cycle-safe; `no_file_changed` untouched |
| D3 `--run-unattended` | done | `--yes` deleted from `do` (catalog, parser, handler, rehearsal refusal, serve and API launcher, contract, guides, tests); full plan: terminal question or stop naming the flag |
| D4 no silent waits | done | `do_progress.py`; heartbeat names the step and both providers, not the active one (the run log writes no role event during a call) |
| D5 cockpit first | done | sequence init, study, plan, shape, ui, run, apply; launch failure prints `remedy ui start <job id>` and the run goes on |
| D6 no invented scope | done | two prompt rules (golden updated, declared) and the guard `do_scope.py`, which falls back to the deterministic plan |
| Test 1 incident end to end | done | `test_do_bounded_lane.py::test_the_incident_order_is_one_job_one_task_with_no_flag_and_no_planning_call` and the cockpit-order test |
| Test 2 call count | done | tripwires on every planning and study factory; builder and reviewer counted |
| Test 3 captured plan replay | done | `test_task_deliverables.py`, with and without `files_hint`; rebuilt from the order's task titles because `.data` is blocked by a deny rule here |
| Test 4 visible progress | done | `test_do_progress.py` (injected sink and clock, flush), plus the human-walk test |
| Test 5 machine output | done | json: one document, stderr empty |
| Test 6 cockpit on failure | done | blocked run keeps the started cockpit; launcher failure prints the real command |
| Test 7 scale-up | done | two files keep two tasks in the full lane, `--force-mission` keeps two jobs, many-file repository and a vague order is full |
| Test 8 scope fabrication | done | LICENSE, CI, `.env.example` proposed by a stub planner are replaced by the deterministic plan |
| Test 9 vocabulary | done | catalog, parser, client interface, documents and callers carry no `remedy do ... --yes` |
| Test 10 existing safety | done | target byte and status unchanged without `--apply`; apply, commit and push gates untouched |
| Real acceptance run | **deviated** | shape, calls, progress, cockpit order and absence of the synthetic gate failure are proven; no README diff (provider limit above) |

## Verification (real, trimmed)

- Closure gate, once green: `python3 -m pytest -n auto -q` from the repository root, Python 3.10.12,
  commit `b6741dfbb597c7c109f1bc8e59270fcdb0af359d`, tree `cd64a6283891227588b7a15e885642a7cdd75b33`:
  `23134 passed, 22 skipped, 1 warning in 331.56s`, exit 0. Log: `~/.remedy-loop/amend1014-suite3.txt`.
- Two earlier full runs were red and are this branch's own, both repaired in C9 and C10:
  run 1 at `6e056c629`, `8 failed, 23126 passed` (the task-plan prompt did not name the new verbs;
  four new modules missing from the reachability allowlist; a lint-excused print, a blind handler
  and a terminal read inside packages; a new role-config call site; `context.md` without "Steps");
  run 2 at `31458f162`, `3 failed, 23131 passed` (the task-plan prompt golden). No test was
  deleted, no assertion weakened, no ceiling raised.
- The new tests fail on the old revision (checked in a detached worktree of `e688b30f3`: 23 failed,
  10 errors, the errors being fixtures that need the new modules).
- The tree after `b6741dfbb` differs only in this handback and `.agent/plan.md`.

## Deviations

1. The mission-prompt golden and the task-plan prompt golden carry declared content changes.
2. `F295_GATE_TEST_SHA256` changed because F295's gate test's `do` line now carries `--run-unattended`.
3. The shared audit sentence "auto-approved via --yes" stays (`job` commands keep their `--yes`; F035's feature file pins it); a `do` approval records "auto-approved via --run-unattended".
4. Existing tests that drove the LLM planner on a one-file order now name two files, because a one-file order deliberately makes no planning call; `--force-job` also selects the bounded lane as the order says.
5. `_cmd_do_order`, `plan_order_job` and `do_cmd.py` shrank (184, 250, 1018 lines); three structure rows and the two pins fell with them.
6. Commits C3 to C5 each pass their own focused tests, but the structure ratchet is only whole at C5.
7. The `.data` incident tree could not be read (deny rule), so the captured plan is rebuilt from the order's own titles.

## Remaining blockers and next steps

1. Operator: the Ollama builder question above. Until answered, the default all-Ollama configuration cannot produce a diff for any order.
2. Review and merge the pull request when satisfied; I did not merge it.
3. F078 resumes on its own branch afterward (`.agent/plan.md` there names round 4).
