STEP F035 R2 — T001'S SECOND HALF: hunk decisions, decision answers, clarification answers and plan approval join the ownership ledger, and the ledger is written at the end of every `run_job`

GOAL
Round 1 passed. Book its verdict, record DECISION F035 D2 and one prose-slip line, then finish
T001 in `packages/orchestration/ownership.py`: four more classes of entry, and a run-log dedupe
keyed like `record_ref`. Wire the module in `packages/orchestration/pingpong_job.py` with one
decorator on `run_job` that saves `ownership.json` into the job's evidence export at the end of
every invocation, and move the module from the orphan guard's allow-list into the reachability
list. No report, command, event name or browser code changes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel
as payloads. Read DECISIONS F035 D1 and D2 (D2 is in the booking diff) before you write code.
Before you write anything, read whole: `packages/orchestration/ownership.py` and
`tests/orchestration/test_ownership_ledger.py`; `HUNK_DECISIONS_METADATA_KEY` and the record
`record_hunk_decision_from_view` stores in `packages/orchestration/hunk_decision_record.py`, and
the `HUNK_STATE_*` and `HUNK_LANDING_*` constants of `packages/orchestration/hunk_ledger.py`;
`enqueue_task_decision`, `answer_task_decision`, `auto_apply_safe_default` and the `ANSWER_SOURCE_*`,
`ESCALATION_STATUS_*` and `JOB_METADATA_ESCALATIONS_KEY` constants of
`packages/orchestration/escalation.py`; `clarification_source`, `apply_clarification_answers`,
`AUTO_APPROVAL_MODE`, `auto_approve_task_plan`, `announce_plan_approval` and
`resolve_task_plan_approval` in `packages/orchestration/job_plan.py`; `run_job`'s signature and
its first lines up to the `job_not_found` placeholder in `packages/orchestration/pingpong_job.py`;
`durable_write_json` in `packages/common/secure_fs.py`; `job_dir` and `job_evidence_export_dir` in
`packages/orchestration/data_paths.py`; `tests/orchestration/import_reachability_allowlist.txt`;
and, for a `run_job` fixture with scripted providers, `tests/orchestration/test_task_veto_runner.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f035-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f035-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f035-r2-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f035-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f035-r2-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f035-ownership-ledger`, and `git log --oneline -1` must read `d4495f2a`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f035-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f035-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 59 | 12611 | d02e9e26723e95da0f9d99d54663f28ff59df825019b18cb24b0937bff06ea31 |
| plan.md | 30 | 1005 | 52093632b817b7241f483738cae2a41b5c5d49c5042f3dde884d967c882de79b |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the
reviewer generated it with `git diff HEAD` from a tree at `d4495f2a`. It appends round 1's gate
entry to `.agent/live_review.md`, DECISION F035 D2 to `.agent/decisions.md` and one line to
`.agent/prose_slips.md`.

THE SPECIFICATION. No `except Exception` anywhere. `ownership.py` still imports nothing from
`pingpong_job`, `ui_server` or `apps`, writes no file and reads no clock; every import it adds is
function-scoped, as round 1's are. Every `text` is the record's own string verbatim.
S1 HUNKS, action `hunk_approved` or `hunk_rejected`: for every `attempt_key, value` of
   `job.metadata.get(HUNK_DECISIONS_METADATA_KEY) or {}`, one entry per row of `value["hunks"]`
   whose `state` is `HUNK_STATE_APPROVED` or `HUNK_STATE_REJECTED` — an undecided row yields
   none. `record_ref` `hunk:<attempt_key>:<row id>`, `ts` `value["decided_at"]`, `task_id`
   `value["task_id"]`, `text` the row's `reason`, actor `ownership_actor("")` — the record names
   no door — consequence `{"kind": "landing", "task_ids": [task_id], "ref": row["landing"]}`,
   `detail` `{"attempt": str(value["attempt"]), "hunk_id": row["id"]}`.
S2 DECISION ANSWERS, action `decision_answered`: every record of
   `job.metadata.get(JOB_METADATA_ESCALATIONS_KEY)` whose `status` is
   `ESCALATION_STATUS_ANSWERED`; an open record yields none. `record_ref`
   `decision:<decision_id>`, `ts` `answered_at`, `task_id`, `text` `answer`, actor
   `ownership_actor(answer_source, kind="default_policy")` when `answer_source` is
   `ANSWER_SOURCE_DEFAULT` and `ownership_actor(answer_source)` otherwise, consequence
   `{"kind": "answer_to_task", "task_ids": [task_id], "ref": ""}`, `detail`
   `{"question": question}`.
