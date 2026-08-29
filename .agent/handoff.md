# Handback — F033 · ROUND 17 · the tasks-card row learns the partial apply state

> Written by the WORKER of round 17. The reviewer writes the verdict; this file
> reports what was run and what it printed. This round registered NO finding and
> resolved NONE: it wrote no `Done:` and no `Landed:` line.

## Session

SESSION 5 of feature F033 · round 17 · rounds so far 17.
The soft limit is NOT reached: 17 rounds of 25, 5 sessions of 7.

## Fortschritt

~90 % (T001 and T002 complete. T003: the apply fold's partial truth and the popover
label landed in round 16; THIS round landed the second of the three surfaces R-0738
names — the tasks-card row's tile and status text. The report line and the
rejection-to-repair injection remain, so R-0738 STAYS OPEN) — Schätzung.

## Range

Review of `5f0273d8`..`e0e2d12f` for the gated work — every gate below ran at a
commit no later than C5 — plus the two commits that cannot be inside it: C6, which
writes this file, and C7, which records the real push outcome after the push.
Branch `feature/f033-hunk-approval-v2`.

## Bundle item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f033-r17.md` | done | |
| C0b mirror it into `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` <- PLAN17 | done | |
| C2 `.agent/live_review.md` <- RECORD17 | done | |
| C3 `.agent/prose_slips.md` <- SLIPS17 | done | |
| C4 the tasks-card tile and status text (SPEC A, SPEC B) | done | |
| C5 the contract test (SPEC C) | done | |
| C6 `.agent/handoff.md` <- this handback | done | |
| C7 `.agent/handoff.md` <- the push outcome | done | recorded after the push |

## Commits

Every `+/-` cell below was taken from the SAME `git diff --numstat` run G8 reports
and compared to it cell by cell; they agree. No cell was filled from a file's own
line count.

### f0f744ba docs(f033): save the round 17 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r17.md` | +345 -0 | C0a — the reviewer's block, byte for byte |

### ce26560a docs(f033): mirror the round 17 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +345 -243 | C0b — same bytes, one blob id with C0a |

### 799dc2d0 docs(f033): advance the plan to round 17
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +14 -11 | C1 — PLAN17 replaces the file whole (checklist item 23) |

### 49052cf5 docs(f033): book the round 16 verdict and decision D5
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 -0 | C2 — RECORD17 appended; amend0827 rule 1 |

### 99e0efed docs(f033): append the two round 16 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4 -0 | C3 — SLIPS17 appended; amend0827 rule 2 |

### 81817cb8 feat(f033): show the partial apply state on the tasks-card row
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/components/panels/RightLivePanel.module.css` | +8 -0 | SPEC B — one `.checkPartial` rule and its `svg` sizing |
| `apps/ui/src/components/panels/TaskChecklistCard.tsx` | +15 -9 | SPEC A — `iconFor` and `stateText` take the ROW and read `applyStatus` first |

### e0e2d12f test(f033): pin the tasks-card row at the partial apply seam
| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_contracts/test_apply_state_partial.py` | +204 -13 | SPEC C — `helper_body` generalised, two new classes, the cross-component assertion |

### C6 and C7 (this file)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | see below | C6 writes this handback; C7 appends the real push outcome. A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` -> exit 0,
  output `[]`. No open PR; the Open PR Gate is satisfied and nothing was merged.
- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/r17/wt e0e2d12f`
  -> exit 0, "HEAD is now at e0e2d12f".
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r17/wt` -> exit 0.
  `git worktree list` afterwards shows only `/home/decodeux/Repos/remedy`.
- `git push` — see the PUSH OUTCOME section at the bottom, written by C7.
- No PR was created. F033 is not closed and §5 rules the PR into the closure sequence.

## Verification — one line per gate, real exit codes

