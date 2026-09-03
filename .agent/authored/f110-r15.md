── STEP INTEGRATION GATE — F110 model routing by task class ───────────────────
Round 15 · SESSION 5 of F110 · base `970ffc27` (F110 R14 C5)

Goal:
  Run the INTEGRATION GATE this feature owes before closure — the full suite on
  the branch and at the merge base, compared and attributed — and land its
  evidence under `.agent/gate_f110_r15/`. Round 14's PASS verdict, the
  resolution of `R-0789` and one prose slip are booked in the same round.

  The procedure is `docs/agents/integration_gate.md`, steps 1-5. This block does
  NOT restate it (§3, verification tier 3); it supplies only this round's
  parameters, the repairs three OPEN findings require of it, and the gates.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f110-r15.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   apply PLAN15 to `.agent/plan.md`
  C2   append RECORD15 to `.agent/live_review.md` and SLIPS15 to
       `.agent/prose_slips.md`
  C3   the gate evidence: create `.agent/gate_f110_r15/` and commit the files
       G7 lists
  C4   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f110-r15.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/prose_slips.md`
  `.agent/gate_f110_r15/` (created by this round; the files G7 lists)
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
  3. Slices are transported, not typed: C0a is `shutil.copyfile` from
     `remedy-review-r9-scratch/f110-r15.md`, and every slice is EXTRACTED from
     the COMMITTED `.agent/authored/f110-r15.md` by locating its `<<<BEGIN X>>>`
     and `<<<END X>>>` marker lines with `list.index` and joining the lines
     BETWEEN them, markers excluded. Nothing is taken from this prompt.
  4. THE TARGET WINS on newline convention: `.agent/plan.md` ends WITH exactly
     one trailing newline and the PLAN15 extraction carries none, so the applied
     file is the extraction PLUS that one byte; `.agent/live_review.md` and
     `.agent/prose_slips.md` end WITHOUT one and each append is `\n\n` + slice.
  5. Do NOT run `ruff`, `npm`, or any formatter. This round writes no code.
  6. THE SANDBOX SHAPES HOW THE SUITE IS INVOKED, and the F109 R17 gate already
     solved it — `.agent/gate_f109_r17/gate_summary.txt` is the precedent to
     follow. `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd` and `cp` are all
     DENIED. So: invoke pytest AS A LIBRARY, `pytest.main(["-n", "auto", "-q"])`,
     with the working directory pinned per run; set `REMEDY_UI_NO_AUTO_BUILD`
     IN-PROCESS via `os.environ` for the BASE run only; and copy with
     `python3 -c "import shutil; shutil.copyfile(a, b)"`. Capture a real exit
     code by wrapping any shell gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`.
  7. RUN LOGS ARE WRITTEN OUTSIDE THE REPOSITORY WORKTREE while a suite runs and
     COPIED IN only after that run has exited (R-0176: a log growing inside the
     repo changes the worktree digest mid-run and fails the manifest-identity
     ids as FALSE positives). Use `/home/decodeux/remedy-gate-scratch/`, which
     the reviewer created and verified WRITABLE this session. NOTE, measured by
     the reviewer: this sandbox permits WRITING there but BLOCKS reading a file
     back from outside the repository, so every log is copied in with
     `shutil.copyfile` before it is read. Evidence files carry `.txt` names and
     NEVER `.log` — `.gitignore` drops `*.log` silently and the review-zip guard
     rejects any `\.log$` member (R-0169).
  8. Every destructive or throwaway checkout is a `git worktree` and is removed
     by its EXACT path with `git worktree remove` plus `git worktree prune`, and
     the throwaway BRANCH is deleted. The primary checkout reads
     `git status --porcelain` EMPTY at every verdict. NEVER force-push, never
     work on `main`, create NO pull request, merge nothing.
  9. A sentence THIS ROUND makes stale, anywhere inside the change set, is
     repaired in the commit that falsifies it. One outside the change set is
     DECLARED in the handback and left alone.
  10. `.agent/decisions.md`, `.agent/candidates.md` and
      `docs/roadmap/features/T3_F110.md` are NOT touched. The feature file's
      Design and Task-slicing bullets are the closure sequence's work.

