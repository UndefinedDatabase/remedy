── STEP R22/23 — F107 Context compiler v2 ─────────────
Goal:        Amend DECISION F107 D3 to an archive path this environment can
             actually reach, register the reviewer error that cost R21 its
             second half, then complete the relocation, the rebuild and the
             package verification D3 always intended.
Bundle:      C1 save block · C2 mirror · C3 the finding persists FIRST ·
             C4 the D3 amendment · C5 relocate, rebuild, verify · C6 plan and
             handoff.
Change:      `.agent/authored/f107-r22-1.md` (new) · `.agent/last_block.md` ·
             `.agent/live_review.md` · `.agent/decisions.md` · `.agent/plan.md` ·
             `.agent/handoff.md`. SIX paths, all under `.agent/`, nothing else.
             No production code, no tests, no docs, no STATUS.md, no README.md,
             and NO edit to `scripts/make_review_zip.sh`.
Constraints: AGENTS.md in full. Insertions per commit under 500. Push after
             every commit. No PR this round. No merge. NOTHING IS DELETED: the
             scratch trees are MOVED, and a `mv` that fails is reported, never
             forced and never replaced by `rm`. Do NOT use any sandbox-override
             flag: if a path is denied, that is a finding, not an obstacle.
Done when:   gates A-G below are executed and their REAL results recorded.
Handback:    completion report + rewrite `.agent/handoff.md` (<= 60 lines, or a
             "Deviations, declared" line naming the real count and the mandated
             content that caused it, per AGENTS.md DECISION D15), carrying the
             six closure values: evidence job id, package filename, package
             SHA-256, final verifier verdict, BOTH full-suite counts lines
             (R20's and the reviewer's, never collapsed — R-0296), and the
             integrity-check verdict.

C1 — the block you are executing was handed to you as
`.remedy-wt/f107-r22-1.block.md`. Copy it, do not retype it:
`cp .remedy-wt/f107-r22-1.block.md .agent/authored/f107-r22-1.md`, then
`cmp .remedy-wt/f107-r22-1.block.md .agent/authored/f107-r22-1.md` (silent,
exit 0). Record `wc -l` and `sha256sum` of the saved file. Commit alone, push:
  chore(f107): save the R22 step block verbatim

C2 — `cp .agent/authored/f107-r22-1.md .agent/last_block.md`, then
`cmp .agent/authored/f107-r22-1.md .agent/last_block.md` (silent, exit 0).
Commit alone, then push:
  chore(f107): mirror the R22 block into last block

C3 — THE FINDING PERSISTS FIRST (planner_reviewer_prompt.md §4.4)
PAIR_HDR is a REWRITE. In `.agent/live_review.md` replace the one line:
<<<BEGIN PAIR_HDR_FROM>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0297.
<<<END PAIR_HDR_FROM>>>
<<<BEGIN PAIR_HDR_TO>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0298.
<<<END PAIR_HDR_TO>>>

PAIR_LRF is an APPEND: the TO's first three lines ARE the FROM, the last three
lines of the R-0296 entry. The new entry goes directly beneath them.
<<<BEGIN PAIR_LRF_FROM>>>
  this class; not fixed here, because a timing-sensitive smoke test belongs to
  the feature that owns the suite's stability, not to the context compiler.
  OPEN.
<<<END PAIR_LRF_FROM>>>
<<<BEGIN PAIR_LRF_TO>>>
  this class; not fixed here, because a timing-sensitive smoke test belongs to
  the feature that owns the suite's stability, not to the context compiler.
  OPEN.
- R-0297 (Low, F107 R22, reviewer-side authoring defect): the R21 block ordered
  an action this environment forbids, and cost the round its second half. C5.1
  told the worker to `mkdir -p /home/decodeux/remedy-scratch-archive/f107` and
  move two scratch trees there. Every path outside `/home/decodeux/Repos/remedy`
  is denied by the session's permission layer — the worker proved it was the
  PATH and not the command by creating and removing a probe directory inside
  the repo with the same `mkdir`, and it correctly refused both the
  sandbox-override flag and a subagent detour, since an agent-authored block
  cannot grant permission the permission system withholds. The reviewer
  confirmed the same denial against its own shell before authoring this block.
  Four commits landed and C5/C6 did not, so the round is half-spent, not
  wrong. The authoring error is narrow and worth naming precisely: the block
  made a filesystem PATH load-bearing without probing that path first, the same
  class as §3's checklist item 5, which already says a block may order only
  what it has checked is reachable — item 5 speaks of code branches, and this
  is its filesystem twin. Forward-looking fix, applied in THIS block: the
  archive target is inside the repository, and the reviewer verified before
  emission both that it is gitignored and that the packager prunes it. Not a
  worker finding: two consecutive workers stopped clean at a wall rather than
  route around it, which is the behaviour the rules ask for. OPEN.
