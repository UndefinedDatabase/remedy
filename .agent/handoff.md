# Handback — F031 Decision inbox, R11 — verdicts recorded, D4 and D5 ruled, T002 unblocked
Branch `feature/f031-decision-inbox`. Base `99d77d5cdf2b1ebee5cb25fd18e5258a0d20c131`, the R10 handback commit. Seven commits, no production code, every applied byte reviewer-authored.

The R11 block's `Fortschritt:` block, carried VERBATIM as ordered — all 5 of its lines, counted here because the block states no numeral for them:
Fortschritt: ~30 % (F031 claimed; R1 through R8 landed and gated ·
             R9 and R10 landed, their verdicts recorded by THIS
             round · T001 SHIPPED — the derivation module, the read
             endpoint and 29 tests are on disk and green · T002
             unblocked by D4 and D5 · T003 offen) — Schaetzung
It is TRUE at this commit: D4 and D5 exist in `.agent/decisions.md` at C3, so "T002 unblocked by D4 and D5" needs no correction, unlike at R10.

## Range
Review of `99d77d5c`..HEAD, HEAD being the C5 commit that writes this file.

## Commits
### 7d99fb2b chore(agent): save the F031 R11 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r11.md | +490 / -0 | C0a: the block saved verbatim, the extraction source for every slice |
### 4f7ea025 chore(agent): mirror the R11 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +367 / -252 | C0b: byte-identical mirror, written FROM the committed C0a blob |
### e391ed80 docs(state): the R11 plan, T002 unblocked by the two rulings
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21 / -21 | C1: PLANF031R11, whole-file replacement; first substantive commit per §3 item 23 |
### 37622435 docs(state): record the R9 and R10 round verdicts
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | C2: GATES910 appended; the two owed `Gate:` entries |
### 308b47d3 docs(state): rule DECISION F031 D4 and D5 to unblock T002
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +93 / -0 | C3: DECIS45 appended; the card-shell and test-layer rulings |
### 62a3a904 docs(roadmap): amend F031 with the R11 design rulings
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F031.md | +28 / -0 | C4: FEATAMEND appended; §4.7 routes a wrong spec as an amendment |
### C5 (this commit; SHA and numstat unknowable to the file that creates them — template R-0149 exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5: this handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | `7d99fb2b`; transport verified before and after |
| C0b | done | `4f7ea025`; same git blob id as C0a |
| C1 | done | `e391ed80`; PLANF031R11 byte-equal |
| C2 | done | `37622435`; keys `R9` and `R10` added, no id minted |
| C3 | done | `308b47d3`; `F031 D4` and `F031 D5` added |
| C4 | done | `62a3a904`; the R11 amendments section appended |
| C5 | done | this commit; its own SHA is not self-referable |
| push (G11) | deviated | ordered AFTER C5, so its outcome is a value of no file this round writes — G11 says so; command in `## External actions`, tips measured by the reviewer |

## External actions
`git push origin feature/f031-decision-inbox` — run after this commit, plain, with no force flag of any kind, no history rewrite, no branch deletion, no merge, no pull request, and no other `gh` command beyond one read-only `gh pr list --state open`, which returned `[]`. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R11 entry of `.agent/live_review.md`. No worktree was added or removed; `git worktree list` is 1 line throughout. Pre-existing `.remedy-wt/` scratch was neither edited nor deleted.

