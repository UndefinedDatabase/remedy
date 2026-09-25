STEP F023 R5 — T003 FIRST PART: the L3 evidence panel, its lazy tabs, and the zoom surfaces on layer tokens

GOAL
Book round 4's PASS, record DECISION F023 D5, and land the L3 evidence panel: `EvidencePanel.tsx`
with T5_F023.md's binding CSS, whose raw shadow becomes the token `--remedy-shadow-panel`; its
tabs from `evidencePanel.ts`, only the open one loading; the run detail's Open diff and Why
re-pointed at the panel's tabs; `--remedy-dur-base` and three `--remedy-z-*` layers transcribed
into the app sheet, with the breadcrumbs and the run detail moved onto them; two rows of
`assumption_log.md`; the vitest goldens, the guard `tests/ui_contracts/test_evidence_panel_contract.py`
and the updated `test_run_detail_wiring.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f023-r5/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r5-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f023-r5-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f023-r5-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `08955162`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r5/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| EvidencePanel.module.css | 94 | 2229 | 2b3809057a94cb1306238240c27e049347e0001496ef20e61c3c34e6efe04aa0 |
| EvidencePanel.tsx | 100 | 4534 | 840048b2d56e3d84a7b5c5ec05bfe682566dcb9faac691791c4623022d0ad076 |
| evidencePanel.test.ts | 51 | 2114 | 59bb66c45e47d8f907fc7c83893e3a48a7c2ba12a2ff3c00b0f24e49ddf035d6 |
| evidencePanel.ts | 27 | 1499 | c8b6c24d221c917b42974942c2386dbc40c12e296087b97716323ad2091190a1 |
| ledger.diff | 67 | 10586 | ec5b4c8ea90f81b64e2bc58c7a0e6d94102214bdffa0f21166f6dc15c4179b1b |
| mutations.py | 180 | 8869 | b7a5d91a160cec5065a3293e59ae1c03b939ab933bd8efa18cea99efbcf82844 |
| plan.md | 35 | 1328 | 4ecf52754521e2d2d582372c80078a5ece01b2041fd9a32154a04faf05ce9202 |
| product.diff | 205 | 11102 | 4d63a3e91f668cb26ecffd67deed3c0e7f419e4c4c1c7cd13d36799428dffdce |
| test_evidence_panel_contract.py | 105 | 5170 | 9a8a79fe545a4a9853575d2a677d95d3009b5ff43f006d0d5d393ab36eafe5cd |
| tokens.diff | 56 | 5624 | 336fa418a5ca5eef859370ff9a039a12ec9441f6e1f075fa446706ae30b67f27 |

`plan.md` is a REWRITE of `.agent/plan.md`. Each of the five others is copied whole:
`EvidencePanel.tsx` is a NEW FILE at `apps/ui/src/components/graph/EvidencePanel.tsx`,
`EvidencePanel.module.css` a NEW FILE at `apps/ui/src/components/graph/EvidencePanel.module.css`,
`evidencePanel.ts` a NEW FILE at `apps/ui/src/components/graph/evidencePanel.ts`,
`evidencePanel.test.ts` a NEW FILE at `apps/ui/src/components/graph/evidencePanel.test.ts`, and
`test_evidence_panel_contract.py` a NEW FILE at `tests/ui_contracts/test_evidence_panel_contract.py`.
The three diffs go on with `git apply`; the reviewer generated each with `git diff HEAD` from a
tree at `08955162` into which it wrote the edits. `ledger.diff` appends round 4's gate entry to
`.agent/live_review.md` and DECISION F023 D5 to `.agent/decisions.md`. `tokens.diff` edits
`apps/ui/src/styles/tokens.css`, `docs/ui/design_reference/tokens.css`,
`docs/ui/design_reference/tokens_rules.md` and `docs/ui/design_reference/assumption_log.md`.
`product.diff` edits `apps/ui/src/components/graph/BrainGraphStage.tsx`, `RunDetailPopover.tsx`,
`RunDetailPopover.module.css`, `ZoomBreadcrumbs.module.css`,
`apps/ui/src/components/shell/RemedyShell.tsx` and `tests/ui_contracts/test_run_detail_wiring.py`,
whose update must land with the product change it follows or that commit is red. `mutations.py`
is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f023-r5-block.md` := this block, and `.agent/authored/f023-r5-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F023 R5 C1a: copy round 5 block and plan payload into .agent/authored/`
  Expected insertions: 298. Report the number you measure and STOP rather than commit if it is
  500 or more.

