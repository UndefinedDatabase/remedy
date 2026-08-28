# Handback — F037 Rendered diff viewer, round 16

## Session

SESSION 4 of feature F037 · round 16 · rounds so far 16

Under the soft limit (25 rounds / 7 sessions), so no scope report is owed this
round. T002 is finished: the view model, its vitest suite, the stylesheet, the
component and the render guard are all on disk, and the last named piece —
intraline emphasis — is ruled by DECISION F037 D9 rather than deferred a seventh
time. `.agent/plan.md` carries the standing risk: T003 is three or four rounds
of work against a 25-round limit, so the session that reaches round 21 with T003
unfinished owes a scope report instead of another step.

## Range

Review of `68680786..HEAD`, where HEAD is the C8 commit that writes this file
(the R-0149 self-reference exception — a handoff cannot table its own commit).

## Commits

### 8368a4c5 docs(agent): save the F037 R16 block verbatim — C0a
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r16.md` | +471 / -0 | the block saved byte for byte |

### 81fb30c5 docs(agent): mirror the F037 R16 block into last_block — C0b
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +391 / -373 | same bytes, one git blob with the saved copy |

### 0042f710 docs(agent): set the plan to F037 R16 — C1
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +27 / -26 | byte-equal to the PLANF037R16 slice |

### f9ad7ca5 docs(agent): book the R15 gate verdict and the type-gate slip — C2
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | GATER15 appended |
| `.agent/prose_slips.md` | +12 / -0 | SLIPR16 appended |

### b5478895 docs(roadmap): rule intraline emphasis as DECISION F037 D9 and amendment A5 — C3
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +67 / -0 | DECISION9 appended |
| `docs/roadmap/features/T5_F037.md` | +20 / -0 | AMENDA5 appended |

### c5797353 feat(ui): cut a diff line into intraline segments — C4
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.test.ts` | +126 / -1 | SPEC S3, one new `describe`, no existing test changed |
| `apps/ui/src/api/diffViewModel.ts` | +70 / -1 | SPEC S1 and S2 |

### 1cf93245 style(ui): give the intraline mark the sheet's own two hues — C5
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/diff/DiffView.module.css` | +25 / -8 | SPEC S4: two rules appended, the deliberate-absence paragraph replaced |

### 09c6fc9c feat(ui): draw the diff rows as file, hunk head and line markup — C6
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/diff/DiffView.tsx` | +173 / -0 | SPEC S5 through S9, a NEW file |

