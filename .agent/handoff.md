# Handback — F263 Human-change absorption (absorb) · Round 7 · Book round 6's PASS, the one-path guard, the Built State, the self-use item, the feature's one full suite

## Session

SESSION 2 of feature F263 · round 7 · rounds so far 7

This round is the closure sequence's first half. It booked round 6's PASS
into the ledger (C2), added the one-implementation guard
`tests/orchestration/test_human_change_one_path.py` that holds `absorb`
to being called from `absorb_job` alone and `absorb_job` to being called
from exactly the three entrances DECISIONS F263 D4-D6 name (C3), wrote
the feature file's Built State (C4), generated and ran the closure's
self-use item SU-029 to its approval gate (C5), and ran the feature's ONE
full suite (C6). With T001-T003 already landed, every slice of F263 has
now been built, guarded and demonstrated running for real. G1 through G4
all ran and every reading matched the block's stated expectation
exactly, including the red proofs (2/1/1 failures for m1/m2/m3, both
controls 2 passed). G5, the full suite, went RED with one failing node —
`tests/orchestration/test_run_manifest_logical_identity.py`, unrelated to
F263's own product code — recorded per constraint 4 rather than treated
as a stop. Context self-assessment: a healthy majority of the session's
working context budget remained at handback.

## Range

Review of `d59371c1`..`HEAD`.

## Commits

### f4794c74 F263 R7 C1: copy round 7 block and payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r7-block.md | +212/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f263-r7-built_state.md | +67/-0 | Payload copy |
| .agent/authored/f263-r7-ledger.md | +2/-0 | Payload copy |
| .agent/authored/f263-r7-mutations.py | +57/-0 | Payload copy (G3 tool) |
| .agent/authored/f263-r7-plan.md | +33/-0 | Payload copy |
| .agent/authored/f263-r7-test_human_change_one_path.py | +60/-0 | Payload copy |

Measured insertions by `git show --numstat f4794c74`: 431
(212+67+2+57+33+60), matching the block's stated formula "this block's
line count plus 219" (212 + 219 = 431) exactly. Under the 500 cap.

