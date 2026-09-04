── STEP CLOSE/2 — F112 round 28 ────────────────────────────────
Goal: Book round 27's PASS verdict (resolves R-0792, R-0793), then
rebuild F112's closure evidence bundle and the mandatory review zip
against the now-fixed evidence-packager contract, and confirm
`PACKAGE_STATUS=READY_FOR_REVIEW` / `EVIDENCE_AUTHORITATIVE=true`.

Bundle:
1. C0a/C0b — save this block verbatim (transport proof), same pattern
   as every prior round (`cp`, never retype).
2. C1 — append RECORD27 (below) to `.agent/live_review.md`: books round
   27's PASS verdict, resolves `R-0792` and `R-0793` (`Done:` lines).
3. C2 — apply PLAN28 (below) to `.agent/plan.md` (whole-file replace).
4. C3 — THE EVIDENCE JOB AND THE REVIEW ZIP. This step produces NO
   repository diff (the evidence dir and the zip are never committed —
   both are gitignored). Do it with a Python driver script (write it to
   disk with the Write tool under a path OUTSIDE the repo tracked tree,
   e.g. `.remedy-wt/r28_evidence.py`, and run it with `python3
   .remedy-wt/r28_evidence.py` from the repository root) that:
   a. First re-runs these THREE SCOPED commands exactly as round 23
      ran them (do NOT include the full test suite — a verification
      record may never carry a full-suite node-id list, per
      docs/roadmap/STATUS_closure_protocol.md's own rule; the full-suite
      proof already rides in round 19's integration-gate evidence and
      the reviewer's own re-run this round, ordered separately below):
        "python3 -m pytest tests/orchestration/test_class_prompt_budget.py"
        "python3 -m pytest tests/orchestration/test_context_compiler.py -k \"test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded or test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic\""
        "python3 -m pytest tests/cli/test_golden_path.py"
      via `_run_verifications` imported from
      `packages.orchestration.job_evidence` (the existing, tested
      helper — the same function this round's own C1 booked as fixed
      for R-0792). If ANY of the three exits non-zero, STOP before
      calling `create_manual_completion_bundle` and declare it as a
      BLOCKING finding rather than a routine result.
   b. Calls `create_manual_completion_bundle` from
      `packages.orchestration.job_evidence` with:
      `evidence_dir="remedy-job-evidence-f112-closure"`,
      `repo_root="."`,
      `base_commit="5c28c6741db2d9073fc75cd159d91037e0757fb0"`
      (reconfirm with `git merge-base main HEAD` before using it —
      declare if it has changed),
      `head_commit=<the full 40-char SHA of C2's own commit — reconfirm
      this is still HEAD immediately before the call; if the branch
      moved, use the real current HEAD and declare the discrepancy>`,
      `job_id=uuid4().hex[:16]` (fresh),
      `job_title="F112 Prompt budget per task class — closure evidence
      (post R-0792/R-0793 fix)"`,
      `step_range="T001-T003"`,
      `prior_job_ids=[]`,
      `verification_runs=<the "runs" list from step (a)'s
      _run_verifications(...) return value>`,
      `timestamp=<current UTC ISO-8601, generated fresh>`,
      `generated_at=<current UTC ISO-8601 with microseconds, generated
      fresh>`,
      `num_tasks=3` (default, do not override),
      `note_prefix="F112 closure evidence (rebuild after R-0792/R-0793
      fix)"`,
      `review_feature_id="f112"`.
      Print and capture the returned summary dict in full. If this call
      raises, capture the FULL exception and STOP.
   c. THE OUTPUT_HASH SELF-CHECK: re-read
      `remedy-job-evidence-f112-closure/verification_tests.json` from
      disk after the bundle is written and, for every run, print
      whether `output_hash == sha256(stdout_summary.encode()).hexdigest()`
      — this must read `True` for all three runs; if any reads `False`,
      STOP, the fix did not hold, and declare a finding rather than
      proceeding to the zip.
   d. THE REVIEW ZIP: run
      `bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f112-closure`
      as a real shell command (not through a pipe — the script's own
      exit code must stay measurable). Capture stdout/stderr and the
      real exit code. Confirm the printed SHA-256 with your own
      `sha256sum` of the produced file.
   e. THE READING THAT MATTERS: open the produced zip with `zipfile`
      and read `.review_zip_manifest.json` FROM INSIDE IT (never from
      builder stdout alone). Report `PACKAGE_STATUS`,
      `EVIDENCE_AUTHORITATIVE`, `REVIEW_SUBJECT_ALIGNMENT`,
      `committed_review_subject.base_commit`/`head_commit`/
      `base_is_ancestor`, `ready_gate_matrix.ok` with its
      `blocking_reasons`, and `review_subject_evidence_alignment.verdict`
      with its issue/hash-mismatch counts. `PACKAGE_STATUS` other than
      `READY_FOR_REVIEW` is a CLOSURE BLOCKER: stop, report the exact
      blocking reason(s), change nothing to force it green. This is the
      operator's own expected result per their ruling — if it does NOT
      read `READY_FOR_REVIEW`/`true`, that is the single most important
      fact in this round's handback.
   f. ARCHIVING: if the zip built successfully, attempt to copy (not
      move) it to `/home/decodeux/Repos/remedy-history/zips/` (create
      the directory if missing and permitted). Report the absolute
      archived path, or the literal `NOT ARCHIVED` with the reason.
   g. Confirm `git status --porcelain` and `git status --porcelain
      --ignored=no` both still read EMPTY for tracked paths afterward.
5. C4 — THE INTEGRATION-GATE RE-CONFIRMATION AND INTEGRITY CHECK
   (closure preconditions 2 and 3): report
   `from packages.orchestration.integrity_gate import
   run_integrity_checks; run_integrity_checks()` — `.passed`,
   `.fail_count`, and the name+status of every check (attributes, not a
   dict). Precondition 2 (full suite green) is satisfied by round 19's
   integration-gate PASS plus this round's own re-run of the three
   scoped commands above and the canary at G-canary below; do not
   re-run the full `-n auto` suite this round unless the integrity
   check or anything else raises doubt about it.
6. Handback — completion report + rewrite `.agent/handoff.md`.

Change: `.agent/live_review.md`, `.agent/plan.md`,
`.agent/authored/f112-r28.md` (new), `.agent/last_block.md`,
`.agent/handoff.md`. The evidence dir and the zip are NEVER committed
(gitignored) — confirm this explicitly, do not `git add` either.
Nothing under `packages/`, `apps/`, `tests/`, `docs/` this round.

Constraints:
- `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
  `docs/roadmap/features/T3_F112.md`, `docs/roadmap/STATUS.md`,
  `README.md`, `scripts/self_use_queue.json` are NOT touched this round
  — closure lands in round 29, once this round's zip is confirmed
  READY_FOR_REVIEW.
- Never force-push, never work on `main`, create NO pull request, merge
  nothing, no `--approve` / promotion of anything.
- If the zip still does not read READY_FOR_REVIEW after the R-0792/
  R-0793 fix, do NOT attempt a second fix on this round's own
  initiative — declare the exact blocking reason(s) from step (e) in
  full and stop; that is a new finding for the reviewer to design the
  next round around, not a guess to paper over.

Done when — run every gate and report its REAL exit code/output:
- `git status --porcelain` — empty before C0a and immediately before C3
  is run and again before the handback commit.
- `.agent/live_review.md` reproduces at exactly `2334372` bytes
  immediately after C1 (pre-append `2328447` + 1 + RECORD27's `5924`
  bytes), and RECORD27 extracted from the committed authored file is a
  byte-exact suffix; report registered/`Done:`/open counts before and
  after C1 (before: 354 registered, 72 `Done:`, 282 open; after: 354
  registered, 74 `Done:`, 280 open — UNMOVED registered count, `Done:`
  count up by 2).
- `.agent/plan.md` reproduces byte-identical to PLAN28 (`2218` bytes, no
  trailing newline, `## Goal`/`## Next Steps` each exactly once,
  `wc -l` under 50) after C2.
