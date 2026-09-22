STEP F283 R17 — T002's success half, first batch: twenty modules answer success in the envelope (D10)

GOAL
Book round 16's PASS, register and repair R-1030, pin what round 16's review found unpinned,
record DECISION F283 D10 and land its ratchet, then convert every raw `--json` success document
of twenty smaller command modules to the envelope.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. The reviewer authors only the
RECORD payloads; every change under `apps/`, `packages/` and `tests/` is yours, written to
the SPEC in each commit. DECISION F283 D10, in this round's decisions payload, IS the SPEC for
C5 and C6: read it before C4. DECISION F283 D5 (search `.agent/decisions.md` for `DECISION
F283 D5`; never read that file whole) is the precedent D10 generalises.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r17-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r17-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file
      the reviewer put there before C1, which is read-only to you.
      `python3 .remedy-wt/f283-r17-scratch/run_sel.py . <label>` runs selection A under
      `-n auto` and prints its exit code, summary and bad node ids; about four minutes.
      `python3 .remedy-wt/f283-r17-scratch/raw_sites.py .` prints the raw-document sites per
      module by D10's rule; add `-v` for one row per site.

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
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `488fd05a`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r17-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r17-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 5061 | 10bbddc2c5f146a0ae437cafadae1c63fc39ba626ec0a9af49e08a6d866092d0 |
| decisions.md | 40 | 3155 | 972f7e8521e5dd657312079042c3250dab52b78851191e68e99f4213e7fa2c1a |
| plan.md | 37 | 1636 | 9b0cda9c028c12389e30ebe0b6cd0de4c14c7ab4087dcaa94b11afa230c5372f |

`ledger.md` and `decisions.md` are APPENDS, each beginning with the single newline that
separates records: the ledger carries the round 16 `Gate:` entry and R-1030's registration;
decisions carries DECISION F283 D10. `plan.md` is a REWRITE. Never retype or edit a payload.

THE TWENTY MODULES, all under `apps/cli/commands/`, in two halves:
  HALF A: `job_stop_cmd.py`, `test_cmds.py`, `change.py`, `bench_cmd.py`, `blocker.py`,
          `contract_cmd.py`, `data_cmd.py`, `decision.py`, `roadmap_cmd.py`, `snapshot_cmds.py`
  HALF B: `teacher_cmd.py`, `dev.py`, `failure_stats_cmd.py`, `file.py`, `init_cmd.py`,
          `integrity_cmd.py`, `job_context_cmd.py`, `status_cmd.py`, `study_cmd.py`,
          `worker_facade_cmd.py`

BUNDLE — commits C1 to C7, in this order.

C1 — `.agent/authored/f283-r17-block.md` := this block; `.agent/authored/f283-r17-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R17 C1: copy round 17 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/decisions.md` += decisions.md ·
  `.agent/plan.md` := plan.md
  Subject: `F283 R17 C2: book round 16's PASS, register R-1030, record D10`

C3 — R-1030 AND THE THREE PINS. `packages/orchestration/ui_server.py::start_ui_server`: the
  comment above its function-scoped `apps.cli.json_envelope` import names
  `_command_is_ui_exposed` in this same file as the precedent and makes no claim about
  `apps/cli/json_envelope.py`. Tests: `project attach-job --json` on a job already attached
  answers `added` false (`tests/cli/test_project_current.py`); `ui stop --json` whose
  `os.kill` raises answers a `failed` entry carrying `pid`, `job_id` and `error`, and
  `start_ui_server` under `--json` answers `job_not_found` for a 404 job and `invalid_job_id`
  for a 400 one (`tests/ui_server/test_live_state.py`). Then append to `.agent/live_review.md`
  one line: `Landed: R-1030 — <one line: what changed, this commit>`, and nothing else.
  Subject: `F283 R17 C3: repair R-1030's comment; pin attach-job, ui stop and ui start`

C4 — THE RATCHET, tests only: `tests/cli/test_json_envelope.py` gains a class that scans
  `apps/cli/` with D10's rule — exactly what `raw_sites.py` counts — and asserts the
  per-module counts EQUAL a module-level dict constant, the reading at this commit. Its
  docstring names D10.
  Subject: `F283 R17 C4: a ratchet on the raw --json documents left under apps/cli (D10)`

