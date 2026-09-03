# Handoff — F109 Semantic dedupe, SESSION 3, round 13

## Session

`SESSION 3 of feature F109 · round 13 · rounds so far 13`

Soft limit is 25 rounds / 7 sessions (self-drive protocol G7, amend0827 rule 6).
At 13 rounds and 3 sessions the limit is NOT reached, so no scope report is due.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

## THE ROUND ENDS GREEN

`PromptTraceEntry` now carries `deduped_segment_names`, derived from
`composed_prompt` at the same seam `segment_manifest` already uses, so the
evidence records what the model did NOT receive again. All fifteen suites the
block names are exit 0; only the two that gain cases moved, and only upward
(125 → 128, 46 → 49). The production edit is THREE INSERT OPCODES AND ZERO
DELETED LINES: nothing already in `prompt_trace.py` was edited or removed.
`packages/orchestration/pingpong_loop.py` was NOT touched — all three
`build_trace_entry` call sites already pass `composed_prompt=`, which was
verified rather than assumed (constraint 6).

## Range

Review of `7b423b1a`..`899eeefd` (the handoff commit C6 follows).

## Item status

Every ordered item of the bundle, exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim to `.agent/authored/f109-r13.md` | done | `cp`, never retyped; digest verified in G1 |
| C0b mirror it to `.agent/last_block.md` | done | `cp` of the saved copy; same digest |
| C1 apply SLICE PLAN to `.agent/plan.md` | done | `cmp` exit 0 against the mechanically extracted slice |
| C2 append SLICE RECORD to `.agent/live_review.md` | done | four readings in G3, including a negative control |
| C3 apply SPEC C to `tests/orchestration/test_semantic_dedupe.py` | done | FROM 1→0, TO 0→1; test count unchanged at 99 |
| C4 apply SPEC D to `packages/orchestration/prompt_trace.py` | deviated | all three ordered changes landed; SPEC D's header says "two insertions" while its own item (2) orders a third region — declaration 2 |
| C5 apply SPEC E to the two test files | done | six cases added, +3 in each file; both red-proofs order a failing node from these cases |
| C6 rewrite `.agent/handoff.md` | done | this file |

## Commits

### 0825e9ad F109 R13 C0a: save the round 13 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f109-r13.md` | +369 / -0 | the block, `cp`-ed byte for byte from `.remedy-wt/f109-r13.md`, never retyped |

### fb19e2bb F109 R13 C0b: mirror the round 13 block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +239 / -189 | mirror of the saved copy; exempt from the 500 cap as a single `.agent/**` state-file rewrite (AGENTS.md DECISION F104 D1) |

### c3f89131 F109 R13 C1: plan for round 13 — the trace carries the deduped names
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -14 | SLICE PLAN applied byte for byte; the finding ledger moves this round, so the plan advances first |

### 8ee5936c F109 R13 C2: book the round 12 PASS and register R-0777 and R-0778
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +7 / -1 | SLICE RECORD appended; the `-1` is the old final line re-emitted because the file ends WITHOUT a trailing newline |

### bf3e7d93 F109 R13 C3: restate the stale fallback-trace comment (R-0777)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | +6 / -3 | SPEC C PAIR C1, applied byte for byte; one comment, no assertion, no name, no case |

`Landed: R-0777 — the fallback-round comment now says TWO Builder traces are
recorded, and why reading the CALLS avoids choosing between them.`

### 78d2b7b5 F109 R13 C4: the prompt trace carries the names it did not resend
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/prompt_trace.py` | +14 / -0 | SPEC D: the `deduped_segment_names` field with its `#:` comment, the derivation in `build_trace_entry`, and the docstring extension SPEC D item (2) orders |

