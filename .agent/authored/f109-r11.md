STEP T003a — F109 Semantic dedupe — ROUND 11, SESSION 3

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Goal: Book round 10's PASS, register `R-0773` and `R-0774`, and fix both.
`R-0773` is three docstring passages in `pingpong_loop.py` that still call
F109's config plumbing absent after round 10 landed it. `R-0774` is the
prompt TRACE describing the ABANDONED resumed composition on a resume
fallback instead of the full-content call that actually reached the
provider. The trace fix comes FIRST, before the next round surfaces the
deduped names as a trace field, so that field inherits an honest record
instead of turning a misleading paragraph into a structured false claim.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f109-r11.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   apply SLICE PLAN to `.agent/plan.md`
  C2   append SLICE RECORD to `.agent/live_review.md`
  C3   apply SPEC X to `packages/orchestration/pingpong_loop.py`
  C4   apply SPEC Y to `packages/orchestration/pingpong_loop.py`
  C5   apply SPEC Z to `tests/orchestration/test_semantic_dedupe.py`
  C6   rewrite `.agent/handoff.md`

Change set — exactly these seven paths and no eighth:
  `.agent/authored/f109-r11.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `packages/orchestration/pingpong_loop.py`
  `tests/orchestration/test_semantic_dedupe.py`
  `.agent/handoff.md`

Constraints:

1. Every authored slice is applied BYTE FOR BYTE. This block reached you as
   a file: `cp` it from `/home/decodeux/Repos/remedy/.remedy-wt/f109-r11.md`
   into `.agent/authored/f109-r11.md` and `cp` that into
   `.agent/last_block.md`. Never retype either. A slice is never edited to
   fit, however wrong it looks; declare it in the handback instead.
2. The commit order above is FIXED. C1 advances `.agent/plan.md` as the
   FIRST substantive commit because this round touches the finding ledger.
3. YOU WRITE NO `Done:` PARAGRAPH AND NO VERDICT OF YOUR OWN. SLICE RECORD
   already carries the reviewer-authored text. Apply it and add nothing.
4. `packages/orchestration/pingpong_loop.py` changes ONLY as SPEC X and
   SPEC Y describe. SPEC X changes docstring prose and no executable
   statement; SPEC Y adds two `build_trace_entry` appends and nothing else.
   No signature moves, no helper is extracted, no primary append is edited.
5. Do NOT touch `packages/orchestration/prompt_trace.py`,
   `packages/orchestration/prompt_segments.py` or
   `packages/orchestration/token_ledger.py`. Adding a
   `deduped_segment_names` field is the NEXT round's work and anticipating
   it here would put an untested field under an unreviewed gate.
6. `tests/orchestration/test_semantic_dedupe.py` gains ONE appended class at
   the very END. Zero existing lines are edited, reordered or deleted. The
   one named exception: if a name SPEC Z uses is genuinely not already
   imported or defined in that file, extend the import — and report in the
   handback whether you had to.
7. Every gate G1-G8 runs at C5 or earlier, so the handback can quote every
   reading. The handback commit's own insertion count is NOT quoted
   anywhere in it; the reviewer measures that one.
8. Re-read `.agent/STOP` from disk before your first action and again
   before the handback. If it exists, finish any half-written commit, write
   the handback and end.
9. Destructive verification — G5's mutations and G3's negative control —
   runs ONLY inside a disposable `git worktree` or on a scratch copy, each
   addressed BY EXACT PATH under `.remedy-wt/`, never in the primary
   checkout. Remove and prune what you create, delete scratch copies by
   exact path, and confirm `git status --porcelain` is EMPTY afterwards.
10. Push after the handback commit. Create no PR. Merge nothing. Never
    force-push. Stay on `feature/f109-semantic-dedupe`.

Done when — EIGHT GATES, every one executed with its real exit code
recorded, one line per gate in the handback:

G1 TRANSPORT. `sha256sum .remedy-wt/f109-r11.md .agent/authored/f109-r11.md
   .agent/last_block.md` prints ONE digest three times. Report it. This
   chain compares the scratch original against the saved copy against its
   mirror; it claims nothing about any earlier bytes.

G2 THE PLAN. Extract SLICE PLAN mechanically from
   `.agent/authored/f109-r11.md` (index of the opening `<<<SLICE PLAN`
   line, index of the closing `SLICE PLAN` line, everything between) and
   `cmp` it against `.agent/plan.md`: no output, exit 0. `wc -l
   .agent/plan.md` is strictly under 50. `grep -c '^## Goal'` is 1 and
   `grep -c '^## Next Steps'` is 1.

G3 THE RECORD APPEND, four readings.
   (a) ARITHMETIC. Report base `.agent/live_review.md` size and sha256,
       the appended length S after stripping trailing newlines, and that
       base + S equals the new size exactly. Report the new sha256. The
       file still ends WITHOUT a trailing newline.
   (b) A SECOND, STRUCTURALLY DIFFERENT READER that counts no byte: split
       the WHOLE file on blank-line boundaries into units, COUNT N from the
       payload itself rather than taking it from this block, and assert the
       LAST N units equal the appended paragraphs IN ORDER. Report N and
       the first characters of each.
   (c) NEGATIVE CONTROL on a scratch copy at an exact path under
       `.remedy-wt/`, never on the tracked file: flip one byte INSIDE THE
       FIRST appended paragraph and confirm reader (b) REJECTS it while it
       accepted the tracked file. Report the tracked file's sha256 before
       and after to show it did not move, then delete the copy by exact
       path and confirm its absence.
   (d) COUNTS. `grep -c '^Gate: F109 R10 — '` is 1. `grep -c '^- R-0773 — '`
       is 1. `grep -c '^- R-0774 — '` is 1. `grep -c '^- R-[0-9]\{4\} — '`
       is 335 against 333 at `c22818f59e6f52ea79b10cb0f36390c5070322c7`.
       `grep -c '^Done: R-[0-9]\{4\} — '` is UNCHANGED at 65, because this
       round resolves nothing. Read every base count from
       `git show c22818f5…:.agent/live_review.md`, never by rewinding the
       tracked file.

G4 THE EDIT SHAPE, read from `git show <sha>:<path>` blobs and never by
   writing a revision over the tracked file.
   (a) ACROSS C3: parse the module before and after with `ast.parse` and
       compare `ast.dump(tree, include_attributes=False)`. THE TWO MUST BE
       EQUAL — SPEC X changes docstring prose only, and a docstring is an
       expression, so state plainly whether equality held. If it did not,
       SPEC X was misapplied: stop and declare it.
   (b) ACROSS C4: compare the blobs as SEQUENCES OF LINES with
       `difflib.SequenceMatcher(None, before, after, autojunk=False)`.
       Every non-equal opcode is an `insert`; none is `replace` or
       `delete`. Report the opcodes and TOTAL LINES DELETED, which is 0.
   (c) ACROSS C5: the same line-sequence reading over the test file. One
       `insert` opcode at the END of the file, TOTAL LINES DELETED 0.
   (d) THE ZERO-GATE, scoped to `packages/orchestration/pingpong_loop.py`
       alone and to no other path: after C3,
       `grep -c 'config plumbing that supplies'` in THAT FILE is 0, against
       2 at `c22818f59e6f52ea79b10cb0f36390c5070322c7`.

G5 THE COLOUR. In a disposable worktree added BY EXACT PATH under
   `.remedy-wt/`, checked out at C5. RUN THE IMPORT PROBE FIRST:
   `python3 -B -c "import packages.orchestration.pingpong_loop as m;
   print(m.__file__)"` with the worktree as cwd must resolve INSIDE the
   worktree, or an editable install is shadowing it and the gate is void.
   Purge `__pycache__` before every run; every process is `python3 -B` with
   `-p no:cacheprovider`.
   (a) CONTROL, unmutated: report exit code and passed count.
   (b) MUTATION A: delete the BUILDER's new `build_trace_entry` append from
       the fallback branch. A named case of SPEC Z case 1 must FAIL. Report
       the exit code, the counts and the failing node.
   (c) MUTATION B: delete the REVIEWER's new append instead. A named case
       of SPEC Z case 2 must FAIL. Same reporting.
   Before each write, count the bytes you are about to change IN THAT FILE
   and report the count — it must be 1, and where it is not, quote a longer
   UNIQUE string and say which occurrence you took. Restore from the C5
   blob by exact path between mutations and after the last, then confirm
   `git status --porcelain` inside the worktree is EMPTY. Remove the
   worktree and prune, and show that `git worktree list` holds only the
   primary checkout and the four pre-existing `remedy/job-*` worktrees.

