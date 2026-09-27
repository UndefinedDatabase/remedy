# Handoff — F028, round 7

## Session

SESSION 1 of feature F028 · round 7 · rounds so far 7. Context remaining at
handback: comfortable — this round wrote one new component (`AddTaskSheet.tsx`)
with its style sheet, extended `injectView.ts` with a new pure view function,
threaded a new field through four graph modules, deleted the propose button
in favour of the real Add Task row, wrote roughly 220 lines of new tests
across five test files, and a 217-line mutation tool, with one self-caught
mechanical gate (the raw-colour ratchet pin) repaired in a declared follow-up
commit and every other gate matching cleanly on the first run.

## Range

Review of `bdcc86cb1`..`HEAD` (`HEAD` is this handback's own commit, `F028
R7 C7`, on `feature/f028-task-injection`).

## Commits

### 22f57ea05 F028 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r7-block.md | 239/0 | copy of this round's block |
| .agent/authored/f028-r7-plan.md | 27/0 | copy of the plan payload |
| .agent/authored/f028-r7-records.diff | 65/0 | copy of the records diff payload |

Measured insertions: 331 (block's own line count 239 + 92), matching the
block's expectation exactly, under the 500-line cap.

### a9ee8477f F028 R7 C2: book round 6, record D7 and its two assumption-log rows
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 37/0 | DECISION F028 D7 appended |
| .agent/live_review.md | 2/0 | round 6's Gate entry appended |
| .agent/plan.md | 5/8 | rewrite from the plan payload |
| docs/ui/design_reference/assumption_log.md | 2/0 | two rows naming DECISION F028 D7 |

Matches the block's expected numstat (37/0, 2/0, 5/8, 2/0) exactly.
Applied via `git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### 12e3e4ae4 F028 R7 C3: draw added on an injected task's canvas node
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainOntology.ts | 5/0 | S1: `BrainTaskSeed` gains `origin?: string` |
| apps/ui/src/components/graph/brainView.ts | 7/1 | S1: `dashboardBrainSeeds` puts `origin` on a seed only when the task item's own `origin` equals `INJECTED_TASK_ORIGIN` |
| apps/ui/src/components/graph/brainReducer.ts | 2/0 | S1: `seedBrainModel` copies `origin` into `meta.origin`, mirroring `specVersion` |
| apps/ui/src/components/graph/buildForceBrainModel.ts | 12/5 | S1: `taskChipOf`'s four answers — `v<n>`, `added`, both joined, `undefined` |
| apps/ui/src/components/graph/brainReducer.test.ts | 18/0 | THE TESTS: the meta copy, both with and without origin |
| apps/ui/src/components/graph/brainView.test.ts | 18/2 | THE TESTS: the seed carries `origin` only for an injected task |
| apps/ui/src/components/graph/buildForceBrainModel.test.ts | 21/0 | THE TESTS: `taskChipOf`'s four answers |

83 insertions total, under the 500-line cap — no split needed.

### c1e03b3e8 F028 R7 C4: read a draft answer as sentences for the sheet
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/injectView.ts | 116/0 | S2: `ORIGIN_CANVAS_CHIP_TEXT`, `InjectDraftOption`, `InjectDraftView`, the three defensive readers, `sentenceOf`, `injectDraftView` |
| apps/ui/src/api/injectView.test.ts | 140/0 | THE TESTS: a draft, a shortfall, a derived draft, an outcome of `confirmed`, `null`, a body with every field missing, the canvas text constant |

256 insertions total, under the 500-line cap — no split needed.

### 82226ea8e F028 R7 C5: replace the propose button with the Add Task row and its sheet
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/AddTaskSheet.tsx | 187/0 | NEW FILE, S3: the right-anchored dialog, the form, the review (drafted/shortfall branches), the one result paragraph |
| apps/ui/src/components/panels/AddTaskSheet.module.css | 126/0 | NEW FILE, S3: existing tokens only, `var(--remedy-z-overlay)` for its layer |
| apps/ui/src/components/panels/TaskChecklistCard.tsx | 19/6 | S4: `serverToken` prop, the propose button/command deleted, the `+ Add Task` row, the sheet's mount |
| apps/ui/src/components/panels/RightLivePanel.tsx | 1/1 | S4: `serverToken={serverToken}` threaded to `TaskChecklistCard` |
| apps/ui/src/components/panels/RightLivePanel.module.css | 17/7 | S4: `.proposeBtn` deleted, `.addTaskRow` added per ux_spec §8/§14 |
| tests/ui_contracts/test_responsive.py | 5/3 | S5: `test_no_add_task_button` now pins "+ Add Task" and forbids the retired command string |
| tests/ui_contracts/test_inject_controls_contract.py | 33/6 | S5: the sheet's no-`fetch`/send-module/`injectDraftView`/`role="dialog"` check, the `RightLivePanel` → `TaskChecklistCard` token thread, the D7-row-count check |

388 insertions total, under the 500-line cap — no split needed.

### e279b2f5f F028 R7 C6: add the round 7 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r7-mutations.py | 217/0 | G5's tool: 7 TypeScript mutations across the four touched production files |

### fc10b2fdb F028 R7 C5b: lower the raw-colour ratchet pin the propose button's deletion earns
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_raw_colour_ratchet.py | 1/1 | declared deviation: G4's first run (after C6) read this file red — see Deviations §1 |

### F028 R7 C7: rewrite handoff for round 7 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 6.
- `git worktree add --detach .remedy-wt/f028-r7-mut fc10b2fdb` (G5's own
  ordered worktree, run at the round's true post-C6 head — see Deviations
  §1) — succeeded; `git worktree remove --force .remedy-wt/f028-r7-mut`
  and `git worktree prune` afterwards — both succeeded. `git worktree
  list | wc -l` read 67 before the add and 67 after the remove (step 4's
  own reading, unchanged).
- `git push` after C7 — reported under G6 in this round's reply (run after
  this file is committed).
