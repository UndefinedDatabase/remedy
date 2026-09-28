STEP F036 R6 — THE REPAIRS AND THE PROOF: the model-written tour switched on by the operator (R-1089), the card docked while a stop is shown (R-1088), and one real job's tour end to end

GOAL
Round 5 passed on its block, and its gate registered R-1088 and R-1089. Book them with DECISION
F036 D7, then repair both: a registered key `tour.model_written`, off by default, without which
no terminal asks the summary model for a tour; and the overlay's card docking over the left rail
while a stop is shown, proved by a render that imports the app's global sheet. Then prove one real
job's tour through its file, the browser's route and the command line in a live end-to-end test.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S4 below; the key's description in S1 is given
verbatim and typed exactly. Only the `.agent/` records travel as payloads. Read DECISION F036 D7
and findings R-1088 and R-1089 in the booking diff before you write code. Before you write
anything, read whole: `write_result_tour`, `tour_call_fn` and `tour_view` in
`packages/orchestration/result_tour.py`; the `teacher.lessons` family of `ConfigKeySpec` entries,
`reset_config` and `write_environment_guide` in `packages/orchestration/config.py`;
`lessons_enabled` in `packages/orchestration/lessons.py` and how `tests/orchestration/test_lessons.py`
switches its key; `tests/docs/test_environment_guide.py`; `TourOverlay.tsx` and its CSS module;
`tests/ui_contracts/test_tour_overlay_contract.py`; the five `.agent/authored/f036-r5-render_*`
files; `tests/orchestration/test_resume_kill.py`, whose subprocess runs `run_cycles` to
`all_green`; `tests/ui_server/test_tour_route.py`; and `.agent/authored/f036-r5-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f036-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f036-r6/`           READ-ONLY. The reviewer's block.
  Every other `.remedy-wt/f036-r*` directory and `.remedy-wt/f036-review/`  The reviewer's; do
                                  not touch them.
  `.remedy-wt/f036-r6-worker/`    YOURS for logs, scripts, screenshots and the scratch configs;
                                  create it if absent. `.remedy-wt/f036-render-run/` is the render
                                  harness's own work dir. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables inside tests with `monkeypatch.setenv` and in a subprocess
through its `env=` argument, never on a command line. Never run npm or npx. Stop a process only by
its own recorded pid, never with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f036-guided-result-tour`, and `git log --oneline -1` must read `8c98cadf`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f036-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 59 | 14886 | b97f22efea18b1b032b0a7647c6409beb6e233d1e2094a3d8cbdf33ceee61592 |
| plan.md | 27 | 970 | 75c9d356ee468bd07d91185ed4ec839b12e9352538afbe50fa7c32f607d464df |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `8c98cadf`. It appends round 5's gate entry and
the registrations of R-1088 and R-1089 to `.agent/live_review.md`, and DECISION F036 D7 to
`.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere, no new `# noqa: BLE001`, and no raw colour.
S1 R-1089, THE SWITCH. In `packages/orchestration/config.py`, directly after the
   `teacher.lesson_max_tokens` entry, `ConfigKeySpec(key="tour.model_written",
   env_var="REMEDY_TOUR_MODEL_WRITTEN", description=<DESC>, value_type=bool, default=False)`, where
   <DESC> is exactly these words on one line, single-spaced where this block wraps them: Let the
   summary model write each job's guided tour at the end of its run (F036). Off by default: each
   tour is one summary model call, and a run makes no call the operator did not switch on; with it
   off, every job still gets the tour built from its own records.
   `tour_model_written() -> bool` in `result_tour.py` reads that key the way `lessons_enabled`
   reads its own. `write_result_tour` with no call function handed in uses `tour_call_fn()` when
   `tour_model_written()` is true and `None` otherwise; a call function handed in, `None`
   included, is used as before. `docs/guides/environment.md` is regenerated with
   `write_environment_guide()` and nothing else in it changes.
S2 R-1088, THE DOCK. The card element of `TourOverlay.tsx` carries `data-shown="true"` while the
   current stop is shown and `data-shown="false"` otherwise. `TourOverlay.module.css` gains a rule
   `.card[data-shown="true"]` that sets `top: auto`, `left: 16px`, `bottom: 16px`,
   `transform: none`, `width: calc(var(--remedy-left-width) - 32px)` and `max-height: 60vh`, so
   the shown card sits over the lower left of the left rail. Nothing else in either file changes.