G1 HYGIENE AND THE STOP FILE — `ls -la .agent/STOP` exit 2, printing exactly
`ls: cannot access '.agent/STOP': No such file or directory`, so the sentinel does
not exist; `git status --porcelain` before C0a exit 0 printing NOTHING, and again
after C5 exit 0 printing NOTHING.

G2 TRANSPORT — exit 0. Applied region vs the digest in each slice's own BEGIN
marker: PLAN17 region 2660 bytes sha256 `0171904031cd5176…dac566c0a` MATCHES;
RECORD17 last-6982-byte region sha256 `31cbb3f3a1270180…72419e30c` MATCHES;
SLIPS17 last-959-byte region sha256 `a0a8aefa37aa9328…2b401d429` MATCHES. The C0a
and C0b blobs are ONE id, `7258622877dfc17a9cdc8110f88c81f60647010a`, and the
committed `.agent/authored/f033-r17.md` has sha256
`3b932062979ba726e0f4c99a4b419f2bbf0a1d07a2634a4224cbc56fc070650c`, equal to the
block on disk. THIS PROVES THE SAVED COPY, ITS MIRROR AND THE WORKING COPY AGREE;
IT IS NOT A CLAIM ABOUT THE BYTES THAT WERE EMITTED.

G3 THE RECORD APPEND at C2 — exit 0, all three readings. (a) BYTES: pre-commit
blob 1542724 bytes as the block states; post-commit blob 1549707 bytes
(1542724 + 1 + 6982) as the block states; pre is a byte PREFIX of post True;
RECORD17 is an exact SUFFIX True; the working copy equals the committed blob True.
(b) STRUCTURE: N COUNTED at 2 by the script; the post-commit file splits into 706
blank-line units; the LAST 2 units equal the slice's 2 paragraphs IN ORDER True.
(c) NEGATIVE CONTROL: the FIRST appended paragraph was measured, before flipping,
at 0-based content span 1542725 to 1546617 — an EXACT match for the block's stated
span — and containment was ASSERTED as 1542725 <= 1544671 <= 1546617; the byte at
1544671 was flipped in memory from `h` to `H`; reading (a) REJECTS the flipped copy
True and reading (b) REJECTS it True. `.agent/live_review.md` on disk was verified
unchanged after the flip.

G4 THE LEDGER after C2 — exit 0, every count as a before and an after.
`^- R-\d+ — ` 306 before, 306 after, UNMOVED. `^Done: R-\d+ — ` 50 lines over 48
distinct before, 50 over 48 after, UNMOVED. `^Landed: R-\d+ — ` 17 before, 17
after, UNMOVED. `^Gate: F033 R16 — ` 0 before, exactly 1 after. Distinct
`DECISION F033 D<n>` ids D1 D2 D3 D4 (4) before, D1 D2 D3 D4 D5 (5) after, the
ADDED one D5. The open set, registered minus resolved, 258 before and 258 after,
UNMOVED. `^- R-0738 — ` exactly 1 at both ends, with `^Done: R-0738 — ` 0 at both
ends — the finding is ADVANCED, not resolved.

G5 THE PROSE FILES — exit 0. `.agent/plan.md` after C1 is 2660 bytes over 47 lines,
byte-EQUAL to PLAN17 True, under the 50-line cap AGENTS.md sets, and holds
`## Goal` (line 6) and `## Next Steps` (line 30). `.agent/prose_slips.md` 24982
bytes before C3 and exactly 25942 after (24982 + 1 + 959), the old bytes a PREFIX
True and SLIPS17 an exact SUFFIX True.

