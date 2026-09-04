── STEP CLOSE/5 — F112 round 31 ────────────────────────────────
Goal: Fix README's two stale derived numerals round 30's closure commit
moved without naming, re-confirm the docs gate green, then open the
pull request. This is a closure-sequence correction round, permitted by
amend0827 rule 1's own exception.

Bundle:
1. C0a/C0b — save this block verbatim (transport proof), `cp` never
   retype.
2. C1 — append RECORD30 (below) to `.agent/live_review.md`: books round
   30's PASS-with-declared-deviation verdict. No new finding is
   registered — this is the SAME class the checklist already names, not
   a new defect shape.
3. C2 — apply PLAN31 (below) to `.agent/plan.md` (whole-file replace).
4. C3 — THE README FIX. Exactly `README.md`, two byte-precise edits,
   nothing else in the file touched:
   a. Line currently reading (verify by content before editing, not by
      line number):
        `69 of 266 registered items accepted. Next: the first unchecked item in docs/roadmap/STATUS.md.`
      becomes:
        `70 of 266 registered items accepted. Next: the first unchecked item in docs/roadmap/STATUS.md.`
      (only the `69`->`70` changes; the rest of the line is byte-identical).
   b. Line currently reading (verify by content, not by line number):
        `| 3 | Full Token Economy & Autonomy | 4 | 26 |`
      becomes:
        `| 3 | Full Token Economy & Autonomy | 5 | 26 |`
      (only the Done-column `4`->`5` changes; the rest of the line,
      including the Total column `26`, is byte-identical and UNCHANGED —
      do not touch the total).
   Before editing, independently derive both numbers yourself rather
   than trusting this block's arithmetic: count
   `^\- \[x\] F\d{3} — ` lines in `docs/roadmap/STATUS.md` (expect 70)
   and, among those, how many resolve (via each `F\d{3}`'s own feature
   file's tier, same method `tests/docs/test_docs_consistency.py`'s
   `TestPrimaryDocsAreHonest::test_the_readme_tier_table_done_column_matches_the_ledger`
   uses) to Tier 3 (expect 5). If either reading disagrees with this
   block's numbers, STOP and declare the disagreement rather than
   applying either value.
