# F033 — Hunk-level diff approval · ROUND 3 · THE PARSER SEAM

SESSION 1 of feature F033. Round 3, rounds so far 3.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the handback's deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R3` — because a slice body may quote the bare
   tokens inline.
3. Every WHOLE-FILE slice ends with exactly one trailing newline.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PRODUCTION CODE IS A SPEC, NOT A SLICE. You write it from the description.
   Names, signatures, constants and behaviours the SPEC fixes are binding;
   internal structure and comment wording are yours. If the SPEC is impossible or
   self-contradictory, STOP and say so rather than inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.

## Base

BASE is `fa745748`, the round 2 handback commit, on branch
`feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD` before C0a and
STOP if it differs.

## Goal

Wire `hunk_identity` into the diff parser so hunk ids stop being positional, bump
`DIFF_VIEW_VERSION` to 2 through the seam the parser's own docstring declares,
and move the tests that pin the old shape — replacing two id LITERALS with the
stability PROPERTY they were standing in for.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 2 verdict into `.agent/live_review.md`
- C3 the parser, the version bump and the tests, together
- C4 the handback

## Change set — these paths and nothing else

    .agent/authored/f033-r3.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/diff_parser.py
    tests/orchestration/test_diff_parser.py
    .agent/handoff.md

This round does NOT touch `packages/orchestration/hunk_identity.py`,
`packages/orchestration/diff_view_source.py`,
`packages/orchestration/diff_repair.py`, `packages/orchestration/ui_server.py`,
anything under `apps/ui/`, or `docs/roadmap/STATUS.md`. The client-side fallback
and the diff-repair consolidation are later rounds, deliberately.

## SPEC — `packages/orchestration/diff_parser.py`

### 1. The version

`DIFF_VIEW_VERSION` becomes `2`. Its comment currently calls F033's content-hash
ids "the first planned bump"; it now records that the bump HAS happened and what
changed in it — hunk `id` values are content-derived rather than positional.

### 2. The id, computed in the flush loop

Import `hunk_identity` from `packages.orchestration.hunk_identity`. In the
per-file flush loop that today writes `"id": f"{file_index}:{hunk_index}"`,
replace that value with a content id computed from:

- `path` — the value `region.resolve_path()` already yields for that file, the
  same one written to the file's `"path"` key.
- The hunk's OLD SIDE: the `"content"` value of each entry in `raw["lines"]`
  whose `"kind"` is `DIFF_LINE_CONTEXT` or `DIFF_LINE_DELETED`, in order.
  `DIFF_LINE_ADDED` entries are EXCLUDED. That exclusion is the point: the same
  logical hunk re-emitted next round with a different fix keeps its id, which is
  what the feature file's stability property requires, and the parser already
  computes exactly this membership as `on_old` during the walk.
- `occurrence` — how many EARLIER hunks IN THE SAME FILE have a byte-identical
  normalised old side. Count it per file, resetting for each file: keep a mapping
  from the normalised old-side text to a running count, pass the count BEFORE
  incrementing, then increment. Do not key it on the finished id.

`file_index` and `hunk_index` stop contributing to the id. `hunk_index` is still
needed as the loop variable; if `file_index` becomes unused, stop enumerating.

### 3. The docstring's contract note, which is now WRONG on two counts

The module docstring's CONTRACT NOTES currently say hunk ids are PROVISIONAL and
that "F033 replaces them with content-hash ids, and `DIFF_VIEW_VERSION` is the
seam through which it does so". Rewrite that bullet to describe what the ids ARE
now, naming `packages/orchestration/hunk_identity.py` as where the identity is
computed and stating the stability property a reader can rely on.

It also says `intraline` did not force a bump "because version 1 has never been
served to anything — there is no endpoint yet". THAT IS NO LONGER TRUE and it is
the sentence a later reader would rely on to skip a bump. F256 added the endpoint:
`packages/orchestration/ui_server.py` builds the envelope through
`packages/orchestration/diff_view_source.py`'s `build_diff_view`, which carries
`DIFF_VIEW_VERSION` straight out to a consumer. Correct the sentence rather than
delete it — say that version 1 WAS served once the endpoint landed, and that this
is why the id change takes a real bump instead of riding in unversioned. Do not
restate the old claim anywhere.

### 4. What must NOT change

