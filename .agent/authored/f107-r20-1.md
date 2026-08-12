── STEP R20/21 — F107 Context compiler v2 ─────────────
Goal:        Persist the R19 gate and resolve R-0293, then produce the two
             closure ARTIFACTS the protocol makes mandatory — the evidence
             bundle and a FRESH review zip — and re-confirm preconditions 2
             and 3 with real numbers. The STATUS line, the README sync and the
             PR are deliberately NOT in this round: the reviewer authors the
             STATUS line from the package name and SHA-256 this round reports,
             and a value that does not exist yet cannot be authored verbatim.
Bundle:      C1 save block · C2 mirror · C3 gate and resolution persist FIRST ·
             C4 preconditions 2 and 3 · C5 evidence job · C6 review zip ·
             C7 plan and handoff.
Change:      `.agent/authored/f107-r20-1.md` (new) · `.agent/last_block.md` ·
             `.agent/live_review.md` · `.agent/plan.md` · `.agent/handoff.md`.
             FIVE paths, all under `.agent/`, nothing else. No production code,
             no tests, no docs, no STATUS.md, no README.md. The evidence
             directory and the zip are NEVER committed
             (STATUS_closure_protocol.md, "Evidence dir is not committed");
             both live under the gitignored `.remedy-wt/`, which is why the
             tree still reads clean at handback.
Constraints: AGENTS.md in full. Insertions per commit under 500. Push after
             every commit. Do NOT touch `docs/roadmap/ROADMAP.md`. Do NOT
             create a PR this round. Do NOT merge anything, ever.
Done when:   gates A-H below are executed and their REAL results recorded.
Handback:    completion report + rewrite `.agent/handoff.md` (<= 60 lines, or a
             "Deviations, declared" line naming the real count and the mandated
             content that caused it, per AGENTS.md DECISION D15). The handback
             MUST carry, verbatim and separately: the evidence job id, the
             package filename, its SHA-256, the final verifier verdict, the
             full-suite counts and the integrity-check verdict. Those six
             values are what the next block is authored from — a missing one
             costs a whole relay.

C1 — the block you are executing was handed to you as
`.remedy-wt/f107-r20-1.block.md`. Copy it, do not retype it:
`cp .remedy-wt/f107-r20-1.block.md .agent/authored/f107-r20-1.md`, then
`cmp .remedy-wt/f107-r20-1.block.md .agent/authored/f107-r20-1.md` (silent,
exit 0). Record `wc -l` and `sha256sum` of the saved file. Commit alone, push:
  chore(f107): save the R20 step block verbatim

C2 — `cp .agent/authored/f107-r20-1.md .agent/last_block.md`, then
`cmp .agent/authored/f107-r20-1.md .agent/last_block.md` (silent, exit 0).
Commit alone, then push:
  chore(f107): mirror the R20 block into last block

C3 — GATE AND RESOLUTION PERSIST FIRST (planner_reviewer_prompt.md §4.4)
No finding is registered this round, so `.agent/live_review.md` line 8 is NOT
touched: the next free ID stays R-0295.

PAIR_LRG is an APPEND: the TO's first line IS the FROM, the last line of the
R18 gate entry. The new gate entry goes directly beneath it.
<<<BEGIN PAIR_LRG_FROM>>>
  `LAST_REVIEWED_SHA` advances 54d05e37 -> 6e1970c4.
<<<END PAIR_LRG_FROM>>>
<<<BEGIN PAIR_LRG_TO>>>
  `LAST_REVIEWED_SHA` advances 54d05e37 -> 6e1970c4.
