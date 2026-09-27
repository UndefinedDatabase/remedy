STEP F028 R7 — BOOK ROUND 6, RECORD D7 AND ITS TWO ASSUMPTION-LOG ROWS, AND LAND THE "+ Add Task" ROW WITH ITS DRAFT-AND-CONFIRM SHEET IN PLACE OF THE PROPOSE BUTTON, AND THE CANVAS CHIP

GOAL
Round 6 passed. Book its gate entry and record DECISION F028 D7 with its two assumption-log rows.
Then make the Add Task button real: the tasks card's "+ Add Task" row replaces the button that
copied a retired command and opens a sheet that drafts a task from the operator's words, shows the
draft as sentences, confirms or discards it, and answers a cost shortfall; and an injected task's
node on the canvas carries the chip "added".

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests against S1 to S5. Read DECISION F028 D7 (it arrives with C2),
`docs/ui/design_reference/ux_spec.md` §8, §11 and §14, `tokens_rules.md`, and whole:
`apps/ui/src/components/panels/TaskChecklistCard.tsx`, `RightLivePanel.tsx`, the overlay
`apps/ui/src/components/**/LessonsOverlay.tsx` with its style sheet,
`apps/ui/src/components/detail/TaskVetoForm.tsx`, `apps/ui/src/api/injectView.ts`,
`apps/ui/src/api/injectSend.ts`, and the `specVersion` thread through
`apps/ui/src/components/graph/brainView.ts`, `brainOntology.ts`, `brainReducer.ts` and
`buildForceBrainModel.ts` with their tests.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r7/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/` to `.remedy-wt/f028-r7-sim/`  The reviewer's simulation trees.
  `.remedy-wt/f028-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f028-r7-worker/`    YOURS for logs, scripts and the G5 scratch config; create it
                                  if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx from the shell; vitest, tsc and eslint run through the pytest nodes of
G4, and G5's tool spawns the primary checkout's own vitest binary as a subprocess.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f028-task-injection`, and `git log --oneline -1` must read `bdcc86cb`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 27 | 914 | 1be3f4260aa29c92ca541305b8d040edb18026386626298ecd4e7d8008c2c015 |
| records.diff | 65 | 13238 | e9e06e141a2199fa1bc79b38ff1172a75ea12b12ee75d0803a069fba6a236d61 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; it appends
round 6's gate entry to `.agent/live_review.md`, DECISION F028 D7 to `.agent/decisions.md`, and
two rows naming DECISION F028 D7 to `docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION
S1 THE CANVAS CHIP, along the path `specVersion` takes: `BrainTaskSeed` in `brainOntology.ts`
   gains `origin?: string`; `dashboardBrainSeeds` in `brainView.ts` puts `origin` on a seed ONLY
   when the task item's `origin` equals `INJECTED_TASK_ORIGIN` of `api/injectView.ts`;
   `seedBrainModel` in `brainReducer.ts` copies it into `meta.origin` as it copies `specVersion`,
   and wherever the stage passes `specVersion` into a model already built it passes `origin` the
   same way; `injectView.ts` gains `ORIGIN_CANVAS_CHIP_TEXT = "added"`; and `taskChipOf` in
   `buildForceBrainModel.ts` answers `v<n>` alone, `added` alone, `` `v${n} · added` `` for both,
   and `undefined` for neither.
S2 THE DRAFT VIEW, in `injectView.ts`: `injectDraftView(answer: Record<string, unknown> | null)`
   answers null unless `answer.outcome` is `drafted` or `shortfall`, else an object with `kind`
   (the outcome), `draftId`, `confirmToken` (null for a shortfall), `title`, `goal`,
   `acceptance` (string list), `size` (`f"Size: {band}."`), `placement` (the placement's rationale
   with its first letter upper-cased and a full stop), `cost` (`f"Cost check: {arithmetic}."`),
   `fenceWarnings` (one sentence per fence flag: `` `${path} is outside what this job may change.` ``),
   `expiresAt`, and for a shortfall `question` and `options` (a list of `{option, label}` in the
   seed's order, from its `option_labels` mapping), `[]` for a draft. It reads defensively: a
   missing or mistyped field reads as the empty string or the empty list, never an exception.
S3 THE SHEET, a NEW FILE at `apps/ui/src/components/panels/AddTaskSheet.tsx` with a NEW FILE at
   `apps/ui/src/components/panels/AddTaskSheet.module.css`, props `{ target: DecisionSendTarget;
   tasks: readonly RemedyTaskItem[]; onClose: () => void }`, shaped as `LessonsOverlay.tsx` is: a
   right-anchored glass sheet with `role="dialog"`, `aria-label="Add a task"`,
   `data-ui="add-task-sheet"`, a Close button and Esc closing it. It holds: a labelled text area
   "What should the new task do?" (`maxLength={2000}`); a labelled select "It must follow" whose
   first option "Let the planner place it" has the value "" and whose other options are the tasks,
   value the task's id and text its label; a Draft pill disabled while the text is blank after
   trimming or a send is in flight. The draft's answer is shown through `injectDraftView` alone:
   title, goal, acceptance as a list, size, placement, cost, each fence warning, then Confirm and
   Discard for a draft, or the question and one ghost button per option for a shortfall. Draft
   calls `sendInjectDraft`, Confirm `sendInjectConfirm`, an option `sendInjectAnswer`; a derived
   draft an answer returns is shown as a draft; after `confirmed` or `dropped` the sheet shows its
   sentence and a Close button. Every result sentence goes into one `<p aria-live="polite">`. The
   style sheet uses existing `--remedy-*` tokens only and the overlay layer token for its z-index.
S4 THE ROW. `TaskChecklistCard` gains the prop `serverToken: string`, passed as
   `serverToken={serverToken}` from `RightLivePanel.tsx`. The propose button, its
   `proposeCommand`, the `remedy task propose` text and the `.proposeBtn` rule of
   `RightLivePanel.module.css` are DELETED; in their place a `<button type="button"
   className={styles.addTaskRow}>` reading "+ Add Task" opens the sheet, is disabled with the title
   "Adding a task needs the live page's server token." when `serverToken` is empty, and has the
   title "Draft a new task for this job." otherwise. `.addTaskRow` follows `ux_spec.md` §8's
   "+ Add Task" line and §14's disabled rule with existing tokens only.
S5 THE PINS. In `tests/ui_contracts/test_responsive.py`, `test_no_add_task_button` — the ONLY edit
   this round makes to a test it did not write, other than the tests of this feature's own
   modules — keeps its `AddTaskButton.tsx` absence assertion, replaces its last assertion with
   `assert "remedy task propose" not in checklist` and `assert "+ Add Task" in checklist`, and its
   comment names DECISION F028 D7. `tests/ui_contracts/test_inject_controls_contract.py` gains:
   `AddTaskSheet.tsx` holds no `fetch(` and calls `sendInjectDraft(`, `sendInjectConfirm(`,
   `sendInjectAnswer(` and `injectDraftView(`, and holds `role="dialog"`; `RightLivePanel.tsx`
   passes `serverToken={serverToken}` to `<TaskChecklistCard`; and exactly two lines of the
   assumption log name DECISION F028 D7.

THE TESTS — in `injectView.test.ts`: S2 for a draft, a shortfall, a derived draft, an outcome of
`confirmed`, null, and a body with every field missing; the canvas text constant. In
`brainView.test.ts`, `brainReducer.test.ts` and `buildForceBrainModel.test.ts`: the seed carries
`origin` only for an injected task, the meta copies it, and `taskChipOf`'s four answers.

BUNDLE — the commits are C1 to C7, in this order.
C1 — copy this block and the payloads: `.agent/authored/f028-r7-block.md`,
  `.agent/authored/f028-r7-records.diff`, `.agent/authored/f028-r7-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 92; STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R7 C2: book round 6, record D7 and its two assumption-log rows`
  Expected by `git show --numstat`: 37/0 decisions.md, 2/0 live_review.md, 5/8 plan.md, 2/0 assumption_log.md.
C3 — S1 with its three graph tests. Subject: `F028 R7 C3: draw added on an injected task's canvas node`
C4 — S2 with `injectView.test.ts`. Subject: `F028 R7 C4: read a draft answer as sentences for the sheet`
C5 — S3, S4 and S5. Subject: `F028 R7 C5: replace the propose button with the Add Task row and its sheet`
C6 — THE TOOL: `.agent/authored/f028-r7-mutations.py`. Subject: `F028 R7 C6: add the round 7 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R7 C7: rewrite handoff for round 7`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C3, C4 and C5 before
   you commit them; a commit that would reach 500 is split into parts with their own subjects,
   each part leaving the selection of G4 green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r7-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/ui/design_reference/assumption_log.md`, the files S1 to S5 and THE TESTS name, and
   `.agent/handoff.md`. Report the list `git diff --name-only bdcc86cb` measures after C7. Touch
   nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test THIS round
   wrote that is wrong may be corrected before C7, and the correction is declared. An existing
   test goes red and is edited only where S5 orders it or where it tests `injectView.ts` or the
   three graph modules S1 names; any other is reported, and you stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F028 one full-suite run, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table; then compare each `.agent/authored/f028-r7-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r7/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 329839 | 83d5ebdd13a63cb19de575c2126e3f8ecdf1fe55be41654ffdfc666e410c98bc |
 | .agent/decisions.md | 2272447 | b39f7bf5e70f8cb0b9c91e5ea07abfd9ff22d36a7b5ee02e98b2ec6b2bea8301 |
 | docs/ui/design_reference/assumption_log.md | 18596 | a0045eb241dd0d8afa8f0204cae402dbcf94fb37bcaeb503718d59156b54d512 |
 | .agent/plan.md | 914 | 1be3f4260aa29c92ca541305b8d040edb18026386626298ecd4e7d8008c2c015 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `bdcc86cb` and at C2 (the reviewer read `[]` at both), and `git diff --name-only <C1> <C2>`,
 which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_responsive.py
 tests/ui_contracts/test_inject_controls_contract.py` at C6, with its real exit code. Then quote
 from the diff `taskChipOf`, `injectDraftView`, the row's button and the sheet's mount in the
 card, and the sheet's shortfall branch.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts/test_inject_controls_contract.py tests/ui_server/test_dashboard_task_origin.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py tests/ui_server/test_dashboard_task_specs.py tests/ui_contracts/test_ux_quality.py tests/ui_contracts/test_responsive.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_contracts/test_design_drift.py tests/ui_contracts/test_ui_lint.py tests/ui_contracts/test_pause_controls_contract.py tests/ui_contracts/test_task_version_contract.py tests/ui_contracts/test_veto_controls_contract.py tests/ui_contracts/test_apply_state_partial.py tests/ui_contracts/test_decision_answer_wiring.py tests/ui_contracts/test_humanize_catalog.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_task_injection.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -14; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `bdcc86cb` and read
 `1204 passed, 9 skipped` at real exit code 0. Report every `SKIPPED` line and account for any
 difference from 1204 beyond the Python nodes the round adds. Then
 `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r7-mutations.py` takes a worktree path. For
 each mutation it edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs the PRIMARY checkout's `apps/ui/node_modules/.bin/vitest run --config
 <scratch>` with the primary's `apps/ui` as its working directory, where `<scratch>` is a config
 the tool writes under `.remedy-wt/f028-r7-worker/` exporting a PLAIN OBJECT with `root` the
 primary's `apps/ui`, `cacheDir` a directory under `.remedy-wt/`, `test.environment` `"node"` and
 `test.include` the worktree's `injectView.test.ts`, `brainView.test.ts`, `brainReducer.test.ts`
 and `buildForceBrainModel.test.ts` by absolute path, and restores the bytes. An unmutated control
 runs first and last. It prints one line per mutation (label, exit code, failed count, the
 failing tests' names) and ends with `restored byte-identical: True` per file, the PRIMARY
 checkout's `git status --porcelain` (which must be empty) and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `dashboardBrainSeeds` puts `origin` on every seed (brainView.ts);
  m2 `seedBrainModel` never copies `origin` (brainReducer.ts);
  m3 `taskChipOf` ignores `origin` (buildForceBrainModel.ts);
  m4 `taskChipOf` answers only the version when both apply (buildForceBrainModel.ts);
  m5 `injectDraftView` answers a shortfall's confirm token (injectView.ts);
  m6 `injectDraftView` drops the acceptance lines (injectView.ts);
  m7 a fence warning omits its path (injectView.ts).
 Run it: `git worktree add --detach .remedy-wt/f028-r7-mut <C6>`, then
 `python3 -B .agent/authored/f028-r7-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r7-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then add the test that catches it before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r7-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 8`, showing
 C7 back to C1 and `bdcc86cb` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Your Session section
reads SESSION 1 of feature F028, round 7, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7 with the reviewer's headless render of the row, the sheet and both chips, then the
end-to-end proof. State the open-findings count, 0, and the operator-questions count, 0.
