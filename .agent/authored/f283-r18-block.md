STEP F283 R18 — T002's success half, second batch: eight modules answer success in the envelope (D10)

GOAL
Book round 17's PASS, register and repair R-1031, resolve R-1030 on the record, then convert
every raw `--json` success document of eight command modules to the envelope under DECISION
F283 D10.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/` and `tests/` is yours, written to the SPEC in
each commit. DECISION F283 D10 (search `.agent/decisions.md` for `DECISION F283 D10`; never
read that file whole) IS the SPEC for C4 and C5, and DECISION F283 D8 governs `runtime_cmd.py`,
whose `error_class` stays in every payload that carries it.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r18-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r18-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file
      the reviewer put there before C1, which is read-only to you.
      `python3 .remedy-wt/f283-r18-scratch/run_sel.py . <label>` runs selection A under
      `-n auto` and selection B (the five `tests/runtimes/` suites) SERIALLY, and prints each
      exit code, summary and bad node ids; about nine minutes.
      `python3 .remedy-wt/f283-r17-scratch/raw_sites.py .` prints the raw-document sites per
      module by D10's rule; add `-v` for one row per site.
      `.remedy-wt/f283-r18-scratch/dry_a_bad.txt` lists the tests the reviewer's mechanical dry
      conversion of these eight modules turned red, one node id per line.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`; a `python3 -`
heredoc containing a brace next to a quote is refused too, so put such code in a scratch file.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a
worktree. NEVER USE `git stash` IN ANY FORM, and never check out another commit in the primary
checkout: take each reading after the commit it belongs to. Draft and commit one commit's
change at a time. No test may launch a real browser, opener or blocking server: mock them.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `9f36956f`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r18-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r18-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 6 | 5779 | d9a74b3db455c37e0b4e75968f9067fcb14e5dc9cfbdca52c9c39204e1564f27 |
| plan.md | 35 | 1510 | cd1c8e349ce5525a1c038fab3f56ed50a9bbb4e3ed0ff03a9519d367faa15c41 |

`ledger.md` is an APPEND beginning with the single newline that separates records; it carries
the round 17 `Gate:` entry, R-1031's registration and R-1030's `Done:` paragraph. `plan.md` is
a REWRITE. Never retype or edit a payload.

THE EIGHT MODULES, all under `apps/cli/commands/`, in two halves:
  HALF A: `runtime_cmd.py`, `do_cmd.py`, `real_test_execution_cmd.py`, `event.py`
  HALF B: `memory.py`, `patch.py`, `stats_ledger_cmd.py`, `brain.py`

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f283-r18-block.md` := this block; `.agent/authored/f283-r18-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R18 C1: copy round 18 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md
  Subject: `F283 R18 C2: book round 17's PASS, register R-1031, resolve R-1030`

C3 — R-1031, tests only. For each of `job_stop_cmd.py`, `change.py`, `bench_cmd.py`,
  `blocker.py`, `decision.py`, `roadmap_cmd.py` and `snapshot_cmds.py`, one test through the
  CLI dispatcher (in the test file nearest that module, from selection A) asserts
  `schema_version` 1, `ok` true and one key the old document carried, on a `--json` output
  round 17 converted. Then append to `.agent/live_review.md` one line: `Landed: R-1031 —
  <one line: what changed, this commit>`, and nothing else.
  Subject: `F283 R18 C3: pin the envelope of seven round-17 modules (R-1031)`

C4 — HALF A converted by D10. `run list --json` prints a bare list today and a prose line
  when there are no runs: under `--json` it answers `emit_ok(runs=<the list>)` in both cases,
  the prose line staying in the text branch, and every reader of that output in the
  repository changes in this commit (D10 (4)). A runtime document that carries `ok` true drops
  it; `error_class` stays wherever a payload carries it. The ratchet dict loses these modules.
  For each of the four modules at least one test asserts `schema_version` 1 and `ok` on a
  converted output, and one test asserts `run list --json` with no runs answers
  `runs` empty. Repair every test that pinned an old exact shape, keeping what it asserts;
  the reviewer's dry run lists them in `dry_a_bad.txt` (the two `run list` tests of
  `tests/cli/test_cli_ux.py` and `tests/cli/test_real_test_execution_cli.py::test_snapshot_create_show`
  belong to this half). Split this commit by module if it would pass 500 insertions.
  Subject: `F283 R18 C4: runtime, do, test and event answer --json success in the envelope (D10)`

