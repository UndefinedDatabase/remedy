STEP F039 R1 — CLAIM F039 AND LAND T001: the story's chapters from the phase bar's reading, their key-event clusters, the title templates, their goldens and guard

GOAL
Pull request 292 is merged; `main` is at `4d60eb84`. The first unchecked STATUS line is F286, the
fifth findings paydown, and no finding is open, so DECISION F039 D2 moves F286 one feature down
again and F039 is claimed. Cut F039's branch, claim it, re-head the live review record, book
F038's round 15 verdict, and record DECISIONS F039 D1 and D2. Then land T001 in a NEW module
`apps/ui/src/components/story/storyChapters.ts`: the chapters of a job's event ledger read from
the phase bar's own phase reading, the bar's key events grouped into clusters, the split of a phase
dense in key events, and the title templates — with vitest goldens on fixture ledgers and the demo
recording, and a Python guard. Nothing renders the module yet: no component, route, command, event
name or Python module changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the module, its tests, its guard and the mutation tool yourself against S1 to S6 below. Only
the `.agent/` records and the two roadmap files travel as payloads. Read DECISION F039 D1 in the
claim diff before you write code: it is the design this specification implements. Before you write
anything, read whole: `apps/ui/src/components/timeline/phaseMapping.ts` and its test
`phaseMapping.test.ts`; `apps/ui/src/components/graph/brainOntology.ts` (`BrainEventRow`,
`BrainTaskSeed`); `apps/ui/src/components/graph/brainDemoRecording.ts`;
`apps/ui/src/components/graph/brainReducer.fixtures.ts` (`row`, `GOLDEN_B_*`);
`apps/ui/src/api/humanizeCatalog.ts`; `tests/ui_contracts/test_phase_mapping.py`; and the
mutation tool `.agent/authored/f024-r1-mutations.py`, whose vitest route G5 reuses.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r1-dry/`, `.remedy-wt/f039-r1-sim/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script (`subprocess.run(...,
env=...)`), never on a command line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `4d60eb84e`. Report all three. Then
   `git checkout -b feature/f039-story-replay-mode` and report the branch. Do NOT pull: the Open
   PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 173 | 20231 | 5c82fad2f5549ebd00ee6b115906341f50adac892f0ed8dc8faeafe1495cb19d |
| context.md | 35 | 1456 | 5b0ab13d3ad220d97ca7c2163246228fc2bb5c96c0143ee847e358384b875c42 |
| plan.md | 34 | 1285 | 31c0d2d4cb1ca021bc43cd25c9d2d4bf0112be5f59f0844ab9a4c133fd63a597 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`4d60eb84` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F038's round 15 gate entry
appended), `docs/roadmap/STATUS.md` (F039's line moved from under the second Tier 5 heading to
directly after F038's line, reading `[~]`), `docs/roadmap/features/T2_F286.md` (one two-line
note) and `.agent/decisions.md` (DECISIONS F039 D1 and D2 appended).

THE SPECIFICATION — TypeScript, pure: no React, no DOM, no `Date`, no `Math.random`, no `window.`,
`document.` or `fetch(`.
S1 THE MODULE, a NEW FILE at `apps/ui/src/components/story/storyChapters.ts`. A header comment
   naming T5_F039.md T001 and DECISION F039 D1, with one sentence stating that Remedy deliberately
   writes no chapter prose of its own beyond the title table. It imports from exactly two module
   specifiers: the types `BrainEventRow` and `BrainTaskSeed` from `"../graph/brainOntology"`, and
   `extractSubGlyphs`, `readPhases`, `TIMELINE_PHASES` and the types `SubGlyph` and
   `TimelinePhase` from `"../timeline/phaseMapping"`.
S2 THE CONSTANTS. `export const STORY_CHAPTER_KEY_EVENT_LIMIT = 6;` and
   `export const STORY_CLUSTER_SEQ_GAP = 2;`, each under a one-line comment saying what it bounds.
   `export const STORY_CHAPTER_TITLES: Readonly<Record<TimelinePhase, string>> = {` followed by
   exactly one line per phase in the order of `TIMELINE_PHASES`, each of the form
   `  <phase>: "<title>",` — job `The start`, planning `The plan`, build `The build`, test
   `The tests`, review `The review`, finalized `The finish` — and a closing `};` at column 0. Its
   comment says a title names the phase and never its outcome.
S3 THE TYPES. `export interface StoryCluster { firstSeq: number; lastSeq: number; events: readonly
   SubGlyph[] }` and `export interface StoryChapter { phase: TimelinePhase; part: number; parts:
   number; title: string; startSeq: number; endSeq: number; clusters: readonly StoryCluster[] }`,
   `endSeq` exclusive, one field per line with a comment on the interface.
S4 THE TITLE. `storyChapterTitle(phase, part, parts): string` is the table's title when `parts` is
   1, else the template literal `${title}, part ${part} of ${parts}`, which is the module's ONLY
   template literal. No other double-quoted string in the module outside the title table holds a
   letter, a space and a letter: the module writes no other sentence.