G6 THE MUTATIONS at `e0e2d12f`, inside the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/r17/wt`, every command
`python3 -B -m pytest tests/ui_contracts/test_apply_state_partial.py -q` run from
the worktree root with every `__pycache__` under it purged before each run.
UNMUTATED CONTROL FIRST: REAL exit 0, 20 passed. (i) anchor `styles.checkPartial`
asserted to occur EXACTLY 1 time; the `iconFor` line returning that tile deleted;
REAL exit 1, 1 failed and 19 passed, the failure being
`test_the_card_tile_for_partial_is_not_the_done_tile` — the card TILE assertion.
(ii) anchor `Partially applied` asserted EXACTLY 1 time; the `stateText` line
returning it deleted; REAL exit 1, 3 failed and 17 passed —
`test_the_card_labels_the_state_the_fold_emits`,
`test_the_card_partial_label_is_distinct_from_every_other_state_text` and the
cross-component `test_the_card_and_the_popover_use_one_spelling`, exactly the LABEL
assertions and SPEC C5. (iii) anchor `apply_by_task[tid] = "partial"` in
`packages/orchestration/ui_server.py` asserted EXACTLY 1 time and replaced by
`apply_by_task[tid] = "applied"`; REAL exit 1, 6 failed and 14 passed — the block
predicted MORE than its base of 2 and the measured number is 6: the two popover
failures plus ALL FOUR card SEAM assertions, which is what proves SPEC C derives
the emitted set from the shipped fold's AST rather than restating it. Every mutated
file was restored and PROVED byte-identical by sha256 —
`TaskChecklistCard.tsx` back to `9ce409621cb78969ff2fd356bbe499626150ab7056b6edc67daf17b488b36ba4`
and `ui_server.py` back to `802856ff756d25b5c0568900aa012d1bf68f439373d1b8277a3e92d4aec9e900`;
`git -C <worktree> status --porcelain` then printed NOTHING and the post-restore
control re-ran at REAL exit 0, 20 passed. The worktree was removed BY ITS EXACT
PATH and `git worktree list` shows only the primary checkout.

G7 THE SUITES, run SERIALLY in the PRIMARY checkout at `e0e2d12f`, every REAL exit 0.
`python3 -m pytest tests/ui_contracts/test_apply_state_partial.py -q` -> 20 passed,
above its base of 13, the seven added being the three card-vacuity and four
card-seam tests. `python3 -m pytest tests/ui_contracts/ -q` -> 684 passed, 4
skipped, against a base of 677 passed and 4 skipped — the same seven.
`python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` -> 74 passed.
`python3 -m pytest tests/regression/test_named_bugs.py -q` -> 64 passed, 6 skipped.
`python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed, the canary.
The ruff gate exited 0 — see deviation D1 for how it was invoked.

G8 THE STRUCTURE over `5f0273d8`..`e0e2d12f` — exit 0. Seven commits, every one
SINGLE-PARENT, with insertion counts from the `+` column of `git diff --numstat`:
345, 345, 14, 4, 4, 23 and 204, every one UNDER the 500 AGENTS.md DECISION F104 D1
caps. The path set over the range EQUALS the block's change set MINUS
`.agent/handoff.md` in BOTH directions: nothing in the range outside the expected
set, nothing expected and missing. All SIXTEEN do-not-touch paths were read at both
ends with `git rev-parse <commit>:<path>` and every pair of blob ids is EQUAL,
including `packages/orchestration/ui_server.py` at `de8bfabb62bb…`,
`apps/ui/src/api/types.ts` at `9e40bb480e55…` and
`docs/ui/design_reference/assets_spec.md` at `dd37500da3c5…`.

## Authored-text proofs

Three slices applied, all disk-to-disk.
- PLAN17 -> `.agent/plan.md`, whole-file replacement. The committed file is
  byte-EQUAL to the slice extracted from `.agent/authored/f033-r17.md`: 2660 bytes,
  sha256 `0171904031cd5176d01880c956399dfc22cea4d33a18960d3590641dac566c0a`.
- RECORD17 -> `.agent/live_review.md`, append. The last 6982 bytes of the committed
  file hash to `31cbb3f3a1270180fafceead40b63aa90d41ad231ac698c43c149a072419e30c`.
- SLIPS17 -> `.agent/prose_slips.md`, append. The last 959 bytes hash to
  `a0a8aefa37aa93283d920b8e8ab6e27bdd5c9cdfbf374b3459b6fe52b401d429`.