C5 — HALF B converted by D10, with the same per-module test obligation. The remaining
  entries of `dry_a_bad.txt` belong to this half: sixteen in `tests/test_brain_smoke.py`,
  one each in `tests/cli/test_patch_cmd.py`, `tests/test_brain_detail.py`,
  `tests/test_context_coverage.py` and `tests/test_project_brain.py`. The ratchet dict must
  then name only `job.py`, `mission_cmd.py`, `self_cmd.py`, `project.py`, `config_cmd.py` and
  `worker.py`, plus any text-branch survivor of D10 (5) in the eight, named with its reason.
  Split this commit by module if it would pass 500 insertions.
  Subject: `F283 R18 C5: memory, patch, stats and brain answer --json success in the envelope (D10)`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R18 C6: rewrite handoff for round 18`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the three `.agent/authored/f283-r18-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`, the eight modules above,
   and test files listed in `.remedy-wt/f283-r18-scratch/selection.txt` or
   `selection_serial.txt`. Report the set you measure. Nothing under `packages/`, nothing
   else under `apps/`, nothing under `docs/`, no `README.md`, no `scripts/`, and none of
   `.agent/decisions.md`, `.agent/candidates.md`, `.agent/context.md`,
   `.agent/operator_questions.md`, `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves both selections at zero failed and zero errors: run
   `run_sel.py` after C3, C4 and C5 and report all six readings. A node of
   `tests/runtimes/test_supervisor_portability.py` that fails once serially is re-run alone
   three times and all three readings are reported; it counts as red unless all three pass.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C6 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r18-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r18-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `9f36956f` (529803) plus
     ledger.md; the reviewer composed 535582.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R17 — ` 1, `^- R-1031 — ` 1 and
     `^Done: R-1030 — ` 1. Open set by distinct id via `open_finding_ids` from
     `scripts/rotate_live_review.py` at `9f36956f` and at C2: the reviewer measured 25 and
     25, ADDED `R-1031`, REMOVED `R-1030`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3, C4 and C5 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. Report
 `raw_sites.py .`'s TOTAL line after C4 and C5 (the reviewer read `TOTAL 87 modules 14` at
 `9f36956f`) and every module row left after C5. At C3 report the `Landed: R-1031` line.
 List every token the round's `fail(` and `emit_error(` calls introduce or reuse, each with
 its `git grep -c` count over `apps/` at `9f36956f`. `git diff --name-only 9f36956f <C5> --
 packages/` must print nothing.

G4 THE SELECTIONS — `.remedy-wt/f283-r18-scratch/selection.txt` (304 paths, `-n auto`) and
 `selection_serial.txt` (5 paths, serial). The reviewer read at `9f36956f`: A `11340 passed,
 13 skipped` and B `204 passed`, both exit 0. After C3, C4 and C5: zero failed and zero
 errors in each; passed counts may only rise. Then `python3 -m ruff check` over every `.py`
 path the round touched, and `python3 -m apps.cli.main integrity check --json`, which now
 answers the envelope, all five checks `pass`. `python3 -m pytest
 tests/cli/test_golden_path.py -q` once after C5. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C5, never committed. Its
 first run builds the UI and reddens UI suites once: run the control TWICE and report both,
 judging each mutation against the second. The files: every test file C3, C4 and C5 changed —
 list them — plus `tests/cli/test_json_envelope.py`. Then each mutation alone, reverted
 before the next, reporting the summary line, the exit code and the failing test names:
 (a) `roadmap next --json` prints its raw document again — C3's `roadmap_cmd.py` test must
     fail, beside the ratchet.
 (b) `run list --json` with no runs prints the prose line again — C4's empty-runs test must
     fail.
 (c) `run list --json` writes the bare list again — a C4 `run list` test must fail.
 (d) one converted success document of `runtime_cmd.py` prints raw again — C4's
     `runtime_cmd.py` envelope test must fail.
 (e) `brain node --json` prints its raw document again — a `tests/test_brain_smoke.py` test
     must fail.
 (f) one converted `memory.py` success document drops `schema_version` by printing
     `json.dumps` of the envelope minus that key — C5's `memory.py` envelope test must fail.
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
reads SESSION 4 of feature F283, round 18, and says in one sentence how much context you had
left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 18, then T002's last success batch as `.agent/plan.md` lists it. State the
open-findings count, 25 after this round with R-1031 landed and awaiting review, and the
operator-questions count, 0.
