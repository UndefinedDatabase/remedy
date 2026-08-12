# Handoff — F107 R1 (claim + candidate sweep + state reset)

Branch: feature/f107-context-compiler-v2 (cut from main at 2e4142c3).
Open findings: 8 (R-0221/0239/0247/0262/0265/0266/0268 carried, R-0270 registered this round). Next free ID: R-0271.

## Commits

| Item | SHA      | Subject                                            |
|------|----------|----------------------------------------------------|
| C1   | ef5e31be | chore(f107): save the R1 claim step block verbatim |
| C2   | d86fb80f | chore(f107): mirror the R1 block into last_block   |
| C3   | 17b91df1 | chore(f107): claim F107 in the ledger              |
| C4   | 2a2f2686 | chore(f107): reset live_review and register R-0270 |
| C5   | ab72b132 | chore(f107): empty candidates after the R-0270 sweep |
| C6   | 8c3867bd | chore(f107): rewrite plan for F107                 |
| C7   | 80e5680f | chore(f107): rewrite context for F107              |
| C8   | self-ref | chore(f107): rewrite handoff for R1 (this commit)  |

## Changed files

| File                        | Change                                  |
|-----------------------------|-----------------------------------------|
| .agent/authored/f107-r1-1.md | new; byte-copy of the R1 step block    |
| .agent/last_block.md        | byte-copy of the authored block         |
| docs/roadmap/STATUS.md      | one line: F107 `[ ]` → `[~]`            |
| .agent/live_review.md       | slice LR (registers R-0270, 7 carried)  |
| .agent/candidates.md        | slice CAND (emptied after sweep)        |
| .agent/plan.md              | slice PLAN                              |
| .agent/context.md           | slice CTX                               |
| .agent/handoff.md           | this rewrite (C8)                       |

## Gate results (command → exit → counted value)

a. python3 .remedy-wt/f107_r1_extract.py → 0 → 6/6 slices MATCH marker digests; cmp authored vs last_block → 0 (silent).
b. grep -c -F -- '- [~] F107 — Context compiler v2' STATUS.md → 0 → 1; grep -c -F -- '- [ ] F107' STATUS.md → 1 → 0.
c. cmp live_review/candidates/plan/context vs .check files → 0 (silent).
d. grep -c '^## Steps' live_review → 0 → 1; grep -c '^<<<' on live_review,
   candidates, plan, context, handoff → 1 → 0 each; wc -l plan.md → 0 → 29.
e. python3 -m pytest tests/docs/ -q → 0 → 294 passed (at C3 tree; rerun at
   the pre-C8 tree, whose docs/ equals HEAD).
f. python3 -m pytest tests/cli/test_golden_path.py -q → 0 → 42 passed.
g. git status --porcelain → 0 → empty; HEAD == origin/branch after push.
h. insertions (git log --numstat): C1 274, C2 265, C3 1, C4 62, C5 2,
   C6 22, C7 30, C8 below 100 — each < 500 (single-file .agent rewrites
   also exempt per AGENTS.md F104 D1).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1   | done   |        |
| C2   | done   |        |
| C3   | done   |        |
| C4   | done   |        |
| C5   | done   |        |
| C6   | done   |        |
| C7   | done   |        |
| C8   | done   | self-ref: own SHA and final g not writable inside itself |

Next expected action: R2 — T001 import-neighbor graphs (Python ast + documented TS/JS line scanner).
