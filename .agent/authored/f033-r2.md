# F033 — Hunk-level diff approval · ROUND 2 · THE HUNK IDENTITY FUNCTION

SESSION 1 of feature F033. Round 2, rounds so far 2.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive of both delimiter lines. Apply slices BYTE FOR BYTE. Never reflow,
   re-wrap, re-indent or "fix" anything inside a slice. If a slice looks wrong,
   apply it anyway and say so in the handback's deviations.
2. The delimiter lines are transport only and never reach a target file. ANCHOR
   extraction to the NAMED delimiter at line start — `<<<END RECORDF033R2` — not
   to a bare `<<<END `, because a slice body may quote those tokens inline.
3. Every WHOLE-FILE slice ends with exactly one trailing newline.
4. Extract every slice from the COMMITTED blob you save at C0a — never retype one.
5. THE PRODUCTION CODE IN THIS ROUND IS NOT A SLICE. It is a SPEC, and you write
   the code from it. Where the SPEC fixes a name, a signature, a constant or a
   behaviour, that is binding; everything else — internal helpers, comment
   wording, statement order — is yours. If the SPEC is impossible or
   self-contradictory, STOP and say so rather than inventing your way past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Route copying through `shutil.copyfile` and all measurement through
   Python scripts under the gitignored `.remedy-wt/`, run with `python3 -B`.
   Python is 3.10: no backslash inside an f-string expression, so hoist regexes
   into module-level variables.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.

## Goal

Ship the stable hunk-identity function F033 is built on — pure, total,
deterministic across processes — with the stability property proved by tests and
by mutation, and book the round 1 verdict and its two reviewer prose slips.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 1 verdict into `.agent/live_review.md`
- C3 two reviewer slips into `.agent/prose_slips.md`
- C4 the new module and its tests, together
- C5 the handback

## Change set — these paths and nothing else

    .agent/authored/f033-r2.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/hunk_identity.py
    tests/orchestration/test_hunk_identity.py
    .agent/handoff.md

No other path is created, edited or deleted. In particular this round does NOT
touch `packages/orchestration/diff_parser.py`,
`packages/orchestration/diff_view_source.py`,
`packages/orchestration/diff_repair.py`, anything under `apps/ui/`, or
`docs/roadmap/STATUS.md`. Wiring
the function into the parser and bumping `DIFF_VIEW_VERSION` is round 3's work,
deliberately kept out of this one so the identity function can be proved alone.

## Base

BASE is `8dc4721a`, the round 1 handback commit, on branch
`feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD` before C0a and
STOP if it differs — every number below was measured against it.

## The commits

### C0a — save this block
Copy `.remedy-wt/f033-r2-block.md` byte for byte to `.agent/authored/f033-r2.md`
with `shutil.copyfile`. Commit alone: `docs(f033): save the round 2 identity block`.

### C0b — mirror it
Copy that committed file to `.agent/last_block.md` so the two are ONE blob id.
Commit alone: `chore(f033): mirror the round 2 block to last_block`.

### C1 — the plan
Replace `.agent/plan.md` ENTIRELY with PLANF033R2.
Commit alone: `docs(f033): advance the plan to the identity round`.

### C2 — the record
APPEND to `.agent/live_review.md`: one newline, then RECORDF033R2.
Commit alone: `docs(f033): book the round 1 verdict`.

### C3 — the prose slips
APPEND to `.agent/prose_slips.md`: one newline, then SLIPF033R2.
Commit alone: `docs(f033): record two reviewer prose slips from round 1`.

### C4 — the module and its tests
Create `packages/orchestration/hunk_identity.py` and
`tests/orchestration/test_hunk_identity.py` from the SPEC below. One commit,
both files: `feat(f033): add the stable hunk identity function`.

### C5 — the handback
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
Commit alone: `docs(f033): hand back the round 2 identity result`.

Push with `git push`. Open no pull request. Merge nothing.

## SPEC — `packages/orchestration/hunk_identity.py`

A NEW module. Pure and total: no file system, no subprocess, no network, no
logging, no global mutable state, and it NEVER raises on any input. It imports
only from the standard library.

