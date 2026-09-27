# Handoff — F029, round 6

## Session

SESSION 1 of feature F029 · round 6 · rounds so far 6. Context remaining at
handback: comfortable — reading `injectSend.ts`/its test, `vetoSend.ts`,
`pauseSend.ts`, `decisionAnswer.ts`, `decisionSend.ts`, `RunDetailPopover.tsx`/
its CSS, the two contract test files and the relevant slice of `run_report.py`/
its test, plus a research pass on `subtree_rerun.py`'s task-item fields, then
drafting S1–S5 plus their new/extended tests and the mutation tool took the
bulk of it; one tool bug was found and fixed within the round (below); every
gate ran clean afterward, with ample context left had a further repair round
been needed.

## Range

Review of `4295d0dc4`..`HEAD` (`HEAD` is this handback's own commit, `F029 R6
C7`, on `feature/f029-subtree-rerun`).

## Commits

### 9519fb2ec F029 R6 C1: copy round 6 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r6-block.md | 240/0 | copy of this round's block |
| .agent/authored/f029-r6-booking.diff | 68/0 | copy of the booking diff payload |
| .agent/authored/f029-r6-plan.md | 33/0 | copy of the plan payload |

Measured insertions: 341 (block's own line count 240 + 101), matching the
block's expectation exactly, under the 500-line cap.

### 7e87121af F029 R6 C2: book round 5, record D6 and its assumption-log row
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 41/0 | DECISION F029 D6 appended |
| .agent/live_review.md | 2/0 | round 5's Gate entry appended |
| .agent/plan.md | 9/11 | rewrite from the plan payload |
| docs/ui/design_reference/assumption_log.md | 1/0 | one row naming DECISION F029 D6 |

Matches the block's expected numstat (41/0, 2/0, 9/11, 1/0) exactly. Applied
via `git apply --check` (exit 0) then the real apply (exit 0) of
`booking.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### d83a47278 F029 R6 C3a: send a subtree rerun from the browser and read its answer
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/rerunSend.ts | 257/0 | S1: `JOB_RERUN_SUBTREE_COMMAND_ID`, `RERUN_DEADLINE_MS`, `buildRerunSubtreeRequest`, `submitRerunSubtreeRequest`, `rerunAnswerOf`, `describeRerunResult`, `sendRerunSubtree` |
| apps/ui/src/api/rerunSend.test.ts | 197/0 | S1's tests: every arg combination, a 200, a 409 whose sentence drops the prefix, an unreachable server |

454 total insertions. **Split from the block's single C3**, declared below:
S1 (257) + S2 (92) plus their tests (197 + 95) would have reached 640
insertions in one commit, over the 500-line cap. Split into C3a (this one,
the send half) and C3b (the words half), each measured before committing,
each leaving its own vitest file green in isolation (rerunSend.test.ts: 23
passed; rerunView.test.ts: 9 passed — run individually and together).

### 38d9fc43d F029 R6 C3b: read a subtree rerun's answer as sentences
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/rerunView.ts | 92/0 | S2: `rerunAnswerView`, the estimate and prepared sentences |
| apps/ui/src/api/rerunView.test.ts | 95/0 | S2's tests: both estimate sentences (n=1 and n=3), the prepared sentence and command, null for any other outcome, a null body, a body with every field missing |

187 total insertions, under the 500-line cap; the words half of C3's split
(see C3a above).

### aa7c3b50a F029 R6 C4: make the run detail's Rerun button send the rerun behind its cost
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/RunDetailPopover.tsx | 82/4 | S3: the model field, the real Rerun button gated on `token`, the `needs_confirmation`/`prepared`/message outcome states, "Rerun anyway"/"Cancel"; `RERUN_NOT_YET` and its unconditional reason line deleted |
| apps/ui/src/components/graph/RunDetailPopover.module.css | 26/0 | S3: `.modelField`, `.rerunOutcome`, reusing existing `--remedy-*` tokens and the existing `.action` rules |
| tests/ui_contracts/test_attempt_fan_contract.py | 13/0 | S5: `RunDetailPopover.tsx` holds no `fetch(`; the assumption log names DECISION F029 D6 in exactly one row |
| tests/ui_contracts/test_run_detail_wiring.py | 9/4 | S5: the ONLY pre-existing test this round edits, renamed and re-asserted per the block |

130 total insertions, under the 500-line cap; no split needed.

### 3140bcc07 F029 R6 C5: the final report names a task's attempt and its override
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_report.py | 51/0 | S4: `TaskOutcome.attempt`/`.model_override`, `_attempt_clause`, `_task_attempt`/`_task_model_override` (read defensively as `_task_origin` reads `origin`), wired into `_task_lines` and `collect_report_sources` |
| tests/orchestration/test_run_report.py | 35/0 | S4's tests: the clause for attempt 2 without and with an override, none for attempt 1, a job with no rerun byte-identical |

86 total insertions, under the 500-line cap; no split needed.

### 73cd94d6e F029 R6 C6: add the round 6 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r6-mutations.py | 309/0 | the G5 mutation (red-proof) tool, covering m1–m8 across `rerunSend.ts`, `rerunView.ts`, `run_report.py` and `RunDetailPopover.tsx`, two routes (vitest for m1–m5, pytest for m6–m8) |

### 1b1b12798 F029 R6 correction: fix invalid JS produced by m1/m2 in the mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r6-mutations.py | 2/2 | m1/m2's TO text used a bare object-literal property instead of a spread, which is invalid JS; esbuild's transform failed outright instead of the mutation surfacing as a caught test failure — see Deviations |

### (this commit) F029 R6 C7: rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file |

## External actions

`git worktree add --detach .remedy-wt/f029-r6-mut 73cd94d6e` (first attempt,
at C6 literally) — m1 and m2 both errored out at the esbuild transform stage
rather than failing as caught tests (tool bug, see Deviations); removed with
`git worktree remove --force .remedy-wt/f029-r6-mut` then `git worktree
prune` before fixing the tool. After the correction commit:
`git worktree add --detach .remedy-wt/f029-r6-mut 1b1b12798`, ran the tool
(all 8 mutations caught, see G5 below), then `git worktree remove --force
.remedy-wt/f029-r6-mut` and `git worktree prune`. `git worktree list | wc -l`
read 61 before the first add and 61 after the final remove, matching the
step-4 reading throughout. `git push origin feature/f029-subtree-rerun` —
its real outcome is reported to the delegator, since C7 cannot contain it.
No PR opened, no merge, no branch deleted, no force-push, no stash.

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty;
  `git branch --show-current` → `feature/f029-subtree-rerun`; `git log
  --oneline -1` → `4295d0dc4`.
- Block bytes (R-0954): measured 240 lines, sha256
  `1b616ce3bd4b8826b277865a20245fad4109a86600e4558432ebfd03909b02aa` — both
  match the delegation message's readings exactly.
- `git worktree list | wc -l` → 61.

**PAYLOADS** — both matched the table exactly:
`booking.diff` 68 lines / 14189 bytes /
`442bd4114c85bf67e26e5eae73b07b93e1fd6cca6580a3682c9e03550b39d517`;
`plan.md` 33 lines / 1171 bytes /
`c217f215fe46dc18f1bd3526f3c48b37aca41be563bbba139c701363bc3e5652`.

**G1 TRANSPORT** — each `.agent/authored/f029-r6-*` copy read via `git show
9519fb2ec:<path>` equals its source byte for byte: block copy == source
(True, sha256 `1b616ce3...09b02aa`); booking.diff copy == source (True,
sha256 `442bd411...c9e03550b39d517`); plan.md copy == source (True, sha256
`c217f215...c701363bc3e5652`).

**G2 THE RECORDS** — sha256 of each file read via `git show 7e87121af:<path>`
equals the reviewer's reading exactly:
`.agent/decisions.md` 2302631 bytes,
`6437bdd35357ecbb20b50dfa3abee6843dae8ad113e949271f097876a26ea8d3` — match.
`.agent/live_review.md` 326313 bytes,
`efc0988d0611e6fade0a03ad8e0d62ccfcc3d2368169df342c4884e47b242209` — match.
`.agent/plan.md` 1171 bytes,
`c217f215fe46dc18f1bd3526f3c48b37aca41be563bbba139c701363bc3e5652` — match.
`docs/ui/design_reference/assumption_log.md` 20869 bytes,
`6f2a0c0795b29b31ab692c9e21ded4689eb83669b435b58a2fae60a0b110c031` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s
text: at `4295d0dc4` → `[]`; at `7e87121af` → `[]` — both match the
reviewer's stated readings. `git diff --name-only 9519fb2ec 7e87121af` →
exactly the four paths of the table, nothing else.

**G3 THE CODE** —
```
python3 -m ruff check packages/orchestration/run_report.py tests/orchestration/test_run_report.py tests/ui_contracts/test_run_detail_wiring.py tests/ui_contracts/test_attempt_fan_contract.py
```
→ `All checks passed!`, exit 0 (run at C6, `73cd94d6e`, and unchanged by the
correction commit, which touches only the mutation tool). Quoted from the
diff (all four match what is committed at HEAD):

`buildRerunSubtreeRequest` (`rerunSend.ts`):
```ts
export function buildRerunSubtreeRequest(
  target: DecisionSendTarget,
  taskId: string,
  options: RerunSubtreeOptions,
  clientNonce: string,
): DecisionSendRequest | null {
  if (taskId === "" || !isUsableCommandNonce(clientNonce)) {
    return null;
  }
  const trimmedModel = (options.model ?? "").trim();
  return {
    path: jobCommandsPath(target.jobId),
    method: "POST",
    headers: {
      Authorization: `Bearer ${target.serverToken}`,
      "X-Remedy-CSRF": target.serverToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      command: JOB_RERUN_SUBTREE_COMMAND_ID,
      client_nonce: clientNonce,
      args: {
        task_id: taskId,
        ...(trimmedModel !== "" ? { model: trimmedModel } : {}),
        ...(options.confirmCost === true ? { confirm_cost: true } : {}),
      },
    }),
  };
}
```

`rerunAnswerView`'s `prepared` branch (`rerunView.ts`):
```ts
  if (answer.outcome === "prepared") {
    const subtree = subtreeOf(answer);
    const root = typeof answer.root_task_id === "string" ? answer.root_task_id : "";
    const n = Math.max(subtree.length - 1, 0);
    const runCommand = typeof answer.run_command === "string" ? answer.run_command : "";
    return {
      kind: "prepared",
      sentence: `Task ${root} and ${n} task${pluralSuffix(n)} after it were reset to run again.`,
      runCommand,
    };
  }
```

The Rerun control's JSX (`RunDetailPopover.tsx`):
```tsx
      <label className={styles.modelField}>
        <span>Model for the rerun (optional)</span>
        <input
          type="text"
          maxLength={128}
          value={rerunModel}
          onChange={(event) => setRerunModel(event.target.value)}
        />
      </label>
      <div className={styles.actions}>
        <button type="button" className={styles.action} onClick={() => onOpenEvidence("diff")}>Open diff</button>
        <button
          type="button"
          className={styles.action}
          disabled={detail.promptItemId === null}
          title={detail.promptItemId === null ? "No prompt was recorded for this run." : undefined}
          onClick={() => { if (detail.promptItemId !== null) onOpenEvidence("prompt"); }}
        >
          Why
        </button>
        <button
          type="button"
          className={styles.action}
          disabled={rerunDisabled || rerunSending}
          title={rerunDisabled ? RERUN_TOKEN_REASON : undefined}
          aria-describedby={rerunDisabled ? reasonId : undefined}
          onClick={() => void sendRerun(false)}
        >
          Rerun
        </button>
      </div>
      {rerunDisabled && <p id={reasonId} className={styles.reason}>{RERUN_TOKEN_REASON}</p>}
      {rerunSentence !== null && <p className={styles.rerunOutcome} aria-live="polite">{rerunSentence}</p>}
      {rerunOutcome?.kind === "needs_confirmation" && (
        <div className={styles.actions}>
          <button type="button" className={styles.action} disabled={rerunSending} onClick={() => void sendRerun(true)}>
            Rerun anyway
          </button>
          <button type="button" className={styles.action} disabled={rerunSending} onClick={() => setRerunOutcome(null)}>
            Cancel
          </button>
        </div>
      )}
```

`_attempt_clause` (`run_report.py`):
```python
def _attempt_clause(task: TaskOutcome) -> str:
    """DECISION F029 D6: the rerun clause, or "" (P6) when *task* is on its
    first attempt.
    ...
    """
    if task.attempt < 2:
        return ""
    clause = f" — attempt {task.attempt}"
    if task.model_override:
        clause += f", run on {task.model_override}"
    return clause
```

**G4 THE TESTS** — the exact selection, serially, real exit code:
```
python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/orchestration/test_run_report.py tests/ui_server/test_rerun_subtree_door.py tests/ui_server/test_dashboard_task_attempts.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
```
Run at C6 (`73cd94d6e`; unaffected by the later tool-only correction):
`1696 passed, 11 skipped`, real exit code 0. All eleven `SKIPPED` lines cite
an F252 quarantine (four in `tests/ui_contracts/`, six in
`test_named_bugs.py`, one in `test_agent_tooling.py`) — the same eleven the
reviewer's own base reading at `4295d0dc` already carried. Accounting for the
difference from 1690: this round's own `tests/orchestration/test_run_report.py`
adds 4 new pytest nodes (`TestTheReportNamesATasksAttemptAndItsOverride`'s
four tests) and `tests/ui_contracts/test_attempt_fan_contract.py` adds 2 new
pytest nodes (`test_run_detail_popover_touches_no_network_of_its_own`,
`test_the_assumption_log_names_decision_f029_d6_in_exactly_one_row`);
`test_run_detail_wiring.py`'s one edited test is a rename, not a new node;
every `.ts`/`.tsx` file this round touches is exercised INSIDE the single
`TestVitestFrontendTestFoundation` pytest node, so it adds no further pytest
node of its own. 1690 + 4 + 2 = 1696, exactly the passed count above; no
unexplained difference. Then `python3 -m apps.cli.main integrity check
--json` → all 6 checks `pass` (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`), `fail_count: 0`, `ok: true`.

**G5 THE RED PROOFS** — first attempt, `git worktree add --detach
.remedy-wt/f029-r6-mut 73cd94d6e` (literally C6): m1 and m2 both errored at
esbuild's transform stage (`Expected identifier but found "{"`) rather than
surfacing as a caught test — the tool's own TO text for those two mutations
was invalid JS (a bare object-literal property where a spread was needed).
Read `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False`, exit 1. Removed the
worktree, fixed the tool (commit `1b1b12798`, "F029 R6 correction: ..."),
re-added the worktree at the corrected HEAD:
`git worktree add --detach .remedy-wt/f029-r6-mut 1b1b12798`, then
`python3 -B .agent/authored/f029-r6-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r6-mut`:
```
control (vitest, unmutated, first): exit=0 failed=0
control (pytest, unmutated, first): exit=0 failed=0
m1 the request always sends confirm_cost: true [vitest]: exit=1 failed=4 — buildRerunSubtreeRequest's four args tests
m2 the request never sends model [vitest]: exit=1 failed=2 — buildRerunSubtreeRequest's blank-model and every-combination tests
m3 a refusal's sentence keeps the code's prefix [vitest]: exit=1 failed=1 — describeRerunResult's prefix test
m4 an unavailable estimate reads as the priced sentence [vitest]: exit=1 failed=3 — rerunAnswerView's two cannot-be-estimated tests and its missing-fields test
m5 the prepared view's runCommand is "" [vitest]: exit=1 failed=1 — rerunAnswerView's prepared-command test
m6 _attempt_clause answers a clause for attempt 1 [pytest]: exit=1 failed=15 — the goldens, the apply-state tests, the origin tests and this round's own attempt-1/no-rerun tests
m7 _attempt_clause leaves out the override [pytest]: exit=1 failed=1 — this round's own attempt-2-with-override test
m8 RunDetailPopover.tsx keeps a role="dialog" on its panel [pytest]: exit=1 failed=1 — test_rerun_sends_the_subtree_rerun_and_the_detail_is_not_a_dialog
restored byte-identical: True (rerunSend.ts, rerunView.ts, RunDetailPopover.tsx, run_report.py)
control (vitest, unmutated, last): exit=0
control (pytest, unmutated, last): exit=0
git status --porcelain (primary checkout): '' (empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All eight mutations were red on this (corrected) run; no repair round was
needed for the production code, only the tool bug fixed before this gate
passed. Then `git worktree remove --force .remedy-wt/f029-r6-mut`, `git
worktree prune`; `git worktree list | wc -l` → 61, matching the step-4
reading.

**Constraint 3** — `git diff --name-only 4295d0dc`, run once more after
writing this file, lists exactly the block's tracked path set plus
`.agent/handoff.md` itself: `.agent/authored/f029-r6-block.md`,
`.agent/authored/f029-r6-booking.diff`, `.agent/authored/f029-r6-mutations.py`,
`.agent/authored/f029-r6-plan.md`, `.agent/decisions.md`, `.agent/handoff.md`,
`.agent/live_review.md`, `.agent/plan.md`, `apps/ui/src/api/rerunSend.test.ts`,
`apps/ui/src/api/rerunSend.ts`, `apps/ui/src/api/rerunView.test.ts`,
`apps/ui/src/api/rerunView.ts`,
`apps/ui/src/components/graph/RunDetailPopover.module.css`,
`apps/ui/src/components/graph/RunDetailPopover.tsx`,
`docs/ui/design_reference/assumption_log.md`,
`packages/orchestration/run_report.py`,
`tests/orchestration/test_run_report.py`,
`tests/ui_contracts/test_attempt_fan_contract.py`,
`tests/ui_contracts/test_run_detail_wiring.py` — 19 paths in total; no path
outside the set changed.

## Authored-text proofs

`.agent/authored/f029-r6-block.md`, `f029-r6-booking.diff` and
`f029-r6-plan.md` (C1, `9519fb2ec`): each read back via `git show` equals its
source (`.remedy-wt/f029-r6/block.md`, `.remedy-wt/f029-r6-payloads/booking.diff`,
`.remedy-wt/f029-r6-payloads/plan.md`) byte for byte — see G1 above.
`.agent/authored/f029-r6-mutations.py` (C6, `73cd94d6e`, corrected at
`1b1b12798`) is this session's OWN tool, not reviewer-authored text, so it
carries no fidelity comparison; its behavior is proved instead by G5's live
run above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | deviated | split into C3a (send) + C3b (words); together would have been 640 insertions, over the 500-line cap |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |
| correction | done | fixed this round's own mutation-tool bug (invalid JS in m1/m2) before C7; declared below |
| G1 transport | done | PASS — all copies byte-identical |
| G2 the records | done | PASS — sha256 and open_finding_ids both match |
| G3 the code | done | PASS — ruff exit 0, four functions/mount quoted from disk |
| G4 the tests | done | PASS — 1696 passed, 11 skipped, exit 0; +6 nodes fully accounted |
| G5 the red proofs | done | PASS (after the correction) — all 8 mutations caught, both control kinds green, restored byte-identical |
| S1 the send | done | `rerunSend.ts`: command id, deadline, builder, submit, `rerunAnswerOf`, `describeRerunResult`, `sendRerunSubtree` |
| S2 the words | done | `rerunView.ts`: `rerunAnswerView` for `needs_confirmation` and `prepared` |
| S3 the control | done | `RunDetailPopover.tsx`: model field, real Rerun button, outcome states, "Rerun anyway"/"Cancel" |
| S4 the report | done | `run_report.py`: `TaskOutcome.attempt`/`.model_override`, `_attempt_clause`, wired into `_task_lines`/`collect_report_sources` |
| S5 the pins | done | `test_run_detail_wiring.py`'s rename, `test_attempt_fan_contract.py`'s two additions |

## Deviations & assumptions

1. **C3 split into C3a/C3b** (constraint 2). Measured before committing:
   S1+S2 with their tests together would be 640 insertions, over the
   500-line cap. Split by module — C3a (`rerunSend.ts` + its test, 454
   insertions) and C3b (`rerunView.ts` + its test, 187 insertions) — each
   measured under the cap, each run through vitest on its own (23 and 9
   tests respectively, both green) before committing.

2. **A tool bug found and fixed within the round** (constraint 4's
   correction allowance, read for this round's own tooling rather than a
   test it wrote). `f029-r6-mutations.py`'s m1 and m2 originally replaced a
   spread element with a bare object-literal property
   (`{ confirm_cost: true },` / `{},`), which is invalid inside another
   object literal — esbuild's transform failed outright (`Expected
   identifier but found "{"`) instead of the mutation surfacing as a normal
   caught-test failure, and the tool's own "caught" check (`code != 0 and
   failed_count != 0`) read that as `failed_count == 0` and reported
   `GREEN, NOT CAUGHT`. Fixed by spreading the replacement object instead
   (`...{ confirm_cost: true },` / `...{},`), which keeps each mutation's
   intended effect while staying syntactically valid. Corrected in its own
   commit (`1b1b12798`) before re-running G5; no production file was
   touched by this fix, only the tool.

3. **Two builder/flow signatures read past the block's own compressed
   listing.** S1 writes `buildRerunSubtreeRequest(target, taskId, options,
   clientNonce)` and `sendRerunSubtree(target, taskId, options, deps = {})`
   — the block's own prose lists `buildRerunSubtreeRequest(target, taskId,
   { model, confirmCost })` and `sendRerunSubtree(deps, taskId, { model,
   confirmCost })`, naming neither a nonce parameter for the builder nor a
   `target` parameter for the flow. Every existing send in this cockpit
   (`sendVetoTask`, `sendPauseCommand`, `sendInjectDraft`) takes `target`
   first and an optional `deps` last, and the door requires `client_nonce`
   on every command (`_read_command_payload`, unconditionally) — an
   omission a builder that "composes... reusing composed helpers" from
   `injectSend.ts` could not actually satisfy without one. Read this as a
   prose compression rather than a literal signature and matched the
   codebase's own established shape; flagging it here rather than letting
   a reader assume the two argument orders in the block's prose are
   load-bearing.

No commit was reordered or dropped from the block's ordered sequence beyond
the declared C3 split; no existing test outside this round's own edits was
touched, and the ONE pre-existing test S5 orders edited
(`test_rerun_is_disabled_with_its_reason_visible_and_the_detail_is_not_a_dialog`,
renamed and re-asserted) is exactly the one the block names; no gate went red
in its FINAL (post-correction) state.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 6
with the reviewer's headless render of the Rerun control, then T003's
end-to-end proof — run, rerun a middle task with an override, the subtree
runs again, both attempts in the evidence and the report — then the closure
sequence.

Open findings: 0. Operator questions: 0.
