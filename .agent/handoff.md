# Handoff — F290 Findings paydown v6, round 7 landed clean

## Session

SESSION 4 of feature F290 · round 7 · rounds so far 7

Context self-assessment: context is comfortable; round 7 ran its full ordered sequence — C1, C2
(the closure's self-use item, run through a real frontier-provider job to its approval gate and
never applied), both gates and C3 — with every gate green and the self-use job coming back
`completed`/`pass` with no run defects, so this handback carries the block's success-path content
in full rather than a stop.

Fortschritt: ~85 % (all seven findings resolved and hardened; the closure's self-use item run; the
suite, the evidence and the pull request open) — Schätzung

## Range

Review of `f5ea5713e`..`HEAD`: two commits on `feature/f290-findings-paydown-v6`, `cca0ff94e` and
`65c21907e`, and this handback commit.

## Commits

### `cca0ff94e` F290 R7 C1: book round 6, save the round 7 block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f290-r7.md` | +110/-0 | NEW FILE; byte-for-byte copy of this round's step block `.remedy-wt/f290-s7/block.md` (`wc -l` 110, sha256 `fe213234a72d8212b2e0a4883e0d724f66c2350b479d86844c661a15538cb12f`); byte comparison against the source read equal |
| `.agent/authored/f290-r7-selfuse.py` | +122/-0 | NEW FILE; byte-for-byte copy of `dry-f290-r7-selfuse.py` (reviewer-authored, adapted from `.agent/authored/f200-r10-selfuse.py` with only its paths changed); byte comparison equal |
| `.agent/live_review.md` | +2/-0 | appended the F290 R6 Gate entry (VERDICT PASS, covering round 6's two commits and closure preconditions 4/8); whole-file copy from `.remedy-wt/f290-s7/dry-live_review.md`; append-byte-equality proof (`git show f5ea5713e:.agent/live_review.md` bytes + `append-live_review.txt` bytes == new file, compared with Python `==` over bytes) read `True` |
| `.agent/plan.md` | +5/-5 | whole-file copy from `.remedy-wt/f290-s7/dry-plan.md`, advancing Current Step/Next Steps to round 7 (run the closure's self-use item to its approval gate) and adding the self-use cost risk |

`git diff --cached --numstat` before the commit read `122 0` for the script, `110 0` for the new
block file, `2 0` for `.agent/live_review.md` and `5 5` for `.agent/plan.md` — matching the block's
stated numbers exactly. `git show --numstat cca0ff94e` after the commit read the same four lines.

### `65c21907e` F290 R7 C2: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-044` (tier 4, excused handler `apps/cli/commands/dev.py:140`), `consumed_by` empty |
| `.agent/selfuse_f290/SU-044.md` | +13/-0 | NEW FILE; the job markdown the generator wrote (byte copy of the run's own job file) |
| `.agent/selfuse_f290/changed_paths.txt` | +2/-0 | NEW FILE; the job's changed paths |
| `.agent/selfuse_f290/entry_and_job_file.txt` | +5/-0 | NEW FILE; entry id/title/provenance/consumed_by and the job file path |
| `.agent/selfuse_f290/execution_config.txt` | +39/-0 | NEW FILE; the plan's execution config |
| `.agent/selfuse_f290/full_transcript.txt` | +14/-0 | NEW FILE; job id/title/state, stop reason/source, execution, task summary |
| `.agent/selfuse_f290/job_diff.txt` | +27/-0 | NEW FILE; `git diff HEAD...remedy/job-b30005533dd74be8` |
| `.agent/selfuse_f290/result_state.txt` | +12/-0 | NEW FILE; job/task state, budgets and budget actuals |
| `.agent/selfuse_f290/run_defects.txt` | +1/-0 | NEW FILE; `describe_self_use_run_defects()` output |
| `.agent/selfuse_f290/staleness_after.txt` | +2/-0 | NEW FILE; post-run staleness catalog, read from the job branch |
| `.agent/selfuse_f290/timing.txt` | +3/-0 | NEW FILE; start/finish timestamps and wall seconds |

`git diff --cached --numstat` before the commit matched the eleven lines above exactly.
`git show --numstat 65c21907e` after the commit read the same eleven lines. `git status --porcelain`
immediately after the run and before staging showed only `scripts/self_use_queue.json` modified and
`.agent/selfuse_f290/` untracked, matching the block's required reading; `git diff
scripts/self_use_queue.json` showed exactly one appended entry, id `SU-044` (the id
`next_self_use_item()` printed), `consumed_by` empty.

### this commit — F290 R7 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; documents round 7 landing clean through C1, C2 (the self-use run) and all five gates |

## External actions

- This commit is pushed with `git push origin feature/f290-findings-paydown-v6` immediately after
  it is made.
- No worktree add/remove issued directly by the worker this round; the reviewer's prepared files
  were read from the existing `.remedy-wt/f290-s7/` directory. The self-use runner's OWN code (not
  a worker-issued command) performed one internal `git worktree add --detach
  .remedy-wt/f290-r7-jobtree remedy/job-b30005533dd74be8`, read the job branch's staleness catalog,
  then `git worktree remove --force` and `git worktree prune`, all inside the single run of
  `.agent/authored/f290-r7-selfuse.py`; `git status --porcelain` after the run showed no stray
  worktree state. Scratch helper files were written under `.remedy-wt/f290-r7-worker/` (gitignored,
  newly created this round).
- No pull request was checked, opened, or merged this round: the block names no such step and
  forbids opening one.

## Verification

Gates run once each, after C2 and before C3, in the block's order.

Gate 1 — `git status --porcelain`, then a byte comparison of the four reviewer-authored files
against their committed copies:

    $ git status --porcelain
    (no output)

    $ python3 gate1_cmp.py
    f290-r7.md vs block.md : SILENT(equal)
    f290-r7-selfuse.py vs dry-f290-r7-selfuse.py : SILENT(equal)
    live_review.md vs dry-live_review.md : SILENT(equal)
    plan.md vs dry-plan.md : SILENT(equal)
    ALL_OK: True

Gate 1: GREEN.

Gate 2 — the files under `.agent/selfuse_f290/`, listed with byte size:

    $ python3 gate2_list.py
    SU-044.md 948
    changed_paths.txt 54
    entry_and_job_file.txt 395
    execution_config.txt 1203
    full_transcript.txt 1416
    job_diff.txt 1211
    result_state.txt 801
    run_defects.txt 5
    staleness_after.txt 59
    timing.txt 105

Gate 2: GREEN — ten files, each non-empty, exactly the names the block lists.

Gate 3 — `python3 -B -m pytest tests/cli/test_golden_path.py tests/docs/ -q -n auto
-p no:cacheprovider`, from the primary checkout:

    exit 0
    bringing up nodes...
    ........................................................................ [ 19%]
    ........................................................................ [ 38%]
    ........................................................................ [ 58%]
    ........................................................................ [ 77%]
    ........................................................................ [ 96%]
    ............                                                             [100%]
    372 passed in 16.20s

Gate 3: GREEN — no FAILED or ERROR line, no "process(es) behind" line; `372 passed` matches the
reviewer's dry-tree reading exactly. Run once, not re-run.

Gate 4 — `python3 -m apps.cli.main integrity check --json`, from the primary checkout:

    exit 0
    {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}

Gate 4: GREEN — `fail_count` 0.

Gate 5 — `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:

    exit 0
    ['R-1138']

Gate 5: GREEN — matches the required `['R-1138']` exactly.

## Self-use run

- Entry id: `SU-044`.
- Title: "Narrow the excused handler at apps/cli/commands/dev.py:140".
- Job id: `b30005533dd74be8`.
- Builder: provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`).
- Reviewer: provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`) — the
  `self_use` role's configured frontier provider on both seats, not the local model.
- Job state: `completed`. Stop reason: (empty). Stop source: (empty).
- Task statuses and reviewer verdict (from `result_state.txt`):
  `T001: applied_to_job_workspace (verdict: pass; final_status: staged_review_passed;
  repair_rounds_used: 2; run_id: fd5b96c30e0b44b5)`.
- Wall seconds (from `timing.txt`): `423.7`.
- Changed paths (from `changed_paths.txt`): `apps/cli/commands/dev.py`,
  `tests/test_ble001_ratchet.py`.
- Job diff (from `job_diff.txt`), VERBATIM:

```
$ git diff HEAD...remedy/job-b30005533dd74be8  (exit 0)
diff --git a/apps/cli/commands/dev.py b/apps/cli/commands/dev.py
index 426b70ad4..00361ff39 100644
--- a/apps/cli/commands/dev.py
+++ b/apps/cli/commands/dev.py
@@ -137,7 +137,7 @@ def _dev_status(*, json_output: bool = False) -> None:
     try:
         from packages.orchestration.ui_server import _build_live_state_json
         status["live_ui_ok"] = callable(_build_live_state_json)
-    except (ImportError, Exception):  # noqa: BLE001 — a live-UI check failure must not block other checks
+    except (ImportError, AttributeError):
         status["live_ui_ok"] = False
 
     # Remaining blockers (hard failures) vs advisories (informational)
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index 86e75f777..ff1f68ae3 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 286
+MAX_EXCUSED = 285
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

- `run_defects.txt`, VERBATIM:

```
NONE
```

No finding is registered by this round for the self-use run: `describe_self_use_run_defects()`
returned an empty tuple (rendered as `NONE`), so there is nothing to mint an id for. The job's own
change lives on `remedy/job-b30005533dd74be8` only and was never applied to this branch.

## Authored-text proofs

- `.agent/authored/f290-r7.md` vs `.remedy-wt/f290-s7/block.md`: byte comparison equal; `wc -l` 110,
  sha256 `fe213234a72d8212b2e0a4883e0d724f66c2350b479d86844c661a15538cb12f` on both readings (the
  prompt-delivered digest and the post-copy re-measurement).
- `.agent/authored/f290-r7-selfuse.py` vs `dry-f290-r7-selfuse.py`: byte comparison equal; sha256
  `97e540e7fdd9da4ef9f29252940e03818763f65dc4ec37ff7b33aa47188b6a7c` on both readings.
- `.agent/live_review.md` vs `dry-live_review.md`: byte comparison equal; sha256
  `07d11ae084af5ccb265cc292da99d6594d531dc39217b13f8cfaa1ac8c2715e6` on both readings.
  Append-byte-equality proof (base bytes at `f5ea5713e` plus `append-live_review.txt` bytes equals
  the new file, compared with Python `==` over bytes) read `True`.
- `.agent/plan.md` vs `dry-plan.md`: byte comparison equal; sha256
  `eb7484b4f0fa0e7ea46c97f5828c96b7bdc10eaeabc69d6eaa07c71b1230fabe` on both readings (whole-file
  copy, no append proof applicable).
- Gate 1's four-way re-check (above) confirms all four committed files still match their prepared
  files bit-for-bit after the C1 commit.
- `.agent/selfuse_f290/SU-044.md` is a byte copy (`Path(job_file_path).read_bytes()` written
  verbatim by the reviewer-authored script itself) of the job file the generator produced; not a
  worker-typed text, so no separate disk-to-disk proof is owed beyond the script's own write, which
  is reviewer-authored and run unedited exactly once.

## Deviations & assumptions

1. This session's auto-attached working directory was again a separate worktree
   (`.remedy-wt/f290-r4-dry/apps/ui`), unrelated to this round's work. It was never read from or
   written to: every command in this round ran against `/home/decodeux/Repos/remedy` directly, by
   absolute path or `git -C`, consistent with the block's own rule never to `cd` immediately before
   a git command. Recorded here as an operating assumption, not a departure from the block's
   ordered commit sequence.
2. `python3 .agent/authored/f290-r7-selfuse.py` (C2's run) and the two non-git gates (`apps.cli.main
   integrity check` and the `rotate_live_review` import) were run with a plain `cd` to the primary
   checkout rather than `git -C`, since none of them is a version-control command and the sandbox
   only refuses `cd` immediately before a git command. The self-use script was run exactly once, did
   not raise, and its stdout was captured in full for this handback; it is not re-run.
3. The self-use script's own internal staleness read fell to the "job branch" path rather than the
   "job workspace" path (`staleness_after.txt` reads "Read from: the job branch
   remedy/job-b30005533dd74be8"), because the runner had already removed the job's workspace
   directory by the time the script reached that step even though `result_state.txt` still names
   `Job Workspace: /home/decodeux/Repos/remedy/.remedy-wt/job-b30005533dd74be8` as the path it was
   built at. This is the script's own documented fallback (see its `_stale_lines`/branch-check
   logic), not a worker action or a defect; it is recorded here because it is the kind of reading
   DECISION/precedent text asks a later reader to be able to find.
4. No other deviation from the block's ordered commit sequence (C1, C2, five gates, C3) or from its
   stated paths, numbers, or gate commands. Exactly three commits landed, matching "one records
   commit, one self-use commit, one handback commit" (SLOW MODE).

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate).
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 7's verdict and register every self-use defect in the next round's first commit.
5. The integration gate: the one full suite.

Operator questions open: 1.
Open findings: 1 (R-1138 Low, owned by the next paydown).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 6, save the round 7 block and the self-use script | done | commit `cca0ff94e`; numstat matched the block's stated numbers exactly |
| C2: the closure's self-use item run to its approval gate, never applied | done | commit `65c21907e`; job `b30005533dd74be8` completed, verdict pass, no run defects, never applied |
| Gate 1 (status + four-way byte comparison) | done, GREEN | all four comparisons silent/equal |
| Gate 2 (`.agent/selfuse_f290/` file listing) | done, GREEN | ten files, each non-empty |
| Gate 3 (pytest selection) | done, GREEN | `372 passed` |
| Gate 4 (integrity check) | done, GREEN | `fail_count` 0 |
| Gate 5 (`open_finding_ids`) | done, GREEN | `['R-1138']` |
| C3: handback | done | this commit |
| Push | pending | `git push origin feature/f290-findings-paydown-v6` runs immediately after this commit |
