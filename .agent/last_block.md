STEP T003c — F109 Semantic dedupe — ROUND 13, SESSION 3

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Goal: Surface the deduped names into the prompt TRACE as a first-class
field, now that round 12 made the trace honest about WHICH call it
describes. `PromptTraceEntry` gains `deduped_segment_names`, derived from
the composed prompt at the same seam `segment_manifest` already uses, so
the evidence records what the model did NOT receive again. Also book round
12's PASS, register `R-0777` and `R-0778`, and repair `R-0777` in place.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f109-r13.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   apply SLICE PLAN to `.agent/plan.md`
  C2   append SLICE RECORD to `.agent/live_review.md`
  C3   apply SPEC C to `tests/orchestration/test_semantic_dedupe.py`
  C4   apply SPEC D to `packages/orchestration/prompt_trace.py`
  C5   apply SPEC E to the two test files
  C6   rewrite `.agent/handoff.md`

Change set — exactly these eight paths and no ninth:
  `.agent/authored/f109-r13.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `packages/orchestration/prompt_trace.py`
  `tests/orchestration/test_prompt_trace.py`
  `tests/orchestration/test_semantic_dedupe.py`
  `.agent/handoff.md`

Constraints:

1. Every authored slice is applied BYTE FOR BYTE. This block reached you as
   a file: `cp` it from `/home/decodeux/Repos/remedy/.remedy-wt/f109-r13.md`
   into `.agent/authored/f109-r13.md` and `cp` that into
   `.agent/last_block.md`. Never retype either.
2. The commit order above is FIXED. C1 advances `.agent/plan.md` as the
   FIRST substantive commit because this round touches the finding ledger.
3. YOU WRITE NO `Done:` PARAGRAPH AND NO VERDICT OF YOUR OWN. `R-0777` is
   REPAIRED this round but only the reviewer marks it resolved: if you want
   to record that the fix landed, use a `Landed: R-0777 — <one line>` line
   and nothing else. `R-0778` is registered and not repaired.
4. THE MANIFEST ROW KEYS STAY CLOSED. `ComposedPrompt.manifest_as_dicts`
   returns rows keyed `name`, `rank`, `sha256`, `chars`, `tokens_estimated`,
   and `token_ledger.py`'s `call_segments` table mirrors them column for
   column. `deduped_segment_names` is a TOP-LEVEL field on the entry, NOT a
   sixth row key. Do not touch `packages/orchestration/token_ledger.py` or
   `packages/orchestration/prompt_segments.py`.
5. `packages/orchestration/prompt_trace.py` changes ONLY as SPEC D
   describes: one dataclass field and one derivation. No existing line is
   edited or deleted, and `build_trace_entry`'s signature does NOT gain a
   parameter — the value comes from `composed_prompt` and from nothing
   else, for the reason that function's own docstring already gives about
   `segment_manifest`.
6. Do not touch `packages/orchestration/pingpong_loop.py`. Both roles
   already pass `composed_prompt=` at every append, so the field is fed
   with no loop change; verify that rather than assuming it.
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

G1 TRANSPORT. `sha256sum .remedy-wt/f109-r13.md .agent/authored/f109-r13.md
   .agent/last_block.md` prints ONE digest three times. Report it. This
   chain compares the scratch original against the saved copy against its
   mirror and claims nothing about any earlier bytes.

G2 THE PLAN. Extract SLICE PLAN mechanically from
   `.agent/authored/f109-r13.md` (index of the opening `<<<SLICE PLAN`
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
   (d) COUNTS, AND THE OPEN SET IS A SET DIFFERENCE, NEVER A SUBTRACTION —
       this is `R-0778`, discharged in the same round that registers it.
       Collect the ids matched by `^- (R-\d{4}) — ` and the ids matched by
       `^Done: (R-\d{4}) — ` and report: registered ids, DISTINCT registered
       ids, `Done:` LINES, DISTINCT resolved ids, and the size of the set
       difference. Against `7b423b1a` those read 337 / 337 / 65 / 63 / 274;
       after this round the registered count is 339 and the open set is 276,
       with `Done:` lines and distinct resolved ids both UNCHANGED because
       this round resolves nothing. Also report
       `grep -c '^Gate: F109 R12 — '` as 1 and `grep -c '^- R-077[78] — '`
       as 2. Read every base reading from
       `git show 7b423b1a:.agent/live_review.md`, never by rewinding the
       tracked file.

G4 THE EDIT SHAPE, read from `git show <sha>:<path>` blobs and never by
   writing a revision over the tracked file. Compare blobs as SEQUENCES OF
   LINES with `difflib.SequenceMatcher(None, before, after,
   autojunk=False)`.
   (a) ACROSS C4 on `packages/orchestration/prompt_trace.py`: every
       non-equal opcode is an `insert`; none is `replace` or `delete`.
       Report the opcodes and TOTAL LINES DELETED, which is 0.
   (b) ACROSS C3 and C5: these edit existing lines, so a non-zero deletion
       count is EXPECTED and is not a defect. THE PROPERTY THAT MUST HOLD
       IS THAT NO TEST WAS LOST: report `grep -c '    def test_'` before
       and after for BOTH test files. C3 changes no test count; C5 ADDS
       cases, so its count RISES and you report by how much.
   (c) THE FIELD IS NOT A ROW KEY: after C4,
       `grep -c 'deduped_segment_names'` in
       `packages/orchestration/prompt_segments.py` is 0 and in
       `packages/orchestration/token_ledger.py` is 0.

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
   (a) NEUTER THE DERIVATION: make the new field always take its empty
       default, by replacing the expression SPEC D adds with `[]`. A named
       case from SPEC E must FAIL. Report the failing node.
   (b) FEED IT THE WRONG SOURCE: derive the field from the manifest's names
       instead of from `deduped_names`, i.e. every segment rather than the
       replaced ones. A named case from SPEC E must FAIL. This is the proof
       that the case pins WHICH names, not merely that a list is non-empty.
   Then remove the worktree and prune, and show that `git worktree list`
   holds only the primary checkout and the four pre-existing
   `remedy/job-*` worktrees.

G6 THE SUITES, run SERIALLY — one process starts, finishes, and only then
   the next. ALL FIFTEEN MUST BE EXIT 0. Base readings measured by the
   reviewer at `7b423b1a`, in parentheses. Only the first two may move, and
   only upward, because only they gain cases. Report yours beside each and
   name any that moved.
     tests/orchestration/test_semantic_dedupe.py            (125)
     tests/orchestration/test_prompt_trace.py                (46)
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
   This list names the suites the change set can REACH, not only the ones
   expected to move: `build_trace_entry` serialises through `asdict`, so a
   new field reaches every reader of `prompt_trace.jsonl`.

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
   a round map, or a completion — together with whether it STILL HOLDS.
   One is already known and SPEC C repairs it, so report it as repaired
   rather than as new. Pay particular attention to
   `packages/orchestration/prompt_trace.py`'s own docstrings, which
   describe what an entry carries and which this round widens. Report the
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

Round 13, session 3. Surface the deduped names into the prompt TRACE:
`PromptTraceEntry` gains `deduped_segment_names`, derived from the composed
prompt at the same seam `segment_manifest` already uses, so the evidence
records what the model did NOT receive again. Round 12 made the trace
honest about WHICH call it describes, which is what this field needed to
inherit. Also book round 12's PASS, register `R-0777` and `R-0778`, and
repair the stale comment `R-0777` names.

## Next Steps

- The measurement fixture on a resumed fixture chain with the savings
  recorded, plus the docs (T003) — the last build slice of the feature.
- The integration gate, then the closure sequence.

## Risks

- A positional selector over source text or over a trace list breaks
  silently whenever a correct change adds a site. `R-0775` was that class;
  prefer selecting by a declared property.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each, so line counts overstate what is resolved.
  That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

<<<SLICE RECORD
Gate: F109 R12 — the round 12 entry. VERDICT PASS, AND THE BRANCH IS GREEN AGAIN, over the range `906532ef..7b423b1a`. THE REVIEWER RE-RAN EVERY SUITE RATHER THAN READING THE HANDBACK: all fifteen are exit 0, with the two repair targets at 125 and 46 — the same TOTALS they held while red, so no case was deleted to buy a colour — and the other thirteen at 173, 34, 27, 120, 37, 101, 93, 64, 22, 20, 13, 14, 42, every one identical to its base at `906532ef`. THE SCOPE HELD: `git diff --name-only 906532ef..7b423b1a -- packages apps` is EMPTY, so round 11's production fix stands untouched and this round repaired only the selectors, which is what a repair round should look like. THE TWO REPAIRS ARE BOTH STRICTER THAN WHAT THEY REPLACED, which was the condition `R-0775` set. The dedupe case now collects each round's Builder traces in order and takes index 0 — the abandoned composition its own comment names — instead of relying on a dict comprehension's last-wins. Both `test_prompt_trace.py` guards now split the module source into ALL append sites and select by the `role="…"` each site declares, asserting arity 2 for the Builder and 1 for the Reviewer, so the fallback append `R-0774` added is guarded for the first time and no future insertion can move a numeral. THE LEDGER, re-measured by the reviewer: registered ids 337, all distinct; `Gate: F109 R11 — ` 1; `Note: R-0774 — ` 1; `- R-0775 — ` and `- R-0776 — ` 1 each. THE TREE is clean and the branch is pushed at `7b423b1a`. THE ROUND'S BEST OUTPUT WAS A MEASUREMENT NOBODY ORDERED: the G8 sweep found that `.agent/live_review.md` carries 65 `Done:` LINES but only 63 DISTINCT resolved ids, because `R-0721` and `R-0725` each have two, so the open-set arithmetic every recent round has reported as a subtraction is wrong by two. That is registered below as `R-0778` and its counter-measure is already in force in the block that registers it. The round also declared, correctly, that SPEC B's premise was false — only the Reviewer docstring carried an index sentence, not both — and applied the spec's intent while saying so, which is the third consecutive round in which a worker has proved the reviewer wrong about the reviewer's own text and been right to.

- R-0777 — Low, A TEST COMMENT IN `tests/orchestration/test_semantic_dedupe.py` STILL DESCRIBES ONE BUILDER TRACE PER FALLBACK ROUND, WHICH `R-0774` MADE FALSE. Raised by the reviewer at the F109 R12 gate, from that round's own G8 staleness sweep, and registered rather than slipped because the wrong state is on disk under `tests/` — the amend0827 rule 2 test. MEASURED at `7b423b1a`: the comment opening `test_a_builder_resume_fallback_sends_full_content_at_either_flag_value` reads "the round 2 Builder trace describes the composition the fallback ABANDONED, not the bytes that left the loop", in the singular, as the justification for reading that case off the CALLS rather than the traces. Since `498d98dc` that round records TWO Builder traces, and the SECOND one describes exactly the bytes that left the loop — so the sentence's reason is now wrong even though its conclusion, to read the calls, remains sound. THE CASE ITSELF IS GREEN and asserts nothing about traces, so nothing is red and no behaviour is wrong; this is prose the next reader meets while deciding whether a trace-based reading would do. WHY IT WAS NOT REPAIRED IN THE ROUND THAT FOUND IT: SPEC A's "Change nothing else in the file" forbade it, the worker declared it rather than widening its change set, and that is the correct behaviour under guardrail G8 — the same shape as `R-0773` two rounds earlier, and the reason the standing staleness sweep exists at all. FIX: restate the comment so it says the round now records TWO Builder traces, the abandoned composition first and then the full-content call, and that reading the CALLS says which bytes left the loop without having to choose between them. Resolved when no comment in that file describes a fallback round as recording a single Builder trace.

- R-0778 — Low, THE OPEN FINDING SET HAS BEEN REPORTED AS A SUBTRACTION AND IS ACTUALLY A SET DIFFERENCE: TWO IDS CARRY TWO `Done:` LINES EACH. Found by the WORKER of F109 R12 during that round's G8 sweep, reported honestly as an aside to a gate that had already passed, and registered here at the reviewer's first opportunity. MEASURED INDEPENDENTLY by the reviewer at `7b423b1a`: `^- (R-\d{4}) — ` matches 337 ids of which 337 are distinct, while `^Done: (R-\d{4}) — ` matches 65 LINES of which only 63 are DISTINCT — `R-0721` and `R-0725` each appear twice — so the true open set is 274 by set difference where the subtraction 337 minus 65 gives 272. Every recent round's handback and gate entry that stated an open count as a subtraction is therefore two too low. WHY LOW: no product state is wrong, no gate is blind and nothing on disk under `packages/`, `apps/` or `tests/` is affected; the defect is an accounting method applied to the record itself. WHY IT IS NOT MERELY A SLIP: it is not one round's arithmetic error but a rule the pre-emission checklist's own item 10 licenses when its "minus" is read as arithmetic rather than as set difference, so it reproduces every time anyone follows it literally, and the two duplicate lines are permanent — the record is append-only and they are NOT to be deleted. THE COUNTER-MEASURE IS ALREADY IN FORCE in the block that registers this finding: its G3(d) orders registered ids, distinct registered ids, `Done:` lines, distinct resolved ids and the SET DIFFERENCE, all five reported separately, and forbids the subtraction. Checklist item 10 itself is FROZEN while this feature is open, per amend0827 rule 4, so its wording is not touched now; the consolidation pass in the closure sequence is where that sentence is corrected, and this finding is the note that pass reads. Resolved when the checklist's open-set rule states a set difference in words that cannot be read as a subtraction, and when no handback in this feature reports an open count computed the other way.
SLICE RECORD

<<<SPEC C
SPEC C — R-0777: THE STALE COMMENT.

File: `tests/orchestration/test_semantic_dedupe.py`. One comment changes.
No assertion, no name and no case is touched, and
`grep -c '    def test_'` is identical before and after.

PAIR C1. TO contains FROM: false, so this is a REWRITE and the obligation
is FROM 0x, TO 1x after the commit. FROM occurs exactly 1 time before it.

FROM:
        # R-0771'S PROPERTY, RE-ASSERTED UNDER THE NEW PARAMETER and read off the
        # CALLS rather than the traces, for the reason SPEC O gives: the round 2
        # Builder trace describes the composition the fallback ABANDONED, not the
        # bytes that left the loop.

TO:
        # R-0771'S PROPERTY, RE-ASSERTED UNDER THE NEW PARAMETER and read off the
        # CALLS rather than the traces. Since R-0774 the fallback round records
        # TWO Builder traces — the composition the fallback ABANDONED first, then
        # the full-content call that actually left the loop — so a trace-based
        # reading would have to choose between them, while the calls say which
        # bytes left the loop without choosing. R-0777 corrected this comment,
        # which described a single trace.
SPEC C

<<<SPEC D
SPEC D — THE TRACE CARRIES WHAT WAS NOT RESENT.

File: `packages/orchestration/prompt_trace.py`. Two insertions and no third.
Nothing already in the file is edited or deleted.

(1) `PromptTraceEntry` gains ONE field, placed immediately after
`segment_manifest_chars` so it sits with the other composition-derived
fields rather than at the end of the dataclass:

    deduped_segment_names: list[str] = field(default_factory=list)

Give it a `#:` comment in the file's own style for those two neighbours,
saying: this is F109; these are the names of the segments whose TEXT this
composition replaced with a dedupe marker, in replacement order; and an
EMPTY list means nothing was deduped, which is the normal case, because
dedupe fires only for a call that RESUMES a session that provably already
received the segment. Say explicitly that empty does NOT mean the prompt
was uncomposed — that is what an empty `segment_manifest` means — because
the two empties are next to each other and a reader will otherwise conflate
them.

