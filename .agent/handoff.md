# Handback — F033 Hunk-level diff approval · ROUND 12 · THE RECORDER LEARNS THE VIEWER'S ENVELOPE

## Session

SESSION 3 of feature F033 · round 12 · rounds so far 12

THIS WAS THE LAST DELEGATED ROUND OF SESSION 3. SESSION 3 is carried forward; the next
session opens as SESSION 4 of F033 and its first actions, in this order, are:

1. read `.agent/STOP` from disk;
2. run the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`);
3. book THIS round's verdict into `.agent/live_review.md` — no verdict on round 12 exists yet,
   because the worker writes none;
4. then the CLI command of the plan's step 2 — the `patch.approve_hunks` catalog entry and its
   handler TOGETHER, in the `patch` group beside `patch.approve` and `patch.apply`.

## Range

Review of `624818e6`..HEAD, where HEAD is the C6 handback commit that writes this file. Its SHA
is deliberately NOT quoted here: it is unknowable at authoring time and an invented one would be
worse than an absent one. The seven commits BEFORE it are `624818e6`..`8867c10f`, tabled below.

## Commits

### ea59b739 docs(f033): save the round 12 step block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r12.md` | +407/-0 | C0a — the reviewer's block, produced with `shutil.copyfile`, never retyped |

### df4c3e91 chore(f033): mirror the round 12 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +256/-291 | C0b — the same bytes read back from the committed C0a blob; one blob id with C0a |

### b6871e7b docs(f033): retarget the plan at the viewer envelope seam
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +29/-27 | C1 — whole-file PLANF033R12 |

### 62760bac docs(f033): book the round 11 verdict and resolve R-0742
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4/-0 | C2 — RECORDF033R12: the round 11 `Gate:` line and the `Done: R-0742` resolution |

### c0b10aec docs(f033): record the round 11 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4/-0 | C3 — the dated SLIPSF033R12 lines |

### 06874522 feat(f033): record a hunk decision from the viewer envelope
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_decision_record.py` | +94/-13 | C4 — `record_hunk_decision_from_view` becomes the one implementation, `HUNK_RECORD_REFUSAL_NO_DIFF` is minted, `record_hunk_decision` becomes a wrapper |

### 8867c10f test(f033): pin the view door's availability refusal
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_decision_record.py` | +153/-1 | C5 — six new properties; the nine existing tests are untouched and still pass |

### C6 (the tip) docs(f033): hand back the round 12 envelope seam
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | whole-file rewrite | C6 — the round 12 handback. Its SHA and its `+/-` cells are not quoted: a handoff cannot table the commit that writes it (R-0149 self-reference), and an unmeasured number is worse than a named absence. |

Every `+/-` cell above is `git log --numstat`'s own output, and every insertion cell was
compared cell by cell against the per-commit insertion column G8 measured independently from
`git diff --numstat <rev>^ <rev>`: 407, 256, 29, 4, 4, 94, 153 — identical in both readings.

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add --detach .remedy-wt/g7-r12 8867c10f` | created, detached at C5 |
| `git worktree remove --force .remedy-wt/g7-r12` | removed BY EXACT PATH |
| `git worktree prune` | exit 0; `git worktree list` then shows the primary checkout only |
| `git push -u origin feature/f033-hunk-approval-v2` | see the transcript below |

No PR was created, no PR was merged, no branch was deleted, nothing was force-pushed and no
history was rewritten.

## Verification

### G1 HYGIENE — pass
`ls -la .agent/STOP` → exit 2, "No such file or directory", read from disk BEFORE C0a and again
BEFORE C6; absent both times. `git status --porcelain` empty after every one of C0a, C0b, C1, C2,
C3, C4, C5. Branch `feature/f033-hunk-approval-v2` throughout (`git branch --show-current`).
`git rev-parse feature/f033-hunk-approval` → `ed04081283081f237d96147da39a07fca0b1ccad`, still
`ed040812`. No force-push, no rewrite, no branch deletion.

### G2 TRANSPORT — pass
```
<C0a>:.agent/authored/f033-r12.md : 30167 bytes  sha256 e15f552354d5fbc9a6472535d78195b4f9e08c9e6084e3223f1b7f093565fecf
.remedy-wt/f033-r12-block.md      : 30167 bytes  sha256 e15f552354d5fbc9a6472535d78195b4f9e08c9e6084e3223f1b7f093565fecf
EQUAL: True
git rev-parse df4c3e91:.agent/authored/f033-r12.md -> 3bcfa06bc2d556b0fe8a5dd8dea3d68327f39949
git rev-parse df4c3e91:.agent/last_block.md        -> 3bcfa06bc2d556b0fe8a5dd8dea3d68327f39949
ONE blob id: True
```

### G3 THE RECORD APPEND at C2 — pass
```
(a) BASE .agent/live_review.md : 1506343 bytes (ordered 1506343)
    RECORDF033R12 slice        : 6482 bytes
    C2 blob                    : 1512826 bytes
    BASE + one newline + slice == C2 : True
    BASE is a byte PREFIX of C2      : True
    C2 ends in exactly one newline   : True
