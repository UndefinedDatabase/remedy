STEP F036 R5 — T003'S SECOND HALF: the tour overlay with its backdrop, stepping and "Show me", its button and mount in the shell, and a headless render

GOAL
Round 4 passed and R-1087 is repaired. Book the verdict and the resolution, record DECISION F036
D6, then build the tour's browser surface: `apps/ui/src/components/tour/TourOverlay.tsx` with its
CSS module, portaled to the page body, a "Tour" button beside "Lessons" in `RightLivePanel.tsx`,
the shell's open state, mount and "Show me" navigation in `RemedyShell.tsx`, three more pure rules
in `apps/ui/src/api/resultTour.ts`, one line in the design reference's assumption log, and a
headless render that proves the overlay as a person sees it. No Python, route, event name or
report content changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records and the
assumption log's line travel as payloads. Read DECISION F036 D6 in the booking diff before you
write code. Before you write anything, read whole: `apps/ui/src/api/resultTour.ts`,
`apps/ui/src/api/resultTour.test.ts` and `loadTourView` in `apps/ui/src/api/remedyApi.ts`;
`apps/ui/src/components/lessons/LessonsOverlay.tsx` and its CSS module;
`apps/ui/src/components/panels/AddTaskSheet.tsx` for its `createPortal`;
`apps/ui/src/components/panels/RightLivePanel.tsx`; `apps/ui/src/components/shell/RemedyShell.tsx`;
`shellSelectionIdOf` in `apps/ui/src/components/graph/brainView.ts`; `buildDiffFileSummaries` in
`apps/ui/src/api/diffViewModel.ts` and `diffEnvelopePath` in `remedyApi.ts`;
`apps/ui/src/styles/tokens.css`; `docs/ui/design_reference/assumption_log.md`;
`tests/ui_contracts/test_lessons_overlay_contract.py`, `test_main_layout_guard.py`,
`test_raw_colour_ratchet.py`, `test_timeline_scrub_wiring.py` and `test_brain_stream_ring.py`'s
checks on `<RightLivePanel`; the five `.agent/authored/f035-r7-render_*` files and
`.agent/authored/f035-r7-render.txt`; and `.agent/authored/f036-r4-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f036-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f036-r5/`           READ-ONLY. The reviewer's block.
  Every other `.remedy-wt/f036-r*` directory and `.remedy-wt/f036-review/`  The reviewer's; do
                                  not touch them.
  `.remedy-wt/f036-r5-worker/`    YOURS for logs, scripts, screenshots and the vitest scratch
                                  config and cache; create it if absent. `.remedy-wt/f036-render-run/`
                                  is the render harness's own work dir, created and removed by it.
                                  All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx; the render harness runs the primary's own `vite` binary, and vitest,
tsc and eslint run through the pytest wrappers G4 names. Stop a process only by its own recorded
pid, never with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f036-guided-result-tour`, and `git log --oneline -1` must read `9ac3f750`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f036-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| assumption_line.md | 1 | 825 | 570e89b5009aee14c13e7ee2299c3c2429314f0957e6161c8c865e15d93673d1 |
| booking.diff | 64 | 10055 | 1a17f57ef32593028adb6d8fb4e263aa450e6f71a2359c5946f736a7182070b4 |
| plan.md | 28 | 927 | 65255245e009e45b6849cec241238b00e3659888c49023edbd915bb58b64584b |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `9ac3f750`. It appends round 4's gate entry and
the resolution `Done: R-1087` to `.agent/live_review.md`, and DECISION F036 D6 to
`.agent/decisions.md`. `assumption_line.md` is appended byte for byte to the end of
`docs/ui/design_reference/assumption_log.md`, whose last byte is already a newline.

THE SPECIFICATION. Every colour, shadow, radius and layer comes from a `--remedy-*` token: no raw
colour literal in any file this round adds or edits.
S1 THE PURE RULES, added to `resultTour.ts`: `tourGeneratorLabel(generator)` answering
   `Written by the summary model and checked against the job's records` for `summary-role` and
   `Built from the job's records` for any other generator; `tourCanShow(anchor)`, true exactly for
   the kinds `node` and `diff`; and `tourDiffRowKey(summaries, path)`, the `rowKey` of the first
   summary whose `path` equals `path`, or `null`, taking an array of `{path, rowKey}` so the
   module imports nothing.