S3 CLARIFICATIONS, action `clarification_answered`: every dict of
   `(job.task_plan or {}).get("clarifications_resolved") or []` whose `clarification_source` is
   not `unresolved`. The actor is `ownership_actor(source, kind=K)` with K `operator` for
   `human`, `default_policy` for `default` and `remedy` for `planner`. `record_ref`
   `clarification:<id>`, `ts` "" (the record keeps no time), `task_id` "", `text` `answer`,
   consequence `{"kind": "plan_input", "task_ids": [], "ref": ""}`, `detail` `{"question":
   question, "default_answer": default_answer}`.
S4 PLAN APPROVAL. Reader (g) also reads `plan_approved`, action `plan_approved`: `record_ref`
   `plan_approved:<timestamp>`, `ts` the timestamp, `task_id` "", consequence `{"kind":
   "plan_approved", "task_ids": md["task_ids"], "ref": ""}`, `detail` `{"approval_mode":
   md["approval_mode"]}`. When the mode is `AUTO_APPROVAL_MODE` the actor is
   `ownership_actor(mode, auto_approved=True)` and `text` is `_approval_audit["reason"]` of the
   plan body, or "" without one; otherwise the actor is `ownership_actor("")` and `text` "".
   Reader (g)'s dedupe key becomes `(event, request_id or timestamp)`, the same value
   `record_ref` uses. From the plan body, in a reader of its own: `_approval == "rejected"`
   yields one entry, `record_ref` `plan_rejected`, action `plan_rejected`, `ts` "", actor
   `ownership_actor("")`, consequence kind `plan_rejected`; `_approval == "approved"` with NO
   `plan_approved` event yields one entry, `record_ref` `plan_approved:body`, `ts` "", actor and
   `text` by `_approval_audit`'s mode exactly as for the event, consequence kind
   `plan_approved` with `[]`.
S5 THE WRITE, in `pingpong_job.py`, per DECISION F035 D2. `_writes_ownership_ledger(fn)` wraps
   with `functools.wraps`, calls `fn`, then `_write_ownership_ledger_at_run_end(job)`, and
   returns the job unchanged. That function returns at once unless the job is a `JobPlan` whose
   `job_dir(job.job_id)` is a directory; otherwise it builds the ledger and saves it with
   `durable_write_json` at `job_evidence_export_dir(job.job_id) / OWNERSHIP_FILENAME`. An
   `OwnershipError` or `OSError` is caught and logged with `logging.getLogger(__name__).warning`
   naming the job id and the error, and nothing else happens. Its imports are function-scoped.
   `run_job` gains the decorator line directly above its `def`, and nothing else in `run_job`
   changes.
S6 THE GUARDS. `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py` loses round 1's
   `packages/orchestration/ownership.py` entry, and
   `tests/orchestration/import_reachability_allowlist.txt` gains the one line
   `packages.orchestration.ownership` in its sorted place. If
   `tests/orchestration/test_import_reachability.py` then names any OTHER module, stop and
   report it. Both edits land in the same commit as S5.

THE TESTS. Classes S1 to S4 go into `tests/orchestration/test_ownership_ledger.py`, the write into
a NEW file `tests/orchestration/test_pingpong_job_ownership.py`. At least: a rejected hunk's
entry with its reason verbatim, its landing and no door, an approved one, and no entry for a
pending row; a human decision answer and a default one — the second `default_policy`,
`recorded_as` `default` — and no entry for an open decision; a clarification each by `human`,
`default` and the planner, with the three kinds, and none for an unresolved one; a
`plan_approved` event in human mode and one in `auto_yes` mode, the second with
`auto_approved` true and the audit's reason as its text; two `plan_approved` events with no
request id yield two entries; a rejected plan's entry; a body approval with no event yields
`plan_approved:body`; and, through a real `run_job` with scripted providers, a completed job
whose `ownership.json` equals `build_ownership_ledger` of the returned job; a run with
`packages.orchestration.ownership.build_ownership_ledger` replaced by a stand-in that raises
`OwnershipError` returns the same state as the same run without it, writes no `ownership.json`
and logs one warning naming the job; a `run_job` for an unknown job id writes no file; and
`run_job.__wrapped__` exists. Record every clock-free time a test sets.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f035-r2-block.md` := this block, `.agent/authored/f035-r2-plan.md` := plan.md
  and `.agent/authored/f035-r2-booking.diff` := booking.diff. All by `shutil.copyfile`.
  Subject: `F035 R2 C1: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 89. Report the number you measure.

