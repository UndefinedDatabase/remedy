STEP T003b — F109 Semantic dedupe — ROUND 12, SESSION 3 — REPAIR ROUND

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Goal: Get the branch green again. Round 11's C4 was CORRECT and stays;
what it broke is two test SELECTORS that silently assumed one Builder
trace per role per round. Repair both by the property they meant to
assert instead of the position they happened to use, book round 11's FAIL,
register `R-0775` and `R-0776`, and append the correction that `R-0774`'s
Reviewer half was false. NO PRODUCTION FILE CHANGES THIS ROUND.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f109-r12.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   apply SLICE PLAN to `.agent/plan.md`
  C2   append SLICE RECORD to `.agent/live_review.md`
  C3   apply SPEC A to `tests/orchestration/test_semantic_dedupe.py`
  C4   apply SPEC B to `tests/orchestration/test_prompt_trace.py`
  C5   rewrite `.agent/handoff.md`

Change set — exactly these seven paths and no eighth:
  `.agent/authored/f109-r12.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `tests/orchestration/test_semantic_dedupe.py`
  `tests/orchestration/test_prompt_trace.py`
  `.agent/handoff.md`

Constraints:

1. Every authored slice is applied BYTE FOR BYTE. This block reached you as
   a file: `cp` it from `/home/decodeux/Repos/remedy/.remedy-wt/f109-r12.md`
   into `.agent/authored/f109-r12.md` and `cp` that into
   `.agent/last_block.md`. Never retype either.
2. The commit order above is FIXED. C1 advances `.agent/plan.md` as the
   FIRST substantive commit because this round touches the finding ledger.
3. YOU WRITE NO `Done:` PARAGRAPH AND NO VERDICT OF YOUR OWN. SLICE RECORD
   carries the reviewer-authored text; apply it and add nothing. `R-0775`
   and `R-0776` are REGISTERED this round and resolved by a later one, so
   do not mark either resolved however green the suite ends.
4. NO FILE UNDER `packages/` OR `apps/` IS TOUCHED. Round 11's C4 is
   correct and stays exactly as it is. If a gate below tempts you to
   change production code to make a test pass, that is the wrong repair:
   stop and declare it.
5. UNLIKE ROUND 11, EDITING EXISTING LINES IS THE POINT. SPEC A and SPEC B
   both rewrite lines already in their files. What stays forbidden is
   DELETING a test, weakening an assertion, or loosening a guard to make a
   colour: every repair below makes its guard STRICTER than it was.
6. Do not add a new test case to either file this round. Both files already
   carry the cases; this round fixes how two of them SELECT what they read.
7. Every gate G1-G8 runs at C4 or earlier, so the handback can quote every
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

G1 TRANSPORT. `sha256sum .remedy-wt/f109-r12.md .agent/authored/f109-r12.md
   .agent/last_block.md` prints ONE digest three times. Report it. This
   chain compares the scratch original against the saved copy against its
   mirror and claims nothing about any earlier bytes.

G2 THE PLAN. Extract SLICE PLAN mechanically from
   `.agent/authored/f109-r12.md` (index of the opening `<<<SLICE PLAN`
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
   (d) COUNTS. `grep -c '^Gate: F109 R11 — '` is 1. `grep -c '^- R-0775 — '`
       is 1. `grep -c '^- R-0776 — '` is 1. `grep -c '^Note: R-0774 — '`
       is 1. `grep -c '^- R-[0-9]\{4\} — '` is 337 against 335 at
       `906532ef`. `grep -c '^Done: R-[0-9]\{4\} — '` is UNCHANGED at 65.
       Read every base count from `git show 906532ef:.agent/live_review.md`,
       never by rewinding the tracked file.

G4 THE EDIT SHAPE, read from `git show <sha>:<path>` blobs and never by
   writing a revision over the tracked file. These are REPLACE-shaped
   edits, so unlike round 11 a non-zero deletion count is EXPECTED and is
   not a defect. Compare the blobs as SEQUENCES OF LINES with
   `difflib.SequenceMatcher(None, before, after, autojunk=False)` for each
   of C3 and C4 and report the opcodes. THE PROPERTY THAT MUST HOLD IS
   THAT NO TEST WAS LOST: `grep -c '    def test_'` is IDENTICAL before and
   after in each file. Report both numbers for both files.

G5 THE COLOUR — THREE RED-PROOFS, each with its UNMUTATED CONTROL reported
   beside it, because a colour with no baseline is not evidence. In a
   disposable worktree added BY EXACT PATH under `.remedy-wt/`, checked out
   at C4. RUN THE IMPORT PROBE FIRST: `python3 -B -c "import
   packages.orchestration.pingpong_loop as m; print(m.__file__)"` with the
   worktree as cwd must resolve INSIDE the worktree, or an editable install
   is shadowing it and the gate is void. Purge `__pycache__` before every
   run; every process is `python3 -B` with `-p no:cacheprovider`. Before
   each write, count the bytes you are about to change IN THAT FILE and
   report the count; where it is not 1, quote a longer UNIQUE string and
   say which occurrence you took. Restore from the C4 blob by exact path
   between mutations and after the last.
   (a) In `packages/orchestration/pingpong_loop.py`, delete
       `composed_prompt=reviewer_composed,` from the Reviewer append. THE
       REPAIRED REVIEWER GUARD IN `test_prompt_trace.py` MUST FAIL. This is
       the guard's original purpose and the repair must not have cost it.
   (b) In the same file, delete `composed_prompt=builder_composed,` from
       the BUILDER FALLBACK append that round 11's C4 added — NOT the
       primary one; the two are distinguished by the fallback's own comment
       above it, so quote a string that includes part of that comment. THE
       REPAIRED BUILDER GUARD MUST FAIL. The old positional guard could not
       see this site at all, so this proof is the repair's whole point.
   (c) In the same file, delete the Builder fallback's recomposition
       statement `builder_composed = compose_builder_prompt(effective_goal,
       context, **builder_compose_args)`. THE REPAIRED DEDUPE CASE
       `test_the_recorded_builder_row_describes_the_bytes_that_were_sent`
       MUST FAIL — that statement is the `R-0771` repair, and this case
       exists to keep it from rotting.
   Then remove the worktree and prune, and show that `git worktree list`
   holds only the primary checkout and the four pre-existing
   `remedy/job-*` worktrees.

