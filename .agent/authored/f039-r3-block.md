STEP F039 R3 — BOOK ROUND 2 WITH R-1098's RESOLUTION, REPAIR R-1099, AND LAND T002's AUTOPLAY: one ledger event per step, a pause on every chapter's opening, chapter by chapter under reduced motion, and the pacing a payload may set

GOAL
Round 2 is reviewed PASS at `1e1d7352`. Book its gate entry and R-1098's resolution, register
finding R-1099 and record DECISION F039 D4 with the plan. Repair R-1099: the narration goldens never
hold two key events of one actor kind, so the half of the actor rule that counts events is
untested. Then land T002's autoplay in a NEW module `apps/ui/src/components/story/storyAutoplay.ts`:
which scrub position comes next and how long to wait for it — one ledger event per step, a chapter
pause more before every chapter's first event, chapter by chapter under reduced motion, ending at
the ledger's last seq — with its pacing defaults bound to the motion reference and a decoder of a
pacing payload; vitest goldens and a guard. Nothing renders it yet and nothing starts a timer: no
component, route, command, configuration key, event name or Python module changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the module, its tests, the guard, the R-1099 goldens and the mutation tool yourself against
S1 to S6 below. Only the `.agent/` records travel as payloads. Read DECISION F039 D4 and finding
R-1099 in the records diff before you write code. Before you write anything, read whole:
`apps/ui/src/components/story/storyChapters.ts`, `storyNarration.ts` and `storyNarration.test.ts`
beside them; `docs/ui/design_reference/motion_spec.md` and the `--remedy-dur-*` lines of
`docs/ui/design_reference/tokens.css`; `tests/ui_contracts/test_timeline_scrub_contract.py`, whose
token binding S5 follows; `ts_import_specifiers` in `tests/ui_contracts/test_phase_mapping.py`; and
your round 2 tool `.agent/authored/f039-r2-mutations.py`, whose route G5 reuses.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r3-dry/`, `.remedy-wt/f039-r3-sim/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script, never on a command
line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `1e1d7352d`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 33 | 1279 | afa5917e885bd79ceb75182809511a2afd04b244b326616d851b98bb757ae749 |
| records.diff | 55 | 9668 | 154f1182ac2eac264cd7fae867e384ff03b5ea1d5d9c08449cafb168b2b667d2 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `1e1d7352` into which it wrote the edits. It
appends to `.agent/live_review.md` round 2's gate entry, R-1098's `Done:` paragraph and the
registration of R-1099, and to `.agent/decisions.md` DECISION F039 D4.

THE SPECIFICATION. TypeScript is pure: no React, no DOM, no `Date`, no `performance.`, no
`setTimeout`, `setInterval` or `requestAnimationFrame`, no `Math.random`, no `window.`, `document.`
or `fetch(`.
S1 R-1099, THE GOLDENS. Append to `apps/ui/src/components/story/storyNarration.test.ts` one
   `describe` naming R-1099 with two tests: rows `task_run_started` t1 at 1, `job_stopped` (outcome
   `stopped`) at 2, `job_resumed` at 3 and `job_stopped` at 4, with a view of ONE `job_stopped`
   entry, give beats at seqs 2 and 4 that name NO actor; and rows `task_run_started` t1 at 1 and
   `task_decision_answered` t1 at 2 and at 3, with ONE `decision_answered` entry for t1, give beats
   at seqs 2 and 3 that name no actor. Nothing else in the file changes.
S2 THE LANDED LINE. In C3, append to `.agent/live_review.md` one blank line and then one line that
   begins `Landed: R-1099 — ` and says in one sentence what changed; it names no commit. Never write
   a `Done:` line.
S3 THE MODULE, a NEW FILE at `apps/ui/src/components/story/storyAutoplay.ts`. A header comment
   naming T5_F039.md T002 and DECISION F039 D4, saying the module owns no timer and that Remedy
   deliberately paces a story by its events and chapters, never by the events' timestamps. It
   imports the type `StoryChapter` from `"./storyChapters"` and `chapterAt` from
   `"./storyNarration"`, and nothing else. Exports: `STORY_STEP_MS = 420` and
   `STORY_CHAPTER_PAUSE_MS = 1600`, each declared alone on its line as
   `export const <NAME> = <digits>;` under a comment naming its token; `STORY_PACING_MIN_MS = 50`
   and `STORY_PACING_MAX_MS = 10000`; `interface StoryPacing { stepMs: number; chapterPauseMs:
   number }`; `STORY_PACING_DEFAULT`, the two first constants as a `StoryPacing`; and
   `interface AutoplayStep { position: number; delayMs: number }`.
