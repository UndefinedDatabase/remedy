# Handback — F038, round 5 (book round 4, record DECISION F038 D6, and land T002's first
half: the mechanical intent parse, the action card and the write door's request body, with
nothing sent)

## Session

SESSION 1 of feature F038 · round 5 · rounds so far 5. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, both
payloads and the records diff before writing anything, read every named source file whole
(`UI_EXPOSED_COMMANDS` in `command_catalog.py`, `nonce_is_valid` in `command_nonce.py`,
`_read_command_payload` and the `job.stop`/`job.pause`/`job.unpause`/`job.veto-task`/
`job.steer`/`chat.send`/`job.rerun-subtree` dispatch methods of `ui_server.py`,
`steeringSend.ts`, `test_no_orphan_modules.py`), verified every payload and every committed
copy for real, applied `records.diff`, wrote the parse/card/payload module from the
specification, wrote 33 tests, wrote a fresh 10-mutation red-proof tool, found and fixed a
real bug in that tool's own output parsing after its first G5 run (declared below), re-ran
G5 for real in a disposable worktree, ran the pinned serial test selection and the integrity
check to completion, and ran every gate (G1–G5) for real before writing this handback.

## Range

Review of `8aff505d6..HEAD` (`HEAD` is this handback's own commit, `F038 R5 C5`, on
`feature/f038-grounded-chat`).

## Commits

### 41002992a F038 R5 C1a: copy round 5 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r5-block.md | 288/0 | copy of the block, verified line count (288) and sha256 |
| .agent/authored/f038-r5-plan.md | 29/0 | copy of the reviewer's plan.md payload |

317 insertions total, exactly the block's own note: 288-line block + 29, under the 500-line cap.

### 7a5a0457a F038 R5 C1b: copy round 5 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r5-records.diff | 63/0 | copy of the reviewer's records.diff payload |

Measured 63 insertions, exactly the block's expected reading.

### f2433caed F038 R5 C2: book round 4 and record DECISION F038 D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 45/0 | `git apply records.diff` — appends DECISION F038 D6 |
| .agent/live_review.md | 2/0 | `git apply records.diff` — books round 4's Gate entry |
| .agent/plan.md | 6/5 | rewritten to plan.md payload by `shutil.copyfile` |

Measured numstat matches the block's table exactly: 45/0, 2/0, 6/5.

### b40899f08 F038 R5 C3: parse a chat request into a question, an action card or unknown
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_intent.py | 202/0 | NEW FILE — S1 constants and `ChatIntentError`, S2 `ChatIntent`/`ChatActionCard`, S3 `parse_chat_intent`, S4 `build_action_card`, S5 `card_command_payload` |
| tests/test_no_orphan_modules.py | 3/0 | S6 — `ALLOWED_UNWIRED` entry for `chat_intent.py`, between `chat_answer.py` and `ci_budgets.py`, split over lines as its neighbours are |

No insertion count was expected by the block for C3; measured 205 total, under the cap.

### fd338b92f F038 R5 C4: test the intent parse, the cards and the door payload
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_intent.py | 251/0 | NEW FILE — 33 tests covering every "at least one each" bullet: the verb-table/catalog cross-check, the five question texts, stop/pause/unpause, the note split by focus, veto and rerun completeness/missing combinations, unknown texts, the note card's exact lines, the focused-veto card's exact lines, the unknown card, the question-card raise, the exact stop payload, the bad-nonce raise, the incomplete/unknown-card raises, and the no-file-written proof |
| .agent/authored/f038-r5-mutations.py | 149/0 | the G5 tool (first version): 10 mutations (r1–r10) against `chat_intent.py`, run against `tests/orchestration/test_chat_intent.py` |

400 insertions total, under the 500-insertion cap.

### 4ee5f77b3 F038 R5 C4b: fix the mutation tool's failed-count and node-id parsing
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r5-mutations.py | 8/8 | G5's first run showed every mutation red at the right exit code, but the tool's own `_failed_count_and_nodes` read `failed=0` and blank node ids for every one of them — declared as a deviation below |

8 insertions, 8 deletions, well under the 500-insertion cap. **This commit is not in the
block's ordered BUNDLE list**; see Deviations.

### \<C5-sha\> F038 R5 C5: rewrite handoff for round 5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f038-r5-mut fd338b92f` — added the disposable G5
  worktree at C4. Outcome: `Preparing worktree (detached HEAD fd338b92f)`, exit 0.
