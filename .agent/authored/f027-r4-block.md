STEP F027 R4 — T002: the `replan_proposal` decision derived from each veto, its answer as a create-only control fact, the follow-up job created and never run, the settled completion, and the CLI route

GOAL
Book round 3's verdict, resolve R-1066, add one prose-slip line, record DECISION F027 D4, and land
it: every veto files a `replan_proposal` in the decision queue with the two options
`replan_follow_up` and `accept_reduced_scope`, an answer is recorded as a create-only control fact,
a replan creates an unplanned follow-up job and nothing more, a run whose every veto is answered
completes the job with the reduced scope, and `remedy decision resolve <job> veto:<id>` answers —
with tests and a mutation tool proving they bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel as
payloads. Read DECISION F027 D4 in `records.diff` before you write code: it is the design, and the
plain-words texts it asks for are yours to write within it.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r4-dry/`, `.remedy-wt/f027-r4-drafts/`, `.remedy-wt/f027-review/` and every
                                  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f027-task-veto`, and `git log --oneline -1` must read `c1c36656`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 32 | 1207 | 37219603b525f36035e980556dcd98c65236b9603922c98f4c895e6838d062c0 |
| records.diff | 104 | 14004 | 81557e20692f57d5edb14099553dfd1fb80b76543ea6526897ae9f18d77ff64b |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `c1c36656`. It appends to `.agent/live_review.md`
round 3's gate entry and R-1066's `Done:` paragraph, one line to `.agent/prose_slips.md`, and to
`.agent/decisions.md` DECISION F027 D4.

THE SPECIFICATION
S1 THE ANSWER FILES, in `packages/orchestration/task_veto.py`, beside the veto files and through
   the same helpers: `VETO_ANSWERS_DIRNAME = "veto_answers"`, `REPLAN_FOLLOW_UP =
   "replan_follow_up"`, `ACCEPT_REDUCED_SCOPE = "accept_reduced_scope"` and
   `REPLAN_PROPOSAL_OPTIONS` holding the two in that order; a frozen dataclass `VetoAnswer` of
   `job_id`, `request_id`, `task_id`, `option`, `actor`, `answered_at` and `follow_up_job_id`,
   whose `to_json()` also writes `"veto_answer_v": 1`; `record_veto_answer(job_id, request_id,
   task_id, option, actor, follow_up_job_id, *, control_root_path=None) -> tuple[VetoAnswer,
   bool]`, create-only and named by the first 32 hex characters of the request id's sha256, which
   refuses an option outside the two with `TaskVetoRefused("invalid_option", ...)`, a request id
   that `safe_points.is_safe_id` rejects with `TaskVetoError`, and answers an existing entry
   unchanged with False exactly as `record_task_veto` does; and `veto_answers(job_id, *,
   control_root_path=None) -> dict[str, VetoAnswer]` keyed by request id, empty when nothing
   exists, RAISING `TaskVetoError` on an entry it cannot read or trust.
