STEP F035 R5 — REPAIR R-1082, THEN THE BROWSER'S FIRST HALF OF T003: a pure reader of the `ownership` route, one load in the shell, and a "Who did what" section with chips in the task detail

GOAL
Round 4 FAILED on one Low finding. Its first commit books that verdict and registers R-1082, with
DECISION F035 D5, one prose-slip line and one assumption-log row. Then repair R-1082 in
`packages/orchestration/ownership_phrases.py`, and land the browser's side: a NEW pure module
`apps/ui/src/api/ownership.ts` with its vitest file, `loadOwnershipView` in
`apps/ui/src/api/remedyApi.ts`, one load in `RemedyShell.tsx`, and the "Who did what" section in
`DetailPopover.tsx`, with a NEW contract test. The evidence panel's tab and the end-to-end proof
are the next round's.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge, and you never write a `Done:` paragraph. THE
PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the code and its tests yourself against S0 to
S6 below. Read DECISION F035 D5 and R-1082 in the booking diff first. Before you write anything,
read whole: `packages/orchestration/ownership_phrases.py`, `packages/orchestration/ownership.py`,
`tests/orchestration/test_ownership_phrases.py` and its golden; `apps/ui/src/api/lessons.ts` and
`lessons.test.ts` as the pattern for a decoder and its tests; the lessons and digest loaders of
`apps/ui/src/api/remedyApi.ts`; `apps/ui/src/components/shell/RemedyShell.tsx`;
`apps/ui/src/components/detail/DetailPopover.tsx` and `DetailPopover.module.css`;
`tests/ui_contracts/test_lessons_overlay_contract.py` as the pattern for a contract test; every
test under `tests/ui_contracts/` that reads `DetailPopover.tsx` or `RemedyShell.tsx` (search them);
`tests/ui_contracts/test_raw_colour_ratchet.py`; §13 and §17 of
`docs/ui/design_reference/ux_spec.md`; and G5 of `.agent/authored/f030-r3-block.md`, the
precedent for vitest red proofs in a worktree.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f035-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f035-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f035-r5-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f035-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f035-r5-worker/`    YOURS for logs, scripts and the scratch vitest config; create it
                                  if absent. All five are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx; the pytest nodes named in G4 run tsc, eslint and vitest for you.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f035-ownership-ledger`, and `git log --oneline -1` must read `0faa196f`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f035-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f035-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 75 | 19422 | 79a30514ef2a68c90af92c499d61e9ff80c2dc3524c4edc155790d5981df5abc |
