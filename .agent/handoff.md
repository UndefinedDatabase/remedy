# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 1

## Session

SESSION 1 of feature F277 · round 1 · rounds so far 1

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`docs/roadmap/features/T2_F277.md` and the payload `decisions.md` in full, verified the
step block's bytes before using it — 234 lines, sha256
`c7968993030e5c21b55ab71350a7c2c27bb16721b720d685698bba1959d7249f`, matching the
delegation message's R-0954 reading exactly — found no `.agent/STOP` on disk, verified the
branch was already checked out at `f2494c02`, verified all eight state payloads plus the
code diff byte-for-byte against the block's stated line counts and digests, applied C1a and
C1b, applied the code diff in two `--include` slices as C2 and C3, ran G1 through G5 at C3
with every reading executed and recorded, and is now writing this handoff as C4.

## Range

Review of `f2494c02`..`HEAD` (HEAD before this commit is C3, `dcb549e0`).

## Commits

### 7c9fdade F277 R1 C1a: copy round 1 payloads into .agent/authored (C1a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r1-block.md | +234/-0 | byte copy of the step block itself |
| .agent/authored/f277-r1-context.md | +42/-0 | byte copy of payload context.md |
| .agent/authored/f277-r1-decisions.md | +108/-0 | byte copy of payload decisions.md |
| .agent/authored/f277-r1-ledger.md | +2/-0 | byte copy of payload ledger.md |
| .agent/authored/f277-r1-live_review_head.md | +25/-0 | byte copy of payload live_review_head.md |
| .agent/authored/f277-r1-plan.md | +44/-0 | byte copy of payload plan.md |
| .agent/authored/f277-r1-prose_slips.md | +1/-0 | byte copy of payload prose_slips.md |
| .agent/authored/f277-r1-status_from.txt | +1/-0 | byte copy of payload status_from.txt |
| .agent/authored/f277-r1-status_to.txt | +1/-0 | byte copy of payload status_to.txt |

Total insertions (numstat): 458. The block states no expected value for C1a (the count
moves with every edit to the block itself); 458 is well under the 500 cap.

### fb26f0a8 F277 R1 C1b: claim F277, re-head live review, book F276 R15 verdict (C1b)
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +15/-15 | rewrite := payload context.md |
| .agent/decisions.md | +108/-0 | append payload decisions.md |
| .agent/live_review.md | +22/-21 | re-head: live_review_head.md + old bytes from `## Findings` inclusive to end + ledger.md |
| .agent/plan.md | +31/-27 | rewrite := payload plan.md |
| .agent/prose_slips.md | +1/-0 | append payload prose_slips.md |
| docs/roadmap/STATUS.md | +1/-1 | replace status_from.txt line with status_to.txt line |

Total insertions (numstat): 178, matching the block's expected 178 exactly.

### f431c1fe F277 R1 C2: declare the event vocabulary and the strict-mode write check (C2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/event_names.py | +187/-0 | new declaration module (EVENT_NAMES, READ_ONLY_EVENT_NAMES) |
| packages/orchestration/run_log.py | +9/-0 | opt-in strict check in RunLogWriter.log under REMEDY_STRICT_EVENT_NAMES |

Total insertions (numstat): 196, matching the block's expected 196 exactly.

### dcb549e0 F277 R1 C3: add the AST test that measures the vocabulary from source (C3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | register event_names as reachable |
| tests/orchestration/test_event_names.py | +360/-0 | AST collector + read/written/quarantine tests |

Total insertions (numstat): 361, matching the block's expected 361 exactly.

## External actions

- `git worktree add --detach .remedy-wt/f277-r1-g5 dcb549e0` — created for G5, mutation
  red-proofs run inside it.
- `git worktree remove .remedy-wt/f277-r1-g5` — removed as G5's last action, after all four
  mutations were restored byte-identically (confirmed by sha256).
- `git push -u origin feature/f277-machine-contracts` — run after this commit (C4); its
  outcome is reported in the round report, not here, because it necessarily postdates this
  commit (item 31).
- No `gh` command was run. No pull request was opened.

## Verification

