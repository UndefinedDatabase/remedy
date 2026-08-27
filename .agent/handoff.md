# Handback — F032 R7 (T002b, the test-failure card)

## Session

SESSION 2 of feature F032 · round R7 · rounds so far 7
Session 1 was R1 through R5; this session began at R6. The soft limit is 25
rounds or 7 sessions, whichever comes first, and neither is near.

## Range

Review of 8c481088d511f9ec67ecd66ca697b59a6c553fc0..389429bb
Branch: `feature/f032-evidence-triple`. Round base: `8c481088`.

## Commits

### 4afc9a57 docs(agent): save the F032 R7 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f032-r7.md | +335 / -0 | C0a, the block saved byte for byte |

### 0d2213dd docs(agent): mirror the R7 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +183 / -252 | C0b, the same blob mirrored |

### b4445723 docs(agent): make the plan describe R7
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +16 / -17 | C1, slice PLANF032R7 |

### 0c67a522 docs(agent): book the R6 verdict and register R-0712
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | C2, slice LEDGER7 as a pure append |

### a25823da fix(orchestration): the test-failure card reads the key its emitter writes
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +10 / -1 | C3, the R-0712 fix (S2) |

### 5d0be41a feat(orchestration): the test-failure card carries its receipts
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +41 / -1 | C4, the refs and the unkeyed outcome (S3, S4) |
| packages/orchestration/decision_evidence.py | +3 / -3 | C4, the gate set and the two retired comments (S5) |

### 389429bb test(orchestration): pin the test-failure card on the key its emitter writes
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_decision_evidence.py | +161 / -1 | C5, the tests (S6) |

### C6 — this handback
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | a handoff cannot table the commit that writes it (R-0149) |

## External actions

- `git worktree add .remedy-wt/f032-r7-mut 389429bb` — created for G7's two
  mutation red-proofs; both mutations ran only there.
- `git worktree remove .remedy-wt/f032-r7-mut --force` and `git worktree prune`
  — removed; `git worktree list` is 1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
  `[]`. Nothing merged, nothing created.
- INTENT: `git push origin feature/f032-evidence-triple` after this commit. Its
  outcome is not a value of any file this round writes, so no exit code and no
  remote tip are stated here; both are in the round's completion report.

## Verification

- G1 hygiene — exit 0. Base before C0a `8c481088d511f9ec67ecd66ca697b59a6c553fc0`,
  branch `feature/f032-evidence-triple`, `git status --porcelain` 0 lines after
  each of C0a…C6, `.agent/STOP` absent at both ordered readings.
- G2 transport — exit 0. Scratch, committed `.agent/authored/f032-r7.md` and
  committed `.agent/last_block.md` all sha256
  `8c021ead99bd006bae021a8eec2e830973f528655ca084282910eea8ec17256a`, 29519
  bytes, 335 lines, all three EQUAL; C0a and C0b are the SAME git blob
  `bd2de27477e1`. This proves the scratch original, the saved copy and the
  mirror agree — not the bytes of any prompt.
- G3 extraction and caps — exit 0. 2 regions: PLANF032R7 44 content lines,
  LEDGER7 3. CONTENT 47, TOTAL 335, PROSE 288. PROSE under 400 and TOTAL under
  490.
- G4 the plan — exit 0. `.agent/plan.md` at C1 byte-equal to PLANF032R7;
  negative control (trailing newline removed) FALSE; `wc -l` 44, under 50;
  `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 the ledger append — exit 0. 1051985 + 1 + 7186 = 1059172, byte-equal, and
  the pre-commit blob is a byte PREFIX. Second reader: N 2, the last two
  blank-line units EQUAL IN ORDER to the slice's two paragraphs; a byte flipped
  in the first appended paragraph (in memory) REJECTED by both readers. Sets
  across C2: `Gate: F<n> R<n>` 58 to 59 adding exactly `F032 R6`; `- R-<n>` 272
  to 273 adding exactly `R-0712`; `Done: R-<n>` 22 to 22; `Landed: R-` 1 to 1;
  `Gate: R<n>` 19 to 19. Open set 250 to 251, maximum id `R-0711` to `R-0712`.
  Unchanged across C3, C4 and C5.
- G6 the code — `ruff check` over both modules exit 0, output verbatim
  `All checks passed!`. Behavioural read-back of three drives is in the round
  report. `TRIPLE_REQUIRED_TYPES` is `test_failure`, `token_budget`. Measured
  for S5: 3 of the 8 producing branches set an `options` key and 5 do not, so
  both retired comments now read "five of the eight producing branches carry no
  options list".
- G7 tests — scoped file exit 0, `46 passed`. Worktree control exit 0,
  `46 passed`. Mutation (a), the R-0712 defect restored, exit 1,
  `1 failed, 45 passed`. Mutation (b), `test_failure` removed from the gate set,
  exit 1, `2 failed, 44 passed`. Neither mutation left the run green. The nine
  decision-schema guard files as ONE pytest process: exit 0, `324 passed`, 0
  `^FAILED` lines with the extractor sighted on a control string.
- G8 structure — golden path exit 0, `42 passed`. Both path residues EMPTY;
  `apps/` and `docs/` diffs EMPTY. Insertions 335, 183, 16, 4, 10, 44, 161 for
  C0a…C5, each single-parent and under 500. Markers 0 and 0 in all five listed
  written files against a CONTROL of 2 and 2 over the C0a blob.
  `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line,
  `git branch --list "tmp/*"` 0 lines. Open PR Gate `[]`.

