STEP F039 R5 — BOOK ROUND 4, REPAIR R-1100, AND LAND T002's IN-APP STORY: the docked panel over the timeline's own scrub, its golden walkthrough, its entry and mount, and a headless render

GOAL
Round 4 is reviewed PASS at `c4a1cf5d`. Book its gate entry, register finding R-1100 and record
DECISION F039 D6 with the plan. Repair R-1100: three docstrings promise that a changed
configuration reaches the cockpit without a restart, while `get_config` loads it once per process.
Then close T002 with the in-app story: the pure rules of `apps/ui/src/components/story/storyPlayer.ts`
with the golden walkthrough of the demo recording, the panel `StoryPanel.tsx` with its CSS module
narrating the ledger through the timeline's own scrub, a Story button and the shell's mount, one
line in the design reference's assumption log, and a headless render that proves the panel as a
person uses it. No route, event name, command or dashboard section changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code, its tests, the render harness and the mutation tool yourself against S1 to S7.
Only the `.agent/` records and the assumption log's line travel as payloads. Read DECISION F039 D6
and finding R-1100 in the records diff before you write code. Before you write anything, read
whole: the five modules under `apps/ui/src/components/story/`; `useTimelineScrub.ts` and
`PhaseTimeline.tsx` under `apps/ui/src/components/timeline/`; `ReducedMotionProvider.tsx`;
`dashboardBrainSeeds` in `apps/ui/src/components/graph/brainView.ts`; `TourOverlay.tsx` and its CSS
module for the portal and the glass tokens; `RightLivePanel.tsx`; `RemedyShell.tsx`;
`apps/ui/src/styles/tokens.css`; `docs/ui/design_reference/assumption_log.md`;
`tests/ui_contracts/test_tour_overlay_contract.py`, `test_main_layout_guard.py` and
`test_raw_colour_ratchet.py`; `get_config` and `reset_config` in `packages/orchestration/config.py`;
`_rate_limit_admits_command` and `_build_story_section` in `packages/orchestration/ui_server.py` and
`tests/ui_server/test_story_section.py`; the five `.agent/authored/f036-r7-render_*` files; and your
round 4 tool `.agent/authored/f039-r4-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r5-dry/`, `.remedy-wt/f039-r5-sim/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r5-worker/`    YOURS for logs, scripts and screenshots; create it if absent.
                                  `.remedy-wt/f039-render-run/` is the render harness's own work
                                  dir, created and removed by it. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx: the render harness runs the primary's own `vite` binary. Stop a
process only by its own recorded pid, never with `pkill -f`. Never `git reset` a commit: a commit
made out of order is declared, not rewritten.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `c4a1cf5d7`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| assumption_line.md | 1 | 1014 | 027fa00d2ae812d32da0d39199ca12068eb34984ccf8b0642abcf80c3fd5a678 |
| plan.md | 30 | 1040 | 81aec753edd444ae1d213bb207528c99539c1cc747dfde8fbeee0792635a5385 |
| records.diff | 58 | 10965 | 9000671547adb1d6fd6f7a7b261e460d2c2581ccf17d9e518785d564389508f9 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `c4a1cf5d`. It appends to `.agent/live_review.md`
round 4's gate entry and the registration of R-1100, and to `.agent/decisions.md` DECISION F039 D6.
`assumption_line.md` is appended byte for byte to the end of
`docs/ui/design_reference/assumption_log.md`, whose last byte is already a newline.