S4 THE BEHAVIOUR. `storyPacingOf(raw: unknown): StoryPacing` reads `step_ms` and
   `chapter_pause_ms` from `raw` when it is a plain object, each kept only when it is a whole
   number from the MIN to the MAX inclusive and otherwise its default; it never throws.
   `autoplayStep(chapters, seqs: readonly number[], position: number, pacing: StoryPacing,
   reducedMotion: boolean): AutoplayStep | null`, `seqs` the ledger's seqs ascending, and `here`
   `chapterAt(chapters, position)`. Without reduced motion: the next seq greater than `position`,
   after `stepMs` plus `chapterPauseMs` when `chapterAt` of that seq differs from `here`; null
   when no seq is greater. With reduced motion: the start of the first chapter after `here` whose
   `startSeq` exceeds `position`, after `chapterPauseMs`; when there is none, the last seq after
   `chapterPauseMs` if it exceeds `position`; else null. `autoplayTotalMs(chapters, seqs, pacing,
   reducedMotion): number` sums the delays of the steps from position -1 until `autoplayStep`
   answers null.

THE TESTS. A NEW FILE `apps/ui/src/components/story/storyAutoplay.test.ts`, vitest, whose header
says every expected reading is HAND-DERIVED from the rules and the demo recording's chapters, build
[0, 1), review [1, 9) and finalized [9, 10). At least, one test each: the four constants and the
default as literals; `storyPacingOf` of `{step_ms: 200, chapter_pause_ms: 3000}`, of 50 and 10000,
of 49 and 10001, of 200.5 and the string "3000", and of `null`, `undefined`, `[]`, "x" and 5; with a
pacing of 100 and 1000, the whole walk from -1 over the demo recording as ONE literal, positions 0
to 9 with waits 1100, 1100, then 100 seven times, then 1100; under reduced motion from -1, 0, 4 and
9, positions 0, 1 and 9 each after 1000, then null; `autoplayTotalMs` over the demo recording with
the default pacing, 9000, and under reduced motion, 4800; the demo recording's first four rows, an
unfinished review, ending at seq 3 with and without reduced motion; and an empty ledger with no
step and a total of 0.
A NEW FILE `tests/ui_contracts/test_story_autoplay.py`, a guard whose docstring names T5_F039.md
T002 and DECISION F039 D4, stripping comments first: `STORY_STEP_MS` equals `--remedy-dur-birth`
and `STORY_CHAPTER_PAUSE_MS` equals `--remedy-dur-pulse`, both read from
`docs/ui/design_reference/tokens.css` the way `test_timeline_scrub_contract.py` reads
`--remedy-dur-fast`; the module's specifiers, read with `ts_import_specifiers`, are exactly
`./storyChapters` and `./storyNarration`, it calls `chapterAt(`, and none of the purity words above
occurs.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6 and C7, in this order.
C1a — `.agent/authored/f039-r3-block.md` := this block and `.agent/authored/f039-r3-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F039 R3 C1a: copy round 3 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 33; STOP rather than
  commit at 500 or more.
C1b — `.agent/authored/f039-r3-records.diff` := records.diff. Subject: `F039 R3 C1b: copy round 3
  records diff into .agent/authored/`. Expected insertions: 55.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F039 R3 C2: book
  round 2 and R-1098, register R-1099, record D4`. Expected by `git show --numstat`:
  33/0 decisions.md, 6/0 live_review.md, 5/6 plan.md.
C3 — S1 and S2. Subject: `F039 R3 C3: golden two events of one actor kind (R-1099)`.
C4 — S3 and S4. Subject: `F039 R3 C4: pace the story's autoplay by its events and chapters`.
C5 — the two new test files. Subject: `F039 R3 C5: golden the autoplay and bind its waits to the
  motion reference`.
C6 — your mutation tool (G5) as `.agent/authored/f039-r3-mutations.py`. Subject: `F039 R3 C6: add
  the mutation tool for the autoplay and R-1099`.
C7 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R3 C7:
  rewrite handoff for round 3`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/ui/src/components/story/storyNarration.test.ts`, the two new files under
   `apps/ui/src/components/story/`, `tests/ui_contracts/test_story_autoplay.py` and
   `.agent/handoff.md`. Report the list `git diff --name-only 1e1d7352d` measures after C7. Do NOT
   touch any other file under `apps/`, `tests/` or `docs/`, anything under `packages/`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C7, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree listed at
   your step 4, and every stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as
   that gate's last action, and `git worktree list | wc -l` is reported afterwards.
