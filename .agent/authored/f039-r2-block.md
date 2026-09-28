STEP F039 R2 — BOOK ROUND 1, REPAIR R-1098, AND LAND T002's NARRATION CARDS: one card per cluster, each key event a beat with the catalog's line, its verdict and its actor, the cost so far, and the sync to the scrub position

GOAL
Round 1 is reviewed PASS at `ea7bcbdb`. Book its gate entry, register finding R-1098 and record
DECISION F039 D3 with the plan. Repair R-1098: one reader of a TypeScript module's import
statements for the UI guards, which today cannot see a bare import or a re-export. Then land
T002's first half in a NEW module `apps/ui/src/components/story/storyNarration.ts`: a narration card
per cluster of key events, each key event a beat carrying the humanize catalog's line, the
reviewer's verdict and the ownership ledger's actor where the record names exactly one, the cost so
far from the latest budget tick, and the chapter and card a scrub position shows — with vitest
goldens and a guard. Nothing renders the module yet: no component, route, command, event name or
Python module changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the module, its tests, the guard edits and the mutation tool yourself against S1 to S9
below. Only the `.agent/` records travel as payloads. Read DECISION F039 D3 and finding R-1098 in
the records diff before you write code. Before you write anything, read whole:
`apps/ui/src/components/story/storyChapters.ts` and its test; `apps/ui/src/api/costMetric.ts`
(`BudgetTickFigures`, `costMetricOf`); `apps/ui/src/api/ownership.ts` (`OwnershipView`,
`OwnershipEntry`, `OWNERSHIP_CHIP_WORDS`); `REVIEW_OUTCOME_STATE_TABLE` in
`apps/ui/src/components/graph/brainOntology.ts`; `SUB_GLYPH_TABLE` and `SubGlyphKind` in
`apps/ui/src/components/timeline/phaseMapping.ts`; `GOLDEN_B_ROWS` and `row` in
`apps/ui/src/components/graph/brainReducer.fixtures.ts`; the five guards R-1098 names; and your
round 1 tool `.agent/authored/f039-r1-mutations.py`, whose route G5 reuses.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r2-dry/`, `.remedy-wt/f039-r2-sim/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `ea7bcbdb3`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 34 | 1278 | 725bedfa64517040d58f6fe4b8d01132abad1fa73651fb1e6e19f63990b61839 |
| records.diff | 62 | 11937 | 87732cc04771fd641d66a29dbab955d3f9c8902a2d58d38e45e595424a73cba7 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `ea7bcbdb` into which it wrote the edits. It
appends to `.agent/live_review.md` round 1's gate entry and the registration of R-1098, and to
`.agent/decisions.md` DECISION F039 D3.

THE SPECIFICATION. TypeScript is pure: no React, no DOM, no `Date`, no `Math.random`, no `window.`,
`document.` or `fetch(`.
S1 R-1098, THE READER. In `tests/ui_contracts/test_phase_mapping.py`, after its path constants, a
   comment naming R-1098 and the three statement forms, then
   `TS_IMPORT_RE = re.compile(r'^(?:import|export)\s+(?:[^;]*?\s+from\s+)?"([^"]+)";$', re.MULTILINE)`
   and `def ts_import_specifiers(src: str) -> list[str]` answering `TS_IMPORT_RE.findall(src)`, the
   specifiers in order. Its own import check reads through it, and a new test
   `test_the_import_reader_reads_every_import_statement` feeds it one source holding a named import,
   a type import, a named import spread over lines, a bare import, `export * from`, `export { e }
   from` and an `export const` line, and compares the result with the six specifiers in order.
S2 R-1098, THE GUARDS. `test_timeline_scrub_contract.py`, `test_scrub_snapshots.py`,
   `test_semantic_zoom_contract.py` and `test_story_chapters.py` under `tests/ui_contracts/` import
   `ts_import_specifiers` from `tests.ui_contracts.test_phase_mapping` and read imports through it
   in place of their own `re.findall`; nothing else in them changes.
S3 THE LANDED LINE. In C3, append to `.agent/live_review.md` one blank line and then one line that
   begins `Landed: R-1098 — ` and says in one sentence what changed; it names no commit, because its
   own commit is the one that lands it. Never write a `Done:` line.
