STEP F041 R3 — T002's CORE: the preview record and its state machine, the runner of the harness's own verbs, and `remedy job preview-start` and `preview-stop`

GOAL
Round 2 passed at `8130599a`. Book it and R-1105's resolution and record DECISION F041 D3 in one
commit, then land D3 against the reviewer's tests: `packages/orchestration/preview_control.py`
(the record and its state machine, running nothing), `packages/orchestration/preview_runner.py`
(the one place a runtime verb runs) and `apps/cli/commands/job_preview_cmd.py`, wired by the
reviewer's wiring payload.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS AND THE WIRING ARE THE REVIEWER'S AND THE
MODULES ARE YOURS: tests.diff is the acceptance, wiring.diff is applied as it is, and you write
the three modules against both and S1 to S3 below. You never edit a payload; if one looks wrong
to you, STOP and report it. Read DECISION F041 D3 in records.diff before you write code, and read
whole before you write: `apps/cli/commands/job_story_cmd.py` (the command pattern to follow),
`apps/cli/json_envelope.py` (`emit_ok`, `fail`), and in `apps/cli/commands/runtime_cmd.py` the
module docstring and `_cmd_runtime_serve`, `_cmd_runtime_probe` and `_cmd_runtime_stop`, for the
envelopes the verbs answer.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f041-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f041-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f041-r3-dry/`, `.remedy-wt/f041-r3-sim/`, `.remedy-wt/f041-r1-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f041-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script (`subprocess.run(...,
env=...)`), never on a command line. Never run npm or npx. Before every commit, run
`git diff --cached --stat` and confirm the index holds exactly that commit's paths.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f041-artifact-preview`, and `git log --oneline -1` must read `8130599a1`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f041-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f041-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 30 | 11142 | e487b0f2ea688d789214bbf589411b5f4971eaa7831da8bed556d10663cbfadf |
| wiring.diff | 93 | 4941 | bcd1ee4f13db5fe44b6348de4454960d13fd4ae7643a0e82a424d6d4de34fd31 |
| tests.diff | 423 | 18221 | 0b2a8787906ee346c62950be97e500fad77c26c92be5a33a609bd1b6d89a05be |
| plan.md | 28 | 901 | e1c18716b36a70ca6eac6734da1208d1e3188e491426eed8645ffcb29254aadd |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `8130599a1`. `records.diff` appends round 2's
gate entry and R-1105's `Done:` paragraph to `.agent/live_review.md` and DECISION F041 D3 to
`.agent/decisions.md`. `wiring.diff` adds the catalog entries `job.preview-start` and
`job.preview-stop` to `apps/cli/command_catalog.py`, registers `job_preview_cmd` in
`apps/cli/commands/__init__.py`, adds their rows to `docs/guides/exit-codes.md`, and adds the new
modules to `tests/orchestration/import_reachability_allowlist.txt`. `tests.diff` adds the
NEW FILE at `tests/orchestration/test_preview_control.py`, the
NEW FILE at `tests/orchestration/test_preview_runner.py` and the
NEW FILE at `tests/cli/test_job_preview.py`.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `packages/orchestration/preview_control.py`, NEW, importing no process launcher: not
   `subprocess`, not `packages.runtimes`, not `preview_runner`. Module docstring naming F041 T002
   and DECISION F041 D3. Names: `PREVIEW_SCHEMA = "remedy.preview.v1"`, `PREVIEW_FILENAME =
   "preview.json"`, the six `STATE_*` constants and `PREVIEW_STATES` in the order the test pins,
   `ACTIVE_STATES` (starting, probing, live), `ACTION_START`, `ACTION_STOP`, `PREVIEW_ACTIONS`,
   `CONFIG_ERROR_TOKEN = "runtime_config_error"`, a frozen dataclass `VerbResult(ok: bool,
   payload: dict)`, the alias `RuntimeVerb = Callable[[str, Path], VerbResult]`,
   `preview_path(job_id, data_root=None)` = `job_dir(job_id, data_root) / PREVIEW_FILENAME`,
   `load_preview`, `request_preview(job_id, action, *, now, data_root=None)`,
   `run_pending(job, runner, *, now, data_root=None)` and `preview_view(job_id, data_root=None)`.
   The record's keys and the stopped default are exactly those the first test pins; a stored
   record is used only when its `schema` is `PREVIEW_SCHEMA` and its `state` is in
   `PREVIEW_STATES`, each key taken only when its type matches the default's. Writes go through
   `packages.common.secure_fs.durable_write_json`, creating the job directory when absent. Every
   write sets `updated_at` to `now.isoformat()`; `viewed_at` is set to it when a preview goes
   live. The message of a failed verb is its envelope's `message`, else its `error`, else
   "unknown error". Behaviour: D3 (3), as the tests pin it; a job whose `repo_path` is empty or
   not a directory runs no verb and ends `failed` for a start or `stopped` for a stop, with the
   reason "the job has no project folder to run".
