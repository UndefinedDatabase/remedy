STEP T003d — F109 Semantic dedupe — ROUND 14, SESSION 3

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Goal: MEASURE THE SAVINGS FROM THE RECORD ITSELF. The feature file's
Design closes with "Measurement: actuals comparison on the fixture chain,
recorded", and its Acceptance asks for "savings recorded". Round 13 put the
deduped names on the trace; this round adds ONE PURE FUNCTION that reads a
run's own trace entries and reports what the run did NOT resend, counting
only what it can actually observe and NAMING what it cannot. Also book
round 13's PASS and register and repair `R-0779`.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f109-r14.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   apply SLICE PLAN to `.agent/plan.md`
  C2   append SLICE RECORD to `.agent/live_review.md`
  C3   apply SPEC F to `tests/orchestration/test_semantic_dedupe.py`
  C4   apply SPEC G to `packages/orchestration/prompt_trace.py`
  C5   apply SPEC H to the two test files
  C6   rewrite `.agent/handoff.md`

Change set — exactly these eight paths and no ninth:
  `.agent/authored/f109-r14.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `packages/orchestration/prompt_trace.py`
  `tests/orchestration/test_prompt_trace.py`
  `tests/orchestration/test_semantic_dedupe.py`
  `.agent/handoff.md`

Constraints:

1. Every authored slice is applied BYTE FOR BYTE. This block reached you as
   a file: `cp` it from `/home/decodeux/Repos/remedy/.remedy-wt/f109-r14.md`
   into `.agent/authored/f109-r14.md` and `cp` that into
   `.agent/last_block.md`. Never retype either.
2. The commit order above is FIXED. C1 advances `.agent/plan.md` as the
   FIRST substantive commit because this round touches the finding ledger.
3. YOU WRITE NO `Done:` PARAGRAPH AND NO VERDICT OF YOUR OWN. `R-0779` is
   repaired this round but only the reviewer marks it resolved; a
   `Landed: R-0779 — <one line>` line is permitted and nothing else.
4. THE NEW FUNCTION IS PURE AND READ-ONLY. It takes trace entries and
   returns a value. It opens no file, writes nothing, reads no global, and
   calls no provider. It is NOT wired into `run_pingpong` this round —
   wiring it is a later slice with its own gate, and a function landed
   unwired but tested is the smaller, reviewable step.
5. Do not touch `packages/orchestration/pingpong_loop.py`,
   `packages/orchestration/prompt_segments.py` or
   `packages/orchestration/token_ledger.py`. The manifest ROW KEYS STAY
   CLOSED, as they have every round of this feature.
6. DO NOT REUSE `packages/orchestration/token_economy.py`'s
   `estimate_token_savings`. Read it before deciding you disagree: its own
   docstring says it "Never claims verified savings", and it takes two
   ESTIMATES. This measurement is the opposite kind — the withheld
   characters are recorded exactly — and collapsing the two concepts into
   one name would make a measured number indistinguishable from a guess.
   Say so in the new function's docstring, naming that function, so the
   next reader finds the distinction where they would search for it.
7. Every gate G1-G8 runs at C5 or earlier, so the handback can quote every
   reading. The handback commit's own insertion count is NOT quoted in it.
8. Re-read `.agent/STOP` from disk before your first action and again
   before the handback. If it exists, finish any half-written commit,
   write the handback and end.
9. Destructive verification runs ONLY inside a disposable `git worktree` or
   on a scratch copy, each addressed BY EXACT PATH under `.remedy-wt/`,
   never in the primary checkout. Remove and prune what you create and
   confirm `git status --porcelain` is EMPTY afterwards.
10. Push after the handback commit. Create no PR. Merge nothing. Never
    force-push. Stay on `feature/f109-semantic-dedupe`.

Done when — EIGHT GATES, every one executed with its real exit code
recorded, one line per gate in the handback:

G1 TRANSPORT. `sha256sum .remedy-wt/f109-r14.md .agent/authored/f109-r14.md
   .agent/last_block.md` prints ONE digest three times. Report it. This
   chain compares the scratch original against the saved copy against its
   mirror and claims nothing about any earlier bytes.

G2 THE PLAN. Extract SLICE PLAN mechanically from
   `.agent/authored/f109-r14.md` (index of the opening `<<<SLICE PLAN`
   line, index of the closing `SLICE PLAN` line, everything between) and
   `cmp` it against `.agent/plan.md`: no output, exit 0. `wc -l` is
   strictly under 50. `grep -c '^## Goal'` is 1 and
   `grep -c '^## Next Steps'` is 1.

G3 THE RECORD APPEND, four readings.
   (a) ARITHMETIC. Report base size and sha256, the appended length S after
       stripping trailing newlines, and that base + S equals the new size
       exactly. Report the new sha256. The file still ends WITHOUT a
       trailing newline.
   (b) A SECOND, STRUCTURALLY DIFFERENT READER that counts no byte: split
       the WHOLE file on blank-line boundaries into units, COUNT N from the
       payload itself rather than taking it from this block, and assert the
       LAST N units equal the appended paragraphs IN ORDER. Report N and
       the first characters of each.
   (c) NEGATIVE CONTROL on a scratch copy at an exact path under
       `.remedy-wt/`, never on the tracked file: flip one byte INSIDE THE
       FIRST appended paragraph and confirm reader (b) REJECTS it while it
       accepted the tracked file. Report the tracked sha256 before and
       after to show it did not move, then delete the copy by exact path
       and confirm its absence.
   (d) COUNTS, AND THE OPEN SET IS A SET DIFFERENCE, NEVER A SUBTRACTION
       (`R-0778`). Report registered ids, DISTINCT registered ids, `Done:`
       LINES, DISTINCT resolved ids, and the size of the set difference.
       Against `5fe32449` those read 339 / 339 / 65 / 63 / 276; after this
       round the registered count is 340 and the open set is 277, with
       `Done:` lines and distinct resolved ids both UNCHANGED because this
       round resolves nothing. Also report `grep -c '^Gate: F109 R13 — '`
       as 1 and `grep -c '^- R-0779 — '` as 1. Read every base reading from
       `git show 5fe32449:.agent/live_review.md`, never by rewinding the
       tracked file.

G4 THE EDIT SHAPE, read from `git show <sha>:<path>` blobs and never by
   writing a revision over the tracked file. Compare blobs as SEQUENCES OF
   LINES with `difflib.SequenceMatcher(None, before, after,
   autojunk=False)`.
   (a) ACROSS C4 on `packages/orchestration/prompt_trace.py`: every
       non-equal opcode is an `insert`; none is `replace` or `delete`.
       Report the opcodes and TOTAL LINES DELETED, which is 0.
   (b) ACROSS C3: a docstring rewrite, so a non-zero deletion count is
       expected. Report `grep -c '    def test_'` before and after — it is
       UNCHANGED, because C3 touches no case.
   (c) ACROSS C5: cases are ADDED, so report `grep -c '    def test_'`
       before and after for BOTH test files and say by how much each rose.
   (d) THE FUNCTION IS PURE, proved on the SOURCE rather than asserted:
       parse `packages/orchestration/prompt_trace.py` with `ast`, locate
       the new function, and report that its body contains no `Import`, no
       `Global`, no `Nonlocal`, and no call to `open`, `write`, `Path`, or
       any name from this module that performs I/O. Name what you searched
       for, so the absence is only as wide as the search.

G5 THE COLOUR — TWO RED-PROOFS, each with its UNMUTATED CONTROL reported
   beside it, because a colour with no baseline is not evidence. In a
   disposable worktree added BY EXACT PATH under `.remedy-wt/`, checked out
   at C5. RUN THE IMPORT PROBE FIRST: `python3 -B -c "import
   packages.orchestration.prompt_trace as m; print(m.__file__)"` with the
   worktree as cwd must resolve INSIDE the worktree, or an editable install
   is shadowing it and the gate is void. Purge `__pycache__` before every
   run; every process is `python3 -B` with `-p no:cacheprovider`. Before
   each write, count the bytes you are about to change IN THAT FILE and
   report the count; where it is not 1, quote a longer UNIQUE string and
   say which occurrence you took. Restore from the C5 blob by exact path
   between mutations and after the last.
   (a) DROP THE HONESTY BRANCH: make the function count a deduped segment
       whose full-content size it never observed as though the saving were
       zero, instead of reporting it as unmeasured. The SPEC H case that
       pins the unmeasured report must FAIL. Report the failing node.
   (b) COUNT THE MARKER AS FREE: remove the subtraction of the marker's own
       characters, so the function reports gross rather than net. The
       SPEC H case that pins the arithmetic must FAIL. This is the proof
       that the case pins a NUMBER and not merely a direction.
   Then remove the worktree and prune, and show that `git worktree list`
   holds only the primary checkout and the four pre-existing
   `remedy/job-*` worktrees.