### 774cf732 test(ui-contracts): gate the diff viewer by reading it — C7
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_view_render.py` | +288 / -0 | SPEC S10, a NEW file |

### C8 — this file
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | the handback; a handoff cannot table its own commit |

## External actions

- `git worktree add --detach .remedy-wt/r16-wt 774cf732` — created for G6.
- `git worktree remove .remedy-wt/r16-wt` — removed after G6; `git worktree
  list` shows the primary checkout alone, and the worktree read
  `git status --porcelain` empty before removal.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
  exit 0, stdout `[]`.
- `git push -u origin feature/f037-rendered-diff-viewer` after C8.
- No PR created, nothing merged, no force-push, no history rewrite.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a: ABSENT (`ls`
reports "No such file or directory"); read again before C8: ABSENT.
`git rev-parse HEAD` before C0a was
`68680786e82f0781e3f1f410aee80986884dfa32`, which EQUALS the block's base
`68680786`. `git branch --show-current` is `feature/f037-rendered-diff-viewer`.
`git status --porcelain` line count after each commit: C0a 0, C0b 0, C1 0, C2 0,
C3 0, C4 0, C5 0, C6 0, C7 0.

**G2 TRANSPORT — PASS, one digest comparison.** The committed C0a blob
(`git show 8368a4c5:.agent/authored/f037-r16.md`) is sha256
`fda049537c12a805285830bac86f023690bae4570ffcc6d923f9aa1f16c4612e`, 33024 bytes,
471 lines. The reviewer's scratch original `.remedy-wt/f037-r16-block.md`
measures the SAME three readings, and the disk-to-disk comparison of
`.agent/authored/f037-r16.md` against `.remedy-wt/f037-r16-block.md` is byte
equality True. `git rev-parse 81fb30c5:.agent/authored/f037-r16.md` and
`git rev-parse 81fb30c5:.agent/last_block.md` are both
`9185d96ca9d9323aa05f2b55dbf8124c28b45891` — the SAME blob.
WHAT THE CHAIN COVERS: that the bytes the reviewer measured in scratch are the
bytes committed at C0a and mirrored at C0b, and therefore that every slice
extracted below came from the reviewer's own text. WHAT IT DOES NOT COVER: the
hop from the reviewer's composition into the scratch file, and the prompt that
delegated this round — neither is a value this worker can measure, and the block
was verified against the three readings the delegation named before anything was
touched (471 lines, 33024 bytes, that sha256, all three agreeing).

**G3 EXTRACTION AND CAPS — PASS, measured on the committed C0a blob.**
Content line counts: PLANF037R16 49, GATER15 1, SLIPR16 11, DECISION9 66,
AMENDA5 19. TOTAL 471, CONTENT 146 (their sum), PROSE 325 (TOTAL − CONTENT).
TOTAL ≤ 490: True. PROSE ≤ 400: True.

**G4 THE PLAN AT C1 AND THE STYLESHEET AT C5 — PASS.**
`git show 0042f710:.agent/plan.md` is byte-equal to the PLANF037R16 slice
extracted from the committed C0a blob INCLUDING the trailing newline: True.
Negative control against that slice minus its trailing newline: False. Lines
exactly `## Goal`: 1. Lines exactly `## Next Steps`: 1. `wc -l` 49, strictly
under 50: True.
Stylesheet rule bodies extracted from the C5 blob (`1cf93245`) and from the
`68680786` blob, comments stripped, byte-identical each: `.diffLine` True,
`.diffLine.add` True, `.diffLine.del` True, `.diffLine .ln` True, `.hunkHead`
True — which is constraint 3. WHOLE-FILE comparison of the same two blobs:
False, so the five readings above are not a comparison that cannot fail. The
five bodies still carry `font` before `font-feature-settings`, which is what
finding `R-0720` pinned.

**G5 THE RECORD AT C2 AND C3 — PASS.** All four appends, each re-read from disk:

| Append | reader (a) `before + b"\n" + slice` | units | reader (b) last-N units in order | NEG (a) | NEG (b) | base is byte PREFIX |
|---|---|---|---|---|---|---|
| GATER15 → `.agent/live_review.md` | True | 1 | True | False | False | True |
| SLIPR16 → `.agent/prose_slips.md` | True | 1 | True | False | False | True |
| DECISION9 → `.agent/decisions.md` | True | 9 | True | False | False | True |
| AMENDA5 → `docs/roadmap/features/T5_F037.md` | True | 2 | True | False | False | True |

The negative control flips one byte inside the FIRST appended paragraph and
turns BOTH readers False in every one of the four cases. Each pre-round blob was
read with `git show 68680786:<path>` into memory, never over the tracked file.

Line-anchored over `.agent/live_review.md` after C3, base figure at `68680786`
beside each: `^- R-\d+ — ` 285 → 285; `^Done: R-\d+ — ` 34 → 34; `^Landed: R-`
1 → 1; `^Gate: F\d+ R\d+ — ` 85 → 86; open set 252 → 252; every REGISTERED id
distinct: True (285 occurrences, 285 distinct). This round registers and
resolves nothing, which is why only the gate count moved.
Over `.agent/decisions.md`: `^## DECISION ` 174 → 175; occurrences of
`F037 D9` 0 → 1.
Over `docs/roadmap/features/T5_F037.md`: lines beginning `**A` 4 → 5, one per
amendment A1 through A5.

**G6 THE RED-PROOFS OF THE PYTHON GUARD — PASS.** All runs in the disposable
worktree `.remedy-wt/r16-wt` at the C7 tree, `__pycache__` purged before every
run, `python3 -B` throughout.

