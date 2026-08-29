# STEP 24 — F033 Hunk-level diff approval (SESSION 6, round 24; the soft limit is round 25)

Goal: retire R-0747's false sentence from the SECOND file it landed in, and wire
the last hop — `pingpong_job.py` holds the job, so it reads the task's recorded
decision and hands it to the loop. After this round the feature's functional
scope is complete.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r24.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN24.
4. C2: append slice RECORD24 to `.agent/live_review.md` — books the round 23
   PASS and REGISTERS R-0748.
5. C3: append slice SLIPS24 to `.agent/prose_slips.md`.
6. C4: SPEC A — the R-0748 repair, pair PAIR-DOC, and in the SAME commit the
   `Landed: R-0748` line of SPEC A3.
7. C5: SPEC B — the job-level wiring in `packages/orchestration/pingpong_job.py`.
8. C6: SPEC C — the new test file.
9. C7: rewrite `.agent/handoff.md` as the handback.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r24.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    tests/orchestration/test_builder_prompt_hunk_rejections.py
    packages/orchestration/pingpong_job.py
    tests/orchestration/test_pingpong_job_hunk_ledger.py
    .agent/handoff.md

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `c9dd471f`, this round's base.

- THE IDENTIFIERS ALIGN, and this is the fact the whole round rests on.
  `pingpong_job.py` line 2250 passes `_task_stream_dir(job.job_id, task.task_id)`,
  and that helper returns `.../evidence/task_runs/<task_id>/`. `build_diff_view`
  accepts a `task_id` only when it is a member of `list_task_run_ids(root)` —
  the real directory listing under `task_runs/` — and records it into the view
  envelope. So the `task_id` on a recorded decision IS `task.task_id`, and a
  lookup keyed by `task.task_id` can match. Had it not matched, this wiring
  would have been a call that always returned an empty ledger while looking
  correct, which is why the reading was taken before the round was written.
- `DIFF_SCOPE_JOB` is the literal `"job"`. When the operator decides at JOB
  scope rather than on one task run, `_dispatch_approve_hunks` records under
  that sentinel instead of a task id, so a per-task lookup will not find it.
  SPEC B2 documents that boundary rather than papering over it.
- `job.metadata` is the mapping both doors write into, and
  `load_latest_hunk_ledger_from_metadata` takes exactly that mapping.
- There is NO `tests/orchestration/test_pingpong_job.py`. The nearest neighbour
  is `test_job_task_runner.py`. SPEC C therefore adds a focused new file, the
  way `test_builder_prompt_hunk_rejections.py` sits beside
  `test_builder_prompt_golden.py`.
- The FROM span of PAIR-DOC occurs EXACTLY ONCE in its file, measured at
  `c9dd471f`: 423 bytes over 6 lines.

## SPEC A — the R-0748 repair

A1. Apply PAIR-DOC below to
`tests/orchestration/test_builder_prompt_hunk_rejections.py`. It is a REWRITE,
not an append: the reviewer ran the containment test at `c9dd471f` and the
result is `TO contains FROM: false`, so the obligation is FROM 0x and TO 1x in
the file after the commit. Report both counts.

A2. Do NOT touch the superseding comment block the previous round appended lower
in that file. It corrected the FIRST half of this paragraph honestly and under an
append-only obligation; PAIR-DOC retires the SECOND half, which is the false one,
and the two do not conflict. Leaving that block is not a defect and removing it
would delete an honest record of how the file got here.

A3. In the SAME commit append to `.agent/live_review.md` exactly one line:

    Landed: R-0748 — the false persists-no-decision clause is retired from the acceptance test's module docstring, tests/orchestration/test_builder_prompt_hunk_rejections.py, C4 of round 24.

Write NO `Done:` paragraph.

## SPEC B — the job-level wiring in `packages/orchestration/pingpong_job.py`

