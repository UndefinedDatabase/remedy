STEP F024 R3 — T003's pure half: the phase index, the scrubber machine with its keyboard and catch-up, the bar's view model and their guard, with round 2's PASS and DECISION F024 D3 booked

GOAL
Book round 2's PASS, record DECISION F024 D3, and land T003's pure half under
`apps/ui/src/components/timeline/`: `timelineIndex.ts`, which reads the phases of every prefix
from one fold and is held equal to `readPhases` at every position of fuzzed ledgers;
`scrubState.ts`, the scrubber machine with its keyboard and LIVE's capped fast-forward;
`timelineView.ts`, the bar's view model of six equal segments, sub-glyphs and the readout; their
vitest tests; and the guard `tests/ui_contracts/test_timeline_scrub_contract.py`, with red
proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f024-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f024-r3/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f024-r3-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f024-r3-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f024-r3-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f024-phase-timeline-scrubber`, and `git log --oneline -1` must read `81a92d9b`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f024-r3/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f024-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 70 | 10288 | 1529e71edb1ea6a99af46c9c595ecd296c443b6accd89e3a83c0a64e95a6a9ab |
| mutations.py | 186 | 9985 | 3ea41d83b79a94c75559e1ede55c0eadc3adf97d5f7bb484e7e5729d58f99d7b |
| plan.md | 35 | 1399 | 514eaaffc9f14e20f4ebaf309a453c841039d215dcfccf21dfcbc314536753e6 |
| scrubState.test.ts | 134 | 6026 | 79d9c39a4ab56e5bf18dc98efb6ff59749e58f88fc33c75d2ec39c7584862648 |
| scrubState.ts | 118 | 5099 | 8825c60514c39c5c5f1d3000ea7bd8be31e481c36193970c5cd883e345799eed |
| test_timeline_scrub_contract.py | 64 | 2951 | 859e866ba6e7b1bea3838829d1ceec931633401ab32a43b7a3576c99df297b00 |
| timelineIndex.test.ts | 105 | 4080 | fab8ce5593d8038f47b4dec0eb691e3b3d0c70d60ed396f621e8c94e44434631 |
| timelineIndex.ts | 99 | 4188 | 325bc684aa74509a1a1b8ad20ea4e40c77c34a654e2a1d0d493a335d350d2bdf |
| timelineView.test.ts | 124 | 6082 | a20a9d5b58d0dbde0648cee9d2f79a57c0859f28b3436bf767e4b529d9edab0f |
| timelineView.ts | 128 | 4844 | ead917d2d73736b8b52af3fcb7d5ae3ad90d2de4d2ee851cf640931fbf4e14de |

`plan.md` is a REWRITE of `.agent/plan.md`. `timelineIndex.ts` becomes a NEW FILE at
`apps/ui/src/components/timeline/timelineIndex.ts`, `scrubState.ts` a NEW FILE at
`apps/ui/src/components/timeline/scrubState.ts`, `timelineView.ts` a NEW FILE at
`apps/ui/src/components/timeline/timelineView.ts`, `timelineIndex.test.ts` a NEW FILE at
`apps/ui/src/components/timeline/timelineIndex.test.ts`, `scrubState.test.ts` a NEW FILE at
`apps/ui/src/components/timeline/scrubState.test.ts`, `timelineView.test.ts` a NEW FILE at
`apps/ui/src/components/timeline/timelineView.test.ts`, and `test_timeline_scrub_contract.py` a
NEW FILE at `tests/ui_contracts/test_timeline_scrub_contract.py`, each copied whole.
`ledger.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a
tree at `81a92d9b` into which it wrote the edits. It appends round 2's gate entry to
`.agent/live_review.md` and DECISION F024 D3 to `.agent/decisions.md`. `mutations.py` is a TOOL for G5: it is run, never applied to a
tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f024-r3-block.md` := this block, and `.agent/authored/f024-r3-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F024 R3 C1a: copy round 3 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 35. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the ledger diff and the mutation tool
  `.agent/authored/f024-r3-ledger.diff` := ledger.diff and `.agent/authored/f024-r3-mutations.py`
  := mutations.py.
  Subject: `F024 R3 C1b: copy round 3 ledger diff and mutation tool into .agent/authored/`
  Expected insertions: 256.

C1c — copy the product payloads
  `.agent/authored/f024-r3-timelineIndex.ts`, `.agent/authored/f024-r3-scrubState.ts` and
  `.agent/authored/f024-r3-timelineView.ts`.
  Subject: `F024 R3 C1c: copy round 3 product modules into .agent/authored/`
  Expected insertions: 345.

C1d — copy the test payloads
  `.agent/authored/f024-r3-timelineIndex.test.ts`, `.agent/authored/f024-r3-scrubState.test.ts`,
  `.agent/authored/f024-r3-timelineView.test.ts` and
  `.agent/authored/f024-r3-test_timeline_scrub_contract.py`.
  Subject: `F024 R3 C1d: copy round 3 test payloads into .agent/authored/`
  Expected insertions: 427.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F024 R3 C2: book round 2's PASS, record D3, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 52/0 decisions.md, 2/0 live_review.md, 11/10 plan.md.

C3 — THE PRODUCT: copy timelineIndex.ts, scrubState.ts and timelineView.ts into
  `apps/ui/src/components/timeline/`, then `git add` all three — an untracked module fails
  `integrity check`'s `relevant_untracked`.
  Subject: `F024 R3 C3: add the phase index, the scrubber machine and the bar's view model`
  Expected insertions: 118 scrubState.ts, 99 timelineIndex.ts, 128 timelineView.ts.

