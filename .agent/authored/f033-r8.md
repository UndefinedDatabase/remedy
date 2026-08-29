# F033 — Hunk-level diff approval · ROUND 8 · LANDING THE SUBSET

SESSION 2 of feature F033. Round 8, rounds so far 8.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R8`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON IS A SPEC, NOT A SLICE. You write the module and its tests from the
   description. Names, signatures, codes and the behaviours the SPEC fixes are
   binding; structure, comment wording and test names are yours. If the SPEC is
   impossible, STOP and say so rather than inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>`. NEVER write a base
   blob over a tracked file.
9. Purge `__pycache__` or use `python3 -B` whenever a mutation must reach a test.

## Base

BASE is `f0dc48f307acb092291ec9bd6763c9557352a1b7`, the round 7 handback commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 7 passed every gate; the reviewer re-ran all eight itself, stressed the
module's totality with 28 hostile inputs of its own — none raised — and ran a
FOURTH mutation the block never ordered, replacing every emitted header with a
fixed one, which also went red. Its verdict is in the record slice below.

Rounds 6 and 7 decide WHETHER a selection is coherent and WHICH BYTES it means.
This round LANDS those bytes, and it is the last piece of the plan's step 1.

THE ATOMICITY IS INHERITED, NOT BUILT, and this round's real job is to prove it
rather than to write it. `apply_structured_patch` in
`packages/orchestration/source_apply.py` already takes a mandatory verified
snapshot of exactly the paths a patch names, applies each unified diff in turn,
and on ANY failure calls `_rollback_from_snapshot` and stops — the reviewer read
that control flow at `f0dc48f3`. So a conflict inside the approved set already
falls back to nothing-applied. What is missing is the seam that hands it the
subset, and the tests that demonstrate the fallback on a real repository.

TWO CONSTRAINTS THE REVIEWER READ AT `f0dc48f3` AND THE SPEC BELOW DEPENDS ON:

- `validate_structured_patch` rejects a `unified_diff` patch whose any entry has
  an empty `path` or an empty `diff`, and additionally runs
  `unsafe_path_issues(patch.target_paths)`. So the synthesised patch must set
  `target_paths`, not only `unified_diffs`, or it fails validation for a reason
  that has nothing to do with hunks.
- `build_snapshot_path_set` derives the snapshot set from the `file_ops` and
  `unified_diffs` paths. Setting the diffs correctly is therefore what makes the
  snapshot cover exactly the files the subset touches, which is what makes the
  rollback total.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 7 verdict into `.agent/live_review.md`
- C3 the apply seam module
- C4 its tests
- C5 the handback

C3 and C4 are SEPARATE COMMITS on purpose. The tests need a real repository, a
permissioned job and an approved intent, so module-plus-tests in one commit would
run at or over the 500-insertion cap — round 7's equivalent commit landed at 497.
Splitting them is the cap forcing the design, and it is declared here rather than
discovered by you at commit time.

## Change set — these paths and nothing else

    .agent/authored/f033-r8.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/hunk_apply.py
    tests/orchestration/test_hunk_apply.py
    .agent/handoff.md