7. DO NOT run the full suite: it belongs to F039's closure (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f039-r3-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r3/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2428140 | ef7a9dc0cf2cd77b100aa5a745100f94ec2e6a64d2ab8cb7db192bb73c7fcc35 |
 | .agent/live_review.md | 334053 | dc4f21ceca6a5aeaabca335e2526128e487dee8f479ce10b07b682b0bf80a74e |
 | .agent/plan.md | 1279 | afa5917e885bd79ceb75182809511a2afd04b244b326616d851b98bb757ae749 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at
 `1e1d7352d` and at C2 (the reviewer read `['R-1098']` and `['R-1099']`); `git diff --name-only
 <C1b> <C2>`, which must name exactly the paths of the table; and at C3, the ledger at C2 is a
 byte-exact prefix of the ledger at C3 and what C3 adds to it is exactly "\n" plus one line
 beginning `Landed: R-1099 — ` and ending in "\n".

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_story_autoplay.py
 .agent/authored/f039-r3-mutations.py` at C6, with its real exit code. Then report, quoted from
 the commits, the whole of `autoplayStep` and `storyPacingOf`, and C3's two goldens.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/orchestration/test_feature_mission_adapter.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_review_archive_authority.py tests/orchestration/test_development_artifact_boundary.py tests/test_command_catalog.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C1a to C2 of
 this round and the reviewer's own version of C3 to C5, and read `1873 passed, 10 skipped` at real exit code
 0; five of those skips are toolchain nodes a worktree cannot run, and in the primary checkout each
 must PASS. Your count differs from the reviewer's by what your own guard holds, so report the node
 count of `tests/ui_contracts/test_story_autoplay.py` by `--collect-only -q`, and every `SKIPPED`
 line. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0 — R-1099 is Low, and stays open until the reviewer resolves it.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r3-mutations.py` takes a worktree path and
 follows your round 2 tool's route: vitest over the WORKTREE's three `apps/ui/src/components/story/`
 test files from the primary `apps/ui` with `node_modules/.bin/vitest` and a plain-object scratch
 config under `.remedy-wt/f039-r3-mutscratch/`, and `python3 -B -m pytest` over
 `tests/ui_contracts/test_story_autoplay.py` and `test_story_narration.py` from the worktree's root
 with that root first on `PYTHONPATH`. For each mutation it edits the named file INSIDE the
 worktree (asserting its FROM occurs exactly once), runs both, restores the bytes, and prints one
 line per mutation: its label, each runner's exit code and failed count. It runs an unmutated
 control first and last and ends with `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND
 RESTORED CLEANLY: <bool>`. No mutation may make a step answer its own position, which would never
 end `autoplayTotalMs`. Each is a real behaviour change, in `storyAutoplay.ts` unless named:
  m1 no chapter pause is ever added;
  m2 every step adds a chapter pause;
  m3 entering the first chapter from -1 adds no pause;
  m4 reduced motion is ignored;
  m5 reduced motion never steps to the last seq;
  m6 a wait of exactly 50 is refused;
  m7 a fractional wait is accepted;
  m8 the payload is read by `stepMs` rather than `step_ms`;
  m9 `STORY_STEP_MS` is 400;
  m10 a `setTimeout(() => undefined, 0);` statement is added inside `autoplayTotalMs`;
  m11 in `storyNarration.ts`, the actor check of the count of matching events is deleted — R-1099's
  own proof, green at `1e1d7352` and red once C3 lands.
 Run it: `git worktree add --detach .remedy-wt/f039-r3-mut <C6>`, then
 `python3 -B .agent/authored/f039-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r3-mut`,
 and report its whole output. EVERY mutation must be red in at least one runner; one that stays
 green is reported as green, never papered over, and you then add the test that catches it before
 C7 and re-run the tool. Then `git worktree remove --force .remedy-wt/f039-r3-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C7 to C1a and `1e1d7352d` in order (more lines if a
 commit was split or added); `git worktree list | wc -l`, equal to your step 4 reading; the push's
 real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C6 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 1 of feature F039, round 3, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 3
with the resolution of R-1099, then T002's last part: the in-app story mode on the demo recording,
the pacing's configuration keys, its golden walkthrough and its assumption-log entry. State the
open-findings count, 1 (R-1099, landed and awaiting review), and the operator-questions count, 1.
