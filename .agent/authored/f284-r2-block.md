STEP F284 R2 — BOOK ROUND 1, LAND T003 (R-0950), WRITE THE BUILT STATE, RUN THE SELF-USE TRACK AND THE ONE FULL SUITE

GOAL
Book round 1's PASS with the resolutions of R-1046 and R-0499 and DECISION F284 D2; land T003,
R-0950's repair in `tests/orchestration/test_product_smoke.py`: one helper,
`assert_the_app_left_nothing_behind`, judges teardown at all five teardown sites by the harness's
own sweep, requires this worker's own port closed, and fails an open fallback port only when the
process holding it runs inside the test's project; write F284's Built State and the checklist
consolidation; record the closure's self-use track; and run the feature's one full suite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f284-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f284-r2/`           READ-ONLY. The reviewer's block, texts and builders.
  `.remedy-wt/f284-r2-dry/`, `.remedy-wt/f284-r2-sim/`, `.remedy-wt/f284-r1-dry/` and
  `.remedy-wt/f284-r1-sim/`       The reviewer's trees; do not touch them.
  `.remedy-wt/f284-r2-worker/`    YOURS for logs and scripts; create it if absent. All of these
                                  are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. The ONE npm command this round
allows is the UI build C6 orders; never `npm ci`, `npm install` or `npx`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f284-findings-paydown-v3`, and `git log --oneline -1` must read `60c658d2`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f284-r2/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f284-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| book.diff | 60 | 11148 | cefdca0986bd35458e40bb46968fbae766b0b92d9f6612a3f93dbcb54c4f3961 |
| plan.md | 31 | 1063 | 736249b13c751a6bcfbdcd4bc1588c78c38e8c9297d68393be896e7b6e60a748 |
| smoke.diff | 154 | 7225 | c31bb15a8a72c083521bd96ddefcde75cfbd07aee9f4046b9f72170da0e091e5 |
| docs.diff | 47 | 3102 | 4b4973177005792c961373fb10b2fbe21b9899883da9456570761b51e174f0a5 |
| mutations.py | 89 | 3824 | 023ed20c26aa5fc30f34691ee532fb1b8a811d6e5119582b8acc79ba8b6f2d88 |
| r0950_probe.py | 65 | 2156 | 3f24082e88bd8b6f646929390ca83ffe38df024037653dc2d21fe2e0f4d89d30 |
| selfuse.py | 16 | 755 | abcec8f8aa1c9b2add1c379d7a60bd9b935e205587bf55328f38332a64b28245 |
| selfuse_result.txt | 6 | 274 | d9d483baeb672279e22c401695f33028c814ff09072d3d738d68470bafa93057 |

`plan.md` is a REWRITE of `.agent/plan.md`. The three `.diff` payloads go on with `git apply`;
the reviewer generated each with `git diff HEAD` from a tree at `60c658d2` into which it wrote
the edits. `book.diff` appends round 1's gate entry and the `Done:` lines of R-1046 and R-0499
to `.agent/live_review.md` and DECISION F284 D2 to `.agent/decisions.md`. `smoke.diff` edits
`tests/orchestration/test_product_smoke.py`. `docs.diff` adds the consolidation sentence to
`docs/agents/planner_reviewer_prompt.md` and amends T003 and adds the Built State in
`docs/roadmap/features/T2_F284.md`. `selfuse_result.txt` becomes the NEW FILE
`.agent/selfuse_f284/result.txt`, copied only after C5's readings equal it. `mutations.py`,
`r0950_probe.py` and `selfuse.py` are TOOLS: run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the record payloads: `.agent/authored/f284-r2-block.md` := this
  block, and `.agent/authored/f284-r2-<name>` := each of plan.md, book.diff, docs.diff,
  selfuse.py and selfuse_result.txt, keeping its own file name. All by `shutil.copyfile`.
  Subject: `F284 R2 C1a: copy round 2 block and record payloads into .agent/authored/`
  Expected insertions: 397 (this block's 237 lines plus 160 for the payloads it copies). Report the number you measure and STOP rather than commit if
  it is 500 or more.
C1b — copy the test payload and the tools: `.agent/authored/f284-r2-<name>` := each of
  smoke.diff, mutations.py and r0950_probe.py.
  Subject: `F284 R2 C1b: copy round 2 test payload and probe tools into .agent/authored/`
  Expected insertions: 308.
C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4): `git apply` book.diff, then
  rewrite `.agent/plan.md` := plan.md.
  Subject: `F284 R2 C2: book round 1's PASS, resolve R-1046 and R-0499, record D2`
  Expected insertions by `git show --numstat`: 38 .agent/decisions.md, 6 .agent/live_review.md, 10 .agent/plan.md.