The last two are NEW FILES. This round does NOT touch
`packages/orchestration/source_apply.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/diff_parser.py`,
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py` or
`docs/roadmap/STATUS.md`. No existing module is edited: this round only ADDS.

## SPEC — `packages/orchestration/hunk_apply.py`

A NEW module: the seam between an approved hunk selection and the applier.

### 1. What it is, and what it deliberately is not

It turns an approved selection into an `apply_structured_patch` call and reports
what happened in the vocabulary of HUNKS rather than of files. It does NOT
re-implement atomicity, does not snapshot, does not roll back, and does not
decide whether a selection is coherent — `decide_hunk_approval` did that. Write
those absences into the module docstring in the idiom the three sibling modules
use, and name all three as the places a reader is looking for.

Unlike `hunk_approval.py` and `hunk_subset_diff.py`, THIS MODULE IS NOT TOTAL and
must not pretend to be: it performs I/O through the applier, and an OSError from
a disappearing repository is a real failure that must not be flattened into a
polite value. Say so explicitly in the docstring, and say why the other two are
different. It catches nothing it cannot name.

### 2. The result type

`HunkApplyOutcome`, a frozen dataclass:

- `applied: bool` — true only when every approved hunk landed.
- `apply_id: str` — the applier's own id, or `""` when no apply was attempted.
- `landed: tuple[str, ...]` — the hunk ids that landed, in the subset's order.
  EMPTY whenever `applied` is false; there is no partial landing, and a caller
  must not have to check two fields to learn that.
- `blocked: tuple[str, ...]` — on failure, the hunk ids the failure is
  attributable to; empty on success.
- `code: str` — `""` on success, otherwise a named code.
- `message: str` — one human sentence, never parsed.

Codes, as module-level constants: `HUNK_APPLY_REFUSED` (`"subset_refused"`) when
`build_approved_subset_diff` refused, `HUNK_APPLY_CONFLICT` (`"conflict"`) when
the applier reported failure, and `HUNK_APPLY_NOTHING_TO_APPLY`
(`"nothing_to_apply"`) when the subset came back with no files at all. When the
subset refuses, carry ITS code and message through in `message` and put its
offending ids in `blocked`, so no information is lost by the wrapping.

### 3. The entry point

    apply_approved_hunks(
        diff_text: str,
        approved_hunk_ids: Iterable[str],
        repo_path: Path,
        *,
        job: Any,
        intent_id: str,
        data_dir: str | None = None,
        job_id: UUID | None = None,
    ) -> HunkApplyOutcome

Steps, in order:

1. Call `build_approved_subset_diff`. A `SubsetRefusal` returns immediately as
   `HUNK_APPLY_REFUSED` with its code and message carried in `message` and its
   `hunk_ids` in `blocked`. NOTHING IS WRITTEN in that case — the applier is not
   called at all, and a test pins that by hashing the repository before and
   after.
2. An `ApprovedSubsetDiff` with no files is `HUNK_APPLY_NOTHING_TO_APPLY`, again
   without calling the applier.
3. Otherwise build `StructuredPatch(intent_kind="unified_diff", unified_diffs=...,
   target_paths=...)` — one `UnifiedDiff(path=file.path, diff=file.diff)` per
   subset file, in the subset's order, and `target_paths` the same paths in the
   same order, because `validate_structured_patch` checks them separately.
4. Call `apply_structured_patch` with the job, intent and data dir it was given,
   passing them through UNCHANGED. This module adds no permission check of its
   own: the applier owns that boundary and a second copy would drift from it.
5. On `result.success`, return `applied=True` with `landed` the subset's
   `selected` tuple and `code` empty.
6. On failure, return `applied=False`, `landed=()` and `code=HUNK_APPLY_CONFLICT`.
   ATTRIBUTION: for each subset file, if any string in `result.errors` STARTS
   WITH that file's path followed by `": "`, that file's `hunk_ids` join
   `blocked`. This is a membership test against paths the module already knows
   exactly, never a parse of an error message. If no path matches — a permission
   refusal, a snapshot refusal, a fence refusal, all of which fail before any
   file is touched — `blocked` is EVERY selected id, because the whole selection
   was stopped. Say in a comment which case is which.

## SPEC — `tests/orchestration/test_hunk_apply.py`

A NEW file. `tests/orchestration/test_source_apply.py` already builds a
permissioned job with an approved intent — read its helper near line 166 and
follow the same recipe rather than inventing one; do not import across test
files.

Cover, at least:

- A CLEAN SUBSET LANDS EXACTLY THE APPROVED HUNKS: a two-hunk diff over a real
  file in a temporary repository, one hunk approved, and the file afterwards
  equals the original with ONLY that hunk's change made. Assert the file's bytes,
  not a line count.
- THE ALL-OR-NOTHING PROOF, which is this round's reason to exist: a subset in
  which one approved hunk cannot apply — build it by editing the file on disk so
  a context line no longer matches — leaves EVERY file BYTE-IDENTICAL to before
  the call. Hash before and after and compare the hashes; `applied` is false and
  `landed` is empty.
- The blocked ids on that failure are the conflicting FILE's hunk ids.
- A refusal from the subset builder returns `HUNK_APPLY_REFUSED`, carries the
  subset code in the message, and writes NOTHING — hashed before and after.
- A job WITHOUT `repo_generated_write`, and an intent that is not approved, each
  fail with nothing written, and `blocked` names every selected id.
- A multi-file subset lands both files.

Name each test for the property it pins.

## The slices

<<<SLICE PLANF033R8
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
| the approved subset diff | done | round 7, 17 cases |
| landing the subset all-or-nothing | done | this round, on `source_apply.py` |
| the write-door command and its exposure | open | next, needs the import guard widened |
| the hunk-decision ledger in evidence | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The write door: expose `approve_hunks` and dispatch it. The door may NOT
   import the applier — `packages.orchestration.source_apply` is in
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py` — so the
   command reaches `apply_approved_hunks` through a service seam, and
   `TestCommandDoorImportGuard`'s ALLOWED_IMPORTS is widened in the SAME commit
   that adds the import, with the decision that widens it.