G6 THE SUITES, run SERIALLY — one process starts, finishes, and only then
   the next. ALL FIFTEEN MUST BE EXIT 0. Base readings measured by the
   reviewer at `5fe32449`, in parentheses. Only the first two may move, and
   only upward. Report yours beside each and name any that moved.
     tests/orchestration/test_semantic_dedupe.py            (128)
     tests/orchestration/test_prompt_trace.py                (49)
     tests/orchestration/test_pingpong_cli.py               (173)
     tests/orchestration/test_pingpong.py                    (34)
     tests/orchestration/test_session_resume.py              (27)
     tests/orchestration/test_token_ledger.py               (120)
     tests/orchestration/test_token_truth.py                 (37)
     tests/orchestration/test_token_truth_v1_contract.py    (101)
     tests/orchestration/test_job_evidence.py                (93)
     tests/orchestration/test_provider_evidence_integration.py (64)
     tests/orchestration/test_cost_report.py                 (22)
     tests/ui_server/test_prompt_trace_payload.py            (20)
     tests/ui_server/test_prompt_trace_lens.py               (13)
     tests/test_observability_index.py                       (14)
     tests/cli/test_golden_path.py                           (42)

G7 THE TREE. `git status --porcelain` EMPTY. `git ls-files .remedy-wt`
   returns nothing. Report the insertion count of C0a through C5 from
   `git show --numstat` — the `+` column only, per AGENTS.md DECISION
   F104 D1 — and confirm each is under 500. Confirm every commit is
   single-parent with `git log --format="%h parents=%p"`. Compare those
   numbers CELL BY CELL against your own `## Commits` table and state
   plainly that you ran that comparison.

