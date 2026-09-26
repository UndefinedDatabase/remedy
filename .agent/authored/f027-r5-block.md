STEP F027 R5 — THE CHANNEL COMMANDS: `job.veto-task` in the catalog, the CLI and the write door, the door's answer of a replan proposal, the answerable inbox card, and R-1067's repair

GOAL
Book round 4's verdict, register R-1067, record DECISION F027 D5, and land it: `remedy job
veto-task <job> <task> --reason <text>` and its write-door twin veto a task through
`task_veto.veto_task_command`, the door refuses a bad reason as a shape before it reads the job,
`decision.resolve` answers a `veto:` proposal from the page, the inbox marks that card answerable,
and the CLI's accept answer names `remedy job run` — with tests and a mutation tool proving they
bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel as
payloads. Read DECISION F027 D5 in `records.diff` before you write code: it is the design.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r5-dry/`, `.remedy-wt/f027-r5-drafts/`, `.remedy-wt/f027-review/` and every
                                  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r5-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
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
   `feature/f027-task-veto`, and `git log --oneline -1` must read `9f884fbb`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 32 | 1194 | 29f5c082baba39c3069ede2fd126ff15e72222dc011bb66b2c84449398834a40 |
| records.diff | 68 | 11691 | 60dd619c796ca3768dc61fbdaafed8103f63b96c7d43060ea3812551ad1b3895 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `9f884fbb`. It appends to `.agent/live_review.md`
round 4's gate entry and R-1067's registration, and to `.agent/decisions.md` DECISION F027 D5.

THE SPECIFICATION
S1 R-1067, in `apps/cli/commands/decision.py`'s `veto:` route: the accept's sentence names
   `remedy job run <job>`, the job's id as the operator typed it, instead of `remedy job resume`.
S2 THE CATALOG, in `apps/cli/command_catalog.py`: a `CommandEntry` `job.veto-task` beside
   `job.edit-task` — group `job`, subcommand `veto-task`, a plain description naming F027,
   `write_metadata`, `supports_json=True`, positional `job_id` and `task` (its help saying the task
   is named by its id in the job or its id in the plan, as `remedy job plan-show` prints them), a
   required option `--reason`, `_JSON_OPT`, `may_mutate_repo=False`, `may_execute_commands=False`,
   related `job.pause`, `job.plan-show` and `decision.resolve`, exit codes 0, 1, 2 and 3 — and
   `"job.veto-task"` joins `UI_EXPOSED_COMMANDS`. `docs/guides/exit-codes.md` gains its row beside
   `remedy job edit-task`'s, reading 3.
S3 THE CLI HANDLER, a NEW module `apps/cli/commands/job_veto_cmd.py` registered in
   `apps/cli/commands/__init__.py` as `job_plan_cmd` is, with `COMMAND_HANDLERS["job.veto-task"]`:
   it loads the job, resolves the task argument with `job_plan_cmd._resolve_task_arg`, calls
   `veto_task_command` with the actor `cli`, and on `vetoed` prints the task, the request id and
   the ids of the tasks that can no longer run (or that none are lost), with `--json` emitting the
   answer's own keys; a refusal fails with its code and detail, exit 2 for `reason_required`,
   `reason_too_long`, `reason_invalid` and `unknown_task`, exit 3 for `job_not_vetoable`,
   `task_not_vetoable` and `task_already_vetoed`, exit 1 for a job that does not exist.
S4 THE DOOR, in `packages/orchestration/ui_server.py`: `JOB_VETO_TASK_COMMAND_ID = "job.veto-task"`;
   in `_read_command_payload`, for that command, `args.task_id` must be a non-empty string and
   `args.reason` must pass `task_veto.validate_veto_reason`, imported inside the method as
   `normalize_steering_text` is, each failure a `_command_field_error` on its field; in
   `_handle_command_submission`, one clause beside the pause's with its write order, its audit and
   its fail-soft publish, calling a NEW door method `_dispatch_veto_task(job, payload)` that imports
   `veto_task_command` inside itself and calls it with the token fingerprint as the actor; a
   `refused` answer is audited `rejected_state` and sent as a 409 whose message names the refusal's
   code and detail. In `_dispatch_decision_resolve`, before the escalation route, a `veto:` id calls
   `veto_proposal.answer_replan_proposal(job, decision_id, answer, actor=<token fingerprint>)`,
   imported inside the method; `answered` is returned as the accepted body and any refusal returns
   None, the existing 409.
