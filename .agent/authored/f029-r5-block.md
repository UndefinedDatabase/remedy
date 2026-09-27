STEP F029 R5 — BOOK R4, RECORD D5 AND ITS TWO ASSUMPTION-LOG ROWS, AND LAND T003's DISPLAY HALF: the attempts in the browser's types, the `attempt <n>` canvas chip, and the Attempts list in the task's popover

GOAL
Round 4 passed. Book its gate entry and its prose slip, record DECISION F029 D5 with its two
assumption-log rows, and show a task's attempts in the browser: the dashboard task item's
`attempt` and `attempts` read into the browser's types, the node's text chip reading
`attempt <n>` from the second attempt on, and an Attempts list in the task's detail popover,
shaped as the Versions list, whose rows open the fields that changed from the attempt before. No
Rerun control and no send module: round 6.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code and tests against S1 to S5. Read DECISION F029 D5 (it arrives with C2) and, whole:
`apps/ui/src/api/types.ts`, `apps/ui/src/api/remedyApi.ts` with its test,
`apps/ui/src/api/injectView.ts`, `apps/ui/src/api/taskSpecView.ts`,
`apps/ui/src/components/detail/DetailPopover.tsx` with `DetailPopover.module.css` and
`TaskVersionList.tsx`, and the `specVersion` and `origin` thread through
`apps/ui/src/components/graph/brainView.ts`, `brainOntology.ts`, `brainReducer.ts`,
`buildForceBrainModel.ts`, `BrainGraphStage.tsx` and `apps/ui/src/components/timeline/useTimelineScrub.ts`
with their tests.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r5-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f029-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f029-r5-worker/`    YOURS for logs, scripts and the G5 scratch config; create it
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
   `feature/f029-subtree-rerun`, and `git log --oneline -1` must read `47c63354`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 76 | 15682 | a77e470df3ae910a10f3f70a524fb11bb5e16c94e49d87c23dfd814f170be447 |
| plan.md | 35 | 1326 | 53c31d09cbe8a9a97be9e9e56595ee8e747016f00f416a9eb97bc59726bb9deb |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer generated
it with `git diff HEAD` from a tree at `47c63354`. It appends round 4's gate entry to
`.agent/live_review.md`, DECISION F029 D5 to `.agent/decisions.md`, one line to
`.agent/prose_slips.md`, and two rows naming DECISION F029 D5 to
`docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION
S1 THE TYPES. `types.ts` gains `RemedyTaskAttempt` — `attempt: number`, `status`, `finalStatus`,
   `reviewerVerdict`, `modelOverride`, `worktreeCommit`, `runId`, `rerunId`, `endedAt` as strings
   and `testPassed: boolean | null` — and `RemedyTaskItem` gains `attempt?: number` and
   `attempts?: RemedyTaskAttempt[]`. The task normalisation of `remedyApi.ts` reads `attempt` as
   an integer of at least 1, else 1, and `attempts` as the entries of an array that are objects
   with an integer `attempt` of at least 1, each field read from its snake_case key as a string
   ("" when missing or mistyped) and `test_passed` as a boolean or null; a missing or mistyped
   `attempts` reads as `[]`.
S2 THE CHIP, along the path `specVersion` and `origin` take: `BrainTaskSeed` gains
   `attempt?: number`; `dashboardBrainSeeds` puts `attempt` on a seed ONLY when the item's
   `attempt` is at least 2; `seedBrainModel` copies it into `meta.attempt` as it copies
   `specVersion`, and wherever a model already built receives `specVersion` or `origin` it receives
   `attempt` the same way; a NEW file `apps/ui/src/api/attemptView.ts` exports
   `attemptChipText(n: number): string` answering `` `attempt ${n}` ``; and `taskChipOf` in
   `buildForceBrainModel.ts` answers the parts that apply, in the order `v<n>`, "added",
   `attempt <n>`, joined by " · ", or `undefined` when none applies.
