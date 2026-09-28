# Handback — F039, round 3: book round 2 and R-1098's resolution, register and repair R-1099, and land T002's autoplay pacing

## Session

SESSION 1 of feature F039 · round 3 · rounds so far 3. This session ran round 3 only: booking round
2's PASS and R-1098's resolution, registering and repairing finding R-1099 (the narration goldens
never held two key events of one actor kind), recording DECISION F039 D4, and T002's second half —
the pure `storyAutoplay.ts` module, its pacing clamp, its vitest goldens hand-derived from the demo
recording's chapters, and its Python guard binding the step and the chapter pause to the design
reference's motion tokens. Context self-assessment: a comfortable margin remained through the round,
including the full targeted pytest selection and all 11 mutation red-proofs in one run of the tool;
the work was not near its limit.

For the operator, in plain words: round 2 is booked PASS and R-1098 is booked resolved. R-1099 (the
actor rule's untested event-count half) is registered and repaired with two new goldens: two
`job_stopped` events against one ownership entry, and two answered decisions of one task against one
entry — in both cases neither event names an actor, proving `beatActor`'s count check actually does
something. Autoplay now exists as a pure TypeScript module: given the story's chapters and the
ledger's seqs, it answers which scrub position comes next and how long to wait — one ledger event at
a time, one chapter pause more before every chapter's first event, chapter by chapter under reduced
motion — with its step and chapter pause bound to the motion reference's node-birth and pulse
tokens, and a pacing payload reader clamped to 50–10000ms. Nothing renders it yet: no component,
route, command, configuration key, event name or Python module changed this round.

## Range

Review of `1e1d7352d`..`HEAD` (the commit that writes this file is the eighth in the range). SEVEN
commits precede it: C1a, C1b, C2, C3, C4, C5 and C6 — the block's lettered bundle exactly, no extra
commit and no dropped one.

## Commits

### 8c0b9f75a F039 R3 C1a: copy round 3 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r3-block.md | 255/0 | this block, copied verbatim by `shutil.copyfile` |
| .agent/authored/f039-r3-plan.md | 33/0 | the plan payload, copied verbatim |

(measured: `git show 8c0b9f75a --numstat` reads `255 0`, `33 0`, total 288 — exactly the block's own
expected reading (255 + 33), under the 500-line cap.)

### 1d8f0a690 F039 R3 C1b: copy round 3 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r3-records.diff | 55/0 | the records-diff payload, copied verbatim |

(measured: `git show 1d8f0a690 --numstat` reads `55 0` — exactly the block's expected 55.)

### 8dee5d78b F039 R3 C2: book round 2 and R-1098, register R-1099, record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 33/0 | records.diff appends DECISION F039 D4 |
| .agent/live_review.md | 6/0 | records.diff appends round 2's Gate entry, R-1098's Done paragraph and R-1099's registration |
| .agent/plan.md | 5/6 | records.diff, then rewritten := plan.md (round 3's plan) |

(measured: `git show 8dee5d78b --numstat` reads `33 0`, `6 0`, `5 6` — exactly the block's own
expected reading in G2's table.)

### 9711f756a F039 R3 C3: golden two events of one actor kind (R-1099)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | S2: appends the `Landed: R-1099 — ` line |
| apps/ui/src/components/story/storyNarration.test.ts | 29/0 | S1: two new goldens — two `job_stopped` events against one entry, and two answered decisions of one task against one entry, neither naming an actor |

(measured: `git show 9711f756a --numstat` reads `2 0`, `29 0`, total 31 insertions, under the
500-line cap; the block gave no expected reading for C3.)

### cfd50fb7f F039 R3 C4: pace the story's autoplay by its events and chapters
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyAutoplay.ts | 122/0 | NEW module: S3–S4, `storyPacingOf`, `autoplayStep`, `autoplayTotalMs`, the four constants and `STORY_PACING_DEFAULT` |

(measured: `git show cfd50fb7f --numstat` reads `122 0`; the block gave no expected reading for C4.)

### d3a9dbb2e F039 R3 C5: golden the autoplay and bind its waits to the motion reference
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/storyAutoplay.test.ts | 150/0 | NEW vitest goldens: the four constants and the default, `storyPacingOf`'s clamp and its edges, the whole demo-recording walk as one literal (waits 1100, 1100, then 100×7, then 1100), reduced motion's three steps, `autoplayTotalMs` (9000 / 4800), the first-four-rows unfinished review ending at seq 3, and an empty ledger |
| tests/ui_contracts/test_story_autoplay.py | 51/0 | NEW Python guard: `STORY_STEP_MS`/`STORY_CHAPTER_PAUSE_MS` vs `--remedy-dur-birth`/`--remedy-dur-pulse`, the two import specifiers via `ts_import_specifiers`, the `chapterAt(` call, purity |

(measured: `git show d3a9dbb2e --numstat` reads `150 0`, `51 0`, total 201, under the 500-line cap.)

### edd4ce65a F039 R3 C6: add the mutation tool for the autoplay and R-1099
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r3-mutations.py | 168/0 | NEW mutation tool, `m1`–`m11`, following `f039-r2-mutations.py`'s route over three vitest files and two Python guards |

(measured: `git show edd4ce65a --numstat` reads `168 0`, under the 500-line cap.)

## External actions

`git worktree add --detach .remedy-wt/f039-r3-mut edd4ce65a` before the (single, successful) G5 run;
`git worktree remove --force .remedy-wt/f039-r3-mut` and `git worktree prune` after it —
`git worktree list | wc -l` read 62 before the add and after the remove (step 4's reading,
unchanged). `git push origin feature/f039-story-replay-mode` after this commit — reported in the
worker's final reply, since this file is written and C7 committed before that push, per the block's
ordering.

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
1e1d7352d F039 R2 C7: rewrite handoff for round 2
```
Block bytes: measured line count 255 and sha256
`58b17131bab1518a7b6c0504057732837cec50145ff110592a05b5d8b056d72c` — MATCH both given readings.
`git worktree list | wc -l` at step 4: 62.

PAYLOADS — both measured and MATCH the block's table exactly: plan.md 33/1279/
`afa5917e885bd79ceb75182809511a2afd04b244b326616d851b98bb757ae749`; records.diff 55/9668/
`154f1182ac2eac264cd7fae867e384ff03b5ea1d5d9c08449cafb168b2b667d2`.

C1a: measured insertions 288 (255 + 33), under the 500-line cap — no STOP required.

G1 TRANSPORT — all three `.agent/authored/f039-r3-*` copies, read back with `git show <commit>:<path>`,
equal their sources byte for byte: block.md (against `.remedy-wt/f039-r3/block.md`, at C1a),
plan.md (against the payload, at C1a), records.diff (against the payload, at C1b) — all three
MATCH, confirmed by sha256 on both sides.

G2 THE RECORDS, at C2 (`8dee5d78b`):
```
$ git apply --check .remedy-wt/f039-r3-payloads/records.diff
CHECK_EXIT=0
$ git apply .remedy-wt/f039-r3-payloads/records.diff
APPLY_EXIT=0
```
| path | bytes | sha256 | verdict |
|---|---|---|---|
| .agent/decisions.md | 2428140 | `ef7a9dc0cf2cd77b100aa5a745100f94ec2e6a64d2ab8cb7db192bb73c7fcc35` | MATCH |
| .agent/live_review.md | 334053 | `dc4f21ceca6a5aeaabca335e2526128e487dee8f479ce10b07b682b0bf80a74e` | MATCH |
| .agent/plan.md | 1279 | `afa5917e885bd79ceb75182809511a2afd04b244b326616d851b98bb757ae749` | MATCH |

`open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT: `['R-1098']` at
`1e1d7352d` and `['R-1099']` at C2 — both match the reviewer's own reading. `git diff --name-only
1d8f0a690 8dee5d78b` names exactly `.agent/decisions.md`, `.agent/live_review.md` and
`.agent/plan.md` — exactly G2's table, nothing else.

At C3 (`9711f756a`): the ledger at C2 is a byte-exact prefix of the ledger at C3 (measured by
reading both back with `git show <sha>:.agent/live_review.md` and confirming `c3.startswith(c2)` is
`True`), and what C3 adds is exactly `"\n"` plus one line beginning `Landed: R-1099 — ` and ending in
`"\n"` (measured: the added bytes are `\nLanded: R-1099 — the narration goldens now hold two
job_stopped key events against one ownership entry and two answered decisions of one task against
one entry, so beatActor's count of matching events is exercised and neither stop nor either decision
names an actor.\n`).

G3 THE CODE:
```
$ python3 -m ruff check tests/ui_contracts/test_story_autoplay.py .agent/authored/f039-r3-mutations.py
All checks passed!
REAL_EXIT=0
```
From `git show cfd50fb7f` (C4), the whole of `storyPacingOf`:
```typescript
export function storyPacingOf(raw: unknown): StoryPacing {
  if (!isPlainObject(raw)) return STORY_PACING_DEFAULT;
  return {
    stepMs: clampedField(raw, "step_ms", STORY_STEP_MS),
    chapterPauseMs: clampedField(raw, "chapter_pause_ms", STORY_CHAPTER_PAUSE_MS),
  };
}
```
and the whole of `autoplayStep`:
```typescript
export function autoplayStep(
  chapters: readonly StoryChapter[],
  seqs: readonly number[],
  position: number,
  pacing: StoryPacing,
  reducedMotion: boolean,
): AutoplayStep | null {
  const here = chapterAt(chapters, position);

  if (reducedMotion) {
    const nextChapter = chapters.slice(here + 1).find((chapter) => chapter.startSeq > position);
    if (nextChapter !== undefined) {
      return { position: nextChapter.startSeq, delayMs: pacing.chapterPauseMs };
    }
    const lastSeq = seqs[seqs.length - 1];
    if (lastSeq !== undefined && lastSeq > position) {
      return { position: lastSeq, delayMs: pacing.chapterPauseMs };
    }
    return null;
  }

  const next = seqs.find((seq) => seq > position);
  if (next === undefined) return null;
  const entersNewChapter = chapterAt(chapters, next) !== here;
  return {
    position: next,
    delayMs: pacing.stepMs + (entersNewChapter ? pacing.chapterPauseMs : 0),
  };
}
```
From `git show 9711f756a` (C3), the two R-1099 goldens:
```typescript
describe("R-1099 — two key events of one actor kind, so neither one is counted alone", () => {
  it("names nobody for either job_stopped when two share the ledger", () => {
    const rows = [
      row(1, "task_run_started", "t1"),
      row(2, "job_stopped", "", "stopped"),
      row(3, "job_resumed"),
      row(4, "job_stopped", "", "stopped"),
    ];
    const chapters = buildStoryChapters("job-r1099-a", T1, rows);
    const ownership = ownershipView([ownerEntry("job_stopped", "", "The operator stopped the job.")]);
    const beats = buildNarrationCards(chapters, rows, [], ownership).flatMap((card) => card.beats);
    expect(beats.find((b) => b.seq === 2)?.actor).toBeNull();
    expect(beats.find((b) => b.seq === 4)?.actor).toBeNull();
  });

  it("names nobody for either answered decision when one task answers twice", () => {
    const rows = [
      row(1, "task_run_started", "t1"),
      row(2, "task_decision_answered", "t1"),
      row(3, "task_decision_answered", "t1"),
    ];
    const chapters = buildStoryChapters("job-r1099-b", T1, rows);
    const ownership = ownershipView([ownerEntry("decision_answered", "t1", "Someone answered t1's decision.")]);
    const beats = buildNarrationCards(chapters, rows, [], ownership).flatMap((card) => card.beats);
    expect(beats.find((b) => b.seq === 2)?.actor).toBeNull();
    expect(beats.find((b) => b.seq === 3)?.actor).toBeNull();
  });
});
```

G4 THE TESTS, in the primary checkout at C6 (`edd4ce65a`), SERIALLY:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py tests/orchestration/test_feature_mission_adapter.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_review_archive_authority.py tests/orchestration/test_development_artifact_boundary.py tests/test_command_catalog.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
1881 passed, 5 skipped in 110.89s (0:01:50)
REAL_EXIT=0
```
The reviewer's own simulation (which carries C1a–C2 of this round plus its own version of C3–C5)
read `1873 passed, 10 skipped` at exit 0; five of those skips are toolchain nodes a worktree cannot
run and each PASSES here instead — none of the five SKIPPED lines above are toolchain-related, all
five are the same pre-existing D3/D12 quarantines the round 2 handback also named. This round's own
guard, `tests/ui_contracts/test_story_autoplay.py`, collects 5 nodes by `--collect-only -q`
(`test_the_step_is_the_birth_motion_token`, `test_the_chapter_pause_is_the_pulse_motion_token`,
`test_the_module_imports_only_the_two_named_modules`, `test_the_module_calls_chapterAt`,
`test_the_module_stays_pure`), which — together with the five converted toolchain skips and small
differences from the reviewer's own version of C3 — accounts for the count differing from the
reviewer's simulation reading.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=168", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks' status: `pass`. `fail_count`: 0. (R-1099 is Low, so `high_blockers_open` correctly
still reads pass while R-1099 itself stays open until the reviewer resolves it, per the block.)

G5 THE RED PROOFS — ONE RUN. `git worktree add --detach .remedy-wt/f039-r3-mut edd4ce65a` (C6),
then:
```
$ python3 -B .agent/authored/f039-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f039-r3-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r3-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=67 | guard exit=0 failed=0 passed=10
m1 (no chapter pause is ever added): vitest exit=1 failed=3 passed=64 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m2 (every step adds a chapter pause): vitest exit=1 failed=3 passed=64 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m3 (entering the first chapter from -1 adds no pause): vitest exit=1 failed=3 passed=64 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m4 (reduced motion is ignored): vitest exit=1 failed=5 passed=62 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m5 (reduced motion never steps to the last seq): vitest exit=1 failed=1 passed=66 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m6 (a wait of exactly 50 is refused): vitest exit=1 failed=1 passed=66 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m7 (a fractional wait is accepted): vitest exit=1 failed=1 passed=66 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m8 (the payload is read by stepMs rather than step_ms): vitest exit=1 failed=2 passed=65 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
m9 (STORY_STEP_MS is 400): vitest exit=1 failed=4 passed=63 | guard exit=1 failed=1 passed=9 | caught=True restored byte-identical=True
m10 (a setTimeout statement is added inside autoplayTotalMs): vitest exit=0 failed=0 passed=67 | guard exit=1 failed=1 passed=9 | caught=True restored byte-identical=True
m11 (the actor check of the count of matching events is deleted (R-1099)): vitest exit=1 failed=2 passed=65 | guard exit=0 failed=0 passed=10 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=67 | guard exit=0 failed=0 passed=10
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
All 11 mutations caught (m1–m9 and m11 by vitest, m9 and m10 also/only by the guard's purity and
token checks), every restore byte-identical, both controls green. No repair round needed. `git
worktree remove --force .remedy-wt/f039-r3-mut`, `git worktree prune`; `git worktree list | wc -l`:
62 (unchanged from step 4's reading, both before and after the run).

## Authored-text proofs

The block and the plan payload were each copied verbatim (`shutil.copyfile`) at C1a and compared
byte-identical against their sources under G1 above — both MATCH. The records-diff payload was
copied verbatim at C1b and compared byte-identical under G1 above — MATCH. `.agent/decisions.md`,
`.agent/live_review.md` and `.agent/plan.md` at C2 were verified byte- and sha256-identical to the
reviewer's own simulation readings under G2 above — all three MATCH. `records.diff` applied cleanly
by `git apply` (both `--check` and the real apply read exit 0).

## Deviations & assumptions

NO deviation from the block's ordered commit sequence: C1a, C1b, C2, C3, C4, C5, C6 were followed
exactly, with no dropped step, no reordering and no extra commit — unlike round 2, this round's G5
run caught all 11 mutations on its first pass, so no test correction was needed before C7.
`git diff --name-only 1e1d7352d HEAD` (before this commit) named exactly the round's tracked path
set: the four `.agent/authored/f039-r3-*` copies and the tool, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/plan.md`, `storyNarration.test.ts`, the two new files under
`apps/ui/src/components/story/`, and `tests/ui_contracts/test_story_autoplay.py` — no other file
under `apps/`, `packages/`, `tests/` or `docs/` was touched, `.agent/prose_slips.md`,
`.agent/candidates.md`, `.agent/operator_questions.md` and `README.md` were left alone, and
`docs/roadmap/features/T5_F039.md` was not read this round (T002's clauses came from DECISION F039
D4 and the block's S3–S4) but was not edited either, per constraint 3.

ASSUMPTION: the block left the exact pacing used in the "unfinished review" golden case (S5's last
"at least" item) unspecified, so `STORY_PACING_DEFAULT` was used for both the non-reduced-motion and
reduced-motion assertions there, hand-derived by tracing `readPhases` and `buildStoryChapters` over
the demo recording's first four rows (spans: build `[0, 1)`, review `[1, 4)`) and confirmed by
running the actual test before commit (53 vitest cases, all pass). The other "at least" items in S5
used the pacing the block itself names, 100/1000.

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1a | done | 288 insertions (255 + 33), under the 500-line cap |
| C1b | done | 55 insertions, matches the block's expected reading exactly |
| C2 | done | records.diff applied clean; numstat matches the block's table exactly; records match the reviewer's simulation byte for byte |
| C3 | done | R-1099's two goldens written per S1, the `Landed:` line appended per S2 |
| C4 | done | module written to S3–S4, imports exactly `StoryChapter` and `chapterAt`, purity confirmed |
| C5 | done | both new test files written, all goldens hand-derived and vitest/pytest-verified before commit |
| C6 | done | mutation tool added, `m1`–`m11`, following round 2's tool's route |
| C7 | done | this handback |
| G1 TRANSPORT | done | all three payload/copy readings MATCH |
| G2 THE RECORDS | done | all three file readings MATCH, `open_finding_ids` `['R-1098']`→`['R-1099']`, C3's prefix and Landed-line addition confirmed byte-exact |
| G3 THE CODE | done | ruff clean on the guard and the tool; `storyPacingOf`, `autoplayStep` and C3's two goldens quoted from the commits |
| G4 THE TESTS | done | 1881 passed, 5 skipped, exit 0; new guard collects 5 nodes; integrity 6/6 pass |
| G5 THE RED PROOFS | done | one run: all 11 mutations caught, all restored byte-identical, both controls green, exit 0 |
| G6 TREE AND PUSH | pending | runs after this commit and the push, reported in the worker's final reply |

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 3, with the resolution
of R-1099. Then T002's last part: the in-app story mode on the demo recording, the pacing's
configuration keys, its golden walkthrough and its assumption-log entry. Open findings in the
ledger: 1 (R-1099, landed and awaiting review). Operator questions open: 1.
