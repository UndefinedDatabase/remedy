# Handback — F033 Hunk-level diff approval · ROUND 10 · THE HUNK-DECISION LEDGER

## Session

SESSION 3 of feature F033 · round 10 · rounds so far 10

## Range

Review of `cee20b37`..`bb2e004c` (the handback commit follows this file).

## Commits

### 6b130aa7 docs(f033): save the round 10 ledger block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r10.md` | +436/-0 | C0a — the reviewer's block, copied with `shutil.copyfile`, never retyped |

### 386a274c docs(f033): mirror the round 10 block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +308/-263 | C0b — same bytes, one blob id with C0a |

### 38090058 docs(f033): point the plan at the hunk-decision ledger
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +15/-14 | C1 — whole-file PLANF033R10 |

### c50b5ccf docs(f033): book the round 9 verdict and register R-0741
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +6/-0 | C2 — RECORDF033R10: the R9 gate line, the R-0740 resolution, the R-0741 registration |

### 84971dac docs(f033): log the round 9 prose slip
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +2/-0 | C3 — one dated SLIPSF033R10 line |

### f042e0a3 docs(f033): give the outcome docstring the real reason landed is empty
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_apply.py` | +6/-4 | C4 — the R-0741 repair, comment text only |

### 0e109625 feat(f033): add the hunk-decision ledger
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_ledger.py` | +303/-0 | C5 — the new pure module |

### bd3bdcb1 refactor(f033): state the landing refusal in exactly one place
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_ledger.py` | +14/-7 | C5b — UNORDERED, see Deviations |

### d5e0c2ba test(f033): pin the ledger's two axes and its totality
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_ledger.py` | +285/-0 | C6 — 28 cases |

### bb2e004c docs(f033): land R-0741 in the record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2/-0 | C7 — the worker-authored `Landed: R-0741` line |

### C8 (this commit) docs(f033): hand back the round 10 ledger
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | this file | the handback; a handoff cannot table the commit that writes it |

The `+/-` column above is `git diff --numstat` output, cell for cell, and it agrees with the
per-commit insertion column G8 produced below.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it | done | |
| C1 `.agent/plan.md` | done | |
| C2 verdict, R-0740 resolution, R-0741 registration | done | |
| C3 one line into `.agent/prose_slips.md` | done | |
| C4 the R-0741 repair in `hunk_apply.py` | done | |
| C5 the ledger module | done | |
| C5b single-site landing refusal | deviated | UNORDERED extra commit; see Deviations |
| C6 its tests | done | |
| C7 `Landed: R-0741` into `.agent/live_review.md` | done | |
| C8 the handback | done | this file |
| G1 hygiene | done | |
| G2 transport | done | |
| G3 the record append at C2 | done | |
| G4 the ledger at C2 and C7 | done | |
| G5 the prose files | done | |
| G6 the code against the SPEC | done | |
| G7 totality and the mutation red-proofs | done | four of four RED |
| G8 suites and structure | done | |

## External actions

