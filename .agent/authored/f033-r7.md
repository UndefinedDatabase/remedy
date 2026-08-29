# F033 — Hunk-level diff approval · ROUND 7 · THE APPROVED SUBSET DIFF

SESSION 2 of feature F033. Round 7, rounds so far 7.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R7`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON IS A SPEC, NOT A SLICE. You write the module and its tests from the
   description. Names, signatures, refusal codes, the refusal ORDER and the
   behaviours the SPEC fixes are binding; structure, comment wording and test
   names are yours. If the SPEC is impossible, STOP and say so.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>`. NEVER write a base
   blob over a tracked file.
9. Purge `__pycache__` or use `python3 -B` whenever a mutation must reach a test.

## Base

BASE is `1fdda40215da1f15c248df1ea46cf7b940781a74`, the round 6 handback commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 6 passed every gate; the reviewer re-ran all eight itself, reproduced every
reading, and additionally ran a FOURTH mutation the block never ordered — making
`pending` always empty — which also went red, so that remainder is genuinely
pinned rather than merely computed. Its verdict is in the record slice below.

Round 6 answered "is this selection coherent?". This round answers the next
question: WHICH BYTES does an approved selection actually apply? The plan's step
1 calls it the all-or-nothing subset apply, and it splits cleanly in two. The
part that decides which hunks go in, and emits exactly them, is pure text and is
this round. The part that lands them on a branch is the applier's, which already
has snapshots and rollback, and is a later round.

FOUR FACTS THE REVIEWER MEASURED AT `1fdda402` RATHER THAN ASSUMED, each with a
red control, because the whole design rests on them:

- `packages/orchestration/source_apply.py`'s `_apply_hunks` positions every hunk
  by its OLD-side start and validates context against the ORIGINAL file, keeping
  its own running `offset` for the result. IT NEVER READS THE NEW-SIDE HEADER:
  skewing `+10,3` to `+999,3` applies and gives a byte-identical result. So
  DROPPING A HUNK NEEDS NO HEADER RENUMBERING AT ALL, and a subset is a pure
  selection rather than an arithmetic.
- A hunk whose context does not match the file makes `_apply_hunks` return
  `None`, so a bad selection fails loudly rather than half-applying.
- `parse_unified_diff_to_view` carries, per hunk, its `header` VERBATIM and its
  `lines` as `{kind, content}` with `kind` in `ctx`/`del`/`add` — everything a
  re-emission needs, and the hunk `id` beside it, so the subset is keyed on the
  ONE identity DECISION F033 D3 established rather than on a second one.
- Re-emitting EVERY hunk from that view, header verbatim and one line per view
  line prefixed ` `/`-`/`+`, applies BYTE-IDENTICALLY to applying the raw diff;
  swapping the `add` and `del` prefixes changes the result, so the prefix map is
  load-bearing and a test must pin it.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 6 verdict into `.agent/live_review.md`
- C3 the reviewer prose slip into `.agent/prose_slips.md`
- C4 the subset module and its tests, together
- C5 the handback

## Change set — these paths and nothing else

    .agent/authored/f033-r7.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/hunk_subset_diff.py
    tests/orchestration/test_hunk_subset_diff.py
    .agent/handoff.md