<<<END PAIR_LRF_TO>>>
Commit, then push:
  chore(f107): register R-0297, a block ordering an unreachable path

C4 — the D3 amendment. PAIR_DEC is an APPEND whose anchor is the current LAST
non-empty line of `.agent/decisions.md`; that anchor must remain exactly 1x and
must immediately precede the payload. The payload's first line is blank. D3
itself is NOT edited — a decision that was acted on is amended in the open, not
rewritten, so the record shows what was chosen and what the world refused.
<<<BEGIN PAIR_DEC_ANCHOR>>>
neither the move nor this decision is needed again.
<<<END PAIR_DEC_ANCHOR>>>
<<<BEGIN PAIR_DEC_TO_APPEND>>>

## DECISION F107 D3a (2026-08-12) — the D3 archive moves INSIDE the repo, to a path the packager already prunes

Context: finding R-0297. D3 chose to move the two offending scratch trees to
`/home/decodeux/remedy-scratch-archive/`, outside the repository. That path is
unreachable: this session's permission layer denies every filesystem access
outside `/home/decodeux/Repos/remedy`, for the worker and for the reviewer
alike. D3's REASONING survives intact — move rather than delete, and do not
edit a packager this feature does not own — only its destination was wrong.

Chosen: archive to `.remedy-wt/.cache/f107-archive/` instead. The path is
inside the repository, so it is reachable; `.gitignore:235` already ignores all
of `.remedy-wt/`, so nothing enters the review subject; and the packager's own
prune list matches it — `scripts/make_review_zip.sh:236` prunes
`-path './*/.cache'`, which `./.remedy-wt/.cache` satisfies, so `find` never
descends into it and the 1834 unsafe members never reach the archive. Both
properties were verified by the reviewer against the disk before this block was
emitted, which is exactly what R-0297 says should have happened the first time.
This is strictly better than D3's original target for the R-0288 rule as well:
the raw gate records stay inside the repo's own scratch directory, where the
protocol says scratch lives, rather than migrating to a private sibling path
that a later reader would have no reason to look in.

Alternatives considered: (a) `.data/remedy-scratch-archive/` — pruned and
ignored too, rejected because `.data` is the application's data root and agent
scratch does not belong in it; (b) widen the session sandbox to reach the
original path — rejected, a permission boundary is not an obstacle to route
around, and nothing about this feature justifies loosening one; (c) delete the
trees — rejected for the same reason D3 rejected it, and the reason has not
weakened: they are F107's own R9 and R11 raw gate records.

Reverse this decision by moving the two directories back from
`.remedy-wt/.cache/f107-archive/` to `.remedy-wt/`. The durable fix R-0295
names — one `-path './.remedy-wt'` line in the packager's prune list — retires
D3, this amendment and the move together.
<<<END PAIR_DEC_TO_APPEND>>>
Commit, then push:
  chore(f107): amend DECISION F107 D3 with a reachable archive path

C5 — relocate, rebuild, verify. NOTHING here is committed and NOTHING is
deleted. Run in this order and record the real output of each step.
1. Archive the two offending trees and the rejected package:
     mkdir -p .remedy-wt/.cache/f107-archive
     mv .remedy-wt/r11gate .remedy-wt/.cache/f107-archive/r11gate
     mv .remedy-wt/r9gate .remedy-wt/.cache/f107-archive/r9gate
     mv remedy-review-20260812-232923-READY_FOR_REVIEW.zip .remedy-wt/.cache/f107-archive/rejected-remedy-review-20260812-232923.zip
   Prove each landed with `ls -d` on the two directories and `ls -l` on the
   zip, and prove the sources are gone from `.remedy-wt/` with `ls .remedy-wt`.
   If any `mv` fails, STOP. Do not force it, do not delete, do not override.
2. `git status --porcelain` — still empty; the move touches no tracked file.
3. Move the R20 evidence bundle aside rather than overwrite it, then refresh
   the four `-v` logs so the head they record matches the head the new bundle
   will carry:
     mv .remedy-wt/f107_closure_evidence .remedy-wt/.cache/f107-archive/f107_closure_evidence_r20
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
4. Rebuild the evidence bundle at the current head:
     python3 .remedy-wt/r20_build_evidence.py
   Record the four run lines, the final verifier verdict and the job id.
5. Rebuild the package from the clean tree:
     bash scripts/make_review_zip.sh --evidence-dir
       .remedy-wt/f107_closure_evidence/remedy-job-evidence-f107-closure
   Record the printed package filename, the script's REAL exit code, the
   package_status, and `sha256sum` of the file computed by YOU.