Module docstring states WHY the module exists — F033 needs one hunk identity
shared by the diff viewer and diff-repair, and `diff_parser.py`'s
`"<file_index>:<hunk_index>"` ids are positional, so any edit that inserts a hunk
renumbers every hunk after it. Name that this is the module
`packages/orchestration/diff_parser.py`'s docstring points at when it says F033
replaces the provisional ids and `DIFF_VIEW_VERSION` is the seam. State the
deliberate absence too: this module does NOT parse diffs and does not know what a
diff is — it takes lines that a caller has already identified as a hunk's old
side — because a reader will search here for parsing and must be told it is in
`diff_parser.py`.

Public names, exactly these:

    HUNK_ID_LENGTH = 16

    def normalise_old_side(lines: Iterable[str]) -> str
    def hunk_identity(path: str, old_side_lines: Iterable[str], occurrence: int = 0) -> str

`normalise_old_side` — for each line, remove TRAILING whitespace only, including
a trailing `\r`; join the results with `\n`. LEADING whitespace is preserved
exactly, because indentation is meaning in every language this repository
handles and two hunks differing only in indentation are different hunks. Internal
whitespace runs are NOT collapsed, for the same reason. A non-`str` entry is
coerced with `str()` rather than rejected — that is what makes the function
total. An empty iterable normalises to the empty string.

`hunk_identity` — returns the first `HUNK_ID_LENGTH` characters of the lowercase
hexadecimal SHA-256 of, in this order:

    path, then a NUL byte, then normalise_old_side(old_side_lines), then a NUL
    byte, then the decimal string of occurrence

encoded UTF-8 with `errors="replace"`, so no input can raise a
`UnicodeEncodeError`. The NUL separators exist so that a path ending in the first
line of the context cannot collide with a shorter path and a longer context.
`path` and `occurrence` are coerced with `str()` and `int()` respectively inside
a total guard: a value that cannot be coerced contributes its `repr()` rather
than raising.

`occurrence` disambiguates EXACT duplicates. Two hunks in the SAME file whose
normalised old sides are byte-identical would otherwise share an id; the caller
passes 0 for the first such hunk, 1 for the second, and so on. It is the minimal
disambiguator that keeps the id independent of position: an unrelated edit
elsewhere in the file changes neither a hunk's context nor its rank among its
identical siblings.

USE `hashlib.sha256`. Do NOT use the builtin `hash()` anywhere: it is salted per
process by PEP 456, so an id built on it would differ between two runs of the
same program, and a test below proves this module does not.

The one-line WHY comment sits directly above each public definition, per
AGENTS.md's discoverability conventions.

## SPEC — `tests/orchestration/test_hunk_identity.py`

Tests are named after the source they cover, the repository's pattern. Cover at
least these properties, one test each, named for the property rather than the
mechanism:

1. The same hunk re-emitted keeps its id — identical inputs, identical output.
2. An edit elsewhere in the file leaves other hunks' ids unchanged: build two
   hunks from one file, change the FIRST hunk's lines, and assert the SECOND
   hunk's id is unchanged. This is the stability property the feature turns on.
3. Trailing whitespace does not change the id — a line with trailing spaces, a
   `\r`, and a bare line all give one id.
4. LEADING whitespace DOES change the id. This is the negative of 3 and it is
   what stops the normalisation being over-broad.
5. The same content at a different path gets a different id.
6. Two identical hunks in one file get different ids, via `occurrence`.
7. The id is stable ACROSS PROCESSES. Run a subprocess with a DIFFERENT
   `PYTHONHASHSEED` in its environment — set it explicitly to two different fixed
   values rather than relying on the default — have it print `hunk_identity(...)`
   for fixed inputs, and assert both runs print the same value as the in-process
   call. A salted `hash()` fails this and `hashlib` passes it.
