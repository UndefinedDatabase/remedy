STEP F029 R3 — BOOK R2, REPAIR R-1081, AND LAND THE SECOND HALF OF T002: `remedy job rerun-subtree` with the subtree's cost estimate and the cost preview

GOAL
Round 2 passed. Book its gate entry, resolve R-1080 and register R-1081, record DECISION F029 D3,
repair R-1081, and land the command: `remedy job rerun-subtree <job> <task> [--model M] [--yes]
[--json]` estimates what re-running the subtree will cost, shows that through the cost preview
before anything is touched, prepares the rerun with round 2's `prepare_subtree_rerun`, and names
the command that runs it. No run-log event and no browser change: DECISION F029 D3 moves the event
to T003.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code and tests against S1 to S5; only the `.agent/` records travel as payloads. Read DECISIONS
F029 D2 and D3 in `.agent/decisions.md` after C2 before you write code. Read, before writing:
`packages/orchestration/subtree_rerun.py` whole; `packages/orchestration/cost_preview.py`;
`PLAN_BAND_TO_TOKEN_BAND` in `packages/orchestration/task_injection.py`;
`resolve_predictive_budget_config` in `packages/orchestration/budget_resolution.py`;
`apps/cli/cost_preview_confirm.py`; `apps/cli/commands/job_veto_cmd.py` and
`apps/cli/commands/job_inject_cmd.py`, the two commands this one is modelled on; the `job.veto-task`
and `job.resume` entries of `apps/cli/command_catalog.py`; `apps/cli/commands/__init__.py`;
`docs/guides/exit-codes.md` and `tests/cli/test_exit_codes.py`; the `is_expensive` tests in
`tests/test_command_catalog.py`; `tests/orchestration/import_reachability_allowlist.txt` and the
`ALLOWED_UNWIRED` tuple of `tests/test_no_orphan_modules.py`; `tests/cli/test_job_veto.py`; and the
end-to-end harness of `tests/orchestration/test_subtree_rerun_prepare.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r3-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f029-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f029-r3-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f029-subtree-rerun`, and `git log --oneline -1` must read `aa054d8b`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 63 | 13798 | ec05f1abe49caa56708da6ebc28fe5eadc3063d3a3a65676bfa9b1b363a837ab |
| plan.md | 33 | 1197 | d9564ff256af9b563def34f584f2c928fee3f974f02e24caa6999e3f89acf3ef |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer generated
it with `git diff HEAD` from a tree at `aa054d8b`. It appends to `.agent/live_review.md` round 2's
gate entry, R-1080's `Done:` line and R-1081's registration, and to `.agent/decisions.md`
DECISION F029 D3.

THE SPECIFICATION
S1 R-1081, in `prepare_subtree_rerun`. (a) BEFORE `worktrees.create`, for every subtree task that
   ran and whose stream directory exists, its archive destination
   `rerun_attempts/<task_id>/attempt-<its attempt>` under `job_evidence_dir(job_id)` must not
   exist, else `SubtreeRerunRefused("stream_archive_occupied", ...)` naming that
   evidence-relative path, with nothing touched. (b) AFTER `worktrees.create`, every exit other
   than success and a `SubtreeRerunRefused` from `apply_subtree_reset` passes through
   `worktrees.retain_for_recovery(handle, f"{type(exc).__name__}: {exc}")` before the exception
   propagates — including any exception from the stream moves, the fold, `set_checkpoint_ref` and
   `save_job_plan`. Write it WITHOUT a blind handler (no `except Exception`, no
   `except BaseException`): a completion flag checked in a `finally`, so the frozen count of
   `tests/test_ble001_ratchet.py` stays as it is. The refusal path of round 2 is unchanged.
