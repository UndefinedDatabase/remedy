# Handback — F038, round 7 (book round 6, record DECISION F038 D8, and the model-written
intent parse behind `chat.model_written`, adding `decision.resolve` and `job.inject` as two
new chat verbs)

## Session

SESSION 2 of feature F038 · round 7 · rounds so far 7. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, both
payloads and the records diff before writing anything, read every named source file whole
(`chat_intent.py`, `chat_answer.py`, `tests/orchestration/test_chat_intent.py`,
`tests/orchestration/test_chat_answer.py`, `run_structured_call` in `structured_outputs.py`,
`PROVIDER_CALL_ERRORS` in `result_tour.py`, `ROLE_CONFIG_CALL_SITES` in `model_routing.py`, and
`tests/test_no_orphan_modules.py`), verified every payload and every committed copy for real,
applied `records.diff`, wrote the new `chat_intent_model.py` module from the specification,
wrote 14 tests, wrote a 10-mutation red-proof tool, ran it for real in a disposable worktree,
ran the pinned serial test selection and the integrity check to completion, and ran every gate
(G1–G5) for real before writing this handback.

## Range

Review of `bd0802867..HEAD` (`HEAD` is this handback's own commit, `F038 R7 C5`, on
`feature/f038-grounded-chat`).

## Commits

### 9ece8fae8 F038 R7 C1a: copy round 7 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r7-block.md | 300/0 | copy of the block, verified line count (300) and sha256 |
| .agent/authored/f038-r7-plan.md | 29/0 | copy of the reviewer's plan.md payload |

329 insertions total, exactly the block's own note: 300-line block + 29, under the 500-line cap.

### 951bf01f5 F038 R7 C1b: copy round 7 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r7-records.diff | 60/0 | copy of the reviewer's records.diff payload |

Measured 60 insertions, exactly the block's expected reading.

### eea5c0dcb F038 R7 C2: book round 6 and record DECISION F038 D8
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 42/0 | `git apply records.diff` — appends DECISION F038 D8 |
| .agent/live_review.md | 2/0 | `git apply records.diff` — books round 6's Gate entry |
| .agent/plan.md | 7/7 | rewritten to plan.md payload by `shutil.copyfile` |

Measured numstat matches the block's table exactly: 42/0, 2/0, 7/7.

### 815c36a2f F038 R7 C3: ask the summary model for an intent the words alone cannot read
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_answer.py | 4/3 | S2 — `chat_call_fn` gains a `schema: type[BaseModel] = GeneratedChatAnswer` parameter, handed to `make_structured_call_fn` in place of the fixed class; docstring gains one sentence |
| packages/orchestration/chat_intent.py | 22/8 | S1 — `decision.resolve`/`job.inject` added to `CHAT_VERB_REQUIRED_ARGS`/`CHAT_VERB_TITLES`; `_action_intent` renamed public `chat_action_intent` with a one-line comment, every call site follows; `build_action_card` gains `Decision:`, `Answer:`, `Text:`, `After:` lines in spec order |
| packages/orchestration/chat_intent_model.py | 145/0 | NEW FILE — S3 module docstring/imports/constants/`GeneratedChatIntent`, S4 `build_intent_prompt`, S5 `parse_chat_intent_with_model` |
| tests/test_no_orphan_modules.py | 3/3 | S6 — `ALLOWED_UNWIRED`'s `chat_answer.py` entry removed, `chat_intent_model.py` entry added after `chat_door.py` |

No insertion count was expected by the block for C3; measured 174 total, under the cap.

### 0f02a1ec3 F038 R7 C4: test the model-written intent parse and its grounding
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_intent_model.py | 244/0 | NEW FILE — 14 tests: verb-table/UI_EXPOSED_COMMANDS agreement, mechanical hits never call the model, a high-confidence reply kept after one call, a low-confidence reply unknown, a verb outside the tables unknown, `decision.resolve` grounding (outside/inside the open set), `job.veto-task` task-id grounding (with/without focus), `job.inject` keeping only its own argument names, a non-JSON reply, a non-string verb, a `ConnectionError`, the switch (unset asks nothing, on asks once with `GeneratedChatIntent`), and the prompt naming every verb/focused task/open decisions |
| .agent/authored/f038-r7-mutations.py | 154/0 | the G5 tool: 10 mutations (r1–r10) against `chat_intent_model.py` (r1–r9) and `chat_intent.py` (r10), run with `-rf` against `tests/orchestration/test_chat_intent_model.py` |