The last two are NEW FILES. This round does NOT touch
`packages/orchestration/source_apply.py`, `packages/orchestration/diff_parser.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_identity.py`,
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py` or
`docs/roadmap/STATUS.md`.

## SPEC — `packages/orchestration/hunk_subset_diff.py`

A NEW module.

### 1. What it is, and what it deliberately is not

Given a unified diff and the hunk ids an operator approved, it produces the
unified diff holding EXACTLY those hunks and nothing else, ready to hand to the
applier one file at a time. It APPLIES NOTHING, opens no file, and never learns
whether the subset would land cleanly — a conflict is the applier's answer.

It imports `packages/orchestration/diff_parser.py` and the standard library, and
NOTHING ELSE. That import is the point of the module rather than an accident: the
hunk ids it selects on are the ones `diff_parser` already computes through
`hunk_identity`, so there is still exactly ONE hunk identity in this repository —
DECISION F033 D3. It MUST NOT import `packages/orchestration/source_apply.py`:
this module decides WHICH bytes, the applier decides whether they land, and
`tests/ui_server/test_command_channel.py` already names the applier a module the
write door may never reach. Write both absences into the module docstring, in the
idiom `hunk_identity.py` and `hunk_approval.py` use.

Every public name is TOTAL: it NEVER raises, on any input at all — a non-string
diff, `None`, a non-iterable id set, an id that is not a string. Same reason as
`hunk_approval.py`: this runs behind an approval screen.

### 2. The types

- `ApprovedSubsetFile`, a frozen dataclass: `path: str`, `diff: str`,
  `hunk_ids: tuple[str, ...]`. `diff` is the hunk text for ONE file, which is
  exactly what `UnifiedDiff(path=..., diff=...)` in
  `packages/orchestration/structured_patch.py` carries; `hunk_ids` are the ids
  emitted into it, in the diff's own order.
- `ApprovedSubsetDiff`, a frozen dataclass: `files: tuple[ApprovedSubsetFile, ...]`
  in the diff's own file order, and `selected: tuple[str, ...]` — every id
  emitted across all files, in the diff's own order.
- `SubsetRefusal`, a frozen dataclass: `code: str`, `message: str`,
  `hunk_ids: tuple[str, ...]`. Same shape as `HunkApprovalRefusal` on purpose —
  a caller handles both the same way — but a DISTINCT type, because these codes
  are about the DIFF and those are about the SELECTION.

### 3. The refusal codes, and the ORDER they are checked in

Module-level constants: `SUBSET_REFUSAL_NO_APPROVED_IDS` (`"no_approved_ids"`),
`SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW` (`"untrustworthy_view"`),
`SUBSET_REFUSAL_ABSENT_HUNK` (`"absent_hunk"`).

Checked in exactly that order; the FIRST that trips is returned, and a test pins
the order with an input that trips two at once.

WHY UNTRUSTWORTHY BEFORE ABSENT, and this is the subtle one: a truncated view is
missing hunks it never showed, so "this approved id is not in the diff" is
UNKNOWABLE while the view is untrustworthy. Reporting absence first would blame
the operator's selection for the parser's ceiling.

- NO_APPROVED_IDS when the approved set is empty. Landing nothing is not an
  all-or-nothing apply of nothing, it is a caller mistake;
  `decide_hunk_approval` already refuses an empty DECISION, and a full-rejection
  round reaches the repair loop rather than the applier.
- UNTRUSTWORTHY_VIEW when the parsed view's top-level `truncated` is true, or
  when any file the selection touches carries a `note` or a `status` of
  `binary`. Those are the states in which re-emitting from the view would
  silently produce a diff that is not the diff. `hunk_ids` carries the approved
  ids that fall in such files, and is empty when `truncated` alone tripped it.
- ABSENT_HUNK when an approved id is not among the ids the view carries.
  `hunk_ids` carries every such id, DEDUPLICATED and in the order the caller
  gave them. This is a real integrity check rather than a repeat of round 6's
  `unknown_hunk`: the diff can be re-parsed between the decision and the apply,
  and an id that has since vanished must stop the apply rather than shrink it.

### 4. The entry point

    build_approved_subset_diff(
        diff_text: str,
        approved_hunk_ids: Iterable[str],
    ) -> ApprovedSubsetDiff | SubsetRefusal

Parse `diff_text` with `parse_unified_diff_to_view`. Then, for each file in the
view's order, keep the hunks whose `id` is approved, and emit for that file:

- each kept hunk's `header` VERBATIM, unchanged — the reviewer's measurement
  above is why no renumbering happens, and inventing one would be a defect;
- then one line per entry of that hunk's `lines`, as the prefix for its `kind`
  followed by its `content`: `ctx` takes a single SPACE, `del` a `-`, `add` a
  `+`. A `kind` that is none of those three is an untrustworthy view, not a line
  to guess at.

A file with no kept hunk does not appear at all. Each `ApprovedSubsetFile.diff`
ends with exactly one trailing newline, and carries no `diff --git`, `---` or
`+++` header: `_apply_unified_diff` takes the path from `UnifiedDiff.path` and
`_apply_hunks` reads only `@@` lines, so a header there would be noise the
applier skips.

Duplicate approved ids are harmless and are NOT a refusal — the operator asked
for a hunk twice, which is the same request. Each hunk is emitted ONCE.

Coerce ids to text with the same totality guard `hunk_approval.py` uses. A
`diff_text` that is not a string is coerced the same way before parsing, so a
wrong-typed call becomes a refusal rather than an exception.

## SPEC — `tests/orchestration/test_hunk_subset_diff.py`

A NEW file. Cover, at least:

- THE ROUND-TRIP PROPERTY, which is the one that matters: build a fixture file
  and a two-hunk diff over it; assert that selecting BOTH hunks produces a diff
  which, applied, gives byte-identically what applying the RAW diff gives; and
  that selecting each hunk ALONE changes exactly that hunk's lines and leaves
  the other's alone. Import `_apply_hunks` from
  `packages/orchestration/source_apply.py` for this, and say in a comment why a
  private name is the right import here: the property is about the applier's
  real behaviour, and the public `apply_structured_patch` needs a repository, a
  job and a data directory that this pure test has no business building.
- THE PREFIX MAP is load-bearing: a test that would fail if `add` and `del` were
  swapped.
- Headers come through VERBATIM — assert the emitted header string equals the
  one in the source diff, character for character.
- Each of the three refusal codes on its own, and the ORDER, with one input that
  trips two.
- A multi-FILE diff: only files with a kept hunk appear, in the diff's order,
  and `selected` spans files in the diff's order.
- Duplicate approved ids emit the hunk once and do not refuse.
- TOTALITY: `None`, a non-string diff, a non-iterable id set and a non-string id
  each return a value rather than raising.

Name each test for the property it pins, not for the function it calls.

## The slices

<<<SLICE PLANF033R7
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 2 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | closed round 5, DECISION F033 D3 |
| the approval decision core | done | round 6, 30 cases |
| the approved subset diff | done | this round |
| landing the subset all-or-nothing | open | next, through `source_apply.py` |
| the write-door command and its exposure | open | needs the import guard widened |
| the hunk-decision ledger in evidence | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Land the subset: feed the per-file diffs this round emits through
   `apply_structured_patch`, all-or-nothing, so a conflict inside the approved
   set leaves NOTHING applied and names the hunk that conflicted. The applier
   already snapshots and reverts; the round proves the atomicity, it does not
   build it.
2. Then the write door: `approve_hunks` reaches the applier through a service
   seam, never by importing it — `packages.orchestration.source_apply` is in
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`.
3. Then the hunk-decision ledger in evidence, which T003's report line reads.

