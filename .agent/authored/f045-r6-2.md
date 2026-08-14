BEGIN BLOCK f045-r6-2
── STEP T003b/3 — F045 Loop definitions · ROUND 6 (session close) ────────

Goal:        Persist the three defects the R5 review and the R6 halt found
             before the session ends, and write the session-closing handoff.
             No code changes.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 register R-0351/R-0352/
             R-0353 · ITEM 3 C2 plan + handoff · ITEM 4 gates.
Change:      .agent/authored/f045-r6-2.md · .agent/last_block.md ·
             .agent/live_review.md · .agent/plan.md · .agent/handoff.md.
             Nothing else. Do NOT touch any file under packages/, tests/,
             apps/ or docs/ this round — the fixes are R7's work, and mixing
             them in would hide a finding under its own repair.
Constraints: SPLIT round, bookkeeping only. Never work on main; never
             force-push; no PR; merge nothing.
Insertion budget, per commit: C0a and C0b ≈ block size (single `.agent/**`
             state-file rewrites, cap-exempt by DECISION F104 D1) · C1 ≤ 8 ·
             C2 ≤ 120.
Done when:   every gate in ITEM 4 has been RUN and its real output recorded.
Handback:    completion report + rewrite .agent/handoff.md

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r6-2.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R6 block verbatim`
C0b: copy that file over `.agent/last_block.md`, replacing the R5 block.
Commit subject: `chore(f045): point last_block at the R6 block`
Prove it: cmp .agent/authored/f045-r6-2.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — register R-0351, R-0352 and R-0353 ═══
File `.agent/live_review.md`. APPEND at the END of the `## Findings` section,
after R-0350's paragraph, one blank line between paragraphs. Three lines:

- R-0351 — Medium — the persisted job loses a field the in-memory job has, and no test can see it. The R5 block ordered `run_loop`'s mission branch to set `job.mission = mission.goal` AFTER calling `_materialize_loop_job`, which has already run `(save or _save_job)(job)` at `packages/orchestration/loop_run.py:159`. The cited precedent does the opposite: `mission_state.continue_mission` sets `mission=mission.goal` inside the `Job(...)` constructor at `mission_state.py:948`, before `save_job`. So a real run persists a job record whose `mission` is null while the object the caller holds has it set. Every dispatch test passes a list-appending `save` that stores the same object reference, so the in-memory value is what they assert and the persisted record is never read — the R-0344 shape again, a property decided by the fixture rather than by the code. The R5 worker implemented it exactly as ordered and reported the gap instead of widening the helper's signature on its own authority, which was correct. Impact is display-only today: the non-test readers of `Job.mission` are `packages/orchestration/run_report.py:405` and the goal fallback at `apps/cli/commands/decision.py:167`. Fix by passing the mission text into `_materialize_loop_job` so it is set before the save, and add a test that reads the job back through `storage.load_job` rather than out of the save callable. OPEN.

- R-0352 — Medium — `run_loop`'s `root` isolates the mission store but not the job store. `run_loop(..., root=X)` forwards `root` to `create_mission` (`mission_state.py:387`) and `link_job_to_mission` (`mission_state.py:432`), but `_materialize_loop_job` has no `root` parameter, so its default save calls `storage.save_job(job)` with one argument, which resolves through `_resolve_jobs_dir(None)` (`storage.py:44-49`) to the process-wide `jobs_dir()`. A caller that passes `root` to isolate a run therefore gets the mission under `X` and the job in the real store, and `last_run_for_loop(name, root=X)` can never find the job `run_loop(root=X)` just made — the two halves of the same feature disagree about where a run lives. No test catches it because every dispatch test passes an explicit `save` callable, which bypasses the default path entirely, and the two `last_run_for_loop` tests write their jobs by hand with `storage.save_job(job, tmp_path)`. This is the R5 block's error, not the worker's: the block fixed the helper's parameter list and never gave it a `root`. Fix by threading `root` through `_materialize_loop_job` to `save_job`, and pin it with a test that calls `run_loop` with `root` and NO `save`, then finds the job via `last_run_for_loop` with the same `root`. OPEN.

