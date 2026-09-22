STEP F283 R8 — the single pass answers in the envelope; R-1019, R-1025; the `do` group

GOAL
Book round 7's PASS, the `Done:` lines of R-1023 and R-1024, R-1025's registration and
DECISION F283 D3; then land D3, repair R-1025 and R-1019, close round 7's `patch list`
coverage gap, and move the `do_cmd` group's refusal pairs onto `fail()`.

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
repo-wide, and AN EXISTING SPELLING WINS: before you use ANY token, search `fail("` over
`apps/cli/` and read the tokens in use; where one names the same condition, use it. A pair
whose `print` does NOT begin with `Error: `, whose message is a constant rather than a
literal (e.g. `DO_PUSH_KEY_WITHOUT_COMMIT`), or with more than one `print` before its exit,
is NOT migrated — it stays and the module's ratchet counts it.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r8-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r8-scratch/`   YOURS for logs, captures and scripts, EXCEPT the
      reviewer's `selection.txt` and `base.txt`/`wide.txt`, which are read-only to you.
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
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `a8b8d547`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r8-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r8-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 45 | 3407 | e16d673f9a653b1371ccaee1bbc8517a48da0f19677318eec6d0a4a6def537ef |
| ledger.md | 8 | 7231 | 2f2391b0c38d28837ccc4fa70b9c197b3a6ac0f1a0dbdbf84a34cee98e7f8bff |
| plan.md | 38 | 1724 | c461c06512318971576107b30fd56a2272f8af368413e5850ab28c5ef9917f4e |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 7 `Gate:` entry, the `Done:` lines of
R-1023 and R-1024 and R-1025's registration; decisions carries DECISION F283 D3.
`plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C9, in this order.

C1 — `.agent/authored/f283-r8-block.md` := this block; `.agent/authored/f283-r8-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R8 C1: copy round 8 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R8 C2: book round 7's PASS, resolve R-1023 and R-1024, register R-1025`

C3 — R-1025. SPEC, `tests/cli/test_product_spine.py`,
  `TestJobFacadeNoAgent::test_job_status_invalid_id_safe` ONLY: keep its invocation;
  assert a non-zero exit, an EMPTY stderr, stdout parsing as ONE JSON object with `ok`
  false, `error` `invalid_job_id` and a `message` containing `not-a-uuid`, and no
  `Traceback` in either stream. Its docstring says the command answers in the envelope
  since F283 round 3 and names R-1025. Nothing else in that file changes.
  Subject: `F283 R8 C3: the product-spine test asserts the envelope job show answers in`

C4 — DECISION F283 D3 part (a), the single pass. Read D3 in the payload first.
  SPEC, `apps/cli/commands/job.py`, `_cmd_run_next_task_local` only: under `json_output`
  it writes exactly one envelope to stdout and no prose there, with the keys and the
  three outcomes D3 part (a) names — `emit_ok(...)` on a verified run,
  `fail("verification_failed", ...)` at exit 1 on a failed one, `emit_ok(job_id=...,
  outcome="no_pending_tasks", log=...)` when nothing is pending. Import `emit_ok` from
  `apps.cli.json_envelope`. With the flag off, every byte and exit code is unchanged.
  SPEC, tests, in `tests/test_run_log_cli.py` (it already drives this function with a
  stubbed builder): one test per outcome under `json_output=True`, each parsing the WHOLE
  of stdout as one object and asserting `ok`, the outcome's distinguishing keys and the
  exit code; and the existing text-mode tests unchanged.
  Subject: `F283 R8 C4: the single-pass run answers in the envelope under --json`

C5 — DECISION F283 D3 part (b), the blocked resume.
  SPEC, `apps/cli/commands/job.py`, `_cmd_resume` only: both hand-rolled blocked branches
  become `fail("resume_blocked", <message>, json_output=json_output, resumed=False,
  blocked_reason=<same>, worktrees=<same list>)` at exit 1, the text message carrying one
  indented continuation line per blocked worktree as D3 says.
  SPEC, tests: `tests/orchestration/test_worktree_resume_cli.py` and
  `tests/orchestration/test_worktree_lifecycle.py` keep their `blocked_reason` assertions
  passing unchanged; add to each one assertion that the object also carries `ok` false and
  `error` `resume_blocked`.
  Subject: `F283 R8 C5: a blocked resume refuses through fail() with its keys kept`

C6 — round 7's coverage gap. SPEC, `tests/cli/test_patch_cmd.py`: `_cmd_list_patch_intents`
  with an invalid list option under `json_output=True` exits 1 with an empty stderr and an
  envelope `invalid_list_option`. No product change.
  Subject: `F283 R8 C6: patch list's list-option refusal gets its envelope test`

C7 — R-1019. SPEC, `apps/cli/commands/worker.py::_cmd_worker_unload`: the
  `missing_argument` refusal for neither `--model` nor `--all` moves ABOVE the
  `shutil.which("ollama")` probe, same token, message and exit code; the unavailable
  branch is otherwise unchanged. SPEC, `tests/cli/test_worker.py`: one test with
  `shutil.which` patched to return `None` and one with it patched to return a path, each
  asserting that neither flag under `json_output=True` exits 1 with an envelope
  `missing_argument` — PIN THE PROBE in both, never read the real PATH (finding R-1018).
  Subject: `F283 R8 C7: worker unload refuses a missing target before it probes the provider`

