# Handback — F033 Hunk-level diff approval · Round 9

## Session

SESSION 3 of feature F033 · round 9 · rounds so far 9

## Range

Review of `0ce3b71a52f229551be7a8bbafb0f405f80d6b8f`..`c474a18681acbef956b6c9b52cac19294b01103c`

## Commits

### 8c212792 docs(f033): save the round 9 block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r9.md` | +391 / -0 | C0a — the reviewer's block saved byte for byte, copied with `shutil.copyfile` |

### c53f5ab1 docs(f033): mirror the round 9 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +275 / -225 | C0b — mirror of the C0a file, ONE blob id shared |

### 4574a42c docs(f033): retarget the plan at the failed-rollback truth
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +18 / -14 | C1 — whole-file PLANF033R9 |

### 488149d2 docs(f033): book the round 8 verdict and register R-0740
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 / -0 | C2 — RECORDF033R9 appended (the round 8 verdict and the R-0740 registration) |

### 2b2c7832 docs(f033): record two round 8 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4 / -0 | C3 — SLIPSF033R9 appended, two dated lines |

### de17f054 fix(f033): derive the apply seam failure sentence from the applier errors
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_apply.py` | +59 / -5 | C4 — the R-0740 repair: `_ROLLBACK_UNFINISHED_PREFIXES`, `_rollback_did_not_finish`, `_failure_lead_sentence`, and the two docstring claims the fix retires |

### da551b48 test(f033): pin that a failed rollback is never called an unchanged repository
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_apply.py` | +81 / -5 | C5 — three tests (8 → 11) and the module docstring's property list |

### c474a186 docs(f033): record R-0740 as landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | C6 — the `Landed: R-0740` line |

### C7 (this commit) docs(f033): hand back the round 9 failed-rollback truth
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C7 — this handback. A handoff cannot table the commit that writes it (R-0149 pattern). |

Every `+/-` cell above is the `+`/`-` column of `git diff --numstat <sha>^ <sha>`,
read from the tool, and compared cell by cell against the insertion column G8
produced: 391, 275, 18, 4, 4, 59, 81, 2 — identical in both readings.

## External actions

- `git worktree add .remedy-wt/f033-r9-mut da551b48…` — created, detached HEAD at `da551b48`.
- `git worktree remove .remedy-wt/f033-r9-mut --force` — removed BY EXACT PATH.
- `git worktree prune` — ran; `git worktree list` afterwards shows only the primary checkout.
- `git push -u origin feature/f033-hunk-approval-v2` — see Next; no PR created, nothing merged.
- No force-push, no history rewrite, no branch deletion, no `gh` command.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a: `ls: cannot access
'.agent/STOP': No such file or directory`. Read again before C7: same, absent. `git status
--porcelain` empty after every one of the eight commits. Branch `feature/f033-hunk-approval-v2`
throughout. `git rev-parse feature/f033-hunk-approval` = `ed04081283081f237d96147da39a07fca0b1ccad`,
unchanged.

**G2 TRANSPORT — PASS.** `<C0a>:.agent/authored/f033-r9.md` is 29545 bytes, sha256
`fd870c48179bda4768dbd5a1c2d8a93d86a3e35acc64a92b775ed97a3796f01f`.
`.remedy-wt/f033-r9-block.md` is 29545 bytes, sha256
`fd870c48179bda4768dbd5a1c2d8a93d86a3e35acc64a92b775ed97a3796f01f`. EQUAL: True.
`git rev-parse <C0b>:.agent/authored/f033-r9.md <C0b>:.agent/last_block.md` prints ONE blob id,
`eec2e4bca75265b51e4e2c1fdd72290c3deb49bc`.

**G3 THE RECORD APPEND at C2 — PASS.** (a) BASE 1471135 bytes + one newline + RECORDF033R9
5939 bytes = 1477075 bytes; the C2 blob is 1477075 bytes and `rebuilt == C2` is True. BASE is a
byte PREFIX of C2: True. C2 ends in exactly one newline: True. (b) N counted at 2. The last 2
blank-line units of the C2 blob equal the slice's paragraphs IN ORDER: True. NEGATIVE CONTROL:
the first appended paragraph is proved to span bytes 1471136–1474177; the control offset 1472656
is inside that span (asserted, not assumed), byte `b'e'` → `b'X'`. READER 1 (whole-blob
reconstruction) rejects the mutant: True. READER 2 (last-N unit comparison) rejects the mutant:
True.