S2 THE NEW MODULE `packages/orchestration/veto_proposal.py`, docstring naming DECISION F027 D4:
   `replan_proposal_decisions(job, *, control_root_path=None) -> list[HumanDecision]` builds D4 (1)'s
   decisions, one per `vetoed_tasks` entry whose task is in the job with a status in
   `VETOABLE_TASK_STATUSES` or `vetoed` and whose request id has no answer; the unreachable ids are
   `veto_unreachable(job.tasks, [task id])` without the other entries' tasks. `answer_replan_proposal(
   job, decision_id, option, *, actor, control_root_path=None, root=None) -> dict` is D4 (2) to (4),
   checking in order the id (`unknown_decision` for an id that is not `veto:` plus a request id of an
   entry of this job), the option (`invalid_option`) and an existing answer (`already_answered`, with
   the recorded `option` and `follow_up_job_id`); on success it answers `{"outcome": "answered",
   "decision_id", "option", "follow_up_job_id"}`, the last "" for an accept. A repeated call that
   finds a recorded `replan_follow_up` whose follow-up job does not exist creates it before it
   answers `already_answered`, and every call that finds or writes an answer writes a missing
   `veto_proposal_answered` event, the way `task_veto` repairs its own. `build_follow_up_job(job,
   entry, unreachable_ids, *, job_id)` returns the D4 (4) `JobPlan`, saved by the answer with
   `save_job_plan(follow_up, root)`. Nothing in this module plans, approves or runs a job, or
   writes the original job's record.
S3 THE QUEUE: `"replan_proposal"` joins `DECISION_TYPES` in `packages/orchestration/decision_queue.py`
   and `TRIPLE_REQUIRED_TYPES` in `packages/orchestration/decision_evidence.py`; `list_decisions`
   gains a branch, before its closing `enforce_decision_evidence`, that extends the list with
   `replan_proposal_decisions(job)`, wrapped as its neighbours are and also catching
   `TaskVetoError`, which adds no card. Every decision passes `enforce_decision_evidence`.
S4 SETTLED COMPLETION, in `run_job`'s veto terminal (DECISION F027 D2 (5)): read
   `task_veto.veto_answers`; when every `TASK_VETOED` task's request id, read from
   `job.metadata["task_vetoes"]`, has an answer, the still-pending unreachable tasks become
   `skipped`, `job.metadata["veto_terminal"]` records the two lists with `settled` true and each
   task's answered option, and the run does NOT return there but falls through to the ordinary
   completion path, whose `all_done` reading counts `TASK_VETOED` beside applied, skipped and split;
   otherwise the terminal blocks exactly as it does today, `settled` false. A `TaskVetoError`
   reading the answers blocks with `task_veto_control_error: <detail>`. In
   `packages/orchestration/run_manifest.py`, `_COMPLETED_WORKED_STATUSES` gains `"vetoed"` for
   `EXPECT_EXECUTED`, `EXPECT_PRIOR_EPISODE` and `EXPECT_SKIPPED`.
S5 THE CLI ROUTE, in `apps/cli/commands/decision.py`'s `_cmd_decision_resolve`: a `veto:` id loads
   the job as the other routes do and calls `answer_replan_proposal` with `--reason` as the option
   and the actor `cli`; `answered` prints the option, the follow-up job's id when there is one, and
   for an accept the sentence that the job completes at its next run with the command that runs it,
   the job's own id written out; a refusal fails with its code and the exit code the `proposal:`
   route gives a refusal of the same kind, which you name in the handback. `--answer` and
   `--as-mission` stay refused for it, as for every id but `plan:`.
S6 THE GUARDS: `"veto_proposal_answered"` joins `EVENT_NAMES`;
   `packages.orchestration.veto_proposal` joins `tests/orchestration/import_reachability_allowlist.txt`
   in its sorted place; `tests/orchestration/test_decision_evidence.py`'s exact
   `TRIPLE_REQUIRED_TYPES` set gains the type; and `tests/orchestration/test_decision_inbox.py`
   gains `replan_proposal` in `PRODUCING_DECISION_TYPES` with a fixture in `PRODUCING_FIXTURES`,
   leaves `ANSWERABLE_DECISION_TYPES` alone (the card is not answerable until the door answers it,
   next round), and moves `replan_proposal` out of the zero-blocked parametrization into a test of
   its own that its `blocked_count` equals the veto's unreachable count.

THE TESTS — a NEW FILE at `tests/orchestration/test_veto_proposal.py`, over the data root and the
control root the runner tests use: the decision's id, type, severity, summary beginning
`You vetoed <title> — reason: <reason>` with the reason verbatim, payload keys and option order,
and evidence passing `enforce_decision_evidence`; one card per veto and none for an inert veto or
an answered one; each refusal in its order with nothing written; an accept writing the answer
file, one event and no job; a replan writing the answer file, one event and exactly one new job
whose state is `pending`, with no tasks, the original's repository and project, the goal naming the
vetoed task, the reason verbatim and each unreachable task's goal, and `replan_of`, while the
original job's `job.json` stays byte-identical; a repeated answer `already_answered` with no second
job or event; the repair of a follow-up job whose save failed; and two concurrent answers
converging. `tests/orchestration/test_task_veto.py` gains the answer files' own tests.
`tests/orchestration/test_task_veto_runner.py` gains: a copy job with B vetoed and answered
`accept_reduced_scope` before a run — the job `completed`, B `vetoed`, D `skipped`, `settled`
true, the completed run manifest validating; the same vetoed but unanswered — `blocked`, `settled`
false; a blocked veto terminal answered and relaunched — `completed`. `tests/cli/test_decision_cmd.py`
gains the `veto:` route: an accept, a replan printing the follow-up job's id, and a refusal's exit
code.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r4-block.md`,
  `.agent/authored/f027-r4-plan.md` and `.agent/authored/f027-r4-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 136. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R4 C2: book round 3, resolve R-1066, record D4`
  Expected by `git show --numstat`: 75/0 decisions.md, 4/0 live_review.md, 11/12 plan.md,
  1/0 prose_slips.md.
C3 — THE ANSWER FILES AND THE PROPOSAL: S1, S2 and S3, with their guards from S6.
  Subject: `F027 R4 C3: file a replan proposal for every veto and record its answer`
C4 — THE SETTLED COMPLETION AND THE CLI ROUTE: S4 and S5.
  Subject: `F027 R4 C4: complete a job whose every veto is answered, and answer from the CLI`
