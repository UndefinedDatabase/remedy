STEP F024 R5 — T003's end-to-end: a live fake job scrubbed at every position by the real modules, the fixture's ledger, and the scrub budget on the 500-node fixture with its red control, with round 4's PASS and DECISION F024 D5 booked

GOAL
Book round 4's PASS, record DECISION F024 D5, and land T003's end-to-end: `brainPerfLedger`, the
500-node fixture's seeds and ledger, with its test; `apps/ui/src/components/timeline/scrubLive.test.ts`
and its driver `tests/ui_server/test_timeline_scrub_live.py`, which run a real fake-provider job and
scrub its ledger at every position with the real modules; and the scrub budget tool, kept as
evidence under `.agent/authored/f024-r5-perf-*`, whose run in the primary checkout — the budget and
its red control — is committed as `.agent/authored/f024-r5-perf.txt`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f024-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f024-r5/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f024-r5-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f024-r5-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f024-r5-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f024-phase-timeline-scrubber`, and `git log --oneline -1` must read `a46facfa`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f024-r5/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f024-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| fixture.diff | 59 | 3002 | 0bf580babb8530047ae342d1b7fc0006b95c7bd946577e7eeecab9e5828a042a |
| ledger.diff | 66 | 10900 | 2693eaedb3c1923ffdd5278f8237322d1644bab61611e7b655566cba1a684d07 |
| mutations.py | 169 | 7453 | 59a644d671f7fbaa9706534fb523986858ae280d6fb26cab97fe515958e229ad |
| perf-drive_chrome.mjs | 94 | 4142 | 98e525eacc755d764fee15b8157f527ee3aacb72b553f08032c3d9f04932db59 |
| perf-index.html | 14 | 351 | 5cf33c51a0cda0d6f29f29947237ec63e64aa2bcabe172cdb548a2ecdb0e6194 |
| perf-main.tsx | 142 | 6602 | 4de8b8389d3562c7073e502c718ca52d7d37da75f2ccd135a75f3628f89bca77 |
| perf-measure.py | 191 | 6789 | f3ccaff17821bf8940f5a7ca0386e82a4aaf2a6a47ed9a363e8d49976b2687f2 |
| perf-vite.config.mjs | 28 | 766 | 82b2d0f857c6821f6136d323d41d43ad94e6e4993ff192f17ee5425f9a74c6a9 |
| plan.md | 33 | 1285 | 13d8f463503468a788922ddfb61aa2abfd61705d2704161ad7cfa9454fbab719 |
| scrubLive.test.ts | 74 | 3743 | b0765be3bd127527c08e666b4ed839295906a66fc9bd6eeeabf2403d10a70ed1 |
| test_timeline_scrub_live.py | 73 | 3517 | 45f33a8693c23b7136c68991d61e69e6dea54f92c65376faa64996231d8487cb |

`plan.md` is a REWRITE of `.agent/plan.md`. `scrubLive.test.ts` becomes
a NEW FILE at `apps/ui/src/components/timeline/scrubLive.test.ts`, and `test_timeline_scrub_live.py`
a NEW FILE at `tests/ui_server/test_timeline_scrub_live.py`, each copied whole. The `perf-*` payloads are the
budget tool; each is copied whole to `.agent/authored/f024-r5-perf-<rest of its name>`, where
`perf-measure.py` finds its siblings by that prefix. `ledger.diff` and `fixture.diff` go on with
`git apply`; the reviewer generated each with `git diff HEAD` from a tree at `a46facfa` into which
it wrote the edits. `ledger.diff` appends round 4's gate entry to `.agent/live_review.md` and
DECISION F024 D5 to `.agent/decisions.md`; `fixture.diff` edits
`apps/ui/src/components/graph/brainPerfFixture.ts` and its `.test.ts`. `mutations.py` is a TOOL
for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f024-r5-block.md` := this block, and `.agent/authored/f024-r5-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F024 R5 C1a: copy round 5 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 33. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the ledger diff and the mutation tool
  `.agent/authored/f024-r5-ledger.diff` and `.agent/authored/f024-r5-mutations.py`.
  Subject: `F024 R5 C1b: copy round 5 ledger diff and mutation tool into .agent/authored/`
  Expected insertions: 235.

C1c — copy the fixture and live-test payloads
  `.agent/authored/f024-r5-fixture.diff`, `.agent/authored/f024-r5-scrubLive.test.ts` and
  `.agent/authored/f024-r5-test_timeline_scrub_live.py`.
  Subject: `F024 R5 C1c: copy round 5 fixture and live-test payloads into .agent/authored/`
  Expected insertions: 206.

C1d — THE BUDGET TOOL: copy the five `perf-*` payloads to their `.agent/authored/f024-r5-perf-*`
  names, the paths the G3 table's second part lists.
  Subject: `F024 R5 C1d: add the scrub budget tool to .agent/authored/`
  Expected insertions: 469.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F024 R5 C2: book round 4's PASS, record D5, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 48/0 decisions.md, 2/0 live_review.md, 10/11 plan.md.

C3 — THE FIXTURE: `git apply` fixture.diff.
  Subject: `F024 R5 C3: export the 500-node fixture's ledger`
  Expected by `git show --numstat` (insertions and deletions): 9/0 brainPerfFixture.test.ts, 12/4 brainPerfFixture.ts.