G6 THE SUITES, run SERIALLY — one process starts, finishes, and only then
   the next. All fifteen must be exit 0. Base readings, measured by the
   reviewer at `c22818f59e6f52ea79b10cb0f36390c5070322c7`, in parentheses;
   report yours beside each and name any that moved:
     tests/orchestration/test_semantic_dedupe.py            (122)
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
   expected to move: every one of them reads a prompt trace or drives
   `run_pingpong`. Only the dedupe suite is expected to rise.

G7 THE TREE. `git status --porcelain` EMPTY. `git ls-files .remedy-wt`
   returns nothing. Report the insertion count of C0a through C5 from
   `git show --numstat` — the `+` column only, per AGENTS.md DECISION
   F104 D1, never insertions plus deletions and never a before/after line
   count of a rewritten file — and confirm each is under 500. Confirm every
   commit is single-parent with `git log --format="%h parents=%p"`. Compare
   those numbers CELL BY CELL against your own `## Commits` table and state
   plainly that you ran that comparison.

G8 THE STALENESS SWEEP (finding `R-0417`'s standing counter-measure, which
   is OPEN and binding). For EACH file this round touched, re-read it end
   to end and report every sentence that states a count, a list of modules,
   a round map, or a completion — together with whether it STILL HOLDS
   after this round's own commits. This round is where that gate earns its
   place twice over: C3 exists because round 10 falsified prose it was
   forbidden to repair, and C4 changes what the loop RECORDS, so any
   sentence anywhere in `pingpong_loop.py` or the dedupe suite that
   describes trace behaviour is a candidate. Report the sweep even when it
   finds nothing, and repair nothing outside the change set — declare it.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
