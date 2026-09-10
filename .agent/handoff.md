# Handback — F275 round 28

## Session

SESSION 14 of feature F275 · round 28 · rounds so far 28

## Range

Review of `d3e35f0f`..`HEAD`.

## Commits

### 47400579 F275 R28 C0a: save the round 28 block verbatim as the authored original.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r28.md` | +316 / -0 | the round 28 block saved byte-verbatim as the authored original |

### 1ec9489b F275 R28 C0b: mirror the committed round 28 block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +253 / -358 | round 27's block replaced by the COMMITTED C0a blob |

### 7769c74a F275 R28 C1: point the plan at round 28, the five dead pages and the R-0872 ratchet steps.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17 / -16 | PLAN28 applied byte-for-byte; 45 lines against the cap of 50 |

### 39d85f72 F275 R28 C2: book the round 27 PASS verdict, register R-0873 and record two prose slips.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | LEDGER28 appended: the round 27 PASS gate record and the R-0873 registration |
| `.agent/prose_slips.md` | +4 / -0 | SLIPS28 appended: the two round 27 authoring slips |

### 43374b84 F275 R28 C3: delete the five pages documenting deleted capabilities, drop their index rows, and lower the R-0872 ratchet to 27.
| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +0 / -6 | the six index rows the five pages owned, dropped as whole rows |
| `docs/guides/dogfood-run-user-guide.md` | +0 / -97 | `git rm` — the dogfood run loop is deleted code |
| `docs/guides/self-repair-proposal-user-guide-v0.md` | +0 / -91 | `git rm` — DECISION F260 D3 routes the mechanism to F017's approval gate |
| `docs/system/feature-planner-v0.md` | +0 / -60 | `git rm` — DECISION F274 D6 routes it to NONE |
| `docs/system/progress-ledger-v1.md` | +0 / -77 | `git rm` — DECISION F260 D3 routes it to `job show --full` and `job evidence` |
| `docs/system/run-replay-to-self-repair-proposal-v0.md` | +0 / -111 | `git rm` — the page found only by reading the capability, not by any sweep |
| `tests/cli/test_advertised_commands.py` | +1 / -17 | the 16 allowlist entries those pages carried, and the ceiling 43 -> 27 |

### 7cfd213e F275 R28 C4: cut the dead self-repair section and taxonomy row from the product spine, lowering the R-0872 ratchet to 22.
| Path | +/- | Reason |
|---|---|---|
| `docs/system/core-product-spine-v0.md` | +0 / -17 | the dead `## What self-repair proposals are` section and the `self-repair *` taxonomy row |
| `tests/cli/test_advertised_commands.py` | +1 / -6 | the 5 allowlist entries that page carried, and the ceiling 27 -> 22 |

