# Handback — F009 The single write channel, R3 (R2 VERDICT RECORDED, D1–D9 RULED, ONE FEATURE-FILE LINE AMENDED — no production code, no test file, no config key)
## Range
Review of `ee2fdda7`..C6, the handback commit itself (8 commits, branch feature/f009-single-write-channel). THE ROUND BASE IS `ee2fdda71c40ef99adfb282764f68cf8ebd6eaf3`, read at Step 0 and the value every "at the round base" gate below is measured against; it is the value the block predicted. C6's own SHA cannot exist inside C6, so it is named by role and the round report carries the value (R-0371).
## Commits
### 87e1e8bf chore(agent): save the F009 R3 step block
| Path | +/- | Reason |
| `.agent/authored/f009-r3.md` | +390/-0 | C0a, the R3 block saved byte for byte |

### 7aabbd33 chore(agent): mirror the F009 R3 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +319/-171 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 90a8f586 docs(state): set the plan to the F009 R3 decision round
| Path | +/- | Reason |
| `.agent/plan.md` | +24/-23 | C1, PLANF009R3 applied whole — the first substantive commit |

### d836b061 docs(review): record the R2 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2, LEDGER3 appended as the last paragraph after one blank line |

### f19abdfb docs(decisions): rule the F009 write channel shape as D1 through D9
| Path | +/- | Reason |
| `.agent/decisions.md` | +102/-0 | C3, the DECISIONS slice appended as the new last content |

### 215e4ba0 docs(roadmap): point the F009 contract test at tests ui_server
| Path | +/- | Reason |
| `docs/roadmap/features/T5_F009.md` | +3/-1 | C4, the FEATFROM→FEATTO pair, one substitution, nothing else |

### 20f5dcf0 docs(state): carry the F009 R3 rulings into the context file
| Path | +/- | Reason |
| `.agent/context.md` | +26/-24 | C5, CONTEXTF009R3 applied whole; the push follows it |

### C6 docs(state): write the F009 R3 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C6 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git push` EXIT 0 after C5, printing `ee2fdda7..20f5dcf0  feature/f009-single-write-channel -> feature/f009-single-write-channel`. NO pull request was created and NO Open PR Gate was run (constraint 5 and Step 0). No worktree was added or removed; `git worktree list` names the primary checkout alone. No `gh` command was run this round.