- `python3 -B .agent/authored/f038-r5-mutations.py .../.remedy-wt/f038-r5-mut` (first run,
  buggy tool) — outcome: all 10 mutations exit 1 (genuinely red), but every one reported
  `failed=0 nodes=[]` — a defect in the tool's own output parsing, not in the mutations or
  the product code. Both controls exit 0, `restored byte-identical: True`, final line `True`.
- Fixed `.agent/authored/f038-r5-mutations.py`'s `_failed_count_and_nodes` in place (not
  inside the worktree — the target file `chat_intent.py` the tool mutates lives in the
  worktree, but the tool script itself runs from the primary checkout's own copy).
- `python3 -B .agent/authored/f038-r5-mutations.py .../.remedy-wt/f038-r5-mut` (second run,
  fixed tool) — outcome: all 10 mutations exit 1 with real failed counts (1–6) and real
  failing node ids, both controls exit 0, `restored byte-identical: True`,
  `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove --force .remedy-wt/f038-r5-mut` — outcome: exit 0.
- `git worktree prune` — outcome: exit 0.
- `git push origin feature/f038-grounded-chat` — reported under G6 in the round reply (run
  after this file's own commit, so its outcome is reported there rather than tabled here,
  per the handback template's self-reference exception).

## Verification

### BEFORE ANYTHING ELSE
1. `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, exit 2. Absent.
2. `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty, exit 0.
   `git branch --show-current` → `feature/f038-grounded-chat`. `git log --oneline -1` →
   `8aff505d6 F038 R4 C5: rewrite handoff for round 4`.
3. Block bytes: measured line count 288, sha256
   `f4f3e35d42121c4504270bcbac1432839af51e1d1ea16c39826230e89dc1ccfe`; both equal the two
   readings the delegation message stated.
4. `git worktree list | wc -l` → `70`.

### PAYLOADS
| file | measured lines | measured bytes | measured sha256 | matches table |
|---|---|---|---|---|
| records.diff | 63 | 13152 | 6a5d4a2f8afdb1269d1e720ccc0a9b6e4081cdc7ad846f358b64efa9a00b5ebf | yes |
| plan.md | 29 | 974 | 571c99b525980bfcbdd99259e3aba263928f043be52321dd738602a68f1b2565 | yes |

### G1 TRANSPORT
`git apply --check .remedy-wt/f038-r5-payloads/records.diff` → exit 0. Real `git apply` → exit 0.
Each `.agent/authored/f038-r5-*` copy compared byte-for-byte against its source, read back with
`git show <commit>:<path>`:
- `41002992a:.agent/authored/f038-r5-block.md` == `.remedy-wt/f038-r5/block.md` — MATCH (sha256
  `f4f3e35d...e89dc1ccfe` both).
- `41002992a:.agent/authored/f038-r5-plan.md` == `.remedy-wt/f038-r5-payloads/plan.md` — MATCH
  (sha256 `571c99b5...602a68f1b2565` both).
- `7a5a0457a:.agent/authored/f038-r5-records.diff` == `.remedy-wt/f038-r5-payloads/records.diff`
  — MATCH (sha256 `6a5d4a2f...358b64efa9a00b5ebf` both).

### G2 THE RECORDS
sha256 of each file read with `git show f2433caed:<path>`:
| path | bytes | sha256 | matches reviewer's reading |
|---|---|---|---|
| .agent/decisions.md | 2394024 | 8d4cbb3eb1c3b5efd266cbf632f376acfa1ce61825ef732b2e4626af76418c62 | yes |
| .agent/live_review.md | 320874 | 29156a4a862e8f4dff6ace0536ca125bab671ab28090cf6bcf394f0743625338 | yes |
| .agent/plan.md | 974 | 571c99b525980bfcbdd99259e3aba263928f043be52321dd738602a68f1b2565 | yes |

`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s text at
`f2433caed` → `[]`, matching the reviewer's stated reading.

`git diff --name-only 7a5a0457a f2433caed` →
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Names exactly the three paths of the table above.

### G3 THE CODE
`python3 -m ruff check packages/orchestration/chat_intent.py
tests/orchestration/test_chat_intent.py tests/test_no_orphan_modules.py` at C4 →
`All checks passed!`, exit 0.

Quoted from `git show b40899f08` (C3), the whole of the three named functions:

```python
def parse_chat_intent(text: str, *, focused_task_id: str = "") -> ChatIntent:
    """One line of chat becomes a QUESTION, an ACTION or UNKNOWN (S3)."""
    folded = _fold(text)
    if folded[:7].lower() == "please ":
        folded = folded[7:]
    if not folded:
        return ChatIntent(kind=CHAT_INTENT_UNKNOWN)
    if _is_question(folded):
        return ChatIntent(kind=CHAT_INTENT_QUESTION)

    first_word = folded.split(" ", 1)[0].lower()

    if first_word in _STOP_WORDS:
        return _action_intent("job.stop", {"reason": _reason_after_because(folded)})
    if first_word == "pause":
        return _action_intent("job.pause", {})
    if first_word in _UNPAUSE_WORDS:
        return _action_intent("job.unpause", {})

    note_match = _NOTE_PATTERN.match(folded)
    if note_match:
        message = folded[note_match.end():]
        if focused_task_id:
            return _action_intent(
                "job.steer", {"task_id": focused_task_id, "message": message})
        return _action_intent("chat.send", {"message": message})

    if first_word in _VETO_WORDS:
        return _action_intent(
            "job.veto-task",
            {"task_id": focused_task_id, "reason": _reason_after_because(folded)})

    if first_word in _RERUN_WORDS or _RUN_AGAIN_PATTERN.match(folded):
        return _action_intent("job.rerun-subtree", {"task_id": focused_task_id})

    return ChatIntent(kind=CHAT_INTENT_UNKNOWN)


def build_action_card(intent: ChatIntent, *, job_id: str) -> ChatActionCard:
    """An intent becomes what a person confirms (S4). A QUESTION has nothing to confirm:
    it belongs to the read path, and building a card for it is a caller error."""
    if intent.kind == CHAT_INTENT_QUESTION:
        raise ChatIntentError(
            "a question belongs to the read path, not an action card")
    if intent.kind == CHAT_INTENT_UNKNOWN:
        available = ", ".join(CHAT_AVAILABLE_ACTIONS)
        return ChatActionCard(
            verb="", title=CHAT_UNKNOWN_TITLE,
            lines=(f"Available: {available}.",),
            args={}, missing=(), confirmable=False)

    lines = [f"Job: {job_id}"]
    if "task_id" in intent.args:
        lines.append(f"Task: {intent.args['task_id']}")
    if "message" in intent.args:
        lines.append(f"Message: {intent.args['message']}")
    if "reason" in intent.args:
        lines.append(f"Reason: {intent.args['reason']}")
    if intent.missing:
        lines.append(f"Needs: {', '.join(intent.missing)}. Say it again with them.")
    lines.append(f"Command: {intent.verb}")
    return ChatActionCard(
        verb=intent.verb, title=CHAT_VERB_TITLES[intent.verb], lines=tuple(lines),
        args=dict(intent.args), missing=intent.missing, confirmable=not intent.missing)


def card_command_payload(card: ChatActionCard, *, client_nonce: str) -> dict:
    """A complete card's body, in the write door's own argument names (S5)."""
    if not card.confirmable:
        raise ChatIntentError(
            "this card is not confirmable, so it has no command to send")
    if not nonce_is_valid(client_nonce):
        raise ChatIntentError("client_nonce is not a usable id")
    return {"command": card.verb, "client_nonce": client_nonce, "args": dict(card.args)}
```

### G4 THE TESTS
Serial run, at C4, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py 2>&1 | tail -30; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
Output:
```
501 passed, 6 skipped in 67.96s (0:01:07)
REAL_EXIT=0
```
The six `SKIPPED` lines are exactly the F252 quarantine (`tests/regression/test_named_bugs.py`
lines 295, 312, 321, 383, 392, 399), matching the reviewer's own primary-checkout baseline.

Node count of `tests/orchestration/test_chat_intent.py` by `--collect-only -q` at C4: 33 tests.

Accounting for the difference from the reviewer's base 468 passed at `8aff505d6`: this round
added exactly 33 new nodes in `tests/orchestration/test_chat_intent.py` and touched no other
test file's collection. 468 + 33 = 501, exactly the measured total. The skip count is
unchanged at 6 because the round added no new skip.

`python3 -m apps.cli.main integrity check --json`:
```json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0, exit 0.

### G5 THE RED PROOFS
`git worktree add --detach .remedy-wt/f038-r5-mut fd338b92f` → exit 0
(`Preparing worktree (detached HEAD fd338b92f)`).

FIRST RUN (buggy tool — declared as a deviation, not papered over):
```
control (unmutated, first): exit=0 failed=0 nodes=[]
r1 nothing is ever a question: exit=1 failed=0 nodes=['', '', '', '', '', '']
r2 a ?-ended text is a question only with a question word: exit=1 failed=0 nodes=['', '', '']
r3 a note goes to the job even when a task is focused: exit=1 failed=0 nodes=['', '']
r4 nothing is ever missing: exit=1 failed=0 nodes=['', '', '', '', '', '']
r5 an unknown request is read as a question: exit=1 failed=0 nodes=['', '', '', '']
r6 a card that is not confirmable still yields a payload: exit=1 failed=0 nodes=['', '']
r7 the nonce is not checked: exit=1 failed=0 nodes=['']
r8 the reason after because is never taken: exit=1 failed=0 nodes=['', '', '']
r9 a note's message is lower-cased: exit=1 failed=0 nodes=['', '']
r10 a leading please is kept: exit=1 failed=0 nodes=['']
control (unmutated, last): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation's exit code was already 1 (genuinely red), and both controls already read exit
0 — the mutations and the product code were never in question. The tool's own
`_failed_count_and_nodes` was broken: its ternary's true branch sliced the literal word
"FAILED" instead of the pytest line, and its summary-line count only matched a line starting
with `=`, a decoration pytest omits when stdout is captured (non-tty), as this tool's
`subprocess.run(capture_output=True)` always is. Fixed both in commit C4b (see Deviations),
then re-ran:

SECOND RUN (fixed tool):
```
control (unmutated, first): exit=0 failed=0 nodes=[]
r1 nothing is ever a question: exit=1 failed=6 nodes=['tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[What changed?]', 'tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[did the tests pass]', 'tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[Can you stop it?]', 'tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[  why  ]', 'tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[stop it?]', 'tests/orchestration/test_chat_intent.py::test_question_card_raises']
r2 a ?-ended text is a question only with a question word: exit=1 failed=3 nodes=['tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[did the tests pass]', 'tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[  why  ]', 'tests/orchestration/test_chat_intent.py::test_question_texts_are_questions[stop it?]']
r3 a note goes to the job even when a task is focused: exit=1 failed=2 nodes=['tests/orchestration/test_chat_intent.py::test_tell_the_builder_with_focus_is_steer', 'tests/orchestration/test_chat_intent.py::test_note_card_lines_and_confirmable']
r4 nothing is ever missing: exit=1 failed=6 nodes=['tests/orchestration/test_chat_intent.py::test_tell_it_with_no_message_misses_message', 'tests/orchestration/test_chat_intent.py::test_skip_with_focus_misses_reason', 'tests/orchestration/test_chat_intent.py::test_veto_without_focus_misses_both', 'tests/orchestration/test_chat_intent.py::test_run_again_without_focus_misses_task_id', 'tests/orchestration/test_chat_intent.py::test_focused_veto_card_lines_and_not_confirmable', 'tests/orchestration/test_chat_intent.py::test_incomplete_card_raises_no_command']
r5 an unknown request is read as a question: exit=1 failed=4 nodes=['tests/orchestration/test_chat_intent.py::test_unrecognised_texts_are_unknown[deploy to production]', 'tests/orchestration/test_chat_intent.py::test_unknown_card_titled_and_lined_as_s4_states', 'tests/orchestration/test_chat_intent.py::test_unknown_card_raises_no_command', 'tests/orchestration/test_chat_intent.py::test_parsing_and_building_cards_writes_no_file']
r6 a card that is not confirmable still yields a payload: exit=1 failed=2 nodes=['tests/orchestration/test_chat_intent.py::test_incomplete_card_raises_no_command', 'tests/orchestration/test_chat_intent.py::test_unknown_card_raises_no_command']
r7 the nonce is not checked: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent.py::test_bad_nonce_raises']
r8 the reason after because is never taken: exit=1 failed=3 nodes=['tests/orchestration/test_chat_intent.py::test_stop_because_carries_its_reason', 'tests/orchestration/test_chat_intent.py::test_veto_because_with_focus_is_complete', 'tests/orchestration/test_chat_intent.py::test_stop_card_payload_is_exact']
r9 a note's message is lower-cased: exit=1 failed=2 nodes=['tests/orchestration/test_chat_intent.py::test_tell_the_builder_with_focus_is_steer', 'tests/orchestration/test_chat_intent.py::test_note_card_lines_and_confirmable']
r10 a leading please is kept: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent.py::test_please_cancel_is_stop_with_no_args']
control (unmutated, last): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation caught with at least one real failing node; both unmutated controls read exit
0; every mutation restored byte-identical. No mutation stayed green against the product code,
so constraint 4's "add the test that catches it" branch never fired — only the tool's own
report needed a fix.
`git worktree remove --force .remedy-wt/f038-r5-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list | wc -l` → `70`.

## Authored-text proofs

- `.agent/authored/f038-r5-block.md` (added at `41002992a`) == `.remedy-wt/f038-r5/block.md`,
  byte for byte (sha256 `f4f3e35d...e89dc1ccfe` both). MATCH.
- `.agent/authored/f038-r5-plan.md` (added at `41002992a`) == `.remedy-wt/f038-r5-payloads/plan.md`,
  byte for byte (sha256 `571c99b5...602a68f1b2565` both). MATCH.
- `.agent/authored/f038-r5-records.diff` (added at `7a5a0457a`) ==
  `.remedy-wt/f038-r5-payloads/records.diff`, byte for byte (sha256 `6a5d4a2f...358b64efa9a00b5ebf`
  both). MATCH.
- `.agent/plan.md` after C2 (`f2433caed`) == `.remedy-wt/f038-r5-payloads/plan.md`, byte for byte
  (sha256 `571c99b525980bfcbdd99259e3aba263928f043be52321dd738602a68f1b2565` both, confirmed under
  G2). MATCH.
- `records.diff` applied via `git apply` (not retyped); `.agent/decisions.md` and
  `.agent/live_review.md` after C2 match the reviewer's stated sha256 exactly (G2 table above).
  MATCH.

## Deviations & assumptions

1. **An extra commit, C4b, not in the block's ordered BUNDLE (C1a, C1b, C2, C3, C4, C5).**
   G5's first run against the tool committed in C4 showed every mutation exiting 1 (genuinely
   red against the product code) but reported `failed=0` and blank node ids for all ten,
   because `_failed_count_and_nodes` had two bugs: its ternary's matched branch sliced the
   literal string `"FAILED"` rather than the actual line, and its failed-count scan only
   matched a summary line starting with `=`, which pytest omits under a captured (non-tty)
   `subprocess.run`. This is a real defect in the round's own deliverable (the tool must
   "print... the failed count and the failing node ids" per G5), not a defect in the
   mutations or in `chat_intent.py`. AGENTS.md forbids amending or rewriting any commit,
   pushed or not, so the fix landed as a new commit, `F038 R5 C4b`, rather than folded back
   into C4. G5 was then re-run in full against the same worktree with the fixed tool, and
   every mutation now shows a real failed count and real node ids. Declared here per the
   handback template's instruction that any departure from the block's ordered commit
   sequence belongs in this section even when it is correct.
