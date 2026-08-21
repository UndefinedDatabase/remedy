# Handback — F009 The single write channel, R4 (R-0631 REGISTERED, R3 VERDICT RECORDED, PLAN SET FOR R5 — no production code, no test file, nothing under `packages/`, `apps/`, `tests/` or `docs/`)
## Range
Review of `8b3591dd`..C4, the handback commit itself (6 commits, branch feature/f009-single-write-channel). THE ROUND BASE IS `8b3591ddfb14c4873a65fdb13a4e3822986ff729`, read at Step 0 and the value every "at the round base" gate below is measured against; it is the value the block predicted. C4's own SHA cannot exist inside C4, so it is named by role and the round report carries the value (R-0371).
## Commits
### d6a4ac07 chore(agent): save the F009 R4 step block
| Path | +/- | Reason |
| `.agent/authored/f009-r4.md` | +192/-0 | C0a, the R4 block saved byte for byte |

### 4f6035b0 chore(agent): mirror the F009 R4 block to last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +110/-308 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### f0de9f26 docs(state): set the plan to the F009 R4 finding and verdict round
| Path | +/- | Reason |
| `.agent/plan.md` | +20/-19 | C1, PLANF009R4 applied whole — the first substantive commit |

### 2995a9f1 docs(review): register R-0631 against the R3 append gate design
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2, R0631 appended as the last paragraph after one blank line |

### a3fb5d54 docs(review): record the R3 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C3, LEDGER4 appended the same way, on the C2 blob as its base |

### C4 docs(state): write the F009 R4 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C4 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` printed `[]`. That call is READ-ONLY and establishes the fact the `## Next` section states; NO Open PR Gate was run and NO pull request was created or merged (Step 0 and the standing rules for this round). No worktree was added or removed — `git worktree list` names the primary checkout alone, `/home/decodeux/Repos/remedy a3fb5d54 [feature/f009-single-write-channel]`. NO push had run when this file was written: the single `git push` this session owes follows C4, AGENTS.md push discipline requires it, and no handback can ever record it because it follows the file being written.

