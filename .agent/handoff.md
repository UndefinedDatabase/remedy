# Handback — F009 R15, the dispatch prerequisites round

Round base `de1e5c00fa0209824d50bd0837b39bf123ca20e9`, branch `feature/f009-single-write-channel`. State: 65 % (T001 gebaut · T002 gebaut bis auf die Publikation · T003 begonnen: die Extraktion) — Schätzung

## Range

Review of `de1e5c00..HEAD` — nine commits: C0a, C0b, C1, C2, C3, C4, C5, C6 and C7, in that order. Nothing came between them, none was dropped and none was added. `packages/orchestration/ui_server.py` and `tests/ui_server/test_command_channel.py` are UNTOUCHED by design: the 501 seam still stands and the dispatch is round 2 of DECISION F009 D17.

## Commits

### 89919dbd docs(state): save the F009 R15 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r15.md | +429/-0 | the round's block, byte-exact |

### 4ea0aef3 docs(state): mirror the F009 R15 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +395/-174 | written from the committed C0a blob |

### c92a41b7 docs(state): set the plan to the F009 R15 prerequisites round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18/-18 | PLANF009R15, applied byte-equal |

### db2c6c23 docs(review): record the R14 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER15 appended; R14 PASSED |

### 5188259d docs(state): rule DECISION F009 D17 splitting the first D16 round
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +16/-0 | DECISION17 appended; D16's first round becomes two |

### f52d6534 feat(orchestration): refuse an oversize command nonce record at publication
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/command_nonce.py | +16/-5 | NONCE_CONST, NONCE_DOC, NONCE_PUB — pays R-0637 |
| tests/orchestration/test_command_nonce.py | +42/-0 | NONCE_TESTIMPORT rewrite + NONCE_TESTAPPEND's three tests |

### 8604e557 feat(orchestration): add accepted and replayed to the command audit vocabulary
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/command_audit.py | +9/-2 | AUDIT_OUTCOMES — the two tokens no caller writes yet |
| tests/orchestration/test_command_audit.py | +5/-2 | AUDIT_TEST — the pin that fixes them |

### 53a17d61 docs(review): record R-0637 as landed in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | the worker-authored `Landed:` line, one line |

### C7, this commit, docs(state): write the F009 R15 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | a handback cannot table the commit that writes it |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |

## External actions

`gh` was not run; this branch carries no pull request and F009 opens one at its own closure. ONE disposable worktree was created for G11 and removed: `git worktree add --detach .remedy-wt/r15ctl f52d6534` (created, then `git checkout --detach 8604e557` inside it for control b), then `git worktree remove .remedy-wt/r15ctl` and `git worktree prune`; `git worktree list` now prints 1 line, the primary checkout alone. `git push` follows C7.

## Verification

