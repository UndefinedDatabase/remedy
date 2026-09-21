STEP F283 R12 — the rest of the refusal tail, and D7 for the lines `fail()` cannot write

GOAL
Book round 11's PASS and record DECISION F283 D7, then move the `patch`, `snapshot`,
`real_test_execution` and `self` refusals onto `fail()`; answer the envelope under `--json`
in `config`, `project current`, `patch approve-hunks` and `mission run` under D7, and
collapse the cost-preview refusal; and pin the three `stats` refusals round 11 left
unpinned.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit. Read DECISION F283 D7 in this round's decisions payload before C4.

THE MIGRATION RULE (DECISIONs F277 D7, D8, D9 and F283 D4 — read them in `.agent/decisions.md`)
A refusal `print(f"Error: <msg>", file=sys.stderr)` followed by `sys.exit(<n>)` or `raise
SystemExit(<n>)` becomes `fail("<token>", f"<msg>", json_output=<flag>[, exit_code=<n>])` —
the message WITHOUT its prefix, `exit_code` only when <n> is not 1, <flag> the handler's
own flag (`json_output`, `as_json`, or `getattr(args, "json", False)` where the handler reads
it so). A BRANCHED site — `if <flag>: print(json.dumps({...}))` / `else: print(f"Error:
<msg>", ...)` then one exit — becomes ONE `fail()` whose token is the object's own `error`
value and whose payload keeps every other key that object carried except `ok` and `error`.
The text branch stays byte-identical. D7 governs the sites it names and nothing else.

THE TOKENS, fixed here after the reviewer's search of `fail("` over `apps/cli/` at
`e964343b` (reused unless marked new; confirm each new one by your own search):
- `patch revert`: `ambiguous_intent_id` (new; keeps `intent_id`, `apply_ids`),
  `no_apply_record` (new; keeps `intent_id`), `no_target_repo` (keeps `job_id`).
- `snapshot inspect` / `snapshot list-applies`: `job_not_found` (keeps `job_id`),
  `snapshot_not_found` (new; keeps `snapshot_id`).
- `test result`: `test_run_not_found` (new); `snapshot show`: `snapshot_proof_not_found`
  (new); `test list` and `config list`: `invalid_list_option`.
- `self propose --top`: `invalid_argument` (exit 1, as today).
- Under D7: `project_not_found` / `invalid_project_selector` (new) at exit 3;
  `unknown_config_key`, `config_file_exists`, `invalid_config_value` (all new);
  `patch approve-hunks` the refusal's own `result.code`, keeping `hunk_ids`;
  `mission run`'s empty id `missing_argument`; the cost preview `confirmation_required`.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r12-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r12-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt`, `build_selection.py` and `run_sel.py`, which are
      read-only to you. `run_sel.py <dir> <label>` runs the selection in <dir> and prints
      the exit code, summary and bad node ids. The pair counter is
      `.remedy-wt/f283-r6-scratch/pairs.py` (read-only).

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
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `e964343b`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r12-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r12-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 36 | 2806 | 60badcb05830fe7b15b76f2a21b4eb663a54962c3a00d7c0d4e1115596de3b43 |
| ledger.md | 2 | 3013 | a09e1bda41b4ebbd116d3cdeae4a16102298d49744bfdb0dbacc15f454c6c96a |
| plan.md | 33 | 1338 | 47e3b3c01045a93600566b7036f11e3093658cebdc1c0c0efe774b5d5b6abd96 |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 11 `Gate:` entry; decisions carries
DECISION F283 D7. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r12-block.md` := this block; `.agent/authored/f283-r12-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R12 C1: copy round 12 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R12 C2: book round 11's PASS, record D7`

C3 — the plain rule: `apps/cli/commands/patch.py::_cmd_revert_patch_intent`'s three
  branched sites, `apps/cli/commands/snapshot_cmds.py`'s three, the three refusals of
  `apps/cli/commands/real_test_execution_cmd.py`, and `apps/cli/commands/self_cmd.py`'s
  `--top` refusal. `_cmd_show_patch_intent`'s two-line refusal and the text-only
  revert-blocked lines stay. SPEC, tests: repair any assertion that pinned an old `--json`
  shape; add, in the test file nearest each module (`tests/cli/test_snapshot_cli_runtime.py`,
  `tests/cli/test_real_test_execution_cli.py`, `tests/cli/test_self_dogfood_cli.py`, and
  for `patch revert` whichever of `tests/cli/test_patch_cmd.py` or
  `tests/cli/test_snapshot_cli_runtime.py` already holds its tests — name it), at least one
  `--json` envelope test per module (`schema_version` 1, `ok` false, the token, the kept
  keys, empty stderr). In `tests/cli/test_job_refusal_envelope.py`, ratchet classes for
  `snapshot_cmds.py`, `real_test_execution_cmd.py` and `self_cmd.py` (no pair and no
  `sys.exit` refusal left), and `TestPatchRefusalsAreAllMigrated`'s docstring notes round
  12.
  Subject: `F283 R12 C3: patch, snapshot, test-record and self refusals answer through fail()`