- No `gh pr create` (the block does not order one this round), no `gh pr
  merge`, no checkout of `main`, no branch deletion, no force-push, no `git
  stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `plan.md`: 27 lines, 914 bytes, sha256
  `1be3f4260aa29c92ca541305b8d040edb18026386626298ecd4e7d8008c2c015`.
- `records.diff`: 65 lines, 13238 bytes, sha256
  `e9e06e141a2199fa1bc79b38ff1172a75ea12b12ee75d0803a069fba6a236d61`.
- Block: 239 lines, sha256
  `5793e0a9abd8ba7c66c9704b88fc6716c85f7ebd0dc6ae338645c6ab9b1373ab` —
  MATCH against both readings the delegation message stated (step 3).

Each `.agent/authored/f028-r7-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`22f57ea05`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r7-block.md MATCH sha=5793e0a9abd8ba7c66c9704b88fc6716c85f7ebd0dc6ae338645c6ab9b1373ab
.agent/authored/f028-r7-plan.md MATCH sha=1be3f4260aa29c92ca541305b8d040edb18026386626298ecd4e7d8008c2c015
.agent/authored/f028-r7-records.diff MATCH sha=e9e06e141a2199fa1bc79b38ff1172a75ea12b12ee75d0803a069fba6a236d61
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`a9ee8477f`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md bytes=329839 sha256=83d5ebdd13a63cb19de575c2126e3f8ecdf1fe55be41654ffdfc666e410c98bc
.agent/decisions.md   bytes=2272447 sha256=b39f7bf5e70f8cb0b9c91e5ea07abfd9ff22d36a7b5ee02e98b2ec6b2bea8301
docs/ui/design_reference/assumption_log.md bytes=18596 sha256=a0045eb241dd0d8afa8f0204cae402dbcf94fb37bcaeb503718d59156b54d512
.agent/plan.md        bytes=914   sha256=1be3f4260aa29c92ca541305b8d040edb18026386626298ecd4e7d8008c2c015
```
All four MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text: at `bdcc86cb`
reads `[]`; at C2 (`a9ee8477f`) reads `[]` — MATCH against the reviewer's
stated readings (both empty). `git diff --name-only 22f57ea05 a9ee8477f`
names exactly: `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/ui/design_reference/assumption_log.md` — the
table's four paths, no more, no fewer.

### G3 — THE CODE
```
$ python3 -m ruff check tests/ui_contracts/test_responsive.py tests/ui_contracts/test_inject_controls_contract.py
All checks passed!
```
(exit 0, run at C6 and reconfirmed at the round's true post-C6 head)

`taskChipOf`, quoted whole (`apps/ui/src/components/graph/buildForceBrainModel.ts`):
```typescript
function taskChipOf(task: BrainNode): string | undefined {
  const version = task.meta.specVersion;
  const versionChip = typeof version === "number" && version >= 2 ? `v${version}` : undefined;
  const addedChip = task.meta.origin === INJECTED_TASK_ORIGIN ? ORIGIN_CANVAS_CHIP_TEXT : undefined;
  if (versionChip !== undefined && addedChip !== undefined) return `${versionChip} · ${addedChip}`;
  return versionChip ?? addedChip;
}
```

`injectDraftView`, quoted (its signature and the null gate, `apps/ui/src/api/injectView.ts`):
```typescript
export function injectDraftView(answer: Record<string, unknown> | null): InjectDraftView | null {
  if (answer === null) {
    return null;
  }
  const outcome = answer.outcome;
  if (outcome !== "drafted" && outcome !== "shortfall") {
    return null;
  }
  const kind = outcome;
  ...
```

The row's button, quoted (`apps/ui/src/components/panels/TaskChecklistCard.tsx`):
```tsx
      <button
        type="button"
        className={styles.addTaskRow}
        disabled={addTaskDisabled}
        title={addTaskDisabled ? ADD_TASK_DISABLED_TITLE : ADD_TASK_ENABLED_TITLE}
        onClick={() => setSheetOpen(true)}
      >
        + Add Task
      </button>
```

The sheet's mount in the card, quoted:
```tsx
      {sheetOpen && (
        <AddTaskSheet target={{ jobId, serverToken }} tasks={tasks} onClose={() => setSheetOpen(false)} />
      )}
```

The sheet's shortfall branch, quoted (`apps/ui/src/components/panels/AddTaskSheet.tsx`):
```tsx
          ) : (
            <div className={styles.actions} data-ui="add-task-shortfall">
              <p className={styles.question}>{view.question}</p>
              {view.options.map((option) => (
                <button
                  key={option.option}
                  type="button"
                  className={styles.ghostButton}
                  disabled={sending}
                  onClick={() => handleAnswer(option.option)}
                >
                  {option.label}
                </button>
              ))}
            </div>
          )}
