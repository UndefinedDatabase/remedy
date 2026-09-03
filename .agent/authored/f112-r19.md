── STEP INTEGRATION GATE — F112 Prompt budget per task class ───────────────────
Round 19 · SESSION 6 of F112 · base `c7d68c58` (F112 R18 C5-fix, the tip of
feature/f112-prompt-budget-per-task-class)

Goal:
  Run the INTEGRATION GATE this feature owes before closure — the full suite on
  the branch and at the merge base, compared and attributed — and land its
  evidence under `.agent/gate_f112_r19/`. Round 18's PASS verdict is booked in
  the same round, as its first substantive commit (amend0827 rule 1).

  The procedure is `docs/agents/integration_gate.md`, steps 1-5. This block does
  NOT restate it (§3, verification tier 3); it supplies only this round's
  parameters, the repairs three OPEN findings require of it, and the gates.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r19.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD18 to `.agent/live_review.md`
  C2   apply PLAN19 to `.agent/plan.md`
  C3   the gate evidence: create `.agent/gate_f112_r19/` and commit the files
       G7 lists
  C4   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f112-r19.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `.agent/gate_f112_r19/` (created by this round; the files G7 lists)
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/` or `docs/` is touched. This round
  MEASURES the branch; it does not change it. A red gate is a HANDBACK, never a
  repair applied here — integration_gate.md step 4 makes a reproducible
  branch-only failure coupled to feature code a BLOCKER whose fix is its own
  reviewer-gated round.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE — never edit, retype or re-wrap
     one. If a slice looks wrong, apply it anyway and DECLARE the problem in the
     handback: a declared conflict is worth more than a silent repair.
  2. `.agent/STOP` is read FROM DISK before the first commit and again before
     C4. If it exists at either reading: finish the commit in hand, write the
     handback, push, and stop.
  3. TYPE each slice from THIS PROMPT'S OWN BYTES directly into
     `.agent/authored/f112-r19.md` at C0a — do not name any path under
     `.remedy-wt/` in a bash command; that permission is denied to workers this
     session and naming it will only cost you a turn. The reviewer holds its own
     scratch original separately and will run the transport comparison itself.
  4. `.agent/plan.md` ends WITHOUT a trailing newline in this feature's own
     convention, and PLAN19 is applied as an exact whole-file replacement with
     no trailing newline added. `.agent/live_review.md` also ends WITHOUT a
     trailing newline; append it as `content_bytes + b"\n" + RECORD18_bytes` —
     ONE newline, no blank line — which is the convention every F112 round
     since R14 has used and the one the R18 gate re-verified. If this disagrees
     with anything else you have seen for a DIFFERENT feature's rounds, follow
     THIS file's own established shape, which you confirm yourself before
     writing by reading the byte immediately before the append point.
  5. Do NOT run `ruff`, `npm`, or any formatter. This round writes no code.
  6. THE SANDBOX SHAPES HOW THE SUITE IS INVOKED. `VAR=x cmd`, `env VAR=x cmd`,
     `export VAR=x; cmd` and `cp` are all DENIED. So: invoke pytest AS A
     LIBRARY, `pytest.main(["-n", "auto", "-q"])`, with the working directory
     pinned per run; set `REMEDY_UI_NO_AUTO_BUILD` IN-PROCESS via `os.environ`
     for the BASE run only; and copy with
     `python3 -c "import shutil; shutil.copytree(a, b, symlinks=True)"`.
     Capture a real exit code by wrapping any shell gate as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. NEVER `cd` into a worktree for any
     purpose — it silently does not take effect in this sandbox and a mutation
     or a run issued after one can land in the PRIMARY checkout instead; address
     the worktree by ABSOLUTE path and use `cwd=` on `subprocess.run`, or pass
     an absolute rootdir to `pytest.main`.
  7. RUN LOGS ARE WRITTEN OUTSIDE THE PRIMARY REPO WORKTREE while a suite runs
     and COPIED IN only after that run has exited (R-0176: a log growing inside
     the repo changes the worktree digest mid-run and fails the
     manifest-identity ids as FALSE positives). Use the gitignored
     `.remedy-wt/gate-scratch-r19/` (create it with `os.makedirs`) — it is
     inside the repository but outside `git ls-files --others --exclude-standard`
     because `.remedy-wt/` is in `.gitignore`, which is what R-0176's rule
     actually requires. Evidence files carry `.txt` names and NEVER `.log` —
     `.gitignore` drops `*.log` silently and the review-zip guard rejects any
     `\.log$` member (R-0169).
  8. Every destructive or throwaway checkout is a `git worktree` and is removed
     by its EXACT path with `git worktree remove` plus `git worktree prune`, and
     the throwaway BRANCH is deleted. The primary checkout reads
     `git status --porcelain` EMPTY at every verdict. NEVER force-push, never
     work on `main`, create NO pull request, merge nothing.
  9. A sentence THIS ROUND makes stale, anywhere inside the change set, is
     repaired in the commit that falsifies it. One outside the change set is
     DECLARED in the handback and left alone.
  10. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md` and
      `docs/roadmap/features/T3_F112.md` are NOT touched. Nothing this round
      found needs any of them, and the change set forbids it.

