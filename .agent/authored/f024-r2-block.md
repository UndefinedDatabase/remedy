STEP F024 R2 — T002: the scrubber's snapshot memo, its prefix-equality property test and its guard, with round 1's PASS and DECISION F024 D2 booked

GOAL
Book round 1's PASS, record DECISION F024 D2, and land T002:
`apps/ui/src/components/timeline/scrubSnapshots.ts`, the memo that serves the reducer state at
any seq from snapshots every 200 seq under a cap of 64 — built lazily from the nearest lower
snapshot, dropped farthest-first beyond the cap, invalidated by the rows they should have held
and forgotten on a snapshot-refetch reset; its vitest property test, which holds the memo's
state at fuzzed positions equal to a fresh reduction of the prefix; and the guard
`tests/ui_contracts/test_scrub_snapshots.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f024-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f024-r2/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f024-r2-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f024-r2-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f024-r2-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f024-phase-timeline-scrubber`, and `git log --oneline -1` must read `78d60af2`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f024-r2/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f024-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 64 | 9590 | a7af36b247fc24acc1958dfbe6384d80e1b464994e131d89084c38480a1f0f82 |
| mutations.py | 167 | 8177 | 10448dcdcbf62cf1b1db09a5b369ef2eb67177d80a76388187c8510671f76295 |
| plan.md | 34 | 1321 | 6d461d078ff4f572e5bf010d67ed205159f776f38c7a6d914ca73f39393d606b |
| scrubSnapshots.test.ts | 236 | 10046 | 8a3f62dd6940956564f45402365396abe0dd03390f908dcf1b54e408844511ae |
| scrubSnapshots.ts | 147 | 5533 | c898fd7562f7a0c4fd40ee2184ca117d0c24bb0254818b0ad422dfa6f41266d2 |
| test_scrub_snapshots.py | 57 | 2884 | 0a6fab2256c80ca618e244ef598c8b0235c5d765ff1b2ae854fd9d8b3f1bb6ff |

`plan.md` is a REWRITE of `.agent/plan.md`. `scrubSnapshots.ts` becomes a NEW FILE at
`apps/ui/src/components/timeline/scrubSnapshots.ts`, `scrubSnapshots.test.ts` a NEW FILE at
`apps/ui/src/components/timeline/scrubSnapshots.test.ts`, and `test_scrub_snapshots.py` a NEW
FILE at `tests/ui_contracts/test_scrub_snapshots.py`, each copied whole. `ledger.diff` goes on
with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at `78d60af2` into
which it wrote the edits. It appends round 1's gate entry to `.agent/live_review.md` and DECISION
F024 D2 to `.agent/decisions.md`. `mutations.py` is a TOOL for G5: it is run, never applied to a
tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f024-r2-block.md` := this block, and `.agent/authored/f024-r2-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F024 R2 C1a: copy round 2 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 34. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the ledger diff and the mutation tool
  `.agent/authored/f024-r2-ledger.diff` := ledger.diff and `.agent/authored/f024-r2-mutations.py`
  := mutations.py.
  Subject: `F024 R2 C1b: copy round 2 ledger diff and mutation tool into .agent/authored/`
  Expected insertions: 231.

C1c — copy the product payload
  `.agent/authored/f024-r2-scrubSnapshots.ts` := scrubSnapshots.ts.
  Subject: `F024 R2 C1c: copy round 2 product module into .agent/authored/`
  Expected insertions: 147.

C1d — copy the test payloads
  `.agent/authored/f024-r2-scrubSnapshots.test.ts` and
  `.agent/authored/f024-r2-test_scrub_snapshots.py`.
  Subject: `F024 R2 C1d: copy round 2 test payloads into .agent/authored/`
  Expected insertions: 293.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F024 R2 C2: book round 1's PASS, record D2, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 46/0 decisions.md, 2/0 live_review.md, 10/12 plan.md.

C3 — THE PRODUCT: copy scrubSnapshots.ts into `apps/ui/src/components/timeline/`, then `git add`
  it — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F024 R2 C3: add the scrubber's snapshot memo`
  Expected insertions: 147 scrubSnapshots.ts.

