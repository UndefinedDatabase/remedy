STEP F039 R4 — BOOK ROUND 3 WITH R-1099's RESOLUTION, AND LAND THE STORY'S DATA PATH: two pacing keys and the dashboard's `story` section, a budget tick's figures on its feed row, and the pure story view

GOAL
Round 3 is reviewed PASS at `9cd7cbfd`. Book its gate entry and R-1099's resolution and record
DECISION F039 D5 with the plan. Then land what the in-app story needs from the data it reads: two
configuration keys for the autoplay pacing, served as the dashboard's `story` section and kept raw
by the browser; the figures of a `budget.tick` frame carried on its own feed row, so a card can read
the cost so far; and a NEW pure module `apps/ui/src/components/story/storyView.ts` that assembles a
job's story — chapters, cards, the seqs autoplay steps over, and the decoded pacing — with tests and
a guard binding the two languages' halves of the pacing. Nothing renders the story yet: no
component, no mount, no command and no event name changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code, its tests, the guard and the mutation tool yourself against S1 to S5 below. Only the
`.agent/` records travel as payloads. Read DECISION F039 D5 in the records diff before you write
code. Before you write anything, read whole: `apps/ui/src/api/feedRow.ts` and its test,
`apps/ui/src/api/budgetTick.ts`, the `ConfigKeySpec` entries `chat.model_written` and
`tour.model_written` and `render_environment_guide` in `packages/orchestration/config.py`,
`_build_dashboard` and `_build_budget_final` in `packages/orchestration/ui_server.py`,
`tests/ui_server/test_budget_final_section.py`, `normalizeDashboardPayload` and the fallback
dashboard in `apps/ui/src/api/remedyApi.ts` with `makeDashboardPayload` in its test, the
`RemedyDashboard` line of `apps/ui/src/api/types.ts`, the three modules under
`apps/ui/src/components/story/`, `tests/ui_contracts/test_cost_metric_render.py`'s single-home test,
and your round 3 tool `.agent/authored/f039-r3-mutations.py`, whose route G5 reuses.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r4-dry/`, `.remedy-wt/f039-r4-sim/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script, and inside a test with
`monkeypatch`, never on a command line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `9cd7cbfdf`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 34 | 1301 | f40b22ae09bffae231443379422a73af77faf2c930836fc51da5d6008cdd8319 |
| records.diff | 57 | 7748 | ad32da0164e9805ed7955cb2b293a106f46aa05428326c6b631bf3b85065c56a |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `9cd7cbfd` into which it wrote the edits. It
appends to `.agent/live_review.md` round 3's gate entry and R-1099's `Done:` paragraph, and to
`.agent/decisions.md` DECISION F039 D5.

THE SPECIFICATION. No `except Exception` and no `# noqa: BLE001` in Python; TypeScript under
`components/story/` stays pure (no React, DOM, clock, timer, `Math.random` or `fetch(`).
S1 THE FEED ROW. `FeedRow` in `apps/ui/src/api/feedRow.ts` gains an optional field
   `budget?: BudgetTickFigures` under a comment naming DECISION F039 D5, and `feedRowOf` sets it from
   `budgetTickFiguresOf(frame)` (imported from `./budgetTick`; the type from `./costMetric`) ONLY
   when that answers an object: on every other row the key is absent, not `undefined`. No figure
   field is named in the file.
S2 THE KEYS. `packages/orchestration/config.py` gains, directly before `tour.model_written`,
   `story.step_ms` (`REMEDY_STORY_STEP_MS`, `int`, default 420) and `story.chapter_pause_ms`
   (`REMEDY_STORY_CHAPTER_PAUSE_MS`, `int`, default 1600), each described in one plain sentence
   naming F039 that says the browser keeps a value from 50 to 10000 and its default otherwise; then
   `docs/guides/environment.md` := `render_environment_guide()` of the edited registry.
S3 THE SECTION. `packages/orchestration/ui_server.py` gains
   `_build_story_section() -> dict[str, Any]`, whose docstring names F039 T002 and DECISION F039 D5,
   importing `get_config` inside the function as the file's other config reads do, and answering
   `{"step_ms": <story.step_ms>, "chapter_pause_ms": <story.chapter_pause_ms>}`; `_build_dashboard`
   gains `"story": _build_story_section(),` directly after its `"project_summary"` entry.
   In the browser, `RemedyDashboard` gains the OPTIONAL field `story?: unknown` (a required field
   would break every test fixture that builds a dashboard), `normalizeDashboardPayload` carries
   `story: dashboard.story ?? null` under a comment saying `storyPacingOf` is its one reader, and
   the fallback dashboard carries `story: null`.