### 3212ed8d F263 R7 C2: book round 6's PASS

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | Append of ledger.md payload (round 6's PASS entry) |
| .agent/plan.md | +13/-10 | Rewritten to the round-7 `plan.md` payload |

Measured insertions by `git show --numstat 3212ed8d`: `2 0
.agent/live_review.md`, `13 10 .agent/plan.md` — matching the block's
expected 2, 13 exactly.

### 7ef871ab F263 R7 C3: hold the command, the safe points and the apply to one absorption path

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_human_change_one_path.py | +60/-0 | New file, copied whole from the payload — the one-implementation guard |

Measured insertions by `git show --numstat 7ef871ab`: 60, matching the
block's expected 60 exactly.

### aab638e2 F263 R7 C4: write the feature file's Built State

| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F263.md | +67/-0 | Append of built_state.md payload — the feature file's Built State section |

Measured insertions by `git show --numstat aab638e2`: 67, matching the
block's expected 67 exactly.

### 970b63ca F263 R7 C5: generate and run the closure's self-use item, record its defects

| Path | +/- | Reason |
|---|---|---|
| .agent/selfuse_f263/SU-029.md | +8/-0 | The generated item's markdown |
| .agent/selfuse_f263/entry_and_job_file.txt | +5/-0 | Entry id/title/provenance/consumed_by and the job file path |
| .agent/selfuse_f263/execution_config.txt | +39/-0 | The run's resolved `ExecutionConfig` (self_use role, claude-cli, never fake) |
| .agent/selfuse_f263/full_transcript.txt | +14/-0 | Job/task summary transcript |
| .agent/selfuse_f263/human_change_checks.txt | +2/-0 | `metadata["human_change_checks"]` JSON and `recorded_human_changes(job_id)` sorted list |
| .agent/selfuse_f263/result_state.txt | +9/-0 | Job/task state after the run |
| .agent/selfuse_f263/run_defects.txt | +4/-0 | `describe_self_use_run_defects` output verbatim |
| .agent/selfuse_f263/timing.txt | +3/-0 | Started/Finished/Created timestamps |
| scripts/self_use_queue.json | +8/-0 | Generator's append of entry `SU-029`, `consumed_by` left empty this round |

Measured insertions by `git show --numstat 970b63ca`: 8/5/39/14/2/9/4/3/8
= 92 total. No registration was written; the reviewer authors findings
from `run_defects.txt` next round, per the block.

### (this commit) F263 R7 C6: record the closure suite transcript and rewrite handoff for round 7

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-closure-suite.txt | new | The full suite's summary line, real exit code and full bad-node-id list |
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f263-r7-mut 7ef871ab` (at C3) for
  G3: real exit 0.
- `git worktree remove --force .remedy-wt/f263-r7-mut`: real exit 0.
  `git worktree prune`: real exit 0.
- `run_next_self_use_item` (C5) created worktree
  `.remedy-wt/job-6a38b3203cca4928` and branch
  `remedy/job-6a38b3203cca4928`, `cleanup_status: "retained"` (the job
  blocked before an apply). Left in place per constraint 7 — not created
  by me as scratch, so not deleted.
- `npm --prefix apps/ui run build` (C6a): real exit 0.
- No `gh pr create`, no merge, no branch deletion, no STATUS/README edit,
  no `consumed_by` edit — none ordered, none taken.
- `git push origin feature/f263-human-change-absorption` after C6 — real
  outcome reported in the worker's final reply (G6 readings cannot live
  in this committed file per the block).

## Verification

**G1 — transport**: every payload's lines/bytes/sha256 measured against
the block's PAYLOADS table: all five rows matched exactly (built_state.md
67/4666, ledger.md 2/2444, plan.md 33/1300, test_human_change_one_path.py
60/2752, mutations.py 57/2436 — sha256 digests all equal to the table).
The block itself: 212 lines, 15034 bytes, sha256
`77f3c37140e4b33e813c5a5272ff3949606a568cae9d7e11c48dc18cb97ab021`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f263-r7-*` blob read with `git show
f4794c74:<path>` compared byte-for-byte against its `.remedy-wt/` source:
all six pairs (the block plus the five payloads) byte-identical = True,
sha256 equal to the table in every case.

**G2 — the booking, the guard and the Built State**: at C2 (`3212ed8d`),
`.agent/live_review.md` 386333 bytes, sha256
`5eb308ca8ad0a5edc7d77107c256d8dc94afbbd80b8134979c7b9713b73d7c6a`;
`.agent/plan.md` 1300 bytes, sha256
`2365c1ee82c6098299a9de560529201680663bacec243a56fe7c573bd10b8192`. At C3
(`7ef871ab`), `tests/orchestration/test_human_change_one_path.py` 2752
bytes, sha256
`914a2589d84c7f4957f275d1506fa66eeaa7065e25e93a6b255ecab716c0c145`. At C4
(`aab638e2`), `docs/roadmap/features/T2_F263.md` 10918 bytes, sha256
`95e5ba419bb70a15addae365e683f12e304930470b019db179f8e8824f78e516` — all
four match the block's table exactly. Lines beginning `Gate: F263 R6 — `
at C2: 1, matching. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: at base
`d59371c1`, 28 distinct; at C2 `3212ed8d`, 28 distinct; both set
differences empty — matching the block's reading of 28, 28, both empty
exactly. Then, in the primary checkout at C4: `python3 -m pytest -q
-p no:cacheprovider tests/docs/ tests/orchestration/test_human_change_one_path.py
tests/cli/test_golden_path.py` → `366 passed in 142.74s`, real exit 0.
`python3 -m ruff check .` → `All checks passed!`, real exit 0.

**G3 — the red proofs**: `git worktree add --detach
.remedy-wt/f263-r7-mut 7ef871ab`, real exit 0. `python3 -B
.remedy-wt/f263-r7-payloads/mutations.py .remedy-wt/f263-r7-mut` printed,
verbatim:

```
control_before REAL_EXIT=0
2 passed in 1.91s
m1_the_command_spells_its_own_absorption FROM count in apps/cli/commands/absorb_cmd.py: 1
m1_the_command_spells_its_own_absorption REAL_EXIT=1
FAILED tests/orchestration/test_human_change_one_path.py::test_absorb_is_called_from_absorb_job_alone
FAILED tests/orchestration/test_human_change_one_path.py::test_absorb_job_is_called_from_the_three_entrances_and_nowhere_else
2 failed in 1.94s
m1_the_command_spells_its_own_absorption restored byte-identical: True
m2_the_safe_point_leaves_the_path FROM count in packages/orchestration/pingpong_job.py: 1
m2_the_safe_point_leaves_the_path REAL_EXIT=1
FAILED tests/orchestration/test_human_change_one_path.py::test_absorb_job_is_called_from_the_three_entrances_and_nowhere_else
1 failed, 1 passed in 1.94s
m2_the_safe_point_leaves_the_path restored byte-identical: True
m3_the_apply_leaves_the_path FROM count in packages/orchestration/job_apply.py: 1
m3_the_apply_leaves_the_path REAL_EXIT=1
FAILED tests/orchestration/test_human_change_one_path.py::test_absorb_job_is_called_from_the_three_entrances_and_nowhere_else
1 failed, 1 passed in 1.93s
m3_the_apply_leaves_the_path restored byte-identical: True
control_after REAL_EXIT=0
2 passed in 1.91s
```

Matching the block's stated reading exactly: both controls `2 passed`
exit 0; m1 2 failed, m2 1 failed, m3 1 failed, each at exit 1; every FROM
count 1; every restore byte-identical True. Then `git worktree remove
--force .remedy-wt/f263-r7-mut` real exit 0, `git worktree prune` real
exit 0, `git worktree list` after: primary checkout plus the three
pre-existing `.remedy-wt/job-*` worktrees only (`09441a92`, `cc8696a3`,
`03d435e5`) — no leftover mutation worktree.

**G4 — the self-use item and the tree**: `generate_and_append_if_empty()`
appended `SU-029`, "Address ledger finding R-1000", provenance `generated
(self-use-generator tier 1, ledger scan, R-1000)` — matching the
reviewer's dry-run reading exactly. `next_self_use_item()` answered the
same entry. `run_next_self_use_item(".remedy-wt/f263-r7-selfuse")`
answered entry id `SU-029`, job id `6a38b3203cca4928`, job file path
`.remedy-wt/f263-r7-selfuse/SU-029.md`, job state `blocked`.
`execution_config`: builder `claude-cli` model `claude-sonnet-4-6`
(source `cli`), reviewer `claude-cli` model `claude-sonnet-4-6` (source
`cli`) — the `self_use` role's configured provider, never `fake`.
`describe_self_use_run_defects(result)` verbatim:
`('job 6a38b3203cca4928 (blocked): task_T001_gate_failed:
final_status=provider_unavailable; missing_reviewer_output', 'T001
(blocked): completion_gate_failed: final_status=provider_unavailable;
missing_reviewer_output')` — the job's own `job show` confirms the root
cause: `final_status_detail: "provider_error: RuntimeError: claude CLI
timed out after 120s"`, a real provider-call timeout, not a
misconfiguration (never `fake`). `human_change_checks.txt`, two lines:
`{"count": 9, "max_seconds": 0.232568, "total_seconds": 1.974307}` then
`[]` (no intact human-change record exists for this job — it blocked
before any safe point produced one). `python3 -m pytest tests/docs/ -q`
after the queue file was written: `322 passed in 87.43s`, real exit 0.
`git branch --list 'remedy/job-*'`: 40 before C1, 41 after C5 (one new
branch, `remedy/job-6a38b3203cca4928`, from the self-use run — not
deleted, per constraint 7). `git worktree list` before C1: primary +
3 job worktrees (`09441a92`, `cc8696a3`, `03d435e5`); after C5: primary +
4 job worktrees (those three plus `job-6a38b3203cca4928` at `aab638e2`).
Then, still at C5 and before the UI build: `python3 -m apps.cli.main
integrity check --json` — all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) `pass`, `fail_count: 0`, `ok: true`, real exit 0.
`git status --porcelain` empty, no untracked file (closure precondition
3 met).

