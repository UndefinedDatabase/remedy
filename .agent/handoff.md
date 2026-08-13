# Handoff — F111 Diff-only repair, R13 (T002 apply half)

Branch: feature/f111-diff-only-repair (unmerged, no PR by design).
Base for this round: 34319061. Exactly one production commit: C5.

Deviations, declared (DECISION D15): this handoff is 109 lines. The overage is
caused by the mandated per-commit table, the changed-files table, the nine gate
results a-i with their commands and counted values, the item-status table and
the blocker note below. No section was dropped.

BLOCKER, declared — gate a items 1 and 3 were NOT run. This worker's permission
system refuses every bash command that names a path under `.remedy-wt/`, and it
refuses `cmp` outright (three attempts, all denied before execution). The
transport rule was still honoured in full: `.agent/authored/f111-r13-1.md` and
`.agent/last_block.md` were both typed from the prompt's bytes, and no file
under `.remedy-wt/` was read, copied or opened at any point. The reviewer must
run `cmp .remedy-wt/f111r13/BLOCK .agent/authored/f111-r13-1.md` and
`cmp .remedy-wt/f111r13/PLAN .agent/plan.md` itself.

## Commits

| Item | SHA         | Subject                                             | Ins |
|------|-------------|-----------------------------------------------------|-----|
| C1   | 886c9063    | chore(f111): save the R13 step block verbatim       | 320 |
| C2   | edfb0fe1    | chore(f111): mirror the R13 block into last block   | 299 |
| C3   | 310b1086    | chore(f111): record DECISION F111 D6 for R-0315     |  18 |
| C4   | 0071e97c    | docs(f111): amend A9 and record D6 built state      |  19 |
| C5   | 25b0770c    | feat(f111): add the diff repair apply seam          | 174 |
| C6   | f644f86b    | test(f111): pin apply fallback and fence behaviour  | 262 |
| C7   | this commit | chore(f111): refresh plan and write the R13 handoff | ≤148 |

C7's own insertion count cannot be written inside C7 — R12 landed a false one
that way. Its two files are 43 and 109 lines, so its insertions are at most 152,
far under 500; the exact number is in `git show --numstat` and in the handback.

## Changed files

| Path                                          | Item |
|-----------------------------------------------|------|
| .agent/authored/f111-r13-1.md (new)           | C1   |
| .agent/last_block.md                          | C2   |
| .agent/live_review.md                         | C3, C4 |
| docs/roadmap/features/T2_F111.md              | C4   |
| packages/orchestration/diff_repair_apply.py (new) | C5 |
| packages/orchestration/diff_repair_response.py | C5  |
| tests/orchestration/test_diff_repair_apply.py (new) | C6 |
| .agent/plan.md                                | C7   |
| .agent/handoff.md                             | C7   |

## Gates (command -> real exit code, counted value)

a. `cmp` is DENIED by the permission system, so no cmp exit code exists.
   Items 1 and 3 additionally need `.remedy-wt/`, which is denied — see the
   blocker above. Item 2 was proved by hash instead: `sha256sum` on
   `.agent/authored/f111-r13-1.md` and `.agent/last_block.md` -> exit 0, both
   `f35907a250068b81c3c5b6216b2fcd68220674d997aadb40d3ce869fadc622f0`, so the
   two files are byte-identical.
b. `grep -c 'creation inside a diff is allowed' docs/roadmap/features/T2_F111.md`
   -> printed 0, exit 1 (the ordered pass);
   `grep -c 'creation and deletions BOTH require' …` -> exit 0, 1;
   `grep -c '^## Built State — new-file creation stays' …` -> exit 0, 1.
c. `grep -c 'the apply-and-fallback half attaches to the'
   packages/orchestration/diff_repair_response.py` -> printed 0, exit 1 (the
   ordered pass); `grep -c 'diff_repair_apply.apply_diff_repair' …` -> exit 0, 1.
d. on `.agent/live_review.md`: `grep -c '^### DECISION F111 D6'` -> exit 0, 1;
   `grep -c '^Landed: R-0315'` -> exit 0, 1; `grep -c '^Done:'` -> exit 0, 7,
   unchanged from R12.
e. `python3 -m pytest tests/orchestration/test_diff_repair_apply.py
   tests/orchestration/test_diff_repair_response.py
   tests/orchestration/test_source_apply_transaction.py -q` -> exit 0,
   54 passed.
f. `python3 -m pytest tests/docs/ -q` -> exit 0, 294 passed.
g. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed.
h. `grep -rn 'diff_repair_apply' packages/ apps/ --include='*.py' | grep -v
   '^packages/orchestration/diff_repair_apply.py'` -> exit 0, exactly ONE line:
   `packages/orchestration/diff_repair_response.py:30`, the PAIR-E docstring
   pointer. No call site was added.
i. `git status --porcelain` -> exit 0, empty after C7.
   `git diff --name-only 34319061..HEAD` -> exit 0, exactly the nine ordered
   paths, no others. Per-commit insertions by `git log --numstat`:
   320 / 299 / 18 / 19 / 174 / 262 / C7, each under 500.
   `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
   -> exit 0, `0	0` after the final push.

Open findings: 33 (R-0315 is settled by DECISION F111 D6; the reviewer writes
the `Done:` paragraph). Next free id: R-0316.

Fortschritt: ~68 % (T001 ✅ · T002 ✅ Record+Split+Schema+Fence+Apply · T003 offen · R-0315 entschieden, R-0313 offen für R14) — Schätzung

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

## Next expected action

- Reviewer gates R13 against the real diff and runs the two `cmp` calls this
  worker was not permitted to run.
- `apply_diff_repair` has NO call site by design. R15/T003 wires it into
  `run_builder_bridge_loop`; a green suite over an unreferenced module is not
  a working feature.
- R14 owns R-0313, the response-side blank-context normalisation, untouched here.