## Authored-text proofs

- PLANF032R7 — extracted from the COMMITTED C0a blob and written to
  `.agent/plan.md`; disk-to-disk byte comparison EQUAL, negative control FALSE.
- LEDGER7 — extracted from the COMMITTED C0a blob and appended;
  disk-to-disk byte comparison of base + one newline + slice EQUAL, with the
  base a byte PREFIX and both readers rejecting a one-byte mutation.

## State after this round

The emit gate enforces exactly two decision types: `token_budget` (from R6) and
`test_failure` (from this round's C4). The other six producing branches —
`patch_approval`, `stop_reason`, `repo_dirty`, `memory_review`,
`flight_plan_approval` and `task_decision` — still carry the honest legacy
placeholder `recorded_before_evidence_requirements` and are left entirely alone
by the gate.

`R-0712` is FIXED IN CODE at C3 and pinned by a discriminating test at C5, but
it is still OPEN in the record: no worker authors a `Done:` line, so it stays
open until a reviewer writes one. Open findings after this round: 251.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it into last_block | done | same git blob as C0a |
| C1 the plan | done | |
| C2 the R6 verdict and R-0712 | done | pure append |
| C3 the R-0712 fix | done | |
| C4 the triple, the gate set, two retired comments | done | |
| C5 its tests | done | |
| C6 the handback | done | this commit |
| push | done | reported as an intent above; outcome in the round report |
| S1 read first | done | all three strings measured EXACTLY ONCE at the base |
| S2 the R-0712 fix | done | `command_safe`, then `command`, then `"?"`, with the reason at the site |
| S3 the refs | done | run-id ref always, command ref only when resolved and not `?` |
| S4 the unkeyed outcome | done | exactly one, keyed `UNKEYED_OPTION`, no payload added |
| S5 the gate set and two comments | done | measured 5 of 8 branches optionless |
| S6 the tests | done | the exact-membership assertion updated and 10 tests added, only in the file this feature created (36 to 46) |

## Deviations & assumptions

- NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2, C3, C4, C5,
  C6 in exactly that order; no extra commit, no dropped commit, no reordering.
- G7 mutation (b) was measured TWICE and the two readings differ. The first
  reading reported `3 failed, 43 passed`, naming the R-0712 pin among the
  failures, which is not a consequence of removing `test_failure` from the gate
  set. Cause: mutation (a) swaps two dictionary keys of EQUAL total length, so
  the restored source has the same size and the same mtime second as the
  mutated source and CPython reused the stale `__pycache__` byte code. After
  removing every `__pycache__` under the worktree and re-running both mutations
  with byte-code writing disabled, the control is exit 0 `46 passed` before and
  after each mutation, (a) is exit 1 `1 failed, 45 passed` and (b) is exit 1
  `2 failed, 44 passed`. The second reading is the one reported above; the first
  is recorded here because it was really observed.
- A THIRD SENTENCE R6 FALSIFIED WAS FOUND AND DELIBERATELY NOT FIXED. The
  docstring of `test_an_enforced_optionless_decision_reads_no_options_from_the_payload`
  in `tests/orchestration/test_decision_evidence.py` still calls an optionless
  payload "the six-branch case". S5 named the two comments in
  `decision_evidence.py` and said to retire nothing else, so it was left
  untouched. Declared here rather than repaired; the reviewer decides.
- The `#:` block above `TRIPLE_REQUIRED_TYPES` still says the set "held
  `token_budget` alone from T002a". That is past tense and remains true as
  history, so it was not touched.
- `UNKEYED_OPTION` had to be imported into `decision_queue` for S4. Ruff's
  `I001` rejected the first placement; the import now sits where ruff's isort
  ordering requires, directly after `DECISION_EVIDENCE_STATUS_PRESENT`.
- Every reference numeral the block states about the base was re-measured and
  agreed: base bytes 1051985 over 419 blank-line units, ledger counts 58 / 272 /
  22 / 1 / 19, open 250, maximum `R-0711`, ruff `All checks passed!` at exit 0,
  `324 passed` over the nine guard files and `42 passed` on the golden path.
  The three strings S1 names each occur EXACTLY ONCE. Nothing to reconcile.
- No pull request was created and nothing was merged.

## Next

Reviewer re-runs G1 through G8 at `389429bb` and, if it holds, authors the R7
verdict and the `Done:` text for `R-0712`; T002 then continues with the
repo-dirty producer.
