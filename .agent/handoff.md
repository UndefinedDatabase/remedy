# Handoff — F109 Semantic dedupe, SESSION 2, round 8

Branch: `feature/f109-semantic-dedupe`
Base commit: `81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9` (round 7 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

THIS ROUND BOOKED ROUND 7'S PASS VERDICT, REGISTERED `R-0771` BEFORE THE FIX
EXISTED, AND THEN FIXED IT. A resume FALLBACK is not a resumed session, yet the
loop re-sent the prompt composed FOR the resumed session — `[unchanged: …]`
markers and all — into the brand-new session the retry opens, and then recorded
that deduped manifest as what was sent. Both roles now recompose at full content
as the FIRST statements of their fallback branch and rebind the composed prompt,
so the bytes sent, the `fallback_prompt` stored by `_finalize_call` and the
manifest read by `record_finalized_call` describe one and the same call. The
stale "NO CALLER EXISTS YET" paragraph in `_dedupe_resumed_segments`'s docstring
is retired in the same commit.

READ DEVIATION 1 FIRST: on the REVIEWER side the two names SPEC M lists are not
enough. The reviewer sends `reviewer_effective`, not `reviewer_prompt`, so I
rebound a THIRD name inside that branch. Without it the reviewer half of the fix
does nothing, and SPEC O case 2 fails. Declared, not smuggled.

## Commits this round

| Item | SHA        | Commit subject                                                                            |   +   |   -   |
|------|------------|-------------------------------------------------------------------------------------------|-------|-------|
| C0a  | `3d032c1e` | F109 R8 C0a: save the round 8 step block verbatim                                         |  381  |   0   |
| C0b  | `6033eef4` | F109 R8 C0b: mirror the round 8 block to last_block                                       |  249  |  225  |
| C1   | `9df0ff17` | F109 R8 C1: plan for round 8 — book round 7, register R-0771 and repair the resume fallback |   14  |  11   |
| C2   | `c842ec41` | F109 R8 C2: book the round 7 gate, register R-0771 and its reviewer-prose slip            |    8  |   2   |
| C3   | `1b7759b7` | F109 R8 C3: a resume fallback recomposes at full content and rebinds what it sends        |   53  |  10   |
| C4   | `54f8ffa9` | F109 R8 C4: pin that a resume fallback sends full content on both roles                   |  204  |   2   |

Every `+` and `-` cell above was read from `git show --numstat` for that exact
SHA and COMPARED CELL BY CELL against the numstat output quoted under G7 — I
state plainly that I did that comparison, and the cells agree. The `+` column
only, per AGENTS.md DECISION F104 D1, never insertions plus deletions, and never
a before/after line count of a rewritten file. C2 touches two files (5+1 and
3+1), so its cells are the file-summed 8 and 2; C4 touches two files (3+1 and
201+1), so its cells are the file-summed 204 and 2.

C5 is this handoff rewrite, committed on top of `54f8ffa9`. Every gate G1–G7 ran
at C4 or earlier, per constraint 9, so every reading quoted below already existed
when this file was written; C5's own insertion count is deliberately NOT quoted
anywhere here, because the reviewer measures that one. Six single-parent commits
in the range before C5, no merge commit. The push happens AFTER C5, so the remote
tip is not quoted either.

## Changed files (this round)

| Path                                           | Change                                                          |
|------------------------------------------------|-----------------------------------------------------------------|
| `.agent/authored/f109-r8.md`                   | new — step block, `cp` not retyped                              |
| `.agent/last_block.md`                         | rewritten — byte mirror of the authored block                   |
| `.agent/plan.md`                               | rewritten — SLICE PLAN, whole file, 47 lines                    |
| `.agent/live_review.md`                        | appended TWICE — RECORD+FINDING at C2, SLICE P at C4            |
| `.agent/prose_slips.md`                        | appended ONCE — SLICE SLIP, one paragraph, at C2                |
| `packages/orchestration/pingpong_loop.py`      | 1 docstring paragraph, 2 arg dicts hoisted, 2 fallback repairs  |
| `tests/orchestration/test_semantic_dedupe.py`  | `_provider_pair` extended, 1 new class appended, no case changed |
| `.agent/handoff.md`                            | rewritten — this file (C5)                                      |

No path outside the ordered change set was touched. `git diff --numstat` over
`81a00635..54f8ffa9` lists exactly seven of those paths (C5 adds the eighth,
`.agent/handoff.md`).

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum .agent/authored/f109-r8.md
  .agent/last_block.md` printed ONE digest twice:
  **`d4fecd3d21b3a10e573e66fb5a84b20869a1d6fa98f9d207685c371ccdcdb1d8`**, equal
  to each other AND to the `SHA256_OF_THIS_BLOCK` the delegation wrapper stated.
  The scratch original `.remedy-wt/f109-r8.md` was verified against that digest as
  this round's FIRST action, before anything else was read or written, and printed
  the same digest a third time; C0a and C0b were both `cp` from it, never a
  retype. STATED PLAINLY, AS THE BLOCK REQUIRES: this chain compares THE SAVED
  COPY AGAINST ITS MIRROR and claims nothing about the bytes that were emitted.
- **G2 THE PLAN — PASS.** The SLICE PLAN was extracted MECHANICALLY from
  `.agent/authored/f109-r8.md` by a script that locates the `<<<SLICE PLAN` and
  `SLICE PLAN` delimiter lines by exact line equality and takes the lines strictly
  between them; `cmp .agent/plan.md .remedy-wt/slice_plan.txt` produced NO OUTPUT
  and exit 0. `wc -l .agent/plan.md` = **47**, strictly under 50.
  `grep -c '^## Goal'` = **1** and `grep -c '^## Next Steps'` = **1**. The
  extraction copy was deleted BY EXACT PATH.
- **G3 THE APPENDS — PASS, all five parts.**
  (a) `.agent/live_review.md` BYTE ARITHMETIC at C2: base **2050782** bytes, base
  sha256 `4720fe79346a513edd6854b5e8325b4ba665754b1b1aa0a27e1df37be5c43b6a`,
  confirmed BY BYTE TEST to end WITHOUT a trailing newline. Two paragraphs were
  appended in that commit, S(RECORD) = **3825** and S(FINDING) = **2198** after
  stripping each extracted slice's trailing newline, total S = **6023**. Expected
  2050782 + 2 + 3825 + 2 + 2198 = **2056809**; actual new size **2056809** —
  MATCH. The file still ends WITHOUT a trailing newline. C2 sha256
  `e54873cbbdcac39c1534eb7bfb39f78ef292644d1fcbea068904a35ead4e166c`. SLICE P at
  C4 adds 2 + **241** = 243 more: 2056809 + 243 = **2057052**, actual **2057052**
  — MATCH, still no trailing newline, final sha256
  `6bc249a596c0b4234533159dd3c28f0279acf750e086a86c296466f25167aa3a`.
  (b) A SECOND, STRUCTURALLY DIFFERENT READER, run at C2: the whole file was
  split on blank-line boundaries into units (**858** of them). The script COUNTED
  the units the C2 append itself contains rather than taking the number from the
  block — **N = 2** — and asserted the LAST 2 units equal the appended paragraphs
  IN ORDER: **True**, exit 0. Re-run after C4 over all three of this round's
  paragraphs (**N = 3**, 859 units): **True**, exit 0.
  (c) NEGATIVE CONTROL on a scratch copy `.remedy-wt/live_review_negctl.md`, never
  on the tracked file: the byte at offset **2050884**, which lies inside the FIRST
  appended paragraph, was XOR-flipped with 0x01 (`R` → `S`); reader (b) **REJECTED
  it — exit 1**, reporting unit 0 mismatched while unit 1 still matched. The
  tracked file's sha256 was
  `e54873cbbdcac39c1534eb7bfb39f78ef292644d1fcbea068904a35ead4e166c` BEFORE and
  `e54873cbbdcac39c1534eb7bfb39f78ef292644d1fcbea068904a35ead4e166c` AFTER —
  identical, so the tracked file did not move. The scratch copy was deleted BY
  EXACT PATH.
  (d) COUNTS in `.agent/live_review.md` AFTER C4, each base number measured
  against `git show 81a00635:.agent/live_review.md`:
  `grep -c '^Gate: F109 R7 — '` is **1** (**0** at the base commit).
  `grep -c '^- R-[0-9]\{4\} — '` is **332**, up from **331** — a rise of exactly
  **1** — and `grep -c '^- R-0771 — '` is **1**.
  `grep -c '^Landed: R-'` is **26**, up from **25** — a rise of exactly **1** —
  and `grep -c '^Landed: R-0771 — '` is **1**.
  `grep -c '^Done: R-[0-9]\{4\} — '` is **63**, UNCHANGED from **63**: this round
  resolves nothing and writes no `Done:` paragraph, per constraint 4.
  (e) `.agent/prose_slips.md`: base **43860** bytes, new **45129**; the base bytes
  are a BYTE-EXACT PREFIX of the new file (**True**); the new file still ends
  WITHOUT a trailing newline (**True**); lines matching `^2026-` went **65 → 66**,
  a rise of exactly **1**.
- **G4 THE EDIT SHAPE IS THE ORDERED ONE — PASS; EVERY NON-EQUAL OPCODE IS
  ACCOUNTED FOR.** Both revisions of both files were read as BLOBS with `git show
  <sha>:<path>` — neither revision was ever written over the tracked file — split
  into lines and compared with `difflib.SequenceMatcher(None, pre, post,
  autojunk=False)`.
  **C3, `c842ec41 -> 1b7759b7`, `packages/orchestration/pingpong_loop.py`, 5138 →
  5181 lines: 7 non-equal opcodes (3 `replace`, 4 `insert`), DELETE COUNT 0.**
  Opcode by opcode:
  (1) `replace` a[916:921] → b[916:922], 5 lines for 6 — SPEC N, the docstring
  paragraph that claimed NO CALLER EXISTS YET, replaced by the truth. Nothing else
  in that docstring moved.
  (2) `replace` a[3275:3277] → b[3276:3283], 2 lines for 7 — SPEC M step 1,
  BUILDER: the two lines that opened `compose_builder_prompt(` become the hoist
  comment plus `builder_compose_args = dict(`. A `replace` here is expected: step 1
  is a hoist.
  (3) `insert` a[3287:3287] → b[3293:3296], 3 lines — SPEC M step 1, BUILDER: the
  dict's closing paren, then the call re-opened as `compose_builder_prompt(` with
  `effective_goal, context, **builder_compose_args,` exactly as the block spells
  it. The `dedupe_sent_hashes=(...)` expression and its five-line scope-rule
  comment sit in an `equal` opcode — they were NOT touched.
  (4) `insert` a[3363:3363] → b[3372:3384], 12 lines — SPEC M step 2, BUILDER: the
  ten-line comment plus the two recomposition statements, as the FIRST statements
  inside `if builder_resume_ref and builder_out.error:` and before
  `_begin_stream_call`.
  (5) `replace` a[3562:3565] → b[3583:3588], 3 lines for 5 — SPEC M step 1,
  REVIEWER: the three lines that opened `compose_reviewer_prompt(` (its two
  POSITIONAL arguments are on their own lines, unlike the builder's) become the
  comment plus `reviewer_compose_args = dict(`.
  (6) `insert` a[3578:3578] → b[3601:3606], 5 lines — SPEC M step 1, REVIEWER: the
  dict close, the call re-opened, the two positionals restored on their own lines,
  and `**reviewer_compose_args,`.
  (7) `insert` a[3672:3672] → b[3700:3715], 15 lines — SPEC M step 2, REVIEWER:
  the comment plus the recomposition and THREE rebindings (see deviation 1).
  **C4, `1b7759b7 -> 54f8ffa9`, `tests/orchestration/test_semantic_dedupe.py`,
  1357 → 1557 lines: 3 non-equal opcodes (2 `insert`, 1 `replace`), DELETE COUNT
  0.** (1) `insert` a[594:594] → b[594:595], 1 line — the
  `reviewer_resume_fails: bool = False,` parameter that SPEC O case 2 explicitly
  authorises adding to `_provider_pair`; (2) `replace` a[611:612] → b[612:613], 1
  line for 1 — forwarding `resume_fails=reviewer_resume_fails` to the reviewer
  `FakeProvider`, the other half of that same authorised extension (see deviation
  2); (3) `insert` a[1357:1357] → b[1358:1557], 199 lines — SPEC O cases 1–4
  appended as ONE contiguous suffix at the END of the file. NO import statement
  needed extending this round, and no existing test, assertion, constant, fixture
  or comment was edited, reordered or deleted. Aggregate DELETE COUNT across both
  comparisons: **0**.
- **G5 THE COLOUR OF THE REPAIR — PASS. Control green; MUTATION A red WITH SPEC O
  case 1 in the failure set; MUTATION B red WITH SPEC O case 1's assertion (c) as
  the failing assertion.** Run in a disposable worktree added at the C4 commit
  `54f8ffa9` BY EXACT PATH
  `/home/decodeux/Repos/remedy/.remedy-wt/g5-f109-r8`, never in the primary
  checkout. FIRST, BEFORE ANY MUTATION WAS TRUSTED, with the worktree as cwd:
  `python3 -B -c "import packages.orchestration.pingpong_loop as m;
  print(m.__file__)"` printed
  `/home/decodeux/Repos/remedy/.remedy-wt/g5-f109-r8/packages/orchestration/pingpong_loop.py`
  — INSIDE the worktree, so no editable install shadowed it. `__pycache__` was
  checked before EVERY run and **0** directories existed each time (a fresh
  worktree carries none and `python3 -B` writes none). The command each time was
  the block's exact one, `python3 -B -m pytest
  tests/orchestration/test_semantic_dedupe.py -q`.
  (a) CONTROL, unmutated: **exit 0, 109 passed**.
  (b) MUTATION A — the two recomposition statements SPEC M step 2 adds to the
  BUILDER fallback branch, deleted, restoring exactly the behaviour `R-0771`
  describes. UNIQUENESS: the sub-string `builder_prompt = builder_composed.text`
  occurs **2** times and `builder_composed = compose_builder_prompt(` occurs **2**
  times, so I took the LONGER unique text — both statements together with their
  16-space fallback indentation — which occurs **1** time; the script refuses to
  edit unless that count is exactly 1. Result: **exit 1, 2 failed, 107 passed —
  RED.** The failure set INCLUDES SPEC O case 1,
  `test_a_builder_resume_fallback_sends_full_content`, failing at assertion (b) on
  a `resume=None` call carrying `[unchanged: `. The second failure is SPEC O case
  3, `test_the_recorded_builder_row_describes_the_bytes_that_were_sent`, failing on
  `_sha256_of_marker('builder_system')` being present in the recorded evidence row
  — the manifest half of the same defect. Wider than ordered, and reported.
  (c) MUTATION B — file restored from the C4 blob by exact path
  (`git -C … checkout 54f8ffa9 -- packages/orchestration/pingpong_loop.py`,
  `git status --porcelain` EMPTY afterwards), then the `dedupe_sent_hashes` keyword
  deleted from the BUILDER `compose_builder_prompt(` call. UNIQUENESS: the short
  text `dedupe_sent_hashes=(` occurs **2** times (builder and reviewer), so I took
  the longer unique three-line block naming `builder_resume_ref`, occurrences
  **1**, and took the BUILDER one. Result: **exit 1, 3 failed, 106 passed — RED.**
  The failure set INCLUDES SPEC O case 1, and I confirmed WHICH assertion by
  re-running that node alone: it fails at **assertion (c)**,
  `assert [p for p in resumed if DEDUPE_MARKER_PREFIX in p] != []`, with the
  resumed prompt list `[1110]` and no marker in any of them — which is exactly
  what proves case 1 cannot pass by dedupe simply being switched off. The two
  extra failures are SPEC O case 3 and SPEC O case 4, both of which also require
  dedupe to fire; wider than ordered, and reported.
  No test was edited in any direction to produce a colour. CLEANUP: after the
  final restore `git -C … status --porcelain` was EMPTY inside the worktree, then
  `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/g5-f109-r8` and
  `git worktree prune`. `git worktree list` afterwards shows the primary checkout
  plus exactly the four pre-existing `.remedy-wt/job-*` worktrees
  (`job-48a379ab5ca44ec5`, `job-7d1c93e2dc98415a`, `job-98e9364a83a34872`,
  `job-f76686b8435640e9`), which predate this branch and were left untouched. My
  shell was never left inside the removed worktree.
- **G6 THE SUITES — PASS.** Run SERIALLY, never two pytest processes alive at
  once, in the primary checkout at the C4 commit, every one exit 0 (mine first,
  then the block's base count in brackets):
  `tests/orchestration/test_semantic_dedupe.py` **109** [105] — the only one that
  moved, and only upward, by the 4 new SPEC O cases;
  `tests/orchestration/test_prompt_segments.py` **25** [25];
  `tests/orchestration/test_builder_prompt_golden.py` **36** [36];
  `tests/orchestration/test_reviewer_prompt_golden.py` **39** [39];
  `tests/orchestration/test_builder_prompt_quality.py` **14** [14];
  `tests/orchestration/test_pingpong.py` **34** [34];
  `tests/orchestration/test_session_resume.py` **27** [27];
  `tests/cli/test_golden_path.py` **42** [42]. EVERY OTHER COUNT IS IDENTICAL to
  the base. The two prompt goldens matter most this round, because SPEC M step 1
  is a pure refactor of the very call they cover: both sit EXACTLY at 36 and 39,
  so the composed bytes did not move.
- **G7 THE TREE — PASS.** `git status --porcelain` is EMPTY (no output).
  `git ls-files .remedy-wt` returns NOTHING. Insertion counts before C5, the `+`
  column only, taken from `git show --numstat` and from nothing else: C0a **381**,
  C0b **249**, C1 **14**, C2 **5 + 3 = 8**, C3 **53**, C4 **3 + 201 = 204**. Every
  one is under 500. I COMPARED those numbers CELL BY CELL against the `+` column
  of the `## Commits this round` table above and they agree; no before/after line
  count of a rewritten file was substituted for a numstat column anywhere. The
  full `git diff --numstat
  81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9..54f8ffa9` lists exactly seven paths
  and nothing else: `.agent/authored/f109-r8.md` 381/0, `.agent/last_block.md`
  249/225, `.agent/live_review.md` 7/1, `.agent/plan.md` 14/11,
  `.agent/prose_slips.md` 3/1, `packages/orchestration/pingpong_loop.py` 53/10 and
  `tests/orchestration/test_semantic_dedupe.py` 201/1. Constraint 9 puts every
  gate at C4 or earlier, so this range stops at C4; C5 adds the eighth ordered
  path, `.agent/handoff.md`, whose count the reviewer measures.

## Item status

| Item | Status | Reason                                                                |
|------|--------|-----------------------------------------------------------------------|
| C0a  | done   |                                                                       |
| C0b  | done   |                                                                       |
| C1   | done   |                                                                       |
| C2   | done   | registered `R-0771` BEFORE the fix existed, per constraint 3          |
| C3   | done   | SPEC M both roles + SPEC N; reviewer needed a third rebinding, dev. 1 |
| C4   | done   | all four SPEC O cases landed; `_provider_pair` extended, dev. 2       |
| C5   | done   | this file                                                             |

## What C3 actually landed

SPEC M STEP 1, BOTH ROLES — a pure refactor, and the prompt goldens are what
prove the composed bytes did not move. `builder_compose_args` holds the ten
keyword arguments of the builder call; `reviewer_compose_args` holds the thirteen
of the reviewer call. `dedupe_sent_hashes` stayed at BOTH call sites, unchanged,
with its five-line scope-rule comment untouched — it is the one argument the two
compositions must differ in.

THE HAZARD THE BLOCK WARNED ABOUT WAS REAL AND WAS AVOIDED. The two call sites do
NOT lay out their positional arguments the same way: the builder passes
`effective_goal, context,` on ONE line, the reviewer passes `effective_goal,` and
`builder_out.summary,` on TWO. I read each call site to find its own
positional/keyword boundary rather than applying one textual operation twice, so
`builder_out.summary,` never entered a `dict(...)`. The `ValueError: dictionary
update sequence element #0 has length 1; 2 is required` the block predicts never
occurred, and the four suites that drive the real loop
(`test_semantic_dedupe`, `test_pingpong`, `test_session_resume`,
`tests/cli/test_golden_path`) would have caught it at run time if it had.

SPEC M STEP 2, BOTH ROLES — as the FIRST statements inside `if <role>_resume_ref
and <role>_out.error:`, before `_begin_stream_call` and before the retry, the
prompt is recomposed with NO dedupe argument and the composed object is rebound.
Each carries a comment naming F109 T002b and `R-0771` and saying the three things
the block requires: a fallback is not a resumed session so the scope rule forbids
dedupe on it; the prompt is recomposed at full content because the fresh session
never received the originals; and `<role>_composed` is rebound too so the manifest
recorded below describes what was actually sent.

SPEC N — the `_dedupe_resumed_segments` docstring paragraph now reads "BOTH
CALLERS EXIST, and have since `60343048`", names both compose functions, says
each calls it behind a `dedupe_sent_hashes` parameter that BYPASSES DEDUPE BY
DEFAULT, and states that what remains absent is the config plumbing that supplies
`enabled`, which is T002c. Nothing else in that docstring changed — G4 opcode (1)
is the whole of it.

I DID NOT TOUCH `invalidate_on_resume_fallback`, `record_finalized_call`,
`_finalize_call`, the retry machinery, or either compose function's body, exactly
as constraint 5 requires; G4's opcode list is the evidence, and every opcode sits
either in the docstring at line 916 or inside the two call sites and the two
fallback branches.

I RAN THE SHIPPED CODE, NOT JUST READ IT. Before writing a single test I drove
the real loop three times against `FakeProvider` and captured every provider call
with its `resume` argument. Builder-resume-fails: three builder calls —
`resume=None` clean (561 chars), `resume='sess-builder'` WITH a marker (808), and
`resume=None` again at **1110 chars and NO marker**, which is the repair.
Reviewer-resume-fails: three reviewer calls, the third `resume=None` at 1898
chars with no marker. Clean resumed chain: two calls per role, the resumed one
marked, the fresh one not. All three runs ended `staged_review_passed`.

## What C4 actually landed

201 insertions, 1 deletion. One new module-level constant
(`DEDUPE_MARKER_PREFIX`), one module-level helper (`_capture_role_calls`), one
module-level fixture (`fallback_repo`) and one new class
(`TestAResumeFallbackSendsFullContent`) with four cases, at the END of the file.
109 tests total, up from 105.

SPEC O CASE 1 — `test_a_builder_resume_fallback_sends_full_content`. Drives the
real loop with `_provider_pair(builder_resume_fails=True)` and `repair_rounds=2`,
exactly as `test_a_failed_builder_resume_falls_back_within_the_same_round` does.
`_capture_role_calls` WRAPS `provider.build` and delegates to the bound original,
so the real call still happens and the real run completes; each entry is
`(resume, prompt)`. (a) `final_status == "staged_review_passed"` and
`rounds[1].builder_output.resume_fallback is True`, so the case is known to have
exercised the fallback. (b) no `resume=None` call carries `[unchanged: `.
(c) at least one non-None-`resume` call DOES carry it. G5 mutation B is what
shows (c) is load-bearing rather than decoration.

SPEC O CASE 2 — `test_a_reviewer_resume_fallback_sends_full_content`, the same
three assertions on the reviewer side. `_provider_pair` did NOT expose a reviewer
equivalent of `builder_resume_fails`, so I EXTENDED it with
`reviewer_resume_fails: bool = False` exactly as SPEC O case 2 authorises — an
addition that breaks no existing caller; every existing call site omits it and
`FakeProvider.review` already honoured `resume_fails`. The case-2 escape hatch
("leave this case out") was NOT used and case 1 was NOT weakened.

SPEC O CASE 3 — `test_the_recorded_builder_row_describes_the_bytes_that_were_sent`.
HOW THE CORRESPONDENCE WAS ESTABLISHED, stated in the case's own comment and
repeated here because the block asks for it plainly: the evidence row carries
sha256 values ALONE — no names, no text — and a hash cannot be inverted back into
a substring of the prompt, so "every recorded sha256 corresponds to a segment of
the prompt that was actually sent last" is NOT decidable from outside the loop
and the case does not claim it. THE WEAKER, HONEST FORM I WROTE INSTEAD: a
marker's text follows from its name alone, so its hash is computable via the
shipped producer (`_sha256_of_marker`); the round-2 builder TRACE records the
manifest of the composition the fallback ABANDONED, so the names it replaced are
readable; and the round-1 trace records those same names at FULL content. The
case asserts, for every name the abandoned composition replaced, that the
recorded row holds the FULL-content hash and NOT the marker hash — plus that the
last call this session received opened a fresh session and carried no marker.
That is a statement about the segments the defect touched, which is narrower than
the sentence SPEC O uses, and it is written that way on purpose. It is not
vacuous: it carries its own positive control (`assert replaced`) and it is one of
the two cases G5 mutation A reddens.

SPEC O CASE 4 — `test_a_resumed_chain_that_never_falls_back_still_dedupes`. Round
7's property, re-read off the CALLS rather than the traces: neither role falls
back, every role still carries a marker on its resumed call, and no call that
opened a session carries one. It reuses `TestChainAgainstTheRealLoop._make_repo`,
`._provider_pair`, `._run` and `._rows_by_session` rather than building a second
fixture stack, per constraint 6.

Ruff followed BY CONSTRUCTION per constraint 7, which forbids gating on it and on
`npm run lint`: the longest line in the WHOLE of `pingpong_loop.py` after C3 is
**119** and in `test_semantic_dedupe.py` after C4 is **102**, both under the
configured 120; no line in either file has trailing whitespace; both files parse
with `ast`. NO import statement was added or changed in EITHER file this round,
so the isort clause of constraint 7 had nothing to bind.

## Deviations

1. **SPEC M NAMES TWO REBINDINGS; THE REVIEWER SIDE NEEDS THREE, AND I MADE THE
   THIRD.** SPEC M step 2 orders `<role>_composed` and `<role>_prompt` rebound.
   That is complete for the builder, whose retry sends `builder_prompt`. It is
   NOT complete for the reviewer: at
   `packages/orchestration/pingpong_loop.py` the reviewer computes
   `reviewer_effective = _reviewer_effective_prompt(reviewer_prompt)` BEFORE the
   call, and both the retry (`reviewer_provider.review(reviewer_effective, …)`)
   and `_finalize_call(…, fallback_prompt=reviewer_effective)` use that name, not
   `reviewer_prompt`. Rebinding only the two named names would have left the
   marker in the bytes the reviewer actually receives and repaired nothing on that
   role. I therefore added `reviewer_effective = _reviewer_effective_prompt(
   reviewer_prompt)` as the third statement of that branch, on the authority of
   SPEC M's own stated purpose — "one rebinding each makes the sent bytes, the
   stored prompt and the recorded evidence agree". MEASURED, not argued: with the
   third rebinding the reviewer's `resume=None` fallback call is 1898 chars and
   marker-free; SPEC O case 2 is what pins it. This is G4 opcode (7) on the C3
   comparison and it is the only line in this round that goes beyond SPEC M's
   literal wording. Trivially reversible if the reviewer disagrees — at the cost
   of case 2 going red.
2. **SPEC O CASE 2 AND CONSTRAINT 6 DISAGREE ABOUT `_provider_pair`, AND I
   FOLLOWED SPEC O.** Constraint 6 says nothing already present in the test file
   is edited "with ONE named exception: the existing import statements may be
   EXTENDED". SPEC O case 2, in the same block, orders exactly the edit constraint
   6 does not list: "EXTEND that helper with a `reviewer_resume_fails` parameter
   defaulting to False, which is an addition and breaks no existing caller." I
   took the specific instruction over the general one, because it names the
   helper, names the parameter, names its default and states the safety argument.
   The cost is two G4 opcodes on the test file — one `insert` of the parameter
   line, one `replace` of the `FakeProvider(` reviewer construction to forward it
   — and no import statement needed extending, so the exception constraint 6 DOES
   grant went unused. No existing caller passes the new parameter; every existing
   case behaves identically, which G6's `109 [105]` with 105 unchanged cases
   confirms.
3. **BOTH G5 MUTATIONS FAILED WIDER THAN THE ONE NAMED CASE.** Mutation A: 2
   failures where 1 was named (case 1 named, case 3 extra). Mutation B: 3 where 1
   was named (case 1 named, cases 3 and 4 extra). The block permits a wider red
   and asks that it be reported. Neither extra is collateral in the bad sense:
   case 3 reads the recorded manifest, which is the second half of the same
   defect, and case 4 requires dedupe to fire at all, which mutation B removes.
   No case was weakened and no colour was manufactured.
4. **NO `Done:` PARAGRAPH WAS WRITTEN, though the finding and its fix landed in
   the same round.** Constraint 4 and
   docs/agents/planner_reviewer_prompt.md §4 item 4 reserve that text for the
   reviewer at the next gate. SLICE P's `Landed:` line is the only resolution
   marker this round carries, and G3(d) measures `grep -c '^Done: R-[0-9]\{4\} —
   '` UNCHANGED at 63 to prove it.
5. **The sandbox bash guard refused several command FORMS**, not contents: a
   compound command ending in `echo "exit=$?"`, and an `awk` one-liner over the
   source file. Neither was a gate; the exit codes were read from the tool's own
   non-zero reporting instead (which is how G3(c)'s `exit 1` and G5's `exit 1`
   were recorded), and the line-length scan was done in Python. Every `cmp`,
   `wc -l`, `grep -c`, `sha256sum`, `git show --numstat`, `git status
   --porcelain`, `git ls-files`, `git worktree` and `python3 -B -m pytest` command
   the block names was run VERBATIM. No gate was weakened, reworded or narrowed
   to fit the guard.
6. **Scratch artefacts lived under `.remedy-wt/` and are gitignored**, never
   committed and never in the change set. Every one I created was deleted BY
   EXACT PATH after it had served: `extract_slice.py`, `append_slices.py`,
   `g3b_reader.py`, `g3c_negctl.py`, `g3_prefix.py`, `g4_opcodes.py`,
   `g5_mutate.py`, `probe_r8.py`, `slice_plan.txt`, `slice_record.txt`,
   `slice_finding.txt`, `slice_slip.txt`, `slice_p.txt` and, earlier,
   `live_review_negctl.md`. Nothing was removed by glob. The block file
   `.remedy-wt/f109-r8.md` supplied by the delegation was left in place.
   `git ls-files .remedy-wt` returns nothing, as G7 records.
7. **Four `.remedy-wt/job-*` worktrees predate this branch** and were left alone.
   Exactly one worktree was created this round, `.remedy-wt/g5-f109-r8`, and it
   was removed by exact path and then pruned.
8. **No `docs/` file was touched.** The change set forbids it and T003 owns the
   docs for this feature.
9. **The prompt TRACE ordering is still wrong on a builder fallback and I did NOT
   fix it.** `build_trace_entry` is called BEFORE the provider call, so the
   builder's round-2 trace still describes the abandoned resumed composition
   rather than the full one that was sent. The reviewer's traces do not have this
   problem, because `_rev_trace` fires per actual call and I rebound
   `reviewer_effective` before it. Out of scope — it changes neither the bytes
   sent nor the recorded manifest, both of which this round repaired — and it is
   already written into `.agent/plan.md`'s Risks section for T002c. SPEC O case 1
   is deliberately written against the CALLS, not the traces, for exactly this
   reason.

## Open findings

The ledger stands at **332** findings registered and **63** resolved, so the open
set is **269** — registered up by exactly 1 (`R-0771`), resolved UNCHANGED,
because this round writes a `Landed:` line and no `Done:` paragraph.
`.agent/candidates.md` is unchanged and states "EMPTY — no candidate is open.",
so no block condition stands against F109. `R-0769` remains registered and
unfixed; its repair edits `README.md` and a docs test, neither of which F109
owns. `R-0771` is registered AND repaired in this same round, and its
`Landed:` line is booked; the `Done:` text is the reviewer's to author at the next
gate. `.agent/prose_slips.md` gained round 7's one line and now holds **66**
dated lines. `.agent/STOP` was checked before the first action of the round and
again before this handback, and does not exist.

ONE ITEM ABOVE IS A CANDIDATE FOR AN R-ID AND ONLY THE REVIEWER MAY MINT ONE:
deviation 9, the prompt-trace ordering on a builder fallback. It is recorded in
`.agent/plan.md` as a Risk, not as a finding, because I may not mint ids.

## Next expected action

`git push origin feature/f109-semantic-dedupe` immediately after this commit —
not quoted here by design, so the reviewer measures the remote tip itself. No PR
was created and nothing was merged.

Then the reviewer's round-8 verdict, booked into `.agent/live_review.md` in the
FIRST commit of round 9 (amend0827 rule 1: a verdict never buys a round of its
own), together with the `Done:` paragraph for `R-0771` that constraint 4 reserves
for the reviewer. Before authoring round 9 the reviewer re-reads `.agent/STOP`
from disk (Phase 1 rule 1 before rule 2). The build then continues with T002c:
record the deduped segments in the manifest so evidence shows what the model did
NOT receive again, and plumb the config kill switch through to `dedupe_enabled`;
deviation 9's trace ordering belongs with that evidence work.
