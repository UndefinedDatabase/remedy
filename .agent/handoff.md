# Handback — F272 round 3

## Session

`SESSION 1 of feature F272 · round 3 · rounds so far 3`

Context self-assessment: comfortable. The round did not end on context.

**THE ROUND ENDED ON THE `.agent/STOP` SENTINEL.** `.agent/STOP` did not exist
at the reading taken immediately before C3 and DID exist when C3 was staged
(zero bytes, mtime `2026-09-06 15:30:48`, observed `15:32:14`). Protocol
guardrail G6 says: finish the current commit if one is half-written, then hand
off and end. C3 was half-written, so C3 was finished; **C4 was not started**
and this handback is the round's last commit. Nothing was reverted, no scope
was widened, and the sentinel was NOT deleted.

**THE ROUND'S PURPOSE IS ACHIEVED.** The red round 2 left is gone: the 25-file
set went from 207 failures at `b189a03f` to **2**, and the canary
`tests/cli/test_golden_path.py` is exit 0 at **42 passed**, round 1's reading.

**THE 2 REMAINING FAILURES ARE A SECOND INSTANCE OF R-0818, OUTSIDE `tests/`.**
`tests/cli/test_propose_cli_runtime.py` and `tests/cli/test_worker_cli_runtime.py`
do NOT reach the path through `tests/cli/runtime_helpers.py` as the block states.
They shell out to `scripts/remedy_runtime_cli_smoke.py`, which hand-spells the
job-keyed run log at **line 168**, `runs_dir = root / "runs" / jid`. That path
is outside `tests/`, so the reviewer's "every `"runs" /` component in all of
`tests/`" measurement could not see it, and it is absent from this round's
exhaustive change set. Per the block ("report it rather than editing it") and
protocol G8 ("never widen scope to route around a block"), it was NOT edited.
Attribution is by demonstration, not assumption — see Verification.

## Range

`Review of b189a03f..HEAD` (this handback commit is HEAD).

## Commits

### 96e991e0 f272: save the round 3 repair block as the authored original
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f272-r3.md` | +355/-0 | C0a — `shutil.copyfile` of the block, byte-identical |

### 8ac59b04 f272: mirror the round 3 repair block into the last-block slot
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +279/-303 | C0b — same bytes mirrored into the last-block slot |

### c778a8b7 f272: point the plan at the round 3 repair sweep
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +23/-22 | C1 — PLANF272R3 slice plus exactly one trailing newline |

### 20737a16 f272: register finding R-0818 for the under-counted observer set
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2/-0 | C2 — FIND0818 appended BEFORE any repair |

### aaa55053 f272: sweep the job-keyed run log to job_logs across the 24 test files
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/runtime_helpers.py` | +3/-3 | 1 path component + 2 docstring lines |
| `tests/cli/test_golden_path.py` | +2/-2 | 2 path components |
| `tests/cli/test_job_rerun_manifest.py` | +1/-1 | 1 path component |
| `tests/cli/test_teach_cmd.py` | +1/-1 | 1 path component |
| `tests/orchestration/test_budget_tick.py` | +1/-1 | 1 path component |
| `tests/orchestration/test_event_persistence.py` | +1/-1 | 1 path component |
| `tests/orchestration/test_event_replay.py` | +1/-1 | 1 module-level helper |
| `tests/orchestration/test_job_stop_integration.py` | +2/-2 | 2 path components |
| `tests/orchestration/test_structured_planner_cli.py` | +2/-2 | 2 path components |
| `tests/orchestration/test_worker_execution.py` | +4/-4 | 4 path components |
| `tests/orchestration/test_worktree_lifecycle.py` | +1/-1 | 1 path component |
| `tests/orchestration/test_worktree_resume_cli.py` | +1/-1 | 1 path component |
| `tests/test_agent_loop.py` | +5/-5 | 5 path components |
| `tests/test_agent_loop_execution.py` | +3/-3 | 3 path components |
| `tests/test_brain_detail.py` | +3/-3 | 3 path components |
| `tests/test_brain_smoke.py` | +3/-3 | 2 path components + 1 docstring line |
| `tests/test_brain_viewer.py` | +2/-2 | 2 path components |
| `tests/test_context_coverage.py` | +2/-2 | 2 path components |
| `tests/test_patch_apply.py` | +6/-6 | 6 path components |
| `tests/test_patch_intent_approval.py` | +5/-5 | 5 path components |
| `tests/test_project_brain.py` | +5/-5 | 5 path components |
| `tests/test_project_constitution.py` | +1/-1 | 1 path component |
| `tests/test_project_context_coverage.py` | +4/-4 | 3 path components + 1 comment line |
| `tests/test_run_log_cli.py` | +2/-2 | 1 module-level helper + 1 docstring line |

