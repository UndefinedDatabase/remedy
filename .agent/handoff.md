# Handoff — F032 R3, the evidence-triple schema and its validator

## Session

`SESSION 1 of feature F032 · round R3 · rounds so far 3`

Feature F032, round R3. Branch `feature/f032-evidence-triple`. Round base
`935ef1ed` (`935ef1ed5bc24a55f81d8e2ea4eaca638fd35c00`), the tip R2 handed back.
Soft limit 25 rounds / 7 sessions — not approached.

THIS ROUND WROTE PRODUCTION CODE: two NEW files, `packages/orchestration/decision_evidence.py`
and `tests/orchestration/test_decision_evidence.py`. No existing file under
`packages/`, `apps/` or `tests/` was edited. `list_decisions` was NOT touched.
No pull request was created and nothing was merged.

## Range

Review of `935ef1ed..HEAD`.

## Commits

### fdbcabee chore(agent): save the F032 R3 block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f032-r3.md` | +406 / -0 | C0a, byte-for-byte copy of `.remedy-wt/f032-r3.md` via `shutil.copyfile` |

### fc94ebaf chore(agent): mirror the F032 R3 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +333 / -330 | C0b, mirror of the C0a file; same git blob `38a1f9efdd63` |

### 36821fc2 docs(agent): move the plan to F032 R3, the T001a schema round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +24 / -24 | C1, PLANF032R3 applied byte for byte; first substantive commit |

### 93202603 docs(agent): record DECISION F032 D4 and one R2 prose slip
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +44 / -0 | C2, DEC4 appended: the names ruling |
| `.agent/prose_slips.md` | +5 / -0 | C2, SLIP appended: the R2 wrapped table row |

### 79ab41b2 docs(roadmap): add F032 design amendment A4 on the Python and wire names
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T5_F032.md` | +14 / -0 | C3, FEATA4 appended, where a builder reads it |

### 9aaa9d0d feat(orchestration): add the decision evidence triple schema and its validator
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/decision_evidence.py` | +275 / -0 | C4, NEW, S1 through S8 |

### 4fd27d1a test(orchestration): pin every evidence-triple rule to its problem sentence
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_decision_evidence.py` | +223 / -0 | C5, NEW, S9 |

### C6 — this handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self | a handoff cannot table the commit that writes it (R-0149) |

The `+/-` column is `git diff --numstat <sha>~1..<sha>` verbatim and agrees cell
for cell with G8.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` →
  exit 0, output verbatim `[]`. Open PR Gate clear. NOTHING merged, NOTHING
  created.
- `git worktree add --detach .remedy-wt/g7-mut 4fd27d1a` for the G7 mutation
  proofs, then `git worktree remove --force` and `git worktree prune`. The
  primary checkout was never mutated.
- INTENT after C6: `git push origin feature/f032-evidence-triple`. C6 is
  authored before the push exists, so no exit code and no remote tip is stated
  here; both are in the round's completion report.
- No PR created. No merge. No branch created.

## Verification

One line per gate, with the real exit code.

- G1 hygiene, branch, sentinel — exit 0. `git rev-parse HEAD` before C0a
  `935ef1ed5bc24a55f81d8e2ea4eaca638fd35c00`; `git branch --show-current`
  `feature/f032-evidence-triple`; `git status --porcelain` 0 lines after each of
  C0a, C0b, C1, C2, C3, C4, C5 and C6; `.agent/STOP` ABSENT before C0a and
  ABSENT before C6.
- G2 transport — exit 0. sha256
  `8bdf8620e1560bb615eec3cb0a6d668f0f7c5b41e54bafd00c63942d4fdbb6a7`, 26836
  bytes, 406 lines at ALL FOUR points: the scratch `.remedy-wt/f032-r3.md`, the
  C0a blob, the C0b blob and the working copy read at C5. C0a and C0b are the
  SAME git blob `38a1f9efdd63928a58adc57adc84e837a8491c8a`. Whole-line runs of a
  single repeated character at length ≥ 4: NONE. THIS PROOF COVERS THE SCRATCH
  FILE, THE SAVED COPY, ITS MIRROR AND THE WORKING COPY, AND NOT THE BYTES OF
  ANY PROMPT.