C4 — DECISION F283 D7: `apps/cli/commands/config_cmd.py` (`config list` by the plain rule;
  `get`, `init`, `set` under D7), `apps/cli/commands/project.py::_cmd_project_current`'s
  `(ProjectNotFoundError, InvalidProjectSelectorError)` branch, `patch.py::_cmd_approve_hunks`'s
  refusal, `apps/cli/commands/worker_facade_cmd.py` (`_err` deleted, its caller calls
  `fail()`), and `apps/cli/cost_preview_confirm.py`'s refusal collapsed to one `fail()`.
  SPEC, tests: repair `tests/cli/test_patch_cmd.py`'s `payload["code"]` assertions to
  `payload["error"]`, and any other old-shape assertion; add `--json` envelope tests for
  `config get`, `config init`, `config set` in `tests/cli/test_config_cmd.py`, for `project
  current` with an unknown selector in `tests/cli/test_project_current.py` (exit 3), and a
  text-mode test for each of `config get` and `project current` pinning the unchanged
  bytes. `tests/cli/test_worker_facade_cmd.py` pins `Error: run_id required` if it reaches
  that line. Update the `project` ratchet's docstring in
  `tests/cli/test_job_refusal_envelope.py` (its flagged site now carries a `--json` guard).
  Subject: `F283 R12 C4: config, project current, approve-hunks and mission run answer the envelope (D7)`

C5 — the three `stats` refusals round 11 left unpinned, tests only: in
  `tests/cli/test_failure_cmd.py`, `stats failures --since <not ISO> --json` answers one
  envelope with `invalid_argument` at exit 2 (reached through `_validate_since`); in
  `tests/cli/test_stats_cost.py`, `backfill-ledger` or `verify-ledger` under `--json` with an
  evidence directory that does not exist answers `path_not_found`, and with
  `--all-projects` answers `option_not_applicable`, both at exit 2, empty stderr.
  Subject: `F283 R12 C5: pin the three stats refusals round 11 left unpinned`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R12 C6: rewrite handoff for round 12`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the four `.agent/authored/f283-r12-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/commands/patch.py`, `apps/cli/commands/snapshot_cmds.py`,
   `apps/cli/commands/real_test_execution_cmd.py`, `apps/cli/commands/self_cmd.py`,
   `apps/cli/commands/config_cmd.py`, `apps/cli/commands/project.py`,
   `apps/cli/commands/worker_facade_cmd.py`, `apps/cli/cost_preview_confirm.py`,
   `tests/cli/test_patch_cmd.py`, `tests/cli/test_snapshot_cli_runtime.py`,
   `tests/cli/test_real_test_execution_cli.py`, `tests/cli/test_self_dogfood_cli.py`,
   `tests/cli/test_config_cmd.py`, `tests/cli/test_project_current.py`,
   `tests/cli/test_worker_facade_cmd.py`, `tests/cli/test_cost_preview_confirm.py`,
   `tests/cli/test_job_refusal_envelope.py`, `tests/cli/test_failure_cmd.py` and
   `tests/cli/test_stats_cost.py`. Report the set you measure. Nothing under `packages/` or
   `docs/`, no `README.md`, no `scripts/`, no `apps/cli/json_envelope.py`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
   `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves the G4 selection at zero failed: run it after C3, C4 and
   C5 and report each reading.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r12-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r12-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `e964343b` (501212 bytes)
     plus ledger.md; the reviewer composed 504225. `.agent/decisions.md` (1803831)
     plus decisions.md; the reviewer composed 1806637.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R11 — ` 1. Open set by distinct
     id via `open_finding_ids` from `scripts/rotate_live_review.py` at `e964343b` and at
     C2: the reviewer measured 22 and 22, ADDED empty, REMOVED empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 to C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C5 run
 `python3 .remedy-wt/f283-r6-scratch/pairs.py patch.py config_cmd.py
 real_test_execution_cmd.py self_cmd.py worker_facade_cmd.py ../cost_preview_confirm.py
 project.py snapshot_cmds.py` and report its summary lines. The reviewer read at
 `e964343b`: patch `mechanical 2`, config `mechanical 2`, real_test_execution
 `mechanical 3`, self `mechanical 1`, worker_facade `mechanical 1`, cost_preview
 `mechanical 1`, project `mechanical 2`, snapshot `exits 3 mechanical 0`. At C5
 real_test_execution, self, worker_facade and cost_preview must read `mechanical 0`,
 snapshot `exits 0`, config `mechanical 1` (the `get` text branch D7 keeps); patch and
 project unchanged. List every token C3 and C4 use, with its line and `new` or `reused`,
 and for each `new` one the search you ran. `git diff --name-only e964343b <C5> --
 packages/` must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r12-scratch/selection.txt` is one line of 110
 space-separated paths: round 11's selection plus every test file a search for this
 round's targets found. Run `python3 .remedy-wt/f283-r12-scratch/run_sel.py . <label>` in
 the primary checkout after C3, C4 and C5 and report each summary line and exit code. The
 reviewer read `4548 passed, 1 skipped` at `e964343b`. Zero failed and zero errors at
 each; the passed count may only rise. Then `python3 -m ruff check` over every `.py` path
 the round touched, and `python3 -m apps.cli.main integrity check --json`, all five checks
 `pass`. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed.
 Run every test file C3 to C5 touched UNMUTATED first and report it (exit 0). Then each
 mutation alone, reverted before the next, reporting the summary line, the exit code and
 the failing test names:
 (a) `snapshot_not_found`'s refusal passes `json_output=False` — C3's snapshot envelope
     test must fail.
 (b) `test_run_not_found` renamed — C3's test-record envelope test must fail.
 (c) `project current`'s `--json` guard removed, so the branch answers prose in both
     modes — C4's `project current` envelope test must fail.
 (d) `config set`'s `invalid_config_value` renamed — C4's `config set` test must fail.
 (e) `_validate_since`'s refusal passes `json_output=False` — C5's `stats failures` test
     must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`;
 `git worktree list` (primary plus the three `remedy/job-*`); `git stash list`'s first line
 unchanged from its reading before C1; the push's real outcome; `gh pr list --state open
 --json number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not
 the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 3 of feature F283, round 12, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 12, then `runtime_cmd.py` as `.agent/plan.md` lists it. State the
open-findings count, 22 after this round, and the operator-questions count, 2.
