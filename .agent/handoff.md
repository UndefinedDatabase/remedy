# Handback — F033 Hunk-level diff approval · ROUND 11 · WHAT THE DOOR'S EFFECT IS

## Session

SESSION 3 of feature F033 · round 11 · rounds so far 11

## Range

Review of `97861cdf`..`d8ef9350` (the handback commit follows this file).

## Commits

### fde9b4e5 docs(f033): save the round 11 step block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r11.md` | +442/-0 | C0a — the reviewer's block, copied with `shutil.copyfile`, never retyped |

### 7469e3ea docs(f033): mirror the round 11 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +309/-303 | C0b — same bytes, one blob id with C0a |

### 272fcd43 docs(f033): point the plan at the door decision and the recorder
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +20/-19 | C1 — whole-file PLANF033R11 |

### d48b4850 docs(f033): book the round 10 verdict, R-0741, R-0742 and decision D4
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +8/-0 | C2 — RECORDF033R11: the R10 gate line, the R-0741 resolution, the R-0742 registration, DECISION F033 D4 |

### 25bb5ec3 docs(f033): record two round 10 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4/-0 | C3 — two dated SLIPSF033R11 lines |

### b80a56a1 test(f033): pin the ledger's deliberate none divergence
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_ledger.py` | +14/-1 | C4 — the R-0742 test plus the docstring property line; 28 → 29 cases |

### a5892048 feat(f033): record a hunk decision on the job it belongs to
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_decision_record.py` | +176/-0 | C5 — the new recorder module |