S2 THE OVERLAY, NEW FILE at `apps/ui/src/components/tour/TourOverlay.tsx` with its CSS module
   `TourOverlay.module.css`. Props `{jobId, serverToken, onClose, onShowAnchor}`, the last taking
   a `TourAnchor`. One effect reads the view through `loadTourView` with a `let cancelled = false;`
   guard and the dependency list `}, [jobId, serverToken]);`, and the overlay reads its state only
   through `tourPanelState`. It renders through `createPortal(..., document.body)` a backdrop
   element `data-ui="tour-backdrop"`, fixed over the whole viewport and dimmed with
   `color-mix(in srgb, var(--remedy-ink-strong) 45%, transparent)`, present except while a stop is
   shown, and a card `<section role="dialog" aria-label="Guided tour" data-ui="tour-overlay">` on
   the glass tokens at `z-index: var(--remedy-z-overlay)`, above the backdrop. The card holds: the
   loading line `Reading the tour…`, or the unreadable or empty line, or for the current stop the
   `tourStepLabel`, an `<ol data-ui="tour-progress">` with one `<li>` per stop whose
   `data-state` is its `tourProgress` entry, the title, the body with its line breaks kept, the
   `tourAnchorLabel` — a command's ref inside `<code>` — and the `tourGeneratorLabel`; and the
   buttons Previous and Next, each disabled at its end by `tourNeighbours`, "Show me" only when
   `tourCanShow` holds, and "Close tour". "Show me" calls `onShowAnchor` with the stop's anchor
   and marks the stop shown, which removes the backdrop; stepping clears it. A window keydown
   listener closes on Escape and steps on ArrowLeft and ArrowRight, and is removed on unmount.
S3 THE ENTRY. `RightLivePanel` gains the optional prop `onOpenTour?: () => void` and, directly after
   the Lessons button, `{onOpenTour && (<button type="button" className={styles.advancedToggle}
   onClick={onOpenTour}>Tour</button>)}`. Nothing else in that file changes.
S4 THE SHELL. `RemedyShell` gains `tourOpen` state and a `tourDiffPath` state, passes
   `onOpenTour={() => setTourOpen(true)}` to `RightLivePanel`, and mounts
   `{tourOpen && (<TourOverlay ... />)}` as a sibling directly after the lessons overlay, outside
   `<main>`. Its `onShowAnchor` handler: a `node` anchor calls
   `onSelectNode(shellSelectionIdOf(dashboard.tasks, anchor.ref))`; a `diff` anchor sets
   `tourDiffPath` to the ref and calls `setOpenDiffTaskId("")`, which opens the job's whole diff.
   One effect, when `diffEnvelope` is available and `tourDiffPath` is set, finds
   `tourDiffRowKey(buildDiffFileSummaries(diffEnvelope), tourDiffPath)`, scrolls the element of
   that id into view when it exists, and clears `tourDiffPath`. `<main>` keeps exactly its four
   children, and nothing else in the shell changes.
