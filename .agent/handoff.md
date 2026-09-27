# Handoff — F029, round 5

## Session

SESSION 1 of feature F029 · round 5 · rounds so far 5. Context remaining at
handback: comfortable — reading `types.ts`, `remedyApi.ts`/its test,
`injectView.ts`, `taskSpecView.ts`, `DetailPopover.tsx`/its CSS,
`TaskVersionList.tsx`, `brainView.ts`, `brainOntology.ts`, `brainReducer.ts`,
`buildForceBrainModel.ts`, `BrainGraphStage.tsx`, `useTimelineScrub.ts` and
their tests, then drafting S1–S5 plus their five new/extended test files, the
new contract test and the mutation tool took the bulk of it; one small repair
was found and fixed within the round (below); every gate ran clean afterward,
with ample context left had a further repair round been needed.

## Range

Review of `47c63354b`..`HEAD` (`HEAD` is this handback's own commit, `F029 R5
C7`, on `feature/f029-subtree-rerun`).

## Commits

### eb78f00f2 F029 R5 C1: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r5-block.md | 237/0 | copy of this round's block |
| .agent/authored/f029-r5-booking.diff | 76/0 | copy of the booking diff payload |
| .agent/authored/f029-r5-plan.md | 35/0 | copy of the plan payload |

Measured insertions: 348 (block's own line count 237 + 111), matching the
block's expectation exactly, under the 500-line cap.

### 48eaf23d1 F029 R5 C2: book round 4, record D5 and its two assumption-log rows
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 39/0 | DECISION F029 D5 appended |
| .agent/live_review.md | 2/0 | round 4's Gate entry appended |
| .agent/plan.md | 9/9 | rewrite from the plan payload |
| .agent/prose_slips.md | 1/0 | one line appended |
| docs/ui/design_reference/assumption_log.md | 2/0 | the chip's row and the list's row, both naming DECISION F029 D5 |

Matches the block's expected numstat (39/0, 2/0, 9/9, 1/0, 2/0) exactly.
Applied via `git apply --check` (exit 0) then the real apply (exit 0) of
`booking.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### ee3c2d13c F029 R5 C3: read a task's attempts into the browser
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/types.ts | 22/1 | S1: `RemedyTaskAttempt`; `RemedyTaskItem` gains `attempt?`/`attempts?` |
| apps/ui/src/api/remedyApi.ts | 51/1 | S1: `normalizeTaskAttemptNumber`, `normalizeTaskAttemptEntry`, `normalizeTaskAttempts`, threaded into the task map |
| apps/ui/src/api/remedyApi.test.ts | 98/0 | valid/missing/mistyped attempt and attempts, a dropped invalid entry, per-field snake_case reads |

171 total insertions, under the 500-line cap; no split needed.

### 9cda29c12 F029 R5 C4: draw attempt n on a rerun task's canvas node
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainOntology.ts | 5/0 | S2: `BrainTaskSeed.attempt?` |
| apps/ui/src/components/graph/brainReducer.ts | 2/0 | S2: `seedBrainModel` copies `seed.attempt` into `meta.attempt` |
| apps/ui/src/components/graph/brainView.ts | 4/1 | S2: `dashboardBrainSeeds` puts `attempt` on a seed only when the item's `attempt` is 2 or more |
| apps/ui/src/components/graph/buildForceBrainModel.ts | 13/9 | S2: `taskChipOf` joins `v<n>`, "added" and `attemptChipText(n)` |
| apps/ui/src/api/attemptView.ts | 17/0 | new file, S2 slice only: `attemptChipText(n)` |
| apps/ui/src/api/attemptView.test.ts | 9/0 | new file, S2 slice only: `attemptChipText` tests |
| apps/ui/src/components/graph/brainReducer.test.ts | 19/0 | `attempt (DECISION F029 D5)` describe block |
| apps/ui/src/components/graph/brainView.test.ts | 20/2 | `task()` helper gains an `attempt` param; `dashboardBrainSeeds` attempt threshold test |
| apps/ui/src/components/graph/buildForceBrainModel.test.ts | 23/0 | `taskChipOf` every-combination test |

112 total insertions, under the 500-line cap; no split needed.

### d7baa20ee F029 R5 C5: list a task's attempts in its detail popover
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/attemptView.ts | 150/0 | S3 slice added: `TaskAttemptChange`, `TaskAttemptRow`, the five fact helpers, `changesFromFacts`, `currentStateWord`, `taskAttemptRows`, `attemptFactsSentence` |
| apps/ui/src/api/attemptView.test.ts | 174/1 | S3 slice added: `taskAttemptRows` and `attemptFactsSentence` tests |
| apps/ui/src/components/detail/TaskAttemptList.tsx | 56/0 | new file, S4: the Attempts list, shaped as `TaskVersionList.tsx` |
| apps/ui/src/components/detail/DetailPopover.tsx | 9/0 | S4: mounts `<TaskAttemptList key={task?.id ?? ""} rows={taskAttemptRows(task)} />` directly after `TaskVersionList` |
| tests/ui_contracts/test_attempt_fan_contract.py | 47/0 | new file, S5: the four pins |

436 total insertions, under the 500-line cap; no split needed.

### 4eb233df7 F029 R5 C6: add the round 5 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r5-mutations.py | 259/0 | the G5 mutation (red-proof) tool, covering m1–m8 across `brainView.ts`, `brainReducer.ts`, `buildForceBrainModel.ts`, `attemptView.ts` and `remedyApi.ts` |

### 1613db884 F029 R5 correction: fix a wrong assertion in this round's own attemptView.test.ts
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/attemptView.test.ts | 1/1 | "an unchanged fact between two earlier rows earns no entry in changes" set the first attempt's `reviewerVerdict` to `"fail"` but asserted the row's `before` as `"no review verdict"`; corrected to `"the reviewer said fail"` — see Deviations |

### (this commit) F029 R5 C7: rewrite handoff for round 5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file |

## External actions

`git worktree add --detach .remedy-wt/f029-r5-mut 1613db884` — created the
disposable mutation worktree at the corrected HEAD (one commit past C6; see
Deviations for why). `git worktree remove --force .remedy-wt/f029-r5-mut` then
`git worktree prune` — removed it after G5; `git worktree list | wc -l` read 61
both before and after, matching the step-4 reading. `git push origin
feature/f029-subtree-rerun` — reported below under G6; its real outcome is in
the reply to the delegator, since C7 cannot contain it. No PR opened, no
merge, no branch deleted, no force-push, no stash.

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty;
  `git branch --show-current` → `feature/f029-subtree-rerun`; `git log
  --oneline -1` → `47c63354b`.
- Block bytes (R-0954): measured 237 lines, sha256
  `c591cf57e83a33279ca0a8910f9600b7accf5138297feba565f4572139e6cc00` — both
  match the delegation message's readings exactly.
- `git worktree list | wc -l` → 61.

**PAYLOADS** — both matched the table exactly:
`booking.diff` 76 lines / 15682 bytes /
`a77e470df3ae910a10f3f70a524fb11bb5e16c94e49d87c23dfd814f170be447`;
`plan.md` 35 lines / 1326 bytes /
`53c31d09cbe8a9a97be9e9e56595ee8e747016f00f416a9eb97bc59726bb9deb`.

**G1 TRANSPORT** — each `.agent/authored/f029-r5-*` copy read via `git show
eb78f00f2:<path>` equals its source byte for byte: block copy (18802 bytes) ==
source (True, sha256 `c591cf57...139e6cc00`); booking.diff copy (15682 bytes)
== source (True, sha256 `a77e470d...4f170be447`); plan.md copy (1326 bytes) ==
source (True, sha256 `53c31d09...726bb9deb`).

**G2 THE RECORDS** — sha256 of each file read via `git show 48eaf23d1:<path>`
equals the reviewer's reading exactly:
`.agent/decisions.md` 2299065 bytes,
`9cd9b51634af35901a607bca5096ff10cb9e357647ee79716623dbaa2017a344` — match.
`.agent/live_review.md` 323333 bytes,
`5cc9412ed8a851c4953a55568f0403a49196e34f9ab95ef569e1e78986ecf901` — match.
`.agent/plan.md` 1326 bytes,
`53c31d09cbe8a9a97be9e9e56595ee8e747016f00f416a9eb97bc59726bb9deb` — match.
`.agent/prose_slips.md` 373961 bytes,
`477de5ee5d7c4532ea464030c8ba02ac8afa2170fe407edce8e02bffa1e63de4` — match.
`docs/ui/design_reference/assumption_log.md` 20094 bytes,
`00cf320ab7b049bb192ed5f97ae80ffbbd96971a11b2cc10d6570042a4bba45e` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s
text: at `47c63354b` → `[]`; at `48eaf23d1` → `[]` — both match the reviewer's
stated readings. `git diff --name-only eb78f00f2 48eaf23d1` → exactly the five
paths of the table, nothing else.

**G3 THE CODE** —
```
python3 -m ruff check tests/ui_contracts/test_attempt_fan_contract.py
```
→ `All checks passed!`, exit 0. Quoted from the diff (all three match what is
committed at HEAD):

`taskChipOf` (`buildForceBrainModel.ts`):
```ts
function taskChipOf(task: BrainNode): string | undefined {
  const version = task.meta.specVersion;
  const versionChip = typeof version === "number" && version >= 2 ? `v${version}` : undefined;
  const addedChip = task.meta.origin === INJECTED_TASK_ORIGIN ? ORIGIN_CANVAS_CHIP_TEXT : undefined;
  const attempt = task.meta.attempt;
  const attemptChip = typeof attempt === "number" && attempt >= 2 ? attemptChipText(attempt) : undefined;
  const parts = [versionChip, addedChip, attemptChip].filter((part): part is string => part !== undefined);
  return parts.length > 0 ? parts.join(" · ") : undefined;
}
```

`taskAttemptRows` (`attemptView.ts`):
```ts
export function taskAttemptRows(item: RemedyTaskItem | undefined): TaskAttemptRow[] {
  if (!item || !item.attempts || item.attempts.length === 0) return [];
  const rows: TaskAttemptRow[] = [];
  let previousFacts: string[] | null = null;
  for (const entry of item.attempts) {
    const facts = attemptFacts(entry);
    rows.push({
      attempt: entry.attempt,
      label: `Attempt ${entry.attempt}`,
      facts,
      changes: changesFromFacts(previousFacts, facts),
      current: false,
    });
    previousFacts = facts;
  }
  rows.push({
    attempt: item.attempt as number,
    label: `Attempt ${item.attempt} · current`,
    facts: [`Now ${currentStateWord(item.state)}`],
    changes: [],
    current: true,
  });
  return rows;
}
```

Mount in `DetailPopover.tsx`:
```tsx
<TaskAttemptList key={task?.id ?? ""} rows={taskAttemptRows(task)} />
```

**G4 THE TESTS** — the exact selection, serially, real exit code:
```
python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_task_attempts.py tests/ui_server/test_dashboard_task_origin.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py tests/ui_server/test_dashboard_task_specs.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
```
First run (at C6, `4eb233df7`, before the correction): `1 failed, 1611 passed,
11 skipped`, real exit code 1 — the one failure was
`src/api/attemptView.test.ts > taskAttemptRows > an unchanged fact between two
earlier rows earns no entry in changes`, inside `TestVitestFrontendTestFoundation
::test_vitest_passes`'s subprocess vitest run; a wrong assertion in this
round's own test (see Deviations), not a production defect. After the
correction commit: `1612 passed, 11 skipped`, real exit code 0. All eleven
`SKIPPED` lines cite an F252 quarantine (four in `tests/ui_contracts/`, six in
`test_named_bugs.py`, one in `test_agent_tooling.py`) — the same eleven the
reviewer's own base reading at `47c63354` already carried.
Accounting for the difference from 1608: this round's own
`tests/ui_contracts/test_attempt_fan_contract.py` adds exactly 4 new pytest
nodes (`test_task_attempt_list_touches_no_network`,
`test_the_popover_mounts_task_attempt_list_through_taskattemptrows`,
`test_build_force_brain_model_calls_attempt_chip_text`,
`test_the_assumption_log_names_decision_f029_d5_in_exactly_two_rows`); every
other file this round touches is a `.ts`/`.tsx` module or `.test.ts` file
exercised INSIDE the single `test_vitest_passes` pytest node, so it adds no
further pytest node. 1608 + 4 = 1612, exactly the passed count above; no
unexplained difference. Then `python3 -m apps.cli.main integrity check --json`
→ all 6 checks `pass` (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`), `fail_count: 0`, `ok: true`.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f029-r5-mut
1613db884` (the corrected HEAD, not literally C6 — see Deviations), then
`python3 -B .agent/authored/f029-r5-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r5-mut`:
```
control (unmutated, first): exit=0 failed=0
m1 dashboardBrainSeeds puts attempt on every seed: exit=1 failed=1 — brainView.test.ts's threshold test
m2 seedBrainModel never copies attempt: exit=1 failed=2 — brainReducer.test.ts's meta.attempt copy test, buildForceBrainModel.test.ts's combination test
m3 taskChipOf ignores attempt: exit=1 failed=1 — buildForceBrainModel.test.ts's combination test
m4 taskChipOf drops v<n> when attempt applies: exit=1 failed=1 — buildForceBrainModel.test.ts's combination test
m5 taskAttemptRows omits the current row: exit=1 failed=6 — attemptView.test.ts's third-attempt-changes test and all five current-row-state tests
m6 an earlier row's changes compare with the FIRST earlier row: exit=1 failed=1 — attemptView.test.ts's third-attempt-changes test
m7 the model fact reads 'it ran on ' with an empty override: exit=1 failed=1 — attemptView.test.ts's model-fact test
m8 the normalisation keeps an attempt of 0: exit=1 failed=1 — remedyApi.test.ts's mistyped-attempt test
restored byte-identical: True (all 5 touched files)
control (unmutated, last): exit=0
git status --porcelain (primary checkout): '' (empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation was red on the first run; no repair round was needed for the
production code (only the test correction above, made before this gate ran).
Then `git worktree remove --force .remedy-wt/f029-r5-mut`, `git worktree
prune`; `git worktree list | wc -l` → 61, matching the step-4 reading.

**Constraint 3** — `git diff --name-only 47c63354b`, run once more after
writing this file, lists exactly the 24 paths inside the block's tracked path
set: `.agent/authored/f029-r5-block.md`, `.agent/authored/f029-r5-booking.diff`,
`.agent/authored/f029-r5-mutations.py`, `.agent/authored/f029-r5-plan.md`,
`.agent/decisions.md`, `.agent/handoff.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md`, `apps/ui/src/api/attemptView.test.ts`,
`apps/ui/src/api/attemptView.ts`, `apps/ui/src/api/remedyApi.test.ts`,
`apps/ui/src/api/remedyApi.ts`, `apps/ui/src/api/types.ts`,
`apps/ui/src/components/detail/DetailPopover.tsx`,
`apps/ui/src/components/detail/TaskAttemptList.tsx`,
`apps/ui/src/components/graph/brainOntology.ts`,
`apps/ui/src/components/graph/brainReducer.test.ts`,
`apps/ui/src/components/graph/brainReducer.ts`,
`apps/ui/src/components/graph/brainView.test.ts`,
`apps/ui/src/components/graph/brainView.ts`,
`apps/ui/src/components/graph/buildForceBrainModel.test.ts`,
`apps/ui/src/components/graph/buildForceBrainModel.ts`,
`docs/ui/design_reference/assumption_log.md`,
`tests/ui_contracts/test_attempt_fan_contract.py` — 25 paths in total (the
list above has 24 plus `.agent/handoff.md` itself); no path outside the set
changed — not `RunDetailPopover.tsx`, not `ui_server.py`, nothing under
`packages/`.

## Authored-text proofs

`.agent/authored/f029-r5-block.md`, `f029-r5-booking.diff` and
`f029-r5-plan.md` (C1, `eb78f00f2`): each read back via `git show` equals its
source (`.remedy-wt/f029-r5/block.md`, `.remedy-wt/f029-r5-payloads/booking.diff`,
`.remedy-wt/f029-r5-payloads/plan.md`) byte for byte — see G1 above.
`.agent/authored/f029-r5-mutations.py` (C6, `4eb233df7`) is this session's OWN
tool, not reviewer-authored text, so it carries no fidelity comparison; its
behavior is proved instead by G5's live run above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |
| correction | done | fixed this round's own wrong test assertion before C7; declared below |
| G1 transport | done | PASS — all copies byte-identical |
| G2 the records | done | PASS — sha256 and open_finding_ids both match |
| G3 the code | done | PASS — ruff exit 0, three functions/mount quoted from disk |
| G4 the tests | done | PASS — 1612 passed, 11 skipped, exit 0 after the correction; +4 nodes fully accounted |
| G5 the red proofs | done | PASS — all 8 mutations caught, both controls green, restored byte-identical |
| S1 the types | done | `RemedyTaskAttempt`, `RemedyTaskItem.attempt`/`.attempts`, normalization in `remedyApi.ts` |
| S2 the chip | done | `BrainTaskSeed.attempt`, `dashboardBrainSeeds` threshold, `seedBrainModel` copy, `taskChipOf` join, `attemptChipText` |
| S3 the rows | done | `taskAttemptRows`, `attemptFactsSentence` in `attemptView.ts` |
| S4 the list | done | `TaskAttemptList.tsx`, mounted after `TaskVersionList` in `DetailPopover.tsx` |
| S5 the pins | done | `tests/ui_contracts/test_attempt_fan_contract.py`, four checks |

## Deviations & assumptions

One correction made within the round, declared here per constraint 4 (a test
this round wrote that is wrong may be corrected before C7):

1. `apps/ui/src/api/attemptView.test.ts`'s "an unchanged fact between two
   earlier rows earns no entry in changes" test set the FIRST attempt's
   `reviewerVerdict` to `"fail"`, which means its own `facts[1]` reads `"the
   reviewer said fail"` — not `"no review verdict"`, which is only what an
   EMPTY `reviewerVerdict` reads. The test asserted the wrong `before` value.
   `TestVitestFrontendTestFoundation::test_vitest_passes` (part of G4's
   selection) caught it on the first run at C6 (`4eb233df7`): 1 failed, 1611
   passed. Corrected the assertion's `before` to `"the reviewer said fail"` in
   a new commit (`1613db884`, "F029 R5 correction: ..."), re-ran the vitest
   file directly (24 passed) and the full G4 selection (1612 passed, 0
   failed, exit 0). No production file was touched by this fix, only the
   test's own assertion.

A consequence of the correction landing in a commit of its own: G5's worktree
was created at `1613db884` (one commit past C6, `4eb233df7`) rather than
literally at C6, because C6's own tree still carries the pre-correction wrong
assertion, which would fail the mutation tool's unmutated control run before
any mutation is even applied. Declared here rather than silently reading "at
C6" — the deviation is in WHICH commit G5's worktree was cut from, not in the
tool or the mutations themselves.

No commit was split, reordered or dropped from the block's ordered sequence
(C1–C6 as named, plus one correction commit before C7); no existing test
outside this round's own new file was edited; no gate went red in its FINAL
(post-correction) state.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 5
with the reviewer's headless render of the chip and the Attempts list, then
T003's control half — the Rerun control, the send module with its cost
confirmation, and the report naming an override.

Open findings: 0. Operator questions: 0.