C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F035 R2 C2: book round 1, record D2, log one prose slip, advance the plan`
  Expected by `git show --numstat`: 32/0 decisions.md, 2/0 live_review.md, 9/9 plan.md, 1/0
  prose_slips.md.

C3 — THE CODE AND THE GUARDS: `packages/orchestration/ownership.py`,
  `packages/orchestration/pingpong_job.py`, `tests/test_no_orphan_modules.py` and
  `tests/orchestration/import_reachability_allowlist.txt`.
  Subject: `F035 R2 C3: read hunks, answers, clarifications and approvals, and write the ledger at run end`

C4 — THE TESTS AND THE TOOL: the two test files and your mutation tool (G5) saved as
  `.agent/authored/f035-r2-mutations.py`.
  Subject: `F035 R2 C4: test the remaining ownership classes and the run-end write, add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F035 R2 C5: rewrite handoff for round 2`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so. A
   split of C3 keeps S5 and S6 in ONE part, so no commit of the round leaves either guard red.
3. The round's whole tracked path set is: the `.agent/authored/f035-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `packages/orchestration/ownership.py`, `packages/orchestration/pingpong_job.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/test_ownership_ledger.py`,
   `tests/orchestration/test_pingpong_job_ownership.py`, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only d4495f2a` at the branch tip after C5. Do NOT touch
   anything under `apps/`, any other file under `packages/`, `docs/`, `.agent/context.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards. `git branch --list 'remedy/*' | wc -l` is reported at step 4 and after G5
   and must not change.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F035's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f035-r2-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f035-r2/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2328299 | bf8e0fd805735352f9e4f2028463bcf8e0e240923e86a22b8364950ea360f01b |
 | .agent/live_review.md | 302813 | 79edb1951b5601457ec4ae75ca6131861ee14e50f05ab6b709dae84baa33ece9 |
 | .agent/plan.md | 1005 | 52093632b817b7241f483738cae2a41b5c5d49c5042f3dde884d967c882de79b |
 | .agent/prose_slips.md | 374918 | 8f22b48d6f0b64a674144895411083c298abf07c55e81dbe21260c773a8321b2 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at C2
 (the reviewer read it empty), and the ledger's last line at C2, which must begin
 `Gate: F035 R1 — `.

G3 THE CODE — `python3 -m ruff check packages/orchestration/ownership.py
 packages/orchestration/pingpong_job.py tests/orchestration/test_ownership_ledger.py
 tests/orchestration/test_pingpong_job_ownership.py tests/test_no_orphan_modules.py` at C4, with
 its real exit code. Then report, quoted from `git show <C3>`, the whole of
 `_writes_ownership_ledger` and `_write_ownership_ledger_at_run_end`, the decorator line with the
 `def run_job(` line under it, and reader (g)'s new dedupe key.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py tests/orchestration/test_hunk_decision_record.py tests/orchestration/test_hunk_ledger.py tests/orchestration/test_escalation.py tests/orchestration/test_bundled_clarification.py tests/orchestration/test_job_plan.py tests/orchestration/test_job_plan_state_reads.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_pingpong_job_dod_gate.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_injection_runner.py tests/orchestration/test_job_evidence.py tests/test_role_override_flags.py tests/orchestration/test_task_veto.py tests/orchestration/test_steering_notes.py tests/orchestration/test_pause_resume.py tests/orchestration/test_subtree_rerun.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the new `tests/orchestration/test_pingpong_job_ownership.py`
 and less `tests/ui_server/test_command_channel.py`, serially, in the primary checkout at
 `d4495f2a`, and read `1203 passed, 1 skipped` at real exit code 0; the skip is the F252
 quarantine. Report every `SKIPPED` line, the node counts by `--collect-only -q` of the two
 ownership test files and of `tests/ui_server/test_command_channel.py`, and account for the total.
 Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f035-r2-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py`
 from the worktree's root after purging its `__pycache__` directories, restores the bytes, and
 prints one line per mutation: its label, the exit code, the failed count and the failing node
 ids. It runs an unmutated control first and last and ends with `restored byte-identical: True`
 and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 `ownership.py`: a pending hunk row yields an entry;
  m2 `ownership.py`: a hunk entry's text is "";
  m3 `ownership.py`: a default decision answer is attributed to the operator;
  m4 `ownership.py`: an open decision yields an entry;
  m5 `ownership.py`: the planner's clarification is attributed to the operator;
  m6 `ownership.py`: an unresolved clarification yields an entry;
  m7 `ownership.py`: an unattended plan approval is not `auto_approved`;
  m8 `ownership.py`: the run-log dedupe keys on the request id alone again;
  m9 `ownership.py`: a rejected plan yields no entry;
  m10 `pingpong_job.py`: the decorator line is removed from `run_job`;
  m11 `pingpong_job.py`: an `OwnershipError` in the write propagates;
  m12 `pingpong_job.py`: the job-directory check is removed.
 Run it: `git worktree add --detach .remedy-wt/f035-r2-mut <C4>`, then
 `python3 -B .agent/authored/f035-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f035-r2-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f035-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l` and the `remedy/*` branch count.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `d4495f2a` in that order (more
 lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your step 4
 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F035, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002 — the phrase catalog, the report's Ownership section with its goldens, and the
digest's `ownership` sentences. State the open-findings count, 0, and the operator-questions
count, 0.