### C5 — this handback commit
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | the round 28 handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git push -u origin feature/f275-one-world-completion-part-three` — see the push line below.
- No PR created, none edited, none merged. No `gh` command run.
- No `git worktree add` and no `git worktree remove`: this round ordered no
  destructive verification, so guardrail G5 required no disposable worktree and
  `git worktree list` stayed at exactly one entry throughout.

## Verification

One line per gate, each run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

- **G1 TRANSPORT (at C0b) — REAL_EXIT=0.** `sha256sum` over the scratch original
  `.remedy-wt/f275-r28-block.md`, the committed `.agent/authored/f275-r28.md` and
  the committed `.agent/last_block.md` yields ONE distinct digest,
  `05026d2071b930534091721ea51244a9811f75537e53daa526011fa0485cf706`, at 28018
  bytes and 316 lines; both `cmp` runs report byte-equality. This covers the
  scratch original, the saved copy and the mirror. The block travelled as a FILE
  the worker read at a path — no byte of it was retyped from a prompt.
- **G2 THE PLAN (at C1) — REAL_EXIT=0.** `cmp .agent/plan.md .remedy-wt/plan28.txt`
  reports `written == slice`, byte-identical at 2519 bytes. 45 lines against the
  AGENTS.md cap of 50. `grep -c '^## Goal$'` == 1, `grep -c '^## Next Steps$'` == 1.
- **G3 THE RECORD (at C2) — REAL_EXIT=0.** `.agent/live_review.md` pre 767596 (block
  says 767596: True) -> post 775926, slice 8329; `767596 + 1 + 8329 == 775926` True;
  joining byte read back from the committed post-blob at offset 767596 is `b'\n'`.
  `.agent/prose_slips.md` pre 213983 (block says 213983: True) -> post 215418, slice
  1434; `213983 + 1 + 1434 == 215418` True; joining byte at offset 213983 is `b'\n'`.
  The INDEPENDENT structural reader counted N == 2 paragraphs from each slice ITSELF
  and matched the last 2 blank-line units of each whole post-file in order. Negative
  controls: byte 2610 of paragraph 1's 5221 (`b'a'`->`b'X'`) and byte 311 of 623
  (`b' '`->`b'X'`), each flipped INSIDE THE FIRST appended paragraph — reader A and
  reader B both REJECTED both while both accepted the truth. `^Gate: F275 R27 ` == 1,
  `^- R-0873 — ` == 1. THE OPEN SET BY DISTINCT ID: base `d3e35f0f` 101 registrations
  against 13 resolutions == 88; C2 102 against 13 == **89**, as the block requires for
  a commit that registers one and resolves none. No resolution names an unregistered id
  at either revision.
- **G4 THE DELETIONS (at C3) — REAL_EXIT=0.** All five paths PRESENT at `d3e35f0f` and
  ABSENT at `43374b84` — both readings reported per path, because an absence proves
  nothing without the presence before it. The repo-wide basename sweep over
  `docs tests scripts packages apps` returned **0 hits** for all five basenames, so
  nothing survived outside `.agent/` and the round's own block and no STOP condition
  fired. `docs/README.md` 204 -> 198 lines; the six removed rows are printed verbatim
  in the deviations-free transcript and each was measured 1 before / 0 after.
- **G5 THE RATCHET (at C3 and again at C4) — REAL_EXIT=0**, through the worker's own
  import of the edited module, not by grep. At C3: `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)`
  == 27, `_ALLOWLIST_CEILING` == 27, the two EQUAL, stale entries 0. At C4: both == 22,
  EQUAL, stale 0, and the allowlist digest reads
  `7a6b5f4fa5b0ff693acff44b3c181f0b36df05b098d61c08641fb575c96d41d2` — the exact value
  the block ordered. Operator-facing sweep at C4: seen 387, unresolved 38, distinct keys
  22 over exactly TWO paths, `docs/system/architecture.md` and `docs/system/vocabulary.md`.
  Production sweep UNCHANGED at seen 542, unresolved 0.
- **G6 THE SPINE PAGE AND THE SUITE (at C4) — REAL_EXIT=0.** Measured against the
  committed blobs: S2 section at C3 1 -> at C4 0; S2 row at C3 1 -> at C4 0; each
  one-sided per constraint 3, with no TO count claimed. `self-repair` over the whole
  page 7 -> **0**. The page still EXISTS at C4 (`git ls-tree` resolves it), so
  `tests/cli/test_product_spine.py`'s existence pin is intact; 149 -> 132 lines.
  `python3 -B -m pytest tests/docs/ tests/cli/ -q -p no:randomly`, run SERIALLY with no
  `-n auto`: **1649 passed, 0 failed** in 252.08s at exit 0. The canary
  `tests/cli/test_golden_path.py` is INSIDE `tests/cli/` — it is a real file collecting
  42 tests and was therefore inside this run.
- **G7 NOTHING ELSE MOVED (at C4, before C5) — REAL_EXIT=0.** Through the shipped
  reader `apps.cli.command_catalog`: `len(_BASE_CATALOG)` == 222, `len(GROUPS)` == 44,
  dangling `related=` references == 0 over 286 total references — the three figures the
  block pins. UNCHANGED is proved rather than assumed: the range `d3e35f0f..7cfd213e`
  contains NO `apps/` or `packages/` path at all, and `apps/cli/command_catalog.py` is
  byte-identical between base and C4. `.agent/STOP` absent (read from disk),
  `git status --porcelain` EMPTY, `git worktree list` exactly ONE entry, branch
  `feature/f275-one-world-completion-part-three`. `git diff --name-only d3e35f0f..7cfd213e`
  is an EXACT SET MATCH against the change set minus `.agent/handoff.md`: 13 expected,
  13 actual, MISSING none, EXTRA none. Per-commit insertions, cap 500: C0a 316, C0b 253,
  C1 17, C2 8, C3 1, C4 1 — every one OK, and C3 and C4 are one insertion each because a
  deletion carries none, exactly as the block anticipated.
- **Extra, not ordered by the block:** `python3 -m ruff check tests/cli/test_advertised_commands.py`
  reads `All checks passed!` at exit 0. Run as part of the AGENTS.md self-review loop on
  the round's only touched Python file.

## Authored-text proofs

- `.agent/authored/f275-r28.md` — the C0a original, sha256
  `05026d2071b930534091721ea51244a9811f75537e53daa526011fa0485cf706`, byte-equal to the
  scratch original and to the C0b mirror (G1).
- `.agent/plan.md` vs PLAN28 — `cmp` clean, byte-identical (G2).
- LEDGER28 and SLIPS28 — proved by the G3 append arithmetic and the independent
  structural reader, each against the COMMITTED post-blob.
- S1 ROWS, S2 FROM, S2 ROW — each extracted from the COMMITTED C0a blob with
  `git show 47400579:.agent/authored/f275-r28.md`, never retyped, and applied by exact
  whole-unit match with a measured before-count of 1 and an after-count of 0.
- No marker line reached any target file: the extractor rejects a body containing
  `<<<BEGIN` or `<<<END`, and no target contains either token.

## Deviations & assumptions

The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly — no
extra commit, no dropped commit, no reordering. Every authored slice was applied
byte for byte and none was repaired. Deviations and declared doubts:

1. **DECLARED DOUBT — none of the five slices looked wrong.** Every count the block
   predicted reproduced exactly on measurement: the five page lengths (60, 77, 97, 91,
   111), `docs/README.md` 204 -> 198, the six index rows each occurring once, the 16 + 5
   allowlist split across the five pages, the sweep figures 387 / 38 / 22 over two paths,
   the production sweep 542 / 0, the suite at 1649, and the G5 digest
   `7a6b5f4f...c96d41d2` to the character. I found nothing in this block to doubt.
2. **My first `related=` reader was wrong and I corrected it before reporting.** G7 asks
   for the count of dangling `related=` references. My first reader split each reference
   on whitespace and reported **286 dangling**, which would have been a spectacular false
   alarm. The references are DOTTED catalog ids (`job.show`), not spaced pairs, so every
   one of the 286 was being compared against the wrong key shape. The corrected reader
   resolves `f"{group_id}.{subcommand}"` and reports 0 dangling over 286 references. I
   am declaring the wrong reading because it was run, not hiding it because it was wrong.
   This is the R-0859 pattern from memory — nothing in the repository resolves `related=`
   against the catalog, so every deletion round hand-rolls this check and every hand-rolled
   check can pick the wrong key shape.
3. **G7's "unchanged" was strengthened from a single reading to a comparison.** The block
   states the catalog figures "read 222, 44 and 0 at `d3e35f0f` and must be unchanged". A
   measurement at C4 alone shows the value, not the invariance. I added two readings that
   close that: the range contains no `apps/` or `packages/` path at all, and
   `apps/cli/command_catalog.py` is byte-identical between `d3e35f0f` and `7cfd213e`. No
   disposable worktree was needed, so `git worktree list` stayed at one entry for G7.
4. **`.remedy-wt/` scratch is gitignored and confirmed so.** `git check-ignore -v` resolves
   it to `.gitignore:235`. The six extraction scripts and the six extracted slices live
   there and reach no commit; `git status --porcelain` is empty at every verdict.
5. **`__pycache__` was purged before each import-based gate** and every Python invocation
   used `python3 -B`, so no stale bytecode could shadow an edited module in G5 or G7.
6. **The guard file is touched by two commits by design, not by drift.** Constraint 4
   requires it: `test_the_known_dead_doc_advertisement_list_only_ever_shrinks` fails on an
   allowlist entry whose advertisement no longer occurs, so C3 and C4 each remove
   advertisements, their allowlist entries and the ceiling together. I confirmed the guard
   is green at C3 (6 passed) before committing it, so the tree is green at BOTH commits and
   not merely at the end of the round.
7. **Surviving allowlist entries were never retyped or reordered.** Both edits are
   whole-line removals from the in-place line list; the C3 and C4 diffs show only `-` lines
   inside the frozenset plus the one ceiling line changed. The G5 digest at C4 matching the
   block's expected value is the independent confirmation.
8. **Observation carried forward, NOT repaired this round (no scope drift).** The spine
   page's command-taxonomy table still lists `dogfood create/step/show/stop/replay` and
   `self inspect/plan/propose/reconcile` as development-time commands. These are not
   `remedy <x>` advertisements, so no sweep in this round sees them and none of the seven
   gates covers them; `dogfood` in particular names a mechanism this very round deleted the
   user guide for. I did not touch them — the change set is exact and constraint 8 forbids
   widening it. Flagging it as material for R-0873's page-by-page ruling.

## Next

Review this round: re-run G1 to G7 independently against the committed blobs
`d3e35f0f`..`HEAD` and issue the round 28 verdict. The next authored round is
R-0872's second half — the flat pre-Step-38 CLI in `docs/system/architecture.md`
(21 entries) and the one site in `docs/system/vocabulary.md`, taking the allowlist
to zero and deleting the ratchet, `_ALLOWLIST_CEILING` and
`test_the_known_dead_doc_advertisement_list_only_ever_shrinks` with it, which
resolves R-0872. Before authoring it, re-read `.agent/STOP` from disk (Phase 1
rule 1, before rule 2).

Open findings: **89** by distinct id (102 registrations against 13 resolutions),
four of them High — R-0803, R-0804, R-0806 and R-0807, all F273's per DECISION F272 D12.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `47400579` — block saved verbatim, sha256 verified |
| C0b | done | `1ec9489b` — mirrored from the COMMITTED C0a blob |
| C1 | done | `7769c74a` — PLAN28 byte-identical, 45 lines |
| C2 | done | `39d85f72` — LEDGER28 and SLIPS28 appended |
| C3 | done | `43374b84` — five pages `git rm`'d, six rows dropped, 16 entries removed, ceiling 43 -> 27 |
| C4 | done | `7cfd213e` — spine section and row removed, 5 entries removed, ceiling 27 -> 22 |
| C5 | done | this commit — the handback |
| S1 | done | six whole rows, each 1 before / 0 after; `docs/README.md` 204 -> 198 |
| S2 | done | section and row, each 1 before / 0 after; `self-repair` 7 -> 0 on the page |
| G1 | done | exit 0 — one digest across all three copies |
| G2 | done | exit 0 — `written == slice`, 45 lines, both headings 1 |
| G3 | done | exit 0 — arithmetic + structural reader + both negative controls; open set 89 |
| G4 | done | exit 0 — five present before / absent after; sweep 0 hits; README 204 -> 198 |
| G5 | done | exit 0 — 27/27 at C3, 22/22 at C4, digest matches, 387/38/22 over 2 paths, 542/0 |
| G6 | done | exit 0 — 1 -> 0 both units, page exists, suite 1649 passed 0 failed serially |
| G7 | done | exit 0 — 222/44/0 unchanged, exact set match, all insertions under 500 |
| R-0872 | deviated | NOT resolved and not claimed resolved — the ratchet fell 43 -> 22 in two steps; its second half (`architecture.md`, `vocabulary.md`) is the next round |
| R-0873 | done | registered in C2's LEDGER28; `^- R-0873 — ` == 1 |