6. Verify the package yourself. Write a short read-only python script under
   `.remedy-wt/` that opens the new zip with `zipfile` and reports: the member
   count; the count of members matching the packager's own rejection regex from
   `scripts/make_review_zip.sh:509` (MUST be 0); the count of members whose
   path starts with `.remedy-wt/.cache` (MUST be 0, proving the prune held);
   and the manifest's committed_review_subject base and head. Base MUST be
   2e4142c3ac72042ac4d704da252db263e48dcba3 and head MUST be this round's HEAD.
7. If the build fails again, record the FULL raw error and the offending paths
   and STOP. Never delete to make it pass, never substitute NO_EVIDENCE.

C6 — plan and handoff. Replace `.agent/plan.md` ENTIRELY with:
<<<BEGIN PAYLOAD_PLAN>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0298. R19 reviewed PASS at 65723390; R20 and R21 are
gated on their committed items, each having stopped short on an environment
wall rather than route around one.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R22 — the package, finally built. R-0297 records that R21's block named an
unreachable path; DECISION F107 D3a moves the archive inside the repository to
`.remedy-wt/.cache/f107-archive/`, which is gitignored and which the packager
prunes, so the 1834 unsafe members never reach the zip. The evidence bundle and
the package are rebuilt at this round's head and the package is verified by
opening it. Preconditions 1-5 otherwise hold: 22 open findings, none above
Medium, full suite re-confirmed twice, integrity check passed, Built State
current, tree clean and pushed.

## Next Steps
1. R23 — the closure commit: the reviewer-authored STATUS `[x]` line, the
   README capability sync in the SAME commit (R-0154), the final `.agent/`
   state, then the PR. Verdict PASS_WITH_RISKS for the five pre-existing
   R-0286 `[reviewer]` failures plus the R-0296 flake.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END PAYLOAD_PLAN>>>

Then rewrite `.agent/handoff.md` (you author it) with: feature and round,
branch, the commit SHAs of C1-C4, a changed-files table, the item-status table
for C1-C6, the REAL results of gates A-G, the six closure values, the
open-findings count, and the next expected action. The state block repeats the
operator brief's Fortschritt line verbatim:
  Fortschritt: ~98 % (T001-T004 ✅ · Integration Gate ✅ · Built State ✅ · Evidence + Zip ✅ · STATUS-Zeile + PR offen) — Schätzung
Commit, then push:
  chore(f107): rewrite the plan and handoff for R22

GATES — run every one, record the real output and the real exit code
A transport: `cmp` of the scratch original against `.agent/authored/f107-r22-1.md`
  (silent, exit 0), that file's `wc -l` and `sha256sum`, and the C2 `cmp`
  against `.agent/last_block.md` (silent, exit 0).
B block cap: the gate-A line count against the cap of 400 (DECISION F105 D5).
C pairs, after C3, in `.agent/live_review.md`: `^> Branch:.*Next free ID:
  R-0297` is 0, `^> Branch:.*Next free ID: R-0298` is 1, `^- R-0297` is 1,
  `^Done:` is still 13 and `^Landed:` is 0. PAIR_LRF is APPEND-shaped: its
  three-line FROM stays exactly 1x and every non-blank TO-ONLY line occurs
  exactly 1x AMONG THE LINES C3's OWN DIFF ADDS. Report added/removed from
  `git show --numstat <C3> -- .agent/live_review.md` and the count of added
  lines belonging to no TO body (must be 0).
D decisions: `grep -c '^## DECISION F107 D3a' .agent/decisions.md` is 1, the
  anchor line is still 1x, `^## DECISION F107 D3 ` is still 1 (the original is
  NOT edited), and the payload's first non-blank line directly follows the
  anchor. Report `git show --numstat <C4> -- .agent/decisions.md`.
E marker leak: `grep -c '^<<<'` is 0 in `.agent/live_review.md`,
  `.agent/decisions.md`, `.agent/plan.md` and `.agent/handoff.md`.
F artifacts: the archive proof (both directories and the zip at their new
  paths, and `.remedy-wt` no longer holding the originals), the four refreshed
  run lines, the final verifier verdict, the job id, the new package filename,
  its SHA-256 computed by you, the package_status, the script's exit code, the
  member count, the unsafe count (0), the `.remedy-wt/.cache` member count (0)
  and the manifest's committed_review_subject base and head.
G tree, push and scope: `git status --porcelain` empty, `git worktree list` the
  primary checkout alone, `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` is `0 0` after the last push,
  `git diff --name-only 56ee7dc1..HEAD` lists exactly the six `.agent/` paths
  the Change line names and NOTHING else, insertions per commit each under 500,
  and `gh pr list --state open` still returns an empty list.
── END OF BLOCK ─────────────