The parser stays PURE and TOTAL exactly as its docstring rules: no file system,
no subprocess, no network, no logging, no global mutable state, and it NEVER
raises on malformed input — including the non-`str` early return that already
answers `{"version": DIFF_VIEW_VERSION, ...}`. `hunk_identity` is itself total,
so this holds, but do not introduce a call that can raise around it. Line
`"content"` values, `"header"`, `"old_start"`, `"new_start"`, the per-file
`"stats"`, `"note"`, `"status"` and the ordering of files and hunks are all
untouched: the ONLY key whose value this round changes is a hunk's `"id"`.

## SPEC — `tests/orchestration/test_diff_parser.py`

FOUR existing assertions pin the shape this round changes. Move them; do not
delete a test.

- `test_parse_unified_diff_to_view_reads_empty_input_as_no_files` and
  `test_parse_unified_diff_to_view_reads_non_diff_text_as_no_files` both assert a
  whole dict containing `"version": 1`. They become `2`. Prefer importing
  `DIFF_VIEW_VERSION` and asserting against it, so the next bump moves them
  itself; if you keep a literal, keep exactly one test that pins the literal so
  the constant cannot drift silently, and say in the handback which you chose.
- `test_parse_unified_diff_to_view_keeps_input_order_and_distinct_hunk_ids`
  asserts `ids == ["0:0", "1:0"]` and
  `test_parse_unified_diff_to_view_seeds_each_hunk_from_its_own_header` asserts
  `[h["id"] for h in entry["hunks"]] == ["0:0", "0:1"]`. Those literals are the
  positional shape and cannot survive. Replace each with the PROPERTY it was
  standing in for — that the ids are distinct and well-formed — and keep every
  other assertion in both tests untouched, including the path ordering and the
  `old_start`/`new_start` pairs.

ADD tests for the properties the change exists to create, named for the property:

1. **The stability property, at the parser.** Parse a diff. Then parse a second
   diff, identical except that an EARLIER hunk in the same file has one more
   ADDED line, and assert the LATER hunk's id is UNCHANGED. Positional ids fail
   this and content ids pass it; it is the single most important test in the file.
2. **Added lines do not enter the id.** Two diffs whose hunks share an old side
   but differ in their added lines produce the SAME id for that hunk.
3. **Two identical hunks in one file get distinct ids**, via the occurrence rank.
4. **The id's shape**: every hunk id in a multi-file diff is 16 lowercase hex
   characters, and all ids in one view are distinct.
5. **The same content at a different path gets a different id.**

Use the fixtures already in the file where they fit; add new ones inline
otherwise. Do not add a fixture file.

## The slices

<<<SLICE PLANF033R3
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 1 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| restart, claim, register R-0738 | done | round 1, DECISION F033 D1 |
| the shared identity function and its tests | done | round 2, 10 tests |
| wire the parser, bump DIFF_VIEW_VERSION to 2 | done | this round |
| rule the client's fallback id synthesis | open | next round |
| retire the diff-repair local hunk helper | open | |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Rule the client fallback at `apps/ui/src/api/diffViewModel.ts`, which
   synthesises a positional id when the server sends an empty one, and move the
   TypeScript pins on version 1 and on the `"<n>:<m>"` id form.
2. Retire the local hunk helper in `packages/orchestration/diff_repair.py` onto
   the shared identity, keeping its regression suite green.
3. Then T002: the `approve_hunks` command, its validation and the
   all-or-nothing subset apply.

## Risks
- The diff endpoint added by F256 SERVES this envelope, so the version bump is a
  real consumer-visible change and not a private one.
- The client fallback means an empty server id becomes a POSITIONAL id on screen
  rather than an error, so a content-hash contract can still be violated
  silently until the next round rules it.
- `packages/orchestration/diff_parser.py` is PURE and TOTAL by its own docstring.
  The identity call must not change that.
<<<END PLANF033R3

