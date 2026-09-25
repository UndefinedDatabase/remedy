STEP F024 R1 — CLAIM F024 AND LAND T001: the phase mapping table, the phase boundaries of any prefix, the sub-glyph extraction, their goldens and guard

GOAL
Pull request 278 is merged; `main` is at `1bb3a35d` and F024 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F023's round 10 verdict, record DECISION
F024 D1, and land T001: `apps/ui/src/components/timeline/phaseMapping.ts`, the pure reading of
the event ledger — the phase mapping table over the measured writers, the phase boundaries of any
prefix, and the sub-glyph extraction with humanized lines; its vitest goldens on fixture ledgers
and the demo recording; and the guard `tests/ui_contracts/test_phase_mapping.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f024-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f024-r1/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f024-r1-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f024-r1-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f024-r1-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `1bb3a35d`. Report all three. Then
   `git checkout -b feature/f024-phase-timeline-scrubber` and report the branch. Do NOT pull:
   the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f024-r1/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f024-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 147 | 16701 | ad11fd63156c57b0d46392fbf27431e94bcff84b0451f57c8104542650a0d154 |
| context.md | 37 | 1625 | d6eba45432667408969eefe383de52fe9f53c7bee13a3025e0bffd3cc26ce491 |
| mutations.py | 170 | 8314 | 91cec40171bd9ae07e2d3242e8a69c83c58e0c708e0b10605804b93554583c46 |
| phaseMapping.test.ts | 325 | 12392 | 2cd5f7b9a0931112f5389b12dcd958f8a352080bb857bd3be37798bb3ea41b3c |
| phaseMapping.ts | 213 | 8581 | ae226e2e5386c29a163a2a7b3ea66108a97cba80a36c7df9e0359d0bafa7a27e |
| plan.md | 36 | 1448 | 32b86e0315f74236cd404c7b039d52fee983191377c4c558101df1b2cb7186cf |
| test_phase_mapping.py | 70 | 3525 | ce219529777be40b23e506b221debcefbf427b149b658ae3ff885e81a8f97de7 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`phaseMapping.ts` becomes a NEW FILE at `apps/ui/src/components/timeline/phaseMapping.ts`,
`phaseMapping.test.ts` a NEW FILE at `apps/ui/src/components/timeline/phaseMapping.test.ts`, and
`test_phase_mapping.py` a NEW FILE at `tests/ui_contracts/test_phase_mapping.py`, each copied
whole. `claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a
tree at `1bb3a35d` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head,
which replaces everything above the `## Findings` heading line, then F023's round 10 gate entry
appended), `docs/roadmap/STATUS.md` (F024's line `[ ]` to `[~]`) and `.agent/decisions.md`
(DECISION F024 D1 appended). `mutations.py` is a TOOL for G5: it is run, never applied to a
tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f024-r1-block.md` := this block, and `.agent/authored/f024-r1-plan.md` and
  `.agent/authored/f024-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F024 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 73. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f024-r1-claim.diff` := claim.diff.
  Subject: `F024 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 147.

C1c — copy the mutation tool
  `.agent/authored/f024-r1-mutations.py` := mutations.py.
  Subject: `F024 R1 C1c: copy round 1 mutation tool into .agent/authored/`
  Expected insertions: 170.

C1d — copy the product payload
  `.agent/authored/f024-r1-phaseMapping.ts` := phaseMapping.ts.
  Subject: `F024 R1 C1d: copy round 1 product module into .agent/authored/`
  Expected insertions: 213.

C1e — copy the test payloads
  `.agent/authored/f024-r1-phaseMapping.test.ts` and
  `.agent/authored/f024-r1-test_phase_mapping.py`.
  Subject: `F024 R1 C1e: copy round 1 test payloads into .agent/authored/`
  Expected insertions: 395.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F024 R1 C2: claim F024, re-head the live review record, book F023 R10, record D1`
  Expected by `git show --numstat` (insertions and deletions): 13/15 context.md, 59/0 decisions.md, 25/26 live_review.md, 23/15 plan.md, 1/1 STATUS.md.

C3 — THE PRODUCT: copy phaseMapping.ts into `apps/ui/src/components/timeline/`, then `git add`
  it — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F024 R1 C3: add the phase mapping, its boundaries and the sub-glyph extraction`
  Expected insertions: 213 phaseMapping.ts.

C4 — THE TESTS: copy phaseMapping.test.ts into `apps/ui/src/components/timeline/` and
  test_phase_mapping.py into `tests/ui_contracts/`, and `git add` both.
  Subject: `F024 R1 C4: golden the phase boundaries and sub-glyphs, and guard the table`
  Expected insertions: 325 phaseMapping.test.ts, 70 test_phase_mapping.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F024 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f024-phase-timeline-scrubber`. Do NOT create a pull request:
  the branch opens one at F024's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f024-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, the two files under `apps/ui/src/components/timeline/` that the payloads
   name, `tests/ui_contracts/test_phase_mapping.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 1bb3a35d HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `apps/ui/src/components/timeline/PhaseTimeline.tsx` or `docs/roadmap/features/T5_F024.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f024-r1-sim`, `.remedy-wt/f024-r1-dry` and the older
   `f015-*`, `f020-*`, `f023-*` and `f284-*` ones), and every existing stash alone. The worktree
   G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F024's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f024-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f024-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 297529 | 1b4e6e5c04f9e091f70f5040af1a665341e6926da9e3d7cbafaf70020fef892c |
 | docs/roadmap/STATUS.md | 51749 | 11008e7e63e83fff26f4328cff82b3a7a672677ba6ca08b0b20579bb73f107ee |
 | .agent/decisions.md | 2076619 | 908506bfeeada0f41cd8dc9a0584906ce095762513b9fa734817d774052823d0 |
 | .agent/plan.md | 1448 | 32b86e0315f74236cd404c7b039d52fee983191377c4c558101df1b2cb7186cf |
 | .agent/context.md | 1625 | d6eba45432667408969eefe383de52fe9f53c7bee13a3025e0bffd3cc26ce491 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `1bb3a35d` and at C2 (the reviewer
 read R-1008 alone at both); at C2 the ledger has exactly one line reading `## Findings` and
 exactly one reading `## Steps`, and its last line begins `Gate: F023 R10 — `; F024's STATUS
 line at C2 read back in full, which must read `- [~] F024 — Phase timeline with scrubber`; and
 `git diff --name-only <C1e> <C2>`, which must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/timeline/phaseMapping.ts | 8581 | ae226e2e5386c29a163a2a7b3ea66108a97cba80a36c7df9e0359d0bafa7a27e |
 | C4 | apps/ui/src/components/timeline/phaseMapping.test.ts | 12392 | 2cd5f7b9a0931112f5389b12dcd958f8a352080bb857bd3be37798bb3ea41b3c |
 | C4 | tests/ui_contracts/test_phase_mapping.py | 3525 | ce219529777be40b23e506b221debcefbf427b149b658ae3ff885e81a8f97de7 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_phase_mapping.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1499 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new test file. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f024-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f024-r1-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f024-r1-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `phaseMapping.test.ts` from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f024-r1-mutscratch/`, and pytest over the
 worktree's guard; it asserts each FROM occurs exactly once, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first vitest 24 passed and guard 4 passed, both at exit 0;
 m1 (planning_started marks Build) v2 g0;
 m2 (a round with no reviewer marks Review) v1 g0;
 m3 (a skipped phase gets no start) v7 g0;
 m4 (Finalized is sticky) v1 g0;
 m5 (the seed keeps today's statuses) v2 g0;
 m6 (Finalized ignores a later marker) v1 g0;
 m7 (a pass heals another task's failure) v1 g0;
 m8 (one failure heals twice) v1 g0;
 m9 (a repeated seq keeps the last row) v2 g0;
 m10 (a prototype-named kind resolves as a marker) v1 g0;
 m11 (the hover shows the raw kind) v3 g0;
 m12 (the table names a kind nothing writes) v1 g1;
 m13 (a kind marks Job) v1 g1;
 m14 (the mapping reaches for the wall clock) v0 g1;
 m15 (the bar's phase order drifts from the mapping) v0 g1;
 control last as first;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f024-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `1bb3a35d` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F024, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — snapshot memoization every 200 seq with its memory cap and lazy rebuild,
and the property test that the state at any fuzzed position equals a fresh reduction of that
prefix. State the open-findings count, 1, and the operator-questions count, 3.