## Verification
- G1 `.agent/STOP` ABSENT — `ls -la .agent/STOP` printed `No such file or directory` and exited 2, at Step 0 and again before C6. `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel` at every reading. `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5; the post-C6 reading is in the round report. ROUND BASE `ee2fdda71c40ef99adfb282764f68cf8ebd6eaf3`.
- G2 Transport EQUAL three ways — `.remedy-wt/f009-r3.md` as received, `.agent/authored/f009-r3.md` at C0a and `.agent/last_block.md` at C0b — all sha256 4bb755d088a35f4a466efd3c563b14dcab1518130c7b249770147648c80ada76 over 35658 bytes and 390 lines, and that value EQUALS the digest carried in the task prompt. C0b was written from `git show 87e1e8bf:.agent/authored/f009-r3.md`, never from the scratch file.
- G3 SIX slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob by their marker lines; newline-INCLUDED sha256 prefix/bytes/lines: PLANF009R3 b4224c16/2539/44, LEDGER3 edb594d8/5447/1, DECISIONS 5886087d/12969/101, FEATFROM fdfded12/106/2, FEATTO 40fab35e/281/4, CONTEXTF009R3 44439677/3351/54. Aggregates over those six: ANY TRAILING WHITESPACE False, ANY LEADING BLANK LINE False, ALL NEWLINE TERMINATED True.
- G4 `.agent/plan.md` at C1 BYTE-EQUAL to PLANF009R3 (sha256 b4224c16…, 2539 bytes), 44 lines against the 50-line cap; `Steps` occurs 1×; `^## Goal$` 1 line and `^## Next Steps$` 1 line; the FIRST `\bF\d{3}\b` match is `F009`.
- G5 The append at C2, proved TWICE over independent extractors, the base bytes read with `git show ee2fdda7:.agent/live_review.md` into `.remedy-wt/` scratch and never written over the tracked file. (a) The base blob IS a byte-exact PREFIX of the C2 blob and the remainder EQUALS a newline plus LEDGER3 — remainder sha256 47ef4740ea7577a9beb9f6ad060768637373a4c5c4e4750b1799f366a40bc21a, 5448 bytes, 2 lines. (b) An INDEPENDENT blank-line split of the WHOLE C2 file with its terminating newline normalised first yields N = **204** units whose LAST unit IS LEDGER3's paragraph. NEGATIVE CONTROL, one printable ASCII byte of the remainder flipped (offset 1, `G`→`H`): reader (a) ACCEPTS unflipped True / REJECTS flipped True; reader (b) ACCEPTS unflipped True / REJECTS flipped True — all four as required.
- G6 Line-anchored at the round base and at C2: `^- R-\d+ — ` 196 and 196 with 196 DISTINCT ids at both, so THIS ROUND MINTED NO ID; `^Done: R-\d+ — ` 1 and 1; `^Landed: ` 0 and 0; `^- R-0630 — ` 1 and 1; `^> Next free id` 0 and 0; `^Gate: R\d+ — ` 2 then **3**, over 3 DISTINCT keys (`R1`, `R2`, `R3`). HEADER SHAPE: of the 3 `Gate: ` lines at C2, **2** match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first, and the **1** non-match reads exactly `Gate: R1 — the F008 R36 entry.` — the expected reading.
- G7 The append at C3, proved the same two ways, base bytes read with `git show ee2fdda7:.agent/decisions.md` into scratch. (a) The base blob IS a byte-exact PREFIX of the C3 blob and the remainder EQUALS a newline plus DECISIONS — remainder sha256 24a68e46737b67515853181261c0776a486af478194aabc1ddfc78d29a8598ba, 12970 bytes, 102 lines. (b) An INDEPENDENT blank-line split of the whole C3 file yields N = **1092** units whose LAST unit IS DECISIONS' last paragraph. NEGATIVE CONTROL with a printable byte flipped INSIDE that last paragraph (remainder offset 12906, `R`→`S`): both readers ACCEPT unflipped and both REJECT flipped. `^## DECISION F009 D\d+ — ` 0 at the base and **9** at C3 over 9 DISTINCT keys D1…D9; `^## DECISION ` **85** at the base and **94** at C3.
- G8 The amendment at C4, base bytes read with `git show ee2fdda7:docs/roadmap/features/T5_F009.md` into scratch: FEATFROM 1 at the base and 0 at C4, FEATTO 0 then 1, and the base blob with that substitution applied ONCE is BYTE-EQUAL to the C4 blob — which is also the proof no other line of that file changed. Line count 90 at the base and 92 at C4. `tests/ui_contract/` reads **1** at the base and **1** at C4: FEATTO deliberately QUOTES the retired path while explaining the amendment, so that count does not fall to 0 and this gate reports it rather than driving it.
- G9 `.agent/context.md` at C5 BYTE-EQUAL to CONTEXTF009R3 (sha256 44439677…, 3351 bytes, 54 lines). The four reader assertions, taken over the APPLIED file: `test_dashboard_contract.py:204` `## Active Branch` present and `feature/` present (slug `feature/f009-single-write-channel`) True; `test_dashboard_contract.py:446` `Steps` present True (1 occurrence, no stale `Steps 91-100`); `test_test_runner.py:785` `\bF\d{3}\b` matches, first match `F009`, plus `## Active Branch` and `feature/` True; `test_resource_safety.py:113` `resource` or `pytest` in lowercase True (2 and 3 occurrences). All negative substrings those tests forbid read absent.
- G10 In the PRIMARY checkout, SERIALLY, one process at a time, at C5, each exit code read from the runner rather than from a pipeline: `tests/docs/ -q -rf` EXIT 0, 295 passed 0 skipped, SUM **295**; `tests/orchestration/test_roadmap_index.py -q -rf` EXIT 0, 30 passed 0 skipped, SUM **30**; `tests/ui_server/ + test_test_runner.py + test_resource_safety.py + test_integrity_gate.py -q -rf` EXIT 0, 423 passed 0 skipped, SUM **423**; canary `tests/cli/test_golden_path.py -q -rf` EXIT 0, 42 passed 0 skipped, SUM **42**. The docs gate WAS ordered because C4 edits a path under `docs/roadmap/`. PLAINLY: NEITHER `tests/docs/` NOR `tests/orchestration/test_roadmap_index.py` ASSERTS ANYTHING ABOUT `T5_F009.md`'s BODY — `tests/docs/` derives feature ids from FILENAMES (`_feature_ids` at `tests/docs/test_docs_consistency.py:41-50`) and reads bodies only of `T0_F010.md`, `T0_F011.md` and `T0_F012.md`, and the roadmap index parses only each feature file's title and dependency lines (1–2), while the amendment sits at lines 89–92. Neither suite names F009. G8's byte proof, not either suite, is what establishes the amendment landed; the two suites establish only that the edit broke nothing they do assert.
- G11 `git diff --name-only ee2fdda7 20f5dcf0` lists 7 paths which are EXACTLY the change set minus `.agent/handoff.md`, the set difference EMPTY in both directions. `git rev-list --reverse` gives SEVEN commits, each read to have exactly ONE parent, with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-` column above: insertions 390, 319, 24, 2, 102, 3 and 26 — every one under the 500 cap, 390 the maximum, so the AGENTS.md DECISION F104 D1 single-state-file exemption is NAMED but not needed. Lines beginning `<<<SLICE ` or `<<<END `: 0 in each of `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/features/T5_F009.md` and `.agent/context.md` at their commits. This round's own reflog entries classified by the operation before the first `:` in the reflog subject: 7 entries, all `commit`; `amend` 0, `rebase` 0, `cherry` 0. That reading covers C0a…C5; C6 adds one further `commit` entry whose value cannot exist while this sentence is written (R-0371). No total over the whole reflog is asserted (R-0601).
- G12 This file carries every mandated section of docs/agents/handback_template.md, the item-status table below holding exactly one row for each of C0a, C0b, C1, C2, C3, C4, C5 and C6, the round base SHA, and one line per gate G1–G12 — the raw transcripts are in the round report (R-0582). Its measured `wc -l` is **81**, under the 100 that AGENTS.md allows an eight-commit bundle.

## Authored-text proofs
- `.agent/authored/f009-r3.md` at C0a == the received block byte for byte, and `.agent/last_block.md` at C0b == the same bytes, read out of the COMMITTED C0a blob (G2). All SIX slices were extracted from that committed blob by their marker lines with a script and applied programmatically — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. Whole-file byte equality: PLANF009R3 (G4), CONTEXTF009R3 (G9). Prefix-plus-remainder equality with an independent second extractor and a negative control: LEDGER3 (G5), DECISIONS (G7). Single-substitution byte equality: FEATFROM→FEATTO (G8). G11 confirms 0 marker lines in every committed target.

## State — Fortschritt
10 % (T001 offen · T002 offen · T003 offen — R1 beansprucht, R2 vermessen, R3 entschieden; gebaut wurde noch nichts) — Schätzung

## Item status
| Item | Status | Reason |
| C0a | done | |
| C0b | done | |
| C1 | done | the first substantive commit |
| C2 | done | LEDGER3 appended; no `Done:` paragraph of mine was written |
| C3 | done | D1–D9 appended; NOTHING they rule was implemented |
| C4 | done | one substitution in the feature file, proved byte for byte |
| C5 | done | the push follows it with no commit between |
| C6 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit and the push ran between C5 and C6 with no commit between them.
- G1 ordered TWO STOP readings, "at Step 0 and again immediately before C0a". I took ONE at Step 0, which WAS the reading immediately before C0a — only the digest check, an `ls` of `.agent/authored/`, a `git check-ignore` and the copy script ran between them, and no commit did. A second reading was taken before C6. Declared rather than described as two.
- G7's negative control needed a TARGETED byte and this is declared, not hidden. DECISIONS is 51 paragraphs, so reading (b) as the gate words it — "the split ends in DECISIONS' last paragraph" — is only sensitive to that last paragraph: a byte flipped in the FIRST paragraph (remainder offset 4, `D`→`E`) is REJECTED by reader (a) and by a stronger tail comparison of all 51 units, but ACCEPTED by reader (b). The reported control therefore flips a byte inside the last paragraph, where both readers reject. Both measurements are in the round report; nothing was re-run to obtain a colour.
- NO OBJECTION this round: all six slices read as correct and were applied byte for byte regardless.
- LENGTH, stated rather than claimed clean: this file is 81 lines. That is over the 60-line default and UNDER the 100 AGENTS.md allows a bundle of more than five commits, so no DECISION D15 stated-cause overage is claimed. The length is mandated content — eight per-commit changed-files tables, twelve one-line gate readings of which G5, G7, G9, G10 and G11 each carry a multi-value measurement, and the eight-row item-status table. No section was dropped and no transcript was pasted.
- PARTIAL READ, declared against the AGENTS.md File Editing Safety Rule: `.agent/live_review.md` (388005 bytes / 1046 lines at the round base) and `.agent/decisions.md` (414489 bytes / 6621 lines) were not read end to end. Both edits are pure appends made programmatically over whole-file bytes, with G5's and G7's two independent extractors plus their negative controls and G6's and G7's line-anchored set readings standing in for the human read. `.agent/plan.md`, `.agent/context.md` and `docs/roadmap/features/T5_F009.md` WERE read in full, and every one of the seven diffs was reviewed with `git diff --stat` then `git diff` before its commit.
- NO CODE WAS WRITTEN. Nothing was created under `tests/` — `tests/ui_server/test_command_channel.py` does NOT exist — no config key was added, and no path under `packages/` or `apps/` was touched; G11's path list is the measurement. Every one of D1–D9 is a ruling for R4 onward. `ruff check .` and `npm run lint` were not run: both are red at base, neither is a gate (R-0364, R-0622), and this round authored no code.
- The session command guard rejects `$(...)`, `${...}`, heredocs, shell loops and `;`-chained commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run with `python3`; `git status --porcelain` printed 0 lines after each commit, so nothing from that directory was ever staged. No gate command was piped, so no exit code reported here is a pipeline's last stage.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which is EMPTY — this branch carries no pull request and F009 opens one at its own closure. Then R4, the first BUILD round: T001's first half against D2, D3 and D4 — the POST `/api/jobs/<job_id>/commands` route, the `Authorization: Bearer` plus `X-Remedy-CSRF` pair, `secrets.compare_digest` for BOTH the existing GET check and the new POST check, the `UI_EXPOSED_COMMANDS` frozenset beside `CATALOG` holding `job.stop` and `decision.resolve`, and typed validation errors, with contract tests in `tests/ui_server/test_command_channel.py`. 196 findings are OPEN, all DISTINCT, the highest registered id is R-0630 and the next free id is derived with `max` over the line-anchored `^- R-\d+ — ` entries. `.agent/candidates.md` is EMPTY. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613 and R-0630 stay routed to a paydown branch.