S4 THE VIEW, a NEW FILE at `apps/ui/src/components/story/storyView.ts`, header naming T5_F039.md
   T002 and DECISION F039 D5. Exports `interface StoryView { chapters: readonly StoryChapter[];
   cards: readonly NarrationCard[]; seqs: readonly number[]; pacing: StoryPacing }`;
   `storyTicksOf(rows: readonly BrainEventRow[]): StoryTick[]`, one tick per row of
   `orderedLedger(rows)` whose `budget` is a plain object (not null, not an array), in that order;
   and `buildStoryView(jobId, tasks: readonly BrainTaskSeed[], rows, ownership: OwnershipView | null,
   pacing: unknown): StoryView`, whose chapters are `buildStoryChapters(jobId, tasks, rows)`, cards
   `buildNarrationCards(chapters, rows, storyTicksOf(rows), ownership)`, seqs
   `orderedLedger(rows).map((row) => row.seq)`, and pacing `storyPacingOf(pacing)`.
S5 THE GUARD, a NEW FILE `tests/ui_contracts/test_story_view.py`, docstring naming F039 T002 and
   DECISION F039 D5, stripping comments first: `set(_build_story_section())` is exactly `step_ms` and
   `chapter_pause_ms` and each occurs as a double-quoted literal in `storyAutoplay.ts`;
   `get_key_spec("story.step_ms").default` equals `STORY_STEP_MS` and that of
   `story.chapter_pause_ms` equals `STORY_CHAPTER_PAUSE_MS`, both read from `storyAutoplay.ts`;
   `storyView.ts`'s specifiers, read with `ts_import_specifiers`, are exactly
   `../../api/costMetric`, `../../api/ownership`, `../graph/brainOntology`,
   `../timeline/phaseMapping`, `./storyAutoplay`, `./storyChapters` and `./storyNarration`, and no
   purity word occurs in it; and `feedRow.ts` holds `budgetTickFiguresOf(frame)`.

THE TESTS. In `apps/ui/src/api/feedRow.test.ts`: a `budget.tick` frame's row carries its budget
object unchanged, and `"budget" in row` is false for another kind carrying a `budget` and for a tick
whose `budget` is an array. In `apps/ui/src/api/remedyApi.test.ts`: `story` is carried raw from
`makeDashboardPayload({ story: ... })` and is `null` when absent. A NEW FILE
`tests/ui_server/test_story_section.py`: the section reads 420 and 1600 with both variables unset,
300 and 2500 with them set through `monkeypatch.setenv` and `reset_config()` from
`packages.orchestration.config` (resetting again afterwards), and `_build_dashboard` of a
`JobPlan` with `_load_events` patched to `[]` carries the section. A NEW FILE
`apps/ui/src/components/story/storyView.test.ts`, HAND-DERIVED: ticks read from feed rows of
`budget.tick` frames given out of seq order, skipping another kind and a string budget; no tick
from hand-made rows whose `budget` is an array or a string; the demo recording's view — the titles
`The build`, `The review` and `The finish`, two cards in chapter 1 at seqs 1 to 3 and 6 to 8 with no
cost, seqs 0 to 9, and a pacing of `{step_ms: 300, chapter_pause_ms: 1}` decoding to 300 and 1600;
the demo recording with its seq 2 replaced by a `budget.tick` row of `spent_usd` 0.1, basis cost
`actual`, giving both cards `Cost so far: $0.10`; and rows given out of order with a repeated seq
giving ascending, distinct seqs.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6, C7 and C8, in this order.
C1a — `.agent/authored/f039-r4-block.md` := this block and `.agent/authored/f039-r4-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F039 R4 C1a: copy round 4 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 34; STOP rather than
  commit at 500 or more.
C1b — `.agent/authored/f039-r4-records.diff` := records.diff. Subject: `F039 R4 C1b: copy round 4
  records diff into .agent/authored/`. Expected insertions: 57.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F039 R4 C2: book
  round 3 and R-1099, record D5`. Expected by `git show --numstat`: 37/0 decisions.md, 4/0 live_review.md, 7/6 plan.md.
C3 — S1 and its feed-row tests. Subject: `F039 R4 C3: carry a budget tick's figures on its feed row`.
C4 — S2, the Python half of S3, and `tests/ui_server/test_story_section.py`. Subject: `F039 R4 C4:
  serve the story's pacing keys as the dashboard's story section`.
C5 — the browser half of S3 and its test. Subject: `F039 R4 C5: keep the dashboard's story section
  for the story`.
C6 — S4, S5 and `storyView.test.ts`. Subject: `F039 R4 C6: assemble a job's story from its ledger,
  ownership and pacing`.
C7 — your mutation tool (G5) as `.agent/authored/f039-r4-mutations.py`. Subject: `F039 R4 C7: add
  the mutation tool for the story's data path`.
