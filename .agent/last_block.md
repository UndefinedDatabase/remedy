── STEP CLOSURE PRECONDITION 6 — F112 Prompt budget per task class ─────────
Round 20 · SESSION 6 (or 7) of F112 · base `3b7a3e18` (F112 R19 C4, the tip
of feature/f112-prompt-budget-per-task-class)

Goal:
  Book round 19's PASS verdict (RECORD19, given verbatim below, independently
  re-verified by the reviewer — this worker does not re-derive it) into
  `.agent/live_review.md`, then open the closure sequence's precondition 6
  (docs/roadmap/STATUS_closure_protocol.md): the self-use queue currently
  holds no pending item, so call the generator that replenishes it and
  report exactly what happens. No self-use JOB is planned or run this
  round — only the generation step.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r20.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD19 to `.agent/live_review.md`
  C2   apply PLAN20 to `.agent/plan.md`
  C3   call `packages.orchestration.self_use_generator.generate_and_append_if_empty`
       and commit whatever it writes to `scripts/self_use_queue.json` (if
       anything)
  C4   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f112-r20.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `scripts/self_use_queue.json`
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/` or `docs/` is touched.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE — never edit, retype or
     re-wrap one. If a slice looks wrong, apply it anyway and DECLARE the
     problem in the handback: a declared conflict is worth more than a
     silent repair.
  2. `.agent/STOP` is read FROM DISK before the first commit and again
     before C4. If it exists at either reading: finish the commit in hand,
     write the handback, push, and stop.
  3. TYPE each slice from THIS PROMPT'S OWN BYTES directly into
     `.agent/authored/f112-r20.md` at C0a — do not name any path under
     `.remedy-wt/` in a bash command; that permission is denied this
     session and naming it only costs a turn. This round needs no
     `.remedy-wt/` scratch at all (no worktree, no long-running suite).
  4. `.agent/plan.md` ends WITHOUT a trailing newline in this feature's own
     convention, and PLAN20 is applied as an exact whole-file replacement
     with no trailing newline added. `.agent/live_review.md` also ends
     WITHOUT a trailing newline; append it as
     `content_bytes + b"\n" + RECORD19_bytes` — ONE newline, no blank line
     — which is the convention every F112 round since R14 has used.
     Confirm this yourself before writing by reading the byte immediately
     before the append point.
  5. Do NOT run `ruff`, `npm`, or any formatter. This round writes no
     Python/TS source; `scripts/self_use_queue.json` is data written by
     calling the generator function, never hand-edited.
  6. Invoke the generator as a library call from the repository root:
     `python3 -c "from packages.orchestration.self_use_generator import generate_and_append_if_empty; entry = generate_and_append_if_empty(); print(entry)"`.
     Do not set environment variables, do not `cd` anywhere first — run
     from `/home/decodeux/Repos/remedy` directly.
  7. This round runs no pytest suite and creates no worktree, so R-0176's
     scratch-log rule does not bind it; no `.agent/gate_f112_r20/` directory
     is created.
  8. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`
     and `docs/roadmap/features/T3_F112.md` are NOT touched. Nothing this
     round found needs any of them, and the change set forbids it.
  9. A sentence THIS ROUND makes stale, anywhere inside the change set, is
     repaired in the commit that falsifies it. One outside the change set
     is DECLARED in the handback and left alone.
  10. NEVER force-push, never work on `main`, create NO pull request, merge
      nothing.

THIS ROUND'S PARAMETERS, all measured by the reviewer at `3b7a3e18` before
this block was authored:
  LIVE_REVIEW PRE-C1   `.agent/live_review.md` measures 2286766 bytes,
                       ending WITHOUT a trailing newline.
  RECORD19 LENGTH      3996 bytes (measure this yourself against the
                       committed authored file's own extracted slice; it
                       must match).
  POST-C1 EXPECTED     2286766 + 1 + 3996 = 2290763 bytes.
  HEADER SHAPE         lines matching `^Gate: F\d+ R\d+ — ` currently
                       number 266; lines matching `^Gate: F112 R19 — `
                       currently number 0. Expected after C1: 267 and 1.
  OPEN SET             350 registered (unique `^- R-\d+ — ` ids), 72 unique
                       `^Done: R-\d+ — ` ids, 278 open. UNMOVED by this
                       round's append (it registers no finding and resolves
                       none) — reconfirm this on BOTH sides of C1.
  PLAN.MD PRE-C2       44 lines, ends WITHOUT a trailing newline, currently
                       holds PLAN19 (2088 bytes).
  SELF-USE QUEUE       `packages.orchestration.self_use_queue.pending_self_use_items()`
                       currently answers an empty tuple; `next_self_use_item()`
                       currently answers `None`; `load_self_use_queue()`
                       currently holds exactly 6 items (SU-001..SU-006, ids
                       `SU-\d{3}`), all with non-empty `consumed_by`.
  GENERATOR TIER 1     `self_use_generator._oldest_open_low_or_medium_finding`
                       currently answers `R-0418` (a Low, REVIEWER-BLOCK-
                       DEFECT finding at `.agent/live_review.md` line 135) as
                       the oldest OPEN Low/Medium finding — this is expected
                       and is NOT a defect in this round's own change: R-0418
                       was already the target of SU-005 (consumed by F109)
                       and SU-006 (consumed by F110), both of which really
                       ran the job to the approval gate (see git log
                       `9ee3ab57`, `d56c4a91`) without ever landing a
                       `Done: R-0418` line — that gap is PRE-EXISTING and
                       outside this round's change set; do not attempt to
                       fix it here. `generate_and_append_if_empty()` is
                       therefore expected to append a SEVENTH item,
                       `SU-007`, whose `why` and `job_markdown` quote the
                       SAME R-0418 paragraph, with `consumed_by` left empty
                       (PENDING) and `provenance` reading
                       `generated (self-use-generator tier 1, ledger scan, R-0418)`.

