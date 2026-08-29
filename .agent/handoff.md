# Handback — F033 Hunk-level diff approval, round 22

## Session

SESSION 6 of feature F033 · round 22 · rounds so far 22 (25-round soft limit)

Branch: `feature/f033-hunk-approval-v2`. Base of this round: `0bcae480`.

## Range

Review of `0bcae480`..C6, where C6 is the commit that writes THIS file. Its SHA is not
quoted here because a handback cannot know the SHA of the commit that carries it, and an
unmeasured SHA is worse than an absent one. The last SHA this file can state is C5,
`92d0349c`; C6 is its only child.

## Commits

### b2823fc5 docs(f033): save the round 22 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r22.md | +314/-0 | C0a — the block copied byte for byte with `shutil.copyfile` |

### 09e9ab04 docs(f033): mirror the round 22 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +234/-220 | C0b — the same bytes mirrored |

### 4e2e910e docs(f033): rewrite the plan for round 22
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +12/-11 | C1 — full rewrite from slice PLAN22 |

### 61d2ffe7 docs(f033): book the round 21 verdict and register R-0747
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4/-0 | C2 — slice RECORD22 appended |

### 72dcfd53 fix(f033): replace the false no-stored-decision clause with the measured route
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_loop.py | +9/-6 | C3, SPEC A1/A2 — the R-0747 repair |
| .agent/live_review.md | +2/-0 | C3, SPEC A3 — the single `Landed: R-0747` line |

### a8f3de52 feat(f033): add import_hunk_ledger, the inverse of the ledger export
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/hunk_ledger.py | +48/-0 | C4, SPEC B — the function plus its `Public API::` entry |

### 92d0349c test(f033): pin the ledger import round trip, totality and order
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_hunk_ledger.py | +146/-0 | C5, SPEC C — appended only, prefix preserved |

### C6 (this commit) docs(f033): hand back round 22
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | (self-reference) | C6 — this file. A handback cannot table the commit that writes it (R-0149 pattern); the reviewer measures its insertions. |

## External actions

- `git worktree add .remedy-wt/r22-mut 92d0349c` — created, detached at `92d0349c`.
- `git worktree remove .remedy-wt/r22-mut` — succeeded WITHOUT `--force`, as in round 21.
- `git worktree prune` — ran; `git worktree list` afterwards shows the primary checkout only.
- `git push -u origin feature/f033-hunk-approval-v2` — `0bcae480..92d0349c`, accepted.
- A second push carries C6. No PR was created, edited or merged; `main` was not touched.

## Verification

All eight gates ran at C5, before this handback. One line per gate with its REAL exit code.

**G1 TRANSPORT — REAL_EXIT=0.** Committed `.agent/authored/f033-r22.md` sha256
`0cc435b93d1d5f1320640483c6f23e13000df235d0d3863550455f7119cc2e14` over 25718 bytes,
identical to `.remedy-wt/f033-r22-block.md`'s digest and length; `cmp` between the two was
SILENT at REAL_EXIT=0, and `.agent/last_block.md` is byte-identical to the same source.

**G2 THE PLAN — REAL_EXIT=0.** `.agent/plan.md` is 2577 bytes over 46 lines, byte-EQUAL to
slice PLAN22, under the 50-line cap, and holds both `## Goal` and the substring `Steps`.

**G3 THE RECORD APPEND (measured at C2 `61d2ffe7`) — REAL_EXIT=0.** 1580194 + 1 + 7989 =
1588184, and the committed size at C2 is 1588184. The pre-commit blob (`4e2e910e`) is a byte
PREFIX; the slice is an exact SUFFIX; the separator byte at offset 1580194 is a newline. N
was COUNTED by the script at 2, paragraph lengths 4926 and 3060. Two independent readers —
reader A splitting the blob on the blank-line separator, reader B a line-walk state machine
grouping non-blank runs — each found the file's LAST 2 blank-line units equal to the slice's
2 paragraphs IN ORDER. Negative control: byte offset 1582658, inside the first appended
paragraph's span 1580195..1585121, flipped `'e'` to `'E'`; BOTH readers rejected the flipped
bytes and BOTH accepted the unflipped ones.