C3 — T003, R-0950: `git apply` smoke.diff.
  Subject: `F284 R2 C3: judge smoke teardown by the harness sweep and a port by its holder`
  Expected insertions: 52 tests/orchestration/test_product_smoke.py.
C4 — THE BUILT STATE, T003'S AMENDMENT AND THE CONSOLIDATION: `git apply` docs.diff.
  Subject: `F284 R2 C4: write the Built State and consolidate the checklist`
  Expected insertions: 3 docs/agents/planner_reviewer_prompt.md, 17 docs/roadmap/features/T2_F284.md.
C5 — THE SELF-USE TRACK (closure precondition 6): run
  `python3 .remedy-wt/f284-r2-payloads/selfuse.py /home/decodeux/Repos/remedy` in the primary
  checkout. It prints `next_self_use_item()`, then `generate_and_append_if_empty()`, then
  `next_self_use_item()` again, then `git status --porcelain`. The reviewer read `None`, `None`,
  `None` and a status listing only its own uncommitted edits over its dry tree carrying C2 to C4;
  in your clean checkout the fourth reading must be `''`. If all four readings are those, create
  `.agent/selfuse_f284/` and copy selfuse_result.txt to `.agent/selfuse_f284/result.txt` by
  `shutil.copyfile`, then commit it. If ANY reading differs — the generator returns an item, or
  the queue file changes — STOP under constraint 4: commit nothing for C5, and report the
  readings verbatim.
  Subject: `F284 R2 C5: record the closure's self-use track, NONE`
  Expected insertions: 6 .agent/selfuse_f284/result.txt.
