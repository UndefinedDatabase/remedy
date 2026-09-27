STEP F288 R3 — THE LONG-RUN CYCLE'S ATTEMPT, T002 (THE LIVE GRAPH'S REDUCER), AND THE REPAIR OF R-1075: the stream's rows carry the attempt id and the approved task ids, the reducer births tasks at plan approval, test runs and repair runs, and the demo recording is captured again

GOAL
Round 2 passed. Book its verdict, register R-1075, record DECISION F288 D3, and land it: the
long-run executor's `cycle_repair_round`, `cycle_healed` and `cycle_completed` carry the cycle's
attempt id and result; `feedRowOf` and the reducer's row type carry `attemptId` and
`planTaskIds`; the reducer births tasks at `plan_approved`, a `test_run` from each round's test
and each linked test run, and a `repair_run` from each repair round; the phase table marks two new
kinds; and R-1075 is repaired by its FIX.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE CHANGE IS SPECIFIED, NOT SLICED: you write the code
and its tests yourself against S1 to S6 below. Only the `.agent/` records travel as payloads. Read
DECISION F288 D3 and R-1075 in the records diff before you write code: they are the design and the
repair this specification implements.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f288-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f288-r3/`           READ-ONLY. The reviewer's block.
  Every other `.remedy-wt/f288-*` directory and `.remedy-wt/f288-review/` belongs to the
  reviewer; do not touch them.
  `.remedy-wt/f288-r3-worker/`    YOURS for logs, scripts, the capture and the vitest scratch
                                  config; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`); pass an environment to a