G8 THE STALENESS SWEEP (finding `R-0417`'s standing counter-measure, which
   is OPEN and binding). For EACH file this round touched, re-read it end
   to end and report every sentence that states a count, a list of modules,
   a round map, or a completion — together with whether it STILL HOLDS. Two
   are already known and SPEC F repairs both, so report them as repaired
   rather than as new. Pay particular attention to
   `packages/orchestration/prompt_trace.py`'s module docstring and to
   `build_trace_entry`'s, which round 13 already widened once. Report the
   sweep even where it finds nothing more, and repair nothing outside the
   change set — declare it.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
It carries the state block, the item-status table with every C0a-C6 item
present exactly once, the changed-files table, one line per gate with real
readings, the deviations, the open-findings count STATED AS A SET
DIFFERENCE, and — mandatory — the SESSION NUMBER, which is 3. It has no
length cap. Then push.

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

Round 14, session 3. Measure the savings from the record itself: one PURE
function reads a run's own prompt-trace entries and reports what the run
did not resend, counting only what it can observe and NAMING the segments
whose full-content size was never recorded rather than guessing them. It
is deliberately not wired into the loop this round. Also book round 13's
PASS and register and repair `R-0779`, the module docstring that still
describes one real-loop class where there are now several.

## Next Steps

- The T003 DOCS: describe the feature's built state and register the doc
  in `docs/README.md` in the same commit.
- The integration gate (docs/agents/integration_gate.md), then the closure
  sequence.

## Risks

- The savings function is landed UNWIRED. Nothing reads it yet, so a later
  round must either wire it or say plainly why it stays a library.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

<<<SLICE RECORD
Gate: F109 R13 — the round 13 entry. VERDICT PASS, over the range `7b423b1a..5fe32449`. THE REVIEWER RE-RAN EVERY SUITE RATHER THAN READING THE HANDBACK: all fifteen are exit 0, with the two suites that gained cases at 128 and 49 — up from 125 and 46 by exactly the six cases SPEC E ordered — and the other thirteen at 173, 34, 27, 120, 37, 101, 93, 64, 22, 20, 13, 14, 42, every one identical to its base. THE PRODUCTION DIFF WAS READ IN FULL and is exactly SPEC D: `PromptTraceEntry` gains `deduped_segment_names` with a `#:` comment that distinguishes its empty from `segment_manifest`'s empty, `build_trace_entry` derives it from `composed_prompt` alone, and the function's docstring paragraph is extended to say why it is derived rather than passed. Three `insert` opcodes, ZERO lines deleted, and no parameter was added to the function's signature. THE FIELD IS NOT A ROW KEY, independently confirmed: `deduped_segment_names` occurs 0 times in `prompt_segments.py` and 0 times in `token_ledger.py`, so the manifest rows and the `call_segments` columns they mirror are untouched, which is the constraint every round of this feature has carried. THE LOOP NEEDED NO CHANGE, and the round verified that rather than assuming it: all three `build_trace_entry` call sites already pass `composed_prompt=`. THE LEDGER, re-measured by the reviewer as a SET DIFFERENCE per `R-0778` and not as a subtraction: 339 registered ids, all distinct; 65 `Done:` lines over 63 distinct resolved ids; open set 276. `Gate: F109 R12 — ` 1 and `- R-0777 — `/`- R-0778 — ` 1 each. THE TREE is clean and the branch is pushed at `5fe32449`. THE ROUND'S FOUR DECLARED DEVIATIONS ARE ALL SOUND AND TWO ARE THE REVIEWER'S FAULT: SPEC D said "Two insertions and no third" while its own item (2) ordered a docstring extension, which is a third insertion region — the block contradicted itself and the worker applied all three ordered changes and said so; and SPEC E ordered a `prompt_text_truncated` guard for a list field the text cap cannot reach, so the guard is sound for the neighbouring reads and vacuous for the one it was named for. Neither damaged anything on disk and neither earns an id under amend0827 rule 2; both belong in `.agent/prose_slips.md` at the closure consolidation. The worker also declined to reword `build_trace_entry`'s "BOTH `segment_manifest` and `segment_manifest_chars`" because constraint 5 forbade editing existing lines — correctly, and the sentence remains TRUE as written since it quantifies over the two it names rather than over everything derived from the composed prompt.

