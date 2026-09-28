STEP F035 R4 — T003'S FIRST HALF: `remedy job ownership` and the browser's `ownership` read route answer one shared view, and plan edits read in plain verbs

GOAL
Round 3 passed. Book its verdict and record DECISION F035 D4, then land in
`packages/orchestration/ownership_phrases.py` the plain-verb plan-edit sentences and
`ownership_view`; a NEW read-only command `remedy job ownership <job_id> [--json]` in a NEW module
`apps/cli/commands/job_ownership_cmd.py`; and the route `ownership` in the read table of
`packages/orchestration/ui_server.py`. No browser source file, event name or write-door command
changes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S5 below. Only the `.agent/` records travel
as payloads. Read DECISION F035 D4 in the booking diff before you write code. Before you write
anything, read whole: `packages/orchestration/ownership_phrases.py`,
`tests/orchestration/test_ownership_phrases.py` and its golden
`tests/orchestration/fixtures/ownership/golden/sentences.txt`;
`apps/cli/commands/job_steer_cmd.py` and `tests/cli/test_job_steer.py` as the pattern for a job
command and its tests; the `job.steer` entry and `_JOB_ID`, `_JSON_OPT` in
`apps/cli/command_catalog.py`; `apps/cli/commands/__init__.py`; the exit-code table of
`docs/guides/exit-codes.md`; `do_GET`'s `handlers` table and `_build_digest_json` in
`packages/orchestration/ui_server.py`; `tests/ui_server/test_digest_route.py` as the pattern for a
route test; `tests/ui_server/test_handler_table_walk.py`; `tests/cli/test_exit_codes.py`; and
`tests/docs/test_vocabulary.py`, which reads every catalog description for its binding words.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f035-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f035-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f035-r4-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f035-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f035-r4-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f035-ownership-ledger`, and `git log --oneline -1` must read `490a81f4`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f035-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f035-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 55 | 14156 | 0c8dda65eccf2223d8de6c5eacf21d7f92b3737d59331e754588bca17214c6ec |
| plan.md | 28 | 891 | 166499d5d686f7ca8ae76e09ab94c5a77407ea5a16dddefc66bd7f07f4c78067 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the
reviewer generated it with `git diff HEAD` from a tree at `490a81f4`. It appends round 3's gate
entry to `.agent/live_review.md` and DECISION F035 D4 to `.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere. `ownership_phrases.py` still imports only
`ownership` among the orchestration modules.
S1 PLAIN VERBS, in `ownership_sentence`. `V` is `version <n>` where n is the entry's
   `consequence["ref"]` without a leading `v`, or the ref verbatim when it has none; `T` is the
   task phrase, or `a task` when `task_id` is "". A `plan_edited` entry reads by
   `detail["command"]`: `plan_edit_task` → `A changed T in the plan; the plan is now at V.`;
   `plan_edit_acceptance` → `A changed the acceptance checks of T; the plan is now at V.`;
   `plan_delete_task` → `A deleted T from the plan; the plan is now at V.`; `plan_split_task` →
   `A split T in the plan; the plan is now at V.`; `plan_merge_tasks` → `A merged tasks in the
   plan; the plan is now at V.`; `plan_reorder` → `A reordered the plan's tasks; the plan is now
   at V.`; any other command → `A edited the plan (<command>)`, then ` for T` when `task_id` is
   not "", then `; the plan is now at V.` A `task_edited` entry reads `A edited T while the job
   ran; the plan is now at V.` Update the golden's plan-edit lines to these sentences and add one
   golden line for each command above; no other golden line changes.
S2 THE VIEW. `ownership_view(job) -> dict` answers `{"schema": OWNERSHIP_SCHEMA, "job_id":
   str(job.job_id), "entries": [...], "error": ""}`, each entry the ledger's own dict plus the key
   `sentence`, titles from `job.tasks`; on `OwnershipError` or `OSError` from building it,
   `entries` is `[]` and `error` is `f"The ownership ledger could not be read: {exc}"`.