S3 THE ROWS, in `attemptView.ts`: `taskAttemptRows(item: RemedyTaskItem | undefined):
   TaskAttemptRow[]` answers `[]` unless `item.attempts` holds at least one entry. Otherwise one
   row per entry, oldest first, and last the current one. A row is `{ attempt, label, facts,
   changes, current }`. An earlier row's `label` is `` `Attempt ${n}` `` and its `facts` five
   strings, in order: how it ended — `status` `applied_to_job_workspace` or `passed` "It was
   applied", `blocked` "It was blocked", `failed` "It failed", `skipped` "It was skipped",
   `vetoed` "It was vetoed", `pending` "It had not run", any other `` `It ended as ${status}` ``;
   the verdict — `` `the reviewer said ${verdict}` `` or "no review verdict"; the tests — "its tests
   passed", "its tests failed" or "no test result"; the model — `` `it ran on ${model}` `` or "it
   ran on the job's own model"; the commit — `` `commit ${first twelve}` `` or "no commit". Its
   `changes` are, for each of the labels "Outcome", "Reviewer", "Tests", "Model" and "Commit" in
   that order whose fact differs from the earlier row before it, `{ label, before, after }` with
   the two facts; the first earlier row has none. The current row's `label` is
   `` `Attempt ${item.attempt} · current` ``, its `facts` the one string `` `Now ${words}` `` with
   `words` "waiting to run" for the state `pending`, "running" for `current`, "finished" for
   `done`, "blocked" for `blocked`, the state itself otherwise, its `changes` `[]` and `current`
   true. A helper `attemptFactsSentence(facts)` answers `facts.join("; ") + "."` with the first
   letter upper-cased.
S4 THE LIST. A NEW file `apps/ui/src/components/detail/TaskAttemptList.tsx`, shaped as
   `TaskVersionList.tsx`: `TaskAttemptList({ rows })` renders nothing for `[]`, else a
   `<section>` with the heading "Attempts" and a list `aria-label="Attempts"`, one item per row: a
   button reading the row's `label`, disabled when it has no `changes`, `aria-expanded` for the
   one row open at a time, the row's facts sentence beneath it, and when open the changes as a
   definition list of `before → after`, exactly as the Versions list draws its changes. It is
   mounted in `DetailPopover.tsx` directly after `TaskVersionList`, `key` the task's id and
   `rows={taskAttemptRows(task)}`. Any style it needs reuses the Versions list's classes of
   `DetailPopover.module.css`; a new rule uses existing `--remedy-*` tokens only.
S5 THE PINS. A NEW file `tests/ui_contracts/test_attempt_fan_contract.py`: `TaskAttemptList.tsx`
   holds no `fetch(`; `DetailPopover.tsx` mounts `<TaskAttemptList` with `taskAttemptRows(`;
   `buildForceBrainModel.ts` calls `attemptChipText(`; and exactly two lines of the assumption log
   name DECISION F029 D5.

THE TESTS — vitest, beside their modules: `remedyApi` normalisation of `attempt` and `attempts`
(valid, missing, mistyped, an entry without an integer `attempt` dropped); `attemptView.test.ts`
for `attemptChipText`, every ended word, the verdict, tests and model words, a row list of three
earlier attempts whose third changes back to the first's outcome — its changes compare with the
SECOND — the current row for each of the four states, `[]` for no attempts and for an undefined
item, and the facts sentence; `brainView.test.ts`, `brainReducer.test.ts` and
`buildForceBrainModel.test.ts` for the seed carrying `attempt` only from 2, the meta copying it,
and `taskChipOf` for each combination of the three parts.