**G4 THE LEDGER at C2 and C6 — PASS.** Counts as `registered lines / distinct · Done: lines /
distinct · Landed: · Gate: · ^Gate: F033 R8 — · open set`:

| Revision | registered | `Done:` | `Landed:` | `Gate:` | `^Gate: F033 R8 — ` | open set |
|---|---|---|---|---|---|---|
| BASE `0ce3b71a` | 300 / 300 | 45 / 43 | 12 | 125 | 0 | 257 |
| C2 `488149d2` | 301 / 301 | 45 / 43 | 12 | 126 | 1 | 258 |
| C6 `c474a186` | 301 / 301 | 45 / 43 | 13 | 126 | 1 | 258 |

Added id BASE→C2: exactly `['R-0740']`. Added ids C2→C6: `[]`. `Landed:` 12 UNMOVED at C2, 12 → 13
at C6, and the added line matches `^Landed: R-0740 — ` with exactly 1 hit. `Done:` 45 over 43
UNMOVED throughout — I wrote no `Done:` paragraph. The C2 blob is a byte PREFIX of the C6 blob:
True.

**G5 THE PROSE FILES — PASS.** `.agent/plan.md` at C1 is 2442 bytes and byte-EQUAL to
PLANF033R9: True. Line count 45, under the 50-line cap AGENTS.md sets: True.
`.agent/prose_slips.md`: BASE 19985 bytes + one newline + SLIPSF033R9 775 bytes = 20761 bytes;
the C3 blob is 20761 bytes and `rebuilt == C3` is True; BASE is a byte PREFIX: True. Lines
matching `^2026-\d\d-\d\d · F033 R8 · ` — at BASE 0, at C3 2. Lines beginning `- R-` in the whole
file at C3: 0.

**G6 THE REPAIR AGAINST THE SPEC at C4 — PASS.**
(a) `python3 -B -m ruff check packages/orchestration/hunk_apply.py` → REAL exit 0, summary line
`All checks passed!`.
(b) FULL AST import list at C4: `['__future__.annotations', 'collections.abc.Iterable',
'dataclasses.dataclass', 'packages.orchestration.hunk_subset_diff.ApprovedSubsetDiff',
'packages.orchestration.hunk_subset_diff.SubsetRefusal',
'packages.orchestration.hunk_subset_diff.build_approved_subset_diff',
'packages.orchestration.source_apply.apply_structured_patch',
'packages.orchestration.structured_patch.StructuredPatch',
'packages.orchestration.structured_patch.UnifiedDiff', 'pathlib.Path', 'typing.Any', 'uuid.UUID']`
— 12 entries, UNCHANGED from BASE: True. `packages.orchestration.permissions` absent: True;
`packages.orchestration.approval_queue` absent: True;
`packages.orchestration.repository_snapshot` absent: True.
(c) `HUNK_APPLY_REFUSED = 'subset_refused'`, `HUNK_APPLY_CONFLICT = 'conflict'`,
`HUNK_APPLY_NOTHING_TO_APPLY = 'nothing_to_apply'` — exactly the three ordered values: True. No
fourth module-level CODE constant was added: the `HUNK_APPLY_*` set at C4 equals the whole
module-level uppercase constant set at BASE. The one module-level name added is
`_ROLLBACK_UNFINISHED_PREFIXES = ('rollback_failed:', 'rollback_incomplete ')`, which is the
applier's rollback vocabulary and not a failure code — reported explicitly so the reviewer
measures it rather than discovers it.
(d) `apply_approved_hunks(diff_text: str, approved_hunk_ids: Iterable[str], repo_path: Path, *,
job: Any, intent_id: str, data_dir: str | None=None, job_id: UUID | None=None) ->
HunkApplyOutcome` — UNCHANGED from BASE: True. `HunkApplyOutcome` fields `['applied: bool',
'apply_id: str', 'landed: tuple[str, ...]', 'blocked: tuple[str, ...]', 'code: str', 'message:
str']` — UNCHANGED from BASE: True.
(e) THE SENTENCE, measured by CALLING the shipped function, printed verbatim:

    _failure_lead_sentence([])
      -> 'No approved hunk was applied; the repository is unchanged. '
    _failure_lead_sentence(['rollback_failed:snapshot_not_found'])
      -> 'No approved hunk was applied, and the rollback did not finish, so the repository may still hold part of the change — inspect it before re-diffing. '
    _failure_lead_sentence(['rollback_incomplete (1 file(s)): a.txt'])
      -> 'No approved hunk was applied, and the rollback did not finish, so the repository may still hold part of the change — inspect it before re-diffing. '

