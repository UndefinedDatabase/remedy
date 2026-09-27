STEP F028 R9 — BOOK ROUND 8 AND RESOLVE R-1079, AND LAND THE END-TO-END PROOF: a task injected into a paused job through the live write door and through `remedy job inject --yes`, run in the same job, its origin shown on the dashboard, in the stream, in the edit log and in the final report

GOAL
Round 8 passed. Book its gate entry and R-1079's resolution. Then prove T003's end to end with a
live test in the shape of `tests/ui_server/test_task_veto_e2e_live.py`: a job paused after its
first task takes an injected task through the real write door (draft, then confirm) and, in a
second test, through `remedy job inject --yes`; the next `job run` executes it in the same job;
and its provenance is read back from the job record, the edit log, the stream, the dashboard and
the final report. This round changes no production code.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. You write the test yourself against THE TEST below.
Read `tests/ui_server/test_task_veto_e2e_live.py` whole first: this round's file copies its
helpers, per that file's own header rule, rather than importing them.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r9-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r9/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/` to `.remedy-wt/f028-r9-sim/`  The reviewer's simulation trees.
  `.remedy-wt/f028-review/`       The reviewer's scripts and render harness; do not touch them.
  `.remedy-wt/f028-r9-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f028-task-injection`, and `git log --oneline -1` must read `beea934f`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r9/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r9-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 28 | 1049 | cb4f63eaf6180c0bbd83009fb158cf8dad9d075b64649ddb1c415ab1a17bb369 |
| records.diff | 12 | 7510 | b91ce50f4da5ea7f8676db12c0242e550a08eff7f9be4628f83fe4bd1448f283 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; it appends
round 8's gate entry and R-1079's `Done:` paragraph to `.agent/live_review.md`.

THE TEST — NEW FILE at `tests/ui_server/test_task_injection_e2e_live.py`, its docstring naming
F028 T003 and DECISIONS F028 D2, D5, D6 and D8, one class marked `@pytest.mark.subprocess`, over
an APPROVED two-task plan A then B (B depending on A), saved directly as the veto file saves its
diamond, each task's `files_hint` naming `docs/README.md`, and a repository made by that file's
`_make_repo`. The planner is `packages.orchestration.task_injection.injection_call_fn`,
monkeypatched in the test's own process to answer a call function that returns one valid
`task_injection_draft_v1` object (title, goal, one acceptance line, band `S`, `files_hint`
`["docs/README.md"]`, a rationale); the write door and `apps.cli.grouped.main` run in that same
process, while every `job run` is a `python3 -m apps.cli.main` subprocess as in the veto file.
(a) THE DOOR PATH. Run 1, `job run <id> --builder-provider fake --reviewer-provider fake --tasks
    1`, leaves the job `paused` with A applied and B pending. Through a live door: `job.inject`
    with a text and `after` set to A's OWN task id answers 200 `drafted`, its placement's
    `depends_on` `["A"]` and basis `stated`; `job.inject-confirm` with its token answers 200
    `confirmed`; and the dashboard's tasks still hold no task whose `origin` is
    `human_injected`. Run 2, `job run <id> --tasks 0`, exits 0 and leaves the job `completed`
    with three tasks all applied; the new task's `inputs["plan"]` carries `origin`
    `human_injected` and `plan_rationale` `placed after A because you named it`; the plan's edit
    log ends with one `plan_add_task` entry whose `injection` block names the draft and reads
    `confirmed_unseen` False; the run log holds exactly one `task_injected` event, outcome
    `applied`, naming the new entry's task id; the run report, which a `job run` job shows as
    the `report` section of `python3 -m apps.cli.main job show <id> --full` (a subprocess, as
    the runs are; DECISION F261 D10), holds ` — added by you while the job ran` on exactly one
    line, the new task's; and through a live door again the dashboard names that task's
    `origin` `human_injected` and every other task's `""`, and the events stream holds exactly
    one `task_injected` frame.
(b) THE COMMAND LINE PATH. A fresh job, run 1 as in (a); then `apps.cli.grouped.main(["job",
    "inject", <id>, <text>, "--yes", "--json"])` in the test's process, with `REMEDY_DATA_DIR`
    set through `monkeypatch.setenv`, exits 0 with stdout ONE JSON document carrying `draft` and
    `confirmation`; run 2 completes the job with three tasks applied; the edit log's `injection`
    block reads `confirmed_unseen` True; and the report section of `job show <id> --full` holds
    the clause on the new task's line exactly once.

