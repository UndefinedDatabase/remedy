STEP F024 R4 — T003's components: one ledger and one scrubber in the shell, the bar as a slider, the stage drawing the scrubbed prefix under a SCRUBBED banner, the REPLAY pill and LIVE's fast-forward, with round 3's PASS and DECISION F024 D4 booked

GOAL
Book round 3's PASS, record DECISION F024 D4, and land T003's components: the track's geometry in
`timelineView.ts` with its tests; `useTimelineScrub.ts`, the hook that binds the index, the memo,
the machine and the view to React and owns LIVE's timers; the shell reading the one ledger and
building the one scrubber; `PhaseTimeline.tsx` rebuilt as a slider over six segments with
sub-glyphs, a readout and a LIVE button; the stage drawing the scrubbed prefix under a SCRUBBED
banner; the REPLAY pill; four `assumption_log.md` rows; the re-pointed ledger guard; and the new
guard `tests/ui_contracts/test_timeline_scrub_wiring.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f024-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f024-r4/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f024-r4-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f024-r4-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f024-r4-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f024-phase-timeline-scrubber`, and `git log --oneline -1` must read `b1cfedbe`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f024-r4/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f024-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| bar.diff | 412 | 16594 | 57d409a465b23e915620e58bad33ddbf0c21cdf7179b527d23df1a89f012488e |
| core.diff | 45 | 2309 | 34a868acd4041c3f562cca3ffc0ea83ac821d89c72c481193b0edc4c95dfd19e |
| ledger.diff | 68 | 10394 | 37c9cd4481b2cbf8afaa87542c4898114f1ea22b0c0a95d77b7dad191ea7419e |
| mutations.py | 178 | 8993 | 3c533e5e2d4d84a61c08a17537624d55f13e86589d15cc32af78a0481dfa46d4 |
| plan.md | 34 | 1323 | adf2c4f3ba691c5667d8863b9499af3844a020161be9b376015df7e04089fd51 |
| stage.diff | 296 | 21511 | 7ebba206f52bbbecb6d9e0f1ac5829d5b0013e64003d31998505d72d27a1d924 |
| test_timeline_scrub_wiring.py | 88 | 4373 | fa91fb8710a41ab3183985d4e0a997bb85f115c3df5a88d79dd2948f8db00440 |
| tests.diff | 53 | 2638 | ba1cb8853459d53d9f9968e52fad70a4dac2a7e6b727cd27b48bb70673ec5144 |
| useTimelineScrub.ts | 130 | 5356 | 1dec86a4c9f4f0d97752c601affeebab1037a3f920adf023c9bcb00a5a39fc24 |

`plan.md` is a REWRITE of `.agent/plan.md`. `useTimelineScrub.ts` becomes a NEW FILE at
`apps/ui/src/components/timeline/useTimelineScrub.ts` and `test_timeline_scrub_wiring.py` a NEW
FILE at `tests/ui_contracts/test_timeline_scrub_wiring.py`, each copied whole. The five `.diff`
payloads go on with `git apply`; the reviewer generated each with `git diff HEAD` from a tree at
`b1cfedbe` into which it wrote the edits. `ledger.diff` appends round 3's gate entry to
`.agent/live_review.md` and DECISION F024 D4 to `.agent/decisions.md`; `core.diff` adds the two
geometry functions to `apps/ui/src/components/timeline/timelineView.ts`; `bar.diff` edits
`apps/ui/src/components/timeline/PhaseTimeline.tsx` and its `.module.css`; `stage.diff` edits
`BrainGraphStage.tsx` and its `.module.css`, `RemedyShell.tsx`, `LiveStatusPill.tsx`,
`RightLivePanel.tsx` and its `.module.css`, `docs/ui/design_reference/assumption_log.md` and
`tests/ui_contracts/test_brain_live_wiring.py`; `tests.diff` edits
`apps/ui/src/components/timeline/timelineView.test.ts`. `mutations.py` is a TOOL for G5: it is
run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f024-r4-block.md` := this block, and `.agent/authored/f024-r4-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F024 R4 C1a: copy round 4 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 34. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the ledger diff and the mutation tool
  `.agent/authored/f024-r4-ledger.diff` and `.agent/authored/f024-r4-mutations.py`.
  Subject: `F024 R4 C1b: copy round 4 ledger diff and mutation tool into .agent/authored/`
  Expected insertions: 246.

