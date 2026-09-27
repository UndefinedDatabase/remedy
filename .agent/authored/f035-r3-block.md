STEP F035 R3 — T002: one phrase catalog turns every ownership entry into a plain sentence; the job report gains an Ownership section and loses its per-task `Vetoed by` line; the digest's `ownership` key carries the sentences

GOAL
Round 2 passed. Book its verdict and record DECISION F035 D3, then land T002: a NEW module
`packages/orchestration/ownership_phrases.py`, the only place a sentence about who did what is
worded; the report's Ownership section in `format_job_report_text`; the digest's `ownership`
sentences in `build_job_digest`; the golden sentences; and the three test assertions that read
the deleted `Vetoed by` line re-pointed at the sentence. No command, event name or browser code
changes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S5 below. Only the `.agent/` records travel
as payloads. Read DECISION F035 D3 in the booking diff before you write code. Before you write
anything, read whole: `packages/orchestration/ownership.py`; `format_job_report_text` and
`_write_ownership_ledger_at_run_end` in `packages/orchestration/pingpong_job.py`;
`packages/orchestration/job_digest.py`; the replan sentence in
`packages/orchestration/veto_proposal.py` (search `You vetoed`);
`tests/orchestration/test_job_digest.py` and its fixtures under
`tests/orchestration/fixtures/job_digest/`; `tests/orchestration/test_pingpong_job_ownership.py`;
and every assertion naming `Vetoed by` in `tests/orchestration/test_task_veto_runner.py` and
`tests/ui_server/test_task_veto_e2e_live.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f035-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f035-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f035-r3-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f035-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f035-r3-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f035-ownership-ledger`, and `git log --oneline -1` must read `3a8b1259`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f035-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f035-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 60 | 13447 | 7ee16eec4950baaee19dfc2eb2d9a1bbf69b77a22d8e80bdf3b49edd494914c7 |
| plan.md | 28 | 861 | 32b26c6240876bf5b85c8f962963ec53f77efdcb2fae3e250a00da7e734ae5f8 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the
reviewer generated it with `git diff HEAD` from a tree at `3a8b1259`. It appends round 2's gate
entry to `.agent/live_review.md` and DECISION F035 D3 to `.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere. `ownership_phrases.py` imports only
`ownership` among the orchestration modules, reads no file and no clock. In the sentences below
`A` is the actor phrase, `T` the task phrase of the entry's `task_id`, `R` the reason clause —
` — reason: “<text>”` when `text` is not "" and nothing otherwise — and every other `“…”` holds
the named field verbatim, never cut. `ids` is a list joined with `", "`.
S1 THE ACTOR — `ownership_actor_phrase(actor) -> str`, first match wins:
   `auto_approved` → `You (auto-approved via --yes)`; kind `default_policy` → `The default policy
   (you accepted at plan approval)`; kind `remedy` → `Remedy's <recorded_as> (under this job's
   configuration)`; door `browser` with `token_number` n > 0 → `You (browser, token #<n>)`; door
   `browser` → `You (browser)`; door `cli` → `You (command line)`; `recorded_as` "" or `human` →
   `You`; otherwise `You (recorded as <recorded_as>)`.
S2 THE TASK — `task <id>`, followed by ` (<title>)` when the `titles` mapping holds a non-empty
   title for that id different from the id. `Tc` is the same with a capital `T`.
S3 THE SENTENCES — `ownership_sentence(entry, titles=None) -> str`, one per action, exactly:
   `task_vetoed`: `A vetoed T R.` then, for consequence kind `unreachable` with n ids, ` <n>
   downstream task could not run: ids.` (`tasks` when n is not 1), and for kind `inert`, ` The
   veto took no effect: <ref>.` — `veto_answered`: `A answered the replan proposal for T: <text>.`
   then ` The follow-up job is <ref>.` when `ref` is not "" — `task_injected`: `A added a task:
   “<text>”.` then, by consequence kind, `task_added` ` It became <T of task_ids[0]>.`, `inert`
   ` It was not added: <ref>.`, `not_folded` ` It waits for the next safe point.` —
   `subtree_rerun`: `A reran T and the tasks that depend on it: ids.` then ` Model override:
   <m>.` when `detail["model_override"]` is not "" — `plan_edited`: `A edited the plan
   (<command>)` then ` for T` when `task_id` is not "", then `; the plan is now <ref>.` —
   `task_edited`: `A edited T while the job ran (<command>); the plan is now <ref>.` —
   `steering_sent`: `A sent a steering message: “<text>”.` then ` <Tc of task_ids[0]> took it in
   at <ref>.` when consumed, else ` No task has taken it in yet.` — `note_sent`: `A sent a note to
   T: “<text>”.` then ` It was taken in at <ref>.` when consumed, else ` The task has not taken it
   in.` — `job_paused`: `A paused the job R.` then ` Withheld: ids.` when there are ids —
   `task_paused`: `A paused T R.` — `job_resumed`: `A resumed the job.` — `task_resumed`: `A
   resumed T.` — `job_stopped`: `A stopped the job R.` — `hunk_approved`: `A approved hunk
   <hunk_id> of T.` — `hunk_rejected`: `A rejected hunk <hunk_id> of T R.` —
   `decision_answered`: `A answered “<question>” for T: “<text>”.` — `clarification_answered`:
   `A answered the plan question “<question>”: “<text>”.` — `plan_approved`: `A approved the
   plan.` — `plan_rejected`: `A rejected the plan.` In every template `T R.` means no space
   before `R`. An action with no template raises `OwnershipError`. `ownership_sentences(ledger,
   titles=None) -> list[str]` maps the ledger's entries in order. The module docstring names F035
   T002 and DECISION F035 D3 and says the catalog is the one place this dialect is worded.
S4 THE REPORT, in `format_job_report_text`: after the blank line that ends the task list, build
   the ledger once; with entries, append `Ownership:`, one line per sentence (titles from
   `job.tasks`) as `  - ` plus the sentence with every inner `"\n"` replaced by `"\n    "`, and a
   blank line; with none, append nothing; on `OwnershipError` or `OSError`, append
   `Ownership: the ledger could not be read — <error>` and a blank line. DELETE the per-task
   `Vetoed by` line; `_task_veto_report_map` stays, `export_job_report` still reads it, and the
   `Paused by` line stays unchanged.
S5 THE DIGEST, in `build_job_digest`: `ownership` becomes the sentences, titles from `job.tasks`,
   for a job that is a `JobPlan`; `[f"The ownership ledger could not be read: {exc}"]` on
   `OwnershipError` or `OSError`; `[]` for anything else. Imports of `pingpong_job` and the two
   ownership modules are function-scoped. The comment above the key is rewritten to say this,
   naming DECISION F035 D3; `JOB_DIGEST_VERSION` does not change.

THE TESTS. NEW `tests/orchestration/test_ownership_phrases.py` with NEW golden
`tests/orchestration/fixtures/ownership/golden/sentences.txt`: a hand-built ledger of at least one
entry per action and per consequence kind above, rendered one sentence per line and compared to
the golden byte for byte, BESIDE inline assertions (DECISION F040 D6) of every S1 phrase, of the
reason clause's absence for an empty reason, of a multi-line note kept verbatim, of a title shown
and of one not known, and of `OwnershipError` for an unknown action. In
`tests/orchestration/test_pingpong_job_ownership.py`: a report with the section in ledger order,
no section for a job with no entry, the error line, and no `Vetoed by` for a vetoed task. In
`tests/orchestration/test_job_digest.py`, APPENDED tests only: a job with entries carries the
sentences, a raising ledger gives the one sentence, and a non-`JobPlan` keeps `[]`; its existing
tests stay as they are. Re-point, and change nothing else in them: the two `Vetoed by <actor>:`
assertions of `tests/orchestration/test_task_veto_runner.py` and the one of
`tests/ui_server/test_task_veto_e2e_live.py` each assert the exact report line the catalog gives
for that veto, written out as a literal that holds the reason; the absence assertion stays.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f035-r3-block.md` := this block, `.agent/authored/f035-r3-plan.md` := plan.md
  and `.agent/authored/f035-r3-booking.diff` := booking.diff. All by `shutil.copyfile`.
  Subject: `F035 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 88. Report the number you measure.

C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F035 R3 C2: book round 2, record D3, advance the plan`
  Expected by `git show --numstat`: 42/0 decisions.md, 2/0 live_review.md, 7/9 plan.md.

C3 — THE CODE: `packages/orchestration/ownership_phrases.py`,
  `packages/orchestration/pingpong_job.py`, `packages/orchestration/job_digest.py`,
  `tests/orchestration/import_reachability_allowlist.txt` (the one line
  `packages.orchestration.ownership_phrases` in its sorted place — stop and report if the
  reachability test names any other module), and the three re-pointed test files, so no commit
  leaves a test red.
  Subject: `F035 R3 C3: word every ownership entry in one catalog, in the report and the digest`

C4 — THE TESTS AND THE TOOL: the phrase test and its golden, the appended tests, and your mutation
  tool (G5) saved as `.agent/authored/f035-r3-mutations.py`.
  Subject: `F035 R3 C4: golden ownership sentences, report and digest tests, mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F035 R3 C5: rewrite handoff for round 3`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so. A
   split of C3 keeps the deletion of the `Vetoed by` line and the three re-pointed assertions in
   ONE part.
3. The round's whole tracked path set is: the `.agent/authored/f035-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the three production files of
   C3, `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/test_ownership_phrases.py`,
   `tests/orchestration/fixtures/ownership/golden/sentences.txt`,
   `tests/orchestration/test_pingpong_job_ownership.py`, `tests/orchestration/test_job_digest.py`,
   `tests/orchestration/test_task_veto_runner.py`, `tests/ui_server/test_task_veto_e2e_live.py`,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only 3a8b1259` at
   the branch tip after C5. Do NOT touch `packages/orchestration/ownership.py`, anything under
   `apps/` or `docs/`, `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red, other than the three assertions this block orders re-pointed, is
   never edited to pass; report it and stop.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f035-r3-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f035-r3/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2331973 | 674b30c8c3e0bf6667c4704413111e7c86124d37acb214b963260b376493f42a |
 | .agent/live_review.md | 306286 | be6c3e6a38b2d6dd0c6075684fa7e47ecd21f9454ea82fecb439aa990aedc4ed |
 | .agent/plan.md | 861 | 32b26c6240876bf5b85c8f962963ec53f77efdcb2fae3e250a00da7e734ae5f8 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at C2
 (the reviewer read it empty), and the ledger's last line at C2, which must begin
 `Gate: F035 R2 — `.

G3 THE CODE — `python3 -m ruff check packages/orchestration/ownership_phrases.py
 packages/orchestration/pingpong_job.py packages/orchestration/job_digest.py
 tests/orchestration/test_ownership_phrases.py tests/orchestration/test_pingpong_job_ownership.py
 tests/orchestration/test_job_digest.py tests/orchestration/test_task_veto_runner.py
 tests/ui_server/test_task_veto_e2e_live.py` at C4, with its real exit code. Then report the
 golden file whole, and quote from `git show <C3>` the report section's code and the digest's
 new reading.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_ownership_phrases.py tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py tests/orchestration/test_job_digest.py tests/ui_server/test_digest_route.py tests/cli/test_job_digest_cli.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_token_ledger.py tests/orchestration/test_steering_notes.py tests/orchestration/test_pause_resume.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_veto_proposal.py tests/ui_server/test_task_veto_e2e_live.py tests/ui_server/test_steering_note_e2e_live.py tests/ui_server/test_command_channel.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the new `tests/orchestration/test_ownership_phrases.py`
 and less `tests/ui_server/test_command_channel.py`, serially, in the primary checkout at
 `3a8b1259`, and read `1124 passed, 1 skipped` at real exit code 0; the skip is the F252
 quarantine. Report every `SKIPPED` line, the node counts by `--collect-only -q` of every file
 this round added tests to and of `tests/ui_server/test_command_channel.py`, and account for the
 total. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f035-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_ownership_phrases.py tests/orchestration/test_pingpong_job_ownership.py
 tests/orchestration/test_job_digest.py tests/orchestration/test_task_veto_runner.py` from the
 worktree's root after purging its `__pycache__` directories, restores the bytes, and prints one
 line per mutation: its label, the exit code, the failed count and the failing node ids. It runs
 an unmutated control first and last and ends with `restored byte-identical: True` and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 `ownership_phrases.py`: an unattended action's phrase drops `(auto-approved via --yes)`;
  m2 `ownership_phrases.py`: the default policy's phrase drops `(you accepted at plan approval)`;
  m3 `ownership_phrases.py`: a browser phrase leaves out its token number;
  m4 `ownership_phrases.py`: a reason is cut to its first 20 characters;
  m5 `ownership_phrases.py`: an action with no template renders "" instead of raising;
  m6 `ownership_phrases.py`: the task phrase ignores the title;
  m7 `ownership_phrases.py`: the reason clause is printed for an empty reason;
  m8 `pingpong_job.py`: the section header is printed for a job with no entry;
  m9 `pingpong_job.py`: the per-task `Vetoed by` line is printed again;
  m10 `pingpong_job.py`: a ledger error adds no line to the report;
  m11 `job_digest.py`: `ownership` is `[]` for a job with entries;
  m12 `job_digest.py`: an `OwnershipError` propagates out of `build_job_digest`.
 Run it: `git worktree add --detach .remedy-wt/f035-r3-mut <C4>`, then
 `python3 -B .agent/authored/f035-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f035-r3-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f035-r3-mut` and `git worktree prune`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `3a8b1259` in that order (more
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
of feature F035, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003 — `remedy job ownership`, the chips at the nodes and the evidence tab, and the
end-to-end proof. State the open-findings count, 0, and the operator-questions count, 0.
