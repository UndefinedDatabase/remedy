── STEP CLOSURE PRECONDITION 6 (RUN) — F112 Prompt budget per task class ───
Round 21 · session continuing F112 · base `e9b9c46e` (F112 R20 C4, the tip
of feature/f112-prompt-budget-per-task-class)

Goal:
  Book round 20's PASS verdict (RECORD20, given verbatim below,
  independently re-verified by the reviewer — do not re-derive it), then
  RUN the self-use queue's pending item SU-007 (`self_use_runner.
  run_next_self_use_item`) to the normal approval gate. This is a REAL run
  against the local `ollama` provider (already confirmed by the reviewer to
  resolve for both `builder` and `reviewer` roles — no external network
  cost). Do NOT promote it, do NOT set `consumed_by`, do NOT register any
  finding in `.agent/live_review.md` this round — those are the CLOSURE
  round's own acts (DECISION F257 D2; docs/roadmap/STATUS_closure_protocol.md
  precondition 6). This round only runs the job and lands its evidence.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r21.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD20 to `.agent/live_review.md`
  C2   apply PLAN21 to `.agent/plan.md`
  C3   run SU-007 for real and commit its evidence under `.agent/selfuse_f112/`
  C4   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f112-r21.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `.agent/selfuse_f112/` (new directory this round creates)
  `.agent/handoff.md`
  `scripts/self_use_queue.json` is NOT touched this round (consumed_by is
  set only at the closure commit). NO file under `packages/`, `apps/`,
  `tests/` or `docs/` in the PRIMARY checkout is touched — the job itself
  runs in its OWN separate git worktree under `.remedy-wt/job-<job_id>/`,
  which `run_job` creates and manages; that worktree's own commits are the
  job's business, not this round's, and are not part of this round's diff.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE — never edit, retype or
     re-wrap one. If a slice looks wrong, apply it anyway and DECLARE the
     problem in the handback.
  2. `.agent/STOP` is read FROM DISK before the first commit and again
     before C4. If it exists at either reading: finish the commit in hand,
     write the handback, push, and stop — even mid-run, if you can do so
     without corrupting the job's own state (a job already started via
     `run_job` is not aborted; let it finish, then stop after landing its
     evidence).
  3. `.agent/plan.md` ends WITHOUT a trailing newline; PLAN21 is applied as
     an exact whole-file replacement, no trailing newline added.
     `.agent/live_review.md` also ends WITHOUT a trailing newline; append
     it as `content_bytes + b"\n" + RECORD20_bytes` — ONE newline, no blank
     line. Confirm the byte immediately before the append point yourself
     before writing.
  4. Do NOT run `ruff`, `npm`, or any formatter as a gate for THIS round's
     own authored files (`.agent/**`) — the job itself may run its own
     internal gates, which is the job's business, not this round's.
  5. RUN SU-007 exactly as:
     `from pathlib import Path; from packages.orchestration.self_use_runner import run_next_self_use_item; entry, job_file_path, result = run_next_self_use_item(Path(".remedy-wt/selfuse-f112-run"), repo_path=".")`
     — from the repository root, no `cd`, no environment variable
     overrides, using the function's own DEFAULT budgets
     (`max_provider_calls=6`, `max_cost_usd=0.50`, `max_tasks=1`) and its
     own DEFAULT role resolution (do not pass `builder_name`/
     `reviewer_name`, do not pass `"fake"` for either — let it resolve the
     real local `ollama` provider as designed). If it raises
     `SelfUseRunError` or `SelfUseJobError`, that is a valid outcome to
     report, not a defect to paper over — capture the full exception text
     in the handback and in `run.txt`, and still copy whatever job file
     landed in the scratch dest_dir (see constraint 6) if one exists.
  6. AFTER the run (or after the exception, if one occurred and a job file
     exists), copy the rendered job file byte-identically (verify by
     sha256) from `.remedy-wt/selfuse-f112-run/SU-007.md` into
     `.agent/selfuse_f112/SU-007.md`. Write `.agent/selfuse_f112/run.txt`
     recording, in plain text: the `job_id`; the entry id (`SU-007`); the
     final `status` of the returned `JobPlan` (or the exception, if one was
     raised instead); `result.error` (or the exception text); a table of
     every task's `task_id`/`status`/`error`; the FULL tuple
     `packages.orchestration.self_use_findings.describe_self_use_run_defects(result)`
     answers, each string verbatim, one per line (or, if the run raised
     before producing a `JobPlan`, state plainly that no defects tuple
     could be computed and why); the resolved `execution_config` naming
     which provider/model actually ran for `builder` and `reviewer`; the
     wall-clock duration of the run, measured by you around the call; and
     the job's own worktree path (`.remedy-wt/job-<job_id>`), stated as
     RETAINED and untouched by this round (do not delete it, do not commit
     it — it is a separate git worktree, not a path inside this
     checkout's tracked tree).
  7. AFTER copying, DELETE the scratch directory
     `.remedy-wt/selfuse-f112-run/` (its content is now the committed
     `.agent/selfuse_f112/` copy) — but do NOT touch
     `.remedy-wt/job-<job_id>/`, which is the job's own separate worktree
     and stays exactly as `run_job` left it.
  8. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`
     and `docs/roadmap/features/T3_F112.md` are NOT touched.
  9. A sentence THIS ROUND makes stale, anywhere inside the change set, is
     repaired in the commit that falsifies it. One outside the change set
     is DECLARED in the handback and left alone.
  10. NEVER force-push, never work on `main`, create NO pull request, merge
      nothing. Do not run `--approve` / `job_promote` on this job under any
      circumstance — the approval gate is where this round stops.

THIS ROUND'S PARAMETERS, measured by the reviewer at `e9b9c46e` before this
block was authored:
  LIVE_REVIEW PRE-C1   `.agent/live_review.md` measures 2290763 bytes,
                       ending WITHOUT a trailing newline.
  RECORD20 LENGTH      2953 bytes (measure this yourself against the
                       committed authored file's own extracted slice).
  POST-C1 EXPECTED     2290763 + 1 + 2953 = 2293717 bytes.
  HEADER SHAPE         lines matching `^Gate: F\d+ R\d+ — ` currently
                       number 267; matching `^Gate: F112 R20 — ` currently
                       0. Expected after C1: 268 and 1.
  OPEN SET             350 registered, 72 `Done:`, 278 open. UNMOVED by
                       this round's append — reconfirm on both sides of C1.
  PLAN.MD PRE-C2       46 lines (per `wc -l`), ends WITHOUT a trailing
                       newline, currently holds PLAN20 (2083 bytes).
  SELF-USE QUEUE       `pending_self_use_items()` currently answers exactly
                       one entry, `SU-007`; `next_self_use_item()` answers
                       that same entry. `scripts/self_use_queue.json` is
                       NOT part of this round's change set (see above) —
                       do not write to it.
  ROLE RESOLUTION      `resolve_role_config("builder").provider` and
                       `resolve_role_config("reviewer").provider` both
                       currently answer `"ollama"` (model
                       `muse-glimmer:latest`) — confirmed by the reviewer
                       directly before this block was authored. If your own
                       fresh read differs, DECLARE it; do not silently
                       adjust the run to compensate.

<<<BEGIN RECORD20>>>
Gate: F112 R20 — the round 20 entry, closure precondition 6's generation step (no production code). VERDICT PASS, over the range `3b7a3e18..e9b9c46e` (commits C0a `61b3ef58`, C0b `a1bb9448`, C1 `402f2220`, C2 `6c1dd691`, C3 `5ed84df4` — five real content commits — plus handback commit `e9b9c46e`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r20.md` and `HEAD:.agent/last_block.md` both print blob `7948c69cdc13f327351b58f2c816c2dbe60f719b`, reproduced directly; `wc -l` reproduced 227. THE PLAN REPLACEMENT AT C2 HELD BYTE-IDENTICAL: PLAN20 extracted by delimiter from the committed authored file (2083 bytes) compared byte-for-byte in Python against `.agent/plan.md` at C2 — equal, 2083 bytes both sides; the file ends WITHOUT a trailing newline, and `## Goal` / `## Next Steps` each occur exactly once. THE RECORD APPEND AT C1 (booking RECORD19) HELD BYTE-IDENTICAL: pre-append `.agent/live_review.md` measured 2286766 bytes at `3b7a3e18`, RECORD19 extracted from the committed authored file measured 3996 bytes exactly as pinned, appended as `content_bytes + b"\n" + RECORD19_bytes` (one newline), post-append measured 2290763 bytes exactly matching `2286766 + 1 + 3996`; the pre-append content is an exact byte prefix of the post-append content; the file still ends WITHOUT a trailing newline; the open set recomputed mechanically read 350 registered / 72 `Done:` / 278 open on both sides of the append, and lines matching `^Gate: F\d+ R\d+ — ` read 267 after C1 with exactly one matching `^Gate: F112 R19 — `. THE SELF-USE GENERATION AT C3 HELD EXACTLY AS THE BLOCK PREDICTED: `packages.orchestration.self_use_queue.load_self_use_queue()` read 6 items before this round's own re-check and 7 after, the reviewer's own re-parse of `scripts/self_use_queue.json` confirming the new entry `id="SU-007"`, `consumed_by=""` (PENDING), `provenance="generated (self-use-generator tier 1, ledger scan, R-0418)"`, and its `why`/`job_markdown` quoting the SAME R-0418 paragraph SU-005 and SU-006 already quoted — no exception was raised. G5 RE-VERIFIED BY THE REVIEWER DIRECTLY: `git status --porcelain` reads empty; `git diff --stat 3b7a3e18..e9b9c46e -- packages/ apps/ tests/ docs/` is empty; every commit's insertion count (227, 187, 2, 24, 8) is under 500. NO NEW FINDING AND NONE RESOLVED: the open set is unmoved at 278 (350 registered, 72 `Done:`). The reviewer additionally notes, as the round's own block already declared, that R-0418 was already the target of SU-005 (consumed by F109) and SU-006 (consumed by F110), both run to the approval gate without ever landing a `Done: R-0418` line — a pre-existing gap this round correctly left untouched, since fixing the generator's own selection logic or the ledger bookkeeping gap is out of F112's change set. Round 21 plans and runs SU-007 via `self_use_job`/`self_use_runner` to the normal approval gate, per PLAN20's Next Steps.
<<<END RECORD20>>>

<<<BEGIN PLAN21>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use item SU-007 generated round 20
(RECORD20: VERDICT PASS, booked this round). Round 21 plans and runs
SU-007 to the normal approval gate (closure precondition 6, F257/F258).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 21 runs `self_use_runner.run_next_self_use_item` against SU-007
(job "Address ledger finding R-0418") through the real builder/reviewer
loop (local `ollama` provider, no external cost), stopping at the normal
approval gate — never promoted. Every string
`self_use_findings.describe_self_use_run_defects` returns for the run's
JobPlan is registered as an R-id finding before close. `consumed_by` is
set to F112 only in the closure commit, not this round.

## Next Steps

- Register any findings the run's own defects surface; repair only if
  small and reviewer-gated as its own round.
- Set SU-007's `consumed_by` to F112 in the closure commit.
- Then: evidence job, review zip, STATUS line, PR per
  docs/roadmap/STATUS_closure_protocol.md.

## Risks

- Split children inherit the parent's full files_hint and re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap" / "proceed-overcap once" options are
  deliberately unbuilt (DECISION F112 D9).
- R-0767 stays OPEN on the model-routing seam this feature's config
  borrows from; unrelated to F112.
- A self-use job can stall mid-run (F110 R16's SU-006 precedent) —
  if so, declare it and resume via `resume_job_plan` next round rather
  than treating it as failed.
<<<END PLAN21>>>

Done when — the gates below, each RUN and reported as ONE LINE in the
handback with its real reading. Every gate runs at a commit STRICTLY
EARLIER than C4.

G1 TRANSPORT — `sha256sum` and byte length of the committed
   `.agent/authored/f112-r21.md`. Report that
   `git rev-parse HEAD:.agent/authored/f112-r21.md` and
   `git rev-parse HEAD:.agent/last_block.md` print ONE blob id after C0b.
   Report `wc -l .agent/authored/f112-r21.md`.

G2 THE PLAN — extract PLAN21 by delimiter from the committed authored
   file, compare byte-for-byte against `.agent/plan.md` at C2 — must be
   equal. Report `wc -l .agent/plan.md` (must be under 50), no trailing
   newline, `## Goal` and `## Next Steps` each exactly once.

G3 THE RECORD APPEND — extract RECORD20 by delimiter, report its byte
   length (expected 2953 — if it does not match, DECLARE the mismatch,
   do not silently adjust the arithmetic below). Report the arithmetic
   `2290763 + 1 + <len> = <total>` against the real post-append size, the
   byte-prefix property, no trailing newline, a NEGATIVE CONTROL (flip one
   byte, recompute, report `False`), lines matching `^Gate: F112 R20 — `
   before (0) and after (1) C1, and registered/`Done:`/open counts on both
   sides (expected UNMOVED 350/72/278).

G4 THE RUN — report `pending_self_use_items()` and `next_self_use_item()`
   immediately BEFORE calling `run_next_self_use_item` (expected: one
   pending entry, `SU-007`). Run the exact call in constraint 5, wrapped
   in your own wall-clock measurement. Report: the `job_id`; the final
   `result.status` (or the exception class/message, if one was raised);
   `result.error`; each task's `task_id`/`status`/`error`; the FULL tuple
   `describe_self_use_run_defects(result)` answers (or state plainly that
   none could be computed, and why); the resolved provider/model for
   `builder` and `reviewer` as the run's own `execution_config` states
   them; the wall-clock duration.

G5 THE EVIDENCE COPY — report the sha256 of the job file as it existed in
   the scratch dest_dir immediately after the run, and the sha256 of the
   committed `.agent/selfuse_f112/SU-007.md` — must be equal. Report
   `wc -l .agent/selfuse_f112/run.txt` and that it contains every element
   constraint 6 names (job_id, status, defects tuple, execution_config,
   worktree path).

G6 THE CLEANUP — report `os.path.isdir('.remedy-wt/selfuse-f112-run')` is
   `False` after C3. Report `os.path.isdir('.remedy-wt/job-<job_id>')` is
   `True` and that it was NOT deleted or modified by this round (state
   this as an assertion about what this round did, not a full audit of
   the job's own worktree contents). Report `git status --porcelain` in
   the PRIMARY checkout reads empty before C4 is staged.

G7 THE TREE AND THE COMMITS — `git diff --stat e9b9c46e..<C3> -- packages/
   apps/ tests/ docs/` in the PRIMARY checkout — must be EMPTY. `git ls-files
   scripts/self_use_queue.json` shows it unchanged since `e9b9c46e` (`git
   diff e9b9c46e..<C3> -- scripts/self_use_queue.json` empty). PER-COMMIT
   INSERTIONS (the `+` column) for C0a through C3, each confirmed under 500.

Handback: rewrite `.agent/handoff.md` in full — feature and round, session
number, branch, base and head SHAs, per-commit changed-files table, ONE
line per gate above with its real reading, the item-status table AGENTS.md
mandates, deviations, the open-findings count (expected 278, unmoved),
and the next expected action: the reviewer reads `run.txt`, decides which
(if any) defects become R-id findings, and plans the closure commit
(consumed_by=F112, STATUS line, README sync, evidence job, review zip,
PR). It has NO length cap. State plainly what the job's own outcome was —
completed clean, blocked at the approval gate, or an exception — in your
own words, without characterizing it as good or bad; that judgment is the
reviewer's. Do not write a `Done:` or `Gate:` paragraph anywhere beyond
applying RECORD20 verbatim. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report
the outcome; create NO pull request, merge nothing, run no `--approve`.
══END BLOCK══
