── STEP CLOSE/3 — F112 round 29 ────────────────────────────────
Goal: Book round 28's PASS verdict, then run closure precondition 6's
self-use item (SU-007, already pending) for real through the shipped
generator/runner to the normal approval gate — mirroring F109 R19 and
F110 R16's precedent exactly, never promoted.

Bundle:
1. C0a/C0b — save this block verbatim (transport proof), `cp` never
   retype.
2. C1 — append RECORD28 (below) to `.agent/live_review.md`: books round
   28's PASS verdict. No new finding is registered or resolved by this
   append (round 28 fixed nothing new).
3. C2 — apply PLAN29 (below) to `.agent/plan.md` (whole-file replace).
4. C3 — THE SELF-USE STEP. Read `git show 9ee3ab57` (F109 R19's own
   precedent commit) and `.agent/authored/f110-r16.md`'s constraint 6
   yourself before writing any code, and mirror their shape exactly
   with `f112`/`F112` in place of `f109`/`f110`/`F109`/`F110`, with ONE
   difference from both precedents: SU-007 is ALREADY PENDING in
   `scripts/self_use_queue.json` (`consumed_by=""`), so there is no
   generation step — do not call
   `self_use_generator.generate_and_append_if_empty`.
     a. Print `.agent/STOP` existence (must be False; if True, STOP here
        and write the handoff instead of proceeding).
     b. `packages.orchestration.self_use_queue.load_self_use_queue()`,
        print every entry's id/consumed_by/title. Call
        `pending_self_use_items()` and `next_self_use_item()` and print
        both — expect exactly one pending item, `SU-007`, and
        `next_self_use_item()` returning that same entry. If this is NOT
        what you observe (e.g. SU-007 already consumed, or a different
        item is first), STOP and declare the discrepancy rather than
        proceeding on an assumption.
     c. Call
        `packages.orchestration.self_use_runner.run_next_self_use_item(
        dest_dir=Path('.remedy-wt/selfuse-f112-run'), repo_path='.')`
        with NO `builder_name`/`reviewer_name` override and the DEFAULT
        budgets (`max_provider_calls=6`, `max_cost_usd=0.50`,
        `max_tasks=1`) — the same call shape F109 R19 and F110 R16 both
        used. Print `resolve_role_config('builder')` and
        `resolve_role_config('reviewer')` immediately before the call,
        the elapsed wall-clock seconds, and every field of the returned
        `(entry, job_file_path, JobPlan)` tuple (job_id, status, error,
        execution_config, isolation_mode, worktree_path,
        worktree_cleanup_status/_error, every task's fields) — the same
        set F109's and F110's own `run.txt` print.
     d. Call
        `packages.orchestration.self_use_findings.describe_self_use_run_defects(plan)`
        and print the tuple length plus each string verbatim between
        `--- DEFECT N BEGIN ---` / `--- DEFECT N END ---` markers. Do
        NOT author `.agent/live_review.md` finding text for these
        yourself — that is round 30's job (only reviewer-authored text
        sets a registration); this round only RECORDS the defect
        strings verbatim for round 30 to consume.
     e. Copy the job markdown file from the run's `dest_dir` to
        `.agent/selfuse_f112/SU-007.md` with `shutil.copyfile`, and
        print both sha256 digests (source, copied) proving byte
        identity.
     f. Write the ENTIRE transcript above — every printed value, in the
        order printed — to `.agent/selfuse_f112/run.txt`. Commit both
        files (and `.agent/selfuse_f112/` itself, new) in C3.
     g. Delete the run's OWN `dest_dir` (`.remedy-wt/selfuse-f112-run`)
        by its exact path after the copy in (e); do NOT touch
        `JobPlan.worktree_path` (the job's own isolated worktree under
        `.remedy-wt/job-<id>`) — it is retained by the product itself,
        exactly as both precedents left their own worktrees untouched.
     h. `SU-007` is NOT consumed by this round: `consumed_by` for that
        entry stays the empty string in `scripts/self_use_queue.json`.
        Setting it belongs to round 30's closure commit
        (STATUS_closure_protocol.md precondition 6). This round's own
        Change set does not list `scripts/self_use_queue.json` — since
        no generation happens this round (SU-007 was already queued),
        that file is NOT touched at all this round, unlike F110 R16
        where generation itself wrote to it.
   A `blocked` job status (the normal approval-gate outcome per
   `self_use_runner`'s own docstring) is NOT a round failure and is NOT
   "declared" as a deviation — report it as the measured OUTCOME it is,
   exactly as F109 R19's and F110 R16's own handbacks did.
5. Handback — completion report + rewrite `.agent/handoff.md`.

Change: `.agent/live_review.md`, `.agent/plan.md`,
`.agent/authored/f112-r29.md` (new), `.agent/last_block.md`,
`.agent/selfuse_f112/SU-007.md` (new), `.agent/selfuse_f112/run.txt`
(new), `.agent/handoff.md`. `scripts/self_use_queue.json` is NOT
touched this round (see 4h). Nothing under `packages/`, `apps/`,
`tests/`, `docs/` is touched by THIS round's own commits — the self-use
run's own job worktree under `.remedy-wt/job-<id>` is a separate matter,
governed by that job's own acceptance text, not by this block, and is
never merged or promoted onto this branch.

Constraints:
- `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
  `docs/roadmap/features/T3_F112.md`, `docs/roadmap/STATUS.md`,
  `README.md` are NOT touched this round.
- Do not run `ruff`, `npm`, or any formatter as part of THIS round's own
  commits — they write no `.py` file (the self-use run's own job
  worktree is separate, governed by its own acceptance text).
- Never force-push, never work on `main`, create NO pull request, merge
  nothing, no `--approve` / promotion of the self-use job's own diff —
  "RUN... to the normal approval gate... never promoted" is load-bearing
  and is what distinguishes this from an ordinary feature round.
- If `run_next_self_use_item` raises `SelfUseRunError` or
  `SelfUseJobError`, capture the FULL exception (class + message +
  traceback), STOP, and declare it fully in the handback — do not retry
  with different parameters on your own initiative.

Done when — run every gate and report its REAL exit code/output:
- `git status --porcelain` — empty before C0a and immediately before the
  handback commit.
- `.agent/live_review.md` reproduces at exactly `2338544` bytes
  immediately after C1 (pre-append `2334372` + 1 + RECORD28's `4171`
  bytes), and RECORD28 extracted from the committed authored file is a
  byte-exact suffix; report registered/`Done:`/open counts before and
  after C1 (expect UNMOVED: 354 registered, 74 `Done:`, 280 open, both
  sides).
- `.agent/plan.md` reproduces byte-identical to PLAN29 (`2249` bytes, no
  trailing newline, `## Goal`/`## Next Steps` each exactly once,
  `wc -l` under 50) after C2.