child process through Python's `subprocess` `env=` argument. A heredoc containing a dollar-brace is
refused: write such a script to a file under your own directory and run the file. Never run npm or
npx; the one Node binary you may run is
`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest`, and only as G5 orders it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f288-event-stream-completeness`, and `git log --oneline -1` must read `b1320109`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f288-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git stash list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f288-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 76 | 17172 | d418e1471319bf7ebecb285599076adad570cbfc0d477284c833a87b4dc406a2 |
| plan.md | 30 | 1168 | 04ed14d5caf048e0dc3c76492acba22f872f3e80ff63d11d5de60ba3c9e3110c |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `b1320109` into which it wrote the edits. It
appends round 2's gate entry and R-1075's registration to `.agent/live_review.md` and DECISION
F288 D3 to `.agent/decisions.md`.

THE SPECIFICATION
S1 THE LONG-RUN CYCLE. In `packages/orchestration/long_run_executor.py`, the `cycle_repair_round`
   and `cycle_healed` events `_run_repair_rounds` writes, and the `cycle_completed` event
   `run_cycles` writes, each gain the keyword `attempt_id=f"cycle-{cycle_index}"` and an `outcome`:
   `changed` when the round's `repair.changed_files` is non-empty and `unchanged` otherwise,
   `healed`, and the record's `verify_result` respectively. Every keyword they carry today stays.
   In `packages/orchestration/ui_server.py`, `ATTEMPT_EVENT_KINDS` gains those three kinds and its
   comment names DECISION F288 D3.
S2 THE ROWS. In `apps/ui/src/api/feedRow.ts`, `FeedRow` gains the optional fields
   `attemptId?: string` and `planTaskIds?: readonly string[]`, each with a doc comment naming
   DECISION F288 D3, and `feedRowOf` always sets both: `attemptId` from the envelope's
   `attempt_id` when it is a string and `""` otherwise; `planTaskIds` from the string entries of
   the envelope's `plan.task_ids`, in order, when `plan` is an object and `task_ids` an array, and
   `[]` otherwise. In `apps/ui/src/components/graph/brainOntology.ts`, `BrainEventRow` gains the
   same two optional fields, and two tables join `REVIEW_OUTCOME_STATE_TABLE`:
   `TEST_OUTCOME_STATE_TABLE` = `pass`→`pass`, `passed`→`pass`, `fail`→`fail`, `failed`→`fail`,
   `timeout`→`fail`, `blocked`→`blocked`; and `REPAIR_OUTCOME_STATE_TABLE` = `changed`→`pass`,
   `unchanged`→`blocked`, `error`→`fail`, each with a doc comment naming DECISION F288 D3.
S3 THE REDUCER. In `apps/ui/src/components/graph/brainReducer.ts`, `applyBrainEvent` gains:
   `plan_approved` — births, in `planTaskIds` order, every task id the model lacks as a `task`
   node in state `planned` with `meta.rank` one above the highest rank so far (the way `birthTask`
   ranks), and changes no existing task; with an absent or empty list it returns the model
   unchanged; either way it is a HANDLED kind and never counted in `ignored`.
   `task_round_tested` — with a task id, births a `test_run` under its task in the state
   `TEST_OUTCOME_STATE_TABLE` gives its outcome, `planned` for a word the table lacks.
   `task_round_repaired` — with a task id, births a `repair_run` likewise from
   `REPAIR_OUTCOME_STATE_TABLE`.
   `test_run_completed`, `test_run_timed_out` and `test_run_blocked` — with a task id, birth a
   `test_run` from `TEST_OUTCOME_STATE_TABLE`; without one, ignored.
   Each of the three births the task first, as `onVerification` does, and each run is a child of
   its task with id `runNodeId(taskId, seq)` and `meta: { outcome }`. EVERY run node born from a
   row (the new ones and the existing `builder_run`, `review_run` and verification `test_run`)
   carries `meta.attemptId` when the row's `attemptId` is a non-empty string, and its meta is
   EXACTLY as today when it is not, so every golden in `brainReducer.fixtures.ts` stays
   byte-identical. The cycle events keep falling to `default`. The module header and the doc
   comment of `NodeKind` in `brainOntology.ts` are rewritten to state what is born now and from
   which event, citing DECISION F288 D3, and that `synapse` and `artifact` are still born by
   nothing.
S4 THE PHASES. `PHASE_MARKER_TABLE` in `apps/ui/src/components/timeline/phaseMapping.ts` gains
   `plan_approved: "planning"` and `task_round_tested: "test"`; nothing else in that file changes.
S5 R-1075. Capture the recording again, exactly as the module docstring of
   `apps/ui/src/components/graph/brainDemoRecording.ts` describes, in a scratch repository and data
   root under your own directory, with the code at C4 (neither C3 nor C4 changes an event `run_job` writes):
   `init`, then `do "fix src/main.py and update README.md" --no-llm --plan-only --json`, then the
   dashboard's `tasks` read before the run, then `job run <job id> --builder-provider fake
   --reviewer-provider fake --json`, then every frame `_build_events_since_json` serves from cursor
   0, reusing `_git_repo`, `_env` and `_page_events` from
   `tests/ui_server/test_brain_demo_recording_live.py` by import. Write `BRAIN_DEMO_JOB_ID`,
   `BRAIN_DEMO_TASKS` (the same ten fields in the same order as today, their values mapped as
   today) and `BRAIN_DEMO_FRAMES` (each frame's fields in the envelope's own key order, so an
   attempt kind's frame ends `task_id: "…", attempt_id: "…"`) from that capture, generated by a
   script and never typed, and set the docstring's capture date to the day you capture. Save the
   script as `.agent/authored/f288-r3-capture.py`. In the live test: `_FRAME_RE` accepts an
   optional `, attempt_id: "<value>"` after `task_id`; `_parse_recording` asserts the number of
   frames it parsed equals the number of `{ seq: ` openings in the frames block; and the key-set
   assertion reads `{"seq", "event", "timestamp", "outcome", "task_id", "attempt_id"}` for a frame
   whose kind is in `ATTEMPT_EVENT_KINDS` (imported from `packages.orchestration.ui_server`) and
   the five base keys otherwise. No other assertion of that file changes. In
   `brainDemoRecording.test.ts`, `DEMO_GOLDEN_MODEL` is derived again BY HAND from the new frames
   under S3's rules, its comment rewritten to walk the new frames as the old one walked the old.
S6 NOTHING ELSE. No other production file changes.

THE TESTS
In `apps/ui/src/api/feedRow.test.ts`: `attemptId` read from `attempt_id`, `""` when absent and when
not a string; `planTaskIds` keeping order and dropping non-strings, `[]` when `plan` is absent, not
an object, or its `task_ids` not an array. In
`apps/ui/src/components/graph/brainReducer.test.ts`, with new fixtures in
`brainReducer.fixtures.ts` HAND-DERIVED like the existing goldens: a golden stream of
`plan_approved` naming two tasks on an empty seed, then for the first task `task_run_started`
(attempt `A`), `task_round_tested` fail, `task_round_completed` needs_repair, `task_round_repaired`
changed, `task_round_tested` pass, `task_round_completed` pass and `task_run_completed` pass, every
row but the first carrying attempt `A`, whose expected model is a literal, reached by
`rebuildBrainModel` and by a one-row-at-a-time fold; `plan_approved` changing neither the state nor
the rank of a seeded task, ranking new tasks after it, and leaving `ignored` empty; each repair
outcome's state, `planned` for an unknown word; `test_run_completed`, `test_run_timed_out` and
`test_run_blocked` with a task id and without one; `cycle_repair_round` counted in `ignored`; and
a row with an empty `attemptId` leaving a run's meta without the key. In
`apps/ui/src/components/timeline/phaseMapping.test.ts`: `plan_approved` begins `planning` and
`task_round_tested` begins `test`. In `tests/orchestration/test_self_healing_cycles.py`, with the
file's `RecordingLog`: a repair round's event carries `attempt_id` `cycle-<index>` and outcome
`changed` for a round with changed files and `unchanged` for one without; `cycle_healed` carries
the attempt id and `healed`; and `cycle_completed` carries the attempt id and the cycle's verify
result as `outcome`. In `tests/ui_server/test_sse_stream.py`: the pinned set becomes the nineteen
names of D2 and S1.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f288-r3-block.md` := this block, `.agent/authored/f288-r3-records.diff` :=
  records.diff and `.agent/authored/f288-r3-plan.md` := plan.md, all by `shutil.copyfile`.
  Subject: `F288 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 106. Report the number you measure and STOP
  rather than commit if it is 500 or more.
C2 — THE BOOKING, THE REGISTRATION AND THE PLAN: `git apply` records.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F288 R3 C2: book round 2's PASS, register R-1075, record D3 and the round 3 plan`
  Expected by `git show --numstat`: 56/0 decisions.md, 4/0 live_review.md, 10/11 plan.md.
C3 — THE LONG-RUN CYCLE: S1, with its tests in `tests/orchestration/test_self_healing_cycles.py`
  and `tests/ui_server/test_sse_stream.py`.
  Subject: `F288 R3 C3: give the long-run cycle's events their attempt id and result`
C4 — THE ROWS, THE REDUCER AND THE PHASES: S2 to S4 with their vitest tests and fixtures.
  Subject: `F288 R3 C4: carry the attempt id and the approved tasks on the rows, and birth tasks, test runs and repair runs in the reducer`
C5 — R-1075: S5 — the recording, its golden, the live test and the capture script, and at its end
  one line appended to `.agent/live_review.md`, starting with its own blank line:
  `Landed: R-1075 — the demo recording is captured again with the round events and attempt ids, its live test parses an optional attempt id and counts the frames it parsed, reads the attempt kinds' key set with attempt_id, and the recording's golden is derived again by hand, at this round's C5.`
  — one physical line, exactly that text.
  Subject: `F288 R3 C5: capture the demo recording again and bring its live test to the attempt id (R-1075)`
C6 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f288-r3-mutations.py`.
  Subject: `F288 R3 C6: add the mutation tool for the round's red proofs`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`.
  Subject: `F288 R3 C7: rewrite handoff for round 3`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into lettered parts with their own subjects, and say so. The recording and the
   capture script may be one commit of their own if C5 would reach it.
3. The round's whole tracked path set is: the `.agent/authored/f288-r3-*` copies, script and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/long_run_executor.py`, `packages/orchestration/ui_server.py`,
   `apps/ui/src/api/feedRow.ts`, `apps/ui/src/api/feedRow.test.ts`,
   `apps/ui/src/components/graph/brainOntology.ts`, `apps/ui/src/components/graph/brainReducer.ts`,
   `apps/ui/src/components/graph/brainReducer.test.ts`,
   `apps/ui/src/components/graph/brainReducer.fixtures.ts`,
   `apps/ui/src/components/graph/brainDemoRecording.ts`,
   `apps/ui/src/components/graph/brainDemoRecording.test.ts`,
   `apps/ui/src/components/timeline/phaseMapping.ts`,
   `apps/ui/src/components/timeline/phaseMapping.test.ts`,
   `tests/orchestration/test_self_healing_cycles.py`, `tests/ui_server/test_sse_stream.py`,
   `tests/ui_server/test_brain_demo_recording_live.py`, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only b1320109` at the branch tip after C7.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C7, and the correction is declared. An
   EXISTING test that goes red is never edited to pass, the pinned set of S1 and the three things
   S5 orders in the live test and the recording's golden excepted; report it and stop.
5. NOTHING IS MERGED, AND THE PRIMARY CHECKOUT NEVER LEAVES THE BRANCH. No `gh pr merge`, no
   `gh pr create`, no `git checkout` or `git switch` of anything in the primary checkout, no
   branch deletion, no force-push, and no `git stash` of any kind: round 2's worker ran both and
   the reviewer had to prove they changed nothing. To read an older commit, use `git show
   <sha>:<path>` or a disposable worktree under `.remedy-wt/`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F288's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f288-r3-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f288-r3/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2234111 | 4466404a63bf089a98d4db64c62b9f82e4c9fcdc042c3bf05e7c8b63da632bca |
 | .agent/live_review.md | 307906 | cdf9b015254e45ed9af1642c7fc69a97b157ee4fede3ecf5edd713c1bdfc81bf |
 | .agent/plan.md | 1168 | 04ed14d5caf048e0dc3c76492acba22f872f3e80ff63d11d5de60ba3c9e3110c |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at C2 (the reviewer read `R-1075` alone),
 and `git diff -U0 <C4> <C5> -- .agent/live_review.md`, reported whole, which must add the blank
 line and the one `Landed:` line and nothing else.

G3 THE CODE — `python3 -m ruff check packages/orchestration/long_run_executor.py
 packages/orchestration/ui_server.py tests/orchestration/test_self_healing_cycles.py
 tests/ui_server/test_sse_stream.py tests/ui_server/test_brain_demo_recording_live.py
 .agent/authored/f288-r3-capture.py` at C5, with its real exit code. Then quote from the diff the
 whole of the reducer's `plan_approved` handler and the helper that puts `attemptId` into a run's
 meta, and the frame lines of `BRAIN_DEMO_FRAMES` for the first task.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_long_run_executor.py tests/ui_server/test_sse_stream.py tests/ui_server/test_budget_tick_envelope.py tests/ui_contracts tests/ui_server/test_brain_demo_recording_live.py tests/ui_server/test_semantic_zoom_live.py tests/ui_server/test_timeline_scrub_live.py tests/ui_server/test_live_state.py tests/orchestration/test_event_names.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/test_imports.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this exact selection, serially, in the primary checkout at `b1320109`, and read
 `1 failed, 1819 passed, 5 skipped` at real exit code 1: the failure is R-1075's node,
 `tests/ui_server/test_brain_demo_recording_live.py::test_live_fake_job_renders_identically_to_the_demo_recording`,
 and the skips are four D3 quarantines in `tests/ui_contracts/test_graph_architecture.py` and
 `tests/ui_contracts/test_ux_quality.py` and the D12 one in `tests/test_agent_tooling.py`, which
 stay skipped. At C6 it must read 0 failed at real exit code 0. The whole vitest suite, the
 TypeScript compiler and the UI lint run inside this selection as
 `tests/orchestration/test_test_runner.py::...::test_vitest_passes`,
 `tests/ui_server/test_dashboard_contract.py::...::test_typescript_compiles` and
 `tests/ui_contracts/test_ui_lint.py`. Report every `SKIPPED` line, the Python nodes the round adds
 (`--collect-only -q` on the edited Python test files at `b1320109` and at C6) and the vitest
 tests it adds (`npm run test:unit -- --reporter=json` is NOT available to you: count the `it(`
 blocks the round adds in the edited `.test.ts` files from the diff), and account for any other
 difference from 1820. Then `python3 -m apps.cli.main integrity check --json`, which must read
 all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f288-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs the named tests, restores the bytes, and prints one line per mutation: its
 label, the exit code, the failed count and the failing test names. It runs an unmutated control
 first and last for each runner and ends with `restored byte-identical: True` per file and a final
 line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Python mutations run
 `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_self_healing_cycles.py` and `tests/ui_server/test_sse_stream.py` from
 the worktree's root after purging its `__pycache__` directories. TypeScript mutations run
 `/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest run --config <scratch config>` from
 `/home/decodeux/Repos/remedy/apps/ui`, where the scratch config under your own directory exports a
 PLAIN OBJECT with `root` the primary `apps/ui`, `cacheDir` under `.remedy-wt/`, and
 `test: { environment: "node", include: [<the worktree's feedRow.test.ts, brainReducer.test.ts,
 phaseMapping.test.ts and brainDemoRecording.test.ts by absolute path>] }` (DECISION F256 D6's
 route; a config importing `vitest/config` cannot resolve); before the mutations, prove the route
 reads the worktree's sources by one mutation that cannot pass whatever the tests import, and
 report it. The mutations:
  m1 `cycle_repair_round` carries no `attempt_id`;
  m2 `cycle_repair_round` reads `changed` whatever its changed files;
  m3 `cycle_completed` carries no `outcome`;
  m4 `ATTEMPT_EVENT_KINDS` loses `cycle_healed`;
  m5 `feedRowOf` reads the envelope key `attemptId` instead of `attempt_id`;
  m6 `feedRowOf` keeps non-string plan task ids;
  m7 `plan_approved` births nothing;
  m8 `plan_approved` sets an existing task back to `planned`;
  m9 `plan_approved` ranks its new tasks in reverse order;
  m10 `task_round_tested` births a `review_run`;
  m11 `REPAIR_OUTCOME_STATE_TABLE` maps `unchanged` to `pass`;
  m12 `task_round_repaired` falls to `default`;
  m13 `test_run_completed` without a task id births a task anyway;
  m14 a run's meta carries `attemptId: ""` when its row has none;
  m15 `PHASE_MARKER_TABLE` loses `plan_approved`.
 Run it in `git worktree add --detach .remedy-wt/f288-r3-mut <C6>` and report its whole output.
 EVERY mutation must be red; a green one is reported as green, never papered over: you then add
 the test that catches it and re-run the tool. Then `git worktree remove --force
 .remedy-wt/f288-r3-mut`, `git worktree prune`, and `git worktree list | wc -l`; and
 `git status --porcelain` must be empty, a stray `.vite/` included.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty; `git log --oneline`
 from `b1320109` to the tip; `git worktree list | wc -l` and `git stash list | wc -l`, which must
 equal your step 4 readings; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected (none is expected for C3 to C6 — report what you measure), every gate's real output
and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row per
commit and per gate), the deviations, and the next expected action. Report what you ran, not what
you expected to find. Your Session section reads SESSION 1 of feature F288, round 3, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3 with R-1075's resolution, then T003 — the prompt node kind, its look, and its mouse and
keyboard reach. State the open-findings count, 1 (R-1075, landed and awaiting the reviewer's
`Done:`), and the operator-questions count, 0.