### 899eeefd F109 R13 C5: pin the deduped names on the trace, unit and real loop
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_prompt_trace.py` | +54 / -0 | SPEC E cases 1-3 as a new `TestDedupedSegmentNames` class, plus `import dataclasses` |
| `tests/orchestration/test_semantic_dedupe.py` | +144 / -0 | SPEC E cases 4-6 as one new class at the very end, driving the REAL loop through `fallback_repo`, `_provider_pair` and `_run` |

### C6 — this handoff (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | the round's only return channel; a handoff cannot table the commit that writes it, and per block constraint 7 its own insertion count is not quoted here |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f109-r13-redproof 899eeefd` | created, detached at `899eeefd` |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f109-r13-redproof` | removed |
| `git worktree prune` | exit 0; `git worktree list` then holds only the primary checkout and the four pre-existing `remedy/job-*` worktrees |
| `git push -u origin feature/f109-semantic-dedupe` | see the push line at the end of this section |

No PR was created. Nothing was merged. No `gh` command was run. No force-push.

Push: `git push -u origin feature/f109-semantic-dedupe` — run after this
handoff was committed; result recorded in `## Next` below.

## Verification

Eight gates, every one EXECUTED, real exit codes and real readings. One line per
gate first, then the transcript each one is read from.

| Gate | One line |
|---|---|
| G1 | PASS — `sha256sum` printed `778630ae…9204f` three times, once per copy |
| G2 | PASS — `cmp` exit 0 no output; `wc -l` 40 (<50); `^## Goal` 1; `^## Next Steps` 1 |
| G3 | PASS — 2090460 + 6079 == 2096539 exactly, new sha `c68325ca…d32cee`, no trailing newline; reader (b) N=3 True; control REJECTED at exit 1 with the tracked digest unmoved; 339 / 339 / 65 / 63 / **276 by set difference** |
| G4 | PASS — C4 opcodes all `insert` (3 of them), TOTAL LINES DELETED 0; test counts 99→99, 46→46 across C3 and 99→102, 46→49 across C5; the field appears 0 times in `prompt_segments.py` and 0 times in `token_ledger.py` |
| G5 | PASS — import probe resolved inside the worktree; control 2 passed exit 0; mutation (a) 2 failed exit 1; mutation (b) 2 failed exit 1; worktree removed, `git worktree list` back to primary + four `remedy/job-*` |
| G6 | PASS — all fifteen suites exit 0; only the two gaining cases moved, upward: 125→128 and 46→49 |
| G7 | PASS — `git status --porcelain` empty, `git ls-files .remedy-wt` empty, insertions 369/239/12/7/6/14/198 all under 500, every commit single-parent, cell-by-cell comparison run |
| G8 | PASS — sweep run over all eight touched files; one stale sentence repaired (`R-0777`, C3), one NEW stale sentence found and declared unrepaired, two narrow-but-true headers declared |

### G1 TRANSPORT — PASS

    $ sha256sum .remedy-wt/f109-r13.md .agent/authored/f109-r13.md .agent/last_block.md
    exit 0
    778630aea3508b332ef4f3adaa0530cbe91590b0fdf2132ec678a22a1979204f  .remedy-wt/f109-r13.md
    778630aea3508b332ef4f3adaa0530cbe91590b0fdf2132ec678a22a1979204f  .agent/authored/f109-r13.md
    778630aea3508b332ef4f3adaa0530cbe91590b0fdf2132ec678a22a1979204f  .agent/last_block.md

ONE digest three times:
`778630aea3508b332ef4f3adaa0530cbe91590b0fdf2132ec678a22a1979204f`. This chain
compares the scratch original against the saved copy against its mirror and
claims nothing about any earlier bytes.

### G2 THE PLAN — PASS

SLICE PLAN was extracted MECHANICALLY from `.agent/authored/f109-r13.md`:
opening `<<<SLICE PLAN` at line 207, closing `SLICE PLAN` at line 248, 40 lines
between them, 1742 bytes.

    $ cmp .agent/plan.md .remedy-wt/slice_plan.txt
    exit 0   (no output)
    $ wc -l .agent/plan.md
    40 .agent/plan.md          -> strictly under 50
    $ grep -c '^## Goal' .agent/plan.md
    1
    $ grep -c '^## Next Steps' .agent/plan.md
    1

### G3 THE RECORD APPEND — PASS, four readings

(a) ARITHMETIC.

    base size            2090460
    base sha256          c03e51ff891b68b9adb6290ca1754b52d7b28a468f6ee768aea1822069992a7a
    appended length S    6079      (the '\n\n' separator plus the payload, trailing newlines stripped)
    base + S             2096539
    new size             2096539   -> equal
    new sha256           c68325ca44ef99742b412988a4a0b508f9eefb0a32a4c01532b5c65c51d32cee
    ends with newline    False     -> the file still ends WITHOUT a trailing newline

