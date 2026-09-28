# Handoff — F035, round 5 (repair R-1082, then the browser's first half of T003: a pure reader
of the `ownership` route, one load in the shell, and a "Who did what" section with chips in the
task detail)

## Session

SESSION 1 of feature F035 · round 5 · rounds so far 5. Context remaining at handback: a
comfortable majority of the budget is left — the round read AGENTS.md, the block, the two
payloads and the handback template once, read `ownership_phrases.py`, `ownership.py`,
`test_ownership_phrases.py` and its golden, `lessons.ts` and `lessons.test.ts`, the lessons and
digest loaders of `remedyApi.ts`, `RemedyShell.tsx`, `DetailPopover.tsx` and its module CSS,
`test_lessons_overlay_contract.py`, `test_raw_colour_ratchet.py`, every `tests/ui_contracts/`
file naming `DetailPopover.tsx` or `RemedyShell.tsx`, §13/§17 of `ux_spec.md`, and G5 of
`f030-r3-block.md`, before writing the reader, its loader, the shell's effect, the section, its
CSS, the new contract test and unit test file, and the mutation tool; ran the full gate
selection once and the mutation tool once.

## Range

Review of `0faa196f9`..`HEAD` (`HEAD` is this handback's own commit, `F035 R5 C7`, on
`feature/f035-ownership-ledger`).

## Commits

### fc0a04167 F035 R5 C1: copy round 5 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r5-block.md | 271/0 | verbatim copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f035-r5-booking.diff | 75/0 | verbatim copy of the booking.diff payload |
| .agent/authored/f035-r5-plan.md | 27/0 | verbatim copy of the plan.md payload |

Measured insertions: 373 (271+75+27). Block expected the block's own line count (271) plus 102 =
373. Match, under the 500-line cap.

### 2c05fc953 F035 R5 C2: book round 4's FAIL, register R-1082, record D5, one prose slip, one assumption row, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 37/0 | DECISION F035 D5 appended by `git apply booking.diff` |
| .agent/live_review.md | 4/0 | round 4's FAIL Gate entry and R-1082's registration appended |
| .agent/plan.md | 6/7 | rewritten to the plan.md payload |
| .agent/prose_slips.md | 1/0 | one prose-slip line appended |
| docs/ui/design_reference/assumption_log.md | 1/0 | one assumption-log row appended |

Measured numstat: 37/0, 4/0, 6/7, 1/0, 1/0 — equal to the block's G2 expectation exactly (the
five files' sha256 also matched the reviewer's simulation-tree reading; see Verification).

### 37c8d902a F035 R5 C3: repair R-1082, the plan-edit sentences read as D4 orders
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | one `Landed: R-1082 — …` line appended, naming the files |
| packages/orchestration/ownership_phrases.py | 9/9 | every `plan_edited`/`task_edited` sentence now ends `; the plan is now at version <n>.`; `plan_edit_acceptance` drops `in the plan` |
| tests/orchestration/fixtures/ownership/golden/sentences.txt | 8/8 | the eight plan-edit golden lines re-worded to match |
| tests/orchestration/test_ownership_phrases.py | 10/10 | the eight plan-edit inline assertions re-worded to match |

Measured insertions: 29 (2+9+8+10), 27 deletions. No expectation is stated for C3 to C6; this is
what was measured, under the 500-line cap.

### 163179d13 F035 R5 C4: the ownership view reader, its loader and unit tests
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/ownership.ts | 200/0 | NEW: `OwnershipActor`/`Consequence`/`Entry`/`View`, `decodeOwnershipView`, `ownershipViewPath`, `OWNERSHIP_CHIP_WORDS`/`ownershipChipWord`, `OWNERSHIP_UNREADABLE_LINE`, `ownershipEntriesForTask`, `OWNERSHIP_REFRESH_EVENTS`/`ownershipRefreshKey` |
| apps/ui/src/api/ownership.test.ts | 129/0 | NEW: a wire-shaped fixture decoded, one refusal per malformed field, the path encoded, entries by id/consequence/none for "", every chip word and the fallback, the refresh key over mixed frames, `loadOwnershipView` with a fake and a throwing fetcher |
| apps/ui/src/api/remedyApi.ts | 24/0 | `OwnershipFetcher`, `loadOwnershipView` after the lessons loader, shaped exactly like `loadLessonsIndex` |

Measured insertions: 353 (200+129+24). No expectation is stated for C3 to C6; under the 500-line
cap.