56 path components changed, 5 prose lines corrected, 24 files, +61/-61.

### C5 — this commit
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C5 — this handback (a handoff cannot table its own insertion count; §3 items 14 and 31) |

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | `.agent/authored/f272-r3.md`, byte-identical, committed alone |
| C0b | done | `.agent/last_block.md`, same bytes, committed alone |
| C1 | done | plan rewritten from PLANF272R3 + one newline, committed alone |
| C2 | done | FIND0818 appended, committed alone, BEFORE C3 |
| C3 | done | 24 files swept; 56 job-keyed components; 6 survivors, all non-job-keyed |
| C4 | skipped | `.agent/STOP` appeared mid-round; protocol G6 permits finishing only the half-written commit (C3), then handing off. `docs/roadmap/features/T2_F272.md` is UNCHANGED and DECISION F272 D2 is NOT on disk. See Deviations. |
| C5 | done | this handback |

## External actions

| Command | Outcome |
|---------|---------|
| `git push` | run after this commit; see Next |

No PR created, no PR merged, no branch created or switched, no `git worktree`
added or removed, no `gh` command run, nothing reverted.

## Verification

Every reading below is real. Exit codes were read from
`subprocess.run(...).returncode` inside scripts under the gitignored
`.remedy-wt/`, per the session's shell-guard constraint.

**G1 TRANSPORT — PASS.** One sha256 across all three files:
`428de848e99a4e2cc45e3b9fa6dab16936949819a634c6e17ccceba0280e4fea`, equal to
BLOCK_SHA. One byte length: **24241**, equal across all three.
`filecmp.cmp(shallow=False)` source-vs-saved `True`; source-vs-mirror `True`.

**G2 THE RECORD, at C2 — PASS, all four readers.**
- (a) BYTE: before **961527**, after **965104**, delta **3577** = 1 + 3575 + 1.
  Pre is a byte-exact prefix: `True`. `post == pre + NL + slice + NL`: `True`.
  Pre's own terminal byte asserted before writing: exactly one `\n`. Post also
  ends in exactly one `\n`.
- (b) STRUCTURAL, computed independently of (a) by splitting the whole image on
  `\n{2,}`: units before **438**, after **439**, delta **1**. N counted from the
  slice by the script = **1**. Last N units equal the slice's paragraphs in
  order: `True`. Units before are an unchanged prefix: `True`.