<<<BEGIN RECORD19>>>
Gate: F112 R19 — the round 19 entry, session 6's integration gate (no production code). VERDICT PASS, over the range `c7d68c58..cd3173fc` (commits C0a `8fe10ad8`, C0b `598e228b`, C1 `4f8b4be1`, C2 `d217bab0`, C3 `cd3173fc` — five real content commits — plus handback commit `3b7a3e18`), independently re-verified by the reviewer at the start of round 20. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r19.md` and `HEAD:.agent/last_block.md` both print blob `5f4c5fe15b5fb3cde78732097d4a52af94be45f9`, reproduced directly; `sha256sum .agent/authored/f112-r19.md` reproduced `29563a53dd4fd4568249231d1242c059d2566531a1d8ccde9688f72bed8c1fcc` exactly as the handback claimed, and `wc -l` reproduced 336. THE PLAN REPLACEMENT AT C2 HELD BYTE-IDENTICAL: PLAN19 extracted by delimiter from the committed authored file (2088 bytes) compared byte-for-byte in Python against `.agent/plan.md` at C2 — equal, 2088 bytes both sides; `wc -l .agent/plan.md` reproduced 44, the file ends WITHOUT a trailing newline, and `## Goal` / `## Next Steps` each occur exactly once. THE RECORD APPEND AT C1 (booking RECORD18) HELD BYTE-IDENTICAL: pre-append `.agent/live_review.md` measured 2284151 bytes at `c7d68c58`, RECORD18 measured 2614 bytes, appended as `content_bytes + b"\n" + RECORD18_bytes` (one newline), post-append measured 2286766 bytes exactly matching `2284151 + 1 + 2614`; the pre-append content is an exact byte prefix of the post-append content; the file still ends WITHOUT a trailing newline; the open set recomputed mechanically read 350 registered / 72 `Done:` / 278 open on both sides of the append, reproduced identically by the reviewer against the CURRENT ledger. THE INTEGRATION GATE ITSELF WAS INDEPENDENTLY RE-RUN BY THE REVIEWER, NOT TAKEN ON THE WORKER'S SUMMARY: `pytest.main(["-n", "auto", "-q"])` from the repository root, run by the reviewer directly, reproduced 19546 passed, 23 skipped, 0 failed, exit 0, in 149.46s — matching the worker's own branch-run reading (19546 passed / 23 skipped / 0 failed, exit 0) exactly, on a separate invocation with its own separate wall-clock measurement. Because the branch run alone already shows 0 failures, `branch_only = set(branch_failed) - set(base_failed)` is empty under ANY reading of the base set, which is the decisive fact for this verdict: no branch-only regression exists. The reviewer separately corroborated the worker's base-only attribution without repeating the full base-worktree run: the one `fixed_by_branch` id, `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`, was already independently classified identically (base-only, XDIST-FLAKE, serial-pass) at `.agent/gate_f110_r15/attribution.txt` item 2 on an unrelated feature branch — confirmed by the reviewer's own direct read of that file, not by the worker's citation alone — and the reviewer's own `git diff --name-only 5c28c674..HEAD -- packages/` reproduced the identical eight-file coupling set the worker reported (`config.py`, `context_compiler.py`, `decision_queue.py`, `escalation.py`, `pingpong_job.py`, `pingpong_loop.py`, `prompt_budget.py`, `task_granularity.py`), with the reviewer additionally reading that test's own imports (`json`, `os`, `subprocess`, `sys`, `pathlib` — stdlib only) to confirm it reaches no orchestration module F112 touched. G7 AND G8 RE-VERIFIED BY THE REVIEWER DIRECTLY: `git ls-files .agent/gate_f112_r19` lists exactly the 9 files the block named, 0 named `.log`; `git status --porcelain` reads empty; no `tmp/*` branch and no `.remedy-wt/f112-r19-base` worktree survive; `git diff --stat c7d68c58..cd3173fc -- packages/ apps/ tests/ docs/` is empty. NO NEW FINDING AND NONE RESOLVED: the open set is unmoved at 278 (350 registered, 72 `Done:`). Session 6's round 19 gate is accepted as the integration gate the feature owes before closure; round 20 opens the closure sequence (docs/roadmap/STATUS_closure_protocol.md) at precondition 6, the self-use queue.
<<<END RECORD19>>>

