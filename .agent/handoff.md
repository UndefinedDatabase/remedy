# Handoff — F037 Rendered diff viewer, round 24

## Session

SESSION 7 of feature F037 · round 24 · rounds so far 24.

THIS IS THE LAST DELEGATED ROUND OF SESSION 7 AND OF THIS SESSION. F037 stands
AT the soft limit of operator amendment amend0827-process-diet rule 6 — session
7 of 7, round 24 of 25 — with DECISION F037 D11 and feature-file amendment A6
both recorded on disk. Its remaining work is the closure sequence, and ONE
proposal is open to the operator that no session may execute for them: giving
the split-off scope its own STATUS line.

Branch: `feature/f037-rendered-diff-viewer`. No PR exists and none was created.

## Scope report — F037 at the soft limit

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F037 has reached SESSION 7 of a seven-session soft limit at round 24 of
twenty-five. Operator amendment amend0827-process-diet rule 6 makes this report
the obligation, not more feature work.

WHAT IS FINISHED. T001 the parser and the read endpoint, with its corpus tests
and the bounds of DECISIONS F037 D5, D6 and D7. T002 the rendering core — lines,
intraline spans, hunk heads, collapse — against the feature file's binding CSS.
T003 in the greater part: the file sidebar, virtual scrolling and its windowing
rule, the door and mount into `RemedyShell`, and the lazy language-bundle model
with its promise cache, its retry-after-rejection rule and the prototype-safe
lookup that finding `R-0731` forced.

WHAT IS MISSING, and none of it is discovered late — all three have stood under
Next Steps in `.agent/plan.md` at `82d3d584` and in the two rounds before it:

1. `loadDiffLanguageBundle` is UNWIRED. Measured at `82d3d584`, it has no caller
   outside its own module and its two test files, so highlighting is built and
   not rendered.
2. The 10k-line perf fixture is UNMEASURED end to end, so the Acceptance bullet
   naming a recorded perf budget is unmet.
3. The sidebar's visual treatment is unruled; amendment A4's three design
   authorities are silent on it.

WHAT THIS SESSION DID ABOUT IT. DECISION F037 D11 rules the three pieces OUT of
F037's scope and feature-file amendment A6 records that on the roadmap, so the
narrowing is visible where a later reader looks rather than only in a session
log. F037's remaining work is its closure sequence: the integration-gate round,
the evidence-and-zip round, then the STATUS round.

THE PROPOSAL TO THE OPERATOR, which this session does NOT execute because rule 6
reserves it: give the split-off scope its own STATUS line immediately before
F033 — the highlighting wiring, the 10k-line perf measurement and the sidebar
ruling, as one line of about three to four rounds. The alternative is to reject
A6, in which case reversing it is one paragraph in each of `.agent/decisions.md`
and `docs/roadmap/features/T5_F037.md`, and F037 continues past its soft limit
with the operator's knowledge rather than without it.

## Range

Review of `82d3d584`..`HEAD`.

## Commits

### 61b8f183 chore(agent): save the F037 R24 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r24.md` | +341 / -0 | C0a, the block saved verbatim |

### a01d9036 chore(agent): mirror the R24 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +270 / -282 | C0b, the same bytes mirrored |

### e6e8851f docs(agent): retarget the plan at the F037 scope report
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +25 / -29 | C1, rewritten from the PLANF037R24 slice |

### f4181491 docs(review): book the R23 verdict and resolve the lookup finding
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +10 / -0 | C2, GATER23 then DONE731 appended |

### 421a4004 docs(agent): rule the unbuilt F037 pieces out of scope as D11
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +46 / -0 | C3, DECISIOND11 appended |

### 24a28760 docs(roadmap): narrow F037 to what it ships with amendment A6
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T5_F037.md` | +33 / -0 | C4, AMENDMENTA6 appended |

### C5 — this handoff commit (self-reference exception, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C5, the handback carrying the scope report verbatim |

Six commits precede this one; the ordered sequence C0a, C0b, C1, C2, C3, C4, C5
was followed exactly, with no extra commit, no dropped commit and no reordering.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`,
  exit 0. No PR created, nothing merged, no history rewritten.
- `git push -u origin feature/f037-rendered-diff-viewer` after C5 — see the
  Verification block for its recorded outcome.
- No `git worktree` was added or removed this round; none was needed.
- Scratch: `.remedy-wt/f037-r24-names.txt` was written to hold the measured
  `git diff --name-only` output for G8's set arithmetic and REMOVED by that exact
  path afterwards. `git ls-files .remedy-wt` is 0.

## Verification