- `git worktree add .remedy-wt/f033-r10-mut d5e0c2ba` — created, detached HEAD at C6.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f033-r10-mut --force` — removed BY EXACT PATH.
- `git worktree prune` — ran; `git worktree list` then held only the primary checkout.
- `git push -u origin feature/f033-hunk-approval-v2` — pushed after C8.
- No PR created, none edited, none merged. No `gh` command run.

## Verification

**G1 HYGIENE.** `.agent/STOP` read from disk before C0a — `ls: cannot access '.agent/STOP':
No such file or directory` — and again before C8, same result: ABSENT both times.
`git status --porcelain` measured after every one of the ten commits: `0` lines each time.
Branch `feature/f033-hunk-approval-v2` throughout (`git rev-parse --abbrev-ref HEAD`). No
force-push, no history rewrite, no branch deletion; `git rev-parse feature/f033-hunk-approval`
= `ed04081283081f237d96147da39a07fca0b1ccad`, unchanged.

**G2 TRANSPORT.** `.remedy-wt/f033-r10-block.md`: 34128 bytes, sha256
`dc3caa08752b4992466a70c0fb9479ee5d4a9477f4be4252e4dee2348d3f1368` — verified against the
ordered digest BEFORE any work began. `6b130aa7:.agent/authored/f033-r10.md`: 34128 bytes,
sha256 `dc3caa08752b4992466a70c0fb9479ee5d4a9477f4be4252e4dee2348d3f1368`. EQUAL on both
readings. `git rev-parse 386a274c:.agent/authored/f033-r10.md 386a274c:.agent/last_block.md`
printed ONE blob id twice: `e04eaf4f186bf4a3b4d53d8eea0081a33d1458af`.

**G3 THE RECORD APPEND at C2.** Real exit 0.
(a) BASE blob 1481910 bytes (the ordered figure, measured). Slice RECORDF033R10 9582 bytes.
C2 blob 1491493 bytes. `BASE + one newline + slice == C2 blob`: **True**. BASE a byte
PREFIX of C2: **True**. C2 ends in exactly one newline: **True** (trailing bytes `b's.\n'`).
(b) N paragraphs COUNTED by the script in the slice: **3**. Last 3 blank-line units of the
C2 blob == the slice's 3 paragraphs IN ORDER: **True**. The script computed the FIRST
appended paragraph's span as C2 offsets 1481911..1486878 and asserted the slice's first
paragraph equals those bytes; NEGATIVE CONTROL at offset **1482411**, proven to satisfy
`1481911 <= 1482411 < 1486878`, one byte flipped. Reader 1 (reconstruction equality)
REJECTS it: **True**. Reader 2 (last-3-paragraph comparison) REJECTS it: **True**.

**G4 THE LEDGER at BASE, C2 and C7.** Real exit 0.

| | registered `^- R-\d+ — ` | distinct | `^Done: R-\d+ — ` | distinct | `^Landed: R-` | `^Gate: F\d+ R\d+ — ` | OPEN SET |
|---|---|---|---|---|---|---|---|
| BASE | 301 | 301 | 45 | 43 | 13 | 126 | 258 |
| C2 | 302 | 302 | 46 | 44 | 13 | 127 | 258 |
| C7 | 302 | 302 | 46 | 44 | 14 | 127 | 258 |

ADDED registered id BASE→C2: exactly `R-0741`; C2→C7: none (UNMOVED). ADDED `Done:` id
BASE→C2: exactly `R-0740`; C2→C7: none (UNMOVED) — I authored no `Done:` paragraph.
`Landed:` UNMOVED at 13 across C2, then 13→14 at C7 with the added line matching
`^Landed: R-0741 — `; the existing `Landed: R-0740 — ` line is still present at C7 (count 1)
beside its new `Done:` paragraph. `^Gate: F033 R9 — ` is exactly **1** at C2 and still 1 at
C7. Open set 258 UNMOVED at C2 (one registered, one resolved in the same commit) and
UNMOVED at C7. The C2 blob is a byte PREFIX of the C7 blob: **True**.

**G5 THE PROSE FILES.** Real exit 0. `.agent/plan.md` at C1: **2494 bytes, 46 lines**,
byte-EQUAL to PLANF033R10 (**True**), and 46 < 50, the AGENTS.md cap. `.agent/prose_slips.md`:
BASE 20761 bytes (the ordered figure, measured), slice 451 bytes, C3 21213 bytes;
`BASE + one newline + slice == C3 blob`: **True**; BASE a byte PREFIX of C3: **True**. Lines
matching `^2026-\d\d-\d\d · F033 R9 · ` — BASE **0**, C3 **1**. Lines beginning `- R-` in the
whole C3 file: **0**.

**G6 THE CODE AGAINST THE SPEC.** Real exit 0 on every part.
(a) `packages/orchestration/hunk_apply.py` parsed at BASE (13889 bytes) and at C4 (14059
bytes); raw sources equal: **False**. Every docstring blanked in both trees, `ast.dump` of
the two **EQUAL: True** — so no executable line moved. NEGATIVE CONTROL: five characters
appended to one executable string literal in the C4 tree, and the equality REJECTED it:
**True**, so the equality is one that can fail. The retired reason
`there is no partial landing to distinguish it from` now occurs **0** times in the whole
file, and in `HunkApplyOutcome`'s docstring: absent. The surviving first clause
``landed`` is EMPTY whenever ``applied`` is false: **present**. The docstring points at
`_failure_lead_sentence`: **True**.
(b) `python3 -m ruff check packages/orchestration/hunk_ledger.py tests/orchestration/test_hunk_ledger.py`
— REAL EXIT CODE **0**, summary line `All checks passed!`.
(c) FULL import list of the ledger by AST, **5 entries**:
`['__future__', 'collections.abc', 'dataclasses', 'typing', 'packages.orchestration.hunk_approval']`
— every entry is standard library or `packages.orchestration.hunk_approval`. Present in any
import: `hunk_apply` **False**, `source_apply` **False**, `hunk_subset_diff` **False**,
`diff_parser` **False**. Counts in the module text: `open(` **0**, `import os` **0**,
`import subprocess` **0**, `import logging` **0**, `Path` **0**.
(d) The six vocabulary constants, read from the module's own AST:

    HUNK_STATE_APPROVED       = 'approved'
    HUNK_STATE_REJECTED       = 'rejected'
    HUNK_STATE_PENDING        = 'pending'
    HUNK_LANDING_LANDED       = 'landed'
    HUNK_LANDING_NOT_LANDED   = 'not_landed'
    HUNK_LANDING_UNATTEMPTED  = 'unattempted'

(e) Extracted from the AST at C7:

    build_hunk_ledger(known_hunk_ids: Iterable[str], decision: HunkDecision, *,
                      applied: bool = False, landed_hunk_ids: Iterable[str] = (),
                      apply_attempted: bool = False) -> HunkDecisionLedger
    export_hunk_ledger(ledger: HunkDecisionLedger) -> dict
    HunkLedgerEntry fields:     ['hunk_id: str', 'state: str', 'reason: str', 'landing: str']
    HunkDecisionLedger fields:  ['entries: tuple[HunkLedgerEntry, ...]']

**G7 TOTALITY AND THE MUTATION RED-PROOFS.** Real exit 0 on the probe.
FIRST, the SHIPPED function called directly in the primary checkout, not through the tests.
`build_hunk_ledger.__module__` resolved to `packages.orchestration.hunk_ledger`. Six cases,
**0 raised**, every `type()` the same:

| call | `type()` of the return | entries |
|------|------------------------|---------|
| `known_hunk_ids=None` | `<class 'packages.orchestration.hunk_ledger.HunkDecisionLedger'>` | `[]` |
| `known_hunk_ids=NotIterable()` | `<class '…HunkDecisionLedger'>` | one row, id `'<__main__.NotIterable object at 0x…>'`, `pending`/`unattempted` |
| `known_hunk_ids=[1, 2.5, None]` (non-string ids) | `<class '…HunkDecisionLedger'>` | `[('1', 'pending', 'unattempted'), ('2.5', …), ('None', …)]` |
| `decision=None` | `<class '…HunkDecisionLedger'>` | `[('h1', 'pending', 'unattempted'), ('h2', 'pending', 'unattempted')]` |
| `known_hunk_ids=[BrokenText()]` (`__str__` raises) | `<class '…HunkDecisionLedger'>` | `[('<BrokenText>', 'pending', 'unattempted')]` |
| `decision=BrokenText()` (`__str__` raises) | `<class '…HunkDecisionLedger'>` | `[('h1', 'pending', 'unattempted')]` |

THEN, in the disposable worktree `.remedy-wt/f033-r10-mut` at `d5e0c2ba`, `python3 -B` with
`PYTHONDONTWRITEBYTECODE=1`, never in the primary checkout. The import was proved to resolve
to the worktree's own copy FIRST:
`/home/decodeux/Repos/remedy/.remedy-wt/f033-r10-mut/packages/orchestration/hunk_ledger.py`.
Each anchor was asserted UNIQUE (occurrences printed) before replacement, and the file was
restored to the original bytes before and after every mutation.

| run | anchor hits | REAL exit | result | failing test(s) |
|-----|-------------|-----------|--------|-----------------|
| UNMUTATED CONTROL | — | **0** | 28 passed | — |
| (i) honour `landed_hunk_ids` even when `applied` is False | 1 | **1** | RED, 1 failed 27 passed | `test_a_failed_apply_does_not_honour_the_landed_ids_it_was_handed` |
| (ii) ignore `apply_attempted`, treat it as always True | 1 | **1** | RED, 1 failed 27 passed | `test_an_unattempted_apply_overrides_every_other_landing_argument` |
| (iii) emit entries in the decision's order | 1 | **1** | RED, 14 failed 14 passed | `test_the_ledger_is_in_the_diffs_order_and_not_the_decisions`, `test_each_of_the_three_states_lands_on_the_hunk_that_earned_it`, `test_a_repeated_known_id_gets_exactly_one_row`, `test_a_rejection_reason_arrives_verbatim_and_every_other_reason_is_empty`, `test_each_of_the_three_landings_appears_in_the_case_that_produces_it`, `test_a_failed_apply_does_not_honour_the_landed_ids_it_was_handed`, `test_an_unattempted_apply_overrides_every_other_landing_argument`, `test_a_decided_id_the_attempt_does_not_carry_is_dropped`, and the six `test_no_hostile_decision_makes_the_ledger_raise[…]` cases |
| (iv) strip the rejection reason | 1 | **1** | RED, 1 failed 27 passed | `test_a_rejection_reason_arrives_verbatim_and_every_other_reason_is_empty` |
| REVERTED CONTROL | — | **0** | 28 passed | — |

Four of four went RED; none came back green. Target restored byte-identically: **True**.
Worktree removed by exact path, `git worktree prune` run, `git worktree list` then held only
`/home/decodeux/Repos/remedy`.

**G8 SUITES AND STRUCTURE.** Six suites, SERIALLY, one pytest process at a time, every REAL
exit code captured through a Python runner (the shell rejects `$?` by FORM):

| suite | REAL exit | count | BASE |
|-------|-----------|-------|------|
| `tests/orchestration/test_hunk_ledger.py` | 0 | 28 passed | new this round |
| `tests/orchestration/test_hunk_approval.py` | 0 | 30 passed | 30 |
| `tests/orchestration/test_hunk_apply.py` | 0 | 11 passed | 11 |
| `tests/orchestration/test_hunk_subset_diff.py` | 0 | 17 passed | 17 |
| `tests/regression/test_resource_safety.py` | 0 | 21 passed | 21 |
| `tests/cli/test_golden_path.py` (canary) | 0 | 42 passed | 42 |

`git rev-list --reverse cee20b37..bb2e004c` — **10 commits, each with exactly ONE parent**,
insertions from the `+` column of `git diff --numstat` (never insertions plus deletions):

| sha | +ins | -del | subject |
|-----|------|------|---------|
| `6b130aa7` | 436 | 0 | save the round 10 ledger block |
| `386a274c` | 308 | 263 | mirror the round 10 block |
| `38090058` | 15 | 14 | point the plan at the hunk-decision ledger |
| `c50b5ccf` | 6 | 0 | book the round 9 verdict and register R-0741 |
| `84971dac` | 2 | 0 | log the round 9 prose slip |
| `f042e0a3` | 6 | 4 | give the outcome docstring the real reason landed is empty |
| `0e109625` | 303 | 0 | add the hunk-decision ledger |
| `bd3bdcb1` | 14 | 7 | state the landing refusal in exactly one place |
| `d5e0c2ba` | 285 | 0 | pin the ledger's two axes and its totality |
| `bb2e004c` | 2 | 0 | land R-0741 in the record |

Maximum 436, every one under 500. C8's own numbers are not measured here.
PATH SET, both directions: touched-but-not-declared `[]`, declared-but-not-touched `[]`,
range path set EQUALS the change set: **True**.
Delimiter residue at C7 — `<<<SLICE ` / `<<<END `: `.agent/plan.md` **0/0**,
`.agent/prose_slips.md` **0/0**, `packages/orchestration/hunk_ledger.py` **0/0**,
`tests/orchestration/test_hunk_ledger.py` **0/0**, against the non-zero control
`.agent/authored/f033-r10.md` at **5/6**.
`git ls-files .remedy-wt`: **0**.
DO-NOT-TOUCH PATHS byte-identical at BASE and at C7, by blob id — **10 paths measured, 10
identical**: `source_apply.py` `3ca8033856d1`, `hunk_approval.py` `25d1a8d0d08d`,
`hunk_subset_diff.py` `6c47c2083795`, `hunk_identity.py` `0c0d51877aeb`, `ui_server.py`
`df581292f384`, `apps/cli/command_catalog.py` `2c71af53fae4`,
`tests/ui_server/test_command_channel.py` `7ff931e2f005`,
`tests/orchestration/test_hunk_apply.py` `2dcba450d20f`, `docs/roadmap/STATUS.md`
`a370be066b7a`, `.agent/context.md` `4e3a3f2d9c3f`.

## The tests I wrote, and the property each pins

`tests/orchestration/test_hunk_ledger.py`, 28 cases from 13 test functions:

| test | property it pins |
|------|------------------|
| `test_the_ledger_is_in_the_diffs_order_and_not_the_decisions` | rows follow `known_hunk_ids`, with the decision deliberately in a DIFFERENT order (`approved == ("h4", "h1")`) so the two are distinguishable |
| `test_a_repeated_known_id_gets_exactly_one_row` | repeats removed keeping first-appearance order |
| `test_each_of_the_three_states_lands_on_the_hunk_that_earned_it` | approved / rejected / pending, per hunk |
| `test_a_rejection_reason_arrives_verbatim_and_every_other_reason_is_empty` | the reason keeps its surrounding whitespace; every other reason is `""` |
| `test_each_of_the_three_landings_appears_in_the_case_that_produces_it` | `landed`, `not_landed` and `unattempted` in one successful-apply case |
| `test_an_approved_hunk_whose_apply_failed_is_still_approved_and_did_not_land` | the TWO AXES coming apart — the reason the module exists |
| `test_a_failed_apply_does_not_honour_the_landed_ids_it_was_handed` | `applied=False` ⇒ `landed_hunk_ids` ignored entirely |
| `test_an_unattempted_apply_overrides_every_other_landing_argument` | `apply_attempted=False` ⇒ every landing `unattempted`, states untouched |
| `test_a_decided_id_the_attempt_does_not_carry_is_dropped` | an id outside `known_hunk_ids` gets no row (hand-built `HunkDecision`, since `decide_hunk_approval` refuses that input) |
| `test_the_export_carries_the_four_keys_and_nothing_else` | `{"hunks": [...]}`, keys `id`/`state`/`reason`/`landing` in order, all `str`, JSON round-trip |
| `test_no_hostile_argument_makes_the_ledger_raise` (8 cases) | totality over `known_hunk_ids`, the flags and `landed_hunk_ids` |
| `test_no_hostile_decision_makes_the_ledger_raise` (6 cases) | totality over `decision`, including broken `__str__` and broken `__getattr__` |
| `test_no_hostile_ledger_makes_the_export_raise` (4 cases) | totality of `export_hunk_ledger` |

## Authored-text proofs

| reviewer text | applied at | result |
|---------------|-----------|--------|
| the whole block → `.agent/authored/f033-r10.md` | `6b130aa7` | 34128 bytes, sha256 `dc3caa08…3f1368`, EQUAL to `.remedy-wt/f033-r10-block.md` disk-to-disk |
| the same bytes → `.agent/last_block.md` | `386a274c` | ONE blob id with C0a: `e04eaf4f186bf4a3b4d53d8eea0081a33d1458af` |
| `PLANF033R10` → `.agent/plan.md` | `38090058` | byte-EQUAL, 2494 bytes |
| `RECORDF033R10` → `.agent/live_review.md` | `c50b5ccf` | 1481910 + 1 + 9582 = 1491493, reconstruction exact, BASE a prefix |
| `SLIPSF033R10` → `.agent/prose_slips.md` | `84971dac` | 20761 + 1 + 451 = 21213, reconstruction exact, BASE a prefix |

Every slice was extracted from the COMMITTED C0a blob via `git show`, never retyped; the
extractor takes the bytes from the end of the `<<<SLICE` marker line up to and INCLUDING the
newline ending the last content line, and asserts that byte is a newline.

## Deviations & assumptions

1. **AN UNORDERED ELEVENTH COMMIT, `bd3bdcb1`, sits between C5 and C6.** The bundle ordered
   C5 (module) then C6 (tests); I added `bd3bdcb1` between them. WHY: as first written at
   C5 the module stated the landing refusal in TWO places — a conditional on the `landed`
   assignment in `build_hunk_ledger` AND the `if not applied:` branch in `_entry_landing` —
   and with both present G7's ordered mutation (i), "honour `landed_hunk_ids` even when
   `applied` is False", CANNOT REACH ANY TEST from a single unique anchor: whichever of the
   two you mutate, the other still forces `not_landed`, so the mutation would have come back
   green for a reason that says nothing about the tests. `bd3bdcb1` removes the duplicate
   guard so the rule has exactly one site, which is also the better module (a rule enforced
   twice is a rule whose copies drift). I did NOT amend `0e109625`, because amending is a
   history rewrite and the guardrails forbid one. Both commits touch only
   `packages/orchestration/hunk_ledger.py`, a declared change-set path, so G8's path-set
   equality is unaffected.
2. **C4 re-wrapped one line the SPEC did not name.** The SPEC ordered COMMENT TEXT ONLY and
   said every other sentence of the `HunkApplyOutcome` docstring is untouched. My
   replacement sentence is longer than the one it replaces, which pushed `apply_id`'s
   sentence onto a ~180-character line; I re-wrapped that one line. No sentence other than
   the repaired one changed in content, and G6(a) proves by AST that no executable line
   moved.
3. **`_entries(None)` returns NO entries in the ledger, where `hunk_approval._entries`
   returns one.** The SPEC ordered the `_total_text` guard restated and totality on `None`,
   and both hold; this is the one place I departed from the sibling's shape. A validator
   reports the strange value it was handed, but a LEDGER would render it as a ROW, and a
   fabricated hunk called `"None"` in the operator's durable record is worse than an empty
   record. The divergence is stated in `_entries`'s own docstring, and the totality probe
   above shows it: `known_hunk_ids=None` yields `entries=[]`.
4. **Three totality cases beyond the ordered five.** The SPEC listed `None`, a non-iterable,
   a non-string id, `decision=None` and a broken `__str__`; the module also has to survive a
   broken `__bool__` (the two flags) and a broken `__getattr__` (the decision and entry
   readers), so `_BrokenFlag` and `_BrokenAttributes` are in the suite and `decision=BrokenText()`
   is in the probe. Nothing ordered was dropped.
5. **`.agent/context.md` deliberately not touched**, as the block directed — branch, scope
   and constraints are unchanged. I measured it in G8's frozen-path table alongside the nine
   paths the change-set section names, which is why that table reports 10 paths and not 9.
6. **No `Done:` paragraph authored**, as ordered; `Done:` is the reviewer's word. The C7
   `Landed: R-0741 — ` line is mine and is the only prose I authored into
   `.agent/live_review.md`.
7. `git status --porcelain` empty after every commit; all destructive verification ran only
   inside the disposable worktree. `.agent/STOP` never appeared.

No verdict on this round's work is written here. The reviewer gates it.

## Next

Reviewer gates round 10 at `bb2e004c` plus this handback commit; then the write door, which
needs a DECISION ruling what its effect IS before any command id is exposed.