(b) N paragraphs COUNTED in the slice : 2
    LAST 2 blank-line units of C2 == the slice's paragraphs IN ORDER : True
    FIRST appended paragraph BYTE span : 1506344 to 1511396 (measured on bytes, convention 10)
    NEGATIVE CONTROL at byte offset 1508870, proved inside that span
      (1506344 <= 1508870 < 1511396 -> True), one bit flipped
    reader 1 (base + newline + slice equality) rejects it : True
    reader 2 (last-N paragraph comparison)      rejects it : True
```

### G4 THE LEDGER at C2 — pass, every ordered reading reproduced
| Reading | BASE | C2 | Ordered |
|---------|------|----|---------|
| `^- R-\d+ — ` lines / distinct ids | 303 / 303 | 303 / 303 | 303 UNMOVED ✓ |
| `^Done: R-\d+ — ` lines / distinct ids | 47 / 45 | 48 / 46 | 47→48 lines, 45→46 distinct ✓ |
| ADDED resolved id | — | `R-0742` | exactly `R-0742` ✓ |
| `^Landed: R-` | 15 | 15 | 15 UNMOVED ✓ |
| `^Landed: R-0742` present beside its new `Done:` paragraph | — | 1 | present ✓ |
| `^Gate: F\d+ R\d+ — ` | 128 | 129 | 128→129 ✓ |
| `^Gate: F033 R11 — ` | 0 | 1 | exactly 1 ✓ |
| `^DECISION F033 D\d+ — ` | 4 | 4 | 4 UNMOVED ✓ |
| OPEN SET (distinct registered − distinct resolved) | 258 | 257 | 258→257 ✓ |

### G5 THE PROSE FILES — pass
```
.agent/plan.md at C1 : 2713 bytes, 49 lines
  byte-EQUAL to PLANF033R12          : True
  under the 50-line AGENTS.md cap    : True (49 < 50)
.agent/prose_slips.md :
  BASE 22079 bytes (ordered 22079); SLIPSF033R12 927 bytes; C3 23007 bytes
  BASE + one newline + slice == C3   : True
  BASE is a byte PREFIX of C3        : True
  '^2026-\d\d-\d\d · F033 R11 · ' at BASE : 0
  '^2026-\d\d-\d\d · F033 R11 · ' at C3   : 2
  lines beginning '- R-' in the whole file at C3 : 0
