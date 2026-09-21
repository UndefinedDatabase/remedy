STEP F283 R11 — the `stats` refusals and `job stop`, the helpers taking the caller's flag

GOAL
Book round 10's PASS and resolve R-1026, then move every refusal in `stats_ledger_cmd.py`,
`bench_cmd.py`, `failure_stats_cmd.py` and `job_stop_cmd.py` onto `fail()` — the exiting
validation helpers taking the caller's `json_output` — and pin the two refusals round 10
left untested.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit.

THE MIGRATION RULE (DECISIONs F277 D7, D8, D9 and F283 D4 — read them in `.agent/decisions.md`)
A refusal `print(f"Error: <msg>", file=sys.stderr)` followed by `sys.exit(<n>)` OR by
`raise SystemExit(<n>)` becomes `fail("<token>", f"<msg>", json_output=<flag>[,
exit_code=<n>])` — the message WITHOUT its prefix, `exit_code` only when <n> is not 1,
<flag> the caller's own `json_output`. A BRANCHED site — `if json_output:
print(json.dumps({...}))` / `else: print(f"Error: <msg>", ...)` then one exit — becomes ONE
`fail()` whose token is named below and whose payload keeps every other key that JSON
object carried except `ok` and `error`. The text branch stays byte-identical. An EXITING
HELPER — a function without the flag that prints a refusal and exits — gains a REQUIRED
keyword-only `json_output: bool` (no default, so a caller that forgets it is a
`TypeError`, not a silent prose answer), and every caller passes its own flag.

THE TOKENS, fixed here after the reviewer's search of `fail("` over `apps/cli/` at
`590abe57` (reused unless marked new; confirm each new one by your own search):
- `--by` not a grouping, `--since`/`--until` not ISO-8601, `--multiplier` not a number or
  not above 0 → `invalid_argument` (exit 2).
- `--all-projects` given to an action that needs one project → `option_not_applicable`
  (exit 2).
- no project resolved → `no_project` (exit 1).
- an evidence directory required and empty → `missing_argument` (exit 2); given and not a
  directory → `path_not_found` (new, exit 2).
- the token ledger unreadable (`sqlite3.Error`) → `ledger_unreadable` (new, exit 1), both
  sites; `FailureStatsError` → `evidence_unreadable` (new, exit 1). Their old JSON put the
  exception text in `error`; it now sits in `message`.
- `job stop`: a job that does not exist → `job_not_found` at `EXIT_UNKNOWN_JOB` with
  `job_id`; `StopControlError` from `validate_job_id` → `invalid_job_id` (exit 2);
  `job_not_stoppable` with `job_id` and `job_status`; `stop_not_requested` with `detail`
  and `job_id` (both exit 1).
`stats verify-ledger`'s `raise SystemExit(EXIT_DRIFT)` is a RESULT, not a refusal: it stays.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r11-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r11-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt`, `build_selection.py` and `run_sel.py`, which are
      read-only to you. `run_sel.py <dir> <label>` runs the selection in <dir> and prints
      the exit code, summary and bad node ids.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a file in your
scratch directory (written with your file tool) for counting, hashing, copying
(`shutil.copyfile`) and running pytest; use `git -C <dir>` for a worktree.
NEVER USE `git stash` IN ANY FORM: the stash stack is shared with other sessions on this
machine. Make each commit's edits, verify, commit, then make the next commit's edits.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `590abe57`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r11-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r11-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 4563 | b701059a12f572e5242410fe344e4f43abbaaa9ba187df18740219eae6ff188d |
| plan.md | 36 | 1555 | 6d159a6c91398989243abf4115b95d88ed9b90d6a77460b76a8895ebeff9576c |

`ledger.md` is an APPEND beginning with the single newline that separates records: the
round 10 `Gate:` entry and the `Done:` line of R-1026. `plan.md` is a REWRITE. Never retype
or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r11-block.md` := this block; `.agent/authored/f283-r11-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R11 C1: copy round 11 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md
  Subject: `F283 R11 C2: book round 10's PASS, resolve R-1026`

C3 — `apps/cli/commands/stats_ledger_cmd.py`, `apps/cli/commands/bench_cmd.py` and
  `apps/cli/commands/failure_stats_cmd.py`: every refusal by the rule and the tokens
  above. The exiting helpers — `_validate_by`, `_validate_period_bound`,
  `_one_project_ledger`, `_require_evidence_dir`, `_validate_multiplier`,
  `_one_project_history`, `_validate_since` — take the required `json_output` and every
  caller passes its own. SPEC, tests: repair in this commit every assertion in
  `tests/cli/test_stats_cost.py`, `tests/cli/test_stats_report.py`,
  `tests/cli/test_stats_bench.py` and `tests/cli/test_failure_cmd.py` that pinned an old
  `--json` shape (prose on stderr, or `error` holding exception text) or called a helper
  without the flag. In each of the four files, at least one test that a `--json` refusal
  REACHED THROUGH A HELPER answers one envelope (`schema_version` 1, `ok` false, its
  token) with an empty stderr — one of them `ledger_unreadable`. In
  `tests/cli/test_job_refusal_envelope.py`, a ratchet class reading the AST of the three
  modules: no `raise SystemExit` remains except `stats_ledger_cmd.py`'s one
  `EXIT_DRIFT`, and `pairs`-style no print-then-exit pair survives.
  Subject: `F283 R11 C3: stats refusals answer through fail(), helpers take the flag`

C4 — `apps/cli/commands/job_stop_cmd.py`: `_unknown_job`, the `validate_job_id` refusal,
  `job_not_stoppable` and `stop_not_requested` by the rule and the tokens above.
  SPEC, tests: repair the old-shape assertions in `tests/cli/test_job_stop.py`; its
  existing `job_not_found`, `job_not_stoppable` and `stop_not_requested` tests assert
  `schema_version` 1 and their kept keys; one test pins `invalid_job_id` at exit 2 under
  `--json`. Extend C3's ratchet class to `job_stop_cmd.py` (no `raise SystemExit`).
  Subject: `F283 R11 C4: job stop refusals answer through fail()`

C5 — the two refusals round 10 left untested, in `tests/cli/test_job_refusal_envelope.py`:
  `apps/cli/commands/test_cmds.py::_cmd_test_status`'s `job_not_found` (reach it with a
  resolver that accepts the id and a store without it) and `_cmd_discover_commands`'s
  `job_store_error` (a `require_job_plan` that raises), each one envelope with its token
  and an empty stderr under `--json`. In `tests/test_command_discovery.py`, the docstring
  of `TestDiscoverNoTargetRepoAnswersInTheEnvelope` names the migration rule's branched
  form, not DECISION F283 D5. Tests and that docstring only.
  Subject: `F283 R11 C5: pin the two test-group refusals round 10 left untested`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R11 C6: rewrite handoff for round 11`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the three `.agent/authored/f283-r11-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/commands/stats_ledger_cmd.py`, `apps/cli/commands/bench_cmd.py`,
   `apps/cli/commands/failure_stats_cmd.py`, `apps/cli/commands/job_stop_cmd.py`,
   `tests/cli/test_stats_cost.py`, `tests/cli/test_stats_report.py`,
   `tests/cli/test_stats_bench.py`, `tests/cli/test_failure_cmd.py`,
   `tests/cli/test_job_stop.py`, `tests/cli/test_job_refusal_envelope.py` and
   `tests/test_command_discovery.py`. Report the set you measure. Nothing under
   `packages/` or `docs/`, no `README.md`, no `scripts/`, no `apps/cli/json_envelope.py`,
   and none of `.agent/decisions.md`, `.agent/candidates.md`, `.agent/context.md`,
   `.agent/operator_questions.md`, `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves the G4 selection at zero failed: run it after C3, C4 and
   C5 and report each reading.