C8 — the `do` group: every pair the rule reaches in `apps/cli/commands/do_cmd.py`. SPEC,
  `tests/cli/test_job_refusal_envelope.py`: a ratchet class, as rounds 6 and 7 wrote for
  `decision.py`, `brain.py` and `patch.py`, counting what stayed. One envelope test in the
  `do` test file you judge nearest (name it) for a `--json` refusal you can reach.
  Subject: `F283 R8 C8: do refusals answer through fail()`

C9 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R8 C9: rewrite handoff for round 8`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the four `.agent/authored/f283-r8-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/handoff.md`, `apps/cli/commands/job.py`, `apps/cli/commands/worker.py`,
   `apps/cli/commands/do_cmd.py`, `tests/cli/test_product_spine.py`,
   `tests/test_run_log_cli.py`, `tests/orchestration/test_worktree_resume_cli.py`,
   `tests/orchestration/test_worktree_lifecycle.py`, `tests/cli/test_patch_cmd.py`,
   `tests/cli/test_worker.py`, `tests/cli/test_job_refusal_envelope.py`, and the ONE `do`
   test file C8 names. A test a change breaks is repaired in that same commit ONLY inside
   this set, and only where it asserted the OLD `--json` shape (prose on stderr, or a raw
   object with no `ok`); a text-mode assertion that breaks means the change altered bytes
   — fix the change. Otherwise STOP. Report the set you measure. Nothing under
   `packages/` or `docs/`, no `README.md` or `apps/cli/json_envelope.py`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
   `.agent/prose_slips.md`.
4. Every commit leaves the G4 selection no redder than its base: at C2 the one red node
   is R-1025's test, and from C3 on there are none.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C9 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r8-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r8-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `a8b8d547` (479875 bytes)
     plus ledger.md; the reviewer composed 487106. `.agent/decisions.md` (1793909) plus
     decisions.md; the reviewer composed 1797316.
 (b) Line-anchored on the committed ledger: `^Done: R-1023 — ` 1, `^Done: R-1024 — ` 1,
     `^- R-1025 — ` 1, `^Done: R-1025 — ` 0. Open set by distinct id via
     `open_finding_ids` from `scripts/rotate_live_review.py` at `a8b8d547` and at C2: the
     reviewer measured 25 and 24, ADDED exactly `R-1025`, REMOVED exactly `R-1023` and
     `R-1024`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for every commit C3 to C8 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C8 run
 `python3 .remedy-wt/f283-r6-scratch/pairs.py job.py do_cmd.py` and report its summary
 lines; the reviewer read at `a8b8d547` `job.py exits 4 mechanical 0 flagged 0
 unflagged 0` and `do_cmd.py exits 19 mechanical 18 flagged 15 unflagged 3`. List every
 token C4, C5, C7 and C8 use, with its line and `new` or `reused`, and for each `new` one
 the search you ran. Report `git diff --name-only a8b8d547 <C8> -- packages/`, which must
 print nothing.

G4 THE SELECTION — WIDENED THIS ROUND BY R-1025. `.remedy-wt/f283-r8-scratch/selection.txt`
 is one line of 76 space-separated paths: every test file that pairs `--json` with a
 stderr or `Error: ` assertion, found by search, plus the files nearest this round's
 modules, plus `tests/docs/`. `tests/runtimes/test_supervisor_portability.py` is left out
 on purpose: under `-n auto` it reports process-teardown noise that a serial run of it at
 `a8b8d547` reads as `99 passed`, and nothing on this branch touches what it tests. Run,
 in the primary checkout at C8, `python3 -m pytest -q -p no:cacheprovider -n auto` over
 exactly those paths (read them from the file in a script) and report the summary line
 and exit code. The reviewer read `1 failed, 3207 passed` at `a8b8d547`, the one failure
 being R-1025's test. At C8: zero failed, zero errors, zero xfailed; the passed count may
 only rise. If C8's `do` test file is not in the list, add it and say so. Then
 `python3 -m ruff check` over every `.py` path the round touched, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass`. DO NOT run
 the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C8, never committed.
 Run every test file C3 to C8 touched UNMUTATED first and report it (exit 0). Then each
 mutation alone, reverted before the next, reporting the summary line, the exit code and
 the failing test names:
 (a) the verified-run branch of C4 prints its prose line to stdout before the envelope
     even under the flag — C4's verified-run test must fail.
 (b) C4's `verification_failed` token becomes `verify_failed` — C4's failed-run test
     must fail.
 (c) C5's `resume_blocked` token becomes `resume_refused` — both C5 assertions must fail.
 (d) C7's `missing_argument` check is moved back BELOW the probe — C7's `None`-probe
     test must fail and its path-probe test must pass.
 (e) one migrated `fail()` in `do_cmd.py` is put back as its old print-then-exit pair —
     C8's ratchet must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C9: `git status --porcelain` empty; `git log --oneline -n 11`;
 `git worktree list` (primary plus the three `remedy/job-*`); the push's real outcome;
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 2 of feature F283, round 8, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 8, then round 9 — the `Done:` lines of R-1019 and R-1025 booked in its
first commit, and the `project` group with a ruling on its uppercase `ERROR:` prefix.
State the open-findings count, 24 after this round, and the operator-questions count, 2.