8. It never raises on hostile input: an empty iterable, an empty path, a lone
   surrogate such as `"\ud800"` in BOTH the path and a line, a non-`str` line, a
   negative `occurrence`, an `occurrence` that is not a number at all such as
   `"x"` — which is what the totality guard on `int()` exists for — and a very
   long line. Assert a well-formed id comes back in every case, not merely that
   nothing raised. The reviewer measured that `"\ud800".encode("utf-8")` raises
   `UnicodeEncodeError` while `errors="replace"` yields `b"?"`, so the encoding
   clause in the SPEC is load-bearing rather than decorative.
9. The id's shape: exactly `HUNK_ID_LENGTH` characters, all lowercase hex.

Use the repository's existing test style in `tests/orchestration/`. Do not add a
fixture file; construct inputs inline.

## The slices

<<<SLICE PLANF033R2
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
| restart F033 from current main | done | round 1, DECISION F033 D1 |
| claim F033, book the F257 verdict, register R-0738 | done | round 1 |
| survey the hunk-identity surface | done | round 1, in the handback |
| the shared identity function and its tests | done | this round |
| wire it into the parser, bump DIFF_VIEW_VERSION | open | round 3 |
| rule the client's fallback id synthesis | open | round 3 |
| retire the diff-repair local hunk helper | open | round 4 |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Round 3 wires `hunk_identity` into `packages/orchestration/diff_parser.py`,
   bumps `DIFF_VIEW_VERSION` to 2 and moves the tests that pin version 1.
2. Round 3 also rules the client fallback at `apps/ui/src/api/diffViewModel.ts`,
   which synthesises a positional id when the server sends an empty one.
3. Round 4 retires the local hunk helper in
   `packages/orchestration/diff_repair.py` onto the shared identity.

## Risks
- `packages/orchestration/diff_parser.py` is PURE and TOTAL by its own docstring
  and never raises on malformed input. The identity function must not change that.
- The client fallback means an empty server id becomes a POSITIONAL id on screen
  rather than an error, so a content-hash contract can be violated silently. It
  is ruled in round 3, not worked around here.
- The parked branch `feature/f033-hunk-approval` at `ed040812` holds a 574-line
  inventory taken at `32cde54e`. It is INPUT to be re-derived, never fact.
<<<END PLANF033R2

<<<SLICE RECORDF033R2
Gate: F033 R1 — THE RESTART AND CLAIM ROUND. THE ROUND PASSED. Every gate was re-executed by the reviewer at `8dc4721a` from a script of its own, and every reading reproduced exactly. TRANSPORT EQUAL: the committed blob `6379b23f:.agent/authored/f033-r1.md` is 28666 bytes at sha256 `144702a2…cd6178`, byte-identical to the reviewer's own original `.remedy-wt/f033-r1-block.md`, which existed before this worker did — so the reading covers delivery and not merely the worker's self-consistency, the distinction R-0705 exists to force — and `89ed735a:.agent/authored/f033-r1.md` and `89ed735a:.agent/last_block.md` are ONE blob id `f3776f61…d9619`. THE RECORD APPEND at `e158c8b0` was proved by TWO independent readers as §3 item 36 requires, because a byte reader and a structural reader fail differently: (a) 1422879 bytes plus one newline plus an 8979-byte slice equals 1431859, the committed blob exactly, with the base blob a byte PREFIX and the file ending in exactly one newline; and (b) N was COUNTED at 3 rather than asserted, and the LAST THREE blank-line units of the file equal the slice's three paragraphs IN ORDER. The NEGATIVE CONTROL was placed inside the FIRST appended paragraph — offset 1422890, the paragraph spanning 1422880 to 1427398 — and BOTH readers rejected it, which is the placement item 36 requires and the one a tail-only reader cannot see. THE LEDGER at that commit: registered 298 to 299 all DISTINCT, `Done:` 44 lines over 42 distinct ids UNMOVED, `Landed:` 11 UNMOVED, `Gate:` 117 to 118, the open set 256 to 257 — exactly the one id this round registers — with `^- R-0738 — ` reading 0 at the base and 1 after, and `^Gate: F257 R12 — ` reading 1. THE CLAIM at `c843211d`: the pair is a REWRITE by a mechanical containment test printing `TO contains FROM: false`, the FROM occurring once at the base and zero times after, the TO once after, and the committed blob equal to the base blob with ONLY that one pair applied; `- [~] F\d{3} —` reads 1 and `- [x] F\d{3} — ` reads 62, unmoved. THE PROSE FILES are byte-equal to their slices — `.agent/plan.md` at 1943 bytes over 39 lines, under the 50-line cap, and `.agent/context.md` at 3215 bytes — and the context file carries all five tokens the four state readers require, `## Active Branch`, a `feature/` slug, a roadmap feature id, `Steps` and `pytest`. THE STRUCTURE: seven SINGLE-PARENT commits of 385, 364, 27, 6, 1, 22 and 398 insertions, every one under 500; the range's path set equals the declared change set in BOTH directions, with nothing touched that the block did not name and nothing named that it did not touch; the `<<<SLICE `/`<<<END ` residue is 0 and 0 in the plan, the context and the STATUS file against a 9/11 control in the saved block; and `git ls-files .remedy-wt` reads 0. THE SEVEN SUITES were re-run by the reviewer SERIALLY in the primary checkout, one pytest process at a time: `tests/docs/` 295 passed, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 497, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 and the canary `tests/cli/test_golden_path.py` 42, every REAL exit 0 and every count identical to the reading taken at `1209dfb9` before the round began — so the round introduced no regression. THE PARKED BRANCH WAS NOT DISTURBED: `git rev-parse feature/f033-hunk-approval` still reads `ed040812`, and the worker reached it only through `git show`, which is the single contact DECISION F033 D1 permits. THE WORKER CAUGHT TWO ERRORS IN THE REVIEWER'S OWN TEXT AND DECLARED THEM INSTEAD OF SILENTLY APPLYING THEM, which is the required behaviour and is recorded as two dated lines in `.agent/prose_slips.md` this round under amend0827 rule 2: neither damaged anything on disk, so neither spends an id and neither earns a correction round.
<<<END RECORDF033R2