C1b — copy the three diffs
  `.agent/authored/f023-r5-ledger.diff`, `-tokens.diff` and `-product.diff`, each prefixed
  `f023-r5-` like the others.
  Subject: `F023 R5 C1b: copy round 5 ledger, token and product diffs into .agent/authored/`
  Expected insertions: 328.

C1c — copy the mutation tool
  `.agent/authored/f023-r5-mutations.py` := mutations.py.
  Subject: `F023 R5 C1c: copy round 5 mutation tool into .agent/authored/`
  Expected insertions: 180.

C1d — copy the product payloads
  `.agent/authored/f023-r5-EvidencePanel.tsx`, `-EvidencePanel.module.css` and
  `-evidencePanel.ts`, each prefixed `f023-r5-` like the others.
  Subject: `F023 R5 C1d: copy round 5 product modules into .agent/authored/`
  Expected insertions: 221.

C1e — copy the test payloads
  `.agent/authored/f023-r5-evidencePanel.test.ts` and
  `.agent/authored/f023-r5-test_evidence_panel_contract.py`.
  Subject: `F023 R5 C1e: copy round 5 test payloads into .agent/authored/`
  Expected insertions: 156.

C2 — THE RECORDS, in this order: `git apply` ledger.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F023 R5 C2: book round 4's PASS, record D5, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 49/0 decisions.md, 2/0 live_review.md, 12/13 plan.md.

C3 — THE PRODUCT: `git apply` tokens.diff, then `git apply` product.diff, then copy
  EvidencePanel.tsx, EvidencePanel.module.css and evidencePanel.ts into
  `apps/ui/src/components/graph/`, then `git add` all three — an untracked module fails
  `integrity check`'s `relevant_untracked`.
  Subject: `F023 R5 C3: open the L3 evidence panel with its lazy tabs on layer tokens`
  Expected by `git show --numstat`: 17/7 BrainGraphStage.tsx, 94/0 EvidencePanel.module.css, 100/0 EvidencePanel.tsx, 1/1 RunDetailPopover.module.css, 7/6 RunDetailPopover.tsx, 1/1 ZoomBreadcrumbs.module.css, 27/0 evidencePanel.ts, 1/1 RemedyShell.tsx, 9/0 tokens.css, 2/0 assumption_log.md, 1/0 tokens.css, 3/0 tokens_rules.md, 9/8 test_run_detail_wiring.py.