B1. Add ONE small module-level helper taking the job and the task and returning
the ledger of that task's latest recorded hunk decision, by delegating to
`load_latest_hunk_ledger_from_metadata` with `job.metadata` and `task.task_id`.
It exists as a named function rather than an inline expression so it can be
TESTED — an inline call at a site only a full job run reaches would be provable
only by its shape, and a gate over a call's shape is not a gate over its truth.

B2. It is TOTAL: a job without usable `metadata`, or a task without a usable
`task_id`, yields an EMPTY ledger and raises nothing. ONE structural guard; do
not nest a second inside it. Document in the idiom BOTH deliberate boundaries:
  (i) it looks up TASK-SCOPED decisions only. A decision recorded at JOB scope
      lands under the `DIFF_SCOPE_JOB` sentinel `"job"` rather than a task id,
      and is deliberately NOT quoted into any one task's prompt, because it was
      never attributed to one. The reviewer measured at `c9dd471f` that this
      holds by the id comparison alone, and with it the one collision it admits:
      a task whose own `task_id` were literally `"job"` WOULD match a job-scoped
      record. Say so in the same paragraph rather than leaving it for a reader
      to find. Do not add a guard against it — the sentinel and the task-id
      space are the write door's to separate, not this helper's, and a guard
      here would put that decision in two places.
  (ii) an empty ledger is the honest answer for "no decision recorded", is not
      an error, and is indistinguishable from an unreadable job on purpose —
      both mean there is nothing of the operator's to quote.

B3. Pass its result as `hunk_ledger=` at the `run_pingpong` call in this module.
Change nothing else about that call.

B4. Import `load_latest_hunk_ledger_from_metadata` the way this module already
imports its `packages.orchestration` dependencies at that site. If the
surrounding code imports inside the function, follow that; do not convert an
existing local-import style to module level, and do not add a module-level
import that ruff will then reorder across unrelated lines.

## SPEC C — `tests/orchestration/test_pingpong_job_hunk_ledger.py`

New file. It tests the HELPER's truth, not the call site's shape.

C1. A job whose `metadata` carries a decision recorded for a task yields that
task's ledger, and a rejection reason with leading spaces, an interior blank
line and a tab survives into it BYTE FOR BYTE. Use a simple fake job and task —
two small objects with the attributes the helper reads — rather than
constructing a real job.
C2. Composed through: feeding that ledger to `compose_builder_prompt` puts the
same reason in the prompt as an exact substring. This is the link from the job
to the prompt, and it is the round's point.
C3. A decision recorded for a DIFFERENT task is not returned.
C4. A decision recorded at JOB scope — `task_id` the literal `"job"` — is NOT
returned for a task whose own id differs. This is B2(i) measured rather than
merely documented.
C5. Totality: a job with no metadata, metadata that is not a mapping, no
decisions key, a task with no `task_id`, and a job whose `metadata` attribute
raises on access — each yields an empty ledger and raises nothing.
C6. The call site IS wired: by AST over `packages/orchestration/pingpong_job.py`,
the `run_pingpong` call passes a `hunk_ledger` keyword. This is a SHAPE check and
the block says so plainly — C1 to C5 are what prove the behaviour; this one only
prevents the helper being shipped unreferenced.

## Slice PLAN24 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file.

<<<BEGIN PLAN24
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 6 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| T002 decision core, subset apply, ledger, the door | done | rounds 6-15 |
| T003 partial truth on all three surfaces, R-0738 | done | rounds 16-19 |
| rejections rendered verbatim as repair findings | done | round 20 |
| that renderer reaches the builder prompt as a segment | done | round 21 |
| R-0747, and the inverse of the ledger export | done | round 22 |
| the stored decision selected, and forwarded by the loop | done | round 23 |
| R-0748, and the job-level caller supplies the ledger | open | this round |
| R-0745, the door's transitive import closure | open | not scheduled |
| the operator docs for `patch approve-hunks` | open | not scheduled |
| the integration gate round, then closure | open | not scheduled |

## Next Steps
1. This round retires R-0747's false sentence from the second file it reached,
   and wires `packages/orchestration/pingpong_job.py` — the one place holding
   the job — to read the task's decision and hand it to the loop. That
   completes the feature's FUNCTIONAL scope.