THIS ROUND'S PARAMETERS, all measured by the reviewer at `970ffc27`:
  BRANCH      `feature/f110-model-routing-by-task-class` at this round's C2 tree
              (C0a-C2 touch only `.agent/`, so the code under test is the code
              at `970ffc27`).
  MERGE BASE  `6f2230cea29af36a75fea253afc10f4dfe5a79f0`, from
              `git merge-base main HEAD`.
  BASE TREE   a worktree at `.remedy-wt/base-gate` created ON A THROWAWAY BRANCH
              — `git worktree add -b tmp/base-gate .remedy-wt/base-gate
              6f2230cea29af36a75fea253afc10f4dfe5a79f0`. A DETACHED base
              worktree fails the self-dogfood branch guard BY DESIGN (DECISION
              D3, F053 R2), so the branch is not optional.
  COLLECTION  `pytest --collect-only -q` answers 19510 tests on the branch.
  UI DIST     `apps/ui/dist` holds 4 files; `apps/ui/dist/index.html` has mtime
              1788057215.85 against a newest-file-under-`apps/ui/src` mtime of
              1788057023.74, so the PRIMARY checkout's build is WARM and no cold
              build is owed there. G4 re-measures this rather than trusting it.
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
    `apps/ui/dist` past that worktree's own checkout time, and report
    `_frontend_is_stale()` read from INSIDE the base worktree as False BEFORE
    the base run starts. Nothing is rebuilt and nothing is faked: what is
    corrected is a timestamp the copy mechanism cannot carry across a fresh
    checkout.
  R-0590 — ATTRIBUTE BOTH COMPARISON SETS UNCONDITIONALLY. A gate that
    attributes `comm -23` only "if the parity claim went VOID" demands nothing
    in exactly the case where the ids still exist. Every id in `branch_only.txt`
    AND every id in `fixed_by_branch.txt` is attributed by direct evidence,
    whether parity holds or not.

<<<BEGIN PLAN15>>>
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

Round 15, session 5 — THE INTEGRATION GATE, the tier-3 full-suite gate this
feature owes before closure. `docs/agents/integration_gate.md` steps 1-5 run
against the branch and against the merge base in a throwaway worktree, with the
base-worktree UI parity restored the way findings R-0591 and R-0736 require and
BOTH comparison sets attributed the way R-0590 requires. The evidence lands
under `.agent/gate_f110_r15/`. Round 14's PASS verdict, the resolution of
`R-0789` and one prose slip are booked in the same round. This round changes no
code: a red gate is handed back, never repaired here.

## Next Steps

- The closure sequence, which takes two rounds, runs the one §3 checklist
  consolidation pass DECISION F110 D1 carries into it, needs an evidence job
  and a FRESH review zip, and updates the Design and Task-slicing bullets of
  `docs/roadmap/features/T3_F110.md`.
- The STATUS line and the closure pull request, which the operator merges at
  the next feature's Open PR Gate.

## Risks

- The base worktree is the known-fragile half: without the R-0591 symlink
  argument and the R-0736 mtime advance it produces false base failures by the
  hundred, so the gate reports `_frontend_is_stale()` from inside that tree
  before the run rather than after it.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN15>>>