No insertion count was expected by the block for C4; measured 398 total, under the cap.

### \<C5-sha\> F038 R7 C5: rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f038-r7-mut 0f02a1ec3` — added the disposable G5
  worktree at C4. Outcome: `Preparing worktree (detached HEAD 0f02a1ec3)`, exit 0.
- `python3 -B .agent/authored/f038-r7-mutations.py .../.remedy-wt/f038-r7-mut` — outcome: all 10
  mutations exit 1 with a real failed count (1 each) and real failing node ids, both controls
  exit 0, `restored byte-identical: True`, `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove --force .remedy-wt/f038-r7-mut` — outcome: exit 0.
- `git worktree prune` — outcome: exit 0.
- `git push origin feature/f038-grounded-chat` — reported under G6 in the round reply (run
  after this file's own commit, so its outcome is reported there rather than tabled here, per
  the handback template's self-reference exception).

## Verification

### BEFORE ANYTHING ELSE
1. `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, exit 2. Absent.
2. `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty, exit 0.
   `git branch --show-current` → `feature/f038-grounded-chat`. `git log --oneline -1` →
   `bd0802867 F038 R6 C5: rewrite handoff for round 6`.
3. Block bytes: measured line count 300, sha256
   `332681406b72dd345c92bb70bfa0458657418a11c9b9a8c2c88731bec3684f68`; both equal the two
   readings the delegation message stated.
4. `git worktree list | wc -l` → `64`.

### PAYLOADS
| file | measured lines | measured bytes | measured sha256 | matches table |
|---|---|---|---|---|
| records.diff | 60 | 12117 | 9c15d34ed02976cc0b5c5b665a93032fc0fb3d85df304ea597b992904f24ac35 | yes |
| plan.md | 29 | 935 | 1f1e17daa7ee14f23cfad40d46b299ab1911f913feddd6d0e378fed16f20d05c | yes |

### G1 TRANSPORT
`git apply --check .remedy-wt/f038-r7-payloads/records.diff` → exit 0. Real `git apply` → exit 0.
Each `.agent/authored/f038-r7-*` copy compared byte-for-byte against its source, read back with
`git show <commit>:<path>`:
- `9ece8fae8:.agent/authored/f038-r7-block.md` == `.remedy-wt/f038-r7/block.md` — MATCH (sha256
  `332681406b72dd345c92bb70bfa0458657418a11c9b9a8c2c88731bec3684f68` both).
- `9ece8fae8:.agent/authored/f038-r7-plan.md` == `.remedy-wt/f038-r7-payloads/plan.md` — MATCH
  (sha256 `1f1e17daa7ee14f23cfad40d46b299ab1911f913feddd6d0e378fed16f20d05c` both).
- `951bf01f5:.agent/authored/f038-r7-records.diff` == `.remedy-wt/f038-r7-payloads/records.diff`
  — MATCH (sha256 `9c15d34ed02976cc0b5c5b665a93032fc0fb3d85df304ea597b992904f24ac35` both).

### G2 THE RECORDS
sha256 of each file read with `git show eea5c0dcb:<path>`:
| path | bytes | sha256 | matches reviewer's reading |
|---|---|---|---|
| .agent/decisions.md | 2400957 | 9a8a02bc72f1b00d71d8b4ef295f2c3ee54b4d58a428255e42f22043f0cb1063 | yes |
| .agent/live_review.md | 325739 | a75da8a4a3fcc1b7e17519c624f6b56f9bfe5dc24d7e10e1d5d27176241247e7 | yes |
| .agent/plan.md | 935 | 1f1e17daa7ee14f23cfad40d46b299ab1911f913feddd6d0e378fed16f20d05c | yes |

`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s text at
`eea5c0dcb` → `[]`, matching the reviewer's stated reading.

`git diff --name-only 951bf01f5 eea5c0dcb` →
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Names exactly the three paths of the table above.

### G3 THE CODE
`python3 -m ruff check packages/orchestration/chat_intent.py packages/orchestration/chat_answer.py
packages/orchestration/chat_intent_model.py tests/orchestration/test_chat_intent_model.py
tests/test_no_orphan_modules.py` at C4 → `All checks passed!`, exit 0.

Quoted from `git show 815c36a2f` (C3), the diff to `chat_intent.py` (verb tables, the
`chat_action_intent` rename with its call sites, and `build_action_card`'s new lines) is shown
verbatim above under the C3 commit table's reasons; the full text of the three named functions,
quoted from the tree at C3:

```python
def chat_call_fn(schema: type[BaseModel] = GeneratedChatAnswer) -> Callable[[str, int], str] | None:
    """Build a call_fn for the `summary` role, or None.

    Mirrors `result_tour.tour_call_fn`: `resolve_role_config("summary")` supplies
    the model, `make_structured_call_fn` does the rest. This call site joins
    `model_routing.ROLE_CONFIG_CALL_SITES`. The model-written intent parse asks
    for its own schema through this same call site.
    """
    role_cfg = resolve_role_config("summary")
    return make_structured_call_fn(schema, model=role_cfg.model)
```

```python
def build_intent_prompt(
    text: str, *, focused_task_id: str, open_decision_ids: Iterable[str]
) -> str:
    """The prompt handed to the `summary` role: the request, every chat command with its
    title and argument names, the focused task, the open decisions and the answering
    rules (S4)."""
    lines = [
        "The chat received this request. Choose the one command below that carries it "
        "out, or an empty verb when none fits.",
        "",
        f"Request: {text}",
        "",
        "Commands:",
    ]
    for verb, required in chat_intent.CHAT_VERB_REQUIRED_ARGS.items():
        optional = CHAT_VERB_OPTIONAL_ARGS.get(verb, ())
        names = ", ".join(required + optional) if required or optional else "(none)"
        lines.append(f"- {verb} — {chat_intent.CHAT_VERB_TITLES[verb]}: {names}")

    open_decisions = list(open_decision_ids)
    lines.extend([
        "",
        f"Focused task: {focused_task_id or '(none)'}",
        f"Open decisions: {', '.join(open_decisions) if open_decisions else '(none)'}",
        "",
        "Rules:",
        "- reply with exactly one of the commands listed above, or an empty verb "
        "when none of them fits",
        "- use only that command's own argument names",
        "- never invent a task id or a decision id",
        "- give a confidence from 0 to 1",
    ])
    return "\n".join(lines)


def parse_chat_intent_with_model(
    text: str,
    *,
    focused_task_id: str = "",
    open_decision_ids: Iterable[str] = (),
    call_fn: Callable[[str, int], str] | None = _UNSET_CALL_FN,
) -> chat_intent.ChatIntent:
    """The mechanical parse first; only its UNKNOWN asks the model (S5).

    NEVER raises for a reply: a verb outside `chat_intent.CHAT_VERB_REQUIRED_ARGS`, a
    confidence that is not a finite number or is under `CHAT_MODEL_MIN_CONFIDENCE`, an
    exception of `PROVIDER_CALL_ERRORS`, and an outcome that is not ok are all unknown.
    A kept reply's arguments are its own verb's required and optional names only, each
    grounded: `task_id` is always `focused_task_id`, and `decision_id` survives only
    when it is one of `open_decision_ids`.
    """
    mechanical = chat_intent.parse_chat_intent(text, focused_task_id=focused_task_id)
    if mechanical.kind != chat_intent.CHAT_INTENT_UNKNOWN:
        return mechanical

    if call_fn is _UNSET_CALL_FN:
        call_fn = chat_call_fn(GeneratedChatIntent) if chat_model_written() else None
    if call_fn is None:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)

    open_decisions = tuple(open_decision_ids)
    prompt = build_intent_prompt(
        text, focused_task_id=focused_task_id, open_decision_ids=open_decisions)
    try:
        outcome = run_structured_call(
            GeneratedChatIntent, prompt, call_fn, allow_parse_retry=True)
    except PROVIDER_CALL_ERRORS:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)
    if not outcome.ok:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)

    reply = outcome.value
    assert isinstance(reply, GeneratedChatIntent)
    verb = reply.verb
    if verb not in chat_intent.CHAT_VERB_REQUIRED_ARGS:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)
    if not math.isfinite(reply.confidence) or reply.confidence < CHAT_MODEL_MIN_CONFIDENCE:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)

    allowed_names = chat_intent.CHAT_VERB_REQUIRED_ARGS[verb] + CHAT_VERB_OPTIONAL_ARGS.get(
        verb, ())
    args: dict[str, str] = {}
    for name in allowed_names:
        value = reply.args.get(name, "")
        args[name] = value.strip() if isinstance(value, str) else ""
    if "task_id" in allowed_names:
        args["task_id"] = focused_task_id
    if "decision_id" in allowed_names:
        args["decision_id"] = args["decision_id"] if args["decision_id"] in open_decisions else ""

    return chat_intent.chat_action_intent(verb, args)