S4 THE MODULE, a NEW FILE at `apps/ui/src/components/story/storyNarration.ts`. A header comment
   naming T5_F039.md T002 and DECISION F039 D3, with one sentence stating that Remedy deliberately
   invents no narration. It imports from exactly five specifiers: `"../../api/costMetric"`
   (`costMetricOf` and the type `BudgetTickFigures`), `"../../api/ownership"` (types),
   `"../graph/brainOntology"` (types), `"../timeline/phaseMapping"` (types) and `"./storyChapters"`
   (types).
S5 THE TABLES. `export const STORY_VERDICT_LINES: Readonly<Record<string, string>> = {` with one
   line per outcome in `REVIEW_OUTCOME_STATE_TABLE`'s order, `  <outcome>: "<line>",` — pass
   `Verdict: pass`, fail `Verdict: fail`, needs_repair `Verdict: needs repair`, blocked
   `Verdict: blocked` — and `};` at column 0. `export const STORY_ACTOR_ACTIONS: Readonly<Record<
   string, string>> = {` with `  job_stopped: "job_stopped",` and
   `  task_decision_answered: "decision_answered",` and `};` at column 0. Every key is read with
   `hasOwnProperty`, never a bare lookup.
S6 THE TYPES. `StoryTick { seq: number; figures: BudgetTickFigures }`; `NarrationBeat { seq: number;
   glyph: SubGlyphKind; taskId: string; line: string; verdict: string | null; actor: string | null }`;
   `NarrationCard { chapter: number; firstSeq: number; lastSeq: number; beats: readonly
   NarrationBeat[]; cost: string | null }`, all exported.
S7 THE COST. `storyCostLine(ticks: readonly StoryTick[], seq: number): string | null` takes the tick
   with the greatest seq at or before `seq`; none → null. `costMetricOf` of its figures is null when
   its `display` equals `costMetricOf({}).display` (so no second copy of the dash exists); else the
   template literal `Cost so far: ${estimated ? "~" : ""}${display}${unit is tokens ? " tokens" : ""}`,
   the module's ONLY template literal.
S8 THE CARDS. `buildNarrationCards(chapters: readonly StoryChapter[], rows: readonly BrainEventRow[],
   ticks: readonly StoryTick[], ownership: OwnershipView | null): NarrationCard[]` gives one card per
   cluster, chapter by chapter and cluster by cluster: `chapter` the chapter's index, `firstSeq` and
   `lastSeq` the cluster's, `cost` `storyCostLine(ticks, lastSeq)`, and one beat per key event with
   its seq, glyph, task and line. A beat's `verdict` is `STORY_VERDICT_LINES[outcome]` when the row
   of its seq (the first row holding that seq) is a `task_round_completed` whose outcome the table
   holds, else null. Its `actor` is null unless `ownership` is not null, its `error` is `""`, the
   event's kind is a key of `STORY_ACTOR_ACTIONS`, and — counting, for `decision_answered`, only
   events and entries of the event's own task — the chapters' key events hold exactly ONE event of
   that kind and the view exactly ONE entry of the mapped action; then it is that entry's
   `sentence`.
S9 THE SYNC. `chapterAt(chapters, position): number` is the index of the chapter with
   `startSeq <= position < endSeq`, else -1. `cardAt(chapters, cards, position): NarrationCard | null`
   is the LAST card whose `chapter` is `chapterAt(chapters, position)` and whose `firstSeq` is at or
   before `position`, else null.
No double-quoted string in the module outside `STORY_VERDICT_LINES` holds a letter, a space and a
letter: the module writes no other sentence.

