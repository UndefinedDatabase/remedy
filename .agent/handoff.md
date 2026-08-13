# Handoff — F111 Diff-only repair, R16 (T003 prompt half)

Branch: feature/f111-diff-only-repair (unmerged, no PR by design). Base for
this round: d457219a (R15 PASS, recorded in C3). One production commit (C4),
one test commit (C5). Before C4 nothing imported the T001/T002 modules.

Deviations, declared (DECISION D15): 105 lines, over the cap, caused by the
mandated per-commit table, changed-files table, ten gate results a-j,
item-status table and next-action block. No section dropped. No other
deviation: TEXT-A..TEXT-D were applied byte for byte, extracted from the
authored file rather than retyped.

Ordered pre-C4 check, result: `rg -n 'repair_ctx\[|repair_context' tests/` ->
32 hits, NONE asserting an exact key set. The closest,
`test_build_repair_context_basic`, asserts individual keys plus
`"stdout" not in json.dumps(rc)`; the new keys carry no such token.

## Commits

| Item | SHA         | Subject                                              | Ins |
|------|-------------|------------------------------------------------------|-----|
| C1   | b2c98e27    | chore(f111): save the R16 step block verbatim        | 316 |
| C2   | 94c31599    | chore(f111): mirror the R16 block into last_block    | 287 |
| C3   | 987ce642    | docs(f111): record the R15 verdict and resolve R-0316 and R-0317 |  82 |
| C4   | b5b35d16    | feat(f111): carry margin-expanded repair hunks in the repair context |  70 |
| C5   | 9ac2a399    | test(f111): pin diff mode, the margin, and the visible full-file reason | 142 |
| C6   | this commit | chore(f111): refresh plan and write the R16 handoff  | see |

C6's own insertion count is NOT written inside C6. The real number is in
`git show --numstat` and is stated in the handback.

## Changed files

| Path                                             | Item |
|--------------------------------------------------|------|
| .agent/authored/f111-r16-1.md (new)              | C1   |
| .agent/last_block.md                             | C2   |
| .agent/live_review.md                            | C3   |
| packages/orchestration/builder_bridge.py         | C4   |
| tests/orchestration/test_builder_repair_loop.py  | C5   |
| .agent/plan.md                                   | C6   |
| .agent/handoff.md                                | C6   |

## Gates (command -> real exit code, counted value)

a. `sha256sum .agent/authored/f111-r16-1.md .agent/last_block.md` -> exit 0,
   both `c361c291408ccbc09c051ccedc08859de0111c70c3a43189670cccd5945a880a`,
   18501 bytes, 316 lines (< 400), no trailing whitespace. `cmp` -> exit 0.
   `.agent/last_block.md` was copied from the authored file.
b. on `.agent/live_review.md`: `grep -c '^Done:'` -> exit 0, 11 (was 9);
   `grep -c '^- R-0'` -> exit 0, 42 (unchanged); `grep -c '^### R15 — PASS'`
   -> exit 0, 1; `grep -c '^Landed:'` -> printed 0, exit 1 (the ordered pass).
c. `grep -n '_attach_diff_repair_hunks' …/builder_bridge.py` -> exit 0, exactly
   2 hits: line 269 (def) and line 412 (the single call site).
   `grep -c 'repair_mode_selected' …/builder_bridge.py` -> exit 0, 1.
d. VALUE PROBE, diff mode on -> exit 0, printed exactly:
   `repair_mode: diff`, `path: calc.py`, `start_line: 1`, `end_line: 6`.
   The patch names line 3 only; start_line 1 is the margin, not the selection.
e. VALUE PROBE, diff mode off -> exit 0, printed exactly `full_file` and
   `False` for `'diff_hunks' in repair_ctx`.
f. `pytest tests/orchestration/test_builder_repair_loop.py -q` -> exit 0,
   9 passed (was 6).
g. `pytest test_diff_repair.py test_diff_repair_response.py
   test_diff_repair_apply.py -q` -> exit 0, 71 passed, unmoved.
h. CANARY `pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed.
i. MUTATION PROBE, in worktree `.remedy-wt/r16mut` (detached at 9ac2a399,
   removed before this handback): with the body of `_attach_diff_repair_hunks`
   replaced by `raise AssertionError("mutant")` -> exit 1, 5 failed, 4 passed.
   Failing: `test_succeeds_on_second_cycle`, `test_stops_at_max_cycles`,
   `test_repair_context_passed_to_builder` (the three pre-existing tests that
   now traverse the default-on path), plus the two new ones,
   `…attaches_margin_expanded_hunks…` and `…without_line_ranges…`. The new
   `…diff_mode_off…` test stays green, which is right: mode off must not reach
   the helper. `git worktree list` -> one entry, the primary checkout.
j. `git status --porcelain` -> exit 0, empty after C6.
   `git diff --name-only d457219a..HEAD` -> exit 0, exactly the seven scoped
   paths, no others. Per-commit insertions from `git log --numstat`:
   316 / 287 / 82 / 70 / 142 / C6, each under 500.
   `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
   -> exit 0, `0	0` after the final push.

Open findings: 31 (42 registered minus 11 resolved; R-0316 and R-0317 closed by
the reviewer-authored `Done:` texts in C3). Next free id: R-0318. None is High.

Fortschritt: ~80 % (T001 ✅ · T002 ✅ · T003 Prompt-Hälfte in dieser Runde ·
T003 Apply-Hälfte offen · R-0316 ✅ · R-0317 ✅) — Schätzung

## Item status

| Item | Status   | Reason                                                 |
|------|----------|--------------------------------------------------------|
| C1   | done     |                                                        |
| C2   | done     |                                                        |
| C3   | done     | TEXT-A, TEXT-B, TEXT-C appended in that order          |
| C4   | done     | no contradiction found; no test pins the ctx key set   |
| C5   | done     | three tests added, the six existing ones untouched     |
| C6   | done     |                                                        |

## Next expected action

- Reviewer gates R16 against the real diff, re-running probes and mutation.
- Then R17 — T003's apply half: route the builder's diff answer through
  `apply_diff_repair`, emit the apply-side mode (`full_fallback`) and token
  actuals, add the fixture token comparison. Hunk TEXT lives in the repair
  context only; counts only in the timeline, and R17 must keep it that way.