(2) `build_trace_entry` sets it from the composed prompt and from nothing
else, mirroring the two fields above it exactly:

    deduped_segment_names=(
        list(composed_prompt.deduped_names) if composed_prompt is not None else []
    ),

DO NOT add a parameter to `build_trace_entry`. The function's own docstring
already explains why `segment_manifest` and `segment_manifest_chars` are
derived from `composed_prompt` rather than passed separately — "a caller
that could set them independently could describe one prompt with another
prompt's manifest" — and the same reasoning governs this field: a caller
that could pass its own list could name segments the prompt never replaced.
Extend that docstring paragraph to say so, naming the new field beside the
two it joins.

`ComposedPrompt.deduped_names` already exists and is already populated by
both compose functions; this round adds no producer, only a reader.
SPEC D

<<<SPEC E
SPEC E — THE TESTS FOR THE NEW FIELD.

Two files. No existing case is edited, renamed or deleted in either; every
case below is ADDED.

IN `tests/orchestration/test_prompt_trace.py` — the unit-level claims,
appended to the class that already covers `segment_manifest`, or to a new
class if that reads better in context:
  1. A `build_trace_entry` call with NO `composed_prompt` yields
     `deduped_segment_names == []`.
  2. A call WITH a composed prompt that replaced nothing yields `[]`.
  3. A call with a composed prompt carrying deduped names yields exactly
     those names, IN ORDER, and as a `list` rather than the source tuple —
     assert the type, because `asdict` serialises this entry to JSON and a
     tuple would round-trip differently.