BUNDLE — the commits are C1 to C5, in this order.
C1 — copy this block and the payloads: `.agent/authored/f028-r9-block.md`,
  `.agent/authored/f028-r9-records.diff`, `.agent/authored/f028-r9-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R9 C1: copy round 9 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 40; STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R9 C2: book round 8, resolve R-1079`
  Expected by `git show --numstat`: 4/0 live_review.md, 8/9 plan.md.
C3 — THE TEST. Subject: `F028 R9 C3: prove an injection end to end through the door and the command line`
C4 — THE TOOL: `.agent/authored/f028-r9-probes.py`. Subject: `F028 R9 C4: add the round 9 probe tool`
C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R9 C5: rewrite handoff for round 9`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`; a commit that would reach it
   is split into parts with their own subjects, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r9-*` copies and tool,
   `.agent/live_review.md`, `.agent/plan.md`, `tests/ui_server/test_task_injection_e2e_live.py`,
   and `.agent/handoff.md`. Report the list `git diff --name-only beea934f` measures after C5.
   Touch nothing else — in particular no production file: a red this test shows in production
   code is reported and you stop.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. The test this
   round writes may be corrected before C5, and the correction is declared. Any other existing
   test that goes red is never edited; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F028 one full-suite run, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table; then compare each `.agent/authored/f028-r9-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r9/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 337093 | 038cc36f4b134dea3c13cbf4ee4fc8ae9c936b91ead44bda2b7039e9c2b61a16 |
 | .agent/plan.md | 1049 | cb4f63eaf6180c0bbd83009fb158cf8dad9d075b64649ddb1c415ab1a17bb369 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `beea934f` and at C2 (the reviewer read `['R-1079']` and `[]`), and `git diff --name-only <C1>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check tests/ui_server/test_task_injection_e2e_live.py` at C4, with
 its real exit code.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_task_injection_e2e_live.py tests/ui_server/test_task_veto_e2e_live.py tests/ui_server/test_task_edit_e2e_live.py tests/orchestration/test_task_injection_runner.py tests/cli/test_job_inject.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_run_report.py tests/ui_server/test_dashboard_task_origin.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the new file, serially, in the primary checkout at
 `beea934f`, and read `607 passed` at real exit code 0. Report every `SKIPPED` line and account
 for any difference from 607 beyond the new file's nodes. Then
 `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0.

G5 THE REACH OF THE TEST — the test is what this round ships, so prove it can fail where the
 feature breaks. Your tool `.agent/authored/f028-r9-probes.py` takes a worktree path and, for each
 probe below, edits the named file INSIDE that worktree (asserting its FROM text occurs exactly
 once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_server/test_task_injection_e2e_live.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per probe: label, exit code,
 failed count, failing node ids. An unmutated control runs first and last; it ends with
 `restored byte-identical: True` per file and `ALL PROBES CAUGHT AND RESTORED CLEANLY: <bool>`.
  p1 `_origin_clause` answers "" (packages/orchestration/run_report.py);
  p2 the dashboard's `_task_origin` answers "" (packages/orchestration/ui_server.py);
  p3 `_fold_task_injections` answers False before it reads any confirmation
     (packages/orchestration/pingpong_job.py).
 Run it: `git worktree add --detach .remedy-wt/f028-r9-mut <C4>`, then
 `python3 -B .agent/authored/f028-r9-probes.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r9-mut`
 and report its whole output. EVERY probe must be red on both tests where it applies; one that
 stays green is reported, and you then tighten the test before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r9-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, empty; `git log --oneline -n 6`, showing
 C5 back to C1 and `beea934f` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4), every gate's
real output and exit code, the authored-text proofs, the item-status table AGENTS.md requires
(one row per commit and per gate), the deviations, and the next expected action. Your Session
section reads SESSION 1 of feature F028, round 9, and says in one sentence how much context you
had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 9, then the closure sequence (docs/roadmap/STATUS_closure_protocol.md). State the
open-findings count, 0, and the operator-questions count, 0.