- R-0779 — Low, THE DEDUPE SUITE'S MODULE DOCSTRING DESCRIBES A FILE THAT NO LONGER EXISTS: ONE REAL-LOOP CLASS WHERE THERE ARE NOW SEVERAL, AND A SCOPE LINE NAMING ONLY T001a. Found by the WORKER of F109 R13 during that round's G8 sweep, reported honestly against a gate that had already passed, and registered here at the reviewer's first opportunity. MEASURED INDEPENDENTLY by the reviewer at `5fe32449`: `tests/orchestration/test_semantic_dedupe.py` opens "Tests for the per-session sent-hash index (F109 T001a)." while the file now also covers the composition hook and its markers (T002), the config kill switch (T002c, landed at `b245e1c9`) and the trace's record of what was not resent (T003c, landed at `899eeefd`); and its third paragraph says "the final class deliberately drives the real ping-pong loop against ``FakeProvider`` in a tmp_path (F109 T001b-ii)", where SEVERAL later classes now drive the real loop and the final one is the T003c class rather than the T001b-ii one. Both sentences were TRUE when written and later rounds falsified them without touching them — the `R-0749` and `R-0773` shape, and the third instance of it on this branch, which is why the standing staleness sweep that found it is worth its place in every gate list. WHY LOW: no behaviour is wrong, no gate is blind, no test is weakened, and every case in the file passes; the defect is confined to the paragraph a reader meets FIRST when deciding what the file is for, which is the reason it is registered rather than ignored. WHY IT WAS NOT REPAIRED IN THE ROUND THAT FOUND IT: SPEC C and SPEC E both scoped round 13 to one comment and to additive cases, so repairing it would have widened the change set past the block, and the worker declared it instead — the correct behaviour under guardrail G8. FIX: restate the opening line to name the slices the file actually covers, and restate the real-loop sentence WITHOUT a numeral, since the count of such classes has now changed twice and a number in that sentence would only go stale again. Resolved when the module docstring names no single "final class" and no slice the file does not cover.
SLICE RECORD

<<<SPEC F
SPEC F — R-0779: THE MODULE DOCSTRING.

File: `tests/orchestration/test_semantic_dedupe.py`. Two prose
replacements in the module docstring. No case, name or assertion is
touched, and `grep -c '    def test_'` is identical before and after.

PAIR F1. TO contains FROM: false, so this is a REWRITE. FROM occurs
exactly 1 time before the commit.

FROM:
"""Tests for the per-session sent-hash index (F109 T001a).

TO:
"""Tests for F109 semantic dedupe — the per-session sent-hash index
(T001a), the composition hook and its markers (T002), the config kill
switch (T002c) and the trace's record of what was not resent (T003c).

PAIR F2. TO contains FROM: false, so this is a REWRITE. FROM occurs
exactly 1 time before the commit. The TO states NO COUNT of the real-loop
classes on purpose: that number has already changed twice, and a numeral
here is a sentence nobody re-derives.

FROM:
PURE — no tmp_path, no provider — while the final class deliberately drives the
real ping-pong loop against ``FakeProvider`` in a tmp_path (F109 T001b-ii). The

TO:
PURE — no tmp_path, no provider — while the later classes deliberately drive
the real ping-pong loop against ``FakeProvider`` in a tmp_path, beginning at
F109 T001b-ii and continuing through every slice that followed it. The
SPEC F

<<<SPEC G
SPEC G — THE MEASUREMENT, READ FROM THE RECORD.