THE TESTS. A NEW FILE `apps/ui/src/components/story/storyNarration.test.ts`, vitest, whose header
says every expected reading is HAND-DERIVED. At least, one test each: both tables as whole literals;
`storyCostLine` over ticks at seqs 1 (`spent_usd` 0.1, basis cost `actual`), 5 (`spent_usd` 0.25), 7
(`{}`) and 8 (`spent_tokens` 1500, basis tokens `actual`) at seqs 0, 1, 6, 7 and 9 — null,
`Cost so far: $0.10`, `Cost so far: ~$0.25`, null and `Cost so far: 1.5k tokens` — and null for no
tick; the demo recording's cards as ONE whole literal, two cards in chapter 1, each a
`needs repair` beat and a `pass` beat of one task with the catalog's review line, no actor and no
cost; `GOLDEN_B_ROWS` with ticks at 5 (`spent_usd` 0.25) and 8 (`spent_usd` 0.5, basis cost `actual`)
and a view holding one `job_stopped` entry, as ONE whole literal — the first card's beats at seqs 2,
3, 4 and 6 read `Verdict: fail`, `Verdict: needs repair`, the stop with the entry's sentence as
actor and `Verdict: pass`, cost `Cost so far: ~$0.25`, and the second card's one decision beat at
seq 9, cost `Cost so far: $0.50`; the stop names no actor for a null view, an unreadable one, two
`job_stopped` entries or only a `job_paused` entry; the planned-job ledger of `phaseMapping.test.ts`
gives one card whose two failure beats carry NO verdict, though each row's outcome is `fail`; an
answered decision names its entry's sentence for its own task and nobody for another task's entry;
and over the demo recording, positions -1, 0, 1, 2, 5, 6, 8, 9 and 10 read chapters -1, 0, 1, 1, 1,
1, 1, 2, -1 and cards starting at none, none, 1, 1, 1, 6, 6, none and none.
A NEW FILE `tests/ui_contracts/test_story_narration.py`, a guard whose docstring names T5_F039.md
T002 and DECISION F039 D3, stripping comments first: `STORY_VERDICT_LINES`'s keys equal
`REVIEW_OUTCOME_STATE_TABLE`'s, in order, and its values the four lines; `STORY_ACTOR_ACTIONS` is
the two pairs, its keys among `SUB_GLYPH_TABLE`'s keys and its values among `OWNERSHIP_CHIP_WORDS`'s;
the module's specifiers, read with `ts_import_specifiers`, are exactly the five of S4, it calls
`costMetricOf(`, and no purity word occurs; and outside the verdict table no double-quoted literal
holds a letter, a space and a letter and the one template literal begins `Cost so far: ${`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6 and C7, in this order.
C1a — `.agent/authored/f039-r2-block.md` := this block and `.agent/authored/f039-r2-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F039 R2 C1a: copy round 2 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 34; STOP rather than
  commit at 500 or more.
C1b — `.agent/authored/f039-r2-records.diff` := records.diff. Subject: `F039 R2 C1b: copy round 2
  records diff into .agent/authored/`. Expected insertions: 62.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F039 R2 C2: book
  round 1, register R-1098, record D3`. Expected by `git show --numstat`: 42/0 decisions.md, 4/0 live_review.md, 8/8 plan.md.
C3 — S1, S2 and S3. Subject: `F039 R2 C3: read every import statement in the UI guards (R-1098)`.
C4 — S4 to S9. Subject: `F039 R2 C4: compose the story's narration cards and sync them to the
  scrub position`.
C5 — the two new test files. Subject: `F039 R2 C5: golden the narration cards and guard their
  words`.
C6 — your mutation tool (G5) as `.agent/authored/f039-r2-mutations.py`. Subject: `F039 R2 C6: add
  the mutation tool for the narration cards and R-1098`.
C7 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R2 C7:
  rewrite handoff for round 2`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the five guards S1 and S2 name,
   the two new files under `apps/ui/src/components/story/`, `tests/ui_contracts/test_story_narration.py`
   and `.agent/handoff.md`. Report the list `git diff --name-only ea7bcbdb3` measures after C7. Do
   NOT touch any other file under `apps/`, `tests/` or `docs/`, anything under `packages/`,
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
 the PAYLOADS table; then compare each `.agent/authored/f039-r2-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2425281 | dc09ed888ba2776338e28a5c9f84739f99b021820bd2b04c9fb04a1deb26c52a |
 | .agent/live_review.md | 329589 | b748ff6b7053ed80ff94e46d1427e571a96fb00b3c30291b720f8655b6b49059 |
 | .agent/plan.md | 1278 | 725bedfa64517040d58f6fe4b8d01132abad1fa73651fb1e6e19f63990b61839 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at
 `ea7bcbdb3` and at C2 (the reviewer read `[]` and `['R-1098']`); `git diff --name-only <C1b> <C2>`,
 which must name exactly the paths of the table; and at C3, the ledger at C2 is a byte-exact prefix
 of the ledger at C3 and what C3 adds to it is exactly "\n" plus one line beginning
 `Landed: R-1098 — ` and ending in "\n".

