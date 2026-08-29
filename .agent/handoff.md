# Handback — F033 Hunk-level diff approval · ROUND 6 · OPENING T002

## Session

SESSION 2 of feature F033 · round 6 · rounds so far 6

## Range

Review of `cb49a3ea39659dbc270dfd36ea296171cf6dc439`..`da81db5487d460b91b5e481f5c9b4eb5f7365bde`
plus the C4 commit `410509253b4c028570f3273270693925cd1725ee` and this handback commit.
BASE was confirmed with `git rev-parse HEAD` before C0a. Branch
`feature/f033-hunk-approval-v2` throughout.

## Commits

### 57889e78 chore(f033): save the round 6 step block

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r6.md | +337 / -0 | C0a — the block saved with `shutil.copyfile`, never retyped |

### acafb28f chore(f033): mirror the round 6 block to last_block

| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +249 / -252 | C0b — mirrored from the COMMITTED C0a blob via `git show` |

### 8e6183fd docs(f033): retarget the plan on the decision core

| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +15 / -17 | C1 — whole-file PLANF033R6, applied byte for byte |

### f3a8b0ed docs(f033): book the round 5 verdict and resolve R-0739

| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | C2 — RECORDF033R6 appended: the R5 gate paragraph and `Done: R-0739` |

### da81db54 docs(f033): record the two round 5 reviewer prose slips

| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +4 / -0 | C3 — SLIPSF033R6 appended, no id spent (amend0827 rule 2) |

### 41050925 feat(f033): add the hunk approval decision core

| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/hunk_approval.py | +272 / -0 | C4 — NEW: the pure decision core, written from the block's SPEC |
| tests/orchestration/test_hunk_approval.py | +220 / -0 | C4 — NEW: 17 test functions, 30 collected cases |

### C5 this handback (self-reference — a handoff cannot table the commit that writes it)

| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | (this commit) | C5 — rewritten per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f033-r6-wt 41050925` — created for G7; every
  mutation ran there, never in the primary checkout.
- `git worktree remove --force .remedy-wt/f033-r6-wt` then `git worktree prune` — removed
  BY EXACT PATH, no glob. Exit 0 both.
- `git push -u origin feature/f033-hunk-approval-v2` after C5.
- No `gh` command was run. No PR created, no merge, no force-push, no history rewrite, no
  branch deleted.

## Verification

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a and again before C5:
  `ls` exit 2, "No such file or directory" both times. `git status --porcelain` empty
  after every one of the six commits. Branch `feature/f033-hunk-approval-v2` throughout.
  `git rev-parse feature/f033-hunk-approval` = `ed04081283081f237d96147da39a07fca0b1ccad`,
  unmoved.
- **G2 TRANSPORT — PASS.** `.remedy-wt/f033-r6-block.md` = 24108 bytes, sha256
  `a68745f0d20f4119b83927edeee3bee00ba63a1f3c2ede5140d60ebfd109ee19`. The C0a blob
  `57889e78:.agent/authored/f033-r6.md` = 24108 bytes, same sha256 — EQUAL.
  `git rev-parse acafb28f:.agent/authored/f033-r6.md` and
  `git rev-parse acafb28f:.agent/last_block.md` both print ONE blob id,
  `7f1228d5b26b2eca72b682192338677585a8b46b`.
- **G3 THE RECORD APPEND at C2 — PASS.** (a) BASE blob 1456716 bytes as ordered; slice
  5024; 1456716 + 1 + 5024 = 1461741 = the C2 blob, byte for byte EQUAL; BASE a byte
  PREFIX; ends in exactly one newline. (b) N counted by the script = 2. The last 2
  blank-line units of the C2 blob equal the slice's paragraphs IN ORDER (unit 0 = 3192
  bytes, opens `Gate: F033 R5 —`; unit 1 = 1830 bytes, opens `Done: R-0739 —`). NEGATIVE
  CONTROL: the first appended paragraph was PROVEN to span offsets 1456717–1459909, a byte
  flipped at 1458313 (inside that span); the byte-formula reader rejected it and the
  paragraph reader rejected it — BOTH.
- **G4 THE LEDGER at C2 — PASS.** BASE: registered 300 distinct, `Done:` 44 lines over 42
  distinct, `Landed:` 12, `Gate:` 122, open set 258. C2: registered 300 (UNMOVED — this
  round registers nothing, ADDED registered ids = []), `Done:` 45 lines over 43 distinct
  with the ADDED resolved id exactly `R-0739` and nothing else, `Landed:` 12 UNMOVED,
  `Gate:` 122 to 123, open set 258 to 257. `^Gate: F033 R5 — ` at C2 reads exactly 1.
  `Landed: R-0739` still reads 1 at C2 — it stays beside its `Done:` paragraph.
- **G5 THE PROSE-SLIPS APPEND at C3 — PASS.** BASE blob 18681 bytes as ordered; the slice
  OPENS with a blank line so no separator was added; 18681 + 897 = 19578 = the C3 blob,
  byte for byte EQUAL; BASE a byte PREFIX; ends in exactly one newline. The lines the C3
  diff ADDS are 4 and equal the slice's 4 lines IN ORDER.
  `^2026-08-29 · F033 R5 · ` at C3 reads exactly 2. No contradiction this round between the
  byte formula and the added-line clause — the slice's leading blank line makes them agree.
- **G6 THE MODULE AGAINST THE SPEC at C4 — PASS.** (a) `python3 -B -m ruff check` over both
  new files: summary line `All checks passed!`, REAL EXIT 0. (b) By AST, the module's
  import statements name exactly `['__future__', 'collections', 'collections.abc',
  'dataclasses', 'typing']`; checked against `sys.stdlib_module_names`, non-stdlib = [] —
  ONLY standard library, and no module of this package. (c) All five are module-level
  `ast.Assign` of a string constant, exact: `REFUSAL_EMPTY_DECISION` = `empty_decision`,
  `REFUSAL_DUPLICATE_HUNK` = `duplicate_hunk`, `REFUSAL_OVERLAPPING_SETS` =
  `overlapping_sets`, `REFUSAL_UNKNOWN_HUNK` = `unknown_hunk`, `REFUSAL_MISSING_REASON` =
  `missing_reason`. (d) TOTALITY run as a real probe, not asserted: `None`, `object()`, the
  integer id `7`, and an object whose `__str__` raises, each in the `approved` and the
  `rejected` position — 8 of 8 calls RETURNED, 0 raised, every return a
  `HunkApprovalRefusal` with code `unknown_hunk`. (e) forbidden tokens in the module:
  `open(` = 0, `import os` = 0, `import subprocess` = 0, `import logging` = 0, `Path` = 0.
- **G7 THE MUTATION RED-PROOFS at C4 — PASS, all three RED.** Run in the disposable
  worktree `.remedy-wt/f033-r6-wt` detached at `41050925`, with `python3 -B`, never in the
  primary checkout. UNMUTATED CONTROL: `python3 -B -m pytest
  tests/orchestration/test_hunk_approval.py -q` REAL EXIT 0, 30 passed. Each anchor was
  asserted UNIQUE in the file before replacement, and the file was reverted fully between
  mutations.
  (i) OVERLAPPING_SETS never trips (`    if overlapping:` → `    if False and
  overlapping:`, occurrences 1): REAL EXIT 1, 2 failed / 28 passed —
  `test_an_id_in_both_sets_is_refused_as_overlapping`,
  `test_the_earlier_refusal_wins_when_one_input_trips_two[overlapping-first]`.
  (ii) a whitespace-only reason accepted as a reason (`if not r.reason.strip()` → `if not
  r.reason`, occurrences 1): REAL EXIT 1, 2 failed / 28 passed —
  `test_a_rejection_without_a_real_reason_is_refused[spaces]`,
  `test_a_rejection_without_a_real_reason_is_refused[tab-newline]`.
  (iii) UNKNOWN_HUNK never trips (`    if unknown:` → `    if False and unknown:`,
  occurrences 1): REAL EXIT 1, 4 failed / 26 passed —
  `test_an_id_the_diff_does_not_carry_is_refused_as_unknown`,
  `test_the_earlier_refusal_wins_when_one_input_trips_two[unknown-first]`,
  `test_every_offending_id_is_reported_at_once_rather_than_one_per_round_trip`,
  `test_a_broken_object_is_named_by_its_repr_rather_than_crashing`.
  REVERTED CONTROL after the third: REAL EXIT 0, 30 passed. No mutation came back green.
- **G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time, every REAL
  exit 0: `tests/orchestration/test_hunk_approval.py` 30 passed (new this round);
  `tests/orchestration/test_hunk_identity.py` 10 passed (10 at BASE, unmoved);
  `tests/orchestration/test_diff_parser.py` 50 passed (50 at BASE, unmoved);
  `tests/regression/test_resource_safety.py` 21 passed;
  `tests/test_no_interactive_guard.py` 6 passed; canary `tests/cli/test_golden_path.py`
  42 passed (42 at BASE, unmoved). Structure walk `git rev-list --reverse BASE..C4`, each
  commit exactly ONE parent and insertions taken from the `+` column of
  `git diff --numstat` alone: `57889e78` 337, `acafb28f` 249, `8e6183fd` 15, `f3a8b0ed` 4,
  `da81db54` 4, `41050925` 492 — all six under 500. Range path set =
  `.agent/authored/f033-r6.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/prose_slips.md`, `packages/orchestration/hunk_approval.py`,
  `tests/orchestration/test_hunk_approval.py`; in range but not in the change set = none;
  in the change set but not in the range = `.agent/handoff.md` only, the expected absence,
  since C5 lands after the walk. Delimiter residue `<<<SLICE ` / `<<<END `: `.agent/plan.md`
  0/0, `.agent/prose_slips.md` 0/0, `packages/orchestration/hunk_approval.py` 0/0,
  `tests/orchestration/test_hunk_approval.py` 0/0, against the non-zero control
  `.agent/authored/f033-r6.md` at 5/6. `git ls-files .remedy-wt` = 0.

## Authored-text proofs

Three reviewer-authored slices were applied this round, each extracted from the COMMITTED
C0a blob with `git show`, never retyped, and each anchored to its NAMED delimiter at line
start. Slice byte lengths and sha256 as extracted:

- PLANF033R6 — 1936 bytes, `07756c37b6a062961efe5d1fa1c8aadb4760940e0c929802c90dcf0dc6da0552`.
  Applied whole-file to `.agent/plan.md`; the committed blob is those bytes exactly, ending
  in one newline (38 lines).
- RECORDF033R6 — 5024 bytes, `44f9831f55764934b2b966aa99dde32d865d06ad4222539dc3fad591272cc1a7`.
  Appended per G3(a); proved byte for byte against the C2 blob, with the negative control
  rejected by both readers.
- SLIPSF033R6 — 897 bytes, `c8d2fb0102706505d26d1d4cfcb0352f4a3bb482f1c1c8c953b8c37eee1ce3e9`.
  Appended per G5; proved byte for byte against the C3 blob.

The C0a disk-to-disk comparison is in G2: the file on disk at
`.remedy-wt/f033-r6-block.md` and the committed `.agent/authored/f033-r6.md` blob are 24108
bytes with an identical sha256.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it | done | |
| C1 `.agent/plan.md` | done | |
| C2 the R5 verdict and `Done: R-0739` into `.agent/live_review.md` | done | |
| C3 the two reviewer prose slips into `.agent/prose_slips.md` | done | |
| C4 the decision core and its tests, together | done | one commit, as ordered |
| C5 the handback | done | this commit |
| G1 HYGIENE | done | pass |
| G2 TRANSPORT | done | pass |
| G3 THE RECORD APPEND at C2 | done | pass |
| G4 THE LEDGER at C2 | done | pass |
| G5 THE PROSE-SLIPS APPEND at C3 | done | pass |
| G6 THE MODULE AGAINST THE SPEC at C4 | done | pass, five parts |
| G7 THE MUTATION RED-PROOFS at C4 | done | pass, three of three RED |
| G8 SUITES AND STRUCTURE | done | pass |

## The shipped signature

    decide_hunk_approval(
        known_hunk_ids: Iterable[str],
        approved: Iterable[str],
        rejected: Iterable[HunkRejection | tuple[str, str] | Mapping[str, str]],
    ) -> HunkDecision | HunkApprovalRefusal

17 test functions, 30 collected cases, each named for the property it pins:

| Test | Property pinned |
|------|-----------------|
| `test_a_decision_naming_no_hunk_is_refused_as_absent` | EMPTY_DECISION, and its `hunk_ids` is empty because no single id is at fault |
| `test_an_id_repeated_inside_one_set_is_refused_as_a_duplicate` (2 cases) | DUPLICATE_HUNK, within `approved` and within `rejected` separately |
| `test_an_id_in_both_sets_is_refused_as_overlapping` | OVERLAPPING_SETS |
| `test_an_id_the_diff_does_not_carry_is_refused_as_unknown` | UNKNOWN_HUNK |
| `test_a_rejection_without_a_real_reason_is_refused` (6 cases) | MISSING_REASON for empty, spaces, tab+newline, a bare string, an explicit null reason and a missing reason key |
| `test_the_earlier_refusal_wins_when_one_input_trips_two` (3 cases) | the ORDER: duplicate before overlapping, overlapping before unknown, unknown before missing-reason |
| `test_a_mixed_decision_reports_approved_rejected_and_the_pending_remainder` | approved in the order given, rejected normalised, pending the remainder |
| `test_pending_follows_the_order_the_known_set_gave` | pending is in the KNOWN set's order, not the approved set's |
| `test_pending_is_empty_when_every_known_hunk_is_decided` | pending empty when nothing is undecided |
| `test_rejecting_everything_is_a_valid_decision_with_an_empty_approved_set` | the feature file's full-rejection edge case is VALID, not a refusal |
| `test_a_rejection_reason_is_kept_verbatim_including_its_whitespace` | reasons survive byte for byte, for T003's verbatim quote |
| `test_the_three_rejection_spellings_produce_the_same_decision` | dataclass, tuple and wire mapping agree |
| `test_offending_ids_are_deduplicated_in_first_appearance_order` | the offending list is deduplicated and ordered by first appearance |
| `test_every_offending_id_is_reported_at_once_rather_than_one_per_round_trip` | offending ids from BOTH sets arrive together |
| `test_no_hostile_input_raises_in_any_position` (6 cases) | TOTALITY in all three argument positions |
| `test_a_broken_object_is_named_by_its_repr_rather_than_crashing` | a broken `__str__` degrades to `repr()` and is NAMED |
| `test_a_non_string_id_is_compared_as_text` | an id is compared as text |

## Deviations & assumptions

No departure from the block's ordered commit sequence: the six bundle commits landed in
the ordered order, none added, none dropped, none reordered. The following are authoring
decisions the SPEC left to me, or readings of it that a reviewer should check.

1. **C4's size forced the prose down, not the content.** The first complete draft of the
   two files measured 558 insertions in one commit, over both the AGENTS.md 500-insertion
   cap and G8's own "each under 500 INSERTIONS" clause, while the block orders the core and
   its tests as ONE commit. Rather than split against the block or declare an oversize
   commit, I tightened comment and docstring WORDING — which Convention 5 leaves to me — to
   272 + 220 = 492. No SPEC-mandated behaviour, no refusal code, no test property and no
   paragraph of the DELIBERATE ABSENCE or totality material was dropped; only reflowing and
   the merging of some multi-paragraph docstrings into single ones.
2. **A null or absent reason is an ABSENT reason.** `_reason_text` maps both a missing
   `reason` key and an explicit `None` to `""`, so both trip MISSING_REASON. Coercing them
   with the totality guard instead would produce the literal text `"None"`, which is not
   empty and not whitespace and would therefore sail past the very check that code names.
   Two of the six MISSING_REASON cases pin this.
3. **A non-iterable argument is ONE entry, and so are a `str`, a bytes-like, a `Mapping`
   and a `HunkRejection`.** This follows the shape `normalise_old_side` uses in
   `hunk_identity.py` for the same situation. It matters most for `rejected`: a caller that
   passes a single wire-form mapping without wrapping it in a list gets that one rejection
   back rather than two strange ids named `id` and `reason`. It is also why
   `approved="h1h2"` is reported as one unknown id and not as four.
4. **`_total_text` is re-stated, not imported.** G6(b) requires the module's imports to name
   ONLY standard-library modules, so importing `hunk_identity._total_text` was not
   available; the name is private there in any case. The module docstring says so at the
   point a reader would ask.
5. **The §4 sentence about a malformed rejection entry is subordinate to the §3 ORDER.**
   The block says an entry in none of the three spellings "is a REFUSAL_MISSING_REASON",
   but §3 makes UNKNOWN_HUNK strictly earlier, so a malformed entry whose recovered id is
   not in `known_hunk_ids` returns UNKNOWN_HUNK. I read the §4 sentence as naming the fault
   CLASS rather than overriding the order it is stated beside, and the bare-string test
   uses a KNOWN id so both readings give the same answer. Flagging it because it is the one
   place the SPEC's two halves could be read against each other.
6. **`known_hunk_ids` is deduplicated, preserving first appearance, before `pending` is
   computed.** The block calls it "the known SET", and a set cannot hold a repeat; without
   this a duplicated known id would appear twice in `pending` and desynchronise the "5/8
   hunks" count the docstring explains `pending` exists to keep single-sourced.
7. **`_ID_KEYS` accepts `hunk_id` as well as `id`.** The feature file's wire form is
   `rejected[{id, reason}]` and that is the primary spelling; `hunk_id` is accepted so a
   caller that dumps a `HunkRejection` to a dict round-trips. No test depends on any other
   key existing.

No verdict on this round's work is written here; the reviewer gates it.

## Next

The reviewer re-runs all eight gates over
`cb49a3ea..<C5>` on `feature/f033-hunk-approval-v2`. The next build round is T002's second
piece, the all-or-nothing SUBSET APPLY on `packages/orchestration/source_apply.py`, whose
`apply_structured_patch` takes no subset today; it validates its input against
`decide_hunk_approval` and still touches neither the write door nor its import guard.