<<<SLICE RECORDF033R3
Gate: F033 R2 — THE HUNK IDENTITY FUNCTION. THE ROUND PASSED. Every gate was re-executed by the reviewer at `fa745748` from a script of its own, and every reading reproduced. TRANSPORT EQUAL: `749316a2:.agent/authored/f033-r2.md` is 22433 bytes at sha256 `4ee838f6…7e9190`, byte-identical to the reviewer's own original `.remedy-wt/f033-r2-block.md`, which predates this worker; and the authored blob and `.agent/last_block.md` at `1198698c` are ONE blob id. THE TWO APPENDS: `.agent/live_review.md` reconstructs 1431859 plus one newline plus a 3900-byte slice to 1435760, the committed blob exactly, the base a byte PREFIX and the file ending in one newline, with the structural reader counting N at 1 and matching the last unit in order, and the NEGATIVE CONTROL placed at offset 1431900 INSIDE the first appended paragraph rejected by BOTH readers; `.agent/prose_slips.md` reconstructs 17728 plus one newline plus 952 to 18681, carries ZERO lines beginning `- R-`, and its two added lines both match `^2026-\d\d-\d\d · F033 R1 · `. THE LEDGER is UNMOVED where it must be — registered 299 all DISTINCT, `Done:` 44 over 42, `Landed:` 11 and the open set 257 all unchanged — with `Gate:` alone moving 118 to 119 and `^Gate: F033 R1 — ` reading 1. THE MODULE WAS READ, NOT SUMMARISED: it is pure and total as specified, `ruff check` exits 0 at "All checks passed!", the exported names are exactly `HUNK_ID_LENGTH`, `normalise_old_side` and `hunk_identity`, `HUNK_ID_LENGTH` is 16, the source contains ZERO occurrences of the builtin `hash` call and no `import os`, `import subprocess`, `import logging` or `open(`, and the reviewer exercised the shipped function directly: trailing whitespace stable True, leading whitespace significant True, path significant True, occurrence significant True, a lone-surrogate path with a non-`str` line and a non-numeric occurrence still returning a well-formed id, and `normalise_old_side(7)` answering `"7"` rather than raising. THE THREE MUTATION RED-PROOFS WERE REPRODUCED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, with its own anchors rather than the worker's, each anchor asserted UNIQUE before replacement and reverted after: the UNMUTATED CONTROL exits 0 at 10 passed — a colour with no baseline is not evidence — then dropping `path` from the digest exits 1 at 1 failed with `test_the_same_content_at_a_different_path_gets_a_different_id`, dropping `occurrence` exits 1 with `test_two_identical_hunks_in_one_file_are_separated_by_occurrence`, and removing the trailing strip exits 1 with `test_trailing_whitespace_does_not_change_the_id`. Each mutation reddened exactly the one test that names its property and no other, which is what makes the ten green tests mean something. THE STRUCTURE: seven SINGLE-PARENT commits of 331, 251, 16, 2, 4, 348 and 301 insertions, all under 500; the path set matches the change set in BOTH directions; residue 0 and 0 in the plan, the module and the test file against a 6/8 control in the saved block; `git ls-files .remedy-wt` reads 0; and the worktree list holds only the primary checkout, so the worker's own worktree was removed as ordered. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout: the new `tests/orchestration/test_hunk_identity.py` 10 passed, `tests/docs/` 295, `tests/ui_server/` 497, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/orchestration/test_diff_parser.py` 43 and the canary `tests/cli/test_golden_path.py` 42, every REAL exit 0. THE WORKER SHIPPED A TENTH TEST BEYOND THE SPEC'S NINE and was right to: the SPEC called the `errors="replace"` clause load-bearing, and `test_a_lone_surrogate_cannot_be_encoded_strictly` pins the `UnicodeEncodeError` that makes it so, which converts a reviewer's claim into a guard. IT ALSO DECLARED A COLLISION IN THE REVIEWER'S OWN GATE — G5 forbade the substring `hash(` in a module the SPEC required to EXPLAIN why the builtin is unused, so a natural docstring would have reddened a gate over prose rather than over code — and it wrote around the collision in the prose instead of weakening either half, then reported it. That is a reviewer slip, it damaged nothing on disk, and under amend0827 rule 2 it spends no id and buys no correction round.
<<<END RECORDF033R3

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback.

