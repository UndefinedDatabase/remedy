# Handback — F272 round 2

## Session

`SESSION 1 of feature F272 · round 2 · rounds so far 2`

Context self-assessment: comfortable. The round ended on a RED GATE, not on
context exhaustion.

**THE ROUND IS BLOCKED. THE BRANCH TIP IS RED.** G8's canary was ordered exit 0
at 42 passed and is exit 1 at 41 passed at C4. The cause is not a defect in the
applied change: it is that the block's change set, and DECISION F272 D1's own
sentence "the only code that observes the change is the three test files that
hand-spell the layout", are FALSE BY MEASUREMENT. **22 test files** hand-spell
`<root>/runs/<job_id>`, and **205 tests** are red at `1d24b4a7`. Per
`docs/agents/self_drive_protocol.md` guardrail G8 — "any red gate,
contradiction … → write the handoff and end cleanly. Never guess, never widen
scope to route around a block" — this worker did NOT widen the sweep beyond the
three files the block named, and did NOT revert. Both are re-rulings that
belong to the planner/reviewer.

## Range

Review of `69138a45eeb5d31d996e47ec5c2591bfec57085c`..`1d24b4a7` plus the C5
commit that writes this file.

## Commits

### 5a93878c f272: save the round 2 step block as the authored original
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r2.md` | +379/-0 | C0a — `shutil.copyfile` of the block, never a retype |

### 948977a7 f272: mirror the round 2 step block into the last-block slot
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +322/-431 | C0b — same bytes; one indivisible `.agent/**` state rewrite (DECISION F104 D1 exemption) |

### bdef4507 f272: point the plan at the round 2 run re-key and its staging
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +20/-20 | C1 — the PLANF272R2 slice plus exactly one trailing newline |

### 6f1efb37 f272: book the round 1 verdict into the live review record
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C2 — the GATEF272R1 append; blank separator plus the one paragraph |

### 43d91cda f272: record DECISION F272 D1 staging the run re-key in two moves
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +62/-0 | C3 — the DECISIOND1 append; blank separator plus the slice's 61 lines |

### 1d24b4a7 f272: move the job run log to job_logs and the run store to runs
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | +35/-25 | C4(a) — `job_logs_dir` added; `run_log_dir` and `pingpong_runs_dir` bodies changed; Public API list and both comment blocks re-stated |
| `tests/test_data_paths.py` | +18/-12 | C4(b) — the `run_log_dir` and `pingpong_*` equalities and their docstrings |
| `tests/test_run_log.py` | +3/-3 | C4(b) — lines 128, 134, 175 |
| `tests/test_timeline.py` | +11/-5 | C4(b) — the `_runs_path` helper plus lines 255, 273, 274, 767 |

### C5 (this commit) f272: record the round 2 blocker in the plan and hand back
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C5 — this handback |
| `.agent/plan.md` | rewrite | AGENTS.md "If Blocked" rule 2 — the plan MUST carry the exact blocker; declared as a deviation below |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | block copied byte-identical to `.agent/authored/f272-r2.md`, committed alone |
| C0b | done | same bytes mirrored to `.agent/last_block.md`, committed alone |
| C1 | done | `.agent/plan.md` = PLANF272R2 + one newline, 2172 bytes, 43 lines |
| C2 | done | GATEF272R1 appended; every G2 count landed on its predicted value |
| C3 | done | DECISIOND1 appended; nothing already in the file moved by one byte |
| C4 | deviated | applied as specified, and it turns the branch tip RED: the spec's three-file observer set is incomplete by 22 files / 205 tests. The sweep was NOT widened (protocol G8). One in-file docstring outside the cited lines was corrected — see deviations |
| C5 | deviated | written as ordered, but the commit also rewrites `.agent/plan.md`, which AGENTS.md "If Blocked" rule 2 compels and which the block attributed to C1 only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f272-r2-redproof 1d24b4a7` | exit 0 — G7 |
| `git worktree remove --force .remedy-wt/f272-r2-redproof` | exit 0 |
| `git worktree add --detach .remedy-wt/f272-r2-diffprobe 1d24b4a7` | exit 0 — G7 addendum |
| `git worktree remove --force .remedy-wt/f272-r2-diffprobe` | exit 0 |
| `git worktree add --detach .remedy-wt/f272-r2-canary-control 43d91cda` | exit 0 — canary attribution control |
| `git worktree remove --force .remedy-wt/f272-r2-canary-control` | exit 0 |
| `git worktree prune` (after each) | exit 0 |
| `git worktree list` | 13 lines: the primary checkout plus the 12 pre-existing `remedy/job-*` worktrees that predate this round. No `f272-r2` worktree remains |
| `git push` | see below |
| `gh pr create` / `gh pr merge` | NOT RUN — constraint 9 |

## Verification

**G1 TRANSPORT.** One sha256
`3376cfc5939bdde59665369d310971ea4a84d1af3c66c7e6f64ceeb6718ffcc6` = BLOCK_SHA,
one byte length 27503, 379 lines, for all three artefacts.
`filecmp.cmp(shallow=False)` source-vs-saved `True`; source-vs-mirror `True`.

**G2 THE RECORD, at 6f1efb37.**
(a) BYTE — pre-image terminal byte asserted BEFORE writing: exactly one newline
(last two bytes `b'.\n'`). 955908 → 961527 bytes, delta 5619 = 1 + 5617 + 1.
`post == pre + NL + slice + NL` `True`; pre is a byte-exact PREFIX `True`;
post ends in exactly one newline `True`.
(b) STRUCTURAL, computed independently — N counted from the slice by the script
= 1. Units 437 → 438; last N units equal the slice's paragraphs IN ORDER `True`;
the leading units are unchanged as a prefix `True`.
(c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk — first
appended paragraph occupies `[955909, 961526)`; chosen offset 958717 asserted
INSIDE it `True`; byte `b'e'` flipped to `b'E'`. Reader (a) REJECTS `True`;
reader (b) REJECTS `True`. After restoring: reader (a) ACCEPTS `True`; reader
(b) ACCEPTS `True`; restored image == disk image `True`.
(d) COUNTS before → after: `^Gate: ` 23 → 24; `^Gate: F272 R1 — ` 0 → 1;
`^Gate: R1 — ` 1 → 1 UNCHANGED; distinct `^- R-\d{4} — ` 301 → 301; distinct
`^Done: R-\d{4} — ` 3 → 3; open set BY DISTINCT ID 298 → 298. Every one of the
six landed on the value the block predicted. No id minted, resolved or
renumbered. Also confirmed by reading `scripts/rotate_live_review.py`: its
first pattern `^Gate: F(\d{3}) R\d+` (line 73) is the one this header matches.

**G3 THE PLAN, at bdef4507.** `.agent/plan.md` = PLANF272R2 + exactly one
trailing newline: `True`. 2172 bytes (slice 2171). 43 lines, under the
AGENTS.md 50-line cap. Carries `## Goal` `True` and `## Next Steps` `True`.

**G4 THE FEATURE FILE, at 43d91cda.** Pre-commit blob 6852 bytes is a byte-exact
PREFIX of the 10790-byte post-commit file `True`. Slice + leading + trailing
newline is an exact SUFFIX `True`. Lines the diff ADDS: 62 = the blank separator
the append recipe writes, then the slice's 61 lines IN ORDER (`added[1:] ==
slice_lines` `True`; `added == [""] + slice_lines` `True`). See deviations.
`python3 -m pytest tests/docs/ -q -p no:randomly` exit **0**, `303 passed`.
`python3 -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly`
exit **0**, `30 passed`. Both at their base counts.

**G5 THE CODE, at 1d24b4a7.**
`python3 -m ruff check packages/orchestration/data_paths.py
tests/test_data_paths.py tests/test_run_log.py tests/test_timeline.py`
exit **0**, `All checks passed!`.
Read from the SHIPPED functions with `R = Path("/R")`:

| Call | Returned |
|---|---|
| `job_logs_dir(R)` | `/R/job_logs` |
| `run_log_dir("j1", R)` | `/R/job_logs/j1` |
| `runs_dir(R)` | `/R/runs` |
| `run_dir("r1", R)` | `/R/runs/r1` |
| `pingpong_runs_dir(R)` | `/R/runs` |
| `pingpong_run_dir("r1", R)` | `/R/runs/r1` |

All six equal their expected value. `pingpong_runs` occurs **0** times in those
six RETURNED paths. Module resolved from
`/home/decodeux/Repos/remedy/packages/orchestration/data_paths.py`.

**G6 THE OBSERVERS AND THE NEIGHBOURS, at 1d24b4a7, run SERIALLY.**

| Command | Exit | Result |
|---|---|---|
| `pytest tests/test_data_paths.py tests/test_run_log.py tests/test_timeline.py -q -p no:randomly` | 0 | `140 passed in 0.78s` |
| `pytest tests/test_do_job_flow.py tests/orchestration/test_job_run_refs.py -q -p no:randomly` | 0 | `182 passed in 28.58s` (178 + 4, both base counts) |
| `pytest tests/ui_server/ -q -p no:randomly` | 0 | `515 passed in 33.43s` |
| `pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -p no:randomly` | 0 | `89 passed in 17.32s` |

Every ordered suite is green at its base count. G6 as written cannot see the
failure G8 found, because none of the 22 files below is in it.

**G7 THE PRE-SWEEP RED PROOF**, in the disposable worktree
`.remedy-wt/f272-r2-redproof` at `1d24b4a7`, `python3 -B` throughout, every
`__pycache__` purged before each run.

(i) CONTROL: `python3 -B -m pytest tests/test_data_paths.py tests/test_run_log.py
tests/test_timeline.py -q -p no:randomly` exit **0**, `140 passed in 0.81s`.
`packages.orchestration.data_paths.__file__` as imported there is
`/home/decodeux/Repos/remedy/.remedy-wt/f272-r2-redproof/packages/orchestration/data_paths.py`
— INSIDE the worktree `True`, so no editable install shadowed it. The control is
exit 0, so the proof is NOT void.

(ii) PRE-SWEEP: `git checkout 43d91cda -- tests/test_data_paths.py
tests/test_run_log.py tests/test_timeline.py` exit 0, `data_paths.py` left at
C4. Same pytest command: exit **1**, `17 failed, 123 passed in 0.94s`. The 17:

```
tests/test_data_paths.py::TestDirectoryHelpers::test_run_log_dir_coerces_a_uuid_job_id_to_its_string_form
tests/test_data_paths.py::TestDirectoryHelpers::test_run_log_dir_explicit_root
tests/test_data_paths.py::TestDirectoryHelpers::test_run_log_dir_follows_the_process_data_root
tests/test_data_paths.py::TestJobAndRunLayout::test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir
tests/test_run_log.py::TestRunLogWriterConstruction::test_creates_job_directory
tests/test_run_log.py::TestRunLogWriterConstruction::test_default_data_root_is_the_process_data_dir
tests/test_run_log.py::TestRunLogWriterConstruction::test_path_is_inside_job_directory
tests/test_timeline.py::TestCmdTimeline::test_prints_planning_completed_in_output
tests/test_timeline.py::TestCmdTimeline::test_prints_timeline_for_job_with_logs
tests/test_timeline.py::TestCmdTimeline::test_timeline_output_includes_next_action
tests/test_timeline.py::TestLoadRunEvents::test_accepts_uuid_or_str_job_id
tests/test_timeline.py::TestLoadRunEvents::test_ignores_empty_lines
tests/test_timeline.py::TestLoadRunEvents::test_ignores_malformed_json_lines
tests/test_timeline.py::TestLoadRunEvents::test_loads_multiple_files_sorted_by_timestamp
tests/test_timeline.py::TestLoadRunEvents::test_loads_single_jsonl_file
tests/test_timeline.py::TestOneRunPerInvocation::test_all_events_of_one_invocation_share_one_run
tests/test_timeline.py::TestOneRunPerInvocation::test_two_jobs_do_not_share_a_run_file
```

Every one names a run-log or ping-pong path assertion. Non-zero exit, real
failures, real names: the swept tests do observe the paths C4(a) moved.

(iii) `git -C <worktree> diff --name-only` after the restore: exit 0, **empty**.
That is the real output of the ordered command; it is empty because
`git checkout <sha> -- <paths>` STAGES what it writes. Rather than assert that,
it was measured in a second disposable worktree (`f272-r2-diffprobe`, same
commit, same checkout): `git diff --name-only` → empty; `git diff --name-only
HEAD` → exactly `tests/test_data_paths.py`, `tests/test_run_log.py`,
`tests/test_timeline.py`; `git status --porcelain` → `M ` on those three and
nothing else. So the restore touched exactly the three intended files.

Both worktrees removed and pruned. `git worktree list` = 13 lines, none of them
this round's.

**G8 THE CANARY, INTEGRITY AND THE TREE, at 1d24b4a7, before C5 was staged.**

`python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly`
exit **1** — `1 failed, 41 passed in 20.93s`. **RED. The block ordered exit 0 at
42 passed.** The single failure:

```
tests/cli/test_golden_path.py::TestLLMIntakeWiring::test_fake_provider_stores_llm_intake_with_evidence
  tests/cli/test_golden_path.py:335: AssertionError: evidence directory must exist
  runs_dir = tmp_path / "data" / "runs" / job_id      # line 334, hand-spelled
```

ATTRIBUTION MEASURED, not inferred: in a disposable worktree at C4's PARENT
`43d91cda`, the same command is exit **0**, `42 passed in 21.69s`. C4 causes it.

`python3 -m apps.cli.grouped integrity check --json` exit **0**,
`"passed": true`, `"fail_count": 0`.

`git status --porcelain` **EMPTY**. `git ls-files .remedy-wt` **EMPTY**.

Per-commit INSERTIONS from `git diff --numstat <parent> <commit>`, C0a–C4 only:

| Item | SHA | Insertions | Parents | ≤500 |
|---|---|---|---|---|
| C0a | 5a93878c | 379 | 1 | yes |
| C0b | 948977a7 | 322 | 1 | yes |
| C1 | bdef4507 | 20 | 1 | yes |
| C2 | 6f1efb37 | 2 | 1 | yes |
| C3 | 43d91cda | 62 | 1 | yes |
| C4 | 1d24b4a7 | 67 | 1 | yes |

Every commit single-parent. Marker-prefix lines (`<<<BEGIN` / `<<<END`) in each
of `.agent/plan.md`, `.agent/live_review.md`,
`docs/roadmap/features/T2_F272.md`, `packages/orchestration/data_paths.py`,
`tests/test_data_paths.py`, `tests/test_run_log.py`, `tests/test_timeline.py`:
**0, 0, 0, 0, 0, 0, 0**.

**Constraint 11 — block size, re-measured from the committed
`.agent/authored/f272-r2.md`.** TOTAL **379** lines against the 490-line budget
of DECISION F085 D6. Slice CONTENT lines: PLANF272R2 43 + GATEF272R1 1 +
DECISIOND1 61 = 105. PROSE = 379 − 105 = **274** against the 400-line cap of
DECISION F105 D5. Both figures reproduce the block's own claim exactly. (Counting
the 6 marker lines as slice rather than prose would give 268; the 274 the block
states is the reading in which marker lines count as prose.)

**Constraint 10 — the three `.agent/STOP` readings**, all by `os.path.exists`:

| When | Reading |
|---|---|
| before C0a | does NOT exist |
| before C4 | does NOT exist |
| before C5 | does NOT exist |

## Authored-text proofs

| Text | Result |
|---|---|
| the block itself | `filecmp.cmp(shallow=False)` `.remedy-wt/f272-r2-block.md` vs `.agent/authored/f272-r2.md` → `True`; vs `.agent/last_block.md` → `True`. All 27503 bytes, all sha256 `3376cfc5…8ffcc6` = BLOCK_SHA |
| PLANF272R2 | extracted by exact-position marker matching, exactly one BEGIN and one END asserted; 2171 bytes; `.agent/plan.md` at C1 == slice + `\n` → `True` |
| GATEF272R1 | 5617 bytes; post-image == pre + `\n` + slice + `\n` → `True`, plus the independent structural reader and the negative control above |
| DECISIOND1 | 3936 bytes; slice + leading/trailing newline is an exact SUFFIX of the post-commit file → `True`; the diff's added lines are the slice's 61 lines in order after the separator |

No slice was edited. Marker lines reached no file (all seven counts 0).

## Deviations & assumptions

**1. BLOCKING — C4's observer set is incomplete, and the branch tip is RED.**
The block's C4(b) and DECISION F272 D1 both state that the three swept test
files are the only code observing the moved directory. Measured at `1d24b4a7`
over 30 candidate files found by grepping `tests/` for the hand-spelled
layouts: `205 failed, 1454 passed`, across **22 files**:

| File | Failures |
|---|---|
| `tests/test_run_log_cli.py` | 56 |
| `tests/test_patch_apply.py` | 18 |
| `tests/orchestration/test_event_replay.py` | 18 |
| `tests/orchestration/test_worktree_resume_cli.py` | 16 |
| `tests/test_brain_smoke.py` | 13 |
| `tests/orchestration/test_structured_planner_cli.py` | 12 |
| `tests/orchestration/test_worktree_lifecycle.py` | 12 |
| `tests/orchestration/test_job_stop_integration.py` | 11 |
| `tests/orchestration/test_budget_tick.py` | 9 |
| `tests/test_brain_viewer.py` | 6 |
| `tests/test_project_brain.py` | 5 |
| `tests/cli/test_teach_cmd.py` | 4 |
| `tests/test_agent_loop_execution.py` | 4 |
| `tests/test_context_coverage.py` | 4 |
| `tests/test_patch_intent_approval.py` | 4 |
| `tests/test_agent_loop.py` | 3 |
| `tests/test_brain_detail.py` | 3 |
| `tests/orchestration/test_worker_execution.py` | 3 |
| `tests/cli/test_golden_path.py` | 1 |
| `tests/cli/test_job_rerun_manifest.py` | 1 |
| `tests/orchestration/test_event_persistence.py` | 1 |
| `tests/test_project_constitution.py` | 1 |

`tests/cli/runtime_helpers.py:279` is a shared non-test helper spelling the same
join, so its blast radius reaches further than its own file.

This worker did NOT sweep them. Constraint 2 makes the change set exhaustive,
`docs/agents/self_drive_protocol.md` G8 forbids widening scope to route around a
block, and a 22-file sweep is precisely the "whole-feature change standing
inside a T001 slice" that DECISION F272 D1 exists to refuse. It also did NOT
revert C4, because reverting drops an ordered commit and the reviewer needs C4
present to reproduce these numbers. The choice between widening the sweep and
re-ruling D1 belongs to the planner/reviewer.

Note that D1's ruling is not wrong about PRODUCTION code: no caller moved, and
all 74 readers and 35 writers resolve through `run_log_dir` exactly as ruled.
What was under-measured is the TEST side — the sentence "the only code that
observes the change is the three test files" was measured over three files
rather than over `tests/`.

**2. C4(b) — three cited line lists were incomplete; three more spellings were
swept inside the named files.** Re-grepped before editing, as ordered. The block
cited `tests/test_timeline.py` lines 66 and 255; lines 273, 274 and 767 carry
the same `tmp_path / "runs" / str(job_id)` join and were swept too, since C4(b)'s
binding sentence is "sweep EVERY hand-spelled occurrence … in [these three
files]" and leaving them would have left those files red. The block also did not
cite `tests/test_data_paths.py:132` (`run_log_dir("j1") == runs_dir() / "j1"`),
which is not a string literal but asserts the old relationship; it now reads
`job_logs_dir() / "j1"`. Lines 79, 102, 120 and 392 were LEFT UNCHANGED as
ordered (392 now reads 396 after a docstring grew above it; the assertion is
byte-identical).

**3. C4(a) — one docstring outside the two named comment blocks was corrected.**
`resolve_any_job_id`'s docstring said run logs live "under
`<data_root>/runs/<job-id>/`". C4(a) orders that "no comment survives claiming a
layout the code no longer has"; that sentence was one, so it now reads
`<data_root>/job_logs/<job-id>/`. One line, same file, no behaviour.

**4. C4(b) — a test helper NAME still says "runs" while returning `job_logs`.**
`tests/test_timeline.py::_runs_path`, and the local variables `runs_dir` /
`run_dir` / `job_dir` at several sites, now name a `job_logs/` path. Renaming
them is not a hand-spelled layout occurrence, so it was NOT done; instead
`_runs_path` gained a docstring stating exactly what it returns. Recommend the
rename rides along with the `pingpong_runs_dir` / `pingpong_run_dir` deletion
round, which is already a naming round.

**5. C5 also rewrites `.agent/plan.md`.** The block attributes `.agent/plan.md`
to C1 only. AGENTS.md "If Blocked" rule 2 — "Update `.agent/plan.md` with the
exact blocker" — is mandatory and AGENTS.md outranks the block, and the Commit
Gate forbids committing while the plan misdescribes the work. The plan written
at C1 said the round "sweeps the three test files that hand-spell those paths"
and listed a Risk that measurement has now refuted. The path was already in the
change set; only a second write to it was added. Still 43 lines, under the cap.

**6. G4's two clauses about the added lines do not agree, and the append recipe
decides it.** G4 asks that "the lines C3's diff ADDS are exactly the slice's
lines IN ORDER" while also requiring that "the slice plus its LEADING and
trailing newline is an exact SUFFIX". The recipe's leading newline necessarily
adds one blank line, so the diff adds 62 lines, not 61. Both readings are
reported: `added == [""] + slice_lines` is `True` and `added[1:] == slice_lines`
is `True`. The same applies to C2, where the diff adds 2 lines for a 1-line
slice. This matches the F260 R23 precedent already in `.agent/live_review.md`
("one of them the blank separator").

**7. Slice boundary convention.** A slice was taken as the text between its
marker lines MINUS the newline terminating its own last content line, so that
`slice + b"\n"` gives a file ending in exactly one newline. This is forced by
G2(a), which requires the post-image to end in exactly one newline, and it
reproduces round 1's "byte-equal to its slice plus exactly one trailing
newline" arithmetic.

**8. C0a and C0b precede the plan advance.** Not a deviation but the rule:
`docs/agents/planner_reviewer_prompt.md` §3 item 23 exempts exactly the two
block-save commits, which write nothing but the block itself.

**9. Housekeeping.** No slice was edited; no commit was reordered or dropped
from C0a–C5; no finding id was minted, resolved or renumbered (open set 298 →
298 BY DISTINCT ID; next free id remains R-0817's successor R-0818, unspent).
Nothing was merged and no PR was created. The 12 `remedy/job-*` worktrees under
`.remedy-wt/` predate this round and were left alone. All scratch lives under
the gitignored `.remedy-wt/`; `git ls-files .remedy-wt` is empty.

## Next

**The planner/reviewer must rule on the widened observer set before any further
build work.** The two options, both re-rulings:

1. **Widen the sweep.** Amend DECISION F272 D1's "three test files" sentence to
   the measured 22, and order a round that replaces the job-keyed `"runs"`
   component with `"job_logs"` across those files plus
   `tests/cli/runtime_helpers.py`. Mechanical, but it needs its own change set
   and probably its own insertion budget.
2. **Revert C4** on this branch and re-rule the re-key's staging with the
   22-file cost on the table.

Until one of those lands, the branch tip `1d24b4a7` is RED at 205 tests and
must not be merged.