S3 THE COMMAND. A catalog entry directly above the `job rerun-subtree` comment line, under a
   comment line `# ── job ownership (F035 T003, DECISION F035 D4) ─` padded with `─` to the
   width of its neighbours: `command_id="job.ownership"`, `group_id="job"`,
   `subcommand="ownership"`, `description="Show who did what in a job under its mission: every
   recorded action of the operator on the job or one of its tasks, every default the operator
   accepted and every choice Remedy's planner made, one plain sentence each, read from the job's
   own records and never written by this command (F035)."`, `action_class="read_only"`,
   `args=(_JOB_ID, _JSON_OPT)`, `supports_json=True`, `related=("job.show", "job.veto-task",
   "job.steer")`, `exit_codes=(0, 1, 2, 3)`. The module follows `job_steer_cmd.py`: its
   docstring names F035 T003, DECISION F035 D4 and the exit codes; `resolve_job_id_or_fail`
   answers a malformed id with 2; a job whose record `load_job_plan` cannot read fails
   `job_not_found` with 3; a view with an `error` fails `ownership_unreadable` with 1 and the
   error as its message; `--json` emits `emit_ok(job_id=..., schema=..., entries=...)`; the text
   form prints `Who did what in job <id>:` and one line per entry, `  - ` plus its sentence with
   every inner `"\n"` replaced by `"\n    "`, or the one line `No action is recorded for job <id>
   yet.` Register it in `apps/cli/commands/__init__.py` in both places, alphabetically; add the
   row `| \`remedy job ownership\` | 3 |` directly under `remedy job steer`'s row of
   `docs/guides/exit-codes.md`; and add `apps.cli.commands.job_ownership_cmd` to
   `tests/orchestration/import_reachability_allowlist.txt` in its sorted place — stop and report
   if the reachability test names any other module.
S4 THE ROUTE. `_build_ownership_json(job)` returns `ownership_view(job)`, its import
   function-scoped as `_build_digest_json`'s is, and `"ownership": _build_ownership_json` joins
   the `handlers` table directly after `"digest"`. Nothing else in `ui_server.py` changes.
S5 UNCHANGED: `ownership.py`, the report section and the digest's reading, every event name,
   `UI_EXPOSED_COMMANDS`, and every existing test except the golden lines S1 names.

THE TESTS. In `tests/orchestration/test_ownership_phrases.py`: inline assertions of every S1
sentence, of `version 7` for ref `v7`, and of the fallback for an unknown command; the view with a
sentence on every entry, and its error form. NEW `tests/cli/test_job_ownership.py`: the text form
with entries and with none, `--json`'s keys and entries, exit 2 for a malformed id, 3 for an
unknown job and 1 for a ledger that raises, each through the real CLI entry the neighbour tests
use. NEW `tests/ui_server/test_ownership_route.py` after `test_digest_route.py`: 200 with the
view's keys and sentences for a job with an action, 404 for an unknown job, 403 for a wrong
token, and a neighbouring name still unhandled.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f035-r4-block.md` := this block, `.agent/authored/f035-r4-plan.md` := plan.md
  and `.agent/authored/f035-r4-booking.diff` := booking.diff. All by `shutil.copyfile`.
  Subject: `F035 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 83. Report the number you measure.

