STEP F027 R9 — T003 LAST: the diamond end-to-end through the real CLI and a live write door, both answers carried to their effects — and R-1069's and R-1070's repair

GOAL
Book round 8's verdict, register R-1069 and R-1070, add one prose-slip line, record DECISION F027
D9, repair both findings, and land `tests/ui_server/test_task_veto_e2e_live.py`: a veto filed through
a live write door on a diamond job the task cap paused after its first task, the run finished through
the real CLI to a blocked end that names the veto, the replan proposal answered through the door both
ways and carried to its effect — with a mutation tool proving the end-to-end bites.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE CHANGE IS SPECIFIED, NOT SLICED: you write the code
and tests yourself against S1 to S3 below. Only the `.agent/` records travel as payloads. Read
DECISION F027 D9 in `records.diff` before you write the test: its CONTEXT holds every state the
reviewer measured through the real CLI and door at `46305052`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r9-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r9/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r9-drafts/`, `.remedy-wt/f027-r8-dry/`, `.remedy-wt/f027-r8-render/`,
  `.remedy-wt/f027-review/` and every older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r9-worker/`    YOURS for logs, scripts and scratch configs; create it if
                                  absent. All are gitignored. You may copy round 8's
                                  `.remedy-wt/f027-r8-worker/` helpers into it.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx; the one Node binary you may run is
`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest`, and only as G5 orders it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f027-task-veto`, and `git log --oneline -1` must read `46305052`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r9/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r9-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 29 | 1078 | ed20409e81fc200bde9d7d31a2b6abc63864e9e4e9caa3a737a5e4772140a81a |
| records.diff | 72 | 14549 | bdd17b382d5cf28c5d051a3acd547c20c66a7d3f00e9e6f96ae770588aefcf8a |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `46305052`. It appends to `.agent/live_review.md`
round 8's gate entry and the registrations of R-1069 and R-1070, one line to
`.agent/prose_slips.md`, and to `.agent/decisions.md` DECISION F027 D9.

THE SPECIFICATION
S1 R-1069, as its FIX states: in `docs/ui/design_reference/assumption_log.md`, the F027 row for
   `ForceBrainGraph.tsx` keeps every cell but its technical reason, whose clause about a markup rule
   becomes the real reason in plain words — an operator-typed reason handed to the library as a
   string would be read as markup; and in `apps/ui/src/api/vetoView.ts` the comment above
   `vetoAnswerSentence` names `veto_proposal.py` and `task_veto.REPLAN_PROPOSAL_OPTIONS` instead of
   `escalation.py`. No other line of either file changes.
S2 R-1070, as its FIX states: in `DetailPopover.tsx`'s Veto section the paragraph
   `Will not run because of this veto:` renders only in the branch that lists at least one task, and
   `tests/ui_contracts/test_veto_controls_contract.py` gains a test that the lead-in's text sits
   inside that branch and not before the length check.
S3 THE END-TO-END, a NEW FILE at `tests/ui_server/test_task_veto_e2e_live.py`, marked
   `@pytest.mark.subprocess`, structured as `tests/ui_server/test_task_edit_e2e_live.py` and keeping
   its OWN copies of that file's plan, server, POST and events-since helpers per its header rule. A
   saved, approved diamond plan: A; B and C each depending on A; D depending on B and C; every task's
   `files_hint` `docs/README.md`; plan order A, B, C, D. The reason is the exact string
   `Duplicates the <auth> work & its "legacy" path`. Two tests:
   (a) THE ACCEPT PATH. Run 1, `job run <id> --builder-provider fake --reviewer-provider fake
   --tasks 1` in a subprocess: exit 0, the job `paused`, A `applied_to_job_workspace`, B, C and D
   `pending`. A live server: `job.veto-task` for B answers 200 with `outcome` `vetoed`, the reason
   byte for byte and `unreachable` equal to `[D]`; the `dashboard` endpoint's `vetoes` section holds
   one entry whose reason is byte for byte the string and whose `unreachable_task_ids` is `[D]`, and
   its `vetoable_task_ids` omit B; the `decisions` endpoint holds exactly one open `veto:` decision,
   of type `replan_proposal`, whose `safe_summary` holds the reason byte for byte. Run 2, `job run
   <id> --tasks 0`: exit 0, stdout holding the line `Vetoed by <the door's actor>: <reason>` with the
   actor the door answered, the job `blocked` with the error `all_remaining_work_vetoed: vetoed <B>;
   unreachable <D>`, A and C `applied_to_job_workspace`, B `vetoed`, D `skipped`, and `metadata`'s
   `veto_terminal` `{"vetoed": [B], "unreachable": [D], "settled": False}`. A live server:
   `events-since` holds exactly one `task_vetoed` frame, for B; `decision.resolve` of the `veto:`
   decision with `accept_reduced_scope` answers 200 with `outcome` `answered` and an empty
   `follow_up_job_id`. Run 3, `job run <id>`: exit 0, the job `completed` with an empty error, B still
   `vetoed`, D still `skipped`, and `veto_terminal` settled with `answers` `{B: "accept_reduced_scope"}`.
   The `task_vetoed` event's `metadata["reason"]` in the job's run log, read from disk, is byte for
   byte the string.
   (b) THE REPLAN PATH. A second such job; a live server's `job.veto-task` for B before any run;
   run 1 with the fake providers: exit 0, the job `blocked`. A live server: `decision.resolve` with
   `replan_follow_up` answers 200 with a non-empty `follow_up_job_id`; that job's record reads
   status `pending`, `tasks` `[]`, and `metadata["replan_of"]` naming the original job, B and the
   request id, and its `user_prompt` holds the reason byte for byte; the `decisions` endpoint no
   longer lists the `veto:` decision as open. Run 2 of the original: exit 0, the job `completed`
   with `answers` `{B: "replan_follow_up"}`; the follow-up's record still reads status `pending`
   with `tasks` `[]`.
   Every server-side read sets `REMEDY_DATA_DIR` in `os.environ` and pops it in a `finally`, as the
   pattern does; every subprocess has a timeout.