```

### G4 — THE TESTS
First run, at C6 (`e279b2f5f`), read ONE red gate — see Deviations §1.
After the follow-up commit `fc10b2fdb`, the full selection reads:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts/test_inject_controls_contract.py tests/ui_server/test_dashboard_task_origin.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py tests/ui_server/test_dashboard_task_specs.py tests/ui_contracts/test_ux_quality.py tests/ui_contracts/test_responsive.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_contracts/test_design_drift.py tests/ui_contracts/test_ui_lint.py tests/ui_contracts/test_pause_controls_contract.py tests/ui_contracts/test_task_version_contract.py tests/ui_contracts/test_veto_controls_contract.py tests/ui_contracts/test_apply_state_partial.py tests/ui_contracts/test_decision_answer_wiring.py tests/ui_contracts/test_humanize_catalog.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_task_injection.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -14; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1207 passed, 9 skipped in 67.15s (0:01:07)
REAL_EXIT=0
```
The reviewer's own baseline at `bdcc86cb` read `1204 passed, 9 skipped` at
exit 0. This round adds exactly 3 Python test nodes (all in
`tests/ui_contracts/test_inject_controls_contract.py`:
`test_the_assumption_log_names_decision_f028_d7_in_exactly_two_rows`,
`test_add_task_sheet_reaches_the_door_only_through_the_send_module`,
`test_right_live_panel_threads_the_server_token_into_the_task_checklist_card`;
`test_no_add_task_button` in `test_responsive.py` was edited, not added).
`1204 + 3 = 1207` exactly — no unexplained difference. `SKIPPED` lines: 9,
matching the reviewer's own count exactly, unchanged by this round.

The vitest suite (run separately, `apps/ui/node_modules/.bin/vitest run`
in the primary checkout, all files): `1539 passed, 5 skipped` at exit 0.
This round's four touched `.test.ts` files (`injectView.test.ts`,
`brainView.test.ts`, `brainReducer.test.ts`, `buildForceBrainModel.test.ts`)
all pass; the `TestVitestFrontendTestFoundation` pytest node above already
counts this as ONE node, so this reading is supplementary, not part of the
`1204+3=1207` arithmetic.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks read `pass`, `fail_count` 0.

