# Handback — F033 Hunk-level diff approval, round 23

## Session

SESSION 6 of feature F033 · round 23 · rounds so far 23

Branch: `feature/f033-hunk-approval-v2` (never main; no PR created, none merged).
Block on disk: `.remedy-wt/f033-r23-block.md`, sha256
`cab2e62a63be01e525c8e73c8fcab5ff671acfca0d064818a8f5fb7b1ee5931e`, 26181 bytes —
computed by the worker before reading it and equal to the digest the block prompt
stated.

Round 23 connects the two pieces rounds 21 and 22 built. `hunk_decision_record.py`
gains `load_latest_hunk_ledger_from_metadata`, which selects a task's LATEST
recorded decision out of a job's metadata MAPPING and rebuilds it through
`import_hunk_ledger`; `run_pingpong` gains a keyword-only `hunk_ledger` it forwards
to `compose_builder_prompt`; and the acceptance test drives the REAL loop and ties
the loop's own segment bytes to the operator's reason by sha256. The JOB-level
caller in `pingpong_job.py` is deliberately untouched and is the next round.

## Range

Review of `d0c86c2d`..HEAD, where HEAD is C6 — the commit that adds this file — and its
parent is C5 `5fe56ddb`, the revision every gate below was run at. C6's own sha is not
written here because it does not exist while this file is being written, and this
repository does not put an unmeasured sha on disk.

## Commits

### 9ba7f6ec docs(f033): save the round 23 step block  (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r23.md` | +350/-0 | the round-23 block, copied byte for byte with `shutil.copyfile` — never retyped |

### 0527a1a3 docs(f033): mirror the round 23 block into last_block  (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +256/-220 | the same bytes mirrored into the fast-resume slot |

### 7fe2f553 docs(f033): rewrite the plan for round 23  (C1)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +14/-11 | full rewrite from slice PLAN23, byte for byte |

### ce6c2866 docs(f033): book the round 22 verdict and resolve R-0747  (C2)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4/-0 | slice RECORD23 appended after one blank-line separator; the `Landed: R-0747` line is untouched and the `Done:` paragraph joins it |

### 39acdfb0 feat(f033): read a task latest recorded hunk decision back as a ledger  (C3, SPEC A)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_decision_record.py` | +108/-10 | `load_latest_hunk_ledger_from_metadata` and its private parse guard `_parsed_decision_stamp`; `import_hunk_ledger` added to the existing import block; the new name added to `Public API::`; the module docstring's totality paragraph narrowed to the two recording doors (see deviation D3) |

### 88197da8 feat(f033): forward a hunk ledger from run_pingpong into the builder prompt  (C4, SPEC B)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +29/-11 | `run_pingpong` gains keyword-only `hunk_ledger: Any = None` and forwards it at the `builder_composed` call; `compose_builder_prompt`'s stale "does NOT supply this parameter from the run loop yet" paragraph rewritten per SPEC B3 |

### 5fe56ddb test(f033): follow a stored hunk decision through the real loop to the prompt  (C5, SPEC C)
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_decision_record.py` | +188/-0 | APPEND ONLY: eight tests over SPEC A — latest-wins in both insertion orders, task isolation, unparseable-loses, none-parseable-last-wins, the `>=` tie discriminator, the absent task, the totality table, and the C2 record→read round trip |
| `tests/orchestration/test_builder_prompt_hunk_rejections.py` | +155/-0 | APPEND ONLY: SPEC C3, the acceptance test through the REAL `run_pingpong`, plus C4's negative half |

### C6 docs(f033): hand back round 23  (this file; sha unknown at authoring time)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | this handback, and the only path C6 touches; a handoff cannot table the commit that writes it (R-0149 pattern) |

Every commit is single-parent. Insertions: 350, 256, 14, 4, 108, 29, 343 — all under
500. No commit was reordered, added or dropped relative to the block's ordered
sequence C0a, C0b, C1, C2, C3, C4, C5, C6.

## External actions

- `git worktree add .remedy-wt/wt-r23 5fe56ddb --detach` → REAL_EXIT=0.
- `git worktree remove .remedy-wt/wt-r23` → REAL_EXIT=0 (no `--force` needed).
- `git worktree prune` → REAL_EXIT=0. `git worktree list` afterwards shows the
  primary checkout only.
- `git push -u origin feature/f033-hunk-approval-v2` → runs after C6; see the Push
  paragraph at the end of Verification for why its exit code is not on disk here.
- No `gh` command was run. No PR was created, edited or merged. `main` untouched.

## Verification

Every gate ran at C5 (`5fe56ddb`), before the C6 handback commit. REAL exit codes come
from `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with no pipe, or from a Python driver's
`subprocess.returncode`.