BUNDLE — the commits are C1 to C6, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r9-block.md`,
  `.agent/authored/f027-r9-plan.md` and `.agent/authored/f027-r9-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R9 C1: copy round 9 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 101. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R9 C2: book round 8, register R-1069 and R-1070, record D9`
  Expected by `git show --numstat`: 41/0 decisions.md, 6/0 live_review.md, 9/10 plan.md,
  1/0 prose_slips.md.
C3 — R-1069 and R-1070: S1 and S2, then append to `.agent/live_review.md` a blank line and
  `Landed: R-1069 — <one sentence>, at this round's C3.`, a blank line and `Landed: R-1070 — <one
  sentence>, at this round's C3.` — never a `Done:` line.
  Subject: `F027 R9 C3: repair R-1069 and R-1070`
C4 — THE END-TO-END: S3. Subject: `F027 R9 C4: the diamond veto end to end through the CLI and the door`
C5 — THE MUTATION TOOL: `.agent/authored/f027-r9-mutations.py`.
  Subject: `F027 R9 C5: the round's red-proof mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F027 R9 C6: rewrite handoff for round 9`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r9-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `.agent/handoff.md`, `docs/ui/design_reference/assumption_log.md`, `apps/ui/src/api/vetoView.ts`,
   `apps/ui/src/components/detail/DetailPopover.tsx`,
   `tests/ui_contracts/test_veto_controls_contract.py` and
   `tests/ui_server/test_task_veto_e2e_live.py`. Report the list `git diff --name-only 46305052`
   measures after C6. Do NOT touch `packages/`, `apps/cli/`, any other file under `apps/ui/`,
   `tests/conftest.py`, `.agent/context.md`, `.agent/candidates.md` or
   `.agent/operator_questions.md`. If the end-to-end finds the product behaving other than D9's
   CONTEXT measured, that is a finding for the reviewer: STOP and report it, never change `packages/`.
4. If a gate goes red on a test this round did not write, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back with the tree clean: a draft
   you cannot verify is saved as a patch under your own directory and removed from the tree. A
   test this round itself wrote that is wrong may be corrected inside the path set, in its own
   commit, and declared. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every worktree `git worktree list` showed at your step 4, and every stash, alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F027 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload the line count, byte count and sha256 you measured against the
 table; then each `.agent/authored/f027-r9-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r9/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 323564 | 9b6ffe9a52a061a53e0daea8b4f11a3485dac34b2e5fec02c5ecf477f7b580bd |
 | .agent/decisions.md | 2192648 | 0484cfb7ef66eac6543ec5c7b8b11b7626487871c28ed7399ca5e527c3cd60a4 |
 | .agent/prose_slips.md | 369727 | 8f881e35241059245a03c186880e4a036b0fd72b1da8525815356f4565e7d12b |
 | .agent/plan.md | 1078 | ed20409e81fc200bde9d7d31a2b6abc63864e9e4e9caa3a737a5e4772140a81a |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read `['R-1069', 'R-1070']`).

G3 THE CODE — `python3 -m ruff check tests/ui_server/test_task_veto_e2e_live.py
 tests/ui_contracts/test_veto_controls_contract.py` at the last code commit, and the `SKIPPED`
 lines of G4, which must name none of the round's own tests and no TypeScript, lint or vitest node.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_task_veto_e2e_live.py tests/ui_server/test_task_edit_e2e_live.py tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_veto_proposal.py tests/orchestration/test_test_runner.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 It must read no failure. Report every `SKIPPED` line, the nodes the new file contributes
 (`--collect-only -q`), and the new file's own wall time from `--durations=0` in a second run over
 it alone. Then `python3 -m apps.cli.main integrity check --json`, which must read all six `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r9-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/ui_server/test_task_veto_e2e_live.py` and `tests/ui_contracts/test_veto_controls_contract.py`
 from the worktree's root after purging its `__pycache__` directories, restores the bytes, and prints
 one line per mutation: its label, the exit code, the failed count and the failing test names. It
 runs an unmutated control first and last and ends with `restored byte-identical: True` per file and
 a final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations:
  m1 the linear runner dispatches a task unreachable behind a veto (`pingpong_job.py`);
  m2 `format_job_report_text` drops the `Vetoed by` line;
  m3 `_build_veto_section` reports no veto entry (`ui_server.py`);
  m4 the runner's terminal accounting treats an answered veto as unanswered, so the job never
     settles (`pingpong_job.py`);
  m5 answering `replan_follow_up` creates no follow-up job (`veto_proposal.py`);
  m6 the Veto section's lead-in renders before the length check again (`DetailPopover.tsx`).
 Run it in `git worktree add --detach .remedy-wt/f027-r9-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over:
 you then say whether a test can see the behaviour at all, add the test that catches it if one
 can, and re-run the tool. Then `git worktree remove --force .remedy-wt/f027-r9-mut`,
 `git worktree prune`, and `git worktree list`; and `git status --porcelain` must be empty.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty; `git log --oneline`
 from `46305052` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 2
of feature F027, round 9, and says in one sentence how much context you had left. Where S1 to S3
leave a choice open, make it, say so in the deviations, and never widen the path set for it.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 9, then F027's closure sequence. State the open-findings count, 2 (R-1069 and R-1070, landed
this round and awaiting the reviewer's resolution), and the operator-questions count, 5.