S5 THE INBOX, in `packages/orchestration/decision_inbox.py`: `_answerable_by_decision_resolve` gains
   a `veto:` branch, true exactly while the id names a `vetoed_tasks` entry of the job with no
   `veto_answers` entry — the door's own refusal reversed — and a `TaskVetoError` reads false.
S6 THE GUARDS: `tests/ui_server/test_command_channel.py`'s `DOOR_METHODS` gains
   `_dispatch_veto_task` and its `ALLOWED_IMPORTS` exactly
   `("packages.orchestration.task_veto", "veto_task_command")`,
   `("packages.orchestration.task_veto", "validate_veto_reason")` and
   `("packages.orchestration.veto_proposal", "answer_replan_proposal")`, with a comment naming
   DECISION F027 D5; the transitive-forbidden set stays as it is, and if the transitive test goes
   red you stop and report it. `tests/orchestration/test_decision_inbox.py`'s
   `ANSWERABLE_DECISION_TYPES` gains `replan_proposal`. `apps.cli.commands.job_veto_cmd` joins
   `tests/orchestration/import_reachability_allowlist.txt` in its sorted place.

THE TESTS — a NEW FILE at `tests/cli/test_job_veto.py`: a veto by the task's id and by its id in
the plan, the printed request id and unreachable ids, `--json`, each refusal's exit code, a blank
`--reason` refused with nothing written, and the `task_vetoed` event carrying the reason verbatim.
`tests/ui_server/test_command_dispatch.py` gains the door's veto — a 200 with the veto written and
its event, a blank, a too-long and a secret-shaped reason each a 400 on `reason` with no control
file written and no job read, a missing `task_id` a 400, an already vetoed task and a finished job
each a 409 naming the code, the audit line's outcome for each — and the door's answer of a `veto:`
proposal: an accept and a replan each a 200, a second answer and an unknown id each a 409.
`tests/orchestration/test_decision_inbox.py` gains the `veto:` card answerable while open and not
answerable once answered. `tests/cli/test_decision_cmd.py`'s accept test reads `remedy job run`.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r5-block.md`,
  `.agent/authored/f027-r5-plan.md` and `.agent/authored/f027-r5-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R5 C1: copy round 5 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 100. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R5 C2: book round 4, register R-1067, record D5`
  Expected by `git show --numstat`: 48/0 decisions.md, 4/0 live_review.md, 11/11 plan.md.
C3 — R-1067: S1 and its test. Subject: `F027 R5 C3: repair R-1067, name job run for an accepted scope`
C4 — THE CATALOG AND THE CLI: S2 and S3, with the reachability line and `tests/cli/test_job_veto.py`.
  Subject: `F027 R5 C4: job.veto-task in the catalog and the CLI`
C5 — THE DOOR AND THE INBOX: S4, S5 and the rest of S6, with their tests.
  Subject: `F027 R5 C5: the door vetoes a task and answers a replan proposal`
