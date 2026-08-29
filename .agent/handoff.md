# Handback — F033 Hunk-level diff approval · ROUND 7 · THE APPROVED SUBSET DIFF

## Session

SESSION 2 of feature F033 · round 7 · rounds so far 7

## Range

Review of `1fdda40215da1f15c248df1ea46cf7b940781a74`..`<C5>` on branch
`feature/f033-hunk-approval-v2`. BASE was confirmed with `git rev-parse HEAD` before C0a.

## Commits

### 6620a145 chore(f033): save the round 7 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r7.md | +364/-0 | C0a, the block saved with `shutil.copyfile`, never retyped |

### d797e7d0 chore(f033): mirror the round 7 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +227/-200 | C0b, mirrored from the committed C0a file |

### 6a7d935d docs(f033): retarget the plan on the approved subset diff
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +11/-8 | C1, whole-file slice PLANF033R7 |

### d887643a docs(f033): book the round 6 verdict
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | C2, RECORDF033R7 appended after one newline |

### 42d0a76f docs(f033): record the round 6 reviewer prose slip
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +2/-0 | C3, SLIPSF033R7 appended; the slice opens with its own blank line |

### c4b11af5 feat(f033): build the approved subset diff
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/hunk_subset_diff.py | +278/-0 | C4, the NEW module written from the SPEC |
| tests/orchestration/test_hunk_subset_diff.py | +219/-0 | C4, its 17 property tests |

### C5 — this handback (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewritten | C5; a handoff cannot table the commit that writes it |

C4 totals 497 insertions, under the 500 cap. No commit is oversize and none is declared.

## External actions

- `git worktree add --detach .remedy-wt/f033r7-wt c4b11af5` — created, G7 ran there only.
- `git worktree remove --force .remedy-wt/f033r7-wt` then `git worktree prune` — removed BY
  EXACT PATH; `git worktree list` afterwards shows only the primary checkout.
- `git push -u origin feature/f033-hunk-approval-v2` — run immediately after C5, per Push
  Discipline. No PR created, no `gh` command run, no force-push, no history rewrite, no
  branch deleted.

## Verification

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a and again before C5:
  `ls` exit 2, "No such file or directory", absent both times. `git status --porcelain`
  empty after every one of C0a, C0b, C1, C2, C3, C4. Branch `feature/f033-hunk-approval-v2`
  throughout. `git rev-parse feature/f033-hunk-approval` = `ed04081283081f237d96147da39a07fca0b1ccad`,
  unchanged. No force-push, no rewrite, no branch deletion.
- **G2 TRANSPORT — PASS.** `6620a145:.agent/authored/f033-r7.md` = 24748 bytes, sha256
  `8634f5526f8d8048b69e6837be71656f568083d1a10ef353b247958d233158a4`;
  `.remedy-wt/f033-r7-block.md` = 24748 bytes, same sha256; EQUAL = True.
  `git rev-parse d797e7d0:.agent/authored/f033-r7.md` and
  `git rev-parse d797e7d0:.agent/last_block.md` both print ONE blob id,
  `9d08302b43991069794a281b16db05b8631b6f36`.
- **G3 THE RECORD APPEND at C2 — PASS.** (a) BASE blob 1461741 bytes (as ordered); BASE +
  one newline + RECORDF033R7 (4515 bytes) = 1466257 = the C2 blob byte for byte, True; BASE
  is a byte PREFIX, True; the result ends in exactly one newline, True. (b) N COUNTED in
  RECORDF033R7 = **1**; the LAST 1 blank-line unit of the C2 blob equals the slice's
  paragraph in order, True. NEGATIVE CONTROL: the first appended paragraph was proven to
  span offsets 1461742..1466256, the flip was made at offset **1463999**, asserted inside
  that span, and BOTH readers rejected it (whole-blob equality True, last-N-paragraph
  comparison True).
- **G4 THE LEDGER at C2 — PASS, every reading as ordered.** registered `^- R-\d+ — `
  300 lines / 300 distinct at BASE and 300/300 at C2, UNMOVED. `^Done: R-\d+ — ` 45 lines
  over 43 distinct at BASE and 45 over 43 at C2, UNMOVED. `^Landed: R-` 12 at BASE and 12 at
  C2, UNMOVED. Open set (registered distinct − done distinct) 257 at BASE and 257 at C2,
  UNMOVED — this round registered and resolved nothing. `^Gate: F\d+ R\d+ — ` 123 → **124**.
  `^Gate: F033 R6 — ` at C2 reads exactly **1** (0 at BASE).