<<<SLICE SLIPF033R2
2026-08-29 · F033 R1 · DECISION F033 D1 states that F256 moved `apps/ui/src/components/diff/DiffView.tsx` by "192 added lines" and `apps/ui/src/components/diff/DiffFileSidebar.tsx` by 45, but 192 and 45 are the `--stat` CHANGED-line totals; the added columns measured by `git diff --numstat 32cde54e..bd8d9529` are 172 and 27, the CSS figure of 63 is right, and the ruling's substance — that F256 rewrote F033's own surface and the parked inventory is stale on it — is untouched by the correction.

2026-08-29 · F033 R1 · The block's G6 called its list "the four state readers' full contract" while enumerating five tokens, which reads as a miscount although four READERS holding five TOKENS is consistent; the carried constraint inside `.agent/context.md` separately lists only four tokens for that file, omitting the `pytest`-or-`resource` token `tests/regression/test_resource_safety.py` asserts, and the next context rewrite should add it.
<<<END SLIPF033R2

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and before C5, absent
  both times. `git status --porcelain` empty after EVERY commit.
  `git branch --show-current` reads `feature/f033-hunk-approval-v2` throughout.
  No force-push, no history rewrite, no branch deletion;
  `git rev-parse feature/f033-hunk-approval` still reads `ed040812` at C5.
