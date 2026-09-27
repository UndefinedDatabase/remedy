# Handoff — F029, round 7

## Session

SESSION 2 of feature F029 · round 7 · rounds so far 7. Context remaining at
handback: comfortable — reading the model live-e2e file, the prepare test's
fixture and S5 section, `RunDetailPopover.tsx`/its CSS, `subtree_rerun.py`'s
three named functions, the CLI door and command wiring, `run_report.py`'s
attempt clause and the data-path/run-log helpers, then drafting and running
S1, S2 and the mutation tool took most of it; one tool bug was found and
fixed within the round (below), every gate ran clean afterward, and there was
ample context left had a further repair round been needed.

## Range

Review of `cfd779c64`..`HEAD` (`HEAD` is this handback's own commit, `F029 R7
C6`, on `feature/f029-subtree-rerun`).

## Commits

### d0b547815 F029 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r7-block.md | 240/0 | copy of this round's block |
| .agent/authored/f029-r7-booking.diff | 19/0 | copy of the booking diff payload |
| .agent/authored/f029-r7-plan.md | 35/0 | copy of the plan payload |

Measured insertions: 294 (block's own line count 240 + 54), matching the
block's expectation exactly, under the 500-line cap.

### aabc2a2bc F029 R7 C2: book round 6 and its prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | round 6's Gate entry appended |
| .agent/plan.md | 12/10 | rewrite from the plan payload |
| .agent/prose_slips.md | 1/0 | round 6's owed prose slip appended |

Matches the block's expected numstat (2/0, 12/10, 1/0) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of `booking.diff`,
followed by the `plan.md` rewrite via `shutil.copyfile`.

### 7621ba772 F029 R7 C3: give the run detail's confirmation row its space
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/RunDetailPopover.module.css | 6/0 | S1: new `.confirmActions { display: flex; gap: 8px; margin: 8px 0 0; }` rule directly after `.actions` |
| apps/ui/src/components/graph/RunDetailPopover.tsx | 1/1 | S1: the `needs_confirmation` actions `<div>` takes `styles.confirmActions` instead of `styles.actions`; the first actions row keeps `styles.actions` |

7 total insertions/1 deletion, under the 500-line cap; no split needed.

### 393b26d2b F029 R7 C4a: prove a subtree rerun end to end through the write door
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_subtree_rerun_e2e_live.py | 436/0 | S2 (new file): docstring naming DECISIONS F029 D1-D6, the own-copy helpers from `test_task_injection_e2e_live.py` (`_start_ui_server_for_job`, `_post`, `_job_data`, `_get_json`, `_by_planned`, `_all_events_since`, `_report_markdown`), the new helpers (`_git`, `_make_repo`, `_task`, `_save_approved_three_task_job`, `_sha256_tree`, `_run_log_subtree_rerun_prepared_events`), and `test_the_door_path_reruns_a_middle_task_end_to_end` |

**Split from the block's single C4**, declared below: the whole file measured
502 insertions before committing, 2 over the 500-line cap. Split by test
method exactly as constraint 2 orders — C4a (helpers + test (a), 436
insertions) and C4b (test (b), 66 insertions) — each measured before
committing, each leaving the file's collected tests passing (1 test collected
and green at C4a; 2 collected and green at C4b).

### c16806bec F029 R7 C4b: prove a subtree rerun through the command line
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_subtree_rerun_e2e_live.py | 66/0 | S2: `test_the_command_line_path_reruns_with_yes` |

66 total insertions, under the 500-line cap; the second half of C4's split
(see C4a above). 436 + 66 = 502, the file's own full line count.

### 76b5afdfa F029 R7 C5: add the round 7 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r7-mutations.py | 223/0 | the G5 mutation (red-proof) tool, covering m1-m4 across `pingpong_job.py`, `ui_server.py`, `run_report.py` and `subtree_rerun.py`, one pytest route against the new e2e file |

### add1a61d9 F029 R7 correction: fix the mutation tool's failed-count parser
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r7-mutations.py | 5/8 | `_failed_count_and_names` only matched a summary line shaped "N failed, M passed in Xs" or one bare-ending in "failed"; a run where every collected test failed prints "N failed in Xs", matching neither clause and silently reading `failed=0` — m3 and m4 misreported as `GREEN, NOT CAUGHT` although both genuinely reddened the suite (exit 1, 2 failed each). Replaced with a count of the distinct `FAILED` node-id lines — see Deviations |

### (this commit) F029 R7 C6: rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file |

## External actions

`git worktree add --detach .remedy-wt/f029-r7-mut 76b5afdfa` (first attempt,
at C5 literally) — m3 and m4 both genuinely reddened the suite (exit 1, 2
failed) but the tool's own parser read `failed=0` for both and reported them
`GREEN, NOT CAUGHT` (tool bug, see Deviations); removed with `git worktree
remove --force .remedy-wt/f029-r7-mut` then `git worktree prune` before
fixing the tool. After the correction commit: `git worktree add --detach
.remedy-wt/f029-r7-mut add1a61d9`, ran the tool (all 4 mutations caught, see
G5 below), then `git worktree remove --force .remedy-wt/f029-r7-mut` and
`git worktree prune`. `git worktree list | wc -l` read 62 before the first
add and 62 after the final remove, matching the step-4 reading throughout.
`git push origin feature/f029-subtree-rerun` — its real outcome is reported
to the delegator, since C6 cannot contain it. No PR opened, no merge, no
branch deleted, no force-push, no stash.

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty;
  `git branch --show-current` → `feature/f029-subtree-rerun`; `git log
  --oneline -1` → `cfd779c64`.
- Block bytes (R-0954): measured 240 lines, sha256
  `cdc5c160dfab23bdb8b1a4f895291f6aa04ec6285d363451b1e643327323ee72` — both
  match the delegation message's readings exactly.
- `git worktree list | wc -l` → 62.

**PAYLOADS** — both matched the table exactly:
`booking.diff` 19 lines / 10507 bytes /
`0b11f442f40785e3bf0b0a794351620fc7c196dd13e44d49cf44d61943f57717`;
`plan.md` 35 lines / 1369 bytes /
`09426a6990397d3192aa3edfa8579d9394ff22dda437a8d26c29dc04886b58b9`.

**G1 TRANSPORT** — each `.agent/authored/f029-r7-*` copy read via `git show
d0b547815:<path>` equals its source byte for byte: block copy == source
(True, sha256 `cdc5c160...7323ee72`); booking.diff copy == source (True,
sha256 `0b11f442...43f57717`); plan.md copy == source (True, sha256
`09426a69...886b58b9`).

**G2 THE RECORDS** — sha256 of each file read via `git show aabc2a2bc:<path>`
equals the reviewer's reading exactly:
`.agent/live_review.md` 329576 bytes,
`7b9e2a2b0a6b5103ad1eafebdf98808ad2f0e2ccf813a9e36ee245ab5ffa230b` — match.
`.agent/plan.md` 1369 bytes,
`09426a6990397d3192aa3edfa8579d9394ff22dda437a8d26c29dc04886b58b9` — match.
`.agent/prose_slips.md` 374248 bytes,
`16e2ef58281e8cfd5b1d5de8dac99d824a9ad8781d778928d184b6240c67853e` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s
text: at `cfd779c64` → `[]`; at `aabc2a2bc` → `[]` — both match the reviewer's
stated readings. `git diff --name-only d0b547815 aabc2a2bc` → exactly the
three paths of the table, nothing else.

**G3 THE CODE** —
```
python3 -m ruff check tests/ui_server/test_subtree_rerun_e2e_live.py
```
→ `All checks passed!`, exit 0 (run at C5, `76b5afdfa`, and unaffected by the
correction commit, which touches only the mutation tool). Quoted from the
diff (matches what is committed at HEAD):

S1, `RunDetailPopover.module.css`:
```css
.confirmActions {
  display: flex;
  gap: 8px;
  margin: 8px 0 0;
}
```

S1, `RunDetailPopover.tsx`:
```diff
-        <div className={styles.actions}>
+        <div className={styles.confirmActions}>
```

S2 step 4 (`test_subtree_rerun_e2e_live.py`):
```python
        status, body = _post(port, token, "job.rerun-subtree", job_id=job_id,
                             nonce="n-rerun-2",
                             args={"task_id": b_id, "model": MODEL_M, "confirm_cost": True})
        assert status == 200, body
        assert body["outcome"] == "prepared", body
        assert body["root_task_id"] == b_id, body
        assert body["subtree"] == [b_id, c_id], body
        assert body["exact"] is True, body
        assert body["pre_task_tree_equal"] is True, body
        assert body["model"] == {
            "override": MODEL_M, "configured": "", "reason": "human_override"}, body
        run_command = f"remedy job run {job_id}"
        assert body["run_command"] == run_command, body
```

S2 step 5 (`test_subtree_rerun_e2e_live.py`):
```python
        assert _git(repo, "rev-parse", f"{b_commit_1}^").strip() == base_commit
        assert (_git(repo, "rev-parse", f"{reset_commit}^{{tree}}").strip()
               == _git(repo, "rev-parse", f"{base_commit}^{{tree}}").strip())
        job_branch = _job_data(data_dir, job_id)["worktree"]["branch"]
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", b_commit_1, job_branch],
            cwd=str(repo), capture_output=True, text=True)
        assert ancestor.returncode == 0, ancestor.stderr