S2 `packages/orchestration/preview_runner.py`, NEW. Module docstring naming F041 T002 and
   DECISION F041 D3; it and every comment name the verbs as `remedy runtime serve`,
   `remedy runtime probe` and `remedy runtime stop`, never with a placeholder in place of the verb,
   because `tests/cli/test_advertised_commands.py` refuses a `remedy <group>` line that reaches no
   command. Names: `RUNTIME_VERBS = ("serve", "probe", "stop")`, `VERB_TIMEOUT_SECONDS = 180`,
   `runtime_verb_argv(verb, root)` (ValueError for another verb) and `run_runtime_verb(verb,
   root) -> VerbResult`, which runs that argv with `subprocess.run(..., cwd=<the Remedy checkout,
   parents[2] of the module>, capture_output=True, text=True, timeout=VERB_TIMEOUT_SECONDS,
   check=False)`. Its failures carry `{"error": "runtime_error", "message": ...}` with exactly the
   messages the tests pin; an `OSError` gives "runtime <verb> could not be run: <strerror>".
S3 `apps/cli/commands/job_preview_cmd.py`, NEW, following `job_story_cmd.py`: module docstring
   naming F041 T002, DECISION F041 D3 and the exit codes; `_cmd_job_preview(job_id_str, action, *,
   json_output=False)` resolves the id with `resolve_job_id_or_fail`, answers `job_not_found` at
   exit 3 when `load_job_plan` gives None, then calls `request_preview` and `run_pending` with
   `run_runtime_verb` (imported by name into this module, so the tests can replace it) and
   `datetime.now(timezone.utc)`, and reads `preview_view`. When the state is not `live` for a
   start or `stopped` for a stop it calls `fail(f"preview_{state}", <the reason, else "the preview
   is <state>">, ...)` with `job_id` and the view's keys; otherwise `emit_ok(job_id=..., **view)`
   under `--json`, or prints exactly the sentences the tests pin. `COMMAND_HANDLERS` maps both
   command ids.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — `.agent/authored/f041-r3-block.md` := this block, and `.agent/authored/f041-r3-plan.md`,
  `.agent/authored/f041-r3-records.diff` and `.agent/authored/f041-r3-wiring.diff` := plan.md,
  records.diff and wiring.diff, by `shutil.copyfile`.
  Subject: `F041 R3 C1a: copy round 3 block, plan, records and wiring into .agent/authored/`
  Its insertions are this block's line count plus 151.
C1b — `.agent/authored/f041-r3-tests.diff` := tests.diff.
  Subject: `F041 R3 C1b: copy round 3 tests diff into .agent/authored/`
  Expected insertions: 423.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F041 R3 C2: book round 2 and R-1105's resolution, record D3`
  Expected by `git show --numstat` (insertions and deletions): 10/0 .agent/decisions.md, 4/0 .agent/live_review.md, 7/8 .agent/plan.md.
C3 — THE CODE: S1 to S3 and `git apply` wiring.diff, in one commit, so every new module is
  imported and listed at the same commit. The wiring paths' numstat is expected as 28/0 apps/cli/command_catalog.py, 2/1 apps/cli/commands/__init__.py, 2/0 docs/guides/exit-codes.md, 3/0 tests/orchestration/import_reachability_allowlist.txt. IF
  THIS COMMIT WOULD REACH 500 INSERTIONS, split it in two at this point and no other:
  C3a = `packages/orchestration/preview_control.py` alone, C3b = everything else of C3. Between
  them `tests/test_no_orphan_modules.py` reads `preview_control` as an orphan by construction;
  that is the reviewer's ordering, not a deviation, and you say which you did.
  Subject: `F041 R3 C3: record preview requests and run them through the harness's own verbs`
  (a split uses the same subject with `C3a` and `C3b`).
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F041 R3 C4: add the reviewer's preview state machine, runner and command tests`
  Expected by `git show --numstat`: 111/0 tests/cli/test_job_preview.py, 208/0 tests/orchestration/test_preview_control.py, 86/0 tests/orchestration/test_preview_runner.py.