G6 THE SUITES, run SERIALLY — one process starts, finishes, and only then
   the next. ALL FIFTEEN MUST BE EXIT 0; that is this round's whole point.
   Base readings measured by the reviewer at `906532ef`, in parentheses.
   The first two are the ROUND'S TARGET and are the only ones that may
   move: each currently holds ONE failing case and must reach the same
   TOTAL with zero failures. Report yours beside each and name any that
   moved.
     tests/orchestration/test_semantic_dedupe.py   (125 total: 124 passed, 1 FAILED)
     tests/orchestration/test_prompt_trace.py       (46 total:  45 passed, 1 FAILED)
     tests/orchestration/test_pingpong_cli.py               (173 passed)
     tests/orchestration/test_pingpong.py                    (34 passed)
     tests/orchestration/test_session_resume.py              (27 passed)
     tests/orchestration/test_token_ledger.py               (120 passed)
     tests/orchestration/test_token_truth.py                 (37 passed)
     tests/orchestration/test_token_truth_v1_contract.py    (101 passed)
     tests/orchestration/test_job_evidence.py                (93 passed)
     tests/orchestration/test_provider_evidence_integration.py (64 passed)
     tests/orchestration/test_cost_report.py                 (22 passed)
     tests/ui_server/test_prompt_trace_payload.py            (20 passed)
     tests/ui_server/test_prompt_trace_lens.py               (13 passed)
     tests/test_observability_index.py                       (14 passed)
     tests/cli/test_golden_path.py                           (42 passed)