## Risks
- The door's import guard is an EQUALITY guard, so any new import is widened in
  the SAME commit that adds it, or the branch tip ships red.
- A truncated or binary view cannot be re-emitted faithfully; the subset builder
  refuses rather than shrinking a diff silently, and the apply round must keep
  that refusal rather than defaulting past it.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R7

<<<SLICE RECORDF033R7
Gate: F033 R6 — THE DECISION CORE. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `1fdda402` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 24108 bytes at sha256 `a68745f0…09ee19`, byte-identical to the reviewer's own pre-emission original, with ONE blob id at C0b. THE RECORD APPEND at `f3a8b0ed` reconstructs 1456716 plus one newline plus 5024 to 1461741, the committed blob exactly, base a byte PREFIX, N counted at 2, the last two blank-line units equal to the slice's paragraphs IN ORDER, and a byte flipped at offset 1457017 — inside the FIRST appended paragraph, spanning 1456717 to 1459909 — rejected by BOTH readers. THE LEDGER moved exactly where the block allowed: registered 300 UNMOVED with NO id added, `Done:` 44 to 45 over 42 to 43 with the added resolved id exactly `R-0739`, `Landed:` 12 UNMOVED with the `Landed: R-0739` line still present beside its new `Done:` paragraph as this append-only record requires, `Gate:` 122 to 123, the open set 258 to 257, and `^Gate: F033 R5 — ` exactly 1. THE PROSE-SLIPS APPEND at `da81db54` is 18681 plus 897 equals 19578 byte for byte with the base a prefix and both dated lines present. THE MODULE AGAINST THE SPEC: `ruff check` over both new files exits 0 at "All checks passed!"; the AST import set is `__future__`, `collections`, `collections.abc`, `dataclasses` and `typing`, with NO non-standard-library entry, so the module's own claim to import nothing of this package is measured rather than asserted; the five refusal constants are module-level with exactly the ordered values; and `open(`, `import os`, `import subprocess`, `import logging` and `Path` all read 0. THE MUTATION RED-PROOFS WERE REPRODUCED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE at `41050925`, with its own anchors, each asserted unique before replacement, under `python3 -B`: the UNMUTATED CONTROL is a real exit 0 at 30 passed, disabling the overlap check is exit 1 at 2 failed, accepting a whitespace-only reason is exit 1 at 2 failed, and disabling the unknown-id check is exit 1 at 4 failed. THE REVIEWER THEN RAN A FOURTH MUTATION THE BLOCK NEVER ORDERED — returning an empty `pending` tuple unconditionally — and it went RED at 3 failed, naming `test_a_mixed_decision_reports_approved_rejected_and_the_pending_remainder`, `test_pending_follows_the_order_the_known_set_gave` and `test_a_non_string_id_is_compared_as_text`, so the PENDING remainder is genuinely pinned and not merely computed. The reverted control returned to exit 0 at 30 passed, the worktree was removed by exact path and pruned, and the primary checkout's `git status --porcelain` was empty throughout. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the new `tests/orchestration/test_hunk_approval.py` 30, `tests/orchestration/test_hunk_identity.py` 10, `tests/orchestration/test_diff_parser.py` 50, `tests/regression/test_resource_safety.py` 21, `tests/test_no_interactive_guard.py` 6 and the canary `tests/cli/test_golden_path.py` 42. THE STRUCTURE: six single-parent commits of 337, 249, 15, 4, 4 and 492 insertions, every one under 500, the path set matching the change set in BOTH directions with `.agent/handoff.md` the sole expected absence, residue 0 in every target against a control of 5 and 6, `git ls-files .remedy-wt` 0, and `ui_server.py`, `command_catalog.py`, `source_apply.py`, `hunk_identity.py`, `diff_parser.py` and `docs/roadmap/STATUS.md` all byte-identical across the round. THE WORKER DECLARED A TENSION IN THE REVIEWER'S OWN SPEC AND RESOLVED IT CORRECTLY: §4 called a malformed rejection entry a `REFUSAL_MISSING_REASON` while §3 fixed `UNKNOWN_HUNK` strictly earlier, and it read §4 as naming the fault CLASS rather than overriding the order stated beside it — which is the reading the shipped order makes true, and which the reviewer confirmed by reading the code rather than the handback. It damaged nothing on disk, so under operator amendment amend0827 rule 2 it spends no id and buys no correction round; it is the dated line this round's C3 puts in `.agent/prose_slips.md`. The reviewer also read the module in full for defects the gates could not see and found none: the totality guards sit at the BOUNDARY so the rules below them need no catch-all that would swallow a real defect, and treating an absent reason and an explicit `None` alike is right, because coercing `None` to the literal text would sail past the very emptiness check the code names.
<<<END RECORDF033R7

