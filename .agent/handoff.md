# Handoff — F110 Model routing by task class, round 16 (interrupted)

## Session

SESSION 6 of feature F110 · round 16 (recovery/continuation of a round
started in session 5) · rounds so far 16

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed at the C4 SHA
  this handback lands as. NO pull request open.
- Base of this recovery action: `cf0e00e9` (F110 R16 C2, session 5's last
  clean commit).
- Session 5 authored and delegated round 16's block (`.agent/last_block.md`,
  `.agent/authored/f110-r16.md`), and its worker completed C0a through C2
  cleanly, then began constraint 6's self-use step (C3): the self-use
  generator ran (`generate_and_append_if_empty()`, appending `SU-006` to
  `scripts/self_use_queue.json`) and the runner's planning phase wrote
  `.remedy-wt/selfuse-f110-run/SU-006.md`. Session 5 ended there — with NO
  handoff written — before constraint 6's remaining steps (defect capture,
  evidence copy with sha256 proof, `run.txt`, commit C3, commit C4) or any
  confirmation of the underlying job's terminal status.
- Session 6 (this one) found this at its Phase 0 state probe:
  `git status --porcelain` was NOT empty (`M scripts/self_use_queue.json`),
  violating the probe's stated precondition. Investigated rather than
  guessed: `.remedy-wt/selfuse-f110-run/SU-006.md` exists (the planned job
  markdown); job worktree `.remedy-wt/job-6f74dd7367704fd5` exists, branched
  from `cf0e00e9`, with ZERO commits ahead of that base; `.agent/selfuse_f110/`
  does not exist. This does not by itself prove the job run failed —
  F109 R19's precedent also retains its job worktree regardless of outcome —
  but it does not prove success either, and re-running
  `run_next_self_use_item()` or `generate_and_append_if_empty()` to find out
  risks double-generating a queue entry or double-executing a real
  builder/reviewer job (real provider calls, real cost). Per G8
  ("ambiguity ends the round... never guess, never widen scope to route
  around a block"), session 6 did NOT attempt to resume, complete, or
  re-run any part of constraint 6. It committed only the one confirmed,
  harmless side effect already on disk (the `SU-006` queue append) and
  writes this handback in its place, leaving `.remedy-wt/selfuse-f110-run/`
  and `.remedy-wt/job-6f74dd7367704fd5` exactly as found.
- `.agent/STOP` read from disk before this recovery action: ABSENT.
- `.agent/candidates.md` is EMPTY (unchanged, not touched).

## Range

Base `1d1a82e1` (F110 R15 C4) → head `5e6ab5c135f583f1d7f0626ec307d3de88436e9b` for the commits below.

## Commits

| # | SHA | Subject | Files | +/- |
|---|-----|---------|-------|-----|
| C0a | `0a4470d6` | F110 R16 C0a: save the round 16 block verbatim to authored | `.agent/authored/f110-r16.md` | (session 5) |
| C0b | `31020939` | F110 R16 C0b: mirror the committed authored file to last_block | `.agent/last_block.md` | (session 5) |
| C1 | `d6323046` | F110 R16 C1: apply PLAN16 to plan.md | `.agent/plan.md` | (session 5) |
| C2 | `cf0e00e9` | F110 R16 C2: book round 15's PASS verdict, DECISION F110 D6 and one prose slip | `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` | (session 5) |
| C3 | `5e6ab5c135f583f1d7f0626ec307d3de88436e9b` | F110 R16 C3: commit the self-use generation side effect | `scripts/self_use_queue.json` | +8 / -0 |
| C4 | (this commit) | F110 R16 C4: the round 16 handback (interrupted, recovery session) | `.agent/handoff.md` | — |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a-C2 | done | landed cleanly in session 5, unchanged by session 6 |
| C3 (self-use run, full) | INCOMPLETE | only the generation side effect (queue append) is confirmed and committed; job execution outcome, defect capture, evidence copy and `run.txt` are NOT done and NOT claimed |
| C4 | done | this handback |
| G5 THE TREE | pass | `git status --porcelain` EMPTY immediately before this commit was staged |

## External actions

- NO pull request created. NOTHING merged. NO force-push. No work on `main`.
- NO self-use generator or runner code was invoked by session 6.
- NO file under `.remedy-wt/` was created, deleted, or modified by session 6.

## Deviations & assumptions

- Round 16's own constraint 6 (steps f through j) is NOT complete. This is
  a DEVIATION from the block as authored, declared rather than hidden, per
  constraint 1's "if a slice looks wrong, apply it anyway and DECLARE the
  problem" spirit and per G8.
- The queue append (`SU-006`, `consumed_by` empty) was committed as-is
  because constraint 6j already anticipated and permitted this exact
  file changing as a side effect independent of the run's outcome.
- No process was killed, no evidence was deleted, no code was re-run.

## Next

Open findings: **278** (unchanged from round 15; this recovery action
registers no new finding, since nothing on disk is confirmed wrong — the
self-use job's outcome is simply UNKNOWN, not failed).

Next expected action, in this order:
1. Phase 1 rule 1 — read `.agent/STOP` from disk.
2. Phase 1 rule 2 — the Open PR Gate (expected empty, unchanged).
3. Before authoring any new round: investigate
   `.remedy-wt/job-6f74dd7367704fd5` and
   `.remedy-wt/selfuse-f110-run/SU-006.md` to determine whether the
   self-use job for `SU-006` reached `JOB_COMPLETED` or `JOB_BLOCKED` —
   likely by reading whatever run-manifest or episode record
   `packages/orchestration/pingpong_job.py`'s `run_job()` persists (see
   its `run_manifest_path` / `_write_run_manifest_record` machinery), NOT
   by re-invoking `run_next_self_use_item()` or
   `generate_and_append_if_empty()` again.
4. If the job is confirmed to have reached a terminal state: finish
   constraint 6's steps (f) through (j) using the ALREADY-PRODUCED
   artifacts (do not regenerate), commit as C3-continued, then write a
   fresh C4 handback.
5. If it cannot be confirmed: treat the job as abandoned, decide (as a
   round of its own) whether to discard `SU-006`'s pending state and
   redo the self-use step cleanly, or leave it pending and proceed — this
   decision belongs to that round's reviewer, not to this handback.
6. Round 16 remains OPEN; round 17 (findings + evidence job + review zip
   + feature file Built State) has not started.

SESSION 6 spent one recovery round (no new delegated build round) and
ends here with this handback. F110 stands at 16 rounds against the
25-round soft limit; not reached, no scope report owed.