S5 THE CLUSTERS. `clusterKeyEvents(events: readonly SubGlyph[]): StoryCluster[]` takes key events
   already in seq order and starts a new cluster wherever an event's seq exceeds the previous
   event's seq by MORE than `STORY_CLUSTER_SEQ_GAP`; each cluster's `firstSeq` and `lastSeq` are
   its first and last event's seq. `[]` for no event.
S6 THE CHAPTERS. `buildStoryChapters(jobId: string, tasks: readonly BrainTaskSeed[], rows: readonly
   BrainEventRow[]): StoryChapter[]` reads `readPhases(jobId, tasks, rows)` over the WHOLE ledger
   and returns `[]` when its `lastSeq` is null. The key events are `extractSubGlyphs(rows)`. For
   every phase in `TIMELINE_PHASES` order that has a span: `start` is the span's `startSeq`, `end`
   its `endSeq` or, when that is null, `lastSeq + 1`; a phase with `start >= end` gives no chapter.
   The phase's key events are those with `start <= seq < end`. With `n` of them and the limit `L`,
   `parts` is `max(1, ceil(n / L))`; part `k`, counted from 1, holds key events `(k-1)L` to `kL-1`;
   its `startSeq` is `start` for part 1 and its own first key event's seq otherwise; its `endSeq` is
   `end` for the last part and the next part's first key event's seq otherwise; its `title` is
   `storyChapterTitle(phase, k, parts)`; and its `clusters` are `clusterKeyEvents` of its OWN key
   events. Chapters come out phase by phase, part by part.

THE TESTS. A NEW FILE `apps/ui/src/components/story/storyChapters.test.ts`, vitest, whose header
comment says every expected reading is a literal HAND-DERIVED from the rules and the phase readings
`phaseMapping.test.ts` pins, never computed by the code under test. At least, one test each: the
title table and both constants as whole literals; `storyChapterTitle` bare for one part and
`The review, part 2 of 3`; `clusterKeyEvents` of `[]`, and of events at seqs 1, 3 and 6 giving two
clusters, `{1, 3}` and `{6, 6}`; the demo recording, `brainDemoRows()` with its two task ids seeded
`pending`, as ONE whole literal of the chapter list in which every key event is a full `SubGlyph` —
build `[0, 1)` with no cluster, review `[1, 9)` with clusters `{1, 3}` and `{6, 8}`, each a failure
and its heal of one task, and finalized `[9, 10)` titled `The finish`; `GOLDEN_B_ROWS`, a stopped
run that never finishes — build `[1, 2)` and review `[2, 10)` with clusters holding seqs 2, 3, 4
and 6, then 9; the ledger of `phaseMapping.test.ts`'s "a planned job walks Planning, Build and Test"
case — `The plan`, `The build` and `The tests` holding one cluster of two failures with their catalog
lines; a review of eight key events (seven `needs_repair` rounds and a pass) splitting into parts
of six and two with both part titles, followed by `The finish`; a review of exactly six key events
staying whole; rows with no marker giving one `The start` chapter; an empty ledger giving `[]`; the
chapters of the demo recording and of `GOLDEN_B_ROWS` tiling the ledger from its first seq to one
past its last with no gap; and two builds of the same ledger equal with the rows unchanged.
A NEW FILE `tests/ui_contracts/test_story_chapters.py`, a guard whose docstring names T5_F039.md
T001 and DECISION F039 D1 and which strips `//` and `/* */` comments before reading the module: the
title table's keys equal `TIMELINE_PHASES` read from `phaseMapping.ts`, in order, and its values the
six titles; the module's import specifiers are exactly the two of S1, it calls `readPhases(` and
`extractSubGlyphs(`, and none of the purity words above occurs; and outside the title table no
double-quoted literal holds a letter, a space and a letter, and the template literals are exactly
the one of S4.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f039-r1-block.md` := this block, and `.agent/authored/f039-r1-plan.md` and
  `.agent/authored/f039-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F039 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 69. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f039-r1-claim.diff` := claim.diff.
  Subject: `F039 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 173.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F039 R1 C2: claim F039, move F286 behind it, book F038 R15, record D1 and D2`
  Expected by `git show --numstat` (insertions and deletions): 13/15 context.md, 71/0 decisions.md, 23/21 live_review.md, 21/13 plan.md, 1/1 STATUS.md, 2/0 T2_F286.md.

C3 — THE MODULE: `apps/ui/src/components/story/storyChapters.ts`, then `git add` it — an
  untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F039 R1 C3: chapter a job's ledger by the phase bar's reading, with key-event clusters`

