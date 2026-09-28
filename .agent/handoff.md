# Handback — F039, round 1: claim F039, book F038 R15, and land T001 — the story's chapters, key-event clusters, title templates, goldens and guard

## Session

SESSION 1 of feature F039 · round 1 · rounds so far 1. This session ran round 1 only: the claim,
the re-head, F038 round 15's booking, and T001's pure module with its vitest goldens, its Python
guard and its mutation tool. Context self-assessment: a comfortable margin of context remained
through the round, including the full targeted pytest selection and the mutation red-proofs; the
work was not near its limit.

For the operator, in plain words: F039 (Story/replay mode) is now claimed, and its first slice is
built — a pure TypeScript module that turns a job's event ledger into chapters, following the same
phase-bar reading the timeline already uses. Nothing renders it yet: no component, no route, no
command changed this round. The findings paydown F286 was moved one feature further down the list
again, since no defect is open, exactly as DECISION F039 D2 records.

## Range

Review of `4d60eb84e`..`HEAD` (the commit that writes this file is the seventh in the range). SIX
commits precede it: C1a, C1b, C2, C3, C4a and C4b, matching the block's ordered bundle with C4
split into two parts under constraint 2 (declared below), then this handback commit (C5).

## Commits

### 4f5a713a6 F039 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r1-block.md | 301/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f039-r1-context.md | 35/0 | the context payload, copied verbatim |
| .agent/authored/f039-r1-plan.md | 34/0 | the plan payload, copied verbatim |

(measured: `git show 4f5a713a6 --numstat` reads `301 0`, `35 0`, `34 0`, total 370 — exactly the
block's own expected reading of the block's line count (301) plus 69, under the 500-line cap.)

### a704ae20b F039 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r1-claim.diff | 173/0 | the claim-diff payload, copied verbatim |

