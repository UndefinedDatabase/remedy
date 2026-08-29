# F033 — Hunk-level diff approval · ROUND 5 · CLOSING T001

SESSION 2 of feature F033. Round 5, rounds so far 5.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R5`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. PRODUCTION TEXT IS A SPEC, NOT A SLICE. The comment repairs in §SPEC are
   written by you from the description. The FACTS each comment must state, and
   the false claims it must no longer state, are binding; wording and line
   wrapping are yours. If the SPEC is impossible, STOP and say so.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Invoke `npx` through Python's
   `subprocess.run`, never through `npm run`. Python 3.10 forbids a backslash
   inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>` into memory or into a
   scratch file under `.remedy-wt/`. NEVER write a base blob over a tracked file.

## Base

BASE is `7434f54632e75e9d1e86044d8edc7f96c0ef0ae6`, the round 4 handback commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 4 passed every gate; the reviewer re-ran all eight itself and every reading
reproduced. Its verdict is in the record slice below.

Two things it surfaced are this round's work.

FIRST, round 4's deviation 3 reported a stale comment in
`apps/ui/src/api/diffViewModel.ts` and correctly did not repair it, because that
block's SPEC forbade touching anything outside two functions. The reviewer then
swept the rest of the seam and found the same class in a SECOND production file:
`packages/orchestration/hunk_identity.py`. Both still describe the world as it
was BEFORE round 3 wired the parser. Registered below as R-0739.

SECOND, and larger: T001's last item does not exist. Both
`docs/roadmap/features/T5_F033.md` and `.agent/plan.md` order the "v1-local hunk
lib" in the diff-repair side to retire onto `hunk_identity`. Measured at
`7434f546`, `packages/orchestration/diff_repair.py` contains no hunk identity, no
id field, no digest and no import of `hunk_identity`: its `RepairHunk` is
`(path, start_line, end_line, text)` — a span of CURRENT source selected for a
repair prompt, which has no old side to hash. `review_scope.parse_diff_line_ranges`
turns hunk headers into line ranges and names nothing;
`source_apply._hash_content` digests a whole FILE for an apply proof, not a hunk.
The only importer of `hunk_identity` in the repository is `diff_parser.py`.
There is no second hunk identity to consolidate, so the clause is discharged as
VACUOUS rather than performed. DECISION F033 D3, in the record slice, rules it
and the feature file records it as amendment A1.

With R-0739 repaired and D3 recorded, T001 is COMPLETE and T002 opens.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 4 verdict, R-0739 and DECISION F033 D3 into `.agent/live_review.md`
- C3 the staleness repair, both production files together
- C4 the feature-file amendment
- C5 the `Landed: R-0739` line
- C6 the handback

## Change set — these paths and nothing else

    .agent/authored/f033-r5.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/hunk_identity.py
    apps/ui/src/api/diffViewModel.ts
    docs/roadmap/features/T5_F033.md
    .agent/handoff.md

This round does NOT touch `packages/orchestration/diff_parser.py`,
`packages/orchestration/diff_repair.py`, `apps/ui/src/api/diffViewModel.test.ts`,
or `docs/roadmap/STATUS.md`. No behaviour changes anywhere: C3 edits COMMENT text
only, and not one executable line.

## SPEC — the staleness repair at C3

Both files below carry sentences that were true when written and were falsified
by round 3, which wired `diff_parser.py` to `hunk_identity` and bumped
`DIFF_VIEW_VERSION` to 2. Repair the FACTS; keep each comment's voice, its
reading order and its surrounding structure. Change no executable line.

### 1. `packages/orchestration/hunk_identity.py` — the module docstring

Three claims in the opening paragraphs are false at `7434f546`:

- that `diff_parser.py` "currently names hunks" positionally. It does not: at
  `7434f546` that module imports `hunk_identity` and calls it for every hunk's
  `id`.
