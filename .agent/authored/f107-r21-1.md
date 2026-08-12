── STEP R21/22 — F107 Context compiler v2 ─────────────
Goal:        Register the packaging defect that blocked R20's C6, record the
             decision that resolves it WITHOUT editing a script F107 does not
             own and WITHOUT deleting anything, relocate the two scratch trees
             that trip the packager's own safety scan, and rebuild the evidence
             bundle and the review zip at the round's final head.
Bundle:      C1 save block · C2 mirror · C3 the finding persists FIRST ·
             C4 DECISION F107 D3 · C5 relocate, rebuild, verify · C6 plan and
             handoff.
Change:      `.agent/authored/f107-r21-1.md` (new) · `.agent/last_block.md` ·
             `.agent/live_review.md` · `.agent/decisions.md` · `.agent/plan.md` ·
             `.agent/handoff.md`. SIX paths, all under `.agent/`, nothing else.
             No production code, no tests, no docs, no STATUS.md, no README.md,
             and above all NO edit to `scripts/make_review_zip.sh`.
Constraints: AGENTS.md in full. Insertions per commit under 500. Push after
             every commit. Do NOT create a PR this round. Do NOT merge.
             NOTHING IS DELETED THIS ROUND. The two scratch trees are MOVED to
             an archive outside the repository, never removed: they are raw
             gate records from earlier F107 rounds and the R-0288 rule expects
             them to stay re-derivable.
Done when:   gates A-G below are executed and their REAL results recorded.
Handback:    completion report + rewrite `.agent/handoff.md` (<= 60 lines, or a
             "Deviations, declared" line naming the real count and the mandated
             content that caused it, per AGENTS.md DECISION D15). The handback
             MUST carry, verbatim and separately, the six closure values the
             R20 handback listed, REFRESHED from this round's rebuild: evidence
             job id, package filename, package SHA-256, final verifier verdict,
             full-suite counts line and integrity-check verdict. No full suite
             runs here: quote R20's line AND the reviewer's differing re-run
             (`6 failed, 16536 passed, 19 skipped in 143.86s`), which R-0296
             explains — never collapse the two into one number.

C1 — the block you are executing was handed to you as
`.remedy-wt/f107-r21-1.block.md`. Copy it, do not retype it:
`cp .remedy-wt/f107-r21-1.block.md .agent/authored/f107-r21-1.md`, then
`cmp .remedy-wt/f107-r21-1.block.md .agent/authored/f107-r21-1.md` (silent,
exit 0). Record `wc -l` and `sha256sum` of the saved file. Commit alone, push:
  chore(f107): save the R21 step block verbatim

C2 — `cp .agent/authored/f107-r21-1.md .agent/last_block.md`, then
`cmp .agent/authored/f107-r21-1.md .agent/last_block.md` (silent, exit 0).
Commit alone, then push:
  chore(f107): mirror the R21 block into last block

C3 — THE FINDING PERSISTS FIRST (planner_reviewer_prompt.md §4.4)
PAIR_HDR is a REWRITE. In `.agent/live_review.md` replace the one line:
<<<BEGIN PAIR_HDR_FROM>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0295.
<<<END PAIR_HDR_FROM>>>
<<<BEGIN PAIR_HDR_TO>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0297.
<<<END PAIR_HDR_TO>>>

PAIR_LRF is an APPEND: the TO's first line IS the FROM, the last line of the
R-0294 entry. The new entry goes directly beneath it, inside `## Findings`.
<<<BEGIN PAIR_LRF_FROM>>>
  block before emission, mechanically, on the final bytes.
<<<END PAIR_LRF_FROM>>>
<<<BEGIN PAIR_LRF_TO>>>
  block before emission, mechanically, on the final bytes.
