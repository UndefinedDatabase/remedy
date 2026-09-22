STEP F283 R6 — the `job` group's last mechanical refusals, and the `decision` group

GOAL
Book round 5's PASS and R-1021's `Done:`, thread `json_output` into
`_cmd_run_next_task_local` and move its eight print-then-exit pairs onto `fail()`, move
`decision.py`'s refusal pairs onto `fail()`, and finish R-1022's prose corrections.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit.

THE MIGRATION RULE (DECISION F277 D7, D8, D9 — read `.agent/decisions.md` for D8 and D9
before C4)
A pair `print(f"Error: <msg>", file=sys.stderr)` + `sys.exit(<n>)` becomes
  fail("<token>", f"<msg>", json_output=<flag>[, exit_code=<n>])
— the message WITHOUT `Error: `, because `fail()` writes it; `exit_code` only when <n> is
not 1; <flag> is the handler's own `json_output` when it has one, else `False`. A message
with an embedded `\n  ...` keeps it verbatim: `fail()`'s text branch then writes the same
bytes. TOKENS: one per CONDITION, repo-wide, and an existing spelling wins — before you
mint one, search `fail("` across `apps/cli/` for the condition. A single exception whose
instances differ only by prose gets `<layer>_error` (D9). A pair whose `print` does NOT
begin with `Error: `, or that has more than one `print` before its exit, is NOT
migrated: it stays and is counted.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r6-scratch/`   YOURS for logs, captures and scripts; the reviewer's
      `pairs.py` there is read-only to you (usage: `python3 <it> job.py decision.py`).

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `$?` or `${...}` outside a `bash -c`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a
file in your scratch directory for counting, hashing and copying (`shutil.copyfile`).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `63141657`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r6-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r6-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 5383 | 19827c93cba352eaac7b8ced3461161c0ef3a84df02ee7decea187c14e780fd1 |
| plan.md | 42 | 1899 | 959308eef0051b24ffca83d0003322386325210b76cfd17dfc1fec5eb6bbdb8a |
| slips.md | 1 | 471 | 4738ad39bbb23cad71c79c9875ede1eba40c105d7fae5f769a21c828ed953654 |

`ledger.md` is an APPEND beginning with the single record-separating newline: the round 5
`Gate:` entry and R-1021's `Done:` line. `slips.md` is an APPEND of one line with no
leading newline. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r6-block.md` := this block; `.agent/authored/f283-r6-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R6 C1: copy round 6 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md ·
  `.agent/prose_slips.md` += slips.md
  Subject: `F283 R6 C2: book round 5's PASS and resolve R-1021`

C3 — `job`: the single pass answers in the envelope
  SPEC, `apps/cli/commands/job.py`:
  - `_cmd_run_next_task_local(job_id_str: str, *, json_output: bool = False)`; it passes
    the flag to its `resolve_job_id_or_fail` call; `_cmd_job_run_cycles`'s single-pass
    branch passes its own `json_output` to it.
  - Its eight mechanical pairs move by the rule. Each condition already has a token
    elsewhere in `job.py` (`job_not_found`, `plan_awaiting_approval`, `plan_rejected`,
    `permission_denied`, `missing_dependency`, `invalid_builder_output`,
    `configuration_error`, `builder_error`); use the spelling the sibling site uses. The
    verification-failure loop at the end of the function is NOT mechanical and stays.
  - `_plan_rejected_error` loses its last caller: delete it, and make
    `_plan_rejected_message`'s docstring say it is the one form, with no `Error: `
    because `fail()` writes it.
  SPEC, tests:
  - The ten monkeypatches that replace `_cmd_run_next_task_local` with a
    single-positional stand-in — in `tests/orchestration/test_long_run_executor.py`,
    `tests/orchestration/test_escalation.py` and `tests/cli/test_cost_preview.py` —
    accept the keyword (`lambda _j, **_kw: None`, or a wrapper around `.append` that keeps
    the recorded value exactly as before). Change nothing else in those files.
  - `tests/cli/test_job_refusal_envelope.py`: the ratchet
    `test_the_unflagged_sites_are_counted_not_forgotten` asserts the unflagged list is
    EMPTY and its docstring says why; the `_plan_rejected_error` test becomes a test that
    `_plan_rejected_message` has no `Error: ` prefix.
  - `tests/test_cli_main.py`, class `TestWorkspaceWriteDenialPreBuilder`: one test that
    `_cmd_run_next_task_local(<id>, json_output=True)` exits 1 with an empty stderr and an
    envelope `permission_denied`, and one that `_cmd_job_run_cycles(<id>,
    json_output=True, yes=True)` does the same — the second proves the caller threads.
  Subject: `F283 R6 C3: the single-pass run answers a refusal in the envelope`

C4 — `decision`: the group's refusals move onto `fail()`
  SPEC, `apps/cli/commands/decision.py`: every pair the rule reaches. `_cmd_decision_list`
  and `_cmd_decision_show` use their `json_output`; `_cmd_decision_resolve` and
  `_create_mission_for_job` use `False`, because `decision.resolve` declares no
  `supports_json`. The derived-decision refusal near the end of `_cmd_decision_resolve`
  (two prints, no `Error: `) stays. If `sys` is left unused, remove its import.
  SPEC, tests:
  - `tests/cli/test_job_refusal_envelope.py`: generalise `_refusal_sites` to take a path
    (default `job.py`, so its callers do not change) and add a class asserting that in
    `decision.py` the flagged list is EMPTY and the unflagged list has exactly ONE site.
  - In `tests/cli/test_decision_cmd.py` (or the file you judge nearest; name it): under
    `json_output=True`, an unknown decision id on `_cmd_decision_show` exits 1 with an
    empty stderr and an envelope carrying the token you chose, and an invalid list
    option on `_cmd_decision_list` does the same with `invalid_list_option`.
  - Existing tests that assert a decision refusal's text keep passing UNCHANGED — they
    are the identity proof. If one fails, the migration changed bytes: fix the migration,
    never the test.
  In the handback, list every token C4 uses with its line and `new` or `reused`.
  Subject: `F283 R6 C4: decision refusals answer through fail()`

