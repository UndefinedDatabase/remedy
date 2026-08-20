# Handback — F255 R5 (Teacher role): apply D6, add checklist item 30, record R4

## Range
Review of `b40c0616..HEAD` — branch `feature/f255-teacher-role`, eight commits, no code.

## Commits

### d450dfe2 docs(state): save the F255 R5 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f255-r5.md` | 287/0 | C0a — the R5 block, byte-copied from `.remedy-wt/f255-r5.md`. |

### 4ecf0204 docs(state): mirror the F255 R5 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 218/268 | C0b — same bytes mirrored; verbatim rewrite of one `.agent/` state file. |

### fcd0ee37 docs(review): register finding R-0603
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | C1 — R0603 appended after exactly one blank line. |

### 4d1ca90c docs(agents): withdraw the handback token cap per DECISION F255 D6
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/handback_template.md` | 10/2 | C2 — CAPFROM→CAPTO, a REWRITE pair; the token cap is gone. |

### 9a4b3fbf docs(agents): add checklist item 30 on searching the open set
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | 19/0 | C3 — ITEM30FROM→ITEM30TO, APPEND-shaped; zero deletions. |

### 6e5b2196 docs(review): record the R4 verdict and resolve three findings
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 8/0 | C4 — RECORDR4, DONE0462, DONE0602, DONE0603 appended in order. |

### 22825f85 chore(plan): advance the plan to F255 R5
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 18/16 | C5 — whole-file PLAN255R5, 42 lines. |

### (this commit) docs(state): write the F255 R5 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | see round report | C6 — this file; a handback cannot table its own cell (R-0149). |

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

## External actions
`git push` after C6 — real output in the round report. No pull request created and none open on
this branch; no CI run awaited or reported (constraint 10); no `gh` command run; no git worktree
created or removed this round.

## Verification
One line per gate; the full transcripts are in the round report, not here (R-0582).
- G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every one of the eight commits and at the handback; `git worktree list` reports the primary checkout alone. Every blob reading taken with `git show`, nothing written over a tracked file to read it.
- G2 `.remedy-wt/f255-r5.md`, `.agent/authored/f255-r5.md` @d450dfe2 and `.agent/last_block.md` @4ecf0204 are all EQUAL at sha256 `ce51cd34…`, 26527 B, 287 lines — the digest stated at delegation.
- G3 slices extracted by `git show d450dfe2:.agent/authored/f255-r5.md` piped through a marker regex, from the COMMITTED C0a blob, never retyped; newline-INCLUDED convention (R-0600). The block carries TEN slices, not nine (declared below); all ten measured: CAPFROM `ad36f5b4…` 104 B 2 L · CAPTO `f2039951…` 708 B 10 L · ITEM30FROM `f3a49657…` 76 B 1 L · ITEM30TO `2bf0bdd7…` 1563 B 20 L · R0603 `f7f38e91…` 1838 B 1 L · RECORDR4 `075a20c6…` 3795 B 1 L · DONE0462 `07dc188f…` 1513 B 1 L · DONE0602 `89cccbfd…` 960 B 1 L · DONE0603 `7b223224…` 777 B 1 L · PLAN255R5 `234b7965…` 2363 B 42 L.
- G4 the base blob is a byte-exact PREFIX of the C1 blob; remainder `a236b09b…` 1839 B 2 lines equals LF + R0603, blank separator PRESENT. Registered / resolved / open / line-anchored `^Landed:` measured 178 / 0 / 178 / 0 at b40c0616 and 179 / 0 / 179 / 0 at C1, exactly the ordered move. `- R-0603 — ` occurs 0x at the base and 1x at C1.
- G5 in `docs/agents/handback_template.md` CAPFROM is present 1x at the base and 0x at C2; CAPTO 0x at the base and 1x at C2 — the FROM-zero count this REWRITE shape owes. `git diff --numstat` for the file at C2 is `10  2`. The LINE-cap sentence naming ≤60, ≤100 and ≤160 is present exactly 1x at BOTH ends and was NOT edited; the file goes 70 → 78 lines.
- G6 in `docs/agents/planner_reviewer_prompt.md` the pair is APPEND-shaped, so NO FROM-zero count is reported: it is unreachable by construction (§4.9, R-0207). ITEM30FROM occurs exactly 1x at the base AND exactly 1x at C3. Each of the 19 lines of ITEM30TO not in ITEM30FROM occurs exactly 1x among the 19 lines C3's diff ADDS. `git diff --numstat` for the file at C3 is `19  0`. `^  30. ` occurs 0x at the base and 1x at C3. SCOPED to the checklist block — lines 173..722 of the C3 blob, from `- **Pre-emission block checklist` to `  Why this is on disk` — the lines matching `^  \d+\. \*\*` number exactly 1..30 with no gap and no repeat; the same regex measured UNSCOPED reads 34, as the gate predicted.
- G7 the C1 blob is a byte-exact PREFIX of the C4 blob; remainder `efadbb7b…` 7049 B 8 lines equals LF+RECORDR4, LF+DONE0462, LF+DONE0602, LF+DONE0603 byte for byte, each preceded by exactly one blank line. A SECOND, independent paragraph-level split of the whole C4 blob yields 191 units whose LAST FOUR are those four slices in that order. Negative control — one character of the expected remainder mutated, `t`→`u` — is REJECTED by BOTH readings. Sets 179 / 0 / 179 / 0 at C1 and 179 / 3 / 176 / 0 at C4. `Done: R-0462 — `, `Done: R-0602 — ` and `Done: R-0603 — ` each occur 1x; `Gate: R5 — the R4 entry.` occurs 1x and is the LAST of the five lines beginning `Gate: R`, whose header keys `Gate: R1`…`Gate: R5` are all distinct.
- G8 `.agent/plan.md` @22825f85 byte-equals PLAN255R5 at `234b7965…`, 2363 B, 42 lines — under the 50-line cap — with `## Goal`, `## Next Steps` and the roadmap F-id `F255` all present.
- G9 serially, in the primary checkout, never two pytest processes at once: the four-file state-reader selection exit 0, 160 passed; `python3 -m pytest tests/docs/ -q -rf` exit 0, 295 passed; `tests/cli/test_golden_path.py` exit 0, 42 passed. All three equal the reviewer's readings at b40c0616. The `tests/docs/` run is a REGRESSION check only and is NOT evidence about C2 or C3 — that suite is blind to `docs/agents/**`; the proof for this round's two edits is G5 and G6, which read the files themselves.
- G10 `git diff --name-only b40c0616..HEAD` equals the Change list with no path on either side alone; the same command scoped to `apps/ packages/ tests/ scripts/` is EMPTY; each of the seven paths named untouched is PRESENT at the base and absent from the range; every commit in the range has exactly one parent; insertion columns 287, 218, 2, 10, 19, 8, 18, every one under 500 and the same `+/-` cells as the tables above. Reflog as TWO measured claims read from the operation PREFIX before the first colon (R-0601): 7 entries whose prefix is `commit`, one per commit made before C6, and 0 whose prefix contains `amend`, `reset`, `rebase` or `cherry`. C6's own entry, the final 8 / 0 reading and C6's numstat cell are in the round report.
- G11 lines beginning `<<<SLICE ` or `<<<END `: `.agent/live_review.md` @6e5b2196 0, `docs/agents/handback_template.md` @4d1ca90c 0, `docs/agents/planner_reviewer_prompt.md` @9a4b3fbf 0, `.agent/plan.md` @22825f85 0. `.agent/handoff.md` carries no such line either; its committed-blob reading is in the round report.
- G12 `git push` after C6 — real output in the round report. No pull request created, no CI run awaited.