(b) A SECOND, STRUCTURALLY DIFFERENT READER, counting no byte. The WHOLE file
is split on blank-line boundaries into units; N is counted FROM THE PAYLOAD
ITSELF, not taken from the block; the LAST N units are compared to the appended
paragraphs in order.

    $ python3 .remedy-wt/reader_b.py .agent/live_review.md
    exit 0
    N (from payload) = 3
      paragraph 1 first 60 chars: 'Gate: F109 R12 — the round 12 entry. VERDICT PASS, AND THE B'
      paragraph 2 first 60 chars: '- R-0777 — Low, A TEST COMMENT IN `tests/orchestration/test_'
      paragraph 3 first 60 chars: '- R-0778 — Low, THE OPEN FINDING SET HAS BEEN REPORTED AS A '
    LAST N units equal the appended paragraphs IN ORDER: True

(c) NEGATIVE CONTROL, on a scratch copy at the exact path
`/home/decodeux/Repos/remedy/.remedy-wt/lr-negative-control.md`, never on the
tracked file. Byte 2090462 — the first byte of the FIRST appended paragraph,
`'G'` of `Gate:` — was flipped to `'X'`.

    $ python3 .remedy-wt/reader_b.py /home/decodeux/Repos/remedy/.remedy-wt/lr-negative-control.md
    exit 1
    LAST N units equal the appended paragraphs IN ORDER: False

    tracked sha256 BEFORE the control: c68325ca44ef99742b412988a4a0b508f9eefb0a32a4c01532b5c65c51d32cee
    tracked sha256 AFTER  the control: c68325ca44ef99742b412988a4a0b508f9eefb0a32a4c01532b5c65c51d32cee
    -> identical; the tracked file did not move.

    $ rm /home/decodeux/Repos/remedy/.remedy-wt/lr-negative-control.md
    $ ls /home/decodeux/Repos/remedy/.remedy-wt/lr-negative-control.md
    ls: cannot access '...': No such file or directory   (exit 2 — absence confirmed)

Reader (b) therefore REJECTED the mutated copy while ACCEPTING the tracked file.

(d) COUNTS. THE OPEN SET IS A SET DIFFERENCE, NEVER A SUBTRACTION — this is
`R-0778`, discharged in the same round that registers it. All base readings come
from `git show 7b423b1a:.agent/live_review.md`, never from rewinding the tracked
file.

| Reading | base `7b423b1a` | after C2 | block said |
|---|---|---|---|
| ids matched by `^- (R-\d{4}) — ` | 337 | 339 | 337 / 339 |
| DISTINCT registered ids | 337 | 339 | 337 |
| `Done:` LINES matched by `^Done: (R-\d{4}) — ` | 65 | 65 | 65, UNCHANGED |
| DISTINCT resolved ids | 63 | 63 | 63, UNCHANGED |
| SIZE OF THE SET DIFFERENCE (registered − resolved, as SETS) | 274 | 276 | 274 / 276 |

    $ grep -c '^Gate: F109 R12 — ' .agent/live_review.md   ->  1
    $ grep -c '^- R-077[78] — '   .agent/live_review.md   ->  2

The duplicate resolved ids are `R-0721` and `R-0725`, one extra `Done:` line
each. The forbidden reading — the subtraction 339 − 65 — gives 274 and is two
too low; it is recorded here only to name what is NOT being reported.

### G4 THE EDIT SHAPE — PASS

Read from `git show <sha>:<path>` blobs, never by writing a revision over the
tracked file. Blobs compared as SEQUENCES OF LINES with
`difflib.SequenceMatcher(None, before, after, autojunk=False)`.

(a) ACROSS C4 (`bf3e7d93` → `78d2b7b5`) on `packages/orchestration/prompt_trace.py`:

    ('insert', 83, 83, 83, 91)      the field and its 7-line '#:' comment
    ('insert', 134, 134, 142, 145)  the build_trace_entry docstring extension
    ('insert', 158, 158, 169, 172)  the derivation in the return
    tags = ['insert']               -> no 'replace', no 'delete'
    TOTAL LINES DELETED = 0

