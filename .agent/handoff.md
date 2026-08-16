# Handback — F083 CI self-check, R13

Feature F083, round R13 — measure the serial cost of `remedy ci`. Branch
`feature/f083-ci-self-check`. No pull request created, as ordered.

## Range

Review of 6af03d95..HEAD. C4 is HEAD and cannot table its own SHA or insertion
count (R-0371, R-0149) — both are in the round's final message.

## Commits

### f3ab6cc4 docs(f083): save the R13 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r13.md | +281/-0 | C0a — the block, verbatim |

### 01dd9481 docs(f083): mirror the R13 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +180/-99 | C0b — byte-identical mirror |

### 03f2f88a docs(f083): record the R12 PASS and register R-0474
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C1 — RECORD-R12 appended at EOF |

### 20d3cd07 docs(f083): record the measured serial stage cost as Q10
| Path | +/- | Reason |
|---|---|---|
| .agent/f083_inventory.md | +90/-0 | C2 — `## Q10` appended |

### 322a77c8 docs(f083): point the plan at the R14 budget work
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18/-11 | C3 — PLAN slice as a whole file |

C4 writes `.agent/handoff.md`, the sixth path of the change set.

## External actions

None before C4 — no push, no PR, no gh command, no worktree add or remove. The
push, the post-C4 clean-tree reading and the open-PR list postdate C3 and go to
the round's final message (R-0449, R-0452).

## Verification

1. `pwd` = /home/decodeux/Repos/remedy. `git status --porcelain` EMPTY before the
   first commit and again before C4. `git worktree list` ONE line both times.
   `.agent/STOP` ABSENT both times.
2. BASE: `git rev-parse HEAD` before MY first commit (C2) = 03f2f88a, NOT
   6af03d95 — see Deviations 2. `git rev-parse f3ab6cc4^` =
   6af03d95ceaa2b5dd9e95de1de25ee0cfe4bb2c6.
3. TRANSPORT: `.agent/authored/f083-r13.md` and `.agent/last_block.md` are both
   sha256 75da10a8a4eb11ee, 23716 bytes, 281 lines, and EQUAL; each equals its
   committed blob at C0a and C0b. Measured line count 281, at or under the
   400-line cap.
4. C1 prefix property holds; `post[len(pre):]` is byte-equal to one newline plus
   RECORD-R12 extracted from the COMMITTED authored file. numstat `4 0`.
5. C2 prefix property holds; the tail BEGINS with the ordered
   `\n## Q10 — Serial stage cost through the production runner, measured at R13\n`.
   numstat `90 0`.
6. `^## Q\d` counts 10, ordered Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 Q10, none repeated.
   `## Q5 — Measured wall time and outcome per stage` = 1;
   `## Q9 — Stage runtime, measured at R11` = 1.
7. `## Q10` holds 14 table rows: 12 SAMPLE rows (fast 3, standard 3, ui 3,
   smoke 3), 1 uncapped-probe row (standard), 1 `excluded` not-run row. Red
   control exit code 5. Sample exit codes — fast 0/0/0, standard 124/124/124,
   ui 0/0/0, smoke 0/0/0, uncapped probe 0. ONE uncapped probe was run, for
   `standard`, because all three of its samples returned 124; fast, ui and smoke
   returned no 124, so none was run for them and none was needed. `not measured`
   appears 6 times, `not run` 2 times. I declare that `## Q10` contains no
   ceiling, no budget number and no recommendation.
8. Each its own process, exit code read from that process — test_ci_stages.py 0
   `7 passed`; test_ci_stage_selection.py 0 `9 passed`; test_ci_cmd.py 0
   `6 passed`; test_ci_run.py 0 `8 passed`.
9. test_dashboard_contract.py 0 `70 passed`; test_resource_safety.py 0
   `21 passed`; test_integrity_gate.py 0 `15 passed`; test_golden_path.py 0
   `42 passed`. All eight gate paths resolve on disk (R-0438).
10. C3 `.agent/plan.md` byte-equals the PLAN slice, sha256 2043c38937c87ca3,
    39 lines (<50), `## Goal` and `## Next Steps` present, 0 `- [ ]` lines,
    1 numbered item under `## Next Steps`.