- that this module "IS the module `diff_parser.py`'s docstring points at when it
  says its hunk `id` values are PROVISIONAL". `diff_parser.py`'s docstring no
  longer says that; at `7434f546` it says hunk `id` values "are CONTENT-DERIVED
  and carry no position at all".
- that "The parser is not wired to this module yet — that wiring and the version
  bump are their own change". Both landed in round 3.

Rewrite those paragraphs so they state, in the present tense, that
`diff_parser.py` calls this module for every hunk id and that `DIFF_VIEW_VERSION`
is 2. KEEP the reason the module exists — positional ids move when a file is
edited above them, and an operator's approval must survive that — as the WHY,
stated as the motivation it is rather than as a description of current
behaviour. KEEP the DELIBERATE ABSENCE paragraph, the totality paragraph and
every sentence about purity, and keep the pointers to `diff_parser.py` and
`diff_repair.py` that tell a searching reader where to go.

The sentence "The diff-repair side will share this same function rather than
keep a local hunk helper" is the one DECISION F033 D3 retires. Replace it with
the measured fact: the diff-repair side holds no hunk identity to share —
`RepairHunk` selects spans of current source and never names a hunk — so this
module has ONE caller by design, and a reader who expected a second one should
read amendment A1 of `docs/roadmap/features/T5_F033.md`.

### 2. `apps/ui/src/api/diffViewModel.ts` — the `buildDiffRowModels` KEYS note

Its KEYS paragraph says the hunk-derived keys are built from an id
`diff_parser.py` assigns as `"<fileIndex>:<hunkIndex>"`, "both zero-based and
unique within one parse", and that "Those ids are PROVISIONAL: F033 replaces them
with content-hash ids". Round 3 did that replacing.

State instead that the server's hunk `id` is content-derived, and KEEP the
sentence that already carries the load here: nothing in this function depends on
the id's SHAPE, only on the server assigning distinct ones. Note that the client
supplies its own id when a payload carries none, and that
`UNIDENTIFIED_HUNK_ID_PREFIX` is what keeps such an id out of the server's id
space. Change nothing else in the file — the constant, the fallback expression
and `readDiffHunk`'s contract note are round 4's work and are correct.

CONSTRAINT, and it is a real guard rather than a caution:
`tests/ui_contracts/test_diff_view_model.py` counts the collapse threshold
literal over the RAW text of `diffViewModel.ts` and its test file, comments
INCLUDED, and requires exactly one occurrence. Do not write that number in any
comment you touch. The same file's other guards read comment-STRIPPED source, so
a comment-only edit is invisible to them.

## SPEC — the T002 inventory at C6

The handback carries a section headed `## T002 seam inventory`. It is a READING,
not a design: report what you found, and propose nothing. Cover, each with a
`path:line` that resolves at your own HEAD:

- where the write door dispatches a command in `packages/orchestration/ui_server.py`
  — the constants naming the two commands it dispatches today, and the line that
  answers an exposed-but-undispatched command.
- how a command becomes UI-exposed: the set `ui_server.py` imports from
  `apps/cli/command_catalog.py`, and where that set is declared.
- `TestCommandDoorImportGuard` in `tests/ui_server/test_command_channel.py`:
  quote what it pins, because it is an equality guard over the write door's
  imports and T002 will need to widen it.
- the public entry point of `packages/orchestration/source_apply.py` that lands a
  patch, its signature, and whether it already takes a SUBSET of anything.
- whether any module today reads an approved/rejected hunk set — say "none found"
  and give the search you ran if that is the answer.

## The slices

<<<SLICE PLANF033R5
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
| restart, claim, register R-0738 | done | round 1, DECISION F033 D1 |
| the shared identity function and its tests | done | round 2, 10 tests |
| wire the parser, bump DIFF_VIEW_VERSION to 2 | done | round 3, 50 tests |
| rule the client's invented id | done | round 4, DECISION F033 D2 |
| repair the two stale production comments | done | this round, R-0739 |
| retire the diff-repair local hunk helper | dropped | this round, DECISION F033 D3 — no such helper exists |
| T001 stable ids, viewer v2, consolidation | done | closed by this round |
| T002 approve_hunks, subset atomicity, ledger | open | next |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Open T002 on the seam this round's handback inventories: the validation core
   for `approve_hunks` — ids exist in that attempt's diff, approved and rejected
   are disjoint, a rejection carries a reason — as a pure function with tests,
   before any write door or applicator work.