<<<SLICE SLIPSF033R7

2026-08-29 · F033 R6 · The block's SPEC §4 said a rejection entry in none of the three accepted spellings "is a `REFUSAL_MISSING_REASON`" while its own §3 fixed `UNKNOWN_HUNK` strictly earlier in the refusal order, so the two clauses are readable against each other; the worker took §4 as naming the fault class rather than overriding the order, shipped the order §3 fixed, and declared the tension.
<<<END SLIPSF033R7

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C4, so the handback at C5 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C5,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r7.md` and of `.remedy-wt/f033-r7-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r7.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1461741 bytes, plus one newline plus RECORDF033R7 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R7 — report it
  — and compare the LAST N blank-line units of the C2 blob against the slice's
  paragraphs IN ORDER. NEGATIVE CONTROL at an offset your script PROVES lies
  inside the FIRST appended paragraph; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and at C2 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`, and
  `^Gate: F\d+ R\d+ — `; report the open set at both. Ordered: registered 300
  UNMOVED, `Done:` 45 over 43 UNMOVED, `Landed:` 12 UNMOVED, the open set 257
  UNMOVED — this round registers and resolves NOTHING — and `Gate:` 123 to 124.
  `^Gate: F033 R6 — ` at C2 must read exactly 1.
- **G5 THE PROSE-SLIPS APPEND at C3.** The BASE blob of `.agent/prose_slips.md`,
  which must be 19578 bytes, plus SLIPSF033R7 equals the C3 blob byte for byte —
  the slice OPENS with a blank line, so no separator is added. BASE a byte
  PREFIX; result ending in exactly one newline; the lines that commit's diff ADDS
  are exactly the slice's lines IN ORDER. Report `^2026-08-29 · F033 R6 · ` at C3
  as exactly 1.
- **G6 THE MODULE AGAINST THE SPEC at C4.** Each as a measurement over
  `packages/orchestration/hunk_subset_diff.py`. (a) `ruff check` over both new
  files exits 0 — report its summary line. (b) By AST, not by grep: report the
  FULL import list; every entry must be either standard library or exactly
  `packages.orchestration.diff_parser`, and `source_apply` must appear ZERO
  times anywhere in the module's text. (c) The three refusal constants are
  module-level assignments with exactly the values `no_approved_ids`,
  `untrustworthy_view` and `absent_hunk` — report each name with its value.
  (d) TOTALITY, as a real probe rather than an assertion: call
  `build_approved_subset_diff` with each of `None`, `object()`, an integer and a
  non-iterable id set, in both argument positions, and report that every call
  RETURNED and what type came back. (e) `open(`, `import os`,
  `import subprocess` and `import logging` each read 0.
- **G7 THE MUTATION RED-PROOFS at C4.** In a DISPOSABLE `git worktree` at C4,
  never in the primary checkout, with `python3 -B`. FIRST the UNMUTATED CONTROL:
  `python3 -B -m pytest tests/orchestration/test_hunk_subset_diff.py -q` must be
  a REAL exit 0 — report the count. Then, one at a time, reverting fully between
  each, asserting the anchor is UNIQUE before replacing it, and reporting the
  REAL exit code, the failure count and the NAME of each failing test:
  (i) swap the `add` and `del` prefixes in the emission;
  (ii) make the UNTRUSTWORTHY_VIEW check never trip;
  (iii) make the ABSENT_HUNK check never trip.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red — a green mutation is a real finding about the
  tests and the reviewer wants it. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/orchestration/test_hunk_subset_diff.py` (new
  — report the count), `tests/orchestration/test_hunk_approval.py` (30 at BASE),
  `tests/orchestration/test_diff_parser.py` (50 at BASE),
  `tests/orchestration/test_hunk_identity.py` (10 at BASE),
  `tests/orchestration/test_source_apply.py` (34 at BASE — the reviewer resolved
  this path and ran it, so it is ordered outright rather than conditionally) and
  the canary `tests/cli/test_golden_path.py` (42 at BASE). Then
  walk `git rev-list --reverse BASE..C4`: each commit exactly ONE parent, each
  under 500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions
  plus deletions — and report the per-commit list. C5's own numbers are NOT
  ordered here; the reviewer measures C5 at the next gate. Report the range's
  path set against the change set in BOTH directions. Count `<<<SLICE ` and
  `<<<END ` in `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/hunk_subset_diff.py` and
  `tests/orchestration/test_hunk_subset_diff.py`: each 0, against
  `.agent/authored/f033-r7.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 2,
round 7, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts — one line
per gate with real numbers, the item-status table with every ordered item exactly
once, and your deviations. Quote `build_approved_subset_diff`'s final signature,
and list the test names you wrote with the property each pins. No length cap.
Write no verdict on your own work.
