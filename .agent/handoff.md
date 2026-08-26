# Handback — F031 Decision inbox, round R14

Branch `feature/f031-decision-inbox`; base `d63a146fb9c7f0a782887dd768ec7c5bb6f7dcf6`, the R13 handback. Commits this round: 11c013fb, 2f80a495, 597c20ce, e97264fd, 475f0f36 and the C4 commit that writes this file.

Fortschritt: ~45 % (F031 claimed; R1 through R13 landed and gated ·
             T001 SHIPPED · T002a's MODEL shipped, red-proofed and now
             WIRED · the `.tsx` projection, T002b ordering/filtering/
             badge and T003 offen) — Schaetzung

## Range

Review of d63a146f..HEAD.

## Commits

### 11c013fb chore(agent): save the F031 R14 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r14.md | +444/-0 | C0a — the block, saved verbatim |

### 2f80a495 chore(agent): mirror the R14 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +266/-167 | C0b — byte-identical mirror of C0a |

### 597c20ce docs(agent): point the F031 plan at the R14 wiring step
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18/-18 | C1 — slice PLANF031R14, whole file |

### e97264fd docs(agent): record the F031 R13 verdict and resolve R-0680
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — slice LEDGER14, appended |

### 475f0f36 feat(ui): project the decision inbox into the dashboard payload
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/types.ts | +14/-2 | S1 — non-optional `decisionInbox` field |
| apps/ui/src/api/remedyApi.ts | +29/-2 | S2 projection, S3 `/decisions` fetch |
| apps/ui/src/api/remedyApi.test.ts | +40/-0 | S4 — four appended cases, none edited |

### C4 docs(agent): write the F031 R14 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | a handoff cannot table its own commit (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| push (G11) | done | ordered after C4; outcome carried by G11 to the reviewer |

## External actions

`git worktree add --detach .remedy-wt/wt-r14 475f0f36` → rc 0; `git worktree remove --force .remedy-wt/wt-r14` → rc 0, path gone, list back to 1 line.
`git push origin feature/f031-decision-inbox`, run after C4. Its outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R14 entry of `.agent/live_review.md`.
No pull request created, edited or merged; no `gh` command run; no force flag, no history rewrite, no branch deletion.

## Verification