C1c — copy the geometry, hook and test payloads
  `.agent/authored/f024-r4-core.diff`, `.agent/authored/f024-r4-useTimelineScrub.ts`,
  `.agent/authored/f024-r4-tests.diff` and `.agent/authored/f024-r4-test_timeline_scrub_wiring.py`.
  Subject: `F024 R4 C1c: copy round 4 geometry, hook and test payloads into .agent/authored/`
  Expected insertions: 316.

C1d — copy the bar diff
  `.agent/authored/f024-r4-bar.diff`.
  Subject: `F024 R4 C1d: copy round 4 bar diff into .agent/authored/`
  Expected insertions: 412.

C1e — copy the stage diff
  `.agent/authored/f024-r4-stage.diff`.
  Subject: `F024 R4 C1e: copy round 4 stage diff into .agent/authored/`
  Expected insertions: 296.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F024 R4 C2: book round 3's PASS, record D4, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 50/0 decisions.md, 2/0 live_review.md, 10/11 plan.md.

C3 — THE GEOMETRY AND THE HOOK: `git apply` core.diff, copy useTimelineScrub.ts into
  `apps/ui/src/components/timeline/`, and `git add` it — an untracked module fails
  `integrity check`'s `relevant_untracked`.
  Subject: `F024 R4 C3: add the track's geometry and the scrubber hook`
  Expected insertions: 34 timelineView.ts, 130 useTimelineScrub.ts.

C4 — THE WIRING: `git apply` bar.diff, then `git apply` stage.diff.
  Subject: `F024 R4 C4: wire one ledger and one scrubber through the shell, the bar, the stage and the pill`
  Expected by `git show --numstat` (insertions and deletions): 40/0 BrainGraphStage.module.css, 19/12 BrainGraphStage.tsx, 7/1 LiveStatusPill.tsx, 2/0 RightLivePanel.module.css, 2/2 RightLivePanel.tsx, 12/3 RemedyShell.tsx, 61/3 PhaseTimeline.module.css, 134/116 PhaseTimeline.tsx, 4/0 assumption_log.md, 25/15 test_brain_live_wiring.py.