**G4 THE LEDGER — REAL_EXIT=0.** Registered `^- R-\d+ — ` 307 distinct at `0bcae480` going
to 308 at C2 and C3, the ADDED id set exactly `{R-0747}`. `^Done: R-\d+ — ` 52 lines over 50
distinct, UNMOVED at all three revisions. `^Landed: ` 18 at base and at C2, 19 at C3;
`^Landed: R-0747 — ` 0, 0, then exactly 1 at C3. `^Gate: F033 R21 — ` 0 before, exactly 1
after. Open set (registered distinct minus resolved distinct) 257 going to 258.

**G5 THE CODE AGAINST THE SPEC — REAL_EXIT=0.** `python3 -m ruff check` over all three
changed files: "All checks passed!", REAL_EXIT=0. By AST, `import_hunk_ledger` is defined at
MODULE level in `hunk_ledger.py` with no leading underscore and sits DIRECTLY after
`export_hunk_ledger` in the module-level function order; its name appears in the module
docstring's `Public API::` block; `pingpong_loop.py` contains ZERO occurrences of the string
`persists NOTHING` and does contain the key `hunk_decisions`. RUNNING the shipped function
over a ledger whose states are `['approved', 'rejected', 'pending']`:
`import_hunk_ledger(export_hunk_ledger(L)) == L` is True.

**G6 MUTATION RED-PROOFS — REAL_EXIT=0 for the script; each mutation's own pytest exit code
below.** Run in the disposable worktree `.remedy-wt/r22-mut` ONLY, `__pycache__` purged
before every run, `python3 -B`, `-p no:cacheprovider`. UNMUTATED CONTROL FIRST: REAL_EXIT=0,
44 passed. Every anchor was asserted to occur EXACTLY ONCE in
`packages/orchestration/hunk_ledger.py` (count 1 reported for each of the three), and after
each mutation the file was restored and its sha256 proved equal to the committed blob.
  - (i) round trip made LOSSY (`reason=reason` → `reason=""`): REAL_EXIT=1, 3 failed / 41
    passed — `test_the_export_and_the_import_are_inverses_over_all_three_states`,
    `test_a_rejection_reason_survives_the_round_trip_byte_for_byte`,
    `test_a_stored_rejection_reaches_the_repair_renderer_verbatim`.
  - (ii) SPEC B4's structural guard REMOVED (the whole `try`/`except` deleted and the body
    dedented): REAL_EXIT=1, 9 failed / 35 passed — all nine cases of
    `test_no_malformed_input_makes_the_import_raise`: `[none]`, `[non-mapping]`,
    `[bare-string]`, `[no-rows-key]`, `[non-iterable-rows]`, `[row-not-a-mapping]`,
    `[row-missing-a-key]`, `[list-instead-of-mapping]`, `[non-subscriptable]`. This mutation
    reddened tests; the "it reddened nothing" outcome G6(ii) permits did NOT occur.
  - (iii) an unknown `state` NORMALISED to pending on import: REAL_EXIT=1, 1 failed / 43
    passed — `test_an_unknown_state_imports_intact_rather_than_being_normalised`.
  - Control re-run after all three restores: REAL_EXIT=0, 44 passed.

**G7 THE SUITES, SERIALLY, in the PRIMARY checkout — every REAL_EXIT=0.**
`tests/orchestration/test_hunk_ledger.py` 44 passed; `test_hunk_repair_findings.py` 17
passed; `test_hunk_approval.py` 30 passed; `test_hunk_decision_record.py` 15 passed;
`test_builder_prompt_hunk_rejections.py` 14 passed; `test_builder_prompt_golden.py` 21
passed; canary `tests/cli/test_golden_path.py` 42 passed in 20.71s.

**G8 STRUCTURE — REAL_EXIT=0.** `git status --porcelain` EMPTY (raw output `''`). Every
commit C0a through C5 is single-parent, with insertions 314, 234, 12, 4, 11, 48 and 146 —
each under 500. The path set over `0bcae480`..`92d0349c` EQUALS the declared change set
minus `.agent/handoff.md` in BOTH directions: measured-minus-declared is empty and
declared-minus-measured is empty, over the seven paths.