## Verification — one line per gate
G1 PASS — `git branch --show-current` prints `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk is ABSENT before C0a and again before C5; `git status --porcelain` is 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
G2 PASS — all FOUR readings equal at sha256 `8f7a61d3b41ed80f6f3b5c8454cd08af97bfbec501bf71bae271616519e1fe3e`, 40798 bytes, 490 lines: `.remedy-wt/f031-r11.md` before C0a, the committed C0a blob, the committed C0b blob, and `.agent/last_block.md` off disk after C0b; C0a's and C0b's file resolve to the SAME blob id `25af0eedce1fe354c0cab8cd3fd82856bf44a596`.
G3 PASS — my extractor over the COMMITTED C0a blob printed 4 slices, 171 CONTENT lines inside markers, 8 marker lines and 490 TOTAL lines.
G4 PASS — `.agent/plan.md` at C1 is byte-equal to PLANF031R11 under the newline-INCLUDED convention, slice 2894 bytes and file 2894 bytes; the NEGATIVE CONTROL against that slice with its trailing newline REMOVED is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
G5 PASS — the three appends each hold as ONE equality over the whole file in the shape constraint 7 states. Reader A TRUE for all three: 570870 + 1 + 11496 = 582367 for the ledger, 560571 + 1 + 6086 = 566658 for the decisions, 6705 + 1 + 1779 = 8485 for the feature file, each equal to that target's committed byte count. Reader B, one property applied to all three — split the committed file on a blank line after dropping its single trailing newline, take the LAST N units — gave units 285→287 with N=2 for the ledger, 1339→1352 with N=13 for the decisions and 14→18 with N=4 for the feature file, and in every case those last N units equal that slice's N paragraphs IN ORDER. NEGATIVE CONTROL per target: one byte flipped inside the FIRST paragraph the append added, at offsets 574538, 560643 and 6727 — BOTH readers REJECTED all three mutants and BOTH ACCEPTED all three true files.
G6 PASS — base→C2 in `.agent/live_review.md`: `^- R-\d+ — ` 240→240 all DISTINCT, ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, maximum `R-0679`→`R-0679`, `^Done: R-` 2→2, `^Recurrence: R-` 15→15 UNCHANGED, `^Gate: R\d+ — ` 9→11 gaining exactly the keys `R9` and `R10`, with `R19` and `R1` through `R8` still present; all 11 keys are DISTINCT, so the two added keys differ from each other and from every key already there.
G7 PASS — `.agent/decisions.md` at C3: `^## DECISION ` 129→131, the ids ADDED exactly `F031 D4` and `F031 D5`, `^## DECISION F031 D4` exactly 1 and `^## DECISION F031 D5` exactly 1; no line of the base blob changed — the base is a byte-exact PREFIX of the committed file, the same reading G5 takes.
G8 PASS — `docs/roadmap/features/T5_F031.md` at C4: `^## ` headings 9→10, the LAST now `## Design amendments (F031 R11, 2026-08-26)`, byte-equal to the line FEATAMEND opens with; `## Design amendments (F031 R5, 2026-08-23)` still present exactly once; line 1 `# T5_F031 — Decision inbox` and line 2 `**Tier 5 · Depends on: F009, F050, F051 · Blocks/used by: the central human queue**` BYTE-IDENTICAL to line 1 and line 2 at the base, and `tests/orchestration/test_roadmap_index.py` is 30 passed at the C4 tree under G10.
G9 PASS — `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `.agent/decisions.md` at C3 and the feature file at C4. `git diff --name-only 99d77d5c..62a3a904` names 6 paths: none under `packages/`, none under `apps/`, none under `tests/`, exactly ONE under `docs/`, and neither `.agent/f031_inventory.md` nor `.agent/f031_ui_inventory.md` nor either of the two protected roadmap files. The range path set MINUS the change set is EMPTY; the change set MINUS the range is exactly `.agent/handoff.md`. Per commit over C0a..C4, each single-parent, INSERTIONS from `git diff --numstat`: 490, 367, 21, 4, 93 and 28 — each under 500, and cell for cell what the `## Commits` table above carries (§3 item 28). `git ls-files .remedy-wt` 0, `git ls-files` over `*.zip` 0, `git worktree list` 1 line. REFLOG, with scope and field stated in the reading: over THIS ROUND'S 7 entries only — the branch checkout that opened it plus its 6 commits — read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, the prefixes are 6 `commit` and 1 `checkout`, so `amend` 0, `rebase` 0 and `cherry` 0.
G10 PASS — word-bounded `[0-9a-f]{7,40}` over the COMMITTED C0a blob: 23 occurrences over 9 DISTINCT tokens, each passed to `git cat-file -t`, giving `commit` for `000b1b63`, `21c3f15e`, `21c3f15e9246a88bf5ee0bea1936dac720a67ecc`, `6325ac2f`, `8d31351c`, `95610316`, `99d77d5c` and `99d77d5cdf2b1ebee5cb25fd18e5258a0d20c131`, and `blob` for `fc7e17798b211103f5262223d864e231eaf16f8b` — the FAILING SET IS EMPTY, as the block predicted, and it carried no positive control. `git worktree list` was 1 line immediately before the first pytest. The seven suites then ran SERIALLY in the PRIMARY checkout at the C4 tree, never two processes alive at once, each a REAL exit 0: `tests/docs/` 295 passed, `test_roadmap_index.py` 30, `tests/ui_server/` 474, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16 and `test_golden_path.py` 42 — cell for cell the reviewer's base readings, so there is no difference to account for.
G11 ORDERED AFTER C5 and therefore not yet run at this commit — command and carrier sentence in `## External actions`; the real outcome goes to the reviewer in the round report, per the gate's own wording.