2. Then the subset apply itself, all-or-nothing over the approved set, built on
   `packages/orchestration/source_apply.py`.
3. Then the write-door command and the hunk-decision ledger in evidence.

## Risks
- `packages/orchestration/repo_applicator.py` applies nothing by design, so the
  subset seam is new work rather than a parameter on something existing.
- The write door's import guard is an EQUALITY guard, so T002 widens it in the
  same commit that adds an import, or the branch tip ships red.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R5

<<<SLICE RECORDF033R5
Gate: F033 R4 — THE CLIENT SEAM. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `7434f546` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 19163 bytes at sha256 `f92ac6a1…18aff` and the C0b `.agent/last_block.md` blob is byte-identical to it. This workflow has no paste relay, so that chain proves the worker's own copies agree and makes no claim about the bytes the reviewer emitted. THE RECORD APPEND at `201823cf` reconstructs 1440101 plus one newline plus 6185 to 1446287, the committed blob exactly, with the base a byte PREFIX, N counted at 2 by the reviewer's own script, the last two blank-line units equal to the slice's paragraphs IN ORDER, and a byte flipped at offset 1440202 — proved by span arithmetic to lie inside the FIRST appended paragraph, which spans 1440102 to 1444310 — REJECTED by both readers. THE LEDGER is UNMOVED at 299 registered over 299 distinct, `Done:` 44 over 42, `Landed:` 11 and the open set 257, with `Gate:` alone moving 120 to 121 and `^Gate: F033 R3 — ` reading 0 at the base and exactly 1 after. THE PLAN slice landed byte-EQUAL at 1975 bytes over 40 lines, under the 50-line cap. THE CLIENT AGAINST THE SPEC: `UNIDENTIFIED_HUNK_ID_PREFIX` is exported at `unidentified:`, and the bare positional template reads 1 at the base and 0 after under BOTH readings the gate's wording admits — with backticks and as the bare substring — which is the reading the worker's deviation 1 chose the spelling `file<i>:hunk<j>` to make unambiguous, correctly. `npx tsc --noEmit` in `apps/ui` exits 0. THE SUITES, re-run by the reviewer in the primary checkout with pytest SERIAL: vitest 95 passed at exit 0 against 93 at the base, `tests/ui_server/` 497, the canary `tests/cli/test_golden_path.py` 42, and `tests/ui_contracts/` 664 passed with 4 skipped — that last one unordered but run because it reads both edited files as TEXT. THE MUTATION RED-PROOF WAS REPRODUCED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE at `76b6448b`, with the runner invoked from the primary checkout against `--config <primary>/apps/ui/vitest.config.ts` and `--root <worktree>/apps/ui`, scoped to the one test file: the UNMUTATED CONTROL is a real exit 0 at 95 passed, and restoring the bare positional fallback is exit 1 at 2 failed over 93 passed, reddening `marks a hunk with no usable id UNIDENTIFIED instead of inventing a server-shaped one` and `gives two id-less hunks in ONE file DISTINCT ids, so the collapse set still sees two` — the same two names the handback reports. The worktree was removed by exact path and pruned, and `git status --porcelain` in the primary checkout was empty before, during and after. THE STRUCTURE: five single-parent commits of 249, 155, 17, 4 and 107 insertions over the range ending at `76b6448b`, every one under 500, the path set matching the change set in BOTH directions with `.agent/handoff.md` the sole expected absence, delimiter residue 0 in every target against a non-zero control of 4 and 5 in the saved block, and `git ls-files .remedy-wt` reading 0. The handback commit `7434f546` itself is 270 insertions over one parent, which the block correctly declined to order of a commit that cannot measure itself. THE WORKER FOUND WHAT THE BLOCK COULD NOT: its deviation 3 reported a stale comment two functions away from its change set and correctly left it, because that block's SPEC §3 forbade the edit. That report is why R-0739 below exists and why the reviewer swept the rest of the seam, which turned up the same class in a second file the round never touched.