C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F035 R4 C2: book round 3, record D4, advance the plan`
  Expected by `git show --numstat`: 37/0 decisions.md, 2/0 live_review.md, 6/6 plan.md.

C3 — THE CODE AND ITS GUARD LISTS: `ownership_phrases.py`, `ui_server.py`, the catalog, the new
  command module, `apps/cli/commands/__init__.py`, `docs/guides/exit-codes.md`, the reachability
  list, and the golden's changed lines, so no commit leaves a test red.
  Subject: `F035 R4 C3: remedy job ownership and the ownership route over one view, plain edit verbs`

C4 — THE TESTS AND THE TOOL: the test files and your mutation tool (G5) saved as
  `.agent/authored/f035-r4-mutations.py`.
  Subject: `F035 R4 C4: test the ownership view, command and route, add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F035 R4 C5: rewrite handoff for round 4`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so. A
   split of C3 keeps the golden's changed lines with the S1 code, and the catalog entry with its
   module, registration, exit-code row and reachability line.
3. The round's whole tracked path set is: the `.agent/authored/f035-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/ownership_phrases.py`, `packages/orchestration/ui_server.py`,
   `apps/cli/command_catalog.py`, `apps/cli/commands/job_ownership_cmd.py`,
   `apps/cli/commands/__init__.py`, `docs/guides/exit-codes.md`,
   `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/fixtures/ownership/golden/sentences.txt`,
   `tests/orchestration/test_ownership_phrases.py`, `tests/cli/test_job_ownership.py`,
   `tests/ui_server/test_ownership_route.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 490a81f4` at the branch tip after C5. Do NOT touch
   `packages/orchestration/ownership.py`, `pingpong_job.py`, `job_digest.py`, anything under
   `apps/ui/`, `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` and the
   `remedy/*` branch count are reported afterwards; neither may change.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F035's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f035-r4-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f035-r4/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2335016 | 00dcdd7272a756ca58599ad03c5aaa44124cce450d6d6fed38706ec11970ba62 |
 | .agent/live_review.md | 309756 | d8ab67afee13dd427fbff5d4bbab12c30a2ff06e52edb2c9415e08c8bf57d161 |
 | .agent/plan.md | 891 | 166499d5d686f7ca8ae76e09ab94c5a77407ea5a16dddefc66bd7f07f4c78067 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at C2
 (the reviewer read it empty), and the ledger's last line at C2, which must begin
 `Gate: F035 R3 — `.

G3 THE CODE — `python3 -m ruff check packages/orchestration/ownership_phrases.py
 packages/orchestration/ui_server.py apps/cli/command_catalog.py
 apps/cli/commands/job_ownership_cmd.py apps/cli/commands/__init__.py
 tests/orchestration/test_ownership_phrases.py tests/cli/test_job_ownership.py
 tests/ui_server/test_ownership_route.py` at C4, with its real exit code. Then report
 `git show <C3> -- tests/orchestration/fixtures/ownership/golden/sentences.txt` whole, the
 catalog entry and the handler quoted from `git show <C3>`, and the real output of
 `python3 -m apps.cli.main job ownership --help`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_job_ownership.py tests/ui_server/test_ownership_route.py tests/orchestration/test_ownership_phrases.py tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py tests/orchestration/test_job_digest.py tests/ui_server/test_digest_route.py tests/ui_server/test_handler_table_walk.py tests/ui_server/test_command_channel.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/cli/test_job_steer.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the two new test files, serially, in the primary checkout
 at `490a81f4`, and read `1272 passed, 1 skipped` at real exit code 0; the skip is the F252
 quarantine. Report every `SKIPPED` line and the node counts by `--collect-only -q` of the two new
 files and of `tests/orchestration/test_ownership_phrases.py` at `490a81f4` and at C4, and account
 for the total. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f035-r4-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_ownership_phrases.py tests/cli/test_job_ownership.py
 tests/ui_server/test_ownership_route.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and
 last and ends with `restored byte-identical: True` and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 `ownership_phrases.py`: `plan_delete_task` reads with the unknown-command fallback;
  m2 `ownership_phrases.py`: the version keeps its leading `v`;
  m3 `ownership_phrases.py`: `ownership_view` leaves out each entry's `sentence`;
  m4 `ownership_phrases.py`: `ownership_view` answers an empty `error` when the ledger raises;
  m5 `job_ownership_cmd.py`: an unknown job exits 1 instead of 3;
  m6 `job_ownership_cmd.py`: a ledger error exits 0 and prints nothing;
  m7 `job_ownership_cmd.py`: a job with no entry prints nothing;
  m8 `ui_server.py`: the `ownership` key is left out of the `handlers` table.
 Run it: `git worktree add --detach .remedy-wt/f035-r4-mut <C4>`, then
 `python3 -B .agent/authored/f035-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f035-r4-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f035-r4-mut` and `git worktree prune`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `490a81f4` in that order (more
 lines if constraint 2 split a commit); `git worktree list | wc -l` and the `remedy/*` branch
 count, which must equal your step 4 readings; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F035, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003's second half — the chips at a task's detail, the evidence panel's ownership
tab, and the end-to-end proof. State the open-findings count, 0, and the operator-questions
count, 0.