S5 THE ASSUMPTION LOG. `assumption_line.md` appended to `docs/ui/design_reference/assumption_log.md`.
S6 THE RENDER, five NEW files `.agent/authored/f036-r5-render_measure.py`, `_index.html`,
   `_main.tsx`, `_vite.config.mjs` and `_drive.mjs`, adapted from F035 round 7's with the work
   dir `.remedy-wt/f036-render-run` and screenshots under your own directory. `main.tsx` mounts
   the real `TourOverlay` from `apps/ui/src` with a `window.fetch` answering one fixed view of six
   stops — a `node` stop on the first task of the demo recording, two `diff` stops, an `evidence`
   stop, a `command` stop and a second `evidence` stop — records every `onShowAnchor` call and the
   close on `window`, and can remount with a fetch answering an unreadable payload. `drive.mjs`
   checks over CDP, printing one PASS or FAIL line each: C-a the backdrop covers the viewport with
   a non-transparent computed background and the card's z-index is above it; C-b the step label
   reads `Stop 1 of 6` and the progress list holds six items, the first `current`; C-c Previous is
   disabled at the first stop and, after five ArrowRight presses, Next is disabled and the label
   reads `Stop 6 of 6`; C-d on the first `diff` stop "Show me" records that anchor and removes the
   backdrop, and ArrowRight brings it back; C-e the `command` stop shows its command inside
   `<code>`, and an `evidence` stop shows no "Show me"; C-f the overlay's root and backdrop are
   children of `document.body`; C-g Escape closes and is recorded; C-h the unreadable remount
   shows exactly `This job's tour could not be read.` and no text of the payload. It takes
   `render-tour.png` at the first stop and `render-tour-shown.png` after "Show me", and prints
   `RENDER: <n> of 8 checks pass`. Its whole output is saved as `.agent/authored/f036-r5-render.txt`.

THE TESTS. `apps/ui/src/api/resultTour.test.ts` gains tests of S1's three rules, and
`remedyApi`'s job-scope path: `diffEnvelopePath` with an empty task id reads `/api/jobs/<id>/diff`.
NEW FILE at `tests/ui_contracts/test_tour_overlay_contract.py`, reading sources through
`strip_ts_comments`: the overlay holds `role="dialog"`, `data-ui="tour-overlay"`,
`data-ui="tour-backdrop"`, `createPortal(`, `document.body`, the Escape line, the `cancelled`
guard, the dependency line of S2 and a call of `loadTourView`, and no `fetch(`; its CSS module
names `var(--remedy-z-overlay)` and `var(--remedy-ink-strong)`; the shell's `</main>` precedes
`<TourOverlay`, its `<RightLivePanel` line holds `onOpenTour=`, and it calls
`setOpenDiffTaskId("")` and `tourDiffRowKey(`; and `RightLivePanel.tsx` holds the button of S3.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f036-r5-block.md` := this block, and
  `.agent/authored/f036-r5-assumption_line.md`, `-booking.diff` and `-plan.md` := the payloads, by
  `shutil.copyfile`. Subject: `F036 R5 C1: copy round 5 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 93. STOP rather than commit at 500 or more.
C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md. Subject: `F036 R5 C2: book round 4, resolve R-1087, record DECISION F036 D6`
  Expected by `git show --numstat`: 44/0 decisions.md, 4/0 live_review.md, 7/7 plan.md.
C3 — THE SURFACE: `resultTour.ts`, the overlay and its CSS, `RightLivePanel.tsx`,
  `RemedyShell.tsx`, and S5's append. Subject: `F036 R5 C3: show the tour as an overlay with a backdrop, stepping and Show me`
C4 — THE TESTS: the vitest additions and the contract test.
  Subject: `F036 R5 C4: test the overlay's rules and pin its contract`
C5 — THE RENDER: the five render files and `.agent/authored/f036-r5-render.txt`.
  Subject: `F036 R5 C5: render the tour overlay headless and record its checks`