C5 — HALF A converted by D10: every raw `--json` document in those ten modules is written
  through the envelope; a document with `ok` true drops it; `test run --json` whose run did
  not pass answers `test_run_failed` at exit 1, and because its document carries
  `exit_code` it is written by `emit_error` then `sys.exit(1)` (D10 (3)). The ratchet dict
  loses these modules. For each of the ten modules at least one test asserts `schema_version`
  1 and `ok` on a converted output, and `test run --json`'s failure envelope is asserted
  (token, `ok` false, exit 1, a top-level document key). Repair every test that pinned an old
  exact shape, keeping what it asserts; the reviewer's dry run found
  `tests/cli/test_contract_cmd.py::TestTheJobView::test_a_job_in_no_mission_is_one_sentence_and_null`,
  `tests/cli/test_contract_cmd.py::TestTheMissionView::test_json_carries_the_stored_body`,
  `tests/orchestration/test_data_reclaim.py::test_the_default_json_carries_no_hint_and_the_human_line_is_not_in_it`,
  `::test_the_json_shape`, `::test_the_orphan_json_shape` and
  `::test_without_the_flag_the_json_is_byte_for_byte_what_it_was`. Split this commit by
  module groups if it would pass 500 insertions.
  Subject: `F283 R17 C5: ten command modules answer --json success in the envelope (D10)`

C6 — HALF B converted by D10, with the same per-module test obligation; `init --json`'s
  indented `{"steps", "summary"}` document and `dev status --json`'s status document are among
  them. The ratchet dict must then name no module of the twenty unless a site is a text-branch
  survivor under D10 (5), named with its reason in the constant's comment.
  Subject: `F283 R17 C6: ten more command modules answer --json success in the envelope (D10)`

C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R17 C7: rewrite handoff for round 17`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the four `.agent/authored/f283-r17-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/ui_server.py`, the twenty modules above, and test files listed in
   `.remedy-wt/f283-r17-scratch/selection.txt`. Report the set you measure. Nothing else
   under `packages/` or `apps/`, nothing under `docs/`, no `README.md`, no `scripts/`, and
   none of `.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
   `.agent/prose_slips.md`.
4. EVERY COMMIT from C3 on leaves selection A at zero failed and zero errors: run
   `run_sel.py` after C3, C4, C5 and C6 and report all four readings.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. A worktree you add for G5 goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C7 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r17-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r17-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, each pre-file read at `488fd05a`:
     `.agent/live_review.md` (524486) plus ledger.md, the reviewer composed 529547;
     `.agent/decisions.md` (1823772) plus decisions.md, 1826927.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R16 — ` 1 and `^- R-1030 — ` 1.
     Open set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at
     `488fd05a` and at C2: the reviewer measured 24 and 25, ADDED `R-1030`, REMOVED empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE CHANGE, COUNTED FROM THE TREE — for C3 to C6 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. Report
 `raw_sites.py .`'s TOTAL line after C4, C5 and C6 (the reviewer read `TOTAL 122 modules 34`
 at `488fd05a`) and the module rows left after C6. At C3 report the `Landed: R-1030` line and
 the new comment's text. List every token the round's `fail(` and `emit_error(` calls
 introduce or reuse, each with its `git grep -c` count over `apps/` at `488fd05a`.
 `git diff --name-only 488fd05a <C6> -- packages/` prints
 `packages/orchestration/ui_server.py` alone.

G4 THE SELECTION — `.remedy-wt/f283-r17-scratch/selection.txt` (299 paths, `-n auto`).
 The reviewer read at `488fd05a`: `11250 passed, 13 skipped`, exit 0. After C3, C4, C5 and
 C6: zero failed and zero errors; the passed count may only rise. Then `python3 -m ruff
 check` over every `.py` path the round touched, and `python3 -m apps.cli.main integrity
 check --json`, all five checks `pass`. `python3 -m pytest tests/cli/test_golden_path.py
 -q` once after C6. DO NOT run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C6, never committed. Its
 first run builds the UI and reddens UI suites once: run the control TWICE and report both,
 judging each mutation against the second. The files: `tests/cli/test_project_current.py`,
 `tests/ui_server/test_live_state.py`, `tests/cli/test_json_envelope.py`, and every test
 file C5 and C6 changed — list them. Then each mutation alone, reverted before the next,
 reporting the summary line, the exit code and the failing test names:
 (a) `project attach-job`'s envelope carries `added=True` always — C3's pin must fail.
 (b) `ui stop`'s `failed` entries drop `error` — C3's pin must fail.
 (c) `start_ui_server` answers a 404 job with `invalid_job_id` — C3's pin must fail.
 (d) one converted `blocker list --json` site goes back to `print(_json.dumps(...))` — the
     ratchet must fail; report every other test that fails with it.
 (e) `test run --json` on a failed run answers `emit_ok` — C5's failure envelope test must
     fail.
 (f) `dev status --json` prints its raw document again — C6's `dev` envelope test must fail.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C7: `git status --porcelain` empty; `git log --oneline -n 8`;
 `git worktree list` (the primary checkout alone); `git stash list`'s first line unchanged
 from its reading before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the
 handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the token list, the item-status table, the deviations, and the next action. Your
Session section reads SESSION 4 of feature F283, round 17, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 17, then T002's second batch as `.agent/plan.md` lists it. State the
open-findings count, 25 after this round with R-1030 landed and awaiting review, and the
operator-questions count, 0.