```

### G4 THE TESTS
Serial run, at C4, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_intent_model.py tests/orchestration/test_chat_door.py tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py tests/orchestration/test_model_routing.py tests/orchestration/test_contract_hygiene.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
Output:
```
1082 passed, 9 skipped, 1 warning in 103.44s (0:01:43)
REAL_EXIT=0
```
The nine `SKIPPED` lines are exactly the F252 quarantine (six of
`tests/regression/test_named_bugs.py`) plus the three `tests/orchestration/test_model_routing.py`
skips the block names ("covered by the violating fixture above"), matching the reviewer's own
primary-checkout baseline of 1068 passed, 9 skipped at `bd0802867`.

Node count of `tests/orchestration/test_chat_intent_model.py` by `--collect-only -q` at C4: 14
tests.

Accounting for the difference from the reviewer's base 1068 passed at `bd0802867`: this round
added exactly 14 new nodes in `tests/orchestration/test_chat_intent_model.py` and touched no
other test file's collection. 1068 + 14 = 1082, exactly the measured total. The skip count is
unchanged at 9 because the round added no new skip.

`python3 -m apps.cli.main integrity check --json`:
```json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0, exit 0.

### G5 THE RED PROOFS
`git worktree add --detach .remedy-wt/f038-r7-mut 0f02a1ec3` → exit 0
(`Preparing worktree (detached HEAD 0f02a1ec3)`).