It carries the state block, the item-status table with every C0a-C6 item
present exactly once, the changed-files table, one line per gate with real
readings, the deviations, the open-findings count, and — mandatory, since
this is session 3 — the SESSION NUMBER of the running feature. It has no
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

Round 11, session 3. Book round 10's PASS, register `R-0773` and `R-0774`,
and fix both. `R-0773` is three docstring passages in `pingpong_loop.py`
that still call F109's config plumbing absent after round 10 landed it.
`R-0774` is the prompt TRACE describing the abandoned resumed composition
on a resume fallback rather than the full-content call that actually
reached the provider; the fix appends a second trace in each role's
fallback branch, so one trace exists per real provider invocation.

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

- A suite that no round gate names can go red without anyone seeing it.
  That is what `R-0772` was. Every block from here names the suites its
  change set can REACH, not only the ones it expects to move.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

<<<SLICE RECORD
Gate: F109 R10 — the round 10 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ FROM THE HANDBACK, over the range `d7fbff5b99d35e1601c6001086a508187eaed323..c22818f59e6f52ea79b10cb0f36390c5070322c7`. THE TRANSPORT: `sha256sum .agent/authored/f109-r10.md .agent/last_block.md` prints `3a8ef357639196c7bc40e0c98dba54ac49f4224832dae0fd6ca843cb2f6011d5` twice; that chain compares the saved copy against its mirror and claims nothing about the emitted bytes. THE PLAN: 45 lines, `^## Goal` 1, `^## Next Steps` 1. THE LEDGER, re-measured against `git show d7fbff5b…:.agent/live_review.md` rather than against the handback: `Done: R-` rose 64 to 65, `- R-` unchanged at 333, `Gate: F109 R9 — ` 0 to 1, and `Landed: R-0772 — ` still reads 1, standing beside its new `Done:` paragraph as the record requires. THE PRODUCTION DIFF, read in full rather than sampled: `packages/orchestration/pingpong_loop.py` gains one parameter, one docstring paragraph and two keyword arguments, with ZERO lines deleted. The claim that the two resume-fallback recompositions stay outside the flag was verified NOT by reading the comment that asserts it but by reading `builder_compose_args`, the dict both the primary and the fallback call sites splat: it holds no dedupe key, so the fallback cannot carry one whatever the comment says. `_dedupe_resumed_segments` opens `if not enabled: return tuple(segments), ()`, so the flag really is consulted first and alone. THE COLOUR, reproduced independently by the reviewer in a disposable worktree removed and pruned after, `python3 -B`, with an import probe confirming `pingpong_loop` resolved INSIDE the worktree: mutation A (`semantic_dedupe_enabled: bool = True,` to `False`) gives exit 1 at 7 failed, 115 passed; mutation B (the BUILDER site's `dedupe_enabled=semantic_dedupe_enabled` to `True`, reached by the two-line string ending `# into it.`, which occurs exactly once) gives exit 1 at 3 failed, 119 passed — both counts and both failure SETS identical to the handback's, including the named node in each. THE SUITES, all ten re-run serially by the reviewer: 122, 46, 25, 120, 36, 39, 14, 34, 27, 42, every one exit 0 and every one equal to the handback's reading. THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and `origin/feature/f109-semantic-dedupe` equal to HEAD, so the round was pushed as its handback said it would be. NO BLOCK CONDITION IS MET: not one number in the handback failed to reproduce, and the three declared deviations were all accurate. TWO FINDINGS ARE RAISED BY THIS REVIEW AND NEITHER IS THE ROUND'S FAULT — `R-0773`, whose repair round 10's own constraint 4 forbade and whose staleness the worker declared rather than hid, and `R-0774`, which the reviewer found while reading the trace seam the NEXT round was to change and which predates F109's trace work entirely.

- R-0773 — Low, `packages/orchestration/pingpong_loop.py` STILL DOCUMENTS F109'S CONFIG PLUMBING AS ABSENT IN THREE PLACES AFTER ROUND 10 LANDED IT. Raised by the reviewer at the F109 R10 gate, from the worker's own declared deviation 1, and registered with an id rather than slipped because the wrong state is on disk under `packages/` — the amend0827 rule 2 test — and the next reader meets it in the exact paragraph that explains the seam. MEASURED at `c22818f59e6f52ea79b10cb0f36390c5070322c7`: `grep -n "config plumbing that supplies"` over that file returns lines 1006 and 1541, each reading "the config plumbing that supplies it is T002c.", once in `compose_builder_prompt`'s docstring and once in `compose_reviewer_prompt`'s; and `_dedupe_resumed_segments`'s own scope-boundary paragraph closes at lines 921-922 with "What remains absent is the config plumbing that supplies ``enabled``, which is T002c." That plumbing landed at `b245e1c96a5568d0f8b471ed00ae0618d91b00db`, where `run_pingpong` gained `semantic_dedupe_enabled` and forwarded it to both primary compositions as `dedupe_enabled`. All three sentences were TRUE when written and round 10 falsified them without touching them — the `R-0749` shape, raised against the round that made the prose false rather than the round that wrote it. WHY LOW: no behaviour is wrong, no gate is blind, no test is weakened, and by AST the module's executable statements are untouched by the repair; the defect is confined to explanatory prose. WHY IT IS NOT HARMLESS: the first of the three is a DELIBERATE-ABSENCE note of exactly the kind AGENTS.md's discoverability section asks a reader to trust — "text search cannot find code that does not exist" — so a reader who trusts it concludes the kill switch is unbuilt, and the obvious next move is to build it a second time. THE FAULT IS THE REVIEWER'S: round 10's constraint 4 permitted only the edits SPEC V described and said "nothing else in that file changes", so the worker applied the constraint as written and declared the residual in its handback, which is exactly what guardrail G8 requires of it. FIX: rewrite all three passages to state the plumbing as it now IS, naming `b245e1c9` as the commit the reading was taken at, and change no executable statement of the module. Resolved when no docstring under `packages/` asserts that F109's config plumbing is absent, unbuilt or pending — a reading taken over the CLAIM and not over any one wording of it.

- R-0774 — Medium, ON EVERY RESUME FALLBACK THE PROMPT TRACE DESCRIBES THE ABANDONED RESUMED COMPOSITION INSTEAD OF THE BYTES THAT ACTUALLY REACHED THE PROVIDER. Raised by the reviewer at the F109 R10 gate while reading the trace seam round 11 was to change; it PREDATES F109's trace work and is not caused by it. MEASURED at `c22818f59e6f52ea79b10cb0f36390c5070322c7` by driving the REAL loop through the dedupe suite's own `fallback_repo` fixture with `builder_resume_fails=True` and `repair_rounds=2`, inside a disposable worktree removed after: `result.rounds[1].builder_output.resume_fallback` is True, the captured Builder calls of that round are `(resume='sess-builder', marker PRESENT, 808 chars)` followed by `(resume=None, marker ABSENT, 1110 chars)`, and the ONE builder trace recorded for that round reads `prompt_chars=808` with the dedupe marker present in `prompt_text_redacted`. The 1110-character full-content call that actually reached the provider has NO trace at all, and the trace that does exist describes an attempt the provider rejected. THE CAUSE IS ORDERING, NOT CONTENT: the Builder trace is appended at line 3352, the first `_call_with_retry` runs at 3373, the fallback branch opens at 3395 and rebinds `builder_composed` and `builder_prompt` at 3406-3407, and the second `_call_with_retry` at 3410 sends the rebound prompt — so the trace is written two statements before the composition it names is discarded. The Reviewer side is the same shape: append at 3658, call at 3699, fallback recomposition at 3738. `R-0771` repaired the bytes SENT and the manifest `record_finalized_call` reads, and the rebinding comment at lines 3401-3405 claims that rebinding makes "the bytes sent, the ``fallback_prompt`` stored by ``_finalize_call`` and the recorded evidence describe one and the same call" — the prompt TRACE is the one artefact that promise does not reach, which is why the defect survived that repair. WHY MEDIUM: nothing is corrupted and no security boundary is crossed, but `prompt_trace.jsonl` is the artefact that answers "what did we send the model", `token_ledger.record_call_segments` copies its manifest rows into the `call_segments` table, and on a fallback every one of `prompt_sha256`, `prompt_chars`, `segment_manifest`, `segment_manifest_chars` and `prompt_text_redacted` describes bytes that were never delivered — a FALSE live indicator in the evidence rather than a missing one, which this repository's own block conditions treat as the more serious of the two. It also blocks the next slice from landing honestly: surfacing the deduped names as a trace field on top of this ordering would turn a misleading paragraph into a structured, machine-readable claim that named segments were withheld from a call that re-sent them in full. FIX: in EACH role's fallback branch, after the recomposition rebinding and before the stream call, append a SECOND trace entry built from the rebound composition, mirroring that role's own existing append argument for argument. The entry already carries `transport_attempt` and `is_transport_retry` and its contract is one trace per ACTUAL provider invocation — which `tests/orchestration/test_structured_outputs.py`'s parse-retry pair, whose own name promises two traces for two calls, already relies on — so a second invocation earns a second entry rather than an overwrite of the first, and the failed resumed attempt keeps its own honest record. Resolved when a Builder resume fallback and a Reviewer resume fallback each record TWO traces for that round, the second carrying the full-content prompt's own character count and no dedupe marker, and when deleting either new append turns a named test red.
SLICE RECORD

<<<SPEC X
SPEC X — R-0773: THE THREE STALE PASSAGES.

File: `packages/orchestration/pingpong_loop.py`. Three prose replacements
and no fourth. No executable statement changes — G4(a) proves that by AST.

PAIR X1. TO contains FROM: false, so this is a REWRITE and the obligation
is FROM 0x, TO 1x after the commit. FROM occurs exactly 1 time before it.

FROM:
    supplies a real set. What remains absent is the config plumbing that
    supplies ``enabled``, which is T002c.

TO:
    supplies a real set. THE CONFIG PLUMBING NOW EXISTS: ``run_pingpong``
    carries ``semantic_dedupe_enabled`` and forwards it to both primary
    compositions as ``dedupe_enabled`` (F109 T002c, landed at
    ``b245e1c9``), so ``enabled`` is supplied on every production
    composition. The remaining bypass is ``dedupe_sent_hashes`` being
    ``None`` off a call that is not resuming, which is the scope rule
    rather than a gap.

PAIR X2. TO contains FROM: false, so this is a REWRITE. FROM occurs
exactly 2 times before the commit — once in `compose_builder_prompt`'s
docstring and once in `compose_reviewer_prompt`'s — and BOTH are replaced
with the same TO. After the commit FROM occurs 0 times and TO occurs
exactly 2 times. Report both counts.

FROM:
    ``dedupe_enabled`` is the kill switch, forwarded straight to
    :func:`_dedupe_resumed_segments`; the config plumbing that supplies it is
    T002c.

TO:
    ``dedupe_enabled`` is the kill switch, forwarded straight to
    :func:`_dedupe_resumed_segments`. ``run_pingpong`` supplies it from its
    own ``semantic_dedupe_enabled`` parameter (F109 T002c, landed at
    ``b245e1c9``), which reaches this composition and the other role's and
    nothing else.
SPEC X

<<<SPEC Y
SPEC Y — R-0774: ONE TRACE PER ACTUAL PROVIDER INVOCATION.

File: `packages/orchestration/pingpong_loop.py`. Two insertions, one per
role, and no third. Nothing already in the file is edited or deleted.

Each role's resume-fallback branch — the Builder's
`if builder_resume_ref and builder_out.error:` and the Reviewer's
counterpart — already recomposes at full content and rebinds BOTH
`<role>_composed` and `<role>_prompt`. Immediately AFTER that rebinding
pair, and BEFORE the `_begin_stream_call` that opens the fallback attempt,
add a second `result.prompt_traces.append(build_trace_entry(...))`.

That call MIRRORS THAT ROLE'S OWN EXISTING PRIMARY APPEND ARGUMENT FOR
ARGUMENT. Copy the role's primary append and change exactly two things:
  - `prompt_text=` takes the REBOUND `<role>_prompt`
  - `composed_prompt=` takes the REBOUND `<role>_composed`
Every other argument is copied unchanged from that SAME role's primary
append — including any the Reviewer's carries and the Builder's does not.
Do not invent an argument, do not drop one, do not reorder them, and do
not refactor the primary append into a shared helper: the two appends
differ by role and a helper would be a third thing to keep in step.

Carry a short comment above each insertion naming F109 and `R-0774`, and
stating WHY this is a second entry rather than a rewrite of the first: the
resumed attempt really did reach the provider and keeps its own honest
record, and the entry's contract is one trace per ACTUAL provider
invocation, so a fallback — which is a second invocation — earns a second
trace. The Reviewer comment may point at the Builder comment rather than
repeat it.
SPEC Y

<<<SPEC Z
SPEC Z — THE TESTS FOR R-0774.

File: `tests/orchestration/test_semantic_dedupe.py`, ONE new class appended
at the very END. No existing line is edited, reordered or deleted.

Drive the REAL loop through the file's existing fixtures — `fallback_repo`,
`TestChainAgainstTheRealLoop._provider_pair` and `._run`,
`_capture_role_calls` and `_split` — exactly as the existing
`test_a_builder_resume_fallback_sends_full_content` does. Reuse them; do
not build a second fixture that could drift from the first.

Every trace you read is asserted `prompt_text_truncated is False` BEFORE it
is read, so a marker absence is only as wide as the recorded text and no
wider — the same guard `_marked_traces` already applies, for the same
reason.

CASE 1 — THE BUILDER FALLBACK RECORDS THE BYTES IT ACTUALLY SENT. With
`builder_resume_fails=True` and `repair_rounds=2`: assert FIRST that the
fallback really fired (`result.rounds[1].builder_output.resume_fallback is
True`), so the case cannot pass vacuously on a run that never took the
branch it is about. Then, over the BUILDER traces of that fallback round:
there are exactly TWO; the FIRST carries the dedupe marker in
`prompt_text_redacted`; the SECOND does not; and the SECOND's
`prompt_chars` equals the length of the full-content prompt actually sent
to the fresh session. Take that length from `_split(calls)`'s fresh list
rather than hard-coding a number, so the case survives a fixture change
instead of pinning today's byte count.

CASE 2 — THE REVIEWER FALLBACK, the same claim for the other role, using
the reviewer-side resume failure `_provider_pair` already supports and the
existing `test_a_reviewer_resume_fallback_sends_full_content` already
drives.

CASE 3 — A CHAIN THAT NEVER FALLS BACK RECORDS ONE TRACE PER ROLE PER
ROUND. This is the DISCRIMINATOR: without it, cases 1 and 2 would still
pass if the loop began appending a second trace unconditionally, which
would be a different defect wearing the same green.
SPEC Z
