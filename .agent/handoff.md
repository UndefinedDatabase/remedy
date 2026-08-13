# Handoff — F111 Diff-only repair, R14 (T002 close, R-0313)

Branch: feature/f111-diff-only-repair (unmerged, no PR by design).
Base for this round: 9a17fad2. Exactly one production commit: C4.

Deviations, declared (DECISION D15): this handoff is over the 60-line cap. The
overage is caused by the mandated per-commit table, the changed-files table,
the nine gate results a-i with their counted values, the item-status table and
the block-contradiction note below. No section was dropped.

DEVIATION, declared — C5 case 3. The block ordered the input
`DIFF_ONE_FILE + "\n" + second section of DIFF_TWO_FILES` with the assertion
"output equals input". That assertion CANNOT hold under the C4 algorithm the
same block ordered, and the two are inconsistent by measurement, not by
opinion: `DIFF_ONE_FILE` declares `@@ -1,3 +1,3 @@` over a body that spends
only two old and two new lines, so at the separator blank the hunk still has
`old_remaining=1, new_remaining=1` and step 4 fires exactly as written. Real
output on that input:
`'…+value = 2\n \n--- a/src/util.py…'` — the separator became " ".
Safe reading applied (precedent R-0274, R-0280): the PRODUCTION algorithm was
implemented verbatim, unweakened, and case 3 proves the ordered PROPERTY with a
first section whose header matches its body (`@@ -1,2 +1,2 @@`), where the
separator is provably out of budget and is left untouched. The measurement and
the reason are written into that test's own docstring. Reviewer decides whether
`DIFF_ONE_FILE`'s inflated header is itself worth a finding: a model that
over-declares a hunk count now gets a separator blank silently converted.

## Commits

| Item | SHA         | Subject                                             | Ins |
|------|-------------|-----------------------------------------------------|-----|
| C1   | 8ff44b05    | chore(f111): save the R14 step block verbatim       | 293 |
| C2   | 66c97c74    | chore(f111): mirror the R14 block into last block   | 224 |
| C3   | f3e99b1f    | chore(f111): resolve R-0315, register R-0316, gate  |  70 |
| C4   | 0b554660    | feat(f111): restore stripped blank context lines    |  96 |
| C5   | 23f0019f    | test(f111): pin blank context normalisation, apply  | 102 |
| C6   | this commit | chore(f111): refresh plan and write the R14 handoff | see |

C6's own insertion count is NOT written inside C6 — R12 landed a false one that
way and R13 was faulted for guessing a bound instead. The real number is in
`git show --numstat` and is stated in the handback.

## Changed files

| Path                                            | Item |
|-------------------------------------------------|------|
| .agent/authored/f111-r14-1.md (new)             | C1   |
| .agent/last_block.md                            | C2   |
| .agent/live_review.md                           | C3   |
| packages/orchestration/diff_repair_response.py  | C4   |
| tests/orchestration/test_diff_repair_response.py| C5   |
| tests/orchestration/test_diff_repair_apply.py   | C5   |
| .agent/plan.md                                  | C6   |
| .agent/handoff.md                               | C6   |

## Gates (command -> real exit code, counted value)

a. `sha256sum .agent/authored/f111-r14-1.md .agent/last_block.md` -> exit 0,
   both `1113f75d07f29bd2bb1218a1f793a5917636c0dd55f2d0a3291bc4af8a9ddaaf`.
   No path under `.remedy-wt/` was read, listed or copied at any point; the
   two files were typed from the prompt bytes. The reviewer runs its own cmp.
b. on `.agent/live_review.md`: `grep -c '^Landed:'` -> printed 0, exit 1 (the
   ordered pass); `grep -c '^Done:'` -> exit 0, 8; `grep -c '^- R-0'` -> exit
   0, 41; `grep -c '^### R13 — PASS'` -> exit 0, 1.
c. `grep -c 'def normalize_diff_blank_context' …/diff_repair_response.py`
   -> exit 0, 1; `grep -c 'split_diff_by_path(normalize_diff_blank_context' …`
   -> exit 0, 1.
d. VALUE PROBE -> exit 0, printed exactly
   `'@@ -1,3 +1,3 @@\n a\n \n-b\n+B\n'`.
e. VALUE PROBE -> exit 0, printed exactly `'a\n\nB\n'`. The same call without
   `n()` printed `None` before this round, measured on this machine at C4.
f. `pytest test_diff_repair_response.py test_diff_repair_apply.py
   test_diff_repair.py -q` -> exit 0, 68 passed (was 62 before C5).
g. `pytest test_source_apply.py test_source_apply_transaction.py -q` -> exit 0,
   55 passed. The applier is untouched and the number did not move.
h. `pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed.
i. `git status --porcelain` -> exit 0, empty after C6.
   `git diff --name-only 9a17fad2..HEAD` -> exit 0, exactly the eight ordered
   paths, no others; `source_apply.py` and `diff_repair_apply.py` untouched.
   Per-commit insertions from `git log --numstat`: 293 / 224 / 70 / 96 / 102 /
   C6, each under 500.
   `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
   -> exit 0, `0	0` after the final push.

Open findings: 33 (R-0315 resolved by the reviewer-authored `Done:` text;
R-0313 fixed here and awaiting the reviewer's `Done:`; R-0316 registered and
OPEN for R15). Next free id: R-0317.

Fortschritt: ~72 % (T001 ✅ · T002 ✅ komplett · T003 offen · R-0315 ✅ · R-0313 ✅ · R-0316 offen für R15) — Schätzung

## Item status

| Item | Status   | Reason                                                |
|------|----------|-------------------------------------------------------|
| C1   | done     |                                                       |
| C2   | done     |                                                       |
| C3   | done     |                                                       |
| C4   | done     | algorithm implemented verbatim, unweakened            |
| C5   | deviated | case 3's ordered input contradicts C4; see above      |
| C6   | done     |                                                       |

## Next expected action

- Reviewer gates R14 against the real diff, runs its own transport cmp, and
  rules on the C5 case-3 contradiction — the block's own defect, not a scope
  drift, and disclosed rather than routed around.
- `normalize_diff_blank_context` is reached only through
  `diff_repair_response_to_patch`. `apply_diff_repair` still has NO call site;
  R15/T003 wires it into `run_builder_bridge_loop` and fixes R-0316 there.