C6 — THE MUTATION TOOL: `.agent/authored/f027-r5-mutations.py`.
  Subject: `F027 R5 C6: the round's red-proof mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, and
  appended to `.agent/live_review.md` a blank line and then exactly one line
  `Landed: R-1067 — <one sentence naming what changed>, at <C3's short SHA>.`, never a `Done:`
  line (docs/agents/planner_reviewer_prompt.md §4 item 4).
  Subject: `F027 R5 C7: rewrite handoff for round 5`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C5a and C5b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r5-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `apps/cli/commands/decision.py`,
   `apps/cli/command_catalog.py`, `apps/cli/commands/job_veto_cmd.py`,
   `apps/cli/commands/__init__.py`, `docs/guides/exit-codes.md`,
   `packages/orchestration/ui_server.py`, `packages/orchestration/decision_inbox.py`,
   `tests/orchestration/import_reachability_allowlist.txt`, `tests/cli/test_job_veto.py`,
   `tests/cli/test_decision_cmd.py`, `tests/ui_server/test_command_dispatch.py`,
   `tests/ui_server/test_command_channel.py`, `tests/orchestration/test_decision_inbox.py`, and
   `.agent/handoff.md`. One widening is allowed and must be declared: a test file that pins, by an
   exact equality, the catalog or the exposed set S2 widens may gain the one new entry. Report the
   list `git diff --name-only 9f884fbb` measures after C7. Do NOT touch
   `packages/orchestration/task_veto.py`, `veto_proposal.py`, `pingpong_job.py`,
   `long_run_executor.py`, `apps/ui/`, `docs/roadmap/`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. Any other existing
   test that goes red because of S1 to S6 is reported with its output, and you stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every worktree `git worktree list` showed at your step 4, and every stash, alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F027 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload the line count, byte count and sha256 you measured against the
 table; then each `.agent/authored/f027-r5-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r5/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 307293 | 6701311c7082de519bd0a555414149dcffd415b9d32fb234bf06887817db0a44 |
 | .agent/decisions.md | 2177395 | 864434df8a8ac0d3b4d2fee6df1e54cc5a6423a0e063b8b53c737cdc8028e03f |
 | .agent/plan.md | 1194 | 29f5c082baba39c3069ede2fd126ff15e72222dc011bb66b2c84449398834a40 |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read `['R-1067']`), and the ledger's last line, which
 must begin `- R-1067 — `.

G3 THE CODE — `python3 -m ruff check` over every Python file of the round's path set at the last
 code commit; `python3 -m apps.cli.main job veto-task --help` at that commit, reported whole; and
 `git diff -U0 <C4> <C5> -- tests/ui_server/test_command_channel.py`, reported whole, which must
 hold exactly S6's door-method name, its three import entries and their comment.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_job_veto.py tests/cli/test_job_plan_cmd.py tests/cli/test_job_pause.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_contracts/test_steering_send_contract.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_veto_proposal.py tests/orchestration/test_task_veto.py tests/cli/test_decision_cmd.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py tests/orchestration/test_event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the round's records, and read `943 passed` at real exit code
 0. Report every `SKIPPED` line, the nodes each new or grown test file contributes
 (`--collect-only -q`), and account for every difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r5-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/cli/test_job_veto.py`, `tests/ui_server/test_command_dispatch.py`,
 `tests/orchestration/test_decision_inbox.py` and `tests/cli/test_decision_cmd.py` from the
 worktree's root after purging its `__pycache__` directories, restores the bytes, and prints one
 line per mutation: its label, the exit code, the failed count and the failing node ids. It runs an
 unmutated control first and last and ends with `restored byte-identical: True` per file and a
 final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each mutation is a behaviour a
 test can see:
  m1 the accept's sentence names `remedy job resume` again;
  m2 the CLI resolves no id in the plan, only the id in the job;
  m3 the CLI exits 2 for `task_already_vetoed`;
  m4 the door's payload check lets a blank reason through to the job;
  m5 the door's payload check is removed for `task_id`;
  m6 the door's clause answers a refused veto with a 200;
  m7 the door's clause passes a fixed actor instead of the token fingerprint;
  m8 the door's `veto:` branch is removed, so the answer falls to the escalation route;
  m9 the inbox's `veto:` branch reads true for an answered proposal.
 Run it in `git worktree add --detach .remedy-wt/f027-r5-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over:
 you then say whether a test can see the behaviour at all, add the test that catches it if one
 can, and re-run the tool. Then `git worktree remove --force .remedy-wt/f027-r5-mut`,
 `git worktree prune`, and `git worktree list`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty; `git log --oneline`
 from `9f884fbb` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F027, round 5, and says in one sentence how much context you had left. Where S1 to S6
leave a choice open, make it, say so in the deviations, and never widen the path set for it
beyond constraint 3's one declared widening.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then T003 — the strike, the reason on hover, the dimmed unreachable set with its link,
the veto affordance and the inbox card's plain-words menu on the page. State the open-findings
count, 1 (R-1067, landed this round and awaiting the reviewer's resolution), and the
operator-questions count, 5.
