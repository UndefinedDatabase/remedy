── STEP T002b-i — F109 Semantic dedupe, ROUND 6, SESSION 2 ────────────

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Base commit: 552bbd05ca3d458ef966b4d87157f62e917d444a. Branch:
feature/f109-semantic-dedupe. Do not create a branch, do not switch
branch, do not create a PR, do not merge anything.

Goal:
  Book round 5's PASS verdict into the record, then land the FIRST HALF of
  T002b: the pure composition transform `_dedupe_resumed_segments` in
  `packages/orchestration/pingpong_loop.py`. It rewrites an already-sent
  segment's TEXT to its marker while leaving that segment's NAME, RANK and
  POSITION alone, and reports which names it replaced. NO CALL SITE IS
  ADDED. `compose_builder_prompt` and `compose_reviewer_prompt` are NOT
  touched, so every prompt this repository composes stays byte-identical
  to the base commit's.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f109-r6.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   rewrite `.agent/plan.md` from SLICE PLAN
  C2   append SLICE RECORD to `.agent/live_review.md`
  C3   add the transform to `packages/orchestration/pingpong_loop.py`
  C4   add the cases of SPEC H to `tests/orchestration/test_semantic_dedupe.py`
  C5   rewrite `.agent/handoff.md`

Change set — these paths and no others:
  .agent/authored/f109-r6.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  packages/orchestration/pingpong_loop.py
  tests/orchestration/test_semantic_dedupe.py
  .agent/handoff.md

Constraints:
  1. SLICE PLAN and SLICE RECORD are applied BYTE FOR BYTE. Do not edit,
     rewrap, retype or improve them. C0a and C0b are `cp`, never a retype.
  2. C2 is an APPEND to `.agent/live_review.md`. The file ends WITHOUT a
     trailing newline at the base commit; keep it that way. Nothing already
     in that file is edited, renumbered or deleted — in particular the
     `Landed: R-0770` line and the earlier `R-0770` paragraph both STAY.
  3. C1 lands BEFORE C2, and C2 before C3.
  4. In `pingpong_loop.py` the new function goes AFTER the end of
     `_drop_one_newline_per_segment_boundary` and BEFORE the comment block
     beginning `# F105 T003 migration site 5.` that belongs to
     `compose_builder_prompt`. Nothing else in that file is edited,
     reordered or deleted, with ONE named exception: the four import
     statements listed in SPEC G may be EXTENDED with the names SPEC G
     requires. No existing function body changes.
  5. NO CALL SITE. Nothing in `pingpong_loop.py` calls
     `_dedupe_resumed_segments` at the end of this round. Gate G6 measures
     that directly, and it is the property that keeps every prompt golden
     green without this round having to run them all.
  6. In the test file, nothing already present is edited, reordered or
     deleted; the existing `from packages.orchestration.pingpong_loop
     import ...` statement may be EXTENDED. New cases go at the END of the
     file, after the last existing class. Reuse the existing helpers
     `_real_manifest_rows` and `SegmentStabilityRank`; do not redefine them.
  7. Do NOT gate on `npm run lint` and do NOT gate on `ruff`. Follow ruff
     by construction instead: keep every new line under 120 characters and
     keep each extended import list in the repo's `order-by-type` isort
     order — CONSTANTS first, then classes, then functions, alphabetical
     within each group.
  8. Every pytest process uses `python3 -B`, and `__pycache__` is purged
     before every run of G5. G5's mutations run ONLY inside a disposable
     worktree, added and removed BY EXACT PATH, never in the primary
     checkout.
  9. EVERY gate below — G1, G2, G3, G4, G5, G6 and G7 — runs at C4 or
     earlier, so every reading the handback quotes already exists when C5
     writes it. C5's own insertion count is NOT quoted anywhere in C5; the
     reviewer measures that one.

