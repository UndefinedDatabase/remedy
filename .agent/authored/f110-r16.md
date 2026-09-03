── STEP F110 CLOSURE ROUND 1 — self-use precondition + checklist ruling ──────
Round 16 · SESSION 5 of F110 · base `1d1a82e1` (F110 R15 C4)

Goal:
  Book round 15's PASS verdict. Run closure precondition 6's self-use item for
  real, through the shipped generator and runner, mirroring F109 R19's own
  precedent commit `9ee3ab57` exactly (dest_dir, budgets, evidence shape).
  Author DECISION F110 D6 ruling on DECISION F110 D1's consolidation-pass
  obligation: the pass runs (a genuine read of all 37 items for merge
  candidates), finds two real candidates, and performs NEITHER, because
  renumbering would falsify roughly 2,013 existing by-number citations of
  docs/agents/planner_reviewer_prompt.md section 3 that the append-only ledger
  forbids correcting. This is closure round 1 of what is now a THREE-round
  closure sequence (round 17: findings + evidence job + review zip + feature
  file Built State; round 18: STATUS/README/PR) — plan.md's earlier estimate
  of two rounds undercounted the self-use and consolidation work; that
  correction is itself part of PLAN16 below.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f110-r16.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   apply PLAN16 to `.agent/plan.md`
  C2   append RECORD16 to `.agent/live_review.md`, DECISION16 to
       `.agent/decisions.md`, and SLIPS16 to `.agent/prose_slips.md`
  C3   the self-use run: generate, plan, RUN (never promoted, never faked),
       land the evidence under `.agent/selfuse_f110/`
  C4   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f110-r16.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/decisions.md`
  `.agent/prose_slips.md`
  `.agent/selfuse_f110/` (created by this round; the files constraint 6 lists)
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/` or `docs/` is touched BY THIS
  ROUND'S OWN COMMITS. The self-use run itself operates in ITS OWN isolated
  job worktree (created and managed by `self_use_runner`/`pingpong_job`, e.g.
  `.remedy-wt/job-<id>`) exactly as F109 R19's precedent shows — that
  worktree's own commits, if any, are the SELF-USE JOB's business, not this
  round's, are never merged or promoted, and are not part of this change set.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE — never edit, retype or
     re-wrap one. If a slice looks wrong, apply it anyway and DECLARE the
     problem in the handback.
  2. `.agent/STOP` is read FROM DISK before the first commit and again before
     C4. If it exists at either reading: finish the commit in hand, write the
     handback, push, and stop.
  3. Slices are transported, not typed: C0a is `shutil.copyfile` from
     `remedy-review-r9-scratch/f110-r16.md`; every slice is EXTRACTED from the
     COMMITTED `.agent/authored/f110-r16.md` by locating its `<<<BEGIN X>>>`
     and `<<<END X>>>` marker lines with `list.index` and joining the lines
     BETWEEN them, markers excluded. Nothing is taken from this prompt.
  4. NEWLINE CONVENTION, THE TARGET WINS: `.agent/plan.md` ends WITH exactly
     one trailing newline and the PLAN16 extraction carries none, so the
     applied file is the extraction PLUS that one byte. `.agent/live_review.md`
     and `.agent/prose_slips.md` end WITHOUT a trailing newline and each
     append is TWO newlines + slice. `.agent/decisions.md` ENDS WITH a
     trailing newline (measured by the reviewer: base is 738004 bytes, ends
     in a single `\n`) and its OWN convention differs from the other two
     record files: the append is ONE newline + DECISION16 (DECISION16 itself
     already ends with its own trailing newline, so the applied file's total
     tail is the base's final paragraph, one blank line, then the new
     DECISION heading through its own closing sentence and trailing newline —
     matching the D4-to-D5 boundary the reviewer read on disk: the prior
     paragraph's final period, then a blank line, then the next `## DECISION`
     heading).
  5. Do NOT run `ruff`, `npm`, or any formatter — this round's own commits
     write no `.py` file (the self-use run's OWN job worktree is a separate
     matter, governed by that job's own acceptance text, not by this block).
  6. THE SELF-USE STEP (C3) FOLLOWS F109 R19 C3's PRECEDENT EXACTLY — read
     `git show 9ee3ab57` yourself before writing any code, and mirror its
     shape with `f110`/`F110` in place of `f109`/`F109`:
       a. Print `.agent/STOP` existence (must be False; if True, stop here
          per constraint 2).
       b. `packages.orchestration.self_use_queue.load_self_use_queue()`,
          print every entry's id/consumed_by/title, and
          `pending_self_use_items()` / `next_self_use_item()` BEFORE any
          change (expect 0 pending, `None`).
       c. Call `packages.orchestration.self_use_generator.generate_and_append_if_empty()`
          with no arguments. Print the returned `SelfUseQueueEntry` in full.
          If it returns `None` (Tier 1 found nothing eligible either): STOP,
          write `self-use NONE (queue exhausted)` in the handback exactly as
          STATUS_closure_protocol.md precondition 6 names it, and do not
          attempt a job run — report this as a DEVIATION, not a failure, and
          proceed to C4.
       d. Re-read `pending_self_use_items()` / `next_self_use_item()` AFTER
          generation and print them (expect 1 pending, the new entry).
       e. Call `packages.orchestration.self_use_runner.run_next_self_use_item(
          dest_dir=Path('.remedy-wt/selfuse-f110-run'), repo_path='.')` with
          NO `builder_name`/`reviewer_name` override and the DEFAULT budgets
          (max_provider_calls=6, max_cost_usd=0.50, max_tasks=1) — the same
          call shape F109 R19 used. Print `resolve_role_config('builder')` and
          `resolve_role_config('reviewer')` immediately before the call, the
          elapsed wall-clock seconds, and every field of the returned
          `(entry, job_file_path, JobPlan)` tuple that F109's `run.txt`
          printed (job_id, status, error, execution_config, isolation_mode,
          worktree_path, worktree_cleanup_status/_error, every task's fields).
       f. Call `packages.orchestration.self_use_findings.describe_self_use_run_defects(plan)`
          and print the tuple length plus each string verbatim between
          `--- DEFECT N BEGIN ---` / `--- DEFECT N END ---` markers, exactly
          as F109's `run.txt` does. Do NOT author `.agent/live_review.md`
          finding text for these yourself — that is round 17's, per section 4
          item 4 (only reviewer-authored text sets a registration); this round
          only RECORDS the defect strings verbatim for round 17 to consume.
       g. Copy the job markdown file from the run's `dest_dir` to
          `.agent/selfuse_f110/<ENTRY_ID>.md` with `shutil.copyfile`, and
          print BOTH sha256 digests (source, copied) proving byte-identity —
          the same proof F109's `run.txt` STEP 5 shows.
       h. Write the ENTIRE transcript above — every printed value, in the
          order printed — to `.agent/selfuse_f110/run.txt`. Commit both files
          in C3.
       i. Delete the run's OWN `dest_dir` (`.remedy-wt/selfuse-f110-run`) by
          its exact path after the copy in (g); do NOT touch
          `JobPlan.worktree_path` (the job's own isolated worktree under
          `.remedy-wt/job-<id>`) — it is retained by the product itself,
          exactly as F109 R19's precedent left its own worktrees untouched.
       j. `SU-005` is NOT consumed by this round: `consumed_by` for the new
          entry stays the empty string in `scripts/self_use_queue.json`.
          Setting it belongs to round 18's closure commit
          (STATUS_closure_protocol.md precondition 6), and this round's own
          change set does not list `scripts/self_use_queue.json` at all —
          if the generator's own `append_generated_item` call writes to it
          (it does, by design), that file's change IS necessarily part of
          this round's diff even though it is not separately listed above;
          report it honestly in the handback rather than pretending it did
          not happen.
  7. A `blocked` job status (the normal approval-gate outcome per
     `self_use_runner`'s own docstring) is NOT a round failure and is NOT
     "declared" as a deviation — report it as the measured OUTCOME it is,
     exactly as F109 R19's own handback did.

DECISION F110 D6's OWN MEASUREMENT, taken by the reviewer before this block
was authored (re-verify only if the branch has moved — it has not, since
round 15 changed no code): a mechanical scan of the checklist's by-number
citation forms across `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/prose_slips.md`, `.agent/candidates.md` and every file under
`.agent/authored/` found approximately 2,013 total citations and 0 under
docs/; item 20 alone carries roughly 220 and item 30 roughly 243. DECISION16
below states this measurement; do not re-run it, it is prose, not a gate.

<<<BEGIN PLAN16>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 16, session 5 — CLOSURE ROUND 1: THE SELF-USE PRECONDITION AND THE
CHECKLIST-CONSOLIDATION RULING. Round 15's PASS verdict (the integration
gate: branch clean, both base-only failures attributed to the XDIST-FLAKE
class, no blocker) is booked. Closure precondition 6's self-use item is
generated (the queue is exhausted at 0 pending), planned and RUN for real
through the shipped generator and runner, mirroring F109 R19's own
precedent exactly — never promoted, never faked. DECISION F110 D6 rules on
the section-3 consolidation pass DECISION F110 D1 committed to: it ran,
found two real merge candidates, and performed neither, because
renumbering would falsify roughly 2,013 existing by-number citations the
append-only ledger forbids correcting; the checklist stays at 37 items,
amend0827 rule 4's "same length" branch.

## Next Steps

- Round 17: register the self-use run's defects (if any) as findings, run
  the evidence job and build a FRESH review zip, and give
  `docs/roadmap/features/T3_F110.md` its Built State section plus the
  Design/Task-slicing bullet updates.
- Round 18: the closure commit — the authored STATUS line, the README
  capability sync in the same commit, the self-use item's `consumed_by`
  set to `F110`, and the PR.

## Risks

- The self-use run may land `blocked` at its own approval gate (F109's
  SU-005 did) — a normal outcome per `self_use_runner`'s own docstring,
  not a failure of this round; its defects route to round 17's findings.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN16>>>

<<<BEGIN RECORD16>>>
Gate: F110 R15 — the round 15 entry. VERDICT PASS (GREEN, no blocker), over the range `970ffc27..f14b0d34` plus the handback commit `1d1a82e1`. THE ROUND RAN THE TIER-3 INTEGRATION GATE THIS FEATURE OWES BEFORE CLOSURE, per docs/agents/integration_gate.md steps 1-5, and changed no code: `git diff --stat 970ffc27..f14b0d34 -- packages/ apps/ tests/ docs/` is EMPTY, reproduced by the reviewer directly. THE TRANSPORT PROOF REACHED THE REVIEWER'S OWN BYTES: one sha256 digest `754dbb5c2d40cd2577ee1e85722e55fe5851f4251093d7023c191f8f046dbd3e`, reproduced by the reviewer against the scratch original, the committed `.agent/authored/f110-r15.md` and the mirror `.agent/last_block.md`, all three identical; `wc -l` on the authored file is 307, matching the worker's own reading. EVERY SLICE IS BYTE-EXACT, REPRODUCED INDEPENDENTLY: `.agent/plan.md` is 41 lines, `## Goal` and `## Next Steps` each occurring once; `.agent/live_review.md` is `2222266 + 2 + 6737 = 2229003` against a real 2229003, base an exact byte prefix, still ending without a trailing newline; `.agent/prose_slips.md` is `64121 + 2 + 928 = 65049` against a real 65049, same shape. THE OPEN SET, recomputed by the reviewer directly from the committed ledger: 350 unique registered ids, 72 unique resolved across 74 `Done:` lines (the `R-0721`/`R-0725` double pair), open = 278; `R-0767` is IN that set and `R-0789` is OUT of it, both reproduced. THE SUITE NUMBERS WERE CROSS-CHECKED, NOT MERELY READ: the reviewer's own `pytest --collect-only -q` at this round's HEAD (run before the round was delegated) answered 19510 tests, and 19487 passed + 23 skipped = 19510 exactly, so the branch run's own arithmetic closes against an independently-taken collection count. BOTH BASE-ONLY FAILURES WERE REPRODUCED BY THE REVIEWER, SERIALLY, ON THE PRIMARY CHECKOUT AT THE BRANCH HEAD: `tests/orchestration/test_diff_parser.py::test_the_huge_diff_parses_inside_the_recorded_perf_budget` and `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup` both PASS together in 0.55s, consistent with the XDIST-FLAKE classification (a fixed wall-clock ceiling and an unscoped `pgrep` pattern, neither reaching `model_routing.py`, `config.py` or `role_config.py`) and inconsistent with a real base-commit defect. PARITY WAS MEASURED AS AN EVENT, per R-0444, and the reviewer's own reading of `parity_mtime.txt` shows all four `apps/ui/dist` files' before/after mtimes identical and outside the run window — PARITY HOLDS, independently read. PER-COMMIT INSERTIONS, reproduced cell for cell against the handback's own `## Commits` table: `298a1580` 307, `42976190` 234, `fb111342` 17, `8a45ea10` 8, `f14b0d34` 321 — every one under 500 and every one matching. A STALL WAS REPORTED MID-ROUND, BY THE REVIEWER, AND WAS WRONG: byte-growth stagnation in a log file polled from outside the process is not a liveness signal on its own — this run's log evidently buffered rather than flushing continuously, so a near-final read looked identical to a hung one; the worker's own investigation, corroborated here, found the run had already completed cleanly (fresh completion-artifact timestamps, a matching wall-clock reading, an ordinary tail with full tracebacks, zero live processes) and took no corrective action, correctly. THE LESSON IS RECORDED IN `.agent/prose_slips.md` THIS ROUND, not against the worker's conduct, which was correct throughout. NO CODE PATH WAS TOUCHED and `git diff --stat` over `docs/` is also EMPTY. NO FINDING IS OWED BY THIS ROUND.
<<<END RECORD16>>>

<<<BEGIN DECISION16>>>
## DECISION F110 D6 (2026-09-03, F110 R16) — the section 3 consolidation pass DECISION F110 D1 ordered cannot renumber the checklist, and none is performed

CONTEXT. DECISION F110 D1 committed this closure sequence to running one consolidation pass over the pre-emission checklist of docs/agents/planner_reviewer_prompt.md section 3, against amend0827 rule 4's requirement that the list come out "the SAME LENGTH OR SHORTER" than the 37 items it held on 2026-08-27. The pass was run at this round: every one of the 37 items was read for a genuine merge candidate, and two real ones were found — items 11, 16 and 32 state the identical rule (no hand-counted numeral about the block's own parts) over three different surfaces (a convention paragraph, a heading or quantifying sentence, and a gate or constraint), and items 4 and 15 split one rule (an APPEND pair requires containment) from its verification method (a mechanical, never-by-eye test) across two items that each explicitly name the other as its only reason to exist separately.

MEASURED. Both merges would RENUMBER every item after the earliest one touched, because neither pair sits at the end of the list. Section 3 is cited BY ITEM NUMBER outside itself, in text this repository's own rules forbid rewriting: `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` (append-only, never rewritten or renumbered) and roughly 1,200 files under `.agent/authored/` (one committed block per historical round, never edited after landing). A mechanical scan of "section 3 item N" and "checklist item N" across those locations, run by the reviewer at this round, found approximately 2,013 such citations; zero exist anywhere under docs/. Individually, item 20 alone carries roughly 220 citations and item 30 roughly 243 — both sit AFTER item 16 and item 15 in the current numbering, so either merge would silently change what "item 20" and "item 30" mean in every one of those historical sentences, none of which can be corrected without violating the append-only rule those same sentences exist to enforce.

CHOSEN. The pass runs, finds two real merge candidates, and performs NEITHER, because section 3 is a rare case where the numbered position IS the reference and not merely a locator: a merge is safe here only when it touches solely the LAST item of the list (nothing after it to renumber) or when it is written as an in-place widening paragraph under the EARLIER item's existing number — which is already how items 9, 14, 16, 18 and 20 have each absorbed later findings into themselves without ever renumbering. Items 11/16/32 and items 4/15 are not that shape: each is a genuinely separate, independently-cited surface rather than a later widening of an earlier one, so folding them together would have to delete a heading and shift every number after it. The list stays at 37 items — SAME LENGTH, which is the rule's OR clause, not its failure. F109's lessons that D1 also owed are on disk: `.agent/prose_slips.md` already carries F109's rounds 1, 2, 6, 7, 17, 18, 20 and 21; rounds 8 through 16 raised no reviewer-prose defect of the kind that file records.

ALTERNATIVE CONSIDERED AND REJECTED. Renumber anyway and treat the roughly 2,013 stale citations as accepted drift, on the theory that they are historical prose rather than live rules. Rejected because several are load-bearing explanations of WHY a specific finding was raised — `.agent/authored/f109-r2.md` names "section 3 item 32" as the rule a defect broke — and a reader resolving that citation against a renumbered document would attribute the wrong rule to a real, closed defect, which is a worse outcome than an unconsolidated list.

CONSEQUENCE. docs/agents/planner_reviewer_prompt.md section 3 is UNCHANGED by this round. DECISION F110 D1's obligation is discharged by this DECISION, not deferred: the pass ran, is recorded, and its answer is "no safe merge exists under current citation discipline," which amend0827 rule 4's own "SAME LENGTH OR SHORTER" wording already permits. A future amendment wishing to actually shrink the list would need either a citation-migration pass over `.agent/authored/` (which the append-only rule currently forbids) or a documented exception permitting it — neither exists today.

REVERSE by deleting this DECISION; F110 D1's obligation then reverts to open.
<<<END DECISION16>>>

<<<BEGIN SLIPS16>>>
2026-09-03 · F110 R15 (reviewer) · Polling a background pytest run's captured-output file for byte-growth was read as a liveness signal — three samples 90-180s apart showed the file frozen near 99% and were reported mid-round as "the base run appears hung." The run had, in fact, either already finished or was progressing normally behind a buffer that had not yet flushed; the worker's own investigation (fresh completion timestamps, a matching wall-clock reading between the run's meta file and pytest's self-report, an ordinary tail with tracebacks, zero live processes) found no hang and took no corrective action. THE LESSON: a captured log's byte count is evidence of I/O buffering, not of process liveness; check the run's own completion artifacts (a written end-timestamp, the process table) before reporting a stall, rather than sampling a log file's size. Reviewer-prose false alarm, nothing wrong on disk, no process was harmed; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS16>>>

Done when — the gates below, within the amend0827 rule 5 budget, each RUN and
each reported as ONE LINE in the handback with its real exit code. Every gate
runs at a commit STRICTLY EARLIER than C4, the commit that writes the
handback.

G1 TRANSPORT — one digest comparison.
   `cmp remedy-review-r9-scratch/f110-r16.md .agent/authored/f110-r16.md` —
   exit 0. `sha256sum` those two plus `.agent/last_block.md` — one digest,
   repeated. Report `wc -l .agent/authored/f110-r16.md`.

G2 THE PLAN — a byte-equality check of the plan slice, nothing more.
   Extract PLAN16 by delimiter index from the COMMITTED authored file. `cmp`
   the extraction PLUS ONE TRAILING NEWLINE against `.agent/plan.md` — exit 0;
   report the bare extraction's exit code beside it. Report `wc -l
   .agent/plan.md` (must be under 50), `grep -c '^## Goal'` and `grep -c '^##
   Next Steps'`.

G3 THE RECORD APPENDS — full byte forensics for `.agent/live_review.md` and
   `.agent/decisions.md` (amend0827 rule 5 reserves it for exactly these two
   plus production code); `.agent/prose_slips.md` gets the lighter
   byte-equality check only.
   For `.agent/live_review.md` and `.agent/decisions.md`: report the base size
   at `1d1a82e1`, the arithmetic `<base> + <separator bytes> + <slice bytes> =
   <total>` against the real size (separator is TWO newlines for
   live_review.md, ONE newline for decisions.md per constraint 4), that the
   pre-C2 content is an exact byte PREFIX, and the trailing-newline state
   (live_review.md: still none; decisions.md: still exactly one). SECOND
   READER for `.agent/live_review.md`: let N be the paragraph count your
   script COUNTS in RECORD16 — do not take N from this block — and compare
   the LAST N blank-line units of the whole file against RECORD16's N
   paragraphs IN ORDER; NEGATIVE CONTROL on RECORD16's FIRST paragraph (flip
   byte 0 in a COPY, confirm rejection). HEADER SHAPE: count of lines matching
   `Gate: F110 R15 — the round 15 entry.` BEFORE C2 (expected 0) and AFTER
   (expected 1). For `.agent/decisions.md`: count of lines matching `## DECISION
   F110 D6` BEFORE C2 (expected 0) and AFTER (expected 1).
   For `.agent/prose_slips.md`: `cmp` of (base + two newlines + SLIPS16)
   against the committed file — exit 0.
   THE OPEN SET, recomputed mechanically and never carried forward: unique
   registered ids, unique resolved ids (with the `Done:` LINE count beside
   it), the open total, and whether `R-0767` is IN the open set.

