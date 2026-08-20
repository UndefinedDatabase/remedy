# Handback — F086 R20, the install smoke module and the R19 record (branch feature/f086-release-capability)

## Range

Review of bc85e5f7..HEAD (6 commits: 7f89c13f, 03136104, 992c70da, 4dc7cbdf, 724882f2, C4).

## Commits

### 7f89c13f docs(state): save the F086 R20 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r20.md | +482/-0 | C0a — the R20 block, byte-verbatim |

### 03136104 docs(state): mirror the F086 R20 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +406/-283 | C0b — mirror read back from the committed C0a |

### 992c70da docs(state): advance the plan to F086 R20
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +7/-10 | C1 — PLAN20, whole file, alone |

### 4dc7cbdf docs(review): register R-0586 and record the R19 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — pure append: FIND0586 then RECORD18 |

### 724882f2 test(install): add the opt-in install smoke module for F086 T2
| Path | +/- | Reason |
|---|---|---|
| tests/test_install_smoke.py | +220/-0 | C3 — SMOKE, a file new on this branch, alone |

### C4 docs(state): write the F086 R20 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — this file; a handoff cannot table its own commit (R-0149) |

## External actions

- `git worktree add --detach .remedy-wt/r20probe 724882f2` — created for G10/G11 only.
- `git worktree remove --force .remedy-wt/r20probe` then `git worktree prune` — removed; `git worktree list` reads one line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. Nothing created, nothing merged.
- `git push -u origin feature/f086-release-capability` — see the round report for its outcome.

## Verification