SPEC G — the transform (C3). Write this as production code; it is
described here, not sliced, so write it in the file's own idiom.

  Name: `_dedupe_resumed_segments`. Private: it is the composition hook's
  decision step and the two compose functions are its only future callers.

  Signature, keyword-only after the third positional:

    def _dedupe_resumed_segments(
        segments: Sequence[PromptSegment],
        sent_hashes: Container[str],
        *,
        enabled: bool = True,
        min_chars: int = DEDUPE_MIN_SEGMENT_CHARS,
    ) -> tuple[tuple[PromptSegment, ...], tuple[str, ...]]:

  Returns TWO things: the segments to compose, and the names that were
  replaced, in the order they were replaced. The second element exists so
  T002c can record what the model did NOT receive again WITHOUT re-deciding
  it — a second decision site is a second thing that can disagree.

  Behaviour, exactly:
  - When `enabled` is false, return `(tuple(segments), ())` immediately and
    consult nothing else. The kill switch stays total, matching
    `should_dedupe_segment`'s own first-and-alone rule.
  - Otherwise, for each segment IN THE ORDER GIVEN, obtain that segment's
    sha256 FROM THE SHIPPED PRODUCER — `compose_prompt_segments((segment,))`
    and read `.manifest[0].sha256`. DO NOT recompute a hash with `hashlib`
    here. The index remembers manifest hashes, so the decision must ask the
    same producer that made them; a second hashing expression in this file
    is a drift the feature would fail silently and safely, which is the
    worst way for it to fail. Composing one segment at a time is also what
    makes this correct for a duplicate segment NAME, which a name-keyed
    lookup over a whole manifest would collapse.
  - Call `should_dedupe_segment(segment.text, that_sha256, sent_hashes,
    enabled=True, min_chars=min_chars)`. `enabled` is already handled above,
    so pass True here rather than threading the flag twice.
  - When it answers True, append `dataclasses.replace(segment,
    text=dedupe_marker_for_segment(segment.name))` to the result and append
    `segment.name` to the replaced names. When it answers False, append the
    segment UNCHANGED — the same object, not a copy.
  - RETURN ORDER IS INPUT ORDER. Do not sort by rank. `compose_prompt_segments`
    does its own (rank, registration index) sort afterwards, so re-ordering
    here would change the tie-break between equal ranks and move segments
    the cache discipline requires to stay put.

  Docstring: say that this is F109 T002b's decision step; that names and
  ranks survive by construction so composition order and the cacheable
  prefix are untouched; that the sha256 comes from the shipped producer for
  the drift reason above; and — as a deliberate absence a reader should
  find here rather than conclude was forgotten — that NO CALLER EXISTS YET,
  that wiring it into `compose_builder_prompt` and `compose_reviewer_prompt`
  behind a bypass-by-default parameter is the next slice of T002b, and that
  the `enabled` flag's config plumbing is T002c.

  Imports to EXTEND (constraint 4's named exception), each keeping isort
  order-by-type:
  - `from collections.abc import Callable` gains `Container` and `Sequence`.
  - `from dataclasses import dataclass, field` gains `replace`.
  - the `from packages.orchestration.prompt_segments import (...)` block
    gains `PromptSegment`.
  - the `from packages.orchestration.session_sent_index import (...)` block
    gains `DEDUPE_MIN_SEGMENT_CHARS`, `dedupe_marker_for_segment` and
    `should_dedupe_segment`.

SPEC H — the cases (C4). One new class at the end of the file, plus the
import extension. Every case is PURE: no tmp_path, no provider, no loop.
Build segments through `PromptSegmentRegistry` and
`registry.registered_segments()`, never by constructing `PromptSegment`
literals, so the cases run against the shape that actually ships.

  Use a long text of at least `DEDUPE_MIN_SEGMENT_CHARS` characters and a
  short one below it. These cases are MANDATORY and each is its own named
  test:
  1. A long, already-sent segment has its TEXT replaced by exactly
     `dedupe_marker_for_segment(<that name>)`.
  2. THE SAME CASE asserts the segment's NAME and RANK are unchanged.
  3. The returned names tuple holds exactly the names that were replaced,
     in order.
  4. ORDER: the returned segments' names equal the input segments' names,
     in the same order, over a set of at least three segments whose ranks
     are NOT in registration order — so a rank sort would visibly fail it.
  5. The kill switch: `enabled=False` returns the segments unchanged and an
     EMPTY names tuple, though every other condition holds. Name this case
     so it cannot rot; it is the only assertion that says disabling is total.
  6. An empty `sent_hashes` replaces nothing.
  7. A long segment whose hash was never sent is not replaced.
  8. A short already-sent segment is not replaced, and the case asserts the
     hash IS in the sent set first, so the refusal is demonstrably about
     LENGTH and not about a missing hash.
  9. `min_chars` override: a segment the default refuses is replaced under a
     smaller `min_chars`, both asserted in the same case.
  10. THE ANTI-DRIFT PIN, end to end and the most important case here: build
      the segments, take the manifest rows through `_real_manifest_rows`,
      record them into a real `SessionSentIndex` with `record_call(...,
      ok=True)`, read the set back with `sent_hashes(...)`, and assert the
      transform replaces exactly the long segment and leaves the short one.
      This is what pins the transform's hash source to the index's, so a
      change to either that broke dedupe could not land green.
  11. The input is not mutated: after the call, the original segments'
      texts are still their original texts.
  12. Composition AFTER the transform: compose the returned segments and
      assert the composed text CONTAINS the marker, does NOT contain the
      long segment's original text, and still contains the short segment's
      text verbatim.

SLICE PLAN — the WHOLE of `.agent/plan.md`, byte for byte:
<<<SLICE PLAN
# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 6, session 2 — book round 5's PASS verdict, then land the first
half of T002b: the pure composition transform `_dedupe_resumed_segments`
in `packages/orchestration/pingpong_loop.py`, which rewrites an
already-sent segment's TEXT to its marker while leaving that segment's
NAME, RANK and POSITION alone, and reports which names it replaced. No
call site is added: `compose_builder_prompt` and `compose_reviewer_prompt`
are not touched, so every prompt this repository composes stays
byte-identical to the one before this round.

## Next Steps

- Wire the transform into `compose_builder_prompt` and
  `compose_reviewer_prompt` behind a parameter that defaults to no dedupe,
  and pass the session's sent hashes at the two loop call sites only when
  a resume ref is actually set. The non-resume byte-equality golden is
  that round's first acceptance item.
- Record the deduped segments in the manifest so evidence shows what the
  model did NOT receive again, and plumb the config kill switch through
  to `enabled` (T002c).
- The measurement fixture and the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still NOT wired into
  the index. That records strictly less than was sent, which errs in the
  safe direction; the wiring step must not assume the index is complete.
- `tests/orchestration/test_builder_prompt_golden.py` pins frozen renders
  and an exact ten-name manifest tuple. This round adds no call site, so
  it cannot reach them; the wiring step must gate on that suite.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

SLICE RECORD — appended to `.agent/live_review.md`. It is ONE paragraph.
Append a blank line, then this text, and leave the file without a trailing
newline:
<<<SLICE RECORD
Gate: F109 R5 — the round 5 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ FROM THE HANDBACK, over the range `2f25302e5c1e30f2d847c80a80458220702b1f52..552bbd05ca3d458ef966b4d87157f62e917d444a`. TRANSPORT: `sha256sum .agent/authored/f109-r5.md .agent/last_block.md` printed one digest twice, `4d20295bb21fd4a0e41b938b4f40e884a1a64fc5ba4cb00bb9311e80ea9714ca`, equal to the digest the delegation wrapper stated — and THAT CHAIN COVERS THE SAVED COPY AND ITS MIRROR, both of which are the worker's own output, so it establishes self-consistency and says nothing about the bytes that were emitted; docs/agents/planner_reviewer_prompt.md §3 item 37 is the rule and this clause is its application rather than a claim beyond it. THE PRODUCTION CODE IS THE ROUND'S POINT AND IT IS SOUND: `should_dedupe_segment` consults `enabled` first and alone, returns False rather than raising on a malformed `text` or `sha256`, and compares `len(text) >= min_chars`, so the boundary is inclusive by decision and not by accident; `dedupe_marker_for_segment("dossier")` returns `[unchanged: dossier, previously provided]`, which the reviewer measured at 41 characters against the threshold of 200, so the constant's justification is arithmetic rather than assertion. THE MODULE STAYS PURE: `ast` over `packages/orchestration/session_sent_index.py` at `552bbd05ca3d458ef966b4d87157f62e917d444a` reports its only imports are `__future__` and `collections.abc`, so nothing from `prompt_segments` and no file, network or provider call reaches the decision. THE COLOUR IS THE REVIEWER'S OWN, run in a disposable worktree added at `552bbd05ca3d458ef966b4d87157f62e917d444a` by exact path and removed by exact path afterwards, with `packages.orchestration.session_sent_index.__file__` confirmed to resolve INSIDE that worktree before any mutation was trusted: the unmutated control is a real exit 0 at 79 passed; deleting the `enabled` guard is exit 1 at 1 failed and the single failure is `test_the_kill_switch_refuses_though_every_other_condition_holds`; turning `>=` into `>` is exit 1 at 2 failed including `test_a_segment_of_exactly_the_minimum_length_is_deduped`; deleting the membership check is exit 1 at 2 failed including `test_a_hash_the_session_never_received_is_not_deduped`. THE APPEND SHAPES WERE MEASURED, NOT READ: the C2 record append leaves the base bytes a byte-exact prefix and its last two blank-line units equal the slice's two paragraphs in order; the C4 test addition is 125 added lines against 0 removed, and a sequence comparison of the pre-commit against the post-commit blob yields only insertions — three single-name lines into the existing import list and one contiguous 122-line suffix — so no existing test was edited, reordered or deleted, which is exactly the worker's declared deviation 1 and nothing wider. THE SUITES ARE THE REVIEWER'S OWN, run serially, every one exit 0: 79, 34, 27, 515, 52, 21, 16 and 42. STRUCTURE: every commit in the range is single-parent, with insertions 344, 228, 17, 5, 72, 125 and 281 in that order, all under 500; the range's `git diff --numstat` lists the six ordered paths plus `.agent/handoff.md` and nothing else, and names no `packages/orchestration/pingpong_loop.py`, so T002's wiring is untouched as ordered; `git status --porcelain` is empty and the remote tip equals the local tip at `552bbd05ca3d458ef966b4d87157f62e917d444a`. THE ONE RULING THE ROUND ASKED FOR: the worker's deviation 2 offered to hoist `DEDUPE_MIN_SEGMENT_CHARS` to the top of the module, and the answer is NO — the constant stays beside the two functions that read it, because AGENTS.md's discoverability convention puts the one-line WHY comment directly above the definition a reader searches for, and hoisting would buy a layout convention at the cost of that placement. THE ROUND PASSES.
SLICE RECORD

Done when — the gates listed below. Run every one, record its REAL exit
code and output, and give each ONE line in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r6.md .agent/last_block.md`
     prints ONE digest twice, and it equals the digest the delegation
     wrapper states for this block. Report the digest. State that the chain
     compares the saved copy against its mirror and claims nothing about
     the emitted bytes.

  G2 THE PLAN. `cmp` `.agent/plan.md` against the SLICE PLAN text extracted
     mechanically from `.agent/authored/f109-r6.md` — no output, exit 0.
     `wc -l .agent/plan.md` is strictly under 50. `grep -c '^## Goal'` is 1
     and `grep -c '^## Next Steps'` is 1.

  G3 THE RECORD APPEND, all four parts, at C2.
     (a) BYTE ARITHMETIC: report the base byte count and its sha256, the
         slice length S after stripping any trailing newline, and confirm
         base + 2 + S equals the actual new size. Confirm the file still
         ends WITHOUT a trailing newline.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER: split the whole file on
         blank-line boundaries into units; let N be the number of units the
         SLICE RECORD itself contains, COUNTED by your script and not taken
         from this block; assert the LAST N units equal the slice's
         paragraphs IN ORDER.
     (c) NEGATIVE CONTROL on a scratch copy under `.remedy-wt/`, never on
         the tracked file: XOR-flip one byte lying inside the FIRST appended
         paragraph, confirm reader (b) REJECTS it, report the tracked file's
         sha256 before and after to show it did not move, and delete the
         scratch copy BY EXACT PATH.
     (d) COUNTS: `grep -c '^Gate: F109 R5 — '` is 1; `grep -c '^- R-[0-9]\{4\} — '`
         is UNCHANGED from the base commit; `grep -c '^Done: R-[0-9]\{4\} — '`
         is UNCHANGED; `grep -c '^Landed: R-'` is UNCHANGED. No finding is
         registered or resolved this round.

  G4 THE CODE ADDITIONS ARE ADDITIONS. For `pingpong_loop.py` at C3 and for
     the test file at C4, read the pre-commit and post-commit blobs with
     `git show <sha>:<path>` — never by writing either revision over the
     tracked file — compare them as SEQUENCES OF LINES with
     `difflib.SequenceMatcher(..., autojunk=False)`, and report that the
     opcodes are `equal` and `insert` ONLY, with no `delete` and no
     `replace`, together with the position and length of each inserted run.
     This is what proves constraints 4 and 6 rather than asserting them.

  G5 THE COLOUR OF THE TRANSFORM: control green, all three mutations red on
     the named cases. In a disposable worktree added at the C4 commit BY
     EXACT PATH under `.remedy-wt/`. FIRST, before trusting any mutation,
     run with the worktree as cwd:
       python3 -B -c "import packages.orchestration.pingpong_loop as m; print(m.__file__)"
     and confirm the path is INSIDE the worktree — an editable install can
     otherwise shadow it with the primary copy and every colour would be a
     reading of the wrong file. Purge `__pycache__` before every run. The
     command each time is:
       python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q
     (a) CONTROL, unmutated: exit 0, and report the passed count.
     (b) MUTATION A — delete the `enabled` early return. The failure set must
         INCLUDE SPEC H case 5, the kill-switch case.
     (c) MUTATION B — make the True branch append the segment UNCHANGED
         instead of the marker-replaced one. The failure set must INCLUDE
         SPEC H case 1.
     (d) MUTATION C — delete the line that appends the replaced NAME. The
         failure set must INCLUDE SPEC H case 3.
     Before each mutation, confirm the exact text you are changing occurs
     EXACTLY ONCE in `packages/orchestration/pingpong_loop.py`, and report
     that count. Restore with `git checkout --
     packages/orchestration/pingpong_loop.py` between mutations. Afterwards
     confirm the worktree is clean, remove it BY EXACT PATH with
     `git worktree remove --force <path>`, run `git worktree prune`, and
     report `git worktree list`. A wider red than ordered is fine — report
     it; a MISSING named case is a failure of the gate.

  G6 NO CALL SITE, AND THE SUITES. First the property this round is built
     on, measured SEMANTICALLY and not by grep — a docstring that names the
     function would defeat a text count, and a call is not a mention. Parse
     `packages/orchestration/pingpong_loop.py` with `ast`, walk every
     `ast.Call` node, and report the number whose callee resolves to the
     NAME `_dedupe_resumed_segments`. It must be 0. Report alongside it that
     exactly one `ast.FunctionDef` of that name exists, so the gate
     distinguishes "defined and uncalled" from "absent".
     Then run these suites SERIALLY, never two pytest processes alive at
     once, and report each exit code and passed count. The count in
     parentheses is what the REVIEWER measured at the base commit, so state
     yours beside it; only the first is expected to move, and only upward:
       tests/orchestration/test_semantic_dedupe.py        (79)
       tests/orchestration/test_prompt_segments.py        (25)
       tests/orchestration/test_builder_prompt_golden.py  (36)
       tests/orchestration/test_reviewer_prompt_golden.py (39)
       tests/orchestration/test_pingpong.py               (34)
       tests/orchestration/test_session_resume.py         (27)
       tests/orchestration/test_test_runner.py            (52)
       tests/cli/test_golden_path.py                      (42)
     The two prompt goldens are in this list precisely because constraint 5
     says this round cannot reach them: they are the evidence for that
     claim, not decoration. `test_builder_prompt_golden.py` pins frozen
     renders and an exact ten-name manifest tuple, so if a call site ever
     did slip in, that suite is where it would surface.

  G7 THE TREE. `git status --porcelain` is EMPTY. `git ls-files .remedy-wt`
     returns nothing. Report the insertion count — the `+` column only, per
     AGENTS.md DECISION F104 D1, never insertions plus deletions — for each
     commit BEFORE C5, and confirm each is under 500. Take those numbers
     from `git show --numstat` and from nothing else: a full-file rewrite's
     line counts before and after are NOT its numstat columns, and the
     handback's `## Commits` table is where that substitution has landed
     before. Compare the number you write in that table, cell by cell,
     against the numstat output you quote for this gate, and say in the
     handback that you did. Finally report the full `git diff --numstat` for
     `552bbd05ca3d458ef966b4d87157f62e917d444a..` your last commit and
     confirm it lists exactly the change set above and nothing else.

Handback: rewrite `.agent/handoff.md`. It carries F109, ROUND 6,
SESSION 2, the branch, the commit table with subjects and its `+/-`
column, the changed-files table, ONE LINE PER GATE with its real result,
the item-status table over C0a–C5, every deviation, the open-findings
count, and the next expected action. There is no length cap. Push after
C5.