- G1 `.agent/STOP` ABSENT at step 0 and again before C7; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel` at both readings; `git status --porcelain` printed 0 lines after each of C0a through C7; the round base read at step 0 is `de1e5c00fa0209824d50bd0837b39bf123ca20e9`, which was also HEAD at step 0.
- G2 EQUAL — the scratch file as received, `.agent/authored/f009-r15.md` at C0a and `.agent/last_block.md` at C0b are all sha256 `9267d80767b2069481d1cfdf66363804f9ae832dec5086653f9734da03b22f15` over 30644 bytes and 429 lines, equal to the digest the task prompt named; C0b was written from the committed C0a blob, never from the scratch file again.
- G3 16 slices from my own ordered marker extraction out of the committed C0a blob (16 `<<<SLICE ` and 16 `<<<END ` lines, matched pairwise): PLANF009R15 `f189245f…` 2545 B 43 L · LEDGER15 `49ccb7d2…` 4342 B 1 L · DECISION17 `55e432ad…` 4120 B 15 L · NONCE_CONST_FROM `e45bdc0a…` 206 B 3 L · NONCE_CONST_TO `0a97d456…` 468 B 6 L · NONCE_DOC_FROM `1886b1da…` 210 B 3 L · NONCE_DOC_TO `28ef0b3b…` 257 B 3 L · NONCE_PUB_FROM `3b689210…` 421 B 9 L · NONCE_PUB_TO `fbd5d0c2…` 936 B 17 L · NONCE_TESTIMPORT_FROM `0fc15c10…` 70 B 2 L · NONCE_TESTIMPORT_TO `161a507c…` 98 B 3 L · NONCE_TESTAPPEND `25daf881…` 2123 B 41 L · AUDIT_OUTCOMES_FROM `86367610…` 437 B 12 L · AUDIT_OUTCOMES_TO `e39f45b0…` 872 B 19 L · AUDIT_TEST_FROM `26a41bdf…` 460 B 13 L · AUDIT_TEST_TO `6d25328c…` 584 B 16 L; the aggregates my script printed are 16 slices, 18149 bytes and 206 lines.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R15 — `cmp` exit 0, both sha256 `f189245f1b0367ddced1db89d2380608922b6036b91f487b0d0972585e2cb2f1` — at 43 lines against the 50-line cap of AGENTS.md; line-anchored `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 BOTH APPENDS HOLD UNDER BOTH READERS, each with its own negative control on its FIRST appended paragraph. C2 over `.agent/live_review.md`, base the round base: (a) the base blob is a byte-exact PREFIX and the remainder is sha256 `09ef4431…` over 4343 bytes and 2 lines, EQUAL to a newline plus LEDGER15; the file goes 463574 → 467917 bytes and 1086 → 1088 lines. (b) N COUNTED BY MY SCRIPT is 1 and the last 1 blank-line unit equals LEDGER15's 1 paragraph in order. CONTROL, one printable byte flipped at offset 463575 (`G` → `g`): (a) ACCEPT true / REJECT flipped, (b) ACCEPT true / REJECT flipped — all four. C3 over `.agent/decisions.md`, base the C2 commit's blob of that file: (a) prefix holds, remainder sha256 `d3d79605…` over 4121 bytes and 16 lines, EQUAL to a newline plus DECISION17; 445935 → 450056 bytes and 6811 → 6827 lines. (b) N is 8 and the last 8 units equal DECISION17's 8 paragraphs in order. CONTROL at offset 445939 (`D` → `d`): (a) ACCEPT true / REJECT flipped, (b) ACCEPT true / REJECT flipped — all four. Nothing already in either file was edited; both stay append-only.
- G6 line-anchored — `^` is line-start under a MULTILINE regex — over `.agent/live_review.md` at the round base and at C6: `^- R-\d+ — ` 203 and 203 with every captured id DISTINCT at each (203/203 both times); `^Done: R-\d+ — ` 2 and 2; `^Landed: R-\d+ — ` 0 and 1; `^Gate: R\d+ — ` 14 and 15 over that many DISTINCT keys (14/14 and 15/15); `^Gate: R15 — ` 0 and 1. Max id at both readings is R-0637. Open at C6 is 201 by DECISION F009 D10's rule — line-anchored `^- R-\d+ — ` 203 minus line-anchored `^Done: R-\d+ — ` 2.
- G7 line-anchored over `.agent/decisions.md` at the round base and at C3: `^## DECISION F009 D\d+ — ` 16 and 17, every captured number DISTINCT at each (16/16 and 17/17); `^## DECISION F009 D17 — ` 0 and 1; `^## DECISION ` totals 101 and 102.
- G8 ALL SIX PAIRS ARE REWRITES AND ALL SIX LANDED. At C4 `f52d6534` in `packages/orchestration/command_nonce.py`: NONCE_CONST, NONCE_DOC and NONCE_PUB each read FROM 0 and TO 1; at C4 in `tests/orchestration/test_command_nonce.py`: NONCE_TESTIMPORT FROM 0, TO 1; at C5 `8604e557` in `packages/orchestration/command_audit.py`: AUDIT_OUTCOMES FROM 0, TO 1; at C5 in `tests/orchestration/test_command_audit.py`: AUDIT_TEST FROM 0, TO 1. The whole-line and the indent-agnostic count were BOTH taken at every one of those 24 readings and AGREE at every one. RECONSTRUCTION: the round-base blob of `command_nonce.py` with the three pairs applied in the order NONCE_CONST, NONCE_DOC, NONCE_PUB is sha256 `b18b62c6bb022ed1c60015e7e6d3346ea6b6243aec6a2687cb61c42cf3e78491`, BYTE-EQUAL to what C4 landed; the round-base blob of `command_audit.py` with AUDIT_OUTCOMES applied is sha256 `7815263ee50414b9402b42dd45449f2236e01e968cdde54e69bec0c7930478c6`, BYTE-EQUAL to what C5 landed. No byte of either file changed beyond the authored pairs.
- G9 the round-base blob of `tests/orchestration/test_command_nonce.py` is NOT a prefix of what C4 landed — my script read that false, as the block said it would. The three readings instead: with NONCE_TESTIMPORT applied ALONE the round-base blob becomes sha256 `4c651558…` over 9282 bytes, and (i) that is a byte-exact PREFIX of the landed file, (ii) NONCE_TESTAPPEND (`25daf881…`, 2123 B, 41 L) is an exact SUFFIX of it, and (iii) the landed file (`5af111ce…`, 11405 B, 269 L) EQUALS that prefix followed by that slice with NOTHING between them. §4.9 ordered equality also holds: the last 41 lines the C4 diff ADDS to that path are EXACTLY the slice's 41 lines IN ORDER.
- G10 ALL FOUR EXIT 0, run SERIALLY in the PRIMARY checkout at C6, never two pytest processes at once. `python3 -m ruff check` over the four changed `command_nonce`/`command_audit` paths printed `All checks passed!` at exit 0. `python3 -m pytest tests/orchestration/test_command_nonce.py tests/orchestration/test_command_audit.py -q -rf` printed `45 passed in 0.31s` at exit 0. `python3 -m pytest tests/cli/test_golden_path.py -q -rf` printed `42 passed in 20.63s` at exit 0. The four-path state-reader group owed by R-0607 printed `507 passed in 38.85s` at exit 0. No count here was predicted; each is what the run printed.
- G11 BOTH RED CONTROLS WENT RED, in the disposable worktree `.remedy-wt/r15ctl` only and never in the primary checkout. (a) At C4, the three-line sequence `    raw = _record_bytes(record)` / `    if len(raw) > MAX_NONCE_RECORD_BYTES:` / `        return None` reads 1 in `command_nonce.py` under BOTH the whole-line and the indent-agnostic count, and deleting the last two of those lines makes `python3 -m pytest tests/orchestration/test_command_nonce.py -q -rf` EXIT 1, RED, failing `test_a_record_over_the_bound_is_refused_at_publication` and `test_the_bound_refuses_before_the_store_is_created`; restored, the same command EXITS 0. (b) At C5, the two-line sequence `    "accepted",` / `    "replayed",` reads 1 in `command_audit.py` under both counts, and deleting it makes `python3 -m pytest tests/orchestration/test_command_audit.py -q -rf` EXIT 1, RED, failing `test_the_outcome_vocabulary_is_the_closed_set_d14_ruled`; restored, EXIT 0. The worktree was then removed and pruned and `git worktree list` prints 1 line.
- G12 the range from the round base to C6 lists EXACTLY the nine declared paths other than `.agent/handoff.md`, the set difference EMPTY in both directions, with 0 paths beginning `apps/`, `docs/`, `tests/ui_server/` or `tests/cli/` and 0 equal to `packages/orchestration/ui_server.py`. Each of the eight commits has ONE parent; `git show --numstat` and `git diff --numstat` AGREE on every cell, and I compared them cell by cell against the `+/-` column of the `## Commits` tables above — every cell is equal. Pre-handback insertions are 429, 395, 18, 2, 16, 58, 14 and 2, each under the 500-insertion cap of AGENTS.md DECISION F104 D1. `^<<<SLICE ` and `^<<<END ` read 0 lines in every committed slice-target file — see the deviation below on the count. `git ls-files .remedy-wt` reads 0. THIS ROUND'S reflog rows classify by the operation before the first `:` as `commit` 8, with `amend`, `rebase` and `cherry` reading 0 each; no total is asserted over the whole reflog (R-0601).
- G13 this handback carries every mandated section of docs/agents/handback_template.md, an item-status table with exactly one row for each of C0a, C0b, C1, C2, C3, C4, C5, C6 and C7, the round base SHA, one line per gate with the transcripts left to the round report, and the Fortschritt line — see the deviation below on its source. `wc -l` measures it at 100 lines against the 100 a bundle of more than five commits allows.