- **G5 THE PROSE-SLIPS APPEND at C3 — PASS.** BASE blob 19578 bytes (as ordered); BASE +
  SLIPSF033R7 (407 bytes, opening with its own blank line, no separator added) = 19985 = the
  C3 blob byte for byte, True; BASE a byte PREFIX, True; ends in exactly one newline, True.
  The lines that commit's diff ADDS are exactly the slice's 2 lines IN ORDER, True.
  `^2026-08-29 · F033 R6 · ` at C3 = **1**.
- **G6 THE MODULE AGAINST THE SPEC at C4 — PASS.** (a) `python3 -B -m ruff check` over both
  new files: REAL exit **0**, summary line `All checks passed!`. (b) By AST, the FULL import
  list is `['__future__', 'collections.abc', 'dataclasses', 'packages.orchestration.diff_parser',
  'typing']` — every entry standard library except exactly `packages.orchestration.diff_parser`;
  `source_apply` occurs **0** times anywhere in the module's text. (c) All three constants are
  module-level assignments, in the declared order:
  `SUBSET_REFUSAL_NO_APPROVED_IDS = 'no_approved_ids'`,
  `SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW = 'untrustworthy_view'`,
  `SUBSET_REFUSAL_ABSENT_HUNK = 'absent_hunk'`. (d) TOTALITY as a real probe: `None`,
  `object()`, the integer 7 and a non-iterable id set whose `__iter__` RAISES were each
  passed in BOTH argument positions — 8 calls, all 8 RETURNED, every one a `SubsetRefusal`
  (`absent_hunk`), 0 raised. (e) `open(` 0, `import os` 0, `import subprocess` 0,
  `import logging` 0; `Path` 0 as well, measured though not ordered this round.
- **G7 THE MUTATION RED-PROOFS at C4 — PASS, all three RED.** In the disposable worktree
  `.remedy-wt/f033r7-wt` at `c4b11af5`, under `python3 -B`, never in the primary checkout;
  the gate's own command was proven to import
  `.remedy-wt/f033r7-wt/packages/orchestration/hunk_subset_diff.py`. UNMUTATED CONTROL:
  REAL exit **0**, 17 passed. Each anchor was asserted UNIQUE (count 1) before replacement
  and the module was fully reverted between mutations, each revert re-measured at exit 0 /
  17 passed.
  - (i) swap the `add` and `del` prefixes → REAL exit **1**, 3 failed / 14 passed:
    `test_a_subset_of_every_hunk_applies_exactly_as_the_raw_diff_does`,
    `test_one_approved_hunk_changes_its_own_lines_and_leaves_the_others_alone`,
    `test_the_line_prefix_map_is_load_bearing`.
  - (ii) UNTRUSTWORTHY_VIEW never trips → REAL exit **1**, 4 failed / 13 passed:
    `test_a_hunk_in_a_binary_file_is_refused`,
    `test_a_hunk_in_a_file_the_parser_could_not_read_is_refused_by_name`,
    `test_a_truncated_view_is_refused_and_blames_no_hunk`,
    `test_an_untrustworthy_view_is_reported_before_an_absent_hunk`.
  - (iii) ABSENT_HUNK never trips → REAL exit **1**, 2 failed / 15 passed:
    `test_absent_ids_are_deduplicated_in_the_order_the_caller_gave_them`,
    `test_an_id_the_diff_no_longer_carries_stops_the_apply`.
  No mutation came back green. Worktree removed by exact path and pruned; the primary
  checkout's `git status --porcelain` was empty throughout and after.