G3 THE CODE — `python3 -m ruff check` over the six guard files this round touches or adds and the
 tool, at C6, with its real exit code. Then report, quoted from the commits, `TS_IMPORT_RE` with
 its comment, the whole of `buildNarrationCards`, `storyCostLine` and `cardAt`, and the golden B
 test.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/orchestration/test_feature_mission_adapter.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_review_archive_authority.py tests/orchestration/test_development_artifact_boundary.py tests/test_command_catalog.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C1a to C2 of
 this round and the reviewer's own version of C3 to C5, and read `1870 passed, 10 skipped` at real exit code
 0; five of those skips are toolchain nodes a worktree cannot run, and in the primary checkout each
 must PASS. Your count differs from the reviewer's by what your own guards hold, so report the node
 count of each Python guard this round adds or edits by `--collect-only -q`, and every `SKIPPED`
 line. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0 — R-1098 is Low, and stays open until the reviewer resolves it.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r2-mutations.py` takes a worktree path and
 follows your round 1 tool's route: vitest over the WORKTREE's two `apps/ui/src/components/story/`
 test files from the primary `apps/ui` with `node_modules/.bin/vitest` and a plain-object scratch
 config under `.remedy-wt/f039-r2-mutscratch/`, and `python3 -B -m pytest` over the six guards of
 `tests/ui_contracts/` this round touches or adds, from the worktree's root with that root first on
 `PYTHONPATH`. For each mutation it edits the named file INSIDE the worktree (asserting its FROM
 occurs exactly once, or prepending a line), runs both, restores the bytes, and prints one line per
 mutation: its label, each runner's exit code and failed count. It runs an unmutated control first
 and last and ends with `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED
 CLEANLY: <bool>`. In `storyNarration.ts`, each a real behaviour change:
  m1 the cost line reads the earliest tick at or before the seq instead of the latest;
  m2 the cost line reads a tick one seq past the cluster;
  m3 an estimated figure loses its `~`;
  m4 a token figure loses ` tokens`;
  m5 a tick with no figure gives a cost line;
  m6 every row's outcome is read as a verdict, not only a review round's;
  m7 an actor is named when two ownership entries match;
  m8 an unreadable ownership view still names an actor;
  m9 a decision's actor ignores its task;
  m10 `cardAt` shows a card of another chapter;
  m11 `cardAt` shows a card before its first key event;
  m12 `chapterAt` counts a chapter's `endSeq` as inside it;
  m13 `STORY_VERDICT_LINES` gains `  skipped: "Verdict: skipped",` after its `blocked` line;
  m14 a statement `void "no cost here";` is added inside `storyCostLine`;
 and for R-1098, m15 to m22 prepend the line `import "../../api/unguarded";` to, in turn,
 `phaseMapping.ts`, `scrubState.ts`, `timelineIndex.ts`, `timelineView.ts` and `scrubSnapshots.ts`
 under `apps/ui/src/components/timeline/`, `semanticZoom.ts` and `zoomWheel.ts` under
 `apps/ui/src/components/graph/`, and `storyChapters.ts`; and m23 restores `TS_IMPORT_RE`'s pattern
 to `^import [^;]*from "([^"]+)";$`. Run it: `git worktree add --detach .remedy-wt/f039-r2-mut <C6>`,
 then `python3 -B .agent/authored/f039-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r2-mut`,
 and report its whole output. EVERY mutation must be red in at least one runner; one that stays
 green is reported as green, never papered over, and you then add the test that catches it before
 C7 and re-run the tool. Then `git worktree remove --force .remedy-wt/f039-r2-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C7 to C1a and `ea7bcbdb3` in order (more lines if a
 commit was split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must
 be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C6 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 1 of feature F039, round 2, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 2
with the resolution of R-1098, then T002's second half: the autoplay pacing with chapter pauses, and
the in-app story mode on the demo recording. State the open-findings count, 1 (R-1098, landed and
awaiting review), and the operator-questions count, 1.
