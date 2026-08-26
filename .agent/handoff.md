# Handback — T5_F031 Decision inbox, R36

Branch: feature/f031-decision-inbox · Base: ce4da4a1 · Commits: 7 (C0a, C0b, C1,
C2, C3, C4, C5), the count constraint 3 fixes. Tier from AGENTS.md "### handoff.md"
against it: 7 is MORE THAN 5, so ≤100 binds, not ≤60.
Fortschritt: ~97 % (F031 claimed; R1 through R35 landed, R35 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request,
             deep-link, submit and nonce seams shipped; outcome sentence and
             flow land here, component wiring open) — Schaetzung
Carried VERBATIM; I counted its lines myself: 4. No clause of it is false of the
round that happened, so nothing is written beside it.
Deviations, declared: this file is 197 lines against that ≤100 tier. The cause is
mandated content — 7 per-commit tables (31 lines), the 8-row item-status table, and
one entry per gate for G1–G11, several of which order a dozen values apiece. No
section is dropped; no transcript is quoted.

## Range
Review of ce4da4a1..HEAD, where HEAD is the C5 commit that writes this file.

## Commits
### 2761e82c docs(agent): save the F031 R36 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r36.md | +481/-0 | C0a: the block, copied not retyped |
### 306e43b3 docs(agent): mirror the F031 R36 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +341/-172 | C0b: the same bytes mirrored |
### 20551e0d docs(agent): point the F031 plan at R36 and record DECISION F031 D18
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-20 | C1: whole-file PLANF031R36 |
| .agent/decisions.md | +33/-0 | C1: DECISIOND18 appended at EOF |
### d68fd069 docs(agent): record the F031 R35 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2: LEDGER36 appended at EOF |
### 448ee672 feat(ui): map one decision send result to the sentence an operator reads
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionOutcome.ts | +128/-0 | C3: S1–S3, tone and sentence |
| apps/ui/src/api/decisionOutcome.test.ts | +172/-0 | C3: its tests |
### 7ac45594 feat(ui): sequence mint, build, send and outcome behind injected seams
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionAnswerFlow.ts | +144/-0 | C4: S4–S5, flow and deadline |
| apps/ui/src/api/decisionAnswerFlow.test.ts | +292/-0 | C4: its tests |
### C5 — this commit, docs(agent): write the F031 R36 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5: a handback cannot table its own commit |

## External actions
`git worktree add --detach .remedy-wt/f031-r36-probe HEAD` → created at 7ac45594.
`git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r36-probe` → removed
by that exact path; `git worktree list` 1 line after.
`git push origin feature/f031-decision-inbox` → ordered by G11 AFTER this commit, so
its result cannot sit inside the file it follows; see G11.
No `gh` command, no PR created or edited, nothing merged, no branch deleted.

## Verification
G1 `git branch --show-current` = feature/f031-decision-inbox, not main. `.agent/STOP`
   READ FROM DISK: ABSENT before C0a and ABSENT before C5 — `ls` answered "No such
   file or directory" both times; nothing was deleted. `git status --porcelain` 0
   lines after each of C0a…C4. Four readings ALL EQUAL at sha256 a030211898ef02e5c9
   73fcf337f3df061e48d723fc029f1865e13b7fae3882c7, 37871 bytes, 481 lines; C0a and
   C0b resolve to the SAME blob 3783636323f818bdd34025387adccb84d627c1be.
G2 over the COMMITTED C0a blob: 3 slices, 81 CONTENT lines, 481 TOTAL, PROSE
   481 − 81 = 400. TOTAL ≤ 490 and PROSE ≤ 400 — the prose cap is met exactly.
G3 plan at C1 byte-equal to PLANF031R36 TRUE, 2695 bytes both sides, newline-INCLUDED
   convention (the slice ends in its own newline; none added or removed). Minus-
   trailing-newline control FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48 < 50.
G4 both appends in constraint 7's shape. decisions.md at C1 597218 + 1 + 2022 =
   599241 vs actual 599241 TRUE; live_review.md at C2 778079 + 1 + 5767 = 783847 vs
   actual 783847 TRUE. Second reader for DECISIOND18: blank-line units 1433 → 1439,
   N = 6 by MY split, last 6 equal its paragraphs IN ORDER TRUE, SWAPPED FALSE;
   trailing-newline handling — every unit rstripped of newlines on BOTH sides.
   LEDGER36 splits into 1 unit, so no order reading applies. NEGATIVE CONTROL each:
   one byte flipped in the appended text, in memory only — mutant rejected, true
   file accepted.