- The three scoped commands' real pass/fail/skip counts and node_ids
  counts (must equal `selected`).
- `create_manual_completion_bundle`'s full returned summary dict, or the
  full exception if it raised.
- The C3c output_hash self-check reading (`True`/`True`/`True`
  expected) for all three runs.
- The zip build's real exit code, printed filename and SHA-256, and
  your own independent `sha256sum` confirming the same digest.
- The `.review_zip_manifest.json` readings from step (e) in full —
  `PACKAGE_STATUS`, `EVIDENCE_AUTHORITATIVE`,
  `REVIEW_SUBJECT_ALIGNMENT`, base/head commit, `base_is_ancestor`,
  `ready_gate_matrix.ok`/`blocking_reasons`,
  `review_subject_evidence_alignment.verdict`.
- The archiving outcome (absolute path or `NOT ARCHIVED` + reason).
- `run_integrity_checks()` — `.passed`, `.fail_count`, per-check status.
- `git check-ignore -v remedy-job-evidence-f112-closure` confirming it
  is gitignored.

Handback: completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

--- BEGIN RECORD27 sha256=35a3c5fffd383da5d75f222bda03cf283150cad22acd71f3c70caffb23723a91 ---
Gate: F112 R27 — the round 27 entry, the evidence-packager contract fix (operator ruling, 2026-09-04). VERDICT PASS, over the range `ade5abd4..7a1e3095` (commits C0a `dbba6ca9`, C0b `f9f65916`, C1 `734ecde8`, C2 `091ca97b`, C3 `42eb4342`, C4 `82c20785`, C5 `f39ecfef`, C6 `7a1e3095` — eight real content commits — plus handback commit `313126ce`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r27.md` and `HEAD:.agent/last_block.md` both print blob `e311d9295e87cbfe411f97f47e17907a33379e1e`, reproduced directly; `sha256sum .agent/authored/f112-r27.md` reproduced `60fd7980ad29045226901c0c8279bd2e74b3f9805bfa5898224a5f3b75ba219c` at 16170 bytes. THE PLAN HELD: `.agent/plan.md` reproduced at 2337 bytes, 47 lines, `## Goal`/`## Next Steps` each exactly once, no trailing newline. THE RECORD APPEND AT C1 HELD: `.agent/live_review.md` reproduced at 2328447 bytes immediately after C1, matching the round's own pinned figure exactly. THE CODE DIFF HELD, READ BOTTOM-UP AGAINST THE BLOCK'S OWN ORDERED ITEMS, NOT SUMMARIZED: `git diff ade5abd4..HEAD -- packages/ apps/ tests/ docs/` touches exactly `packages/orchestration/job_evidence.py` (+22/-11), `packages/orchestration/manual_attestation.py` (+9/-7) and the new `tests/orchestration/test_job_evidence_verification_contract.py` (+134/-0), matching the reported "3 files changed, 165 insertions(+), 18 deletions(-)" exactly. `job_evidence._scrub_paths` now delegates to `packages.common.path_redaction.scrub_paths` after its own repo-root/`$HOME` relativization, unchanged in shape. `_default_verification_runner` now scrubs-then-truncates `stdout_summary`/`stderr_summary` and hashes the FINAL string, not raw `stdout`. `_run_verifications`'s normalization loop unconditionally recomputes `_output_hash` from the final `_stdout_summary`, discarding any caller-supplied value; the dead local `import hashlib as _hl_norm` is gone with it. `manual_attestation._vt_run_v11` now imports and calls the shared `scrub_paths` before truncating, and unconditionally recomputes `output_hash` the same way — this call site previously applied NO scrubbing at all, confirmed fixed. GATES REPRODUCED INDEPENDENTLY, NOT TAKEN FROM THE HANDBACK: `python3 -m pytest tests/orchestration/test_job_evidence_verification_contract.py -q` → 4 passed; `python3 -m pytest tests/orchestration/test_job_evidence.py tests/orchestration/test_review_verification_tests_strict.py tests/orchestration/test_failure_postmortem.py -q` → 258 passed, no regression; `python3 -m pytest tests/cli/test_golden_path.py -q` → 42 passed, canary held; `python3 -m ruff check packages/orchestration/job_evidence.py packages/orchestration/manual_attestation.py tests/orchestration/test_job_evidence_verification_contract.py` → All checks passed. THE MUTATION RED-PROOF WAS REPRODUCED BY THE REVIEWER DIRECTLY (not only read from the worker's report): reverting `_run_verifications`'s C4 fix to the old caller-supplied-hash-with-fallback shape, applied and removed in the primary checkout with `git status --porcelain` confirmed empty both before and immediately after the revert-and-restore, turned `test_wrong_caller_supplied_hash_is_discarded_and_recomputed` RED (`AssertionError: assert 'deadbeef...' == '3c596061...'`, 1 failed/3 passed) and restoring the fix returned it to 4 passed/0 failed; the worker's own C3/R-0793 mutation (reverting the scrub delegation, run inside the disposable worktree `.remedy-wt/f112-r27-mutation`, reddening the (b) test alone) is taken on the worker's report per G5, which reserves the disposable-worktree route for exactly this kind of check and the worker's transcript shows the expected 1 failed/3 passed reading with the worktree removed and the primary tree confirmed clean afterward. ONE DEVIATION, CORRECTLY HANDLED: the block's C7 wording named "C3c's ordering" as the mutation target for test (a); the worker found that reverting C3c alone left all 4 tests green because test (a) exercises `_run_verifications` via an injected `runner=` callable that bypasses `_default_verification_runner` (C3c) entirely, and correctly mutated C4 instead (the code test (a) actually reaches), which is what the reviewer's own independent reproduction above also confirms is the right target — not a defect, a correctly-diagnosed and declared block imprecision. `git status --porcelain` reads empty now. THE OPERATOR'S ROOT-CAUSE RULING IS THEREFORE CONFIRMED FIXED AT BOTH NAMED SITES PLUS THE SCRUBBING GAP, and round 28 proceeds to rebuild F112's closure evidence job and review zip against this fix.

Done: R-0792 — RESOLVED at `42eb4342`/`82c20785`/`f39ecfef` (F112 R27), verified by the reviewer independently above. `output_hash` is now always `sha256` of the exact stored `stdout_summary` bytes, at all three call sites the operator's ruling named (`_default_verification_runner`, `_run_verifications`'s normalization loop, `manual_attestation._vt_run_v11`), proved by `tests/orchestration/test_job_evidence_verification_contract.py::TestRunVerificationsOutputHashContract` and `::TestVtRunV11ScrubsAndRehashes`, and mutation red-proofed by the reviewer directly (above) as well as by the worker in a disposable worktree.

