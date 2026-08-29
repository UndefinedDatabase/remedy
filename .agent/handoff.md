# Handback — F033 Hunk-level diff approval · ROUND 8 · LANDING THE SUBSET

## Session

SESSION 2 of feature F033 · round 8 · rounds so far 8

## Range

Review of `f0dc48f307acb092291ec9bd6763c9557352a1b7`..`HEAD` on
`feature/f033-hunk-approval-v2`. BASE confirmed with `git rev-parse HEAD` before C0a.

## Commits

### 05b734c8 chore(f033): save the round 8 block  (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r8.md` | +341 / -0 | the reviewer's block, copied with `shutil.copyfile`, never retyped |

### fe29a06f chore(f033): mirror the round 8 block to last_block  (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +223 / -246 | the same bytes mirrored; one blob id across both paths |

### 4be37872 docs(f033): retarget the plan on the apply seam  (C1)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +16 / -16 | slice `PLANF033R8`, extracted from the C0a blob |

### 6dcbc15e docs(f033): book the round 7 verdict  (C2)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | slice `RECORDF033R8` appended; base + one newline + slice |

### ad30a99c feat(f033): add the approved-hunk apply seam  (C3)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_apply.py` | +207 / -0 | NEW: `apply_approved_hunks`, `HunkApplyOutcome`, the three codes |