C6 — THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C5:
  (a) Build the UI first, because a cold or stale `apps/ui/dist` reddens `tests/ui_server/` under
      `-n`: `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`.
      A refused or failing build is a STOP under constraint 4. Then `git status --porcelain`,
      which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its output written to a file under
      `.remedy-wt/f284-r2-worker/` while it runs, and its wall time measured. Write
      `.agent/authored/f284-closure-suite.txt` holding the command, the real exit code, the wall
      time, the summary line and the FULL list of bad node ids (failed plus errors), or the
      literal `NONE`.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F284 R2 C6: record the closure suite transcript and rewrite handoff for round 2`
  Then `git push origin feature/f284-findings-paydown-v3` and report its real outcome. Do NOT
  create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f284-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `tests/orchestration/test_product_smoke.py`, `docs/agents/planner_reviewer_prompt.md`,
   `docs/roadmap/features/T2_F284.md`, `.agent/selfuse_f284/result.txt`,
   `.agent/authored/f284-closure-suite.txt` and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 60c658d2` over the range to C6. No edit to `README.md`,
   `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`, `.agent/prose_slips.md`,
   `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. THE ONE
   EXCEPTION is the full suite in C6: a red suite is this feature's work and not a stop — commit
   its transcript exactly as measured, report every bad node id, and hand back. Never weaken an
   assertion, delete a test or mark anything xfail on your own initiative.
5. You write no `Done:` line and no `Landed:` line: the reviewer authors R-0950's resolution at
   the next gate.
6. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no STATUS edit, no evidence job, no review package.
7. Leave every existing worktree under `.remedy-wt/` and its branch, every local branch, and
   every stash alone. The worktree G3 adds goes under `.remedy-wt/`, is removed as that step's
   last action, and `git worktree list` is reported afterwards.
8. The full suite runs ONCE, in C6, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C6 is written, and G5
is the suite C6 runs.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f284-r2-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f284-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS, THE TEST, THE DOCS AND THE TRACK — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 builder printed from its simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2022752 | 85963c6a345604e21dfa24bf38e0c77cd5d7132ffd63725d696f0b1ae739fc7f |
 | C2 | .agent/live_review.md | 308181 | b823ea7fd34f9bfefd2eab7169fbc8eb7a542446547d854079a06ba7f68cc9d5 |
 | C2 | .agent/plan.md | 1063 | 736249b13c751a6bcfbdcd4bc1588c78c38e8c9297d68393be896e7b6e60a748 |
 | C3 | tests/orchestration/test_product_smoke.py | 46128 | 4f1394f32c5476fac1e42c79a9fe13fdad544dbedbb8719658a9768764f873f2 |
 | C4 | docs/agents/planner_reviewer_prompt.md | 101079 | 07fe64f06b9292e2637703978a93dc3128a606f3c45f021d654fb96c667593bc |
 | C4 | docs/roadmap/features/T2_F284.md | 5171 | 0e566a028433aa513bdaa4915bd4f9eca5c1a717ccd1dcc847ca48ef2ccac02a |
 | C5 | .agent/selfuse_f284/result.txt | 274 | d9d483baeb672279e22c401695f33028c814ff09072d3d738d68470bafa93057 |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the counts of those beginning
 `Gate: F284 R1 — `, `Done: R-1046 — ` and `Done: R-0499 — ` (the reviewer's builder read 1
 each); the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `60c658d2` and at C2 (the reviewer read
 R-0499, R-0950, R-1008 and R-1046 at `60c658d2`, and R-0950 and R-1008 at C2); and the
 checklist's item numbers, computed with `live_checklist_items` of
 `packages/orchestration/block_lint.py` over `docs/agents/planner_reviewer_prompt.md` at
 `60c658d2` and at C4, which must be the same list.

G3 THE RED PROOFS — `git worktree add --detach .remedy-wt/f284-r2-mut <C3>`, then
 `python3 -B .remedy-wt/f284-r2-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f284-r2-mut 60c658d2
 .remedy-wt/f284-r2-payloads/r0950_probe.py` and report its whole output. The tool runs the five
 teardown nodes under the probe plugin's modes with this round's test file and with the file at
 `60c658d2`, removes the one owner check for m1, restores the file byte-identical, removes the
 plugin copy it placed, and counts fixture app processes before and after, which must be EQUAL;
 their value is the machine's, and the reviewer's 1 is an orphaned `flow_app.py` left by an
 earlier run, which you leave alone. The reviewer read, over the same tool against its
 simulated tree at C3:
 m1 FROM occurs 1x in tests/orchestration/test_product_smoke.py
 control first: exit 0: 5 passed in 2.08s; failed: []
 p1 FOREIGN, this round's file: exit 0: 5 passed in 2.39s; failed: []
 p2 FOREIGN, the base file: exit 1: 5 failed in 2.21s; failed: ['test_no_zombie_processes_after_every_outcome', 'test_no_zombie_processes_after_the_suite', 'test_the_app_is_always_stopped', 'test_the_app_is_stopped_after_a_path_failure', 'test_the_app_is_stopped_even_when_the_console_is_dirty']
 p3 LEAK, this round's file: exit 1: 5 failed in 23.19s; failed: ['test_no_zombie_processes_after_every_outcome', 'test_no_zombie_processes_after_the_suite', 'test_the_app_is_always_stopped', 'test_the_app_is_stopped_after_a_path_failure', 'test_the_app_is_stopped_even_when_the_console_is_dirty']
 p4 REPORTED, this round's file: exit 1: 5 failed in 2.25s; failed: ['test_no_zombie_processes_after_every_outcome', 'test_no_zombie_processes_after_the_suite', 'test_the_app_is_always_stopped', 'test_the_app_is_stopped_after_a_path_failure', 'test_the_app_is_stopped_even_when_the_console_is_dirty']
 p5 REPORTED, the base file: exit 1: 3 failed, 2 passed in 2.17s; failed: ['test_the_app_is_always_stopped', 'test_the_app_is_stopped_after_a_path_failure', 'test_the_app_is_stopped_even_when_the_console_is_dirty']
 m1 LEAK, the owner check removed: exit 1: 1 failed, 4 passed in 23.00s; failed: ['test_the_app_is_always_stopped']
 control last: exit 0: 5 passed in 2.03s; failed: []
 test file restored byte-identical: True
 fixture app processes alive before: 1, after: 1
 ALL PROBES READ AS EXPECTED AND RESTORED CLEANLY: True
 Then `git worktree remove --force .remedy-wt/f284-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G4 THE TESTS, THE LINTER AND THE TREE — in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_product_smoke.py tests/orchestration/test_dod_runners.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command, serially, inside its simulated tree at C5 and read
 `615 passed, 1 skipped` at real exit code 0; your tree carries nothing the simulation lacked. Then
 `python3 -m ruff check tests/orchestration/test_product_smoke.py`, which must read
 `All checks passed!`; `python3 -m apps.cli.main integrity block .remedy-wt/f284-r2/block.md`,
 real exit code 0 with every item `[OK]`; `python3 -m apps.cli.main integrity check --json`, all
 six checks `pass` at `fail_count` 0; and `git status --porcelain` empty with no untracked file
 (closure precondition 3).

G5 THE INTEGRATION GATE — the UI build's last line and real exit code, `git status --porcelain`
 after it, then the full suite's real exit code, its wall time, its summary line and every bad
 node id, all of it in `.agent/authored/f284-closure-suite.txt`. Report whether
 `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
 bad node (closure precondition 7).

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6, C5, C4, C3, C2, C1b, C1a and `60c658d2` in that
 order; `git worktree list`, which must show no worktree this round added; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F284, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2 and of the closure suite transcript, then the evidence job and the review package.
State the open-findings count, 2, and the operator-questions count, 3.