(measured: `git show a704ae20b --numstat` reads `173 0` — exactly the block's expected 173.)

### 5b7947c72 F039 R1 C2: claim F039, move F286 behind it, book F038 R15, record D1 and D2
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | 13/15 | `git apply claim.diff` re-heads the scope paragraph, then rewritten := context.md |
| .agent/decisions.md | 71/0 | claim.diff appends DECISIONS F039 D1 and D2 |
| .agent/live_review.md | 23/21 | claim.diff re-heads the heading/Steps section and appends the F038 R15 Gate entry |
| .agent/plan.md | 21/13 | claim.diff, then rewritten := plan.md (round 1's plan) |
| docs/roadmap/STATUS.md | 1/1 | claim.diff moves F039's line to `[~]` directly after F038, and drops it from Tier 5 |
| docs/roadmap/features/T2_F286.md | 2/0 | claim.diff appends the "moved behind F039" note |

(measured: `git show 5b7947c72 --numstat` reads `13 15`, `71 0`, `23 21`, `21 13`, `1 1`, `2 0` —
exactly the block's own expected reading.)

### 757fd719b F039 R1 C3: chapter a job's ledger by the phase bar's reading, with key-event clusters
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyChapters.ts | 124/0 | NEW module: S1–S6, `git add`ed so `relevant_untracked` sees a tracked file |

(measured: `git show 757fd719b --numstat` reads `124 0`; the block gave no expected reading for
C3, per its own "none is expected for C3 and C4" instruction.)

### 5c83f21a1 F039 R1 C4a: golden the story's chapters and guard their titles
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyChapters.test.ts | 242/0 | NEW vitest goldens: title table, `storyChapterTitle`, `clusterKeyEvents`, the demo recording and `GOLDEN_B_ROWS` as whole literals, the planned-job case, a hand-built 8-key-event split, a hand-built 6-key-event whole phase, the no-marker and empty-ledger edges, and the two-builds-equal check |
| tests/ui_contracts/test_story_chapters.py | 93/0 | NEW Python guard: title table vs `TIMELINE_PHASES`, the two import specifiers, the two library calls, purity, the one template literal, no stray sentence |

(measured: `git show 5c83f21a1 --numstat` reads `242 0`, `93 0`, total 335, under the 500-line cap.)

### 447dabe5b F039 R1 C4b: add the mutation tool for the story's chapters
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r1-mutations.py | 170/0 | NEW mutation tool, `m1`–`m12`, following `f024-r1-mutations.py`'s route |

(measured: `git show 447dabe5b --numstat` reads `170 0`, under the 500-line cap. C4a+C4b together
total 505 insertions, over the cap as ONE commit, which is why constraint 2 split them — declared
under Deviations below.)

## External actions

`git checkout -b feature/f039-story-replay-mode` from `main` at `4d60eb84e` (step 2). `git
worktree add --detach .remedy-wt/f039-r1-mut 447dabe5b` before G5, `git worktree remove --force
.remedy-wt/f039-r1-mut` and `git worktree prune` after it (G5) — `git worktree list | wc -l` read
62 both before and after (step 4's reading, unchanged). `git push -u origin
feature/f039-story-replay-mode` after this commit — reported in the worker's final reply, since
this file is written and C5 committed before that push, per the block's ordering.

## Verification

BEFORE ANYTHING ELSE:
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
(absent, as required)
```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
main
$ git log --oneline -1
4d60eb84e Merge pull request #292 from UndefinedDatabase/feature/f038-grounded-chat
```
Block bytes: measured line count 301 and sha256
`80fc6ea37e6096b8caccbb428e08f677258722332e95b13022cf5b193bb9417c` — MATCH both given readings.
`git worktree list | wc -l` at step 4: 62.

PAYLOADS — all three measured and MATCH the block's table exactly: claim.diff 173/20231/
`5c82fad2f5549ebd00ee6b115906341f50adac892f0ed8dc8faeafe1495cb19d`; context.md 35/1456/
`5b0ab13d3ad220d97ca7c2163246228fc2bb5c96c0143ee847e358384b875c42`; plan.md 34/1285/
`31c0d2d4cb1ca021bc43cd25c9d2d4bf0112be5f59f0844ab9a4c133fd63a597`.

C1a: measured insertions 370 (301 + 69), under the 500-line cap — no STOP required.

G1 TRANSPORT — every `.agent/authored/f039-r1-*` copy, read back with `git show <commit>:<path>`,
equals its source byte for byte: block.md (at `4f5a713a6`, against `.remedy-wt/f039-r1/block.md`),
plan.md and context.md (at `4f5a713a6`, against the payloads), claim.diff (at `a704ae20b`, against
the payload) — all four MATCH.

G2 THE CLAIM, at C2 (`5b7947c72`):
| path | bytes | sha256 | verdict |
|---|---|---|---|
| .agent/decisions.md | 2421566 | `01e6b463bc6dbbde543313a6f974ee918c2262c5bf792aa36bd5fd4b7b195f14` | MATCH |
| .agent/live_review.md | 325814 | `be9f7300f14f4f9efb925d0e14b0ee2b7a98bf8e3b250a1c42c82ff55abac270` | MATCH |
| docs/roadmap/STATUS.md | 56978 | `e8119679658dd57c1db6d5e0314d6caf9dc63e4f5b5938208a104e24896ac03c` | MATCH |
| docs/roadmap/features/T2_F286.md | 2570 | `0a75e8e61bca9afd3d23d5a9290af21e631bc6fb105860a901bc02c063a72654` | MATCH |
| .agent/plan.md | 1285 | `31c0d2d4cb1ca021bc43cd25c9d2d4bf0112be5f59f0844ab9a4c133fd63a597` | MATCH |
| .agent/context.md | 1456 | `5b0ab13d3ad220d97ca7c2163246228fc2bb5c96c0143ee847e358384b875c42` | MATCH |

`open_finding_ids(text)` of `scripts.rotate_live_review` over `.agent/live_review.md`: `[]` at
`4d60eb84e` and `[]` at C2 — both match the reviewer's own reading. At C2 the ledger has exactly
one line reading `## Findings` and exactly one reading `## Steps`; its last non-empty line begins
`Gate: F038 R15 — `. The STATUS lines at C2: line 172 `F038` (`[x]`), line 173 `- [~] F039 —
Story/replay mode` (directly after F038, before line 177's F286), and `F039` occurs on exactly
that one line of the file. `git diff --name-only a704ae20b 5b7947c72` names exactly the six paths
of G2's table, nothing else.

G3 THE CODE:
```
$ python3 -m ruff check tests/ui_contracts/test_story_chapters.py
All checks passed!
REAL_EXIT=0
```
From `git show 757fd719b` (C3), the title table:
```
export const STORY_CHAPTER_TITLES: Readonly<Record<TimelinePhase, string>> = {
  job: "The start",
  planning: "The plan",
  build: "The build",
  test: "The tests",
  review: "The review",
  finalized: "The finish",
};
```
and the whole of `buildStoryChapters`:
```
export function buildStoryChapters(
  jobId: string,
  tasks: readonly BrainTaskSeed[],
  rows: readonly BrainEventRow[],
): StoryChapter[] {
  const reading = readPhases(jobId, tasks, rows);
  if (reading.lastSeq === null) return [];
  const lastSeq = reading.lastSeq;
  const keyEvents = extractSubGlyphs(rows);
  const spanByPhase = new Map(reading.spans.map((span) => [span.phase, span] as const));
  const chapters: StoryChapter[] = [];

  for (const phase of TIMELINE_PHASES) {
    const span = spanByPhase.get(phase);
    if (span === undefined) continue;
    const start = span.startSeq;
    const end = span.endSeq === null ? lastSeq + 1 : span.endSeq;
    if (start >= end) continue;
    const phaseEvents = keyEvents.filter((event) => event.seq >= start && event.seq < end);
    const parts = Math.max(1, Math.ceil(phaseEvents.length / STORY_CHAPTER_KEY_EVENT_LIMIT));

    for (let part = 1; part <= parts; part += 1) {
      const partStartIndex = (part - 1) * STORY_CHAPTER_KEY_EVENT_LIMIT;
      const partEvents = phaseEvents.slice(partStartIndex, partStartIndex + STORY_CHAPTER_KEY_EVENT_LIMIT);
      const startSeq = part === 1 ? start : partEvents[0].seq;
      const endSeq = part === parts ? end : phaseEvents[partStartIndex + STORY_CHAPTER_KEY_EVENT_LIMIT].seq;
      chapters.push({
        phase,
        part,
        parts,
        title: storyChapterTitle(phase, part, parts),
        startSeq,
        endSeq,
        clusters: clusterKeyEvents(partEvents),
      });
    }
  }

  return chapters;
}
```
From `git show 5c83f21a1` (C4a), the demo recording's golden:
```
    const chapters = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows());
    expect(chapters).toEqual([
      { phase: "build", part: 1, parts: 1, title: "The build", startSeq: 0, endSeq: 1, clusters: [] },
      {
        phase: "review",
        part: 1,
        parts: 1,
        title: "The review",
        startSeq: 1,
        endSeq: 9,
        clusters: [
          { firstSeq: 1, lastSeq: 3, events: [e1, e3] },
          { firstSeq: 6, lastSeq: 8, events: [e6, e8] },
        ],
      },
      { phase: "finalized", part: 1, parts: 1, title: "The finish", startSeq: 9, endSeq: 10, clusters: [] },
    ] satisfies StoryChapter[]);
```

G4 THE TESTS, in the primary checkout at C4b (`447dabe5b`), SERIALLY:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/orchestration/test_feature_mission_adapter.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_review_archive_authority.py tests/orchestration/test_development_artifact_boundary.py tests/test_command_catalog.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
1870 passed, 5 skipped in 83.37s (0:01:23)
REAL_EXIT=0
```
The reviewer's simulation read `1861 passed, 10 skipped` at exit 0. This run's own new tests
account for the difference: `tests/ui_contracts/test_story_chapters.py` collects 7 nodes
(`--collect-only -q` confirmed), all 7 passed; the FOUR toolchain nodes the block named — the two
`eslint` nodes in `tests/ui_contracts/test_ui_lint.py`, the `tsc --noEmit` node in
`tests/ui_server/test_dashboard_contract.py`, and the vitest node in
`tests/orchestration/test_test_runner.py` (which runs the UI's whole unit suite, including this
round's new `storyChapters.test.ts`) — each PASSED, not skipped, in this primary-checkout run (none
of the five SKIPPED lines above name any of the four). None of the five skips are new; all are
pre-existing D3/D12 quarantines unrelated to this round.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=168", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks' status: `pass`. `fail_count`: 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f039-r1-mut 447dabe5b`, then:
```
$ python3 -B .agent/authored/f039-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r1-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r1-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=14 | guard exit=0 failed=0 passed=7
m1 (two key events exactly two seqs apart fall into separate clusters): vitest exit=1 failed=3 passed=11 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m2 (a phase of exactly six key events splits): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m3 (a phase with a zero span gives a chapter): vitest exit=1 failed=4 passed=10 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m4 (a later part begins at its phase's start): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m5 (an earlier part ends at its phase's end): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m6 (the last chapter ends at the ledger's last seq instead of one past it): vitest exit=1 failed=6 passed=8 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m7 (a split phase's titles lose their part numbers): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m8 (heals are dropped from the key events): vitest exit=1 failed=4 passed=10 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m9 (clusters are read over the whole phase instead of inside a part): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=7 | caught=True restored byte-identical=True
m10 (Finalized's title reads `The review`): vitest exit=1 failed=3 passed=11 | guard exit=1 failed=1 passed=6 | caught=True restored byte-identical=True
m11 (the module reads the clock): vitest exit=0 failed=0 passed=14 | guard exit=1 failed=1 passed=6 | caught=True restored byte-identical=True
m12 (the title table's test and review lines swap places): vitest exit=0 failed=0 passed=14 | guard exit=1 failed=1 passed=6 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=14 | guard exit=0 failed=0 passed=7
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every mutation caught (vitest for the ten structural/behavioural mutations m1–m9 — nine of them —
plus m10's title swap; the guard for m10 (title-table value drift), m11 (the `Date` purity word)
and m12 (key order drift, invisible to `toEqual`)), every restore byte-identical, both controls
green. Then `git worktree remove --force .remedy-wt/f039-r1-mut` and `git worktree prune`; `git
worktree list | wc -l`: 62 (unchanged from step 4's reading).

## Authored-text proofs

The block itself and all three plan/context/claim-diff payloads were each copied verbatim
(`shutil.copyfile`) and compared byte-identical against their sources under G1 above — all four
MATCH. `.agent/decisions.md`, `.agent/live_review.md`, `docs/roadmap/STATUS.md`,
`docs/roadmap/features/T2_F286.md`, `.agent/plan.md` and `.agent/context.md` at C2 were verified
byte- and sha256-identical to the reviewer's own simulation readings under G2 above — all six
MATCH. `claim.diff` applied cleanly by `git apply` (both `--check` and the real apply read
`REAL_EXIT=0`).

## Deviations & assumptions

ONE declared deviation: the block's C4 ("THE TESTS AND THE TOOL") was split into C4a (the vitest
goldens and the Python guard, 335 insertions) and C4b (the mutation tool, 170 insertions) under
constraint 2, because the three files together total 505 insertions — at the 500-line cap. Both
parts individually stay well under the cap; the split follows the block's own naming convention
("C4a and C4b, and say so"). No other departure from the block's ordered commit sequence: C1a,
C1b, C2, C3, C4a, C4b were followed exactly, with no dropped step and no reordering. `git diff
--name-only 4d60eb84e HEAD` (before this commit) named exactly the round's tracked path set:
the five `.agent/authored/f039-r1-*` copies and the tool, `.agent/live_review.md`,
`docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F286.md`, `.agent/decisions.md`,
`.agent/plan.md`, `.agent/context.md`, the two new files under
`apps/ui/src/components/story/`, and `tests/ui_contracts/test_story_chapters.py` — no other file
under `apps/`, `packages/`, `tests/` or `docs/` was touched, and `docs/roadmap/features/T5_F039.md`
was read but not edited, per constraint 3.

ASSUMPTION: within the custom-built test scenarios (a review of eight key events splitting, and
one of exactly six staying whole), finalizing the job core state requires a real `task_run_completed`
event, not merely a `task_round_completed` with a `pass` outcome — confirmed by reading
`onTaskRoundCompleted` and `onTaskRunClosed` in `brainReducer.ts` directly (the former only births
a `review_run` child and never closes the open `builder_run` or sets the task's own state; only the
latter, driven by `task_run_completed`/`task_run_failed`, does). Both custom ledgers were built
and vitest-verified against this reading before being written into the golden literals, and all 14
vitest cases plus all 7 guard cases pass.

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1a | done | 370 insertions (301 + 69), under the 500-line cap |
| C1b | done | 173 insertions, matches the block's expected reading exactly |
| C2 | done | claim.diff applied clean; numstat matches the block's table exactly; records match the reviewer's simulation byte for byte |
| C3 | done | module written to S1–S6, `git add`ed, tsc and eslint clean |
| C4a | deviated | split from the block's single C4 under constraint 2 (505 insertions together, over the cap); vitest goldens + Python guard, 335 insertions |
| C4b | deviated | the other half of the C4 split; mutation tool, 170 insertions |
| C5 | done | this handback |
| G1 TRANSPORT | done | all four payload/copy readings MATCH |
| G2 THE CLAIM | done | all six file readings MATCH, `open_finding_ids` `[]` at both commits, ledger structure and STATUS lines all as required |
| G3 THE CODE | done | ruff clean; title table, `buildStoryChapters` and the demo golden quoted from the commits |
| G4 THE TESTS | done | 1870 passed, 5 skipped, exit 0; all four named toolchain nodes passed (not skipped); integrity 6/6 pass |
| G5 THE RED PROOFS | done | all 12 mutations caught, all restored byte-identical, both controls green, exit 0 |
| G6 TREE AND PUSH | pending | runs after this commit and the push, reported in the worker's final reply |

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of this round (round 1).
Then, once round 1 is accepted, round 2 lands T002's first slice: the narration card for a
cluster, its line source settled between the humanize catalog and F255's narration, and its sync
to the scrub position. Open findings in the ledger: 0 (matching `open_finding_ids` `[]` at C2, and
carried forward from F038's closure). Operator questions open: 1 (Q6, empty-paydown-waits).