- R-0295 (Medium, F107 R21, found by the R20 zip build failing): the review-zip
  packager publishes local scratch it was never taught about, and then rejects
  its own package for containing it — so closure is blocked by construction on
  any machine where a gate round left a nested `.data/` or `.git/` in scratch.
  Mechanism, read off the script rather than inferred: the collector at
  `scripts/make_review_zip.sh:218-259` is a filesystem `find .` with a
  HARDCODED prune list (`.git`, `.data`, `node_modules`, the cache dirs, the
  top-level `remedy-job-evidence-*` dirs) plus a few `! -name` filters. That
  list predates the `.remedy-wt/` convention this project adopted for agent
  scratch, and `.gitignore` has no bearing on a `find` — so every scratch tree
  is swept in. The post-publication scan at `:509` then greps the published
  listing for path components including `/.data/` and `/.git/`, finds them, and
  exits 1 without deleting the package. R20's build is the instance: this
  reviewer's own scan of
  `remedy-review-20260812-232923-READY_FOR_REVIEW.zip` counts 10534 members of
  which exactly 1834 are unsafe — 1804 under `.remedy-wt/r11gate/realrun`,
  whose staged pingpong artifacts carry a `.data/` component, and 30 under
  `.remedy-wt/r9gate/demo_repo`, a fixture git repo carrying `.git/`. NOTHING
  from the review subject is implicated: the manifest's
  committed_review_subject reads base 2e4142c3 and head ca8e36ab exactly as
  ordered, and zero local paths leaked. The defect is real beyond this feature
  — the scan also implies any scratch holding a `.env`, a `.log` or a coverage
  file would publish it before rejecting it, which is a leak surface as much as
  a packaging bug. Registered NOT fixed here: `scripts/make_review_zip.sh` is
  not F107's code, and a packaging change needs its own round, its own tests
  and its own gate — the same boundary R-0287 and R-0290 respect. DECISION F107
  D3 records what this round does instead. The durable fix is one line, adding
  `-path './.remedy-wt'` to that prune list, and it belongs to a follow-up that
  owns the packager. OPEN.