THE SPECIFICATION. Every colour, shadow, radius and layer comes from a `--remedy-*` token that
`apps/ui/src/styles/tokens.css` defines: no raw colour in any file this round adds or edits.
S1 R-1100. The docstrings of `_rate_limit_admits_command` and `_build_story_section` in
   `packages/orchestration/ui_server.py` and the module docstring of
   `tests/ui_server/test_story_section.py` say the value is read on every request (or call) from the
   process's configuration, which `get_config` loads once and keeps, so a change takes effect when
   the cockpit restarts, and name R-1100; no code changes. That test file gains one test: with
   `REMEDY_STORY_STEP_MS` unset and `reset_config()`, the section's `step_ms` reads 420; after
   `monkeypatch.setenv` to "900" it STILL reads 420; after `reset_config()` it reads 900; the test
   undoes the variable and resets again in a `finally`. In C3, append to `.agent/live_review.md` one
   blank line and one line beginning `Landed: R-1100 — ` saying in one sentence what changed; it
   names no commit. Never write a `Done:` line.
S2 THE PURE RULES, a NEW FILE `apps/ui/src/components/story/storyPlayer.ts`, pure, importing only
   from `./storyAutoplay`, `./storyNarration` and `./storyView`. `STORY_RUNNING_LINE` is
   `This job is still running, so its story ends where the record ends now.`
   `storyPositionLabel(view, position)`: `No event is recorded yet.` when the view has no chapter;
   `Before the first event` below the first chapter's start; `After the last event` when
   `chapterAt` answers -1; else `Chapter <index + 1> of <count>: <title>`.
   `storyPlayStart(view, position, live)`: -1 when `live`, when the view has no seq, or when
   `position` is at or past the last seq; else `position`. `storyBeatsAt(card, position)`: `[]` for
   a null card, else the card's beats whose seq is at or before `position`, in order.
   `interface StoryFrame { position; delayMs; label; cardFirstSeq: number | null; beats: number }`
   and `storyWalk(view, reducedMotion)`: the frames of `autoplayStep` from -1 until it answers null,
   each with its step's position and wait, `storyPositionLabel` there, `cardAt`'s first seq or null,
   and the count of `storyBeatsAt` there.
S3 THE PANEL, NEW FILES `StoryPanel.tsx` and `StoryPanel.module.css` beside it. Props
   `{ dashboard: RemedyDashboard; rows: readonly BrainEventRow[]; ownership: OwnershipView | null;
   scrub: TimelineScrub; onClose: () => void }`. The view is `buildStoryView(dashboard.jobId,
   dashboardBrainSeeds(dashboard.tasks), rows, ownership, dashboard.story)`, memoised. It renders
   through `createPortal(..., document.body)` a `<section role="region" aria-label="Story"
   data-ui="story-panel">` holding: a heading `Story`; `<p data-ui="story-position">` with
   `storyPositionLabel` at `scrub.state.position`; `<p data-ui="story-running">` with
   `STORY_RUNNING_LINE` only while `dashboard.live.running`; `<ol data-ui="story-chapters">`, one
   `<button>` per chapter naming its title, which stops play and calls `scrub.scrubTo(startSeq)`,
   the current chapter's with `aria-current="step"`; `<div data-ui="story-card">` only when
   `cardAt` answers a card, listing `storyBeatsAt`'s beats — each its line, then its verdict and its
   actor when not null — and `<p data-ui="story-cost">` with the card's cost when not null; and the
   buttons `Previous chapter` and `Next chapter` (disabled at their ends and with no chapter), `Play`
   or `Pause`, disabled with no seq, and `Close story`. Play: `storyPlayStart` at the position, a
   `scrubTo` of it when the scrub is LIVE or the start differs, then playing. THE ONE TIMER: an
   effect that, while playing, asks `autoplayStep(view.chapters, view.seqs, position, view.pacing,
   reducedMotion)` with `useReducedMotion()`, stops playing on null, else calls
   `window.setTimeout(() => scrub.scrubTo(step.position), step.delayMs)` and returns a cleanup that
   calls `window.clearTimeout`. A window keydown listener, removed on unmount: Escape stops play and
   closes; Space, unless the target is an input or a textarea, prevents its default and toggles play.
   The CSS docks the card `position: fixed` at `left: calc(var(--remedy-left-width) + 16px)`,
   `bottom: 96px`, 360 px wide, `max-height: 60vh` scrolling, `z-index: var(--remedy-z-overlay)`, on
   `--remedy-glass-bg-strong`, `--remedy-glass-border`, `--remedy-radius-lg` and
   `--remedy-shadow-card`, text `--remedy-ink`; chapter and action buttons small pills on
   `--remedy-glass-border` with `--remedy-radius-sm`, the current chapter outlined and written in
   `--remedy-purple`, disabled buttons at half opacity; verdict, actor, cost and running line in
   `--remedy-muted`.