**G5 — the integration gate**: `npm --prefix apps/ui run build` last line
`✓ built in 1.50s`, real exit 0 (`PIPESTATUS[0]`); `git status
--porcelain` empty after it. `python3 -m pytest -n auto -q` in the
primary checkout: real exit 1; summary line `1 failed, 18692 passed, 20
skipped, 1 warning in 346.85s (0:05:46)`; the one bad node id
`tests/orchestration/test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogicalIdentity::test_different_execution_identities_same_logical_hash`
(assertion that two real runs' `logical_input_sha256()` match; they did
not). All committed verbatim to `.agent/authored/f263-closure-suite.txt`
alongside this handback. Neither `tests/orchestration/test_import_reachability.py`
nor `tests/test_no_orphan_modules.py` holds a bad node id in this run
(closure precondition 7 unaffected).

## Authored-text proofs

- `.agent/authored/f263-r7-block.md` (C1) == `.remedy-wt/f263-r7-block.md`: byte-identical True (sha256 `77f3c37140e4b33e813c5a5272ff3949606a568cae9d7e11c48dc18cb97ab021`, 212 lines, 15034 bytes).
- `.agent/authored/f263-r7-built_state.md` (C1) == `.remedy-wt/f263-r7-payloads/built_state.md`: byte-identical True (4666 bytes).
- `.agent/authored/f263-r7-ledger.md` (C1) == `.remedy-wt/f263-r7-payloads/ledger.md`: byte-identical True (2444 bytes).
- `.agent/authored/f263-r7-plan.md` (C1) == `.remedy-wt/f263-r7-payloads/plan.md`: byte-identical True (1300 bytes).
- `.agent/authored/f263-r7-test_human_change_one_path.py` (C1) == `.remedy-wt/f263-r7-payloads/test_human_change_one_path.py`: byte-identical True (2752 bytes).
- `.agent/authored/f263-r7-mutations.py` (C1) == `.remedy-wt/f263-r7-payloads/mutations.py`: byte-identical True (2436 bytes).
- `.agent/live_review.md` at C2 == pre-C2 bytes + `ledger.md` payload:
  byte-identical True (sha256 matches the block's table).
- `.agent/plan.md` at C2 == `plan.md` payload verbatim (rewrite): byte-identical True.
- `tests/orchestration/test_human_change_one_path.py` at C3 ==
  `test_human_change_one_path.py` payload (new file via
  `shutil.copyfile`): byte-identical True.
- `docs/roadmap/features/T2_F263.md` at C4 == pre-C4 bytes +
  `built_state.md` payload: byte-identical True.
- Every payload was applied with `shutil.copyfile` (whole-file copies) or
  a plain binary append (`ledger.md`, `built_state.md`); none was edited
  or retyped.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 431 insertions, matches block formula (212+219) exactly |
| C2 | done | 2/13 insertions, matches block exactly; G2 fully passed |
| C3 | done | 60 insertions, matches block exactly |
| C4 | done | 67 insertions, matches block exactly |
| C5 | done | 92 insertions total; self-use item generated and run to the approval gate (blocked on a provider timeout, an outcome to record) |
| C6 | done | this handback; full suite RED with one unrelated bad node, recorded per constraint 4 |
| G1 | done | all readings match |
| G2 | done | all readings match; open-set 28 at base and at C2, both differences empty |
| G3 | done | all readings match the block's table exactly |
| G4 | done | self-use item/run readings all captured; `tests/docs/` 322 passed exit 0; integrity check all-pass exit 0; tree clean |
| G5 | done | UI build exit 0; full suite exit 1, one bad node (unrelated to F263's own code), summary line and node id committed |
| T001-T003 | done | already landed before this round; this round adds the one-path guard, Built State, self-use evidence and the full-suite run on top |

## Deviations & assumptions

1. The full-suite log could not be written to
   `~/remedy-gate-scratch/f263-r7-full-suite.log`: the sandbox refused
   `mkdir` outside `/home/decodeux/Repos/remedy` ("For security, Claude
   Code may only create directories in the allowed working directories
   for this session"). Per the block's own fallback clause, it was
   written under `.remedy-wt/f263-r7-worker/f263-r7-full-suite.log`
   instead, and this substitution is stated here.
2. The full suite (G5) is RED: one failing node,
   `tests/orchestration/test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogicalIdentity::test_different_execution_identities_same_logical_hash`.
   This is unrelated to any file F263 touched this round or any prior
   round (F263's own files are untouched by this failure's assertion,
   which compares two real jobs' `logical_input_sha256()`). Per
   constraint 4, this is F263's work to repair in a later round, not a
   reason to stop; the transcript, exit code and node id are committed
   exactly as measured in `.agent/authored/f263-closure-suite.txt`. No
   assertion was weakened, no test deleted, nothing marked xfail.
3. The self-use run (C5) ended `blocked`, not `completed`: task T001's
   `claude CLI timed out after 120s` on its review call
   (`final_status_detail`, read via `job show`). This is a real
   provider-call outcome (`execution_config` shows `claude-cli`/
   `claude-sonnet-4-6` throughout, never `fake`), and the block states a
   blocked or stopped job is "an outcome to record, not a reason to
   stop." Recorded verbatim in `.agent/selfuse_f263/run_defects.txt`
   and `result_state.txt`; no registration was written (the reviewer's
   to author next round, per the block).
4. `run_next_self_use_item` left worktree `.remedy-wt/job-6a38b3203cca4928`
   and branch `remedy/job-6a38b3203cca4928` behind (`cleanup_status:
   "retained"`, since the job never reached an apply). Reported per
   constraint 7; not deleted, since it is the runner's own artifact and
   not scratch this worker created, and branches are never deleted.
5. No other departure from the block's ordered commit sequence: bytes
   verified before use, the six-commit bundle landed in order
   C1-C2-C3-C4-C5-C6, no payload was edited or retyped, G1 through G5 all
   ran and every reading matched the block's stated expectation except
   the two items named above (both explicitly anticipated by the block's
   own constraints). No worktree, branch or stash was touched beyond
   what G3 and C5 required; the three pre-existing `.remedy-wt/job-*`
   worktrees and their branches were left untouched. No commit of this
   round touched `docs/roadmap/STATUS.md`, root `README.md`, or any
   `consumed_by` field. This round is SESSION 2 of F263.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
7 by the reviewer, then the closure sequence's second half: the
registrations the self-use run's defects ask for (the T001 provider
timeout) and any repair the full suite requires (the
`test_run_manifest_logical_identity` failure), then the evidence job and
the review package, and then the closing round — the ledger rotation,
the STATUS line with the README counters in the same commit, and the
pull request. Open findings count: 28 (unchanged from `d59371c1`).
Operator-questions count: 0.