- R-0296 (Low, F107 R21, flake class, found by the reviewer re-running closure
  precondition 2): `tests/orchestration/test_product_smoke.py::test_no_zombie_
  processes_after_every_outcome` is LOAD-SENSITIVE and fails intermittently in
  a full `-n auto` run. Evidence is two runs of the SAME head, ca8e36ab: the
  R20 worker's run reported `5 failed, 16537 passed, 19 skipped in 143.59s`
  with all five in the pre-existing R-0286 `[reviewer]` class, and this
  reviewer's own run minutes later reported `6 failed, 16536 passed, 19 skipped
  in 143.86s` — the same five plus this test. Run alone it passes in 0.91s.
  Same commit, same machine, different outcome, so this is flakiness by
  definition and not a regression: F107's change set touches
  `context_compiler.py` and its tests only, while this test asserts process
  hygiene after a smoke run and is exactly the kind that other concurrent
  processes on the machine can perturb. Recorded rather than waved through,
  because closure precondition 2 is a reviewer re-run and this reviewer's run
  is the one that disagreed with the handback — a discrepancy silently rounded
  down to "the expected five" would be a false completion claim. Carried as a
  documented Low risk at closure and routed to F252 flake paydown, which owns
  this class; not fixed here, because a timing-sensitive smoke test belongs to
  the feature that owns the suite's stability, not to the context compiler.
  OPEN.
<<<END PAIR_LRF_TO>>>
Commit, then push:
  chore(f107): register R-0295 and R-0296

C4 — the DECISION. PAIR_DEC is an APPEND whose anchor is the current LAST
non-empty line of `.agent/decisions.md`; that anchor must remain exactly 1x and
must immediately precede the payload. The payload's first line is blank.
<<<BEGIN PAIR_DEC_ANCHOR>>>
again, which is the state R-0292 recorded.
<<<END PAIR_DEC_ANCHOR>>>
<<<BEGIN PAIR_DEC_TO_APPEND>>>

## DECISION F107 D3 (2026-08-12) — the blocked package is unblocked by MOVING scratch, not by editing the packager and not by deleting evidence

Context: finding R-0295. F107's closure needs a review zip; the build published
one and then rejected it, exit 1, because 1834 of its 10534 members came from
two scratch trees under `.remedy-wt/` that carry `.data/` and `.git/` path
components. The review subject itself is correct. Three ways out existed and
they are not equally safe.

Chosen: MOVE `.remedy-wt/r11gate` and `.remedy-wt/r9gate` to
`/home/decodeux/remedy-scratch-archive/f107/`, outside the repository, then
rebuild the evidence bundle and the zip at the round's final head. This changes
no tracked file, destroys nothing, and is reversed by moving the two
directories back. The scratch stays on the same machine and stays readable, so
the R-0288 rule that a gate's raw records remain re-derivable still holds — the
path changes, the record does not.

Alternatives considered: (a) add `-path './.remedy-wt'` to the packager's prune
list — the correct DURABLE fix and the one R-0295 names, rejected HERE because
`scripts/make_review_zip.sh` is not F107's code: a packaging change made inside
a context-compiler feature is exactly the scope drift AGENTS.md forbids, and it
would ship a production change whose own tests and gate this feature never
planned. (b) delete the two scratch trees — rejected outright: deletion is
irreversible, it destroys the raw records of F107's own R9 and R11 gates, and
no closure is worth trading evidence for convenience.

Reverse this decision by moving both directories back from the archive. The
follow-up that owns the packager should then apply alternative (a), after which
neither the move nor this decision is needed again.
<<<END PAIR_DEC_TO_APPEND>>>
Commit, then push:
  chore(f107): record DECISION F107 D3

C5 — relocate, rebuild, verify. NOTHING here is committed and NOTHING is
deleted. Run the steps in this order and record the real output of each.
1. Archive the two offending trees, and the rejected package with them so only
   one candidate package is ever on disk:
     mkdir -p /home/decodeux/remedy-scratch-archive/f107
     mv .remedy-wt/r11gate /home/decodeux/remedy-scratch-archive/f107/r11gate
     mv .remedy-wt/r9gate /home/decodeux/remedy-scratch-archive/f107/r9gate
     mv remedy-review-20260812-232923-READY_FOR_REVIEW.zip /home/decodeux/remedy-scratch-archive/f107/rejected-remedy-review-20260812-232923.zip
   Prove each landed: `ls -d` on the two archived directories and `ls -l` on the
   archived zip. If any `mv` fails, STOP — do not force it and do not delete.
2. Confirm the tree is untouched by the move: `git status --porcelain` empty.
3. Refresh the four `-v` logs so their recorded head matches the head the
   bundle will carry (the code under test has not changed since R20 — only
   `.agent/` files have — but the logs record a head, so they are re-run rather
   than reused):
     python3 -m pytest tests/orchestration/test_context_compiler.py -v
       -> .remedy-wt/r20_logs/vr0001.txt          (expect 65 passed)
     python3 -m pytest tests/orchestration/test_context_compiler_e2e.py
       tests/cli/test_job_context_cmd.py -v
       -> .remedy-wt/r20_logs/vr0002.txt          (expect 15 passed)
     python3 -m pytest tests/docs/ -v
       -> .remedy-wt/r20_logs/vr0003.txt          (expect 294 passed)
     python3 -m pytest tests/cli/test_golden_path.py -v
       -> .remedy-wt/r20_logs/vr0004.txt          (expect 42 passed)
   Each MUST end 0 failed and 0 skipped; the producer asserts exactly that.
4. Rebuild the evidence bundle at the current head. Delete nothing: the
   producer writes into a fresh directory, so first move the R20 bundle aside
   rather than overwrite it:
     mv .remedy-wt/f107_closure_evidence /home/decodeux/remedy-scratch-archive/f107/f107_closure_evidence_r20
     python3 .remedy-wt/r20_build_evidence.py
   Record the four run lines, the final verifier verdict and the job id.
5. Rebuild the package from the clean tree:
     bash scripts/make_review_zip.sh --evidence-dir
       .remedy-wt/f107_closure_evidence/remedy-job-evidence-f107-closure
   Record the printed package filename, the script's exit code, the
   package_status, and `sha256sum` of the file COMPUTED BY YOU.
6. Verify the package yourself before calling it good. Write a short read-only
   python scratch script under `.remedy-wt/` that opens the new zip with
   `zipfile`, counts its members, and counts members matching the packager's
   own rejection regex — the one at `scripts/make_review_zip.sh:509`. Report
   both counts. The unsafe count MUST be 0. Report the manifest's
   committed_review_subject base and head; base MUST be
   2e4142c3ac72042ac4d704da252db263e48dcba3 and head MUST be this round's HEAD.
7. If the build fails again, record the FULL raw error and the offending paths
   and STOP. Do not delete anything to make it pass, and do not fall back to a
   NO_EVIDENCE package.

C6 — plan and handoff. Replace `.agent/plan.md` ENTIRELY with:
<<<BEGIN PAYLOAD_PLAN>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0297. R19 reviewed PASS at 65723390; R20 partially
gated — its three commits are reviewed, its C6 was blocked.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R21 — unblocking the package. R-0295 records that the zip packager sweeps local
scratch into the published archive and then rejects its own output; DECISION
F107 D3 chooses to MOVE the two offending scratch trees out of the repository
rather than edit a packager F107 does not own or delete gate evidence. The
evidence bundle and the zip are rebuilt at this round's head. R-0296 records a
load-sensitive smoke test that the reviewer's own full-suite re-run caught and
the worker's did not. Preconditions 1-5 otherwise hold: 21 open findings, none
above Medium, full suite re-confirmed at R20 and again by the reviewer,
integrity check passed, Built State current, tree clean and pushed.

## Next Steps
1. R22 — the closure commit: the reviewer-authored STATUS `[x]` line, the
   README capability sync in the SAME commit (R-0154), the final `.agent/`
   state, then the PR. Verdict PASS_WITH_RISKS for the five pre-existing
   R-0286 `[reviewer]` failures.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END PAYLOAD_PLAN>>>

Then rewrite `.agent/handoff.md` (you author it) with: feature and round,
branch, the commit SHAs of C1-C4, a changed-files table, the item-status table
for C1-C6, the REAL results of gates A-G, the six refreshed closure values, the
open-findings count, and the next expected action. The state block repeats the
operator brief's Fortschritt line verbatim:
  Fortschritt: ~98 % (T001-T004 ✅ · Integration Gate ✅ · Built State ✅ · Evidence + Zip ✅ · STATUS-Zeile + PR offen) — Schätzung
Commit, then push:
  chore(f107): rewrite the plan and handoff for R21

GATES — run every one, record the real output and the real exit code
A transport: `cmp` of the scratch original against `.agent/authored/f107-r21-1.md`
  (silent, exit 0), that file's `wc -l` and `sha256sum`, and the C2 `cmp`
  against `.agent/last_block.md` (silent, exit 0).
B block cap: the gate-A line count against the cap of 400 (DECISION F105 D5).
C pairs, after C3, in `.agent/live_review.md`: `^> Branch:.*Next free ID:
  R-0295` is 0, `^> Branch:.*Next free ID: R-0297` is 1, `^- R-0295` is 1,
  `^- R-0296` is 1, `^Done:` is still 13 and `^Landed:` is 0. PAIR_LRF is
  APPEND-shaped: its FROM
  stays exactly 1x and every non-blank TO-ONLY line occurs exactly 1x AMONG THE
  LINES C3's OWN DIFF ADDS. Report added/removed from `git show --numstat <C3>
  -- .agent/live_review.md` and the count of added lines in no TO body (0).
D decisions: `grep -c '^## DECISION F107 D3' .agent/decisions.md` is 1, the
  anchor line is still 1x, and the payload's first non-blank line directly
  follows it. Report `git show --numstat <C4> -- .agent/decisions.md`.
E marker leak: `grep -c '^<<<'` is 0 in `.agent/live_review.md`,
  `.agent/decisions.md`, `.agent/plan.md` and `.agent/handoff.md`.
F artifacts: the archive proof (both directories and the rejected zip listed at
  their new paths), the four refreshed run lines, the final verifier verdict,
  the job id, the new package filename, its SHA-256 computed by you, the
  package_status, the script's exit code, the member count, the unsafe-member
  count (must be 0) and the manifest's committed_review_subject base and head.
G tree, push and scope: `git status --porcelain` empty, `git worktree list` the
  primary checkout alone, `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` is `0 0` after the last push,
  `git diff --name-only ca8e36ab..HEAD` lists exactly the six `.agent/` paths
  the Change line names and NOTHING else, insertions per commit each under 500,
  and `gh pr list --state open` still returns an empty list.
── END OF BLOCK ─────────────