- **G2 TRANSPORT.** Report sha256 and byte length of the committed blob
  `<C0a>:.agent/authored/f033-r2.md` and of `.remedy-wt/f033-r2-block.md`, and
  whether they are EQUAL; no expected digest is stated here because a block
  cannot carry its own. Then `git rev-parse <C0b>:.agent/authored/f033-r2.md` and
  `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE TWO APPENDS.** For `.agent/live_review.md` at C2, two readers:
  (a) the BASE blob, which must be 1431859 bytes, plus one newline, plus the
  RECORDF033R2 slice equals the C2 blob byte for byte, the BASE blob a byte
  PREFIX, the result ending in exactly one newline; (b) let N be the paragraph
  count your script COUNTS in the slice — report it — and compare the LAST N
  blank-line units against the slice's paragraphs IN ORDER. NEGATIVE CONTROL at
  an offset your script PROVES lies inside the FIRST appended paragraph; BOTH
  readers must reject it. For `.agent/prose_slips.md` at C3, a byte check only:
  the BASE blob, which must be 17728 bytes, plus one newline plus SLIPF033R2
  equals the C3 blob. Then confirm the C3 file carries ZERO lines beginning
  `- R-`, which is what keeps it a slip record and not a second ledger, and that
  the two added lines each match `^2026-\d\d-\d\d · F033 R1 · `.
- **G4 THE LEDGER at C2.** At BASE and at C2 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`, and
  `^Gate: F\d+ R\d+ — `, and report the open set at both. This round registers no
  id and resolves none: registered must stay 299, `Done:` 44 over 42, `Landed:`
  11 and the open set 257, all UNMOVED, with `Gate:` alone moving 118 to 119.
  `^Gate: F033 R1 — ` at C2 must read exactly 1.
- **G5 THE MODULE AGAINST THE SPEC.** Report, each as a measurement:
  `python3 -m ruff check packages/orchestration/hunk_identity.py tests/orchestration/test_hunk_identity.py`
  exits 0 with its real output; the module's exported names are exactly
  `HUNK_ID_LENGTH`, `normalise_old_side` and `hunk_identity`; `HUNK_ID_LENGTH`
  is 16; the module's source contains NO occurrence of the builtin call `hash(`
  and no `import os`, `import subprocess`, `import logging` or `open(`; and
  `hunk_identity("a.py", ["x"])` returns a 16-character lowercase hex string —
  print it. Take these readings at C4, before C5.
- **G6 THE TESTS.** `python3 -m pytest -q tests/orchestration/test_hunk_identity.py`
  must exit 0; report the count. Then the canary
  `python3 -m pytest -q tests/cli/test_golden_path.py` must exit 0 at 42 passed.
  Run them SERIALLY, one pytest process at a time, in the PRIMARY checkout.
- **G7 THE MUTATION RED-PROOFS.** In a DISPOSABLE `git worktree` at C4 — never in
  the primary checkout, which must satisfy `git status --porcelain` empty
  throughout — and with `python3 -B` so no stale bytecode is read. FIRST run the
  UNMUTATED control, `python3 -B -m pytest -q tests/orchestration/test_hunk_identity.py`,
  and report its REAL exit code and count: a colour with no baseline is not
  evidence. Then, one at a time, each reverted before the next:
  (M1) remove `path` from the digest input — the different-path test must FAIL;
  (M2) remove `occurrence` from the digest input — the identical-hunks test must
  FAIL; (M3) make `normalise_old_side` return its lines joined with no trailing
  strip — the trailing-whitespace test must FAIL. For each, report the REAL exit
  code, the failed count and the NAME of the failing test. If a mutation comes
  back GREEN, say so plainly and do not adjust the test to make it red — a green
  mutation is a finding about reachability and the reviewer owns it. Remove the
  worktree BY EXACT PATH and run `git worktree prune` when finished.
- **G8 STRUCTURE.** Walk `git rev-list --reverse BASE..C4` mechanically: each
  commit exactly ONE parent, each under 500 INSERTIONS — the `+` column of
  `git diff --numstat`, never insertions plus deletions — and report the
  per-commit list. C5's own numbers are NOT ordered here; the reviewer measures
  C5 at the next gate. Report the range's path set against the change set above
  in BOTH directions. Count `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
  `packages/orchestration/hunk_identity.py` and
  `tests/orchestration/test_hunk_identity.py`: each must read 0, against
  `.agent/authored/f033-r2.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the SESSION
number (1), the round (2), BASE, the changed-files table with real `+/-` from
`git diff --numstat`, one line per gate with real numbers, the item-status table
with every ordered item present exactly once, and your deviations. Include the
FULL TEXT of `packages/orchestration/hunk_identity.py`'s two public signatures
and the list of test names you shipped, so the reviewer can read the shape
without reconstructing it. No length cap. Write no verdict on your own work.