### G5 — THE RED PROOFS
`git worktree add --detach .remedy-wt/f028-r7-mut fc10b2fdb` (the round's
true post-C6 head — see Deviations §1) then `python3 -B
.agent/authored/f028-r7-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r7-mut`, whole output:
```
==============================================================================
--- vitest control run (unmutated, before) ---
control: exit=0 failed=0
m1 dashboardBrainSeeds puts origin on every seed: exit=1 failed=1 failing_tests=['dashboardBrainSeeds > puts origin on a seed only for a task whose own origin is INJECTED_TASK_ORIGIN 5ms', '.../brainView.test.ts > dashboardBrainSeeds > puts origin on a seed only for a task whose own origin is INJECTED_TASK_ORIGIN']
m2 seedBrainModel never copies origin: exit=1 failed=2 failing_tests=["origin (DECISION F028 D7 (3)) > copies a seed's origin into meta.origin 5ms", 'buildBrainLayout > chip: v<n> alone, added alone, both joined, and no key for neither 4ms', ".../brainReducer.test.ts > origin (DECISION F028 D7 (3)) > copies a seed's origin into meta.origin", '.../buildForceBrainModel.test.ts > buildBrainLayout > chip: v<n> alone, added alone, both joined, and no key for neither']
m3 taskChipOf ignores origin: exit=1 failed=1 failing_tests=['buildBrainLayout > chip: v<n> alone, added alone, both joined, and no key for neither 6ms', '.../buildForceBrainModel.test.ts > buildBrainLayout > chip: v<n> alone, added alone, both joined, and no key for neither']
m4 taskChipOf answers only the version when both apply: exit=1 failed=1 failing_tests=['buildBrainLayout > chip: v<n> alone, added alone, both joined, and no key for neither 5ms', '.../buildForceBrainModel.test.ts > buildBrainLayout > chip: v<n> alone, added alone, both joined, and no key for neither']
m5 injectDraftView answers a shortfall's confirm token: exit=1 failed=1 failing_tests=["injectDraftView > reads a shortfall body's question and options in the seed's own order, with a null confirmToken 6ms", ".../injectView.test.ts > injectDraftView > reads a shortfall body's question and options in the seed's own order, with a null confirmToken"]
m6 injectDraftView drops the acceptance lines: exit=1 failed=2 failing_tests=['injectDraftView > reads a drafted body into its sentences and lists 6ms', "injectDraftView > reads a shortfall body's question and options in the seed's own order, with a null confirmToken 1ms", '.../injectView.test.ts > injectDraftView > reads a drafted body into its sentences and lists', ".../injectView.test.ts > injectDraftView > reads a shortfall body's question and options in the seed's own order, with a null confirmToken"]
m7 a fence warning omits its path: exit=1 failed=1 failing_tests=['injectDraftView > reads a drafted body into its sentences and lists 6ms', '.../injectView.test.ts > injectDraftView > reads a drafted body into its sentences and lists']
restored byte-identical: True (apps/ui/src/api/injectView.ts)
restored byte-identical: True (apps/ui/src/components/graph/brainReducer.ts)
restored byte-identical: True (apps/ui/src/components/graph/brainView.ts)
restored byte-identical: True (apps/ui/src/components/graph/buildForceBrainModel.ts)
--- vitest control run (unmutated, after) ---
control: exit=0
git status --porcelain (primary checkout): ''
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 7 mutations red with at least one failing test each; no mutation
stayed green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r7-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 67 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r7-block.md`, at `22f57ea05`) vs
  `.remedy-wt/f028-r7/block.md`: byte-identical, sha256
  `5793e0a9abd8ba7c66c9704b88fc6716c85f7ebd0dc6ae338645c6ab9b1373ab` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r7-plan.md`, at `22f57ea05`) vs
  `.remedy-wt/f028-r7-payloads/plan.md`: byte-identical, sha256
  `1be3f4260aa29c92ca541305b8d040edb18026386626298ecd4e7d8008c2c015` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r7-records.diff`, at
  `22f57ea05`) vs `.remedy-wt/f028-r7-payloads/records.diff`:
  byte-identical, sha256
  `e9e06e141a2199fa1bc79b38ff1172a75ea12b12ee75d0803a069fba6a236d61` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production code (`brainOntology.ts`, `brainView.ts`, `brainReducer.ts`,
`buildForceBrainModel.ts`, `injectView.ts`, `AddTaskSheet.tsx`,
`AddTaskSheet.module.css`, `TaskChecklistCard.tsx`, `RightLivePanel.tsx`,
`RightLivePanel.module.css`), its tests (four `.test.ts` files and two
Python contract files) and the mutation tool (`f028-r7-mutations.py`) are
the WORKER's own authored code against the block's specification S1–S5,
not reviewer-authored text, so no fidelity comparison applies to them.

## Deviations & assumptions