<<<BEGIN RECORD15>>>
Gate: F110 R14 — the round 14 entry. VERDICT PASS, over the range `f0bbdc5c..37d62419` plus the handback commit `970ffc27`. THE ROUND DID TWO THINGS AND THE REVIEWER RE-DERIVED BOTH FROM DISK. THE TRANSPORT PROOF REACHED THE REVIEWER'S OWN BYTES: `cmp` between the reviewer's scratch original and the committed `.agent/authored/f110-r14.md` exits 0, and ONE digest `8966f2c6982617f79238707b43d171b4568a0cf3634bdf77691e00d4222b5954` covers that original, the saved copy at `b335a56b` and the mirror at `040ef860`; the block is 399 lines against the reviewer's own pre-emission count of 399, under the §3 item 1 cap of 400. EVERY SLICE IS BYTE-EXACT: `.agent/plan.md` equals PLAN14 plus the one trailing newline the target's convention adds, at 42 lines, and the BARE extraction's `cmp` exits 1 on that single byte — the round reported BOTH readings because this round's own SLIPS14 slip asked a block to state the newline up front, and this block's G2 did; `.agent/live_review.md` is 2215298 + 2 + 6966 = 2222266, base an exact byte prefix, still ending without a newline; `.agent/prose_slips.md` is 62351 + 2 + 1768 = 64121, same shape. The second reader counted N = 2 paragraphs in each slice and matched the last 2 blank-line units of each file against them IN ORDER, and the negative control flipped byte 0 of the FIRST appended paragraph in a copy and was REJECTED by that reader in both files — the §3 item 36 shape, satisfied on both targets. `ruff check` over all three changed files answers "All checks passed!", run reviewer-side because the worker's permission layer refuses the tool. R-0789 IS DISCHARGED ON DISK AND THE REPAIR IS PROSE-ONLY, PROVED PER LINE RATHER THAN PER HUNK: C3 `d8a66340` is 11 insertions against 6 deletions in `model_routing.py` and 2 against 2 in `config.py`; the reviewer parsed the BASE file with `ast` to fix the docstring span of `promotion_evidence_from_mapping` at base lines 876..901, then walked the diff line by line to map each deletion to its own base line number — 895, 896, 897, 898, 899, 900, every one strictly inside that span and every one matching the base file at that number. Both `config.py` deletions are `#` comment lines. The count of `NOTHING IN PRODUCTION CALLS THIS YET` in `model_routing.py` is 0 and of `NOTHING READS THIS KEY YET` in `config.py` is 0, the repaired docstring NAMES `resolve_promotion_evidence`, and that name's count in `config.py` went 0 at `f0bbdc5c` to 1. THE ROUTING WAS RUN, NOT READ, and it did not move: with nothing configured `builder` and `reviewer` both answer provider `ollama`, model `muse-glimmer:latest`, effort `medium`, tier `mid`, reason `seed_mapping` and `promoted_by` None — byte-identical to the reviewer's own reading at `f0bbdc5c` across all four configuration states it probed. THE ACCEPTANCE CLAUSE IS BUILT AND ITS COVERAGE IS NEW, WHICH THE RED PROOF ESTABLISHES RATHER THAN ASSERTS. C4 `37d62419` is 205 insertions against ZERO deletions, so "no existing test was edited" is MEASURED; the committed file with the one added import line removed has the base blob as a byte-exact PREFIX, so the import went in at its anchor and all 204 remaining lines were APPENDED with nothing edited between. The reviewer re-ran the red proof INDEPENDENTLY in its own disposable worktree at `970ffc27`, module paths printed from inside it: control 126 passed at exit 0; mutation (i), the pairing check replaced by a never-firing branch, reddens EXACTLY 8 ids and they are exactly the eight parametrizations of the two new refusal tests, which means NO PRE-EXISTING TEST CATCHES THAT MUTATION and the acceptance clause added coverage that did not exist; mutation (ii), a REFUSED override table routed anyway, reddens 13, a strict SUPERSET of (i). Both reverts return to the 126-passed control, the primary checkout read `git status --porcelain` empty at all six readings, and the worktree was removed by its exact path. The worker's own red proof reported the same two counts and the same subset relation, as a measured result rather than as a fault. THE SUITES WERE RE-RUN BY THE REVIEWER at 126 passed for `test_role_config.py`, grown from 101 by the 25 tests C4 adds, then 406 with 3 skipped, 81, 34, 130, 54, 295 and 42, every one exit 0, and ONLY the suite this round adds to moved. Per-commit insertions are 399, 374, 19, 10, 13 and 205, every one under the AGENTS.md cap and every one matching the handback's `## Commits` table cell by cell, which is §3 item 28 met on the table and not only on the verification line; `970ffc27` is 350 insertions, a verbatim rewrite of a single `.agent/**` state file. `git diff --stat f0bbdc5c..37d62419` over `packages/` and `apps/` with the two edited files excluded is EMPTY and over `docs/` is EMPTY. The open set is 279 over 350 unique registered and 71 unique resolved, against 73 `Done:` lines, because `R-0721` and `R-0725` each carry two. `R-0767` stays OPEN. The tree is clean, `git ls-files .remedy-wt` is empty, no worktree of the round's making survives, no `remedy.toml` sits in the repository root, `.agent/candidates.md` is untouched and still EMPTY, and the branch is pushed with no pull request open. ONE PROSE SLIP IS OWED and it is the reviewer's own; it is in `.agent/prose_slips.md` this round. NO FINDING IS OWED.