## Findings
By §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 238, measured at C2 `37622435` from 240 paragraphs and 2 `Done:` lines. THIS ROUND MINTED NO FINDING ID and wrote no `Recurrence:` line: `^- R-\d+ — ` is 240 before and 240 after with maximum `R-0679` unchanged, and `^Recurrence: R-` is 15 before and 15 after. The findings THIS FEATURE MUST STILL ACT ON — a narrower set, never called "open" unqualified — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.

## Authored-text proofs
All four slices — PLANF031R11, GATES910, DECIS45 and FEATAMEND — were extracted PROGRAMMATICALLY from the COMMITTED C0a blob `.agent/authored/f031-r11.md` by their `<<<SLICE`/`<<<END` marker LINES, never retyped or rewrapped, and each was compared disk-to-disk against its target: PLANF031R11 byte-equal to the whole of `.agent/plan.md` at C1 (G4), and GATES910, DECIS45 and FEATAMEND each equal to their target's committed bytes minus base-plus-one-newline under both of G5's independent readers. No marker line reached any target (G9).

## Deviations & assumptions
1. The C5 row of `## Commits` carries `rewrite` rather than a numstat, and the C5 item-status row names no SHA: a commit cannot table or number itself. That is the handback template's R-0149 self-reference exception, not a departure from the ordered sequence — C0a, C0b, C1, C2, C3, C4, C5 was followed exactly, with no extra commit, none dropped and no reordering.
2. The `push` item-status row is `deviated` because G11 itself rules its outcome to be a value of no file this round writes. The row records what the block ORDERED; the reviewer records what the push DID, in the R11 ledger entry.
3. G5's three negative controls were computed IN MEMORY and no mutant byte was ever written to disk. Constraint 11 binds any mutant that IS written; writing none is strictly stronger than writing one under a disposable worktree. Consequently no worktree was created, none was removed, and `git worktree list` read 1 line at every point it was taken.
4. Round scratch: `.remedy-wt/r11-slices/` and the four slice files inside it were created by THIS round as the extractor's output, then deleted BY THEIR EXACT PATHS and never by a glob. Nothing pre-existing under `.remedy-wt/` — this round's own block file included — was edited or deleted; the block file was read once, for the G2 pre-C0a transport reading.
5. The sandbox rejected five commands by FORM rather than content: one compound `git` chain using `$?`, three `python3` heredocs carrying a literal path-set, and the heredoc that would have written this file. Each rejected reading was re-obtained through a differently shaped command with the same semantics — the path-set difference, for instance, by parsing the change set out of the block's own `Change set:` section rather than restating it as a literal, and this file by the editor rather than by a shell redirect. No measurement was skipped, softened or inferred, and no number written here is unmeasured.
6. G5's blank-line unit counts use the splitter stated in that same line. The R9 ledger entry records 284→285 units for the ledger file under the R9 reviewer's own splitter, while mine reads 285→287 at this base and commit. Different splitter and different commit, so this is not a contradiction; it is stated because G5 requires the N and the unit counts MY split measured rather than ones quoted from elsewhere.
7. NO contradiction was found inside the block, and every base reading it states reproduced exactly at `99d77d5c`: live_review 570870 bytes / 1197 lines with 240 ids, maximum `R-0679`, 2 `Done:` lines, 15 `Recurrence:` lines and the 9 `Gate:` keys `R19` and `R1` through `R8`; decisions 560571 / 7441 with 129 DECISIONs and D3 the highest F031 key; T5_F031 6705 / 122 with the R5 amendments heading last; plan 49 lines / 2964 bytes; handoff 71 lines. One reading is recorded so the reviewer need not re-derive it rather than as a defect: constraint 6 names GATES910 as a single slice while G6 requires two `Gate:` keys from it, which is consistent because that one slice carries two entries.
8. Cap: constraint 3 fixes SEVEN commits, C0a through C5, so AGENTS.md `### handoff.md` gives the >5-commit tier of 100 lines — resolved from the count the block ORDERS, per R-0676, not from a number quoted to me. This file is measured under that tier with `wc -l`; no section was dropped, no DECISION D15 overage is owed or claimed, and no token cap is claimed, that cap having been withdrawn by DECISION F255 D6.

## Next
1. Phase 1 rule 1: re-read `.agent/STOP` from disk. It is ABSENT as of this commit, read once before C0a and again before C5.
2. NO pull request exists for `feature/f031-decision-inbox` — `gh pr list --state open` returned `[]` — and none should be created yet.
3. T002a is now UNBLOCKED and builds the inbox card and the GENERIC options renderer as PURE model functions under `apps/ui/src/api/` with `.test.ts` files beside them, per DECISION F031 D4 and D5; the extensibility test for a novel options payload runs at the model layer.
4. T002a's first commit also records the R11 verdict, which by DECISION F085 D9 no artefact of this round can carry.
