# Handback — F109 Semantic dedupe, round 16

## Session

SESSION 4 of feature F109 · round 16 · rounds so far 16

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 16 rounds and 4 sessions it is NOT reached, so no scope report is due.
`.agent/STOP` was read from disk at the start of the round and does not exist.

## Range

Review of `cf210f6f..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `c7733977` | done | block copied verbatim with `shutil.copyfile`; G1 `cmp` exit 0 against the reviewer's own `.remedy-wt/f109-r16.md` |
| C0b `19ba3a0b` | done | mirrored to `.agent/last_block.md`; one sha256 for both files |
| C1 `9fda9b36` | done | PLAN16 extracted by delimiter index from the COMMITTED authored copy and applied; G2 `cmp` exit 0 |
| C2 `6c9a6ee6` | done | RECORD16 appended as the two bytes `\n\n` + slice; G3 (a)(b)(c)(d) all pass |
| C3 `9dab6cae` | done | PAIR A and PAIR B applied byte for byte to `session_sent_index.py` |
| C4 `ca4879b4` | done | PAIR C and PAIR D applied byte for byte to `test_semantic_dedupe.py` |
| C5 (this commit) | done | handback rewritten per handback_template.md, then pushed |

No item was skipped, none deviated, and the block's ordered commit sequence was
followed exactly — no extra commit, no dropped commit, no reordering.

## Commits

### c7733977 F109 R16 C0a: save the round 16 block verbatim to authored

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f109-r16.md` | +327 / -0 | the reviewer's round 16 block, byte-for-byte |

### 19ba3a0b F109 R16 C0b: mirror the round 16 block to last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +199 / -259 | mirror of the saved block; single-state-file rewrite |

### 9fda9b36 F109 R16 C1: the plan turns to the staleness repair round

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +10 / -11 | PLAN16 verbatim; Current Step turns to round 16, the landed `R-0780` next step is retired |

### 6c9a6ee6 F109 R16 C2: book the round 15 gate and register R-0781

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +5 / -1 | RECORD16 appended: the round 15 PASS entry and the `R-0781` registration |

### 9dab6cae F109 R16 C3: the sent-index absence notes name the wiring that landed

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/session_sent_index.py` | +13 / -8 | PAIR A and PAIR B — the two stale "deliberate absence" bullets now name the call sites and the commits that made them exist |

### ca4879b4 F109 R16 C4: the dedupe suite docstring names T003d and drops the positional claim

| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_semantic_dedupe.py` | +7 / -5 | PAIR C and PAIR D — the module docstring enumerates T003d and quantifies over manifest-shape cases instead of "the first case" |

### (this commit) F109 R16 C5: handback for round 16

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | see the commit itself | the round 16 handback; a handoff cannot table the commit that writes it (R-0149 pattern), and constraint 7 forbids quoting its own insertion count |

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f109-semantic-dedupe` | run after this commit; the real result is reported in the round report |
| `git worktree list` | four PRE-EXISTING `remedy/job-*` worktrees plus the primary checkout; this round created NONE and removed NONE |
| `gh pr ...` | none. No PR was created, edited or merged this round, per constraint 8 |

No destructive verification was needed this round, so no disposable worktree was
added. The one scratch artefact the block ordered —
`.remedy-wt/live_review_negative_control_r16.md` — was created, used and deleted
BY ITS EXACT PATH inside G3(c), and `os.path.exists` on that exact path reads
False.

## Verification

Eight gates, every one RUN, every exit code REAL. All eight ran at commits
strictly earlier than this one.

- **G1 TRANSPORT — PASS.** `cmp .remedy-wt/f109-r16.md .agent/authored/f109-r16.md` → `REAL_EXIT=0`, no output. `sha256sum .agent/authored/f109-r16.md .agent/last_block.md` → `b85da6a0394e996f10a3f672c1204c09024818efc41f1563388f25252e135c52` TWICE, one digest for both files. The source is the reviewer's own pre-emission original, so this is a real transport proof and not self-consistency.
- **G2 THE PLAN — PASS.** PLAN16 re-extracted by delimiter index from the COMMITTED `.agent/authored/f109-r16.md` (43 lines strictly between `BEGIN PLAN16` and `END PLAN16`, 1904 bytes); `cmp` against `.agent/plan.md` → `REAL_EXIT=0`, no output. `wc -l .agent/plan.md` = 43 (under the AGENTS.md 50). `grep -c '^## Goal'` = 1, `grep -c '^## Next Steps'` = 1.
- **G3 THE RECORD APPEND — PASS, all four readings.**
  - (a) ARITHMETIC. Base at `cf210f6f`: size 2108223, sha256 `e8cef8e7cdb7a4fecc631b57a41cf28599977cd7878ceb9ecaaade1f4c34a1cc`, ends WITHOUT a trailing newline. That digest was independently confirmed against `git show cf210f6f:.agent/live_review.md`, so the base really was the round 15 tip and not a rewound file. S (appended bytes) = 4630. New size 2112853. `2108223 + 4630 == 2112853` → True. New sha256 `27f9d1b9bfbb530fabaf895bf473469632af2ee14bd56e14196ba06f1c9e83bc`; the file still ends WITHOUT a trailing newline.
  - (b) SECOND READER, COUNTING NO BYTE, over the WHOLE appended region. The script split the entire file on blank-line boundaries and derived N from the slice itself: **N = 2**. The LAST 2 units equal RECORD16's 2 paragraphs IN ORDER → True. Unit 1 opens `'Gate: F109 R15 — the round 15 entry. VERDICT PASS, over the '`; unit 2 opens `"- R-0781 — Low, THE DEDUPE SUITE'S MODULE DOCSTRING OMITS A "`.
  - (c) NEGATIVE CONTROL on the FIRST appended paragraph. Tracked sha256 BEFORE `27f9d1b9…e83bc`. Copy written to `.remedy-wt/live_review_negative_control_r16.md`; first appended paragraph located at offset 2108225; byte at offset 2108235 flipped from `' '` to `'X'`. Reader (b) ACCEPTS the copy: **False**. Reader (b) ACCEPTS the tracked file: **True**. Tracked sha256 AFTER `27f9d1b9…e83bc` — never moved. `os.remove` by exact path, then `os.path.exists('/home/decodeux/Repos/remedy/.remedy-wt/live_review_negative_control_r16.md')` → **False**.
  - (d) COUNTS AS A SET DIFFERENCE (`R-0778`), base read from `git show d52a5371:.agent/live_review.md` and never by rewinding the tracked file. Base `d52a5371`: registered ids 340, DISTINCT 340, `Done:` lines 65, DISTINCT resolved ids 63, `len(set(registered) - set(resolved))` = **277**. New state: registered ids 342, DISTINCT 342, `Done:` lines 66, DISTINCT resolved ids 64, open set = **278**. `grep -c '^Gate: F109 R15 — '` = 1. `grep -c '^- R-0781 — '` = 1. (The base/new registered gap of 2 is `R-0780`, landed by round 15's own C2 between `d52a5371` and `cf210f6f`, plus `R-0781` added here; at `cf210f6f` the figures were 341 registered / 66 `Done:` / 64 distinct resolved / open 277, exactly as RECORD16 states.)
- **G4 THE FOUR PAIRS — PASS, every one a REWRITE.** Measured off `git show <sha>^:<path>` and `git show <sha>:<path>` blobs, so the readings are of the committed states and not of a working copy.

  | Pair | File | FROM before | FROM after | TO before | TO after |
  |---|---|---|---|---|---|
  | A | `packages/orchestration/session_sent_index.py` (C3 `9dab6cae`) | 1 | 0 | 0 | 1 |
  | B | `packages/orchestration/session_sent_index.py` (C3 `9dab6cae`) | 1 | 0 | 0 | 1 |
  | C | `tests/orchestration/test_semantic_dedupe.py` (C4 `ca4879b4`) | 1 | 0 | 0 | 1 |
  | D | `tests/orchestration/test_semantic_dedupe.py` (C4 `ca4879b4`) | 1 | 0 | 0 | 1 |

  The containment test was also re-run mechanically before applying anything: for all four pairs `TO contains FROM` is **False**, so each is a genuine rewrite. The test file's first three bytes read `'"""'` and the module holds exactly **one** top-level bare string expression, so the triple quote was not duplicated.
- **G5 COMMENTS ONLY, NO CODE MOVED — PASS.** `ast` over the BEFORE and AFTER blobs of each commit.
  - `packages/orchestration/session_sent_index.py` at `9dab6cae`: definition names IDENTICAL (17 names, sorted equality). Per-definition executable-statement counts (body with a leading bare docstring stripped) unchanged, and the per-NAME body-statement map is identical. Constants 68 before, 68 after, with exactly **1** differing pair, and that differing constant IS the module docstring on both sides (`ast.get_docstring(tree, clean=False)` equality → `True -> True`). SequenceMatcher(None, before, after, autojunk=False) produced 42 non-equal opcodes, all inside the character range 1575–2603, which is the docstring's absence-bullet region. TOTAL lines deleted: **8**.
  - `tests/orchestration/test_semantic_dedupe.py` at `ca4879b4`: definition names IDENTICAL (155 names). Per-definition executable-statement counts unchanged; per-name map identical. Constants 755 before, 755 after, exactly **1** differing pair, and it IS the module docstring (`True -> True`). SequenceMatcher produced 15 non-equal opcodes, all within the first ~1180 characters, i.e. the module docstring. TOTAL lines deleted: **5**.
- **G6 THE SUITES, RUN SERIALLY — PASS, and NO COUNT MOVED IN EITHER DIRECTION.** One process finished before the next started.

  | Suite | Collected / result | Real exit | Reviewer's `cf210f6f` figure |
  |---|---|---|---|
  | `tests/orchestration/test_semantic_dedupe.py` | 130 passed | 0 | 130 |
  | `tests/orchestration/test_prompt_trace.py` | 54 passed | 0 | 54 |
  | `tests/orchestration/test_session_resume.py` | 27 passed | 0 | 27 |
  | `tests/orchestration/test_pingpong.py` | 34 passed | 0 | 34 |
  | `tests/orchestration/test_pingpong_cli.py` | 173 passed | 0 | 173 |
  | `tests/docs/` | 295 passed | 0 | 295 |
  | `tests/cli/test_golden_path.py` (canary) | 42 passed | 0 | 42 |

  Total 755 passed, nothing red, nothing skipped, nothing xfailed. The dedupe suite was additionally run BEFORE C4 in the same shell posture and read **130 passed, exit 0** there too, so constraint 3's "identical before and after" is a measured before/after pair and not an inference from a single reading. No count rose and none fell.
- **G7 THE REPAIRED PROSE IS TRUE — PASS, every reading re-measured.**
  - (a) In `packages/orchestration/session_sent_index.py`: `invokes it yet` = **0**, `invokes either function yet` = **0**.
  - (b) In `packages/orchestration/pingpong_loop.py`: `invalidate_on_resume_fallback(` = **2**, `record_finalized_call(` = **2**, `should_dedupe_segment(` = **1**, `dedupe_marker_for_segment(` = **1**. Every count the new PAIR A / PAIR B text claims holds.
  - (c) `git cat-file -e <sha>^{commit}` → exit **0** for all four of `7451e9c7`, `24352750`, `60343048`, `b245e1c9`.
  - (d) Module docstring READ ALONE via `ast.get_docstring(ast.parse(source))`: contains `T003d` **1x** and `the first case` **0x**. The WHOLE-FILE count of `the first case` is **1**, which is the unrelated plural `they are the first cases in this` that PAIR D deliberately does not touch — it now sits at line **560**, having moved down by two lines because PAIR C lengthened the docstring; the block's "line 558" was measured at `cf210f6f` and was correct there. The class `TestTheRunsOwnTraceMeasuresWhatItWithheld` is present.
  - NO reading contradicted any slice. Nothing was silently corrected.
- **G8 THE TREE AND THE SWEEP — PASS.** `git status --porcelain` → EMPTY (no output). `git ls-files .remedy-wt` → nothing. Insertion counts from `git show --numstat`, `+` column ONLY per AGENTS.md DECISION F104 D1, for every commit of this round except C5: C0a `c7733977` **327**, C0b `19ba3a0b` **199**, C1 `9fda9b36` **10**, C2 `6c9a6ee6` **5**, C3 `9dab6cae` **13**, C4 `ca4879b4` **7**. Compared cell by cell against the `## Commits` table above: every figure matches, and every commit is far under the 500-insertion cap, so no oversize declaration is due. The full-file staleness re-read is in the section below.

## Authored-text proofs

| Slice | Target | Proof |
|---|---|---|
| the whole block | `.agent/authored/f109-r16.md` | `cmp` against the reviewer's own `.remedy-wt/f109-r16.md` → exit 0; sha256 `b85da6a0…35c52` |
| the whole block | `.agent/last_block.md` | same sha256 `b85da6a0…35c52` as the authored copy |
| PLAN16 | `.agent/plan.md` | `cmp` of the delimiter-extracted slice (from the COMMITTED authored copy) against the file → exit 0 |
| RECORD16 | `.agent/live_review.md` | G3 (a) byte arithmetic + (b) whole-region paragraph reader + (c) negative control |
| PAIR A, PAIR B | `packages/orchestration/session_sent_index.py` | G4: FROM 1→0, TO 0→1, each measured on the commit's own blobs |
| PAIR C, PAIR D | `tests/orchestration/test_semantic_dedupe.py` | G4: FROM 1→0, TO 0→1, same method |

Every slice was extracted BY DELIMITER INDEX (`lines.index("BEGIN <NAME>")` /
`lines.index("END <NAME>")`) and applied as bytes. Nothing was retyped, nothing
was rewrapped, nothing was re-indented, and no slice was altered in any way.

## Pending resolution — NOT resolved this round

`R-0780` and `R-0781` are REPAIRED ON DISK but are NOT RESOLVED. No `Done:`
paragraph and no `Landed:` line was written for either, because only
reviewer-authored text sets a resolution (block constraint 4). This handback is
the durable carrier of that pending state under amend0827 rule 1, so the next
round's first commit can book both resolutions from the disk state these commits
produced.

- `R-0780` — resolution condition "no bullet of that section says any part of this module's wiring is absent from `pingpong_loop.py`". Measured met for the two bullets the finding names: both now assert the call sites EXIST and name `7451e9c7`, `24352750`, `60343048` and `b245e1c9`, all four of which `git cat-file -e` resolves. See the sweep below for the one bullet the finding explicitly excluded.
- `R-0781` — resolution condition "the docstring names every F109 slice the file covers and makes no positional claim about which case uses the real producer". Measured met: `T003d` appears 1x in the docstring read alone, `the first case` appears 0x in it, and the T003d class is present in the file.

Open-finding count as a SET DIFFERENCE (`R-0778`, never a subtraction):
**278 open** = 342 distinct registered ids − 64 distinct resolved ids. With
`R-0780` and `R-0781` resolved next round it becomes 276.

## G8 staleness sweep — every file this round touched, re-read end to end

`.agent/authored/f109-r16.md` and `.agent/last_block.md` are byte-identical
copies of the reviewer's block and are not swept for staleness: correcting them
would destroy the transport proof they exist to be.

`.agent/plan.md` — re-read in full at 43 lines. Nothing stale. Every claim in
Risks was re-checked: every concrete adapter still returns `supports_resume =
False`; `measure_dedupe_savings_from_traces` still has no production caller;
`R-0778` and `R-0769` are both still open in the record.

`.agent/live_review.md` — append-only by constraint 2; no landed entry was read
for repair and none was rewritten. The `\ No newline at end of file` marker moved
from the `R-0780` line to the `R-0781` line, which is the only way an append to a
newline-less file can appear in a diff; the `R-0780` line's own bytes are
unchanged, as `git diff` showed with an unmodified context line.

`packages/orchestration/session_sent_index.py` — re-read all 374 lines.

- DECLARED, NOT REPAIRED (outside the four pairs, constraint 5). The FIRST
  absence bullet, lines 22–26, still reads "Writing ``as_evidence_dicts()`` into
  the run evidence at the ``on_call_finalized`` seam is F109 T001b", phrased as
  outstanding work. It is not: `pingpong_loop.py` assigns
  `result.session_sent_evidence = session_sent_index.as_evidence_dicts()` at
  lines 3479 and 3827, which I measured. The bullet's FIRST sentence is still
  strictly true — it is scoped by the word "here" to this module, and this module
  genuinely neither persists nor re-reads the index — so only the second sentence
  reads as pending. `R-0780`'s own registered text examined this bullet and left
  it alone deliberately, so this is a KNOWN and DOCUMENTED exclusion rather than
  a new defect, and the block supplied no pair for it. Declared here so the
  reviewer can decide whether to widen `R-0780` or leave the exclusion standing;
  I did not touch it.
- Everything else re-read as true. The "This module is PURE … imports nothing
  from ``packages.orchestration``" claim holds — the only import is
  `collections.abc`. The `DEDUPE_MIN_SEGMENT_CHARS` comment's "roughly forty
  characters" for a marker holds: `[unchanged: {name}, previously provided]` is
  35 characters plus the name. The Public API block matches the module's actual
  public names one for one.

`tests/orchestration/test_semantic_dedupe.py` — re-read all 2310 lines, with the
whole prose surface (every comment and every docstring) extracted mechanically
via `tokenize` + `ast` so no comment could be skipped by eye.

- DECLARED, NOT REPAIRED (outside the four pairs, constraint 5) — A NEW
  STALENESS INSTANCE. The `_capture_compositions` helper docstring at line 1694
  ends "so wrapping the two functions in the loop's own module namespace is how
  the LOOP's compositions are read without widening production code **that has
  no consumer for the report yet**". That "yet" is now false. `deduped_names` HAS
  a production consumer: `packages/orchestration/prompt_trace.py:172` reads
  `list(composed_prompt.deduped_names)` to populate
  `PromptTraceEntry.deduped_segment_names`. I grepped `deduped_names` across
  `packages/` and `apps/` to establish this rather than inferring it. This is the
  same CLASS as `R-0780` and `R-0781` — a stale "not yet" note in the place a
  reader is told to look — but it is a THIRD site, in a helper docstring neither
  finding names, and no pair in this block reaches it. NOT repaired, per
  constraints 1 and 5.
- EXAMINED AND FOUND TRUE, recorded so a later reader does not re-open it. The
  `TestChainAgainstTheRealLoop` class docstring says its cases "are the first
  cases in this feature proving the index is fed by ACTUAL provider calls". This
  is the whole-file `the first case` substring match G7(d) predicted, and it is
  NOT a positional claim of the `R-0775` class: it is a chronological claim about
  which slice first drove the real loop, it says T001b-ii, and the module
  docstring PAIR C just wrote agrees ("beginning at F109 T001b-ii"). It is true
  and PAIR D correctly leaves it alone.
- The other dated comments were checked and are historically framed rather than
  stale: the SPEC Z preamble's "Until this round the Builder wrote its trace two
  statements BEFORE that recomposition" describes the state the repair replaced,
  and the comment at line 1892 already carries its own correction note ("R-0777
  corrected this comment, which described a single trace").
- Nothing outside the change set was edited anywhere in this round.

## Deviations & assumptions

**No deviation from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3,
C4, C5 were committed in exactly that order, one commit each, with no extra
commit, no dropped commit and no reordering.

**No deviation from any slice.** All four pairs and both `.agent/` slices were
applied byte for byte. No slice looked wrong, so constraint 1's "apply anyway and
declare" route was not needed for any of them.

Assumptions, each stated because a reader could reasonably have chosen otherwise:

1. **The G2 comparison text carries a trailing newline.** The block says to
   `cmp` the delimiter-extracted PLAN16 against `.agent/plan.md` and expect exit
   0. I read "the lines strictly between the delimiters" as each line carrying
   its own terminating newline, so the extracted text ends with one and
   `.agent/plan.md` does too. Under the other reading — join with `\n`, no
   trailing newline — the same `cmp` would exit 1 on an EOF difference while the
   file content was correct. The reading I chose is the one that makes the gate
   meetable; the file is 1904 bytes, 43 lines, each newline-terminated.
2. **G2 was re-derived from the COMMITTED authored copy**, not from the
   `.remedy-wt` scratch, so the gate reads the artefact the branch actually
   carries. G1 already proved the two are byte-identical, so this is strictly
   stronger.
3. **G5's "only differing AST constant" check compares RAW docstrings.**
   `ast.get_docstring()` defaults to `clean=True`, which dedents, so a raw
   constant never equals it and the check read False on a correct file at first
   pass. Re-run with `clean=False` it reads `True -> True` for both files. The
   underlying fact — exactly one differing constant per file — was unchanged by
   the fix; only the identification of WHICH constant needed the correct call.
4. **G5's "executable statement count" is per definition, over the body with a
   leading bare docstring stripped.** Reported two ways — the multiset of counts,
   and the per-NAME map — and both are identical across both commits.
5. **No `Done:` and no `Landed:` line was written** for `R-0780` or `R-0781`, per
   constraint 4. The pending state rides in the "Pending resolution" section
   above.
6. **Two defects found in the sweep were declared and NOT repaired** — the first
   absence bullet in `session_sent_index.py` (a documented `R-0780` exclusion)
   and the `_capture_compositions` "no consumer yet" docstring in the dedupe
   suite (a new, third instance of the same class). Both are outside the four
   authored pairs, so constraint 5 forbade touching them.
7. **Scratch discipline.** Helper logic ran from `.py` files under the gitignored
   `.remedy-wt/` and each was removed by its exact path after use; no glob
   deletion was used anywhere. `.remedy-wt/f109-r16.md` — the REVIEWER's own file,
   not mine — was left in place so the reviewer can re-run G1 independently.
   `git ls-files .remedy-wt` returns nothing, and the tree is clean.
   ONE SURPRISE, DECLARED RATHER THAN TIDIED: `.remedy-wt/r16slices/` ALREADY
   EXISTED, left behind by an earlier feature's round 16 (it holds
   `PLANF021R16`, `CONTRACTNOW`, `ANCFILE`, `RECORD16`, `RLP3_FROM`, `RLP3_TO`,
   `CONTRACTPATHS3_FROM`, `CONTRACTPATHS3_TO`, none of them mine). My slice files
   all carried a `.txt` suffix, so none of those eight names was written to or
   overwritten, and I deleted only my own twelve `.txt` files, by exact path. The
   directory therefore survives with exactly its prior contents; I did not remove
   another round's artefacts.

## Next

The INTEGRATION GATE (`docs/agents/integration_gate.md`), over a tree whose
comments are now true. Before that, the reviewer's round 16 gate should book the
two pending resolutions — `R-0780` and `R-0781` — from the disk state these
commits produced, and decide what to do with the two staleness sites declared in
the sweep above: the excluded first absence bullet in `session_sent_index.py`,
and the `_capture_compositions` docstring's falsified "no consumer for the report
yet". Phase 1 rule 1 first: re-read `.agent/STOP` from disk before anything else.