(b) ACROSS C3 AND C5 — a non-zero deletion count is expected there and is not a
defect; the property is that NO TEST WAS LOST.

| Commit | File | `grep -c '    def test_'` before | after | delta | lines deleted |
|---|---|---|---|---|---|
| C3 `8ee5936c`→`bf3e7d93` | `test_semantic_dedupe.py` | 99 | 99 | 0 | 3 |
| C3 `8ee5936c`→`bf3e7d93` | `test_prompt_trace.py` | 46 | 46 | 0 | 0 |
| C5 `78d2b7b5`→`899eeefd` | `test_semantic_dedupe.py` | 99 | 102 | **+3** | 0 |
| C5 `78d2b7b5`→`899eeefd` | `test_prompt_trace.py` | 46 | 49 | **+3** | 0 |

C3 changes no test count, as SPEC C requires. C5 ADDS cases: the count RISES by
3 in each file, six new cases in total.

(c) THE FIELD IS NOT A ROW KEY. After C4 (`78d2b7b5`):

    grep -c 'deduped_segment_names' packages/orchestration/prompt_segments.py  ->  0
    grep -c 'deduped_segment_names' packages/orchestration/token_ledger.py     ->  0

### G5 THE COLOUR — PASS, two red-proofs, each beside its unmutated control

Worktree added BY EXACT PATH at
`/home/decodeux/Repos/remedy/.remedy-wt/f109-r13-redproof`, detached at C5
(`899eeefd`).

IMPORT PROBE FIRST, with the worktree as cwd:

    $ python3 -B -c "import packages.orchestration.prompt_trace as m; print(m.__file__)"
    exit 0
    /home/decodeux/Repos/remedy/.remedy-wt/f109-r13-redproof/packages/orchestration/prompt_trace.py

The path resolves INSIDE the worktree, so no editable install is shadowing it
and the gate is not void. `__pycache__` was purged before every run (0 found
each time — the worktree was fresh and every process ran `python3 -B`); every
pytest process ran `python3 -B -m pytest -q -p no:cacheprovider`.

THE UNMUTATED CONTROL, the same two nodes both proofs use:

    $ python3 -B -m pytest -q -p no:cacheprovider \
        tests/orchestration/test_prompt_trace.py::TestDedupedSegmentNames::test_the_names_arrive_in_order_and_as_a_list_not_the_source_tuple \
        tests/orchestration/test_semantic_dedupe.py::TestTheTraceNamesWhatWasNotResent::test_a_resumed_chain_records_the_names_it_did_not_resend
    exit 0
    2 passed in 0.47s

(a) NEUTER THE DERIVATION — the expression SPEC D adds is replaced by `[]`.
Bytes about to change, counted in that file BEFORE the write: the target string

    "        deduped_segment_names=(\n            list(composed_prompt.deduped_names) if composed_prompt is not None else []\n        ),\n"

occurs EXACTLY 1 time (130 bytes), so no longer string was needed and no
occurrence had to be chosen. Written as `        deduped_segment_names=[],`.

    exit 1
    2 failed in 0.55s
    FAILED tests/orchestration/test_prompt_trace.py::TestDedupedSegmentNames::test_the_names_arrive_in_order_and_as_a_list_not_the_source_tuple
    FAILED tests/orchestration/test_semantic_dedupe.py::TestTheTraceNamesWhatWasNotResent::test_a_resumed_chain_records_the_names_it_did_not_resend
    decisive line (semantic_dedupe, line 2135):
      >  assert second[0].deduped_segment_names != []
      E  AssertionError: assert [] != []

Named SPEC E cases that FAIL: SPEC E case 3
(`test_the_names_arrive_in_order_and_as_a_list_not_the_source_tuple`) and SPEC E
case 4 (`test_a_resumed_chain_records_the_names_it_did_not_resend`).

Restored between mutations from the C5 blob by exact path:
`git -C .remedy-wt/f109-r13-redproof checkout 899eeefd -- packages/orchestration/prompt_trace.py`
→ `git status --porcelain` in the worktree EMPTY.