C6 — THE TOOL: your mutation tool (G5) as `.agent/authored/f036-r5-mutations.py`.
  Subject: `F036 R5 C6: add the round 5 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F036 R5 C7: rewrite handoff for round 5`. Then `git push`, and report its outcome.
  Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f036-r5-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the files C3 and C4 name,
   `docs/ui/design_reference/assumption_log.md`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 9ac3f750` at the branch tip after C7. Do NOT touch any other
   file under `apps/`, `packages/`, `tests/` or `docs/`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C7, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F036's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f036-r5-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f036-r5/block.md`), read back with
 `git show <C1>:<path>`, and show that `docs/ui/design_reference/assumption_log.md` at C3 equals
 its bytes at `9ac3f750` followed by `assumption_line.md`'s. Report one reading each.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2368177 | 5a4bcc1eac838c749e535d7b6ca7e17023de911365fcb17b6e2bac4da99560d2 |
 | .agent/live_review.md | 324894 | 0c57a55cad4cf14f9f0fd96b846b4ae952f339827d7901f2f06c68b59a2c0256 |
 | .agent/plan.md | 927 | 65255245e009e45b6849cec241238b00e3659888c49023edbd915bb58b64584b |
 Also: `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2, which the reviewer read as `[]` and `PASS`.

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_tour_overlay_contract.py
 .agent/authored/f036-r5-render_measure.py` at C6, with its real exit code. Then report, quoted
 from C3, the whole of `TourOverlay.tsx`'s effect and its keydown listener, the backdrop's and
 the card's CSS rules, the shell's `onShowAnchor` handler and its scroll effect, and S1's rules.

G4 THE TESTS AND THE RENDER — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_result_tour.py tests/cli/test_job_show.py tests/ui_server/test_tour_route.py tests/ui_server/test_handler_table_walk.py tests/ui_server/test_command_channel.py tests/ui_server/test_ownership_route.py tests/ui_contracts tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, serially, in the primary checkout at `9ac3f750`, and read
 `1777 passed, 5 skipped` at real exit code 0; the skips are four F252 quarantines in
 `tests/ui_contracts/` and the one in `tests/test_agent_tooling.py`. It runs vitest, `tsc
 --noEmit` and eslint over the whole of `apps/ui`. Report every `SKIPPED` line and the node count
 of each test file this round added or grew, and account for any difference from 1777. Then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.
 Then `python3 .agent/authored/f036-r5-render_measure.py /home/decodeux/Repos/remedy`, whose
 whole output C5 saves: it must print `RENDER: 8 of 8 checks pass` and exit 0, and afterwards
 `.remedy-wt/f036-render-run` must be gone and `git status --porcelain` empty. Report both
 screenshots' paths and sizes.

G5 THE RED PROOFS — your tool `.agent/authored/f036-r5-mutations.py`, modelled on round 4's, runs
 VITEST exactly as round 4's does with `test.include` the worktree's
 `apps/ui/src/api/resultTour.test.ts`, and a CONTRACT runner, `python3 -B -m pytest -q -p
 no:cacheprovider tests/ui_contracts/test_tour_overlay_contract.py` from the worktree's root. It
 prints one line per mutation, controls of each runner first and last,
 `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 VITEST (`resultTour.ts`) `tourCanShow` holds for `command`;
  m2 VITEST (`resultTour.ts`) `tourDiffRowKey` answers the LAST matching summary's key;
  m3 VITEST (`resultTour.ts`) `tourGeneratorLabel` calls every generator model-written;
  m4 CONTRACT (`TourOverlay.tsx`) the overlay renders in place, without `createPortal`;
  m5 CONTRACT (`TourOverlay.tsx`) the Escape handling is removed;
  m6 CONTRACT (`RemedyShell.tsx`) the tour mounts inside `<main>` instead of after it;
  m7 CONTRACT (`RemedyShell.tsx`) a diff stop opens the diff of the task id `"x"`, not the job's.
 Run it on `git worktree add --detach .remedy-wt/f036-r5-mut <C6>` and report its whole output.
 EVERY mutation must be red; a green one is reported as green, and you then add the test that
 catches it before C7 and re-run. Then remove the worktree, `git worktree prune`, and report
 `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C7 to C1 and `9ac3f750` in that order (more lines if
 constraint 2 split a commit); `git worktree list | wc -l`, equal to your step 4 reading; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Your Session section reads SESSION 1 of feature F036, round 5, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the demo's tour and the end-to-end proof of one real job's tour through both doors,
with the feature's Built State. State the open-findings count, 0, and the operator-questions
count, 1.