**G1 TRANSPORT — REAL_EXIT=0.**
`cmp .remedy-wt/f033-r23-block.md .agent/authored/f033-r23.md` → REAL_EXIT=0, silent.
`cmp .remedy-wt/f033-r23-block.md .agent/last_block.md` → REAL_EXIT=0, silent.
Committed `.agent/authored/f033-r23.md` at C5: 26181 bytes, sha256
`cab2e62a63be01e525c8e73c8fcab5ff671acfca0d064818a8f5fb7b1ee5931e` — equal to the
source file's, byte-identical.

**G2 THE PLAN — REAL_EXIT=0.**
`.agent/plan.md` at C5: 2690 bytes, 49 lines, sha256
`be450d505e65f31f60a75c2a52cd1eb5a0d38b73d412590b2285e9ba31df7d6a`. Slice PLAN23:
2690 bytes, same sha256. byte-EQUAL True; under 50 lines True; holds `## Goal` True;
holds `Steps` True.

**G3 THE RECORD APPEND, measured at C2 — REAL_EXIT=0, with one block numeral
corrected (deviation D1).**
Base `.agent/live_review.md` at `d0c86c2d`: **1588340** bytes, ends with a newline.
The block's Constraint 2 and G3 both state 1588184; that is the size at `61d2ffe7`,
BEFORE round 22's own C3 commit `72dcfd53` appended the 156-byte `Landed: R-0747`
line. Delta measured: +156. Reconstruction with the measured base:
1588340 + 1 + 6800 = **1595141** = the committed size at C2. True.
RECORD23 slice: 6800 bytes, sha256
`bc4a18b7e05886178ef66b6adf9e16591b0c5ae3c46df0626fb5290255ac4fdb`.
READER 1 (base a byte PREFIX, slice an exact SUFFIX, separator exactly one `\n`):
accepts the committed bytes. READER 2 (the file's last N blank-line units equal the
slice's paragraphs IN ORDER): accepts. N was COUNTED by the script from the slice,
not taken from the block: **N = 2**.
Negative control: first appended paragraph spans bytes 1588341..1593478; flip offset
**1592341** proved inside that span; byte `b't'` → `b'T'`. READER 1 REJECTS the
flipped bytes and ACCEPTS the unflipped; READER 2 REJECTS the flipped and ACCEPTS the
unflipped. `\nLanded: R-0747 — ` still occurs exactly 1 time at C2.

**G4 THE LEDGER — REAL_EXIT=0, every ordered numeral reproduced.**

| reading | at `d0c86c2d` | at C2 `ce6c2866` | ordered |
|---|---|---|---|
| registered `^- R-\d+ — ` | 308 lines / 308 distinct | 308 / 308, ids ADDED: none | 308 distinct UNMOVED ✓ |
| resolved `^Done: R-\d+ — ` | 52 lines / 50 distinct | 53 / 51 | 52/50 → 53/51 ✓ |
| id ADDED to the resolved set | — | exactly `R-0747` | ✓ |
| `^Landed: ` | 19 lines (16 distinct ids) | 19 lines (16 distinct ids) | 19 UNMOVED ✓ |
| `^Landed: R-0747 — ` | 1 | 1 | still exactly 1 ✓ |
| `^Gate: F033 R22 — ` | 0 | 1 | 0 before, exactly 1 after ✓ |
| open set (registered − resolved) | 308 − 50 = 258 | 308 − 51 = 257 | 258 → 257 ✓ |

**G5 THE CODE AGAINST THE SPEC, at C5 — REAL_EXIT=0.**
`python3 -m ruff check --no-cache <path>` exit 0 on all four changed files:
`packages/orchestration/hunk_decision_record.py` 0,
`packages/orchestration/pingpong_loop.py` 0,
`tests/orchestration/test_hunk_decision_record.py` 0,
`tests/orchestration/test_builder_prompt_hunk_rejections.py` 0.
By AST: `load_latest_hunk_ledger_from_metadata` is defined at MODULE level in
`hunk_decision_record.py` (exactly 1 such def), carries no leading underscore, and its
name appears in that module docstring's `Public API::` block. `run_pingpong` carries
`hunk_ledger` as a KEYWORD-ONLY parameter whose default is the constant `None`, with no
positional twin. Exactly 1 `compose_builder_prompt` call exists inside `run_pingpong`
and it passes `hunk_ledger=hunk_ledger` as a plain Name.
DECISION F033 D4's standing property, SPEC A7's claim: occurrences of `open(` in
`hunk_decision_record.py` = **0**; occurrences of `save_job` = **0** (both counted as
substring occurrences over the whole source, not as matching lines). See deviation D5 —
an early draft of the new docstring pushed `save_job` to 1 and was reworded before C3.

**G6 MUTATION RED-PROOFS — run ONLY in the disposable worktree `.remedy-wt/wt-r23`
at C5, `python3 -B`, `__pycache__` purged before every run.**
Scope of each run: both changed test files together.

- UNMUTATED CONTROL, run FIRST: **REAL_EXIT=0, 39 passed in 0.83s.**
- (i) the selector returns the FIRST matching record instead of the latest — anchor
  occurrences in `hunk_decision_record.py`: **exactly 1**. Result: **REAL_EXIT=1,
  3 failed, 36 passed.** FAILED
  `test_the_latest_decision_for_a_task_wins_in_both_insertion_orders`,
  `test_two_decisions_sharing_one_stamp_resolve_to_the_last_recorded`,
  `test_with_no_parseable_stamp_the_last_recorded_decision_wins`.
  Restored; sha256 identical to pre-mutation:
  `e443b6b25880fa7b308852089cade1962bd8558934ece60ee9d6cccd155db083`.
- (ii) SPEC A5's structural guard removed so a malformed input raises (the `except`
  body replaced by a bare `raise`) — anchor occurrences: **exactly 1**. Result:
  **REAL_EXIT=1, 2 failed, 37 passed.** FAILED
  `test_no_malformed_metadata_makes_the_reader_raise_or_answer_partially` and
  `test_a_task_with_no_recorded_decision_yields_an_empty_ledger`. The guard is
  genuinely REACHABLE, so the answer the gate permits — "this mutation reddened
  nothing" — did NOT arise. Restored; sha256 identical, same digest as above.