THIS ROUND'S PARAMETERS, all measured by the reviewer at `c7d68c58`:
  BRANCH      `feature/f112-prompt-budget-per-task-class` at this round's C2
              tree (C0a-C2 touch only `.agent/`, so the code under test is the
              code at `c7d68c58`).
  MERGE BASE  `5c28c6741db2d9073fc75cd159d91037e0757fb0`, from
              `git merge-base main HEAD`.
  BASE TREE   a worktree at `.remedy-wt/f112-r19-base` created ON A THROWAWAY
              BRANCH — `git worktree add -b tmp/f112-base-gate
              .remedy-wt/f112-r19-base 5c28c6741db2d9073fc75cd159d91037e0757fb0`.
              A DETACHED base worktree fails the self-dogfood branch guard BY
              DESIGN (DECISION D3, F053 R2), so the branch is not optional.
  COLLECTION  `pytest --collect-only -q` answers 19569 tests on the branch.
  UI DIST     `apps/ui/dist/index.html` has mtime 1788057215.85 against a
              newest-file-under-`apps/ui/src` mtime of 1788057023.74, so the
              PRIMARY checkout's build is WARM and no cold build is owed there.
              G4 re-measures this rather than trusting it.
  UI SHIMS    `apps/ui/node_modules/.bin` holds 23 SYMLINKS.
  STALENESS   `_frontend_is_stale()` is `packages/orchestration/ui_server.py:3071`
              and returns True when ANY file under `apps/ui/src` has an mtime
              greater than `apps/ui/dist/index.html`'s.

THREE OPEN FINDINGS BIND THIS ROUND'S PROCEDURE. Each is a repair the literal
text of integration_gate.md does not yet carry, so the block carries it:
  R-0591 — `shutil.copytree` DEFAULTS to `symlinks=False`, which DEREFERENCES
    those 23 npm bin shims and CAUSES base-only failures the parity exists to
    prevent. Write `symlinks=True` EXPLICITLY on every copytree of
    `apps/ui/node_modules` and `apps/ui/dist`. Order the argument, not the
    function.
  R-0736 — `copytree` PRESERVES source mtimes while `git worktree add` stamps
    every checked-out file with the CHECKOUT time, so a byte-correct copied
    build is mtime-STALE: `_frontend_is_stale()` reads True in the base
    worktree, `REMEDY_UI_NO_AUTO_BUILD` then correctly suppresses the rebuild,
    the UI is never built, and every test reaching the door dies on
    `React UI not built.` — measured at 114 FAILED on the F033 R27 gate. AFTER
    copying, ADVANCE the mtimes of every file under the base worktree's
    `apps/ui/dist` past that worktree's own checkout time (e.g. `os.utime` set
    to the current time), and report `_frontend_is_stale()` read from INSIDE
    the base worktree as False BEFORE the base run starts. Nothing is rebuilt
    and nothing is faked: what is corrected is a timestamp the copy mechanism
    cannot carry across a fresh checkout.
  R-0590 — ATTRIBUTE BOTH COMPARISON SETS UNCONDITIONALLY. A gate that
    attributes `comm -23` only "if the parity claim went VOID" demands nothing
    in exactly the case where the ids still exist. Every id in `branch_only.txt`
    AND every id in `fixed_by_branch.txt` is attributed by direct evidence,
    whether parity holds or not. Compute the comparison as a Python SET
    DIFFERENCE (`comm` is unavailable through this session's guard for piped
    forms) — `branch_only = set(branch_failed) - set(base_failed)`,
    `fixed_by_branch = set(base_failed) - set(branch_failed)` — and say so.