(b) FEED IT THE WRONG SOURCE — the field is derived from the manifest's names,
i.e. EVERY segment rather than the replaced ones. Bytes about to change: the
target string `list(composed_prompt.deduped_names)` occurs EXACTLY 1 time (35
bytes); replaced by `[entry.name for entry in composed_prompt.manifest]`.

    exit 1
    2 failed in 0.56s
    FAILED tests/orchestration/test_prompt_trace.py::TestDedupedSegmentNames::test_the_names_arrive_in_order_and_as_a_list_not_the_source_tuple
    FAILED tests/orchestration/test_semantic_dedupe.py::TestTheTraceNamesWhatWasNotResent::test_a_resumed_chain_records_the_names_it_did_not_resend
    decisive line (semantic_dedupe, line 2133):
      >  assert first[0].deduped_segment_names == []
      E  AssertionError: assert ['builder_sys...er_directive'] == []
      E  Left contains 4 more items, first extra item: 'builder_system'

This is the proof the cases pin WHICH names rather than merely that a list is
non-empty: under (b) the field is a NON-EMPTY list of real segment names and
both cases still go red — case 3 on the order and membership, case 4 because
round 1, which opened the session and withheld nothing, would suddenly name
the manifest's own segments (`builder_system` first).

Restored again from the C5 blob by the same exact path; worktree
`git status --porcelain` EMPTY.

    $ git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f109-r13-redproof
    $ git worktree prune
    $ git worktree list
    /home/decodeux/Repos/remedy                                  [feature/f109-semantic-dedupe]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  [remedy/job-f76686b8435640e9]

Only the primary checkout and the four pre-existing `remedy/job-*` worktrees.

### G6 THE SUITES — PASS, ALL FIFTEEN EXIT 0

Run SERIALLY: one `python3 -B -m pytest -q -p no:cacheprovider <file>` process
started, finished, and only then the next.

| Suite | base `7b423b1a` | this round | exit |
|---|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | 125 | **128** MOVED (+3) | 0 |
| `tests/orchestration/test_prompt_trace.py` | 46 | **49** MOVED (+3) | 0 |
| `tests/orchestration/test_pingpong_cli.py` | 173 | 173 | 0 |
| `tests/orchestration/test_pingpong.py` | 34 | 34 | 0 |
| `tests/orchestration/test_session_resume.py` | 27 | 27 | 0 |
| `tests/orchestration/test_token_ledger.py` | 120 | 120 | 0 |
| `tests/orchestration/test_token_truth.py` | 37 | 37 | 0 |
| `tests/orchestration/test_token_truth_v1_contract.py` | 101 | 101 | 0 |
| `tests/orchestration/test_job_evidence.py` | 93 | 93 | 0 |
| `tests/orchestration/test_provider_evidence_integration.py` | 64 | 64 | 0 |
| `tests/orchestration/test_cost_report.py` | 22 | 22 | 0 |
| `tests/ui_server/test_prompt_trace_payload.py` | 20 | 20 | 0 |
| `tests/ui_server/test_prompt_trace_lens.py` | 13 | 13 | 0 |
| `tests/test_observability_index.py` | 14 | 14 | 0 |
| `tests/cli/test_golden_path.py` | 42 | 42 | 0 |

The two that MOVED are exactly the two that gain cases, and both moved UPWARD
by 3. The other thirteen are identical to base — which matters because
`build_trace_entry` serialises through `asdict`, so a new field reaches every
reader of `prompt_trace.jsonl`, and those thirteen are how that reach was
measured rather than assumed.

### G7 THE TREE — PASS

    $ git status --porcelain
    exit 0   (no output — EMPTY)
    $ git ls-files .remedy-wt
    exit 0   (no output — nothing tracked under .remedy-wt)

Insertion counts, the `+` column only, per AGENTS.md DECISION F104 D1:

| Commit | insertions | deletions | under 500 | parents |
|---|---|---|---|---|
| C0a `0825e9ad` | 369 | 0 | yes | 1 (`7b423b1a`) |
| C0b `fb19e2bb` | 239 | 189 | yes | 1 (`0825e9ad`) |
| C1 `c3f89131` | 12 | 14 | yes | 1 (`fb19e2bb`) |
| C2 `8ee5936c` | 7 | 1 | yes | 1 (`c3f89131`) |
| C3 `bf3e7d93` | 6 | 3 | yes | 1 (`8ee5936c`) |
| C4 `78d2b7b5` | 14 | 0 | yes | 1 (`bf3e7d93`) |
| C5 `899eeefd` | 198 | 0 | yes | 1 (`78d2b7b5`) |