C5 — THE TESTS AND THE MUTATION TOOL, with `.agent/authored/f027-r4-mutations.py`.
  Subject: `F027 R4 C5: test the replan proposal, its answers and the settled completion`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F027 R4 C6: rewrite handoff for round 4`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `packages/orchestration/task_veto.py`, `packages/orchestration/veto_proposal.py`,
   `packages/orchestration/decision_queue.py`, `packages/orchestration/decision_evidence.py`,
   `packages/orchestration/event_names.py`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/run_manifest.py`, `apps/cli/commands/decision.py`,
   `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_veto_proposal.py`,
   `tests/orchestration/test_task_veto.py`, `tests/orchestration/test_task_veto_runner.py`,
   `tests/orchestration/test_decision_evidence.py`, `tests/orchestration/test_decision_inbox.py`,
   `tests/cli/test_decision_cmd.py`, and `.agent/handoff.md`. One widening is allowed and must be
   declared: a test file that pins, by an exact equality, a vocabulary S3, S4 or S6 widens may gain
   the one new entry. Report the list `git diff --name-only c1c36656` measures after C6. Do NOT
   touch `packages/orchestration/ui_server.py`, `decision_inbox.py`, `long_run_executor.py`,
   `apps/cli/command_catalog.py`, `apps/ui/`, `docs/`, `.agent/context.md`, `.agent/candidates.md`
   or `.agent/operator_questions.md`.
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
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload the line count, byte count and sha256 you measured against the
 table; then each `.agent/authored/f027-r4-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r4/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 303547 | 058976c45fc7088603912a1ee70fea43ba26b65ad76957403938544ae9e200ee |
 | .agent/decisions.md | 2173285 | 714abd6ef4574b4528df338336df71aa7455edba90233758b42b4939b500caec |
 | .agent/prose_slips.md | 368884 | 9a17eb60ce00d4322e3d01bb29505564a46c30232547a6425fe1f10ac65d030c |
 | .agent/plan.md | 1207 | 37219603b525f36035e980556dcd98c65236b9603922c98f4c895e6838d062c0 |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read it empty).

G3 THE CODE — `python3 -m ruff check` over every Python file of the round's path set at the last
 code commit; `python3 -m apps.cli.main decision resolve --help` at that commit, reported whole;
 and a python `ast` reading of `veto_proposal.py` naming every module it imports, which must name
 none of `subprocess`, `threading`, `signal` or `packages.orchestration.long_run_executor`.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_veto_proposal.py tests/cli/test_decision_answers.py tests/cli/test_decision_cmd.py tests/cli/test_open_decisions_view.py tests/cli/test_plan_approval.py tests/orchestration/test_approval_queue.py tests/orchestration/test_bundled_clarification.py tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_escalation.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_job_digest.py tests/orchestration/test_mission_state.py tests/orchestration/test_proposal_decision.py tests/ui_server/test_live_state.py tests/ui_contracts/test_decision_answer_wiring.py tests/ui_contracts/test_decision_urgency_parity.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_zero_call_expectations.py tests/orchestration/test_event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the round's records, and read `1257 passed` at real exit code
 0. Report every `SKIPPED` line, the nodes each new or grown test file contributes
 (`--collect-only -q`), and account for every difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r4-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_veto_proposal.py`, `tests/orchestration/test_task_veto.py`,
 `tests/orchestration/test_task_veto_runner.py`, `tests/orchestration/test_decision_inbox.py` and
 `tests/cli/test_decision_cmd.py` from the worktree's root after purging its `__pycache__`
 directories, restores the bytes, and prints one line per mutation: its label, the exit code, the
 failed count and the failing node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each mutation is a behaviour a test can see:
  m1 a proposal is derived for an answered veto;
  m2 the summary drops the reason;
  m3 the options are offered in the other order;
  m4 the answer file is published without `create_only`;
  m5 a replan saves no follow-up job;
  m6 a replan also sets the original job `completed` and saves it;
  m7 the follow-up job's goal leaves out the reason;
  m8 a repeated answer writes a second event;
  m9 an option outside the two is recorded;
  m10 the settled completion ignores the answers and always completes;
  m11 the settled completion never completes;
  m12 `all_done` leaves out `TASK_VETOED`, so a settled run ends as it began;
  m13 the CLI route answers with `--answer` instead of `--reason`.
 Run it in `git worktree add --detach .remedy-wt/f027-r4-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over:
 you then say whether a test can see the behaviour at all, add the test that catches it if one
 can, and re-run the tool. Then `git worktree remove --force .remedy-wt/f027-r4-mut`,
 `git worktree prune`, and `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty; `git log --oneline`
 from `c1c36656` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F027, round 4, and says in one sentence how much context you had left. Where S1 to S6
leave a choice open, make it, say so in the deviations, and never widen the path set for it
beyond constraint 3's one declared widening.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the channel commands — `job.veto-task` in the catalog, the CLI and the write door,
and the door's answer of a replan proposal. State the open-findings count, 0, and the
operator-questions count, 5.