TESTS ABSENT AT THE BASE ARE NOT REGRESSIONS. `5c28c674` predates several of
F112's own test files (`tests/orchestration/test_class_prompt_budget.py` among
them, and any other path this branch added under `tests/orchestration/`). If
any branch-only id belongs to a file absent at the base — prove absence with
`git cat-file -e 5c28c674:<path>` returning non-zero — classify it as a NEW
TEST, separately from any genuine regression, rather than as an attribution
target.

<<<BEGIN RECORD18>>>
Gate: F112 R18 — the round 18 entry, session 5's closing bookkeeping-and-reverification round (no production code). VERDICT PASS, over the range `92f773c6..c7d68c58` (commits C0a, C0b, C1, C2 — four real content commits — plus handback commit `12d882e6` and its same-round correction `c7d68c58`), independently reviewed by the reviewer at the start of session 6's round 19. NO PRODUCTION CODE MOVED: every changed path across all six commits is confirmed under `.agent/` only (`.agent/authored/f112-r18.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`); no `packages/`, `apps/`, `tests/`, `scripts/` or `docs/` path appears anywhere in the range. THE TRANSPORT HELD: `.agent/authored/f112-r18.md` and `.agent/last_block.md` compare byte-identical, `cmp` exit 0. THE LEDGER APPEND AT C1 HELD BYTE-IDENTICAL: `git show 788c7a0c -- .agent/live_review.md` reproduced RECORD17 appended to the prior tail exactly as authored, one blank line before it and the file ending in exactly one trailing newline. THE PLAN REPLACEMENT AT C2 HELD BYTE-IDENTICAL: `git show 9c37e9ff:.agent/plan.md` reproduced PLAN18 exactly, matching the authored blob (2375 bytes, 49 content lines, no trailing newline). THE ACCEPTANCE RE-VERIFICATION HELD, REPRODUCED INDEPENDENTLY A THIRD TIME BY THE REVIEWER ITSELF: `python3 -m pytest tests/orchestration/test_class_prompt_budget.py -q` reproduced at 24 passed; `python3 -m pytest tests/orchestration/test_context_compiler.py -q` reproduced at 69 passed; the same file narrowed with `-k` to `test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded or test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic` reproduced at 2 passed, 67 deselected; the canary `python3 -m pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed — all four numbers matching both the worker's own round 18 reading and RECORD17's prior one, `git status --porcelain` reading empty before and after. THE CORRECTION COMMIT `c7d68c58` CHECKED CLEAN: its corrected changed-files figures (`.agent/last_block.md` 32/48, `.agent/plan.md` 26/24) match `git show --stat` exactly for both `13f747a4` and `9c37e9ff`, and the round's own handoff discloses the double-commit and the write-once departure inline rather than silently rewriting history — a deviation the reviewer finds justified, since the alternative was a live self-referential `<C5 SHA>` placeholder left standing in the permanent record. NO NEW FINDING AND NONE RESOLVED: the open set is unmoved at 278 (350 registered, 72 `Done:`) on both sides of this append.
<<<END RECORD18>>>

<<<BEGIN PLAN19>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
Acceptance re-verified round 18 (RECORD18: VERDICT PASS, booked this
round). Round 19 opens session 6 at the integration gate.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 19, session 6 — books RECORD18 (round 18, VERDICT PASS) into the
ledger, then runs the integration gate (docs/agents/integration_gate.md):
full-suite branch run, base-worktree run with node_modules/dist parity
restored and mtime-corrected (R-0736), comparison, per-id attribution.
No production code touched. First of the two full-suite runs the
feature owes before closure.

## Next Steps

- If the gate PASSES cleanly: proceed to closure per
  docs/roadmap/STATUS_closure_protocol.md — evidence job, fresh review
  zip, the STATUS line, the PR — in session 6 or session 7.
- If the gate finds a reproducible branch-only regression coupled to
  feature code: STOP, hand back; the fix is its own reviewer-gated
  round, never folded into the gate round.

## Risks

- Split children inherit the parent's full files_hint and so re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap for this job" / "proceed-overcap once"
  options are deliberately unbuilt (DECISION F112 D9) — no audit/
  attended-mode seam exists anywhere in this codebase to hook them to.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- R-0736 (base-worktree mtime staleness) and R-0591 (copytree
  dereferencing symlinks) both bind this round's own base run; both are
  neutralized by constraint, not by code change.
<<<END PLAN19>>>

Done when — the gates below, within the amend0827 rule 5 budget, each RUN and
each reported as ONE LINE in the handback with its real exit code. Every gate
runs at a commit STRICTLY EARLIER than C4, the commit that writes the handback.

G1 TRANSPORT — one digest comparison, per amend0827 rule 5.
   Report `sha256sum` of the committed `.agent/authored/f112-r19.md` and its
   byte length. The reviewer holds its own scratch original of this exact text
   and will run the comparison independently; you are not asked to produce a
   second reading of it. Report that `git rev-parse
   HEAD:.agent/authored/f112-r19.md` and `git rev-parse
   HEAD:.agent/last_block.md` print ONE blob id after C0b (proving the mirror
   is byte-identical to the saved copy). Report `wc -l
   .agent/authored/f112-r19.md`.

G2 THE PLAN — a byte-equality check of the plan slice, and nothing more.
   Extract PLAN19 by delimiter from the COMMITTED authored file. `cmp` the
   extraction against `.agent/plan.md` at C2 — exit 0. Report
   `wc -l .agent/plan.md` (must be under 50, and the file must end WITHOUT a
   trailing newline per constraint 4), `grep -c '^## Goal'` and
   `grep -c '^## Next Steps'`, each expected 1.

G3 THE RECORD APPEND — full byte forensics, which amend0827 rule 5 reserves for
   exactly this target.
   `.agent/live_review.md`: base 2284151 bytes at `c7d68c58`, ending WITHOUT a
   newline. Append `\n` + RECORD18 (ONE newline, per constraint 4's stated
   convention for this file). Report the arithmetic
   `2284151 + 1 + <len(RECORD18)> = <total>` against the real post-append size,
   that the pre-C1 content is an exact byte PREFIX of the post-C1 content, and
   that the file still ends WITHOUT a trailing newline. NEGATIVE CONTROL: flip
   one byte at an offset inside the appended RECORD18 paragraph, recompute, and
   report the equality is now `False`. HEADER SHAPE (§3 item 26): report the
   count of lines matching `^Gate: F112 R18 — ` BEFORE C1 (expected 0) and
   AFTER C1 (expected 1).
   THE OPEN SET, recomputed mechanically and never carried forward: paragraphs
   matching `^- R-\d+ — ` reduced to UNIQUE ids, and lines matching
   `^Done: R-\d+ — ` reduced to UNIQUE ids, the set difference their open set.
   Report registered (expected UNMOVED at 350), unique `Done:` (expected
   UNMOVED at 72), the open total (expected UNMOVED at 278) — all measured on
   BOTH sides of C1, since this round registers no finding and resolves none.
   Report the count of lines matching `^Gate: F\d+ R\d+ — ` before (expected
   265) and after (expected 266) C1.

G4 STEP 1, THE BRANCH RUN. Assert the WARM-BUILD precondition FIRST and report
   both readings: `apps/ui/dist/index.html` exists, and its mtime exceeds the
   mtime of EVERY file under `apps/ui/src` (a cold or stale dist reddens one
   `tests/ui_server` id for a reason that has nothing to do with this branch).
   Then run the full suite from the repository root per integration_gate.md
   step 1, invoked as a library per constraint 6, with NO environment variable
   set. Report the raw tail, the exit code, the wall clock, and write the
   sorted `^FAILED` list to `branch_failed.txt` and the tail to
   `branch_run_tail.txt`. The reviewer's own reading at `c7d68c58` is in the
   handback of this round's review, not here: report yours as measured and
   compare it to nothing.

G5 STEP 2, THE BASE RUN. Create the base worktree exactly as THIS ROUND'S
   PARAMETERS specifies — on the throwaway branch, at the named merge base.
   Restore parity BEFORE the run, applying R-0591 and R-0736 as stated above,
   and report: the entry count copied for each of `apps/ui/node_modules` and
   `apps/ui/dist`; how many of those entries were SYMLINKS and that they were
   PRESERVED; and `_frontend_is_stale()` evaluated FROM INSIDE the base
   worktree, which must read False before the run starts. Then run the same
   suite there with `REMEDY_UI_NO_AUTO_BUILD` set in-process. Report the raw
   tail, exit code and wall clock; write `base_failed.txt` and
   `base_run_tail.txt`.
   PARITY AS AN EVENT, NOT AN OUTCOME (R-0444): record the mtime of EVERY file
   under the base worktree's `apps/ui/dist` immediately before and immediately
   after the run, report the run's wall-clock window, and state per file
   whether its mtime falls inside it. ANY mtime inside the window VOIDS the
   parity claim. A content digest may accompany that reading and NEVER
   replaces it, because equal content is consistent both with no rebuild and
   with a byte-identical one. Write it all to `parity_mtime.txt`.

G6 STEPS 3 AND 4, THE COMPARISON AND THE ATTRIBUTION.
   Compute `branch_only = sorted(set(branch_failed) - set(base_failed))` and
   `fixed_by_branch = sorted(set(base_failed) - set(branch_failed))` in Python,
   per R-0590's stated method, and write them to `branch_only.txt` and
   `fixed_by_branch.txt`. Report the line count of all four files.
   Classify every branch-only id absent at the base (per the NEW-TESTS
   paragraph above) into its own list before attributing anything else.
   ATTRIBUTE BOTH REMAINING SETS UNCONDITIONALLY, per R-0590 — not only when
   parity is void. For every remaining id in `branch_only.txt`: serially
   re-run that EXACT node id and classify per integration_gate.md step 4 —
   serial-pass is the xdist-flake class and is recorded, not a blocker;
   serial-fail is reproduced AT THE MERGE BASE before the feature is blamed;
   a reproducible branch-only failure coupled to F112 code is a BLOCKER, which
   means STOP and hand back. For every id in `fixed_by_branch.txt`: name the
   direct evidence for its class — the missing base artifact per id, or the
   branch commit that fixed it. An unattributed id in either set blocks the
   gate verdict. Write it all to `attribution.txt`. If both sets are empty
   after the new-test split, say so and attribute nothing: that is the honest
   discharge of this gate.

G7 THE EVIDENCE DIRECTORY. C3 creates `.agent/gate_f112_r19/` and commits
   exactly these files, all `.txt` and none `.log`, matching the file set
   `.agent/gate_f109_r17/` and `.agent/gate_f110_r15/` established:
   `gate_summary.txt`, `branch_run_tail.txt`, `branch_failed.txt`,
   `base_run_tail.txt`, `base_failed.txt`, `branch_only.txt`,
   `fixed_by_branch.txt`, `parity_mtime.txt`, `attribution.txt`.
   `gate_summary.txt` follows the shape of its `.agent/gate_f109_r17/`
   predecessor — the branch and base identifiers, then one block per
   integration_gate.md step, then the test-count delta and the cleanup note —
   and states that the VERDICT belongs to the reviewer. Report `ls -la` of the
   directory and `git ls-files .agent/gate_f112_r19` so the committed set is
   measured rather than claimed. Report the count of committed members whose
   name ends `.log` (expected 0).

G8 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C4 is staged — EMPTY.
   `git worktree list` — the base worktree does NOT survive; `git branch
   --list 'tmp/*'` — the throwaway branch does NOT survive; report
   `os.path.isdir('.remedy-wt/f112-r19-base')`, expected False. `git ls-files
   .remedy-wt` — EMPTY. `ls /home/decodeux/Repos/remedy/remedy.toml` — no such
   file.
   `git diff --stat c7d68c58..<C3> -- packages/ apps/ tests/ docs/` — must be
   EMPTY, which is the change set's "this round measures, it does not change"
   clause MEASURED.
   PER-COMMIT INSERTIONS, the `+` column only (DECISION F104 D1), for every
   commit from C0a through C3 — the commits that exist when this gate runs —
   reported cell by cell against the handback's own `## Commits` table and
   each confirmed under 500. If the evidence commit exceeds 500 insertions,
   declare it in the handback WITH the inseparability reason BEFORE review,
   per AGENTS.md. C4's own numbers are not this gate's business: §3 item 14
   routes them to the next ledger entry.

Handback: rewrite `.agent/handoff.md` in full — feature and round, SESSION 6 of
F112, branch, base and head SHAs, the per-commit changed-files table with its
`+/-` column, ONE line per gate above with its real exit code, the item-status
table AGENTS.md mandates covering every C-commit and every gate, the
deviations, the open-findings count (must read 278), the next expected action.
It has NO length cap (amend0827 rule 3). State plainly whether the gate is
GREEN or whether a blocker was found; the VERDICT itself is the reviewer's and
you do not write one — do not write a `Done:` or `Gate:` paragraph anywhere
beyond applying RECORD18 verbatim. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report the
outcome; create NO pull request, merge nothing.