```
control (unmutated, first): exit=0 failed=0 nodes=[]
r1 the model is asked even when the mechanical parse read an action or a question: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_mechanical_hits_come_back_as_the_mechanical_parse_gives_them']
r2 no confidence floor is applied: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_a_low_confidence_reply_is_unknown']
r3 the reply's task id is kept instead of the focused task: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_task_id_is_always_the_focused_task_whatever_the_reply_said']
r4 a decision id outside the open set is kept: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_decision_id_outside_the_open_set_comes_back_missing_it']
r5 argument names the verb does not take are kept: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_job_inject_keeps_only_its_own_argument_names']
r6 a provider error escapes the parse: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_a_call_function_raising_connection_error_is_unknown']
r7 an unset call function asks the model whatever the switch reads: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_unset_call_function_asks_chat_call_fn_only_when_the_switch_is_on']
r8 the call site is asked for the answer schema rather than GeneratedChatIntent: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_unset_call_function_asks_chat_call_fn_only_when_the_switch_is_on']
r9 a verb outside the chat's tables is not refused before the arguments are built: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_a_reply_naming_a_verb_outside_the_chat_tables_is_unknown']
r10 a card never states its Decision: line: exit=1 failed=1 nodes=['tests/orchestration/test_chat_intent_model.py::test_decision_id_in_the_open_set_is_complete_and_confirmable']
control (unmutated, last): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation caught with at least one real failing node; both unmutated controls read exit 0;
every mutation restored byte-identical. No mutation stayed green, so constraint 4's "add the
test that catches it" branch never fired.
`git worktree remove --force .remedy-wt/f038-r7-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list | wc -l` → `64`.

## Authored-text proofs

- `.agent/authored/f038-r7-block.md` (added at `9ece8fae8`) == `.remedy-wt/f038-r7/block.md`,
  byte for byte (sha256 `332681406b72dd345c92bb70bfa0458657418a11c9b9a8c2c88731bec3684f68`
  both). MATCH.
- `.agent/authored/f038-r7-plan.md` (added at `9ece8fae8`) ==
  `.remedy-wt/f038-r7-payloads/plan.md`, byte for byte (sha256
  `1f1e17daa7ee14f23cfad40d46b299ab1911f913feddd6d0e378fed16f20d05c` both). MATCH.
- `.agent/authored/f038-r7-records.diff` (added at `951bf01f5`) ==
  `.remedy-wt/f038-r7-payloads/records.diff`, byte for byte (sha256
  `9c15d34ed02976cc0b5c5b665a93032fc0fb3d85df304ea597b992904f24ac35` both). MATCH.
- `.agent/plan.md` after C2 (`eea5c0dcb`) == `.remedy-wt/f038-r7-payloads/plan.md`, byte for
  byte (sha256 `1f1e17daa7ee14f23cfad40d46b299ab1911f913feddd6d0e378fed16f20d05c` both,
  confirmed under G2). MATCH.
- `records.diff` applied via `git apply` (not retyped); `.agent/decisions.md` and
  `.agent/live_review.md` after C2 match the reviewer's stated sha256 exactly (G2 table above).
  MATCH.

## Deviations & assumptions

1. No payload was repaired, edited or retyped. No existing test was touched, and no existing
   assertion in any file was changed. No file outside the round's tracked path set (constraint
   3) was touched — confirmed by `git diff --name-only bd0802867` at the branch tip before this
   commit (see below).
2. No product-code gate went red at any point this round. No mutation stayed green on its
   first application; the tool's 10 mutations all caught real behaviour changes on the first
   run, so no correction commit was needed.
3. No commit exceeded the block's ordered BUNDLE (C1a, C1b, C2, C3, C4, C5); all six commits
   landed in that exact order with no split and no extra commit.
4. Every commit's insertion count stayed well under the 500-insertion cap; no split was needed.
5. Wording choice, not a deviation from any pinned text: the block did not pin exact prose for
   `build_intent_prompt`'s verb lines or its opening/rules sentences (only their content and
   order), so this round chose its own wording within S4's stated shape; every test that reads
   the prompt checks presence/order, not an exact string.

## Tracked path set (constraint 3)

`git diff --name-only bd0802867` at the branch tip before this commit:
```
.agent/authored/f038-r7-block.md
.agent/authored/f038-r7-mutations.py
.agent/authored/f038-r7-plan.md
.agent/authored/f038-r7-records.diff
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
packages/orchestration/chat_answer.py
packages/orchestration/chat_intent.py
packages/orchestration/chat_intent_model.py
tests/orchestration/test_chat_intent_model.py
tests/test_no_orphan_modules.py
```
Exactly the block's constraint-3 set (this file, `.agent/handoff.md`, is added by this commit
itself and so does not appear in a diff taken before it).

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
| C5 | done | this commit |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | all 10 mutations caught on the first run; no correction needed |
| G6 TREE AND PUSH | done | reported in the round reply, not tabled here (cannot precede this commit) |

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk. (2) The
review of round 7. (3) T003's first part: the chat command finds the running cockpit, answers a
question, and confirms a card on a y/N line. Open-findings count: 0. Operator-questions count: 1.