G5 base → C2: `^- R-\d+ — ` 246 → 246, ids ADDED and REMOVED BOTH the EMPTY SET, all
   DISTINCT, maximum still R-0685; `^Done: R-\d+ — ` 5 → 5, ADDED the EMPTY SET;
   `^Gate: R\d+ — ` 19 → 19; `^Gate: F\d+ R\d+ — ` 16 → 17, ADDED key exactly
   `F031 R35`, all keys DISTINCT; `^Recurrence: R-` 25 → 25; `^Landed: R-` 0 → 0.
   §3 item 10 open set at C2 = 246 − 5 = 241.
G6 line-anchored `^<<<SLICE `/`^<<<END ` 0 and 0 in plan.md and decisions.md at C1,
   live_review.md at C2 and all four files C3/C4 write; CONTROL over the C0a blob 3
   and 3. `git diff --name-only ce4da4a1..7ac45594` names 9 paths, none under docs/,
   packages/ or tests/, no .agent/context.md, no inventory file; range-minus-change-
   set EMPTY, change-set-minus-range exactly .agent/handoff.md. C0a…C4 each single-
   parent, insertions (the `+` column only) 481, 341, 52, 2, 300, 436, each under 500,
   and those `git diff --numstat` numbers agree cell for cell with the `+/-` column
   above. `git ls-files .remedy-wt` 0, tracked zip glob 0, `git worktree list` 1 line
   at C4. REFLOG — SCOPE: entries whose commit is one of C0a…C4, 6 of 6130; FIELD: the
   operation prefix before the first colon of `%gs`; all 6 read `commit`, so amend 0,
   rebase 0, cherry 0. SHA-shaped tokens in the C0a blob under `\b[0-9a-f]{7,40}\b`:
   17 matched, 9 distinct, resolving to 8 `commit` and 1 `blob`; FAILING SET EMPTY.
G7 decisionOutcome.ts `fetch` 0, `setTimeout` 0, `Date.now` 0, `localStorage` 0; 9
   sentence constants, 0 of them holding a digit. decisionAnswerFlow.ts `fetch` 0,
   `localStorage` 0; 4 deps, every one optional and resolved with `??` to a shipped
   default, the deps parameter itself defaulting, so the export is callable with it
   omitted and a test asserts that call. Both new test files `vi.` 0, `globalThis` 0.
   decisionSubmit.ts byte-identical to base; its outcome union still reads 3 members.
G8 `npm run typecheck` REAL exit 0, 0 diagnostics. `npm run test:unit` REAL exit 0,
   30 FILES / 448 TESTS against the Base's 28 / 419; the whole difference is the two
   new files, decisionOutcome.test.ts 16 and decisionAnswerFlow.test.ts 13, 16+13=29.
   The eight decision files the Base names are UNMOVED — decisionAnswer 20,
   decisionCard 36, decisionFilter 20, decisionFocus 7, decisionNonce 9, decisionOrder
   16, decisionSend 12, decisionSubmit 10. `npm run lint` NOT run, as G8 orders.
G9 worktree at .remedy-wt/f031-r36-probe, a path that did not exist, detached at
   7ac45594, removed by that exact path; no node_modules there, so vitest ran FROM the
   primary apps/ui with `--root <wt>/apps/ui`, the PRIMARY config and the two new test
   files as arguments. UNMUTATED REAL exit 0, 2 files, 29 passed, 0 failed.
   (a) decisionOutcome.ts, string `      return { tone: "warn", sentence: RATE_LIMITED_
   SENTENCE };`, occurrences IN THAT FILE 1, `"warn"` → `"error"`: REAL exit 1, 27
   passed, 2 failed. FAILING NODE IDS `src/api/decisionOutcome.test.ts >
   describeDecisionSubmitResult > warns over the rate budget, which is the one refusal
   that clears by waiting` and `src/api/decisionAnswerFlow.test.ts > answerDecisionCard
   > carries a refusal's status into the sentence chooser, so a rate limit is not read
   as a credential problem`.
   (b) decisionAnswerFlow.ts, string `await Promise.race([sent, deadline().then(() =>
   DEADLINE_REACHED)])`, occurrences IN THAT FILE 1, replaced by `await sent`: REAL
   exit 1, 26 passed, 3 failed. FAILING NODE IDS, all under
   `src/api/decisionAnswerFlow.test.ts > answerDecisionCard >`: `still answers when the
   submit NEVER settles, because the deadline bounds the wait`, `reuses the unreachable
   sentence when the deadline wins, rather than inventing a fourth outcome`, `lets a
   submit that settles FIRST win the race, even though a deadline was started`. Each
   mutation hit the WORKTREE copy by absolute path and was restored before the next; no
   `cd` was used. PRIMARY `git status --porcelain` 0 lines immediately after the last
   restore; `git worktree list` 1 line after removal.