C4 — THE TESTS: copy scrubSnapshots.test.ts into `apps/ui/src/components/timeline/` and
  test_scrub_snapshots.py into `tests/ui_contracts/`, and `git add` both.
  Subject: `F024 R2 C4: hold the memo to a fresh fold at fuzzed positions, and guard its spacing`
  Expected insertions: 236 scrubSnapshots.test.ts, 57 test_scrub_snapshots.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F024 R2 C5: rewrite handoff for round 2`
  Then `git push origin feature/f024-phase-timeline-scrubber`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f024-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the two files under
   `apps/ui/src/components/timeline/` that the payloads name,
   `tests/ui_contracts/test_scrub_snapshots.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 78d60af2 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `docs/roadmap/STATUS.md`, `README.md`,
   `apps/ui/src/components/timeline/phaseMapping.ts` or `docs/roadmap/features/T5_F024.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f024-r2-sim`, `.remedy-wt/f024-r2-dry`, the round 1 ones
   and the older `f015-*`, `f020-*`, `f023-*` and `f284-*` ones), and every existing stash alone.
   The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F024's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f024-r2-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f024-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 299296 | a4ac18dee4af1177cd028bef5665e702c280e92482ee6d0cad9c390e464d69f9 |
 | .agent/decisions.md | 2080562 | 64fa6f4fb7a71774eed6e6e9598025be9536e5300d439616ac4ebba2f84a2aa1 |
 | .agent/plan.md | 1321 | 6d461d078ff4f572e5bf010d67ed205159f776f38c7a6d914ca73f39393d606b |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `78d60af2` and at C2 (the reviewer
 read R-1008 alone at both); the lines C2's diff ADDS to `.agent/live_review.md`, of which the
 reviewer read 2, exactly one beginning `Gate: F024 R1 — `; the ledger's last line at C2, which
 must begin `Gate: F024 R1 — `; and `git diff --name-only <C1d> <C2>`, which must name exactly
 the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/timeline/scrubSnapshots.ts | 5533 | c898fd7562f7a0c4fd40ee2184ca117d0c24bb0254818b0ad422dfa6f41266d2 |
 | C4 | apps/ui/src/components/timeline/scrubSnapshots.test.ts | 10046 | 8a3f62dd6940956564f45402365396abe0dd03390f908dcf1b54e408844511ae |
 | C4 | tests/ui_contracts/test_scrub_snapshots.py | 2884 | 0a6fab2256c80ca618e244ef598c8b0235c5d765ff1b2ae854fd9d8b3f1bb6ff |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_scrub_snapshots.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1456 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new test file. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f024-r2-mut <C4>`, then
 `python3 -B .remedy-wt/f024-r2-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f024-r2-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `scrubSnapshots.test.ts` from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f024-r2-mutscratch/`, and pytest over the
 worktree's guard; it asserts each FROM occurs exactly once, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first vitest 14 passed and guard 4 passed, both at exit 0;
 m1 (the boundary rounds down one seq early) v3 g0;
 m2 (a snapshot also holds the row at its boundary) v7 g0;
 m3 (the ledger is kept in arrival order) v4 g0;
 m4 (a gap-filling row leaves the snapshots above it) v2 g0;
 m5 (a row at the head drops every snapshot) v3 g0;
 m6 (a reset keeps the old snapshots) v1 g0;
 m7 (the cap drops the nearest snapshot) v2 g0;
 m8 (a tie drops the higher snapshot) v1 g0;
 m9 (the cap is never enforced) v3 g0;
 m10 (a missing snapshot is always rebuilt from the seed) v1 g0;
 m11 (the memo seeds with today's statuses) v8 g1;
 m12 (the spacing drifts from the spec) v2 g1;
 m13 (the memo reaches for the wall clock) v0 g1;
 m14 (every position folds from the seed) v6 g0;
 m15 (a position also folds the row after it) v7 g0;
 control last as first;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f024-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `78d60af2` in
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
section reads SESSION 1 of feature F024, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T003 — the bar reading the phase mapping and the memo, the scrubber with its
keyboard, the LIVE toggle with the SCRUBBED banner and the capped catch-up, and the end-to-end
on a live fake job and the demo recording. State the open-findings count, 1, and the
operator-questions count, 3.