G4 THE SELF-USE RUN — report every value constraint 6 orders printed, as ONE
   block quoting `.agent/selfuse_f110/run.txt` verbatim (or a clear pointer to
   it plus the key numbers inline): the entry id generated, the job id, the
   final `JobPlan.status`, whether `describe_self_use_run_defects` returned
   any strings (and if so, quote them), the source/copied sha256 pair proving
   the evidence copy is byte-identical, and confirmation that
   `scripts/self_use_queue.json`'s new entry still has `consumed_by` equal to
   the empty string. Report `git status --porcelain` immediately after C3 is
   staged, BEFORE C4 — must show only the paths this round's own change set
   names (plus `scripts/self_use_queue.json`, per constraint 6j).

G5 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C4 is staged — EMPTY.
   `git diff --stat 1d1a82e1..<C3> -- packages/ apps/ tests/ docs/` — must be
   EMPTY (this round's own commits touch none of them; the self-use job's own
   worktree is not part of this diff by construction).
   `git worktree list` — no NEW worktree beyond the self-use job's own
   `.remedy-wt/job-<id>` (which the product retains, not this round);
   `ls -d .remedy-wt/selfuse-f110-run` — no such file (deleted per
   constraint 6i).
   PER-COMMIT INSERTIONS, the `+` column only (DECISION F104 D1), for every
   commit from C0a through C3, reported cell by cell against the handback's
   own `## Commits` table and each confirmed under 500.

Handback: rewrite `.agent/handoff.md` in full — feature and round, SESSION 5
of F110, branch, base and head SHAs, the per-commit changed-files table with
its `+/-` column, ONE line per gate above with its real exit code, the
item-status table AGENTS.md mandates, the deviations, the open-findings count,
the next expected action. It has NO length cap (amend0827 rule 3). Then `git
push -u origin feature/f110-model-routing-by-task-class`; create NO pull
request, merge nothing.