S2 THE ESTIMATE, in `subtree_rerun.py`: `subtree_rerun_cost_estimate(job, subtree_ids, *, config)
   -> CostBandEstimate`. For each id in order, the task's plan band is
   `task.inputs.get("plan", {}).get("est_tokens_band")` read defensively (a missing or non-dict
   `plan` counts as no band) and mapped through `PLAN_BAND_TO_TOKEN_BAND`; the task's estimate is
   `estimate_cost_band(tb, tb, config=config)`. When any task has no band or an unavailable
   estimate, the answer is `CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, inputs)`; otherwise
   `band_usd_low` and `band_usd_high` are the sums of the tasks' bounds, rounded to 6 places, and
   `basis` reads `f"sum over the {n} tasks of the subtree of class defaults per plan band x
   price_basis_usd_per_1k_tokens={config.price_basis_usd_per_1k_tokens}"`. `inputs` is
   `{"tasks": [{"task_id", "plan_band"}, ...], "unpriced": [ids without an estimate]}`, the band ""
   when none.
S3 THE COMMAND, a new module `apps/cli/commands/job_rerun_cmd.py` whose docstring names F029 T002
   and DECISION F029 D3, modelled on `job_veto_cmd.py`: `_cmd_rerun_subtree(job_id_str, task_arg,
   *, model="", yes=False, json_output=False)`. In order: `resolve_job_id_or_fail`;
   `require_job_plan`, a missing job failing `job_not_found` at exit 1; the task through
   `job_plan_cmd._resolve_task_arg`; `rerun_subtree_ids`, `unknown_task` failing at exit 2 before
   any preview; the estimate of S2 with `resolve_predictive_budget_config(project_root=job.repo_path
   or None)`; `confirm_cost_preview(estimate, confirm_above_usd=resolve_confirm_above_usd(), yes=yes,
   command_name="job.rerun-subtree", json_output=json_output)`, whose False answer prints
   `Cancelled. Nothing was changed.` (to stderr under `--json`, where stdout then carries
   `emit_ok(job_id=..., cancelled=True)`) and returns with nothing prepared; then
   `prepare_subtree_rerun(job_id, task_id, model_override=model, actor=CLI_ACTOR)` with
   `CLI_ACTOR = "cli"`. A `SubtreeRerunRefused` fails with its code and detail at exit 2 for
   `unknown_task` and `model_invalid`, 1 for `job_not_found`, and 3 for every other code, passing
   `job_id`, `task_id` and the refusal's `facts` into the envelope. Success under `--json` is ONE
   `emit_ok` carrying the prepared record's keys plus `estimate` (`band_usd_low`,
   `band_usd_high`, `basis`) and `run_command`, with no keyword passed twice. The human answer
   prints: `Rerun <rerun_id> prepared for job <job_id>: task <root> and <n> dependent task(s) reset.`,
   the reset commit's first twelve characters, the files put back (or `no file changed`), the
   tasks returned to pending, the override beside the configured model when one was given, and
   last `Run it with: remedy job run <job_id>` with the real id. `COMMAND_HANDLERS` maps
   `job.rerun-subtree` from `args.job_id`, `args.task`, `args.model`, `args.yes` and `args.json`.
S4 THE WIRING. A `CommandEntry` after `job.veto-task`'s: `command_id="job.rerun-subtree"`,
   `subcommand="rerun-subtree"`, a description naming F029, `action_class="apply_write"`, args
   `_JOB_ID`, `task`, `--model` (option), `--yes` (flag, worded as `job.resume` words it) and
   `_JSON_OPT`, `supports_json=True`, `may_mutate_repo=True`, `may_execute_commands=False`,
   `is_expensive=True`, related `("job.run", "job.plan-show", "job.veto-task")`, exit codes
   `(0, 1, 2, 3)`. The module joins the import list and the `for mod in (...)` tuple of
   `apps/cli/commands/__init__.py`; `remedy job rerun-subtree` joins the table of
   `docs/guides/exit-codes.md` where `tests/cli/test_exit_codes.py` requires it; the pin
   `test_exactly_one_command_is_marked_expensive_so_far` in `tests/test_command_catalog.py` reads
   the two ids `["job.rerun-subtree", "job.resume"]` — rename the test so its name stays true and
   keep its message naming F114 and DECISION F029 D3; `tests/orchestration/import_reachability_allowlist.txt`
   gains the two modules the test's own regeneration names; `subtree_rerun.py`'s entry leaves
   `ALLOWED_UNWIRED`.