C4 — THE LIVE END-TO-END: copy scrubLive.test.ts into `apps/ui/src/components/timeline/` and
  test_timeline_scrub_live.py into `tests/ui_server/`, and `git add` both.
  Subject: `F024 R5 C4: scrub a live fake job's ledger at every position with the real modules`
  Expected insertions: 74 scrubLive.test.ts, 73 test_timeline_scrub_live.py.

C5 — THE BUDGET READING: `.agent/authored/f024-r5-perf.txt`, a NEW FILE holding, in this order,
  the whole output of G5's budget run, a line reading exactly
  `--- red control: slow_ms 25 ---`, and the whole output of G5's red-control run.
  Subject: `F024 R5 C5: record the scrub budget and its red control`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F024 R5 C6: rewrite handoff for round 5`
  Then `git push origin feature/f024-phase-timeline-scrubber`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before every real
   `git apply` and report each exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f024-r5-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, every path the G3 table's
   first part names, and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only a46facfa HEAD` after C6. Do NOT touch `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `.agent/context.md`,
   `docs/roadmap/STATUS.md`, `README.md` or `docs/roadmap/features/T5_F024.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f024-r5-sim`, `.remedy-wt/f024-r5-dry`, the rounds 1 to 4
   ones and the older `f015-*`, `f020-*`, `f023-*` and `f284-*` ones), and every existing stash
   alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action,
   and `git worktree list` is reported afterwards. The budget tool makes and removes its own work
   directory `.remedy-wt/f024-perf-run`; report that it is gone afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F024's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written, and G5's
two budget runs before C5.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f024-r5-*` copy of a payload byte
 for byte with its source (the block copy against `.remedy-wt/f024-r5/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 305257 | db2ad1e9d9e6a8d20496d2133176868180721339ee2ccf5212aa36d054fd0b80 |
 | .agent/decisions.md | 2093454 | d2194596dd69a335dfcae8c585982ee2f0fe3d53630a57c0a07c9b30e2238af0 |
 | .agent/plan.md | 1285 | 13d8f463503468a788922ddfb61aa2abfd61705d2704161ad7cfa9454fbab719 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `a46facfa` and at C2 (the reviewer
 read R-1008 alone at both); the lines C2's diff ADDS to `.agent/live_review.md`, of which the
 reviewer read 2, exactly one beginning `Gate: F024 R4 — `; the ledger's last line at C2, which
 must begin `Gate: F024 R4 — `; and `git diff --name-only <C1d> <C2>`, which must name exactly
 the paths of the table above.

G3 THE PRODUCT, THE TESTS AND THE TOOL — the sha256 of each file below, read with `git show` at the
 commit named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/brainPerfFixture.ts | 7700 | 44efb6bf35d1fbd9243b0035b8c8028278855f11a97c06ce6558f2b03372cc90 |
 | C3 | apps/ui/src/components/graph/brainPerfFixture.test.ts | 3215 | 567356998996f397d5c5bae1b7bef2008d8a07bffbbb6e607941fd86171ee8e7 |
 | C4 | apps/ui/src/components/timeline/scrubLive.test.ts | 3743 | b0765be3bd127527c08e666b4ed839295906a66fc9bd6eeeabf2403d10a70ed1 |
 | C4 | tests/ui_server/test_timeline_scrub_live.py | 3517 | 45f33a8693c23b7136c68991d61e69e6dea54f92c65376faa64996231d8487cb |
 and each budget-tool copy, read at C1d:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/authored/f024-r5-perf-drive_chrome.mjs | 4142 | 98e525eacc755d764fee15b8157f527ee3aacb72b553f08032c3d9f04932db59 |
 | .agent/authored/f024-r5-perf-index.html | 351 | 5cf33c51a0cda0d6f29f29947237ec63e64aa2bcabe172cdb548a2ecdb0e6194 |
 | .agent/authored/f024-r5-perf-main.tsx | 6602 | 4de8b8389d3562c7073e502c718ca52d7d37da75f2ccd135a75f3628f89bca77 |
 | .agent/authored/f024-r5-perf-measure.py | 6789 | f3ccaff17821bf8940f5a7ca0386e82a4aaf2a6a47ed9a363e8d49976b2687f2 |
 | .agent/authored/f024-r5-perf-vite.config.mjs | 766 | 82b2d0f857c6821f6136d323d41d43ad94e6e4993ff192f17ee5425f9a74c6a9 |
 Also `git diff --name-only` between C2 and C3 and between C3 and C4, each of which must name
 exactly the paths the first table gives that commit; and `python3 -m ruff check
 tests/ui_server/test_timeline_scrub_live.py .agent/authored/f024-r5-perf-measure.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_timeline_scrub_live.py tests/ui_server/test_brain_demo_recording_live.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1466 passed, 11 skipped` at real exit code 0. FIVE of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`), the vitest node in `tests/orchestration/test_test_runner.py`, which runs the
 UI's whole unit suite with `scrubLive.test.ts` skipping there, and the new live end-to-end in
 `tests/ui_server/test_timeline_scrub_live.py`, which must read its five live checks run and
 passed. Report every `SKIPPED` line the `-rs` summary prints. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS AND THE BUDGET — first `git worktree add --detach .remedy-wt/f024-r5-mut <C4>`,
 then `python3 -B .remedy-wt/f024-r5-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f024-r5-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `brainPerfFixture.test.ts` from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f024-r5-mutscratch/`, and pytest over the
 worktree's live end-to-end, for which it links the primary's `apps/ui/node_modules` into the
 worktree first and removes the link last; it asserts each FROM occurs exactly once, restores the
 bytes, and runs an unmutated control first and last. Its guard counts are read from the
 combined output, which quotes the inner vitest run's own counts when the live test fails. The
 reviewer read, over the same tool against its sim tree (v = vitest failed, g = guard failed,
 each red at exit 1 wherever its count is not 0):
 control first vitest 11 passed and contract tests 1 passed, both at exit 0;
 m1 (a snapshot also holds the row at its boundary) v0 g1;
 m2 (the index reads a position without its own row) v0 g2;
 m3 (the handle sits at the start of its event's slot) v0 g1;
 m4 (End scrubs to the head instead of returning to LIVE) v0 g1;
 m5 (the fixture's ledger loses its first row) v3 g0;
 control last as first;
 every `restored byte-identical` reading True, the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`, and `node_modules link removed: True`.
 Then `git worktree remove --force .remedy-wt/f024-r5-mut`, `git worktree prune`, and report
 `git worktree list`.
 THEN THE BUDGET, in the primary checkout at C4, each run's whole output saved under your own
 directory for C5:
 `bash -c 'python3 .agent/authored/f024-r5-perf-measure.py /home/decodeux/Repos/remedy; echo "REAL_EXIT=$?"'`
 must end `BUDGET 500 nodes, scrubbed one event per frame: PASS` at real exit code 0, and
 `bash -c 'python3 .agent/authored/f024-r5-perf-measure.py /home/decodeux/Repos/remedy 25; echo "REAL_EXIT=$?"'`
 must end with the same line reading `FAIL` at real exit code 1. The reviewer's readings on its
 sim tree were `FRAMES: worst p95 16.8 ms, worst mean 60 fps` and
 `SCRUB: worst warm p95 1.4 ms, worst cold max 2.1 ms` for the first, and a worst mean near 30
 frames a second for the second; your machine's numbers may differ, the verdicts may not.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and `a46facfa`
 in that order; `git worktree list`, which must show the primary checkout and the worktrees
 constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F024, round 5, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the closure sequence's first half — the Built State, the one full suite, the
self-use track and the checklist consolidation. State the open-findings count, 1, and the
operator-questions count, 3.
