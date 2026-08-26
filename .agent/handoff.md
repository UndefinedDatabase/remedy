# Handback — F031 Decision inbox, R27

Feature F031, round R27, branch `feature/f031-decision-inbox`, base
`beec7b83cb51bf4a34db82f3bb029623e14433f6`. Commits C0a `cdf40849`, C0b
`ce374ca6`, C1 `a81a04ae`, C2 `7b601083`, C3 `2e06cd62`, C4 this commit.

Fortschritt: ~92 % (F031 claimed; R1 through R26 landed, R26 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer-command model
             shipped, deep-link seam here, sender and forms open)
             — Schaetzung

## Range
Review of `beec7b83`..HEAD, HEAD being C4, the commit that writes this file.

## Commits
`+/-` is `git diff --numstat`; it agrees cell for cell with `git diff --shortstat`.

### cdf40849 docs(agent): save the F031 R27 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f031-r27.md` | +449/-0 | C0a: copied from the scratchpad, never retyped |

### ce374ca6 docs(agent): mirror the F031 R27 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +245/-244 | C0b: byte-identical mirror of the C0a blob |

### a81a04ae docs(agent): point the F031 plan at R27
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +24/-24 | C1: whole-file replacement by slice PLANF031R27 |

### 7b601083 docs(agent): record the F031 R26 verdict and R-0377's recurrence
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C2: append of slice LEDGER27, nothing else |

