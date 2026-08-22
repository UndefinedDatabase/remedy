# F021 R38 handback — the integration gate and the acceptance read

Fortschritt: 100 % der Bauarbeit; das Integrations-Gate ist gelaufen, Evidenz-
             Runde und STATUS-Runde stehen noch aus — Schaetzung

## Range
Review of 24a6b899975ea849700c21a3d6a73f45a14f2873..HEAD — round base `24a6b899`,
branch `feature/f021-live-activity-feed`. Open findings 223, by
`planner_reviewer_prompt.md` §3 item 10 — canonical `^- R-\d+ — ` 224 minus
`^Done: R-` 1 — measured at C2 `dee2e6d8`. No id minted, none resolved. NO
BLOCKER: the branch-only failure set is empty and no clause is UNSATISFIED.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a `a5b6cdb0` | done | |
| C0b `11c20d0f` | done | |
| C1 `94d4b0b2` | done | |
| C2 `dee2e6d8` | done | |
| C3 `fa3e29f7` | done | |
| C4 `af5bac0a` | done | |
| C5 (this file) | done | its own SHA and insertions are unnameable from inside it |

## Commits

### a5b6cdb0 chore(agent): save the F021 R38 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r38.md | +243/-0 | the block saved byte for byte (C0a) |

### 11c20d0f chore(agent): mirror the R38 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +186/-111 | written FROM the committed C0a blob (C0b) |

### 94d4b0b2 docs(state): point the F021 plan at R38, the integration-gate round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-14 | PLANF021R38 whole-file write (C1) |

### dee2e6d8 docs(review): record the R37 PASS in the ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | RECORD38 appended, ONE blank line at the join (C2) |

### fa3e29f7 docs(state): record the F021 integration-gate evidence for R38
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f021_r38/ | +222/-0 | 11 files under that dir, the gate readings (C3) |

### af5bac0a docs(state): read the F021 acceptance criteria clause by clause at R38
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f021_r38/acceptance_read.md | +84/-0 | 18 clauses, one row each (C4) |

### C5 docs(state): hand back F021 R38 — SHA unnameable: this is the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to the next round | the handback itself (C5) |

Every `+/-` cell above is the `git diff --numstat` reading and equals the number
the G7 line reports, compared cell by cell (block constraint 12).