- G3 extraction and caps — exit 0. The extractor printed 4 slices from the
  COMMITTED C0a blob by their marker lines: PLANF032R3 45, DEC4 43, SLIP 4,
  FEATA4 13. CONTENT 105, TOTAL 406, PROSE 301. PROSE ≤ 400 and TOTAL ≤ 490
  both hold.
- G4 the prose writes — exit 0. `.agent/plan.md` at C1 BYTE-EQUAL to PLANF032R3
  under the newline-INCLUDED convention; the negative control against the slice
  MINUS its trailing newline reads FALSE. `^## Goal$` 1, `^## Next Steps$` 1,
  `\bF\d{3}\b` matches `F032`, `wc -l` 45 (STRICTLY under 50). At C2:
  `.agent/decisions.md` pre-commit blob 633319 bytes (EQUAL to the reviewer's
  measurement at `935ef1ed`) + 1 + slice 2738 = 636058, and the C2 blob is
  636058 bytes, EQUALS pre + ONE newline + DEC4, and STARTS WITH the pre-commit
  blob as a byte PREFIX. `.agent/prose_slips.md` pre-commit blob 1681 bytes
  (EQUAL to the reviewer's) + 1 + slice 289 = 1971, and the C2 blob is 1971
  bytes, with the same equality and the same byte-PREFIX reading.
  `^## DECISION F032 D\d+ ` 3 → 4 with the ADDED key exactly
  `## DECISION F032 D4`.
- G5 the feature file and the docs gate — exit 0. `docs/roadmap/features/T5_F032.md`
  pre-commit blob 7291 bytes (EQUAL to the reviewer's) + 1 + slice 933 = 8225,
  and the C3 blob is 8225 bytes, EQUALS pre + ONE newline + FEATA4, and STARTS
  WITH the pre-commit blob as a byte PREFIX. `^## Design amendments$` still
  exactly 1 after C3. `python3 -m pytest tests/docs/
  tests/orchestration/test_roadmap_index.py -q` → REAL exit 0,
  `325 passed in 0.72s` — EQUAL to the reviewer's base measurement.
- G6 the new module, linted and read back — exit 0. `python3 -m ruff check
  packages/orchestration/decision_evidence.py` → REAL exit 0, output verbatim
  `All checks passed!`, under the repository's own `pyproject.toml` and never
  `--isolated`. By IMPORTING the module: `DECISION_EVIDENCE_REF_KINDS` sorted is
  exactly `['coverage', 'decision', 'failure', 'file']`; `NO_MATERIAL_DOWNSIDE`
  is `'no material downside identified'`; `UNKEYED_OPTION` is `''`;
  `DecisionEvidenceRef` fields `['kind', 'target', 'label']` frozen True,
  `DecisionOptionOutcome` fields `['option', 'expected_outcome', 'downside']`
  frozen True, `DecisionEvidenceTriple` fields `['refs', 'outcomes']` frozen
  True; `BOILERPLATE_PHRASES` sorted is `['-', '?', 'n/a', 'na', 'none',
  'nothing', 'same as above', 'see above', 'see below', 'tbd', 'to be
  determined', 'unknown']`; `NO_MATERIAL_DOWNSIDE in BOILERPLATE_PHRASES` is
  FALSE. The substring `resolve` occurs 5 times in the module. The
  deliberate-absence sentence S8 orders reads: "Remedy deliberately does NOT
  resolve a ref or render a staleness badge here, because the resolver is F066
  and is unbuilt — a badge with no resolver behind it would be a false live
  indicator, claiming a ref had been checked when nothing checked it."
- G7 the new tests, green then red under mutation, the mutations isolated —
  exit 0 in the primary checkout. `python3 -m pytest
  tests/orchestration/test_decision_evidence.py -q` after C5 → REAL exit 0,
  `15 passed in 0.25s`. In a disposable worktree at C5 under `.remedy-wt/`:
  CONTROL, nothing mutated → REAL exit 0, `15 passed in 0.25s`. The four
  mutations, one at a time with the pristine module restored between each, are
  listed under Deviations; ALL FOUR went RED and NONE left the run green. The
  worktree was removed and pruned; `git worktree list` reads 1 line.
- G8 structure, artifacts, state readers, Open PR Gate, push — exit 0.
  `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/cli/test_golden_path.py -q`, ONE process → REAL exit 0,
  `620 passed in 75.05s (0:01:15)`, `^FAILED` count 0 — EQUAL to the reviewer's
  base measurement. The `^FAILED` extractor was proved NOT BLIND: run over a
  string containing `FAILED tests/x.py::test_y - AssertionError` it matched 1.
  `git diff --name-only 935ef1ed..4fd27d1a` is exactly the eight expected paths;
  BOTH residues EMPTY. `git diff --stat 935ef1ed..4fd27d1a` restricted to
  `apps/` is EMPTY; restricted to `packages/` it holds EXACTLY
  `packages/orchestration/decision_evidence.py` (+275), and to `tests/` EXACTLY
  `tests/orchestration/test_decision_evidence.py` (+223). Insertions from
  `git diff --numstat`: C0a 406, C0b 333, C1 24, C2 49, C3 14, C4 275, C5 223 —
  each single-parent and under 500. `^<<<SLICE ` / `^<<<END ` 0 / 0 in
  `.agent/plan.md`, `.agent/decisions.md`, `.agent/prose_slips.md`,
  `docs/roadmap/features/T5_F032.md`,
  `packages/orchestration/decision_evidence.py` and
  `tests/orchestration/test_decision_evidence.py`, against the CONTROL over the
  C0a blob which reads 4 / 4. `git ls-files .remedy-wt` 0 lines,
  `git worktree list` 1 line, `git branch --list "tmp/*"` 0 lines.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

- `.agent/authored/f032-r3.md` == `.remedy-wt/f032-r3.md`: same sha256
  `8bdf8620…4fdbb6a7`, same 26836 bytes, same 406 lines.
- `.agent/last_block.md` == the same bytes, and the SAME git blob as C0a.
- `.agent/plan.md` == PLANF032R3: byte-equal, negative control (slice minus its
  trailing newline) FALSE.
- `.agent/decisions.md` == pre-commit blob + ONE newline + DEC4: byte-equal, and
  the pre-commit blob is a byte PREFIX.
- `.agent/prose_slips.md` == pre-commit blob + ONE newline + SLIP: byte-equal,
  and the pre-commit blob is a byte PREFIX.
- `docs/roadmap/features/T5_F032.md` == pre-commit blob + ONE newline + FEATA4:
  byte-equal, and the pre-commit blob is a byte PREFIX.
- The two production files carry NO authored text: S1 through S9 specify them
  and the worker wrote the code, as constraint 3 orders.

## Item status

Every ordered Bundle item and every spec item, exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it into `last_block` | done | same git blob as C0a |
| C1 the plan | done | first substantive commit, as constraint 5 orders |
| C2 DECISION F032 D4 and the prose slip | done | DEC4 and SLIP, both appends |
| C3 the feature file's amendment A4 | done | FEATA4 appended |
| C4 the new module | done | `packages/orchestration/decision_evidence.py`, NEW |
| C5 the new tests | done | `tests/orchestration/test_decision_evidence.py`, NEW |
| C6 the handback | done | this commit |
| push | done | outcome reported in the round report, not here |
| S1 module docstring, public API, purity | done | states no I/O, no `decision_queue` import, no cycle in T001b |
| S2 `DECISION_EVIDENCE_REF_KINDS` | done | frozenset of the four F066 strings, with the D2 WHY comment and both comment-only precedents named |
| S3 `NO_MATERIAL_DOWNSIDE`, `UNKEYED_OPTION` | done | exact literals `no material downside identified` and the empty string |
| S4 the three frozen dataclasses | done | fields and order as ordered, all `frozen=True` |
| S5 `BOILERPLATE_PHRASES` | done | 12 members chosen by the worker; case-insensitive on the stripped string; `NO_MATERIAL_DOWNSIDE` excluded by name |
| S6 `evidence_triple_problems` | done | rules (a)-(h), one distinct sentence each, never raises |
| S7 `export_decision_evidence` | done | keys `evidence_refs` and `outcomes`, with the wire-spelling WHY comment |
| S8 deliberate-absence paragraph | done | in the module docstring, quoted under G6 |
| S9 the new test file | done | 15 tests; every assert is on the problem SENTENCE |

## Deviations & assumptions

1. NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. The commits are exactly C0a,
   C0b, C1, C2, C3, C4, C5, C6 in that order — no extra commit, none dropped,
   none reordered. ANY COMMIT MADE BEYOND THE ORDERED SEQUENCE WOULD RECEIVE ITS
   OWN `## Commits` ROW AND ITS OWN ITEM-STATUS ROW; none was made.
2. THE FOUR G7 MUTATION RESULTS, one line each, all inside the disposable
   worktree at C5, with the pristine module restored between each:
   - (i) rule (a) never fires, empty `refs` accepted → REAL exit 1,
     `2 failed, 13 passed in 0.25s`, `^FAILED` count 2. RED.
   - (ii) rule (b) never fires, an unknown kind accepted → REAL exit 1,
     `1 failed, 14 passed in 0.25s`, `^FAILED` count 1. RED.
   - (iii) rule (f) never fires, a boilerplate phrase accepted → REAL exit 1,
     `1 failed, 14 passed in 0.25s`, `^FAILED` count 1. RED.
   - (iv) rule (g)'s missing-option half never fires → REAL exit 1,
     `1 failed, 14 passed in 0.24s`, `^FAILED` count 1. RED.
   NONE OF THE FOUR LEFT THE SUITE GREEN. The colours and counts above are
   OBSERVED; the block named no expected number and no test name.
3. ONE TEST BEYOND S9'S ENUMERATION, declared here rather than left to be found:
   `test_a_malformed_triple_produces_problems_rather_than_raising`. S9 lists one
   test per rule (a)-(h) plus four named additions; this is a thirteenth kind of
   test. It pins S6's own stated property that a malformed triple produces
   problems and never an exception, which nothing else in the file covered. It
   adds no production code and touches no other file. The reviewer rules on
   whether it stands.
4. `.agent/live_review.md` was NOT written, as the Change line orders. NO
   FINDING WAS REGISTERED OR RESOLVED. `R-0710` stays OPEN and was not fixed:
   this round does not edit `packages/orchestration/decision_queue.py`.
5. `.agent/context.md` was NOT rewritten. The Change line does not list it and
   it is accurate as it stands.
6. NO SLICE CONTRADICTED ANYTHING MEASURED. All four slices were applied byte
   for byte from the extracted C0a blob, never retyped.
7. Every numeral the block stated about the round base `935ef1ed` was
   re-measured here and NONE differed: 633319 for `.agent/decisions.md`, 1681
   for `.agent/prose_slips.md`, 7291 for `docs/roadmap/features/T5_F032.md`,
   `325 passed`, `620 passed`, `All checks passed!` at exit 0 for ruff, and `[]`
   at the Open PR Gate. Nothing needed reconciling.
8. Scratch artifacts left in place, by exact path, under the gitignored
   `.remedy-wt/`: `f032-r3-slices.json` (the four extracted slices G4 and G5
   were measured against) and the helper scripts `g3_extract.py`,
   `c1_plan.py`, `c2_appends.py`, `c3_feature.py`, `g6_introspect.py`,
   `g7_mutations.py`, `g8_structure.py`. `git ls-files .remedy-wt` reads 0.
9. A NOTE ON G6'S `resolve` COUNT, reported rather than adjusted: the substring
   occurs 5 times, four of them inside the deliberate-absence paragraph S8
   orders and one in the `DECISION_EVIDENCE_REF_KINDS` WHY comment, which says
   the migration happens "when F066 lands its resolver". The block set no
   required value for this count.
10. No further defect was found this round.

## Open findings

250 open after this round, unchanged: 271 finding paragraphs minus 21 `Done:`
lines, maximum id `R-0710`. No id minted, none resolved.

## Next

The reviewer reviews `935ef1ed..HEAD`, books R3's verdict, and plans T001b — the
emit gate at `decision_queue.list_decisions`, legacy rendering for records with
no triple, and the CI canary a tripleless producer must fail. That round first
edits `packages/orchestration/decision_queue.py`, so `R-0710`'s fix clause binds
it. Phase 1 rule 1 first: re-read `.agent/STOP`.