- R-0353 — Low — a block's line citations were not re-measured against the file the same session had just changed. The R6 block cited the save call at `packages/orchestration/loop_run.py:157`; `grep -n "save or _save_job"` puts it at 159, because R5's own commits shifted the file underneath the citation. The worker halted before its first commit rather than write a `file:line` into the durable review record that does not resolve on disk, which is the correct behaviour and the second halt this session caused by a reviewer citation — the first was the phantom `start_follow_up` in R-0349. R-0349's counter-measure covers SYMBOLS cited as precedent, which were all grepped and all correct here; it does not cover a bare line number in prose, which is the gap this finding names. Nothing landed wrong either time. Counter-measure: a block that cites `file:line` for a file the CURRENT feature branch has modified re-greps that line at emission time, and prefers citing the symbol plus its distinguishing text over a bare number, because a symbol survives an edit above it and a line number does not. OPEN.

Commit subject: `docs(f045): register R-0351 to R-0353, the R5 dispatch defects`

═══ ITEM 3 · C2 — plan and session-closing handoff ═══
Rewrite `.agent/plan.md` (under 50 lines, keeps `## Goal` and `## Next
Steps`): Current Step becomes R5 reviewed PASS — dispatch, inert notice and
last-run lookup landed; R-0348/R-0349 resolved; R-0350 to R-0353 open. Next
Steps become: R7 fixes R-0351 and R-0352 FIRST, then the CLI (`remedy loop
list | validate | run`), then the integration gate, then closure per
docs/roadmap/STATUS_closure_protocol.md. Open findings becomes 4 (R-0350,
R-0351, R-0352, R-0353); next free finding ID R-0354. Fortschritt becomes
`Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung`. Keep the
config-file risk and the inert-trigger risk, and replace the third with: the
mission path persists jobs and missions through two different root
resolutions until R-0352 is fixed, so no caller may rely on `root` isolating a
whole run.

Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). This is a SESSION-CLOSING handoff,
so it carries:
- feature + round, branch, and the fact that this was a one-session self-drive
  run (docs/agents/self_drive_protocol.md) that ended at its declared round
  cap with work committed and pushed — a success under G7, not a failure
- a per-round table: R3 HALTED (two block/disk contradictions, no feature
  work), R4 PASS reviewed at `7c6524ee`, R5 PASS reviewed at `1a86c36d`, R6
  halted once on a citation and completed on re-emission
- every commit SHA of THIS round with its changed files
- the reviewer's re-run verification results for R5, recorded as the reviewer
  reported them: `328 passed` over test_loop_run.py + test_loop_spec.py +
  tests/docs/ in one run, canary `42 passed`, ruff `All checks passed!`,
  `grep -c "^Done: R-" .agent/live_review.md` = 6, `.agent/plan.md` 42 lines,
  an empty `git status --porcelain`, and one line from `git worktree list`
- this round's own gate results from ITEM 4
- open-findings count 4, naming R-0350, R-0351, R-0352, R-0353
- an item-status table with one row per ITEM 1-4
- the next expected action, which names Phase 1 rule 1 (read `.agent/STOP`
  from disk) BEFORE rule 2 (the Open PR Gate), then R7's ordered work: fix
  R-0351 and R-0352 first, then the CLI
- the statement that the branch has NO PR, that nothing was merged, that main
  was never touched and that no force-push occurred
- the Fortschritt line verbatim
Commit subject: `docs(f045): close the session with the R5 review handoff`

═══ ITEM 4 · gates ═══
Run every command; record the REAL exit code and REAL output. Report counts as
OBSERVED — do not predict them and do not restate a count this block gave you.

(a) cmp .agent/authored/f045-r6-2.md .agent/last_block.md
(b) grep -c "^- R-0351 — Medium" .agent/live_review.md
(c) grep -c "^- R-0352 — Medium" .agent/live_review.md
(d) grep -c "^- R-0353 — Low" .agent/live_review.md
(e) grep -c "^- R-0" .agent/live_review.md
(f) git diff --stat e672374f..HEAD                 → only .agent/** paths
(g) python3 -m pytest tests/cli/test_golden_path.py -q      (canary)
(h) git status --porcelain                         → EMPTY
(i) git worktree list                              → one line only

Gates (b)-(e) are scoped to `.agent/live_review.md`, never to this block or to
`.agent/authored/**`, both of which legitimately contain the same strings.

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r6-2