G7 THE TREE. `git status --porcelain` EMPTY. `git ls-files .remedy-wt`
   returns nothing. Report the insertion count of C0a through C4 from
   `git show --numstat` — the `+` column only, per AGENTS.md DECISION
   F104 D1 — and confirm each is under 500. Confirm every commit is
   single-parent with `git log --format="%h parents=%p"`. Compare those
   numbers CELL BY CELL against your own `## Commits` table and state
   plainly that you ran that comparison.

G8 THE STALENESS SWEEP (finding `R-0417`'s standing counter-measure, which
   is OPEN and binding). For EACH file this round touched, re-read it end
   to end and report every sentence that states a count, a list of modules,
   a round map, or a completion — together with whether it STILL HOLDS.
   Two are already known and SPEC A and SPEC B both repair them, so report
   them as repaired rather than as new: the dedupe case's own comment about
   what the round 2 trace records, and the two `test_prompt_trace.py`
   docstrings naming index positions. Report the sweep even where it finds
   nothing more, and repair nothing outside the change set — declare it.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
It carries the state block, the item-status table with every C0a-C5 item
present exactly once, the changed-files table, one line per gate with real
readings, the deviations, the open-findings count, and — mandatory — the
SESSION NUMBER, which is 3. It has no length cap. Then push.

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

Round 12, session 3, a REPAIR round. Round 11 landed the correct fix for
`R-0774` on the Builder side and ended RED: two test selectors assumed one
Builder trace per role per round, and a second, honest trace falsified
them. Repair both by the property they meant to assert rather than the
position they used, book round 11's FAIL, register `R-0775` and `R-0776`,
and record that `R-0774`'s Reviewer half was false — that role already
recorded two traces before the round began. No production file changes.

## Next Steps

- Surface the deduped names as a first-class `deduped_segment_names` field
  on `PromptTraceEntry`, derived from `composed_prompt.deduped_names` at
  the same seam `segment_manifest` already uses. The manifest ROW KEYS
  STAY CLOSED: `token_ledger.py`'s `call_segments` table mirrors them
  column for column, so widening a row is a token-ledger change.
- The measurement fixture on a resumed fixture chain with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- A positional selector over source text or over a trace list breaks
  silently whenever a correct change adds a site. `R-0775` is that class;
  prefer selecting by a declared property.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

<<<SLICE RECORD
Gate: F109 R11 — the round 11 entry. VERDICT FAIL, AND THE FAULT IS THE REVIEWER'S ON THREE COUNTS WHILE THE ROUND'S EXECUTION WAS EXEMPLARY, over the range `c22818f59e6f52ea79b10cb0f36390c5070322c7..906532ef`. THE ROUND ENDS RED AND THE WORKER SAID SO RATHER THAN ROUTING AROUND IT: `tests/orchestration/test_semantic_dedupe.py` is exit 1 at 124 passed 1 failed and `tests/orchestration/test_prompt_trace.py` is exit 1 at 45 passed 1 failed, both independently reproduced by the reviewer at the tip. WHAT LANDED AND IS CORRECT: `R-0773`'s three docstring repairs, verified by the reviewer with the zero-gate `grep -c 'config plumbing that supplies'` over `packages/orchestration/pingpong_loop.py` reading 0 against 2 at `c22818f5`, and the replacement text present 3 times; and C4's Builder second trace append, which does exactly what `R-0774` ordered. THE THREE REVIEWER DEFECTS. FIRST, `R-0774`'s REVIEWER HALF WAS FALSE and is corrected in the `Note:` paragraph below. SECOND, gate G4(a) WAS UNMEETABLE AS ORDERED: it demanded `ast.dump(tree, include_attributes=False)` be EQUAL across a commit that changes only docstrings, and that dump renders `Constant` values, so no docstring edit can satisfy it — the reviewer independently reproduced this with a two-function control, and the worker had already proved it and correctly continued after showing the stop clause's antecedent false. Registered as `R-0776`. THIRD, and the reason the round is FAIL rather than PASS, THE BLOCK ORDERED A CHANGE WHOSE RIPPLE ITS OWN CONSTRAINTS FORBADE REPAIRING: constraint 6 barred editing any existing line of the dedupe suite and `tests/orchestration/test_prompt_trace.py` was not in the change set at all, so neither break was fixable inside the round's authority. Registered as `R-0775`. THE GATE LIST DID ITS JOB, which is the one thing to keep from this round: `test_prompt_trace.py` was named in G6 ONLY because `R-0772` taught that a gate list must name the suites a change can REACH rather than the ones it expects to move, and it is exactly the suite that moved without being touched. THE OTHER THIRTEEN SUITES were re-run by the reviewer at the tip and are unchanged and green: 173, 34, 27, 120, 37, 101, 93, 64, 22, 20, 13, 14, 42. THE LEDGER, re-measured against `git show c22818f5…:.agent/live_review.md`: `- R-` rose 333 to 335, `Done: R-` unchanged at 65, `Gate: F109 R10 — ` 1, `- R-0773 — ` 1, `- R-0774 — ` 1. THE TREE is clean and the branch is pushed. NO BLOCK CONDITION OF §4 ITEM 5 IS MET — nothing was fabricated, no indicator is false, the changed-files table is present and accurate, and every deviation was declared before review; the FAIL is the red tip, and the round that produced it behaved exactly as a worker should when a correct change meets a constraint that forbids completing it.