Additional obligation, Constraint 4 (ORDERED EQUALITY for the code append): the pre-commit
blob of `tests/orchestration/test_hunk_ledger.py` (11798 bytes, 298 lines) is a byte-exact
PREFIX of the post-commit file (18265 bytes, 444 lines); the C5 diff REMOVES 0 lines and the
146 lines it ADDS equal the 146 appended lines IN ORDER.

## Authored-text proofs

- `.agent/authored/f033-r22.md` — copied from `.remedy-wt/f033-r22-block.md` with
  `shutil.copyfile`, never retyped. `cmp` against the source: SILENT, REAL_EXIT=0.
- `.agent/last_block.md` — same bytes, same source, byte-identical (proved in G1).
- Slice PLAN22 (2577 bytes) — extracted by script between its markers and written whole;
  `.agent/plan.md` is byte-EQUAL to it (G2).
- Slice RECORD22 (7989 bytes) — extracted by script and appended unmodified; proved an exact
  SUFFIX of the C2 blob, and its 2 paragraphs matched IN ORDER by two independent readers (G3).
- The `Landed: R-0747` line of SPEC A3 was applied verbatim as the block spells it. No `Done:`
  paragraph was written.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed exactly:
no extra commit, none dropped, none reordered.

1. **A SEVENTH test beyond SPEC C's ordered six.** SPEC C says "Cover at least" and names C1
   through C6; I appended one more,
   `test_a_broken_field_value_is_coerced_rather_than_emptying_the_ledger`. Reason: SPEC B4
   claims the STRUCTURAL guard and the COERCION guard are separate, and none of the ordered
   six discriminates them — without it, either guard could stand in for the other unnoticed.
   It feeds a row whose `id` has a broken `__str__` and asserts the row SURVIVES as
   `"<BrokenText>"` rather than emptying the ledger. No path outside the change set was touched.
2. **Function-local imports in the new tests.** `import_hunk_ledger` and
   `render_rejection_findings` are imported INSIDE each new test rather than in the file's
   import block. This is what SPEC C directs ("otherwise import inside the new tests") and it
   is also forced: the existing import block is outside the appended region, and ruff's `E402`
   is selected repo-wide with no per-file ignore for `tests/**`, so a second module-level
   import block appended mid-file would have failed G5's lint.
3. **Stale prose left in place, deliberately, in the test file's module docstring.** That
   docstring enumerates "The properties, in the order they appear below" and its list now
   stops short of the seven appended tests. SPEC C forbids editing one existing line, so I
   applied the append as ordered and declare the staleness here rather than repairing it on
   my own initiative. It is a candidate for the next round or for a prose slip; I registered
   nothing and touched `.agent/prose_slips.md` not at all, as the change set requires.
4. **SPEC A's replacement paragraph does NOT name `import_hunk_ledger`.** SPEC A2 asks for
   the module and the key, and that is what the paragraph names. I deliberately did not name
   the new function there: C3 lands BEFORE C4, so a cross-reference to it would have been
   dangling in the commit that introduced it. The paragraph says what is missing is "the step
   between — reading that key for the current attempt and rebuilding a ledger from its rows",
   which describes the wiring without pointing at a symbol that did not yet exist.
5. **G6(ii)'s mutation form.** I removed the whole `try`/`except` and dedented the body — a
   genuine removal — rather than narrowing the caught exception class, so the red-proof
   measures the guard's absence and not a weakened variant of it.
6. **G6(i) reddened MORE than the ordered minimum.** The block predicted "the verbatim test
   goes RED"; three tests went red, because the round-trip equality test and the
   stored-rejection-to-renderer test also read the reason. More red than ordered, declared
   rather than folded into "as expected".
7. **G3's flip offset was chosen by the script, not fixed in advance.** It walks forward from
   the first appended paragraph's midpoint to the next ASCII letter, landing on 1582658, and
   the script proves that offset inside the span 1580195..1585121 rather than asserting it.

No gate came out RED, so nothing was repaired on my own initiative and no test or assertion
was weakened.

## Open findings

