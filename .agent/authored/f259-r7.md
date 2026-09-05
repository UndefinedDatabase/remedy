STEP INTEGRATION GATE / F259 — Vocabulary & concept model v1 — round 7 of session 1
BRANCH feature/f259-vocabulary, head 6e6e73ae at the time this block was written.
MERGE BASE 25961794 (the reviewer measured `git merge-base main HEAD` at 6e6e73ae).

Goal
  The dedicated integration-gate round of docs/agents/planner_reviewer_prompt.md
  §3 tier 3, executed per docs/agents/integration_gate.md steps 1 to 4: the full
  suite on this branch, the full suite at the merge base in a throwaway worktree
  with real build parity, the two failure sets compared, and EVERY branch-only id
  attributed. The evidence lands under `.agent/gate_f259_r7/`. Also book the
  reviewer's PASS verdict on round 6.

  Only the reviewer issues the gate verdict, and only this round's ledger entry
  may carry a "full suite" claim. Your job is to produce the readings.

TWO OPEN FINDINGS BIND THIS ROUND'S PARITY RECIPE. Read both before step 2.
  R-0736 (OPEN, Medium) — `docs/agents/integration_gate.md` step 3 says to restore
  parity by COPYING `apps/ui/node_modules` and `apps/ui/dist` into the base
  worktree. `shutil.copytree` PRESERVES source mtimes while `git worktree add`
  stamps every checked-out source file with the checkout time, so the copied
  `dist` is byte-correct and mtime-STALE.
  `packages/orchestration/ui_server.py::_frontend_is_stale` returns True when any
  file under `apps/ui/src/` is newer than `apps/ui/dist/index.html`, staleness
  fires, the auto-build is correctly suppressed, and 114 `tests/ui_server/` ids
  fail with `ERROR: React UI not built.` — false base failures manufactured by
  the recipe. THE FIX, which this block orders: AFTER copying `apps/ui/dist`, set
  the mtimes of `apps/ui/dist/index.html` and everything under `apps/ui/dist` to
  be NEWER than the newest file under the worktree's `apps/ui/src`. Content
  parity is not the relation the code reads; the mtime relation is.
  R-0591 (via §3 checklist item 18) — `shutil.copytree` defaults to
  `symlinks=False` and therefore DEREFERENCES symlinks. The reviewer measured
  `apps/ui/node_modules/.bin` at 6e6e73ae: it holds 23 symlinks. Dereferencing
  them caused 7 base-only failures on a previous gate. COPY WITH
  `symlinks=True`. The repository's own precedent, `.agent/gate_f085_r72/base_parity.txt`,
  reads "symlinks preserved". Order the argument, never the function alone.
  `docs/agents/integration_gate.md` is NOT edited by this round — it is not
  F259's surface and AGENTS.md forbids mixing an unrelated fix into a feature
  branch. R-0736 stays open; this round obeys its fix clause and says so.

Bundle, in this order (one commit each)
  C0a save the block file to .agent/authored/f259-r7.md (copy, never retype)
  C0b mirror it to .agent/last_block.md
  C1  .agent/plan.md ← PLANF259R7 (whole rewrite)
  C2  .agent/live_review.md: GATE_R6 appended at end of file
  C3  .agent/gate_f259_r7/ — the evidence files listed under "The evidence
      directory" below, committed only AFTER every run has exited
  then push; C4 rewrite .agent/handoff.md; push again.

  Create NO pull request. F259's pull request belongs to the closure round.