S3 THE RENDER, five NEW files `.agent/authored/f036-r6-render_*`, copies of round 5's with these
   changes only: `main.tsx` also imports `apps/ui/src/styles/globals.css`; `drive.mjs` adds C-i,
   after "Show me" on the first diff stop the card's box lies within the value of
   `--remedy-left-width` read from the page, its bottom within 24 pixels of the viewport's, and it
   does not intersect the box x 514 to 854, y 90 to 490, where the task detail sits at this
   viewport; and C-j, after the following ArrowRight the card's centre lies within 2 pixels of the
   viewport's; and it prints `RENDER: <n> of 10 checks pass`. Its output is saved as
   `.agent/authored/f036-r6-render.txt`.
S4 THE PROOF, NEW FILE at `tests/ui_server/test_tour_e2e_live.py`, marked `@pytest.mark.subprocess`
   and structured like `tests/orchestration/test_resume_kill.py`'s subprocess run with this file's
   own copies of its helpers: one file-based job of two tasks runs to `all_green` through
   `run_cycles` with the fake provider in a subprocess whose environment names a scratch
   `REMEDY_DATA_DIR` and holds no `REMEDY_TOUR_MODEL_WRITTEN`. Then, in the test process with the
   same data root: `stored_tour_versions` reads `[1]`; the stored tour's generator is `fallback`
   and `tour_problems` of it is `[]`; its first stop anchors to the evidence file `report.md`;
   every stop's anchor has `anchor_problem` "" against `collect_tour_context` of the job; a real
   server on port 0, as `test_tour_route.py` starts it, serves at the `tour` route exactly
   `tour_view` of the job, with `stored` true and `version` 1; and
   `python3 -m apps.cli.main job show <job id> --tour` in a subprocess with the same environment
   exits 0, its JSON's `tour` section holds the same tour, and its stderr holds the lines of
   `render_tour_lines` of that tour in order.

THE TESTS beside S4. `tests/orchestration/test_result_tour.py` gains, at least: the key reads
false by default; with it off, `_apply_terminal` at `all_green` writes a tour labelled `fallback`
and never calls `tour_call_fn` (spy with `monkeypatch`); with `REMEDY_TOUR_MODEL_WRITTEN` set on
and `reset_config()` called as `test_lessons.py` does, it calls `tour_call_fn` once; and a call
function handed in is used whatever the key. `tests/ui_contracts/test_tour_overlay_contract.py`
gains: the overlay holds `data-shown=`, and its CSS holds `.card[data-shown="true"]` and
`var(--remedy-left-width)`.

BUNDLE — the commits are C1 to C7, in this order.
C1 — copy this block and the payloads: `.agent/authored/f036-r6-block.md` := this block,
  `.agent/authored/f036-r6-booking.diff` and `-plan.md` := the payloads, by `shutil.copyfile`.
  Subject: `F036 R6 C1: copy round 6 block and payloads into .agent/authored/`. Its insertions
  are this block's line count plus 86; STOP rather than commit at 500 or more.
C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md. Subject: `F036 R6 C2: book round 5, register R-1088 and R-1089, record DECISION F036 D7`
  Expected by `git show --numstat`: 37/0 decisions.md, 6/0 live_review.md, 7/8 plan.md.
C3 — R-1089: `config.py`, `result_tour.py`, `docs/guides/environment.md` and the switch's tests in
  `test_result_tour.py`. Subject: `F036 R6 C3: write the model's tour only when the operator switches it on`
C4 — R-1088: `TourOverlay.tsx`, its CSS module, the contract test's additions, the render files
  and `f036-r6-render.txt`, split under constraint 2 if needed.
  Subject: `F036 R6 C4: dock the tour's card over the left rail while a stop is shown`
C5 — THE PROOF: `tests/ui_server/test_tour_e2e_live.py`.
  Subject: `F036 R6 C5: prove one real job's tour through its file, its route and the command line`