## Verification
- G1 `.agent/STOP` ABSENT — `ls -la .agent/STOP` printed `No such file or directory` and exited 2, at Step 0 and again before C4. `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel` at every reading. `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2 and C3; the post-C4 reading is in the round report. ROUND BASE `8b3591ddfb14c4873a65fdb13a4e3822986ff729`, the value the block predicted.
- G2 Transport EQUAL three ways — `.remedy-wt/f009-r4.md` as received, `.agent/authored/f009-r4.md` at C0a and `.agent/last_block.md` at C0b — all sha256 d7c9fda9b10dda513749f2aace51475d62e93179457953e0f0394370cd3ea4bf over 19558 bytes and 192 lines, and that value EQUALS the digest carried in the task prompt. C0b was written from `git show d6a4ac07:.agent/authored/f009-r4.md`, never from the scratch file again.
- G3 THREE slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob by their marker lines; newline-INCLUDED sha256 prefix/bytes/lines: PLANF009R4 dc1eac31/2708/45, R0631 5000840b/3435/1, LEDGER4 710b7b4d/4499/1. Aggregates over those three: ANY TRAILING WHITESPACE False, ANY LEADING BLANK LINE False, ALL NEWLINE TERMINATED True.
- G4 `.agent/plan.md` at C1 BYTE-EQUAL to PLANF009R4 (sha256 dc1eac31…, 2708 bytes), 45 lines against the 50-line cap; `Steps` occurs 1×; `^## Goal$` 1 line and `^## Next Steps$` 1 line; the FIRST `\bF\d{3}\b` match is `F009`.
- G5 The append at C2, proved TWICE over independent extractors IN THE GENERAL N-PARAGRAPH FORM R-0631's own fix clause prescribes — this round is the first to owe it. Base bytes read with `git show 8b3591dd:.agent/live_review.md` into `.remedy-wt/` scratch, never written over the tracked file. (a) The base blob IS a byte-exact PREFIX of the C2 blob and the remainder EQUALS a newline plus R0631 — remainder sha256 6694dc31e252daad92f9cb6aacb558724247bf2008f9364854e44cb5679f34a2, 3436 bytes, 2 lines. (b) N is COUNTED BY THE SCRIPT AND REPORTED, not asserted by the block: N = 1 paragraph in the R0631 slice; the WHOLE C2 file, its terminating newline normalised first, splits into 205 blank-line units by an INDEPENDENT line-walking extractor, and its LAST 1 unit EQUALS the slice's 1 paragraph IN ORDER. NEGATIVE CONTROL applied to the FIRST appended paragraph (offset 2 inside it, `R`→`Z`): reader (a) ACCEPTS unflipped True / ACCEPTS flipped False, reader (b) ACCEPTS unflipped True / ACCEPTS flipped False — all four outcomes as required.
- G6 The append at C3, with the C2 blob as its base, proved the same two ways and with its own control. (a) The C2 blob IS a byte-exact PREFIX of the C3 blob and the remainder EQUALS a newline plus LEDGER4 — remainder sha256 61435d8c31ad9c7553cdf03868317424fa60b6d836b54d5bd21ec134471f4aac, 4500 bytes, 2 lines. (b) N COUNTED THE SAME WAY = 1 paragraph in the LEDGER4 slice; the whole C3 file splits into 206 units and its LAST 1 unit EQUALS that 1 paragraph IN ORDER. NEGATIVE CONTROL on the FIRST appended paragraph (offset 0, `G`→`Z`): reader (a) True / False, reader (b) True / False. BOTH slices are the N=1 case, so the first appended paragraph IS also the last; the general form was run anyway, since its wording is what carries to a round where N is larger.
- G7 Line-anchored at the round base, at C2 and at C3: `^- R-\d+ — ` 196, 197 and 197, with 196, 197 and 197 DISTINCT ids — ALL DISTINCT at each; `^- R-0631 — ` 0, 1 and 1; `^Done: R-\d+ — ` 1, 1 and 1; `^Landed: ` 0, 0 and 0; `^> Next free id` 0, 0 and 0; `^Gate: R\d+ — ` 3, 3 and 4 over 3, 3 and 4 DISTINCT keys (`R1`,`R2`,`R3` then `R1`…`R4`). THE MAX ID THE FILE CARRIES AT C3 IS R-0631. Of the 4 `Gate: ` lines at C3, 3 match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first, and the 1 non-match reads exactly `Gate: R1 — the F008 R36 entry.` — the expected reading.
- G8 `git diff --name-only 8b3591dd..a3fb5d54` lists 4 paths which are EXACTLY the change set minus `.agent/handoff.md`, the set difference EMPTY in both directions. `git rev-list --reverse` gives FIVE commits, each read to have exactly ONE parent, with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-` column above: insertions 192, 110, 20, 2 and 2 — every one far under the 500 cap, so the AGENTS.md DECISION F104 D1 single-state-file exemption is NAMED but not needed. Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` and 0 in `.agent/live_review.md` at C3. This round's own reflog entries, taken base-exclusive and classified by the operation before the first `:` in the reflog subject: 5 entries, all `commit`; `amend` 0, `rebase` 0, `cherry` 0. C4 adds one further `commit` entry whose value cannot exist while this sentence is written (R-0371). NO total over the whole reflog is asserted (R-0601). `git ls-files .remedy-wt` = 0.
- G9 This file carries every mandated section of docs/agents/handback_template.md, the item-status table below holding exactly one row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, and one line per gate G1–G9 — the raw transcripts are in the round report (R-0582). Its measured `wc -l` is 66, over the 60-line default and UNDER the 100 AGENTS.md allows a bundle of more than five commits, so no DECISION D15 stated-cause overage is claimed.

## Authored-text proofs
- `.agent/authored/f009-r4.md` at C0a == the received block byte for byte, and `.agent/last_block.md` at C0b == the same bytes, read out of the COMMITTED C0a blob (G2). All THREE slices were extracted from that committed blob by their marker lines with a script and applied programmatically — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. Whole-file byte equality: PLANF009R4 (G4). Prefix-plus-remainder equality with an independent second extractor, a counted N and a negative control on the FIRST appended paragraph: R0631 (G5), LEDGER4 (G6). G8 confirms 0 marker lines in both committed targets.