```

### G6 THE CODE AGAINST THE SPEC at C4 — pass

(a) `python3 -B -m ruff check packages/orchestration/hunk_decision_record.py
tests/orchestration/test_hunk_decision_record.py` → REAL exit 0, summary line
`All checks passed!`

(b) The module's FULL AST import list — 12 `(module, name)` pairs (11 at BASE plus `Mapping`):
```
__future__.annotations                          collections.abc.Iterable
collections.abc.Mapping                         dataclasses.dataclass
datetime.datetime                               typing.Any
packages.orchestration.diff_parser.parse_unified_diff_to_view
packages.orchestration.hunk_approval.HunkApprovalRefusal
packages.orchestration.hunk_approval.decide_hunk_approval
packages.orchestration.hunk_ledger.HunkDecisionLedger
packages.orchestration.hunk_ledger.build_hunk_ledger
packages.orchestration.hunk_ledger.export_hunk_ledger
```
Every entry is standard library or from `packages.orchestration.diff_parser`,
`packages.orchestration.hunk_approval` or `packages.orchestration.hunk_ledger`.
ABSENT: `hunk_apply` True · `source_apply` True · `storage` True · `subprocess` True ·
`shutil` True. Text counts over the whole module: `open(` → 0, `save_job` → 0. DECISION F033 D4
survives this round unchanged — the module the write door will import still drags neither the
applier nor a storage write behind it.

(c) The three module-level refusal-and-key constants:
```
HUNK_DECISIONS_METADATA_KEY            = 'hunk_decisions'       (BASE 'hunk_decisions')       UNCHANGED
HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW = 'untrustworthy_view'   (BASE 'untrustworthy_view')   UNCHANGED
HUNK_RECORD_REFUSAL_NO_DIFF            = 'no_diff_available'    (BASE absent)                 NEW, reads no_diff_available
```

(d) Both extracted signatures:
```
def record_hunk_decision(
    job: Any,
    *,
    task_id: Any,
    attempt: Any,
    attempt_diff_text: str,
    approved: Iterable[str],
    rejected: Iterable[Any],
    now: datetime,
) -> HunkDecisionRecord | HunkApprovalRefusal:

def record_hunk_decision_from_view(
    job: Any,
    *,
    task_id: Any,
    attempt: Any,
    attempt_view: Mapping[str, Any],
    approved: Iterable[str],
    rejected: Iterable[Any],
    now: datetime,
) -> HunkDecisionRecord | HunkApprovalRefusal:
```
`record_hunk_decision` BYTE-IDENTICAL to its signature at BASE: True — both sides sha256
`52b64e15a7acd466c4ad629103955146d1ecc45dcafd9b6c6f958859243b19f9`.

(e) THE WRAPPER HOLDS NO SECOND COPY. `record_hunk_decision`'s AST body, unparsed, is its
docstring plus exactly one statement:
```
"Validate one hunk decision over ``attempt_diff_text`` and RECORD it on ``job``.\n\n    This is the TEXT door of the two. It parses the diff and hands the resulting view to\n    ``record_hunk_decision_from_view``, which holds the implementation and documents the\n    guarantees; a caller that ALREADY has the viewer's envelope should call that one directly\n    rather than serialise a diff it has already parsed."
return record_hunk_decision_from_view(job, task_id=task_id, attempt=attempt, attempt_view=parse_unified_diff_to_view(attempt_diff_text), approved=approved, rejected=rejected, now=now)
```
contains `record_hunk_decision_from_view`: True. ABSENT: `build_hunk_ledger` True ·
`decide_hunk_approval` True · `export_hunk_ledger` True · `setdefault` True.

(f) BOTH shipped entry points exercised once DIRECTLY, not through the tests, on the SAME
two-hunk diff (ids `9875fe8cff31a91a`, `efedcf5048a9537b`) and two separate jobs:
```
text  -> HunkDecisionRecord t-1:2
view  -> HunkDecisionRecord t-1:2
exported records EQUAL   : True
metadata documents EQUAL : True
the record: {'task_id': 't-1', 'attempt': '2', 'decided_at': '2026-08-29T12:30:45',
             'hunks': [{'id': '9875fe8cff31a91a', 'state': 'approved',  'reason': '',             'landing': 'unattempted'},
                       {'id': 'efedcf5048a9537b', 'state': 'rejected', 'reason': 'out of scope', 'landing': 'unattempted'}]}
```

### G7 THE MUTATION RED-PROOFS at C5 — pass, all four RED
Run inside the disposable worktree `.remedy-wt/g7-r12` at `8867c10f`, never in the primary
checkout, with `python3 -B` and `-p no:cacheprovider`. Import resolution proved FIRST:
```
python3 -B -c "import packages.orchestration.hunk_decision_record as m; print(m.__file__)"
exit 0 -> /home/decodeux/Repos/remedy/.remedy-wt/g7-r12/packages/orchestration/hunk_decision_record.py
resolves INSIDE the worktree: True
```
UNMUTATED CONTROL — `pytest tests/orchestration/test_hunk_decision_record.py` → REAL exit 0,
`15 passed in 0.63s`. 15 exceeds the 9 BASE gives.

| # | Mutation | Anchor unique | REAL exit | Failures | Failing test names |
|---|----------|---------------|-----------|----------|--------------------|
| i | skip the availability refusal entirely (`if not attempt_view.get("available", True):` → `if False:`) | 1 | 1 | 2 failed, 13 passed | `test_an_unavailable_envelope_refuses_with_no_diff_quoting_its_reason_and_writes_nothing`, `test_an_unavailable_and_truncated_envelope_answers_no_diff_not_untrustworthy` |
| ii | default `available` to False instead of True | 1 | 1 | 11 failed, 4 passed | the nine existing tests (`test_a_clean_decision_writes_one_record_under_the_composed_attempt_key_unattempted`, `test_the_recorded_rows_carry_the_ledgers_four_keys_in_the_diffs_order`, `test_a_rejection_reason_survives_verbatim_into_the_record`, `test_a_second_decision_on_the_same_attempt_replaces_the_first`, `test_a_decision_on_a_different_attempt_leaves_the_first_record_standing`, `test_a_truncated_view_refuses_and_writes_nothing`, `test_a_decision_refusal_is_returned_unchanged_and_writes_nothing`, `test_unrelated_metadata_keys_survive_the_recording`, `test_the_whole_recorded_document_survives_json_dumps_without_a_custom_encoder`) plus `test_a_view_with_no_available_key_is_treated_as_available_and_records_normally` and `test_both_doors_record_the_same_document_for_the_same_diff` |
| iii | check truncation BEFORE availability | 1 | 1 | 1 failed, 14 passed | `test_an_unavailable_and_truncated_envelope_answers_no_diff_not_untrustworthy` |
| iv | write the record even when the availability refusal fires | 1 | 1 | 2 failed, 13 passed | `test_an_unavailable_envelope_refuses_with_no_diff_quoting_its_reason_and_writes_nothing`, `test_an_unavailable_and_truncated_envelope_answers_no_diff_not_untrustworthy` |

Each anchor was asserted to occur EXACTLY ONCE before it was replaced, and after each mutation
the module was restored and re-read byte-identically to its C5 blob (True in all four cases);
`git status --porcelain` inside the worktree read empty at the end. Nothing was adjusted to force
a red. The worktree was then removed BY EXACT PATH and pruned.

### G8 SUITES AND STRUCTURE — pass
Serially, one pytest process at a time, each a REAL exit 0:
| Suite | Result | BASE |
|-------|--------|------|
| `tests/orchestration/test_hunk_decision_record.py` | exit 0, 15 passed | 9 |
| `tests/orchestration/test_hunk_ledger.py` | exit 0, 29 passed | 29 |
| `tests/orchestration/test_hunk_approval.py` | exit 0, 30 passed | 30 |
| `tests/orchestration/test_hunk_apply.py` | exit 0, 11 passed | 11 |
| `tests/orchestration/test_diff_view_source.py` | exit 0, 15 passed | — |
| `tests/ui_server/test_command_channel.py` | exit 0, 106 passed | 106 |
| `tests/regression/test_resource_safety.py` | exit 0, 21 passed | 21 |
| `tests/cli/test_golden_path.py` (canary) | exit 0, 42 passed | 42 |

`git rev-list --reverse 624818e6..8867c10f` — 7 commits, each with EXACTLY ONE parent, each
under 500 INSERTIONS (the `+` column of `git diff --numstat`, never insertions plus deletions):
```
ea59b739 parents=1 insertions=407  docs(f033): save the round 12 step block
df4c3e91 parents=1 insertions=256  chore(f033): mirror the round 12 block to last_block
b6871e7b parents=1 insertions=29   docs(f033): retarget the plan at the viewer envelope seam
62760bac parents=1 insertions=4    docs(f033): book the round 11 verdict and resolve R-0742
c0b10aec parents=1 insertions=4    docs(f033): record the round 11 prose slips
06874522 parents=1 insertions=94   feat(f033): record a hunk decision from the viewer envelope
8867c10f parents=1 insertions=153  test(f033): pin the view door's availability refusal
```
Range path set, BOTH directions against the declared change set:
```
range path set: .agent/authored/f033-r12.md, .agent/last_block.md, .agent/live_review.md,
                .agent/plan.md, .agent/prose_slips.md,
                packages/orchestration/hunk_decision_record.py,
                tests/orchestration/test_hunk_decision_record.py
range MINUS change set : []
change set MINUS range : []   (`.agent/handoff.md` lands at C6, outside BASE..C5 by order)
```
Delimiter residue at C5, `<<<SLICE ` and `<<<END `:
```
.agent/plan.md                                   : 0 / 0
.agent/prose_slips.md                            : 0 / 0
packages/orchestration/hunk_decision_record.py   : 0 / 0
tests/orchestration/test_hunk_decision_record.py : 0 / 0
.agent/authored/f033-r12.md (non-zero control)   : 5 / 6
```
`git ls-files .remedy-wt` → 0.

The twelve do-not-touch paths, byte-identical at BASE and at C5 BY BLOB ID — 12 of 12:
```
packages/orchestration/hunk_ledger.py       57c00fcfde62 == 57c00fcfde62
packages/orchestration/hunk_apply.py        195f0d223210 == 195f0d223210
packages/orchestration/hunk_approval.py     25d1a8d0d08d == 25d1a8d0d08d
packages/orchestration/hunk_subset_diff.py  6c47c2083795 == 6c47c2083795
packages/orchestration/source_apply.py      3ca8033856d1 == 3ca8033856d1
packages/orchestration/diff_parser.py       b6632f657426 == b6632f657426
packages/orchestration/diff_view_source.py  30a86b1b977d == 30a86b1b977d
packages/orchestration/ui_server.py         df581292f384 == df581292f384
apps/cli/command_catalog.py                 2c71af53fae4 == 2c71af53fae4
apps/cli/commands/patch.py                  051789258623 == 051789258623
tests/ui_server/test_command_channel.py     7ff931e2f005 == 7ff931e2f005
docs/roadmap/STATUS.md                      a370be066b7a == a370be066b7a
```
THE DOOR AND THE CATALOG ARE UNCHANGED THIS ROUND, and that is a measurement rather than a claim.

## The six tests written at C5, and the property each pins

| Test | Property it pins |
|------|------------------|
| `test_an_unavailable_envelope_refuses_with_no_diff_quoting_its_reason_and_writes_nothing` | an envelope with `available` False refuses with `HUNK_RECORD_REFUSAL_NO_DIFF`, carries `hunk_ids == ()`, QUOTES the envelope's own `reason` (`evidence_dir_unavailable`) in its message, and leaves `job.metadata` byte-equal to a pre-call `deepcopy` with the metadata key absent |
| `test_an_unavailable_and_truncated_envelope_answers_no_diff_not_untrustworthy` | a view that is BOTH unavailable AND truncated answers the NO_DIFF code and NOT `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW` — availability is decided first, because an absent artifact was never cut short |
| `test_a_view_with_no_available_key_is_treated_as_available_and_records_normally` | THE RAW-PARSER CASE and the discriminator that stops the `True` default being flipped: it asserts `"available" not in parse_unified_diff_to_view(...)` and then that the recording succeeds with the diff's own id order |
| `test_a_truncated_but_available_envelope_still_refuses_as_untrustworthy` | the pre-existing truncation refusal is unmoved on the view door: code, empty `hunk_ids`, and metadata untouched |
| `test_both_doors_record_the_same_document_for_the_same_diff` | ONE implementation, two doors: the same diff through `record_hunk_decision` and through `record_hunk_decision_from_view`, on two separate jobs, produces EQUAL `exported` dicts and EQUAL metadata documents |
| `test_a_nine_key_viewer_envelope_records_normally` | an envelope carrying exactly the nine keys `build_diff_view` really returns records normally, with every landing `unattempted` and the rejection reason verbatim |

The nine pre-existing tests were not edited and all nine still pass — that is the proof the text
entry point's behaviour did not move.

## Authored-text proofs

| Text | Result |
|------|--------|
| `.agent/authored/f033-r12.md` (C0a) | 30167 bytes, sha256 `e15f5523…5fecf`, byte-identical to the reviewer's pre-emission original `.remedy-wt/f033-r12-block.md`; produced with `shutil.copyfile`, never retyped |
| `.agent/last_block.md` (C0b) | read back from the COMMITTED C0a blob with `git show`; one blob id `3bcfa06b` with C0a |
| PLANF033R12 → `.agent/plan.md` (C1) | extracted from the committed C0a blob; 2713 bytes; byte-EQUAL, 49 lines |
| RECORDF033R12 → `.agent/live_review.md` (C2) | extracted from the committed C0a blob; 6482 bytes; BASE + one newline + slice == C2, byte for byte |
| SLIPSF033R12 → `.agent/prose_slips.md` (C3) | extracted from the committed C0a blob; 927 bytes; BASE + one newline + slice == C3, byte for byte |

No slice was reflowed, re-wrapped or corrected. Every slice was taken as the bytes from the end
of its `<<<SLICE` marker line up to and INCLUDING the newline ending its last content line.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | `ea59b739` |
| C0b mirror it | done | `df4c3e91` |
| C1 `.agent/plan.md` | done | `b6871e7b` |
| C2 round 11 verdict + R-0742 resolution | done | `62760bac` |
| C3 dated line into `.agent/prose_slips.md` | done | `c0b10aec` (the slice carries TWO dated lines — see deviations) |
| C4 the view entry point | done | `06874522` |
| C5 its tests | done | `8867c10f` |
| C6 the handback | done | this file, at the branch tip; its own SHA is not quoted, see Range |
| G1 hygiene | done | STOP absent twice, porcelain empty after every commit, sibling branch `ed040812` |
| G2 transport | done | 30167 bytes both sides, EQUAL; one blob id `3bcfa06b` |
| G3 record append | done | 1506343 + 1 + 6482 = 1512826; N=2; control at byte 1508870 rejected by both readers |
| G4 ledger | done | 303 / 47→48 / 15 / 128→129 / 4 / 258→257, added id `R-0742` |
| G5 prose files | done | plan 2713 bytes 49 lines; slips 22079 + 1 + 927 = 23007; `- R-` 0 |
| G6 code against the SPEC | done | ruff `All checks passed!`; 12 imports; three constants; signature byte-identical; wrapper body clean; both doors EQUAL |
| G7 mutation red-proofs | done | control exit 0 / 15 passed; all four mutations exit 1 |
| G8 suites and structure | done | eight suites exit 0; 7 commits, 1 parent each, max 407 insertions; path set equal both ways; 12/12 do-not-touch identical |
| Push the branch | done | see External actions |
| Create a PR / merge anything | skipped | the block forbids both explicitly |
| Register a finding | skipped | this round registers none, so there is no `Landed:` line and no `Landed:` commit |
| Write a `Done:` paragraph or a verdict | skipped | `Done:` is the reviewer's word and the worker writes no verdict on its own work |

## Deviations & assumptions

1. **The Bundle line for C3 says "one dated line"; the SLIPSF033R12 slice carries TWO dated
   paragraphs, and G5 orders the `^2026-\d\d-\d\d · F033 R11 · ` count at C3 without fixing it.**
   Per convention 1 the slice is applied BYTE FOR BYTE and per convention 11 the gate is
   load-bearing, so both paragraphs landed and the count reads 2 at C3 against 0 at BASE. Nothing
   was reflowed or dropped. Declared here because the Bundle's prose and the slice disagree.
2. **The AST import count is 12, where the round 11 verdict recorded 11 at BASE.** The single
   added entry is `from collections.abc import Mapping`, required by
   `record_hunk_decision_from_view`'s `attempt_view: Mapping[str, Any]` annotation and by the
   widened annotation on the private `_known_hunk_ids`. It is standard library, so G6(b)'s
   property is unaffected, and all five forbidden names are still absent.
3. **`_known_hunk_ids`'s parameter annotation changed from `dict` to `Mapping[str, Any]`.** It is
   a PRIVATE helper, so the SPEC's "every public name keeps its name, its signature and its
   behaviour" is untouched; the change makes the annotation true of the envelopes the view door
   now accepts.
4. **Comment prose on `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW` and one line of the module
   docstring's Public API block were edited.** Both said "the ONE refusal code this module
   mints", which the new constant makes false. G6(c) binds the constant's VALUE, which is
   unchanged at `untrustworthy_view`; only the surrounding prose moved, and it moved because
   leaving it would have shipped a false statement beside a correct gate.
5. **No `.agent/context.md` update.** The block states it is deliberately not touched, and the
   scope and constraints it records did not change this round.
6. No commit was added, dropped or reordered relative to the Bundle: C0a, C0b, C1, C2, C3, C4,
   C5, C6, in exactly that order.
7. No commit exceeded 500 insertions, so the AGENTS.md oversize-commit exception was not used.

## Next

The single expected next action: the PLANNER/REVIEWER opens SESSION 4 of F033 — read
`.agent/STOP` from disk, run the Open PR Gate, gate this round and BOOK ITS VERDICT into
`.agent/live_review.md` (no verdict on round 12 exists yet), then order the plan's step 2, the
`patch.approve_hunks` catalog entry and its handler in ONE round.