G1 — `git branch --show-current` printed `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk was ABSENT before C0a and again before C4; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3.
G2 — all four readings (scratch before C0a, committed C0a blob, committed C0b blob, `.agent/last_block.md` off disk) are sha256 `1a6e1b0f6058637e59e8cc84122a414d46729a97f551b4bbcea0e205665b9827`, 32941 bytes, 444 lines, EQUAL; C0a's and C0b's file is the same git blob `cb5e9ea8188e9ec89b9419238a53bfa4813e0ebe`.
G3 — my extractor over the committed C0a blob printed: 2 slices (PLANF031R14, LEDGER14), 52 content lines inside markers, 444 total lines.
G4 — convention newline-INCLUDED; `.agent/plan.md` at C1 is byte-equal to PLANF031R14, 2925 slice bytes = 2925 file bytes, TRUE; negative control against the slice with its trailing newline REMOVED is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
G5 — reader (a), the whole-file equality in the shape constraint 7 states: TRUE, arithmetic 597681 + 1 + 6373 = 604055 against an actual 604055; reader (b), blank-line units 290 → 292, N = 2 as MY split of the slice measured it, and the last 2 units equal LEDGER14's 2 paragraphs IN ORDER; negative control, one byte flipped 100 bytes into the FIRST paragraph the append added, written only inside the disposable worktree: both readers REJECT the mutant and both ACCEPT the true file.
G6 — `^- R-\d+ — ` 241 → 241, all DISTINCT at both ends, ids ADDED the EMPTY SET, ids REMOVED the EMPTY SET, maximum `R-0680` UNCHANGED; `^Done: R-` 2 → 3 with the ids added exactly `R-0680`; `^Recurrence: R-` 15 → 15; `^Gate: R\d+ — ` 13 → 14, gaining exactly the key `R13`, `R19` and `R1` through `R12` still present, all 14 DISTINCT; §3 item 10 open set at C2 = 238.
G7 — `^<<<SLICE `/`^<<<END ` count 0/0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and each of the three `apps/` files at C3; `git diff --name-only d63a146f..475f0f36` names no path under `packages/`, `tests/` or `docs/`, no `apps/` path beyond section 5's three, and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory; per commit single-parent TRUE with insertions 444, 266, 18, 4, 83, each under 500, every one derived from `git diff --numstat` and agreeing cell for cell with the `## Commits` tables above (§3 item 28); range path set MINUS change set is EMPTY, change set MINUS range is exactly `.agent/handoff.md`; `git ls-files .remedy-wt` 0 and `git ls-files '*.zip'` 0; reflog scoped to THIS ROUND'S 5 entries and read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs` — all 5 are `commit`, so amend 0, rebase 0, cherry 0.
G8 — in `apps/ui` at C3, `npm run typecheck` real exit 0 with ZERO diagnostics, so S1's non-optional field named no third construction site; `npm run test:unit` real exit 0 at 21 files, UNCHANGED, and 316 tests, strictly greater than the base's 312 by a difference of +4; `git diff d63a146f..475f0f36 -- apps/ui` deletes 0 lines in `remedyApi.test.ts`.
G9 — unmutated control at the worktree root: exit 0, 1 file, 56 tests passed; then `normalizeDashboardPayload` mutated in the WORKTREE ONLY so `decisionInbox` is the empty array for every input, same command re-run: exit 1, the run is RED, 1 failed and 55 passed, and the only failing test is `decisionInbox projection > projects every card of the document, in the endpoint's order`, which is S4 case (a); worktree removed by its exact path, `git worktree list` 1 line and `git status --porcelain` 0 lines in the primary checkout.
G10 — 22 SHA-shaped tokens with repeats, 9 distinct, FAILING SET EMPTY; `15e71b0dbeabdd80100b08cb9c236d1a013258d7` resolves to type `blob` and the other eight (`13306809`, `6325ac2f`, `8b4e2295`, `8df27c6e`, `a48e0144`, `bae304bc`, `d63a146f`, `d63a146fb9c7f0a782887dd768ec7c5bb6f7dcf6`) to type `commit`; `git worktree list` was 1 line immediately before the first pytest; the five suites ran SERIALLY, never two alive, every one a real exit 0 — tests/ui_server/ 474, test_test_runner 52, test_resource_safety 21, test_integrity_gate 16, test_golden_path 42, identical to the reviewer's base readings, so there is no difference to account for.
G11 — the push runs after C4; the command and its named carrier are in `## External actions`.

## Authored-text proofs

Both slices were extracted PROGRAMMATICALLY from the committed C0a blob `11c013fb:.agent/authored/f031-r14.md` by their `<<<SLICE`/`<<<END` marker lines and never retyped.
Disk-to-disk: `.agent/plan.md` at C1 is byte-equal to PLANF031R14 (G4); `.agent/live_review.md` at C2 equals its base blob plus one newline plus LEDGER14 (G5, two independent readers plus a rejected mutant).

## Deviations & assumptions

The ordered sequence C0a, C0b, C1, C2, C3, C4 ran exactly: no extra commit, none dropped, none reordered, and no contradiction was found inside the block.
Assumption declared: section 5 left the fourth parameter's TYPE unstated, so I used `any`, matching `dashboard: any` and `brainDetail?: any` in the same signature inside the file's existing `no-explicit-any` disable region.
Handback tier, derived rather than quoted: constraint 3 fixes SIX commits, and 6 > 5, so AGENTS.md `### handoff.md` puts this file at the ≤100-line tier, which it meets.
Finding counts per DECISION F009 D10: by the §3 item 10 rule — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 238, measured in `.agent/live_review.md` at commit e97264fd; the findings THIS FEATURE MUST STILL ACT ON are the eighteen named in `.agent/plan.md` at 597c20ce, and R-0680 is no longer among them.

## Next

1. Phase 1 rule 1: re-read `.agent/STOP` from disk.
2. Phase 1 rule 2, the Open PR Gate: run `gh pr list --state open`, and report what it printed and whether any pull request exists for this branch.
3. The R14 verdict is UNRECORDED and is owed by the next round's ledger commit — by DECISION F085 D9 no artefact of this round can carry it.
4. The next build step is the `.tsx` projection per DECISION F031 D4: a card built from the shipped `RightLivePanel.module.css` shell, mounted in `RightLivePanel`, reading `dashboard.decisionInbox`, with no branching of its own.
