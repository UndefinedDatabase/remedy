# Handback — F085 Sandbox hardening, R24 (T002b/1)

Branch: feature/f085-sandbox-hardening. Base f28ed65a.
Fortschritt: ~78 % (T001 gebaut · R13-R23 PASS · T002a KOMPLETT · T002b begonnen:
Seam + erster von zwölf `test`-Sites · T002b Rest, T002c-d, T003 offen) — Schätzung.

## Range

Review of f28ed65a..HEAD

## Commits

### 6c7bfd66 docs(f085): save the R24 step block
| Path | +/- | Reason |
| .agent/authored/f085-r24.md | +355/-0 | C0a byte-for-byte save of the block |

### 5e4a0ec6 docs(f085): mirror the R24 block into last_block
| Path | +/- | Reason |
| .agent/last_block.md | +315/-328 | C0b, sourced from the committed C0a blob |

### 444b29f2 docs(review): record the R23 PASS
| Path | +/- | Reason |
| .agent/live_review.md | +46/-0 | C1 RECORD1 appended after one blank line |

### 8b5e1d9c feat(f085): add the shared test-class exec seam
| Path | +/- | Reason |
| packages/orchestration/exec_guard.py | +105/-4 | C2 allowlist, policy, runner, coverage bullet |
| tests/orchestration/test_exec_guard.py | +101/-0 | C2 six added tests (a)-(f) |

### 3cb53f4a feat(f085): migrate run_tests_local onto the guarded seam
| Path | +/- | Reason |
| packages/orchestration/test_runner.py | +12/-5 | C3 spawn through the seam |
| tests/orchestration/test_test_runner.py | +34/-2 | C3 2 patches retargeted + real-run golden |
| tests/test_test_runner.py | +16/-9 | C3 7 patches retargeted, shell assertion replaced |

### d3aece1d docs(f085): advance the plan to the R24 T002b opening
| Path | +/- | Reason |
| .agent/plan.md | +9/-8 | C4 PLANF to PLANT rewrite |

### C5 — .agent/handoff.md, this file. A handoff cannot table the commit that writes it.
| Item | Status | Reason |
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## External actions

`git worktree add .remedy-wt/g10-probe HEAD --detach` for G10, then `git worktree remove
--force` + `git worktree prune`. `git push -u origin <branch>` after C5. No PR, no merge.

## Verification

G1 `.agent/STOP` absent before C0a and before C5; `git status --porcelain` empty at
round start and after every commit; `git worktree list` 1 line.
G2 committed authored + committed last_block + both working copies byte-EQUAL: sha256
46db5e38c4b586971364f75b7976daa3ff88e20ac5558aa2d82b807698380340, 22645 B, 355 lines,
6 markers. Regions 1-60 7804f388, 61-140 69d643fe, 141-end 7ac81591 — all reproduce.
G3 C1's pre-commit blob is a byte-exact PREFIX of the post file, remainder == one blank
line + RECORD1, HEAD blob == working copy, RECORD1 first line 1x, 0 markers; numstat
reading `46  0  .agent/live_review.md`, insertions 46.
G4 base 130 / 13 / 0, 117 open; HEAD 130 / 13 / 0, 117 open; both symmetric differences
empty; 0 duplicate ids; 0 resolutions of an unregistered id; max R-0515, next R-0516.
G5 PLANF 0x, PLANT 1x; `## Goal` and `## Risks` byte-identical to base; sha256
2b3551e814e677dd9666b0edfc8695c02b94be3bc9ce80216c6d54929e30d4c6, 2492 B, 43 lines;
`## Next Steps` parses to the numerals 1, 2, 3.
G6 exit 0, `All checks passed!`. G7 exit 0, `119 passed in 18.84s`, 0 failed, 0 errors
(base 112; +6 seam tests, +1 golden). G8 exit 0, `158 passed in 20.49s` (base 157, +1
golden); CANARY exit 0, `42 passed in 22.18s`.
G9 changed paths before C5 = the 9 declared, 0 outside. Insertions C0a 355, C0b 315, C1
46, C2 206, C3 62, C4 9 — none over 500; C5 is a single-file `.agent/` rewrite that cannot
measure itself. Six commits, one parent each; `git reflog -10` is all `commit:` entries.
G10 PROBE: in a disposable worktree at HEAD `run_guarded_test_command` was made to
raise on entry and the C3 golden ran alone. It STOPPED passing — exit 1, `1 failed`,
`RuntimeError: G10 PROBE: run_guarded_test_command was reached` at exec_guard.py:545.

## Authored-text proofs

RECORD1 42b82f30, PLANF b90d1cf7, PLANT ec0f3aaa — each extracted programmatically from
the committed `.agent/authored/f085-r24.md` by its marker pair and applied verbatim;
PLANF's digest equals R23's PLANT. 0 markers in live_review.md and in plan.md.

## Deviations & assumptions

No departure from the ordered sequence: C0a, C0b, C1, C2, C3, C4, C5 ran once each, in
order. Three in-file additions the block did not spell out: (1) C3 corrected two
`test_runner.py` "Safety constraints" bullets the migration falsified ("subprocess.run
receives an argv list", "Environment: inherits os.environ"); (2) the exec_guard test file
reaches `test_command_exec_policy` via a module handle, because bound as a bare name it
matches pytest's `test_*` collection pattern and errors on absent fixtures; (3) the
16 MiB default is the named constant `TEST_COMMAND_OUTPUT_CAP_BYTES`, its reason beside
the value. Observed, out of scope: that test file's docstring still claims the guard has
"NO callers in this repository" — stale since T002a, and no edit to it was ordered.

## Next

Reviewer re-runs G1-G10 over f28ed65a..HEAD and issues the R24 verdict.
