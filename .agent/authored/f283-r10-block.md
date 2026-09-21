STEP F283 R10 — `do --json` in one envelope, the parser's usage refusals, the `test` group, R-1026

GOAL
Book round 9's PASS, register R-1026 and record DECISIONs F283 D5 and D6, then: `remedy do
--json` answers in one envelope (D5); the parser's usage refusals in `apps/cli/grouped.py`
answer in the envelope under `--json` (D6); the `test` group's refusals move onto `fail()`;
and the three refusals R-1026 names pass `job_not_found`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit. Read DECISIONs F283 D5 and D6 in this round's decisions payload before C3.

THE MIGRATION RULE (DECISION F277 D7, D8, D9 and F283 D4 — read them in `.agent/decisions.md`)
A pair `print(f"Error: <msg>", file=sys.stderr)` + `sys.exit(<n>)` becomes
  fail("<token>", f"<msg>", json_output=<flag>[, exit_code=<n>])
— the message WITHOUT its prefix; `exit_code` only when <n> is not 1; <flag> is the
handler's own `json_output` / `as_json` when it has one, else `False`. A BRANCHED site —
`if <flag>: print(json.dumps({"error": "<T>", ...}))` / `else: print(f"Error: <msg>", ...)`
then one exit — becomes ONE `fail("<T>", f"<msg>", json_output=<flag>, <every other key of
that JSON object as a keyword>)`, so no key a consumer read is lost. TOKENS: one per
CONDITION, repo-wide, and AN EXISTING SPELLING WINS: before you use a token, search
`fail("` over `apps/cli/` (multi-line calls included) and use the one that names the same
condition. The text branch stays byte-identical everywhere except where D4 already rules.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r10-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r10-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt`, `build_selection.py`, `run_sel.py`, `measure.py` and
      `dryrun_edit.py`, which are read-only to you. The pair counter is
      `.remedy-wt/f283-r6-scratch/pairs.py` (read-only). `run_sel.py <dir> <label>` runs
      the selection in <dir> and prints the exit code, summary and bad node ids.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a file in your
scratch directory (written with your file tool) for counting, hashing, copying
(`shutil.copyfile`) and running pytest; use `git -C <dir>` for a worktree.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `859f883c`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r10-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r10-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 62 | 4523 | faf88c18c672ec06b509a97dd372258004efb24034101c37fe1422b738ec5753 |
| ledger.md | 4 | 4492 | 0c645ff788b875b7491d13f3853a4319e1aba41c5924e1fd6f4a46cf9983cc3f |
| plan.md | 39 | 1760 | 979c1237856fac5d00ebf8c6a536f3361d407c920bd48a86f9ca51da2ab47e1a |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 9 `Gate:` entry and the registration of
R-1026; decisions carries DECISIONs F283 D5 and D6. `plan.md` is a REWRITE. Never retype
or edit a payload.

BUNDLE — commits C1 to C7, in this order.

C1 — `.agent/authored/f283-r10-block.md` := this block; `.agent/authored/f283-r10-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R10 C1: copy round 10 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R10 C2: book round 9's PASS, register R-1026, record D5 and D6`

C3 — `apps/cli/commands/do_cmd.py::_cmd_do_order`, by DECISION F283 D5. Under
  `json_output` build the same dict with the same keys; when `ctx.failed`, call
  `fail("step_failed", f"{last.name} failed: {last.detail}", json_output=True,
  failed_step=last.name, **document)` where `last = ctx.results[-1]`; otherwise
  `emit_ok(**document)` and return. The text branch is unchanged and its trailing failure
  line becomes `fail("step_failed", ..., json_output=False)`, byte-identical on stderr;
  delete the NOT-migrated comment. `step_failed` is new — confirm it by search.
  SPEC, tests: repair in this commit the three tests that pin the old shape —
  `tests/cli/test_do_flags.py::test_an_unknown_project_exits_1_with_the_init_step_failed_and_no_mission`,
  `tests/cli/test_do_commit_flags.py::test_a_push_the_remote_refuses_leaves_the_commit_and_fails_the_walk`
  and `tests/cli/test_do_sequence_cli.py::test_an_apply_the_baseline_check_refuses_fails_the_walk_naming_the_job`
  — to assert an empty stderr and, on the one stdout object, `ok` false, `error`
  `step_failed`, `failed_step` and the `message` their old stderr assertion read (without
  `Error: `), keeping every document assertion they already make. Add one test that a
  successful `do --json` object carries `schema_version` 1 and `ok` true beside
  `mission_id`, and one text-mode test that a failed walk still writes
  `Error: init failed: ` on stderr, both in `tests/cli/test_do_flags.py`. In
  `tests/cli/test_job_refusal_envelope.py`, `TestDoRefusalsAreAllMigrated` asserts NO
  flagged pair survives, docstring updated.
  Subject: `F283 R10 C3: do --json answers in one envelope`

C4 — `apps/cli/grouped.py::main`, by DECISION F283 D6. Every parse-level refusal asks
  `_wants_json(raw)`; when it holds, `emit_error(<token>, <message>)` then the SAME exit
  code, and when it does not, today's bytes. Tokens exactly as D6 names them:
  `conflicting_options` (replacing the hand-written object, which lacks
  `schema_version`), `unknown_command` for an unknown group or subcommand,
  `unrecognized_arguments`, and on a usage error for a known subcommand
  `missing_argument` when the message begins `the following arguments are required`, else
  `invalid_argument`, with the message `invalid arguments for remedy <group> <subcommand>`
  if the parser left none. A small helper for the repeated shape is welcome. The two
  post-parse pairs (`Error: unknown command`, `Error: no handler for ...`) become
  `fail("unknown_command", ...)` and `fail("no_handler", ...)` with
  `json_output=_wants_json(raw)`. Confirm each new token by search.
  SPEC, tests: repair the four parameters of
  `tests/cli/test_do_flags.py::test_a_flag_removed_from_do_exits_2_and_runs_nothing` to
  assert exit 2, an empty stderr and one envelope with `error` `unrecognized_arguments`,
  keeping their nothing-was-written assertions. In `tests/test_grouped_cli.py` add one
  class: under `--json` an unknown subcommand, an unrecognized argument, a missing
  positional and the conflicting pair each exit 2 with an empty stderr and one envelope
  (`schema_version` 1, `ok` false, the token above); and without `--json` the
  unrecognized-argument stderr is byte-identical to `render_error`'s. In
  `tests/cli/test_job_refusal_envelope.py` add `TestGroupedRefusalsAreAllMigrated`
  (`_refusal_sites("../grouped.py")`, no pair survives).
  Subject: `F283 R10 C4: parser usage refusals answer in the envelope under --json`

C5 — `apps/cli/commands/test_cmds.py`: `_cmd_discover_commands`'s `except Exception`
  pair → `fail("job_store_error", str(exc), json_output=as_json)` (the catch-all token
  `job.py` gives a `require_job_plan` failure); its branched `no_target_repo` site and
  `_cmd_test_status`'s branched `job_not_found` site by the BRANCHED rule, keeping `job_id`
  and `candidates` / `job_id`. `_cmd_run_tests` stays — a result document, T002's.
  SPEC, tests: in the ONE test file you judge nearest (name it), a `test discover --json`
  on a job with no target repo answers one envelope with `no_target_repo`, `job_id` and
  `candidates` `[]`, empty stderr; and in text mode stderr reads
  `Error: no target_repo attached.\n` exactly. In `tests/cli/test_job_refusal_envelope.py`
  add `TestTestCmdsRefusalsAreAllMigrated` (no pair survives).
  Subject: `F283 R10 C5: test group refusals answer through fail()`

C6 — R-1026: `apps/cli/commands/job_context_cmd.py::_cmd_job_context`,
  `apps/cli/commands/project.py::_cmd_attach_project_job` and `::_cmd_project_adopt` pass
  `job_not_found` where they pass `invalid_job_id` after `require_job_plan` raises
  `JobNotFoundError`; nothing else changes. SPEC, test: in
  `tests/cli/test_job_context_cmd.py`, `job context --json` on an id the resolver accepts
  and the store does not hold (monkeypatch the module's resolver) answers one envelope with
  `job_not_found` and an empty stderr. Do NOT write a `Done:` line; the reviewer does.
  Subject: `F283 R10 C6: a job the store cannot find answers job_not_found (R-1026)`

C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R10 C7: rewrite handoff for round 10`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the four `.agent/authored/f283-r10-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/commands/do_cmd.py`, `apps/cli/grouped.py`, `apps/cli/commands/test_cmds.py`,
   `apps/cli/commands/job_context_cmd.py`, `apps/cli/commands/project.py`,
   `tests/cli/test_do_flags.py`, `tests/cli/test_do_commit_flags.py`,
   `tests/cli/test_do_sequence_cli.py`, `tests/cli/test_job_refusal_envelope.py`,
   `tests/test_grouped_cli.py`, `tests/cli/test_job_context_cmd.py`, and the ONE test file
   C5 names. Report the set you measure. Nothing under `packages/` or `docs/`, no
   `README.md`, no `scripts/`, no `apps/cli/json_envelope.py`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
   `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves the G4 selection at zero failed: run it after C3, C4, C5
   and C6 and report each reading. Read the guards a file carries before changing its
   imports.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C7 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r10-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r10-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `859f883c` (492157 bytes)
     plus ledger.md; the reviewer composed 496649. `.agent/decisions.md` (1799308) plus
     decisions.md; the reviewer composed 1803831.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R9 — ` 1, `^- R-1026 — ` 1.
     Open set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py`
     at `859f883c` and at C2: the reviewer measured 22 and 23, ADDED exactly `R-1026`,
     REMOVED empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 to C6 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C6 run
 `python3 .remedy-wt/f283-r6-scratch/pairs.py do_cmd.py ../grouped.py test_cmds.py
 project.py job_context_cmd.py` and report its summary lines; the reviewer read at
 `859f883c` do_cmd `mechanical 1 flagged 1`, grouped `mechanical 5`, test_cmds
 `mechanical 1 flagged 1`, project `mechanical 2 flagged 1 unflagged 1`, job_context
 `exits 0`. At C6 do_cmd, grouped and test_cmds must read `mechanical 0`, project
 unchanged. List every token C3 to C6 use, with its line and `new` or `reused`, and for
 each `new` one the search you ran. `git diff --name-only 859f883c <C6> -- packages/`
 must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r10-scratch/selection.txt` is one line of 100
 space-separated paths: round 9's selection plus every test file a search for this
 round's targets found. Run `python3 .remedy-wt/f283-r10-scratch/run_sel.py . <label>` in
 the primary checkout after C3, C4, C5 and C6 and report each summary line and exit code.
 The reviewer read `4205 passed, 1 skipped` at `859f883c`. Zero failed and zero errors at
 each; the passed count may only rise. If C5's named test file is not in the list, run it
 separately beside each reading and say so. Then `python3 -m ruff check` over every `.py`
 path the round touched, and `python3 -m apps.cli.main integrity check --json`, all five
 checks `pass`. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C6, never committed.
 Run every test file C3 to C6 touched UNMUTATED first and report it (exit 0). Then each
 mutation alone, reverted before the next, reporting the summary line, the exit code and
 the failing test names:
 (a) in `_cmd_do_order`'s `--json` path, delete the failed-walk branch so a failed walk
     reaches `emit_ok` — C3's repaired unknown-project test must fail.
 (b) in `grouped.py`, make the usage refusals' `--json` test never hold (name the line
     you changed) — C4's `--json` tests and the four repaired parameters must fail.
 (c) `_cmd_discover_commands`'s `no_target_repo` refusal passes `json_output=False` —
     C5's envelope test must fail.
 (d) `_cmd_job_context`'s refusal passes `invalid_job_id` again — C6's test must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C7: `git status --porcelain` empty; `git log --oneline -n 9`;
 `git worktree list` (primary plus the three `remedy/job-*`); the push's real outcome;
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 3 of feature F283, round 10, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 10, then the tail of the refusal sweep as `.agent/plan.md` lists it.
State the open-findings count, 23 after this round, and the operator-questions count, 2.