<<<BEGIN PLAN20>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
Acceptance re-verified round 18, integration gate PASSED round 19
(RECORD19: VERDICT PASS, booked this round, independently re-run by the
reviewer: branch suite 19546 passed / 23 skipped / 0 failed reproduced
directly). Round 20 opens the closure sequence
(docs/roadmap/STATUS_closure_protocol.md).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 20 books RECORD19, then opens closure precondition 6 (the
self-use queue, F257/F258): the queue holds no pending item
(`next_self_use_item()` is None), so this round calls
`self_use_generator.generate_and_append_if_empty` and reports the
result. No self-use job is planned or run this round.

## Next Steps

- New item generated: a later round runs it via `self_use_job` /
  `self_use_runner` to the approval gate, registers any findings
  `self_use_findings.describe_self_use_run_defects` reports, and sets
  `consumed_by` to F112 at closure.
- Generator also answers None: record `self-use NONE (queue exhausted)`
  and proceed without one.
- Either way: evidence job, review zip, STATUS line, PR per
  docs/roadmap/STATUS_closure_protocol.md.

## Risks

- Split children inherit the parent's full files_hint and re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap" / "proceed-overcap once" options are
  deliberately unbuilt (DECISION F112 D9).
- R-0767 stays OPEN on the model-routing seam this feature's config
  borrows from; unrelated to F112.
- `self_use_runner.run_next_self_use_item` refuses an unflagged fake
  provider (R-0767/R-0768 class) — a real provider must resolve first.
<<<END PLAN20>>>

Done when — the gates below, each RUN and each reported as ONE LINE in the
handback with its real exit code / real reading. Every gate runs at a
commit STRICTLY EARLIER than C4.

G1 TRANSPORT — one digest comparison. Report `sha256sum` of the committed
   `.agent/authored/f112-r20.md` and its byte length. Report that
   `git rev-parse HEAD:.agent/authored/f112-r20.md` and
   `git rev-parse HEAD:.agent/last_block.md` print ONE blob id after C0b.
   Report `wc -l .agent/authored/f112-r20.md`.

G2 THE PLAN — extract PLAN20 by delimiter from the COMMITTED authored file.
   `cmp` (or a byte-equality check) against `.agent/plan.md` at C2 —
   must be equal. Report `wc -l .agent/plan.md` (must be under 50), that the
   file ends WITHOUT a trailing newline, `grep -c '^## Goal'` and
   `grep -c '^## Next Steps'` (each expected 1).

G3 THE RECORD APPEND — extract RECORD19 by delimiter from the committed
   authored file, report its byte length (expected 3996 — if it does not
   match, DECLARE the mismatch, do not silently adjust the arithmetic
   below). Report the arithmetic `2286766 + 1 + <len> = <total>` against
   the real post-append size, that pre-C1 content is an exact byte PREFIX
   of post-C1 content, and that the file still ends WITHOUT a trailing
   newline. NEGATIVE CONTROL: flip one byte inside the appended RECORD19
   slice, recompute, report the equality is now `False`. Report the count
   of lines matching `^Gate: F112 R19 — ` before C1 (expected 0) and after
   (expected 1). Report registered/`Done:`/open counts on BOTH sides of C1
   (expected UNMOVED at 350/72/278).

G4 THE SELF-USE GENERATION — report `pending_self_use_items()` and
   `next_self_use_item()` BEFORE calling the generator (expected empty
   tuple / `None`). Run the exact command in constraint 6. Report the
   printed `entry` value in full. Report `scripts/self_use_queue.json`'s
   item count before (6) and after (expected 7) by re-parsing the file
   directly (not by trusting the return value alone). Report the new
   item's `id` (expected `SU-007`), that its `consumed_by` is empty
   (PENDING), and its `provenance` string. Report that
   `load_self_use_queue()` re-parses the post-write file without raising.
   If the generator raises instead of returning (e.g.
   `SelfUseGenerationError`), STOP before C3's commit, do not paper over
   it, and report the full exception in the handback instead of this
   gate's expected reading — that is a valid, honestly-reported outcome
   of this round, not a defect in the block.

G5 THE TREE AND THE COMMITS — `git status --porcelain` immediately before
   C4 is staged — EMPTY. `git diff --stat 3b7a3e18..<C3> -- packages/ apps/
   tests/ docs/` — must be EMPTY. PER-COMMIT INSERTIONS (the `+` column
   only) for C0a through C3, each confirmed under 500 by `git show --stat`.

Handback: rewrite `.agent/handoff.md` in full — feature and round, SESSION
number, branch, base and head SHAs, the per-commit changed-files table with
its `+/-` column, ONE line per gate above with its real reading, the
item-status table AGENTS.md mandates covering every C-commit and every
gate, deviations, the open-findings count (expected 278, unmoved), the next
expected action (plan and run SU-007 via `self_use_job`/`self_use_runner`
in the following round, per PLAN20's Next Steps). It has NO length cap.
State plainly what the generator returned. Do not write a `Done:` or
`Gate:` paragraph anywhere beyond applying RECORD19 verbatim — the VERDICT
on THIS round is the reviewer's, not yours. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report
the outcome; create NO pull request, merge nothing.
══END BLOCK══