## Authored-text proofs
All ten slices were applied by script from the COMMITTED `.agent/authored/f255-r5.md`, never retyped and never rewrapped. Disk-to-disk against that file: the C1 append remainder equals LF + R0603; the C4 append remainder equals the four verdict/resolution slices with their LF separators; the C2 and C3 edits replace an extracted FROM with an extracted TO in place; `.agent/plan.md` at C5 byte-equals PLAN255R5. Digests under G3, G4, G5, G6, G7 and G8 above.

## Deviations & assumptions
- ORDERED COMMIT SEQUENCE FOLLOWED EXACTLY. C0a, C0b, C1, C2, C3, C4, C5, C6 in the block's order, one path each, no extra commit, none dropped, none reordered.
- THE BLOCK SAYS "NINE SLICES" AT G3 AND CARRIES TEN. The markers found in the committed C0a blob are CAPFROM, CAPTO, ITEM30FROM, ITEM30TO, R0603, RECORDR4, DONE0462, DONE0602, DONE0603 and PLAN255R5 — ten. Nothing was edited or dropped to reconcile the numeral: all ten are measured under G3 and all ten were applied, and the discrepancy is declared here rather than repaired (constraint 1).
- NO FROM-ZERO COUNT IS REPORTED FOR THE C3 PAIR. G6 forbids it and the shape cannot reach it; ITEM30FROM is reported 1x at BOTH ends instead. The C2 pair is a REWRITE and does carry its FROM-zero count.
- THE REFLOG WHOLE-LINE CONTROL RETURNED 0 THIS ROUND. Read by operation prefix: 7 `commit`, 0 rewrite. Read as a whole line — the form R-0601 retired — also 0, because no subject this round contains `amend`, `reset`, `rebase` or `cherry`. Last round the same control returned 1 and discriminated; this round it does not, which is reported rather than presented as the control passing.
- "HEADER KEY" READ AS THE `Gate: R<n>` PREFIX. Under that reading the five verdict lines carry `Gate: R1`…`Gate: R5`, all distinct. A naive text-before-the-first-colon reading returns `Gate` five times and is not the ordered reading; both were measured and the interpretation is stated so the reviewer can re-measure the one it meant.
- SCRATCH HELPERS, NOT PART OF THE CHANGE SET. The extraction and gate scripts and the ten extracted slice files live under the gitignored `.remedy-wt/` and are absent from the range.
- NO TOKEN-CAP CLAIM IS MADE EITHER WAY. C2 removed that sentence from the template; the LINE cap this eight-commit table earns is the operative bound and this file is inside it.
- NOTHING WAS BUILT. No source file, no test, no role, no config key (Change list, and the scoped G10 reading is EMPTY).

## Next
1. Phase 1 rule 1 of the next session: re-read `.agent/STOP` from disk.
2. R6 — the first source-touching round of this feature, building T001, the role vocabularies: `teacher` joins `KNOWN_ROLES` and `ConventionsRole`, the seven-to-eight pin lands in the SAME commit as the tuple it guards, and a `teacher.model` config key is added.

R5 awaits review. There is no open pull request on this branch.

Fortschritt: ~15 % (F086 merged · F255 claimed · ground measured · six DECISIONs ruled · the feature file carries its spec · the process holes closed · T001 builds next) — Schätzung