IN `tests/orchestration/test_semantic_dedupe.py` — the claim that matters,
appended as ONE new class at the very END, driving the REAL loop through
the file's existing fixtures exactly as the neighbouring chain cases do.
Reuse `fallback_repo`, `TestChainAgainstTheRealLoop._provider_pair` and
`._run`; do not build a second fixture that could drift from the first.
  4. A RESUMED CHAIN RECORDS THE NAMES IT DID NOT RESEND. On a chain that
     resumes without falling back, the round 2 trace's
     `deduped_segment_names` is NON-EMPTY, and every name in it also
     appears in that same trace's `segment_manifest` — the marker rows are
     still rows, so the two readings must agree. Assert non-vacuity first:
     the chain really resumed.
  5. THE FALLBACK'S TWO TRACES DISAGREE, AND THAT IS THE POINT. With
     `builder_resume_fails=True`, the fallback round's FIRST Builder trace
     reports a non-empty `deduped_segment_names` and its SECOND reports
     `[]` — the abandoned composition withheld segments, the call that
     actually reached the provider withheld none. This case is what ties
     the new field to `R-0774`'s repair; without that repair the field
     would have reported withheld segments for a call that re-sent them in
     full.
  6. A DISABLED RUN REPORTS NO NAMES ANYWHERE. With
     `semantic_dedupe_enabled=False`, every trace of the run reports `[]`.
     This is the discriminator against the field being wired to something
     other than the dedupe decision.

Assert `prompt_text_truncated is False` on every trace before reading it,
the same guard `_marked_traces` already applies, for the same reason.
SPEC E