11. `git diff --name-only 6af03d95..HEAD -- packages/ apps/ tests/ scripts/
    docs/` printed NOTHING, run from /home/decodeux/Repos/remedy.
12. Integrity: passed true, fail_count 0, check_count 5; handler_import pass
    `handlers=338`, live_review_verdict pass, plan_consistency pass,
    relevant_untracked pass, high_blockers_open pass.
13. Open set at HEAD: 102 registered, 6 `Done:`, 0 `Landed:`, open 96, max
    R-0474, next free R-0475, no duplicate id.
14. Change set at C3 — 5 paths: `.agent/authored/f083-r13.md`,
    `.agent/f083_inventory.md`, `.agent/last_block.md`, `.agent/live_review.md`,
    `.agent/plan.md`. C4 adds `.agent/handoff.md` as the sixth.
15. Insertions: C0a 281, C0b 180 (verbatim single-state-file rewrite,
    AGENTS.md-exempt, reported anyway), C1 4, C2 90, C3 18. None over 500.

THE READING THE ROUND EXISTED FOR: today's `remedy ci` TRUNCATES `standard`.
Three samples, three exit 124s at the runner's own 600 s default; the uncapped
probe at `REMEDY_PYTEST_TIMEOUT_SEC=5400` completes it green in 927.72 s.

## Authored-text proofs

RECORD-R12 and PLAN were both extracted from the COMMITTED
`.agent/authored/f083-r13.md` by their own markers and compared disk-to-disk:
RECORD-R12 equals C1's appended tail exactly, and PLAN equals `.agent/plan.md`
byte-for-byte at sha256 2043c38937c87ca3. `## Q10`'s body is worker-authored
from measurements, so no byte-equality proof exists for it and the block orders
none (its SHAPES paragraph).

## Deviations & assumptions

1. This handback is 164 lines, over BOTH the ≤60-line AGENTS.md cap and the
   ≤100-line >5-commit cap. Cause is mandated content only: five per-commit
   tables, fifteen gate values and a 21-row item-status table covering every
   C-item and every gate. No section was dropped (D15, R-0462).
2. Gate 2 measured 03f2f88a because C0a, C0b and C1 were already committed when
   this worker took the round over at C2. The block's BASE clause holds at the
   block's OWN first commit: `f3ab6cc4^` is 6af03d95. Declared, not repaired;
   6af03d95 stayed the base of every range gate.
3. Scratch: `.remedy-wt/f083-r13/` did NOT exist before this worker created it.
   It is gitignored (`.gitignore:235`) and nothing in it entered the change set.
4. The background sample driver was killed once by the session harness, after
   `excluded#1` was recorded and before the uncapped probe finished. The driver
   is resumable off `samples.jsonl`: it was relaunched, skipped all 14 recorded
   samples and re-ran only the probe. No sample was lost or double-counted.
5. No `run_command=` injection was used — every sample went through the
   production `_run_via_subprocess`, with the sample process's own stdout and
   stderr redirected to a per-sample log that the summary line was read from. No
   log reached the runner's 512 KiB cap (largest 14062 bytes), so no summary
   line is quoted out of a truncated stream.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit; cannot table its own SHA |
| Gate 1 | done | |
| Gate 2 | deviated | HEAD 03f2f88a at C2; `f3ab6cc4^` = 6af03d95 |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Gate 6 | done | |
| Gate 7 | done | |
| Gate 8 | done | |
| Gate 9 | done | |
| Gate 10 | done | |
| Gate 11 | done | |
| Gate 12 | done | |
| Gate 13 | done | |
| Gate 14 | done | |
| Gate 15 | done | |

## Next

R14 writes the budget and determinism stages from the `## Q10` samples, never
from the `-n auto` readings in `## Q9`; rules on R-0468 from the 26-error ruff
baseline `## Q10` records; and settles the determinism stage's shape as a
DECISION. Open findings 96, max R-0474, next free R-0475.

Fortschritt: 45 % (F083 beansprucht · R1 bis R7 und R9 bis R12 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests samt Live-Wächter als Code gelandet · R13 misst zum ersten Mal, was `remedy ci` seriell wirklich kostet, denn jede bisherige `-n auto`-Messung beschreibt einen Lauf, den das Kommando gar nicht ausführt · noch keine Determinismus- oder Budget-Stage, kein Ceiling, keine hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt
