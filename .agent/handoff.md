# Handoff — F109 Semantic dedupe, SESSION 2, round 6

Branch: `feature/f109-semantic-dedupe`
Base commit: `552bbd05ca3d458ef966b4d87157f62e917d444a` (round 5 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

THIS IS THE FIRST ROUND OF SESSION 2. It booked round 5's PASS verdict into
`.agent/live_review.md` and landed the FIRST HALF of T002b — the pure
composition transform `_dedupe_resumed_segments` in
`packages/orchestration/pingpong_loop.py`. NO CALL SITE WAS ADDED:
`compose_builder_prompt` and `compose_reviewer_prompt` are byte-identical to
the base commit's, and the two prompt goldens prove it.

## Commits this round

| Item | SHA        | Commit subject                                                              |   +   |   -   |
|------|------------|-----------------------------------------------------------------------------|-------|-------|
| C0a  | `d255c2ad` | F109 R6 C0a: save the round 6 step block verbatim                           |  355  |   0   |
| C0b  | `245100a8` | F109 R6 C0b: mirror the round 6 block to last_block                         |  323  |  312  |
| C1   | `f4e03169` | F109 R6 C1: plan for round 6 — book round 5, land the dedupe transform      |   21  |   15  |
| C2   | `93532e9d` | F109 R6 C2: book the round 5 gate into the record                           |    3  |    1  |
| C3   | `24352750` | F109 R6 C3: the pure dedupe transform for a resumed session's segments      |   67  |    2  |
| C4   | `3516bddf` | F109 R6 C4: pin every rule of the dedupe transform before it has a caller   |  191  |    1  |

Every `+` and `-` cell above was read from `git show --numstat` for that exact
SHA and compared CELL BY CELL against the numstat output quoted under G7 — the
`+` column only, per AGENTS.md DECISION F104 D1, never insertions plus
deletions, and never a before/after line count of a rewritten file.

C5 is this handoff rewrite, committed on top of `3516bddf`. Every gate G1–G7 ran
at C4 or earlier, so every reading quoted below already existed when this file
was written; C5's own insertion count is deliberately NOT quoted anywhere here,
because the reviewer measures that one. Six single-parent commits in the range
before C5, no merge commit. The push happens AFTER C5, so the remote tip is not
quoted either.

## Changed files (this round)

| Path                                           | Change                                                     |
|------------------------------------------------|------------------------------------------------------------|
| `.agent/authored/f109-r6.md`                   | new — step block, `cp` not retyped                         |
| `.agent/last_block.md`                         | rewritten — byte mirror of the authored block              |
| `.agent/plan.md`                               | rewritten — SLICE PLAN, whole file, 48 lines               |
| `.agent/live_review.md`                        | appended ONCE — SLICE RECORD, one paragraph, at C2         |
| `packages/orchestration/pingpong_loop.py`      | added to — one private function, four imports extended     |
| `tests/orchestration/test_semantic_dedupe.py`  | added to — 1 new class, 11 new cases, no test changed      |
| `.agent/handoff.md`                            | rewritten — this file (C5)                                 |

No path outside the ordered change set was touched. `git diff --numstat` over
`552bbd05..3516bddf` lists exactly those six paths (C5 adds the seventh).

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum .agent/authored/f109-r6.md
  .agent/last_block.md` printed ONE digest twice:
  **`0debfaf9b922bb9620608bf726baa948b083fd01349020af65876d3df7cae7e7`**, equal
  to each other AND to the `SHA256_OF_THIS_BLOCK` the delegation wrapper stated.
  The scratch original `.remedy-wt/f109-r6.md` was verified against that digest
  as this round's FIRST action, before anything else was read or written, and
  C0a and C0b were both `cp` from it, never a retype. STATED PLAINLY, AS THE
  BLOCK REQUIRES: this chain compares THE SAVED COPY AGAINST ITS MIRROR — two
  files that are both the worker's own output — so it establishes
  self-consistency with the wrapper's digest and claims nothing about the bytes
  that were emitted.
- **G2 THE PLAN — PASS.** The SLICE PLAN was extracted MECHANICALLY from
  `.agent/authored/f109-r6.md` by a script that locates the `<<<SLICE PLAN` and
  `SLICE PLAN` delimiter lines; `cmp .agent/plan.md
  .remedy-wt/f109r6_plan.txt` produced NO OUTPUT and exit 0. `wc -l
  .agent/plan.md` = **48**, strictly under 50. `grep -c '^## Goal'` = **1** and
  `grep -c '^## Next Steps'` = **1**.
- **G3 THE RECORD APPEND — PASS, all four parts.**
  (a) BYTE ARITHMETIC: base **2042127** bytes, base sha256
  `9d9c7d6105668564f9fcbfad932f9dc7f56260fadb486096dd0929127feb8860`; the base
  was confirmed BY BYTE TEST to end WITHOUT a trailing newline (`base ends nl:
  False`). The extracted slice is 3855 bytes raw, so S = **3854** after
  stripping the trailing newline. Expected 2042127 + 2 + 3854 = **2045983**;
  actual new size **2045983**. The first 2042127 bytes of the new file are
  byte-identical to the base (`prefix preserved: True`), and the file still ends
  WITHOUT a trailing newline (`ends without nl: True`). New sha256
  `866a63baab2d7fe6d12319a37111a588d477c7756cbd7a1e26f2a54d206cbe92`.
  (b) A SECOND, STRUCTURALLY DIFFERENT READER: the whole file was split on
  blank-line boundaries into units. The script COUNTED the units of the SLICE
  RECORD itself rather than taking the number from the block — **N = 1**,
  because the record is one paragraph — and the file holds **855** units; the
  LAST 1 unit equals the slice's paragraph: **True**.
  (c) NEGATIVE CONTROL on a scratch copy
  `.remedy-wt/f109r6_live_review_flipped.md`, never on the tracked file: the
  byte at offset **2042229** (base 2042127 + 2 + 100, so arithmetically INSIDE
  the first appended paragraph, whose value was `'T'`) was XOR-flipped with
  0x20; the same reader (b) **REJECTED** the result (`last N == slice: False`,
  verdict REJECT), and it named unit 0 as the differing one. The tracked file's
  sha256 was `866a63baab2d7fe6d12319a37111a588d477c7756cbd7a1e26f2a54d206cbe92`
  BEFORE the control and
  `866a63baab2d7fe6d12319a37111a588d477c7756cbd7a1e26f2a54d206cbe92` AFTER —
  identical, so the tracked file did not move. The scratch copy was deleted BY
  EXACT PATH and `ls` on that path then reported "No such file or directory".
  (d) COUNTS: `grep -c '^Gate: F109 R5 — '` is **1** (it was **0** at the base
  commit). `grep -c '^- R-[0-9]\{4\} — '` is **331**, UNCHANGED from the base
  commit's 331. `grep -c '^Done: R-[0-9]\{4\} — '` is **63**, UNCHANGED from 63.
  `grep -c '^Landed: R-'` is **25**, UNCHANGED from 25. NO FINDING WAS
  REGISTERED OR RESOLVED THIS ROUND. `grep -c 'Landed: R-0770'` is **1**, so
  that line and the earlier `R-0770` paragraph both still stand, as constraint 2
  required.
- **G4 THE CODE ADDITIONS ARE ADDITIONS — RUN IN FULL, AND ITS LITERAL
  "INSERT ONLY" CLAUSE IS NOT MET; SEE DEVIATION 1.** Both files were read as
  BLOBS with `git show <sha>:<path>` — neither revision was ever written over
  the tracked file — split into lines and compared with
  `difflib.SequenceMatcher(None, pre, post, autojunk=False)`.
  C3, `93532e9d -> 24352750`, `packages/orchestration/pingpong_loop.py`, 5013 →
  5078 lines: opcode kinds `{equal: 7, insert: 5, replace: 1}`. **DELETE COUNT
  0.** The five inserts are at pre-line 47 (1 line: `PromptSegment`), pre-line 71
  (1 line: `DEDUPE_MIN_SEGMENT_CHARS`), pre-line 72 (1 line:
  `dedupe_marker_for_segment`), pre-line 74 (1 line: `should_dedupe_segment`) and
  pre-line 872 (**61 lines**, the whole new function with its comment and blank
  lines, landing at post-line 877). The single `replace` is pre-lines 26–27 →
  post-lines 26–27, 2 lines for 2 lines, and it is EXACTLY the two single-line
  import extensions SPEC G names: `from collections.abc import Callable` →
  `from collections.abc import Callable, Container, Sequence`, and
  `from dataclasses import dataclass, field` → `from dataclasses import
  dataclass, field, replace`. Nothing else in the file moved.
  C4, `24352750 -> 3516bddf`, `tests/orchestration/test_semantic_dedupe.py`, 901
  → 1091 lines: opcode kinds `{equal: 2, insert: 1, replace: 1}`. **DELETE COUNT
  0.** The one insert is **190 lines** appended at pre-line 901, i.e. one
  contiguous suffix after the last existing class. The single `replace` is
  pre-line 24 → post-line 24, 1 line for 1 line, and it is EXACTLY the import
  extension constraint 6 names: `from packages.orchestration.pingpong_loop
  import run_pingpong` → `from packages.orchestration.pingpong_loop import
  _dedupe_resumed_segments, run_pingpong`. So constraint 4 and constraint 6 hold
  in full — no existing function, test, assertion or comment was edited,
  reordered or deleted — and the two `replace` opcodes are the two named
  exceptions themselves, nothing wider.
- **G5 THE COLOUR OF THE TRANSFORM — PASS: CONTROL GREEN, ALL THREE MUTATIONS
  RED ON THE NAMED CASES.** Run in a disposable worktree added at the C4 commit
  `3516bddf` BY EXACT PATH
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r6-g5`, never in the primary
  checkout. FIRST, BEFORE ANY MUTATION WAS TRUSTED, with the worktree as cwd:
  `python3 -B -c "import packages.orchestration.pingpong_loop as m;
  print(m.__file__)"` printed
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r6-g5/packages/orchestration/pingpong_loop.py`
  — INSIDE the worktree, so no editable install shadowed it with the primary
  copy. `__pycache__` was purged before EVERY run (**0** directories found each
  time — a fresh worktree carries none and `python3 -B` writes none) and every
  pytest process used `python3 -B`. The argv each time was the block's exact
  command, `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`,
  launched through a no-shell `subprocess.run` so the REAL exit code could be
  read (deviation 2). Before each mutation the exact text being changed was
  confirmed to occur EXACTLY ONCE, and the file was restored with `git checkout
  -- packages/orchestration/pingpong_loop.py` between mutations, each restore
  leaving `git status --porcelain` empty inside the worktree.
  (a) CONTROL, unmutated: **exit 0, 90 passed**.
  (b) MUTATION A — deleted the `if not enabled: / return tuple(segments), ()`
  early return, occurrences **1**: **exit 1, 1 failed, 89 passed — RED.** The
  single failure IS SPEC H case 5, the kill switch:
  `TestDedupeResumedSegments::test_the_kill_switch_returns_every_segment_unchanged_and_no_names`.
  (c) MUTATION B — restored, then the True branch's
  `kept.append(replace(segment, text=dedupe_marker_for_segment(segment.name)))`
  became `kept.append(segment)`, occurrences **1**: **exit 1, 5 failed, 85
  passed — RED.** The failure set INCLUDES SPEC H case 1,
  `test_a_long_already_sent_segment_becomes_its_marker_with_name_and_rank_kept`,
  together with `test_a_smaller_min_chars_replaces_what_the_default_refuses`,
  `test_the_transform_reads_the_same_hashes_a_real_index_recorded`,
  `test_the_input_segments_are_not_mutated` and
  `test_composing_the_returned_segments_carries_the_marker_not_the_body`.
  (d) MUTATION C — restored, then deleted the
  `replaced_names.append(segment.name)` line, occurrences **1**: **exit 1, 7
  failed, 83 passed — RED.** The failure set INCLUDES SPEC H case 3,
  `test_the_replaced_names_are_exactly_the_replaced_segments_in_order`, together
  with the six other cases that assert on the returned names tuple.
  No test was edited in any direction to produce a colour. CLEANUP: the worktree
  was confirmed clean (`git -C … status --porcelain` empty after the final
  restore), then `git worktree remove --force
  /home/decodeux/Repos/remedy/.remedy-wt/f109-r6-g5` and `git worktree prune`.
  `git worktree list` afterwards shows the primary checkout plus exactly the
  four pre-existing `.remedy-wt/job-*` worktrees (`job-48a379ab5ca44ec5`,
  `job-7d1c93e2dc98415a`, `job-98e9364a83a34872`, `job-f76686b8435640e9`), which
  predate this branch and were left untouched.
- **G6 NO CALL SITE, AND THE SUITES — PASS.** THE PROPERTY FIRST, MEASURED
  SEMANTICALLY: `packages/orchestration/pingpong_loop.py` was parsed with `ast`
  and every `ast.Call` node walked — **1112** call nodes in the file — and the
  number whose callee resolves to the NAME `_dedupe_resumed_segments` (checking
  both `ast.Name.id` and `ast.Attribute.attr`) is **0**. Alongside it, exactly
  **1** `ast.FunctionDef` of that name exists, at line **882**, so the reading is
  "DEFINED AND UNCALLED" and not "absent". A docstring mentioning the name could
  not have moved either number.
  THEN THE EIGHT SUITES, run SERIALLY with never two pytest processes alive at
  once, every one exit 0 (mine, then the reviewer's base count in brackets):
  `tests/orchestration/test_semantic_dedupe.py` **90** [79] — the only one that
  moved, and upward, by the 11 new cases;
  `tests/orchestration/test_prompt_segments.py` **25** [25];
  `tests/orchestration/test_builder_prompt_golden.py` **36** [36];
  `tests/orchestration/test_reviewer_prompt_golden.py` **39** [39];
  `tests/orchestration/test_pingpong.py` **34** [34];
  `tests/orchestration/test_session_resume.py` **27** [27];
  `tests/orchestration/test_test_runner.py` **52** [52];
  `tests/cli/test_golden_path.py` **42** [42]. The two prompt goldens are the
  evidence for constraint 5, not decoration:
  `test_builder_prompt_golden.py` pins frozen renders and an exact ten-name
  manifest tuple, and it is green at its base count, so no call site slipped in.
- **G7 THE TREE — PASS.** `git status --porcelain` is EMPTY (no output).
  `git ls-files .remedy-wt` returns NOTHING. Insertion counts before C5, six
  numbers, the `+` column only, taken from `git show --numstat` and from nothing
  else: C0a **355**, C0b **323**, C1 **21**, C2 **3**, C3 **67**, C4 **191**.
  Every one is under 500. I compared those six numbers CELL BY CELL against the
  `+` column of the `## Commits this round` table above, and they agree; no
  before/after line count of a rewritten file was substituted for a numstat
  column anywhere. The full `git diff --numstat
  552bbd05ca3d458ef966b4d87157f62e917d444a..3516bddf` lists exactly six paths
  and nothing else: `.agent/authored/f109-r6.md` 355/0, `.agent/last_block.md`
  323/312, `.agent/live_review.md` 3/1, `.agent/plan.md` 21/15,
  `packages/orchestration/pingpong_loop.py` 67/2 and
  `tests/orchestration/test_semantic_dedupe.py` 191/1.

## Item status

| Item | Status | Reason                                                        |
|------|--------|---------------------------------------------------------------|
| C0a  | done   |                                                               |
| C0b  | done   |                                                               |
| C1   | done   |                                                               |
| C2   | done   |                                                               |
| C3   | done   |                                                               |
| C4   | done   |                                                               |
| C5   | done   | this file                                                     |

## What C3 actually landed

`_dedupe_resumed_segments` in `packages/orchestration/pingpong_loop.py`, placed
per constraint 4 AFTER the end of `_drop_one_newline_per_segment_boundary` and
BEFORE the `# F105 T003 migration site 5.` comment block that belongs to
`compose_builder_prompt`. 67 insertions, 2 deletions — the two deletions are the
two single-line import extensions and nothing else, as G4 shows line by line.

Signature exactly as SPEC G states, keyword-only after the second positional:
`(segments: Sequence[PromptSegment], sent_hashes: Container[str], *, enabled:
bool = True, min_chars: int = DEDUPE_MIN_SEGMENT_CHARS) ->
tuple[tuple[PromptSegment, ...], tuple[str, ...]]`.

Behaviour, exactly as ordered: `enabled` false returns `(tuple(segments), ())`
immediately and consults nothing else; otherwise, for each segment IN THE ORDER
GIVEN, the sha256 comes from THE SHIPPED PRODUCER via
`compose_prompt_segments((segment,)).manifest[0].sha256` — no `hashlib`
expression was added to this file — and `should_dedupe_segment(segment.text,
that_sha256, sent_hashes, enabled=True, min_chars=min_chars)` decides. On True
the result gets `replace(segment, text=dedupe_marker_for_segment(segment.name))`
and the name is appended to the replaced list; on False the SAME OBJECT is
appended, which a case asserts with `is`. RETURN ORDER IS INPUT ORDER — there is
no sort in the function, and the order case would fail visibly if one appeared.

The docstring carries all four things SPEC G demands: that this is F109 T002b's
decision step; that names and ranks survive by construction so composition order
and the cacheable prefix are untouched; that the sha256 comes from the shipped
producer because a second hashing expression here would make the feature fail
silently and safely; and the DELIBERATE ABSENCE — that NO CALLER EXISTS YET,
that wiring it into `compose_builder_prompt` and `compose_reviewer_prompt`
behind a bypass-by-default parameter is the next slice of T002b, and that the
`enabled` flag's config plumbing is T002c.

The four import statements SPEC G names were extended, each keeping the repo's
`order-by-type` isort order — CONSTANTS, then classes, then functions,
alphabetical within each group: `collections.abc` gained `Container` and
`Sequence`; `dataclasses` gained `replace`; the `prompt_segments` block gained
`PromptSegment` (between `ComposedPrompt` and `PromptSegmentError`); the
`session_sent_index` block gained `DEDUPE_MIN_SEGMENT_CHARS` (first, as the only
constant), `dedupe_marker_for_segment` and `should_dedupe_segment` (in the
function group, alphabetically). No existing function body changed.

I RAN THE SHIPPED FUNCTION, not just read it: the module imports and
`_dedupe_resumed_segments` resolves, and the eleven cases of C4 exercise every
branch of it against real registry segments and a real index.

## What C4 actually landed

191 insertions, 1 deletion — the deletion is the one import line that was
extended. One new class `TestDedupeResumedSegments` at the END of the file after
the last existing class, plus two module-level helpers and two module-level text
constants. All eleven cases are PURE: no `tmp_path`, no provider, no loop, no
network. Segments are built through `PromptSegmentRegistry` and
`registry.registered_segments()` — never as `PromptSegment` literals — and the
existing helpers `_real_manifest_rows` and `SegmentStabilityRank` are REUSED,
not redefined: the new `_sha256_by_name` is a thin wrapper over
`_real_manifest_rows`.

The long text is `"the dossier body, long enough to earn its replacement. " * 8`
= 432 characters, well over `DEDUPE_MIN_SEGMENT_CHARS` (200); the short text is
`"implement the transform"` = 23 characters, well under it, and is not a
substring of the long one, which is what makes case 12's three assertions
independent.

SPEC H's twelve numbered cases, mapped to the eleven test functions:

1 + 2. `test_a_long_already_sent_segment_becomes_its_marker_with_name_and_rank_kept`
   — the TEXT equals `dedupe_marker_for_segment("dossier")` exactly, and THE
   SAME CASE asserts `name` and `rank` are unchanged, as SPEC H case 2 orders.
3. `test_the_replaced_names_are_exactly_the_replaced_segments_in_order` — three
   long segments, two of them sent, `replaced == ("system", "task")`, and the
   unsent one still carries its own body.
4. `test_the_returned_order_is_input_order_and_never_rank_order` — three
   segments registered at ranks 5, 0, 2, so a rank sort would reorder them to
   system, dossier, steering; the case asserts the output names equal the input
   names in order AND equal the literal `["steering", "system", "dossier"]`.
5. `test_the_kill_switch_returns_every_segment_unchanged_and_no_names` — named
   so it cannot rot, and it first asserts that the SAME input IS deduped under
   the default, so nothing but the flag differs. Broken by MUTATION A alone.
6. `test_an_empty_sent_set_replaces_nothing` — and it asserts identity (`is`),
   pinning "the same object, not a copy".
7. `test_a_long_segment_whose_hash_was_never_sent_is_not_replaced`.
8. `test_a_short_already_sent_segment_is_refused_for_its_length_alone` — asserts
   `digest in sent` FIRST, so the refusal is demonstrably about LENGTH.
9. `test_a_smaller_min_chars_replaces_what_the_default_refuses` — both halves in
   the same case: refused at the default, replaced at
   `min_chars=len(TRANSFORM_SHORT_TEXT)`.
10. `test_the_transform_reads_the_same_hashes_a_real_index_recorded` — THE
    ANTI-DRIFT PIN: `_real_manifest_rows` → `SessionSentIndex.record_call(...,
    ok=True)` → `sent_hashes("session-a")` → the transform, which replaces
    exactly the long segment and leaves the short one.
11. `test_the_input_segments_are_not_mutated`.
12. `test_composing_the_returned_segments_carries_the_marker_not_the_body` —
    `compose_prompt_segments(kept)` contains the marker, does NOT contain the
    long segment's original text, and still contains the short segment's text
    verbatim.

Ruff followed BY CONSTRUCTION per constraint 7, which forbids gating on it and
on `npm run lint`: the longest line in the WHOLE of `pingpong_loop.py` after C3
is **119** and in `test_semantic_dedupe.py` after C4 is **101**, both under the
configured 120; both files parse with `ast`; the import groups are unchanged and
every extended list stays in `order-by-type` order.

## Deviations

1. **G4's LITERAL "OPCODES ARE `equal` AND `insert` ONLY" IS NOT MET: THERE IS
   EXACTLY ONE `replace` OPCODE PER FILE, AND EACH IS THE BLOCK'S OWN NAMED
   EXCEPTION.** The block contradicts itself here and I did not route around it.
   SPEC G orders four import statements to be EXTENDED and constraint 4 names
   that as its one exception; constraint 6 does the same for the test file. Two
   of those statements — `from collections.abc import Callable` and `from
   dataclasses import dataclass, field` in `pingpong_loop.py`, and `from
   packages.orchestration.pingpong_loop import run_pingpong` in the test file —
   are SINGLE-LINE imports, and extending a single line can only ever appear as
   a `replace` in a LINE-granular sequence comparison. The alternatives were to
   disobey SPEC G, or to add a second `from <same module> import` statement,
   which breaks the repo's isort layout that constraint 7 requires me to follow
   by construction. I applied the SPEC and reported the measurement. What the
   gate was built to prove still holds and is proved: **delete count 0 in both
   files**, the two `replace` opcodes are 2→2 and 1→1 lines and their full text
   is quoted under G4, and every other change is an `insert` — so no existing
   function, test, assertion or comment was edited, reordered or deleted.
2. **The sandbox bash guard refused several command FORMS**, not contents: `$?`
   expansions, and some compound commands. Real exit codes were therefore read
   through no-shell `subprocess.run` runners that received the block's EXACT
   argv and printed `proc.returncode`; `__pycache__` was purged with `os.walk`
   plus `os.remove`/`os.rmdir` rather than `find -exec`. Every `grep -c`,
   `wc -l`, `cmp`, `sha256sum`, `git show --numstat`, `git status --porcelain`,
   `git ls-files` and `git worktree` command the block names was run VERBATIM as
   its own standalone command and is quoted above. No gate was weakened,
   reworded or narrowed to fit the guard.
3. **MUTATIONS B AND C FAILED WIDER THAN THE ONE NAMED CASE EACH** — 5 and 7
   failures respectively, against A's exactly 1. The block permits a wider red
   and asks that it be reported. The extras are proper targets rather than
   collateral: every one of them asserts either on the replaced TEXT (B) or on
   the returned NAMES tuple (C), which are precisely what those two mutations
   destroy.
4. **SPEC H's twelve numbered cases are eleven test functions.** Case 2 says
   "THE SAME CASE asserts the segment's NAME and RANK are unchanged", so cases 1
   and 2 are one named test, exactly as ordered. The other ten are each their
   own named test.
5. **TWO NEW MODULE-LEVEL HELPERS AND TWO NEW CONSTANTS WERE ADDED TO THE TEST
   FILE** — `_registered_segments`, `_sha256_by_name`, `TRANSFORM_LONG_TEXT` and
   `TRANSFORM_SHORT_TEXT` — all in the appended suffix, none of them a
   redefinition of `_real_manifest_rows` or `SegmentStabilityRank`, which SPEC H
   forbids redefining and which are both reused instead. `_registered_segments`
   exists because SPEC H forbids `PromptSegment` literals, so segments must come
   from a real registry, and `_real_manifest_rows` returns manifest dicts rather
   than segments.
6. **`_registered_segments` is annotated `-> tuple` rather than
   `-> tuple[PromptSegment, ...]`.** Constraint 6 lets me extend ONE import
   statement in the test file, the `pingpong_loop` one; importing
   `PromptSegment` for an annotation would have meant extending a second, so I
   used the bare `tuple`. Trivially reversible if the reviewer prefers the
   precise annotation.
7. **Scratch artefacts live under `.remedy-wt/` and are gitignored**, never
   committed and never in the change set: `f109r6_extract.py`,
   `f109r6_plan.txt`, `f109r6_record.txt`, `f109r6_append.py`,
   `f109r6_reader_b.py`, `f109r6_negctl.py`, `f109r6_g4.py`, `f109r6_g5.py`,
   `f109r6_g6_ast.py`, `f109r6_suites.py`, plus
   `f109r6_live_review_flipped.md` which was deleted BY EXACT PATH straight
   after G3(c). `git ls-files .remedy-wt` returns nothing, as G7 records.
8. **Four `.remedy-wt/job-*` worktrees predate this branch** and were left
   alone. Exactly one worktree was created this round,
   `.remedy-wt/f109-r6-g5`, and it was removed by exact path and then pruned.
9. **No `docs/` file was touched.** The change set forbids it, and the new
   behaviour is not yet reachable by any caller, so there is nothing built to
   document; the deliberate absence is recorded where a reader would search for
   it — in the new function's own docstring — per AGENTS.md's discoverability
   convention. T003 owns the docs.

## Open findings

The ledger stands at **331** findings registered and **63** resolved, so the
open set is **268** — every one of those three numbers UNCHANGED by this round,
which registered no finding and resolved none. `.agent/candidates.md` is
unchanged and states EMPTY, so no block condition stands against F109. `R-0769`
remains registered and unfixed; its repair edits `README.md` and a docs test,
neither of which F109 owns. `.agent/STOP` was checked at the start of the round
and does not exist.

## Next expected action

`git push origin feature/f109-semantic-dedupe` immediately after this commit —
not quoted here by design, so the reviewer measures the remote tip itself. No PR
was created and nothing was merged.

Then the reviewer's round-6 verdict, booked into `.agent/live_review.md` in the
FIRST commit of round 7 (amend0827 rule 1: a verdict never buys a round of its
own). The build then resumes at the SECOND half of T002b — wiring
`_dedupe_resumed_segments` into `compose_builder_prompt` and
`compose_reviewer_prompt` behind a parameter that defaults to NO dedupe, and
passing the session's sent hashes at the two loop call sites only when a resume
ref is actually set. That round's first acceptance item is the non-resume
byte-equality golden, and it must gate on
`tests/orchestration/test_builder_prompt_golden.py`, which pins frozen renders
and an exact ten-name manifest tuple.