- **G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time, every REAL
  exit **0**: `tests/orchestration/test_hunk_subset_diff.py` **17 passed** (new),
  `tests/orchestration/test_hunk_approval.py` 30, `tests/orchestration/test_diff_parser.py`
  50, `tests/orchestration/test_hunk_identity.py` 10,
  `tests/orchestration/test_source_apply.py` 34, canary `tests/cli/test_golden_path.py` 42.
  COMMIT WALK `git rev-list --reverse BASE..c4b11af5`, each exactly ONE parent, insertions
  from the `+` column of `git diff --numstat`: 6620a145 364, d797e7d0 227, 6a7d935d 11,
  d887643a 2, 42d0a76f 2, c4b11af5 497 — all under 500. PATH SET both directions: in the
  range but not in the change set = none; in the change set but not in the range =
  `.agent/handoff.md` only, the expected absence. DELIMITER RESIDUE `<<<SLICE ` / `<<<END `:
  `.agent/plan.md` 0/0, `.agent/prose_slips.md` 0/0,
  `packages/orchestration/hunk_subset_diff.py` 0/0,
  `tests/orchestration/test_hunk_subset_diff.py` 0/0, against the non-zero control
  `.agent/authored/f033-r7.md` at **5** and **6**. `git ls-files .remedy-wt` = **0**.

### The four facts, re-derived rather than trusted

All four hold at `1fdda402`, each with a real red control (script
`.remedy-wt/f033r7/facts.py`):

- The applier never reads a hunk header's NEW side: skewing both `+N,M` headers to `+999,M`
  applies byte-identically (True); `m.group(3)` and `m.group(4)` occur 0 times in
  `_apply_hunks`. RED CONTROL: skewing the OLD side instead changes the result (True) — the
  control's anchor is asserted to match, so it cannot pass vacuously.
- A context mismatch makes `_apply_hunks` return `None` (True); control on the unmodified
  original returns not-None (True).
- `parse_unified_diff_to_view` carries each hunk's `header` VERBATIM (equal to the source
  headers, True), its `lines` with kinds exactly `{add, ctx, del}` and a `content` on every
  entry, and an `id` beside them.
- Re-emitting EVERY hunk from the view applies byte-identically to applying the raw diff
  (True); swapping the `add`/`del` prefixes changes the result (the applier returns `None`).
  Also measured: dropping either hunk applies correctly with NO renumbering.

### `build_approved_subset_diff` — final signature

    def build_approved_subset_diff(
        diff_text: str,
        approved_hunk_ids: Iterable[str],
    ) -> ApprovedSubsetDiff | SubsetRefusal:

### The 17 tests and the property each pins

| Test | Property |
|------|----------|
| test_a_subset_of_every_hunk_applies_exactly_as_the_raw_diff_does | THE ROUND TRIP: selecting both hunks applies byte-identically to applying the raw diff |
| test_one_approved_hunk_changes_its_own_lines_and_leaves_the_others_alone | each hunk alone changes exactly its own lines |
| test_the_line_prefix_map_is_load_bearing | would fail if `add`/`del` were swapped; a swapped emission no longer applies |
| test_a_header_is_re_emitted_character_for_character | headers VERBATIM, and dropping the first hunk does not renumber the second |
| test_an_emitted_file_carries_only_hunks_and_one_trailing_newline | no `diff --git`/`---`/`+++`, exactly one trailing newline |
| test_an_empty_approved_set_is_refused_rather_than_applying_nothing | NO_APPROVED_IDS, with no id blamed |
| test_a_truncated_view_is_refused_and_blames_no_hunk | UNTRUSTWORTHY_VIEW from `truncated`, `hunk_ids` empty |
| test_a_hunk_in_a_file_the_parser_could_not_read_is_refused_by_name | UNTRUSTWORTHY_VIEW from a file `note`, naming the approved id |
| test_a_hunk_in_a_binary_file_is_refused | UNTRUSTWORTHY_VIEW from a `binary` status |
| test_an_untouched_unreadable_file_does_not_refuse_a_clean_selection | the check is scoped to files the SELECTION touches |
| test_an_id_the_diff_no_longer_carries_stops_the_apply | ABSENT_HUNK stops rather than shrinks the apply |
| test_absent_ids_are_deduplicated_in_the_order_the_caller_gave_them | absent ids deduplicated, caller's order |
| test_an_untrustworthy_view_is_reported_before_an_absent_hunk | THE ORDER, on one input tripping two codes |
| test_only_files_with_a_kept_hunk_appear_and_in_the_diffs_own_order | multi-FILE: untouched files absent, diff order not caller order, `selected` spans files |
| test_a_hunk_approved_twice_is_emitted_once_and_is_not_a_refusal | duplicate approval is harmless and emits once |
| test_no_input_raises_in_either_argument_position | TOTALITY over 7 hostile values in both positions |
| test_an_id_that_is_not_a_string_is_compared_as_text | a non-string id is coerced and matches |