Note: R-0774 — CORRECTION, appended rather than rewritten because this record is append-only and a dated wrong sentence is better than an overwritten one. `R-0774`'s REVIEWER HALF WAS FALSE. The finding stated "The Reviewer side is the same shape: append at 3658, call at 3699, fallback recomposition at 3738", and that sentence was produced by grepping `build_trace_entry` for line numbers and generalising the Builder's structure to the Reviewer WITHOUT reading the enclosing code — an inference presented as a measurement, which is the `R-0747` move this record exists to catch. THE TRUTH, measured at `906532ef` by the reviewer: line 3695 defines a closure `_rev_trace`, and the Reviewer's traces are written through `on_call=_rev_trace(...)` passed to `_call_with_retry` at the primary call, at the FALLBACK call and at the parse-retry call. `_call_with_retry` fires that callback once per ACTUAL provider invocation and `_rev_trace` reads `reviewer_composed` at call time, so the Reviewer already picked up the fallback rebinding and already recorded a second, full-content entry BEFORE round 11 began. `R-0774`'s own "Resolved when" clause was therefore already satisfied for that role at `c22818f5`. The Builder half of the finding was correct and its fix landed at `498d98dc`. THE ROUND 11 WORKER CAUGHT THIS, refused to apply SPEC Y's Reviewer half on the ground that it would write a THIRD entry and double-count one provider call in `prompt_trace.jsonl` and `call_segments`, and declared the refusal loudly instead of applying an order it had measured to be wrong — which is precisely what AGENTS.md's Commit Gate requires and is the correct behaviour under self-drive guardrail G8. It additionally left a deliberate-absence comment at the Reviewer fallback naming `R-0774` and stating why no append belongs there, which is the discoverability convention AGENTS.md asks for, applied unprompted. `R-0774` remains OPEN: the Builder half is fixed and the Reviewer half needs no fix, but the finding is not resolved until `R-0775`'s repair makes the suite green, because its own resolution clause requires a named test to go red on deleting the new append and that test is currently one of the two that are red.

