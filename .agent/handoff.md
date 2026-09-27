# Handoff — F028, round 6

## Session

SESSION 1 of feature F028 · round 6 · rounds so far 6. Context remaining at
handback: comfortable — this round wrote one new Python helper, one new
pure TypeScript view module, one new TypeScript send module (three
builders, a submit, a describe function and three flows), two component
edits and two CSS additions, plus roughly 900 lines of new tests and a
292-line mutation tool, with zero self-caught implementation bugs in the
production code and every gate matching cleanly on the first run.

## Range

Review of `d82a407c1`..`HEAD` (`HEAD` is this handback's own commit, `F028
R6 C7`, on `feature/f028-task-injection`).

## Commits

### d88c2eafb F028 R6 C1: copy round 6 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r6-block.md | 246/0 | copy of this round's block |
| .agent/authored/f028-r6-plan.md | 30/0 | copy of the plan payload |
| .agent/authored/f028-r6-records.diff | 64/0 | copy of the records diff payload |

Measured insertions: 340 (block's own line count 246 + 94), matching the
block's expectation exactly, under the 500-line cap.

### e19046c9c F028 R6 C2: book round 5, resolve R-1078, record D6 and its assumption-log row
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 35/0 | DECISION F028 D6 appended |
| .agent/live_review.md | 4/0 | round 5's Gate entry and R-1078's `Done:` paragraph appended |
| .agent/plan.md | 7/7 | rewrite from the plan payload |
| docs/ui/design_reference/assumption_log.md | 1/0 | one row naming DECISION F028 D6 |

Matches the block's expected numstat (35/0, 4/0, 7/7, 1/0) exactly.
Applied via `git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### 386302c26 F028 R6 C3: carry each task's origin on the dashboard
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | 17/0 | S1: new helper `_task_origin(t)` reading `inputs["plan"]["origin"]` when `inputs["plan"]` is a dict and the value a non-empty string, else `""`; wired as the task item's LAST key |
| apps/ui/src/api/types.ts | 1/1 | S1: `RemedyTaskItem` gains `origin?: string` |
| apps/ui/src/api/remedyApi.ts | 1/0 | S1: `normalizeDashboardPayload` sets `origin` only when the raw value is a non-empty string |
| tests/ui_server/test_dashboard_task_origin.py | 95/0 | NEW FILE: an injected task's item names `human_injected`, a planned task's and a task with no plan inputs at all name `""`; the last-key ordering is also asserted |

114 insertions total, under the 500-line cap — no split needed.

### c5e8b0074 F028 R6 C4: show Added by you on an injected task in the list and the popover
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/injectView.ts | 39/0 | NEW FILE, S2: `INJECTED_TASK_ORIGIN`, `ORIGIN_CHIP_TEXT`, `ORIGIN_CHIP_TITLE`, `taskOriginChip` |
| apps/ui/src/api/injectView.test.ts | 35/0 | NEW FILE, S5: every branch of `taskOriginChip` |
| apps/ui/src/components/panels/TaskChecklistCard.tsx | 3/0 | S4: the pill mounted after the label, `chip = taskOriginChip(row)` |
| apps/ui/src/components/panels/RightLivePanel.module.css | 18/0 | S4: `.originChip`, `.decisionChip`'s declarations plus `margin-left: 6px; flex: none;` |
| apps/ui/src/components/detail/DetailPopover.tsx | 5/0 | S4: the same pill in the status row, before the version chip |
| apps/ui/src/components/detail/DetailPopover.module.css | 6/0 | S4: `.originChip`, `.versionChip`'s declarations with `margin-left: auto` replaced by `margin-left: 6px` |
| tests/ui_contracts/test_inject_controls_contract.py | 64/0 | NEW FILE, S5: no `fetch(` in the three files, `taskOriginChip(` present in both components, the send module's three ids equal the door's three constants, the assumption log names DECISION F028 D6 exactly once |

170 insertions total, under the 500-line cap — no split needed.

### 29f0a7531 F028 R6 C5a: add the browser's send module for the three injection commands
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/injectSend.ts | 425/0 | S3: the three command ids, `INJECT_SHORTFALL_OPTIONS`, the two deadlines, the three request builders, `submitInjectRequest`, `describeInjectResult` (the four 200 outcomes, the sixteen 409 sentences, the 400-on-`text` case, the pause fallback), `injectAnswerOf`, and `sendInjectDraft`/`sendInjectConfirm`/`sendInjectAnswer` |

### b0c2f29ed F028 R6 C5b: test the send module's requests, refusals and each flow
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/injectSend.test.ts | 448/0 | S5: the three exact requests, each null case, the token never in the path, every refusal code's sentence, the unknown code, the 400 on `text`, the pause fallback, each 200 outcome, `injectAnswerOf`, and each send function's network/no-network/deadline paths |

**DECLARED DEVIATION (constraint 2 split):** the block's bundle names one
C5 carrying `injectSend.ts` and `injectSend.test.ts`. Measured before
committing: 425 (module) + 448 (test) = 873, over the 500-line cap, so
this round split it into C5a (the module alone, 425 insertions, subject
above) and C5b (the test file alone, 448 insertions, subject above), per
constraint 2's own instruction. The test file did not exist at C5a, so no
node in G4's selection was affected between the two parts; G4 was run
once, after both parts landed (C5b is HEAD for every gate below G3), and
reads green.

### 3a857e2aa F028 R6 C6: add the round 6 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r6-mutations.py | 292/0 | G5's tool: 7 mutations (m1 Python, m2-m7 TypeScript) across the three touched production files |

### F028 R6 C7: rewrite handoff for round 6 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 5.
- `git worktree add --detach .remedy-wt/f028-r6-vitest-base d82a407c` (to
  measure the vitest suite's own baseline test count for G4's accounting,
  with the primary's `apps/ui/node_modules` symlinked in temporarily) —
  succeeded; symlink removed, `git worktree remove --force
  .remedy-wt/f028-r6-vitest-base` and `git worktree prune` afterwards —
  both succeeded, `git worktree list | wc -l` read 66 before and after.
- `git worktree add --detach .remedy-wt/f028-r6-mut 3a857e2aa` (at C6,
  G5's own ordered worktree) — succeeded; `git worktree remove --force
  .remedy-wt/f028-r6-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 66 before the add and 66
  after the remove (step 4's own reading, unchanged).
- `git push` after C7 — reported under G6 in this round's reply (run after
  this file is committed).
- No `gh pr create` (the block does not order one this round), no `gh pr
  merge`, no checkout of `main`, no branch deletion, no force-push, no `git
  stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `plan.md`: 30 lines, 1072 bytes, sha256
  `51d9e9f00ee359684f41633f7d4662ef9488461a60573c7176d5419365252ff2`.
- `records.diff`: 64 lines, 13623 bytes, sha256
  `7c26043f0e7215bf8a39e811d67caaf4203fe035e86b09d1365f8d6a7760a60b`.
- Block: 246 lines, 19750 bytes, sha256
  `84c3dcd954c057d3f76073e066d59522a37d36e53b10ce0d1edfcb59643ce060` —
  MATCH against both readings the delegation message stated (step 3).

Each `.agent/authored/f028-r6-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`d88c2eafb`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r6-block.md MATCH sha=84c3dcd954c057d3f76073e066d59522a37d36e53b10ce0d1edfcb59643ce060
.agent/authored/f028-r6-records.diff MATCH sha=7c26043f0e7215bf8a39e811d67caaf4203fe035e86b09d1365f8d6a7760a60b
.agent/authored/f028-r6-plan.md MATCH sha=51d9e9f00ee359684f41633f7d4662ef9488461a60573c7176d5419365252ff2
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`e19046c9c`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md bytes=327502 sha256=5b6ca36fb4bc2e0f57c50f3b32b47dbd5c46a516682cb23ff65bbd01679217dd
.agent/decisions.md   bytes=2269306 sha256=1ef9f83ef76cdd752f6817397249198e701ff1b5c497abea939fcc41bde5cc0b
docs/ui/design_reference/assumption_log.md bytes=17173 sha256=4ed2e280fc62bcb523bac936bb34482497a6759d098ea36a788bcf90d2e40e81
.agent/plan.md        bytes=1072   sha256=51d9e9f00ee359684f41633f7d4662ef9488461a60573c7176d5419365252ff2
```
All four MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text: at `d82a407c`
reads `['R-1078']`; at C2 (`e19046c9c`) reads `[]` — MATCH against the
reviewer's stated readings. `git diff --name-only d88c2eafb e19046c9c`
names exactly: `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/ui/design_reference/assumption_log.md` — the
table's four paths, no more, no fewer.

### G3 — THE CODE
```
$ python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_dashboard_task_origin.py tests/ui_contracts/test_inject_controls_contract.py
All checks passed!
```
(exit 0, run at C6)

The new task-item key, quoted (C6 state, `packages/orchestration/ui_server.py`):
```python
            "is_current": tstat in ("running", "active"),
            "is_future": tstat == "pending",
            "is_reviewer_suggested": False,
            "origin": _task_origin(t),
        })
```

`taskOriginChip`, quoted whole (`apps/ui/src/api/injectView.ts`):
```typescript
export function taskOriginChip(task: { origin?: string } | null | undefined): string | null {
  return task?.origin === INJECTED_TASK_ORIGIN ? ORIGIN_CHIP_TEXT : null;
}
```

Both pill mounts, quoted:
```tsx
// TaskChecklistCard.tsx
              {chip && <span className={styles.originChip} title={ORIGIN_CHIP_TITLE}>{chip}</span>}
```
```tsx
// DetailPopover.tsx
        {originChip && <span className={styles.originChip} title={ORIGIN_CHIP_TITLE}>{originChip}</span>}
```

Both `.originChip` rules, quoted:
```css
/* RightLivePanel.module.css */
.originChip {
  padding: 2px 8px;
  border-radius: var(--remedy-radius-pill);
  background: var(--remedy-bg-2);
  border: 1px solid var(--remedy-line);
  font-size: 11px;
  color: var(--remedy-muted);
  margin-left: 6px;
  flex: none;
}
```
```css
/* DetailPopover.module.css */
.originChip { margin-left: 6px; padding: 2px 8px; border: 1px solid var(--remedy-line); border-radius: var(--remedy-radius-pill); color: var(--remedy-ink-soft); font: 600 11px var(--remedy-font-ui); }
```

`describeInjectResult`, quoted whole (`apps/ui/src/api/injectSend.ts`):
```typescript
/** THE MAPPING: one send's result becomes the one thing to say about it. A
 *  fresh object every call, `vetoSend.ts`'s own rule. */
export function describeInjectResult(result: InjectSubmitResult): DecisionOutcomeMessage {
  if (result.outcome === "accepted") {
    return describeInjectAcceptance(result.body);
  }
  if (result.outcome === "refused" && result.status === 409) {
    return describeInjectConflict(result.body);
  }
  if (result.outcome === "refused" && result.status === 400 && result.body?.field === "text") {
    return describeInjectBadText(result.body);
  }
  return describePauseSendResult(result);
}
```

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_dashboard_task_origin.py tests/ui_contracts/test_inject_controls_contract.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py tests/ui_server/test_dashboard_task_specs.py tests/ui_contracts/test_ux_quality.py tests/ui_contracts/test_responsive.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_contracts/test_design_drift.py tests/ui_contracts/test_ui_lint.py tests/ui_contracts/test_pause_controls_contract.py tests/ui_contracts/test_task_version_contract.py tests/ui_contracts/test_veto_controls_contract.py tests/ui_contracts/test_apply_state_partial.py tests/ui_contracts/test_decision_answer_wiring.py tests/ui_contracts/test_humanize_catalog.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_task_injection.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -14; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1204 passed, 9 skipped in 71.81s (0:01:11)
REAL_EXIT=0
```
The reviewer's own baseline at `d82a407c` (this selection less the two new
Python test files, which did not yet exist) read `1197 passed, 9 skipped`
at exit 0 — matching the reviewer's stated reading exactly. `--collect-only
-q` node counts of the two new files:
```
tests/ui_contracts/test_inject_controls_contract.py: 4
tests/ui_server/test_dashboard_task_origin.py: 3
```
`1197 + 4 + 3 = 1204` exactly — no unexplained difference.

The vitest test count the vitest node's own output prints, read directly
(the primary's `apps/ui/node_modules` symlinked temporarily into a
disposable worktree at `d82a407c`, then removed):
```
                 files          tests
