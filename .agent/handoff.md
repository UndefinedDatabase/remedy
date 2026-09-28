# Handback — F039, round 2: book round 1, register and repair R-1098, and land T002's narration cards with their sync to the scrub position

## Session

SESSION 1 of feature F039 · round 2 · rounds so far 2. This session ran round 2 only: booking
round 1's PASS, registering and repairing finding R-1098 (five UI guards blind to a bare import or
a re-export), and T002's first half — the narration cards, their tables, their sync functions, the
vitest goldens and the Python guard. Context self-assessment: a comfortable margin of context
remained through the round, including the full targeted pytest selection and all 23 mutation
red-proofs across two runs of the tool; the work was not near its limit.

For the operator, in plain words: round 1 is booked PASS, and F039's one open finding (R-1098, a
blind spot in five test guards that could not see a bare `import "x";` or a re-export) is repaired
in this round's first commits. T002's narration cards now exist as a pure TypeScript module — one
card per cluster of key events, each beat carrying the catalog's own line, the reviewer's own
verdict word, and the ownership ledger's own sentence where exactly one event and one entry agree —
plus the sync functions a scrub position uses to find its chapter and its latest card. Nothing
renders it yet: no component, route, command or Python module changed this round.

## Range

Review of `ea7bcbdb3`..`HEAD` (the commit that writes this file is the ninth in the range). EIGHT
commits precede it: C1a, C1b, C2, C3, C4, C5, C6 and C6b — C6b is a declared addition beyond the
block's lettered bundle (see Deviations below) — then this handback commit (C7).

## Commits

### da97774b9 F039 R2 C1a: copy round 2 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r2-block.md | 290/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f039-r2-plan.md | 34/0 | the plan payload, copied verbatim |