### a4df13c5a F035 R5 C5: who did what in the task detail, loaded once by the shell
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/detail/DetailPopover.module.css | 6/0 | `.ownershipChip` (shaped as `.originChip`: same radius, same font rule) and `.ownershipSentence` (`white-space: pre-line`); no new raw-colour literal |
| apps/ui/src/components/detail/DetailPopover.tsx | 26/1 | optional prop `ownership`; the "Who did what" section directly after the unreachable section and before the changed-files comment |
| apps/ui/src/components/shell/RemedyShell.tsx | 20/2 | `[ownership, setOwnership]` state and an effect beside the digest's, guarded by `cancelled`, dependent on `dashboard.jobId`, `serverToken`, `ownershipKey` and `focusedTaskId`; `ownership` passed to `DetailPopover` |
| tests/ui_contracts/test_ownership_view_contract.py | 114/0 | NEW: the view/entry/actor/consequence wire keys against the server, the four forbidden substrings, every refresh event a real event name, the chip words against the catalog's own actions, the section's placement and never-the-raw-error rule, the shell effect's guard and dependency array |

Measured insertions: 166 (6+26+20+114), 3 deletions. No expectation is stated for C3 to C6;
under the 500-line cap.

### 9c66860d3 F035 R5 C6: add the round 5 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r5-mutations.py | 231/0 | the G5 red-proof tool: nine mutations (two PYTHON over the phrase catalog and the two `.tsx` files the contract test reads as source, seven VITEST/PYTHON over the TypeScript files), an unmutated control of each runner first and last, restore-and-verify |

Measured insertions: 231. No expectation is stated for C3 to C6; under the 500-line cap.

### This commit F035 R5 C7: rewrite handoff for round 5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback, per `docs/agents/handback_template.md` |

## External actions

- `git apply --check .remedy-wt/f035-r5-payloads/booking.diff` — exit 0.
- `git apply .remedy-wt/f035-r5-payloads/booking.diff` — exit 0.
- `git worktree add --detach .remedy-wt/f035-r5-mut 9c66860d3` at C6 — succeeded; ran the
  mutation tool (all nine caught on the only run); `git worktree remove --force
  .remedy-wt/f035-r5-mut` and `git worktree prune` — both succeeded.
- `git push` — reported in the reply per the block (G6 cannot go in this file, written before
  the push).
- No PR created or merged — the block orders none, and none was created.

## Verification