### ee4fbaeb test(f033): pin the all-or-nothing landing of an approved subset  (C4)
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_apply.py` | +294 / -0 | NEW: 8 property tests over a real temporary repository |

### C5 (this commit, self-referential — grouped per R-0149)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | — | this handback; a handoff cannot table the commit that writes it |

No existing module was edited. All seven do-not-touch paths
(`source_apply.py`, `hunk_subset_diff.py`, `hunk_approval.py`, `diff_parser.py`,
`ui_server.py`, `apps/cli/command_catalog.py`, `docs/roadmap/STATUS.md`) are untouched:
the BASE..C4 path set is exactly the change set minus `.agent/handoff.md`.

## External actions

- `git worktree add .remedy-wt/r8-mut ee4fbaeb --detach` — created for G7 only.
- `git worktree remove .remedy-wt/r8-mut --force` then `git worktree prune` — removed BY
  EXACT PATH; `git worktree list` shows the primary checkout alone; the directory is gone.
- `git push -u origin feature/f033-hunk-approval-v2` — `f0dc48f3..ee4fbaeb`, OK. A second
  push carries C5.
- No `gh` command, no PR, no merge, no force-push, no history rewrite, no branch deletion.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a and again before C5:
absent both times (`ls` exit 2, "No such file or directory"). `git status --porcelain`
empty after every one of C0a–C4. Branch `feature/f033-hunk-approval-v2` throughout.
`git rev-parse feature/f033-hunk-approval` = `ed04081283081f237d96147da39a07fca0b1ccad`,
unmoved.

**G2 TRANSPORT — PASS.** `05b734c8:.agent/authored/f033-r8.md` = 23191 bytes, sha256
`18bc25bd6cea6f3f81181d3ee0c5b1680c0be2e590b652a4a7239c0d65061ab3`.
`.remedy-wt/f033-r8-block.md` = 23191 bytes, same sha256. EQUAL: True.
`git rev-parse fe29a06f:.agent/authored/f033-r8.md fe29a06f:.agent/last_block.md | sort -u`
prints ONE blob id: `fa8dc50604abe60b24f1621ce6c8416d513313ad`.

**G3 THE RECORD APPEND at C2 — PASS.** (a) BASE blob 1466257 bytes (ordered value
confirmed), sha256 `547f0d31…c694e38c`; slice `RECORDF033R8` 4877 bytes, sha256
`5212a0f7…52d69453`; 1466257 + 1 + 4877 = 1471135 = the C2 blob, equal BYTE FOR BYTE
(sha256 `8e5428b95b16822d126a37d86fabce68492402d53ea7aa970c9d38a202547dcf`); BASE is a byte
PREFIX; the result ends in exactly one newline. (b) N COUNTED = 1 paragraph; the last 1
blank-line unit of the C2 blob equals the slice's paragraph (4876 bytes each, exact match).
NEGATIVE CONTROL: byte flipped at offset 1466298, PROVEN to lie inside the first appended
paragraph (paragraph starts at 1466258, length 4876) and after BASE; reader A
(reconstruction) rejects it, reader B (paragraph tail) rejects it — BOTH reject.

**G4 THE LEDGER at C2 — PASS, every ordered reading reproduced.**

| Reading | BASE | C2 | Ordered |
|---|---|---|---|
| `^- R-\d+ — ` distinct ids | 300 | 300 | UNMOVED ✓ |
| `^Done: R-\d+ — ` lines / distinct ids | 45 / 43 | 45 / 43 | UNMOVED ✓ |
| `^Landed: R-` | 12 | 12 | UNMOVED ✓ |
| open set (registered − done) | 257 | 257 | UNMOVED ✓ |
| `^Gate: F\d+ R\d+ — ` | 124 | 125 | 124 → 125 ✓ |

`^Gate: F033 R7 — ` at C2 = exactly 1. This round registers and resolves nothing.

**G5 THE MODULE AGAINST THE SPEC at C3 — PASS.**
(a) `python3 -B -m ruff check packages/orchestration/hunk_apply.py` → `All checks passed!`,
REAL EXIT 0.
(b) FULL AST import list: `__future__`, `collections.abc`, `dataclasses`, `pathlib`,
`typing`, `uuid`, `packages.orchestration.hunk_subset_diff`,
`packages.orchestration.source_apply`, `packages.orchestration.structured_patch`.
Required present: `hunk_subset_diff` ✓, `source_apply` ✓. Forbidden absent:
`packages.orchestration.permissions` ✓, `packages.orchestration.approval_queue` ✓ — the
module adds no second permission boundary.
(c) Module-level assignments: `HUNK_APPLY_REFUSED = 'subset_refused'`,
`HUNK_APPLY_CONFLICT = 'conflict'`, `HUNK_APPLY_NOTHING_TO_APPLY = 'nothing_to_apply'` —
each module-level, each matching the SPEC value.
(d) Both `apply_approved_hunks` and `HunkApplyOutcome` are module-level. Extracted
signature:

    apply_approved_hunks(diff_text: str, approved_hunk_ids: Iterable[str], repo_path: Path, *,
                         job: Any, intent_id: str, data_dir: str | None = None,
                         job_id: UUID | None = None) -> HunkApplyOutcome

Extracted field list of the frozen dataclass `HunkApplyOutcome`: `applied: bool`,
`apply_id: str`, `landed: tuple[str, ...]`, `blocked: tuple[str, ...]`, `code: str`,
`message: str` — matching §2 and §3.

**G6 THE ALL-OR-NOTHING PROOF at C4 — PASS.**
`python3 -B -m pytest tests/orchestration/test_hunk_apply.py -q` → `8 passed in 0.27s`,
REAL EXIT 0.
For `test_a_conflicting_hunk_leaves_every_file_byte_identical` specifically, re-run through
the test module's own `_conflict_scenario` helper:

    BEFORE f.txt sha256: 5757e4a559c2d85e49c2abd50b019a7bff9ff25991dd9ff1b9c355e39c0b8ab9
    AFTER  f.txt sha256: 5757e4a559c2d85e49c2abd50b019a7bff9ff25991dd9ff1b9c355e39c0b8ab9
    EQUAL: True

    BEFORE g.txt sha256: 07c2b5ce9dcff0a1c5c5b1d06674a73320223baee2cab7ff4fe4cf41b721b365
    AFTER  g.txt sha256: 07c2b5ce9dcff0a1c5c5b1d06674a73320223baee2cab7ff4fe4cf41b721b365
    EQUAL: True

Outcome: `applied=False`, `landed=()`, `code='conflict'`, `blocked=('c378b64dd1a00f63',)`.
The digests are a ROLLBACK proof and not merely an ordering one: an auxiliary reading of the
same patch through `apply_structured_patch` returns `success=False`,
`errors=['g.txt: diff hunks did not apply cleanly']`, `snapshot_verified=True` and
**`files_modified=1`** — `f.txt` WAS written and then restored to the identical digest.

**G7 THE MUTATION RED-PROOFS at C4 — PASS, all three RED.** Disposable worktree
`.remedy-wt/r8-mut` at `ee4fbaeb`, `python3 -B` with `PYTHONDONTWRITEBYTECODE=1`, primary
checkout never touched. Import path proved FIRST:
`packages.orchestration.hunk_apply.__file__` →
`/home/decodeux/Repos/remedy/.remedy-wt/r8-mut/packages/orchestration/hunk_apply.py`.
Each mutation asserted its anchor UNIQUE (count == 1) before replacing, and was fully
reverted to byte-identical pristine bytes before the next.

| Run | REAL EXIT | Counts | Failing tests |
|---|---|---|---|
| UNMUTATED CONTROL | 0 | 8 passed | — |
| (i) `applied=True` + subset ids even when the applier failed | 1 | 3 failed, 5 passed | `test_a_conflicting_hunk_leaves_every_file_byte_identical`, `test_a_job_without_the_write_capability_lands_nothing_and_blocks_every_id`, `test_an_unapproved_intent_lands_nothing_and_blocks_every_id` |
| (ii) call the applier even when the subset REFUSED | 1 | 1 failed, 7 passed | `test_a_subset_refusal_writes_nothing_and_carries_the_builders_own_code` |
| (iii) attribution always returns every selected id | 1 | 1 failed, 7 passed | `test_the_blocked_ids_of_a_conflict_are_the_conflicting_files_hunks` |
| reverted control | 0 | 8 passed | — |

No mutation came back green. Worktree removed by exact path and pruned;
`git worktree list` shows the primary checkout alone.

**G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time, every REAL
exit 0:

| Suite | REAL EXIT | Count | At BASE |
|---|---|---|---|
| `tests/orchestration/test_hunk_apply.py` | 0 | 8 passed | new file |
| `tests/orchestration/test_source_apply.py` | 0 | 34 passed | 34 ✓ |
| `tests/orchestration/test_hunk_subset_diff.py` | 0 | 17 passed | 17 ✓ |
| `tests/orchestration/test_hunk_approval.py` | 0 | 30 passed | 30 ✓ |
| `tests/regression/test_resource_safety.py` | 0 | 21 passed | 21 ✓ |
| `tests/cli/test_golden_path.py` (canary) | 0 | 42 passed | 42 ✓ |

`git rev-list --reverse BASE..C4`, insertions from the `+` column of `git diff --numstat`:

| Commit | Parents | Insertions | < 500 |
|---|---|---|---|
| `05b734c8` | 1 | 341 | yes |
| `fe29a06f` | 1 | 223 | yes |
| `4be37872` | 1 | 16 | yes |
| `6dcbc15e` | 1 | 2 | yes |
| `ad30a99c` | 1 | 207 | yes |
| `ee4fbaeb` | 1 | 294 | yes |

Every commit has exactly ONE parent. Path set BOTH directions: touched but not in the
change set = `[]`; in the change set but not touched in BASE..C4 = `['.agent/handoff.md']`,
the sole expected absence (it is C5). Delimiter residue: `<<<SLICE ` and `<<<END ` read
0 and 0 in `.agent/plan.md`, 0 and 0 in `packages/orchestration/hunk_apply.py`, 0 and 0 in
`tests/orchestration/test_hunk_apply.py`; the non-zero control
`.agent/authored/f033-r8.md` reads 4 and 5 (2 real slice pairs plus the block's own prose
mentions of the delimiters, including the `<<<END RECORDF033R8` example in Conventions).
`git ls-files .remedy-wt` reads 0.

## Authored-text proofs

Two reviewer-authored texts applied, both extracted from the COMMITTED C0a blob, never
retyped:

- `PLANF033R8` → `.agent/plan.md`: 2123 bytes, sha256
  `f8328ebec58e043a11c6a48a8bac8754d0e1877ea95615053905d232737d6368`, 41 lines, ends in
  exactly one newline.
- `RECORDF033R8` → appended to `.agent/live_review.md`: 4877 bytes, sha256
  `5212a0f7987aa25870597b4a5ec845b8dbf3a4a6b6b0c2609147324152d69453`; reconstruction and
  paragraph-tail proofs under G3.

Block fidelity: the file the reviewer wrote and the committed `.agent/authored/f033-r8.md`
are byte-identical (G2).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `05b734c8`, `shutil.copyfile` |
| C0b mirror it | done | `fe29a06f`, one blob id |
| C1 `.agent/plan.md` | done | `4be37872` |
| C2 round 7 verdict into `.agent/live_review.md` | done | `6dcbc15e` |
| C3 the apply seam module | done | `ad30a99c` |
| C4 its tests | done | `ee4fbaeb` |
| C5 the handback | done | this commit |
| G1 HYGIENE | done | PASS |
| G2 TRANSPORT | done | PASS |
| G3 THE RECORD APPEND | done | PASS, N = 1 |
| G4 THE LEDGER | done | PASS, Gate 124 → 125 |
| G5 THE MODULE AGAINST THE SPEC | done | PASS, ruff exit 0 |
| G6 THE ALL-OR-NOTHING PROOF | done | PASS, 8 passed, two equal digests |
| G7 THE MUTATION RED-PROOFS | done | PASS, 3 of 3 RED |
| G8 SUITES AND STRUCTURE | done | PASS, 152 tests across six suites |

## Confirmations the block asked me to re-derive rather than trust

All three re-read at `f0dc48f3` before the SPEC was relied on:

1. `apply_structured_patch` takes a MANDATORY verified snapshot of
   `build_snapshot_path_set(patch)`, applies each unified diff in turn, and on ANY failure
   calls `_rollback_from_snapshot` and breaks — confirmed at `source_apply.py` lines
   275–318. The atomicity is genuinely inherited.
2. `validate_structured_patch` rejects a `unified_diff` entry with an empty `path` or an
   empty `diff`, and additionally calls `unsafe_path_issues(patch.target_paths)` —
   confirmed at `structured_patch.py` lines 302–312.
3. `build_snapshot_path_set` derives the path set from the `file_ops` and `unified_diffs`
   paths — confirmed at `repository_snapshot.py` lines 353–377.

Also confirmed, because the attribution rule depends on it: `_apply_unified_diff` appends
its errors as `f"{diff.path}: {reason}"`, so the `path + ": "` prefix test is a membership
test against a string the applier really emits (`source_apply.py` lines 414–437), and the
G6 reading `errors=['g.txt: diff hunks did not apply cleanly']` witnesses it.

## Test names and the property each pins

| Test | Property |
|------|----------|
| `test_a_clean_subset_lands_exactly_the_approved_hunks_and_nothing_else` | one approved hunk of two lands; the file's BYTES equal the original with only that hunk's change |
| `test_a_conflicting_hunk_leaves_every_file_byte_identical` | the all-or-nothing proof: `f.txt` is written then restored when `g.txt` conflicts; every file's digest is unchanged, `applied` false, `landed` empty |
| `test_the_blocked_ids_of_a_conflict_are_the_conflicting_files_hunks` | attribution is per-FILE, not a blanket: the clean file's approved hunk is not blamed |
| `test_a_subset_refusal_writes_nothing_and_carries_the_builders_own_code` | a `SubsetRefusal` never reaches the applier; digests unchanged although the FULL diff would have applied; `subset_refused` carrying `absent_hunk` in the message and the offending id in `blocked` |
| `test_a_job_without_the_write_capability_lands_nothing_and_blocks_every_id` | a permission refusal names no file, so the WHOLE selection is blocked |
| `test_an_unapproved_intent_lands_nothing_and_blocks_every_id` | same for the approval boundary; both boundaries stay the applier's, not this module's |
| `test_a_multi_file_subset_lands_both_files` | a subset spanning two files lands both |
| `test_a_subset_with_no_file_never_reaches_the_applier` | an empty subset is `nothing_to_apply` with `apply_id == ""` — no apply id is minted for a mutation that never happened |

## Deviations & assumptions

1. **A block statement that is stronger than the code, declared not routed around.** The
   block's "TWO CONSTRAINTS" says the synthesised patch "must set `target_paths`, not only
   `unified_diffs`, or it fails validation". Re-derived: `validate_structured_patch` calls
   `unsafe_path_issues(patch.target_paths)`, and that function returns `[]` for an EMPTY
   tuple, so an unset `target_paths` would NOT fail validation. Every MEASURED fact the
   block states is true; only the inferred consequence is stronger than the code. The SPEC's
   order was followed exactly anyway — `target_paths` is set to the same paths in the same
   order as `unified_diffs` — so nothing on disk differs from the block's instruction.
2. **`HUNK_APPLY_NOTHING_TO_APPLY` is unreachable through the real builder.**
   `build_approved_subset_diff` refuses an empty approved set (`no_approved_ids`) and refuses
   any id the diff does not carry (`absent_hunk`), so every `ApprovedSubsetDiff` it returns
   has at least one file. The branch ships as a named outcome exactly as SPEC §2 and step 2
   order, is documented as unreachable in the code comment, and is pinned by injection
   (`monkeypatch` of the module's own `build_approved_subset_diff`, plus an applier stub that
   raises if called). Declared rather than hidden, following the round 7 precedent for the
   untrustworthy check's third limb.
3. **G6's "the target file" is TWO files by design.** A single-file conflict never reaches
   the applier's writer at all — `_apply_hunks` returns `None` before any `write_text` — so a
   one-file test would prove ordering rather than rollback. The scenario therefore spans
   `f.txt` (clean, written first) and `g.txt` (its context line drifted on disk). Both files'
   BEFORE/AFTER digests are reported above, and the `files_modified=1` reading proves `f.txt`
   was really written and really restored.
4. **G7 mutation (ii) had to be spelled concretely.** The block orders "call the applier even
   when the subset REFUSED" without saying with what patch. I used the repository's own
   reading of raw diff text — `parse_structured_patch(diff_text)` — so the mutation is
   generic rather than shaped around the test. It went red on the digest assertion, which is
   the property the block wanted pinned.
5. **The two pushes.** The branch was pushed after C4 (`f0dc48f3..ee4fbaeb`) per AGENTS.md
   Push Discipline, and a second push carries C5. No departure from the block's ordered
   commit sequence: C0a, C0b, C1, C2, C3, C4, C5 in that order, no extra commit, none
   dropped, none reordered.

No verdict is written here on this round's own work.

## Next

The write door: expose `approve_hunks` and dispatch it. The door may NOT import
`packages.orchestration.source_apply` — it is in `FORBIDDEN_MODULES` in
`tests/ui_server/test_command_channel.py` — so the command must reach
`apply_approved_hunks` through a service seam, and `TestCommandDoorImportGuard`'s
`ALLOWED_IMPORTS` (an EQUALITY guard) must be widened in the SAME commit that adds the
import, with the decision that widens it.