C5 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f041-r3-mutations.py`.
  Subject: `F041 R3 C5: add the round 3 mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F041 R3 C6: rewrite handoff for round 3`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   names its one split point.
3. The round's whole tracked path set is: the `.agent/authored/f041-r3-*` copies and tool, the
   paths records.diff, wiring.diff and tests.diff edit, `.agent/plan.md`, the three new modules,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only 8130599a1` at
   the branch tip after C6. Do NOT touch `apps/ui/`, `packages/runtimes/`,
   `apps/cli/commands/runtime_cmd.py`, `packages/orchestration/ui_server.py`, `.agent/context.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. Every test tests.diff carries passes against your code unedited, at C4.
5. You write no `Done:` line and no `Landed:` line.
6. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. An EXISTING test that goes red is never edited to pass.
7. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`, and no reset of a pushed commit.
8. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
9. DO NOT run the full suite (amend0917 rule 1). Run no self-use job, no command that calls a
   provider, and never `remedy runtime serve` against a real project: the tests replace the verbs,
   except the one test that serves an empty folder, which the harness refuses before starting
   anything.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f041-r3-*` payload copy byte for
 byte with its source, read back with `git show <commit>:<path>` from the commit that added it.

G2 THE RECORDS, THE WIRING AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named (C3 meaning C3b if you split), equals the
 reviewer's reading from its simulation tree:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2459012 | 623734a9cf069f4551e69afb28c23d7fb837563034149fbccb942586cb5b6018 |
 | .agent/live_review.md | C2 | 300552 | b63dd0d2c35bf6deeccfe075cf8a02d5f8e36c92f4a030a909403600bea1aa34 |
 | .agent/plan.md | C2 | 901 | e1c18716b36a70ca6eac6734da1208d1e3188e491426eed8645ffcb29254aadd |
 | apps/cli/command_catalog.py | C3 | 134211 | 945d42e4412a1154558affd191f2cc8cad464c863a3d325be8193bf65898ae40 |
 | apps/cli/commands/__init__.py | C3 | 2445 | c86f2e8aa8d0cd08106cd1394b81cab96200a1968c6771765987a89341d87da5 |
 | docs/guides/exit-codes.md | C3 | 4671 | e70b37764952ec34acae496f11602003ca912013c7a1237150eb5528128eefcf |
 | tests/orchestration/import_reachability_allowlist.txt | C3 | 11130 | c3d07831a2f25353c41f97dee3731d1b7e9f1910f6ff27ee0ebe84c60f735ccf |
 | tests/orchestration/test_preview_control.py | C4 | 9157 | dc1e5263fda6e029f132a86bdd846304c45b699dd9b20571b67186ca5e829d05 |
 | tests/orchestration/test_preview_runner.py | C4 | 3452 | 8697f11ab7c7eee4f377cd298bd4ac808bf6550354c2d5bcc8cecdded3f6ca6b |
 | tests/cli/test_job_preview.py | C4 | 4554 | 383534a9c1a07e07932d85c77d10bc09d308092a4d2f6cefee269b96d707d141 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show`, at `8130599a1` and at
 C2 (the reviewer read `['R-1105']` and `[]`).

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/preview_control.py
 packages/orchestration/preview_runner.py apps/cli/commands/job_preview_cmd.py
 apps/cli/commands/__init__.py apps/cli/command_catalog.py
 tests/orchestration/test_preview_control.py tests/orchestration/test_preview_runner.py
 tests/cli/test_job_preview.py .agent/authored/f041-r3-mutations.py` at C5, with its real exit
 code. Report the three new modules at C3 (C3b), whole. Then, in the primary checkout at C5,
 SERIALLY (it takes about ten minutes):
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_preview_control.py tests/orchestration/test_preview_runner.py tests/cli tests/docs tests/test_subprocess_timeouts.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/ui_server/test_command_channel.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it serially in its simulation tree, which carries C2, the wiring, the tests and
 its own version of S1 to S3 but no `.agent/authored/f041-r3-*` copy, and read `2754 passed, 1 skipped` at
 real exit code 0, the skip being `SKIPPED [1] tests/test_agent_tooling.py:43`, the D12
 quarantine. Report your count, every `SKIPPED` line, and the node counts of the three new test
 files by `--collect-only -q` (the reviewer's read 16, 9 and 7). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f041-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its FROM
 text occurs exactly once there), runs `python3 -B -m pytest -q -p no:cacheprovider <the test file
 named>` with the worktree as the working directory and its root first on `PYTHONPATH` (through
 `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation: its label,
 the exit code and the failed count. It runs an unmutated control of each test file the
 mutations name first and last, reports `restored byte-identical: True` after each restore, and
 ends with `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  p1 a start records the serve's answer as the probe's, never running the probe
     (test_preview_control.py);
  p2 a failed probe no longer stops the runtime (same file);
  p3 a serve the harness cannot configure is recorded `failed`, not `not_applicable` (same file);
  p4 a start while live puts the record back to `starting` (same file);
  p5 a stored record is used whatever its `schema` (same file);
  p6 `run_runtime_verb` believes an ok envelope at a non-zero exit (test_preview_runner.py);
  p7 `run_runtime_verb` passes no `timeout` (same file);
  p8 the command never fails, whatever the state (tests/cli/test_job_preview.py).
 Run it: `git worktree add --detach .remedy-wt/f041-r3-mut <C5>`, then
 `python3 -B .agent/authored/f041-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r3-mut`
 and report its whole output. EVERY mutation must exit non-zero; one that stays green is reported
 as green and you STOP, because the tests are the reviewer's. Then
 `git worktree remove --force .remedy-wt/f041-r3-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G5 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8` (one more if C3 was split), which must show C6, C5, C4, C3, C2, C1b,
 C1a and `8130599a1` in that order; `git worktree list | wc -l`, which must equal your step 4
 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for the new modules and C5),
every gate's real output and exit code, the authored-text proofs, the item-status table AGENTS.md
requires (one row per commit and per gate), the deviations, and the next expected action. Your
Session section reads SESSION 1 of feature F041, round 3, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then the door's preview commands with the server-side step acting on them. State the
open-findings count, 0, and the operator-questions count, 1.
