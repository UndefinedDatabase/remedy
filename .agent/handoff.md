# Handback — F085 Sandbox hardening, R25 (T002b paydown)

Branch: feature/f085-sandbox-hardening. Base 3d1821bf.
Fortschritt: ~78 % (T001 gebaut · R13-R24 PASS · T002a KOMPLETT · T002b: Seam
gebaut, 1 von 12 `test`-Sites migriert · T002b Rest, T002c-d, T003 offen) —
Schätzung.

## Range

Review of 3d1821bf..HEAD

## Commits

### b0376acf docs(f085): save the R25 step block
| Path | +/- | Reason |
| .agent/authored/f085-r25.md | +296/-0 | C0a byte-for-byte save of the block |

### bb91d7b7 docs(f085): mirror the R25 block into last_block
| Path | +/- | Reason |
| .agent/last_block.md | +217/-276 | C0b, sourced from the committed C0a blob |

### f10e5a30 docs(review): record the R24 PASS and register R-0516
| Path | +/- | Reason |
| .agent/live_review.md | +67/-0 | C1 RECORD1 appended after one blank line |

### 1548455c test(f085): retire the stale no-callers claim in the guard fixtures
| Path | +/- | Reason |
| tests/orchestration/test_exec_guard.py | +6/-2 | C2 DOCF to DOCT docstring rewrite |

### ae3ec2d3 docs(review): resolve R-0516
| Path | +/- | Reason |
| .agent/live_review.md | +12/-0 | C3 DONE1 appended after one blank line |

### b543da3a docs(f085): advance the plan to R25
| Path | +/- | Reason |
| .agent/plan.md | +7/-8 | C4 PLANF to PLANT rewrite |

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

`git push -u origin feature/f085-sandbox-hardening` after C5. No worktree added: no
destructive verification was needed. No PR created, nothing merged.

## Verification

G1 `.agent/STOP` absent on disk before C0a and again before C5; `git status
--porcelain` empty at round start and after every commit; `git worktree list` 1 line.
G2 committed authored + committed last_block + both working copies byte-EQUAL: sha256
4abce714f82e9a6b2baad095c02c6f0aecebfd009ce4a8883531c908b8971262, 18089 B, 296 lines,
12 markers. Regions 1-60 07199a30, 61-140 cad21f6b, 141-end 3de16b95 all reproduce.
G3 for C1 and C3: each pre-commit blob is a byte-exact PREFIX of its post file, each
remainder == one blank line + the slice, each HEAD blob == the working copy, each
slice's first line 1x, 0 markers. Numstat `67  0` and `12  0`; insertions 67 and 12.
G4 base 130 / 13 / 0, 117 open; after C1 131 / 13 / 0, 118 open; HEAD 131 / 14 / 0,
117 open. Registered symdiff base..C1 = {R-0516}, resolved symdiff C1..HEAD = {R-0516};
0 duplicate ids; 0 resolutions of an unregistered id; max R-0516, next free R-0517.
G5 TAKEN AFTER C2 AND BEFORE C3: DOCF 1x at base, 0x at HEAD; DOCT 1x at HEAD; sha256
ee200a92041190027a59efc08a835dd2827dc951de57eb7e35cf158957d2d04c, 21388 B; the file's
first line is byte-unchanged from base (`"""Runaway fixtures for ... T001.`).
G6 PLANF 0x, PLANT 1x; `## Goal` and `## Risks` byte-identical to their base bytes;
sha256 ff75c9228c57e25d0919c5b9204b642956e5b5e8a9b8bac1c582ed96b71fd423, 2404 B,
42 lines; `## Next Steps` parses to the numerals 1, 2, 3.
G7 run after C2: exit 0, `24 passed in 12.97s` — the edit did NOT move the base 24.
G8 exit 0, `158 passed in 19.91s` (base 158, unmoved); CANARY exit 0, `42 passed in
20.32s` (base 42). Also run: ruff on the changed `.py`, exit 0, `All checks passed!`.
G9 changed paths before C5 = the 5 declared, 0 outside. Insertions C0a 296, C0b 217,
C1 67, C2 6, C3 12, C4 7 — none over 500; C5 cannot measure itself. Six commits, one
parent each; `git reflog -10` holds only `commit:` entries — no amend/rebase/reset.

## Authored-text proofs

RECORD1 546e435e, DOCF 16f77135, DOCT 0df6e2d8, DONE1 6d147885, PLANF ec0f3aaa, PLANT
26e70b26 — each extracted programmatically from the committed R25 authored file by its
marker pair and applied byte-verbatim; PLANF's digest equals R24's PLANT. On disk DOCT
does not contain DOCF and PLANT does not contain PLANF, both REWRITEs; 0 markers left.

## Deviations & assumptions

None. C0a, C0b, C1, C2, C3, C4, C5 ran once each, in the block's order, with no extra
commit, no dropped commit and no reordering. No gate came out red and the block
contradicted neither itself nor the code.

## Next

Reviewer re-runs G1-G9 over 3d1821bf..HEAD and issues the R25 verdict. The next
session's first action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE
rule 2, the Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). R25's verdict is NOT a §4.13 terminator: that
clause covers the last round of a BRANCH and this branch continues, so the next
session's first reviewed round records R25's gate entry in `.agent/live_review.md`.
First work item: the remaining `test`-class sites, the three in `autorun.py` first.