The first is byte-identical to the string the BASE module hard-codes, trailing space included:
True (the BASE literal `'No approved hunk was applied; the repository is unchanged. '` was
confirmed present in the BASE source before the comparison). The second and third each differ
from the first: True, True. Neither contains `the repository is unchanged`: True, True.

**G7 THE BEHAVIOUR AND THE MUTATION RED-PROOFS at C5 — PASS.**
Primary checkout: `python3 -B -m pytest tests/orchestration/test_hunk_apply.py -q` → REAL exit 0,
`11 passed in 0.27s`. 11 exceeds the 8 BASE gives.
The four digests, taken by running the shipped test
`test_a_rollback_that_could_not_run_is_not_reported_as_an_unchanged_repository` BY NAME with a
recording wrapper around the suite's own `_tree_digests` (the wrapper delegates and returns the
real result, so the test's behaviour is unaltered):

    f.txt BEFORE 5757e4a559c2d85e49c2abd50b019a7bff9ff25991dd9ff1b9c355e39c0b8ab9
    f.txt AFTER  9794694830dabd6ac53554baca77bb4778f069b5d1d6e638049dd403d5066ca3
    f.txt DIFFER True
    g.txt BEFORE 07c2b5ce9dcff0a1c5c5b1d06674a73320223baee2cab7ff4fe4cf41b721b365
    g.txt AFTER  07c2b5ce9dcff0a1c5c5b1d06674a73320223baee2cab7ff4fe4cf41b721b365
    g.txt EQUAL  True

Disposable worktree `.remedy-wt/f033-r9-mut` at `da551b48`, `python3 -B` with
`PYTHONDONTWRITEBYTECODE=1` and every `__pycache__` purged before each run. Import path proved
FIRST: `import packages.orchestration.hunk_apply` resolves to
`/home/decodeux/Repos/remedy/.remedy-wt/f033-r9-mut/packages/orchestration/hunk_apply.py` —
inside the worktree: True.

| Run | anchor unique | REAL exit | summary | failures |
|---|---|---|---|---|
| UNMUTATED CONTROL | — | 0 | `11 passed in 0.29s` | 0 |
| (i) `_rollback_did_not_finish` returns False unconditionally | 1 occurrence | 1 | `1 failed, 10 passed in 0.30s` | 1 |
| (ii) `_rollback_did_not_finish` returns True unconditionally | 1 occurrence | 1 | `2 failed, 9 passed in 0.31s` | 2 |
| REVERTED CONTROL | — | 0 | `11 passed in 0.29s` | 0 |

Names of the failing tests:
- (i) `tests/orchestration/test_hunk_apply.py::test_a_rollback_that_could_not_run_is_not_reported_as_an_unchanged_repository`
- (ii) `tests/orchestration/test_hunk_apply.py::test_a_rollback_that_finished_still_reports_an_unchanged_repository`
- (ii) `tests/orchestration/test_hunk_apply.py::test_a_failure_that_never_reached_a_file_still_reports_an_unchanged_repository`

Both mutations went RED. Each was reverted fully before the next, verified by comparing the file
back to the original bytes. The worktree was removed BY EXACT PATH and pruned; `git worktree
list` then shows only `/home/decodeux/Repos/remedy`. The primary checkout's `git status
--porcelain` was empty throughout.

**G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time, every REAL exit 0:

| Suite | REAL exit | count | BASE |
|---|---|---|---|
| `tests/orchestration/test_hunk_apply.py` | 0 | 11 passed | 8 |
| `tests/orchestration/test_source_apply.py` | 0 | 34 passed | 34 |
| `tests/orchestration/test_hunk_subset_diff.py` | 0 | 17 passed | 17 |
| `tests/orchestration/test_hunk_approval.py` | 0 | 30 passed | 30 |
| `tests/regression/test_resource_safety.py` | 0 | 21 passed | 21 |
| `tests/cli/test_golden_path.py` (canary) | 0 | 42 passed | 42 |

`git rev-list --reverse BASE..C6` walk — every commit exactly ONE parent, insertions from the `+`
column of `git diff --numstat` alone:

| Commit | parents | insertions | <500 |
|---|---|---|---|
| `8c212792` | 1 | 391 | yes |
| `c53f5ab1` | 1 | 275 | yes |
| `4574a42c` | 1 | 18 | yes |
| `488149d2` | 1 | 4 | yes |
| `2b2c7832` | 1 | 4 | yes |
| `de17f054` | 1 | 59 | yes |
| `da551b48` | 1 | 81 | yes |
| `c474a186` | 1 | 2 | yes |

Path set BOTH directions: in range but not in the change set — `[]`; in the change set but not in
the range — `['.agent/handoff.md']`, the sole expected absence, written by C7. Delimiter residue:
`.agent/plan.md` 0/0, `.agent/prose_slips.md` 0/0, `packages/orchestration/hunk_apply.py` 0/0,
`tests/orchestration/test_hunk_apply.py` 0/0, for `<<<SLICE ` and `<<<END ` respectively; the
non-zero CONTROL `.agent/authored/f033-r9.md` reads 5 and 6 (three real slice pairs plus the
conventions' and G8's own quoted mentions). `git ls-files .remedy-wt` reads 0. Do-not-touch paths,
byte-identical at BASE and at C6 by blob id — 9 of 9:

- `packages/orchestration/source_apply.py` `3ca8033856d1` IDENTICAL
- `packages/orchestration/hunk_approval.py` `25d1a8d0d08d` IDENTICAL
- `packages/orchestration/hunk_subset_diff.py` `6c47c2083795` IDENTICAL
- `packages/orchestration/hunk_identity.py` `0c0d51877aeb` IDENTICAL
- `packages/orchestration/ui_server.py` `df581292f384` IDENTICAL
- `apps/cli/command_catalog.py` `2c71af53fae4` IDENTICAL
- `tests/ui_server/test_command_channel.py` `7ff931e2f005` IDENTICAL
- `docs/roadmap/STATUS.md` `a370be066b7a` IDENTICAL
- `.agent/context.md` `4e3a3f2d9c3f` IDENTICAL

## The two failure sentences the module now chooses between

Verbatim, trailing space included, as `_failure_lead_sentence` returns them:

    predicate FALSE: "No approved hunk was applied; the repository is unchanged. "
    predicate TRUE:  "No approved hunk was applied, and the rollback did not finish, so the repository may still hold part of the change — inspect it before re-diffing. "

The reviewer's own wording was used verbatim for the true branch. The false branch is byte-for-byte
the string the BASE module hard-coded.

## The three tests and the property each pins

- `test_a_rollback_that_could_not_run_is_not_reported_as_an_unchanged_repository` — THE PROPERTY.
  With `packages.orchestration.source_apply.load_snapshot` substituted to return None over the
  two-file conflict fixture: `applied` false, `code` is `HUNK_APPLY_CONFLICT`, the message does
  NOT contain `the repository is unchanged`, the message DOES carry
  `rollback_failed:snapshot_not_found` through from the applier, and the tree digests after the
  call DIFFER from those before — `f.txt` named as the file that moved, `g.txt` as one that did
  not. The disk assertion is what makes this a test about the world rather than about wording.
- `test_a_rollback_that_finished_still_reports_an_unchanged_repository` — DISCRIMINATOR 1. The
  same fixture with no substitution: the message contains `the repository is unchanged` and the
  digests are EQUAL before and after. Without it, a predicate returning true always would pass.
- `test_a_failure_that_never_reached_a_file_still_reports_an_unchanged_repository` —
  DISCRIMINATOR 2. `_approved_job(allow_write=False)` on the same fixture: the applier refuses on
  the capability before touching anything, neither `rollback_failed` nor `rollback_incomplete`
  appears in the message, the message contains `the repository is unchanged`, and the digests are
  EQUAL before and after.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `8c212792`, copied with `shutil.copyfile`, 29545 bytes, sha256 matches the reviewer's original |
| C0b mirror it | done | `c53f5ab1`, ONE blob id `eec2e4bc` shared with the C0a file |
| C1 `.agent/plan.md` | done | `4574a42c`, byte-EQUAL to PLANF033R9, 45 lines |
| C2 the round 8 verdict and the R-0740 registration | done | `488149d2`, RECORDF033R9 appended, N=2 |
| C3 two dated lines into `.agent/prose_slips.md` | done | `2b2c7832`, SLIPSF033R9 appended |
| C4 the R-0740 repair in `hunk_apply.py` | done | `de17f054` |
| C5 its tests in `test_hunk_apply.py` | done | `da551b48`, 8 → 11 |
| C6 the `Landed: R-0740` line | done | `c474a186` |
| C7 the handback | done | this commit |
| SPEC §1 derived failure sentence | done | `_ROLLBACK_UNFINISHED_PREFIXES`, `_rollback_did_not_finish`, `_failure_lead_sentence`; `code` unchanged, no fourth code, both deliberate absences written into the comment |
| SPEC §2 module docstring atomicity paragraph | done | fallback scoped to "WHENEVER THAT RESTORE FINISHES"; the exception stated in the present tense |
| SPEC §2 the `landed` closing sentence | done | first clause kept; the reason replaced with the real one |
| SPEC §2 test module docstring | done | in C5 with the tests, property list extended, byte-identical claim scoped to the completed rollback |
| SPEC tests: property + 2 discriminators | done | three tests, named for the property each pins |
| G1 hygiene | done | STOP absent both times, clean tree after every commit, `feature/f033-hunk-approval` still `ed040812` |
| G2 transport | done | 29545 / `fd870c48…` on both sides, EQUAL; ONE blob id at C0b |
| G3 the record append | done | 1471135 + 1 + 5939 = 1477075, prefix, N=2, both readers reject the control |
| G4 the ledger | done | 300→301 (added `R-0740`), `Done:` 45/43 unmoved, `Landed:` 12→13, `Gate:` 125→126, open 257→258 |
| G5 the prose files | done | plan 2442 bytes / 45 lines; slips 19985 + 1 + 775 = 20761; R8 slip lines 0→2; `- R-` 0 |
| G6 the repair against the SPEC | done | ruff exit 0, imports unchanged, three codes intact, signature and fields unchanged, all three sentences printed |
| G7 behaviour and mutations | done | 11 passed exit 0; four digests reported; both mutations RED at exit 1 |
| G8 suites and structure | done | six suites all real exit 0; eight single-parent commits, max 391 insertions; path sets match; residue 0; 9/9 do-not-touch identical |

## Authored-text proofs

Three reviewer-authored slices applied this round, all extracted from the COMMITTED C0a blob
(`8c212792:.agent/authored/f033-r9.md`), never retyped:

- PLANF033R9 → `.agent/plan.md` at C1. 2442 bytes. Disk-to-disk: the C1 blob is byte-EQUAL to the
  extracted slice — True.
- RECORDF033R9 → `.agent/live_review.md` at C2. 5939 bytes. Disk-to-disk: BASE + one newline +
  slice reconstructs the C2 blob byte for byte — True; BASE a byte PREFIX — True.
- SLIPSF033R9 → `.agent/prose_slips.md` at C3. 775 bytes. Disk-to-disk: BASE + one newline +
  slice reconstructs the C3 blob byte for byte — True; BASE a byte PREFIX — True.

The C0a file itself is byte-identical to the reviewer's own pre-emission original at
`.remedy-wt/f033-r9-block.md`: 29545 bytes, sha256
`fd870c48179bda4768dbd5a1c2d8a93d86a3e35acc64a92b775ed97a3796f01f` on both sides.

## Deviations & assumptions

No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6, C7, in
that order, one commit each, no extra commit, none dropped, none reordered.

1. **A THIRD SITE ASSERTS THE ABSOLUTE THE FIX RETIRES AND THE SPEC DID NOT ORDER IT REPAIRED —
   left byte-identical on purpose, and this is the one thing I most want read.**
   `HunkApplyOutcome`'s own docstring in `packages/orchestration/hunk_apply.py` still says
   "``landed`` is EMPTY whenever ``applied`` is false — a caller must not have to check two
   fields to learn that nothing landed, because there is no partial landing to distinguish it
   from." The FIRST clause is still true and the module docstring's twin was repaired by SPEC §2;
   the REASON clause is the same absolute the round retires, because after a rollback that did
   not finish there IS a partial landing on disk. I ran the block's own grep myself across the
   five modules and both suites of this seam at BASE — `nothing-applied`, `falls back to
   nothing`, `no partial landing`, `repository is unchanged`, `byte-identical` — and it returns
   seven hits: `hunk_apply.py:14` and `:17` (SPEC §2 bullets 1 and 2, repaired), `:82` (this
   one), `:205` (the sentence itself, replaced), `test_hunk_apply.py:6` (SPEC §2 bullet 3,
   repaired), plus `hunk_subset_diff.py:15` and `hunk_identity.py:112`, which really are about a
   different property — byte-identical TEXT comparison, not repository state. The block's
   "two hits … deliberately left alone" therefore resolves, by file and by count, to
   `hunk_subset_diff.py:15` and `hunk_apply.py:82`, so `:82` sits inside the SPEC's leave-alone
   set and §1's "Everything not named below stays byte-identical" forbids me touching it. I
   followed the SPEC rather than editing past it. Two facts about that leave-alone clause are
   nonetheless worth the reviewer's eye: (a) it attributes the hit to "`hunk_apply.py`'s
   `_blocked_ids` docstring", and `_blocked_ids`'s docstring contains none of the five grepped
   strings — the hit is in `HunkApplyOutcome`'s docstring; and (b) calling that hit "about a
   DIFFERENT property" does not hold, since it asserts the same absolute as the `:17` hit the
   SPEC ordered repaired. Both are prose, damaged nothing on disk, and I have changed nothing on
   account of them. If the reviewer agrees, one more comment-only edit closes it.
2. **`_ROLLBACK_UNFINISHED_PREFIXES` is a module-level uppercase constant.** G6(c) orders "no
   fourth module-level *code* constant"; this is the applier's message vocabulary, not a failure
   code, and no caller matches on it. It is named privately for that reason and reported
   explicitly in the G6 transcript so the reviewer measures it rather than discovers it.
3. **G6(e) was satisfied against the BASE literal, verified rather than recalled.** Before
   comparing, I asserted that `'No approved hunk was applied; the repository is unchanged. '`
   really is present in the BASE source of `hunk_apply.py`, so "byte-identical to the sentence
   the BASE module hard-codes" rests on a measurement and not on my reading of the block.
4. **G7's four digests were taken by running the shipped test function BY NAME**, with a
   recording wrapper around the suite's own `_tree_digests` that delegates to the real one and
   returns its result unchanged. No assertion in the test was relaxed and no committed file was
   edited to obtain them. This was necessary because the digests live inside the test's own local
   scope and the block asked for them for that test specifically.
5. **`.agent/context.md` was not touched**, per the change-set section; it is confirmed
   byte-identical at BASE and at C6 in the G8 table above.
6. No verdict on this round's work is written anywhere by me, and no `Done:` paragraph was
   authored — the ledger's `Done:` counts are 45 lines over 43 distinct at BASE, at C2 and at C6.

## Next

Reviewer gates round 9. If it passes, the next work item is the hunk-decision ledger in evidence
— approved, rejected and pending hunks with the rejection reasons kept VERBATIM — which
`.agent/plan.md` now places ahead of the write door because it is what the door's effect writes.