S5 NOTHING ELSE: no event, nothing under `apps/ui/`, no edit to `ui_server.py`, `pingpong_job.py`,
   `worktrees.py` or `cost_preview.py`.

THE TESTS — a NEW file `tests/cli/test_job_rerun_subtree.py`, and R-1081's tests beside round 2's in
`tests/orchestration/test_subtree_rerun_prepare.py`. At least: S1 (a) a completed job whose
archive destination already holds a file refuses `stream_archive_occupied` with no worktree
re-added and `job.json` byte-identical; S1 (b) a `save_job_plan` made to raise `OSError` inside
`subtree_rerun` leaves `worktrees.lock_is_held(...)` False and the `OSError` propagating. S2 with a
price basis of $0.01 per thousand tokens and class defaults 8000, 32000 and 120000: bands `S` and
`M` sum to 0.4 at both bounds, one `XL` or one task without a band makes the whole estimate
unavailable with `unpriced` naming it. S3 over the three-task job of round 2's end-to-end harness,
run to `completed`: `--yes --json` prepares the rerun, its envelope carrying `subtree`
`["T002", "T003"]`, the estimate and `run_command` `remedy job run <id>`; the human answer's last
line is exactly that command; without `--yes` on a stdin that is not a terminal the answer is
`confirmation_required` at exit 2 with `job.json` byte-identical; a declined prompt changes
nothing; `--model rerun-model` reaches the record's `model.override`; `unknown_task` exits 2 with
no preview printed; `model_invalid` exits 2; a job in state `running` exits 3 `job_running`; an
interleaved rerun exits 3 with `interleaving` in the JSON envelope; `job_not_found` exits 1.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.
C1 — `.agent/authored/f029-r3-block.md` := this block, `.agent/authored/f029-r3-booking.diff` and
  `.agent/authored/f029-r3-plan.md` := the payloads, by `shutil.copyfile`.
  Subject: `F029 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 96. Report the number you measure.
C2 — `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F029 R3 C2: book round 2's PASS, resolve R-1080, register R-1081, record D3`
  Expected by `git show --numstat`: 41/0 decisions.md, 6/0 live_review.md, 10/11 plan.md.
C3 — S1 and its tests. Subject: `F029 R3 C3: R-1081 — never leave a rerun's worktree lock held`
C4 — S2 and its tests. Subject: `F029 R3 C4: estimate a subtree rerun's cost from its plan bands`
C5 — S3, S4 and the command's tests. Subject: `F029 R3 C5: add remedy job rerun-subtree behind the cost preview`
  Split under constraint 2 when it would reach 500 insertions.
C6 — `.agent/authored/f029-r3-mutations.py` (G5) as C6a, subject `F029 R3 C6a: add the mutation
  tool`, then `.agent/handoff.md` per `docs/agents/handback_template.md` as C6b, subject
  `F029 R3 C6b: rewrite handoff for round 3`. Then `git push origin feature/f029-subtree-rerun`
  and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`; split a commit that would
   reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f029-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/subtree_rerun.py`, `apps/cli/commands/job_rerun_cmd.py`,
   `apps/cli/commands/__init__.py`, `apps/cli/command_catalog.py`, `docs/guides/exit-codes.md`,
   `tests/cli/test_job_rerun_subtree.py`, `tests/orchestration/test_subtree_rerun_prepare.py`,
   `tests/test_command_catalog.py`, `tests/orchestration/import_reachability_allowlist.txt` and
   `tests/test_no_orphan_modules.py`. Report `git diff --name-only aa054d8b` at the tip after C6b.
   A guard outside this set that goes red because the new command exists is reported and stops
   the round under constraint 4; it is never edited.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round wrote that is wrong may be corrected
   before C6b, and the correction is declared. An EXISTING test that goes red is never edited to
   pass unless this block names it; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F029 one full-suite run, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C6b is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; then
 each `.agent/authored/f029-r3-*` copy read back with `git show <C1>:<path>` compared byte for byte
 with its source (the block copy against `.remedy-wt/f029-r3/block.md`). One reading per copy.