- Reviewer gate on R19 (2026-08-12): PASS. Range `6e1970c4..65723390` = six
  commits over exactly the eight paths the R19 Change line names; `git diff
  --numstat` reads 379/0, 293/321, 96/1, 14/2 and 28/0, 67/0, 10/12 and
  103/99, so every commit stands far under the 500 cap. Transport by the
  PRIMARY shape, restored after R18 could not offer it: the reviewer's own
  original survives at `.remedy-wt/f107-r19-1.block.md`, and `cmp` against
  `.agent/authored/f107-r19-1.md` is silent at exit 0, as is `cmp` of that file
  against `.agent/last_block.md`. Stronger than the counts: every authored
  payload was extracted from the reviewer's original and searched for as a
  whole string in its target — PAIR_HDR_TO, PAIR_LRF_TO, PAIR_LRG_TO and
  PAIR_DONE_TO each occur exactly 1x in `.agent/live_review.md`, PAIR_BS_TO
  exactly 1x in `docs/roadmap/features/T2_F107.md`, and `.agent/plan.md` equals
  PAYLOAD_PLAN byte for byte. Nothing was retyped and nothing drifted. The
  block was 379 lines against the 400 cap, so R-0294's first instance did not
  recur. Append shapes: C3 adds 96 and removes 1, and 35 + 35 + 25 TO-only
  lines plus the one-line header rewrite account for all 96; the worker's
  qualifier that two of those TO-only lines are blank is correct and is the
  R-0253 exception this file already records. Gates RE-RUN here rather than
  read: 80 passed across `test_context_compiler.py` (65, up from 64),
  `test_context_compiler_e2e.py` (6) and `tests/cli/test_job_context_cmd.py`
  (9), `tests/docs/` 294 passed, the canary 42 passed in 20.06s, `ruff` "All
  checks passed!", `^Done:` 12 and `^Landed:` 0, `^<<<` 0 across all six
  touched files, `^## Built State` 1 in the feature file with zero deletions in
  that commit. The red-proof was re-run INDEPENDENTLY by this reviewer in a
  disposable worktree at HEAD: removing only the phase-A `parse_failed` append
  turns the new test red with `Right contains one more item: ('unparseable',
  'signatures')`, and the worktree was removed and pruned, leaving the primary
  checkout clean and alone. This reviewer's own probe, written before the
  repair existed, now reports the `unparseable` record where it reported none —
  the fix is confirmed against evidence that predates it. The two declared
  substitutions are accepted: `remedy` is unavailable to this session's shell
  and both plan probes ran through `python3 -m apps.cli.grouped`, the same
  entry point the R17 gate used, with real output pasted; and the 119-line
  handoff is a DECISION D15 stated-cause overage carrying every mandated
  section. `git status --porcelain` empty, one worktree, `0 0` against the
  remote, `gh pr list --state open` empty. R-0293 is resolved below.
  `LAST_REVIEWED_SHA` advances 6e1970c4 -> 65723390.
<<<END PAIR_LRG_TO>>>

PAIR_DONE is an APPEND at the END of the file: the TO's first line IS the FROM,
the current last line of `.agent/live_review.md`.
<<<BEGIN PAIR_DONE_FROM>>>
meets a word the plan does not carry. Open findings 19 -> 18.
<<<END PAIR_DONE_FROM>>>
<<<BEGIN PAIR_DONE_TO>>>
meets a word the plan does not carry. Open findings 19 -> 18.

Done: R-0293 — RESOLVED. Phase A of `compile_task_context` now takes the
`FileSignatures` object once through `extract_file_signatures`, estimates from
its own rendered lines, and appends an `unparseable` record beside the existing
`budget` one when `parse_failed` is set, so the third and last signature path
stops blaming the budget for a blank the budget did not cause. Verified three
ways by this reviewer rather than once: the diff reads as specified with the
budget record unchanged; the probe that FOUND the gap, written before any fix
existed, now reports `('broken.py', 2, 'unparseable', 'signatures')` where it
reported only the budget record; and the new test, run in a disposable worktree
with only that append removed, fails with `Right contains one more item:
('unparseable', 'signatures')` — it bites the exact line it names.
`_signature_render_text` survives for `render_compiled_context_text`, unchanged.
The suite collects 65 where it collected 64, and the Edge-cases clause
"signature-skipped WITH REASON otherwise" now holds on every path that renders
signatures. Open findings 20 -> 19.
<<<END PAIR_DONE_TO>>>
Commit, then push:
  chore(f107): record the R19 gate and resolve R-0293

C4 — preconditions 2 and 3 of STATUS_closure_protocol.md. Nothing is committed
by this item; record the REAL output of each command in the handback.
1. Full suite, the closure re-confirmation of the R16 integration gate:
     python3 -m pytest -n auto -q
   Save the raw output to `.remedy-wt/r20_logs/full_suite.txt` and report the
   final counts line verbatim. EXPECTED, from the R16 gate and this branch's
   R17 re-run: five failures, all in the pre-existing R-0286 `[reviewer]`
   class. That expectation is not a licence to see it — report what the run
   prints. If the failure count or the ids differ from R-0286's five, STOP and
   report; that is a regression, not a closure.
2. Integrity, precondition 3:
     python3 -m apps.cli.grouped integrity check --json
   Report `passed`, the check count, the untracked/relevant counts and any open
   blocker or high findings.

C5 — the evidence job, per STATUS_closure_protocol.md step 1. The producer call
is already written for you at `.remedy-wt/r20_build_evidence.py`, adapted from
the script that produced F105's READY package; read it before running it.
1. `mkdir -p .remedy-wt/r20_logs`, then produce the four `-v` logs it parses.
   Each command's stdout goes to its own file, and each MUST end 0 failed and
   0 skipped — the script asserts exactly that and stops if not:
     python3 -m pytest tests/orchestration/test_context_compiler.py -v
       -> .remedy-wt/r20_logs/vr0001.txt          (expect 65 passed)
     python3 -m pytest tests/orchestration/test_context_compiler_e2e.py
       tests/cli/test_job_context_cmd.py -v
       -> .remedy-wt/r20_logs/vr0002.txt          (expect 15 passed)
     python3 -m pytest tests/docs/ -v
       -> .remedy-wt/r20_logs/vr0003.txt          (expect 294 passed)
     python3 -m pytest tests/cli/test_golden_path.py -v
       -> .remedy-wt/r20_logs/vr0004.txt          (expect 42 passed)
