# Handoff — F109 Semantic dedupe, SESSION 2, round 7

Branch: `feature/f109-semantic-dedupe`
Base commit: `7ab865280a44e1078feb320f5508cd1901cbb27d` (round 6 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

THIS ROUND BOOKED ROUND 6'S PASS VERDICT and its one reviewer-prose slip, then
landed the SECOND HALF of T002b: `compose_builder_prompt` and
`compose_reviewer_prompt` each gained the keyword-only pair
`dedupe_sent_hashes` / `dedupe_enabled`, and the two `run_pingpong` call sites
supply the session's sent hashes ONLY when a resume ref is actually set. THE
SAFETY PROPERTY IS THAT THE DEFAULT BYPASSES: `dedupe_sent_hashes=None` does not
call the transform at all, so every existing caller composes byte-identical
bytes. `test_builder_prompt_golden.py` (36) and `test_reviewer_prompt_golden.py`
(39) both sit EXACTLY at their base counts, which is the evidence for that claim
rather than decoration beside it.

READ DEVIATION 1 FIRST: the ordered G5 MUTATION B is an EQUIVALENT MUTANT and
came back GREEN. It is reported as green, a substitute discriminator was run in
addition, and SPEC L case 6 was NOT weakened to manufacture a colour.

## Commits this round

| Item | SHA        | Commit subject                                                                        |   +   |   -   |
|------|------------|---------------------------------------------------------------------------------------|-------|-------|
| C0a  | `b8407db4` | F109 R7 C0a: save the round 7 step block verbatim                                     |  357  |   0   |
| C0b  | `9ef933d7` | F109 R7 C0b: mirror the round 7 block to last_block                                   |  261  |  259  |
| C1   | `502a8ffd` | F109 R7 C1: plan for round 7 — book round 6, wire the dedupe into both compose functions |   16  |   20  |
| C2   | `637628a5` | F109 R7 C2: book the round 6 gate and its one reviewer-prose slip                     |    6  |    2  |
| C3   | `60343048` | F109 R7 C3: both compose functions take the dedupe hashes, bypassing by default        |   46  |    2  |
| C4   | `2e0398fd` | F109 R7 C4: the loop supplies the sent hashes only when a resume ref is set             |   16  |    0  |
| C5   | `bb694018` | F109 R7 C5: pin the bypass golden and the scope rule at both call sites                |  267  |    1  |

Every `+` and `-` cell above was read from `git show --numstat` for that exact
SHA and COMPARED CELL BY CELL against the numstat output quoted under G7 — I
state plainly that I did that comparison. The `+` column only, per AGENTS.md
DECISION F104 D1, never insertions plus deletions, and never a before/after line
count of a rewritten file. C2 touches two files (3+1 and 3+1), so its cells are
the file-summed 6 and 2.

C6 is this handoff rewrite, committed on top of `bb694018`. Every gate G1–G7 ran
at C5 or earlier, so every reading quoted below already existed when this file
was written; C6's own insertion count is deliberately NOT quoted anywhere here,
because the reviewer measures that one. Seven single-parent commits in the range
before C6, no merge commit. The push happens AFTER C6, so the remote tip is not
quoted either.

## Changed files (this round)

| Path                                           | Change                                                       |
|------------------------------------------------|--------------------------------------------------------------|
| `.agent/authored/f109-r7.md`                   | new — step block, `cp` not retyped                           |
| `.agent/last_block.md`                         | rewritten — byte mirror of the authored block                |
| `.agent/plan.md`                               | rewritten — SLICE PLAN, whole file, 44 lines                 |
| `.agent/live_review.md`                        | appended ONCE — SLICE RECORD, one paragraph, at C2           |
| `.agent/prose_slips.md`                        | appended ONCE — SLICE SLIP, one paragraph, at C2             |
| `packages/orchestration/pingpong_loop.py`      | 2 signatures extended, 2 returns replaced, 2 call sites      |
| `tests/orchestration/test_semantic_dedupe.py`  | 1 import extended, 1 new class appended, no test changed     |
| `.agent/handoff.md`                            | rewritten — this file (C6)                                   |

No path outside the ordered change set was touched. `git diff --numstat` over
`7ab86528..bb694018` lists exactly those seven paths (C6 adds the eighth).

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum .agent/authored/f109-r7.md
  .agent/last_block.md` printed ONE digest twice:
  **`711f3a135f35671111975c4ec48456258156811389c6b7364e9e2db574573954`**, equal
  to each other AND to the `SHA256_OF_THIS_BLOCK` the delegation wrapper stated.
  The scratch original `.remedy-wt/f109-r7.md` was verified against that digest
  as this round's FIRST action, before anything else was read or written, and it
  printed the same digest a third time; C0a and C0b were both `cp` from it, never
  a retype. STATED PLAINLY, AS THE BLOCK REQUIRES: this chain compares THE SAVED
  COPY AGAINST ITS MIRROR and claims nothing about the bytes that were emitted.
- **G2 THE PLAN — PASS.** The SLICE PLAN was extracted MECHANICALLY from
  `.agent/authored/f109-r7.md` by a script that locates the `<<<SLICE PLAN` and
  `SLICE PLAN` delimiter lines and takes the lines strictly between them; `cmp
  .agent/plan.md .remedy-wt/f109-r7-plan-verify.txt` produced NO OUTPUT and exit
  0, re-run against a freshly re-extracted copy AFTER the commit. `wc -l
  .agent/plan.md` = **44**, strictly under 50. `grep -c '^## Goal'` = **1** and
  `grep -c '^## Next Steps'` = **1**. The verify copy was deleted BY EXACT PATH.
- **G3 THE TWO APPENDS — PASS, all five parts.**
  (a) `.agent/live_review.md` BYTE ARITHMETIC: base **2045983** bytes, base
  sha256 `866a63baab2d7fe6d12319a37111a588d477c7756cbd7a1e26f2a54d206cbe92`,
  confirmed BY BYTE TEST to end WITHOUT a trailing newline. S = **4797** after
  stripping the extracted slice's trailing newline. Expected 2045983 + 2 + 4797 =
  **2050782**; actual new size **2050782** — MATCH. The file still ends WITHOUT a
  trailing newline. New sha256
  `4720fe79346a513edd6854b5e8325b4ba665754b1b1aa0a27e1df37be5c43b6a`.
  (b) A SECOND, STRUCTURALLY DIFFERENT READER: the whole file was split on
  blank-line boundaries into units. The script COUNTED the units of the SLICE
  RECORD itself rather than taking the number from the block — **N = 1**, because
  the record is one paragraph — and asserted the LAST 1 unit equals the slice's
  paragraph IN ORDER: **True**.
  (c) NEGATIVE CONTROL on a scratch copy `.remedy-wt/f109-r7-lr-scratch.md`,
  never on the tracked file: the byte at offset **2048383**, which the script
  located as the MIDPOINT of the first appended paragraph rather than by
  arithmetic on the block's own numbers, was XOR-flipped with 0x20; reader (b)
  **REJECTED** the result (`accepts=False`). The tracked file's sha256 was
  `4720fe79346a513edd6854b5e8325b4ba665754b1b1aa0a27e1df37be5c43b6a` BEFORE and
  `4720fe79346a513edd6854b5e8325b4ba665754b1b1aa0a27e1df37be5c43b6a` AFTER —
  identical, so the tracked file did not move. The scratch copy was deleted BY
  EXACT PATH.
  (d) COUNTS in `.agent/live_review.md`, each measured at the base commit through
  `git show 7ab86528:.agent/live_review.md` and again on the working file:
  `grep -c '^Gate: F109 R6 — '` is **1** (it was **0** at the base commit).
  `grep -c '^- R-[0-9]\{4\} — '` is **331**, UNCHANGED from 331.
  `grep -c '^Done: R-[0-9]\{4\} — '` is **63**, UNCHANGED from 63.
  `grep -c '^Landed: R-'` is **25**, UNCHANGED from 25. NO FINDING WAS REGISTERED
  OR RESOLVED THIS ROUND.
  (e) `.agent/prose_slips.md`: base **42621** bytes, new **43860**; the base bytes
  are a BYTE-EXACT PREFIX of the new file (**True**); the new file still ends
  WITHOUT a trailing newline (**True**); lines matching `^2026-` went **64 → 65**,
  a rise of exactly **1**. Reader (b) also passed over this file with N = 1.
- **G4 THE EDIT SHAPE IS THE ORDERED ONE — RUN IN FULL; EVERY NON-EQUAL OPCODE
  IS ACCOUNTED FOR, WITH ONE DECLARED READING (deviation 2).** Both revisions of
  every file were read as BLOBS with `git show <sha>:<path>` — neither revision
  was ever written over the tracked file — split into lines and compared with
  `difflib.SequenceMatcher(None, pre, post, autojunk=False)`.
  **C3, `637628a5 -> 60343048`, `packages/orchestration/pingpong_loop.py`, 5078 →
  5122 lines: 6 non-equal opcodes, DELETE COUNT 0.** Opcode by opcode:
  (1) `insert` a[958:958] → b[958:960], 2 lines — the BUILDER parameter addition,
  constraint 4(a);
  (2) `insert` a[994:994] → b[996:1006], 10 lines — the BUILDER docstring
  paragraph documenting those two parameters, which SPEC J orders in the same
  breath as the parameters themselves ("Document both parameters in each
  function's docstring"); I account it to constraint 4(a), see deviation 2;
  (3) `replace` a[1113:1114] → b[1125:1136], 1 line for 11 — the BUILDER return
  replacement, constraint 4(b), and the removed line is exactly
  `    return compose_prompt_segments(registry.registered_segments())`;
  (4) `insert` a[1497:1497] → b[1519:1521], 2 lines — the REVIEWER parameter
  addition, constraint 4(a);
  (5) `insert` a[1505:1505] → b[1529:1539], 10 lines — the REVIEWER docstring
  paragraph, same reading as (2);
  (6) `replace` a[1641:1642] → b[1675:1686], 1 line for 11 — the REVIEWER return
  replacement, constraint 4(b), removing the same one line.
  **C4, `60343048 -> 2e0398fd`, same file, 5122 → 5138 lines: 2 non-equal
  opcodes, DELETE COUNT 0.** (1) `insert` a[3287:3287] → b[3287:3295], 8 lines —
  the BUILDER call-site keyword plus its scope-rule comment, constraint 4(c);
  (2) `insert` a[3570:3570] → b[3578:3586], 8 lines — the REVIEWER call-site
  keyword plus its comment, constraint 4(c). NOTHING ELSE.
  **C5, `2e0398fd -> bb694018`, `tests/orchestration/test_semantic_dedupe.py`,
  1091 → 1357 lines: 2 non-equal opcodes, DELETE COUNT 0.** (1) `replace`
  a[23:24] → b[23:30], 1 line for 7 — EXACTLY the import extension constraint 6
  names, `from packages.orchestration.pingpong_loop import
  _dedupe_resumed_segments, run_pingpong` becoming the parenthesised list
  `ReviewFinding, _dedupe_resumed_segments, compose_builder_prompt,
  compose_reviewer_prompt, run_pingpong`; (2) `insert` a[1091:1091] →
  b[1097:1357], 260 lines appended as ONE contiguous suffix after the last
  existing class — the test append constraint 6 names. So NO existing function,
  test, assertion, constant or comment in either file was edited, reordered or
  deleted, and the aggregate DELETE COUNT across all three comparisons is **0**.
- **G5 THE COLOUR OF THE WIRING — CONTROL GREEN, MUTATIONS A AND C RED ON THEIR
  NAMED CASES, MUTATION B GREEN AND SHOWN TO BE AN EQUIVALENT MUTANT (deviation
  1); a substitute discriminator B′ reddens SPEC L case 6 alone.** Run in a
  disposable worktree added at the C5 commit `bb694018` BY EXACT PATH
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r7-g5-wt`, never in the primary
  checkout. FIRST, BEFORE ANY MUTATION WAS TRUSTED, with the worktree as cwd:
  `python3 -B -c "import packages.orchestration.pingpong_loop as m;
  print(m.__file__)"` printed
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r7-g5-wt/packages/orchestration/pingpong_loop.py`
  — INSIDE the worktree, so no editable install shadowed it. `__pycache__` was
  purged before EVERY run (**0** directories found each time — a fresh worktree
  carries none and `python3 -B` writes none) and the command each time was the
  block's exact one, `python3 -B -m pytest
  tests/orchestration/test_semantic_dedupe.py -q`.
  (a) CONTROL, unmutated: **exit 0, 105 passed**. Re-run after the last restore:
  **exit 0, 105 passed** again.
  (b) MUTATION A — the `is not None` guard removed so the transform runs
  unconditionally (`if dedupe_sent_hashes is not None:` → `if True:`). The short
  ordered text occurs **2** times, so I quoted a LONGER UNIQUE ANCHOR — the block
  running from `["\nProvide your changes and a summary of what you did."],`
  through `registry.register(name, rank, text)` down to the `if` line, which
  occurs **1** time — and took the **BUILDER** one. Result: **exit 1, 21 failed,
  84 passed — RED.** The failure set INCLUDES SPEC L golden cases 1 and 3:
  `test_the_builder_default_and_an_explicit_none_compose_the_same_bytes[0]`,
  `[1]`, `[2]` and
  `test_an_empty_sent_set_runs_the_transform_and_still_composes_the_same_bytes[0]`,
  `[1]`, `[2]`. So the golden CAN fail. The red is wide because the unguarded
  call passes `None` into `should_dedupe_segment`, which raises `TypeError` at
  `session_sent_index.py:322`, taking the ten pre-existing
  `TestChainAgainstTheRealLoop` loop cases with it — reported, not hidden.
  (c) MUTATION B — restored, then the BUILDER call site's conditional dropped for
  `session_sent_index.sent_hashes(builder_resume_ref or "")`. Anchor occurrences:
  the short text `dedupe_sent_hashes=(` occurs **2** times, so I took the longer
  unique three-line anchor naming `builder_resume_ref`, which occurs **1** time.
  Result: **exit 0, 105 passed — GREEN, i.e. the gate's ordered mutation did NOT
  redden SPEC L case 6.** This is an EQUIVALENT MUTANT and I measured why rather
  than arguing it: run inside the mutated worktree,
  `SessionSentIndex.record_call("", rows, ok=True)` returns **0** (a named session
  returns 1), so `sent_hashes("")` is **`frozenset()`** for every possible run;
  and `compose_builder_prompt(..., dedupe_sent_hashes=None).text ==
  compose_builder_prompt(..., dedupe_sent_hashes=frozenset()).text` is **True**.
  The mutant therefore substitutes exactly `frozenset()` for `None` on every
  non-resuming round and changes no composed byte anywhere; on a resuming round
  `builder_resume_ref or ""` IS `builder_resume_ref`, so it is unchanged there
  too. SPEC L case 6 was NOT weakened and no pass was fabricated.
  (c′) SUBSTITUTE DISCRIMINATOR B′, run in addition so case 6 is not left
  unproved — the SAME edit's intent (conditional dropped, scope rule gone)
  expressed with a session key the index can actually hold:
  `dedupe_sent_hashes=session_sent_index.sent_hashes(next(iter(session_sent_index.session_ids()),
  ""))`, same unique anchor, occurrences **1**. Result: **exit 1, 1 failed, 104
  passed — RED, and the single failure IS SPEC L case 6**,
  `test_a_chain_that_never_resumes_composes_no_marker_anywhere`, failing on a
  round-2 builder prompt that now carries `[unchanged: builder_system, previously
  provided]`. Exactly one case, no collateral.
  (d) MUTATION C — restored, then the BUILDER `dedupe_enabled` default flipped to
  `False`. The short text `    dedupe_enabled: bool = True,` occurs **2** times,
  so I took the longer unique anchor spanning `tiered_diff_text` through the
  builder docstring's first line, which occurs **1** time. Result: **exit 1, 2
  failed, 103 passed — RED.** The failure set INCLUDES SPEC L case 4,
  `test_a_second_composition_against_its_own_recorded_manifest_carries_markers`.
  The second failure is SPEC L case 5's own POSITIVE CONTROL — the kill-switch
  case asserts the same input IS deduped under the default before flipping the
  flag, so nothing but the flag differs — which is a discriminator doing its job,
  not collateral.
  No test was edited in any direction to produce a colour. CLEANUP: after the
  final restore `git -C … status --porcelain` was EMPTY inside the worktree, then
  `git worktree remove --force
  /home/decodeux/Repos/remedy/.remedy-wt/f109-r7-g5-wt` and `git worktree prune`.
  `git worktree list` afterwards shows the primary checkout plus exactly the four
  pre-existing `.remedy-wt/job-*` worktrees (`job-48a379ab5ca44ec5`,
  `job-7d1c93e2dc98415a`, `job-98e9364a83a34872`, `job-f76686b8435640e9`), which
  predate this branch and were left untouched.
- **G6 THE SUITES — PASS.** Run SERIALLY, never two pytest processes alive at
  once, in the primary checkout at the C5 commit, every one exit 0 (mine, then
  the block's base count in brackets):
  `tests/orchestration/test_semantic_dedupe.py` **105** [90] — the only one that
  moved, and only upward, by the 15 new cases;
  `tests/orchestration/test_prompt_segments.py` **25** [25];
  `tests/orchestration/test_builder_prompt_golden.py` **36** [36];
  `tests/orchestration/test_reviewer_prompt_golden.py` **39** [39];
  `tests/orchestration/test_builder_prompt_quality.py` **14** [14];
  `tests/orchestration/test_pingpong.py` **34** [34];
  `tests/orchestration/test_session_resume.py` **27** [27];
  `tests/cli/test_golden_path.py` **42** [42]. EVERY OTHER COUNT IS IDENTICAL to
  the base. The two prompt goldens are what prove the default really bypasses:
  `test_builder_prompt_golden.py` pins frozen renders and an exact ten-name
  manifest tuple, and it is green at its base count, so no existing caller's
  bytes moved.
- **G7 THE TREE — PASS.** `git status --porcelain` is EMPTY (no output).
  `git ls-files .remedy-wt` returns NOTHING. Insertion counts before C6, the `+`
  column only, taken from `git show --numstat` and from nothing else: C0a **357**,
  C0b **261**, C1 **16**, C2 **3 + 3 = 6**, C3 **46**, C4 **16**, C5 **267**.
  Every one is under 500. I COMPARED those numbers CELL BY CELL against the `+`
  column of the `## Commits this round` table above and they agree; no
  before/after line count of a rewritten file was substituted for a numstat
  column anywhere. The full `git diff --numstat
  7ab865280a44e1078feb320f5508cd1901cbb27d..bb694018` lists exactly seven paths
  and nothing else: `.agent/authored/f109-r7.md` 357/0, `.agent/last_block.md`
  261/259, `.agent/live_review.md` 3/1, `.agent/plan.md` 16/20,
  `.agent/prose_slips.md` 3/1, `packages/orchestration/pingpong_loop.py` 62/2 and
  `tests/orchestration/test_semantic_dedupe.py` 267/1.

## Item status

| Item | Status | Reason                                                          |
|------|--------|-----------------------------------------------------------------|
| C0a  | done   |                                                                 |
| C0b  | done   |                                                                 |
| C1   | done   |                                                                 |
| C2   | done   |                                                                 |
| C3   | done   | docstring paragraphs added per SPEC J; see deviation 2          |
| C4   | done   |                                                                 |
| C5   | done   | all seven SPEC L cases implemented, including case 7            |
| C6   | done   | this file                                                       |

## What C3 and C4 actually landed

Both compose functions gained, as the LAST two entries of their signature and
immediately before the closing `) -> ComposedPrompt:`, exactly:

    dedupe_sent_hashes: Container[str] | None = None,
    dedupe_enabled: bool = True,

Both are KEYWORD-ONLY by construction — each signature has a bare `*` well
before them — and both carry defaults, so NO SIGNATURE BREAKS: every existing
caller keeps working unchanged. `_build_builder_prompt` and
`_build_reviewer_prompt` were NOT touched, so they pass neither parameter and
therefore bypass, which is the intended behaviour rather than an omission.

Constraint 4's import claim was CONFIRMED BEFORE ANY EDIT and it holds: at the
base commit `Container` is already imported at line 26 (`from collections.abc
import Callable, Container, Sequence`) and `_dedupe_resumed_segments` is defined
in the same module at line 882, above both compose functions. NO IMPORT WAS
ADDED OR CHANGED in `pingpong_loop.py` this round.

The line `return compose_prompt_segments(registry.registered_segments())`
occurred EXACTLY TWICE before the edit — counted with `grep -c`, which printed
**2** — and occurs **0** times after it. Both became the eleven-line block SPEC J
dictates, verbatim including its five-line comment about discarding the replaced
names until T002c needs them.

C4 added ONE keyword argument to each of the two `run_pingpong` call sites,
`builder_composed = compose_builder_prompt(` and `reviewer_composed =
compose_reviewer_prompt(`, each under 120 characters (102 and 104), each with a
comment above it naming F109 T002b and the scope rule. `record_finalized_call`,
`invalidate_on_resume_fallback` and `result.session_sent_evidence` were NOT
touched.

I RAN THE SHIPPED FUNCTIONS, not just read them: a probe drove the real loop
against `FakeProvider` twice before the tests were written. A resumed pair
produced round-2 prompts carrying `[unchanged: builder_system, previously
provided]` and `[unchanged: reviewer_system, previously provided]`; a
`supports_resume=False` pair produced none. Both runs ended
`staged_review_passed`.

## What C5 actually landed

267 insertions, 1 deletion — the deletion is the one import line that was
extended. One new class,
`TestTheComposeSeamBypassesUntilAResumedSessionSaysOtherwise`, at the END of the
file, plus four module-level constants and two module-level helpers. 15 new test
functions, 105 total. Nothing already present was edited, reordered or deleted.

ALL SEVEN SPEC L CASES ARE IMPLEMENTED, INCLUDING CASE 7. The case-7 escape
hatch was NOT used and case 6 was NOT weakened. Mapping:

1. `test_the_builder_default_and_an_explicit_none_compose_the_same_bytes[0..2]`
   over THREE shapes that vary `findings`, `safe_diff`, `round_number`,
   `test_result`, `task_body` and `scope_contract`. It asserts `.text` equality
   AND `.manifest` equality, as ordered. Its discriminator
   `test_the_three_builder_shapes_are_not_the_same_prompt` proves the three
   shapes really compose different prompts, so the golden is not vacuous.
2. `test_the_reviewer_default_and_an_explicit_none_compose_the_same_bytes[0..1]`
   over TWO shapes, with the same manifest assertion and the same discriminator
   (`test_the_two_reviewer_shapes_are_not_the_same_prompt`).
3. `test_an_empty_sent_set_runs_the_transform_and_still_composes_the_same_bytes[0..2]`
   plus `test_an_empty_sent_set_composes_the_same_reviewer_bytes_too` —
   `frozenset()` is not None, so the transform really runs and must still produce
   identical bytes. This is the case that proves the bypass is about the DATA.
4. `test_a_second_composition_against_its_own_recorded_manifest_carries_markers`
   — the sent set is built from the FIRST composition's own
   `manifest_as_dicts()` through a real `SessionSentIndex.record_call(...,
   ok=True)` and `sent_hashes(...)`. It asserts at least one segment's text is
   EXACTLY that segment's marker (via `_sha256_of_marker`, which takes the marker
   digest from the SHIPPED manifest producer rather than adding a second hashing
   expression), that the second composition is STRICTLY shorter, and that the
   manifest's NAMES and RANKS are unchanged between the two compositions.
5. `test_the_kill_switch_composes_the_no_dedupe_bytes_from_the_same_full_set` —
   the positive control runs FIRST on the same full sent set, so nothing but the
   flag differs.
6. `test_a_chain_that_never_resumes_composes_no_marker_anywhere` — drives the
   REAL loop with `TestChainAgainstTheRealLoop._provider_pair(supports_resume=False)`
   and `._run`, reusing that class's provider construction rather than inventing
   another, and asserts over `result.prompt_traces` — THE RUN'S OWN RECORDED
   PROMPTS, not a re-composition. It asserts `prompt_text_truncated is False`
   FIRST, so the absence is only as wide as the recorded text and a 50 000-char
   cap cannot hide a marker.
7. `test_a_resumed_repair_chain_composes_a_marker_and_still_completes` — the same
   helpers with a resuming pair; the run still ends `staged_review_passed`, at
   least one recorded prompt carries `[unchanged: `, and EVERY marked prompt is
   from a round > 1, which pins "resumed session only" from the positive side.

Ruff followed BY CONSTRUCTION per constraint 7, which forbids gating on it and on
`npm run lint`: the longest line in the WHOLE of `pingpong_loop.py` after C4 is
**119** and in `test_semantic_dedupe.py` after C5 is **102**, both under the
configured 120; both files parse with `ast`; the extended import list is in the
repo's `order-by-type` isort order — the class `ReviewFinding` first, then the
four functions alphabetically, `_dedupe_resumed_segments` before
`compose_builder_prompt` before `compose_reviewer_prompt` before `run_pingpong`.

## Deviations

1. **THE ORDERED G5 MUTATION B IS AN EQUIVALENT MUTANT AND CAME BACK GREEN — 105
   passed, exit 0.** It cannot redden SPEC L case 6, or anything else, under any
   construction of that case. Measured, not argued: `SessionSentIndex.record_call`
   refuses an empty session id (`return 0`), so `sent_hashes("")` is ALWAYS
   `frozenset()`; and an empty frozenset composes byte-identical bytes to `None`
   because nothing in an empty container can match a hash. So `sent_hashes(ref or
   "")` differs from `... if ref else None` only in substituting `frozenset()` for
   `None` on non-resuming rounds, which is unobservable. I did NOT weaken case 6,
   did NOT rewrite it to pass a different mutant, and did NOT report a colour I
   did not see. I ran a SUBSTITUTE DISCRIMINATOR B′ in addition — the same edit's
   intent with a session key the index can actually hold — and it reddens SPEC L
   case 6 and ONLY case 6 (1 failed, 104 passed), so case 6 is demonstrably not
   vacuous. If the reviewer wants the ordered mutation to bite, the code would
   have to make an empty set behave differently from None, which is precisely the
   distinction SPEC L case 3 forbids.
2. **SPEC J AND CONSTRAINT 4 DISAGREE ABOUT THE DOCSTRINGS, AND I FOLLOWED SPEC
   J.** Constraint 4 says only three edit kinds are permitted in
   `pingpong_loop.py` and "no other line of that file changes"; SPEC J, in the
   same block, orders "Document both parameters in each function's docstring in
   that file's own style". I read constraint 4(a) as delegating its own definition
   to SPEC J — it says "the two parameter additions OF SPEC J" — so a parameter
   addition includes the docstring entry SPEC J orders for it. The result is
   opcodes (2) and (5) under G4, ten lines each, both pure `insert`, both
   adjacent to the function they document, neither touching an existing line.
   Reversible in one edit if the reviewer prefers the literal reading of
   constraint 4.
3. **A CLAIM IN SHIPPED CODE WENT STALE THIS ROUND AND CONSTRAINT 4 FORBIDS ME TO
   REPAIR IT.** `_dedupe_resumed_segments`'s docstring still carries, at
   `packages/orchestration/pingpong_loop.py`, the paragraph "Scope boundary — a
   deliberate absence … NO CALLER EXISTS YET. Nothing in this module calls this
   function. Wiring it into ``compose_builder_prompt`` and
   ``compose_reviewer_prompt`` behind a parameter that bypasses dedupe by default
   is the next slice of T002b". As of C3 that is FALSE: this round is that slice
   and both functions now call it. Constraint 4 permits no other line of the file
   to change and G4 measures exactly that, so I left it and declare it instead of
   routing around the constraint. IT SHOULD BE RETIRED IN THE NEXT ROUND'S CHANGE
   SET. The parallel claim in the test file — "no tmp_path, no provider and no
   loop below this line" above the T002a block — I could not edit either
   (constraint 6), so the new section header I appended says explicitly that the
   note stops there and that the last two cases drive the real loop.
4. **A REAL PRODUCT RISK THE WIRING INTRODUCES, OUT OF THIS ROUND'S SCOPE,
   REPORTED FOR REGISTRATION.** In `run_pingpong` the builder prompt is composed
   ONCE, with dedupe applied whenever `builder_resume_ref` is set. If that resume
   attempt then ERRORS, the loop's F106 T002c fallback re-sends THE SAME
   `builder_prompt` with `resume=None`, i.e. a prompt whose segments were replaced
   by `[unchanged: …]` markers into a session that never received the originals.
   `invalidate_on_resume_fallback` correctly clears the index AFTER the fact, but
   the already-composed prompt is not recomposed. The reviewer's own C4 path has
   the identical shape at `reviewer_resume_ref`. SPEC K explicitly forbids me to
   touch `record_finalized_call` or `invalidate_on_resume_fallback`, and
   recomposing on fallback is a change to neither this round's change set nor its
   SPECs, so I did not make it. Existing coverage:
   `test_a_failed_builder_resume_falls_back_within_the_same_round` and
   `test_the_fallback_invalidation_shrinks_exactly_the_builder_row` both stay
   green, so nothing regressed — but neither of them looks at the fallback
   prompt's TEXT, which is why this is a gap and not a red gate. I recommend an
   R-id.
5. **The sandbox bash guard refused several command FORMS**, not contents: `find
   … -exec rm`, `git checkout -- <path>`, `git restore <path>`, and some compound
   commands. `__pycache__` was therefore purged by a script that walks ONE
   allowed root — it refuses any root other than this round's worktree — and
   prints every directory it removes, so the removal set is a readable list and
   never a glob. The between-mutation restore was done by writing the file's own
   committed blob (`git show bb694018:<path>`) back into the worktree, which is
   exactly what `git checkout --` does; each restore was verified by `git -C …
   status --porcelain` printing EMPTY. Every `grep -c`, `wc -l`, `cmp`,
   `sha256sum`, `git show --numstat`, `git status --porcelain`, `git ls-files`
   and `git worktree` command the block names was run VERBATIM. No gate was
   weakened, reworded or narrowed to fit the guard.
6. **`ReviewFinding` is imported FROM `packages.orchestration.pingpong_loop`**,
   which re-exports it, rather than from its defining module
   `packages.orchestration.pingpong_provider`. Constraint 6 permits extending
   exactly ONE import statement in the test file — the `pingpong_loop` one — and
   SPEC L case 1 orders the shapes to vary `findings`, which needs the class.
   Extending the `pingpong_provider` import instead would have been a second
   edited statement and a second G4 opcode the block does not name. Trivially
   changed if the reviewer prefers the defining module.
7. **The new class carries its own `loop_repo` fixture** rather than reusing
   `TestChainAgainstTheRealLoop`'s `isolate_data_root` and `demo_repo`, because
   those are declared INSIDE that class and are not visible to another one. The
   fixture is deliberately NOT autouse, so the ten pure golden cases stay free of
   `tmp_path`; the repo itself comes from `TestChainAgainstTheRealLoop._make_repo`
   and the providers from its `_provider_pair`, so no construction was duplicated.
8. **MUTATION A FAILED WIDER THAN THE ONE NAMED CASE** — 21 failures. The block
   permits a wider red and asks that it be reported. Ten of the extras are the
   pre-existing `TestChainAgainstTheRealLoop` cases, which die on the `TypeError`
   the unguarded call raises inside `should_dedupe_segment`; that is genuine
   collateral of an unguarded `None`, not a second subject. MUTATION C's one
   extra is principled rather than collateral: it is case 5's own positive
   control.
9. **Scratch artefacts live under `.remedy-wt/` and are gitignored**, never
   committed and never in the change set: `f109-r7-extract.py`,
   `f109-r7-plan.txt`, `f109-r7-g3.py`, `f109-r7-g3c.py`, `f109-r7-g3e.py`,
   `f109-r7-g4.py`, `f109-r7-linelen.py`, `f109-r7-probe.py`,
   `f109-r7-purge.py`, `f109-r7-mutate.py`, `f109-r7-restore.py`,
   `f109-r7-mutb-evidence.py`, `f109-r7-lr-base.md`. Two were deleted BY EXACT
   PATH the moment they had served: `f109-r7-lr-scratch.md` (the G3(c) negative
   control) and `f109-r7-plan-verify.txt` (the G2 re-extraction). `git ls-files
   .remedy-wt` returns nothing, as G7 records.
10. **Four `.remedy-wt/job-*` worktrees predate this branch** and were left
    alone. Exactly one worktree was created this round,
    `.remedy-wt/f109-r7-g5-wt`, and it was removed by exact path and then pruned.
11. **No `docs/` file was touched.** The change set forbids it and T003 owns the
    docs for this feature. The deliberate absences are recorded where a reader
    would search for them — in both compose functions' docstrings and in the new
    test section's header — per AGENTS.md's discoverability convention.

## Open findings

The ledger stands at **331** findings registered and **63** resolved, so the open
set is **268** — every one of those three numbers UNCHANGED by this round, which
registered no finding and resolved none. `.agent/candidates.md` is unchanged and
states "EMPTY — no candidate is open.", so no block condition stands against
F109. `R-0769` remains registered and unfixed; its repair edits `README.md` and a
docs test, neither of which F109 owns. `.agent/prose_slips.md` gained round 6's
one line and now holds **65** dated lines. `.agent/STOP` was checked before the
first action of the round and again before this handback, and does not exist.

TWO ITEMS ABOVE ARE CANDIDATES FOR AN R-ID AND ONLY THE REVIEWER MAY MINT ONE:
deviation 4 (a resume-fallback re-sends an already-deduped prompt into a session
that never received the originals — wrong behaviour reachable in production) and
deviation 3 (a shipped docstring now says it has no caller when it has two).

## Next expected action

`git push origin feature/f109-semantic-dedupe` immediately after this commit —
not quoted here by design, so the reviewer measures the remote tip itself. No PR
was created and nothing was merged.

Then the reviewer's round-7 verdict, booked into `.agent/live_review.md` in the
FIRST commit of round 8 (amend0827 rule 1: a verdict never buys a round of its
own). The build then continues with T002c: record the deduped segments in the
manifest so evidence shows what the model did NOT receive again, and plumb the
config kill switch through to `dedupe_enabled`. Deviation 3's stale docstring
should be retired in that round's change set, and deviation 4 decided on before
T003's measurement fixture runs against a resumed chain.