### 2e06cd62 feat(ui): resolve a decision card to the task's graph node
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/decisionCard.ts` | +26/-4 | S1: `taskId` field, its projection, falsified sentence retired |
| `apps/ui/src/api/decisionCard.test.ts` | +26/-1 | S3(a): 4 new tests; both whole-model `toEqual` gained `taskId` |
| `apps/ui/src/api/decisionFocus.ts` | +35/-0 | S2: `nodeIdForDecisionCard`, NEW |
| `apps/ui/src/api/decisionFocus.test.ts` | +61/-0 | S3(b): 7 tests, NEW |
| `.agent/decisions.md` | +34/-0 | S4: DECISION F031 D12 |

### C4 (this commit) docs(agent): write the F031 R27 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C4: this file; a handback cannot table its own SHA (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| S1 | done | |
| S2 | done | |
| S3 | deviated | (a)'s full-card fixture also gained `task_id`; Deviation 2 |
| S4 | done | |
| push (G9) | done | ordered after C4; outcome carried by G9 to the reviewer |

## External actions
`git worktree add --detach .remedy-wt/f031-r27-red 2e06cd62` — created at a path that
did not exist; removed BY THAT EXACT PATH with `git worktree remove`.
`git push origin feature/f031-decision-inbox` — ordered by G9, run after C4. THAT
PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures
the pushed tips at the next gate and records them in the R27 entry of
`.agent/live_review.md`. No PR created, no branch deleted, nothing merged.

## Verification
G1 branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` ABSENT on disk
before C0a and again before C4; `git status --porcelain` 0 after each of C0a, C0b,
C1, C2, C3. Four readings — scratchpad, C0a blob, C0b blob, `.agent/last_block.md`
on disk — ALL FOUR EQUAL at sha256
`3f31a05d2e5969ba0dfca086ef1255350fa326baad80041a623936ee10d82fda`, 38339 bytes,
449 lines; C0a and C0b are the SAME blob `b723f36ca5a27ba8b1ee76d27baf5f68d6c198d9`.
G2 extractor over the COMMITTED C0a blob: 2 slices, 50 CONTENT lines, 449 TOTAL,
PROSE 399 — under both caps, 400 PROSE (F085 D5) and 490 TOTAL (F085 D6).
G3 `.agent/plan.md` at `a81a04ae` byte-equal to PLANF031R27 TRUE under the
newline-INCLUDED convention, 2781 bytes slice and 2781 file; the negative control
against the slice MINUS its trailing newline FALSE; `^## Goal$` 1,
`^## Next Steps$` 1, `wc -l` 47, strictly under 50.
G4 whole-file equality in the shape constraint 8 states: TRUE, 696400 + 1 + 8741 =
705142 against an actual 705142. Second, independent reader: a blank-line split
moves the unit count 313 → 315 and its LAST 2 units equal LEDGER27's 2 paragraphs
IN ORDER, trailing newlines rstripped on BOTH sides. Negative control run in memory,
never on the tracked file — one byte flipped at offset 696601, inside the appended
text: both readers REJECT the mutant and both ACCEPT the true file.
G5 base `beec7b83` → C2 `7b601083`: `^- R-\d+ — ` 244 → 244, ids ADDED and ids
REMOVED BOTH the EMPTY SET, all DISTINCT, maximum `R-0683`; `^Done: R-\d+ — ` 5 → 5
with ids ADDED the EMPTY SET; `^Landed: R-` 0 → 0; `^Recurrence: R-` 19 → 20 and
`^Recurrence: R-0377` 0 → 1; `^Gate: R\d+ — ` 19 → 19 UNCHANGED; `^Gate: F\d+ R\d+ — `
7 → 8, the ADDED key exactly `F031 R26`, all keys DISTINCT. §3 item 10 open set 239
at `7b601083`; `- R-0377 — ` line-anchored exactly 1, so its landed paragraph was
not edited; `git diff --name-only` over C3 names 5 paths and NOT
`.agent/live_review.md`.
G6 disposable worktree `.remedy-wt/f031-r27-red`, path did not exist, detached at
`2e06cd62`. UNMUTATED, from the PRIMARY checkout's `apps/ui`: `npx vitest run
--config <PRIMARY>/apps/ui/vitest.config.ts --root <WT>/apps/ui src/api/` gave REAL
exit 0 at 22 files and 360 tests. With the resolver mutated INSIDE that worktree to
return `decision.taskId` instead of `owner.nodeId` — one occurrence, every other
byte alone — the same line gave REAL exit 1 at 3 failed and 357 passed, the three
being `resolves a decision to the node of the task it is about`, `reads the task id
rather than the decision's own id` and `answers the task's nodeId and never the task
id it matched on`. The file was restored byte-identically inside the worktree, that
worktree's `git status --porcelain` 0, and the worktree removed BY THAT EXACT PATH;
`git worktree list` 1 line after, naming `/home/decodeux/Repos/remedy` only.
G7 structure at C3: `decisionFocus.ts` carries the import line `import type {
FocusableTask } from "./feedFocus";` and declares 0 types of that name; `fetch(` 0,
`Date.now` 0, `useState` 0. In `decisionCard.ts` the string `absent everywhere is
ANSWERING` occurs 0 times and `taskId` appears in the `DecisionCardModel` interface
exactly 1 time. `git worktree list` 1 line immediately BEFORE the first suite.
Suites run SERIALLY, never two alive at once, every one a REAL exit 0:
`npm run typecheck` exit 0 with ZERO diagnostics on stdout and stderr;
`npm run test:unit` exit 0 at 25 files and 385 tests — the FILE count exactly 1 more
than the Base's 24, that one being `decisionFocus.test.ts` — with
`decisionAnswer.test.ts` 17, `decisionFilter.test.ts` 20 and `decisionOrder.test.ts`
16 all UNMOVED, `decisionCard.test.ts` 36 against the Base's 32 so S3(a) added 4,
and the new file's own count 7. Then `tests/ui_server/` 480, `test_test_runner` 52,
`test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525
passed with 4 skipped, and `test_golden_path` 42 — every count identical to the
Base's reading, so there is no difference to account for.
G8 line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1,
`.agent/live_review.md` at C2 and all five files C3 writes, against a CONTROL of 2
and 2 over the COMMITTED C0a blob. `beec7b83..2e06cd62` names 9 paths, none under
`docs/`, `packages/` or `tests/`, none of the forbidden set and no inventory file;
the range MINUS the change set is EMPTY and the change set MINUS the range is
exactly `.agent/handoff.md`. Per commit C0a..C3: single-parent TRUE for all five,
insertions 449, 245, 24, 4 and 182, each under the 500 cap (F104 D1), and those
numstat numbers agree cell for cell with `git diff --shortstat`.
`git ls-files .remedy-wt` 0 and `git ls-files` over `*.zip` 0. Reflog SCOPED to THIS
ROUND'S 5 entries, FIELD the operation prefix before the first colon of
`git reflog --format=%gs`: all 5 are `commit`, so `amend` 0, `rebase` 0, `cherry` 0.
SHA-shaped tokens in the COMMITTED C0a blob under the word-bounded 7-to-40-hex
pattern: 21 occurrences, 10 distinct, 9 `commit` and 1 `blob`, FAILING SET EMPTY.
G9 push ordered after C4; see `## External actions`.

## Authored-text proofs
PLANF031R27 and LEDGER27 were extracted PROGRAMMATICALLY from the COMMITTED C0a blob
by their marker LINES, and no marker line reached a target file (G8). The block
states no digest of itself, so fidelity is G1's disk-to-disk comparison over four
readings, all four EQUAL. The digest measured here is
`3f31a05d2e5969ba0dfca086ef1255350fa326baad80041a623936ee10d82fda`.

## Findings
Open set 239, measured at C2 `7b601083` by the §3 item 10 rule — every
`^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — unchanged from the base
`beec7b83`. This round minted no id and resolved none; R-0377 gained a recurrence
and stays OPEN. The narrower set, the findings THIS FEATURE MUST STILL ACT ON, is
the 23 ids `.agent/plan.md` names at `a81a04ae`; R-0495 and R-0574 are the two Highs.

## Deviations & assumptions
1. COMMIT SEQUENCE: no departure. C0a, C0b, C1, C2, C3, C4 exactly — none extra,
   none dropped, none reordered. Constraint 11 held: nothing was wired, no
   component was edited, and the resolver has no caller yet.
2. S3(a), DEVIATION: beyond the two whole-model `toEqual` assertions gaining
   `taskId`, the full-card FIXTURE feeding the first of them gained
   `task_id: "T-7"`, so that assertion pins a NON-EMPTY id; minimal compliance
   would have made a test named "flattens a full card" assert that a full card has
   no task. The second assertion, over `buildDecisionCardModel({})`, gained
   `taskId: ""` with no fixture change.
3. BLOCK CONTRADICTION, declared and NOT silently fixed: S3(a) says "S1's own edit
   to the same file moves them" of lines 164 and 188. S1 edits `decisionCard.ts`,
   not `decisionCard.test.ts`, so nothing moved them; both were re-grepped before
   editing and both were still at 164 and 188.
4. S1, SCOPE NOTE: the falsified sentence begins mid-line — the preceding comment
   line ended "What is still genuinely" — so retiring it also rewrote that line's
   tail. That is the ordered sentence rewrite, not a second edit. A private
   `payloadTaskId` reader was added beside the existing `payloadOptions` per
   constraint 2's "prefer the idiom the neighbouring module already uses"; no other
   field of the model changed.
5. G6: the mutant produced 3 failing tests, reported rather than compared, since
   the block states no number. ASSUMPTION: `<PRIMARY>` and `<WT>` in G6's command
   line resolve to `/home/decodeux/Repos/remedy` and `.remedy-wt/f031-r27-red`
   under it.
6. HANDBACK CAP, DECISION D15 stated-cause overage: the tier is 100 lines, resolved
   from AGENTS.md `### handoff.md` against the 6 commits constraint 4 fixes — more
   than 5, so the 100-line tier rather than the 60. This file is 196 lines.
   The mandated content behind the overage is the per-commit changed-files tables
   for 6 commits, the 11-row item-status table, the one-line-per-gate record for 9
   gates, the four-reading transport proof, and the finding counts with their rule
   and commit. No section was dropped and no token cap is claimed.

## Next
1. The next session reads `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the
   Open PR Gate as rule 2.
2. The R27 verdict is UNRECORDED and is owed by the next round's ledger commit
   (DECISION F085 D9).
3. T003's SENDER round needs the token-delivery ruling the plan's Next Steps names —
   the browser holds no bearer token and no `X-Remedy-CSRF` value today — before any
   wiring is written.