C8 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R4 C8:
  rewrite handoff for round 4`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `apps/ui/src/api/feedRow.ts`,
   `apps/ui/src/api/feedRow.test.ts`, `apps/ui/src/api/types.ts`, `apps/ui/src/api/remedyApi.ts`,
   `apps/ui/src/api/remedyApi.test.ts`, `packages/orchestration/config.py`,
   `packages/orchestration/ui_server.py`, `docs/guides/environment.md`, the two new files under
   `apps/ui/src/components/story/`, `tests/ui_server/test_story_section.py`,
   `tests/ui_contracts/test_story_view.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only 9cd7cbfdf` measures after C8. Do NOT touch anything else, and in particular
   not `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or
   `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C8, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree listed at
   your step 4, and every stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as
   that gate's last action, and `git worktree list | wc -l` is reported afterwards.
7. DO NOT run the full suite: it belongs to F039's closure (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C8 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f039-r4-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2431157 | 41f1b43468e2a6bd83763072e2f7b3af29a7a4ad20a6298fdf1ae8582816b176 |
 | .agent/live_review.md | 336809 | d5fbf8bfd4aabba7e3899a34c5d2e9dbebf3ba9f3359bec9b326def89e7faf77 |
 | .agent/plan.md | 1301 | f40b22ae09bffae231443379422a73af77faf2c930836fc51da5d6008cdd8319 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at
 `9cd7cbfdf` and at C2 (the reviewer read `['R-1099']` and `[]`); and `git diff --name-only <C1b>
 <C2>`, which must name exactly the paths of the table.

G3 THE CODE — `python3 -m ruff check packages/orchestration/config.py
 packages/orchestration/ui_server.py tests/ui_server/test_story_section.py
 tests/ui_contracts/test_story_view.py .agent/authored/f039-r4-mutations.py` at C7, with its real
 exit code. Then report, quoted from the commits, `feedRowOf`'s changed lines, both `ConfigKeySpec`
 entries, `_build_story_section`, the `story` lines of `remedyApi.ts` and the whole of
 `storyView.ts`.

G4 THE TESTS — in the primary checkout at C7, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/orchestration/test_doc_staleness.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/orchestration/test_import_reachability.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/test_no_orphan_modules.py tests/test_command_catalog.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C1a to C2 of
 this round and the reviewer's own version of C3 to C6, and read `2548 passed, 10 skipped` at real exit code
 0. Every skip of that run which names `node_modules`, `dist` or vitest is a toolchain node a fresh
 worktree lacks, and in the primary checkout each must PASS rather than skip. Your count differs from the reviewer's by what your own Python tests hold, so report
 the node count of each Python test file this round adds by `--collect-only -q`, and every
 `SKIPPED` line. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r4-mutations.py` takes a worktree path and
 follows your round 3 tool's route: vitest over the WORKTREE's `storyView.test.ts`,
 `storyNarration.test.ts`, `feedRow.test.ts` and `remedyApi.test.ts` from the primary `apps/ui` with
 `node_modules/.bin/vitest` and a plain-object scratch config under `.remedy-wt/f039-r4-mutscratch/`,
 and `python3 -B -m pytest` over `tests/ui_server/test_story_section.py`,
 `tests/ui_contracts/test_story_view.py` and `tests/docs/test_environment_guide.py` from the
 worktree's root with that root first on `PYTHONPATH`. For each mutation it edits the named file
 INSIDE the worktree (asserting its FROM occurs exactly once), runs both, restores the bytes, and
 prints one line per mutation: its label, each runner's exit code and failed count. It runs an
 unmutated control first and last and ends with `restored byte-identical: True` and `ALL MUTATIONS
 CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 `feedRowOf` never sets `budget`;
  m2 `feedRowOf` sets a `budget` key on every row, `undefined` where there is no tick;
  m3 `storyTicksOf` reads the rows in the order given, not `orderedLedger`'s;
  m4 `storyTicksOf` accepts an array `budget`;
  m5 `buildStoryView` hands the cards no tick;
  m6 `buildStoryView` decodes `null` instead of its pacing argument;
  m7 the view's seqs are the rows' seqs in the order given;
  m8 `normalizeDashboardPayload` carries `story: null` always;
  m9 `_build_story_section`'s `step_ms` reads `story.chapter_pause_ms`;
  m10 `story.step_ms`'s default is 400;
  m11 `_build_dashboard` omits the `story` entry;
  m12 `storyView.ts` gains the line `import "../../api/unguarded";` after its imports.
 Run it: `git worktree add --detach .remedy-wt/f039-r4-mut <C7>`, then
 `python3 -B .agent/authored/f039-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r4-mut`,
 and report its whole output. EVERY mutation must be red in at least one runner; one that stays
 green is reported as green, never papered over, and you then add the test that catches it before
 C8 and re-run the tool. Then `git worktree remove --force .remedy-wt/f039-r4-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C8: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C8 to C1a and `9cd7cbfdf` in order (more lines if a
 commit was split or added); `git worktree list | wc -l`, equal to your step 4 reading; the push's
 real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C8 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C7 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 1 of feature F039, round 4, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 4,
then T002's last part: the in-app story panel on the demo recording, driving the timeline's scrub,
with its golden walkthrough and its assumption-log entry. State the open-findings count, 0, and the
operator-questions count, 1.