Done: R-0789 — RESOLVED at `d8a66340` (F110 R14 C3), verified by the reviewer at the F110 R14 gate. Both deliberate-absence notes are retired in ONE commit, which is what this finding's own FIX clause required, and the block that ordered it scoped its permitted-deletion region to the FILE rather than to a module docstring and named `config.py` in its change set for that purpose alone — the two things the fix clause asked of the next block. MEASURED: the count of `NOTHING IN PRODUCTION CALLS THIS YET` in `packages/orchestration/model_routing.py` is 0 and of `NOTHING READS THIS KEY YET` in `packages/orchestration/config.py` is 0, where each was 1 at `f0bbdc5c`. Each replacement NAMES the reader that now exists — `role_config.resolve_promotion_evidence` — and names the commit it landed at, `8efa2330`, so a searching reader lands on the caller rather than on a retired promise. The repair is PROSE-ONLY and proved per line, not per hunk: all six deletions in `model_routing.py` are base lines 895 through 900, strictly inside the `promotion_evidence_from_mapping` docstring span the reviewer fixed at 876..901 by parsing the base file with `ast`, and both `config.py` deletions are `#` comment lines. The shipped routing did not move: `builder` and `reviewer` both still answer `ollama` / `muse-glimmer:latest` / `medium` at tier `mid` with reason `seed_mapping`, byte-identical to the reading taken at `f0bbdc5c` before the repair.
<<<END RECORD15>>>

<<<BEGIN SLIPS15>>>
2026-09-03 · F110 R14 · The round 14 block sent the worker into `remedy-review-r9-scratch/` — the REVIEWER's own scratch directory — without reserving a namespace for the worker's files, so the worker created its own `probe14.py` over the reviewer's file of that name and then correctly removed it by exact path, exactly as the no-delete-by-glob rule asks. Nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` was wrong and no gate depended on the lost file, which the reviewer simply rewrote under a different name; the worker declared the removal in its handback, which is how it was traced at all rather than guessed at. THE LESSON: a block that names a shared scratch directory gives the worker its own prefix for anything it creates there, because a reviewer's pre-emission probe and a worker's gate script converge on the same obvious filename, and the reviewer's copy is the one that vanishes silently.
<<<END SLIPS15>>>

Done when — the gates below, within the amend0827 rule 5 budget, each RUN and
each reported as ONE LINE in the handback with its real exit code. Every gate
runs at a commit STRICTLY EARLIER than C4, the commit that writes the handback.

G1 TRANSPORT — one digest comparison.
   `cmp remedy-review-r9-scratch/f110-r15.md .agent/authored/f110-r15.md` — exit
   0. `sha256sum` those two plus `.agent/last_block.md` — one digest, repeated.
   Report `wc -l .agent/authored/f110-r15.md`. This proves the scratch original,
   the saved copy and the mirror agree; it claims nothing about other bytes.

