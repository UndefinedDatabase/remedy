# Handback — F085 Sandbox hardening (stage 1) — R26

Feature F085 · Round R26 · Branch `feature/f085-sandbox-hardening`
Base 5b02cff9 · pre-C4 HEAD 3b4231d2 · open findings 117 · next free id R-0517
Fortschritt: ~80 % (T001 gebaut · R13-R25 PASS · T002a KOMPLETT · T002b: Seam
gebaut, `test_runner` + `autorun` migriert · T002b Rest, T002c-d, T003 offen) —
Schätzung.

## Range

Review of 5b02cff9..HEAD — 6 commits: C0a C0b C1 C2 C3 C4.

## Commits

### cd1666d7 docs(f085): save the R26 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r26.md | +313 | R26 block verbatim; 26 markers, 13 pairs |

### be6c0b6e docs(f085): mirror the R26 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +258/-241 | byte copy of the committed R26 blob |

### b77cb568 docs(review): record the R25 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +35 | RECORD1 appended: blank line + 34 slice lines |

### e0b5e8fd refactor(f085): guard the autorun test-class spawns
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/autorun.py | +12/-7 | 3 test-class spawns onto the seam |

### 3b4231d2 docs(f085): advance the plan to R26
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +5/-6 | PLANF→PLANT; Goal and Risks byte-identical |

### C4 (this commit) docs(f085): rewrite the handback for R26
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file; cannot table itself (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | ran under the corrected 313-line gate; see Deviations |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

`git worktree add .remedy-wt/probe HEAD --detach` → created at e0b5e8fd (G8);
`git worktree remove --force` + `git worktree prune` → removed, list is 1 line.
`git push -u origin feature/f085-sandbox-hardening` → run after this commit.
No PR created, nothing merged.

## Verification

G1 exit 0. `.agent/STOP` absent before C0a and before C4; `git status --porcelain`
empty at round start and after C0a-C3; `git worktree list` = 1 line.
G2 authored blob, last_block blob and BOTH working copies byte-EQUAL: sha256
4220f7db082fd722fa28163fdbdfe2684f6c0ec42d772c866106009c26402908, 16616 B, 313
lines, 26 markers; regions 1-60 9a91a0ce · 61-140 41d355bc · 141-end e34ff2fa.
G3 pre-commit blob is a byte-exact PREFIX; remainder = one blank line + RECORD1
(2671 B = 1 + 2670); 0 markers landed; RECORD1's first line 1x; HEAD blob ==
working copy; `git show --numstat b77cb568 -- .agent/live_review.md` → `35  0`.
G4 FLAT: 131 registered / 14 done / 0 landed, 117 open at base AND at HEAD; all
three symmetric differences EMPTY; 0 duplicate ids; 0 resolutions naming an
unregistered id; max R-0516, next free R-0517.
G5 autorun.py: `subprocess.run(` 0x (3x at base); 5 FROM texts 0x, 5 TO texts 1x;
`run_guarded_test_command` 5x = 3 call sites + 2 imports; AST says both functions
read ONLY `.returncode`; `import subprocess` kept in `_run_fixture_builder`, gone
from `_run_repair_loop_fixture`; sha256 6d2b0d8aaecad48a5…266b9aa0412, 27438 B.
G6 PLANF 0x, PLANT 1x; `## Goal` and `## Risks` BYTE-IDENTICAL to base; sha256
a6fea08db28a9c3a7…2d5c4d6c66250, 2396 B, 41 lines (<50); Next Steps → 1, 2, 3.
G7 `python3 -m pytest tests/orchestration/test_autorun.py
tests/test_cli_execution_loop_closure.py tests/regression/test_named_bugs.py -q`
exit 0 → READING `140 passed, 6 skipped in 5.96s`; the migration did NOT move it.
G8 probe worktree at e0b5e8fd, seam made to raise `F085-R26-PROBE-INJECTED-
FAILURE` on entry, G7's exact command line re-run there → `18 failed, 122 passed,
6 skipped in 2.21s`; the injected `RuntimeError` DOES appear, at
`packages/orchestration/exec_guard.py:525`; the 18 nodes span BOTH driving files
(14 test_autorun, 4 loop_closure), so C2 sits on a path the suite executes.
G9 exec_guard `24 passed` exit 0; four state readers READING `158 passed` exit 0;
canary `tests/cli/test_golden_path.py` `42 passed` exit 0; `python3 -m ruff check
packages/orchestration/autorun.py` `All checks passed!` exit 0.
G10 changed set before C4 = exactly the 5 declared paths; insertions C0a 313 ·
C0b 258 · C1 35 · C2 12 · C3 5, none over 500, C4's own in the round report as it
cannot measure itself; one parent per commit; `git reflog -12` all `commit:`.

## Authored-text proofs

Digest fallback (§4.9): no reviewer-side pre-delegation original exists in this
session, so the proof is the G2 four-way byte-equality at sha256 4220f7db…2908 /
16616 B / 313 lines / 26 markers with its three region digests. All six applied
slices — RECORD1, the IMP1/SITE1/IMP2/SITE2/SITE3 pairs, PLANF/PLANT — came
PROGRAMMATICALLY out of the committed file by marker pair; 0 marker lines reached
live_review.md, autorun.py or plan.md.

## Deviations & assumptions

TRANSPORT GATE CORRECTED MID-ROUND — declared. The block ordered a 312-line save;
the delivered text measures 313. The worker halted BEFORE C0a per that
instruction, committed nothing and left the tree byte-clean at 5b02cff9. The
reviewer re-measured its own source, confirmed 313 and traced 312 to hand-summed
section counts after a late edit, then re-issued the gate as 313 lines + sha256
4220f7db…2908 + 16616 B. Both of the worker's independent transcriptions produced
exactly that sha256, so the file was re-created and the round ran from C0a. No
block bytes changed: the count lived in the instructions, not in the sentinels.
NO DEPARTURE from the ordered commit sequence — C0a, C0b, C1, C2, C3, C4, in
order, one commit each, none extra and none dropped.
Declared overage (DECISION D15): this file is 125 lines against the
100-line ceiling its six per-commit tables engage. Cause is mandated content only
— the six per-commit tables, the six-row item-status table and the G1-G10
transcripts with the transport, append-shape and pair proofs. No section dropped.

## Next

Reviewer re-runs G1-G10 over 5b02cff9..HEAD and records a verdict for R26.