- `pending_self_use_items()`/`next_self_use_item()` readings before C3
  (expect: 1 pending, `SU-007`).
- Every field `run_next_self_use_item` returns, printed in full, plus
  the elapsed wall-clock seconds and the resolved role configs.
- `describe_self_use_run_defects(plan)`'s tuple length and every string
  verbatim.
- The two sha256 digests proving the copied job markdown is byte
  identical to the source.
- `scripts/self_use_queue.json`'s `SU-007` entry still has
  `consumed_by=""` after this round (report the read).
- `git status --porcelain --ignored=no` immediately before the handback
  commit — confirm `.remedy-wt/selfuse-f112-run` no longer appears
  (deleted per 4g) and the job's own `.remedy-wt/job-<id>` worktree, if
  any, is untracked/gitignored and not staged.

Handback: completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

--- BEGIN RECORD28 sha256=70db6db54e3e1007aad2b79ef389e7a4f3c1334594d7097dc47b59272f0d95c3 ---
Gate: F112 R28 — the round 28 entry, the closure evidence bundle rebuild and review zip (docs/roadmap/STATUS_closure_protocol.md algorithm steps 1-2). VERDICT PASS, over the range `313126ce..346c178f` (commits C0a `e4790bff`, C0b `fdaf902b`, C1 `e259d851`, C2 `346c178f` — four real content commits — plus handback commit `6dd06718`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r28.md` and `HEAD:.agent/last_block.md` both print blob `df782cadec1cb4436b6560f55a5663812983042c`, reproduced directly; `sha256sum .agent/authored/f112-r28.md` reproduced `4a64111331abc8f31617d0658f7f53fb22af236f10766a18339655079705595c` at 17747 bytes. THE PLAN HELD: `.agent/plan.md` reproduced at 2218 bytes, 47 lines, `## Goal`/`## Next Steps` each exactly once, no trailing newline. THE RECORD APPEND AT C1 HELD: `.agent/live_review.md` reproduced at 2334372 bytes immediately after C1 (booking RECORD27, resolving R-0792/R-0793 — see round 27's own gate entry above), matching the round's own pinned figure exactly; registered/`Done:` counts read 354/74 both before and after this round's own C1, unmoved by round 28 itself since round 28 mints and resolves nothing new. NO CODE CHANGED: `git diff --stat 313126ce..6dd06718 -- packages/ apps/ tests/ docs/` reproduced empty — the evidence dir and the zip are gitignored and were never `git add`ed, confirmed with `git status --porcelain` and `git status --porcelain --ignored=no` both empty throughout. THE EVIDENCE JOB AND ZIP WERE REPRODUCED INDEPENDENTLY BY THE REVIEWER, NOT TAKEN ON THE WORKER'S REPORT: the three scoped commands reproduced `test_class_prompt_budget.py` 24 passed, the two named `test_context_compiler.py` fixtures 2 passed, `test_golden_path.py` 42 passed — matching `create_manual_completion_bundle`'s reported summary (`job_id` `79b21c8cba8b4352`, `head_commit` `346c178f3241fad3984dca9baea3f37e34c3892a` = this round's own C2, `total_passed` 68, `verdict` `PASS_WITH_RISKS`) exactly. THE OUTPUT_HASH CONTRACT HOLDS ON THE PACKAGED ARTIFACT ITSELF: the reviewer independently re-opened `evidence/current/verification_tests.json` FROM INSIDE the produced zip (not from the worker's transcript) and confirmed `output_hash == sha256(stdout_summary.encode())` `True` for all three of `vr-0001`/`vr-0002`/`vr-0003`, proving round 27's fix (R-0792) holds on the real packaged evidence this closure will ship, not merely on the new unit tests. THE ZIP ITSELF WAS RE-OPENED BY THE REVIEWER DIRECTLY: `sha256sum /home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-123332-READY_FOR_REVIEW.zip` reproduced `b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927`, matching the script's own printed `final_sha256` exactly; `.review_zip_manifest.json` read from inside that exact file (via `zipfile`, never from stdout) reproduced `PACKAGE_STATUS` `READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE` `True`, `REVIEW_SUBJECT_ALIGNMENT` `PASS` with 0 issues and 0 hash mismatches, `committed_review_subject.base_commit` `5c28c6741db2d9073fc75cd159d91037e0757fb0`, `head_commit` `346c178f3241fad3984dca9baea3f37e34c3892a`, `base_is_ancestor` `True`, `ready_gate_matrix.ok` `True` with an empty `blocking_reasons` list — every one of these READ DIRECTLY BY THE REVIEWER, not paraphrased from the handback. THIS IS THE OPERATOR'S RULING CONFIRMED END TO END: the `BLOCKED_EVIDENCE` defect the round 26 handoff escalated is now demonstrated FIXED on the real closure artifact, not only on unit tests. THE INTEGRITY CHECK WAS REPRODUCED BY THE REVIEWER DIRECTLY: `run_integrity_checks()` read `.passed` `True`, `.fail_count` `0`, all five checks (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `high_blockers_open`) `PASS`. Closure preconditions 1 (this verdict, PASS), 2 (round 19 integration gate plus this round's own scoped re-runs), 3 (this round's integrity check), 4 (Built State landed round 22) and 5 (clean tree, pushed, worker idle — confirmed) are now satisfied; precondition 6 (the self-use item) is the one remaining precondition, taken up next round. `git status --porcelain` reads empty now.
--- END RECORD28 ---

--- BEGIN PLAN29 sha256=a7ed5cae805ccd0df3b904ed8642d8d3d3867b3816013d45e39815c48eb87130 ---
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1. Round 27 fixed the evidence-packager
contract (R-0792, R-0793); round 28 rebuilt the closure evidence bundle
and review zip, confirmed READY_FOR_REVIEW/true on the real packaged
artifact (RECORD28, this round). Closure preconditions 1-5 are now
satisfied; precondition 6 (the self-use item) is the last one — SU-007
is already pending in scripts/self_use_queue.json (consumed_by=""), so
this round plans and RUNS it for real through the shipped generator/
runner, mirroring F109 R19 and F110 R16's precedent exactly.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 29 books round 28's PASS verdict, then runs SU-007 (an "Address
ledger finding R-0418" job) through
`packages.orchestration.self_use_runner.run_next_self_use_item` to the
normal approval gate — never promoted, `consumed_by` stays empty this
round. The run's defects (if any) and `consumed_by=F112` land in round
30, together with the closure commit.

## Next Steps

- Round 30: register any self-use-run defects as normal R-id findings,
  author the STATUS `[x]` line from round 28's evidence values, closure
  commit (STATUS, README capability sync, `self_use_queue` SU-007
  `consumed_by=F112`, final `.agent/` state), PR opened, not merged.
- Round 31: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule;
  hand back the built zip's name and SHA-256 to the operator.

## Risks

- The self-use run may land `blocked` at its own approval gate (F109's
  SU-005 and F110's SU-006 both did) — a normal outcome per
  `self_use_runner`'s own docstring, not a failure of this round; its
  defects route to round 30's findings.
- R-0784 and R-0767 (both OPEN, unrelated to F112) carry forward as
  documented risks per precondition 1's "Resolved or documented risk".
--- END PLAN29 ---
