# Handback — F009 The single write channel, R2 (R1 VERDICT RECORDED, THE GROUND INVENTORIED — no production code touched)
## Range
Review of `87ad9e5c`..C4, the handback commit itself (6 commits, branch feature/f009-single-write-channel). THE ROUND BASE IS `87ad9e5ca9e31f16742eccd76afbd82ee8143c34`, read at Step 0 and the value every "at the round base" gate below is measured against; it is the value the block predicted. C4's own SHA cannot exist inside C4, so it is named by role and the round report carries the value (R-0371).
## Commits
### d7fc0801 chore(agent): save the F009 R2 step block as authored text
| Path | +/- | Reason |
| `.agent/authored/f009-r2.md` | +242/-0 | C0a, the R2 block saved byte for byte |

### c418b13c chore(agent): mirror the F009 R2 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +186/-353 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 37781d57 docs(state): set the plan to the F009 R2 inventory round
| Path | +/- | Reason |
| `.agent/plan.md` | +21/-18 | C1, PLANF009R2 applied whole — the first substantive commit |

### 81ea873e docs(review): record the R1 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2, LEDGER2 appended as the last paragraph after one blank line |

### c52f10ba docs(state): inventory the F009 write-channel ground from the source
| Path | +/- | Reason |
| `.agent/f009_inventory.md` | +425/-0 | C3, the six-question inventory — MY content, measured in the source |

### C4 docs(state): write the F009 R2 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C4 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git push` EXIT 0 after C3, printing `87ad9e5c..c52f10ba  feature/f009-single-write-channel -> feature/f009-single-write-channel`. NO pull request was created and NO Open PR Gate was run (constraint 5 and Step 0). No worktree was added or removed; `git worktree list` names the primary checkout alone. No `gh` command was run this round.

## Verification
- G1 `.agent/STOP` ABSENT — `ls -la .agent/STOP` printed `No such file or directory`, read at Step 0 and again immediately before C0a. `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel` at every reading. `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2 and C3; the post-C4 reading is in the round report. ROUND BASE `87ad9e5ca9e31f16742eccd76afbd82ee8143c34`.
- G2 Transport EQUAL three ways — `.remedy-wt/f009-r2.md` as received, `.agent/authored/f009-r2.md` at C0a and `.agent/last_block.md` at C0b — all sha256 ef766a8c474548c03e5e850e69c28f21a5f43058c51f8582f8061ef7eb638891 over 20682 bytes and 242 lines, and that value EQUALS the digest carried in the task prompt. C0b was written from `git show d7fc0801:.agent/authored/f009-r2.md`, never from the scratch file.
- G3 TWO slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob by their marker lines; newline-INCLUDED sha256 prefix/bytes/lines: PLANF009R2 455a24f9/2509/43, LEDGER2 3c218ada/5574/1. Aggregates over those two: ANY TRAILING WHITESPACE False, ANY LEADING BLANK LINE False, ALL NEWLINE TERMINATED True.
- G4 `.agent/plan.md` at C1 sha256 455a24f997bd4f4c4c6123e546341f9c9c358fc4a720367a89fd9d59bd884281, 2509 bytes, 43 lines (<50), BYTE-EQUAL to PLANF009R2; `Steps` occurs; `^## Goal$` 1 line and `^## Next Steps$` 1 line; the FIRST `\bF\d{3}\b` match is `F009`.
- G5 The append at C2, proved TWICE over independent extractors, the base bytes read with `git show 87ad9e5c:.agent/live_review.md` into `.remedy-wt/` scratch and never written over the tracked file. (a) The base blob IS a byte-exact PREFIX of the C2 blob and the remainder EQUALS a newline plus LEDGER2 — remainder sha256 190306b7396f2ca2227f2f9676fb7fde87e7bad142767c01aed6a53b0a0738f0, 5575 bytes, 2 lines. (b) An INDEPENDENT blank-line split (`\n[ \t]*\n`) of the WHOLE C2 file with its terminating newline normalised first yields N = **203** units whose LAST unit IS LEDGER2's paragraph. NEGATIVE CONTROL, one printable ASCII byte of the remainder flipped (offset 1, `G`→`H`): reader (a) ACCEPTS unflipped True / REJECTS flipped True; reader (b) ACCEPTS unflipped True / REJECTS flipped True — all four outcomes as required.
- G6 Line-anchored at the round base and at C2: `^- R-\d+ — ` 196 and 196 with 196 DISTINCT ids at both, so THIS ROUND MINTED NO ID; `^Done: R-\d+ — ` 1 and 1; `^Landed: ` 0 and 0; `^- R-0630 — ` 1 and 1; `^> Next free id` 0 and 0; `^Gate: R\d+ — ` 1 then **2**, over 2 DISTINCT keys (`1`, `2`). MAX ID at both: R-0630. HEADER SHAPE (§3 item 26): of the 2 `Gate: ` lines at C2, **1** matches `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first, and the **1** non-match reads exactly `Gate: R1 — the F008 R36 entry.` — the expected reading, because that entry names the F008 R36 round rather than an R0.
- G7 The inventory at C3: `## Q` headings **6**, covering Q1…Q6 with no repeat; `## Open questions for R3` PRESENT; 425 lines; 0 marker lines. CITATION AUDIT by my own script over the COMMITTED C3 blob, extracting every `path:line` and `path:line-line` token and checking each path exists at C3 AND the line number lies within that file's line count: **191 citations audited, 0 FAILING**, over 43 distinct files, 0 missing paths. Per question: Q1 19, Q2 28, Q3 50, Q4 25, Q5 33, Q6 20, Open questions 16 — no question is answered without citations.
- G8 In the PRIMARY checkout, SERIALLY, one process at a time, at C3, each exit code read from the runner rather than from a pipeline: `tests/ui_server/ + tests/orchestration/test_test_runner.py + tests/regression/test_resource_safety.py + tests/orchestration/test_integrity_gate.py -q -rf` EXIT 0, 423 passed 0 skipped, SUM **423**; canary `tests/cli/test_golden_path.py -q -rf` EXIT 0, 42 passed 0 skipped, SUM **42**. Both reproduce the reviewer's readings at `87ad9e5c`. The docs gate was NOT ordered and was NOT run: no path under `docs/` or `docs/roadmap/` is in this round's change set.
- G9 `git diff --name-only 87ad9e5c..c52f10ba` lists 5 paths which are EXACTLY the change set minus `.agent/handoff.md`, the set difference EMPTY in both directions. `git rev-list --reverse` gives FIVE commits, each read to have exactly ONE parent, with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-` column above: insertions 242, 186, 21, 2 and 425 — every one under the 500 cap, 425 the maximum, so the AGENTS.md DECISION F104 D1 single-state-file exemption is NAMED but not needed. Lines beginning `<<<SLICE ` or `<<<END `: 0 in each of `.agent/plan.md`, `.agent/live_review.md` and `.agent/f009_inventory.md` at C3. This round's own reflog entries classified by the operation before the first `:` in the reflog subject: 5 entries, all `commit`; `amend` 0, `rebase` 0, `cherry` 0. That reading covers C0a…C3; C4 adds one further `commit` entry whose value cannot exist while this sentence is written (R-0371). No total over the whole reflog is asserted (R-0601).
- G10 This file carries every mandated section of docs/agents/handback_template.md, the item-status table below holding exactly one row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, and one line per gate G1–G10 — the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f009-r2.md` at C0a == the received block byte for byte, and `.agent/last_block.md` at C0b == the same bytes, read out of the COMMITTED C0a blob (G2). BOTH slices were extracted from that committed blob by their marker lines with a script and applied programmatically — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. Whole-file byte equality: PLANF009R2 (G4). Prefix-plus-remainder equality with an independent second extractor and a negative control: LEDGER2 (G5). G9 confirms 0 marker lines in every committed target. `.agent/f009_inventory.md` is MY OWN text, not an authored slice, as the block's C3 section requires.