- R-0775 — High, THE BRANCH TIP SHIPS A RED SUITE: TWO TEST SELECTORS ASSUMED ONE BUILDER TRACE PER ROLE PER ROUND AND A CORRECT SECOND TRACE FALSIFIED THEM. Registered by the reviewer at the F109 R11 gate, against the reviewer's own block. MEASURED independently at `906532ef`: `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py tests/orchestration/test_prompt_trace.py -q` reads exit 1 at 2 failed, 169 passed. THE TWO BREAKS ARE THE SAME CLASS — A POSITIONAL SELECTOR OVER A LIST THAT GREW — arriving in two different materials. (1) `test_the_recorded_builder_row_describes_the_bytes_that_were_sent` builds `traces = {trace.round: ... for trace in result.prompt_traces if trace.role == "builder"}`, a dict comprehension that is LAST-WINS per round, so `traces[2]` used to be the abandoned resumed composition and is now the full-content one; its positive control `assert replaced, sorted(traces[2])` then fails because the full-content composition replaced nothing. The case's own comment already states which composition it needs — "the round 2 Builder trace records the manifest of the composition the fallback ABANDONED" — so the selector, not the intent, is what broke. (2) `test_the_reviewer_call_site_hands_its_composition_down` takes `source.split("result.prompt_traces.append(build_trace_entry(")[2]` as the Reviewer's append, and round 11's C4 inserted a third append earlier in the file, so index 2 now resolves to the BUILDER's fallback site and the guard fails on `assert 'role="reviewer",' in site`. Its sibling `test_the_builder_call_site_hands_its_composition_down` takes index 1, still resolves, and is GREEN — which is worse than red, because it means the same latent trap survives untripped in the same file, and it does not guard the new fallback append at all. THE FAULT IS THE REVIEWER'S, TWICE: §3 item 7 orders a grep of the suite for guards over a file BEFORE ordering an addition to it, and the round 11 block ran that check for closed KEY SETS over the trace record and never for POSITIONAL selectors over the trace LIST or over the module source; and the block's own constraint 6 then forbade editing any existing line of the dedupe suite while `test_prompt_trace.py` was not in its change set, so an honest worker could not repair either break and correctly stopped. WHY HIGH: a red branch tip blocks the integration gate and therefore blocks closure, which is exactly the severity `R-0772` carried for the same symptom on the same branch. FIX, and it must make each guard STRICTER rather than merely green: select by the property the assertion is about, never by position. For (1), take the FIRST Builder trace of the round — the abandoned composition the case's own comment names — rather than relying on dict last-wins, and update that comment to say the round now records two. For (2), split the source into ALL append sites and select by the `role="..."` each site declares, asserting the Reviewer has exactly one and that BOTH Builder sites hand their composition down, so the fallback append round 11 added is guarded too and no future insertion can move a numeral. Resolved when all fifteen suites the round 12 block names are exit 0, and when deleting `composed_prompt=builder_composed,` from the Builder FALLBACK append alone turns the repaired Builder guard red.

- R-0776 — Low, A GATE OVER PRODUCTION CODE WAS UNMEETABLE BY CONSTRUCTION: G4(a) DEMANDED AN AST DUMP BE EQUAL ACROSS A COMMIT THAT CHANGES DOCSTRINGS. Registered by the reviewer at the F109 R11 gate, against the reviewer's own block, under amend0827 rule 2's clause for a gate over production code shown to be blind or unmeetable. THE ORDER: round 11's G4(a) required `ast.parse` of `packages/orchestration/pingpong_loop.py` before and after C3 and demanded `ast.dump(tree, include_attributes=False)` be EQUAL, on the stated reasoning that "SPEC X changes docstring prose only, and a docstring is an expression". THE MEASUREMENT, taken independently by the reviewer: a docstring is an `Expr` wrapping a `Constant`, and `include_attributes=False` suppresses line and column attributes ONLY, not VALUES, so the dump renders the docstring text itself — two functions differing only in their docstring produce unequal dumps. The gate could therefore never pass for the commit it was written for, and its own stop clause ("If it did not, SPEC X was misapplied: stop and declare it") would have halted a round whose slice was applied perfectly. THE ROUND 11 WORKER HANDLED IT CORRECTLY: it recorded the real red, proved the antecedent false with a three-line control, showed by a stripped-docstring comparison that the module's executable statements were genuinely untouched (23625 nodes on both sides, exactly the three intended docstrings differing), and continued. WHY LOW AND NOT HIGHER: no product state is wrong, no test was weakened, and the property the gate MEANT to establish was established by the worker's own stronger reading; the cost was a declared deviation on a round that did nothing wrong — the same shape as `R-0252`, whose lesson is item 5 of the pre-emission checklist. FIX: where a gate must prove that a prose-only commit changed no executable statement, compare the AST with docstrings STRIPPED — walk the tree and drop the leading `Expr(Constant(str))` of every module, class and function body before dumping — or compare `co_consts`-free structural summaries; and never assert equality of a representation that renders the very bytes the commit changes. Resolved when a later block orders such a proof in a form that a correct prose-only commit can actually satisfy, and states which reading it used.
SLICE RECORD