One line per gate, all real and all executed in the primary checkout.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk and ABSENT before C0a and
  again before C5 (`ls` exit 2, "No such file or directory"). `git rev-parse HEAD`
  before C0a was `82d3d58460b64c473f008d733ba5bf8ac915ed04`, equal to BASE. Branch
  `feature/f037-rendered-diff-viewer`. `git status --porcelain | wc -l` was 0
  after C0a, C0b, C1, C2, C3 and C4.
- **G2 TRANSPORT — PASS.** The committed C0a blob is 26106 bytes, 341 lines,
  sha256 `fe2e3a1afdc6479472ec744f9afb7f34b86f640d353ebe21a0010f890b674cda`. At
  C0b `git rev-parse HEAD:.agent/authored/f037-r24.md` and
  `HEAD:.agent/last_block.md` are ONE blob,
  `dce091538cc0d1e695cc0f92d0cd616bf1c308b1`. THIS CHAIN COVERS THE SAVED COPY
  AND ITS MIRROR ONLY, and says nothing about the emitted bytes, which this
  workflow cannot measure and which this handback therefore does not claim.
- **G3 THE PLAN AT C1 — PASS.** PLANF037R24 extracted from the COMMITTED C0a blob
  (`git show 61b8f183:.agent/authored/f037-r24.md`) versus
  `git show e6e8851f:.agent/plan.md`: byte equality True, including the trailing
  newline. Negative control, the same slice minus its trailing newline: False.
  `wc -l` 43, strictly under 50. Lines exactly `## Goal`: 1. Lines exactly
  `## Next Steps`: 1.
- **G4 THE RECORD AT C2 — PASS, both readers.** (a) `82d3d584` blob + `\n` +
  GATER23 + `\n` + DONE731 == the `f4181491` blob: True. Negative control, one
  byte flipped inside GATER23, the FIRST appended paragraph: False. (b) Splitting
  the C2 blob on blank lines, MY script measured 5 appended units against the
  slices' 5 paragraphs, matching IN ORDER: True — units 1-4 the GATER23
  paragraphs, unit 5 `Done: R-0731 …`. The pre-round blob is a byte PREFIX of the
  C2 blob, 1308970 bytes growing to 1316230. Every non-current revision was read
  with `git show <sha>:<path>` into memory; nothing was written over a tracked
  file.
- **G5 THE LEDGER — PASS, every figure as ordered.** Over the C2 blob:
  `^- R-\d+ — ` 292 [292], UNMOVED, and all 292 DISTINCT; `^Done: R-\d+ — ` 42
  [41], risen by ONE for `R-0731`; `^Landed: R-` 11 [11], UNMOVED;
  `^Gate: F\d+ R\d+ — ` 94 [93], risen by ONE; the OPEN SET computed AS A SET 252
  [253], FALLEN BY ONE. `Gate: F037 R23` occurs exactly 1 time in the C2 blob.
  Base figures were re-measured at `82d3d584` before C0a, not inherited.
- **G6 THE DECISION AT C3 AND THE AMENDMENT AT C4 — PASS.** C3: the `f4181491`
  blob of `.agent/decisions.md` is a byte PREFIX of the `421a4004` blob, 684609 →
  687668; pre + `\n` + DECISIOND11 == post True; negative control with one byte
  flipped in that slice's FIRST paragraph False. C4: the `421a4004` blob of
  `docs/roadmap/features/T5_F037.md` is a byte PREFIX of the `24a28760` blob,
  10885 → 12982; pre + `\n` + AMENDMENTA6 == post True; negative control False.
  Over the C3 blob `^## DECISION ` is 177 [176], risen by ONE, and `F037 D11`
  occurs exactly 1 time. Over the C4 blob lines starting `**A6` are exactly 1 and
  lines starting `**A5 ` are still exactly 1.