G2 THE PLAN — a byte-equality check of the plan slice, and nothing more.
   Extract PLAN15 by delimiter index from the COMMITTED authored file. `cmp` the
   extraction PLUS ONE TRAILING NEWLINE against `.agent/plan.md` — exit 0; also
   report the bare extraction's exit code beside it. Report
   `wc -l .agent/plan.md` (must be under 50), `grep -c '^## Goal'` and
   `grep -c '^## Next Steps'`.

G3 THE RECORD APPENDS — full byte forensics, which amend0827 rule 5 reserves for
   exactly this target.
   `.agent/live_review.md`: base 2222266 bytes at `970ffc27`, ending WITHOUT a
   newline. Append `\n\n` + RECORD15. `.agent/prose_slips.md`: base 64121 bytes,
   same convention; append `\n\n` + SLIPS15. For EACH file report the arithmetic
   `<base> + 2 + <len> = <total>` against the real size, that the pre-C2 content
   is an exact byte PREFIX, and that the file still ends without a newline.
   SECOND READER over the WHOLE appended region, per file: let N be the number of
   paragraphs your script COUNTS in that slice — do not take N from this block —
   and compare the LAST N blank-line units of the whole file against the slice's
   N paragraphs IN ORDER. NEGATIVE CONTROL on the FIRST appended paragraph of
   each: flip its byte 0 in a COPY and confirm the reader REJECTS it; the real
   files are never written. HEADER SHAPE (§3 item 26): report the count of lines
   matching the slice's own `Gate: F110 R14 — the round 14 entry.` prefix BEFORE
   C2 (expected 0) and AFTER C2 (expected 1).
   THE OPEN SET, recomputed mechanically and never carried forward: paragraphs
   matching `^- R-\d+ — ` and lines matching `^Done: R-\d+ — `, each reduced to
   UNIQUE IDS, the set difference their open set. Report registered, unique
   resolved, the `Done:` LINE count beside it, the open total, and whether
   `R-0767` is IN the open set and `R-0789` is OUT of it — RECORD15 carries the
   `Done:` paragraph that resolves R-0789, so this reading is what proves the
   resolution landed rather than merely having been written.

G4 STEP 1, THE BRANCH RUN. Assert the WARM-BUILD precondition FIRST and report
   both readings: `apps/ui/dist/index.html` exists, and its mtime exceeds the
   mtime of EVERY file under `apps/ui/src` (a cold or stale dist reddens one
   `tests/ui_server` id for a reason that has nothing to do with this branch).
   Then run the full suite from the repository root per integration_gate.md step
   1, invoked as a library per constraint 6, with NO environment variable set.
   Report the raw tail, the exit code, the wall clock, and write the sorted
   `^FAILED` list to `branch_failed.txt` and the tail to `branch_run_tail.txt`.
   The reviewer's own reading at `970ffc27` is in the handback of this round's
   review, not here: report yours as measured and compare it to nothing.

G5 STEP 2, THE BASE RUN. Create the base worktree exactly as THIS ROUND'S
   PARAMETERS specifies — on the throwaway branch, at the named merge base.
   Restore parity BEFORE the run, applying R-0591 and R-0736 as stated above,
   and report: the entry count copied for each of `apps/ui/node_modules` and
   `apps/ui/dist`; how many of those entries were SYMLINKS and that they were
   PRESERVED; and `_frontend_is_stale()` evaluated FROM INSIDE the base worktree,
   which must read False before the run starts. Then run the same suite there
   with `REMEDY_UI_NO_AUTO_BUILD` set in-process. Report the raw tail, exit code
   and wall clock; write `base_failed.txt` and `base_run_tail.txt`.
   PARITY AS AN EVENT, NOT AN OUTCOME (R-0444): record the mtime of EVERY file
   under the base worktree's `apps/ui/dist` immediately before and immediately
   after the run, report the run's wall-clock window, and state per file whether
   its mtime falls inside it. ANY mtime inside the window VOIDS the parity claim.
   A content digest may accompany that reading and NEVER replaces it, because
   equal content is consistent both with no rebuild and with a byte-identical
   one. Write it all to `parity_mtime.txt`.

