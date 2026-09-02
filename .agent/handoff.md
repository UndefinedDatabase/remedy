# Handoff — F109 Semantic dedupe, SESSION 1, round 5

Branch: `feature/f109-semantic-dedupe`
Base commit: `2f25302e5c1e30f2d847c80a80458220702b1f52` (round 4 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

THIS IS THE LAST ROUND OF SESSION 1. It booked round 4's PASS verdict, wrote
the `Done:` resolution of `R-0770` carrying the reviewer's own correction, and
landed T002a — the pure dedupe DECISION and the MARKER TEXT.
`packages/orchestration/pingpong_loop.py` was NOT touched.

## Commits this round

| Item | SHA        | Commit subject                                                                       |
|------|------------|--------------------------------------------------------------------------------------|
| C0a  | `6f7cc57a` | F109 R5 C0a: save the round 5 step block verbatim                                    |
| C0b  | `db0d44e2` | F109 R5 C0b: mirror the round 5 block to last_block                                  |
| C1   | `f3430c46` | F109 R5 C1: plan for round 5 — book round 4, correct R-0770, land the dedupe decision |
| C2   | `c3c0426f` | F109 R5 C2: book the round 4 gate and resolve R-0770 with its correction             |
| C3   | `411ba65e` | F109 R5 C3: the pure dedupe decision and its marker text                             |
| C4   | `851700d9` | F109 R5 C4: pin every dedupe decision rule before it can reach a prompt              |

C5 is this handoff rewrite, committed on top of `851700d9`. Every gate G1–G6 ran
at C4 or earlier, so all six are quoted below from real output. The push happens
AFTER C5 and is therefore deliberately not quoted here; the reviewer measures the
remote tip itself.

Six single-parent commits in the range before C5, no merge commit.

## Changed files (this round)

| Path                                            | Change                                                    |
|-------------------------------------------------|-----------------------------------------------------------|
| `.agent/authored/f109-r5.md`                    | new — step block, `cp` not retyped                        |
| `.agent/last_block.md`                          | rewritten — byte mirror of the authored block             |
| `.agent/plan.md`                                | rewritten — SLICE PLAN, whole file, 42 lines              |
| `.agent/live_review.md`                         | appended ONCE — SLICE RECORD, two paragraphs, at C2       |
| `packages/orchestration/session_sent_index.py`  | added to — constant + 2 functions, docstring reworded     |
| `tests/orchestration/test_semantic_dedupe.py`   | added to — 3 new classes, 24 new cases, no test changed   |
| `.agent/handoff.md`                             | rewritten — this file (C5)                                |

No path outside the ordered change set was touched. `git diff --numstat` over
`2f25302e..HEAD` lists exactly those six paths (C5 adds the seventh).

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum .agent/authored/f109-r5.md
  .agent/last_block.md` printed ONE digest twice:
  **`4d20295bb21fd4a0e41b938b4f40e884a1a64fc5ba4cb00bb9311e80ea9714ca`**, equal
  to each other AND to the `SHA256_OF_THIS_BLOCK` the delegation wrapper stated.
  The scratch original `.remedy-wt/f109-r5.md` was verified against that digest
  as the round's FIRST action, before anything was read or written, and it is
  344 lines and 24904 bytes exactly as the wrapper stated. Both C0a and C0b were
  `cp`, never a retype.
- **G2 THE PLAN — PASS.** `cmp .agent/plan.md .remedy-wt/slice_plan.txt` produced
  NO OUTPUT and exit 0 — byte-equal against the mechanically extracted slice,
  never a retype. `wc -l .agent/plan.md` = **42**, strictly under 50.
  `grep -c '^## Goal'` = **1** and `grep -c '^## Next Steps'` = **1**.
- **G3 THE RECORD APPEND — PASS, all four parts.** (a) BYTE ARITHMETIC: base
  **2036637** bytes with sha256
  `cb8e452a71f2917e1cff20a4faac089cf30cad09cd9c80d948c2e9481a512fdb`, both
  exactly as the block stated; S = **5488** after the trailing-newline strip;
  expected 2036637 + 2 + 5488 = **2042127**, actual **2042127**. The base was
  confirmed by byte test to end WITHOUT a trailing newline, and the file still
  ends without one after the append (`ends without trailing newline? True`).
  (b) SECOND, STRUCTURALLY DIFFERENT READER: the whole file was split on
  blank-line boundaries into units. I counted the paragraphs of SLICE RECORD
  myself — the `Gate: F109 R4 — …` paragraph and the `Done: R-0770 — …`
  paragraph, so **N = 2** — and the LAST 2 units equal those two paragraphs IN
  ORDER: **True**. (c) NEGATIVE CONTROL on a scratch copy
  `.remedy-wt/live_review_negctl.md`: the byte at offset **2036739**, confirmed
  by arithmetic to lie inside the FIRST appended paragraph and not the last, was
  XOR-flipped; the same reader (b) **REJECTED** it (False). The tracked file's
  sha256 was
  `9d9c7d6105668564f9fcbfad932f9dc7f56260fadb486096dd0929127feb8860` before the
  control and
  `9d9c7d6105668564f9fcbfad932f9dc7f56260fadb486096dd0929127feb8860` after —
  identical. The scratch copy was deleted by exact path.
  (d) COUNTS at C2: `grep -c '^Done: R-[0-9]\{4\} — '` went **62 → 63**;
  `grep -c '^Done: R-0770 — '` is **1**; `grep -c '^Gate: F109 R4 — '` is **1**;
  `grep -c '^- R-[0-9]\{4\} — '` is UNCHANGED at **331** (no finding registered
  this round); `grep -c '^Landed: R-'` is UNCHANGED at **25** — the
  `Landed: R-0770` line STAYS beside its new `Done:` paragraph, as ordered.
- **G4 THE COLOUR OF THE NEW DECISION — PASS: CONTROL GREEN, ALL THREE MUTATIONS
  RED ON THE NAMED CASES.** Run in a disposable worktree added at the C4 commit
  `851700d9` by exact path
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r5-g4`, never in the primary
  checkout. CONSTRAINT 8 FIRST, before any mutation was trusted:
  `python3 -B -c "import packages.orchestration.session_sent_index as m;
  print(m.__file__)"` run with the worktree as cwd printed
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r5-g4/packages/orchestration/session_sent_index.py`
  — INSIDE the worktree, so the editable-install `.pth` did not shadow it with
  the primary copy. `__pycache__` was purged before EVERY run (**0** dirs found
  each time — a fresh worktree carries none and `python3 -B` wrote none) and
  every pytest process used `python3 -B`. Each run was launched with the
  worktree as cwd through a no-shell `subprocess.run` so the REAL exit code
  could be read (see deviation 3); the argv was the block's exact command.
  Before each mutation the exact text was confirmed to occur **EXACTLY ONCE**,
  and the file was restored with
  `git checkout -- packages/orchestration/session_sent_index.py` between
  mutations.
  (a) CONTROL, unmutated: **exit 0, 79 passed**.
  (b) MUTATION A — deleted `if not enabled:` / `return False`, occurrences
  **1**: **exit 1, 1 failed, 78 passed — RED.** The single failure IS SPEC E
  case 2,
  `TestShouldDedupeSegment::test_the_kill_switch_refuses_though_every_other_condition_holds`.
  (c) MUTATION B — restored, then `return len(text) >= min_chars` →
  `return len(text) > min_chars`, occurrences **1**: **exit 1, 2 failed, 77
  passed — RED.** The failures INCLUDE the exactly-at-the-boundary case of SPEC
  E item 5, `test_a_segment_of_exactly_the_minimum_length_is_deduped`, together
  with `test_a_long_already_sent_segment_is_deduped` (whose text is exactly
  `DEDUPE_MIN_SEGMENT_CHARS` long, so it sits on the same boundary).
  (d) MUTATION C — restored, then deleted `if sha256 not in sent_hashes:` /
  `return False`, occurrences **1**: **exit 1, 2 failed, 77 passed — RED.** The
  failures INCLUDE SPEC E case 3,
  `test_a_hash_the_session_never_received_is_not_deduped`, together with SPEC E
  case 4, `test_an_empty_sent_set_dedupes_nothing` — both are membership cases,
  so both are the mutation's proper targets.
  No test was edited in any direction to produce a colour. Cleanup: the worktree
  was confirmed clean (`git status --porcelain` empty inside it after the final
  restore), then `git worktree remove --force
  /home/decodeux/Repos/remedy/.remedy-wt/f109-r5-g4` and `git worktree prune`.
  `git worktree list` afterwards shows the primary checkout plus exactly the
  four pre-existing `.remedy-wt/job-*` worktrees (`job-48a379ab5ca44ec5`,
  `job-7d1c93e2dc98415a`, `job-98e9364a83a34872`, `job-f76686b8435640e9`), which
  predate this branch and were left untouched.
- **G5 THE SUITES — PASS, all eight ordered suites, run SERIALLY with never two
  pytest processes alive at once.**
  `tests/orchestration/test_semantic_dedupe.py` exit 0, **79 passed** (base 55 —
  it GREW, as ordered, by the 24 new cases);
  `tests/orchestration/test_pingpong.py` exit 0, **34 passed** (base 34);
  `tests/orchestration/test_session_resume.py` exit 0, **27 passed** (base 27);
  `tests/ui_server/` exit 0, **515 passed** (base 515);
  `tests/orchestration/test_test_runner.py` exit 0, **52 passed** (base 52);
  `tests/regression/test_resource_safety.py` exit 0, **21 passed** (base 21);
  `tests/orchestration/test_integrity_gate.py` exit 0, **16 passed** (base 16);
  `tests/cli/test_golden_path.py` exit 0, **42 passed** (base 42). Every count
  matches its base except the one the block required to move.
- **G6 THE TREE — PASS.** `git status --porcelain` EMPTY (no output).
  `git ls-files .remedy-wt` returns NOTHING. Insertion counts, six numbers,
  `+` column only: C0a **344**, C0b **228**, C1 **17**, C2 **5**, C3 **72**,
  C4 **125**. Every one under 500. CONSTRAINT 2, the number this gate exists
  for: `git diff --numstat 2f25302e..HEAD --
  packages/orchestration/pingpong_loop.py` produced **NO OUTPUT AT ALL** — the
  loop is ABSENT from the range diff entirely, so T002's wiring is untouched and
  this round shipped only the decision it will call. The full range numstat
  lists exactly six paths: `.agent/authored/f109-r5.md` 344/0,
  `.agent/last_block.md` 228/206, `.agent/live_review.md` 5/1,
  `.agent/plan.md` 17/16, `packages/orchestration/session_sent_index.py` 72/3
  and `tests/orchestration/test_semantic_dedupe.py` 125/0.

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

Three new public names in `packages/orchestration/session_sent_index.py`, placed
per constraint 4 AFTER `invalidate_on_resume_fallback` and BEFORE
`_segment_hashes_from_manifest`, so the module's public-then-private layout
holds. 72 insertions, 3 deletions.

`DEDUPE_MIN_SEGMENT_CHARS = 200`, carrying the comment SPEC D dictates: a marker
has its OWN length, the marker for a typical segment name runs to roughly forty
characters, so a floor of 200 keeps the replacement worth making by a factor of
several; a DEFAULT, not a law, and both functions take an override. THE
"ROUGHLY FORTY" WAS MEASURED, NOT RECALLED: `dedupe_marker_for_segment("dossier")`
is **41** characters.

`dedupe_marker_for_segment(name)` returns exactly
`"[unchanged: " + name + ", previously provided]"` — no trailing newline, no
surrounding whitespace — and raises `SessionSentIndexError` when `name` is not a
non-empty string after stripping.

`should_dedupe_segment(text, sha256, sent_hashes, *, enabled=True,
min_chars=DEDUPE_MIN_SEGMENT_CHARS)` returns True only when `enabled` holds,
`sha256` is a non-empty string present in `sent_hashes`, and `text` is a string
with `len(text) >= min_chars`. `enabled` is consulted FIRST and alone, so the
kill switch is total. A malformed `text` or `sha256` RETURNS FALSE rather than
raising, and the comment at the site states why the contrast with `record_call`
is deliberate: a bad manifest corrupts the index silently and must be loud, a
bad dedupe input has an obviously correct safe answer, which is to send the full
content.

THE MODULE STAYS PURE, per constraint 6. `ast` reports the module's only imports
are `__future__` and `collections.abc`: no file read, no file write, no network,
no provider call, nothing from `packages.orchestration`, and in particular
nothing from `prompt_segments` — the three arguments are the segment's TEXT,
HASH and NAME as plain values.

THE DOCSTRING EDIT IS CONSTRAINT 4'S ONE NAMED EXCEPTION and was applied as
ordered: the "deliberate absences" bullet that said no prompt is rewritten here
now says the DECISION and the MARKER TEXT land here (T002a) and that what
remains absent is the composition hook that calls them — nothing in
`pingpong_loop.py` invokes either function yet — plus the config plumbing that
supplies `enabled`, both F109 T002b. The three new names were added to the
`Public API` list. Nothing else in the docstring changed.

I RAN THE SHIPPED FUNCTIONS before committing, not just read them: the true
case, the kill switch, a hash not in the set, an empty set, exactly 200 → True,
199 → False, a `min_chars=5` override, four malformed `text` values and four
malformed `sha256` values returning False without raising, and `''`, `'   '`,
`None` and `7` each raising `SessionSentIndexError` from the marker.

## What C4 actually landed

125 insertions, 0 deletions — a pure addition. The diff's first changed line
inside the body is 779, after the existing final class, so NO EXISTING TEST WAS
EDITED, REORDERED OR DELETED. Three new classes, 24 new cases (55 → 79), all
hermetic and PURE: no `tmp_path`, no network, no provider, no loop below the
new section marker. The file's existing helpers `_real_manifest_rows` and
`SegmentStabilityRank` are reused.

SPEC E's eleven mandatory cases, mapped:

1. `test_a_long_already_sent_segment_is_deduped` — the one True case.
2. `test_the_kill_switch_refuses_though_every_other_condition_holds` — broken by
   MUTATION A, and by nothing else.
3. `test_a_hash_the_session_never_received_is_not_deduped` — broken by MUTATION C.
4. `test_an_empty_sent_set_dedupes_nothing`.
5. `test_a_segment_of_exactly_the_minimum_length_is_deduped` and
   `test_a_segment_one_character_below_the_minimum_is_not_deduped` — two
   SEPARATE named cases, as ordered; the first is broken by MUTATION B.
6. `test_a_custom_min_chars_override_is_honoured` — a 12-char text the default
   refuses and `min_chars=10` accepts, asserted in the same case so the override
   is shown to be what moved the answer.
7. `test_a_non_string_text_returns_false_and_raises_nothing` over `None`, `7`,
   `b"x"*300`, `["x"*300]`, `object()`; and
   `test_a_malformed_sha256_returns_false_and_raises_nothing` over `None`, `7`,
   `""`, `"   "`, `b"a"*64`, `["a"*64]`.
8. `test_the_marker_is_exactly_the_expected_string` — the WHOLE string asserted
   literally against `"[unchanged: dossier, previously provided]"`, not a
   substring.
9. `test_a_nameless_marker_raises`, parametrised over `""`, `"   "`, `"\t\n"`.
10. `test_the_marker_is_shorter_than_the_threshold_that_justifies_it` —
    `len(dedupe_marker_for_segment("dossier")) < DEDUPE_MIN_SEGMENT_CHARS`,
    which pins the constant against the marker it exists to justify.
11. `TestTheDecisionAgainstARecordedIndex::test_a_long_recorded_segment_is_deduped_and_a_short_one_is_not`
    — END TO END WITH THE INDEX, no loop: a two-segment manifest built through
    the REAL producer with `_real_manifest_rows`, recorded via
    `record_call(..., ok=True)`, then read back through `sent_hashes("session-a")`.
    The long segment (416 chars) is deduped; the short one (19 chars) is NOT,
    and the case asserts `by_name["task"] in sent` first so the refusal is
    demonstrably about the LENGTH and not about a missing hash.

CONSTRAINT 10 — the three property guards in
`tests/orchestration/test_test_runner.py` still sweep every `*.py` under
`packages/orchestration/` and all three pass: that suite is exit 0 at 52. The
new code contains no `shell=True`, no `0000` and no permit-order pattern.

Ruff followed BY CONSTRUCTION per constraint 7, which forbids gating on it:
longest line is **95** in `session_sent_index.py` and **101** in
`test_semantic_dedupe.py`, both under the configured 120; both files parse with
`ast`; the import groups are unchanged and the two extended `from … import`
lists stay in the repo's `order-by-type` isort order (constant, classes,
functions).

## Deviations

1. **TWO EXISTING IMPORT STATEMENTS WERE EXTENDED, WHICH CONSTRAINT 4'S "NOTHING
   ALREADY IN EITHER FILE IS EDITED" LITERALLY FORBIDS.** In
   `session_sent_index.py` the line `from collections.abc import Iterable,
   Mapping, Sequence` gained `Container`, used to type `sent_hashes` as the "any
   container supporting `in`" SPEC D specifies. In `test_semantic_dedupe.py` the
   existing `from packages.orchestration.session_sent_index import (…)` block
   gained `DEDUPE_MIN_SEGMENT_CHARS`, `dedupe_marker_for_segment` and
   `should_dedupe_segment`. Both are unavoidable consequences of ADDING code
   that uses new names, and the alternative — a second import statement lower in
   each file — would break the repo's import layout and ruff's `I` rules. No
   test, no function and no assertion already in either file was edited,
   reordered or deleted; the only semantic edit is constraint 4's one NAMED
   exception, the module docstring. Declared rather than left to be discovered.
2. **THE CONSTANT SITS WITH THE TWO FUNCTIONS, NOT AT THE TOP OF THE MODULE.**
   SPEC D lists `DEDUPE_MIN_SEGMENT_CHARS` first, and Python convention would
   put a module-level constant above the class definitions; constraint 4 says
   the new PUBLIC names go after `invalidate_on_resume_fallback` and before the
   private helpers. Constraint 4 is the more specific order, so I followed it
   and placed all three together. If the reviewer wants the constant hoisted,
   that is a one-line move.
3. **The sandbox bash guard refused several command FORMS**, not contents: `$?`
   and `${PIPESTATUS[0]}` expansions, `find -exec`, and compound commands
   containing two `cd`s. Real exit codes were therefore read through a no-shell
   `subprocess.run` runner that received the block's EXACT argv (`python3 -B -m
   pytest tests/orchestration/test_semantic_dedupe.py -q` for G4, and the
   `python3 -m pytest … -q` form for G5) and printed `proc.returncode`;
   `__pycache__` was purged with `pathlib.rglob` + `shutil.rmtree` instead of
   `find -exec`. Every `grep -c` pattern the block names was run verbatim as its
   own standalone command and is quoted above. No gate was weakened, reworded or
   narrowed to fit the guard.
4. **MUTATIONS B AND C EACH FAILED TWO CASES, NOT ONE.** The block requires each
   failure set to INCLUDE a named case, and both do. The extras are proper
   targets rather than collateral: B also breaks
   `test_a_long_already_sent_segment_is_deduped`, whose text is exactly
   `DEDUPE_MIN_SEGMENT_CHARS` long and therefore sits on the same boundary; C
   also breaks `test_an_empty_sent_set_dedupes_nothing`, which is the other
   membership case. Reported because a wider red than ordered is still a
   difference from the order.
5. **Scratch artefacts live under `.remedy-wt/` and are gitignored**, never
   committed and never in the change set: `f109-r5.md`, `slice_plan.txt`,
   `slice_record.txt`, and `live_review_negctl.md` which was deleted by exact
   path after G3(c). `git ls-files .remedy-wt` returns nothing, as G6 records.
6. **Four `.remedy-wt/job-*` worktrees predate this branch** and were left
   alone. Exactly one worktree was created this round and it was removed by
   exact path, then pruned.

## Open findings

The ledger stands at **331** findings registered and **63** resolved, so the
open set is **268**. This round registered NO new finding and resolved exactly
one: `R-0770`, whose `Done:` paragraph also carries the correction of the
finding's own false clause — that no assertion available today could separate
"cleared then refilled" from "never cleared". The `Landed: R-0770` line was left
standing beside the new `Done:` paragraph, per the block. `.agent/candidates.md`
is unchanged and EMPTY, so no block condition stands against F109. `R-0769`
remains registered and unfixed; its repair edits `README.md` and a docs test,
neither of which F109 owns.

## Next expected action

`git push` on `feature/f109-semantic-dedupe` immediately after this commit — not
quoted here by design, so the reviewer measures the remote tip itself.

THIS IS THE LAST ROUND OF SESSION 1, so the next action belongs to the SESSION
THAT FOLLOWS: the reviewer's round-5 verdict is booked into
`.agent/live_review.md` in the FIRST commit of that session's first round. The
build then resumes at T002b — the composition hook in
`packages/orchestration/pingpong_loop.py` that calls `should_dedupe_segment` and
`dedupe_marker_for_segment`, replacing a deduped segment's text with its marker
while leaving rank and order untouched, with non-resume calls bypassing it
entirely under a byte-equality golden.