## External actions
`git worktree add -b tmp/f021-r38-base .remedy-wt/base-gate-f021-r38 4548995d`
then `git worktree remove --force` (the copied `node_modules` makes the tree
dirty), `git worktree prune`, `git branch -D tmp/f021-r38-base` — deleted,
proved by `git worktree list` (1 entry) and `git branch --list 'tmp/*'` (0
lines). `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
exit 0, output `[]`; no `gh pr create`, no `gh pr merge`. `git push -u origin
feature/f021-live-activity-feed` after C5.

## Verification — one line per gate, transcripts in `.agent/gate_f021_r38/`
G1 `.agent/STOP` ABSENT before C0a and again before C5; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
G2 sha256 `42def0677ea427b885a201c86285b3d1b24e0eb5d9680d0bf9347e1f8d3ff37c`, 19303 bytes, 243 lines — EQUAL over the bytes I read, `.remedy-wt/f021-r38.md`, `.agent/authored/f021-r38.md` at C0a and `.agent/last_block.md` at C0b. My extractor printed 2 whole texts, 43 CONTENT lines and 4 marker lines; TOTAL 243 against 490 and PROSE 200 against 400, re-measured from the committed C0a blob, both equal to constraint 11.
G3 `cmp` plan.md vs PLANF021R38 + one newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1 (`EOF … after byte 2402, in line 42`); last byte `0xa`; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 42, under 50.
G4 canonical `^- R-\d+ — ` 224→224, ALL DISTINCT at both, max R-0661 at both; loose `^- R-` 225→225, gap 1 at both; `^Done: R-` 1→1; `^Gate: R` 36→37, DISTINCT at both; `^Gate: R38` 0→1; `^Recurrence: ` 14→14. RECORD38 paragraphs opening with the bytes `- R-`: 0 of 1. Base blob a byte-exact PREFIX of the C2 blob; remainder EXACTLY one newline + RECORD38 + one newline, 3072 bytes.
G5 BRANCH exit 0, 17651 passed, 20 skipped, 0 FAILED, 160.9 s. BASE at merge base `4548995de3e46dc5304d3584dc249262d54edac9` exit 0, 17572 passed, 20 skipped, 0 FAILED, 160.1 s. `comm -13` 0 ids (list EMPTY), `comm -23` 0 ids (list EMPTY), so nothing to re-run or attribute; both sets red-controlled. Canary `tests/cli/test_golden_path.py` exit 0, 42 passed, serial, primary checkout. PARITY BY THE BUILD ROUTE: `copytree(symlinks=True)`, `.bin` 23 entries / 23 symlinks in BOTH copy and primary; `npm run build` in the base worktree exit 0, 962 modules. Both runs under 5 min, no perf note owed. See deviation 2 for the mtime reading.
G6 18 clauses — 10 Goal & Done, 8 Acceptance. SATISFIED 17, SATISFIED-WITHOUT-A-TEST 1 (GD8, the binding CSS: nothing here renders CSS), UNSATISFIED 0. Node ids from `--collect-only -q`, 17671 collected; see deviation 1 for the five vitest-pinned clauses.
G7 `git diff --name-only 24a6b899..HEAD` I COUNT SIXTEEN paths at C4, every one either `.agent/authored/f021-r38.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md` or under `.agent/gate_f021_r38/`; NO path outside those classes, and none under `apps/`, `packages/`, `tests/` or `docs/`. 6 commits at C4, 7 at C5 — as many as `Bundle:` names — every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell on all six measurable commits; insertions 243, 186, 12, 2, 222 and 84, each under 500, C5's own left to the next round. Marker sweep LINE-ANCHORED 0 for each of `<<<SLICE ` and `<<<END ` over `.agent/plan.md` and `.agent/live_review.md`. Reflog BY OPERATION: all six rows `commit`, with `amend`, `rebase` and `cherry` 0 each in that field. `gh pr list --state open` printed `[]`.

## Authored-text proofs
Both texts were extracted BY MARKER LINE from the COMMITTED C0a blob
`a5b6cdb0:.agent/authored/f021-r38.md`, never retyped. `plan.md`: `cmp` exit 0
against PLANF021R38 plus one newline, exit 1 against the bare slice.
`live_review.md`: the base blob is a byte-exact PREFIX and the remainder is
EXACTLY one newline plus RECORD38 plus one terminator.

## Deviations & assumptions
1. G6 orders every SATISFIED node id from `pytest --collect-only -q`. Five
   clauses (GD3, GD6, A2, A3, A5) are pinned ONLY by vitest, whose ids that
   command cannot produce. I took them from `npm run test:unit --
   --reporter=json` (exit 0, 218 tests, 218 passed) and prefixed them
   `vitest:`. That run is also a command the block did not order.
2. THE PARITY CLAIM IS VOID BY THE BLOCK'S OWN RULE. All 3 files under the base
   worktree's `apps/ui/dist` moved their mtime INSIDE the base run window
   (1787436366.861, ~74 s in) while all 3 sha256 digests stayed EQUAL: a
   byte-identical rebuild, so `REMEDY_UI_NO_AUTO_BUILD=1` did not prevent the
   EVENT. Nothing turns on it here — attribution is unconditional and both
   `comm` sets are empty — but it is the R-0169/R-0444 class recurring.
3. TWO RED CONTROLS the block did not order, added because two EMPTY readings
   are worthless unpaired: a 2-test module run OUTSIDE the repo proved the
   `^FAILED` extractor finds a real failure (exit 1, 1 failed 1 passed), and a
   synthetic pair proved `comm -13`/`comm -23` each report 1 id.
4. No departure from the ordered commit sequence: exactly C0a, C0b, C1, C2, C3,
   C4, C5 — none extra, dropped or reordered. No product file touched, no
   finding id minted or resolved, no formatter or linter run, `npm run lint`
   NOT run, no PR created or merged, exactly ONE worktree, never two pytest
   processes at once.
5. DECISION D15, size: this handback measures 143 lines against the ≤100-line
   tier its seven commits earn. Mandated cause: seven commit tables, the
   item-status table,
   seven gate lines carrying the integration gate's two suite figures and both
   `comm` sets, the authored-text section, and the five reported-not-minted
   findings constraint 3 requires the handback to carry. No section is dropped
   and no transcript is restated here.

## Reported, NOT minted — the next round's to mint (constraint 3)
1. THE COPY ROUTE IS THE TRAP, AND THE NUMBER IS 78 vs 0. The reviewer measured
   78 base-only failures at `24a6b899` by copying `apps/ui/dist`. The BUILD
   route measured 0. `docs/agents/integration_gate.md` step 3 still names
   `apps/ui/dist` among the artifacts to COPY — that wording produces the 78.
2. `REMEDY_UI_NO_AUTO_BUILD=1` did not prevent the rebuild event (deviation 2).
3. GD8: `.activityItem { gap: 12px }` against T5_F021's binding `gap:10px`, and
   the row's `padding:9px 14px` plus `font:` shorthand live on child selectors
   rather than on the row. Spec deviation or CSS-module realization is a
   reviewer's call.
4. Nothing asserts that `ActivityFeedCard` renders the seq; GD3 is pinned at the
   data level only.
5. Nothing asserts that `RemedyShell` hands the SAME `onSelectNode` to the graph
   and to the feed panel, which is what makes GD9 true.

## Next
THE INTEGRATION GATE IS RUN AND THE ACCEPTANCE CRITERIA ARE READ. The next
action is the EVIDENCE round, then the STATUS-commit round
(`docs/roadmap/STATUS_closure_protocol.md`; the two are never one round), then
the pull request, opened at closure and merged only at the Open PR Gate. R38's
own verdict is recorded by the NEXT round's ledger entry (§3 item 31): C2
preceded every gate this round ran. The next session's FIRST action is Phase 1
rule 1 of `docs/agents/self_drive_protocol.md` — re-reading `.agent/STOP` from
disk — BEFORE rule 2. Owed to the next round, because C5 cannot state them about
itself: C5's SHA, C5's insertion count and the `git status --porcelain` reading
after C5.