## Authored-text proofs

- PLANF033R7, RECORDF033R7, SLIPSF033R7 were all extracted from the COMMITTED C0a blob by
  `git show 6620a145:.agent/authored/f033-r7.md`, anchored to the named delimiter at line
  start, each delimiter asserted UNIQUE; none was retyped.
- Disk-to-disk: `6620a145:.agent/authored/f033-r7.md` is byte-identical to
  `.remedy-wt/f033-r7-block.md` — 24748 bytes, sha256
  `8634f5526f8d8048b69e6837be71656f568083d1a10ef353b247958d233158a4` on both sides.
- The Python module and its tests are a SPEC, not a slice, and were written from the
  description as the block's convention 5 requires.

## Deviations & assumptions

1. **A TENSION IN THE BLOCK, resolved rather than routed around, and declared.** SPEC §1
   orders "Write both absences into the module docstring" while naming the applier as
   `packages/orchestration/source_apply.py`; gate G6(b) orders `source_apply` to read ZERO
   times "anywhere in the module's text". Both are satisfiable at once, so this is a
   constraint rather than a contradiction: I treated G6(b) as the binding MEASUREMENT and
   satisfied §1's intent by writing BOTH `DELIBERATE ABSENCE` paragraphs into the docstring
   — it applies nothing, and it does not import the applier — naming the applier by its
   public entry point `apply_structured_patch` and by `FORBIDDEN_MODULES` in
   `tests/ui_server/test_command_channel.py`, so the absence still greps to something real
   without the forbidden token. That G6(b) is scoped to the MODULE's text, while the test
   SPEC positively orders the test file to import `_apply_hunks` from that same module, is
   what makes the two clauses coherent: the gate is about what the module reaches, not about
   what the round may mention. Nothing on disk is wrong either way.
2. **A KNOWN COVERAGE GAP, stated rather than hidden.** The third untrustworthy limb — a
   line `kind` that is none of `ctx`/`del`/`add` — is UNREACHABLE through the public entry
   point, because `parse_unified_diff_to_view` emits only those three kinds. It is shipped
   because without it `_emit` would `KeyError` if the view ever grew a fourth kind, which
   would break the module's totality claim. No test exercises it: reaching it needs a
   monkeypatched parser, and C4 closed at 497 of its 500 permitted insertions with no room
   for one. Mutation (ii) still goes red on the other two limbs, so the gate is not blind,
   but this limb specifically is guarded by construction rather than by a test.
3. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5
   were committed in exactly that order, one per ordered item, nothing added, dropped or
   reordered. No path outside the declared change set was written.
4. `G6(e)` was measured with the four tokens the block names plus `Path` (0), which the
   round 6 record used; the extra reading is reported, not substituted.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it | done | |
| C1 `.agent/plan.md` | done | |
| C2 the round 6 verdict into `.agent/live_review.md` | done | |
| C3 the reviewer prose slip into `.agent/prose_slips.md` | done | |
| C4 the subset module and its tests | done | 497 insertions, one commit |
| C5 the handback | done | this file |
| G1 HYGIENE | done | PASS |
| G2 TRANSPORT | done | PASS, one blob id |
| G3 THE RECORD APPEND | done | PASS, N=1, control at 1463999 |
| G4 THE LEDGER | done | PASS, Gate: 123 → 124, all else unmoved |
| G5 THE PROSE-SLIPS APPEND | done | PASS, 19578 + 407 = 19985 |
| G6 THE MODULE AGAINST THE SPEC | done | PASS, ruff exit 0, 8/8 totality calls returned |
| G7 THE MUTATION RED-PROOFS | done | PASS, 3/3 red, control 17 passed |
| G8 SUITES AND STRUCTURE | done | PASS, six suites exit 0, C4 at 497 |
| Re-derive the four measured facts | done | all four hold, each with a real red control |

## Next

Round 8: land the subset. Feed each `ApprovedSubsetFile` through the applier as a
`UnifiedDiff(path=..., diff=...)`, all-or-nothing, so a conflict inside the approved set
leaves NOTHING applied and names the hunk that conflicted — the applier already snapshots
and reverts, so the round proves the atomicity rather than building it.