G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2290828 | 41fe5d8c643f8b198b3d3347ef930259c1ea3f3ca538af159764d9f4dd680444 |
 | .agent/live_review.md | 317154 | 4e36aac15aa01185a11404da02129933eb2a51c0f7e493b3ca5e8a2965eaf703 |
 | .agent/plan.md | 1197 | d9564ff256af9b563def34f584f2c928fee3f974f02e24caa6999e3f89acf3ef |
 Also the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the file's TEXT at `aa054d8b` (the reviewer read `['R-1080']`) and at C2 (the reviewer read
 `['R-1081']`).
G3 THE CODE — `python3 -m ruff check` over every Python file the round touched, at the tip before
 C6b, with its real exit code; then quote from the commit that landed it the whole of
 `_cmd_rerun_subtree` and the part of `prepare_subtree_rerun` from `worktrees.create` to its return.
G4 THE TESTS — in the primary checkout at the last commit before C6b, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_job_rerun_subtree.py tests/orchestration/test_subtree_rerun.py tests/orchestration/test_subtree_rerun_prepare.py tests/cli/test_job_veto.py tests/cli/test_job_inject.py tests/cli/test_command_catalog.py tests/test_command_catalog.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/cli/test_job_refusal_envelope.py tests/cli/test_json_envelope.py tests/cli/test_list_commands_everywhere.py tests/test_grouped_cli.py tests/test_cli_main.py tests/cli/test_cost_preview.py tests/cli/test_cost_preview_confirm.py tests/orchestration/test_cost_preview.py tests/orchestration/test_job_worktree_integration.py tests/cli/test_job_commands.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/cli/test_job_rerun_subtree.py`, serially, in the
 primary checkout at `aa054d8b`, and read `1683 passed, 7 skipped` at real exit code 0; the seven
 skips are the F252 quarantines. Report every `SKIPPED` line, the node count the round added by
 `--collect-only -q` over the test files it touched, and account for any difference from 1683 plus
 that count — a parametrized guard over the catalog gains nodes for a new command, and those are
 named. Then `python3 -m apps.cli.main integrity check --json`, every check's status and
 `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f029-r3-mutations.py` takes a worktree path, and for
 each mutation below edits the named module INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_job_rerun_subtree.py
 tests/orchestration/test_subtree_rerun_prepare.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and
 last and ends with `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 S1 (a) is skipped;
  m2 S1 (b) never calls `retain_for_recovery`;
  m3 S2 skips a task without a band instead of making the estimate unavailable;
  m4 S2 counts the root task alone;
  m5 S3 prepares the rerun after a declined preview;
  m6 S3 exits 3 for `unknown_task`;
  m7 S3 exits 1 for `job_running`;
  m8 S3 passes no model to `prepare_subtree_rerun`;
  m9 S3 passes `yes=False` to the preview;
  m10 S3 leaves the refusal's `facts` out of the envelope.
 Run it: `git worktree add --detach .remedy-wt/f029-r3-mut <the last commit before C6b>`, then
 `python3 -B .agent/authored/f029-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r3-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, then you add the test that catches it in its own commit and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f029-r3-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.
G6 TREE AND PUSH — after C6b: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`; `git worktree list | wc -l`, which must equal your step 4 reading; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These go in your reply, since C6b cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected, every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per S-item), the deviations, and the next expected action. Report what you ran, not what you
expected. Your Session section reads SESSION 1 of feature F029, round 3, and says in one sentence
how much context you had left. Mark R-1081 as `Landed: R-1081 — <one line>`; never write `Done:`.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003 — the rerun's run-log event with every reader of its name, the attempt fan and
its popover, the browser's command, and the end-to-end proof. State the open-findings count, 1
(R-1081, landed and awaiting review), and the operator-questions count, 0.