G1 TRANSPORT — payloads measured against the PAYLOADS table before use:
```
booking.diff: 75 lines, 19422 bytes, sha256 79a30514ef2a68c90af92c499d61e9ff80c2dc3524c4edc155790d5981df5abc — MATCH
plan.md:      27 lines, 870 bytes,   sha256 5093dc17928e81f95dd004bb208108f801309812bd2b585a4afe5f4732c38b14 — MATCH
```
Copies at C1, read back with `git show <C1>:<path>` and compared byte-for-byte against the
source: `.agent/authored/f035-r5-block.md` vs `.remedy-wt/f035-r5/block.md` — IDENTICAL (sha256
`b8584d4bda500646e4955ba57fe3b0803fc33f4a13d2d95342902af398cd10d9` both sides; line count 271,
matching the delegation message's two given readings exactly);
`.agent/authored/f035-r5-plan.md` vs the plan.md payload — IDENTICAL;
`.agent/authored/f035-r5-booking.diff` vs the booking.diff payload — IDENTICAL.

G2 THE BOOKING — at C2 (`2c05fc953`), `git show <C2>:<path>` read and hashed:
```
.agent/decisions.md                            2338101 bytes  d13d01e6782b99c94cd5fb115612aa6d731b6c8ce3e126fd763b87af305684c1 — MATCH
.agent/live_review.md                           314109 bytes  1e8412bee857d57a09240a8486f5f79ce07a176cd855660525a2ee756e0ac1fd — MATCH
.agent/plan.md                                     870 bytes  5093dc17928e81f95dd004bb208108f801309812bd2b585a4afe5f4732c38b14 — MATCH
.agent/prose_slips.md                           375262 bytes  47785db09ed39a4820e8aa20702eee8804f9add8ff97b723aacaf5bf837943c7 — MATCH
docs/ui/design_reference/assumption_log.md       22672 bytes  b2d1a80614b45a9382aefe4eec97077f4aa4196c62988f2f9c69438dac0ffc8a — MATCH
```
`scripts.rotate_live_review.open_finding_ids` over the C2 ledger text: `['R-1082']` — equal to
the reviewer's own reading.

G3 THE CODE — after C3/C5:
```
$ python3 -m ruff check packages/orchestration/ownership_phrases.py tests/orchestration/test_ownership_phrases.py tests/ui_contracts/test_ownership_view_contract.py
All checks passed!
REAL_EXIT=0
```
The golden file's changed lines, quoted from `git show 37c8d902a -- tests/orchestration/fixtures/ownership/golden/sentences.txt`:
```
-You (browser, token #1) edited the plan (task edit T2 --acceptance add) for task T2 (Task Two); the plan is now version 7.
-You changed task T1 (Task One) in the plan; the plan is now version 9.
-You changed the acceptance checks of task T2 (Task Two) in the plan; the plan is now version 10.
-You deleted task T3 (Task Three) from the plan; the plan is now version 11.
-You split task T4 (Task Four) in the plan; the plan is now version 12.
-You merged tasks in the plan; the plan is now version 13.
-You reordered the plan's tasks; the plan is now version 14.
-You edited task T3 (Task Three) while the job ran; the plan is now version 8.
+You (browser, token #1) edited the plan (task edit T2 --acceptance add) for task T2 (Task Two); the plan is now at version 7.
+You changed task T1 (Task One) in the plan; the plan is now at version 9.
+You changed the acceptance checks of task T2 (Task Two); the plan is now at version 10.
+You deleted task T3 (Task Three) from the plan; the plan is now at version 11.
+You split task T4 (Task Four) in the plan; the plan is now at version 12.
+You merged tasks in the plan; the plan is now at version 13.
+You reordered the plan's tasks; the plan is now at version 14.
+You edited task T3 (Task Three) while the job ran; the plan is now at version 8.
```
The shell's effect, quoted from `git show a4df13c5a:apps/ui/src/components/shell/RemedyShell.tsx`:
```ts
  const [ownership, setOwnership] = useState<OwnershipView | null>(null);
  const ownershipKey = ownershipRefreshKey(stream.recent ?? []);
  useEffect(() => {
    let cancelled = false;
    void loadOwnershipView({ jobId: dashboard.jobId, token: serverToken }).then((loaded) => {
      if (!cancelled) setOwnership(loaded);
    });
    return () => { cancelled = true; };
  }, [dashboard.jobId, serverToken, ownershipKey, focusedTaskId]);
```
The popover's section, quoted from `git show a4df13c5a:apps/ui/src/components/detail/DetailPopover.tsx`:
```tsx
      {task && ownership && (ownership.error !== "" || ownershipEntriesForTask(ownership, task.id).length > 0) && (
        <section className={styles.section} data-ui="ownership-section">
          <h3>Who did what</h3>
          {ownership.error !== "" ? (
            <p>{OWNERSHIP_UNREADABLE_LINE}</p>
          ) : (
            <ul>
              {ownershipEntriesForTask(ownership, task.id).map((entry) => (
                <li key={entry.recordRef}>
                  <span className={styles.ownershipChip}>{ownershipChipWord(entry.action)}</span>{" "}
                  <span className={styles.ownershipSentence}>{entry.sentence}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
```

G4 THE TESTS — SERIALLY, at C6 (`9c66860d3`), the block's full selection:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_ownership_route.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_ownership_phrases.py tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py tests/cli/test_job_ownership.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1649 passed, 11 skipped in 62.22s
REAL_EXIT=0
```
Accounting for 1649: the block states the reviewer's own reading at `0faa196f` (this round's
untouched base) was `1640 passed, 11 skipped`. This round's ONLY new pytest node source is the
NEW `tests/ui_contracts/test_ownership_view_contract.py`, which carries exactly 9 test
functions; no other file this round touched added a test function (`test_ownership_phrases.py`
kept its existing 29, only re-wording eight assertions' expected strings), and
`ownership.test.ts`'s new vitest cases all run under the one pre-existing pytest node
`test_vitest_passes` of `TestVitestFrontendTestFoundation` (unchanged in count — vitest cases are
not individually collected by pytest). 1640 + 9 = 1649. Match, real exit 0; the 11 skips are
exactly the ten F252 quarantine lines plus the one `test_agent_tooling.py` D12 quarantine listed
above, unchanged from the reviewer's own reading.

Then:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass` (`live_review_verdict`'s message names round 4's booked FAIL, which is
the correct last-booked verdict at this point in the ledger — round 5's own verdict is the
reviewer's to book next).

G5 THE RED PROOFS — one run, over C6 (`9c66860d3`): `git worktree add --detach
.remedy-wt/f035-r5-mut 9c66860d3`, then `python3 -B .agent/authored/f035-r5-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f035-r5-mut`:
```
control (start) PYTHON: exit=0 failed=0 tests=[]
control (start) VITEST: exit=0 failed=0 tests=[]
m1 the plan-edit sentences drop at: runner=PYTHON exit=1 failed=2 tests=[test_the_golden_ledger_s_sentences_match_byte_for_byte, test_plan_edit_task_reads_changed_t_in_the_plan] caught=True restored=True
m2 the acceptance sentence gains in the plan: runner=PYTHON exit=1 failed=2 tests=[test_the_golden_ledger_s_sentences_match_byte_for_byte, test_plan_edit_acceptance_reads_changed_the_acceptance_checks_of_t] caught=True restored=True
m3 the decoder accepts an entry whose sentence is not a string: runner=VITEST exit=1 failed=1 tests=["decodeOwnershipView refuses the whole view for a sentence that is not a string"] caught=True restored=True
m4 ownershipEntriesForTask ignores consequence.taskIds: runner=VITEST exit=1 failed=1 tests=["the section's rules answers the entries for a task by its own id and by a consequence, in order, none for \"\""] caught=True restored=True
m5 ownershipRefreshKey counts every frame's seq: runner=VITEST exit=1 failed=1 tests=["the section's rules reads the refresh key over mixed frames"] caught=True restored=True
m6 the path leaves the job id unencoded: runner=VITEST exit=1 failed=1 tests=["the section's rules builds the route with the job id and token encoded"] caught=True restored=True
m7 loadOwnershipView lets a throwing fetcher reject: runner=VITEST exit=1 failed=1 tests=["loadOwnershipView answers null, never throws, when the read fails"] caught=True restored=True
m8 the section renders ownership.error instead of the line: runner=PYTHON exit=1 failed=1 tests=[test_the_popover_places_the_section_after_unreachable_and_never_shows_the_raw_error] caught=True restored=True
m9 the effect's dependencies drop the refresh key: runner=PYTHON exit=1 failed=1 tests=[test_the_shell_s_effect_carries_the_guard_and_the_refresh_key] caught=True restored=True
control (end) PYTHON: exit=0 failed=0 tests=[]
control (end) VITEST: exit=0 failed=0 tests=[]
restored byte-identical: True (all nine files)
PRIMARY checkout git status --porcelain: (empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
`git worktree remove --force .remedy-wt/f035-r5-mut` and `git worktree prune` — both succeeded;
`git worktree list | wc -l` read 61 (equal to step 4's reading, unchanged) and `git branch
--list 'remedy/*' | wc -l` read 197 (unchanged).

## Authored-text proofs

`.agent/authored/f035-r5-block.md`, `.agent/authored/f035-r5-plan.md` and
`.agent/authored/f035-r5-booking.diff`, each compared byte-for-byte at C1 against its payload
source — all IDENTICAL (see G1 above). `booking.diff`'s own effect on `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md` and
`docs/ui/design_reference/assumption_log.md`, read at C2 by size and sha256 — all equal to the
reviewer's own reading (see G2 above).

## Deviations & assumptions

None. The round followed the block's ordered commit sequence C1 to C7 exactly, split nothing (no
commit approached the 500-line cap), corrected no test of its own, and found every G5 mutation
red on the tool's only run — nothing needed a second run or a strengthened test.

## Next

Per AGENTS.md Phase 1 rule 1 (read `.agent/STOP` from disk) and the block's ordering: the review
of round 5, including R-1082's repair, then the evidence panel's ownership tab and the
end-to-end proof. Open findings: 1 (R-1082, landed and awaiting review). Operator questions: 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| Step 1 (`.agent/STOP` check) | done | |
| Step 2 (primary checkout, branch, HEAD) | done | |
| Step 3 (block byte verification) | done | |
| Step 4 (worktree count) | done | |
| Payload verification (2 payloads) | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 (this handback) | done | |
| R-1082 | done | repaired in C3, `Landed:` line appended in the same commit |
| G1 Transport | done | |
| G2 The booking | done | |
| G3 The code | done | |
| G4 The tests | done | |
| G5 The red proofs | done | all nine mutations caught on the only run |
| G6 Tree and push | done | reported in the reply, not this file (block: "cannot go in C7") |