- R-0739 — Low, TWO PRODUCTION FILES STILL DESCRIBE THE WORLD ROUND 3 REPLACED, AND ONE OF THEM MISQUOTES A SIBLING MODULE'S DOCSTRING AS EVIDENCE FOR IT. Raised by the reviewer at the F033 R4 gate, from the worker's own deviation 3, and measured at `7434f546`. THE STATE ON DISK. `packages/orchestration/hunk_identity.py`'s module docstring says `diff_parser.py` "currently names hunks" positionally, that this module "IS the module `diff_parser.py`'s docstring points at when it says its hunk `id` values are PROVISIONAL", and that "The parser is not wired to this module yet — that wiring and the version bump are their own change". `apps/ui/src/api/diffViewModel.ts`'s `buildDiffRowModels` KEYS paragraph says the keys derive from an id `diff_parser.py` assigns as `"<fileIndex>:<hunkIndex>"` and that "Those ids are PROVISIONAL: F033 replaces them with content-hash ids". Round 3 wired the parser and bumped `DIFF_VIEW_VERSION` to 2, so every one of those sentences is false, and the second cross-module claim is false in a way a reader cannot catch locally: `diff_parser.py`'s docstring at `7434f546` says hunk `id` values "are CONTENT-DERIVED and carry no position at all", which is the opposite of what it is cited as saying. WHY LOW AND NOT LOWER: no behaviour is wrong and no test can see this, so it costs nothing today; but `hunk_identity.py` is the module a reader arrives at to learn what a hunk id IS, and it currently tells them the parser does not use it — which invites re-doing round 3. The same class was resolved twice already on adjacent code, at R-0727 and R-0730, so the sweep is the thing that keeps failing rather than any one comment. WHY IT SURVIVED ROUND 3: that round's own ledger entry records that it "corrected two neighbouring comments that still asserted the positional fact"; the sweep reached the comments beside the code it changed and not the module whose whole purpose the change completed, nor the client. A staleness sweep is scoped to the CLAIM, never to the diff. FIX: repair both, stating the wiring in the present tense and keeping each comment's WHY intact; the retired sentence about a shared diff-repair helper is DECISION F033 D3's, not this finding's. BINDING ON THE NEXT BLOCK THAT LANDS A SEAM CHANGE: name, in the block, the files whose COMMENTS assert the fact the change falsifies, and grep for the claim rather than reading the diff.