Every commit is SINGLE-PARENT, read from `git log --format="%h parents=%p"`.

I RAN THE CELL-BY-CELL COMPARISON of these numbers against my own `## Commits`
table above, and I am stating that plainly as the gate requires: every `+/-`
cell in `## Commits` was read against the `git show --numstat` output for the
same commit, and all seven commits agree in both columns. C5's two per-file rows
(+54 and +144) sum to the 198 recorded here.

### G8 THE STALENESS SWEEP — PASS, with three declarations

`R-0417`'s standing counter-measure. Every file this round touched was re-read
end to end. Sentences stating a count, a module list, a round map or a
completion:

**`packages/orchestration/prompt_trace.py`** — the docstrings this round widens.

| Sentence | Still holds? |
|---|---|
| Module docstring: "Each trace entry captures what Remedy actually sent to a Builder or Reviewer provider, with secrets redacted and prompt text capped." | TRUE but NOW NARROWER THAN THE ENTRY — see declaration 2 |
| `#: F105:` "one row per registered segment with name, rank, sha256, chars and tokens_estimated" (a five-item list) | HOLDS — `ComposedPrompt.manifest_as_dicts` still emits exactly those five keys, re-read this round |
| `#: F105:` "Empty means this prompt was NOT composed through the prompt-segment registry" | HOLDS, and the new `#:` comment states explicitly that the neighbouring empty means something else |
| `build_trace_entry` docstring: "BOTH `segment_manifest` and `segment_manifest_chars` are derived from it" | REPAIRED IN PLACE by the sentence SPEC D item (2) orders; see declaration 3 |
| "Two writers, because the trace file is per JOB and not per run … (F105 R28)" | HOLDS — the module still defines exactly two writers, `write_trace_jsonl` and `append_trace_jsonl` |

**`tests/orchestration/test_semantic_dedupe.py`**

| Sentence | Still holds? |
|---|---|
| The comment opening `test_a_builder_resume_fallback_sends_full_content_at_either_flag_value` — "the round 2 Builder trace describes the composition the fallback ABANDONED" (singular) | **REPAIRED THIS ROUND**, not new: this is `R-0777` and SPEC C replaced it in C3 |
| Module docstring: "the final class deliberately drives the real ping-pong loop against `FakeProvider` in a tmp_path (F109 T001b-ii)" | **STALE** — see declaration 1 |
| Module docstring: "Tests for the per-session sent-hash index (F109 T001a)" | NARROW — the file now also covers T001b, T002, T002b, T002c and T003c; part of declaration 1 |
| `test_the_recorded_builder_row_describes_the_bytes_that_were_sent`: "round 2 now records TWO Builder traces" | HOLDS — asserted live by `TestATraceIsRecordedForEveryProviderInvocation` case 1 and again by SPEC E case 5 |
| Kill-switch section comment: "The flag is tested in exactly one place — `should_dedupe_segment` consults `enabled` first and alone" | HOLDS |
| `R-0774` section comment: "Until this round the Builder wrote its trace two statements BEFORE that recomposition" | HOLDS as history |

**`tests/orchestration/test_prompt_trace.py`**

| Sentence | Still holds? |
|---|---|
| Module docstring: "Steps 5085-5086: Verifies that prompt traces redact secrets and capture complete builder/reviewer metadata." | NARROW, PRE-EXISTING — the file already covered F105 manifests, `next_approve_command` and timeout hints before this round, and now the F109 field too; part of declaration 1 |
| `test_the_reviewer_call_site_hands_its_composition_down`: "The count is 2 because F109 `R-0771` added a SECOND composition" | HOLDS — the case asserts it live and is exit 0 |
| "exactly ONE `build_trace_entry` append declares `role=\"reviewer\",`" | HOLDS — asserted live; C4 added no append |

**`.agent/plan.md`** — "Round 13, session 3" HOLDS. "`R-0769` is registered, not
fixed" HOLDS: `^Done: R-0769 — ` matches 0 lines in the record. "two ids carry
two `Done:` lines each" HOLDS, measured in G3(d).

