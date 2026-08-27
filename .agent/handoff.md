# Handoff — F032 R1, approval with the evidence triple

## Session

`SESSION 1 of feature F032 · round R1 · rounds so far 1`

Feature F032, round R1. Branch `feature/f032-evidence-triple`, cut from `main`
at the round base `a399a330`
(`a399a3304f9d962cd920c251488c40c486b35fdc`). Soft limit 25 rounds / 7
sessions — not approached.

## Range

Review of `a399a330..HEAD` (this round created every commit in the range).

## Commits

### 9ae08cb8 chore(agent): save the F032 R1 block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f032-r1.md` | +404 / -0 | C0a, byte-for-byte copy of `.remedy-wt/f032-r1.md` via `shutil.copyfile` |

### 9359d743 chore(agent): mirror the F032 R1 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +337 / -323 | C0b, mirror of the C0a file; same git blob |

### 134244a7 chore(agent): open the F032 plan and context
| Path | +/- | Reason |
|---|---|---|
| `.agent/context.md` | +29 / -49 | C1, CTXF032R1 applied byte for byte |
| `.agent/plan.md` | +34 / -35 | C1, PLANF032R1 applied byte for byte |

### afecb4ee docs(roadmap): claim F032 in the status ledger
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1 / -1 | C2, SFROM/STO pair: F032 open to active |

### 7db4d7ed chore(agent): reset the live review header for F032
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +23 / -21 | C3, LFROM/LTO pair, header region only |

### 650bf1a7 docs(agent): put the F032 source inventory on disk
| Path | +/- | Reason |
|---|---|---|
| `.agent/f032_inventory.md` | +369 / -0 | C4, Q1-Q8 each measured |

### C5 — this handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self | a handoff cannot table the commit that writes it (R-0149) |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
  Open PR Gate clear. Nothing merged, nothing created.
- `git checkout -b feature/f032-evidence-triple` from `main` at `a399a330` → branch created.
- INTENT after C5: `git push -u origin feature/f032-evidence-triple`. C5 is
  authored before the push exists, so no exit code and no remote tip is stated
  here; both are in the round's completion report.
- No worktree added or removed. No PR created. No merge.

## Verification

One line per gate, with the real exit code.

- G1 hygiene/branch/sentinel — exit 0. `git rev-parse HEAD` before the cut
  `a399a3304f9d962cd920c251488c40c486b35fdc`; `git branch --show-current` after
  C0a `feature/f032-evidence-triple`; `git status --porcelain` 0 lines after
  each of C0a, C0b, C1, C2, C3, C4; `.agent/STOP` ABSENT before C0a and ABSENT
  before C5.
- G2 transport — exit 0. sha256
  `ae44bcac6839ea2ec4d0242d3d18a54edf7f6b12dcac7d57407d4123d9e01b59`,
  25032 bytes, 404 lines at ALL FOUR points (scratch, C0a, C0b, C4 working
  copy). C0a and C0b are the SAME git blob
  `dc9584b3f2228203d9b0f607495c817a3f5be8af`. Whole-line repeated-character runs
  of length ≥ 4: none.
- G3 extraction and caps — exit 0. 6 slices from the committed C0a blob:
  PLANF032R1 46, CTXF032R1 53, LFROM 24, LTO 26, SFROM 1, STO 1. CONTENT 151,
  TOTAL 404, PROSE 253. PROSE ≤ 400 and TOTAL ≤ 490 both hold.
- G4 plan and context — exit 0. Both BYTE-EQUAL to their slices under the
  newline-INCLUDED convention; both negative controls FALSE. `plan.md`:
  `^## Goal$` 1, `^## Next Steps$` 1, `\bF\d{3}\b` matches `F032`, `wc -l` 46
  (< 50). `context.md`: `^## Active Branch$` 1, `feature/` matches,
  `\bF\d{3}\b` matches `F032`, `Steps` present.
- G5 ledger reset — exit 0. LFROM 1→0, LTO 0→1. Findings region from the first
  byte of `## Findings`: 1023923 bytes, sha256
  `3c0dac3dd2b4a9292722f0ec94598b9aa4c34e0ba255a28aaf896865699081d1` at BOTH
  points, EQUAL. Line-anchored counts unchanged at 270 / 21 / 0 / 19 / 53. All
  four id delta sets EMPTY, ids DISTINCT at both points, max id `R-0709` at
  both, open set 249 at both. `^## Findings$` 1 at both; `Steps` present at both.
- G6 STATUS claim and docs gate — pytest exit 0,
  `325 passed in 0.72s`. `docs/roadmap/STATUS.md` at C2: SFROM 0, STO 1;
  `^- \[ \] ` 197 → 196, `^- \[x\] ` 58 → 58, `^- \[~\] ` 0 → 1; total `^- \[`
  255 → 255, UNCHANGED.
- G7 state readers and canary — pytest exit 0,
  `620 passed in 73.84s (0:01:13)`, `^FAILED` count 0. The extractor was proved
  not blind against a string containing a `FAILED` line.
- G8 structure, artifacts, Open PR Gate — exit 0. Both path-set residues EMPTY.
  `apps/`, `packages/`, `tests/` diffs EMPTY; `docs/` holds
  `docs/roadmap/STATUS.md` alone (+1/-1). Every commit single-parent and under
  500 insertions. `^<<<SLICE ` / `^<<<END ` 0/0 in plan, context and
  live_review at their commits, against the C0a control 6/6.
  `git ls-files .remedy-wt` 0, `git worktree list` 1, `git branch --list
  "tmp/*"` 0. `gh pr list` → `[]`.

