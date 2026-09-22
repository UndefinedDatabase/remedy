STEP F283 R20 — T002's taxonomy half: the exit codes documented, declared in the catalog and asserted (D12)

GOAL
Book round 19's PASS, record DECISION F283 D12, give every exit code one written meaning in
`apps/cli/exit_codes.py`, declare every command's codes in the catalog with a test that reads
each handler, write the guide `docs/guides/exit-codes.md` asserted from the catalog, and make
`job resume --checkpoint` refuse where it did not resume.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/`, `tests/` and `docs/` is yours, written to the
SPEC in each commit. DECISION F283 D12, in this round's decisions payload, IS the SPEC for C3,
C4 and C5; read it whole before C3. Never read `.agent/decisions.md` whole.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r20-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r20-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file
      the reviewer put there before C1, which is read-only to you.
      `python3 .remedy-wt/f283-r20-scratch/run_sel.py . <label>` runs selection A under
      `-n auto` and prints its exit code, summary and bad node ids; about four minutes. It
      skips a listed path that does not exist yet, so `tests/cli/test_exit_codes.py` joins
      the selection once C3 creates it.
      `python3 .remedy-wt/f283-r20-scratch/reach_proto.py .` is the reviewer's prototype of
      D12 (4)'s static reading; its output at `98a85b67` is `reach_expected.txt` beside it,
      whose `DECLARE` block lists every command whose handler reaches a code above the floor,
      with those codes. You may adapt its method for the test; the test is yours.
      `python3 .remedy-wt/f283-r20-scratch/exit_scan.py .` counts the exit sites under
      `apps/cli/` by code.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion,
`awk`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`; put multi-step code in a scratch file. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. NEVER USE
`git stash` IN ANY FORM — round 19's worker did and had to declare it — and never check out
another commit in the primary checkout: take each reading after the commit it belongs to.
Draft and commit one commit's change at a time. No test may launch a real browser, opener,
provider or blocking server: mock them.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `98a85b67`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r20-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r20-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 3378 | 4ae959c58b8e721f3f572c9fa56083274faca1690468d69ecc4d6f0b00760df5 |
| decisions.md | 66 | 5350 | e6c67a303065ba858aa78a66f73e14d382040264556e2170ddb1b9527522cdba |
| plan.md | 33 | 1401 | 45435f942017f8f82f2f0debc595545ed73471945915a203de1a30ba36ecaabd |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 19 `Gate:` entry; decisions carries DECISION
F283 D12. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r20-block.md` := this block; `.agent/authored/f283-r20-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R20 C1: copy round 20 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R20 C2: book round 19's PASS, record D12`

C3 — THE TAXONOMY IN CODE, D12 (1) to (4).
  (a) NEW `apps/cli/exit_codes.py`, importing nothing from `apps.cli`: the CLI table and the
      runtime table of D12 (1) and (2), each code with its name and a one-sentence meaning
      taken from D12; the floor `(0, 1, 2)` of D12 (4); and one function that returns the
      table for a group id (the runtime table for `runtime`, the CLI table otherwise). Public
      names carry a domain word (AGENTS.md, Code Discoverability); the module docstring
      states D12 (5) as a deliberate absence.
  (b) `apps/cli/command_catalog.py`: `CommandEntry` gains `exit_codes: tuple[int, ...]`
      defaulting to that floor, with a one-line WHY comment above it. Exactly the commands in
      `reach_expected.txt`'s `DECLARE` block declare `exit_codes`, each as the floor plus the
      listed codes, ascending. No other entry changes and no entry is added or removed.
  (c) NEW `tests/cli/test_exit_codes.py`: every entry's `exit_codes` contains the floor and
      only codes its group's table names; per command, the codes above the floor its handler
      reaches by D12 (4)'s static reading EQUAL the codes above the floor it declares; an
      unresolved site is named in one constant with the codes a reader verified and its
      reason — the reviewer expects exactly `ci run`'s `sys.exit(ci_exit_code(results))`,
      codes 0 and 1 by `ci_exit_code` in `packages/orchestration/ci_run.py` — and an unnamed
      unresolved site fails the test with its location. Report what you measure.
  Subject: `F283 R20 C3: declare every command's exit codes in the catalog and assert them (D12)`

C4 — THE GUIDE, D12 (3). NEW `docs/guides/exit-codes.md`, written for an operator in plain,
  complete sentences (docs/agents/self_drive_protocol.md, amend0921 rule 3): what an exit code
  is for, then three tables under their own headings — the CLI codes (`| Code | Name | Meaning
  |`), the runtime group's codes, and one row per command that declares a code above the floor
  (`| Command | Exit codes |`, the command spelled `remedy <group> <subcommand>`) — and one
  sentence stating D12 (5). `docs/README.md` gains one quick-find row and one row under
  `## Guides (`docs/guides/`)`, in the alphabetical place of each table. `test_exit_codes.py`
  gains a test that parses the three tables and asserts each EQUAL to its source: the two
  module tables, and the catalog's declarations above the floor.
  Subject: `F283 R20 C4: document the exit codes in docs/guides/ and assert the guide from the catalog (D12)`