File: `packages/orchestration/prompt_trace.py`. One new module-level
function, appended after the existing ones. Nothing already in the file is
edited or deleted.

THE FUNCTION takes an ordered sequence of `PromptTraceEntry` — a run's own
`result.prompt_traces`, or the entries parsed back out of
`prompt_trace.jsonl` — and returns what the run did NOT resend. Name it so
it greps to itself and says which kind of number it is: it MEASURES, it
does not estimate.

WHAT IT COMPUTES. Walk the entries IN ORDER, remembering for each
`(role, segment name)` the most recent FULL-CONTENT size seen for that
segment — that is, its `chars` in the manifest of an entry whose
`deduped_segment_names` does NOT contain it. When an entry DOES report a
name in `deduped_segment_names`, that entry's manifest row for the same
name carries the MARKER's `chars` instead. For each such occurrence:
  - the characters avoided are the remembered FULL size,
  - the characters spent are the marker's `chars` in this entry,
  - the net saving is the first minus the second.
Report the totals, and the number of deduped segment occurrences counted.

THE HONESTY BRANCH, WHICH IS THE POINT OF THE FUNCTION. A name may be
reported as deduped with NO earlier full-content observation in the
entries given — a caller can hand over a partial trace, and a resumed
session's first recorded call may already be deduping against a session
opened before the record begins. Such an occurrence is NOT counted as
zero and is NOT guessed: it is collected into a reported field naming
those segments, and excluded from every total. A reader must be able to
tell "nothing was saved" from "the saving is not measurable from what you
gave me", and a function that conflates the two would report a confident
zero for an unmeasured run.

Return a small frozen structure — a dataclass in this module's own idiom,
or a dict if that fits the file better — carrying the totals, the counted
occurrences, and the unmeasured names as a tuple in first-seen order.

THE DOCSTRING must say, in the file's own voice: that every number is
MEASURED from recorded evidence rather than estimated; that
`packages/orchestration/token_economy.py`'s `estimate_token_savings` is
the DIFFERENT, estimate-shaped concept and is deliberately not reused
here, because that function's own docstring says it never claims verified
savings while this one reports only what the record proves; and that the
unmeasured names exist so an absent measurement can never read as a zero.
Purity is part of the contract: say that it opens nothing and writes
nothing, since gate G4(d) proves exactly that.
SPEC G

<<<SPEC H
SPEC H — THE TESTS FOR THE MEASUREMENT.

Two files. No existing case is edited, renamed or deleted; every case is
ADDED.

IN `tests/orchestration/test_prompt_trace.py` — the arithmetic, on
hand-built entries, where the numbers can be exact:
  1. NO ENTRIES yields zeroed totals, no counted occurrences and no
     unmeasured names.
  2. ENTRIES THAT DEDUPED NOTHING yield the same, however many entries.
  3. THE ARITHMETIC CASE: one entry sending a named segment at a known
     full size, then a later entry of the SAME role reporting that name in
     `deduped_segment_names` with a known smaller marker size. Assert the
     avoided total, the spent total, the NET, and the counted occurrences,
     all as exact numbers. This is the case gate G5(b) reddens.
  4. THE UNMEASURED CASE: an entry reporting a deduped name with no
     earlier full-content observation. Assert that the name appears in the
     unmeasured field, that it is EXCLUDED from every total, and that the
     totals are therefore zero — and assert BOTH halves, because a
     function that simply returned zero would satisfy the totals alone.
     This is the case gate G5(a) reddens.
  5. ROLES DO NOT CROSS: a full-content observation recorded for one role
     does not supply the size for the other role's deduped name of the
     same segment name. That name is unmeasured, not measured from the
     wrong role. The scope rule of this feature is about what a SESSION
     provably received, and a per-role reading is the nearest honest thing
     the trace alone supports.

IN `tests/orchestration/test_semantic_dedupe.py` — the claim on the REAL
loop, appended as ONE new class at the very END, driving the existing
fixtures exactly as the neighbouring chain classes do. Reuse
`fallback_repo`, `TestChainAgainstTheRealLoop._provider_pair` and `._run`.
  6. A RESUMED CHAIN REPORTS A POSITIVE NET SAVING, and the counted
     occurrences equal the total number of names across every entry's
     `deduped_segment_names`. Assert non-vacuity first: the chain really
     resumed.
  7. A DISABLED RUN REPORTS ZERO AND NAMES NOTHING UNMEASURED. With
     `semantic_dedupe_enabled=False` the totals are zero, the counted
     occurrences are zero, and the unmeasured field is EMPTY — the
     discriminator that stops case 6 passing on a function that reports
     activity whatever the run did.
SPEC H