DECISION F033 D3 — T001'S "SHARED-HELPER CONSOLIDATION WITH DIFF-REPAIR" IS DISCHARGED AS VACUOUS, BECAUSE THERE IS NO SECOND HUNK IDENTITY IN THIS REPOSITORY. THE SITUATION. `docs/roadmap/features/T5_F033.md` gives T001 "the shared-helper consolidation with diff-repair (its tests stay green)" and its How-it-fits paragraph promises "the v1-local hunk lib retires — one hunk identity across repair and approval". THE MEASUREMENT, taken by the reviewer at `7434f546` by reading each module in full, not by grep alone: `packages/orchestration/diff_repair.py` holds no id field, no digest, no hashing and no import of `hunk_identity`; its `RepairHunk` is `(path, start_line, end_line, text)`, a span of CURRENT source lines selected for a repair prompt, which has no old side and therefore nothing `hunk_identity` could be called on. `review_scope.parse_diff_line_ranges` turns hunk headers into line ranges and names no hunk. `source_apply._hash_content` digests a whole FILE for an apply proof. The only importer of `hunk_identity` anywhere under `packages/`, `apps/` or `tests/` is `diff_parser.py`. CHOSEN: record the clause as discharged-vacuous, close T001 on its three real deliverables — the content-derived identity with its property tests, the parser wiring with `DIFF_VIEW_VERSION` 2, and the client seam — and amend the feature file so the next reader is not sent looking for a module that never existed. ALTERNATIVE 1, give `RepairHunk` a `hunk_identity`-derived id anyway, REJECTED: that is new scope wearing a consolidation's clothes, it would require synthesising an old side the repair path does not have, and F033's Do-not-touch list names applicator internals. ALTERNATIVE 2, leave the clause open and let T001 stay unclosable, REJECTED: an item no round can perform blocks the feature's own completion test forever, and the feature file would keep asserting a module that is not there. WHY THIS IS THE REVIEWER'S CALL AND NOT A QUESTION: docs/agents/planner_reviewer_prompt.md §4 item 7 routes a wrong spec to planning as a loud, persisted, reversible DECISION carried in the block, never as a question to the operator. HOW TO REVERSE: delete amendment A1 from `docs/roadmap/features/T5_F033.md` and restore the T001 clause; nothing in code depends on this decision, because its whole content is that no code was ever there.
<<<END RECORDF033R5

<<<SLICE FEATUREF033A1

## Amendments

**A1 (DECISION F033 D3) — T001's diff-repair consolidation is discharged as
vacuous.** The Task-slicing line for T001 and the How-it-fits paragraph both
promise that a "v1-local hunk lib" on the diff-repair side retires onto the
shared identity. No such library exists. Measured while closing T001:
`packages/orchestration/diff_repair.py` holds no hunk id, no digest and no
import of `packages/orchestration/hunk_identity.py`; its `RepairHunk` is a span
of current source lines selected for a repair prompt, with no old side to hash.
`review_scope.parse_diff_line_ranges` yields line ranges and names no hunk, and
`source_apply` digests whole files for apply proofs. `diff_parser.py` is the
only caller of the shared identity, and one caller is the design.

T001 is therefore complete on its three real deliverables — the stable
content-derived identity with its stability property tests, the parser wiring
with the `DIFF_VIEW_VERSION` bump to 2, and the client seam that stops the
viewer inventing a server-shaped id. Acceptance's "Diff-repair's suite green on
the shared helper" is read as "diff-repair's suite stays green", which it does,
untouched.

Reverse this amendment by deleting this section; the T001 clause above is
unchanged and would then read as originally written.
<<<END FEATUREF033A1

## The `Landed:` line at C5 — you write it, not a slice

`docs/agents/planner_reviewer_prompt.md` §4 item 4 reserves `Done:` for
reviewer-authored text and gives the WORKER the `Landed:` line, so this one is
not a slice and must not be extracted from the block. Append to
`.agent/live_review.md`, after one newline, exactly ONE line matching
`^Landed: R-0739 — ` and ending in a newline. It states what changed and names
the REAL SHA of C3 — a value that does not exist while this block is being
written, which is why the line is yours. Nothing else goes in that commit.

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C5, so the handback at C6 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C6,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r5.md` and of `.remedy-wt/f033-r5-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r5.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPENDS.** (a) At C2: the BASE blob of `.agent/live_review.md`,
  which must be 1446287 bytes, plus one newline plus RECORDF033R5 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R5 — report it
  — and compare the LAST N blank-line units of the C2 blob against the slice's
  paragraphs IN ORDER. NEGATIVE CONTROL at an offset your script PROVES lies
  inside the FIRST appended paragraph; BOTH readers must reject it. (c) At C5:
  the C2 blob plus one newline plus LANDEDF033R5 equals the C5 blob byte for
  byte, where that line is the one you wrote per the section above; that
  commit's diff must ADD exactly one line, and it must match `^Landed: R-0739 — `.