Done: R-0793 — RESOLVED at `42eb4342`/`f39ecfef` (F112 R27), verified by the reviewer independently above. `job_evidence._scrub_paths` now delegates to `packages.common.path_redaction.scrub_paths`, and `manual_attestation._vt_run_v11` now calls the same shared scrubber where it previously called none; a third-party absolute path (`/usr/bin/python3`) is redacted at both call sites and the `R-0790` "+/-" non-match guard is confirmed unregressed, proved by `TestScrubPathsCatchesThirdPartyAbsolutePaths`, `TestScrubPathsDoesNotRegressPlusMinusGuard` and `TestVtRunV11ScrubsAndRehashes`, mutation red-proofed by the worker in the disposable worktree per the Gate paragraph above.
--- END RECORD27 ---

--- BEGIN PLAN28 sha256=33d287544d2c9b4c447bfd7cf64deccd7165a28b0c1f1e2492c3a6af3bf5805e ---
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use consumed round 21, Built
State landed round 22. Round 27 fixed the evidence-packager contract
(R-0792, R-0793) per the operator's ruling of 2026-09-04 and is
independently re-verified (RECORD27, this round). All six closure
preconditions are now satisfied; round 28 rebuilds the evidence job and
review zip against the fixed contract.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 28 rebuilds the F112 closure evidence bundle via
`job_evidence.create_manual_completion_bundle` (the same three scoped
verification commands round 23 used, via `_run_verifications`, now
fixed) and the mandatory review zip
(`scripts/make_review_zip.sh --evidence-dir <path>`), then confirms
`PACKAGE_STATUS=READY_FOR_REVIEW` / `EVIDENCE_AUTHORITATIVE=true` by
reading `.review_zip_manifest.json` from INSIDE the built zip.

## Next Steps

- Round 29: reviewer authors the STATUS `[x]` line from round 28's
  reported job_id/package/hash/path/accepted-HEAD; closure commit
  (STATUS, README capability sync, `self_use_queue` SU-007
  `consumed_by=F112`, final `.agent/` state); PR opened, not merged.
- Round 30: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule;
  hand back the built zip's name and SHA-256 to the operator.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to
  F112, carried forward per precondition 1's "Resolved or documented
  risk".
- A PACKAGE_STATUS other than READY_FOR_REVIEW is still a closure
  BLOCKER even after the R-0792/R-0793 fix; round 28 declares rather
  than works around any remaining blocking reason.
--- END PLAN28 ---