d82a407c         76 (75 passed, 1 skipped)   1464 (1459 passed, 5 skipped)
C6 (3a857e2aa)   78 (77 passed, 1 skipped)   1533 (1528 passed, 5 skipped)
```
Delta: +2 files, +69 tests — exactly `injectView.test.ts` (6 tests) +
`injectSend.test.ts` (63 tests) = 69. No unaccounted difference; the
pytest node `TestVitestFrontendTestFoundation::test_vitest_passes` counts
as ONE pytest node regardless of this internal count, so this reading is
supplementary to (not part of) the `1197+7=1204` arithmetic above.

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
`git worktree add --detach .remedy-wt/f028-r6-mut 3a857e2aa` (C6) then
`python3 -B .agent/authored/f028-r6-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r6-mut`, whole output:
```
==============================================================================
--- pytest control run (unmutated, before) ---
control: exit=0 failed=0
--- vitest control run (unmutated, before) ---
control: exit=0 failed=0
m1 the task item's origin is always the empty string: exit=1 failed=1 failing_node_ids=['tests/ui_server/test_dashboard_task_origin.py::test_an_injected_tasks_item_names_human_injected']
m2 taskOriginChip answers the chip for any non-empty origin: exit=1 failed=1 failing_tests=['taskOriginChip > is null for a task with any other origin 3ms', '.../injectView.test.ts > taskOriginChip > is null for a task with any other origin']
m3 buildInjectDraftRequest accepts a blank text: exit=1 failed=2 failing_tests=['buildInjectDraftRequest > is null for text blank after trimming 5ms', 'sendInjectDraft > never reaches the network when the text is blank 1ms', ...]
m4 buildInjectAnswerRequest accepts an option outside the three: exit=1 failed=2 failing_tests=['buildInjectAnswerRequest > is null for an option outside the three 5ms', 'sendInjectAnswer > never reaches the network when the option is outside the three 1ms', ...]
m5 INJECT_DRAFT_DEADLINE_MS is 20000: exit=1 failed=1 failing_tests=["the three deadlines > the draft waits on the planner's call 6ms", ...]
m6 a 409 draft_expired is worded by the unknown-code fallback: exit=1 failed=1 failing_tests=['describeInjectResult > 409 code draft_expired 6ms', ...]
m7 buildInjectConfirmRequest names job.inject as its command: exit=1 failed=3 failing_tests=['buildInjectConfirmRequest > builds the exact request 6ms', 'buildInjectConfirmRequest > names the command job.inject-confirm 1ms', "sendInjectConfirm > sends exactly once and reports the door's answer 1ms", ...]
restored byte-identical: True (apps/ui/src/api/injectSend.ts)
restored byte-identical: True (apps/ui/src/api/injectView.ts)
restored byte-identical: True (packages/orchestration/ui_server.py)
--- pytest control run (unmutated, after) ---
control: exit=0
--- vitest control run (unmutated, after) ---
control: exit=0
git status --porcelain (primary checkout): ''
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 7 mutations red with at least one failing node/test each; no mutation
stayed green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r6-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 66 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r6-block.md`, at `d88c2eafb`) vs
  `.remedy-wt/f028-r6/block.md`: byte-identical, sha256
  `84c3dcd954c057d3f76073e066d59522a37d36e53b10ce0d1edfcb59643ce060` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r6-plan.md`, at `d88c2eafb`) vs
  `.remedy-wt/f028-r6-payloads/plan.md`: byte-identical, sha256
  `51d9e9f00ee359684f41633f7d4662ef9488461a60573c7176d5419365252ff2` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r6-records.diff`, at
  `d88c2eafb`) vs `.remedy-wt/f028-r6-payloads/records.diff`:
  byte-identical, sha256
  `7c26043f0e7215bf8a39e811d67caaf4203fe035e86b09d1365f8d6a7760a60b` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production code (`ui_server.py`, `types.ts`, `remedyApi.ts`,
`injectView.ts`, `injectSend.ts`, the two components, the two CSS files),
its tests (four new/changed test files) and the mutation tool
(`f028-r6-mutations.py`) are the WORKER's own authored code against the
block's specification S1–S6, not reviewer-authored text, so no fidelity
comparison applies to them.

## Deviations & assumptions

1. **C5 split into C5a and C5b (constraint 2).** The block's bundle lists
   one C5 carrying "`injectSend.ts`, `injectSend.test.ts`". Measured
   before committing: `injectSend.ts` alone totals 425 insertions;
   `injectSend.test.ts` alone totals 448. Combined (873) would exceed the
   500-line cap, so this round split the commit into C5a (the module
   alone, 425 insertions, subject "F028 R6 C5a: add the browser's send
   module for the three injection commands") and C5b (the test file
   alone, 448 insertions, subject "F028 R6 C5b: test the send module's
   requests, refusals and each flow"), per constraint 2's own instruction
   that a commit reaching 500 is split into parts with their own subjects,
   each leaving the selection of G4 green. The test file did not exist at
   C5a, so no node in G4's selection was affected by the split; G4 was run
   once, after both parts landed (C5b is HEAD for every gate below G3),
   and reads green.
2. **The 200-outcome and 409-refusal sentences in `injectSend.ts`.** S3
   orders the shape (four 200 outcomes, sixteen 409 codes each worded as
   one complete plain sentence, an unknown code echoed verbatim, a 400 on
   `text` through the door's own detail, everything else through
   `describePauseSendResult`) but no exact wording; the sentences
   themselves are this round's own composition, following the operator-
   facing, present-tense register `vetoSend.ts`'s and `pauseSend.ts`'s own
   sentences already use, and reading each refusal code's meaning off
   `task_injection.py`'s own docstrings and `job_inject_cmd.py`'s own
   comments before wording it.
3. **`_task_origin`'s placement in `ui_server.py`.** The block names no
   exact line for the new helper; it was placed directly after
   `_task_completed_at` (the last of the existing per-task helpers) and
   before `_event_backed_actor`, grouping it with the other `_task_*`
   helpers the task-item loop calls, rather than inline in the loop body.
4. **Test-file/payload line/byte/sha256 measurements, the `--collect-only`
   node counts, the FROM-text occurrence checks and the vitest baseline
   count** were done with small Python helper scripts written to
   `.remedy-wt/f028-r6-worker/` and run via `python3 -B <script>` rather
   than shell pipelines the sandbox denies (heredocs containing a
   brace-with-quote, command substitution, multi-operation one-liners
   outside `bash -c`) — per the block's own "THIS SANDBOX REFUSES SHAPES"
   section. The vitest baseline count was measured in a disposable
   worktree at `d82a407c` with the primary's `apps/ui/node_modules`
   symlinked in temporarily (removed immediately after use, before the
   worktree itself was removed).

No test went red unexpectedly, no reviewer payload was edited or retyped,
no gate was skipped, and every G5 mutation was caught on the first run —
no fix-up test was required.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | deviated | split into C5a (module, 425 insertions) and C5b (test file, 448 insertions) under constraint 2 — combined would have reached 873 insertions; declared in Deviations §1 |
| C5a | done | see C5's note |
| C5b | done | see C5's note |
| C6 | done | |
| C7 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | 1204 passed, 9 skipped, exit 0; the 7-node delta from the reviewer's 1197 baseline fully accounted for by the two new files' collect-only counts (4+3); the vitest suite's own +69/+2 delta also fully accounted for by the two new `.test.ts` files |
| G5 | done | all 7 mutations caught, both controls clean, all three files restored byte-identical, primary checkout clean |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| S1 | done | `_task_origin` in `ui_server.py`, `origin?: string` in `types.ts`, the mapping in `remedyApi.ts` |
| S2 | done | `injectView.ts`: `INJECTED_TASK_ORIGIN`, `ORIGIN_CHIP_TEXT`, `ORIGIN_CHIP_TITLE`, `taskOriginChip` |
| S3 | done | `injectSend.ts`: the three command ids, the shortfall options, the two deadlines, the three builders, the submit, `describeInjectResult`, `injectAnswerOf`, the three send flows |
| S4 | done | both pill mounts and both `.originChip` CSS rules |
| S5 | done | `injectView.test.ts`, `injectSend.test.ts`, `test_dashboard_task_origin.py`, `test_inject_controls_contract.py` |
| S6 | done | no Add Task row, no sheet, no canvas chip added this round; `+ Propose task` untouched |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 6,
then the Add Task row and its sheet, the canvas chip and the render proof.
Open findings (by `open_finding_ids` at this round's head): 0. Operator
questions open: 0.