## Authored-text proofs

- `.agent/plan.md` == PLANF032R1: byte-equal, negative control (slice minus its
  trailing newline) FALSE.
- `.agent/context.md` == CTXF032R1: byte-equal, negative control FALSE.
- LFROM/LTO and SFROM/STO applied as whole-file `bytes.replace`, each FROM
  occurring exactly once before and zero times after.
- `.agent/authored/f032-r1.md` == `.remedy-wt/f032-r1.md`: same sha256, same
  byte count, same line count.

## Item status

Every ordered item, exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror into `last_block` | done | |
| C1 plan and context | done | |
| C2 STATUS claim | done | |
| C3 live-review header reset | done | |
| C4 the inventory | done | |
| C5 the handback | done | this commit |
| push | done | outcome reported in the round report, not here |
| Q1 enforcement point | done | measured: there is NO enqueue seam |
| Q2 schema as built | done | 13 fields; `payload` the only additive slot; 2 of 9 sites write it |
| Q3 where a decision is persisted | done | measured: no decision store exists |
| Q4 evidence-ref vocabulary | done | measured: the typed vocabulary and its resolver DO NOT EXIST |
| Q5 the options list | done | only 2 of 8 branches carry an options list |
| Q6 the card surface | done | attachment points named at model and render side |
| Q7 migration precedent | done | `DECISION_INBOX_VERSION` has no reader at all |
| Q8 guards a schema change must satisfy | done | `rg` unavailable; equivalent `grep -rlE` run, declared below |

## Deviations & assumptions

1. **WHAT Q1 MEASURED ABOUT THE ENQUEUE SEAM — THERE IS NONE.** The feature
   file states at `docs/roadmap/features/T5_F032.md:31-33` that "the enforcement
   point is the enqueue seam every producer already funnels through (one gate)".
   Measured against the source, that seam does not exist. All eight producing
   branches mint their `HumanDecision` INLINE inside
   `packages/orchestration/decision_queue.py::list_decisions`, which is a
   read-only derivation over eight other subsystems' records — its own docstring
   says so at `decision_queue.py:4-6`. The underlying records are created at 16
   distinct sites across 12 modules, none shared by two branches. Only branch 8
   has anything named like an enqueue (`escalation.enqueue_task_decision`,
   `escalation.py:211`) and it serves that one branch. The one common point is
   `list_decisions` itself — nine `HumanDecision(...)` calls in one function
   body — but that is a DERIVATION point: a gate there can refuse to EMIT a
   tripleless decision, not refuse to CREATE one, because nothing is created.
   The feature file's Design does not survive contact with the source, and the
   reviewer rules on it.
2. Two further measurements bear on the same Design paragraph. Q4: the typed
   provenance vocabulary and the resolver the file names
   (`file/failure/decision` kinds, resolver badges) DO NOT EXIST in code —
   `grep -rn "resolve_ref\|ProvenanceRef\|REF_KIND\|ref_kind" packages/ apps/`
   returns zero lines; they are the unbuilt spec `T3_F066.md:24-40`, and F066 is
   `[ ]` at `STATUS.md:136`. Q3: the "queue storage" the file's Do-not-touch
   list names has no referent — there is no decision store.
3. `rg` is not installed in this session. The Q8 command
   `rg -ln 'decision_queue|HumanDecision|export_decision_json' tests/` raised
   `FileNotFoundError: [Errno 2] No such file or directory: 'rg'`. The
   equivalent `grep -rlE 'decision_queue|HumanDecision|export_decision_json'
   tests/` was run and its real 17-file output is quoted verbatim in the
   inventory. Declared rather than silently substituted.
4. Latent defect measured while answering Q1, NOT fixed and no id minted
   (constraint 7): `decision_queue.py:223` filters memory entries by
   `e.validity in ("stale", "needs_review")`, but `validity` is
   `Literal["active", "stale", "superseded", "contradicted"]`
   (`packages/memory/models.py:44`) — `"needs_review"` is a `review_status`
   value (`models.py:45`), so that half of the predicate can never match. The
   reviewer rules on it.
5. Scratch artifacts left in place, by exact path, under the gitignored
   `.remedy-wt/f032r1/`: the six extracted slice files `PLANF032R1`,
   `CTXF032R1`, `LFROM`, `LTO`, `SFROM`, `STO`. They are the bytes G4's
   byte-equality was measured against; deleting them would remove the evidence.
   `git ls-files .remedy-wt` reads 0.
6. NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. The commits are exactly C0a,
   C0b, C1, C2, C3, C4, C5 in that order — no extra commit, none dropped, none
   reordered. Had any commit been made beyond the ordered sequence it would
   carry its own `## Commits` row and its own item-status row.
7. Not measured, stated as a gap: no vitest ran this round, so the 53 `it(`
   cases in `apps/ui/src/api/decisionCard.test.ts` are a source count, not
   collected tests; and no test was run against a mutated schema, so every
   "would turn red" in Q8 is read from the assertion text, not observed.

## Open findings

249 open, measured at both the pre-C3 blob and the C3 commit: 270 finding
paragraphs minus 21 `Done:` lines, maximum id `R-0709`. NO finding was
registered or resolved this round; all four id delta sets are empty.

## Next

The reviewer reviews `a399a330..HEAD`, books R1's verdict into
`.agent/live_review.md` in the first commit of R2, and rules on the Q1/Q3/Q4
measurements — whether the feature file's Design paragraph is corrected by a
DECISION before T001 is planned. Phase 1 rule 1 first: re-read `.agent/STOP`.