- (iii) `run_pingpong` stops forwarding `hunk_ledger` at the `compose_builder_prompt`
  call — anchor occurrences in `pingpong_loop.py`: **exactly 1**. Result:
  **REAL_EXIT=1, 1 failed, 38 passed.** FAILED
  `test_a_rejection_reason_reaches_the_real_loops_composed_builder_prompt` — the
  acceptance test, and the proof that the end to end is really end to end. Restored;
  sha256 identical:
  `bcdd613be3bfdc3c91bb30e728929dace7f5f1f02b0795bf62cb30f8165fc518`.
- POST-RESTORE CONTROL: **REAL_EXIT=0, 39 passed in 0.83s** — the worktree is back at
  the committed state.

Note: G6 was executed TWICE end to end. The first execution produced identical exit
codes and counts but its name-extraction printed `FAILED FAILED`; the driver was fixed
to read the node id and the whole gate re-run. Both runs are reported as one result
because the mutations, anchors and outcomes were identical.

**G7 THE SUITES, SERIALLY, in the PRIMARY checkout at C5 — every REAL exit 0.**

| suite | REAL_EXIT | result |
|---|---|---|
| `tests/orchestration/test_hunk_decision_record.py` | 0 | 23 passed in 0.63s |
| `tests/orchestration/test_builder_prompt_hunk_rejections.py` | 0 | 16 passed in 0.36s |
| `tests/orchestration/test_hunk_ledger.py` | 0 | 44 passed in 0.22s |
| `tests/orchestration/test_hunk_repair_findings.py` | 0 | 17 passed in 0.20s |
| `tests/orchestration/test_builder_prompt_golden.py` | 0 | 21 passed in 0.26s |
| `tests/orchestration/test_pingpong.py` | 0 | 34 passed in 0.69s |
| `tests/orchestration/test_pingpong_cli.py` | 0 | 172 passed in 2.69s |
| `tests/cli/test_golden_path.py` (canary) | 0 | 42 passed in 22.46s |

One UNORDERED extra check, run because C1 rewrote `.agent/plan.md`:
`tests/ui_server/test_dashboard_contract.py` → REAL_EXIT=0, 74 passed in 4.01s.