## State — Fortschritt
5 % (T001 offen · T002 offen · T003 offen — R1 hat beansprucht, R2 hat den Boden vermessen; gebaut wurde noch nichts) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | the first substantive commit |
| C2 | done | LEDGER2 appended; no `Done:` paragraph of mine was written |
| C3 | done | the push follows it with no commit between |
| C4 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit and the push ran between C3 and C4 with no commit between them.
- NO OBJECTION this round: both slices read as correct and were applied byte for byte regardless.
- DECLARED OVERAGE, DECISION D15 stated cause: this file exceeds the 60-line default. The cause is mandated content — six per-commit changed-files tables, ten one-line gate readings of which G5, G7 and G9 each carry a multi-value measurement, and the item-status table. No section was dropped to meet the cap and no transcript was pasted. Its measured `wc -l` is in the round report; it is under the 100 that AGENTS.md allows a >5-commit bundle.
- PARTIAL READ, declared against the AGENTS.md File Editing Safety Rule: `.agent/live_review.md` (382430 bytes / 1044 lines at the round base) was not read end to end. Its edit is a pure two-line append made programmatically over whole-file bytes, with G5's two independent extractors plus their negative control and G6's line-anchored set readings standing in for the human read. `.agent/plan.md` and `.agent/f009_inventory.md` WERE read in full, and every one of the five diffs was reviewed with `git diff --stat` then `git diff` before its commit.
- No production code was touched and nothing was created under `tests/`: G9's path list is the measurement. `ruff check .` and `npm run lint` were not run — both are red at base, neither is a gate (R-0364, R-0622), and this round authored no code.
- The inventory's Q6 answer CONTRADICTS the feature file, deliberately and with the contradiction carried rather than resolved: `docs/roadmap/features/T5_F009.md:90` suggests `tests/ui_contract/test_command_channel.py`, that directory does not exist (`git ls-tree -d HEAD tests/ui_contract` prints nothing), and the inventory argues for `tests/ui_server/` on the convention at `tests/README.md:12-13`. No file and no directory was created; the choice is routed to R3 as an open question.
- The session command guard rejects `$(...)`, `${...}`, heredocs, shell loops and `;`-chained commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run with `python3`; `git status --porcelain` printed 0 lines after each commit, so nothing from that directory was ever staged. No gate command was piped, so no exit code reported here is a pipeline's last stage.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which is EMPTY — this branch carries no pull request and F009 opens one at its own closure. Then R3: record the R2 verdict and RULE the channel's shape as a DECISION, answering the ten items `.agent/f009_inventory.md` leaves open — chiefly the test directory, the missing plan-approval backend, the decision queue's lack of a write target, the audit record's path and fields (two later features already read it), the token fingerprint's derivation, the rate limit's key and window, the nonce store that can return an original body, and whether the bearer header displaces the query-parameter token. 196 findings are OPEN, all DISTINCT, the highest registered id is R-0630 and the next free id is derived with `max` over the line-anchored `^- R-\d+ — ` entries. `.agent/candidates.md` is EMPTY. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613 and R-0630 stay routed to a paydown branch.