BUNDLE — the commits are C1 to C7, in this order.
C1 — `.agent/authored/f029-r5-block.md` := this block, `.agent/authored/f029-r5-booking.diff` and
  `.agent/authored/f029-r5-plan.md` := the payloads, by `shutil.copyfile`.
  Subject: `F029 R5 C1: copy round 5 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 111. Report the number you measure.
C2 — `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F029 R5 C2: book round 4, record D5 and its two assumption-log rows`
  Expected by `git show --numstat`: 39/0 decisions.md, 2/0 live_review.md, 9/9 plan.md,
  1/0 prose_slips.md, 2/0 assumption_log.md.
C3 — S1 with its tests. Subject: `F029 R5 C3: read a task's attempts into the browser`
C4 — S2 with its tests. Subject: `F029 R5 C4: draw attempt n on a rerun task's canvas node`
C5 — S3, S4 and S5 with their tests. Subject: `F029 R5 C5: list a task's attempts in its detail popover`
C6 — `.agent/authored/f029-r5-mutations.py` (G5). Subject: `F029 R5 C6: add the round 5 mutation tool`
C7 — `.agent/handoff.md` per `docs/agents/handback_template.md`. Subject: `F029 R5 C7: rewrite handoff for round 5`
  Then `git push origin feature/f029-subtree-rerun` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C3, C4 and C5 before
   you commit them; a commit that would reach 500 is split into parts with their own subjects,
   each part leaving G4's selection green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f029-r5-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `docs/ui/design_reference/assumption_log.md`, the files S1 to S5 and THE TESTS name, and
   `.agent/handoff.md`. Report `git diff --name-only 47c63354` after C7. Touch nothing else —
   not `RunDetailPopover.tsx`, not `ui_server.py`, nothing under `packages/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test THIS round wrote that is wrong may be corrected
   before C7, and the correction is declared. An existing test goes red and is edited only where it
   tests a module S1 or S2 names; any other is reported, and you stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F029 one full-suite run, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; then
 each `.agent/authored/f029-r5-*` copy read back with `git show <C1>:<path>` compared byte for byte
 with its source (the block copy against `.remedy-wt/f029-r5/block.md`). One reading per copy.
G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2299065 | 9cd9b51634af35901a607bca5096ff10cb9e357647ee79716623dbaa2017a344 |
 | .agent/live_review.md | 323333 | 5cc9412ed8a851c4953a55568f0403a49196e34f9ab95ef569e1e78986ecf901 |
 | .agent/plan.md | 1326 | 53c31d09cbe8a9a97be9e9e56595ee8e747016f00f416a9eb97bc59726bb9deb |
 | .agent/prose_slips.md | 373961 | 477de5ee5d7c4532ea464030c8ba02ac8afa2170fe407edce8e02bffa1e63de4 |
 | docs/ui/design_reference/assumption_log.md | 20094 | 00cf320ab7b049bb192ed5f97ae80ffbbd96971a11b2cc10d6570042a4bba45e |
 Also `open_finding_ids` over the ledger's text at `47c63354` and at C2 (the reviewer read `[]` at
 both), and `git diff --name-only <C1> <C2>`, which must name exactly the paths of the table.
G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_attempt_fan_contract.py` at C6 with
 its real exit code; then quote from the diff `taskChipOf`, `taskAttemptRows` and the mount of
 `TaskAttemptList` in `DetailPopover.tsx`.
G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_task_attempts.py tests/ui_server/test_dashboard_task_origin.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py tests/ui_server/test_dashboard_task_specs.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `47c63354` and read
 `1608 passed, 11 skipped` at real exit code 0; the eleven skips are F252 quarantines. Report
 every `SKIPPED` line and account for any difference from 1608 beyond the Python nodes the round
 adds. Then `python3 -m apps.cli.main integrity check --json`: every check's status and
 `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f029-r5-mutations.py` takes a worktree path. For
 each mutation it edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs the PRIMARY checkout's `apps/ui/node_modules/.bin/vitest run --config
 <scratch>` with the primary's `apps/ui` as its working directory, where `<scratch>` is a config
 the tool writes under `.remedy-wt/f029-r5-worker/` exporting a PLAIN OBJECT with `root` the
 primary's `apps/ui`, `cacheDir` a directory under `.remedy-wt/`, `test.environment` `"node"` and
 `test.include` the worktree's `remedyApi` test, `attemptView.test.ts`, `brainView.test.ts`,
 `brainReducer.test.ts` and `buildForceBrainModel.test.ts` by absolute path, and restores the
 bytes. An unmutated control runs first and last. It prints one line per mutation (label, exit
 code, failed count, the failing tests' names) and ends with `restored byte-identical: True` per
 file, the PRIMARY checkout's `git status --porcelain` (which must be empty) and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `dashboardBrainSeeds` puts `attempt` on every seed (brainView.ts);
  m2 `seedBrainModel` never copies `attempt` (brainReducer.ts);
  m3 `taskChipOf` ignores `attempt` (buildForceBrainModel.ts);
  m4 `taskChipOf` drops `v<n>` when `attempt` applies (buildForceBrainModel.ts);
  m5 `taskAttemptRows` omits the current row (attemptView.ts);
  m6 an earlier row's changes compare with the FIRST earlier row (attemptView.ts);
  m7 the model fact reads `it ran on ` with an empty override (attemptView.ts);
  m8 the normalisation keeps an `attempt` of 0 (remedyApi.ts).
 Run it: `git worktree add --detach .remedy-wt/f029-r5-mut <C6>`, then
 `python3 -B .agent/authored/f029-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r5-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, then you add the test that catches it before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f029-r5-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.
G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 9`;
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected, every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per S-item), the deviations, and the next expected action. Your Session section reads SESSION 1
of feature F029, round 5, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5 with the reviewer's headless render of the chip and the Attempts list, then T003's
control half — the Rerun control, the send module with its cost confirmation, and the report
naming an override. State the open-findings count, 0, and the operator-questions count, 0.