Change set — EXACTLY these paths and nothing else
  .agent/authored/f259-r7.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md (C2) —
  .agent/gate_f259_r7/** (C3) — .agent/handoff.md (C4)

Delivery
  The block is at `.remedy-wt/f259-r7-block.md`, gitignored scratch. C0a COPIES
  it to .agent/authored/f259-r7.md, C0b to .agent/last_block.md. Slices are
  extracted from the COMMITTED authored file by marker extraction in Python.

The record append (C2)
  `.agent/live_review.md` ends with a newline. Append `"\n" + GATE_R6 + "\n"`.

Where the run logs live WHILE a suite runs
  R-0176: a log file GROWING INSIDE the repository during a suite run changes the
  worktree digest mid-run and produces false failures in
  `test_run_manifest_logical_identity` and `test_job_rerun_workspace_identity`.
  Write every run log OUTSIDE the repository — use `~/remedy-gate-f259/` — and
  copy the finished files into `.agent/gate_f259_r7/` only after the run has
  exited. If writing under `~` is refused, report the refusal verbatim, fall back
  to the gitignored `.remedy-wt/`, and report explicitly whether either of those
  two node ids failed, so the reader can tell a real failure from this artifact.
  R-0169: evidence files are named `.txt`, NEVER `.log` — `.gitignore` drops
  `*.log` silently and the review-zip guard rejects any `\.log$` member.

The evidence directory (C3) — `.agent/gate_f259_r7/`
  `branch_tail.txt`   the branch run's raw tail, its exit code and wall time
  `branch_failed.txt` `grep '^FAILED' <branch log> | sort`
  `base_tail.txt`     the base run's raw tail, its exit code and wall time
  `base_failed.txt`   `grep '^FAILED' <base log> | sort`
  `comm_13.txt`       `comm -13 base_failed.txt branch_failed.txt` — branch-only
  `comm_23.txt`       `comm -23 base_failed.txt branch_failed.txt` — base-only
  `base_parity.txt`   what was copied, with `symlinks=True` stated; the symlink
                      count in the worktree's `apps/ui/node_modules/.bin` AFTER
                      the copy; the newest `apps/ui/src` mtime and the `dist`
                      mtimes set against it; and the dist mtime window of the
                      run (see G4)
  `attribution.txt`   one entry per branch-only id and per base-only id, with the
                      evidence, per G5 and G6
  Every one of these is written in full. NOTHING is truncated, summarised or
  elided — a sweep that is cut off proves nothing about what was cut.

Constraints
  1. Slices are applied BYTE FOR BYTE from the committed authored file. Apply a
     slice you believe wrong verbatim and declare it in the handback.
  2. THE BASE WORKTREE IS CREATED ON A THROWAWAY BRANCH, never detached:
     `git worktree add -b tmp/f259-base-gate <path> 25961794`. The self-dogfood
     branch guard refuses a detached HEAD by design (DECISION D3, F053 R2), so a
     detached base worktree fails the guard-dependent ids for the wrong reason.
     Remove the worktree, delete the tmp branch, prune, and prove with
     `git worktree list`. The ten pre-existing `remedy/job-*` worktrees are not
     yours and stay.
  3. The BRANCH run happens in the PRIMARY checkout, which is the only tree with
     the installed dependencies the suite needs. The primary checkout is never
     mutated: `git status --porcelain` is empty before and after it.
  4. `REMEDY_UI_NO_AUTO_BUILD=1` is set for the base run but NOT trusted alone —
     a spawned build path ignored it once (R-0169). G4 measures the EVENT.
  5. Read `.agent/STOP` from disk before C0a, before C3 and before C4.
  6. NEWLINE CONVENTIONS: PLANF259R7 replaces `.agent/plan.md` whole with exactly
     one trailing newline; the record append is as described above.
  7. This session's shell guard refuses some command FORMS outright — shell
     loops, `$(...)` substitution, `$?` in a compound command, `${PIPESTATUS[0]}`,
     a `$` anchor inside a `grep -c` pattern, brace-with-quote literals in a
     heredoc, and a non-ASCII character in a Python bytes literal. Re-express in
     Python and report the Python you ran beside its output, with any refusal
     quoted verbatim. `comm` may be run through Python's `subprocess` if the
     shell form is refused; report which route was used.
  8. Commit subjects are `f259: <what>`. No leading-slash token, no absolute
     path. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
  9. AGENTS.md binds you in full. Never `--force`, never a history rewrite, never
     `gh pr merge`, never a branch deletion beyond the throwaway `tmp/f259-base-gate`
     that constraint 2 creates. C4 is ONE commit and reports no reading that only
     exists after it is pushed.
 10. IF A BRANCH-ONLY FAILURE IS REPRODUCIBLE AND COUPLED TO THIS FEATURE'S CODE,
     THAT IS A BLOCKER: stop, commit the evidence you have, write the handback
     naming the id and its evidence, and do NOT attempt the fix. The fix is its
     own reviewer-gated round (integration_gate.md step 4).
 11. Do-not-touch: no product code, no test, no doc is edited this round. This
     round MEASURES. `docs/agents/integration_gate.md` is not edited even though
     R-0736 names a defect in it.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback plus the full transcripts in the evidence directory. Every gate runs at
or before C3; none is ordered after the commit that writes the handback.

  G1 TRANSPORT. `sha256sum .remedy-wt/f259-r7-block.md .agent/authored/f259-r7.md .agent/last_block.md`
     — one digest, three times. Report it and all three paths.
  G2 THE RECORD APPEND. The pre-append bytes of `.agent/live_review.md` are a
     byte-exact PREFIX of the post-append bytes and the remainder equals exactly
     `"\n" + GATE_R6 + "\n"` — report both booleans — and
     `grep -c '^Gate: R6 — ' .agent/live_review.md` goes from 0 to 1. Report the
     byte length before and after.
  G3 THE BRANCH RUN (integration_gate.md step 1). In the primary checkout, from
     the repo root: `python3 -m pytest -n auto -q`, its log written outside the
     repository. Report the raw tail, the exit code, the wall time, and the count
     of lines in `branch_failed.txt`. Report `git status --porcelain` immediately
     before and immediately after the run — both empty.
  G4 THE BASE RUN (step 2) WITH REAL PARITY. Create the worktree per constraint
     2 at 25961794. Then, IN THIS ORDER, and report each reading:
       (i)   `shutil.copytree(<primary>/apps/ui/node_modules, <wt>/apps/ui/node_modules, symlinks=True)`
             and the same for `apps/ui/dist`. Report the symlink count under the
             worktree's `apps/ui/node_modules/.bin` afterwards; the reviewer
             measured 23 in the primary checkout at 6e6e73ae and the two counts
             must be equal. A count of 0 means the copy dereferenced them and the
             parity is void — say so rather than continuing quietly.
       (ii)  Compute the newest mtime under the worktree's `apps/ui/src`, then set
             every mtime under the worktree's `apps/ui/dist` to a value strictly
             GREATER than it. Report the newest-src mtime, the dist mtime you set,
             and the boolean that dist/index.html is now newer — this is R-0736's
             fix clause and without it the base run manufactures false failures.
       (iii) Record the mtime of EVERY file under the worktree's `apps/ui/dist`
             immediately before the run and again immediately after (R-0444: the
             EVENT, not the outcome). Report the run's start and end times and
             whether ANY dist mtime falls inside that window. If any does, the
             parity claim is VOID and every base-only id must be attributed
             individually — report that plainly rather than claiming parity.
       (iv)  Run `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` with the
             worktree as the working directory, log written outside the
             repository. Report the raw tail, exit code, wall time, and the line
             count of `base_failed.txt`.
     Finish by removing the worktree, deleting `tmp/f259-base-gate`, pruning, and
     showing `git worktree list`.
  G5 COMPARE (step 3). Produce `comm_13.txt` (branch-only) and `comm_23.txt`
     (base-only) from the two SORTED failure files. Report the line count of each
     and reproduce BOTH LISTS IN FULL in the handback — not a sample, not a head,
     not a count alone. For every base-only id, attribute it to the environment
     class by direct evidence naming the missing artifact, or state that it is a
     genuine base failure; an unattributed base-only id blocks the gate verdict.
     If the parity work above did its job, this list should be short — report the
     number it actually is.
  G6 ATTRIBUTION OF EVERY BRANCH-ONLY ID (step 4). For each id in `comm_13.txt`,
     re-run that exact node id SERIALLY (no `-n auto`) in the primary checkout and
     classify it: serial-pass means the xdist-flake class, recorded and not a
     blocker; serial-fail means reproduce it at the merge base in a worktree
     before blaming the feature. A reproducible branch-only failure coupled to
     this feature's code is a BLOCKER under constraint 10. Report every id with
     its classification and the command output that establishes it. If
     `comm_13.txt` is empty, say so and report the empty result — that is the
     expected outcome for a docs-and-tests feature and it still gets stated.
  G7 THE EVIDENCE DIRECTORY. List `.agent/gate_f259_r7/` with the byte size of
     every file, and confirm: no file name ends in `.log`; every file named under
     "The evidence directory" exists; and no file was truncated — for the two
     failure files and the two comm files, the line count in the file equals the
     line count you reported for it in G3, G4 and G5.
  G8 THE PLAN AND THE STRUCTURE. `wc -l .agent/plan.md` under 50; one `## Goal`
     and one `## Next Steps` (report both counts); `filecmp.cmp(..., shallow=False)`
     True against the slice plus one newline. Then `git status --porcelain` empty
     immediately before C4 is staged; `git ls-files .remedy-wt` returns nothing;
     every commit single-parent; `git diff --numstat <parent> <commit>` for EACH
     commit C0a through C3 reported cell by cell; each commit's insertion count
     against the 500 cap, with C3 declared with its inseparability reason if the
     evidence files exceed it; the push result; and confirmation that no pull
     request was created.

The handback (C4) — rewrite .agent/handoff.md whole
  No length cap, and this round's handback is expected to be long because it
  carries two full-suite transcripts' worth of readings. Carry: feature, round
  and SESSION NUMBER — still SESSION 1 of F259, round 7, rounds so far 7; the
  commit range; a `## Commits` table with the `+/-` numbers G8 printed; the
  AGENTS.md item-status table, one row per bundle item C0a through C4; one line
  per gate G1 through G8 with its real reading; the COMPLETE branch-only and
  base-only lists with their attributions; the parity transcript of G4 including
  the symlink count, the mtime relation and the dist mtime window; the
  deviations; ONE sentence of context self-assessment; and the next expected
  action — the reviewer's gate verdict on the integration gate, then the CLOSURE
  round per docs/roadmap/STATUS_closure_protocol.md. Repeat this line verbatim in
  its state block:
  `~95 % (T001–T004 ✅ · Integration Gate gelaufen · Closure offen) — Schätzung`

<<<BEGIN PLANF259R7>>>
# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 6
PASSED the reviewer's gate; the round-6 verdict is booked in
`.agent/live_review.md` by round 7's own C2. All four task slices are built.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 7 is the INTEGRATION GATE — the full suite on this branch and at the merge
base 25961794, compared, with every branch-only id attributed, per
docs/agents/integration_gate.md. The base worktree's parity obeys the fix clause
of the open finding R-0736: after copying `apps/ui/dist`, its mtimes are set
newer than the newest file under `apps/ui/src`, because the mtime relation is
what `_frontend_is_stale` reads and content parity alone manufactures 114 false
base failures. `apps/ui/node_modules` is copied with `symlinks=True` so the 23
`.bin` shims are not dereferenced.

## Next Steps

- The closure sequence per docs/roadmap/STATUS_closure_protocol.md: the evidence
  job, a FRESH review zip, the ledger rotation, the §3 checklist consolidation
  pass, the reviewer-authored STATUS line committed last, and the pull request —
  which is NOT merged in this session but at the next feature's Open PR Gate.

## Risks

- A branch-only failure coupled to this feature's code is a blocker and gets its
  own reviewer-gated repair round; the gate round never fixes what it finds.
- The suite is large and both runs are full runs, so this round is the session's
  longest by wall clock.
<<<END PLANF259R7>>>

<<<BEGIN GATE_R6>>>
Gate: R6 — the F259 R6 entry. R6 WAS T004: THE README DIAGRAM, THE DOC-INDEX REGISTRATION AND THE BYTE-EQUALITY PIN. VERDICT PASS, AND F259'S BUILD WORK IS COMPLETE. Range cc8834bf..6e6e73ae, eight commits, all single-parent, pushed, no pull request; largest commit 344 insertions. TRANSPORT: one digest `96a4ddf9376d64a0d722251ccab71d27482c098644ae82a87194c1f96224f44e` across `.remedy-wt/f259-r6-block.md`, `.agent/authored/f259-r6.md` and `.agent/last_block.md`, equal to the digest the reviewer computed over its own scratch file before emission; per §3 item 37 that is a COPY chain covering scratch, saved copy and mirror. EVERY EDIT PROVED BY TOTAL RECONSTRUCTION: `README.md` at 91fecaa4 is byte-EQUAL to its parent with ONE occurrence of the anchor replaced by the ordered replacement and nothing else changed (13 893 to 14 219 bytes, anchor count 1 before and 0 after); `docs/README.md` at 8972af01 is byte-EQUAL to its parent with exactly the two authored pairs applied (21 616 to 21 946), and `system/vocabulary.md` occurs in it exactly twice; `.agent/live_review.md` equals its parent plus exactly `"\n" + GATE_R5 + "\n"` (834 169 to 839 318); `.agent/prose_slips.md` equals its parent plus exactly the three ordered slips, still ending with no newline (79 043 to 82 415); `.agent/plan.md` equals its slice plus one newline at 42 lines. THE DIAGRAM NOW EXISTS IN THREE FILES AND ALL THREE ARE ONE TEXT: `README.md`, `docs/system/vocabulary.md` and `docs/roadmap/features/T2_F259.md` each hold exactly one fenced mermaid block and all three bodies hash `6f6d59ee6f3d2b36525d64596b04fee3f5ce43d2c439367e6e40c613d313e07c`. FINDING R-0797's BINDING CLAUSE IS DISCHARGED FOR THIS ROUND, and by the TOKENS rather than by the pin's direction, which is what that clause asks: `README.md`'s four `Accepted in Tier N so far:` blocks are byte-IDENTICAL before and after the insertion, and the reviewer enumerated all 31 `F\d{3}` tokens inside them — 008, 009, 013, 014, 016, 021, 022, 031, 032, 034, 037, 046, 047, 048, 050, 051, 052, 053, 086, 103, 104, 105, 106, 107, 251, 252, 254, 255, 256, 257 and 262 — and confirmed every one carries `- [x]` in `docs/roadmap/STATUS.md`. The worker's observation that the new `docs/README.md` row mentions F260 and F261 was checked and is harmless: no test scans `docs/README.md` for feature ids, the guard reads `REPO / "README.md"` alone, and no `F\d{3}` token entered `README.md`. THE NEW PIN'S RED PROOF WAS RE-RUN BY THE REVIEWER INDEPENDENTLY, in its own disposable worktree at HEAD with `__pycache__` purged and `python3 -B -m pytest`: the unmutated control is exit 0 at 8 passed; changing ONE character inside the worktree's README diagram body — the reviewer mutated `per task` to `per Task`, a different byte from the one the worker chose — gives exit 1 with `test_the_readmes_mermaid_block_is_byte_equal_to_the_pages` as the ONLY failure at 1 failed and 7 passed; restoring gives exit 0 again, the README byte-identical; the worktree was removed and pruned and the primary checkout's `git status --porcelain` is empty. Every run printed `apps.cli.command_catalog.__file__` from inside the worktree and it resolved to the worktree's own copy. SUITES, re-run by the reviewer serially and all exact: `tests/docs/test_vocabulary.py` 8, `tests/docs/` 303 — which is the 302 measured at cc8834bf plus exactly the one test this round added — `tests/orchestration/test_roadmap_index.py` 30, `tests/orchestration/test_test_runner.py` 52, `tests/orchestration/test_integrity_gate.py` 16, `tests/regression/test_resource_safety.py` 21. OPEN SET, recomputed mechanically per §3 item 10: 299 registrations against 5 `Done:` lines, 294 open, unchanged. POST-PUSH READINGS, taken by the reviewer per §3 item 31: `git status --porcelain` EMPTY, `git ls-files .remedy-wt` empty, `origin/feature/f259-vocabulary` at 6e6e73ae, `gh pr list --state open` returning `[]`, and `git worktree list` showing the primary checkout plus the ten pre-existing `remedy/job-*` worktrees and nothing else. The worker's note that the shipped `_mermaid_body` helper captures the newline before the closing fence, so the same body reads 310 bytes and a different digest under the helper's own convention, is correct and is not drift: the reviewer's readings above use the convention this record has used since R3, the bytes are identical in all three files under either convention, and the shipped test compares README to the page with ONE helper, so no convention mismatch can reach it. No finding; no reviewer prose slip this round.
<<<END GATE_R6>>>
