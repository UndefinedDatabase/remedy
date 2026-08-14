# Handback — F045 Loop definitions, round R13 (repair + report provenance)

Branch `feature/f045-loop-definitions`. Base 785373ac. No merge, no PR, no
force-push. Open findings after this round: 3 — R-0350, R-0354, R-0357.

## Range
Review of 785373ac..HEAD (7 commits).

## Commits
### b3d2ebf6 chore(f045): save the R13 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f045-r13.md` | +224/-0 | C0a, verbatim block save (cap-exempt, F104 D1) |
### 4616ff4e chore(f045): point last_block at the R13 block
| `.agent/last_block.md` | +197/-194 | C0b, byte-identical copy (cap-exempt) |
### 3ecbe404 docs(f045): register R-0357 on the inventory citation
| `.agent/live_review.md` | +2/-0 | C1, finding persisted FIRST, before any fix |
### 62fc329c docs(f045): point the terminal citation at its real module
| `.agent/f045_e2e_inventory.md` | +7/-4 | C2, FROM→TO rewrite of the Q1 paragraph |
### 679202b6 feat(f045): carry the loop reference into the run report
| `packages/orchestration/run_report.py` | +11/-0 | C3, `loop_ref` field, reader, conditional emit |
### 613b20b1 test(f045): pin the loop line in the run report
| `tests/orchestration/test_run_report.py` | +35/-0 | C4, 3 tests; ZERO deletions — no golden touched |
### C5 (this commit) docs(f045): hand back R13 with the report provenance
| `.agent/plan.md` | rewrite | 49 lines, Goal + Next Steps, open set from gate (b) |
| `.agent/handoff.md` | rewrite | this file (self-reference, R-0149 pattern) |

## External actions
`git push -u origin feature/f045-loop-definitions` after each of the 6 commits
above — exit 0 each time. `git worktree add .remedy-wt/f045_r13_redproof HEAD
--detach` → created at 613b20b1; `git worktree remove --force` + `git worktree
prune` → `git worktree list` prints ONE line. `gh pr list --state open --json
number,headRefName` → `[]`. No PR created, none merged.

## Verification
(a) `cmp .agent/authored/f045-r13.md .agent/last_block.md` → exit 0, no output.
(b) open-set script → `OPEN ['R-0350', 'R-0354', 'R-0357']` (exact match).
(c) C1 numstat `2 0 .agent/live_review.md`; the added lines are one blank plus
    ONE `- R-0357 — Low — …` line, 2059 chars, appearing exactly once.
(d) after C2: FROM-C2 count 0, TO-C2 count 1;
    `grep -c "in the same module" .agent/f045_e2e_inventory.md` → `0` (exit 1,
    no match). `grep -rn "_apply_terminal" --include=*.py packages/ apps/` →
    `long_run_executor.py:911` (def) and `:1578` (call) — the repaired citation.
(e) `pytest tests/orchestration/test_run_report.py -q` → `71 passed in 0.17s`
    (68 before C4). `-k` the three goldens → `test_green_terminal_matches_golden
    PASSED`, `test_blocked_with_decision_matches_golden PASSED`,
    `test_budget_terminal_matches_golden PASSED`, `3 passed, 68 deselected`.
    Deleted-line count for `tests/orchestration/test_run_report.py`: **0**.
(f) RED-PROOF in `.remedy-wt/f045_r13_redproof` at 613b20b1. Import probe:
    `IMPORT PATH /home/decodeux/Repos/remedy/.remedy-wt/f045_r13_redproof/
    packages/orchestration/run_report.py` — inside the worktree (R-0337).
    Both emit lines deleted → `2 failed, 1 passed`:
    `test_a_loop_job_renders_the_loop_line_right_after_the_mission` failed at
    `assert len(at) == 1` (`0 == 1`);
    `test_the_key_is_read_from_the_loop_run_constant_not_a_literal` failed at
    `assert "- Loop: nightly-tidy" in render_report(renamed).splitlines()`.
    `test_a_job_without_a_loop_renders_no_loop_line_anywhere` still passed — it
    is the negative pin and is expected to survive deletion. Worktree removed.
(g) `pytest tests/cli/test_loop_cmd.py tests/orchestration/test_loop_run.py
    tests/orchestration/test_loop_spec.py -q` → `51 passed in 0.22s`.
(h) `pytest tests/cli/test_golden_path.py -q` → `42 passed in 15.72s`.
(i) `git diff --name-only 785373ac..HEAD` before C5 → the 6 non-C5 paths; C5
    adds `.agent/plan.md` and `.agent/handoff.md` = the 8 paths in Change.
(j) `git status --porcelain` → empty before C5; `git worktree list` → 1 line.
(k) Python scan `l != l.rstrip()` over every file written this round (`grep -rn
    ' $'` not used) → `[]` for all eight. Also `ruff check` on both Python
    files → `All checks passed!`.
(l) `gh pr list --state open --json number,headRefName` → `[]`.
Post-commit re-runs of (h), (i), (j) are in the completion report — a handoff
cannot contain output from the commit that writes it.

## Authored-text proofs
FINDING-357, FROM-C2 and TO-C2 were extracted from the committed
`.agent/authored/f045-r13.md` by script and applied disk-to-disk; none was
retyped. Fidelity: (a) `cmp` exit 0; FROM 0x / TO 1x; finding 1x, 2059 chars.

## Item status
| Item | Status | Reason |
| C0a save the block | done | |
| C0b last_block | done | |
| C1 persist R-0357 | done | |
| C2 repair the citation | done | |
| C3 report change | done | local import of `LOOP_REF_METADATA_KEY` is not circular |
| C4 tests | done | |
| C5 plan + handoff | done | |

## Deviations & assumptions
Deviations, declared: this file is 98 lines, over the 60-line cap and within
the template's ≤100 allowance for >5-commit tables. Cause: the mandated
per-commit tables for 7 commits plus the 12-gate Verification transcript
(a)-(l) with real exit codes and the red-proof assertion names.
No section dropped. No `Done:` paragraph written. No golden, no `loop_run.py`,
`loop_spec.py` or `loop_cmd.py` touched. Nothing refused.

## Next
R14: the end-to-end fixture loop driving `run_cycles`, asserting the loop line
in the `report.md` actually written to `job_evidence_dir`.

Fortschritt: ~72 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