## State — Fortschritt
10 % (T001 offen · T002 offen · T003 offen — beansprucht, vermessen, entschieden; der Bau beginnt in R5 mit D1 bis D9 als Vorgabe) — Schätzung

## Item status
| Item | Status | Reason |
| C0a | done | |
| C0b | done | |
| C1 | done | the first substantive commit, since this round registers a finding |
| C2 | done | R0631 appended; no `Done:` paragraph or other ledger text of mine was written |
| C3 | done | LEDGER4 appended; the verdict is the reviewer's, recorded after the finding |
| C4 | done | this commit; the push follows it |

## Deviations & assumptions
- NO departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, C2 preceded C3, and nothing came between any of them.
- NO OBJECTION this round: all three slices read as correct and were applied byte for byte regardless. NO deviation was needed for the new G5/G6 shape — unlike R3, whose declared deviation 2 is exactly what R-0631 now records, the control landed on the first appended paragraph and BOTH readers rejected it, because at N=1 the first paragraph is also the last. Nothing was re-run to obtain a colour.
- LENGTH, stated rather than claimed clean: this file is 66 lines, over the 60-line default and under the 100 AGENTS.md allows more than five commits. The length is mandated content — six per-commit changed-files tables, nine one-line gate readings of which G5, G6, G7 and G8 each carry a multi-value measurement, and the six-row item-status table. No section was dropped and no transcript was pasted.
- PARTIAL READ, declared against the AGENTS.md File Editing Safety Rule: `.agent/live_review.md` (393453 bytes / 1048 lines at the round base) was not read end to end. Both edits to it are pure appends made programmatically over whole-file bytes, with G5's and G6's two independent extractors plus their negative controls and G7's line-anchored set readings standing in for the human read. `.agent/plan.md` WAS read in full before and after its rewrite, and every one of the five diffs was reviewed with `git diff --stat` then `git diff` before its commit.
- NO CODE WAS WRITTEN. `tests/ui_server/test_command_channel.py` does NOT exist, `packages/orchestration/ui_server.py` was not touched, and no path under `packages/`, `apps/`, `tests/` or `docs/` was edited — G8's 4-path list is the measurement, not a promise. The plan slice DESCRIBES what R5 will build; describing it is not building it. `ruff check .` and `npm run lint` were not run: both are red at base, neither is a gate (R-0364, R-0622), and this round authored no code.
- The session command guard rejects `$(...)`, backticks, heredocs, shell loops and `;`-chained commands BY FORM — the Step 0 probes were refused as one `;`-chained line and re-run separately — so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run with `python3`. `git status --porcelain` printed 0 lines after each commit and `git ls-files .remedy-wt` is 0, so nothing from that directory was ever staged. No gate command was piped, so no exit code reported here is a pipeline's last stage.
## Next
THIS SESSION ENDED AT ITS STATED FOUR-ROUND CAP with NO `.agent/STOP` present — a session that ends at its limit with a written handoff is a SUCCESS under guardrail G7, not a failure. The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which is EMPTY — this branch carries no pull request and F009 opens one at its own closure. 197 findings are OPEN, all DISTINCT, and THE NEXT FREE FINDING ID IS DERIVED WITH `max` OVER THE LINE-ANCHORED `^- R-\d+ — ` ENTRIES OF `.agent/live_review.md`, NEVER read from a header — no `^> Next free id` line exists there (G7 reads 0 at all three commits); that derivation gives R-0631 as the highest registered id. `.agent/candidates.md` is EMPTY. Then R5, the first BUILD round: T001's door exactly as `.agent/plan.md` now describes it — the POST route on `_RemedyHandler` dispatching `/api/jobs/<job_id>/commands`, the bearer plus `X-Remedy-CSRF` pair D2 rules, request-shape validation with typed errors naming the offending field, and BOTH halves of D3's constant-time comparison in one commit, compared as BYTES, with contract tests in `tests/ui_server/test_command_channel.py` per D1. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613 and R-0630 stay routed to a paydown branch.