C6 — THE TOOL: your mutation tool (G5) as `.agent/authored/f036-r6-mutations.py`.
  Subject: `F036 R6 C6: add the round 6 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, and two
  lines appended to `.agent/live_review.md`, each preceded by a blank line:
  `Landed: R-1089 — <one sentence naming C3's short SHA>` and `Landed: R-1088 — <one sentence
  naming C4's short SHA>`. Nothing else in the ledger changes.
  Subject: `F036 R6 C7: rewrite handoff for round 6, mark R-1088 and R-1089 landed`.
  Then `git push`, and report its outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f036-r6-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the files C3, C4 and C5 name,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only 8c98cadf` at the
   branch tip after C7. Do NOT touch any other file under `apps/`, `packages/`, `tests/` or
   `docs/`, `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C7, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F036's belongs to its closure. No test may reach a live model: the switch stays off in every
   subprocess this round starts, and every call function in the tests is a stub or `None`.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f036-r6-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f036-r6/block.md`), read back with
 `git show <C1>:<path>`. Report one reading each.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2371422 | c1b761a933b5d89860973792dc6b2fecb27536ab0806e646d62d6e7e1424f73d |
 | .agent/live_review.md | 332264 | e8cf27b58933833780d67eaad26e903254bbe61ee3dad4ab0e5f249d91302174 |
 | .agent/plan.md | 970 | 75c9d356ee468bd07d91185ed4ec839b12e9352538afbe50fa7c32f607d464df |
 Also: `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2, which the reviewer read as `['R-1088', 'R-1089']` and `PASS`.

G3 THE CODE — `python3 -m ruff check packages/orchestration/config.py
 packages/orchestration/result_tour.py tests/orchestration/test_result_tour.py
 tests/ui_contracts/test_tour_overlay_contract.py tests/ui_server/test_tour_e2e_live.py
 .agent/authored/f036-r6-render_measure.py` at C6, with its real exit code. Then report, quoted
 from the commits that wrote them, the new key entry, `tour_model_written`, the changed lines of
 `write_result_tour`, the `data-shown` line of the overlay and the new CSS rule.

G4 THE TESTS AND THE RENDER — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_result_tour.py tests/cli/test_job_show.py tests/ui_server/test_tour_route.py tests/ui_server/test_tour_e2e_live.py tests/ui_server/test_handler_table_walk.py tests/ui_server/test_command_channel.py tests/ui_server/test_ownership_route.py tests/ui_contracts tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/orchestration/test_resume_kill.py tests/orchestration/test_run_report_hook.py tests/orchestration/test_long_run_executor.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/ui_server/test_tour_e2e_live.py`, serially, in the
 primary checkout at `8c98cadf`, and read `1988 passed, 5 skipped` at real exit code 0; the skips
 are four F252 quarantines in `tests/ui_contracts/` and the one in `tests/test_agent_tooling.py`.
 Report every `SKIPPED` line, the node count of each test file this round added or grew, and the
 selection's wall time, and account for any difference from 1988. Then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0. Then
 `python3 .agent/authored/f036-r6-render_measure.py /home/decodeux/Repos/remedy`, which must print
 `RENDER: 10 of 10 checks pass` and exit 0, leave no `.remedy-wt/f036-render-run` and leave
 `git status --porcelain` empty; report both screenshots' paths and sizes.

G5 THE RED PROOFS — your tool `.agent/authored/f036-r6-mutations.py`, modelled on round 5's, has a
 PYTHON runner, `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_result_tour.py
 tests/orchestration/test_config.py` from the worktree's root with that root first on `sys.path`,
 and round 5's CONTRACT runner. It prints one line per mutation, controls of each runner first and
 last, `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 PYTHON (`config.py`) the key's default is `True`;
  m2 PYTHON (`result_tour.py`) `write_result_tour` asks `tour_call_fn()` whatever the key;
  m3 PYTHON (`result_tour.py`) `tour_model_written` answers the key's opposite;
  m4 CONTRACT (`TourOverlay.module.css`) the `.card[data-shown="true"]` rule is removed;
  m5 CONTRACT (`TourOverlay.tsx`) the card's `data-shown` attribute is removed.
 Run it on `git worktree add --detach .remedy-wt/f036-r6-mut <C6>` and report its whole output.
 EVERY mutation must be red; a green one is reported as green, and you then add the test that
 catches it before C7 and re-run. Then remove the worktree, `git worktree prune`, and report
 `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C7 to C1 and `8c98cadf` in that order (more lines if
 constraint 2 split a commit); `git worktree list | wc -l`, equal to your step 4 reading; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Your Session section reads SESSION 1 of feature F036, round 6, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then the closure sequence — the Built State and the docs, the one full-suite run, the
evidence package and the STATUS acceptance. State the open-findings count, 2 (R-1088 and R-1089,
landed and awaiting the reviewer's resolution), and the operator-questions count, 1.