- G1 HYGIENE: `git status --porcelain` empty at every commit and at the handback; `.agent/STOP` re-read from disk before C0a and at the handback, absent both times; branch feature/f086-release-capability; `git worktree list` one line.
- G2 TRANSPORT: `.remedy-wt/f086-r20.md`, committed `.agent/authored/f086-r20.md` and committed `.agent/last_block.md` byte-EQUAL at sha256 c88049f01e95e66db81fcbb778cde3a93746525eac864d9264876ff0f30b9231, 32032 B over 482 lines.
- Constraint 7 re-measured on the committed C0a: 482 total / 212 prose / 270 slice incl. 8 marker lines — the block's own declaration, under D6's 490 and D5's 400.
- G3 PLAN: `.agent/plan.md` at 992c70da byte-equal to PLAN20 at sha256 2043155c37445fb5ce7823556623299110c56c5da674af789b9a11194ba5453c, 40 lines (< 50), contains `## Goal`, `## Next Steps`, `F086`.
- G4 APPEND: pre-C2 blob is a byte-exact PREFIX of the post-C2 blob; the 4-line remainder equals blank + FIND0586 + blank + RECORD18 at sha256 7a4502ccf0774f4d941d77b6aebe98bbd1bc1b1851b564ca6dc9d276417bf23b.
- G5 LEDGER SETS: at 4dc7cbdf both extractions read 169 / 3 / 0 / 0 / 0 / 166 and their registered SETS are equal; registered symmetric difference against bc85e5f7 is exactly `['R-0586']`; CONTROL f0b27118..7b84524c reads `[]` registered while its resolved set gains `R-0584`.
- G6 THE FINDING'S OWN RULE: over the lines 4dc7cbdf ADDS to `.agent/live_review.md`, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 (6 before the strip, all quoted); RED CONTROL over `fd166295`'s added lines reads 3 with the same extractor.
- G7 NO MARKER LEAKED: 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`, `tests/test_install_smoke.py` at C4 — see the round report for the four readings.
- G8 THE MODULE IS THE SLICE AND IS NEW: `git ls-tree bc85e5f7 -- tests/test_install_smoke.py` printed NOTHING; at 724882f2 the file and the SMOKE slice are byte-EQUAL at sha256 ea84a2f5233b277e7b9fbd0bac3c77447885d4110b8d5e2d9bf668a09ef83f61, 9475 B over 220 lines.
- G9 THE MODULE RUNS, THE SKIP IS REAL: `python3 -m pytest tests/test_install_smoke.py -q -rs` exit 0, 14 passed, 1 skipped; skip line verbatim `SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access`; the one skip is `test_the_wheel_installs_and_the_installed_cli_runs_the_golden_path`.
- G10 LINT, BOTH HALVES: clean file, both `python3 -m ruff check` and `--preview` exit 0; with one separating blank line deleted INSIDE the probe worktree the PLAIN half still exits 0 while the PREVIEW half exits 1 naming E302 — the R-0500 disagreement, measured, then reverted.
- G11 MUTATION PROBES, in the probe worktree, each target line occurring exactly 1x, each reverted before the next: (a) `return False` → exit 1, FAILED `TestInstallSmokeOptIn::test_any_other_value_enables_it`; (b) `if False:` → exit 1, FAILED `TestBuildRootLiesOutsideTheRepository::test_a_path_inside_the_repository_is_refused` and `::test_the_repository_root_itself_is_refused`. The install test STILL SKIPPED in both.
- G12 SUITES, primary checkout, serially, no two pytest processes at once: 24 passed exit 0 (marker/step-file/CI-stage guards), then 160 passed exit 0 (the state-file readers), then 42 passed exit 0 (golden-path canary).
- G13 CHANGE SET: `git diff --name-only bc85e5f7..HEAD` before C4 equals the constraint-2 list AS SETS, symmetric difference empty both ways; all six forbidden paths resolve at bc85e5f7 via `git ls-tree` and none appears in the range.
- G14 HISTORY: five single-parent commits, linear; `git reflog` over this round shows only `commit:` entries — no amend, rebase, reset, force-push. Insertions before C4: 482, 406, 7, 4, 220 — none over 500, no DECISION F104 D1 exemption invoked.
- G15 HANDBACK AND PR GATE: this file's `wc -l` reading and the Open PR Gate output are in the round report; the gate printed `[]`.

NO INSTALL RAN THIS ROUND. `REMEDY_INSTALL_SMOKE` stayed UNSET in every environment created, the probe worktree's included, so the module's one install test SKIPPED in every run reported above. A skipped test is not coverage: DECISION F086 D4 already records that F086's DONE condition stays UNPROVEN until that variable is set on a host that can honour it. No wheel was built, no venv was created, no network was reached.

## Authored-text proofs

- PLAN20, FIND0586, RECORD18 and SMOKE were EXTRACTED programmatically from the COMMITTED `.agent/authored/f086-r20.md`, never retyped and never reformatted; SMOKE was applied as bytes with no formatter run over it.
- Disk-to-disk: `.agent/plan.md` == PLAN20 (G3), `.agent/live_review.md`'s C2 remainder == blank + FIND0586 + blank + RECORD18 (G4), `tests/test_install_smoke.py` == SMOKE (G8) — all three byte-equal, digests above.
- The committed C0a is byte-equal to the `.remedy-wt/f086-r20.md` scratchpad the round was delegated from, and `.agent/last_block.md` mirrors the committed C0a read back with `git show` (G2).

## Deviations & assumptions

- No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4 were committed in that order, one commit each, nothing extra, nothing dropped, nothing reordered.
- OBSERVATION for the reviewer, not a change: the RECORD18 slice opens `Gate: R19 — the R18 entry. R19 PASSED …`, while every prior entry in `.agent/live_review.md` follows `Gate: R<this round> — the R<previous round> entry. R<previous round> …` and the entry immediately above it already opens `Gate: R19 — the R18 entry.`. Constraint 1 forbids editing a slice and constraint 3 forbids the worker authoring a verdict, so the slice was applied byte-verbatim and the discrepancy is reported rather than repaired. No gate this block orders measures that prose.
- No verdict on this round is written here. The worker reports what the gates measured; ruling is the reviewer's.

## Next

The reviewer re-runs G1-G15 over bc85e5f7..HEAD and rules on R20. Before authoring R21, re-read `.agent/STOP` from disk (Phase 1 rule 1 before rule 2); R21 promotes R-0586's rule into the §3 pre-emission checklist item 20 and records R20's verdict.
