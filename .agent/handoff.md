# Handback — plan0806 (registration F255 + self-drive planning)

Branch: feature/reg-f255-teacher-role. Registration micro-round
(precedent reg0803) + planning extension. PR created after this
commit, NOT merged; it merges at the next round's Open PR Gate.
F079 PR #181 was merged by this round's Open PR Gate (main 7007cf2a).

## Changed files per commit
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 419a6243 | docs/roadmap/STATUS.md | +1/-0 | F255 line appended to Tier 5 list |
| 419a6243 | docs/roadmap/features/T5_F255.md | +49/-0 | new feature file, scope verbatim |
| 419a6243 | tests/docs/test_docs_consistency.py | +4/-3 | TOTAL_FEATURES 254 -> 255 + registry comment |
| 419a6243 | README.md | +2/-2 | "of 255"; Tier 5 total 29 (same commit — ledger atomicity) |
| B (this) | .agent/selfdrive_package.md | new | full S1–S5 package + sequence + runtime rows |
| B (this) | .agent/plan.md | rewrite | plan0806 state, operator constraint verbatim, sequence |
| B (this) | .agent/context.md | rewrite | branch/scope/constraints for this round |
| B (this) | .agent/handoff.md | rewrite | this handback |

## Presence checks (all empty before registering)
    grep -rn "F255" docs/roadmap/STATUS.md          -> no hit
    ls docs/roadmap/features/ | grep F255           -> no hit
    grep -rn -i "teacher" docs/roadmap/features/    -> no hit

## Gates
    python3 -m pytest tests/docs/ -q                   -> exit 0 (293 passed)
    python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0 (42 passed)
Precondition gate ran green before any edit (293 passed); both gates
re-ran green after the registration commit.

## Open findings
0 this round. Carry-forward: .agent/candidates.md still holds R-0200,
R-0202 and the xdist-flake id — they block the F080 claim (its R1
sweeps them), not this registration.

## Next expected action
F080 (Machine-readable roadmap mirror & STATUS.md) in a fresh
session; its first block runs the Open PR Gate and merges this PR.
Then S1+S2 skill build, S4 rehearsal on F254 — see
.agent/selfdrive_package.md. Hard date 2026-08-12.

## Item status
| Item | Status | Reason |
|---|---|---|
| P1 precondition gate | done | 293 passed pre-edit |
| P1 presence checks | done | all three empty |
| P1 register F255 | done | commit 419a6243, ledger atomicity in one commit |
| P1 gates + PR | done | both green; PR number in completion report |
| P2 plan extension | done | selfdrive_package.md + plan.md rewrite, this commit |
