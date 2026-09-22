STEP F283 R19 — T002's success half, last batch: six modules answer success in the envelope (D10, D11)

GOAL
Book round 18's PASS, resolve R-1031 on the record, record DECISION F283 D11, pin `patch
revert`'s failure token, then convert every raw `--json` success document of the last six
command modules to the envelope, so the ratchet holds only the text-branch survivors.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit. DECISION F283 D10 (search `.agent/decisions.md` for `DECISION F283 D10`; never
read that file whole) and DECISION F283 D11, in this round's decisions payload, ARE the SPEC
for C4 and C5.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r19-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r19-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file
      the reviewer put there before C1, which is read-only to you.
      `python3 .remedy-wt/f283-r19-scratch/run_sel.py . <label>` runs selection A under
      `-n auto` and prints its exit code, summary and bad node ids; about four minutes.
      `python3 .remedy-wt/f283-r17-scratch/raw_sites.py .` prints the raw-document sites per
      module by D10's rule; add `-v` for one row per site.
      `.remedy-wt/f283-r19-scratch/dry_bad.txt` lists the tests the reviewer's mechanical dry
      conversion of these six modules turned red, one node id per line.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion,
`awk`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`; a
`python3 -` heredoc containing a brace next to a quote is refused too, so put such code in a
scratch file. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use
`git -C <dir>` for a worktree. NEVER USE `git stash` IN ANY FORM, and never check out another
commit in the primary checkout: take each reading after the commit it belongs to. Draft and
commit one commit's change at a time. No test may launch a real browser, opener or blocking
server: mock them.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `5d1510ca`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r19-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r19-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 4374 | 0757d61e8198c97248bb3d3b782bf3e7409d1c017a215e71dfff240043bbf546 |
| decisions.md | 31 | 2213 | 0c7ddf503f792f96ee5cc49bf882dd201650edf5cfd08c0aa1db8dea42f82637 |
| plan.md | 32 | 1331 | 6d1796f9842b12f8b01b8a11477eaed1218e06aa0e51274021f018dc5c34c5f9 |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 18 `Gate:` entry and R-1031's `Done:`
paragraph; decisions carries DECISION F283 D11. `plan.md` is a REWRITE. Never retype or edit a
payload.

THE SIX MODULES, all under `apps/cli/commands/`, in two halves:
  HALF A: `job.py`, `mission_cmd.py`
  HALF B: `self_cmd.py`, `project.py`, `config_cmd.py`, `worker.py`

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r19-block.md` := this block; `.agent/authored/f283-r19-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R19 C1: copy round 19 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R19 C2: book round 18's PASS, resolve R-1031, record D11`

C3 — THE PIN, tests only. In `tests/cli/test_patch_cmd.py`, `patch revert --json` on a revert
  the revert path refuses answers one failure envelope whose `error` is that refusal's
  `block_reason` (D11 (2)), with `ok` false and the revert's exit code.
  Subject: `F283 R19 C3: pin patch revert's failure token (D11)`

C4 — HALF A converted by D10: every raw `--json` document in `job.py` and `mission_cmd.py`
  is written through the envelope, every old top-level key kept. The ratchet dict loses these
  two modules. For each of the two, at least one test asserts `schema_version` 1 and `ok` on a
  converted output. Repair every test that pinned an old exact shape, keeping what it asserts;
  the reviewer's dry run lists them in `dry_bad.txt`, and the entries in
  `tests/cli/test_job_show.py`, `tests/cli/test_job_report.py`,
  `tests/cli/test_job_budget_set.py` and `tests/orchestration/test_resume_cli.py` belong to this
  half. Split this commit by module if it would pass 500 insertions.
  Subject: `F283 R19 C4: job and mission answer --json success in the envelope (D10)`

C5 — HALF B converted by D10, with the same per-module test obligation for each of the four.
  `config list --json` writes a bare list today: it answers `emit_ok(entries=<the list>)`,
  and its readers change in this commit (D10 (4)), `settings list --json` included through
  the alias. The remaining entries of `dry_bad.txt` belong to this half. The raw document
  `project attach` prints in its TEXT branch stays (D10 (5)). The ratchet dict must then name
  only text-branch survivors, each with its reason in the constant's comment; the reviewer
  expects exactly one, `project.py`'s `project attach` text branch — report what you measure.
  Split this commit by module if it would pass 500 insertions.
  Subject: `F283 R19 C5: self, project, config and worker answer --json success in the envelope (D10)`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R19 C6: rewrite handoff for round 19`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the four `.agent/authored/f283-r19-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`, the
   six modules above, and test files listed in `.remedy-wt/f283-r19-scratch/selection.txt`.
   Report the set you measure. Nothing under `packages/`, nothing else under `apps/`, nothing
   under `docs/`, no `README.md`, no `scripts/`, and none of `.agent/candidates.md`,
   `.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves selection A at zero failed and zero errors: run
   `run_sel.py` after C3, C4 and C5 and report all three readings.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r19-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r19-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, each pre-file read at `5d1510ca`:
     `.agent/live_review.md` (535913) plus ledger.md, the reviewer composed 540287;
     `.agent/decisions.md` (1826927) plus decisions.md, 1829140.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R18 — ` 1 and `^Done: R-1031 — ` 1.
     Open set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at
     `5d1510ca` and at C2: the reviewer measured 25 and 24, ADDED empty, REMOVED `R-1031`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3, C4 and C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. Report
 `raw_sites.py .`'s TOTAL line after C4 and C5 (the reviewer read `TOTAL 51 modules 6` at
 `5d1510ca`) and every site left after C5 with `-v`. List every token the round's `fail(` and
 `emit_error(` calls introduce or reuse, each with its `git grep -c` count over `apps/` at
 `5d1510ca`. `git diff --name-only 5d1510ca <C5> -- packages/` must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r19-scratch/selection.txt` (307 paths, `-n auto`).
 The reviewer read at `5d1510ca`: `11459 passed, 13 skipped`, exit 0. After C3, C4 and C5:
 zero failed and zero errors; the passed count may only rise. Then `python3 -m ruff check`
 over every `.py` path the round touched, and `python3 -m apps.cli.main integrity check
 --json`, all five checks `pass`. `python3 -m pytest tests/cli/test_golden_path.py -q` once
 after C5. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed. Its
 first run builds the UI and reddens UI suites once: run the control TWICE and report both,
 judging each mutation against the second. The files: every test file C3, C4 and C5 changed —
 list them — plus `tests/cli/test_json_envelope.py`. Then each mutation alone, reverted
 before the next, reporting the summary line, the exit code and the failing test names:
 (a) `patch revert`'s failure token is fixed to `revert_failed` — C3's pin must fail.
 (b) `config list --json` writes the bare list again — a C5 `config` test must fail.
 (c) one converted `job.py` success document prints raw again — C4's `job.py` envelope test
     must fail.
 (d) one converted `mission_cmd.py` success document prints raw again — C4's
     `mission_cmd.py` envelope test must fail.
 (e) one converted `self_cmd.py` success document prints raw again — C5's `self_cmd.py`
     envelope test must fail.
 (f) one converted `worker.py` success document prints raw again — C5's `worker.py`
     envelope test must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`;
 `git worktree list` (the primary checkout alone); `git stash list`'s first line unchanged
 from its reading before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the
 handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table — with one row per per-module test obligation,
naming the test that meets it — the deviations, and the next action. Your Session section
reads SESSION 4 of feature F283, round 19, and says in one sentence how much context you had
left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 19, then T002's last slice as `.agent/plan.md` lists it. State the
open-findings count, 24 after this round, and the operator-questions count, 0.