C4 — THE TESTS AND THE TOOL: `apps/ui/src/components/story/storyChapters.test.ts`,
  `tests/ui_contracts/test_story_chapters.py`, and your mutation tool (G5) saved as
  `.agent/authored/f039-r1-mutations.py`.
  Subject: `F039 R1 C4: golden the story's chapters, guard their titles, add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F039 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f039-story-replay-mode`. Do NOT create a pull request: the
  branch opens one at F039's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F286.md`,
   `.agent/decisions.md`, `.agent/plan.md`, `.agent/context.md`, the two files under
   `apps/ui/src/components/story/`, `tests/ui_contracts/test_story_chapters.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 4d60eb84e` at the
   branch tip after C5. Do NOT touch any other file under `apps/`, anything under `packages/`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `docs/ui/design_reference/` or `docs/roadmap/features/T5_F039.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F039's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f039-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f039-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2421566 | 01e6b463bc6dbbde543313a6f974ee918c2262c5bf792aa36bd5fd4b7b195f14 |
 | .agent/live_review.md | 325814 | be9f7300f14f4f9efb925d0e14b0ee2b7a98bf8e3b250a1c42c82ff55abac270 |
 | docs/roadmap/STATUS.md | 56978 | e8119679658dd57c1db6d5e0314d6caf9dc63e4f5b5938208a104e24896ac03c |
 | docs/roadmap/features/T2_F286.md | 2570 | 0a75e8e61bca9afd3d23d5a9290af21e631bc6fb105860a901bc02c063a72654 |
 | .agent/plan.md | 1285 | 31c0d2d4cb1ca021bc43cd25c9d2d4bf0112be5f59f0844ab9a4c133fd63a597 |
 | .agent/context.md | 1456 | 5b0ab13d3ad220d97ca7c2163246228fc2bb5c96c0143ee847e358384b875c42 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT read with `git show <commit>:<path>`, at
 `4d60eb84e` and at C2 (the reviewer read `[]` at both); at C2 the ledger has exactly one line
 reading `## Findings` and exactly one reading `## Steps`, and its last non-empty line begins
 `Gate: F038 R15 — `; the STATUS lines of F038, F039 and F286 at C2 read back with their line
 numbers, where F039's must read `- [~] F039 — Story/replay mode` directly after F038's and before
 F286's, and `F039` must occur on exactly one line of the file; and `git diff --name-only <C1b>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_story_chapters.py` at C4, with its
 real exit code. Then report, quoted from `git show <C3>`, the title table and the whole of
 `buildStoryChapters`, and from `git show <C4>` the demo recording's golden.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/orchestration/test_feature_mission_adapter.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_review_archive_authority.py tests/orchestration/test_development_artifact_boundary.py tests/test_command_catalog.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C1a to C2 of
 this round and the reviewer's own version of the module and its tests, and read
 `1861 passed, 10 skipped` at real exit code 0. Your count differs from it by what your own tests hold, so
 report the node count of `tests/ui_contracts/test_story_chapters.py` by `--collect-only -q`. FOUR
 of the simulation's skips are toolchain nodes a worktree cannot run and the primary checkout can,
 and each must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint
 at zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs the
 UI's whole unit suite and so your new test file. Report every `SKIPPED` line the `-rs` summary
 prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r1-mutations.py` takes a worktree path and
 follows `.agent/authored/f024-r1-mutations.py`'s route: vitest runs over the WORKTREE's
 `storyChapters.test.ts` from the primary `apps/ui` with `node_modules/.bin/vitest` and a
 plain-object scratch config under `.remedy-wt/f039-r1-mutscratch/` whose `root` is the primary
 `apps/ui` and whose `cacheDir` lies under that scratch directory; the guard runs under
 `python3 -B -m pytest` from the worktree's root with the worktree's root first on `PYTHONPATH`.
 For each mutation below it edits `storyChapters.ts` INSIDE the worktree (asserting its FROM text
 occurs exactly once), runs both, restores the bytes, and prints one line per mutation: its label,
 each runner's exit code and failed count. It runs an unmutated control first and last, ends with
 `restored byte-identical: True` and a final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
 <bool>`. Each is a real behaviour change:
  m1 two key events exactly two seqs apart fall into separate clusters;
  m2 a phase of exactly six key events splits;
  m3 a phase with a zero span gives a chapter;
  m4 a later part begins at its phase's start;
  m5 an earlier part ends at its phase's end;
  m6 the last chapter ends at the ledger's last seq instead of one past it;
  m7 a split phase's titles lose their part numbers;
  m8 heals are dropped from the key events;
  m9 clusters are read over the whole phase instead of inside a part;
  m10 Finalized's title reads `The review`;
  m11 the module reads the clock (a `void Date.now();` statement added);
  m12 the title table's `test` and `review` lines swap places.
 Run it: `git worktree add --detach .remedy-wt/f039-r1-mut <C4>`, then
 `python3 -B .agent/authored/f039-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r1-mut`
 and report its whole output. EVERY mutation must be red in at least one runner; a mutation that
 stays green is reported as green, never papered over, and you then add the test that catches it in
 C4 before C5 and re-run the tool. Then `git worktree remove --force .remedy-wt/f039-r1-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `4d60eb84e` in that
 order (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal
 your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of
feature F039, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002's first round: the narration card for a cluster, its line source settled between
the humanize catalog and F255's narration, and its sync to the scrub position. State the
open-findings count, 0, and the operator-questions count, 1.
