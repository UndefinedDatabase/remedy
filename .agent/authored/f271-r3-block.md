-- STEP R3 T002 + R-0982 -- F271 No more legacy: ownership, reachability, replace-is-delete --
Session 1 of F271 · round 3 · base `8bacb0fc` (branch `feature/f271-no-more-legacy`).

Goal: book round 2's verdict and resolve R-0982 by deleting `patch_revert.py`, then land T002 —
the planted-dead-command tests for `doctor core` and closure precondition 7 — DECISION F271 D3.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F271.md; the payload `decisions.md`
(DECISION F271 D3 — this round's spec). The code and the doc text of C2 to C4 are ALREADY
AUTHORED as `.remedy-wt/f271-r3/prototype_final.diff` (a staged diff against `8bacb0fc` built and
run by a research helper and re-run by the reviewer). Read it in full; apply it, split across C2
to C4 as below, and change nothing in it — a defect you find in it is reported, not repaired.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f271-r3/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 e8f54864edc091340b469a182e7c953eb1562850d04bb2d5636d098c624cf792
  ledger.md            sha256 4897747e2fdd6eb367a40d036d32432898131109c1f7bfaf196446ea1e88e896
  decisions.md         sha256 5e937e42fa59ae156ae16067528b85a3866a5fcff57ec8e2b80ae497455de315
  prototype_final.diff sha256 63ba2a7f916f0203cb5bcd841b3b4757e631a54e4200ea9d3b4278dd1362ef00
  block.md             this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of plan.md, ledger.md, decisions.md and
   block.md as `.agent/authored/f271-r3-<name>`; `.agent/plan.md` := plan.md;
   `.agent/live_review.md` := its `8bacb0fc` bytes + ledger.md bytes (it books the F271 R2 gate
   entry and `Done: R-0982`); `.agent/decisions.md` := its `8bacb0fc` bytes + decisions.md bytes.
C2 R-0982 deletion — the prototype's hunks for `packages/orchestration/patch_revert.py` (deleted),
   `tests/orchestration/test_source_apply.py`, `tests/test_no_orphan_modules.py` and
   `scripts/remedy_smoke.sh`.
C3 T002 doctor — the prototype's hunks for `tests/cli/test_worker_facade_cmd.py` and
   `apps/cli/commands/worker_facade_cmd.py` (a comment only).
C4 T002 precondition 7 — the prototype's hunk for `docs/roadmap/STATUS_closure_protocol.md`.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F271 · round 3 · rounds so far 3" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output; open findings by distinct id, measured on the committed ledger; `## Next` naming
   Phase 1 rule 1 then the review of round 3, and "Operator questions open: <the count you read
   from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. Do-not-touch (T2_F271.md): the reachability allowlist, the dead-model check, the catalog's
   command set; no production code other than the one comment and the deleted module.
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python.
4. Never weaken an assertion or delete a test to pass, other than the deletions D3 (3) orders. A
   red gate or an ambiguity D3 does not settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show 8bacb0fc:<path>` bytes.
6. Commit messages "F271 R3 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
7. ORDER: C2, the deletion that resolves R-0982, is the first commit after C1, as the `Done:`
   paragraph of ledger.md states.

Done when (G1 to G5 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` equals its `8bacb0fc` bytes +
   ledger.md, that `.agent/decisions.md` equals its `8bacb0fc` bytes + decisions.md, and that
   each `.agent/authored/f271-r3-*` copy equals its payload.
G2 the change is the prototype: `git diff --binary 8bacb0fc <C4> -- . ':!.agent' | git patch-id
   --stable` prints the same first field as `git patch-id --stable < prototype_final.diff` (the
   reviewer read `0122492bf6ec20f8acd3ad95e1aeb2542cb51b85` from the latter); and per commit,
   `git show --numstat --format=` of C2, C3 and C4 lists exactly the paths the Bundle gives it.
G3 `python3 -m pytest -q -p no:cacheprovider tests/test_no_orphan_modules.py
   tests/orchestration/test_source_apply.py tests/orchestration/test_project_brain.py
   tests/orchestration/test_change_set.py tests/test_remedy_smoke_script.py
   tests/cli/test_worker_facade_cmd.py tests/orchestration/test_dead_command_check.py
   tests/orchestration/test_import_reachability.py tests/test_imports.py
   tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py tests/docs/` → summary
   line, 0 failed (serial, no `-n`), run with `git status --porcelain` empty; and
   `bash -n scripts/remedy_smoke.sh` exit 0.
G4 `python3 -m ruff check apps/cli/commands/worker_facade_cmd.py tests/cli/test_worker_facade_cmd.py
   tests/orchestration/test_source_apply.py tests/test_no_orphan_modules.py` → "All checks
   passed!"; `git grep -n -e "orchestration.patch_revert" -e "orchestration import patch_revert"
   -e revert_patch_intent -e store_pre_apply_snapshot -e PatchRevertResult -- . ':!.agent'
   ':!docs/roadmap'` → print its output literally; the only lines D3 accepts are the historical
   `store_pre_apply_snapshot()` sentence of `docs/system/snapshot-rollback-v1.md` and the two
   `_cmd_revert_patch_intent` lines of `apps/cli/commands/patch.py`, whose name only overlaps.
G5 red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from its root with
   `python3 -B -m pytest -q -p no:cacheprovider -rf tests/cli/test_worker_facade_cmd.py -k
   TestDoctorCoreDeadCommands`, `__pycache__` purged before each run, the imported
   `worker_facade_cmd` module path printed first; the UNMUTATED control first (exit 0); each
   change reverted before the next, each target line counted 1 in
   `apps/cli/commands/worker_facade_cmd.py` first: (a) the line `        "dead_commands": dead_commands,`
   becomes `        "dead_commands": [],` → the JSON planted test fails; (b) the line
   `        for cid in dead_commands:` becomes `        for cid in []:` → the text planted test
   fails. Then with `tests/orchestration/test_source_apply.py -k test_brain_has_patch_revert_node`:
   (c) in `packages/orchestration/project_brain.py` the line
   `        if ev.get("event") != "patch_intent_reverted":` (count it: 1) gets the event name
   `patch_intent_reverted_x` → that test fails. Report exit codes and failing ids; report a
   change that stays green as green. Remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