G6 STEPS 3 AND 4, THE COMPARISON AND THE ATTRIBUTION.
   `comm -13 base_failed.txt branch_failed.txt` → `branch_only.txt`;
   `comm -23 base_failed.txt branch_failed.txt` → `fixed_by_branch.txt`. Report
   the line count of all four files.
   ATTRIBUTE BOTH SETS UNCONDITIONALLY, per R-0590 — not only when parity is
   void. For every id in `branch_only.txt`: serially re-run that EXACT node id
   and classify per integration_gate.md step 4 — serial-pass is the xdist-flake
   class and is recorded, not a blocker; serial-fail is reproduced AT THE MERGE
   BASE before the feature is blamed; a reproducible branch-only failure coupled
   to F110 code is a BLOCKER, which means STOP and hand back. For every id in
   `fixed_by_branch.txt`: name the direct evidence for its class — the missing
   base artifact per id, or the branch commit that fixed it. An unattributed id
   in either set blocks the gate verdict. Write it all to `attribution.txt`.
   If BOTH sets are empty, say so and attribute nothing: that is the honest
   discharge of this gate, and it is what the F109 R17 gate recorded.

G7 THE EVIDENCE DIRECTORY. C3 creates `.agent/gate_f110_r15/` and commits
   exactly these files, all `.txt` and none `.log`, matching the file set
   `.agent/gate_f109_r17/` established: `gate_summary.txt`,
   `branch_run_tail.txt`, `branch_failed.txt`, `base_run_tail.txt`,
   `base_failed.txt`, `branch_only.txt`, `fixed_by_branch.txt`,
   `parity_mtime.txt`, `attribution.txt`. `gate_summary.txt` follows the shape of
   its F109 R17 predecessor — the branch and base identifiers, then one block per
   integration_gate.md step, then the test-count delta and the cleanup note — and
   states that the VERDICT belongs to the reviewer. Report `ls -la` of the
   directory and `git ls-files .agent/gate_f110_r15` so the committed set is
   measured rather than claimed. Report the count of committed members whose
   name ends `.log` (expected 0).

G8 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C4 is staged — EMPTY.
   `git worktree list` — the base worktree does NOT survive; `git branch --list
   'tmp/*'` — the throwaway branch does NOT survive; `ls -d
   .remedy-wt/base-gate` reports no such file. `git ls-files .remedy-wt` —
   EMPTY. `ls /home/decodeux/Repos/remedy/remedy.toml` — no such file.
   `git diff --stat 970ffc27..<C3> -- packages/ apps/ tests/ docs/` — must be
   EMPTY, which is the change set's "this round measures, it does not change"
   clause MEASURED.
   PER-COMMIT INSERTIONS, the `+` column only (DECISION F104 D1), for every
   commit from C0a through C3 — the commits that exist when this gate runs —
   reported cell by cell against the handback's own `## Commits` table and each
   confirmed under 500. If the evidence commit exceeds 500 insertions, declare it
   in the handback WITH the inseparability reason BEFORE review, per AGENTS.md.
   C4's own numbers are not this gate's business: §3 item 14 routes them to the
   next ledger entry.

Handback: rewrite `.agent/handoff.md` in full — feature and round, SESSION 5 of
F110, branch, base and head SHAs, the per-commit changed-files table with its
`+/-` column, ONE line per gate above with its real exit code, the item-status
table AGENTS.md mandates covering every C-commit and every gate, the deviations,
the open-findings count, the next expected action. It has NO length cap
(amend0827 rule 3). State plainly whether the gate is GREEN or whether a blocker
was found; the VERDICT itself is the reviewer's and you do not write one. Then
`git push -u origin feature/f110-model-routing-by-task-class`; create NO pull
request, merge nothing.