**G8 STRUCTURE — REAL_EXIT=0.**
`git status --porcelain` in the primary checkout: **EMPTY** (`''`).
Per-commit insertions from `git diff --numstat`, every one under 500 and every commit
single-parent: C0a 350, C0b 256, C1 14, C2 4, C3 108, C4 29, C5 343.
Path set over `d0c86c2d`..C5, sorted: `.agent/authored/f033-r23.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`packages/orchestration/hunk_decision_record.py`,
`packages/orchestration/pingpong_loop.py`,
`tests/orchestration/test_builder_prompt_hunk_rejections.py`,
`tests/orchestration/test_hunk_decision_record.py`. This EQUALS the declared change set
minus `.agent/handoff.md` in BOTH directions — missing: none; extra: none.
ORDERED EQUALITY for both appended test files:
- `test_hunk_decision_record.py`: pre 18404 bytes → post 28517; the pre-commit blob is a
  byte PREFIX of the committed blob; 0 deleted lines; 188 added lines equal the 188-line
  appended suffix IN ORDER.
- `test_builder_prompt_hunk_rejections.py`: pre 12848 → post 19928; byte PREFIX True;
  0 deleted lines; 155 added lines equal the 155-line appended suffix IN ORDER.

**Push.** `git push -u origin feature/f033-hunk-approval-v2` is the round's last action
and necessarily runs AFTER C6 is committed, so its outcome cannot appear in the file C6
adds — the write-once rule forbids a second handoff commit to record it. The reviewer
reads the push from the remote: `origin/feature/f033-hunk-approval-v2` must point at C6.
The worker reports the real exit code in its session output.

## Authored-text proofs

Two reviewer-authored texts were applied this round, both extracted by script from
`.remedy-wt/f033-r23-block.md` between their `<<<BEGIN`/`<<<END` marker lines,
exclusive, and never retyped or reflowed:

- **PLAN23** → `.agent/plan.md`. 2690 bytes, sha256
  `be450d505e65f31f60a75c2a52cd1eb5a0d38b73d412590b2285e9ba31df7d6a`. The committed
  blob at C5 is byte-EQUAL to the extracted slice (G2).
- **RECORD23** → appended to `.agent/live_review.md`. 6800 bytes, sha256
  `bc4a18b7e05886178ef66b6adf9e16591b0c5ae3c46df0626fb5290255ac4fdb`. The committed
  blob at C2 is the base plus one `\n` plus the slice, exactly (G3).

The block itself went to `.agent/authored/f033-r23.md` and `.agent/last_block.md`
through `shutil.copyfile` — a disk-to-disk copy, so one end of each `cmp` is the
emitted artefact itself. Both comparisons REAL_EXIT=0 and silent (G1).

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block verbatim | done | `9ba7f6ec`; `cmp` silent, digest equal |
| C0b mirror into `last_block.md` | done | `0527a1a3`; `cmp` silent |
| C1 rewrite `plan.md` from PLAN23 | done | `7fe2f553`; byte-equal, 49 lines |
| C2 append RECORD23 | done | `ce6c2866`; books the R22 PASS, resolves R-0747, `Landed:` line untouched |
| C3 SPEC A | done | `39acdfb0` |
| C4 SPEC B | done | `88197da8` |
| C5 SPEC C | done | `5fe56ddb` |
| C6 handback | done | this file; its sha is C6 itself and is unmeasurable at authoring time |
| A1 `import_hunk_ledger` into the EXISTING import block | done | one import statement, name placed last as ruff's isort orders it; ruff exit 0 |
| A2 one public function over a METADATA MAPPING | done | `load_latest_hunk_ledger_from_metadata(metadata, *, task_id)` → `HunkDecisionLedger`; `task_id` made keyword-only (deviation D4) |
| A3 the selection rule, in full, in the docstring | done | greatest parseable `decided_at` wins; unparseable never beats parseable; none-parseable or a tie → last in iteration order; states that nothing sorts the ids and why |
| A4 rebuild by handing the record STRAIGHT to `import_hunk_ledger` | done | no second row walk; the docstring names `_LEDGER_ROWS_KEY`, the shared export root key and the constant's own comment as where the deliberateness is recorded |
| A5 TOTAL, one SINGULAR structural guard | done | one `try` in the reader, no second one nested inside it; `_parsed_decision_stamp` is the SEPARATE parse guard and the docstring says which red-proof is aimed at which — G6(ii) reddens 2 tests, so the structural guard is reachable |
| A6 an empty ledger is the honest answer for "no decision" | done | stated in the docstring, with the reason a caller cannot and need not distinguish the two |
| A7 DELIBERATE ABSENCE — no storage I/O | done | documented in the idiom; `open(` 0 and `save_job` 0 in the module (G5) |
| A8 add the name to `Public API::` in the SAME commit | done | in `39acdfb0`; verified by AST at G5 |
| B1 keyword-only `hunk_ledger: Any = None` on `run_pingpong` | done | AST-verified keyword-only, default `None`, no positional twin; documented in the docstring |
| B2 forward it at the `builder_composed` call, change nothing else | done | one added keyword line; the call is otherwise byte-unchanged |
| B3 refresh the stale "does NOT supply this parameter yet" paragraph | done | now states that the loop forwards a ledger it is GIVEN, keeps the R-0747 repair's storage route including `save_job`, names `load_latest_hunk_ledger_from_metadata`, and names `pingpong_job.py` as the one unwired hop |
| B4 do NOT change `pingpong_job.py` or `do_cmd.py` | done | neither appears in the path set over the range (G8) |
| C1 (SPEC C) selection tests | deviated | all six behaviours covered; the malformed-input set is a TABLE walked in one test rather than `pytest.mark.parametrize` — see deviation D2 |
| C2 (SPEC C) faithful rebuild round trip | done | `test_a_decision_recorded_through_the_view_door_reads_back_as_its_own_ledger` compares against the `ledger` field of the returned `HunkDecisionRecord`, using the file's existing `_job` and `_record_from_view` helpers |
| C3 (SPEC C) the acceptance test, three links | done | (a) exactly 1 `builder_hunk_rejections` manifest row over the real run's traces; (b) the reason an EXACT substring of the segment cut out by its own span from a DIRECT composition with a different goal, context, findings, staged state and task body; (c) the row's `sha256` equals the sha256 of that text. G6(iii) reddens it |
| C4 (SPEC C) the negative half | done | `test_a_loop_round_with_no_hunk_ledger_composes_no_rejection_segment`; non-vacuous — it asserts `builder_system` IS present and the rejection segment is not |
| G1 transport | PASS | REAL_EXIT=0 |
| G2 the plan | PASS | REAL_EXIT=0 |
| G3 the record append | PASS | REAL_EXIT=0, with the base numeral corrected (D1) |
| G4 the ledger | PASS | REAL_EXIT=0, every ordered numeral reproduced |
| G5 the code against the spec | PASS | REAL_EXIT=0 |
| G6 mutation red-proofs | PASS | control 0/39 passed; (i) 1/3 failed, (ii) 1/2 failed, (iii) 1/1 failed |
| G7 the suites | PASS | eight suites, every REAL_EXIT=0 |
| G8 structure | PASS | REAL_EXIT=0 |

## Deviations & assumptions

**D1 — the block's `.agent/live_review.md` base size is stale by 156 bytes. Applied as
written; the numeral is corrected, not the action.** Constraint 2 and G3 both state
1588184 bytes at `d0c86c2d`. The measured size at `d0c86c2d` is **1588340**. 1588184
is the size at `61d2ffe7`, which is round 22's record-append commit; round 22's own C3
`72dcfd53` then appended the 156-byte `Landed: R-0747 — …` line, and the reviewer
carried the earlier number forward into this block. The APPEND FORM the block ordered —
one blank-line separator then the slice — is unaffected and was applied unchanged, and
G3's reconstruction holds exactly against the measured base. Nothing was repaired on the
worker's initiative; only the reading is reported.

**D2 — SPEC C's C1 asked for the malformed-input cases "parametrized"; they are a TABLE
walked inside one test instead.** `pytest.mark.parametrize` needs `import pytest` at
module scope. `tests/orchestration/test_hunk_decision_record.py` carries no such import,
and both the block's SPEC C preamble and Constraint 4 forbid editing one existing line of
that file, so the import cannot be added to the block at the top. A module-level `import`
appended at the BOTTOM is ruff `E402`, which G5 would turn red — measured with a probe,
not assumed: `python3 -m ruff check --no-cache` on a file with a late module-level import
gave `E402 Module level import not at top of file`, REAL_EXIT=1. The contrast C1 actually
draws — a table rather than one test function per input — is honoured: 12 shapes in one
list, walked with their OUTCOMES collected and compared as a whole list, so a case that
raises cannot hide the cases after it and the failure message names the shape. The same
constraint is why the appended section resolves
`load_latest_hunk_ledger_from_metadata` and `HunkDecisionLedger` with function-local
imports, the way this feature's other test file already resolves `hashlib`. All of this is
written into a comment at the head of the appended section.

**D3 — one paragraph of `hunk_decision_record.py`'s MODULE docstring was edited, which
SPEC A did not order.** It opened "THIS MODULE IS NOT TOTAL", a whole-module claim that
SPEC A's total reader falsifies. It now reads "THE TWO RECORDING DOORS ARE NOT TOTAL",
with its body re-pointed at the two doors and one closing sentence naming the reader as
the one total exception and why. The file is inside the change set and no line count or
digest gate covers that paragraph. The reason for doing it rather than leaving it is
R-0747 itself: a false blanket claim in the exact paragraph the next reader meets is the
defect class this branch just spent a round resolving. Declared here because it is an
edit the block did not ask for.

**D4 — `task_id` is KEYWORD-ONLY on the new function.** SPEC A2 fixes the arguments but
not their kind. Both arguments are of unconstrained type, a swap of a mapping and an id
would be silent, and AGENTS.md's discoverability rules ask for exactly this defence. The
module's own idiom agrees — every other public function here takes everything after the
first argument by keyword.

**D5 — a `save_job` occurrence was introduced and removed before C3 was committed.** The
first draft of the new function's DELIBERATE ABSENCE paragraph wrote "a job load, a
``save_job`` or an ``open``", which took the module's `save_job` occurrence count from 0
to 1 and would have turned G5's zero-reading red. The worker's own pre-commit check
caught it and the sentence was reworded to "a job load, a persisting write or a file
read" before anything was staged. No committed state ever carried it; reported because
the gate exists to catch precisely that and it nearly fired on prose.

**D6 — `test_builder_prompt_hunk_rejections.py`'s module docstring still carries its
now-superseded closing paragraph.** It says "nothing here asserts that the RUN LOOP
supplies a ledger. It does not yet", which C4 makes false. That file is APPEND ONLY under
the block's SPEC C preamble and Constraint 4, so the paragraph could not be rewritten. A
correction is APPENDED instead, as the first comment of the new section, stating in as many
words that the module docstring is superseded from there down and why it was corrected
rather than rewritten. If the reviewer prefers the docstring itself repaired, that needs a
block that lifts the append-only obligation for this file.

**D7 — G6 was executed twice.** The first pass produced the same exit codes, the same
counts and the same anchor-uniqueness readings, but its transcript printed `FAILED FAILED`
because the driver split the pytest summary line on the wrong field. The driver was
corrected to read the node id and the entire gate — control, three mutations, restores and
post-restore control — was re-run from scratch. The reported numbers are the second run's;
they match the first in every figure.

**D8 — two unordered readings were taken.** `tests/ui_server/test_dashboard_contract.py`
was run because C1 rewrote `.agent/plan.md` and that suite pins the file's `Steps`
contract (REAL_EXIT=0, 74 passed); and the distinct-id count behind `^Landed: ` was
recounted separately after the first G4 script captured the literal prefix rather than
the id, giving 19 lines over 16 distinct ids at both revisions. Neither changed a verdict.

No assumption was made about anything the block left open beyond D2 and D4, and no gate
was weakened, skipped or re-scoped. No test or assertion was weakened at any point. No
file outside the change set was touched. `.remedy-wt/f033-r23-block.md` was read only;
every scratch file this round created is a new path under `.remedy-wt/`.

## Next

The reviewer re-runs G1-G8 at `5fe56ddb` and reads the real diff. On a PASS, the next
round is the last wiring hop, already named in `.agent/plan.md`: teach the JOB-level
caller in `packages/orchestration/pingpong_job.py` — the one place that actually holds
the job at its `run_pingpong` call — to read the task's latest recorded decision with
`load_latest_hunk_ledger_from_metadata` and pass it as `hunk_ledger`, with a test that
follows a decision recorded on a real job through to the composed prompt. After that:
R-0745's transitive-import-closure test, then the `docs/` operator description of
`remedy patch approve-hunks`, then the integration gate and closure. The scope report
amend0827 rule 6 requires is carried by the session-6 handoff, since steps 2-4 plus the
two closure rounds exceed what the 25-round soft limit leaves.
