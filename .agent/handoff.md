# Handback — F009 R16 (record round)

Feature F009 · round R16 · branch `feature/f009-single-write-channel` · round base `adca4c81`.
Record round by design: it writes NO production code, which G10 measures rather than asserts.

Fortschritt: ~70 % (T001 gebaut · T002 gebaut, jetzt mit Publikations-Bound ·
             T003 begonnen: Extraktion und Vorbedingungen stehen, der Dispatch
             fehlt) — Schätzung

## Range

Review of `adca4c81`..`HEAD`.

## Commits

### 231435c1 docs(state): save the F009 R16 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r16.md | +203/-0 | C0a: the R16 block saved byte-for-byte |

### baff3ed3 docs(state): mirror the F009 R16 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +137/-363 | C0b: mirrored FROM the committed C0a blob |

### 16b05554 docs(state): set the plan to the F009 R16 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-16 | C1: PLANF009R16, byte-equal |

### 6f83dad6 docs(review): record the R15 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2: LEDGER16 appended |

### 80284ce1 docs(review): resolve R-0637 with the reviewer verification
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +1/-1 | C3: DONE0637_FROM → DONE0637_TO, the §4.4 line rewrite |

### C4 — this file (self-reference, R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report (§3 item 14) | C4: this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions

`git push` after C4; outcome in the round report. No PR created — F009 opens one at its own closure. No worktree added or removed; no `gh` command run.

## Verification

One line per gate; the transcripts are in the round report, not here (R-0582).
- G1 `.agent/STOP` ABSENT before C0a and again before C4; `git rev-parse --abbrev-ref HEAD` = `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after each of C0a–C4; round base read at step 0 = `adca4c81`.
- G2 `.agent/authored/f009-r16.md` at C0a, `.agent/last_block.md` at C0b and the received block are all sha256 `32f77b87…1137c6`, 21177 bytes, 203 lines, and byte-equal pairwise. C0b was written from the committed C0a blob.
- G3 4 slices, counted by the extractor script off the C0a blob: PLANF009R16 `1f13a5a5…` 2632 B / 46 L; LEDGER16 `238e9eb3…` 6308 B / 1 L; DONE0637_FROM `e349b294…` 350 B / 1 L; DONE0637_TO `49de83ab…` 1960 B / 1 L. Aggregate printed by the script: 11250 B / 49 L.
- G4 `cmp .agent/plan.md <PLANF009R16>` exit 0 (negative control against `.agent/last_block.md` exit 1); both sha256 `1f13a5a5…`; `wc -l` 46 against the AGENTS.md 50-line cap; `^## Goal$` 1, `^## Next Steps$` 1.
- G5 (a) the base blob is a byte-exact PREFIX and the remainder is exactly a newline plus LEDGER16, sha256 `ba37138c…`, 6309 B / 2 L; (b) N = 1 counted by the script from LEDGER16, and the last 1 blank-line unit of the file equals its 1 paragraph. File 468268 → 474577 bytes, 1090 → 1092 lines. Negative control on the FIRST appended paragraph, byte 0 `G` → `Z` at equal length: reader (a) REJECTS ("remainder != newline + slice"), reader (b) REJECTS ("paragraph 1 of 1 differs"); both ACCEPT the true file.
- G6 at C3, DONE0637_FROM reads 0 whole-line and 0 indent-agnostic (AGREE); DONE0637_TO reads 1 and 1 (AGREE). The C2 blob with the single pair applied is BYTE-EQUAL to what C3 landed — both `7cc1729b…` — so no other byte moved. `git show --numstat 80284ce1 -- .agent/live_review.md` reads `1 1`: yes, 1 insertion and 1 deletion.
- G7 every pattern LINE-START anchored (`re.match`), round base → C3: `^- R-\d+ — ` 203 → 203 with every captured id DISTINCT at each (203 / 203); `^Done: R-\d+ — ` 2 → 3; `^Landed: ` 1 → 0; `^Gate: R\d+ — ` 15 → 16 over 15 → 16 DISTINCT keys; `^Gate: R16 — ` 0 → 1; `^- R-0638 — ` 0 → 0. Max id R-0637 at both. Open by DECISION F009 D10 (line-anchored entries minus line-anchored `Done:` lines): 201 → 200. Measured, not predicted.
- G8 at the round base, line-anchored: `^- R-0585 — ` 1, `^- R-0629 — ` 1, `^- R-0418 — ` 1 — all three already open, so no id was minted.
- G9 serial, primary checkout, one pytest process at a time: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed; `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` exit 0, 507 passed.
- G10 range `adca4c81..80284ce1` lists exactly `.agent/authored/f009-r16.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`; set difference EMPTY in both directions; 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`. Each commit has ONE parent. `git show --numstat` and `git diff --numstat` AGREE on every cell, and I compared each cell against the `+/-` column of `## Commits` above: 203/0, 137/363, 19/16, 2/0, 1/1 — all five rows match. Pre-handback insertions 203, 137, 19, 2, 1, every one under the 500 cap of DECISION F104 D1. `^<<<SLICE ` and `^<<<END ` read 0 in both files a slice lands in, and that set is `.agent/plan.md` and `.agent/live_review.md` — 2 members, named rather than only counted. `git ls-files .remedy-wt` 0. `git worktree list` 1 line throughout; none created. This round's 5 reflog rows classify by the operation before the first `:` as 5 × `commit`: `amend` 0, `rebase` 0, `cherry` 0 — no total asserted over the whole reflog (R-0601).
- G11 this file carries every mandated section of docs/agents/handback_template.md, an item-status table with exactly one row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, one line per gate, and the block's `Fortschritt:` line VERBATIM. Its `wc -l` is in the round report, against the 100 lines a >5-commit bundle allows.

## Authored-text proofs

All four slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` / `<<<END ` marker lines with a script and applied programmatically; none was retyped, rewrapped or reindented. Disk-to-disk: `.agent/plan.md` `cmp` exit 0 against PLANF009R16 with a red control at exit 1; LEDGER16 proved by the G5 prefix-plus-remainder equality; the DONE0637 pair proved by the G6 reconstruction being byte-equal to the landed blob.

## Deviations & assumptions

None. The block's ordered sequence C0a, C0b, C1, C2, C3, C4 ran in exactly that order — no extra commit, none dropped, none reordered. Every slice was applied byte for byte and none was edited. No finding id was minted this round; the next free id is R-0638.
Not a deviation, recorded because a reader will meet it: LEDGER16's prose quotes the tokens `<<<SLICE ` and `<<<END ` inline inside backticks, 2 occurrences. G10's reading is line-anchored, and both slice targets read 0 marker LINES, so no marker reached a target file.

## Next

1. FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP`.
2. SECOND: the AGENTS.md Open PR Gate.
Then round 2 of DECISION F009 D17, which is step 1 of `.agent/plan.md` Next Steps: dispatch `job.stop` to `safe_points.request_stop` and migrate the seam pins.