C4 — THE TESTS: copy evidencePanel.test.ts into `apps/ui/src/components/graph/` and
  test_evidence_panel_contract.py into `tests/ui_contracts/`, and `git add` both.
  Subject: `F023 R5 C4: golden the evidence tabs and pin the panel's binding CSS`
  Expected by `git show --numstat`: 51/0 evidencePanel.test.ts, 105/0 test_evidence_panel_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F023 R5 C5: rewrite handoff for round 5`
  Then `git push origin feature/f023-semantic-zoom-l0-l3`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f023-r5-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the four paths
   `tokens.diff` edits, the six paths `product.diff` edits, the five new files the payloads name,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only 08955162 HEAD`
   after C5. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `README.md`, `docs/roadmap/**`,
   `apps/ui/src/api/**` or `packages/**`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported
   afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F023's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r5-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f023-r5/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 303052 | 81b99e003ec27f6bd4bfe185b7561951200d88e205bc23d8d4aa12a699b1ed46 |
 | .agent/decisions.md | 2064050 | d0db445b0605efc2a90ea347593f7119a4c9d7890d79b3667de058e417c83cea |
 | .agent/plan.md | 1328 | 4ecf52754521e2d2d582372c80078a5ece01b2041fd9a32154a04faf05ce9202 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `08955162` and at C2 (the reviewer
 read R-1008 alone at both); the ledger's last line at C2 begins `Gate: F023 R4 — `; and
 `git diff --name-only <C1e> <C2>`, which must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/styles/tokens.css | 4700 | b463648fd15e07dcde5306f65f2c990610955007417dd709609e3bf4ada84dd8 |
 | C3 | docs/ui/design_reference/tokens.css | 7204 | 1bfb11676af28a88895634cb211764f567c03de09c0948f6531ad60307a2879d |
 | C3 | docs/ui/design_reference/tokens_rules.md | 3370 | d7c84e9ce10888b73ff8eab8507b5f8d63ca759af764c5ddce5868661a57cdb7 |
 | C3 | docs/ui/design_reference/assumption_log.md | 7911 | 3804e907b81aff1bcce8a453faf6d057e2312db806b5eb465c15b57f801c603c |
 | C3 | apps/ui/src/components/graph/BrainGraphStage.tsx | 6024 | c82c5e7595658df8afbbf91bdddef5f06c2b4eb000d5bef27fe4c2e13d409a5e |
 | C3 | apps/ui/src/components/graph/RunDetailPopover.tsx | 4177 | 7b45b4706762354a54f30408573738e09cd630300e265aa899c33b171d02e59b |
 | C3 | apps/ui/src/components/graph/RunDetailPopover.module.css | 2030 | ee91b49fd3d29a5e7e8557c0349e643d65e2965c6c78b4b0bdf29c7c748cf30d |
 | C3 | apps/ui/src/components/graph/ZoomBreadcrumbs.module.css | 1098 | 4ba2f562425573c267b7cee23bda67651ca88798a6d92422385d5ca4cb012000 |
 | C3 | apps/ui/src/components/shell/RemedyShell.tsx | 13139 | 0718c42f7cdf8f27417d1d245e1050f6c7ae36102667b1b2ba74dc54c9a35b7a |
 | C3 | tests/ui_contracts/test_run_detail_wiring.py | 3550 | 8884b83f5c94a801f11a5bf8b2d1807cd106a7cde73e2a505b711ea56e8358be |
 | C3 | apps/ui/src/components/graph/EvidencePanel.tsx | 4534 | 840048b2d56e3d84a7b5c5ec05bfe682566dcb9faac691791c4623022d0ad076 |
 | C3 | apps/ui/src/components/graph/EvidencePanel.module.css | 2229 | 2b3809057a94cb1306238240c27e049347e0001496ef20e61c3c34e6efe04aa0 |
 | C3 | apps/ui/src/components/graph/evidencePanel.ts | 1499 | c8b6c24d221c917b42974942c2386dbc40c12e296087b97716323ad2091190a1 |
 | C4 | apps/ui/src/components/graph/evidencePanel.test.ts | 2114 | 59bb66c45e47d8f907fc7c83893e3a48a7c2ba12a2ff3c00b0f24e49ddf035d6 |
 | C4 | tests/ui_contracts/test_evidence_panel_contract.py | 5170 | 9a8a79fe545a4a9853575d2a677d95d3009b5ff43f006d0d5d393ab36eafe5cd |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_evidence_panel_contract.py
 tests/ui_contracts/test_run_detail_wiring.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1473 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new test file. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f023-r5-mut <C4>`, then
 `python3 -B .remedy-wt/f023-r5-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f023-r5-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `evidencePanel.test.ts` from the primary
 `apps/ui`
 with a scratch config under `.remedy-wt/f023-r5-mutscratch/`, and pytest over the worktree's
 two guards; it asserts each FROM occurs exactly once, restores the bytes, and runs an unmutated
 control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first: vitest 4 passed at exit 0, guard 12 passed at exit 0;
 m1 (the tabs lose the feature's order) v1 g0;
 m2 (the trace lists every task's prompts) v2 g0;
 m3 (the reviewer's prompt is listed before the builder's) v1 g0;
 m4 (the panel's shadow is a raw colour again) v0 g1;
 m5 (the panel's layer is a number) v0 g2;
 m6 (reduced motion still slides the panel in) v0 g1;
 m7 (the diff loads whichever tab is open) v0 g1;
 m8 (a diff read for another task is shown) v0 g1;
 m9 (the panel becomes a dialog Escape skips) v0 g1;
 m10 (the panel opens at L2) v0 g1;
 m11 (the run detail stays open at L3) v0 g2;
 m12 (Open diff opens the prompt tab) v0 g1;
 m13 (the app sheet's slide duration drifts from the reference) v0 g1;
 m14 (the reference's panel shadow drifts from the app sheet) v0 g1;
 m15 (the breadcrumbs' layer is a number again) v0 g1;
 control last: vitest 4 passed at exit 0, guard 12 passed at exit 0;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f023-r5-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `08955162` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F023, round 5, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then T003's second part — deep links that restore the zoom state, and cluster expansion
at the focused task with focus following into it. State the open-findings count, 1, and the
operator-questions count, 3.