C4 — THE TESTS: copy the three `.test.ts` payloads into `apps/ui/src/components/timeline/` and
  test_timeline_scrub_contract.py into `tests/ui_contracts/`, and `git add` all four.
  Subject: `F024 R3 C4: hold the index to the plain fold, golden the machine and the bar, guard their timing`
  Expected insertions: 134 scrubState.test.ts, 105 timelineIndex.test.ts, 124 timelineView.test.ts, 64 test_timeline_scrub_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F024 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f024-phase-timeline-scrubber`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f024-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the six files under
   `apps/ui/src/components/timeline/` that the payloads name,
   `tests/ui_contracts/test_timeline_scrub_contract.py`, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 81a92d9b HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `docs/roadmap/STATUS.md`, `README.md`,
   `apps/ui/src/components/timeline/phaseMapping.ts`,
   `apps/ui/src/components/timeline/scrubSnapshots.ts`,
   `apps/ui/src/components/timeline/PhaseTimeline.tsx` or `docs/roadmap/features/T5_F024.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f024-r3-sim`, `.remedy-wt/f024-r3-dry`, the rounds 1 and 2 ones
   and the older `f015-*`, `f020-*`, `f023-*` and `f284-*` ones), and every existing stash alone.
   The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F024's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f024-r3-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f024-r3/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 301136 | 4ecaeebcd4c6b601f29e11150fdcddeef2b0724fb8ac31a2d3578a841f7d5818 |
 | .agent/decisions.md | 2085007 | de0a6f47e0c0f26bd270ae39238b30e049b848f1987b9bbf4ccf84847fcb27ab |
 | .agent/plan.md | 1399 | 514eaaffc9f14e20f4ebaf309a453c841039d215dcfccf21dfcbc314536753e6 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `81a92d9b` and at C2 (the reviewer
 read R-1008 alone at both); the lines C2's diff ADDS to `.agent/live_review.md`, of which the
 reviewer read 2, exactly one beginning `Gate: F024 R2 — `; the ledger's last line at C2, which
 must begin `Gate: F024 R2 — `; and `git diff --name-only <C1d> <C2>`, which must name exactly
 the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/timeline/timelineIndex.ts | 4188 | 325bc684aa74509a1a1b8ad20ea4e40c77c34a654e2a1d0d493a335d350d2bdf |
 | C3 | apps/ui/src/components/timeline/scrubState.ts | 5099 | 8825c60514c39c5c5f1d3000ea7bd8be31e481c36193970c5cd883e345799eed |
 | C3 | apps/ui/src/components/timeline/timelineView.ts | 4844 | ead917d2d73736b8b52af3fcb7d5ae3ad90d2de4d2ee851cf640931fbf4e14de |
 | C4 | apps/ui/src/components/timeline/timelineIndex.test.ts | 4080 | fab8ce5593d8038f47b4dec0eb691e3b3d0c70d60ed396f621e8c94e44434631 |
 | C4 | apps/ui/src/components/timeline/scrubState.test.ts | 6026 | 79d9c39a4ab56e5bf18dc98efb6ff59749e58f88fc33c75d2ec39c7584862648 |
 | C4 | apps/ui/src/components/timeline/timelineView.test.ts | 6082 | a20a9d5b58d0dbde0648cee9d2f79a57c0859f28b3436bf767e4b529d9edab0f |
 | C4 | tests/ui_contracts/test_timeline_scrub_contract.py | 2951 | 859e866ba6e7b1bea3838829d1ceec931633401ab32a43b7a3576c99df297b00 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_timeline_scrub_contract.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1460 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the three new test files. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f024-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f024-r3-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f024-r3-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's three new `.test.ts` files from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f024-r3-mutscratch/`, and pytest over the
 worktree's guard; it asserts each FROM occurs exactly once, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first vitest 25 passed and guard 4 passed, both at exit 0;
 m1 (a skipped phase gets no start in the index) v3 g0;
 m2 (the index never withdraws a pass) v1 g0;
 m3 (a position reads the row after it) v2 g0;
 m4 (Finalized ignores a later marker in the index) v1 g0;
 m5 (the phase stops repeat a shared start) v1 g0;
 m6 (a scrubbed view follows the head) v1 g0;
 m7 (rows behind the view are not counted) v1 g0;
 m8 (the handle goes below before-the-first-event) v2 g0;
 m9 (a step forward from LIVE leaves LIVE) v1 g0;
 m10 (the queue overflows at the cap itself) v1 g0;
 m11 (Shift is ignored on the arrows) v1 g0;
 m12 (the catch-up replays every queued event) v1 g0;
 m13 (reduced motion still fast-forwards) v1 g0;
 m14 (the frame length drifts from the motion token) v3 g1;
 m15 (segment states come from the whole ledger) v4 g0;
 m16 (a one-event phase is drawn compact) v1 g0;
 m17 (a glyph at the handle is not reached) v1 g0;
 m18 (the readout shows elapsed time before the first event) v1 g0;
 m19 (the view reads the wall clock) v0 g1;
 m20 (a label drifts from the dashboard's title) v2 g1;
 control last as first;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f024-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `81a92d9b` in
 that order; `git worktree list`, which must show the primary checkout and the worktrees
 constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F024, round 3, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003's components — the bar and scrubber in `PhaseTimeline.tsx`, the ledger and
scrub state lifted into the shell, the graph rendering the scrubbed prefix, the SCRUBBED banner
and the REPLAY pill. State the open-findings count, 1, and the
operator-questions count, 3.