2. THE SOFT LIMIT IS ROUND 25 AND THE REMAINING WORK DOES NOT FIT IN IT.
   Outstanding: R-0745, the `docs/` operator description no round has yet been
   allowed a path for, the integration-gate round, and the two-round closure
   sequence. That is four to five rounds against one.
3. The session-6 handoff therefore carries the operator scope report operator
   amendment amend0827 rule 6 requires, with a proposal. It is a DOCUMENTED
   PROPOSAL and is never executed on the reviewer's own authority.
4. No pull request exists and none should be created before the closure
   sequence, which is where docs/agents/split_workflow.md rules it.

## Risks
- R-0745 is open against the write door's import closure and is unscheduled. It
  is not a blocker for the functional scope but it is a block condition at
  closure, so the scope report must name it explicitly.
<<<END PLAN24

## Slice RECORD24 — appended to `.agent/live_review.md`

Two paragraphs, blank-line separated.

<<<BEGIN RECORD24
Gate: F033 R23 — A STORED DECISION REACHES THE REAL LOOP'S COMPOSED PROMPT. THE ROUND PASSED. This entry books, under operator amendment amend0827-process-diet rule 1, the verdict the reviewer reached at `c9dd471f`. All eight gates were re-executed by the reviewer from scripts of its own. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r23.md` against the reviewer's own pre-emission original was SILENT, as was the comparison against `.agent/last_block.md`; the worker copied the file rather than retyping it. THE PLAN is byte-EQUAL to slice PLAN23 at 2690 bytes over 49 lines, under the 50-line cap. THE RECORD APPEND at `ce6c2866` reconstructs 1588340 plus one newline plus 6800 to 1595141, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 2, and a negative control at byte 1590053 — the reviewer's own offset, inside the FIRST appended paragraph's span 1588341 to 1593477 — REJECTED by both readers, which accepted the unflipped bytes. THE BLOCK'S OWN G3 BASE NUMERAL WAS WRONG AND THE WORKER CAUGHT IT: the block asserted 1588340's predecessor 1588184, which is the size at round 22's C2, not at `d0c86c2d`; round 22's own C3 appended the 156-byte `Landed: R-0747` line after that reading. The append FORM was applied unchanged and nothing on disk is wrong, so under amend0827 rule 2 this spends no id and is a dated line in `.agent/prose_slips.md`. THE LEDGER: registered 308 distinct UNMOVED; `Done:` 52 lines over 50 distinct to 53 over 51 with the ADDED resolved id exactly `R-0747`; `Landed:` 19 UNMOVED with `^Landed: R-0747 — ` still exactly 1 beside its new `Done:` paragraph; `^Gate: F033 R22 — ` 0 before and exactly 1 after; and the open set 258 to 257. THE CODE AGAINST THE SPEC: `python3 -m ruff check` exits 0 over all four changed files; by AST the reader is module-level and unprefixed, is named in the module's `Public API::` block, `run_pingpong` carries `hunk_ledger` keyword-only defaulting to `None`, and the ONE `compose_builder_prompt` call inside it forwards that name; and `open(` and `save_job` both still read 0 in `hunk_decision_record.py`, so DECISION F033 D4's standing property survives the round that gave that module a reader. THE SELECTION RULE WAS TRACED BY THE REVIEWER BRANCH BY BRANCH against SPEC A3 and is correct on every case: a first match takes the slot; any later record displaces an incumbent carrying no parseable stamp, which is how "if none parses the LAST wins" is spelled; an unparseable stamp never displaces a parseable one; and `>=` rather than `>` is what makes a tie resolve to the last recorded. THE MUTATIONS were re-run in the reviewer's own disposable worktree at C5 with its OWN anchors, each asserted UNIQUE and every file restored and proved byte-identical by sha256: control a REAL exit 0 at 39 passed; disabling the displacement comparison is exit 1 at 2 failed naming the latest-wins and the tie-resolves-to-last tests; removing the structural guard is exit 1 at 2 failed; and REMOVING THE FORWARDING from `run_pingpong` is exit 1 at exactly 1 failed, naming `test_a_rejection_reason_reaches_the_real_loops_composed_builder_prompt` — which is the mutation that proves the acceptance test is a genuine end to end and not a composer test in disguise. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the six orchestration suites 155 together, and `test_pingpong_cli.py` with the canary 214 together. THE STRUCTURE: eight single-parent commits over `d0c86c2d`..`c9dd471f` of 350, 256, 14, 4, 108, 29, 343 and 320 insertions, every one under 500; the path set to C5 EQUALS the declared change set in BOTH directions; and BOTH test appends satisfy ORDERED EQUALITY with ZERO deleted lines, at 188 and 155 added lines exactly equal to the appended suffix IN ORDER. THE WORKER DECLARED EIGHT DEVIATIONS AND EVERY ONE IS HONEST, THREE OF THEM IMPROVING ON THE ORDER: it caught the reviewer's stale base numeral, it reworded a draft docstring that had pushed `save_job` from 0 to 1 in a module whose zero count is a standing property, and it corrected `hunk_decision_record.py`'s module docstring where the round's own change had falsified it — that file said "THIS MODULE IS NOT TOTAL" and now says "THE TWO RECORDING DOORS ARE NOT TOTAL", naming the new reader as the exception. That edit was not itemised in the SPEC, and making it was right: leaving it would have landed exactly the class of false claim R-0747 registers. ONE READING THE REVIEWER TOOK THAT NO GATE ORDERED, recorded so a later reader knows the boundary: the selector compares two `datetime` values, so a record carrying a NAIVE stamp beside one carrying an AWARE stamp raises `TypeError` inside the structural guard and the answer is an EMPTY ledger rather than the aware record. It cannot arise from either door, which stamp with `datetime.now(timezone.utc)`, and totality holds, so it is not a finding.