2. Then the hunk-decision ledger in evidence, which T003's report line reads.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- A truncated or binary view cannot be re-emitted faithfully; the subset builder
  refuses rather than shrinking a diff silently, and every later caller must
  keep that refusal rather than defaulting past it.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R8

<<<SLICE RECORDF033R8
Gate: F033 R7 — THE APPROVED SUBSET DIFF. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `f0dc48f3` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 24748 bytes at sha256 `8634f552…33158a4`, byte-identical to the reviewer's own pre-emission original, with ONE blob id at C0b. THE RECORD APPEND at `d887643a` reconstructs 1461741 plus one newline plus 4515 to 1466257, the committed blob exactly, base a byte PREFIX, N counted at 1, the last unit equal to the slice's paragraph, and a byte flipped at offset 1462142 inside that appended paragraph rejected by BOTH readers. THE LEDGER moved only where allowed: registered 300, `Done:` 45 over 43, `Landed:` 12 and the open set 257 ALL UNMOVED, `Gate:` 123 to 124, and `^Gate: F033 R6 — ` exactly 1. THE PROSE-SLIPS APPEND at `42d0a76f` is 19578 plus 407 equals 19985 byte for byte. THE MODULE AGAINST THE SPEC: `ruff check` exits 0; the AST import set is `__future__`, `collections.abc`, `dataclasses`, `typing` and `packages.orchestration.diff_parser` and NOTHING else, so the module's claim to hold the ONE identity is measured rather than asserted; `source_apply` occurs 0 times in its text; the three refusal constants carry exactly the ordered values; and `open(`, `import os`, `import subprocess`, `import logging` and `Path` all read 0. THE REVIEWER STRESSED TOTALITY BEYOND WHAT THE BLOCK ORDERED, because the module's totality rests on a DEPENDENCY — `parse_unified_diff_to_view` — and the ordered probe coerced its inputs to text before that parser ever saw them, so it never tested the thing that could break. Twenty-eight hostile values were pushed through both argument positions, among them an empty string, a bare `@@`, a header with a non-numeric old start, a hunk count of fourteen digits, a hundred-thousand-character body, a lone surrogate, CRLF bodies, a no-newline-at-end marker and objects whose `__str__` and `__repr__` both raise: ZERO raised, every call returned an `ApprovedSubsetDiff` or a `SubsetRefusal`. THE ROUND-TRIP PROPERTY WAS RE-DERIVED BY THE REVIEWER, not read out of the handback: selecting both hunks of a two-hunk diff and applying the result through `_apply_hunks` is byte-identical to applying the raw diff, the emitted headers match the source character for character, the second hunk alone changes only its own line, a duplicated id emits its hunk exactly once, and an id the diff does not carry refuses as `absent_hunk` naming that id. THE MUTATION RED-PROOFS WERE REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `c4b11af5`, the import path first proved to resolve to the worktree copy: the UNMUTATED CONTROL is a real exit 0 at 17 passed, swapping the add and del prefixes is exit 1 at 3 failed, disabling the untrustworthy check is exit 1 at 4 failed, and disabling the absent check is exit 1 at 2 failed. THE REVIEWER THEN RAN A FOURTH MUTATION THE BLOCK NEVER ORDERED — replacing every emitted header with a fixed `@@ -1,1 +1,1 @@` — and it went RED at 3 failed, naming the round-trip test, the single-hunk test and `test_a_header_is_re_emitted_character_for_character`, so the VERBATIM-HEADER property is genuinely pinned rather than merely true. The reverted control returned to exit 0 at 17, the worktree was removed by exact path and pruned, and the primary checkout was clean throughout. THE SUITES were re-run SERIALLY, every REAL exit 0: the new file 17, `test_hunk_approval.py` 30, `test_diff_parser.py` 50, `test_hunk_identity.py` 10, `test_source_apply.py` 34 and the canary 42. THE STRUCTURE: six single-parent commits of 364, 227, 11, 2, 2 and 497 insertions, every one under 500, the path set matching in BOTH directions with `.agent/handoff.md` the sole expected absence, residue 0 in every target, `git ls-files .remedy-wt` 0, and all seven do-not-touch paths byte-identical across the round. TWO THINGS THE WORKER DECLARED AND THE REVIEWER CONFIRMED. First, the block's SPEC §1 ordered the docstring to name `packages/orchestration/source_apply.py` as the place an apply-seeking reader should go, while G6(b) ordered that same string to read ZERO in the module; the worker satisfied both by naming the applier as `apply_structured_patch` and pointing at the `FORBIDDEN_MODULES` entry instead of spelling the path, which keeps the reader's pointer and the measurement. That is a reviewer-prose defect that damaged nothing on disk and spends no id under operator amendment amend0827 rule 2. Second, the untrustworthy check's third limb — a line kind the prefix map has no entry for — is UNREACHABLE through the public entry point, because the parser emits only the three kinds it knows; it ships as a guard against a future kind and no test exercises it, which the worker declared rather than hid, and which the reviewer confirmed also means `_emit` has no `KeyError` path.
<<<END RECORDF033R8

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C4, so the handback at C5 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C5,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r8.md` and of `.remedy-wt/f033-r8-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r8.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1466257 bytes, plus one newline plus RECORDF033R8 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R8 — report it
  — and compare the LAST N blank-line units of the C2 blob against the slice's
  paragraphs IN ORDER. NEGATIVE CONTROL at an offset your script PROVES lies
  inside the FIRST appended paragraph; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and at C2 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`, and
  `^Gate: F\d+ R\d+ — `; report the open set at both. Ordered: registered 300
  UNMOVED, `Done:` 45 over 43 UNMOVED, `Landed:` 12 UNMOVED, the open set 257
  UNMOVED — this round registers and resolves NOTHING — and `Gate:` 124 to 125.
  `^Gate: F033 R7 — ` at C2 must read exactly 1.
- **G5 THE MODULE AGAINST THE SPEC at C3.** Each as a measurement over
  `packages/orchestration/hunk_apply.py`. (a) `ruff check` over it exits 0 —
  report the summary line. (b) By AST, report the FULL import list; it must
  include `packages.orchestration.hunk_subset_diff` and
  `packages.orchestration.source_apply` and must NOT include
  `packages.orchestration.permissions` or
  `packages.orchestration.approval_queue`, because step 4 forbids a second
  permission boundary. (c) The three codes are module-level assignments with
  exactly the values `subset_refused`, `conflict` and `nothing_to_apply` —
  report each name with its value. (d) `apply_approved_hunks` and
  `HunkApplyOutcome` are both module-level and their signature and field names
  match §2 and §3 — report the extracted signature and field list.
- **G6 THE ALL-OR-NOTHING PROOF at C4, reported as its own reading.** Run
  `python3 -B -m pytest tests/orchestration/test_hunk_apply.py -q` — REAL exit 0,
  report the count. Then report, for the conflict test SPECIFICALLY and by name:
  the sha256 of the target file BEFORE the call and AFTER it, and that they are
  EQUAL. Print those two digests in the handback. A rollback claimed without two
  equal digests beside it is not a proof.
- **G7 THE MUTATION RED-PROOFS at C4.** In a DISPOSABLE `git worktree` at C4,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy of the module. FIRST the UNMUTATED
  CONTROL — REAL exit 0, report the count. Then, one at a time, reverting fully
  between each, asserting the anchor is UNIQUE before replacing it, and
  reporting the REAL exit code, the failure count and the NAME of each failing
  test:
  (i) return `applied=True` with the subset's ids even when the applier failed;
  (ii) call the applier even when the subset REFUSED;
  (iii) make the blocked-id attribution always return every selected id.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red — a green mutation is a real finding about the
  tests and the reviewer wants it. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/orchestration/test_hunk_apply.py`,
  `tests/orchestration/test_source_apply.py` (34 at BASE),
  `tests/orchestration/test_hunk_subset_diff.py` (17 at BASE),
  `tests/orchestration/test_hunk_approval.py` (30 at BASE),
  `tests/regression/test_resource_safety.py` (21 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C4`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. C5's own numbers are NOT ordered
  here; the reviewer measures C5 at the next gate. Report the range's path set
  against the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `packages/orchestration/hunk_apply.py` and
  `tests/orchestration/test_hunk_apply.py`: each 0, against
  `.agent/authored/f033-r8.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 2,
round 8, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts — one line
per gate with real numbers, the item-status table with every ordered item exactly
once, and your deviations. Quote `apply_approved_hunks`'s final signature, the
two sha256 digests G6 asks for, and the test names you wrote with the property
each pins. No length cap. Write no verdict on your own work.
