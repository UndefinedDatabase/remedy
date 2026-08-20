# Handback — F255 R3 (Teacher role · ruling round)

Fortschritt: ~8 % (F086 merged · F255 claimed · R2 measured the ground · R3 ruled six DECISIONs · R4 amends the feature file next) — Schätzung

## Range

Review of `73d7d6e2..HEAD` — six commits: C0a `f728166b` · C0b `8228c53f` · C1 `b4def48c` · C2 `0b018e32` · C3 `5ce2edd7` · C4 this commit.

## Commits

### f728166b docs(state): save the F255 R3 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f255-r3.md | 384/0 | the R3 block, copied from `.remedy-wt/f255-r3.md` |

### 8228c53f docs(state): mirror the F255 R3 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 327/193 | same file mirrored; replaces the R2 block |

### b4def48c docs(review): record the R2 verdict
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 2/0 | RECORDR2 appended after one blank line |

### 0b018e32 docs(decisions): rule the six F255 design decisions
| Path | +/- | Reason |
|------|-----|--------|
| .agent/decisions.md | 186/0 | DECISIONS255 appended after one blank line: D1..D6 |

### 5ce2edd7 chore(plan): advance the plan to F255 R3
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 23/22 | whole-file replacement by PLAN255R3 |

C4 rewrites `.agent/handoff.md` alone and cannot table its own commit (template
self-reference exception, R-0149). Its `+/-` cell and the complete six-commit
change set are in the round report, as G8 orders.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | this commit |

## External actions

`git push` on feature/f255-teacher-role after C4 — output in the round report.
No PR created, no worktree added or removed, no `gh` command, no CI run watched
(constraint 9).

## Verification

G1 HYGIENE — `.agent/STOP` read from disk before C0a: ABSENT. Branch feature/f255-teacher-role; `git status --porcelain` EMPTY after all six commits; `git worktree list` = the primary checkout alone.
G2 TRANSPORT — `.remedy-wt/f255-r3.md`, `f728166b:.agent/authored/f255-r3.md` and `8228c53f:.agent/last_block.md` are all sha256 `afb54baf…7aaf09`, 28352 B, 384 lines: all three EQUAL.
G3 SLICES — extracted programmatically from the committed authored blob by its marker pairs, never retyped; newline convention = trailing newline INCLUDED. RECORDR2 `80ea3987…` 4787 B 1 line; DECISIONS255 `4a68cf40…` 10851 B 185 lines; PLAN255R3 `202965c9…` 2470 B 43 lines. STRIPPED-convention digests in the round report.
G4 VERDICT ENTRY — pre-C1 blob is a byte-exact PREFIX of the post-C1 blob; remainder `aba1b59e…` 4788 B 2 lines, blank separator PRESENT, remainder == blank line + RECORDR2 byte for byte. Independent paragraph split: 185 units, LAST unit == RECORDR2, sha256 `80ea3987…` (4787 B, newline INCLUDED) and `74c6e6a0…` (4786 B, STRIPPED). Negative control (one byte of the expected remainder flipped): BOTH readings reject. Sets UNCHANGED — base `73d7d6e2` 178 registered / 0 resolved / 178 open / 0 line-anchored `Landed:`, C1 `b4def48c` 178 / 0 / 178 / 0. `Gate: R3 — the R2 entry.` occurs 1x, is the LAST line beginning `Gate: R` (3 such lines), and no `Gate: R` header key repeats.
G5 DECISIONS — pre-C2 blob is a byte-exact PREFIX of the post-C2 blob; remainder == blank line + DECISIONS255 byte for byte (10852 B, 186 lines). `^## DECISION F255 D` count: 0 at the base, 6 at C2. Headings in order: D1 the teacher joins BOTH role vocabularies · D2 F255 does NOT close its own event-vocabulary dependency · D3 teacher spend is REPORTED per role, and no new limit axis is built · D4 read-only is proven BEHAVIOURALLY, because the annotation proves nothing · D5 F255 ships `remedy teach` and does NOT build `do watch` · D6 the handback token cap is withdrawn; the LINE cap is the operative bound — each dated (2026-08-20). Of 389 heading lines in the file, 0 occur twice.
G6 PLAN — `5ce2edd7:.agent/plan.md` byte-equals PLAN255R3: sha256 `202965c9…`, 2470 B, 43 lines (< 50). `## Goal`, `## Next Steps` and the roadmap F-id `T5_F255` all occur.
G7 ROUND GATE — run SERIALLY in the primary checkout. `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, `160 passed`. `python3 -m pytest tests/cli/test_golden_path.py -q -rf` → exit 0, `42 passed`. Both equal the counts measured at `73d7d6e2`.
G8 CHANGE SET — `git diff --name-only 73d7d6e2..HEAD` equals the Change list with no path on either side alone; the same command scoped to `apps/ packages/ tests/ docs/ scripts/` is EMPTY. All eight named paths are PRESENT at the base and ABSENT from the range. Every commit has ONE parent. Insertion columns 384, 327, 2, 186, 23 and C4's (round report) — all under 500. Reflog, as two measured claims (R-0601): commit-producing entries reading `commit` = 6, equal to this round's commit count; entries whose OPERATION PREFIX (text before the first colon of `%gs`) contains `amend`, `reset`, `rebase` or `cherry` = 0.
G9 NO MARKER LEAKED — lines beginning `<<<SLICE ` or `<<<END ` : 0 in `.agent/live_review.md` at C1, 0 in `.agent/decisions.md` at C2, 0 in `.agent/plan.md` at C3, 0 in `.agent/handoff.md` at C4.
G10 PUSH — `git push` run after C4; real output in the round report. No PR, no CI wait.

## Authored-text proofs

All three slices were extracted from the COMMITTED `.agent/authored/f255-r3.md`
(`f728166b`) by marker pair and applied byte for byte, never retyped or
rewrapped. Disk-to-disk equality against that file: RECORDR2 and DECISIONS255
each equal their append remainder minus the blank separator; PLAN255R3 equals
`.agent/plan.md` at C3 exactly (G4, G5, G6). Zero marker lines reached any
target file.

## Deviations & assumptions

- ORDERED SEQUENCE FOLLOWED EXACTLY: six commits, C0a → C0b → C1 → C2 → C3 → C4,
  no extra commit, none dropped, none reordered.
- NO COMPLIANCE CLAIMED WITH THE TEMPLATE'S 800-TOKEN CAP. DECISION F255 D6,
  landed by C2 this round, withdraws it; the LINE cap the six-commit table earns
  (≤100) is the bound this file is measured against. The template still carries
  the withdrawn sentence — the docs round after R4 removes it (D6 "WHERE THIS
  LANDS"), so the disagreement on disk is scheduled, not overlooked.
- NO RULING WAS ACTED ON. No role, command, test or config key was added and
  `docs/roadmap/features/T5_F255.md` was NOT amended (constraint 6). R4 does that.
- NO SLICE WAS EDITED and no slice appeared wrong.
- G7's exit codes were printed by a serial `subprocess` wrapper because the
  session's bash guard rejects `${PIPESTATUS[0]}`; the two pytest commands are
  the block's verbatim ones. Both suites also ran once directly, same results.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from
disk. Its SECOND is R4: amend `docs/roadmap/features/T5_F255.md` from the six
DECISIONs C2 landed, replacing the superseded `do watch` phrasing. R3 awaits
review. There is no open pull request.