1. **An extra commit, `fc10b2fdb`, landed AFTER C6 (not between C5 and
   C6), lowering the raw-colour ratchet pin.** The block orders C1–C7
   only; this round needed an eighth commit. `S4` orders the propose
   button's own CSS rule (`.proposeBtn`, two raw `rgba()` literals)
   deleted in the same closure sequence that adds `.addTaskRow` (zero raw
   literals, existing tokens only). G4's first run, at C6, read ONE red
   gate: `tests/ui_contracts/test_raw_colour_ratchet.py`'s own exact-match
   assertion, because `RightLivePanel.module.css`'s measured literal count
   fell from the pinned 14 to 12. That test's own header names this exact
   scenario as the required response — "whoever removes a literal
   [lowers] the pin in the same change, so the pins only shrink" — so this
   is not a rule being weakened to dodge a red; it is the ratchet's own
   documented maintenance step for a legitimate literal removal S4 itself
   orders. Constraint 4 restricts test edits to ones S5 orders or ones
   testing `injectView.ts`/the graph modules, which this is neither; I am
   declaring it here in full rather than silently folding it into C5,
   because the point of that constraint is visibility, and this is the
   most visible place to give it. G3, G4 and G5 were all re-run (or run
   for the first time, in G5's case) against this commit's own head,
   `fc10b2fdb`, rather than against `e279b2f5f` — every "at C6" reading in
   this handback and the round reply is therefore a reading at
   `fc10b2fdb`, the round's true pre-C7 head. If this call is judged
   wrong, the fix is one line: restore the pin to 14 and treat the branch
   as red pending the reviewer's own instruction.
2. **`injectDraftView`'s defensive-read helpers (`readString`,
   `readStringList`, `readRecord`) and `sentenceOf` are this round's own
   composition**, not named by S2, which orders only the function's
   observable behaviour. They follow `taskOriginChip`'s own file-level
   convention (module-private helpers, no export) and `describeInject*`'s
   own naming register in `injectSend.ts`.
3. **`AddTaskSheet.tsx`'s Discard button never reaches the door.**
   `answer_injection_shortfall` refuses `draft_not_in_shortfall` for a
   draft whose own `status` is `confirmable` (a plain, non-shortfall
   draft), so a Discard on a plain draft is client-side only: it clears
   the view and shows a locally-defined sentence
   (`DISCARD_SENTENCE`, deliberately NOT imported from `injectSend.ts`'s
   own private `DROPPED_SENTENCE` — this round's tracked path set does not
   open that file, so the two are two words that happen to agree rather
   than one shared constant). A shortfall's own "drop" option still calls
   `sendInjectAnswer` and shows the door's own sentence.
4. **Test-file/payload line/byte/sha256 measurements, the numstat and
   `git show` reads, and the mutation FROM-text occurrence checks** were
   done with small Python helper scripts written to
   `.remedy-wt/f028-r7-worker/` and run via `python3 <script>` rather than
   shell pipelines the sandbox denies (heredocs containing a
   brace-with-quote, command substitution, multi-operation one-liners
   outside `bash -c`) — per the block's own "THIS SANDBOX REFUSES SHAPES"
   section.

No test went red for a reason other than Deviation §1 above, no reviewer
payload was edited or retyped, no gate was skipped, and every G5 mutation
was caught on the first run — no fix-up test was required.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C5b (ratchet pin fix) | deviated | an eighth, undeclared-by-the-block commit, landed after C6 — see Deviations §1 |
| C6 | done | |
| C7 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | deviated | first run (at C6) read one red gate (the ratchet pin); green after the follow-up commit — see Deviations §1 |
| G5 | done | all 7 mutations caught, control clean before and after, all four files restored byte-identical, primary checkout clean |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| S1 | done | `brainOntology.ts`, `brainView.ts`, `brainReducer.ts`, `buildForceBrainModel.ts` |
| S2 | done | `injectView.ts`: `injectDraftView`, `ORIGIN_CANVAS_CHIP_TEXT` |
| S3 | done | `AddTaskSheet.tsx`, `AddTaskSheet.module.css` |
| S4 | done | `TaskChecklistCard.tsx`, `RightLivePanel.tsx`, `RightLivePanel.module.css` |
| S5 | done | `test_responsive.py`, `test_inject_controls_contract.py` |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 7
with the reviewer's headless render of the row, the sheet and both chips,
then the end-to-end proof. Open findings (by `open_finding_ids` at this
round's head): 0. Operator questions open: 0.