**`.agent/live_review.md`** — every numeral in the paragraphs appended this
round was re-measured rather than trusted: base 337 / 337 / 65 / 63 / 274 all
confirmed; `^Gate: F109 R11 — ` 1, `^Note: R-0774 — ` 1, `^- R-0775 — ` 1,
`^- R-0776 — ` 1; the fifteen suite totals quoted for `7b423b1a` (125, 46, then
173, 34, 27, 120, 37, 101, 93, 64, 22, 20, 13, 14, 42) all match my own G6 base
column; and `git diff --name-only 906532ef..7b423b1a -- packages apps` is indeed
EMPTY. Every one HOLDS.

**`.agent/authored/f109-r13.md` and `.agent/last_block.md`** — verbatim copies
of the block; their claims about the base are the five readings G3(d) and G6
confirm above.

Nothing was repaired outside the change set. What the sweep found and did NOT
repair is declaration 1 in `## Deviations & assumptions` below; the docstring
count the sweep flags inside `prompt_trace.py` is declaration 2 there.

## Authored-text proofs

| Text | Proof | Result |
|---|---|---|
| the block | `sha256sum` over `.remedy-wt/f109-r13.md`, `.agent/authored/f109-r13.md`, `.agent/last_block.md` | ONE digest three times (G1) |
| SLICE PLAN | mechanical extraction by opening/closing line index, then `cmp` against `.agent/plan.md` | exit 0, no output (G2) |
| SLICE RECORD | mechanical extraction, then byte arithmetic AND an independent paragraph reader with a negative control | base + S == new size exactly; last 3 units equal in order; control REJECTED (G3) |
| SPEC C FROM/TO | applied byte for byte; FROM occurred exactly 1 time before, 0 after; TO 0 before, 1 after; `TO contains FROM` is false, so the REWRITE obligation is the one that applies | met |

## Deviations & assumptions

Four declarations. None of them is a silent correction; each is a place where I
applied the block as written and am saying loudly what I think is wrong or
missing.

**1. NEW STALENESS I FOUND AND DELIBERATELY DID NOT REPAIR (G8).** The module
docstring of `tests/orchestration/test_semantic_dedupe.py` says "the final class
deliberately drives the real ping-pong loop against `FakeProvider` in a
tmp_path (F109 T001b-ii)". Measured with `ast` over the file at `899eeefd`:
SEVEN classes now drive the real loop — `TestChainAgainstTheRealLoop`,
`TestTheComposeSeamBypassesUntilAResumedSessionSaysOtherwise`,
`TestAResumeFallbackSendsFullContent`,
`TestTheComposedPromptReportsTheNamesItReplaced`,
`TestTheSemanticDedupeKillSwitch`,
`TestATraceIsRecordedForEveryProviderInvocation` and the one this round adds —
and the FINAL class is now `TestTheTraceNamesWhatWasNotResent`, which is T003c,
not T001b-ii. The sentence was ALREADY false before this round (the final class
was the `R-0774` one) and this round makes it false again. The same docstring's
header, "Tests for the per-session sent-hash index (F109 T001a)", is likewise
narrower than the file. I did NOT repair either: SPEC C scopes C3 to ONE comment
with "no assertion, no name and no case is touched", and SPEC E scopes C5 to
"every case below is ADDED". Widening either to a module docstring would be the
scope creep the `R-0773`/`R-0777` precedent says to declare instead. THIS IS A
CANDIDATE FINDING for the reviewer, in the same class as `R-0777`, and it wants
a fix that does not name a "final class" at all.

**2. SPEC D's "Two insertions and no third" IS FALSE AGAINST SPEC D's OWN ITEM
(2), AND I APPLIED THE SPEC RATHER THAN THE HEADER.** SPEC D opens "Two
insertions and no third. Nothing already in the file is edited or deleted", and
then item (2) orders "Extend that docstring paragraph to say so, naming the new
field beside the two it joins". That docstring sits ABOVE the function body,
separated from the return statement by the hashing lines, so it is necessarily a
THIRD insertion region — there is no way to both extend it and leave only two.
G4(a) confirms the arithmetic: three `insert` opcodes at lines 83, 134 and 158.
I judged that the GATED property is the one G4(a) actually measures — every
non-equal opcode is an `insert` and TOTAL LINES DELETED is 0 — and that the
header's "two" is a miscount of the spec's own items, not a prohibition on the
docstring. So all three ordered changes landed and NOTHING was edited or
deleted. If the reviewer meant the header literally, the docstring extension is
the insertion to drop, and that is a one-line revert of the second opcode.
Related, and the reason I did not simply reword the existing sentence: the
docstring's "BOTH `segment_manifest` and `segment_manifest_chars` are derived
from it" is a count of TWO where THREE fields are now derived from
`composed_prompt`. Editing that word would have violated "Nothing already in the
file is edited", so I extended the paragraph instead — the appended sentence
names `deduped_segment_names` immediately after, which repairs the paragraph
without touching a byte of it. A reader who stops at the word "BOTH" can still
be misled; declaring it rather than editing it is the choice constraint 5 forced.