S4 THE ENTRY. `RightLivePanel` gains the optional prop `onOpenStory?: () => void` and, directly after
   the Tour button, `{onOpenStory && (<button type="button" className={styles.advancedToggle}
   onClick={onOpenStory}>Story</button>)}`. `RemedyShell` gains `storyOpen` state under a comment
   naming DECISION F039 D6, passes `onOpenStory={() => setStoryOpen(true)}` beside `onOpenTour`, and
   mounts `{storyOpen && (<StoryPanel dashboard={dashboard} rows={ledgerRows} ownership={ownership}
   scrub={scrub} onClose={() => setStoryOpen(false)} />)}` directly after the tour's mount, outside
   `<main>`, which keeps exactly its four children. Nothing else in either file changes.
S5 THE ASSUMPTION LOG. `assumption_line.md` appended to `docs/ui/design_reference/assumption_log.md`.
S6 THE TESTS. A NEW FILE `storyPlayer.test.ts` beside the module, HAND-DERIVED from the demo
   recording's chapters and cards and the default pacing: `storyWalk` without reduced motion as ONE
   literal of ten frames — positions 0 to 9, waits 2020, 2020, then 420 seven times, then 2020; the
   labels `Chapter 1 of 3: The build`, then `Chapter 2 of 3: The review` for positions 1 to 8, then
   `Chapter 3 of 3: The finish`; cards null, 1 for positions 1 to 5, 6 for 6 to 8, null; beat counts
   0, 1, 1, 2, 2, 2, 1, 1, 2, 0 — and with reduced motion as ONE literal of three frames, positions 0,
   1 and 9, each 1600, beat counts 0, 1 and 0; `[]` for an empty ledger; every label of S2 including
   position 10's; `STORY_RUNNING_LINE`; and `storyPlayStart` for LIVE, the last seq, position 4,
   position -1 and an empty view. A NEW FILE `tests/ui_contracts/test_story_panel_contract.py`,
   reading through `strip_ts_comments` of `test_brain_stream_ring.py`: the panel holds
   `createPortal(`, `document.body`, `data-ui="story-panel"`, `role="region"`, `autoplayStep(`,
   `buildStoryView(`, `useReducedMotion()`, exactly one `window.setTimeout(` and a
   `window.clearTimeout(`, and no `fetch(`; its CSS names `var(--remedy-z-overlay)` and
   `var(--remedy-purple)` and no raw colour; `storyPlayer.ts`'s specifiers by `ts_import_specifiers`
   are exactly the three of S2 and no purity word occurs; the shell's `</main>` precedes
   `<StoryPanel`, it passes `onOpenStory={() => setStoryOpen(true)}` and the panel `scrub={scrub}`;
   and `RightLivePanel.tsx` holds S4's button.