- R-0748 — Low, THE FALSE SENTENCE R-0747 RETIRED FROM ONE FILE WAS STILL STANDING IN A SECOND, BECAUSE THE FIX AND ITS GATE WERE BOTH SCOPED TO ONE PATH. Raised by the reviewer at the F033 R23 gate. `tests/orchestration/test_builder_prompt_hunk_rejections.py`, landed at round 21 and measured at `c9dd471f`, carries a module-docstring paragraph reading "nothing here asserts that the RUN LOOP supplies a ledger. It does not yet: ... because `packages/orchestration/hunk_decision_record.py` persists no decision, so there is no route from a stored decision to the loop to test." The second half is the SAME false claim R-0747 registered, in the same words, and it is false for the same measured reason: that module writes each exported ledger onto `job.metadata` under `hunk_decisions` and `save_job` at the write door makes it durable. THIS IS A SECOND ID RATHER THAN EVIDENCE ADDED TO R-0747 because R-0747 was RESOLVED in the same round this instance was found, and reopening a resolved finding in an append-only record is worse than registering the instance that escaped it; the two are the same defect in two files and each resolution says so. WHY IT ESCAPED, which is the part worth keeping: R-0747's FIX clause named one file and its zero-gate counted the retired wording in that one file, so both were PATH-scoped while the defect was CLAIM-scoped. A sweep is only as wide as its search, and a gate that proves a sentence gone from the file you were thinking about proves nothing about the file you were not. The reviewer had the means to catch it — the same grep over `packages/`, `apps/`, `tests/` and `docs/` that found this instance would have found it a round earlier. WHY LOW: no behaviour is wrong and no test is weakened; the defect is a false explanatory paragraph in a test file, which a reader meets while trying to understand what the suite guarantees. THE FIRST HALF OF THAT PARAGRAPH IS ALREADY HONESTLY CORRECTED and must not be double-repaired: round 23 appended a superseding comment block saying the loop now DOES supply a ledger, under an append-only obligation the R23 block imposed, and that block is a correct record of how the file got here. FIX: rewrite the paragraph so the retired reason is gone rather than annotated, leaving the round-23 comment block untouched, and gate the retirement with a search over every path this repository keeps rather than over the one file being edited. Resolved when the wording "persists no decision" and the claim it carries appear nowhere under `packages/`, `apps/`, `tests/` or `docs/`.
<<<END RECORD24