C5 — R-1022's last sentences, and the ambiguous payload
  SPEC, `tests/cli/test_job_refusal_envelope.py` only:
  - The comment above `_LOOKUP_CALLERS` describes the dict as every `lookup_job_id` call
    site under `apps/cli/` and says it was measured at `63141657`; it names no scratch
    script and no round-local commit label.
  - The docstring of `TestResolveJobIdOrFailForwardsAPayload` attributes the pass-through
    to R-1021, not R-1022.
  - A test that `resolve_job_id_or_fail("aaaa1111", json_output=True, job_id="x")` over
    the two-ambiguous-jobs fixture exits 2 with an envelope carrying both `matches` and
    `job_id` equal to `"x"` — round 5's probe (d) found this path unproved.
  Subject: `F283 R6 C5: finish R-1022 and prove the ambiguous payload`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R6 C6: rewrite handoff for round 6`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the four `.agent/authored/f283-r6-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `.agent/handoff.md`, `apps/cli/commands/job.py`, `apps/cli/commands/decision.py`,
   `tests/cli/test_job_refusal_envelope.py`, `tests/test_cli_main.py`,
   `tests/orchestration/test_long_run_executor.py`,
   `tests/orchestration/test_escalation.py`, `tests/cli/test_cost_preview.py`, and the
   ONE decision test file C4 names. Report the set you measure. Nothing under
   `packages/` or `docs/`, no `README.md`, `apps/cli/json_envelope.py` or
   `apps/cli/job_id_arg.py`, and none of `.agent/candidates.md`, `.agent/context.md`,
   `.agent/decisions.md`, `.agent/operator_questions.md`.
4. Migrate only what the rule reaches in the two named functions/modules. The other
   non-mechanical `job.py` sites (in `_cmd_job_run_cycles` and `_cmd_resume`) stay.
5. Every commit leaves the G4 selection green.
6. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
7. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
8. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r6-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r6-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `63141657` (466845 bytes)
     plus ledger.md equals the committed file; the reviewer composed 472228.
     `.agent/prose_slips.md` (360944) plus slips.md; the reviewer composed 361415.
 (b) Line-anchored on the committed ledger: `^- R-1021 — ` 1, `^Done: R-1021 — ` 1,
     `^- R-1022 — ` 1, `^Done: R-1022 — ` 0. Open set by distinct id via
     `open_finding_ids` from `scripts/rotate_live_review.py` at `63141657` and at C2: the
     reviewer measured 25 and 24, ADDED empty, REMOVED exactly `R-1021`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE MIGRATION, COUNTED FROM THE TREE — for every commit C3 to C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C5 run
 `python3 .remedy-wt/f283-r6-scratch/pairs.py job.py decision.py` and report its two
 summary lines; the reviewer read at `63141657`
 `job.py exits 12 mechanical 8 flagged 0 unflagged 8` and
 `decision.py exits 30 mechanical 30 flagged 2 unflagged 28`. Report
 `git diff --name-only 63141657 <C5> -- packages/`, which must print nothing.

G4 THE TARGETED SELECTION, in the primary checkout at C5:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/test_cli_main.py tests/test_run_log_cli.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_escalation.py tests/cli/test_cost_preview.py tests/cli/test_job_commands.py tests/cli/test_plan_approval.py tests/orchestration/test_proposal_decision.py tests/ui_server/test_command_channel.py tests/orchestration/test_run_report.py tests/orchestration/test_job_digest.py tests/cli/test_decision_cmd.py tests/orchestration/test_mission_gate.py tests/cli/test_mission_cmd.py tests/cli/test_open_decisions_view.py tests/cli/test_decision_answers.py tests/cli/test_do_sequence_cli.py tests/orchestration/test_import_reachability.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/docs/; echo "REAL_EXIT=$?"'
```
 The reviewer read `1217 passed` at real exit code 0 at `63141657`. If C4's test file is
 outside that list, add it and say so. Report your summary line and exit code; zero
 failed, zero xfailed, and the passed count may only rise. Then `python3 -m ruff check`
 over every `.py` path the round touched, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass`. DO NOT run
 the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed.
 Run `tests/cli/test_job_refusal_envelope.py`, `tests/test_cli_main.py` and C4's test file
 UNMUTATED first and report it (exit 0). Then each mutation alone, reverted before the
 next, reporting the summary line, the exit code and the failing test names:
 (a) `_cmd_job_run_cycles`'s single-pass call to `_cmd_run_next_task_local` drops
     `json_output=` — the caller-threading test of C3 must fail.
 (b) the `permission_denied` token in `_cmd_run_next_task_local` becomes
     `permission_refused` — both new C3 tests must fail.
 (c) `_cmd_decision_show`'s not-found `fail()` passes `json_output=False` — C4's
     unknown-decision test must fail.
 (d) one migrated `fail()` in `_cmd_decision_resolve` is put back as its old
     `print(f"Error: ...", file=sys.stderr)` + `sys.exit(1)` pair — the `decision.py`
     ratchet must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`;
 `git worktree list` (primary plus the three `remedy/job-*`); the push's real outcome;
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, C4's token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 2 of feature F283, round 6, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 6, then round 7 — R-1022's `Done:` booked in its first commit, and the
non-mechanical `job.py` sites together with the single-pass `job run --json` success
line. State the open-findings count, 24 after this round, and the operator-questions
count, 2.