- (c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk. The first
  appended paragraph occupies post bytes 961528..965103; the flip offset 961568
  was ASSERTED to lie inside it before flipping (`b'O'` → `b'o'`). Reader (a)
  REJECTS, reader (b) REJECTS. Restored: reader (a) `True`, reader (b) `True`,
  and the restored image equals the disk image: `True`.
- (d) COUNTS before → after: distinct `^- R-\d{4} — ` ids **301 → 302**;
  distinct `^Done: R-\d{4} — ` ids **3 → 3**; open set BY DISTINCT ID
  **298 → 299**, up by exactly one; `^- R-0818 — ` **0 → 1**; `^Gate: `
  **24 → 24**; `^Done:` in the appended region **0**; `^Landed:` in the
  appended region **0**. Separately confirmed: the maximum registered id before
  C2 was **R-0817**, and the single pre-existing textual occurrence of "R-0818"
  is the ledger header note naming it as the next free id, not a registration.

**G3 THE PLAN, at C1 — PASS.** `.agent/plan.md` is **2098** bytes = the
PLANF272R3 slice (2097) plus exactly one trailing newline; equality `True`.
**43** lines, under the AGENTS.md cap of 50. Carries `## Goal` and
`## Next Steps`: `True`, `True`.

**G4 THE SWEEP IS COMPLETE AND SCOPED, at C3 — PASS, all three parts.**
- (i) `git diff --numstat 20737a16 aaa55053` exit 0: **24 files, 61 insertions,
  61 deletions**. `git diff --name-only` over C3 lists **24** paths, and the
  sorted list equals the change set's 24 C3 paths exactly — extras `[]`,
  missing `[]`.
- (ii) THE SURVIVOR INVENTORY — every line in ALL of `tests/` still holding a
  `"runs" /` path component after C3, enumerated rather than regex-classified:

      tests/orchestration/test_context_compiler.py:1451:    target = tmp_path / "runs" / CONTEXT_SIZE_FILENAME
      tests/orchestration/test_failure_postmortem.py:412:        run = tmp_path / "runs" / "r1"
      tests/orchestration/test_failure_wiring.py:903:        (real_repo / "remedy_data" / "runs" / "postmortem.json").write_text("{}\n")
      tests/orchestration/test_gauntlet_runner.py:490:    (real_root / "runs" / "postmortem.json").write_text(
      tests/test_data_paths.py:396:        assert run_dir(rid, arg_root) == arg_root / "runs" / rid
      tests/test_data_paths.py:430:        assert pingpong_run_dir(rid, arg_root) == arg_root / "runs" / rid

  **TOTAL SURVIVORS: 6.** Exactly the six non-job-keyed sites named under C3;
  no seventh. My own pre-sweep count over all of `tests/` was **62**
  occurrences, **56** job-keyed across **24** files, **6** surviving — the
  reviewer's figures reproduce.
- (iii) `git diff 20737a16 aaa55053 -- tests/test_data_paths.py
  tests/test_run_log.py tests/test_timeline.py` exit 0, **0 bytes, EMPTY**.

**G5 THE RED IS GONE, at C3 — PARTIAL. The red the round targeted is gone; 2 of
1125 remain, from a site outside the block's search.**
- `python3 -m pytest <the 25 files> -q -p no:randomly`: **EXIT 1**,
  `2 failed, 1123 passed in 69.04s`. Against `b189a03f`'s 207 failures over the
  same observers, that is **205 failures removed**. The 2 are
  `tests/cli/test_propose_cli_runtime.py::TestProposeRuntimeSmoke::test_propose_flow`
  and `tests/cli/test_worker_cli_runtime.py::TestWorkerRuntimeSmoke::test_worker_flow`
  — the two files the block names as unedited-and-must-go-green. Reported, not
  edited.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly`:
  **EXIT 0, 42 passed**. That is round 1's reading; 41 was the red reading.
- `python3 -m apps.cli.grouped integrity check --json`: **EXIT 0**,
  `"passed": true`, `"fail_count": 0`, `check_count`/`checks`/`version` present.

**ATTRIBUTION OF THE 2, BY DEMONSTRATION RATHER THAN ASSUMPTION.** A read-only
probe under `.remedy-wt/` loaded `scripts/remedy_runtime_cli_smoke.py` by path
and ran `smoke_propose` and `smoke_worker` twice — once with the shipped
`read_events`, once with an IN-MEMORY copy whose only difference is
`root / "job_logs" / jid` instead of `root / "runs" / jid`. The repo file was
never written (verified after the probe):

    === UNPATCHED (repo as committed) ===
      propose: FAIL — AssertionError:
      worker:  FAIL — AssertionError:
    === PATCHED to job_logs ===
      propose: PASS
      worker:  PASS
    repo file unchanged on disk: True

The single cause is `scripts/remedy_runtime_cli_smoke.py:168`. Both smoke flows
call `read_events`, which returns `""` because the job-keyed directory moved,
so `assert "proposed_task_evaluated" in events` fails. One line fixes both.

**G6 THE FEATURE FILE, at C4 — NOT RUN.** C4 does not exist (STOP). No
`docs/roadmap/**` path is in this round's diff, so the two docs runs the gate
conditions on that path — `tests/docs/` and
`tests/orchestration/test_roadmap_index.py` — were not triggered and were not
run. `docs/roadmap/features/T2_F272.md` is byte-unchanged this round.

**G7 LINT, at C3 — RED, and PRE-EXISTING. Declared, not routed around.**
`python3 -m ruff check <the 24 changed files>` in one invocation: **EXIT 1**,
`Found 2 errors`, both `F401 [*] 'json' imported but unused` in
`tests/test_project_context_coverage.py` at **line 633** and **line 662**
(`import json as _json`). Neither is a line this round touched; neither is
within 20 lines of a swept line. Pre-existence proved three ways:
`python3 -m ruff check tests/test_project_context_coverage.py` at C2 (working
tree stashed) reports the same 2; the same check against
`git show main:tests/test_project_context_coverage.py` on `main` at `b18fad57`
reports the same 2; and `python3 -m ruff check .` reports **26** errors
repository-wide, of which these are 2. C3's spec says change the `"runs"`
component "and nowhere else", so removing two unrelated unused imports was
declined under protocol G8. The gate as written is unmeetable at any commit on
this branch and on `main`.

**G8 THE TREE — one clause RED, by the sentinel itself.**
- `git status --porcelain` after C3 and before C5 is staged: **NOT EMPTY**. Its
  entire content is `?? .agent/STOP` — the untracked sentinel that ended the
  round. There is no other working-tree residue. The sentinel was deliberately
  not deleted and not committed.
- `git ls-files .remedy-wt`: **empty**.
- Per commit, C0a through C3 (C4 does not exist), insertions from
  `git diff --numstat <parent> <commit>`, all single-parent, all under the
  DECISION F104 D1 cap of 500:

      C0a 96e991e0  +355  -0    1 file   parents=1
      C0b 8ac59b04  +279  -303  1 file   parents=1
      C1  c778a8b7  +23   -22   1 file   parents=1
      C2  20737a16  +2    -0    1 file   parents=1
      C3  aaa55053  +61   -61   24 files parents=1

  C0b's +279/-303 is a verbatim rewrite of a single `.agent/**` state file and
  is exempt by DECISION F104 D1 in any case.
- BEGIN/END marker-prefix line counts in `.agent/plan.md`,
  `.agent/live_review.md`, `docs/roadmap/features/T2_F272.md` and each of the
  24 swept files: **27 files checked, maximum count 0**. No leaked markers.

**Constraint 11, re-measured from the committed `.agent/authored/f272-r3.md`.**
TOTAL **355** lines against the 490-line budget of DECISION F085 D6: within.
Slice BODY lines **79**; PROSE = TOTAL − slice bodies = **276** against the
400-line cap of DECISION F105 D5: within. Both reproduce the reviewer's figures.

**`.agent/STOP` — the three ordered readings, by `os.path.exists`.**

| Reading | When | Result |
|---------|------|--------|
| 1 | before C0a | `False` |
| 2 | before C3 | `False` |
| 3 | before C5 | `True` |

## Authored-text proofs

| Text | Applied | Proof |
|------|---------|-------|
| PLANF272R3 | yes (C1) | disk `.agent/plan.md` == slice + one `\n`, 2098 bytes, equality `True`; slice extracted from the committed `.agent/authored/f272-r3.md`'s source by exact-position marker matching, asserting exactly one BEGIN and one END |
| FIND0818 | yes (C2) | G2 (a)+(b)+(c)+(d) above, all pass, including the in-memory negative control |
| DECISIOND2 | **NO** | C4 not started (STOP). The slice is intact in `.agent/authored/f272-r3.md` and `.agent/last_block.md` and can be applied unchanged next round |

Marker extraction asserted exactly one `<<<BEGIN name>>>` and one
`<<<END name>>>` line per name for all three slices. No slice was edited.

## Deviations & assumptions

1. **C4 WAS NOT EXECUTED — a dropped commit in the block's ordered sequence.**
   `.agent/STOP` appeared between the pre-C3 reading (`False`) and the staging
   of C3. Protocol G6 allows finishing only the half-written commit, then
   handing off. C3 was half-written and was finished; C4 was not started.
   Consequence: **DECISION F272 D2 is not on disk**, D1's premise sentence
   stands uncorrected in `docs/roadmap/features/T2_F272.md`, and block gate G6
   is NOT RUN. Nothing is lost — the finding itself persisted at C2, which is
   exactly the ordering the block chose for this reason.
2. **G7 LINT IS RED AND WAS NOT REPAIRED.** 2 pre-existing `F401`s in
   `tests/test_project_context_coverage.py:633,662`, present on `main` and at
   C2, part of a 26-error repository-wide baseline. C3's spec forbids changing
   anything but the `"runs"` component; protocol G8 forbids widening scope to
   route around a block. Declared here rather than silently fixed.
3. **G8's `git status --porcelain` clause is RED, containing only
   `?? .agent/STOP`.** The sentinel was not deleted, not committed and not
   `.gitignore`d — any of the three would be routing around the block.
4. **THE BLOCK'S EXPLANATION OF THE TWO UNEDITED FILES IS FACTUALLY WRONG, AND
   THE ERROR IS THE SAME ONE R-0818 NAMES.** The block says
   `tests/cli/test_propose_cli_runtime.py` and
   `tests/cli/test_worker_cli_runtime.py` "reach the path through
   `tests/cli/runtime_helpers.py`". They do not — neither file imports it. Both
   `subprocess`-launch `scripts/remedy_runtime_cli_smoke.py`, which hand-spells
   the job-keyed run log at line 168. Because that file is outside `tests/`,
   the reviewer's "all of `tests/`" measurement and this round's own G4(ii)
   survivor inventory are BOTH blind to it. The block was applied as written
   and the two files were not edited, as ordered.
5. **NOT LANDING C4 PREVENTED A SECOND UNDER-SCOPED CLAIM.** The DECISIOND2
   slice's CONSEQUENCE paragraph reads: "The gate is the job-keyed spelling
   counted to zero across all of `tests/`, never the word counted anywhere."
   Finding 4 shows that scope is still too narrow — a job-keyed spelling
   survives outside `tests/`. Applying DECISIOND2 verbatim would have landed a
   correction that repeats the error it corrects. This is recorded as an
   objection under constraint 1; the slice was not edited, because it was not
   applied at all.
6. Five prose lines were corrected beside swept lines, under C3's clause "where
   a docstring or comment beside a swept line describes the old layout as
   current": `tests/cli/runtime_helpers.py:272,274`,
   `tests/test_run_log_cli.py:45`, `tests/test_project_context_coverage.py:682`,
   `tests/test_brain_smoke.py:142`.
7. **One stale prose mention was deliberately LEFT ALONE:**
   `tests/cli/test_teach_cmd.py:196` says a job's run log "sat in
   `<data_root>/runs/edbbc42bba4c4b00/`". It is a dated, past-tense account of
   an operator observation on 2026-08-25, and it sits 139 lines from that
   file's only swept line, so it meets neither half of C3's clause. Rewriting
   it would falsify a historical record.
8. Local variable names (`runs`, `runs_dir`, `_write_run_events`) were not
   renamed. They name the run-log directory generically, not a path spelling,
   and AGENTS.md forbids mass renames as their own activity.
9. All 56 sites were read in context before being changed, and each was
   confirmed job-keyed by its next path component (`job.id`, `job_id`,
   `job.job_id`, `jid`, `str(job.id)`, `str(job_id)`). For
   `tests/orchestration/test_event_persistence.py:29` the confirmation was
   indirect and is worth stating: `jid` is passed to `emit_important_event`,
   which delegates to `timeline.append_run_event`, which resolves through
   `data_paths.run_log_dir`.
10. No file under `packages/` or `apps/` was touched. Round 2's C4 is not
    reverted in whole or in part. Exactly one id was minted (R-0818); none
    resolved, none renumbered. No `Done:` and no `Landed:` line was written.
    Commit order followed the block: C0a, C0b, C1, C2, C3, then C5.

## Next

The reviewer gates this round, then authors round 4, which must do three things
the STOP cut short: (1) apply DECISION F272 D2 to
`docs/roadmap/features/T2_F272.md` — with its CONSEQUENCE paragraph widened
past "all of `tests/`", per deviation 5; (2) change
`scripts/remedy_runtime_cli_smoke.py` line 168 from `root / "runs" / jid` to
`root / "job_logs" / jid`, which is the whole of the remaining red; and (3)
decide whether the sweep's completeness gate should search the repository
rather than `tests/`, which is R-0818's own standing rule applied to itself.
`.agent/STOP` must be removed by the operator before any further round.