C5 — THE RESUME REFUSALS, D12 (6), in `_cmd_resume` of `apps/cli/commands/job.py`: the
  `from_apply` branch whose result did not resume, and the unimplemented-mode branch at the
  function's end, each answer `fail("resume_blocked", <message>, json_output=json_output,
  ...)` with `resumed` false, `blocked_reason` and `worktrees`; the `from_apply` refusal
  carries every key `export_resume_result_json` returns. The worktree bookkeeping before each
  refusal stays as it is; a resume whose tests came out red stays exit 0. In
  `tests/orchestration/test_worktree_resume_cli.py`, one test per branch, on its existing
  `interrupted` fixture: a stubbed continuation returning `resumed=False` with a
  `blocked_reason`, and a checkpoint made safe to resume under a mode other than `from_apply`
  by monkeypatching `event_replay`; each asserts the envelope's `ok` false, `error`
  `resume_blocked`, the `blocked_reason`, and `SystemExit` code 1.
  Subject: `F283 R20 C5: job resume refuses where it did not resume (D12)`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R20 C6: rewrite handoff for round 20`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the `.agent/authored/f283-r20-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/exit_codes.py`, `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
   `tests/cli/test_exit_codes.py`, `tests/orchestration/test_worktree_resume_cli.py`,
   `docs/guides/exit-codes.md`, `docs/README.md`, and a test file listed in
   `.remedy-wt/f283-r20-scratch/selection.txt` whose guard a commit of this round turns red.
   Report the set you measure. Nothing under `packages/`, nothing else under `apps/` or
   `docs/`, no root `README.md`, no `scripts/`, and none of `.agent/candidates.md`,
   `.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves selection A at zero failed and zero errors: run
   `run_sel.py` after C3, C4 and C5 and report all three readings.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).
8. No existing exit code changes value anywhere (D12 (5)); C5 changes the OUTCOME of two
   branches that answered success, not the value of any existing refusal.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r20-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r20-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, each pre-file read at `98a85b67`:
     `.agent/live_review.md` (540287) plus ledger.md, the reviewer composed 543665;
     `.agent/decisions.md` (1829140) plus decisions.md, 1834490.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R19 — ` 1. Open set by distinct id
     via `open_finding_ids` from `scripts/rotate_live_review.py` at `98a85b67` and at C2: the
     reviewer measured 24 and 24, ADDED and REMOVED both empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3, C4 and C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C5, report
 `reach_proto.py .`'s `DECLARE` block beside `reach_expected.txt`'s, and the catalog's own
 list of entries whose `exit_codes` differ from the floor, read by importing `CATALOG`; the
 three must name the same commands with the same codes. Report `exit_scan.py .`'s `CODE`
 lines at C5. `git diff --name-only 98a85b67 <C5> -- packages/` must print nothing.

G4 THE SELECTION — `.remedy-wt/f283-r20-scratch/selection.txt`, under `-n auto`. The
 reviewer read at `98a85b67`: `11460 passed, 13 skipped`, exit 0, over 307 paths. After C3,
 C4 and C5: zero failed and zero errors; the passed count may only rise. Then
 `python3 -m ruff check` over every `.py` path the round touched, and `python3 -m
 apps.cli.main integrity check --json`, all five checks `pass`. `python3 -m pytest
 tests/cli/test_golden_path.py -q` once after C5. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed. The
 files: `tests/cli/test_exit_codes.py`, `tests/orchestration/test_worktree_resume_cli.py`
 and `tests/cli/test_command_catalog.py`. Run the control first and report it; it must exit
 0. Then each mutation alone, reverted before the next, reporting the summary line, the exit
 code and the failing test names:
 (a) `job.stop`'s entry drops 3 from its `exit_codes` — the per-command equality must fail
     naming `job.stop`.
 (b) `job.list`'s entry declares 3 it does not reach — the same test must fail naming
     `job.list`.
 (c) in `init_cmd.py`, the `not_a_git_repo` refusal's `exit_code=4` becomes 3 — the
     per-command equality must fail naming `init.run`.
 (d) the guide's CLI-table row for code 3 loses its last word — the guide test must fail.
 (e) the `from_apply` refusal of C5 answers `emit_ok(...)` again — C5's first test fails.
 (f) the unimplemented-mode refusal of C5 answers `emit_ok(...)` again — C5's second test
     fails.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 8`;
 `git worktree list` (the primary checkout alone); `git stash list`'s first line unchanged
 from its reading before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the
 handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the item-status table with one row per C-item, gate and mutation, the deviations, and
the next action. Your Session section reads SESSION 5 of feature F283, round 20, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 20, then T002's sweep as `.agent/plan.md` lists it. State the open-findings
count, 24 after this round, and the operator-questions count, 0.