## Authored-text proofs

All 16 slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` and `<<<END ` marker lines with a script and applied programmatically; nothing was retyped, rewrapped, reflowed, reindented or whitespace-adjusted. PLANF009R15 is byte-equal to `.agent/plan.md` at C1 (`cmp` exit 0, equal sha256, G4). LEDGER15 and DECISION17 are each proved as an append under two independent extractors with a script-counted N and a negative control on the first appended paragraph (G5). The six FROM/TO pairs are proved by the 24 agreeing count readings plus two byte-equal reconstructions off the round-base blobs (G8), and NONCE_TESTAPPEND by the three-reading prefix/suffix/equality proof plus §4.9 ordered equality (G9). No marker line reached any target file: 0 in all seven.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7 was followed exactly — no commit added, dropped or reordered — and all 16 slices were applied byte for byte with NO OBJECTION to any of them (constraint 1). Two numerals in the block's own gate text read differently when measured, and neither changes an outcome. G12 says `^<<<SLICE ` and `^<<<END ` read 0 in "ALL SIX committed targets"; the slice-target set is SEVEN files — `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`, `command_nonce.py`, `test_command_nonce.py`, `command_audit.py`, `test_command_audit.py` — and all SEVEN read 0, so the property holds over a set one larger than the numeral. G11a says the bare line `    return None` occurs 14 times in `command_nonce.py` at C4; 14 is the INDENT-AGNOSTIC count, while the exact 8-space form reads 12 — the block's point, that the bare line is not unique and the three-line sequence is, holds under both. ASSUMPTION: the block relayed NO Fortschritt line (R-0418 class), so the state line above carries R14's forward VERBATIM rather than inventing a number; it is unchanged and therefore does not credit this round's work. `.agent/context.md` was not touched: this round's scope is the declared change set.

## Next

The reviewer re-runs G1–G13 against the committed diff and records the R15 verdict. No `.agent/STOP` is present. Open findings at C6 are 201 by DECISION F009 D10's rule — line-anchored `^- R-\d+ — ` 203 minus line-anchored `^Done: R-\d+ — ` 2 — and the next free id, derived with `max` over the line-anchored entries, is R-0638. R-0637 is recorded as `Landed:` at C6 and awaits the reviewer's `Done:`; R-0636 is untouched and is owed by round 2, as DECISION F009 D17 rules. The next round is that round 2: `packages/orchestration/ui_server.py` dispatches `job.stop` to `safe_points.request_stop`, writes `accepted`, publishes the nonce record, moves the replay audit to `replayed`, and migrates the seam pins in `tests/ui_server/test_command_channel.py`; `decision.resolve` keeps answering 501. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and R-0635 stay routed to a paydown branch.