FIRST, THE REASON RE-MEASURED RATHER THAN CITED. `python3 -B -m pytest
tests/orchestration/test_test_runner.py -q -k vitest` with the worktree as the
working directory: REAL exit code 1, `1 failed, 3 passed, 48 deselected in
0.77s`. The failure is a STARTUP ERROR NAMING VITEST, not a test result — the
captured output carries `⎯⎯ Startup Error ⎯⎯` and
`Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'vitest' imported from …`,
preceded by `Could not resolve 'vitest/config' in vitest.config.ts` and
`failed to load config from …/.remedy-wt/r16-wt/apps/ui/vitest.config.ts`. No
test file was collected and no assertion of the frontend suite ran. That is
DECISION F037 D8's reason measured rather than quoted: `apps/ui/node_modules` is
gitignored, so it is absent from the disposable worktree guardrail G5 confines
every destructive check to, and a TypeScript mutation red-proof is therefore not
orderable here.

UNMUTATED CONTROL: REAL exit code 0, `12 passed in 0.18s`. Control re-run after
every restore: REAL exit code 0, `12 passed in 0.18s`.

| # | Mutation | occurrences BEFORE the edit | exit | summary line | failing node ids | restored byte-identical (sha256) |
|---|---|---|---|---|---|---|
| a | `DiffView.tsx`: the `splitLineIntoIntralineSegments` call replaced by a plain render of `row.line.content` | 1 | 1 | `2 failed, 10 passed in 0.20s` | `TestTheComponentDerivesNothing::test_the_component_calls_every_rule_it_must_not_carry`, `TestTheIntralineMarkExists::test_the_component_cuts_the_line_and_marks_the_covered_run` | True |
| b | `DiffView.tsx`: the hunk head's `<button` changed to `<div` | 1 | 1 | `1 failed, 11 passed in 0.20s` | `TestTheHunkHeadIsAControl::test_the_collapse_control_is_a_button_rather_than_a_div` | True |
| c | `DiffView.module.css`: the `.diffLine.del .intraline` rule deleted | 1 | 1 | `1 failed, 11 passed in 0.20s` | `TestTheIntralineMarkExists::test_both_intraline_rules_are_real_rules_in_the_stylesheet` | True |
| d | `DiffView.tsx`: `className={styles.hunkHead}` renamed to `className={styles.hunkHeader}`, a class the stylesheet does not define | 1 | 1 | `1 failed, 11 passed in 0.20s` | `TestEveryClassTheComponentNamesIsReal::test_every_class_the_component_names_has_a_rule_in_the_stylesheet` | True |

All node ids are under `tests/ui_contracts/test_diff_view_render.py`. Every
mutation is RED at a REAL exit code of 1, each replaced string occurred exactly
once before its edit, and each file was restored to its pre-mutation sha256. The
four mutations fail four DIFFERENT assertions, so no one reading is carrying the
whole guard.

**G7 SUITES, TYPES, LINT AND CANARY AT C7 — PASS, one pytest process at a
time.** Base figures from the block beside each.