258 open (registered distinct 308 minus resolved distinct 50), measured at C3 and unchanged
at C5. R-0747 was REGISTERED by slice RECORD22 at C2 and carries a `Landed:` line at C3; it
is NOT counted as resolved, because only a reviewer-authored `Done:` paragraph resolves an
id and this worker wrote none.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Bundle 1 — C0a, block to `.agent/authored/f033-r22.md` | done | `shutil.copyfile`; `cmp` silent, exit 0 |
| Bundle 2 — C0b, mirror into `.agent/last_block.md` | done | same bytes; byte-identical |
| Bundle 3 — C1, rewrite `.agent/plan.md` from PLAN22 | done | byte-EQUAL, 46 lines |
| Bundle 4 — C2, append RECORD22 to `.agent/live_review.md` | done | exact suffix; R-0747 registered |
| Bundle 5 — C3, SPEC A repair plus the `Landed:` line | done | one commit, both paths |
| Bundle 6 — C4, `import_hunk_ledger` | done | 48 insertions, lint clean |
| Bundle 7 — C5, tests appended | done | append-only, ordered equality proved |
| Bundle 8 — C6, rewrite `.agent/handoff.md` | done | this file |
| A1 — replace the false clause, keep the true half | done | call site unchanged / always `None` kept verbatim in sense |
| A2 — state only the measured storage route | done | names the module and the `hunk_decisions` key, no line numbers |
| A3 — one `Landed: R-0747` line, no `Done:` | done | exactly 1 at C3, 0 before; no `Done:` written |
| B1 — public inverse, placed after the export, listed in `Public API::` | done | AST proves order and the docstring entry |
| B2 — reuse `_EXPORT_ROOT_KEY` / `_EXPORT_ENTRY_KEYS`, document the `id`→`hunk_id` rename | done | both constants reused; the rename opens the docstring |
| B3 — TOTAL on every input | done | nine malformed inputs, no raise (G6 control, G7) |
| B4 — ONE structural guard, no inner layer; `_total_text` stays the coercion guard | done | single `try`; G6(ii) reddens 9 tests, so the guard is observable |
| B5 — round trip equals the ledger | done | asserted with `==` on the whole frozen ledger |
| B6 — no `state`/`landing` vocabulary validation, documented | done | DELIBERATE ABSENCE paragraph; pinned by the unknown-state test |
| C1 — round trip over all three states | done | `test_the_export_and_the_import_are_inverses_over_all_three_states` |
| C2 — reason survives byte for byte | done | `test_a_rejection_reason_survives_the_round_trip_byte_for_byte` |
| C3 — stored rows reach the renderer verbatim | done | `test_a_stored_rejection_reaches_the_repair_renderer_verbatim` |
| C4 — totality, parametrized | done | `test_no_malformed_input_makes_the_import_raise`, 9 cases |
| C5 — order preserved | done | `test_the_import_preserves_the_order_the_export_wrote`, non-lexicographic |
| C6 — unknown state intact | done | `test_an_unknown_state_imports_intact_rather_than_being_normalised` |
| SPEC C extra | deviated | a seventh test added under "Cover at least"; deviation 1 |
| G1 TRANSPORT | done | exit 0 |
| G2 THE PLAN | done | exit 0 |
| G3 THE RECORD APPEND | done | exit 0 |
| G4 THE LEDGER | done | exit 0 |
| G5 CODE AGAINST THE SPEC | done | exit 0 |
| G6 MUTATION RED-PROOFS | done | control exit 0; all three mutations exit 1 |
| G7 THE SUITES | done | seven suites, every exit 0 |
| G8 STRUCTURE | done | exit 0; tree clean, path set equal both ways |

## Next

The reviewer re-runs G1 through G8 over `0bcae480`..HEAD, reads the real diff, and
writes the round 22 verdict together with the authored `Done: R-0747` resolution that
replaces the `Landed:` line. The next build round is the SUPPLY step `.agent/plan.md` names:
read `job.metadata["hunk_decisions"]` for the current attempt in the run loop, rebuild the
ledger with `import_hunk_ledger`, and pass it to `compose_builder_prompt`, carrying the
two-round end-to-end the Acceptance asks for.