(measured: `git show da97774b9 --numstat` reads `290 0`, `34 0`, total 324 — exactly the block's
own expected reading of the block's line count (290) plus 34, under the 500-line cap.)

### 3f518efbf F039 R2 C1b: copy round 2 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r2-records.diff | 62/0 | the records-diff payload, copied verbatim |

(measured: `git show 3f518efbf --numstat` reads `62 0` — exactly the block's expected 62.)

### 539314061 F039 R2 C2: book round 1, register R-1098, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 42/0 | records.diff appends DECISION F039 D3 |
| .agent/live_review.md | 4/0 | records.diff appends round 1's Gate entry and registers R-1098 |
| .agent/plan.md | 8/8 | records.diff, then rewritten := plan.md (round 2's plan) |

(measured: `git show 539314061 --numstat` reads `42 0`, `4 0`, `8 8` — exactly the block's own
expected reading in G2's table.)

### ea30d1bc4 F039 R2 C3: read every import statement in the UI guards (R-1098)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | S3: appends the `Landed: R-1098 — ` line |
| tests/ui_contracts/test_phase_mapping.py | 34/1 | S1: `TS_IMPORT_RE`, `ts_import_specifiers`, its own import check reads through it, plus the new unit test |
| tests/ui_contracts/test_scrub_snapshots.py | 3/1 | S2: imports and uses `ts_import_specifiers` in place of its own `re.findall` |
| tests/ui_contracts/test_semantic_zoom_contract.py | 3/1 | S2: same |
| tests/ui_contracts/test_story_chapters.py | 3/1 | S2: same |
| tests/ui_contracts/test_timeline_scrub_contract.py | 3/1 | S2: same |

(measured: `git show ea30d1bc4 --numstat` reads `2 0`, `34 1`, `3 1`, `3 1`, `3 1`, `3 1`, total 48
insertions, under the 500-line cap; the block gave no expected reading for C3.)

### eb269754f F039 R2 C4: compose the story's narration cards and sync them to the scrub position
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyNarration.ts | 179/0 | NEW module: S4–S9, `git add`ed so `relevant_untracked` sees a tracked file |

(measured: `git show eb269754f --numstat` reads `179 0`; the block gave no expected reading for C4.)

### 9537304a2 F039 R2 C5: golden the narration cards and guard their words
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyNarration.test.ts | 269/0 | NEW vitest goldens: both tables, `storyCostLine`'s five readings, the demo recording's two cards, GOLDEN_B_ROWS's stop/heal/decision cards, the stop's four no-actor cases, the decision's task scoping, the planned-job no-verdict case, and `chapterAt`/`cardAt` over nine positions |
| tests/ui_contracts/test_story_narration.py | 116/0 | NEW Python guard: `STORY_VERDICT_LINES` vs `REVIEW_OUTCOME_STATE_TABLE`, `STORY_ACTOR_ACTIONS` vs `SUB_GLYPH_TABLE`/`OWNERSHIP_CHIP_WORDS`, the five import specifiers via `ts_import_specifiers`, the `costMetricOf(` call, purity, no stray sentence, the one template literal |

(measured: `git show 9537304a2 --numstat` reads `269 0`, `116 0`, total 385, under the 500-line cap.)

### 6024ac300 F039 R2 C6: add the mutation tool for the narration cards and R-1098
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r2-mutations.py | 209/0 | NEW mutation tool, `m1`–`m23`, following `f039-r1-mutations.py`'s route over two vitest files and six Python guards |

(measured: `git show 6024ac300 --numstat` reads `209 0`, under the 500-line cap.)

### 6dc70a63a F039 R2 C6b: add the golden G5's m2 caught green, for the cost line's own lastSeq
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyNarration.test.ts | 17/0 | a golden with a tick exactly one seq past a cluster's last key event next to one at or before it, so m2 (cost reads `cluster.lastSeq + 1`) cannot pass unnoticed |

(measured: `git show 6dc70a63a --numstat` reads `17 0`, under the 500-line cap. Declared under
Deviations below: this commit is not in the block's lettered bundle.)

## External actions

`git worktree add --detach .remedy-wt/f039-r2-mut 6024ac300` before the first G5 run (which found
mutation m2 green in both runners); `git worktree remove --force .remedy-wt/f039-r2-mut` and `git
worktree prune` after it; `git worktree add --detach .remedy-wt/f039-r2-mut 6dc70a63a` before the
second, successful G5 run; `git worktree remove --force .remedy-wt/f039-r2-mut` and `git worktree
prune` after it — `git worktree list | wc -l` read 62 before both adds and after both removes
(step 4's reading, unchanged throughout). `git push origin feature/f039-story-replay-mode` after
this commit — reported in the worker's final reply, since this file is written and C7 committed
before that push, per the block's ordering.

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
feature/f039-story-replay-mode
$ git log --oneline -1
ea7bcbdb3 F039 R1 C5: rewrite handoff for round 1
```
Block bytes: measured line count 290 and sha256
`dfd46260a01aee7ced98b45d512e54e2be0311a0b7ebb2f907516e08336e0b85` — MATCH both given readings.
`git worktree list | wc -l` at step 4: 62.

PAYLOADS — both measured and MATCH the block's table exactly: plan.md 34/1278/
`725bedfa64517040d58f6fe4b8d01132abad1fa73651fb1e6e19f63990b61839`; records.diff 62/11937/
`87732cc04771fd641d66a29dbab955d3f9c8902a2d58d38e45e595424a73cba7`.

C1a: measured insertions 324 (290 + 34), under the 500-line cap — no STOP required.

G1 TRANSPORT — both `.agent/authored/f039-r2-*` copies of the block and plan, read back with `git
show da97774b9:<path>`, equal their sources byte for byte: block.md (against
`.remedy-wt/f039-r2/block.md`) and plan.md (against the payload); records.diff, read back with
`git show 3f518efbf:.agent/authored/f039-r2-records.diff`, equals the payload byte for byte — all
three MATCH.

G2 THE RECORDS, at C2 (`539314061`):
```
$ git apply --check .remedy-wt/f039-r2-payloads/records.diff
REAL_EXIT=0
$ git apply .remedy-wt/f039-r2-payloads/records.diff
REAL_EXIT=0
```
| path | bytes | sha256 | verdict |
|---|---|---|---|
| .agent/decisions.md | 2425281 | `dc09ed888ba2776338e28a5c9f84739f99b021820bd2b04c9fb04a1deb26c52a` | MATCH |
| .agent/live_review.md | 329589 | `b748ff6b7053ed80ff94e46d1427e571a96fb00b3c30291b720f8655b6b49059` | MATCH |
| .agent/plan.md | 1278 | `725bedfa64517040d58f6fe4b8d01132abad1fa73651fb1e6e19f63990b61839` | MATCH |

`open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT: `[]` at `ea7bcbdb3`
and `['R-1098']` at C2 — both match the reviewer's own reading. `git diff --name-only 3f518efbf
539314061` names exactly `.agent/decisions.md`, `.agent/live_review.md` and `.agent/plan.md` —
exactly G2's table, nothing else.

At C3 (`ea30d1bc4`): the ledger at C2 is a byte-exact prefix of the ledger at C3 (measured by
reading both back with `git show <sha>:.agent/live_review.md` and comparing the first 329589 bytes
of C3's text against C2's whole text — identical), and what C3 adds is exactly `"\n"` plus one line
beginning `Landed: R-1098 — ` and ending in `"\n"` (measured: the added bytes are
`\nLanded: R-1098 — the five UI guards under \`tests/ui_contracts/\` now read a module's imports
through \`ts_import_specifiers\`, which sees a bare import and a re-export the old \`from\`-only
pattern missed.\n`).

G3 THE CODE:
```
$ python3 -m ruff check tests/ui_contracts/test_phase_mapping.py tests/ui_contracts/test_timeline_scrub_contract.py tests/ui_contracts/test_scrub_snapshots.py tests/ui_contracts/test_semantic_zoom_contract.py tests/ui_contracts/test_story_chapters.py tests/ui_contracts/test_story_narration.py .agent/authored/f039-r2-mutations.py
All checks passed!
REAL_EXIT=0
```
From `git show ea30d1bc4` (C3), `TS_IMPORT_RE` with its comment:
```python
# R-1098 — a bare import (`import "x";`), a re-export (`export ... from "x";` or
# `export * from "x";`) and a named import (`import { a } from "x";`, however many lines
# it spans) all name a specifier a guard must see; the five UI guards below read every
# module's imports through this reader rather than through their own `from`-only pattern.
TS_IMPORT_RE = re.compile(r'^(?:import|export)\s+(?:[^;]*?\s+from\s+)?"([^"]+)";$', re.MULTILINE)


def ts_import_specifiers(src: str) -> list[str]:
    return TS_IMPORT_RE.findall(src)
```
From `git show eb269754f` (C4), the whole of `storyCostLine`:
```typescript
export function storyCostLine(ticks: readonly StoryTick[], seq: number): string | null {
  let latest: StoryTick | null = null;
  for (const tick of ticks) {
    if (tick.seq <= seq && (latest === null || tick.seq > latest.seq)) latest = tick;
  }
  if (latest === null) return null;
  const metric = costMetricOf(latest.figures);
  if (metric.display === NO_COST_DISPLAY) return null;
  return `Cost so far: ${metric.estimated ? "~" : ""}${metric.display}${metric.unit === "tokens" ? " tokens" : ""}`;
}
```
the whole of `buildNarrationCards`:
```typescript
export function buildNarrationCards(
  chapters: readonly StoryChapter[],
  rows: readonly BrainEventRow[],
  ticks: readonly StoryTick[],
  ownership: OwnershipView | null,
): NarrationCard[] {
  const allEvents: SubGlyph[] = [];
  for (const chapter of chapters) {
    for (const cluster of chapter.clusters) {
      for (const event of cluster.events) allEvents.push(event);
    }
  }
  const cards: NarrationCard[] = [];
  chapters.forEach((chapter, chapterIndex) => {
    for (const cluster of chapter.clusters) {
      cards.push({
        chapter: chapterIndex,
        firstSeq: cluster.firstSeq,
        lastSeq: cluster.lastSeq,
        beats: cluster.events.map((event) => beatOf(event, rows, allEvents, ownership)),
        cost: storyCostLine(ticks, cluster.lastSeq),
      });
    }
  });
  return cards;
}
```
and the whole of `cardAt` (with `chapterAt` it calls):
```typescript
export function chapterAt(chapters: readonly StoryChapter[], position: number): number {
  return chapters.findIndex((chapter) => chapter.startSeq <= position && position < chapter.endSeq);
}

export function cardAt(
  chapters: readonly StoryChapter[],
  cards: readonly NarrationCard[],
  position: number,
): NarrationCard | null {
  const chapter = chapterAt(chapters, position);
  if (chapter === -1) return null;
  let found: NarrationCard | null = null;
  for (const card of cards) {
    if (card.chapter === chapter && card.firstSeq <= position) found = card;
  }
  return found;
}
```
From `git show 9537304a2` (C5), the golden B test:
```typescript
describe("buildNarrationCards on GOLDEN_B_ROWS: a stop mid-run, a heal, then a decision", () => {
  it("names the stop's actor, marks each review round's verdict, and reads the cost at each cluster's last seq", () => {
    const chapters = buildStoryChapters(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, GOLDEN_B_ROWS);
    const ticks: readonly StoryTick[] = [
      { seq: 5, figures: { spent_usd: 0.25 } },
      { seq: 8, figures: { spent_usd: 0.5, basis: { cost: "actual" } } },
    ];
    const ownership = ownershipView([ownerEntry("job_stopped", "", "The operator stopped the job.")]);
    const cards = buildNarrationCards(chapters, GOLDEN_B_ROWS, ticks, ownership);
    expect(cards).toEqual([
      {
        chapter: 1,
        firstSeq: 2,
        lastSeq: 6,
        beats: [
          { seq: 2, glyph: "failure", taskId: "t1", line: REVIEW_LINE, verdict: "Verdict: fail", actor: null },
          { seq: 3, glyph: "failure", taskId: "t1", line: REVIEW_LINE, verdict: "Verdict: needs repair", actor: null },
          {
            seq: 4, glyph: "stop", taskId: "", line: "The job stopped.",
            verdict: null, actor: "The operator stopped the job.",
          },
          { seq: 6, glyph: "heal", taskId: "t1", line: REVIEW_LINE, verdict: "Verdict: pass", actor: null },
        ],
        cost: "Cost so far: ~$0.25",
      },
      {
        chapter: 1,
        firstSeq: 9,
        lastSeq: 9,
        beats: [
          {
            seq: 9, glyph: "decision", taskId: "t2", line: "task_needs_decision event",
            verdict: null, actor: null,
          },
        ],
        cost: "Cost so far: $0.50",
      },
    ] satisfies NarrationCard[]);
  });
});
```

G4 THE TESTS, in the primary checkout at C6b (`6dc70a63a`, the final state before this handback),
SERIALLY:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/orchestration/test_feature_mission_adapter.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_review_archive_authority.py tests/orchestration/test_development_artifact_boundary.py tests/test_command_catalog.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
1876 passed, 5 skipped in 112.45s (0:01:52)
REAL_EXIT=0
```
The reviewer's own simulation (which carries C1a–C2 of this round plus its own version of C3–C5)
read `1870 passed, 10 skipped` at exit 0; five of its skips are toolchain nodes a worktree cannot
run, none SKIPPED here. This run's own count differs by what this round's guards hold: node counts
by `--collect-only -q`, per Python guard this round adds or edits —
`test_phase_mapping.py` 5, `test_timeline_scrub_contract.py` 4, `test_scrub_snapshots.py` 4,
`test_semantic_zoom_contract.py` 4, `test_story_chapters.py` 7, `test_story_narration.py` 5 (total
29, confirmed also by collecting all six together). None of the five SKIPPED lines above name any
node this round touched; all five are pre-existing D3/D12 quarantines.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=168", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks' status: `pass`. `fail_count`: 0. (R-1098 is Low, so `high_blockers_open` correctly
still reads pass while R-1098 itself stays open until the reviewer resolves it, per the block.)

G5 THE RED PROOFS — TWO RUNS. FIRST, `git worktree add --detach .remedy-wt/f039-r2-mut 6024ac300`
(C6), then:
```
$ python3 -B .agent/authored/f039-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r2-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r2-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=40 | guard exit=0 failed=0 passed=29
[... m1, m3–m23 all caught True, restored byte-identical True ...]
m2 (the cost line reads a tick one seq past the cluster): vitest exit=0 failed=0 passed=40 | guard exit=0 failed=0 passed=29 | caught=False restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=40 | guard exit=0 failed=0 passed=29
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False
REAL_EXIT=1
```
m2 stayed GREEN in both runners: no golden in C5 paired a tick at a cluster's own `lastSeq` with a
different-valued tick exactly one seq later, so shifting the query by +1 changed nothing observable.
Reported as green, not papered over. `git worktree remove --force .remedy-wt/f039-r2-mut`, `git
worktree prune`. Per constraint 4, the test was corrected before C7: commit C6b adds exactly such a
golden (see Commits above), confirmed by hand-mutating the working tree, watching the new test fail
with `expected 'Cost so far: $2.00' to be 'Cost so far: $1.00'`, then `git checkout --` to restore.

SECOND, after C6b: `git worktree add --detach .remedy-wt/f039-r2-mut 6dc70a63a`, then:
```
$ python3 -B .agent/authored/f039-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r2-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r2-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=41 | guard exit=0 failed=0 passed=29
m1 (the cost line reads the earliest tick at or before the seq instead of the latest): vitest exit=1 failed=4 passed=37 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m2 (the cost line reads a tick one seq past the cluster): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m3 (an estimated figure loses its ~): vitest exit=1 failed=2 passed=39 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m4 (a token figure loses ' tokens'): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m5 (a tick with no figure gives a cost line): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m6 (every row's outcome is read as a verdict, not only a review round's): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m7 (an actor is named when two ownership entries match): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m8 (an unreadable ownership view still names an actor): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m9 (a decision's actor ignores its task): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m10 (cardAt shows a card of another chapter): vitest exit=1 failed=1 passed=40 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m11 (cardAt shows a card before its first key event): vitest exit=1 failed=3 passed=38 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m12 (chapterAt counts a chapter's endSeq as inside it): vitest exit=1 failed=3 passed=38 | guard exit=0 failed=0 passed=29 | caught=True restored byte-identical=True
m13 (STORY_VERDICT_LINES gains a skipped line after its blocked line): vitest exit=1 failed=1 passed=40 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m14 (a statement void "no cost here"; is added inside storyCostLine): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m15 (phaseMapping.ts gains an unguarded bare import): vitest exit=1 failed=-1 passed=-1 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m16 (scrubState.ts gains an unguarded bare import): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m17 (timelineIndex.ts gains an unguarded bare import): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m18 (timelineView.ts gains an unguarded bare import): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m19 (scrubSnapshots.ts gains an unguarded bare import): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m20 (semanticZoom.ts gains an unguarded bare import): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m21 (zoomWheel.ts gains an unguarded bare import): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m22 (storyChapters.ts gains an unguarded bare import): vitest exit=1 failed=-1 passed=-1 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
m23 (TS_IMPORT_RE reverts to the blind from-only pattern): vitest exit=0 failed=0 passed=41 | guard exit=1 failed=1 passed=28 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=41 | guard exit=0 failed=0 passed=29
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
All 23 mutations caught (m1–m14 in `storyNarration.ts` by vitest, the guard, or both; m15–m22's
bare imports by the guard always, and by vitest too for the two files vitest's own module graph
reaches, `phaseMapping.ts` and `storyChapters.ts`, where an unresolvable specifier breaks collection
outright; m23 by the guard alone), every restore byte-identical, both controls green. `git worktree
remove --force .remedy-wt/f039-r2-mut`, `git worktree prune`; `git worktree list | wc -l`: 62
(unchanged from step 4's reading, both before and after both runs).

## Authored-text proofs

The block and the plan payload were each copied verbatim (`shutil.copyfile`) at C1a and compared
byte-identical against their sources under G1 above — both MATCH. The records-diff payload was
copied verbatim at C1b and compared byte-identical under G1 above — MATCH. `.agent/decisions.md`,
`.agent/live_review.md` and `.agent/plan.md` at C2 were verified byte- and sha256-identical to the
reviewer's own simulation readings under G2 above — all three MATCH. `records.diff` applied cleanly
by `git apply` (both `--check` and the real apply read `REAL_EXIT=0`).

## Deviations & assumptions

ONE declared deviation: an extra commit, C6b, beyond the block's lettered bundle (C1a, C1b, C2, C3,
C4, C5, C6, C7). G5's first run (worktree at C6) found mutation m2 (the cost line reads a tick one
seq past the cluster) GREEN in both runners, because C5's goldens never placed a tick exactly at a
cluster's `lastSeq` next to a different-valued one exactly one seq later. Per constraint 4 ("a test
this round itself wrote that is wrong may be corrected before C7, and the correction is declared"),
commit C6b adds one golden that pairs such ticks and pins the resulting cost line to the one at
`lastSeq`; hand-mutating the working tree copy and re-running vitest confirmed the new golden fails
under the mutation (`expected 'Cost so far: $2.00' to be 'Cost so far: $1.00'`) and passes
unmutated, before the file was restored with `git checkout --` and the commit made. G5 was then
re-run in a fresh worktree at C6b's SHA and all 23 mutations were caught. No other departure from
the block's ordered commit sequence: C1a, C1b, C2, C3, C4, C5, C6 were followed exactly, with no
dropped step and no reordering. `git diff --name-only ea7bcbdb3 HEAD` (before this commit) named
exactly the round's tracked path set: the four `.agent/authored/f039-r2-*` copies and the tool,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the five guards S1 and S2 name,
the two new files under `apps/ui/src/components/story/`, and
`tests/ui_contracts/test_story_narration.py` — no other file under `apps/`, `packages/`, `tests/`
or `docs/` was touched, `.agent/prose_slips.md`, `.agent/candidates.md`,
`.agent/operator_questions.md` and `README.md` were left alone, and `docs/roadmap/features/T5_F039.md`
was not read this round (T002's clauses came from DECISION F039 D3 and the modules S4 names) but
was not edited either, per constraint 3.

ASSUMPTION: the ownership ledger's own `OwnershipEntry` carries no `seq`, so an actor can only be
named by counting — the module counts occurrences of a key-event kind against occurrences of the
mapped ownership action, scoped to the event's own task for `decision_answered` and unscoped for
`job_stopped` (a job-wide event whose events always carry `taskId: ""`), exactly as DECISION F039
D3 clause 5 states. All hand-derived goldens in C5 and C6b were vitest-verified before being
written into the golden literals, and all 41 vitest cases plus all 29 Python guard cases pass.

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1a | done | 324 insertions (290 + 34), under the 500-line cap |
| C1b | done | 62 insertions, matches the block's expected reading exactly |
| C2 | done | records.diff applied clean; numstat matches the block's table exactly; records match the reviewer's simulation byte for byte |
| C3 | done | R-1098's reader written to S1, the four other guards updated per S2, the `Landed:` line appended per S3 |
| C4 | done | module written to S4–S9, `git add`ed, import specifiers and purity confirmed |
| C5 | done | both new test files written, all goldens hand-derived and vitest/pytest-verified |
| C6 | done | mutation tool added, `m1`–`m23`, following the round 1 tool's route |
| C6b | deviated | extra commit beyond the block's bundle: adds the golden G5's first run found m2 stayed green without |
| C7 | done | this handback |
| G1 TRANSPORT | done | all three payload/copy readings MATCH |
| G2 THE RECORDS | done | all three file readings MATCH, `open_finding_ids` `[]`→`['R-1098']`, C3's prefix and Landed-line addition confirmed byte-exact |
| G3 THE CODE | done | ruff clean over all six guards and the tool; `TS_IMPORT_RE`, `buildNarrationCards`, `storyCostLine`, `cardAt` and the golden B test quoted from the commits |
| G4 THE TESTS | done | 1876 passed, 5 skipped, exit 0; per-guard collect counts sum to 29; integrity 6/6 pass |
| G5 THE RED PROOFS | done | first run found m2 green (reported, not papered over); C6b added its golden; second run: all 23 mutations caught, all restored byte-identical, both controls green, exit 0 |
| G6 TREE AND PUSH | pending | runs after this commit and the push, reported in the worker's final reply |

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 2, with the resolution
of R-1098. Then, once round 2 is accepted, T002's second half: the autoplay pacing with chapter
pauses, and the in-app story mode on the demo recording. Open findings in the ledger: 1 (R-1098,
landed and awaiting review). Operator questions open: 1.
