── STEP F110 R16 REPAIR — resume the stalled self-use job (SU-006) ──────
Round 16 repair · SESSION 7 of F110 · base `aebeea98` (F110 R16 C4)

Goal:
  Session 5's worker began constraint 6 of `.agent/last_block.md` (the
  committed, unedited round-16 block, still on disk) but its process ended
  before the job reached a terminal state — it left job
  `6f74dd7367704fd5` stuck at `status="running"`. Session 6 investigated
  read-only, took no run action, and handed back. This round RESUMES the
  SAME job — never replans, never double-generates — through the
  product's own recovery API, then finishes constraint 6's steps (f)
  through (j) exactly as originally ordered, and writes the handback that
  closes round 16.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f110-r16-repair.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   resume the job, finish constraint 6 f-j, land evidence under
       `.agent/selfuse_f110/`
  C2   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f110-r16-repair.md`
  `.agent/last_block.md`
  `.agent/selfuse_f110/` (created by this round; the files constraint 5
    below lists)
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/`, `docs/`, `.agent/plan.md`,
  `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`
  or `scripts/self_use_queue.json` is touched by this round's own commits.
  The job's own worktree `.remedy-wt/job-6f74dd7367704fd5` is the SELF-USE
  JOB's business, not this round's, and is never merged, promoted, or part
  of this change set — retained exactly as constraint 5(i) below requires.

