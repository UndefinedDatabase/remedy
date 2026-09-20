STEP R6 T002 — F277 Machine contracts: event vocabulary, JSON envelope, exit codes
Session 2 of F277 · round 6 · base `91034712` (the tip of `feature/f277-machine-contracts`,
round 5's C4). This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 5's PASS verdict, register finding `R-1014` — the round 5 gate this reviewer made
unmeetable, which you stopped on and were right to — and land T002: `apps/cli/json_envelope.py`
with one envelope shape, and an error boundary around dispatch in `apps/cli/grouped.py` so that
no uncaught handler exception reaches the operator as a traceback, under `--json` or otherwise.

Read first, completely: AGENTS.md; `docs/roadmap/features/T2_F277.md`; and the payload
`decisions.md`, which is DECISION F277 D6 and is this round's spec — where this block is
terser, D6 rules. D6 exists because T002 as written names a project exception base that does
not exist; it records what the boundary catches instead and why, and C4 amends the feature file
to match.

`R-1014` is registered by C1b and stays OPEN, owned by F277. Its repair is a rule for the
pre-emission checklist of `docs/agents/planner_reviewer_prompt.md` §3, which operator amendment
amend0827-process-diet rule 4 FREEZES while a feature is open, so it lands in this feature's
closure sequence at the one consolidation pass that amendment schedules. Nothing in this round
resolves it and nothing should.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f277-r6-payloads/`. Verify each
line count and sha256 BEFORE use and report both readings; any mismatch stops the round. Apply
byte-exact, never by retyping.
  ledger.md      lines 4   sha256 104f952a6562a6cbb3ed4fe51d91a7329be1b25fc90ec5995210107cd0dbcb32
  decisions.md   lines 43  sha256 e195928a1643e5d099f90f26906f0b820206928dc5dda84f52e3bb1221adfce5
  plan.md        lines 45  sha256 d1eb87045001157555de2cbde0c973de905f9f05fc882ccb28637a8896bbec1e
  block.md       this block; save it and report its line count and digest (R-0954)
CODE — ONE diff the reviewer produced in its own dry-run worktree at `91034712`, applied there,
tested there and red-proved there. Verify its digest, then apply it in THREE disjoint slices
with the `--include` lists below, always from its scratch path. Do not retype a hunk, do not
edit one, do not copy the diff into the repository, and never apply it whole.
  `.remedy-wt/f277-r6-payloads/f277-r6.diff`
    lines 382  sha256 de12e25c172fa3456247d83bef637ba0d944489782486de0c1663430fe649995
TWO OF THE FOUR PATHS ARE NEW FILES — `apps/cli/json_envelope.py` and
`tests/cli/test_json_envelope.py` do not exist at `91034712` and the diff carries them as
`new file mode` hunks. `git apply --include=<path>` creates them; you do not create them by
hand and you do not `git add` them before applying. The reviewer rehearsed all three slices in
a throwaway worktree at `91034712` and every `git apply --check` and `git apply` exited 0.

SHAPE OF EACH STATE PAYLOAD, tested mechanically by the reviewer at `91034712`, one reading per
pair, the label derived from that reading's own output on the same line (item 15):
  `.agent/live_review.md` contains ledger.md — false, so APPEND
  `.agent/decisions.md` contains decisions.md — false, so APPEND
  `.agent/plan.md` contains plan.md — false, so REWRITE
Every pair reads false, so all are NEW bytes and NO FROM-count proof is owed on any of them.
ledger.md and decisions.md each begin with a newline, the blank separator their targets use
between entries. There is no `.agent/prose_slips.md` payload this round: the lesson that would
have gone there took an id instead, because the defect reached a gate over production code
rather than a count, and amend0827 rule 2 lets only one of the two classes spend an id.

Bundle, in commit order
C1a the payload copies, ONE commit whose whole change set is new files under `.agent/authored/`:
   a byte copy of each payload listed above, `block.md` included, as
   `.agent/authored/f277-r6-<name>`. The code diff is NOT copied and is NOT part of this or any
   commit; G2's blob-id gate is its fidelity proof, which pins the applied RESULT rather than
   the instructions. This block states no expected insertion count here, because the commit
   copies THIS BLOCK and the count therefore moves with every edit to it (item 16, R-0656).
   Report the number YOU read with `git show --numstat`, and stop only if yours reaches 500.
C1b the booking, ONE commit: `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `91034712` bytes + ledger.md; `.agent/decisions.md` := its `91034712` bytes + decisions.md.
   Expected insertions 70 — 4 plus 43 for the two appends and 23 for the plan REWRITE, which is
   the numstat of the rewrite and not the payload's 45 lines. All three numbers were computed by
   the reviewer's preflight script from the payload files this block ships. Report the number
   YOU read.
C2 the envelope and the boundary —
   `git apply --include=apps/cli/json_envelope.py --include=apps/cli/grouped.py
    .remedy-wt/f277-r6-payloads/f277-r6.diff`
   then commit. Expected insertions 145; report the number YOU read.
C3 the tests, including the red proof the feature file's Acceptance asks for —
   `git apply --include=tests/cli/test_json_envelope.py
    .remedy-wt/f277-r6-payloads/f277-r6.diff`
   then commit. Expected insertions 179; report the number YOU read.
C4 the feature-file amendment —
   `git apply --include=docs/roadmap/features/T2_F277.md
    .remedy-wt/f277-r6-payloads/f277-r6.diff`
   then commit. Expected insertions 13; report the number YOU read. This is the only
   `docs/roadmap/**` path this round touches and it is why G3 carries `tests/docs/`.
C5 handoff — rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`. The file you
   are replacing is round 5's STOP record, so replace it entirely rather than editing around it.
   The Session section reads "SESSION 2 of feature F277 · round 6 · rounds so far 6" plus ONE
   sentence of context self-assessment; then the per-commit table with `git show --numstat`
   insertion counts for C1a, C1b, C2, C3 and C4; every gate below with its real output and exit
   code, one line per gate; the open-findings count by distinct id; the item-status table; the
   deviations; and `## Next` naming Phase 1 rule 1 first, then the review of round 6, then T003
   — the `fail()` helper and the JSON gaps — and "Operator questions open: <the count of `### Q`
   headings you read from `.agent/operator_questions.md`>". Then
   `git push -u origin feature/f277-machine-contracts`. Open NO pull request.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as a deviation and
   applied anyway; it is never edited and no slice is retyped.
2. Change set: the paths the Bundle names, and nothing else. In particular do NOT edit
   `docs/roadmap/STATUS.md` or `README.md` — no feature is registered or accepted this round.
3. The commit sequence is C1a, C1b, C2, C3, C4, C5: no extra commit, none dropped, none
   reordered. C1b precedes C2 so `.agent/plan.md` is current before the first product commit
   (item 23) and so DECISION F277 D6 is on disk before the code that applies it. C2 precedes C3
   because the tests import the module C2 creates; the reviewer ran the suites nearest this
   change set against C2 alone in its dry-run worktree and read `395 passed` at exit 0, so the
   tip is green at every commit of this round.
4. An insertion count is read with `git show --numstat`, whose `+` column is the reading DECISION
   F104 D1 fixes for the 500-line cap; `git commit`'s own terminal summary applies rename
   detection and is NOT that reading — rounds 3, 4 and 5 each measured the two apart, so report
   which you used. Read it for EVERY commit. If any commit reaches 500 insertions by that
   reading, STOP and report — no oversize exception is declared for this feature. The four
   expected values above are the reviewer's arithmetic; where yours differs, report YOURS and
   say so, and stop only if yours reaches 500.
5. Never force-push, never rewrite history, never delete a branch, never merge. Run NO `gh`
   command at all this round.
6. Read `.agent/STOP` from disk before the first commit. If it exists, write the handoff and end,
   doing nothing else.
7. The shell may deny `VAR=x cmd`, `cp` and some compound commands; copy bytes and read exit
   codes with small python scripts under `.remedy-wt/f277-r6-payloads/`. Prefer `git -C <path>`
   over `cd <path> && git`.
8. `.remedy-wt/` is gitignored scratch. Never run `git clean -x`. The directories whose names
   begin `f277-` under `.remedy-wt/` are the reviewer's and are not yours to delete;
   `f277-r6-dry` is a registered worktree of this repository and removing it is a
   history-touching act this block does not order.
9. Never weaken an assertion or delete a test. A red gate, or an ambiguity DECISION F277 D6 does
   not settle, stops the round: commit nothing half-done and report. Round 5 did exactly that
   against a gate this reviewer had written wrong, and it was the right call.
10. The full suite does NOT run this round (amend0917-throughput rule 1). It runs once per
    feature, in the closure sequence's integration-gate round.
11. Commit messages "F277 R6 C<n>: <summary>", a blank line, then
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when — the six gates below, each EXECUTED, each reporting its REAL output and exit code.
"Green" as a word is a finding. G1 to G5 run at C4, before C5.

G1 TRANSPORT AND STATE. One python check printing an explicit True or False per reading.
   (a) Each `.agent/authored/f277-r6-*` file equals its payload on disk byte for byte. Report
       the number of such files YOU measured rather than taking a count from this block.
   (b) THE RECORD APPENDS, in full byte forensics, which the gate budget reserves for
       `.agent/live_review.md` and `.agent/decisions.md`. For each at C1b — the ledger file
       against its `91034712` bytes plus ledger.md, and the decisions file against its
       `91034712` bytes plus decisions.md — take reading (a), byte equality of pre plus payload
       against post; reading (b), an INDEPENDENT structural reader that splits the post file on
       blank lines and compares its LAST N units, in order, against the payload's N paragraphs,
       where N is a number the script COUNTS from the payload and never one this block states;
       and a NEGATIVE CONTROL that flips one byte inside the FIRST appended paragraph and
       confirms BOTH readings reject it. Each payload's leading newline is the blank SEPARATOR
       between entries and not a paragraph of its own. Decode with `errors="replace"` for the
       structural reading only; reading (a) stays on raw bytes.
   (c) Byte equality only: `.agent/plan.md` at C1b equals plan.md's bytes.
   (d) THE OPEN SET BY DISTINCT ID, counted as the distinct ids matching `^- R-\d+ — ` minus
       those matching `^Done: R-\d+ — `, at `91034712` and at C1b, with whether `R-1014` is
       among the open ids at each. This round REGISTERS without resolving, so the count must
       rise by exactly one and `R-1014` must be absent at the first reading and present at the
       second.
   Report the number of readings taken and that every one is True. SEPARATELY, report the SAVED
   BLOCK's own line count and sha256 beside the line count and digest this block's PAYLOADS
   section gives for `block.md` (R-0954).

G2 CODE TRANSPORT — the committed tree is the tree the reviewer tested, and this gate is the
   ONLY proof the diff arrived intact, since no copy of it is committed. The four lines below
   were PRINTED by the reviewer's rehearsal script from a single `git hash-object` call over the
   same path list the slices are built from, and copied here verbatim; that is the `R-1014`
   counter-measure and this is its first use. At C4, `git rev-parse <commit>:<path>` for each
   path — C2's two paths at C2 or later, C3's at C3 or later, C4's at C4 — must print exactly:
     apps/cli/json_envelope.py         cfa3aaff802f5228a23965b7a80c2faf2a449cb7
     apps/cli/grouped.py               4009a41712a4315619b2c4a38030799347e25fdb
     tests/cli/test_json_envelope.py   f631063418bfb8c625214863969e47a2d1c0db59
     docs/roadmap/features/T2_F277.md  e709f9462ce09f1e7c21f8e9ee964d3e5da2d1f4
   Report each path beside the id YOU read, on one line, so the mapping is visible rather than
   implied. Also report `git diff --name-only <C1b> <C4>` in full: it must name exactly those
   four paths and no other. Report that list and its length.

G3 THE TARGETED SUITE, in the primary checkout, serial (no `-n`), at C4:
     python3 -m pytest -q -p no:cacheprovider tests/cli/test_json_envelope.py
       tests/test_grouped_cli.py tests/test_command_catalog.py tests/docs
       tests/orchestration/test_roadmap_index.py tests/orchestration/test_event_names.py
       tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
       tests/cli/test_golden_path.py
   Report the summary line and the exit code. It must read 0 failed at exit 0. `tests/docs` and
   `tests/orchestration/test_roadmap_index.py` are here because C4 edits a `docs/roadmap/**`
   path; `tests/test_grouped_cli.py` and `tests/test_command_catalog.py` are the files nearest
   the dispatch this round wraps; `tests/test_no_orphan_modules.py` and
   `tests/orchestration/test_import_reachability.py` are the guards a NEW module under `apps/`
   must satisfy; `tests/cli/test_golden_path.py` is the canary.

G4 LINT, at C4:
     python3 -m ruff check apps/cli/json_envelope.py apps/cli/grouped.py
       tests/cli/test_json_envelope.py
   must print "All checks passed!". Pass ONLY these three paths — the fourth changed path is
   markdown and ruff would parse it as Python.

G5 MUTATION RED-PROOFS, in ONE disposable worktree under `.remedy-wt/` created at C4 and removed
   as this gate's last action. Name it `.remedy-wt/f277-r6-g5` and do NOT reuse any existing
   directory there. Run every command from the worktree root with
     python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_json_envelope.py
   Take the UNMUTATED CONTROL FIRST and report its exit code: it must be 0. Then apply each
   mutation below, one at a time, each restored byte-identically before the next; before each,
   COUNT the occurrences of the exact bytes the recipe replaces in the named file and report the
   count, which must be 1, because that uniqueness is what makes the restore safe. Report each
   run's exit code and its failing node ids, and report a mutation that stays green AS GREEN.
   (a) THE BOUNDARY IS REMOVED. In `apps/cli/grouped.py`, replace the single line
       `    _dispatch(handler, args, command_id, raw)` with `    handler(args)`.
       Expected: FAIL, naming `test_an_undeclared_exception_becomes_a_one_line_message`,
       `test_under_json_it_becomes_a_parseable_envelope` and
       `test_a_declared_project_error_is_caught_the_same_way`.
   (b) THE ENVELOPE STOPS SORTING. In `apps/cli/json_envelope.py`, replace the single line
       `    print(json.dumps(envelope, sort_keys=True, default=str), file=stream)` with
       `    print(json.dumps(envelope, default=str), file=stream)`. Expected: FAIL, naming
       `test_every_level_is_sorted_so_two_runs_are_byte_comparable`.
   (c) A PAYLOAD MAY OVERWRITE THE ENVELOPE'S OWN KEYS. In the same file, replace the single
       line `    clash = [k for k in RESERVED_KEYS if k in payload]` with the two lines
       `    clash = []` and `    _unused = [k for k in RESERVED_KEYS if k in payload]`.
       Expected: FAIL, naming both parameters of
       `test_a_payload_may_not_overwrite_the_envelope`.
   (d) THE FAILURE ENVELOPE GOES TO STDERR. In the same file, replace the single line
       `    _write(build_error(error, message, **payload), sys.stdout)` with
       `    _write(build_error(error, message, **payload), sys.stderr)`. Expected: FAIL, naming
       `test_failure_goes_to_stdout_not_stderr` among its failures.
   (e) THE BOUNDARY IS WIDENED PAST `BaseException` WITH NO RE-RAISE. In `apps/cli/grouped.py`,
       replace the three lines beginning `    except (SystemExit, KeyboardInterrupt):` and
       ending with the `except Exception as exc:` line and its trailing comment, with the single
       line `    except BaseException as exc:  # noqa: BLE001 - the whole point is the catch-all`.
       Expected: FAIL, naming `test_a_handler_that_exits_deliberately_is_not_rewritten` and
       `test_a_keyboard_interrupt_is_not_reported_as_a_crash`. The reviewer tried the NARROWER
       mutation first — dropping only the re-raise clause — and it STAYED GREEN, because
       `SystemExit` and `KeyboardInterrupt` derive from `BaseException` and `except Exception`
       never saw them; the clause is what makes a later widening safe rather than what makes
       today's behaviour work, so the control that proves it must widen AND drop it together.
   After the five, show that each of the two touched files is byte-identical to before (report a
   sha256 per file), run the UNMUTATED selection once more and report that it is exit 0 again,
   remove the worktree, and report `git worktree list` in full.

G6 PUSH AND TREE. `git push -u origin feature/f277-machine-contracts` after C5; then
   `git status --porcelain`, which must be EMPTY; then `ls .agent/STOP`, which must be absent;
   then `git worktree list` in full, which must show the primary checkout, the two
   `remedy/job-*` worktrees, and the reviewer's `.remedy-wt/f277-r6-dry`, and no other. These
   readings necessarily POSTDATE the commit that writes the handback, so they belong to your
   final report and not to the handoff's own text (item 31).

Handback
Rewrite `.agent/handoff.md` as C5 describes, then report. The handback names every gate with one
line of its real output, declares every deviation, and carries the item-status table. If any gate
is red, say so plainly WITH the output: a red gate honestly reported ends the round cleanly and
is worth far more than a green word.