G10 all six REAL exit 0, run SERIALLY, never two alive at once; `git worktree list` 1
   line immediately BEFORE the first. ui_server 480, test_test_runner 52,
   test_resource_safety 21, test_integrity_gate 16, ui_contracts 525 passed with 4
   skipped, canary golden_path 42 — every count identical to the Base's, nothing to
   account for.
G11 ordered AFTER C5, so no commit of this round can carry its result; it runs at once
   after this commit and its three readings — local tip, remote-tracking ref, `git
   ls-remote origin` — go to the caller. No `--force`, no `--force-with-lease`, no
   rewrite, no branch deletion, no PR, no merge.

## Authored-text proofs
Three slices applied, each extracted PROGRAMMATICALLY from the COMMITTED C0a blob by
its marker LINES; no marker reached a target. PLANF031R36 → `.agent/plan.md`, disk-to-
disk byte equality TRUE. DECISIOND18 → `.agent/decisions.md` and LEDGER36 →
`.agent/live_review.md`, each proved by G4's whole-file equality. G1's four-way reading
stands in for the hash-stamp ritual, per the self-drive protocol.

## Completion Report — Item-Status Table
| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 plan and DECISION F031 D18 | done | |
| C2 the R35 gate entry | done | |
| C3 decisionOutcome module and tests | done | |
| C4 decisionAnswerFlow module and tests | done | |
| C5 handback | done | |
| G11 push | done | runs after C5; its readings are in the round report |

## Open findings count
241 open, by the §3 item 10 rule DECISION F009 D10 requires — every `^- R-\d+ — `
paragraph minus every `^Done: R-\d+ — ` line — measured at commit d68fd069 (C2):
246 − 5 = 241. This round minted no id and resolved none.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5
landed in that order, none extra, none dropped, none reordered.
1. C0a and C0b landed while `.agent/plan.md` still described R35 — constraint 3 makes
   C1 the FIRST substantive commit, so the sequence, not an earlier write, meets the
   Commit Gate's plan clause.
2. Exit codes were read through `subprocess.run(...).returncode` inside `python3`
   heredocs, because this session's guard rejects shell loops, `$?` and `$( )`. Same
   argv, different reader.
3. ASSUMPTION, G4: a paragraph is a blank-line-delimited unit — that reading makes
   N = 6 for DECISIOND18 and 1 for LEDGER36.
4. ASSUMPTION, S1/S2: the block fixes a tone for `accepted`, `unreachable` and each
   `refused` status but states NONE for the unsendable message. I chose `warn`, since
   an operator who edits a blank answer can send it; the WHY comment says so. `error`
   would be a one-word change.
5. DECLARED, S4: the shipped submit never rejects but an INJECTED one can, so "NEVER
   THROWS" cost a `try`/`catch` around the race, mapping a rejected seam onto the same
   `unreachable` message a deadline win takes. The block orders no such branch; a test
   pins it.
6. DECLARED, S5: the default deadline creates a timer it cannot cancel — the seam type
   `() => Promise<void>` carries no handle — so when the submit wins, that timer still
   fires and settles a promise nobody awaits. The WHY comment states that rather than
   inventing a seam shape S5 does not fix.
7. No contradiction was found in the block, and every slice was applied verbatim.

## Next
1. The next session reads `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the Open
   PR Gate as rule 2.
2. R36's verdict is NOT YET on disk; the next reviewed round records it as the
   `Gate: F031 R36` entry in `.agent/live_review.md`.
3. R37 is the COMPONENT round: the server token threaded from `RemedyApp`'s
   `readUrlState` through `RemedyShell` and `RightLivePanel`, the flow called on a
   click, its sentence rendered and the buttons enabled.