2. No payload was repaired, edited or retyped. No existing test was touched, and no existing
   assertion in any file was changed. No file outside the round's tracked path set (constraint
   3) was touched — confirmed by `git diff --name-only 8aff505d6` at the branch tip (see below).
3. No product-code gate went red at any point this round; only the tool's own report needed
   the fix declared above.
4. C4's 400 insertions and C4b's 8/8 are both well under the 500-insertion cap; no split was
   needed.

## Tracked path set (constraint 3)

`git diff --name-only 8aff505d6` at the branch tip after C5:
```
.agent/authored/f038-r5-block.md
.agent/authored/f038-r5-mutations.py
.agent/authored/f038-r5-plan.md
.agent/authored/f038-r5-records.diff
.agent/decisions.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
packages/orchestration/chat_intent.py
tests/orchestration/test_chat_intent.py
tests/test_no_orphan_modules.py
```
Exactly the block's constraint-3 set, no more and no less.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1 (STOP check) | done | |
| BEFORE ANYTHING ELSE 2 (repo state) | done | |
| BEFORE ANYTHING ELSE 3 (block bytes) | done | |
| BEFORE ANYTHING ELSE 4 (worktree count) | done | |
| PAYLOADS verification | done | |
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C4b | deviated | not in the block's BUNDLE list; fixes a defect in C4's own mutation tool, found by G5's first run — see Deviations item 1 |
| C5 | done | this commit |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | first run exposed the tool's own reporting bug (all mutations still genuinely red); second run, after C4b, shows real counts and node ids |
| G6 TREE AND PUSH | done | reported in the round reply, not tabled here (cannot precede this commit) |

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk. (2) The
review of round 5. (3) T002's second half: a confirmed card sent through the write door, and a
model-written parse for the verbs a sentence cannot fill. Open-findings count: 0.
Operator-questions count: 1.