C5 — THE TESTS: `git apply` tests.diff, copy test_timeline_scrub_wiring.py into
  `tests/ui_contracts/`, and `git add` it.
  Subject: `F024 R4 C5: test the track's geometry and guard the scrubber's wiring`
  Expected insertions: 34 timelineView.test.ts, 88 test_timeline_scrub_wiring.py.

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F024 R4 C6: rewrite handoff for round 4`
  Then `git push origin feature/f024-phase-timeline-scrubber`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before every real
   `git apply` and report each exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f024-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, every path the G3 table
   names, and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only b1cfedbe HEAD` after C6. Do NOT touch `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `.agent/context.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `packages/orchestration/ui_server.py` or
   `docs/roadmap/features/T5_F024.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f024-r4-sim`, `.remedy-wt/f024-r4-dry`, the rounds 1 to 3
   ones and the older `f015-*`, `f020-*`, `f023-*` and `f284-*` ones), and every existing stash
   alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action,
   and `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F024's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f024-r4-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f024-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 302833 | ea93400e6b4317f1a6b60cea1007f5bb5037c0253ae865a6d066294fe4469640 |
 | .agent/decisions.md | 2089317 | 1f8a8b624aebf10c7d5ba08260afd24b920a6530d971ea768350046faa5fc383 |
 | .agent/plan.md | 1323 | adf2c4f3ba691c5667d8863b9499af3844a020161be9b376015df7e04089fd51 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `b1cfedbe` and at C2 (the reviewer
 read R-1008 alone at both); the lines C2's diff ADDS to `.agent/live_review.md`, of which the
 reviewer read 2, exactly one beginning `Gate: F024 R3 — `; the ledger's last line at C2, which
 must begin `Gate: F024 R3 — `; and `git diff --name-only <C1e> <C2>`, which must name exactly
 the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/timeline/timelineView.ts | 6548 | 6d3eebc9d04bcd9f0e524dbbd287afc3a8747abfe34c1869d0f5b9238683c7ee |
 | C3 | apps/ui/src/components/timeline/useTimelineScrub.ts | 5356 | 1dec86a4c9f4f0d97752c601affeebab1037a3f920adf023c9bcb00a5a39fc24 |
 | C4 | apps/ui/src/components/timeline/PhaseTimeline.tsx | 6834 | a0f59da3587fd6c5927259bde15db031a108f1443d7bd86a8f3ca5492af69a47 |
 | C4 | apps/ui/src/components/timeline/PhaseTimeline.module.css | 5156 | 644175840fc0b6225ab9a8893a0b2f3fa08bb13acd32caddf93c55a16d707fd3 |
 | C4 | apps/ui/src/components/graph/BrainGraphStage.tsx | 7146 | a54fed2dba3ebc4697f59e8c9fddddcb649dd9b9ca6659fc9230a50484b6cb95 |
 | C4 | apps/ui/src/components/graph/BrainGraphStage.module.css | 2214 | 713b54b8d390129475d665d15890813ebeb4e342b09753d08d7206dc47b309a7 |
 | C4 | apps/ui/src/components/shell/RemedyShell.tsx | 13750 | a34f41c9063ed6bdf17de8b3cf1b2933806c3cf273644ebba37baccd65a810fe |
 | C4 | apps/ui/src/components/panels/LiveStatusPill.tsx | 1926 | ef3771a4ca1fc13fda5ce3b2cb56afefc06825c5ab222192a4e40a89410b32cf |
 | C4 | apps/ui/src/components/panels/RightLivePanel.tsx | 3336 | abe6b75477b565a29c175adfe2136f3cee08cb2ebd0ad887583cf61d5445119b |
 | C4 | apps/ui/src/components/panels/RightLivePanel.module.css | 25342 | fc1dc0a06ac67ec5411c3bc396aff086d67f70a25c9393a71de8ee82b0a13580 |
 | C4 | docs/ui/design_reference/assumption_log.md | 10804 | aea0081e6e841abc2f52a0bc04fbfacec7b8e1c954093c6e6fc66a993938d1d4 |
 | C4 | tests/ui_contracts/test_brain_live_wiring.py | 5433 | 8e70f3a9b1c93a0d11d901f9156aa17c2fbb7958820c25e0c5089658b6043288 |
 | C5 | apps/ui/src/components/timeline/timelineView.test.ts | 7587 | b165c56468c37b9ae799c7d2f1000282d07ae059f5544bdbdb3084a9ae759888 |
 | C5 | tests/ui_contracts/test_timeline_scrub_wiring.py | 4373 | fa91fb8710a41ab3183985d4e0a997bb85f115c3df5a88d79dd2948f8db00440 |
 Also `git diff --name-only` between C2 and C3, C3 and C4, and C4 and C5, each of which must name
 exactly the paths the table gives that commit; and `python3 -m ruff check
 tests/ui_contracts/test_timeline_scrub_wiring.py tests/ui_contracts/test_brain_live_wiring.py`
 at C5.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C5 with this block's copy, and read `1465 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings over the whole UI source, the new hook's React rules included), the typescript
 node in `tests/ui_server/test_dashboard_contract.py` (`tsc --noEmit` over the rewired shell,
 stage, bar and pill) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite. Report every `SKIPPED` line the `-rs` summary prints. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f024-r4-mut <C5>`, then
 `python3 -B .remedy-wt/f024-r4-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f024-r4-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `timelineView.test.ts` from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f024-r4-mutscratch/`, and pytest over the
 worktree's whole `tests/ui_contracts` directory; it asserts each FROM occurs exactly once,
 restores the bytes, and runs an unmutated control first and last. The reviewer read, over the
 same tool against its sim tree (v = vitest failed, g = contract tests failed, each red at exit 1
 wherever its count is not 0):
 control first vitest 12 passed and contract tests 924 passed, both at exit 0;
 m1 (the handle sits at the start of its event's slot) v3 g0;
 m2 (a segment does not own its right edge) v1 g0;
 m3 (a point in an unreached phase goes before the first event) v1 g0;
 m4 (the stage draws the live model while scrubbed) v0 g1;
 m5 (the banner is not announced) v0 g1;
 m6 (the slider ignores the keyboard) v0 g1;
 m7 (a glyph click lands one event late) v0 g1;
 m8 (the LIVE button hides its state) v0 g1;
 m9 (the bar keeps a timer) v0 g1;
 m10 (the bar's phase order drifts) v0 g2;
 m11 (the stage gets a scrubber without its model) v0 g1;
 m12 (the pill says nothing about the replay) v0 g1;
 m13 (the transport outranks the replay) v0 g1;
 m14 (the banner paints a raw colour) v0 g1;
 m15 (an overflowing LIVE replays instead of rebuilding) v0 g1;
 m16 (LIVE skips the fast-forward) v0 g1;
 control last as first;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f024-r4-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 11`, which must show C6, C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `b1cfedbe` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F024, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003's end-to-end — a live fake job scrubbed to every position against a fresh
fold, the demo recording as a scrubbable story, and the scrub budget on the 500-node fixture with
its snapshot arithmetic. State the open-findings count, 1, and the operator-questions count, 3.