S7 THE RENDER, five NEW files `.agent/authored/f039-r5-render_measure.py`, `_index.html`,
   `_main.tsx`, `_vite.config.mjs` and `_drive.mjs`, adapted from F036 round 7's with the work dir
   `.remedy-wt/f039-render-run`, CDP port 9366, server port 8996, and the screenshot under your own
   directory. `main.tsx` mounts, inside `ReducedMotionProvider`, a host that runs the real
   `useTimelineScrub` over `brainDemoRows()` with `BRAIN_DEMO_TASKS`, renders the real
   `PhaseTimeline` and the real `StoryPanel` with the dashboard `normalizeApiFailure(<demo job id>,
   [])` given the demo tasks, `live.running` from a `running=1` query parameter, and `story`
   `{step_ms: 60, chapter_pause_ms: 150}`; it records every scrub position on `window` from an effect
   on the position, and the close. `drive.mjs` prints one PASS or FAIL line per check at 1280 by 800:
   C-a the panel is a child of `document.body`, its z-index is 80 and its box lies inside the
   viewport; C-b its chapter buttons read `The build`, `The review` and `The finish`, and the label
   `Chapter 3 of 3: The finish`; C-c after clicking `The review` the label reads
   `Chapter 2 of 3: The review`, the card holds ONE beat whose text holds `Verdict: needs repair`, and
   the timeline's readout begins `Event 1 of 9`; C-d Play walks the positions 2 to 9 in order and
   stops with the button reading `Play`; C-e Play again restarts at -1, and Space pressed 400 ms later
   stops the positions growing and the button reads `Play`; C-f Escape removes the panel and records
   the close; C-g after a reload with `prefers-reduced-motion: reduce` emulated, Play walks exactly
   -1, 0, 1 and 9; C-h the page with `running=1` shows the running line. It screenshots after C-c and
   prints `RENDER: <n> of 8 checks pass`. Its whole output is saved as
   `.agent/authored/f039-r5-render.txt`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6, C7, C8 and C9, in this order.
C1a — `.agent/authored/f039-r5-block.md` := this block, and `.agent/authored/f039-r5-plan.md` and
  `.agent/authored/f039-r5-assumption_line.md` := the payloads, by `shutil.copyfile`. Subject:
  `F039 R5 C1a: copy round 5 block and payloads into .agent/authored/`. Its insertions are this
  block's line count plus 31; STOP rather than commit at 500 or more.
C1b — `.agent/authored/f039-r5-records.diff` := records.diff. Subject: `F039 R5 C1b: copy round 5
  records diff into .agent/authored/`. Expected insertions: 58.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F039 R5 C2: book
  round 4, register R-1100, record D6`. Expected by `git show --numstat`: 38/0 decisions.md, 4/0 live_review.md, 6/10 plan.md.
C3 — S1. Subject: `F039 R5 C3: say when a configuration change takes effect (R-1100)`.
C4 — S2 and `storyPlayer.test.ts`. Subject: `F039 R5 C4: golden the story's walkthrough and the
  panel's words`.
C5 — S3, S4 and S5. Subject: `F039 R5 C5: tell the story in a panel over the timeline's scrub`.
C6 — the contract test. Subject: `F039 R5 C6: pin the story panel's seams`.
C7 — S7's five files and `.agent/authored/f039-r5-render.txt`. Subject: `F039 R5 C7: render the
  story panel headless and record its checks`.
C8 — your mutation tool as `.agent/authored/f039-r5-mutations.py`. Subject: `F039 R5 C8: add the
  mutation tool for the story panel and R-1100`.
C9 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R5 C9:
  rewrite handoff for round 5`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r5-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/ui_server.py`, `tests/ui_server/test_story_section.py`, the four new
   files under `apps/ui/src/components/story/`, `apps/ui/src/components/panels/RightLivePanel.tsx`,
   `apps/ui/src/components/shell/RemedyShell.tsx`, `docs/ui/design_reference/assumption_log.md`,
   `tests/ui_contracts/test_story_panel_contract.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only c4a1cf5d7` measures after C9. Do NOT touch anything else, in particular
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C9, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`, no `git reset`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree listed at
   your step 4, and every stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as
   that gate's last action, and `git worktree list | wc -l` is reported afterwards.