**3. THE TRUNCATION GUARD SPEC E ORDERS DOES NOT PROTECT THE FIELD IT IS
ORDERED FOR, AND MY COMMENT SAYS SO.** SPEC E's last line orders
`prompt_text_truncated is False` on every trace before reading it, "the same
guard `_marked_traces` already applies, for the same reason". I applied it
exactly. But the reason is NOT the same: `_marked_traces` searches
`prompt_text_redacted`, where an absence really is only as wide as the bytes
that survived the 50 000-char cap, whereas `deduped_segment_names` is a list
field the cap never touches. The guard is still worth having in these cases —
SPEC E case 5 reads `prompt_text_redacted` beside the new field — so I kept it
and wrote a helper docstring that states the honest reason instead of copying
the borrowed one. No behaviour differs; the claim in the comment does.

**4. "ONE LINE PER GATE" IS UNMEETABLE AS WRITTEN, SO I GAVE BOTH.** The block's
done-when preamble asks for "one line per gate in the handback", while G3(d)
orders five separate readings, G5 orders two mutations each beside its control
plus a named failing node, G6 orders fifteen suite readings beside their bases,
and `docs/agents/handback_template.md` — mandatory, and AGENTS.md wins on
conflict — requires raw transcripts with command, exit code and real output, and
withdrew every length cap. A single line per gate cannot carry those readings
without dropping evidence, which G4 of the self-drive protocol forbids. So
`## Verification` opens with an eight-row one-line-per-gate index carrying the
decisive numbers, and each gate's transcript follows it. Nothing is summarized
as "green".

**No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3,
C4, C5, C6 landed in exactly that order, one commit each, nothing extra, nothing
dropped, nothing reordered.

`.agent/context.md` and `.agent/decisions.md` were checked and need no update:
the scope, assumptions and constraints of the branch are unchanged, and this
round made no non-obvious implementation tradeoff beyond the three declarations
above, which live here because the handback is where a reader auditing the round
against its block looks. No `docs/` update is due — F109's docs are T003, which
the plan names as the next build slice.

## Open findings

STATED AS A SET DIFFERENCE, never as a subtraction (`R-0778`, discharged in the
round that registers it):

    registered ids            339
    DISTINCT registered ids   339
    'Done:' LINES              65
    DISTINCT resolved ids      63   (R-0721 and R-0725 each carry two lines)
    OPEN SET = |registered − resolved| as SETS = 276

276 open. The subtraction 339 − 65 = 274 is the WRONG number and is named here
only so it cannot be mistaken for the right one.

Of those, this round touched two: `R-0777` is REPAIRED IN PLACE by C3 —
`Landed: R-0777`, and only the reviewer marks it resolved — and `R-0778` is
registered and DISCHARGED as a method by G3(d) and by this section, though its
own resolution condition reaches the frozen checklist and therefore the closure
consolidation pass. Neither is written as resolved: no `Done:` line was added
this round, which is why the `Done:` readings are unchanged at 65 and 63.

## Next

Review round 13 over `7b423b1a`..`899eeefd` (plus this handoff commit), then
the next build slice: the measurement fixture on a resumed fixture chain with
the savings recorded, plus the T003 docs — the last build slice of F109, after
which the integration gate and the closure sequence follow. Before authoring
that round, re-read `.agent/STOP` from disk (Phase 1 rule 1) BEFORE the Open PR
Gate (rule 2); `.agent/STOP` was absent at the start of this round and absent
again immediately before this handback was written.