## Slice SLIPS24 — appended to `.agent/prose_slips.md`

One paragraph.

<<<BEGIN SLIPS24
2026-08-29 · F033 R23 · The block's G3 ordered the record append reconstructed from a base of 1588184 bytes, which is `.agent/live_review.md` at round 22's C2 and not at `d0c86c2d`, because that round's own C3 appended a 156-byte `Landed:` line AFTER the reading was taken; the worker measured the true 1588340, applied the append form unchanged and declared it, and a base numeral for a file the PREVIOUS round wrote TWICE must be read at the round's actual base commit rather than at the commit whose gate first measured it.
<<<END SLIPS24

## Pair PAIR-DOC — `tests/orchestration/test_builder_prompt_hunk_rejections.py`

Containment test run by the reviewer at `c9dd471f`: `TO contains FROM: false`.
It is therefore a REWRITE, and the gate is FROM 0x and TO 1x after the commit.
The FROM occurs exactly once in the file, at 423 bytes over 6 lines.

<<<BEGIN PAIRDOC-FROM
DELIBERATE ABSENCE — nothing here asserts that the RUN LOOP supplies a ledger.
It does not yet: ``compose_builder_prompt``'s call site in ``run_pingpong`` is
unchanged this round because ``packages/orchestration/hunk_decision_record.py``
persists no decision, so there is no route from a stored decision to the loop to
test. A test asserting an end-to-end that does not exist would be a green gate
over a missing feature.
<<<END PAIRDOC-FROM

<<<BEGIN PAIRDOC-TO
THE RUN LOOP DOES SUPPLY A LEDGER, and the appended section below drives the real
loop to prove it. This paragraph once said the opposite and gave a reason that
was false when it was written: it claimed
``packages/orchestration/hunk_decision_record.py`` leaves no durable record,
when that module writes each exported ledger onto ``job.metadata`` under
``hunk_decisions`` and ``save_job`` at the write door makes the record durable.
That claim was finding R-0747 where it stood in ``pingpong_loop.py``, and
R-0748 here — one defect in two files, because the first fix and its gate were
both scoped to a path while the claim was not.
<<<END PAIRDOC-TO

## Constraints

1. Apply every slice and the pair BYTE FOR BYTE. If one looks wrong, apply it as
   written and declare the problem; never silently repair it.
2. PLAN24 is a FULL REWRITE. RECORD24 and SLIPS24 are APPENDS: measured at
   `c9dd471f`, `.agent/live_review.md` is 1595141 bytes and
   `.agent/prose_slips.md` is 30807 bytes, and BOTH end with a newline, so each
   append is one blank-line separator then the slice. Re-measure both yourself
   before appending — the R23 block got one of these numbers wrong by taking it
   at the wrong commit, and the slip above is that lesson.
3. `.agent/live_review.md` is written by TWO commits: C2 appends RECORD24, C4
   appends the single `Landed:` line. G3's arithmetic is measured at C2 and
   G4's ledger readings at C4.
4. Do NOT delete or edit the `Landed: R-0747` line, the `Done: R-0747`
   paragraph, or the superseding comment block round 23 appended to the
   acceptance test file. The record and that file's history are append-only
   except for PAIR-DOC's own paragraph.
5. Touch no path outside the change set. In particular do NOT touch
   `apps/cli/commands/do_cmd.py`, `packages/orchestration/pingpong_loop.py` or
   anything under `docs/`.
6. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, process substitution, a heredoc nested in `bash -c`, and a shell
   line containing a brace with a quote inside it. Write scripts under
   `.remedy-wt/` and run them as `python3 -B <path>`; use `python3 -m ruff`.
   REAL exit codes come from `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with NO PIPE.
7. Destructive verification runs ONLY in a disposable `git worktree`, purged of
   `__pycache__`, under `python3 -B`. The primary checkout satisfies
   `git status --porcelain` empty at the handback.
8. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
9. G1 through G8 all run at C6, before the handback commit C7.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r24.md` and `cmp` it against
`.remedy-wt/f033-r24-block.md`. One reading.

G2 THE PROSE FILES. `.agent/plan.md` byte-EQUAL to PLAN24, under 50 lines,
holding `## Goal` and `Steps`. `.agent/prose_slips.md` reconstructs its measured
base plus one newline plus the byte length of SLIPS24 to its committed size;
report all three numbers, the base MEASURED and not taken from this block.

G3 THE RECORD APPEND, at C2. Reconstruct the MEASURED base plus one newline plus
the byte length of RECORD24 to the committed size. Prove the pre-commit blob a
byte PREFIX and the slice an exact SUFFIX. COUNT N in the script. Compare the
file's LAST N blank-line units against the slice's paragraphs IN ORDER. Flip one
byte inside the FIRST appended paragraph, report the offset, prove it in span,
and show BOTH readers reject the flipped bytes and accept the unflipped ones.

G4 THE LEDGER, at `c9dd471f`, at C2 and at C4: registered 308 distinct going to
309 with the ADDED id exactly `R-0748`; `^Done: R-\d+ — ` 53 lines over 51
distinct UNMOVED at all three; `^Landed: ` 19 going to 20 with
`^Landed: R-0748 — ` exactly 1 at C4 and 0 before; `^Gate: F033 R23 — ` 0 before
and exactly 1 after; and the open set 257 going to 258.

G5 THE PAIR. After C4, in
`tests/orchestration/test_builder_prompt_hunk_rejections.py`: the PAIRDOC-FROM
text occurs 0 times and the PAIRDOC-TO text exactly 1 time. Report both counts.
THE SWEEP, and it is the point of R-0748's fix: over ALL of `packages/`,
`apps/`, `tests/` and `docs/`, the string `persists no decision` occurs 0 times
and the string `persists NOTHING` occurs 0 times. Report the command and both
counts. Search those four trees, not one file.

G6 THE CODE AGAINST THE SPEC, at C6. `python3 -m ruff check` exits 0 over both
changed production and test files. By AST over
`packages/orchestration/pingpong_job.py`: the new helper is defined at module
level, and the `run_pingpong` call passes a `hunk_ledger` keyword. Show by
RUNNING the shipped helper that a fake job carrying a recorded decision for a
task yields a ledger whose rejection reason is byte-identical to what was stored.

G7 MUTATION RED-PROOFS, in a disposable worktree at C6. UNMUTATED CONTROL FIRST,
its REAL exit code and pass count reported beside every mutation. Each anchor
shown to occur EXACTLY ONCE; restore and prove byte-identical by sha256 after
each.
  (i) make the helper ignore the task and use a fixed id — C3 or C4 must go RED.
  (ii) remove SPEC B2's structural guard — the totality tests must go RED. If it
       reddens nothing, SAY SO.
  (iii) stop passing `hunk_ledger` at the `run_pingpong` call — C6's wiring
       check must go RED.
Report the failing test NAMES.

G8 SUITES AND STRUCTURE, at C6. SERIALLY, each with REAL exit code and pass
count: the new test file; `test_builder_prompt_hunk_rejections.py`;
`test_hunk_decision_record.py`; `test_job_task_runner.py`; `test_pingpong.py`;
and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. Then
`git status --porcelain` EMPTY; per-commit insertions from C0a through C6 each
under 500; and the path set over `c9dd471f`..C6 equal to the change set minus
`.agent/handoff.md` in BOTH directions.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, SESSION 6 of F033, branch, commit SHAs, changed-files table, one line per
gate G1 through G8 with its REAL exit code, the open-findings count, an
item-status table covering every Bundle and SPEC item, every deviation, and the
next expected action. No length cap. If any gate is RED, do not repair on your
own initiative: report it and stop.