- **G7 SUITES AND THE DOCS GATE AT C4 — PASS, all four, run after C4 and before
  C5, ONE pytest process at a time in the primary checkout, each exit 0.**
  `python3 -m pytest tests/ui_contracts/ -q` → `653 passed, 4 skipped in 5.75s`
  [653, 4]. `python3 -m pytest tests/ui_server/ -q` → `495 passed in 30.17s`
  [495, 0 skipped]. `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/docs/ -q` → `347 passed in 5.58s` [347], constraint 7's docs-round gate.
  Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in
  20.70s` [42]. Nothing was repaired and no test was edited.
- **G8 STRUCTURE AND THE OPEN PR GATE AT C4 — PASS.**
  `git diff --name-only 82d3d584..24a28760` is exactly the six Change-set paths
  minus `.agent/handoff.md`; RESIDUE IS EMPTY BOTH WAYS — measured-minus-changeset
  `[]` and changeset-minus-measured `[]`. `git diff --stat 82d3d584..24a28760`
  restricted to `apps/`, to `packages/` and to `tests/` printed NOTHING in all
  three cases — measured, not asserted. Per-commit insertions 341, 270, 25, 10,
  46 and 33, each under 500 and each matching the `## Commits` table above cell by
  cell; every commit single-parent, the chain running
  `82d3d584 → 61b8f183 → a01d9036 → e6e8851f → f4181491 → 421a4004 → 24a28760`.
  `git grep -c` for `^<<<SLICE ` and for `^<<<END ` at `24a28760` matched NEITHER
  `.agent/plan.md` NOR `.agent/live_review.md` NOR `.agent/decisions.md` NOR
  `docs/roadmap/features/T5_F037.md` — 0 in all four — against the NON-ZERO
  control `.agent/authored/f037-r24.md` at 6 and 6. `git ls-files .remedy-wt | wc -l`
  is 0. `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  is `[]`.

## Authored-text proofs

- PLANF037R24 → `.agent/plan.md` at C1: byte-equal to the slice extracted from
  the COMMITTED `.agent/authored/f037-r24.md`, with the negative control False
  (G3).
- GATER23 and DONE731 → `.agent/live_review.md` at C2: append equality True with
  the negative control False, and an independent paragraph-order reader agreeing
  at 5 units (G4).
- DECISIOND11 → `.agent/decisions.md` at C3 and AMENDMENTA6 →
  `docs/roadmap/features/T5_F037.md` at C4: append equality True with a negative
  control False on each (G6).
- SCOPEREPORT → the section above in this file: applied byte for byte from the
  same committed blob.

## Deviations & assumptions

- NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. There is no commit
  beyond the ordered sequence, none was dropped and none was reordered: C0a, C0b,
  C1, C2, C3, C4, C5 ran in exactly that order.
- No production code and no test file changed. `apps/`, `packages/` and `tests/`
  are measurably untouched (G8), as constraint 2 requires.
- No `Done:` or `Gate:` paragraph was authored by this worker and no `Landed:`
  line was added: everything entering `.agent/live_review.md` is the two C2
  slices applied byte for byte, per constraint 5.
- Constraint 6 was read and this round was NOT flagged as a contradiction: rule 6
  makes the scope report the obligation at the soft limit, and C3 and C4 are
  neither verdicts, registrations nor corrections, with C4 landing under
  `docs/roadmap/`.
- Tooling note, not a scope change: two G8 measurement commands were rejected by
  this session's shell guard on their FORM (brace-literal and indexed-expansion
  syntax). They were re-expressed — the changed-path list captured to
  `.remedy-wt/f037-r24-names.txt` and the set arithmetic run over that file, the
  file then removed by exact path. No gate was weakened or skipped, and no gate's
  ordered property was replaced by a weaker one.
- Assumption about placement: A6 is appended at the END of the file, which is the
  end of its "Design amendments" section and directly after A5 — where every
  prior amendment of this file sits. Nothing above it was edited, reordered or
  deleted, as constraint 3 requires.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | |
| C0b mirror into `last_block.md` | done | one blob with C0a |
| C1 rewrite `.agent/plan.md` | done | |
| C2 append GATER23 then DONE731 | done | |
| C3 append DECISIOND11 | done | |
| C4 append AMENDMENTA6 | done | after C3, as ordered |
| C5 rewrite `.agent/handoff.md` | done | this file |
| G1 hygiene | done | STOP absent twice, tree clean, BASE matched |
| G2 transport | done | one blob; saved copy and mirror only |
| G3 the plan at C1 | done | equality True, control False, 43 lines |
| G4 the record at C2 | done | both readers, 5 units |
| G5 the ledger | done | 292 / 42 / 11 / 94 / open set 252 |
| G6 decision at C3, amendment at C4 | done | both appends proved |
| G7 suites and the docs gate | done | 653+4, 495, 347, 42 — all exit 0 |
| G8 structure and the Open PR Gate | done | residue empty both ways, no open PR |

Open findings: the OPEN SET stands at 252, down one from 253 with `R-0731`
resolved.

## Next

Review this round at `82d3d584..HEAD`, then run F037's closure sequence as
amended by A6 — the integration-gate round first. Before anything else the next
session applies Phase 1 rule 1 (`.agent/STOP`) and only then rule 2 (the Open PR
Gate). The STATUS-split proposal in the scope report above is the operator's to
accept or reject and is NOT executed by any session.
