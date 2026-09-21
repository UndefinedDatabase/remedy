STEP F283 R7 — R-1023, R-1024, and the `brain` and `patch` groups

GOAL
Book round 6's PASS and R-1022's `Done:`, register R-1023 and R-1024, record DECISION F283
D2, then repair both findings and move the `brain` and `patch` groups' refusal pairs onto
`fail()`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit.

THE MIGRATION RULE (DECISION F277 D7, D8, D9 — read D8 and D9 in `.agent/decisions.md`)
A pair `print(f"Error: <msg>", file=sys.stderr)` + `sys.exit(<n>)` becomes
  fail("<token>", f"<msg>", json_output=<flag>[, exit_code=<n>])
— the message WITHOUT `Error: `; `exit_code` only when <n> is not 1; <flag> is the
handler's own `json_output` when it has one, else `False`. TOKENS: one per CONDITION,
repo-wide, and AN EXISTING SPELLING WINS. Round 6 minted two forks of existing spellings
(R-1023), so this round's rule is stricter: before you use ANY token, run a search for
`fail("` over `apps/cli/` and read the tokens already in use; where one names the same
condition, use it. `job_not_found` is the token for a `JobNotFoundError`. A pair whose
`print` does NOT begin with `Error: `, or with more than one `print` before its exit, is
NOT migrated — it stays, and the module's ratchet counts it.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r7-scratch/`   YOURS for logs, captures and scripts. The reviewer's
      counter is `.remedy-wt/f283-r6-scratch/pairs.py` (read-only; usage
      `python3 <it> brain.py patch.py`).

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
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `037acc3d`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r7-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r7-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 28 | 2089 | fadcbee647cfc622e02e2c17c7434cbac6f18e7d417a5d8f988ca24ae9d51882 |
| ledger.md | 8 | 7647 | 1da8fc05d0c0c31c5da1f381cd9a2a4b0fa476ece34a8cf1e88b906d689d7faa |
| plan.md | 36 | 1616 | ae212d0a0781e0a438146e0d209b90621cc68823ed218525e3b5d20ed75bcbd8 |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 6 `Gate:` entry, R-1022's `Done:` line and
the R-1023 and R-1024 registrations; decisions carries DECISION F283 D2. `plan.md` is a
REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C7, in this order.

C1 — `.agent/authored/f283-r7-block.md` := this block; `.agent/authored/f283-r7-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R7 C1: copy round 7 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R7 C2: book round 6's PASS, resolve R-1022, register R-1023 and R-1024`

C3 — R-1023
  SPEC, `apps/cli/commands/decision.py`: `job_has_no_project` becomes `no_project`; both
  `invalid_reason` sites become `invalid_argument`. Nothing else changes.
  SPEC, `tests/cli/test_decision_cmd.py`: a test that reads `decision.py`'s AST, collects
  the first argument of every `fail(...)` call, and asserts the set EQUALS a pinned
  constant you write from the measured result after the rename. Its docstring names
  R-1023 and DECISION F277 D8.
  Subject: `F283 R7 C3: decision's tokens join the vocabulary the product already has`

C4 — R-1024, under DECISION F283 D2 (read it in the payload before you start)
  SPEC, `apps/cli/cost_preview_confirm.py`: `confirm_cost_preview(..., json_output: bool =
  False)`. With the flag off, NOTHING changes — same lines, same streams, same exit. With
  it on: every line the helper writes for a human, including the prompt `input()` would
  write to stdout, goes to stderr with the same text; and the non-terminal refusal
  becomes `fail("confirmation_required", <the same sentence without "Error: ">,
  json_output=json_output, exit_code=EXIT_USAGE)`. Import `fail` from
  `apps.cli.json_envelope`.
  SPEC, `apps/cli/commands/job.py`: `_cmd_job_run_cycles` passes its `json_output`.
  SPEC, tests: in `tests/cli/test_cost_preview_confirm.py`, under `json_output=True`: the
  `--yes` path writes NOTHING to stdout and the estimate line to stderr; the non-terminal
  path exits 2 with an empty stderr and an envelope `confirmation_required`; the existing
  text-mode tests stay unchanged. `tests/orchestration/test_long_run_executor.py`'s
  `fake_confirm` stand-in names its keywords and has no `json_output`: it gains
  `json_output=False` and records nothing new; change nothing else in that file.
  In `tests/test_cli_main.py`,
  `test_the_run_cycles_caller_threads_json_output` parses the WHOLE of stdout as one JSON
  object instead of its last line, and its comment says why that is now possible.
  Subject: `F283 R7 C4: the cost-preview gate keeps stdout for the machine under --json`

C5 — the `brain` group: every pair the rule reaches in `apps/cli/commands/brain.py`.
  SPEC, `tests/cli/test_job_refusal_envelope.py`: a class asserting, with the existing
  `_refusal_sites(path)`, that `brain.py` has no flagged and no unflagged pair left (or
  exactly the count of pairs the rule excluded, named in its docstring). One envelope
  test, in the brain test file you judge nearest (name it): a `--json` brain command
  whose job id resolves but whose job record is missing answers `job_not_found` with an
  empty stderr. If no such command is reachable without building a job, say so and test
  the nearest refusal you can reach.
  Subject: `F283 R7 C5: brain refusals answer through fail()`

C6 — the `patch` group: every pair the rule reaches in `apps/cli/commands/patch.py`; the
  multi-print sites stay. Ratchet class as in C5, counting what stayed. One envelope test
  in `tests/cli/test_patch_cmd.py` for a `--json` patch refusal you can reach.
  Subject: `F283 R7 C6: patch refusals answer through fail()`