5. C4 — GATES, run for real and reported:
   - `python3 -m pytest tests/docs/ -q` — must be fully green now (was
     `2 failed, 293 passed` at round 30's C3; expect `295 passed`).
   - `python3 -m pytest tests/cli/test_golden_path.py -q` (canary,
     re-confirm).
   - `git status --porcelain` — empty.
   If tests/docs/ is STILL red after this fix, STOP before C5 and
   declare the exact new failure — do not attempt a second guess.
6. C5 — THE PULL REQUEST (AGENTS.md PR workflow), the step round 30
   halted before reaching. Push, then `gh pr create` from this branch
   into `main`. Title: short, under 70 chars, naming both the F112
   feature and the evidence-packager contract fix. Body: what changed
   and why — (1) the operator's evidence-packager verification-run
   contract fix (`R-0792`, `R-0793` — `output_hash` now always matches
   the stored `stdout_summary` bytes; `job_evidence._scrub_paths` and
   `manual_attestation._vt_run_v11` both delegate to the shared,
   already-accepted `packages.common.path_redaction.scrub_paths`), (2)
   F112's own feature — prompt budget per task class, T001-T003 — key
   decisions (round-21-already-discharged self-use discovery; the
   README-numeral sweep this round performed), how to review (start
   with `packages/orchestration/job_evidence.py` and
   `packages/orchestration/manual_attestation.py`'s diffs, then the new
   `tests/orchestration/test_job_evidence_verification_contract.py`,
   then `packages/orchestration/prompt_budget.py`/
   `context_compiler.py`'s `fit_task_context_to_class_cap`), a
   changed-files table, the latest verdict (PASS_WITH_RISKS) and open
   findings count (report the real current count, recomputed
   mechanically), runtime actuals for rounds 27-31 this session (earlier
   rounds are prior sessions — state `not-measured` for anything the
   ledger does not carry a number for). Do NOT merge it — that is the
   next round, after hosted CI reads green, per the Open PR Gate.
7. Handback — completion report + rewrite `.agent/handoff.md`. Include
   the PR number and URL, and the built zip's filename + SHA-256 once
   more for the operator to archive/formally review.

Change: `README.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/authored/f112-r31.md` (new), `.agent/last_block.md`,
`.agent/handoff.md`. Nothing under `packages/`, `apps/`, `tests/`,
`docs/roadmap/STATUS.md`, `docs/roadmap/features/`,
`scripts/self_use_queue.json` this round — those already landed
correctly at round 30's C3 and are not touched again.

Constraints:
- `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`
  are NOT touched this round.
- C3 touches ONLY the two lines named — no reformatting, no whitespace
  change, no other numeral anywhere else in `README.md`.
- Never force-push, never work on `main`. The PR is created, never
  merged, this round.
- If C4's docs gate is not green after the fix, STOP before C5 and
  declare the exact failure rather than guessing again.

Done when — run every gate and report its REAL exit code/output:
- `git status --porcelain` — empty before C0a and immediately before the
  handback commit.
- `.agent/live_review.md` reproduces at exactly `2346878` bytes
  immediately after C1 (pre-append `2342756` + 1 + RECORD30's `4121`
  bytes), byte-exact suffix; registered/`Done:`/open counts unmoved
  (354/74/280) both sides of C1.
- `.agent/plan.md` reproduces byte-identical to PLAN31 (`1700` bytes, no
  trailing newline, `## Goal`/`## Next Steps` each exactly once,
  `wc -l` under 50) after C2.
- Both README lines reproduce byte-identical to the TO text above;
  count of `69 of 266` in the file — 1 before, 0 after; count of
  `70 of 266` — 0 before, 1 after; the Tier 3 row's Done cell reads `5`
  and its Total cell still reads `26`, unchanged.
- `python3 -m pytest tests/docs/ -q` — real pass count, must be fully
  green.
- `python3 -m pytest tests/cli/test_golden_path.py -q` — real pass
  count.
- The `gh pr create` outcome — real PR number and URL.

Handback: completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

--- BEGIN RECORD30 sha256=2e49de0afd8009b49321f130aada5a6ad123c1e855a35f6dea365827efde55a2 ---
Gate: F112 R30 — the round 30 entry, the closure commit (docs/roadmap/STATUS_closure_protocol.md algorithm step 5). VERDICT PASS WITH A DECLARED REVIEWER-SIDE DEVIATION, over the range `a5df6f2b..255a4e5f` (commits C0a `be0c9e5b`, C0b `954a56cf`, C1 `38f52919`, C2 `b025d3c2`, C3 `255a4e5f` — five real content commits — plus handback commits `28af00f4` and `9b30be51`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r30.md` and `HEAD:.agent/last_block.md` both print blob `3d23ac8094b202da5e2fb4ed179c0e4b3086614c`, reproduced directly; `sha256sum .agent/authored/f112-r30.md` reproduced `0a02207955e2458e06b83d3e3361ba5d69a869af6186d0673da34317b9d6180c` at 15327 bytes. THE CLOSURE COMMIT AT C3 HELD BYTE-EXACT, REPRODUCED INDEPENDENTLY: `git diff a5df6f2b..HEAD -- docs/roadmap/STATUS.md` shows the F112 line changed from `- [~] F112 — Prompt budget per task class` to EXACTLY the ordered TO text (evidence job `79b21c8cba8b4352`, package `remedy-review-20260904-123332-READY_FOR_REVIEW.zip`, SHA-256 `b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927`, package path `/home/decodeux/Repos/remedy-history/zips`, accepted HEAD `346c178f3241fad3984dca9baea3f37e34c3892a`), byte-for-byte, and no other line in that file moved; `git diff a5df6f2b..HEAD -- README.md` shows READMEF112's paragraph landed byte-identical, exactly once, between the F110 paragraph and `Accepted in Tier 5 so far:`; `git diff a5df6f2b..HEAD -- scripts/self_use_queue.json` shows the ONLY changed value anywhere in the file is `SU-007.consumed_by`, from `""` to `"F112"` — every other byte of every other entry unchanged. `git diff --stat a5df6f2b..HEAD -- packages/ apps/ tests/ docs/roadmap/features/` is empty — `T3_F112.md` correctly untouched, precondition 4 already satisfied from round 22. THE WORKER CORRECTLY HALTED RATHER THAN FORCE A RED GATE THROUGH: `python3 -m pytest tests/docs/ -q`, reproduced by the reviewer at C3's own commit, read `2 failed, 293 passed` — `test_the_readme_accepted_count_equals_the_status_count` (README's "69 of 266" line stale against STATUS's real 70 accepted) and `test_the_readme_tier_table_done_column_matches_the_ledger` (README's Tier 3 table Done cell reads 4, the ledger derives 5) — BOTH A DIRECT, MECHANICAL CONSEQUENCE OF FLIPPING F112 TO `[x]`, which this round's own C3 correctly performed; the golden-path canary (`test_golden_path.py -q`, 42 passed) and the integrity check (`.passed=True`, `.fail_count=0`, all five checks PASS, taken at commit `255a4e5f`) both held. THE DEVIATION IS THE REVIEWER'S OWN, NOT THE WORKER'S: round 30's own authored block (item 4 of its Bundle section) named the STATUS line, the README capability paragraph and the self_use_queue edit, but never named README's own "N of 266 registered items accepted" summary line or its Tier 3 status-table Done cell — both of which necessarily move the moment any feature's STATUS line flips to `[x]`, a class of gap this repository has registered before (`R-0570`, `R-0360`, `R-0156` — the "flipping a STATUS line without sweeping README's own derived numerals" family). The worker's handling is exactly correct and is what this verdict credits: it stopped BEFORE C5 exactly as the block's own constraint ordered ("If ANY gate at C4 is not green, STOP before C5... do not attempt a fix on this round's own initiative"), reported the real red output rather than a summary, diagnosed the precise root cause (README's own derived numerals, not a defect in the closure commit's three intended files), and created NO pull request on a red gate. `git status --porcelain` reads empty. NO NEW FINDING ID IS MINTED for this: it is the SAME class the checklist's item 9/citation discipline already names (a re-swept numeral, not a new defect shape), and it is fully repaired in round 31 rather than left open — a closure-sequence correction round, explicitly permitted by amend0827 rule 1's own exception for "a feature's closure sequence." Round 31 fixes README's two stale numerals, re-runs the docs gate, and proceeds to the pull request.
--- END RECORD30 ---

--- BEGIN PLAN31 sha256=67b435cbe664767cc0da2e1607ab2e6a311869d164bd9c3ed8a58415e57c77bf ---
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1. Round 30 landed the closure commit
(STATUS [x], README capability sync, self_use_queue SU-007
consumed_by=F112) but halted before the pull request: flipping F112's
STATUS line to [x] moved README's own derived "N of 266 accepted" count
and Tier 3 table Done cell, which round 30's block never named. Round 31
fixes exactly those two numerals, re-confirms the docs gate green, and
opens the pull request.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 31 books round 30's PASS-with-declared-deviation verdict, fixes
README.md's stale "69 of 266" -> "70 of 266" line and its Tier 3 table
Done cell "4" -> "5", re-runs the docs gate to confirm green, then opens
the pull request per the AGENTS.md PR workflow. Not merged this round.

## Next Steps

- Round 32: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule; hand
  back the built zip's name and SHA-256 to the operator for archiving
  and the formal package review.

## Risks

- R-0784 and R-0767 (both OPEN, unrelated to F112) are documented,
  pre-existing risks; F112's live-review verdict is PASS_WITH_RISKS.
- Hosted CI must read green before the PR is merged; a red hosted run is
  a blocker, not something to route around.
--- END PLAN31 ---