| Command | exit | summary line | base at `68680786` |
|---|---|---|---|
| `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q -k typescript` | 0 | `1 passed, 73 deselected in 1.94s` | — |
| `python3 -m pytest tests/orchestration/test_test_runner.py -q` | 0 | `52 passed in 5.33s` | `52 passed` |
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | `603 passed, 4 skipped in 5.50s` | `591 passed, 4 skipped` |
| `python3 -m pytest tests/docs/ -q` | 0 | `295 passed in 0.44s` | `295 passed` |
| `python3 -m ruff check tests/ui_contracts/test_diff_view_render.py` | 0 | `All checks passed!` | — |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 20.57s` | `42 passed` |

The typescript node PASSED — it did NOT skip. It skips only when
`apps/ui/node_modules/.bin/tsc` is absent; that binary is present, so the node
really ran this repository's LOCAL `tsc --noEmit` over `apps/ui` and the new
`DiffView.tsx` and the new module code TYPE-CHECK at exit 0. `tests/ui_contracts/`
grew by exactly 12, which is the new guard's 12 tests and nothing else; every
other suite matches its base figure exactly. `tests/orchestration/test_test_runner.py`
is the node that RUNS `npx vitest run`, so the new `describe` in
`diffViewModel.test.ts` is EXECUTED and green in the primary checkout rather
than merely shipped.

**G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C7 — PASS.**
`git diff --name-only 68680786..774cf732` reports 12 paths:
`.agent/authored/f037-r16.md`, `.agent/decisions.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`apps/ui/src/api/diffViewModel.test.ts`, `apps/ui/src/api/diffViewModel.ts`,
`apps/ui/src/components/diff/DiffView.module.css`,
`apps/ui/src/components/diff/DiffView.tsx`,
`docs/roadmap/features/T5_F037.md`,
`tests/ui_contracts/test_diff_view_render.py`.
ACTUAL MINUS EXPECTED: empty. EXPECTED MINUS ACTUAL: `.agent/handoff.md` alone,
which is exactly what the block predicts because C8 writes it.
`git diff --stat` restricted to `packages/`: EMPTY. To `tests/`:
`tests/ui_contracts/test_diff_view_render.py | 288 +` — that file ALONE. To
`apps/`: the four files above, `394 insertions(+), 10 deletions(-)`.
Per-commit insertions from `git show --numstat`, each under 500 and each
matching the `+/-` column of the `## Commits` table above cell by cell: C0a 471,
C0b 391, C1 27, C2 14 (2 + 12), C3 87 (67 + 20), C4 196 (126 + 70), C5 25,
C6 173, C7 288.
Lines matching `^<<<SLICE ` / `^<<<END `: `.agent/plan.md` 0 / 0,
`.agent/live_review.md` 0 / 0, `docs/roadmap/features/T5_F037.md` 0 / 0,
`apps/ui/src/components/diff/DiffView.tsx` 0 / 0. CONTROL over the C0a blob:
5 / 5, so the counter is not blind.
`git ls-files .remedy-wt` line count: 0 — the scratch stays untracked.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`: exit 0,
stdout `[]`.

## Authored-text proofs

Five reviewer-authored texts were applied this round, every one extracted
PROGRAMMATICALLY from the COMMITTED C0a blob rather than retyped, so no slice
passed through a keyboard:

| Slice | Target | Content lines | Applied | Proof |
|---|---|---|---|---|
| PLANF037R16 | `.agent/plan.md` | 49 | rewrite | byte-equal to the extracted slice incl. trailing newline; negative control False (G4) |
| GATER15 | `.agent/live_review.md` | 1 | append | reader (a) and reader (b) both True, both negative controls False (G5) |
| SLIPR16 | `.agent/prose_slips.md` | 11 | append | reader (a) and reader (b) both True, both negative controls False (G5) |
| DECISION9 | `.agent/decisions.md` | 66 | append | reader (a) and reader (b) both True over 9 units, both negative controls False (G5) |
| AMENDA5 | `docs/roadmap/features/T5_F037.md` | 19 | append | reader (a) and reader (b) both True over 2 units, both negative controls False (G5) |

The committed `.agent/authored/f037-r16.md` is byte-identical to the reviewer's
scratch original disk to disk, and is one git blob with `.agent/last_block.md`
(G2). No slice was edited, reflowed or corrected; no marker line was written
into any target file (G8).

## Deviations & assumptions

1. **S1 IS SILENT ABOUT A NEGATIVE START OFFSET, AND I RULED IT AS A CLAMP.**
   The spec names three arithmetic defences — a span starting past the end is
   dropped, a span running past the end is clamped, a negative or zero LENGTH is
   dropped — but says nothing about a span whose START is below zero, and the
   function must be TOTAL. I clamped the start to zero, which is the same
   reading as the clamp at the other end, rather than dropping the span, which
   would lose an emphasis the payload really asked for. The choice is written
   into the function's own WHY comment and covered by its own vitest case
   (`clamps a span reaching back before offset zero`) and by the concatenation
   property. Reversing it means one `continue` and one test.
2. **THE COMPONENT'S ROOT `<section>` CARRIES NO CLASS.** Constraint 3 permits
   no new CSS declaration and SPEC S4 appends exactly two rules, so the
   stylesheet's vocabulary is six class names — `diffLine`, `add`, `del`, `ln`,
   `hunkHead`, `intraline` — and guard (b) requires every `styles.<name>` the
   component asks for to resolve to a real rule. The wrapper, the file rows and
   the truncation notice are therefore unclassed elements, and the reason is
   written into the component beside them. T003 is where a layout class would
   arrive with the sidebar and the virtual scrolling that need it.
3. **THE GUARD CARRIES A STRIPPER-VACUITY CLASS THE SPEC DID NOT ORDER.** S10
   orders assertions (a) through (e); I added `TestTheStripperIsNotVacuous`
   (3 tests) above them, which is the class
   `tests/ui_contracts/test_decision_answer_wiring.py` carries for the same
   reason. Without it a stripper that silently returned its input would leave
   every one of (a) through (e) satisfiable by the component's own prose header,
   which names each asserted symbol. Two of its three tests are synthetic and
   one is a length comparison, so none of them pins a sentence that can go
   stale.
4. **G6 MUTATION (a) TURNED TWO ASSERTIONS RED, NOT ONE.** The block expects
   RED and got it; I report the shape because replacing the call also removes
   the `<mark>` that carries `styles.intraline`, so both the delegation check
   and the intraline-cut check fail. The other three mutations are one
   assertion each.
5. **NO TYPESCRIPT MUTATION RED-PROOF WAS RUN, AS CONSTRAINT 10 ORDERS**, and
   the reason was re-measured rather than cited — see G6's first paragraph. The
   `.tsx` and the new vitest cases are covered instead by the local
   `tsc --noEmit` node (exit 0, PASSED not skipped) and by the node that runs
   `npx vitest run` (exit 0), both in the primary checkout.
6. **ENVIRONMENT, NOT A SCOPE CHANGE.** Three shell forms were refused by this
   session's command guard — a `cat >> … <<'EOF'` append, a `$?` read, and one
   `python3` heredoc the guard rejected by shape. The appended test block was
   written with the editor instead and the two measurements were re-issued in an
   accepted form; no gate, file or commit changed as a result.
7. **NO COMMIT WAS ADDED, DROPPED OR REORDERED.** The nine commits C0a through
   C8 landed in the block's own order, each with its ordered change set and
   nothing outside it. No PR was created, nothing was merged, no branch was
   created or switched, and no history was rewritten.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `8368a4c5` |
| C0b mirror the block | done | `81fb30c5` |
| C1 the plan | done | `0042f710` |
| C2 the R15 verdict and the slip | done | `f9ad7ca5` |
| C3 DECISION F037 D9 and amendment A5 | done | `b5478895` |
| C4 the intraline segmentation and its tests | done | `c5797353` |
| C5 the stylesheet | done | `1cf93245` |
| C6 the component | done | `09c6fc9c` |
| C7 the render guard | done | `774cf732` |
| C8 the handback | done | this file |
| G1 hygiene | done | PASS — STOP absent twice, HEAD equalled `68680786`, tree clean after all eight commits |
| G2 transport | done | PASS — one digest comparison, blob equals scratch, C0a and C0b one blob |
| G3 extraction and caps | done | PASS — TOTAL 471, CONTENT 146, PROSE 325, both caps hold |
| G4 the plan and the untouched declarations | done | PASS — plan byte-equal, five CSS bodies identical, whole file not |
| G5 the record | done | PASS — four appends, both readers, four negative controls, counters as expected |
| G6 the red-proofs | done | PASS — vitest is a startup error in the worktree; control green, four mutations RED at exit 1 |
| G7 suites, types, lint, canary | done | PASS — six commands, every one exit 0, every base figure matched |
| G8 structure, artifacts, PR gate | done | PASS — change set exact, `packages/` empty, no markers leaked, no PR open |

## Next

Review this round at `774cf732` and the C8 handback commit, then author F037 R17
as the first round of T003: mount `DiffView` behind the entry point
`docs/ui/design_reference/component_spec.md:113-116` names —
`onOpenDiff(taskId)` from `DetailPopover` — with the fetch through
`remedyApi.ts` calling `readDiffEnvelope`, and the file sidebar over
`buildDiffFileSummaries`. Phase 1 rule 1 first: re-read `.agent/STOP` from disk
before anything else, then the Open PR Gate.
