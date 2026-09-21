STEP F283 R9 — the `project` group, and the three `do` refusals round 8 declined

GOAL
Book round 8's PASS, the `Done:` lines of R-1019 and R-1025 and DECISION F283 D4, then move
the `project` group's refusal pairs onto `fail()` under D4, and the three `do` refusals
round 8 correctly declined together with the tests that pinned their old `--json` shape.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit.

THE MIGRATION RULE (DECISION F277 D7, D8, D9 — read D8 and D9 in `.agent/decisions.md`;
and DECISION F283 D4 in this round's decisions payload)
A pair `print(f"Error: <msg>", file=sys.stderr)` + `sys.exit(<n>)` becomes
  fail("<token>", f"<msg>", json_output=<flag>[, exit_code=<n>])
— the message WITHOUT its prefix; `exit_code` only when <n> is not 1; <flag> is the
handler's own `json_output` when it has one, else `False`. UNDER D4 a `print` beginning
with `ERROR: ` is migrated the same way. TOKENS: one per CONDITION, repo-wide, and AN
EXISTING SPELLING WINS: before you use ANY token, search `fail("` over `apps/cli/` and
read the tokens in use; where one names the same condition, use it. A pair whose `print`
has NO prefix (e.g. `print(str(exc), file=sys.stderr)`), or with more than one `print`
before its exit, is NOT migrated — it stays and the module's ratchet counts it. A pair
whose function has ALREADY written a JSON document to stdout under the flag is NOT
migrated either (round 8's `_cmd_do_order` finding): a `fail()` there would put a second
object on stdout.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r9-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt` and `build_selection.py`, which are read-only to you.
      The pair counter is `.remedy-wt/f283-r6-scratch/pairs.py` (read-only).

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `$?` or `${...}` outside a `bash -c`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a
file in your scratch directory for counting, hashing, copying (`shutil.copyfile`) and for
running pytest over the selection file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `432c2eb4`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r9-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r9-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 28 | 1992 | 3a1f07ba53d7e1715cfa6c13768828d0808226077c56780ea7551a585f881b5a |
| ledger.md | 6 | 5051 | b611d2cdcb033d76493ee1e4ff724451653d516f93ba38203f582d650e9a9265 |
| plan.md | 35 | 1502 | 6586cb3fe82c081328df99f71c6cea7fc5fa7a58303a606adeade8d10f52d5eb |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 8 `Gate:` entry and the `Done:` lines of
R-1019 and R-1025; decisions carries DECISION F283 D4. `plan.md` is a REWRITE. Never
retype or edit a payload.

BUNDLE — commits C1 to C5, in this order.

C1 — `.agent/authored/f283-r9-block.md` := this block; `.agent/authored/f283-r9-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R9 C1: copy round 9 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R9 C2: book round 8's PASS, resolve R-1019 and R-1025`

C3 — the `project` group: every pair the rule reaches in `apps/cli/commands/project.py`.
  SPEC, tests: in `tests/cli/test_job_refusal_envelope.py`, a ratchet class as rounds 6 to
  8 wrote, counting what stayed and naming why in its docstring. One envelope test in the
  `project` test file you judge nearest (name it) for a `--json` refusal you can reach;
  and one test there that a formerly `ERROR: ` refusal you can reach now writes `Error: `
  in text mode — the D4 change, asserted rather than assumed. A test that asserted an old
  `--json` shape (prose on stderr) is repaired to the envelope in this same commit; a
  text-mode assertion that breaks means the migration altered bytes beyond D4 — fix the
  migration.
  Subject: `F283 R9 C3: project refusals answer through fail()`

C4 — the three `do` refusals round 8 declined: `_cmd_do`'s contract-template lookup,
  `_cmd_run_show`'s run lookup and `_cmd_run_list`'s list-option refusal. Migrate each by
  the rule, and repair in this same commit the tests in `tests/cli/test_do_sequence_cli.py`
  and `tests/cli/test_cli_ux.py` that asserted their old `--json` shape; update `do_cmd.py`'s
  ratchet class in `tests/cli/test_job_refusal_envelope.py` to the new count.
  `_cmd_do_order`'s failure line stays, with its comment.
  Subject: `F283 R9 C4: the last three do refusals answer through fail()`

C5 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R9 C5: rewrite handoff for round 9`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the four `.agent/authored/f283-r9-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/handoff.md`, `apps/cli/commands/project.py`, `apps/cli/commands/do_cmd.py`,
   `tests/cli/test_job_refusal_envelope.py`, `tests/cli/test_do_sequence_cli.py`,
   `tests/cli/test_cli_ux.py`, and the ONE `project` test file C3 names. Report the set
   you measure. Nothing under `packages/` or `docs/`, no `README.md` or
   `apps/cli/json_envelope.py`, and none of `.agent/candidates.md`, `.agent/context.md`,
   `.agent/operator_questions.md`, `.agent/prose_slips.md`.
4. EVERY COMMIT, not only the last, leaves the G4 selection at zero failed: run it after
   C3 and after C4 and report both readings. Round 8 broke this for four commits by
   changing an import line a substring guard read; read the guards a file carries before
   changing its imports.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C5 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r9-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r9-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `432c2eb4` (487106 bytes)
     plus ledger.md; the reviewer composed 492157. `.agent/decisions.md` (1797316) plus
     decisions.md; the reviewer composed 1799308.
 (b) Line-anchored on the committed ledger: `^Done: R-1019 — ` 1, `^Done: R-1025 — ` 1.
     Open set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py`
     at `432c2eb4` and at C2: the reviewer measured 24 and 22, ADDED empty, REMOVED
     exactly `R-1019` and `R-1025`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 and C4 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C4 run
 `python3 .remedy-wt/f283-r6-scratch/pairs.py project.py do_cmd.py` and report its
 summary lines; the reviewer read at `432c2eb4` `project.py exits 25 mechanical 25
 flagged 11 unflagged 14` and `do_cmd.py exits 5 mechanical 4 flagged 4 unflagged 0`.
 List every token C3 and C4 use, with its line and `new` or `reused`, and for each `new`
 one the search you ran. Report `git diff --name-only 432c2eb4 <C4> -- packages/`, which
 must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r9-scratch/selection.txt` is one line of 79
 space-separated paths: round 8's widened selection plus the `project` test files. Run
 `python3 -m pytest -q -p no:cacheprovider -n auto` over exactly those paths (read them
 from the file in a script), in the primary checkout, after C3 and after C4, and report
 both summary lines and exit codes. The reviewer read `3390 passed` at `432c2eb4`. Zero
 failed, zero errors, zero xfailed at each; the passed count may only rise. If C3's
 `project` test file is not in the list, add it and say so. Then `python3 -m ruff check`
 over every `.py` path the round touched, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass`. DO NOT run
 the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C4, never committed.
 Run every test file C3 and C4 touched UNMUTATED first and report it (exit 0). Then each
 mutation alone, reverted before the next, reporting the summary line, the exit code and
 the failing test names:
 (a) one migrated `fail()` in `project.py` is put back as its old print-then-exit pair —
     C3's ratchet must fail.
 (b) the `project` refusal C3's envelope test reaches passes `json_output=False` — that
     test must fail.
 (c) the formerly `ERROR: ` refusal C3's text test reaches is put back as its old
     `print(f"ERROR: ...", file=sys.stderr)` + exit — that test must fail.
 (d) `_cmd_run_list`'s migrated refusal passes `json_output=False` — report what goes
     red; if nothing does, say so plainly (a probe, not a colour).
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain` empty; `git log --oneline -n 7`;
 `git worktree list` (primary plus the three `remedy/job-*`); the push's real outcome;
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 2 of feature F283, round 9, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 9, then round 10 — `_cmd_do_order`'s result document takes the envelope,
then the `grouped` and `test_cmds` groups. State the open-findings count, 22 after this
round, and the operator-questions count, 2.