- **G1 HYGIENE.** `.agent/STOP` read before C0a and before C4, absent both times.
  `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of `<C0a>:.agent/authored/f033-r3.md`
  and of `.remedy-wt/f033-r3-block.md` and whether they are EQUAL; no expected
  digest is stated here because a block cannot carry its own. Then
  `git rev-parse <C0b>:.agent/authored/f033-r3.md` and
  `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** Two readers. (a) the BASE blob, which must be
  1435760 bytes, plus one newline plus RECORDF033R3 equals the C2 blob byte for
  byte; BASE a byte PREFIX; result ending in exactly one newline. (b) let N be
  the paragraph count your script COUNTS in the slice — report it — and compare
  the LAST N blank-line units against the slice's paragraphs IN ORDER. NEGATIVE
  CONTROL at an offset your script PROVES lies inside the FIRST appended
  paragraph; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and C2 count `^- R-\d+ — ` with distinct ids,
  `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`, and
  `^Gate: F\d+ R\d+ — `; report the open set at both. This round registers and
  resolves nothing: registered must stay 299, `Done:` 44 over 42, `Landed:` 11
  and the open set 257, all UNMOVED, with `Gate:` alone moving 119 to 120.
  `^Gate: F033 R2 — ` at C2 must read exactly 1.
- **G5 THE PARSER AGAINST THE SPEC.** At C3, report each as a measurement:
  `python3 -m ruff check packages/orchestration/diff_parser.py tests/orchestration/test_diff_parser.py`
  exits 0 with its real output; `DIFF_VIEW_VERSION` is `2`;
  `parse_unified_diff_to_view` still contains no `import os`, `import subprocess`,
  `import logging` or `open(`; the module imports `hunk_identity`; and the string
  `there is no endpoint yet` occurs ZERO times in the module, which is the stale
  claim §3 of the SPEC orders corrected. Then exercise the SHIPPED parser: parse
  a multi-file diff and print every hunk id, confirming each is 16 lowercase hex
  characters and all are distinct, and print `view["version"]`.
- **G6 THE SUITES.** Serially, one pytest process at a time, in the PRIMARY
  checkout, real exit codes, each exiting 0: `tests/orchestration/test_diff_parser.py`
  (report the count; it was 43 at BASE and this round ADDS tests, so it must be
  higher — report both numbers), `tests/orchestration/test_diff_view_source.py`,
  `tests/orchestration/test_hunk_identity.py` (must still be 10),
  `tests/ui_server/` (497 at BASE — the endpoint serves this envelope, so a
  change here is this round's doing), and the canary
  `tests/cli/test_golden_path.py` (42 at BASE).
- **G7 THE MUTATION RED-PROOFS.** In a DISPOSABLE `git worktree` at C3, never in
  the primary checkout, with `python3 -B`. FIRST the UNMUTATED control over
  `tests/orchestration/test_diff_parser.py` — report its REAL exit code and
  count. Then, one at a time, each reverted before the next:
  (M1) include `DIFF_LINE_ADDED` entries in the old side as well — the
  added-lines-do-not-enter-the-id test must FAIL;
  (M2) pass a constant `0` as `occurrence` — the identical-hunks test must FAIL;
  (M3) set `DIFF_VIEW_VERSION` back to `1` — the version test must FAIL.
  For each, report the REAL exit code, the failed count and the NAME of each
  failing test. Assert each mutation's anchor string is UNIQUE in the file before
  replacing it, and say so. If a mutation comes back GREEN, report that plainly
  and do NOT adjust the test or the code to force a red — a green mutation is
  evidence about reachability and the reviewer owns what it means. Remove the
  worktree BY EXACT PATH, then `git worktree prune`.
- **G8 STRUCTURE.** Walk `git rev-list --reverse BASE..C3`: each commit exactly
  ONE parent, each under 500 INSERTIONS — the `+` column of `git diff --numstat`,
  never insertions plus deletions — and report the per-commit list. C4's own
  numbers are NOT ordered here; the reviewer measures C4 at the next gate. Report
  the range's path set against the change set in BOTH directions. Count
  `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
  `packages/orchestration/diff_parser.py` and
  `tests/orchestration/test_diff_parser.py`: each 0, against
  `.agent/authored/f033-r3.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 1,
round 3, BASE, the changed-files table with real `+/-` from `git diff --numstat`,
one line per gate with real numbers, the item-status table with every ordered
item exactly once, and your deviations. Quote the FINAL text of the parser's
corrected contract-note bullets and the list of test names you added or renamed,
so the reviewer can read the shape without reconstructing it. No length cap.
Write no verdict on your own work.