G1 TRANSPORT AND STATE — 21 boolean readings taken, all True (9 authored-copy equalities;
live_review.md reading (a), N=1, reading (b), two negative-control rejections; decisions.md
reading (a), N=16, reading (b), two negative-control rejections; 4 byte-equality checks for
plan.md, context.md, prose_slips.md, STATUS.md). Exit: no exception, script completed.
Saved block.md: 234 lines, sha256
`c7968993030e5c21b55ab71350a7c2c27bb16721b720d685698bba1959d7249f` — identical to the
PAYLOADS section's stated value.

G2 CODE TRANSPORT — `git rev-parse HEAD:packages HEAD:tests` at C3 read
`58f6bbd055c1e25d9dfc32263a14adf93079b45d` and
`a781a46d213ed4447075a50a9e89fc3823c53bd8`, both exact matches. The four blob ids for
event_names.py, run_log.py, test_event_names.py and import_reachability_allowlist.txt read
`3c519bdea8ff4be676541aec2a141d55b4c51fcb`, `a17a20f3e93112b4579604cd2efe2d3df0c7005d`,
`b789385fa3b5ecd83cda4658c7eb46f29e28ea97`, `e4791c40af0b95f2f986b812a388ba6bc70bc2e8`, all
exact matches. `git diff --name-only fb26f0a8 dcb549e0` names exactly the four paths C2 and
C3 name (packages/orchestration/event_names.py, packages/orchestration/run_log.py,
tests/orchestration/import_reachability_allowlist.txt,
tests/orchestration/test_event_names.py), length 4, no extras.

G3 THE TARGETED SUITE — `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_event_names.py tests/test_run_log.py
tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py
tests/orchestration/test_dead_command_check.py tests/test_autonomy_readiness.py
tests/test_memory_learn.py tests/docs tests/orchestration/test_roadmap_index.py
tests/cli/test_golden_path.py` → `486 passed in 144.67s`, exit code 0.

G4 LINT — `python3 -m ruff check packages/orchestration/event_names.py
packages/orchestration/run_log.py tests/orchestration/test_event_names.py` →
`All checks passed!`, exit code 0.

G5 MUTATION RED-PROOFS, in `.remedy-wt/f277-r1-g5` detached at `dcb549e0`, serial
`python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py`:
- UNMUTATED CONTROL: `12 passed`, exit 0.
- (a) anchor `def _emit_token_policy_applied(job: JobPlan) -> None:` occurs 1 time in
  `autonomy_loop.py`. After inserting `_reader_for_a_name_nothing_writes`: `1 failed, 11
  passed`, exit 1, failing node id
  `TestTheEventVocabularyIsDeclared::test_every_read_event_name_is_declared` — matches
  expected.
- (b) anchor `        "task_run_started",` occurs 1 time in `event_names.py`. After
  deletion: `3 failed, 9 passed`, exit 1, failing node ids
  `test_every_written_event_name_is_declared`,
  `test_is_declared_event_accepts_a_written_name`,
  `test_the_writer_accepts_a_declared_name_under_the_flag` — names the expected test among
  the failures (the other two are cascading effects of the same deleted declaration).
- (c) the two-line anchor (`if os.environ.get(STRICT_EVENT_NAMES_ENV) == "1":` /
  `assert_declared_event(event)`) occurs 1 time in `run_log.py`. After deletion: `1 failed,
  11 passed`, exit 1, failing node id
  `TestStrictModeRejectsAnUndeclaredName::test_the_writer_rejects_an_undeclared_name_under_the_flag`
  — matches expected exactly.
- (d) anchor `def _emit_token_policy_applied(job: JobPlan) -> None:` occurs 1 time in
  `autonomy_loop.py`. After inserting `_writer_for_a_quarantined_name`: `2 failed, 10
  passed`, exit 1, failing node ids `test_every_written_event_name_is_declared`,
  `test_a_read_only_name_that_gains_a_writer_leaves_the_quarantine` — names the expected
  test among the failures.