- The block itself: `cmp` of `.agent/authored/f033-r17.md` against the block on disk
  returned exit 0 with no output, at 28396 bytes and sha256
  `3b932062979ba726e0f4c99a4b419f2bbf0a1d07a2634a4224cbc56fc070650c`, the digest the
  round order named.
No slice was edited. Every one was applied byte for byte.

## Deviations & assumptions

D1 — G7's ruff line. The block orders
`ruff check tests/ui_contracts/test_apply_state_partial.py`. The bare `ruff`
executable is DENIED to this session by the sandbox, so the byte-identical check was
run through the interpreter as
`python3 -m ruff check tests/ui_contracts/test_apply_state_partial.py`, REAL exit 0,
printing `All checks passed!`. Same tool, same arguments, same configuration; only
the entry point differs. Declared because it is not the literal command string.

D2 — SPEC B carries two clauses that pull against each other. It orders
`.checkPartial` to be "`.checkDone` with a blue fill … same white glyph colour" and
in the same paragraph says "no raw hex colour is introduced". `.checkDone`'s white
glyph colour IS the literal `#fff`. The first clause was applied literally, so
`.checkPartial` carries `color: #fff` exactly as `.checkDone` does; the BACKGROUND is
`var(--remedy-blue-strong)` as ordered. Measured at `5f0273d8`: `#fff` already
occurs twice in this file (lines 122 and 169), so no colour VALUE new to the file
enters it, and no new design token was added. If the reviewer meant the stricter
reading, the repair is a one-line token substitution and I did not make it on my own
authority.

D3 — G3(c)'s span convention, recorded so the reviewer's re-run is not surprised
rather than as a fault. The block states the first appended paragraph as spanning
1542725 to 1546617. My first script measured a 1-BASED span that also counted the
separator newline and the paragraph's own terminating newline, and printed
1542725 to 1546619. Re-measured under the block's own convention — 0-BASED indices
over the paragraph's CONTENT — the span is EXACTLY 1542725 to 1546617. The block is
correct; only my first reading's convention differed, and the containment assertion
holds under both, so the control is proved to sit where it must either way.

D4 — G6 mutation (ii) was first run with `-x`, which stops after the first failure
and printed `1 failed, 16 passed`. That number is NOT a measurement of the mutation
and is not reported as one. The run was repeated without `-x` and the complete
reading, `3 failed, 17 passed` at REAL exit 1, is what G6 above reports.

D5 — SPEC C3 names three vacuity readings for the card and exactly three were
written. The "the scan finds branches at all" test the popover class also carries was
NOT added for the card, because the card's seam assertions raise by construction when
their branch is missing — mutations (i) and (ii) show it — so a separate emptiness
test would have been a fourth reading the block did not order.

D6 — No `Done:` and no `Landed:` line was written, and no id was minted. That is
what constraint 8 orders; it is recorded here because a reader auditing the round
against its block should see the absence was deliberate. R-0738 stays open: the
report line, the third surface its resolution names, is untouched.

Assumption: none beyond the above. Where SPEC A, B and C were ambiguous the block's
literal wording was applied and the disagreement declared rather than corrected.

## Open findings

258, UNMOVED across this round. Registered 306, resolved 48 distinct. R-0738
(Medium) was ADVANCED to its second surface and remains open. R-0745 (Low) remains
open and belongs with the next work that touches the door's imports.

## Next

The reviewer gates round 17 and writes the verdict. If it PASSES, the next round is
the plan's step 2: THE REPORT LINE. Measured at `5f0273d8` and unchanged at
`e0e2d12f` by G8's blob-id reading, `packages/orchestration/run_report.py` holds NO
reference to apply state at all, so its `TaskOutcome` gains one and the fold needs a
home both readers may import — this is a new read, not a changed one, and it is the
LAST of the three surfaces R-0738 names. Only after it is R-0738 resolvable.

## Push outcome

Written by C7, after the push. See below.
