# Handoff — F030, round 1 (claim + T001)

## Session

SESSION 1 of feature F030 · round 1 · rounds so far 1. Context remaining at
handback: ample — the round read every named source file once, wrote the
production change and its tests in one pass with no repair round, ran every
gate green on the first try, and still had a comfortable context budget left
when this handoff was written.

## Range

Review of `15f5d3841`..`HEAD` (`HEAD` is this handback's own commit, `F030
R1 C5`, on `feature/f030-steering-messages`).

## Commits

### f2f64a652 F030 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r1-block.md | +304/-0 | verbatim copy of this round's block |
| .agent/authored/f030-r1-context.md | +36/-0 | verbatim copy of the reviewer's context.md payload |
| .agent/authored/f030-r1-plan.md | +30/-0 | verbatim copy of the reviewer's plan.md payload |

### 113f82b00 F030 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r1-claim.diff | +141/-0 | verbatim copy of the reviewer's claim diff |

### 0adbd6d5e F030 R1 C2: claim F030, re-head the live review record, book F029 R11, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +14/-15 | rewritten to the reviewer's context.md payload (claim.diff) |
| .agent/decisions.md | +58/-0 | DECISION F030 D1 appended (claim.diff) |
| .agent/live_review.md | +22/-22 | re-headed above `## Findings`; F029 round 11 Gate entry appended (claim.diff) |
| .agent/plan.md | +16/-13 | rewritten to the reviewer's plan.md payload (claim.diff) |
| docs/roadmap/STATUS.md | +1/-1 | F030's line `[ ]` → `[~]` (claim.diff) |

### 5f41c17c3 F030 R1 C3: address a steering note to one task and carry it in that task's rounds
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +42/-0 | `_task_steering_not_consumed_map` (S5), wired into `export_job_report` and `format_job_report_text` |
| packages/orchestration/pingpong_loop.py | +29/-0 | `operator_notes_text` kwarg + `builder_operator_notes` registration on `compose_builder_prompt` (S4); `_operator_notes_text_for_round`; SAFE POINT 1 wiring |
| packages/orchestration/steering.py | +114/-18 | `task_id` on `record_steering_message`, `note_task_id` (S1); the drain's skip-another-task / no-mission-amend branch (S2); `consumed_task_notes`, `unconsumed_task_notes`, `render_operator_notes_segment`, `OPERATOR_NOTES_HEADING` (S3) |

### 5c5abca11 F030 R1 C4a: test task-addressed steering notes
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_steering_notes.py | +307/-0 | new file, 15 tests covering S1–S5 (see Deviations: split from the block's single C4) |

### e1ca56e1a F030 R1 C4b: add the mutation tool for task-addressed steering notes
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f030-r1-mutations.py | +193/-0 | the G5 mutation tool: 11 labelled mutations, each red-proved (see Deviations) |

### (this commit) F030 R1 C5: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback (R-0149 pattern: a handback cannot table the commit that writes it) |

## External actions

`git worktree add --detach .remedy-wt/f030-r1-mut e1ca56e1a` (G5) — success,
detached HEAD at `e1ca56e1a`. `git worktree remove --force
.remedy-wt/f030-r1-mut` — success. `git worktree prune` — success;
`git worktree list | wc -l` read 61 both at step 4 (BEFORE ANYTHING ELSE)
and after this cleanup, so the round's own worktree left no trace. No push
and no `gh` command yet at the point this handback is written: the block's
single `git push` follows C5, after this handback is committed, so this
file cannot carry its real outcome (C5 cannot contain it) — it is reported
to the delegator in the final reply, together with `gh pr list --state open`
(constraint 5: no PR is created this round). No merge, no branch checked
out or deleted, no force-push, no stash.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, real exit 2 (absent, as required).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty. `git branch --show-current` → `main`. `git log --oneline -1` → `15f5d3841 Merge pull request #288 …`.
- `git checkout -b feature/f030-steering-messages` → `Switched to a new branch 'feature/f030-steering-messages'`.
- Block bytes: measured 304 lines (newline count), 24050 bytes, sha256
  `424bdd0acdd375357d9c734171b977cb98834d10e6d818e84177c3bf0b775557` —
  both readings equal the delegation message's, real exit 0.
- `git worktree list | wc -l` → 61 (step 4 reading).

PAYLOADS (measured against the PAYLOADS table, all MATCH):
- claim.diff: 141 lines, 18213 bytes, sha256 `e3cdb7757158dbc994511a1dbdd9e531323923754f855fc7df4f8993bea20c21`.
- context.md: 36 lines, 1499 bytes, sha256 `d9c2c1f100b4c1b38491db60a61ead352a7b0bb207dd1b183fb1f764f8015225`.
- plan.md: 30 lines, 1059 bytes, sha256 `48a396c33275ac0b41c96d8547a928e4e6d8f137e8111e99a6999f6daab6f41e`.

G1 TRANSPORT — every `.agent/authored/f030-r1-*` copy read back with
`git show <commit>:<path>` and compared byte for byte with its source:
`f030-r1-block.md` (C1a) == `.remedy-wt/f030-r1/block.md`: True (24050
bytes both). `f030-r1-plan.md` (C1a) == payload `plan.md`: True (1059
bytes both). `f030-r1-context.md` (C1a) == payload `context.md`: True
(1499 bytes both). `f030-r1-claim.diff` (C1b) == payload `claim.diff`:
True (18213 bytes both).

G2 THE CLAIM — sha256 of each file at C2 (`git show 0adbd6d5e:<path>`)
against the reviewer's simulation-tree reading, all MATCH:
`docs/roadmap/STATUS.md` 55545 bytes; `.agent/live_review.md` 308465
bytes; `.agent/decisions.md` 2310781 bytes; `.agent/plan.md` 1059 bytes;
`.agent/context.md` 1499 bytes — every sha256 equal. `open_finding_ids`
(scripts/rotate_live_review.py) over `.agent/live_review.md`'s text: `[]`
at `15f5d3841` and `[]` at C2 (both empty, as the reviewer read). At C2 the
ledger has exactly one line reading `## Findings` and exactly one reading
`## Steps`; its last line begins `Gate: F029 R11 — `. F030's STATUS line at
C2 reads in full `- [~] F030 — Steering messages`. `git diff --name-only
113f82b00 0adbd6d5e` names exactly: `.agent/context.md`,
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md` — the table's five paths, no more, no fewer.

G3 THE CODE — `python3 -m ruff check packages/orchestration/steering.py
packages/orchestration/pingpong_loop.py packages/orchestration/pingpong_job.py
tests/orchestration/test_steering_notes.py` → `All checks passed!`, real
exit 0. Quoted from `git show 5f41c17c3` (verified in this file's own
Commits section above): the whole of the new `consume_pending_steering`
loop body (the `addressed_to` skip, the `if addressed_to: amendment=None;
mission_id=""` / `else:` mission-amend split, the marker build, and
`return job_wide_records`); the `builder_operator_notes` registration with
`builder_steering` before it and `builder_directive` after; SAFE POINT 1's
two calls, `steering_text = _steering_text_for_round(job_id, task_id,
round_num)` immediately followed by `operator_notes_text =
_operator_notes_text_for_round(job_id, task_id)`.

G4 THE TESTS — serially, primary checkout, at C4 (tip `e1ca56e1a`):
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs <42 paths incl. tests/orchestration/test_steering_notes.py> 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
→ `SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) …` (the
same F252 quarantine the reviewer named), then `1747 passed, 1 skipped in
232.53s (0:03:52)`, `REAL_EXIT=0`. The reviewer's two disjoint pre-round
runs read `1695 passed, 1 skipped` and `37 passed` (1732 total, real exit 0
both); `tests/orchestration/test_steering_notes.py --collect-only -q` reads
15 nodes; `1732 + 15 = 1747`, which is exactly this run's passed+skipped
count — zero unexplained difference. Then `python3 -m apps.cli.main
integrity check --json` → `"check_count": 6`, all six `"status": "pass"`,
`"fail_count": 0`, `"ok": true`, `"passed": true` — real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f030-r1-mut
e1ca56e1a` → success. `python3 -B .agent/authored/f030-r1-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f030-r1-mut` → whole output:
```
control (start): exit=0 failed=0 nodes=[]
m1 drain consumes a note addressed to another task: exit=1 failed=1 nodes=['tests/orchestration/test_steering_notes.py::TestTheDrain::test_a_note_to_another_task_waits_and_is_consumed_at_its_own_round'] caught=True restored=True
m2 drain returns the notes with the job-wide records: exit=1 failed=4 nodes=['tests/orchestration/test_steering_notes.py::TestTheDrain::test_a_note_to_another_task_waits_and_is_consumed_at_its_own_round', 'tests/orchestration/test_steering_notes.py::TestTheDrain::test_the_return_value_holds_a_job_wide_message_and_never_a_note', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_round_one_is_untouched_and_round_two_differs_by_exactly_the_segment', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_a_note_addressed_to_another_task_never_appears_in_any_prompt'] caught=True restored=True
m3 a note amends the mission's contract as a job-wide message does: exit=1 failed=1 nodes=['tests/orchestration/test_steering_notes.py::TestTheMission::test_a_note_leaves_the_mission_contract_unamended'] caught=True restored=True
m4 the notes are numbered from 0: exit=1 failed=3 nodes=['tests/orchestration/test_steering_notes.py::TestTheNotes::test_three_notes_render_numbered_and_a_second_consume_publishes_nothing_new', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_round_one_is_untouched_and_round_two_differs_by_exactly_the_segment', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_a_note_consumed_at_round_two_is_still_in_round_threes_prompt'] caught=True restored=True
m5 a job-wide record always carries "task_id": "": exit=1 failed=1 nodes=['tests/orchestration/test_steering_notes.py::TestTheAddress::test_a_job_wide_records_key_set_is_exactly_f264s'] caught=True restored=True
m6 compose_builder_prompt never registers builder_operator_notes: exit=1 failed=3 nodes=['tests/orchestration/test_steering_notes.py::TestTheSegment::test_the_manifest_order_and_rank_with_both_texts', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_round_one_is_untouched_and_round_two_differs_by_exactly_the_segment', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_a_note_consumed_at_round_two_is_still_in_round_threes_prompt'] caught=True restored=True
m7 builder_operator_notes is registered after builder_directive: exit=1 failed=3 nodes=['tests/orchestration/test_steering_notes.py::TestTheSegment::test_the_manifest_order_and_rank_with_both_texts', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_round_one_is_untouched_and_round_two_differs_by_exactly_the_segment', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_a_note_consumed_at_round_two_is_still_in_round_threes_prompt'] caught=True restored=True
m8 SAFE POINT 1 passes "" as operator_notes_text: exit=1 failed=2 nodes=['tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_round_one_is_untouched_and_round_two_differs_by_exactly_the_segment', 'tests/orchestration/test_steering_notes.py::TestTheCallBoundary::test_a_note_consumed_at_round_two_is_still_in_round_threes_prompt'] caught=True restored=True
m9 the report lists a consumed note: exit=1 failed=1 nodes=['tests/orchestration/test_steering_notes.py::TestTheReport::test_a_pending_tasks_note_and_a_consumed_note_give_no_key'] caught=True restored=True
m10 the report lists a note of a pending task: exit=1 failed=1 nodes=['tests/orchestration/test_steering_notes.py::TestTheReport::test_a_pending_tasks_note_and_a_consumed_note_give_no_key'] caught=True restored=True
m11 the text report leaves out the Steering not consumed: line: exit=1 failed=1 nodes=['tests/orchestration/test_steering_notes.py::TestTheReport::test_a_passed_tasks_unconsumed_note_is_in_the_report'] caught=True restored=True
control (end): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Real exit 0. Then `git worktree remove --force .remedy-wt/f030-r1-mut` →
success; `git worktree prune` → success; `git worktree list | wc -l` → 61.

## Authored-text proofs

Every reviewer-authored text applied this round, disk-to-disk against the
committed `.agent/authored/` copy (G1 above, all byte-identical, True):
`f030-r1-block.md` vs `.remedy-wt/f030-r1/block.md`; `f030-r1-plan.md` and
`f030-r1-context.md` vs the two state payloads; `f030-r1-claim.diff` vs the
claim payload (and separately, `git apply --check` on it read real exit 0
before the real `git apply`, also real exit 0). No other reviewer-authored
text was applied this round — the production code (S1–S6), the test file
and the mutation tool are worker-authored against the block's specification,
not transcribed reviewer text.

## Deviations & assumptions

1. **C4 split into C4a/C4b (constraint 2).** The block's single C4
   ("tests/orchestration/test_steering_notes.py and … saved as
   .agent/authored/f030-r1-mutations.py") measured, staged together,
   exactly 500 insertions by `git diff --cached --numstat` (307 + 193) —
   AT the cap, not UNDER it. Split into C4a (the test file, 307
   insertions, `5c5abca11`) and C4b (the mutation tool, 193 insertions,
   `e1ca56e1a`), each with its own subject, per constraint 2's own
   instruction ("split a commit that would reach it into parts … C4a and
   C4b, and say so"). No other deviation from the block's ordered commit
   sequence.
2. No test wrote by this round needed correction before C5 (constraint 4
   is not exercised): every new test passed on first run and every
   mutation was caught on the first pass of the mutation tool — no
   test was added after the fact.

No assumption beyond the block's own text was needed.

## Next

Per the block's `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from
disk) first; then the review of round 1; then T002 — the write door's
`job.steer-task` and `remedy job steer` with the task state gate, the
audit and the event. Open-findings count: 0. Operator-questions count: 0.