- **G4 THE LEDGER at C5.** At BASE and at C5 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`, and
  `^Gate: F\d+ R\d+ — `; report the open set at both. Ordered: registered 299 to
  300 with the ADDED id exactly `R-0739`, `Done:` 44 over 42 UNMOVED, `Landed:`
  11 to 12, `Gate:` 121 to 122, and the open set 257 to 258. `^Gate: F033 R4 — `
  at C5 must read exactly 1, and every registered id must still be DISTINCT.
- **G5 THE STALENESS REPAIR at C3.** Each as a measurement, over the RAW text of
  both files, at BASE via `git show <BASE>:<path>` and at C3. Report both
  numbers for every string, because the BASE count is what proves the gate is not
  vacuous. In `packages/orchestration/hunk_identity.py`: `currently names hunks`,
  `The parser is not wired to`, `values are PROVISIONAL` and
  `will share this same function` must each read at least 1 at BASE and exactly 0
  at C3. Each of those is a SINGLE-LINE substring of the file as it stands at
  BASE — the reviewer measured all four rather than reading them off the page,
  because the sentence they come from wraps and a needle spanning the wrap would
  forbid nothing. In `apps/ui/src/api/diffViewModel.ts`: `Those ids are PROVISIONAL` and
  `<fileIndex>:<hunkIndex>` must each read at least 1 at BASE and exactly 0 at
  C3. Still at C3, these must SURVIVE: `Nothing here depends on the id's SHAPE`
  exactly 1 in the client, and `DELIBERATE ABSENCE` exactly 1 in
  `hunk_identity.py`. Finally `git diff <BASE> <C3>` must show ZERO changed lines
  that are not inside a comment or docstring — report how you determined that,
  and report the `+`/`-` counts per file.
- **G6 THE SUITES.** Serially, one pytest process at a time, each a REAL exit 0,
  with the count: `tests/orchestration/test_hunk_identity.py` (10 at BASE),
  `tests/orchestration/test_diff_parser.py` (50 at BASE), `tests/ui_contracts/`
  (664 passed and 4 skipped at BASE), `tests/docs/` (295 at BASE) — ordered
  because this round changes a `docs/roadmap/**` path — and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then, through Python from
  `apps/ui`: `npx tsc --noEmit` exit 0, and
  `npx vitest run --reporter=basic src/api/diffViewModel.test.ts` exit 0 at 95.
  NO MUTATION RED-PROOF IS ORDERED THIS ROUND, deliberately: C3 changes comment
  text only, so no mutated branch is reachable by any test and a colour ordered
  here could only be green. Say so in the handback rather than inventing one.
- **G7 THE FEATURE-FILE APPEND at C4.** The BASE blob of
  `docs/roadmap/features/T5_F033.md`, which must be 5057 bytes, plus
  FEATUREF033A1 equals the C4 blob byte for byte — note the slice OPENS with a
  blank line, so no separator is added. BASE a byte PREFIX; result ending in
  exactly one newline; the lines that commit's diff ADDS are exactly the slice's
  lines IN ORDER. Report `^## Amendments$` at C4 as exactly 1.
- **G8 STRUCTURE.** Walk `git rev-list --reverse BASE..C5`: each commit exactly
  ONE parent, each under 500 INSERTIONS — the `+` column of `git diff --numstat`,
  never insertions plus deletions — and report the per-commit list. C6's own
  numbers are NOT ordered here; the reviewer measures C6 at the next gate. Report
  the range's path set against the change set in BOTH directions. Count
  `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
  `docs/roadmap/features/T5_F033.md`, `packages/orchestration/hunk_identity.py`
  and `apps/ui/src/api/diffViewModel.ts`: each 0, against
  `.agent/authored/f033-r5.md` as a non-zero control whose count you report. `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 2,
round 5, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts — one line
per gate with real numbers, the `## T002 seam inventory` section, the
item-status table with every ordered item exactly once, and your deviations.
Quote the repaired comment regions in full so the reviewer can read them without
the diff. No length cap. Write no verdict on your own work.