<<<SPEC A
SPEC A — R-0775 (1): SELECT THE COMPOSITION THE CASE IS ABOUT.

File: `tests/orchestration/test_semantic_dedupe.py`. One case changes:
`test_the_recorded_builder_row_describes_the_bytes_that_were_sent`.

THE DEFECT. The case builds a dict keyed by `trace.round` over the Builder
traces. A dict comprehension is LAST-WINS, so before round 11 `traces[2]`
was the round's only Builder trace — the ABANDONED resumed composition —
and it is now the SECOND, full-content one, which replaced nothing. The
positive control `assert replaced, sorted(traces[2])` therefore fails.

THE REPAIR. Keep every assertion. Change only WHICH trace the case reads,
so it reads the one its own comment already names: the FIRST Builder trace
of the round, which is the composition the fallback abandoned. Take it
explicitly — collect the Builder traces of each round in order and take
index 0 — rather than by relying on a dict's overwrite order in either
direction, so the selection states what it means and a third trace could
not silently change it again.

ALSO UPDATE THE CASE'S OWN COMMENT, which is now stale in one sentence: it
says "the round 2 Builder trace records the manifest of the composition the
fallback ABANDONED" as though there were one. Say instead that the round
now records TWO Builder traces — the abandoned resumed composition first,
then the full-content call that actually reached the provider — and that
this case reads the FIRST because the names the abandoned composition
replaced are what the assertion is about. Name `R-0774` as the round that
added the second and `R-0775` as the finding this repair closes.

Change nothing else in the file. No case is added, renamed or deleted, and
`grep -c '    def test_'` is identical before and after.
SPEC A

<<<SPEC B
SPEC B — R-0775 (2): GUARD THE SITES BY THE ROLE THEY DECLARE.

File: `tests/orchestration/test_prompt_trace.py`. Two cases change:
`test_the_builder_call_site_hands_its_composition_down` and
`test_the_reviewer_call_site_hands_its_composition_down`.

THE DEFECT. Each splits the module source on
`result.prompt_traces.append(build_trace_entry(` and takes a FIXED INDEX —
`[1]` for the Builder, `[2]` for the Reviewer. Round 11's C4 added a
Builder append in the resume-fallback branch, so `[2]` is now that new
Builder site and the Reviewer guard fails. The Builder guard still passes
by luck, and guards only the primary site.

THE REPAIR, applied to BOTH cases. Split the source into ALL append sites
once — every part after the first, each truncated at its own `))` — and
select by the `role="..."` the site itself declares, never by position.

For the REVIEWER case: exactly ONE site declares `role="reviewer",`. Assert
that arity, take that site, and keep the existing assertions on it
unchanged (`prompt_text=prompt_text,` and
`composed_prompt=reviewer_composed,`).

For the BUILDER case: exactly TWO sites declare `role="builder",` — the
primary and the fallback append `R-0774` added. Assert that arity and then
assert of EVERY one of them that it carries `prompt_text=builder_prompt,`
and `composed_prompt=builder_composed,`. This is strictly stronger than the
old guard: it pins the fallback append, which no index reached before.

UPDATE BOTH DOCSTRINGS. Each currently explains the index it used —
"Index [2] is the reviewer's `build_trace_entry` append; [1] is the
builder's" — and that sentence is exactly the fragility being removed.
Replace it with the property the case now asserts, naming `R-0774` as the
change that added the second Builder site and `R-0775` as the finding that
made the selector positional-free. Leave every other sentence of both
docstrings, including the `R-0771` paragraph about the composition count,
untouched and true.

Change nothing else in the file. No case is added, renamed or deleted, and
`grep -c '    def test_'` is identical before and after.
SPEC B