C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R7 C7: rewrite handoff for round 7`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the four `.agent/authored/f283-r7-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/handoff.md`, `apps/cli/commands/decision.py`,
   `apps/cli/cost_preview_confirm.py`, `apps/cli/commands/job.py`,
   `apps/cli/commands/brain.py`, `apps/cli/commands/patch.py`,
   `tests/cli/test_decision_cmd.py`, `tests/cli/test_cost_preview_confirm.py`,
   `tests/test_cli_main.py`, `tests/orchestration/test_long_run_executor.py`,
   `tests/cli/test_job_refusal_envelope.py`,
   `tests/cli/test_patch_cmd.py`, and the ONE brain test file C5 names. A test a
   migration breaks is repaired in that same commit ONLY inside this set; otherwise STOP.
   Report the set you measure. Nothing under `packages/` or `docs/`, no `README.md` or
   `apps/cli/json_envelope.py`, and none of `.agent/candidates.md`, `.agent/context.md`,
   `.agent/operator_questions.md`, `.agent/prose_slips.md`.
4. Existing tests that assert a refusal's text keep passing UNCHANGED — they are the
   identity proof. If one fails, the migration changed bytes: fix the migration.
5. Every commit leaves the G4 selection green.
6. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
7. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
8. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C7 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r7-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r7-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `037acc3d` (472228 bytes)
     plus ledger.md; the reviewer composed 479875. `.agent/decisions.md` (1791820) plus
     decisions.md; the reviewer composed 1793909.
 (b) Line-anchored on the committed ledger: `^- R-1022 — ` 1, `^Done: R-1022 — ` 1,
     `^- R-1023 — ` 1, `^- R-1024 — ` 1, and no `^Done: ` line for either. Open set by
     distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at
     `037acc3d` and at C2: the reviewer measured 24 and 25, ADDED exactly `R-1023` and
     `R-1024`, REMOVED exactly `R-1022`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE MIGRATION, COUNTED FROM THE TREE — for every commit C3 to C6 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C6 run
 `python3 .remedy-wt/f283-r6-scratch/pairs.py brain.py patch.py decision.py` and report
 its summary lines; the reviewer read at `037acc3d`
 `brain.py exits 13 mechanical 13 flagged 6 unflagged 7` and
 `patch.py exits 18 mechanical 13 flagged 7 unflagged 6`. List every token C3, C4, C5
 and C6 use, with its line and `new` or `reused`, and for each `new` one the search you
 ran. Report `git diff --name-only 037acc3d <C6> -- packages/`, which must print nothing.

G4 THE TARGETED SELECTION, in the primary checkout at C6:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/cli/test_decision_cmd.py tests/cli/test_decision_answers.py tests/cli/test_plan_approval.py tests/orchestration/test_proposal_decision.py tests/cli/test_mission_cmd.py tests/cli/test_cost_preview.py tests/cli/test_cost_preview_confirm.py tests/orchestration/test_long_run_executor.py tests/test_cli_main.py tests/test_brain_detail.py tests/test_brain_smoke.py tests/test_brain_viewer.py tests/test_agent_loop.py tests/test_cockpit.py tests/test_timeline.py tests/test_trust_report.py tests/test_project_constitution.py tests/test_project_brain.py tests/test_context_coverage.py tests/test_patch_intent_approval.py tests/test_patch_apply.py tests/cli/test_patch_cmd.py tests/cli/test_snapshot_cli_runtime.py tests/cli/test_cli_ux.py tests/test_grouped_cli.py tests/orchestration/test_import_reachability.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/docs/; echo "REAL_EXIT=$?"'
```
 The reviewer read `2071 passed` at real exit code 0 at `037acc3d`. If C5's test file is
 outside that list, add it and say so. Report your summary line and exit code; zero
 failed, zero xfailed, and the passed count may only rise. Then `python3 -m ruff check`
 over every `.py` path the round touched, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass`. DO NOT run
 the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C6, never committed.
 Run every test file C3 to C6 touched UNMUTATED first and report it (exit 0). Then each
 mutation alone, reverted before the next, reporting the summary line, the exit code and
 the failing test names:
 (a) `no_project` in `decision.py` goes back to `job_has_no_project` — C3's pinned-set
     test must fail.
 (b) in `confirm_cost_preview`, the `--yes` branch prints its line to stdout even under
     the flag — C4's `--yes` test and the `test_the_run_cycles_caller_threads_json_output`
     test must fail.
 (c) `_cmd_job_run_cycles` stops passing `json_output` to `confirm_cost_preview` — report
     what goes red; if nothing does, say so plainly (a probe, not a colour).
 (d) one migrated `fail()` in `brain.py` is put back as its old print-then-exit pair —
     C5's ratchet must fail.
 (e) one migrated `fail()` in `patch.py` is put back the same way — C6's ratchet must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C7: `git status --porcelain` empty; `git log --oneline -n 9`;
 `git worktree list` (primary plus the three `remedy/job-*`); the push's real outcome;
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 2 of feature F283, round 7, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 7, then round 8 — R-1023's and R-1024's `Done:` lines booked in its first
commit, and the non-mechanical `job.py` sites: the verification-failure loop, the
single-pass `job run --json` success line, and `_cmd_resume`'s two hand-rolled objects.
State the open-findings count, 25 after this round, and the operator-questions count, 2.