| plan.md | 27 | 870 | 5093dc17928e81f95dd004bb208108f801309812bd2b585a4afe5f4732c38b14 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the
reviewer generated it with `git diff HEAD` from a tree at `0faa196f`. It appends round 4's gate
entry and R-1082's registration to `.agent/live_review.md`, DECISION F035 D5 to
`.agent/decisions.md`, one line to `.agent/prose_slips.md`, and one row to
`docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION. No `except Exception` in Python; no `any` type and no raw colour in TypeScript
or CSS; every sentence a server entry carries is shown verbatim, never passed through
`scrubUiText`, never cut.
S0 R-1082'S REPAIR, in `ownership_sentence`: every `plan_edited` and `task_edited` sentence ends
   `; the plan is now at version <n>.`, and `plan_edit_acceptance` reads `A changed the
   acceptance checks of T; the plan is now at version <n>.` — exactly S1 of
   `.agent/authored/f035-r4-block.md`. The golden's plan-edit lines and the inline assertions
   follow; no other golden line changes. In the SAME commit append to `.agent/live_review.md` the
   one line `Landed: R-1082 — <what changed>, in this commit.`, naming the files.
S1 THE READER, `apps/ui/src/api/ownership.ts`, whose header comment states that it opens no
   socket, reads no clock and keeps no storage, and names F035 T003 and DECISION F035 D5:
   types `OwnershipActor` (`kind`, `door`, `recordedAs`, `tokenNumber`, `autoApproved`),
   `OwnershipConsequence` (`kind`, `taskIds`, `ref`), `OwnershipEntry` (`recordRef`, `ts`,
   `actor`, `action`, `taskId`, `text`, `consequence`, `sentence`) and `OwnershipView`
   (`schema`, `jobId`, `entries`, `error`); `decodeOwnershipView(raw: unknown): OwnershipView |
   null`, which answers null for a non-object, a `schema` other than `remedy.ownership.v1`, a
   non-array `entries`, a non-string `error`, or ANY entry with a field of the wrong type;
   `ownershipViewPath({ jobId, token, baseUrl? })`, shaped as `lessonsIndexPath` with the last
   segment `ownership`; `ownershipChipWord(action)` from one exported record
   `OWNERSHIP_CHIP_WORDS` — `task_vetoed` Veto, `veto_answered` Veto answer, `task_injected`
   Added, `subtree_rerun` Rerun, `plan_edited` Plan edit, `task_edited` Edit, `steering_sent`
   Steering, `note_sent` Note, `job_paused` and `task_paused` Pause, `job_resumed` and
   `task_resumed` Resume, `job_stopped` Stop, `hunk_approved` Hunk approved, `hunk_rejected` Hunk
   rejected, `decision_answered` Answer, `clarification_answered` Plan question, `plan_approved`
   Approval, `plan_rejected` Rejection — and the word `Action` for any other;
   `ownershipEntriesForTask(view, taskId)`, the entries whose `taskId` is `taskId` or whose
   `consequence.taskIds` holds it, in the view's order, `[]` for an empty `taskId`;
   `OWNERSHIP_UNREADABLE_LINE = "Who did what could not be read for this job."`; and
   `OWNERSHIP_REFRESH_EVENTS`, exactly `task_vetoed`, `veto_proposal_answered`, `task_injected`,
   `subtree_rerun_prepared`, `plan_approved`, `job_paused`, `task_paused`, `job_resumed`,
   `task_resumed`, `job_stopped`, `steering_message_received`, `steering_message_consumed` and
   `task_decision_answered`, with `ownershipRefreshKey(recent)` answering the newest `seq` of a
   frame of those kinds, as `lessonsRefreshKey` does for its one kind.
S2 THE LOADER, in `remedyApi.ts` after the lessons loader: `OwnershipFetcher` and
   `loadOwnershipView(request, fetchPayload = fetchJson): Promise<OwnershipView | null>`, which
   never throws, as `loadLessonsIndex` does.
S3 THE SHELL, `RemedyShell.tsx`: one `useState<OwnershipView | null>` and one effect beside the
   digest's, guarded by `cancelled`, whose dependencies are `dashboard.jobId`, `serverToken`, the
   `ownershipRefreshKey` of the stream's recent frames and `focusedTaskId`; the view reaches
   `DetailPopover` as the new optional prop `ownership`. Nothing else in the shell changes.
S4 THE SECTION, `DetailPopover.tsx`: the optional prop `ownership?: OwnershipView | null`; directly
   after the unreachable section and before the changed-files comment, a `<section
   className={styles.section} data-ui="ownership-section">` headed `<h3>Who did what</h3>`,
   rendered only when the view is not null and either its `error` is not "" — then one `<p>`
   holding `OWNERSHIP_UNREADABLE_LINE`, never the error text — or `ownershipEntriesForTask(view,
   task.id)` is not empty — then one `<ul>` whose `<li key={entry.recordRef}>` holds a chip
   `<span className={styles.ownershipChip}>` with `ownershipChipWord(entry.action)` and the
   sentence `<span className={styles.ownershipSentence}>` verbatim. `DetailPopover.module.css`
   gains `.ownershipChip`, shaped as the file's `.originChip` (radius `--remedy-radius-pill`, the
   same font rule), and `.ownershipSentence` with `white-space: pre-line`, in `--remedy-*` tokens
   only, so the raw-colour ratchet's count for that file does not change. The popover still never
   fetches.
S5 THE CONTRACT, NEW `tests/ui_contracts/test_ownership_view_contract.py`: the wire keys
   `ownership.ts` reads from the view, an entry, an actor and a consequence each equal the keys
   the server writes (`ownership_view`, `_ENTRY_KEYS` without `detail` plus `sentence`,
   `ownership_actor`'s keys, `_CONSEQUENCE_KEYS`); `ownership.ts` holds no `fetch(`, `Date.now`,
   `new Date` or `localStorage`; every name of `OWNERSHIP_REFRESH_EVENTS` is in `EVENT_NAMES` of
   `packages/orchestration/event_names.py`; the keys of `OWNERSHIP_CHIP_WORDS` equal the actions
   the phrase catalog words, read from its source; `DetailPopover.tsx` places
   `data-ui="ownership-section"` after `data-ui="unreachable-section"`, renders
   `OWNERSHIP_UNREADABLE_LINE` and never `ownership.error`; and the shell's effect carries the
   `cancelled` guard and `ownershipRefreshKey` in its dependencies.
S6 THE UNIT TESTS, NEW `apps/ui/src/api/ownership.test.ts` after `lessons.test.ts`: a wire-shaped
   fixture decoded, one refusal per malformed field, the path with an encoded id and token,
   entries for a task by its own id and by a consequence, in order, and none for "", every chip
   word and the fallback, the refresh key over mixed frames, and `loadOwnershipView` with a fake
   fetcher that records its path and with one that throws.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f035-r5-block.md`,
  `.agent/authored/f035-r5-plan.md` and `.agent/authored/f035-r5-booking.diff`, by
  `shutil.copyfile`. Subject: `F035 R5 C1: copy round 5 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 102. Report the number you measure.
C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md. Subject: `F035 R5 C2: book round 4's FAIL, register R-1082,
  record D5, one prose slip, one assumption row, advance the plan`
  Expected by `git show --numstat`: 37/0 decisions.md, 4/0 live_review.md, 6/7 plan.md, 1/0
  prose_slips.md, 1/0 assumption_log.md.
C3 — S0 with its golden, inline assertions and `Landed:` line. Subject:
  `F035 R5 C3: repair R-1082, the plan-edit sentences read as D4 orders`
C4 — S1, S2 and S6. Subject: `F035 R5 C4: the ownership view reader, its loader and unit tests`
C5 — S3, S4 and S5. Subject: `F035 R5 C5: who did what in the task detail, loaded once by the shell`
C6 — your mutation tool (G5), `.agent/authored/f035-r5-mutations.py`. Subject:
  `F035 R5 C6: add the round 5 mutation tool`
C7 — THE HANDBACK, `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, its own
  commit. Subject: `F035 R5 C7: rewrite handoff for round 5`. Then `git push`. Do NOT create a
  pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f035-r5-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `docs/ui/design_reference/assumption_log.md`, `packages/orchestration/ownership_phrases.py`,
   `tests/orchestration/fixtures/ownership/golden/sentences.txt`,
   `tests/orchestration/test_ownership_phrases.py`, `apps/ui/src/api/ownership.ts`,
   `apps/ui/src/api/ownership.test.ts`, `apps/ui/src/api/remedyApi.ts`,
   `apps/ui/src/components/shell/RemedyShell.tsx`,
   `apps/ui/src/components/detail/DetailPopover.tsx`,
   `apps/ui/src/components/detail/DetailPopover.module.css`,
   `tests/ui_contracts/test_ownership_view_contract.py`, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 0faa196f` after C7. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round itself wrote that is wrong may be
   corrected before C7, and the correction is declared. An EXISTING test that goes red is never
   edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every existing worktree, branch and stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` and the
   `remedy/*` branch count are reported afterwards; neither may change.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F035's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table, then
 each `.agent/authored/f035-r5-*` payload copy compared byte for byte with its source, read back
 with `git show <C1>:<path>`. One reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2338101 | d13d01e6782b99c94cd5fb115612aa6d731b6c8ce3e126fd763b87af305684c1 |
 | .agent/live_review.md | 314109 | 1e8412bee857d57a09240a8486f5f79ce07a176cd855660525a2ee756e0ac1fd |
 | .agent/plan.md | 870 | 5093dc17928e81f95dd004bb208108f801309812bd2b585a4afe5f4732c38b14 |
 | .agent/prose_slips.md | 375262 | 47785db09ed39a4820e8aa20702eee8804f9add8ff97b723aacaf5bf837943c7 |
 | docs/ui/design_reference/assumption_log.md | 22672 | b2d1a80614b45a9382aefe4eec97077f4aa4196c62988f2f9c69438dac0ffc8a |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at C2, which
 the reviewer read as `['R-1082']`.

G3 THE CODE — `python3 -m ruff check packages/orchestration/ownership_phrases.py
 tests/orchestration/test_ownership_phrases.py tests/ui_contracts/test_ownership_view_contract.py`
 with its real exit code; `git show <C3> -- tests/orchestration/fixtures/ownership/golden/sentences.txt`
 whole; and, quoted from `git show <C5>`, the shell's effect and the popover's section.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_ownership_route.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_ownership_phrases.py tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py tests/cli/test_job_ownership.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, serially, in the primary checkout at `0faa196f`, and read
 `1640 passed, 11 skipped` at real exit code 0; the skips are the F252 quarantines. Report every
 `SKIPPED` line and account for the new total by the node counts of the files this round added
 or grew. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f035-r5-mutations.py` takes a worktree path and
 follows G5 of `.agent/authored/f030-r3-block.md` exactly: PYTHON runs `python3 -B -m pytest -q
 -p no:cacheprovider tests/orchestration/test_ownership_phrases.py
 tests/ui_contracts/test_ownership_view_contract.py` from the worktree's root after purging its
 `__pycache__`; VITEST runs the PRIMARY checkout's `apps/ui/node_modules/.bin/vitest run --config
 <scratch>` from the primary's `apps/ui`, the scratch config under `.remedy-wt/f035-r5-worker/`
 exporting a plain object with `root` the primary's `apps/ui`, a `cacheDir` under `.remedy-wt/`,
 `test.environment` `"node"` and `test.include` the worktree's `ownership.test.ts` by absolute
 path. An unmutated control of EACH runner runs first and last; one line per mutation (label,
 runner, exit code, failed count, failing names); `restored byte-identical: True` per file; the
 PRIMARY checkout's `git status --porcelain`, which must be empty; and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 PYTHON `ownership_phrases.py`: the plan-edit sentences drop `at`;
  m2 PYTHON `ownership_phrases.py`: the acceptance sentence gains ` in the plan`;
  m3 VITEST `ownership.ts`: the decoder accepts an entry whose `sentence` is not a string;
  m4 VITEST `ownership.ts`: `ownershipEntriesForTask` ignores `consequence.taskIds`;
  m5 VITEST `ownership.ts`: `ownershipRefreshKey` counts every frame's `seq`;
  m6 VITEST `ownership.ts`: the path leaves the job id unencoded;
  m7 VITEST `remedyApi.ts`: `loadOwnershipView` lets a throwing fetcher reject;
  m8 PYTHON `DetailPopover.tsx`: the section renders `ownership.error` instead of the line;
  m9 PYTHON `RemedyShell.tsx`: the effect's dependencies drop the refresh key.
 Run it: `git worktree add --detach .remedy-wt/f035-r5-mut <C6>`, then
 `python3 -B .agent/authored/f035-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f035-r5-mut`,
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, never papered over, and you then add the test that catches it before C7 and re-run the
 tool. Then `git worktree remove --force .remedy-wt/f035-r5-mut` and `git worktree prune`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C7 down to C1 and `0faa196f` in that order (more lines
 if constraint 2 split a commit); the worktree and `remedy/*` counts, equal to your step 4
 readings; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate, and one for R-1082), the deviations, and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of
feature F035, round 5, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5 including R-1082's repair, then the evidence panel's ownership tab and the end-to-end
proof. State the open-findings count, 1 (R-1082, landed and awaiting review), and the
operator-questions count, 0.