7. DO NOT run the full suite: it belongs to F039's closure (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C9 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f039-r5-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r5/block.md`), read back with `git show
 <commit>:<path>` from the commit that added it, and show that the assumption log at C5 equals its
 bytes at `c4a1cf5d7` followed by `assumption_line.md`'s. One reading each.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2434466 | dfde6038391a4fc455d9ff38df35e21bac1a384bb6548b3350f54cca576a8f0f |
 | .agent/live_review.md | 341289 | a5ced3615b60dd02fcab40ae354cc779bbbbd4d82c6398bcb69f7104286acb12 |
 | .agent/plan.md | 1040 | 81aec753edd444ae1d213bb207528c99539c1cc747dfde8fbeee0792635a5385 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at
 `c4a1cf5d7` and at C2 (the reviewer read `[]` and `['R-1100']`); `git diff --name-only <C1b> <C2>`,
 which must name exactly the paths of the table; and at C3, the ledger at C2 is a byte-exact prefix
 of the ledger at C3 and what C3 adds to it is exactly "\n" plus one line beginning
 `Landed: R-1100 — ` and ending in "\n".

G3 THE CODE — `python3 -m ruff check packages/orchestration/ui_server.py
 tests/ui_server/test_story_section.py tests/ui_contracts/test_story_panel_contract.py
 .agent/authored/f039-r5-render_measure.py .agent/authored/f039-r5-mutations.py` at C8, with its
 real exit code. Then report, quoted from the commits, the three docstrings of S1, the whole of
 `storyPlayer.ts`, the panel's timer effect, its Play and its keydown listener, and the shell's and
 the right panel's changed lines.

G4 THE TESTS AND THE RENDER — in the primary checkout at C8, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C1a to C2 of
 this round and the reviewer's own version of C3 to C6, and read `2344 passed, 10 skipped` at real exit code
 0. Every skip of that run which names `node_modules`, `dist` or vitest is a toolchain node a fresh
 worktree lacks, and in the primary checkout each must PASS rather than skip; they run vitest,
 `tsc --noEmit` and eslint over the whole of `apps/ui`. Report every `SKIPPED` line and the node
 count of each Python test file this round adds or grows. Then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0. Then
 `python3 .agent/authored/f039-r5-render_measure.py /home/decodeux/Repos/remedy`, whose whole
 output C7 saves: it must print `RENDER: 8 of 8 checks pass` and exit 0, and afterwards
 `.remedy-wt/f039-render-run` must be gone and `git status --porcelain` empty. Report the
 screenshot's path and size. The reviewer ran its own version of this render over its own version of
 the panel and read 8 of 8.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r5-mutations.py`, following your round 4 tool's
 route, runs vitest over the WORKTREE's `storyPlayer.test.ts` and `pytest` over
 `tests/ui_contracts/test_story_panel_contract.py` and `tests/ui_server/test_story_section.py`,
 prints one line per mutation with each runner's exit code and failed count, controls first and
 last, `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 `storyBeatsAt` answers every beat of the card;
  m2 `storyPlayStart` restarts only when the scrub is LIVE;
  m3 `storyPlayStart` always answers -1;
  m4 `storyPositionLabel` counts chapters from 0;
  m5 `storyWalk`'s frames carry a wait of 0;
  m6 the panel's timer cleanup no longer clears the timeout;
  m7 the panel renders in place, without `createPortal`;
  m8 the shell mounts the panel inside `<main>`, after the phase timeline;
  m9 the Story button is removed from `RightLivePanel.tsx`;
  m10 `_build_story_section` reads `load_config()` instead of `get_config()`, R-1100's own proof.
 Run it on `git worktree add --detach .remedy-wt/f039-r5-mut <C8>` and report its whole output.
 EVERY mutation must be red; a green one is reported as green, and you then add the test that
 catches it before C9 and re-run. Then remove the worktree, `git worktree prune`, and report
 `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C9: `git status --porcelain`, which must be empty;
 `git log --oneline -n 11`, which must show C9 to C1a and `c4a1cf5d7` in order (more lines if a
 commit was split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must
 be EMPTY. These readings go in your reply, since C9 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C8 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 1 of feature F039, round 5, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 5
with the resolution of R-1100, then T003: the export command and its build, beginning with the font
licensing finding before any font is bundled. State the open-findings count, 1 (R-1100, landed and
awaiting review), and the operator-questions count, 1.