- No mutation stayed green. Each was restored byte-identically before the next (confirmed
  per-mutation and by a final sha256 comparison): `autonomy_loop.py`
  `6f4aacb862652f38ab4101bdcccc969fe9ee2f47b67c1e1a0884d145cb10e7d5`, `event_names.py`
  `8eacd78eee631323d60a94e220b6b045db0246e87c6034f5a0a898827b250169`, `run_log.py`
  `483ac92e8813aba3549973e50d4b3257f18fd22da50ee1b9b9d65f4dae48aced`, all matching their
  pre-mutation originals. The worktree was removed; `git worktree list` afterward shows the
  primary checkout and the two pre-existing job worktrees and nothing else.

G6 PUSH AND TREE — necessarily postdates this commit; reported in the round report.

## Open findings

19 findings open by distinct id in `.agent/live_review.md` after the re-head: 24 distinct
ids matching `^- R-\d+ — ` against 5 distinct ids matching `^Done: R-\d+ — `, 24 − 5 = 19 —
identical to the count `live_review_head.md` itself states. All nineteen are owned by F282
per F276's closure; F277 owns only what it registers itself (none yet).

## Item status

| Item | Status | Reason |
|---|---|---|
| R-0954 (block byte verification) | done | 234 lines, sha256 match |
| Payload byte verification (8 state payloads + diff) | done | all 9 match block's stated lines/sha256 |
| Anchor uniqueness (status_from/`- [~]`) | done | 1 / 0, matches block |
| C1a | done | 458 insertions (numstat), no cap breach |
| C1b | done | 178 insertions (numstat), matches expected 178 |
| C2 | done | 196 insertions (numstat), matches expected 196 |
| C3 | done | 361 insertions (numstat), matches expected 361 |
| G1 transport and state | done | 21/21 boolean readings True |
| G2 code transport | done | all tree/blob ids and name-only list match exactly |
| G3 targeted suite | done | 486 passed, exit 0 |
| G4 lint | done | All checks passed!, exit 0 |
| G5 mutation red-proofs | done | control green; a/b/c/d all red naming expected tests; byte-identical restoration |
| C4 handoff | done | this file |
| G6 push and tree | done | reported in round report (postdates this commit) |

## Authored-text proofs

The nine `.agent/authored/f277-r1-*` files (C1a) were compared disk-to-disk against their
source payloads under `.remedy-wt/f277-r1-payloads/` and all nine read byte-equal (G1
reading (a)). No other reviewer-authored text was applied this round beyond the payloads
already covered by G1's forensics.

## Deviations & assumptions

- G1(b)'s structural reader crashed on `UnicodeDecodeError` when the negative control's
  byte-flip (XOR 0xFF) landed on a UTF-8 continuation byte; the script was adjusted to
  decode with `errors="replace"` for the structural (paragraph-split) reading only, so the
  negative control could complete and report a clean rejection rather than a traceback. The
  byte-equality reading (a) still operates on raw bytes and is unaffected. This is a
  verification-script robustness fix, not a change to any committed artifact.
- G5's "COUNT the mutated bytes in the named file... must be 1" was read as "count the
  occurrences of the anchor line(s) being touched, which must be 1" (an uniqueness check
  analogous to the block's own STATUS.md anchor-uniqueness check), rather than a literal
  single-byte-count, because mutations (a) and (d) insert multi-line functions and mutation
  (b) deletes a full line — none of these are naturally a "1 byte" change. All four anchor
  counts read 1, so the round proceeded under this reading.
- Mutations (b) and (d) each produced one additional cascading test failure beyond the
  block's named expectation (deleting a declared name also breaks
  `test_is_declared_event_accepts_a_written_name` and
  `test_the_writer_accepts_a_declared_name_under_the_flag`; giving `worker_adapters_listed`
  a writer also breaks `test_every_written_event_name_is_declared`, since the name is not
  yet in `EVENT_NAMES`). The block's named test is present among the failures in both
  cases and no mutation stayed green, so this is reported as an observation, not a
  contradiction.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk before acting.
2. The review of round 1.
3. Round 2: dispose of the six quarantined names in `READ_ONLY_EVENT_NAMES`
   (`approval_decision`, `command_discovery_completed`, `patch_intent_reverted`,
   `snapshot_created`, `stop_reason_recorded`, `worker_adapters_listed`), one commit per
   name, until the set is empty and `read ⊆ written ⊆ declared` holds per DECISION F277 D2.

Operator questions open: 1