2. `python3 .remedy-wt/r20_build_evidence.py`. Record the four printed run
   lines and the result JSON, especially the final verifier verdict and the
   evidence job id `f107-closure`.
3. If the producer raises, record the FULL raw error and STOP. Do not fall back
   to a no-evidence package to produce something: F107 has a runtime evidence
   job, so a NO_EVIDENCE package would be a false artifact.

C6 — the review zip, per STATUS_closure_protocol.md step 2. MANDATORY, fresh,
never skipped; a failing build is a closure BLOCKER, not a footnote.
1. The tree must be clean and the branch pushed before the build — the zip
   records the reviewed head. Show `git status --porcelain` first.
2. Build with the explicit evidence dir, never by auto-selection:
     bash scripts/make_review_zip.sh --evidence-dir
       .remedy-wt/f107_closure_evidence/remedy-job-evidence-f107-closure
3. Record the package filename, its SHA-256, the package_status, and the
   manifest's `committed_review_subject` base and head — the head MUST be the
   current HEAD and the base MUST be 2e4142c3ac72042ac4d704da252db263e48dcba3.
4. If the build fails or packages BLOCKED_EVIDENCE, record the raw error and
   the package status and STOP with the reason. Do not retry blindly and do not
   hand back a green word over a red build.

C7 — plan and handoff. Replace `.agent/plan.md` ENTIRELY with:
<<<BEGIN PAYLOAD_PLAN>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0295. R19 reviewed PASS at 65723390.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R20 — the closure ARTIFACT round. The R19 gate is recorded and R-0293 is
resolved, leaving 19 open findings, none above Medium. Preconditions 2 and 3
are re-confirmed with real numbers, the `f107-closure` evidence bundle is built
with the canonical producer, and a fresh review zip is packaged from the clean
reviewed head. Nothing outside `.agent/` is committed this round.

## Next Steps
1. R21 — the closure commit: the reviewer-authored STATUS `[x]` line, the
   README capability sync in the SAME commit (R-0154), the final `.agent/`
   state, then the PR. The five pre-existing R-0286 `[reviewer]` failures are
   carried as a documented risk, so the closure verdict is PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END PAYLOAD_PLAN>>>

Then rewrite `.agent/handoff.md` (you author it) with: feature and round,
branch, the commit SHAs of C1-C3, a changed-files table, the item-status table
for C1-C7, the REAL results of gates A-H, the six closure values the Handback
line names, the open-findings count, and the next expected action. The state
block repeats the operator brief's Fortschritt line verbatim:
  Fortschritt: ~98 % (T001-T004 ✅ · Integration Gate ✅ · Built State ✅ · Evidence + Zip ✅ · STATUS-Zeile + PR offen) — Schätzung
Commit, then push:
  chore(f107): rewrite the plan and handoff for R20

GATES — run every one, record the real output and the real exit code
A transport: `cmp` of the scratch original against `.agent/authored/f107-r20-1.md`
  (silent, exit 0), that file's `wc -l` and `sha256sum`, and the C2 `cmp`
  against `.agent/last_block.md` (silent, exit 0).
B block cap: the gate-A line count against the cap of 400 (DECISION F105 D5).
C pairs, after C3, in `.agent/live_review.md`: `Reviewer gate on R19` is 1,
  `^Done: R-0293` is 1, `^Done:` is 13, `^Landed:` is 0, and
  `^> Branch:.*Next free ID: R-0295` is still 1 (this round registers nothing).
  Both pairs are APPEND-shaped: each FROM stays exactly 1x, and every non-blank
  TO-ONLY line occurs exactly 1x AMONG THE LINES C3's OWN DIFF ADDS. Report
  added/removed from `git show --numstat <C3> -- .agent/live_review.md` and the
  count of added lines belonging to no TO body (must be 0).
D marker leak: `grep -c '^<<<'` is 0 in `.agent/live_review.md`,
  `.agent/plan.md` and `.agent/handoff.md`.
E preconditions: the C4 full-suite counts line verbatim, the failing ids if
  any, and the integrity-check verdict with its check count.
F evidence: the four `-v` run lines the script prints, the final verifier
  verdict, and the evidence job id — or the raw error and the stop.
G package: the zip filename, its SHA-256, the package_status, and the
  manifest's committed_review_subject base and head — or the raw error and the
  stop. This gate has no green word: a package either exists on disk with a
  hash you computed, or it does not.
H tree, push and scope: `git status --porcelain` empty, `git worktree list` the
  primary checkout alone, `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` is `0 0` after the last push,
  `git diff --name-only 65723390..HEAD` lists exactly the five `.agent/` paths
  the Change line names and NOTHING else, insertions per commit each under 500,
  and `gh pr list --state open` still returns an empty list.
── END OF BLOCK ─────────────