```

S2 step 10 (`test_subtree_rerun_e2e_live.py`):
```python
        from packages.orchestration.pingpong_loop import load_run

        b_run_2 = load_run(new_b2["run_id"])
        assert b_run_2["provider_evidence"]["builder_configured_model"] == MODEL_M
        c_run_2 = load_run(new_c2["run_id"])
        assert c_run_2["provider_evidence"]["builder_configured_model"] == MODEL_M

        b_run_1 = load_run(b_run_id_1)
        assert b_run_1["provider_evidence"]["builder_configured_model"] != MODEL_M

        after_hashes = _sha256_tree(run_dir(b_run_id_1, data_dir))
        assert after_hashes == before_hashes
```

**G4 THE TESTS** — the exact selection, serially, real exit code:
```
python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_subtree_rerun_e2e_live.py tests/ui_contracts tests/orchestration/test_run_report.py tests/ui_server/test_rerun_subtree_door.py tests/ui_server/test_dashboard_task_attempts.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_view_model.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
```
Run at C5 (`76b5afdfa`; unaffected by the later tool-only correction):
`1698 passed, 11 skipped`, real exit code 0. All eleven `SKIPPED` lines cite
an F252 quarantine (four in `tests/ui_contracts/`, six in
`test_named_bugs.py`, one in `test_agent_tooling.py`) — the same eleven the
reviewer's own base reading at `cfd779c6` already carried. Accounting for the
difference from 1696: this round's own new file,
`tests/ui_server/test_subtree_rerun_e2e_live.py`, adds exactly 2 pytest nodes
(`test_the_door_path_reruns_a_middle_task_end_to_end` and
`test_the_command_line_path_reruns_with_yes`); S1's `.tsx`/`.css` edit is
exercised inside the single existing `TestVitestFrontendTestFoundation`
pytest node, so it adds no further node of its own. 1696 + 2 = 1698, exactly
the passed count above; no unexplained difference. Then `python3 -m
apps.cli.main integrity check --json` → all 6 checks `pass`
(`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`),
`fail_count: 0`, `ok: true`.

**G5 THE RED PROOFS** — first attempt, `git worktree add --detach
.remedy-wt/f029-r7-mut 76b5afdfa` (literally C5): both control runs green,
but m3 and m4 both printed `failed=0` and `GREEN, NOT CAUGHT` despite the
pasted pytest output showing `2 failed` and exit 1 for each — the tool's own
summary-line parser matched neither of its two recognized shapes against a
bare "N failed in Xs" line (see Deviations). Read `ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: False`, exit 1. Removed the worktree, fixed the tool
(commit `add1a61d9`, "F029 R7 correction: ..."), re-added the worktree at the
corrected HEAD: `git worktree add --detach .remedy-wt/f029-r7-mut
add1a61d9`, then `python3 -B .agent/authored/f029-r7-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r7-mut`:
```
packages.orchestration.subtree_rerun.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/f029-r7-mut/packages/orchestration/subtree_rerun.py
packages.orchestration.pingpong_job.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/f029-r7-mut/packages/orchestration/pingpong_job.py
both modules resolve inside the worktree: True
control: exit=0 failed=0
m1 a run ignores the model override: exit=1 failed=1 — test_the_door_path_reruns_a_middle_task_end_to_end
m2 the dashboard forgets the attempt: exit=1 failed=1 — test_the_door_path_reruns_a_middle_task_end_to_end
m3 the report drops the clause for a second attempt: exit=1 failed=2 — both tests
m4 the fold does not count the attempt: exit=1 failed=2 — both tests
restored byte-identical: True (pingpong_job.py, run_report.py, subtree_rerun.py, ui_server.py)
control (after): exit=0
git status --porcelain (primary checkout): '' (empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All four mutations were red on this (corrected) run; no repair round was
needed for the production code, only the tool bug fixed before this gate
passed. Then `git worktree remove --force .remedy-wt/f029-r7-mut`, `git
worktree prune`; `git worktree list | wc -l` → 62, matching the step-4
reading.

**Constraint 3** — `git diff --name-only cfd779c64`, run once more after
writing this file, lists exactly the block's tracked path set plus
`.agent/handoff.md` itself: `.agent/authored/f029-r7-block.md`,
`.agent/authored/f029-r7-booking.diff`, `.agent/authored/f029-r7-mutations.py`,
`.agent/authored/f029-r7-plan.md`, `.agent/handoff.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`apps/ui/src/components/graph/RunDetailPopover.module.css`,
`apps/ui/src/components/graph/RunDetailPopover.tsx`,
`tests/ui_server/test_subtree_rerun_e2e_live.py` — 11 paths in total; no path
outside the set changed.

## Authored-text proofs

`.agent/authored/f029-r7-block.md`, `f029-r7-booking.diff` and
`f029-r7-plan.md` (C1, `d0b547815`): each read back via `git show` equals its
source (`.remedy-wt/f029-r7/block.md`, `.remedy-wt/f029-r7-payloads/booking.diff`,
`.remedy-wt/f029-r7-payloads/plan.md`) byte for byte — see G1 above.
`.agent/authored/f029-r7-mutations.py` (C5, `76b5afdfa`, corrected at
`add1a61d9`) is this session's OWN tool, not reviewer-authored text, so it
carries no fidelity comparison; its behavior is proved instead by G5's live
run above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4a | deviated | split from the block's single C4 (constraint 2): the full file measured 502 insertions, 2 over the 500-line cap; split by test method — helpers + test (a) here |
| C4b | deviated | second half of the same split — test (b) here |
| C5 | done | |
| correction | done | fixed this round's own mutation-tool bug (failed-count misparse on a bare "N failed in Xs" summary line) before C6; declared below |
| C6 | done | this commit |
| G1 transport | done | PASS — all copies byte-identical |
| G2 the records | done | PASS — sha256 and open_finding_ids both match |
| G3 the code | done | PASS — ruff exit 0, S1 (both files) and S2 steps 4/5/10 quoted from disk |
| G4 the tests | done | PASS — 1698 passed, 11 skipped, exit 0; +2 nodes fully accounted; integrity check all 6 pass |
| G5 the red proofs | done | PASS (after the correction) — all 4 mutations caught, control green before/after, restored byte-identical |
| S1 the spacing | done | `RunDetailPopover.tsx`/`.module.css`: `confirmActions` class + rule, first actions row untouched |
| S2 the proof | done | `test_subtree_rerun_e2e_live.py`: door path (a) and command-line path (b), both attempts read back from the job record, git, the run log, the dashboard, the run records and the report |

## Deviations & assumptions

1. **C4 split into C4a/C4b** (constraint 2, the route the block itself
   anticipates). Measured before committing: the whole new file was 502
   insertions, 2 over the 500-line cap. Split by test method — C4a (the
   header, every helper, and `test_the_door_path_reruns_a_middle_task_end_to_end`,
   436 insertions) and C4b (`test_the_command_line_path_reruns_with_yes`, 66
   insertions) — each measured under the cap, each leaving the file's
   collected tests passing (1 collected and green at C4a; 2 collected and
   green at C4b, run via `python3 -m pytest -q -p no:cacheprovider
   tests/ui_server/test_subtree_rerun_e2e_live.py` both times) before
   committing.

2. **A tool bug found and fixed within the round** (constraint 4's
   correction allowance, read for this round's own tooling rather than a
   test it wrote, exactly as F029 R6 precedent reads it). This round's
   `_failed_count_and_names` recognized only a summary line shaped "N
   failed, M passed in Xs" (via the `passed` substring test) or one ending
   bare in the literal word "failed" with nothing after it; pytest's real
   summary line when EVERY collected test in the file fails prints "N
   failed in Xs" — neither clause matched, so the function silently
   returned `failed_count=0` even though the run's own exit code was 1 and
   its pasted output showed two distinct `FAILED` lines. The tool's
   "caught" check (`code != 0 and failed_count != 0`) then read that as
   `failed_count == 0` and printed `GREEN, NOT CAUGHT` for m3 and m4, both
   of which had genuinely reddened the suite. Fixed by counting the
   distinct `FAILED <node id>` lines directly instead of parsing the
   summary line's shape at all — that count is correct regardless of what
   else ran alongside it. Corrected in its own commit (`add1a61d9`) before
   re-running G5; no production file was touched by the fix, and re-running
   the (corrected) tool read all four mutations caught, matching what the
   raw pytest output already showed on the first attempt.

No commit was reordered or dropped from the block's ordered sequence beyond
the declared C4 split; no existing test was touched by this round at all
(S1 and S2 are additive/renaming-only, and S2 is a wholly new file); no gate
went red in its FINAL (post-correction) state.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 7
with the reviewer's headless render of the confirmation row, then the
closure sequence.

Open findings: 0. Operator questions: 0.