5. If a gate goes red and the fix is outside constraint 3 — a test file outside the set
   pinning an old shape counts — STOP: commit and push what is verified, write an honest
   handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r11-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r11-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `590abe57` (496649 bytes)
     plus ledger.md; the reviewer composed 501212.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R10 — ` 1, `^Done: R-1026 — ` 1.
     Open set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py`
     at `590abe57` and at C2: the reviewer measured 23 and 22, ADDED empty, REMOVED
     exactly `R-1026`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 to C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C4
 report, per module of C3 and C4, the `raise SystemExit` count before and after; the
 reviewer read at `590abe57` stats_ledger 9, bench 3, failure_stats 2, job_stop 4, and
 after C4 they must read 1, 0, 0, 0. List every token C3 and C4 use, with its line and
 `new` or `reused`, and for each `new` one the search you ran. `git diff --name-only
 590abe57 <C5> -- packages/` must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r11-scratch/selection.txt` is one line of 106
 space-separated paths: round 10's selection plus every test file a search for this
 round's targets found. Run `python3 .remedy-wt/f283-r11-scratch/run_sel.py . <label>` in
 the primary checkout after C3, C4 and C5 and report each summary line and exit code. The
 reviewer read `4457 passed, 1 skipped` at `590abe57`. Zero failed and zero errors at
 each; the passed count may only rise. Then `python3 -m ruff check` over every `.py` path
 the round touched, and `python3 -m apps.cli.main integrity check --json`, all five checks
 `pass`. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed.
 Run every test file C3 to C5 touched UNMUTATED first and report it (exit 0). Then each
 mutation alone, reverted before the next, reporting the summary line, the exit code and
 the failing test names:
 (a) the `ledger_unreadable` refusal your C3 test reaches passes `json_output=False` —
     that test must fail.
 (b) one helper's `fail()` is put back as its old `print` + `raise SystemExit` (name
     it) — the C3 ratchet and that helper's envelope test must fail.
 (c) `job stop`'s `invalid_job_id` refusal passes a different token — C4's test must
     fail.
 (d) `_cmd_test_status`'s `job_not_found` refusal passes a different token — C5's test
     must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`;
 `git worktree list` (primary plus the three `remedy/job-*`); `git stash list` unchanged
 from its reading before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the
 handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 3 of feature F283, round 11, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 11, then the rest of the tail as `.agent/plan.md` lists it. State the
open-findings count, 22 after this round, and the operator-questions count, 2.