### 50f09338 test(f033): pin the recorder writing a decision and applying nothing
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_decision_record.py` | +248/-0 | C6 — 9 cases |

### d8ef9350 docs(f033): land R-0742 with its own red-proof
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2/-0 | C7 — the worker-authored `Landed: R-0742` line |

### C8 (this commit) docs(f033): hand back the round 11 recorder
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | this file | the handback; a handoff cannot table the commit that writes it |

The `+/-` column above is `git diff --numstat` output, cell for cell, compared against the
per-commit insertion column G8 produced below: they agree in every cell.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it | done | |
| C1 `.agent/plan.md` | done | |
| C2 verdict, R-0741 resolution, R-0742 registration, DECISION F033 D4 | done | |
| C3 two lines into `.agent/prose_slips.md` | done | |
| C4 the R-0742 test in `test_hunk_ledger.py` | done | |
| C5 the recorder module | done | |
| C6 its tests | done | |
| C7 `Landed: R-0742` into `.agent/live_review.md` | done | |
| C8 the handback | done | this file |
| G1 hygiene | done | |
| G2 transport | done | |
| G3 the record append at C2 | done | |
| G4 the ledger at C2 and C7 | done | |
| G5 the prose files | done | |
| G6 the code against the SPEC | done | |
| G7 the mutation red-proofs at C6 | done | four of four RED |
| G8 suites and structure | done | |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/r11wt 50f09338` — created,
  detached HEAD at C6.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r11wt` — removed BY EXACT PATH.
- `git worktree prune` — ran; `git worktree list` then held only the primary checkout.
- `git push -u origin feature/f033-hunk-approval-v2` — pushed after C8.
- No PR created, none edited, none merged. No `gh` command run.

## Verification

**G1 HYGIENE.** `.agent/STOP` read from disk before C0a — `ls: cannot access '.agent/STOP':
No such file or directory` — and again before C8, same result: ABSENT both times.
`git status --porcelain` measured after every one of the nine commits: `0` lines each time.
Branch `feature/f033-hunk-approval-v2` throughout (`git rev-parse --abbrev-ref HEAD`). No
force-push, no history rewrite, no branch deletion; `git rev-parse feature/f033-hunk-approval`
= `ed04081283081f237d96147da39a07fca0b1ccad`, unchanged. `git rev-parse HEAD` before C0a was
`97861cdfef76355bf522db127dc31992eb54e9f5`, the ordered BASE.

**G2 TRANSPORT.** `.remedy-wt/f033-r11-block.md`: **36001 bytes**, sha256
`7b42b486ae1540387ccc8a3cf6cb93df28dfffa6fae4db8b6874d8b91b056303` — verified against the
ordered digest BEFORE any work began. `fde9b4e5:.agent/authored/f033-r11.md`: **36001 bytes**,
sha256 `7b42b486ae1540387ccc8a3cf6cb93df28dfffa6fae4db8b6874d8b91b056303`. **EQUAL: True** on
both readings. `git rev-parse 7469e3ea:.agent/authored/f033-r11.md` and
`git rev-parse 7469e3ea:.agent/last_block.md` print ONE blob id:
`282dcf69b2beecaaf729f74e4811f93227115abd`.

**G3 THE RECORD APPEND at C2.** Real exit 0.
(a) BASE blob **1493203 bytes** (the ordered figure, measured). Slice RECORDF033R11 **11438
bytes**. C2 blob **1504642 bytes**. Reconstruction `1493203 + 1 + 11438 = 1504642`;
`BASE + one newline + slice == C2 blob`: **True**. BASE a byte PREFIX of C2: **True**. C2
ends in exactly one newline: **True**.
(b) N paragraphs COUNTED by the script in the slice: **4**. Last 4 blank-line units of the C2
blob == the slice's 4 paragraphs IN ORDER: **True**. The FIRST appended paragraph's span,
measured in BYTES per convention 10, is C2 offsets **1493204..1498026** (4822 bytes).
NEGATIVE CONTROL at byte offset **1495615**, asserted to satisfy
`1493204 <= 1495615 < 1498026`, one byte replaced (`b' '` → `b'X'`). Reader (a),
reconstruction equality, REJECTS it: **True**. Reader (b), the last-4-paragraph comparison,
REJECTS it: **True**.

**G4 THE LEDGER at BASE, C2 and C7.** Real exit 0.

| metric | BASE | C2 | C7 |
|---|---|---|---|
| registered `^- R-\d+ — ` lines | 302 | 303 | 303 |
| registered distinct ids | 302 | 303 | 303 |
| `^Done: R-\d+ — ` lines | 46 | 47 | 47 |
| `Done:` distinct ids | 44 | 45 | 45 |
| `^Landed: R-` | 14 | 14 | 15 |
| `^Landed: R-0742 — ` | 0 | 0 | 1 |
| `^Gate: F\d+ R\d+ — ` | 127 | 128 | 128 |
| `^Gate: F033 R10 — ` | 0 | 1 | 1 |
| `^DECISION F033 D\d+ — ` | 3 | 4 | 4 |
| `^DECISION F033 D4 — ` | 0 | 1 | 1 |
| OPEN SET (registered distinct − resolved distinct) | 258 | 258 | 258 |

ADDED registered id BASE→C2: exactly **`R-0742`**; C2→C7: **none** (UNMOVED). ADDED `Done:`
id BASE→C2: exactly **`R-0741`**; C2→C7: **none** (UNMOVED) — I authored no `Done:` paragraph.
`Landed:` UNMOVED at 14 across C2, then 14→15 at C7, the added line matching
`^Landed: R-0742 — ` (count 1). Open set **258 UNMOVED** at C2 — one id registered and one
resolved in the same commit — and UNMOVED at C7. The C2 blob is a byte PREFIX of the C7 blob:
**True** (1504642 of 1506343 bytes).

**G5 THE PROSE FILES.** Real exit 0. `.agent/plan.md` at C1: **2472 bytes, 47 lines**,
byte-EQUAL to PLANF033R11 (**True**), and 47 < 50, the AGENTS.md cap.
`.agent/prose_slips.md`: BASE **21213 bytes** (the ordered figure, measured), slice **865
bytes**, C3 **22079 bytes**; reconstruction `21213 + 1 + 865 = 22079`;
`BASE + one newline + slice == C3 blob`: **True**; BASE a byte PREFIX of C3: **True**; C3 ends
in exactly one newline: **True**. Lines matching `^2026-\d\d-\d\d · F033 R10 · ` — BASE **0**,
C3 **2**. Lines beginning `- R-` in the whole C3 file: **0**.

**G6 THE CODE AGAINST THE SPEC.** Real exit 0 on every part.

(a) `python3 -m ruff check packages/orchestration/hunk_decision_record.py
tests/orchestration/test_hunk_decision_record.py tests/orchestration/test_hunk_ledger.py`
— **REAL EXIT 0**, summary line `All checks passed!`.

(b) FULL import list of the recorder by AST, **8 entries**:

    __future__                              stdlib
    collections.abc                         stdlib
    dataclasses                             stdlib
    datetime                                stdlib
    typing                                  stdlib
    packages.orchestration.diff_parser      allowed
    packages.orchestration.hunk_approval    allowed
    packages.orchestration.hunk_ledger      allowed

Every entry is standard library or one of the three allowed package modules: **True**.
Present anywhere in the import list — `hunk_apply` **False**, `source_apply` **False**,
`storage` **False**, `subprocess` **False**, `shutil` **False**. This is DECISION F033 D4
measured rather than asserted: nothing the write door will import drags the applier behind it.
Counts in the module text: `open(` **0**, `save_job` **0**.

(c) Read from the shipped module:

    HUNK_DECISIONS_METADATA_KEY            = 'hunk_decisions'
    HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW = 'untrustworthy_view'

(d) Extracted from the AST at C7:

    record_hunk_decision(job: Any, *, task_id: Any, attempt: Any, attempt_diff_text: str,
                         approved: Iterable[str], rejected: Iterable[Any],
                         now: datetime) -> HunkDecisionRecord | HunkApprovalRefusal
    HunkDecisionRecord fields: [('attempt_key', 'str'), ('ledger', 'HunkDecisionLedger'),
                                ('exported', 'dict')]

Both match §4 of the SPEC exactly.

(e) The SHIPPED function exercised ONCE directly, not through the tests — REAL EXIT **0**. The
import resolved to `/home/decodeux/Repos/remedy/packages/orchestration/hunk_decision_record.py`.
A two-hunk `difflib` diff over a 20-line file gave ids `9875fe8cff31a91a` and
`efedcf5048a9537b`; the first was approved, the second rejected. `attempt_key` came back
`t-1:2`, and `json.dumps(job.metadata["hunk_decisions"]["t-1:2"], indent=2)` printed:

    {
      "task_id": "t-1",
      "attempt": "2",
      "decided_at": "2026-08-29T12:00:00",
      "hunks": [
        {
          "id": "9875fe8cff31a91a",
          "state": "approved",
          "reason": "",
          "landing": "unattempted"
        },
        {
          "id": "efedcf5048a9537b",
          "state": "rejected",
          "reason": "  the second edit is out of scope  ",
          "landing": "unattempted"
        }
      ]
    }

Every entry's `landing` reads **`unattempted`**. `json.dumps` needed **no custom encoder** —
it was called with `indent=2` and nothing else, and `json.loads(json.dumps(entry)) == entry`
is **True**.

**G7 THE MUTATION RED-PROOFS at C6.** In the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/r11wt` at `50f09338`, `python3 -B`, never in the
primary checkout. The imports were proved to resolve to the WORKTREE's own copies FIRST:
`…/.remedy-wt/r11wt/packages/orchestration/hunk_decision_record.py` and
`…/.remedy-wt/r11wt/packages/orchestration/hunk_ledger.py`. Each anchor was asserted UNIQUE
(occurrence count printed) before replacement, and the edited file was restored and its sha256
re-measured after every run.

| run | anchor hits | REAL exit | result | failing test(s) |
|-----|-------------|-----------|--------|-----------------|
| UNMUTATED CONTROL | — | **0** | 38 passed (`test_hunk_decision_record.py` **9**, `test_hunk_ledger.py` **29**, run separately as well as together) | — |
| (i) recorder passes `apply_attempted=True, applied=True` to `build_hunk_ledger` | 1 | **1** | RED, 1 failed 37 passed | `test_a_clean_decision_writes_one_record_under_the_composed_attempt_key_unattempted` |
| (ii) recorder writes the record under `task_id` alone | 1 | **1** | RED, 4 failed 34 passed | `test_a_clean_decision_writes_one_record_under_the_composed_attempt_key_unattempted`, `test_a_second_decision_on_the_same_attempt_replaces_the_first`, `test_a_decision_on_a_different_attempt_leaves_the_first_record_standing`, `test_the_whole_recorded_document_survives_json_dumps_without_a_custom_encoder` |
| (iii) recorder skips the truncated-view refusal and records anyway | 1 | **1** | RED, 1 failed 37 passed | `test_a_truncated_view_refuses_and_writes_nothing` |
| (iv) `hunk_ledger._entries` loses its `None` guard | 1 | **1** | RED, 1 failed 37 passed | `test_a_none_known_set_yields_no_rows_where_another_unusable_value_yields_one` |
| REVERTED CONTROL | — | **0** | 38 passed | — |

Four of four went RED; none came back green. (iv) is R-0742's own red-proof and it is the
discriminating result of this round: the identical edit came back GREEN at `97861cdf`, which
is why the finding exists, and it is red now. Targets restored byte-identically —
recorder `18530054a9b9749d…` before and after, ledger `4425d168a335a9b3…` before and after:
**True**. Worktree removed by exact path, `git worktree prune` run, `git worktree list` then
held only `/home/decodeux/Repos/remedy`.

**G8 SUITES AND STRUCTURE.** Eight suites, SERIALLY, one pytest process at a time, every REAL
exit code captured through a Python runner (the shell rejects `${PIPESTATUS[0]}` by FORM):

| suite | REAL exit | count | BASE |
|-------|-----------|-------|------|
| `tests/orchestration/test_hunk_decision_record.py` | 0 | 9 passed | new this round |
| `tests/orchestration/test_hunk_ledger.py` | 0 | 29 passed | 28 |
| `tests/orchestration/test_hunk_approval.py` | 0 | 30 passed | 30 |
| `tests/orchestration/test_hunk_apply.py` | 0 | 11 passed | 11 |
| `tests/orchestration/test_diff_parser.py` | 0 | 50 passed | 50 |
| `tests/ui_server/test_command_channel.py` | 0 | 106 passed | 106 |
| `tests/regression/test_resource_safety.py` | 0 | 21 passed | 21 |
| `tests/cli/test_golden_path.py` (canary) | 0 | 42 passed | 42 |

`git rev-list --reverse 97861cdf..d8ef9350` — **9 commits, each with exactly ONE parent**
(verified by `git rev-list --parents -n 1` on every one), insertions from the `+` column of
`git diff --numstat`, never insertions plus deletions:

| sha | +ins | -del | subject |
|-----|------|------|---------|
| `fde9b4e5` | 442 | 0 | save the round 11 step block |
| `7469e3ea` | 309 | 303 | mirror the round 11 block to last_block |
| `272fcd43` | 20 | 19 | point the plan at the door decision and the recorder |
| `d48b4850` | 8 | 0 | book the round 10 verdict, R-0741, R-0742 and decision D4 |
| `25bb5ec3` | 4 | 0 | record two round 10 prose slips |
| `b80a56a1` | 14 | 1 | pin the ledger's deliberate none divergence |
| `a5892048` | 176 | 0 | record a hunk decision on the job it belongs to |
| `50f09338` | 248 | 0 | pin the recorder writing a decision and applying nothing |
| `d8ef9350` | 2 | 0 | land R-0742 with its own red-proof |

Maximum **442**, every one under 500. C8's own numbers are not measured here.
PATH SET, both directions: range paths NOT in the change set **`[]`**; change-set paths NOT in
the range **`['.agent/handoff.md']`**, which is C8's own path and is written after this gate —
every other declared path is touched and no undeclared path is.
Delimiter residue at C7 — `<<<SLICE ` / `<<<END `: `.agent/plan.md` **0/0**,
`.agent/prose_slips.md` **0/0**, `packages/orchestration/hunk_decision_record.py` **0/0**,
`tests/orchestration/test_hunk_decision_record.py` **0/0**, against the non-zero control
`.agent/authored/f033-r11.md` at **5/6**.
`git ls-files .remedy-wt`: **0**.
DO-NOT-TOUCH PATHS byte-identical at BASE and at C7, by blob id — **10 paths measured, 10
identical**, one line each:

| path | blob id at BASE and at C7 | identical |
|------|--------------------------|-----------|
| `packages/orchestration/hunk_ledger.py` | `57c00fcfde62` | True |
| `packages/orchestration/hunk_apply.py` | `195f0d223210` | True |
| `packages/orchestration/hunk_approval.py` | `25d1a8d0d08d` | True |
| `packages/orchestration/hunk_subset_diff.py` | `6c47c2083795` | True |
| `packages/orchestration/source_apply.py` | `3ca8033856d1` | True |
| `packages/orchestration/diff_parser.py` | `b6632f657426` | True |
| `packages/orchestration/ui_server.py` | `df581292f384` | True |
| `apps/cli/command_catalog.py` | `2c71af53fae4` | True |
| `tests/ui_server/test_command_channel.py` | `7ff931e2f005` | True |
| `docs/roadmap/STATUS.md` | `a370be066b7a` | True |

THE DOOR IS PROVABLY UNCHANGED THIS ROUND. `.agent/context.md`, deliberately not touched, is
`4e3a3f2d9c3f` at BASE and at C7 as well.

## The tests I wrote, and the property each pins

`tests/orchestration/test_hunk_ledger.py`, ONE added case (28 → 29):

| test | property it pins |
|------|------------------|
| `test_a_none_known_set_yields_no_rows_where_another_unusable_value_yields_one` | R-0742: `build_hunk_ledger(None, decision).entries == ()` AND `build_hunk_ledger(7, decision)` yields exactly one entry with `hunk_id == "7"`. The second half is the DISCRIMINATOR — without it the test passes under an `_entries` returning `[]` for everything |

`tests/orchestration/test_hunk_decision_record.py`, 9 cases:

| test | property it pins |
|------|------------------|
| `test_a_clean_decision_writes_one_record_under_the_composed_attempt_key_unattempted` | DECISION F033 D4 itself: one record under `"t-1:2"`, `task_id`/`attempt`/`decided_at` as text, every landing `unattempted` and not `not_landed` |
| `test_the_recorded_rows_carry_the_ledgers_four_keys_in_the_diffs_order` | rows in the DIFF's order with the operator naming the second hunk first; keys `id`/`state`/`reason`/`landing`; rows identical to `export_hunk_ledger(record.ledger)["hunks"]`, so the shape is not doubled; the record's own four keys |
| `test_a_rejection_reason_survives_verbatim_into_the_record` | the reason keeps its surrounding whitespace all the way onto the job |
| `test_a_second_decision_on_the_same_attempt_replaces_the_first` | a revision REPLACES rather than appends; the dict stays one entry long |
| `test_a_decision_on_a_different_attempt_leaves_the_first_record_standing` | two attempt keys coexist and the first record is untouched |
| `test_a_truncated_view_refuses_and_writes_nothing` | `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW` with an EMPTY `hunk_ids`, and `job.metadata` compared before and after — the discriminator that stops a recorder refusing and writing anyway |
| `test_a_decision_refusal_is_returned_unchanged_and_writes_nothing` | `REFUSAL_UNKNOWN_HUNK` and `REFUSAL_MISSING_REASON` come back with the decision core's own code, message and offending ids, and nothing is written |
| `test_unrelated_metadata_keys_survive_the_recording` | `permissions` and an unrelated key both survive |
| `test_the_whole_recorded_document_survives_json_dumps_without_a_custom_encoder` | a `UUID` `task_id` is stored as text; `json.loads(json.dumps(document)) == document`; `record.exported` IS the object on the job, not a copy |

## Authored-text proofs

| reviewer text | applied at | result |
|---------------|-----------|--------|
| the whole block → `.agent/authored/f033-r11.md` | `fde9b4e5` | 36001 bytes, sha256 `7b42b486…56303`, EQUAL to `.remedy-wt/f033-r11-block.md` disk-to-disk |
| the same bytes → `.agent/last_block.md` | `7469e3ea` | ONE blob id with C0a: `282dcf69b2beecaaf729f74e4811f93227115abd` |
| `PLANF033R11` → `.agent/plan.md` | `272fcd43` | byte-EQUAL, 2472 bytes, 47 lines |
| `RECORDF033R11` → `.agent/live_review.md` | `d48b4850` | 1493203 + 1 + 11438 = 1504642, reconstruction exact, BASE a prefix |
| `SLIPSF033R11` → `.agent/prose_slips.md` | `25bb5ec3` | 21213 + 1 + 865 = 22079, reconstruction exact, BASE a prefix |

Every slice was extracted from the COMMITTED C0a blob via `git cat-file blob`, never retyped;
the extractor takes the bytes from the end of the `<<<SLICE` marker line up to and INCLUDING
the newline ending the last content line.

## Deviations & assumptions

1. **THE MODULE DOES NOT CONTAIN THE TOKEN `save_job`, although SPEC §1 uses it.** §1 asks the
   persist-nothing paragraph to say "exactly as `escalation.answer_task_decision` leaves
   `save_job` to the door", while G6(b) orders the count of `save_job` in the module text to be
   **0**. Those two cannot both hold literally. I read the gate as load-bearing — its point is
   to prove the recorder does not call the storage write — and the §1 sentence as the reason
   rather than as required wording. The paragraph therefore names
   `escalation.answer_task_decision`, `packages/orchestration/ui_server.py`'s
   `_dispatch_decision_resolve` and DECISION F009 D21, and says the persisting call is the
   caller's, without spelling that identifier. A reader looking for the write still lands on
   the paragraph, and the gate reads a true 0 rather than a docstring false positive.
2. **The block's ordered commit sequence was followed exactly** — C0a, C0b, C1, C2, C3, C4,
   C5, C6, C7, C8 — with no extra commit, no dropped one and no reordering. G7 was run BEFORE
   C7 rather than after it, because the `Landed: R-0742` line I author at C7 quotes the
   red-proof's real numbers and inventing them was not an option; the block places G7 "at C6"
   and every gate "at or before C7", so this is the ordering it asks for.
3. **`job.metadata.setdefault` is how step 5 creates the container.** The SPEC said "creating
   `job.metadata[HUNK_DECISIONS_METADATA_KEY]` if absent"; `setdefault` is that in one call,
   and it also keeps the module's stated non-totality honest — a `job` whose `metadata` is not
   a dict, or which already holds a non-dict under that key, raises to the caller instead of
   being silently repaired, which is the class the docstring admits it does not handle.
4. **The truncated-view fixture repeats a real diff past `DIFF_VIEW_MAX_FILES`.** The SPEC
   ordered diffs built with `difflib.unified_diff`; the truncated case needs a view the parser
   really refuses, so the test multiplies the real two-hunk diff by `DIFF_VIEW_MAX_FILES + 1`
   and asserts `parse_unified_diff_to_view(...)["truncated"] is True` before using it, rather
   than hand-rolling a synthetic string.
5. **`.agent/context.md` deliberately not touched**, as the block directed — branch, scope and
   constraints are unchanged. I measured it beside the ten do-not-touch paths anyway; it is
   `4e3a3f2d9c3f` at BASE and at C7.
6. **No `Done:` paragraph authored**, as ordered; `Done:` is the reviewer's word. The C7
   `Landed: R-0742 — ` line is mine and is the only prose I authored into
   `.agent/live_review.md`.
7. `git status --porcelain` empty after every commit; all destructive verification ran only
   inside the disposable worktree, removed by exact path. `.agent/STOP` never appeared.

No verdict on this round's work is written here. The reviewer gates it.

## Next

Reviewer gates round 11 at `d8ef9350` plus this handback commit; then the write door itself —
`UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py`, the two EQUALITY guards in
`tests/ui_server/test_command_channel.py`, and `packages.orchestration.hunk_apply` joining
`FORBIDDEN_MODULES`, each widened in the same commit as the dispatch that needs it.