Constraints:
  1. `.agent/STOP` is read FROM DISK before the first commit and again
     before C2. If it exists at either reading: finish the commit in hand,
     write the handback, push, and stop.
  2. Transport is PROMPT-EMBEDDED, not a scratch file (the reviewer here is
     100% read-only and holds no separate scratch original). Copy the bytes
     between the BEGIN BLOCK / END BLOCK sentinels above/below exactly as
     received (excluding the sentinel lines themselves) into
     `.agent/authored/f110-r16-repair.md`. C0a and C0b are the ONLY
     slice-transport commits this block orders — there is no
     PLAN/RECORD/DECISION/SLIPS append this round, because constraint 6(f)
     of the original block (still governing, quoted below) forbids this
     round from authoring `.agent/live_review.md` finding text; that is
     round 17's.
  3. BEFORE calling anything that mutates job state, print — via
     `packages.orchestration.pingpong_job.load_job_plan('6f74dd7367704fd5')`
     — the job's CURRENT `status`, `isolation_mode`, `worktree_branch`,
     `worktree_cleanup_status`, `worktree_cleanup_error`,
     `job_workspace_path`, `active_episode_id`, and every task's
     `task_id`/`status`. Then check, in order, and STOP (do not proceed to
     step 4) if any fails, declaring exactly which and its printed value:
       - `status` is `"running"` (a job at any OTHER status did not stall
         the way this one did, and resuming it would be a different action
         than the one this round is authorized for).
       - `worktree_cleanup_status` is one of `{"active", "retained",
         "failed_recoverable"}` (`resume_job_plan`'s own precondition).
       - the branch `remedy/job-6f74dd7367704fd5` exists in this repo
         (`git rev-parse --verify remedy/job-6f74dd7367704fd5`).
     If all three hold, proceed to step 4.
  4. Call `packages.orchestration.pingpong_job.resume_job_plan(
     '6f74dd7367704fd5')` with NO other keyword arguments — the persisted
     `budgets` (`max_provider_calls=6, max_cost_usd=0.5`), `execution_config`
     (`builder='ollama', reviewer='ollama'`) and `max_tasks=1` are REUSED
     unchanged, exactly as F018 Scope 7's "a stopped-then-resumed job must
     NOT reset counters to zero" already requires; passing a fresh
     `budgets=` would override that, not merely repeat it, so do not pass
     one. Print the elapsed wall-clock seconds and every field constraint
     6(e) of `.agent/last_block.md` ordered printed: `job_id`, `status`,
     `error`, `execution_config`, `isolation_mode`, `worktree_path`,
     `worktree_cleanup_status`/`_error`, and every task's fields.
     If the call RAISES (`job_not_resumable`, `job_branch_missing`,
     `job_not_found`, or any other exception): STOP. Do not catch and
     improvise a workaround. Quote the exact exception text in the
     handback and proceed directly to C2 with constraint 5's steps (f)
     through (j) NOT attempted.
  5. If step 4 returns a `JobPlan` (did not raise): finish constraint 6,
     steps (f) through (j), of `.agent/last_block.md` EXACTLY as that
     committed text orders, against the `JobPlan` `resume_job_plan`
     returned and the SAME `dest_dir`
     (`.remedy-wt/selfuse-f110-run`, which still holds `SU-006.md` from the
     original planning phase — do NOT call `plan_next_self_use_item` or
     `run_next_self_use_item` again; both would plan a NEW job and orphan
     this one). Quoted here for reference — the governing text is
     `.agent/last_block.md`'s committed bytes, which you must actually
     read yourself before executing this step:
       f. `packages.orchestration.self_use_findings.describe_self_use_run_defects(plan)`
          — print tuple length and each defect string verbatim between
          `--- DEFECT N BEGIN ---` / `--- DEFECT N END ---` markers.
       g. copy the job markdown file from `dest_dir`
          (`.remedy-wt/selfuse-f110-run/SU-006.md`) to
          `.agent/selfuse_f110/SU-006.md` with `shutil.copyfile`, and print
          BOTH sha256 digests (source, copied) proving byte-identity.
       h. write the ENTIRE transcript of this round (every printed value
          from step 4 onward, in the order printed) to
          `.agent/selfuse_f110/run.txt`. Commit both files in C1.
       i. delete the run's OWN `dest_dir` (`.remedy-wt/selfuse-f110-run`)
          by its exact path after the copy in (g); do NOT touch
          `JobPlan.worktree_path` (`.remedy-wt/job-6f74dd7367704fd5`) — it
          is retained by the product itself.
       j. `scripts/self_use_queue.json` is NOT touched this round;
          `SU-006`'s `consumed_by` stays the empty string, unchanged since
          session 5. Setting it belongs to round 18's closure commit.
  6. A `blocked` OR `completed` final `JobPlan.status` is a normal,
     honestly-measured OUTCOME — not a deviation, exactly as the original
     round 16 block's constraint 7 already rules.
  7. Do NOT run `ruff`, `npm`, or any formatter — this round's own commits
     write no `.py` file (the job's own worktree is a separate matter,
     governed by that job's own acceptance text).
  8. If step 3 stopped the round (any of its three checks failed): C1
     writes NOTHING beyond a record of what step 3 itself observed — do
     not create `.agent/selfuse_f110/` at all, and say so plainly in the
     handback rather than fabricating an evidence directory for a run that
     did not happen.

Done when — each gate run and reported as ONE LINE in the handback with
its real exit code, at a commit STRICTLY EARLIER than C2:

G1 TRANSPORT — sha256sum of `.agent/authored/f110-r16-repair.md` and
   `.agent/last_block.md` — must match each other. Report `wc -l
   .agent/authored/f110-r16-repair.md`.

G2 THE PRE-RESUME STATE — the seven fields constraint 3 orders printed,
   and the three checks' results (pass/fail each), quoted verbatim from
   the transcript.

G3 THE RESUME AND THE RUN (only if constraint 3 passed) — one block
   quoting `.agent/selfuse_f110/run.txt` verbatim (or a clear pointer to
   it plus the key numbers inline): final `JobPlan.status`, whether
   `describe_self_use_run_defects` returned any strings (quote them if
   so), the source/copied sha256 pair proving the evidence copy is
   byte-identical. Report `git status --porcelain` immediately after C1 is
   staged, BEFORE C2 — must show only paths this round's own change set
   names.

G4 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C2 is staged — EMPTY.
   `git diff --stat aebeea98..<C1-sha> -- packages/ apps/ tests/ docs/
   .agent/plan.md .agent/live_review.md .agent/decisions.md
   .agent/prose_slips.md scripts/self_use_queue.json` — must be EMPTY.
   `git worktree list` — no NEW worktree beyond
   `.remedy-wt/job-6f74dd7367704fd5` (retained); `ls -d
   .remedy-wt/selfuse-f110-run` — must report "no such file" (deleted per
   constraint 5(i), only if constraint 3 passed and step 4 did not raise).
   PER-COMMIT INSERTIONS, the `+` column only, for C0a and C1, reported
   cell by cell against the handback's own `## Commits` table and each
   confirmed under 500.

Handback: rewrite `.agent/handoff.md` in full — feature and round (round
16, now CLOSED by this repair if constraint 4 succeeded or constraint 3/4
stopped it — say which, honestly), SESSION 7 of F110, branch, base and
head SHAs, the per-commit changed-files table with its `+/-` column, ONE
line per gate above with its real exit code, the item-status table
AGENTS.md mandates, the deviations, the open-findings count (278,
unchanged — any defect surfaced this round routes to round 17, it is NOT
registered here), the next expected action (round 17: register any
defects as findings, run the evidence job, build a fresh review zip, give
`docs/roadmap/features/T3_F110.md` its Built State section). It has NO
length cap. Then `git push -u origin
feature/f110-model-routing-by-task-class`; create NO pull request, merge
nothing.
──────────────────────────────────────────────────────────────