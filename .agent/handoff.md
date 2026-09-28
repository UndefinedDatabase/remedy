# Handback — F038, round 4 (book round 3, record DECISION F038 D5, and land T001's
model-written answer: the claim check, a switch off by default, the summary-role call and the
mechanical fallback)

## Session

SESSION 1 of feature F038 · round 4 · rounds so far 4. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, both
payloads and the records diff before writing anything, read every named source file whole
(`chat_answer.py`, `test_chat_answer.py`, `chat_evidence.py`'s item/prompt helpers,
`result_tour.py`'s `GeneratedTourContent`/`build_tour_prompt`/`PROVIDER_CALL_ERRORS`/
`generate_result_tour`/`tour_model_written`/`tour_call_fn`/`write_result_tour`,
`make_structured_call_fn` in `intake.py`, `run_structured_call`/`StructuredOutcome` in
`structured_outputs.py`, `FailureSignals`/`classify` in `failure_postmortem.py`, the
`tour.model_written` spec and `write_environment_guide` in `config.py`, `ROLE_CONFIG_CALL_SITES`
in `model_routing.py`, `TestTheCallSiteInventoryIsChecked` and the switch tests of
`test_result_tour.py`), verified every payload and every committed copy for real, applied
`records.diff`, wrote the claim check and the model-written answer path from the specification
against real evidence sets, verified the claim-check scenarios by hand in a scratch script before
writing the tests, wrote 30 tests (16 new) and a fresh 10-mutation red-proof tool and ran it for
real in a disposable worktree, ran the pinned serial test selection and the integrity check to
completion, and ran every gate (G1–G5) for real before writing this handback.

## Range

Review of `47747a499..HEAD` (`HEAD` is this handback's own commit, `F038 R4 C5`, on
`feature/f038-grounded-chat`).

## Commits

### 576ec5532 F038 R4 C1a: copy round 4 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r4-block.md | 309/0 | copy of the block, verified line count (309) and sha256 |
| .agent/authored/f038-r4-plan.md | 28/0 | copy of the reviewer's plan.md payload |

337 insertions total, exactly the block's own note: 309-line block + 28, under the 500-line cap.

### 4e70c5afe F038 R4 C1b: copy round 4 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r4-records.diff | 67/0 | copy of the reviewer's records.diff payload |

Measured 67 insertions, exactly the block's expected reading.

### d0b001113 F038 R4 C2: book round 3 and record DECISION F038 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 49/0 | `git apply records.diff` — appends DECISION F038 D5 |
| .agent/live_review.md | 2/0 | `git apply records.diff` — books round 3's Gate entry |
| .agent/plan.md | 6/9 | rewritten to plan.md payload by `shutil.copyfile` |

Measured numstat matches the block's table exactly: 49/0, 2/0, 6/9.

### 91dfafe15 F038 R4 C3: let the summary model answer the chat behind a switch, with a claim check
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_answer.py | 180/5 | S1 claim check (`_claim_tokens`, `_unsupported_claim_problem`, wired into `check_answer_sentence`), S2 `GeneratedChatAnswer` schema and labels, S3 `build_chat_prompt`, S4 `chat_model_written`/`chat_call_fn`, S5 `answer_chat_question` and its sentinel |
| packages/orchestration/config.py | 12/0 | S6 — `chat.model_written` `ConfigKeySpec`, directly before `tour.model_written` |
| docs/guides/environment.md | 1/0 | S6 — regenerated via `write_environment_guide()`, never by hand |
| packages/orchestration/model_routing.py | 1/0 | S7 — `chat_answer.py`'s `summary` call site added to `ROLE_CONFIG_CALL_SITES`, directly after `artifact_summary.py` |
| packages/orchestration/result_tour.py | 1/1 | S7 — `tour_call_fn`'s docstring: "ten entries" → "eleven entries" |
| tests/orchestration/test_model_routing.py | 4/4 | S7 — `test_most_call_sites_still_pass_no_role_literal`'s pinned counts 10→11, 5→6, and its comment |

No insertion count was expected by the block for C3; measured 199 total, under the cap.

### e221a6ac3 F038 R4 C4: test the claim check, the switch and the model answer's fallbacks
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_answer.py | 267/2 | 16 NEW tests: six claim-check scenarios over a shared two-item set (a supported number, an unsupported number, a supported backtick span, an unsupported backtick span, an unsupported URL, and a token held only by the uncited item), two prompt tests (question line + rendered evidence line + refusal rule; `(no items)` for an empty set), the switch (false by default, true after the env var + `reset_config()`), `chat_call_fn` asking `resolve_role_config`/`make_structured_call_fn` with stand-ins, the switch-gated spy test for `answer_chat_question`'s unset default, a kept reply with a mixed supported/unsupported sentence, a reply with no supported sentence falling back to the mechanical answer, a `ConnectionError` and an unparseable reply each falling back with a non-`no_supported_sentence` label, and THE MODEL CANARY (three round-3 canary questions with a stub inventing a URL, over a real node scope, all reading `mechanical:no_supported_sentence` / `"Not in evidence."`); plus one import-line edit (`chat_call_fn` dropped from the top-level import after ruff flagged it unused — it is exercised only via `chat_answer_module.chat_call_fn`) |
| .agent/authored/f038-r4-mutations.py | 232/0 | the G5 tool: 10 mutations (q1–q10), nine against `chat_answer.py` and one (q10) against `config.py`, run against `tests/orchestration/test_chat_answer.py` |

499 insertions total, one under the 500-insertion cap — no split was needed.

### \<C5-sha\> F038 R4 C5: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f038-r4-mut e221a6ac3` — added the disposable G5
  worktree at C4. Outcome: `Preparing worktree (detached HEAD e221a6ac3)`, exit 0.
- `python3 -B .agent/authored/f038-r4-mutations.py .../.remedy-wt/f038-r4-mut` — ran the
  10-mutation red-proof tool. Outcome: all 10 caught, both controls exit 0, `restored
  byte-identical: True` on every mutation, `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove --force .remedy-wt/f038-r4-mut` — removed the G5 worktree. Outcome: exit 0.
- `git worktree prune` — outcome: exit 0.
- `git push origin feature/f038-grounded-chat` — reported under G6 in the round reply (run after
  this file's own commit, so its outcome is reported there rather than tabled here, per the
  handback template's self-reference exception).

## Verification

### BEFORE ANYTHING ELSE
1. `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, exit 2. Absent.
2. `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty, exit 0.
   `git branch --show-current` → `feature/f038-grounded-chat`. `git log --oneline -1` →
   `47747a499 F038 R3 C5: rewrite handoff for round 3`.
3. Block bytes: measured line count 309, sha256
   `35ee28bd5b9fa938b9dfc88e8cbf6f8420aa329ec8f7a3b12ddb281fc37b4676`; both equal the two readings
   the delegation message stated.
4. `git worktree list | wc -l` → `68`.

### PAYLOADS
| file | measured lines | measured bytes | measured sha256 | matches table |
|---|---|---|---|---|
| records.diff | 67 | 11444 | bca963df465362b2a2bc1c6b0555a52bb7459335c83ee806b74ac5280dc389ce | yes |
| plan.md | 28 | 937 | 5ed12bfd0216e26fb11446797cc7e57e76ad40bb7cec1f82b84b3433486ad3a7 | yes |

### G1 TRANSPORT
`git apply --check .remedy-wt/f038-r4-payloads/records.diff` → exit 0. Real `git apply` → exit 0.
Each `.agent/authored/f038-r4-*` copy compared byte-for-byte against its source, read back with
`git show <commit>:<path>`:
- `576ec5532:.agent/authored/f038-r4-block.md` == `.remedy-wt/f038-r4/block.md` — MATCH (sha256
  `35ee28bd...c37b4676` both).
- `576ec5532:.agent/authored/f038-r4-plan.md` == `.remedy-wt/f038-r4-payloads/plan.md` — MATCH
  (sha256 `5ed12bfd...3486ad3a7` both).
- `4e70c5afe:.agent/authored/f038-r4-records.diff` == `.remedy-wt/f038-r4-payloads/records.diff`
  — MATCH (sha256 `bca963df...280dc389ce` both).

### G2 THE RECORDS
sha256 of each file read with `git show d0b001113:<path>`:
| path | bytes | sha256 | matches reviewer's reading |
|---|---|---|---|
| .agent/decisions.md | 2390061 | f8ddcf879acf3c37c598c53e9455c8b485d6d1f31b5741cfa5857899be2115b1 | yes |
| .agent/live_review.md | 318007 | ca0fba7a18f16d905bf9265e10cab007bdcc5164dda2e4f66582393a575fe42a | yes |
| .agent/plan.md | 937 | 5ed12bfd0216e26fb11446797cc7e57e76ad40bb7cec1f82b84b3433486ad3a7 | yes |

`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s text at
`d0b001113` → `[]`, matching the reviewer's stated reading.

`git diff --name-only 4e70c5afe d0b001113` →
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Names exactly the three paths of the table above.

### G3 THE CODE
`python3 -m ruff check packages/orchestration/chat_answer.py packages/orchestration/config.py
packages/orchestration/model_routing.py packages/orchestration/result_tour.py
tests/orchestration/test_model_routing.py tests/orchestration/test_chat_answer.py` at C4 →
`All checks passed!`, exit 0.

Quoted from `git show 91dfafe15` (C3), the claim check of S1:

```python
def _claim_tokens(sentence: str) -> list[str]:
    """Every claim token of `sentence` with its citations removed, in the order they
    occur: a URL, a backtick span, or a number, each taken without its backticks and
    without a trailing `.`, `,`, `;`, `:`, `)`, `!` or `?` (DECISION F038 D5 (1))."""
    without_citations = _CITATION_RE.sub("", sentence)
    tokens: list[str] = []
    for match in _CLAIM_TOKEN_RE.finditer(without_citations):
        token = match.group(0)
        if token.startswith("`") and token.endswith("`"):
            token = token[1:-1]
        token = token.rstrip(_CLAIM_TRAILING_CHARS)
        if token:
            tokens.append(token)
    return tokens


def _unsupported_claim_problem(sentence: str, cited_items: tuple[Any, ...]) -> str:
    """`""` when every claim token of `sentence` occurs in the ref or text of one of
    `cited_items`; otherwise the problem naming the first token that does not."""
    haystack = " ".join(f"{item.ref} {item.text}" for item in cited_items)
    for token in _claim_tokens(sentence):
        if token not in haystack:
            return f"states {token}, which its cited items do not hold"
    return ""
```

The claim check is wired into `check_answer_sentence` directly after the citation-range check and
before the final `supported=True` return:

```python
    cited_items = tuple(evidence.items[number - 1] for number in citations)
    claim_problem = _unsupported_claim_problem(sentence, cited_items)
    if claim_problem:
        return ChatAnswerSentence(
            text=sentence, citations=citations, supported=False, problem=claim_problem
        )
    return ChatAnswerSentence(text=sentence, citations=citations, supported=True, problem="")
```

The whole of `answer_chat_question`:

```python
def answer_chat_question(
    question: str,
    evidence: ChatEvidenceSet,
    call_fn: Callable[[str, int], str] | None = _UNSET_CALL_FN,
) -> ChatAnswer:
    """Answer `question` over `evidence`: mechanically, or through the summary model
    behind `chat.model_written` (DECISION F038 D5 (5)).

    `call_fn` unset asks :func:`chat_call_fn` only when :func:`chat_model_written` is
    true; unset with the key off, exactly like `call_fn=None` given explicitly,
    answers mechanically instead. A call function HANDED IN, `None` included, is used
    as given whatever the key reads.

    NEVER raises: an exception of `PROVIDER_CALL_ERRORS`, an outcome that is not ok,
    and a reply none of whose sentences is supported all fall back to the mechanical
    answer, labelled `mechanical:<reason>` — the mechanical answer's sentences never
    change, only its label does. A reply that is checked and keeps at least one
    supported sentence is returned labelled `CHAT_GENERATOR_SUMMARY_ROLE`.
    """
    if call_fn is _UNSET_CALL_FN:
        call_fn = chat_call_fn() if chat_model_written() else None
    if call_fn is None:
        return mechanical_answer(question, evidence)

    prompt = build_chat_prompt(question, evidence)
    try:
        outcome = run_structured_call(GeneratedChatAnswer, prompt, call_fn, allow_parse_retry=True)
    except PROVIDER_CALL_ERRORS as exc:
        classification = classify(FailureSignals(exception=exc))
        return dataclasses.replace(
            mechanical_answer(question, evidence),
            generator=f"{CHAT_GENERATOR_MECHANICAL}:{classification.failure_class.value}",
        )

    if not outcome.ok:
        classification = classify(
            FailureSignals(error_class=outcome.error_class, error_text=outcome.hint)
        )
        return dataclasses.replace(
            mechanical_answer(question, evidence),
            generator=f"{CHAT_GENERATOR_MECHANICAL}:{classification.failure_class.value}",
        )

    assert isinstance(outcome.value, GeneratedChatAnswer)
    checked = check_answer(
        outcome.value.answer, evidence, question=question, generator=CHAT_GENERATOR_SUMMARY_ROLE
    )
    if any(sentence.supported for sentence in checked.sentences):
        return checked
    return dataclasses.replace(
        mechanical_answer(question, evidence),
        generator=f"{CHAT_GENERATOR_MECHANICAL}:{CHAT_NO_SUPPORTED_SENTENCE}",
    )
```

Lines C3 adds to `docs/guides/environment.md`:
```
| `REMEDY_CHAT_MODEL_WRITTEN` | yes or no (1, true, yes / 0, false, no) | no | `chat.model_written` | Let the summary model write the grounded chat's answers (F038). Off by default: each answer is one summary model call, and a question makes no call the operator did not switch on; with it off, the chat answers from its evidence mechanically. |
```

### G4 THE TESTS
Serial run, at C4, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/orchestration/test_model_routing.py tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/orchestration/test_result_tour.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
Output:
```
1344 passed, 9 skipped, 1 warning in 78.91s (0:01:18)
REAL_EXIT=0
```
The nine `SKIPPED` lines, in full:
```
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
```
All nine match the reviewer's own primary-checkout baseline exactly (3 `test_model_routing.py` +
6 F252 quarantine).

Node counts by `--collect-only -q`:
- `tests/orchestration/test_chat_answer.py` at `47747a499`: 14 tests.
- `tests/orchestration/test_chat_answer.py` at C4: 30 tests (+16 this round).

Accounting for 1344 vs the reviewer's 1328 at `47747a499`: this round added 16 new nodes to
`test_chat_answer.py` and touched no other test file's collection (S7's edits to
`test_model_routing.py` only change two integer literals inside an already-collected test, not
its node count). 1328 + 16 = 1344, exactly the measured total. The skip count is unchanged at 9
because the round added no new skip.

`python3 -m apps.cli.main integrity check --json`:
```json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0, exit 0.

### G5 THE RED PROOFS
`git worktree add --detach .remedy-wt/f038-r4-mut e221a6ac3` → exit 0
(`Preparing worktree (detached HEAD e221a6ac3)`).
`python3 -B .agent/authored/f038-r4-mutations.py .../.remedy-wt/f038-r4-mut` → whole output:
```
control (before): exit=0 failed=0 nodes=[]
q1 the claim check never finds a token missing: exit=1 failed=5 nodes=['tests/orchestration/test_chat_answer.py::test_a_claim_backtick_span_its_cited_item_does_not_hold_is_unsupported', 'tests/orchestration/test_chat_answer.py::test_a_claim_number_its_cited_item_does_not_hold_is_unsupported', 'tests/orchestration/test_chat_answer.py::test_a_claim_token_held_only_by_the_other_item_is_still_unsupported', 'tests/orchestration/test_chat_answer.py::test_a_claim_url_its_cited_item_does_not_hold_is_unsupported', 'tests/orchestration/test_chat_answer.py::test_model_canary_suite_over_a_real_node_scope_still_reads_not_in_evidence']
q2 the claim check reads every item of the set instead of the cited ones: exit=1 failed=2 nodes=['tests/orchestration/test_chat_answer.py::test_a_claim_number_its_cited_item_does_not_hold_is_unsupported', 'tests/orchestration/test_chat_answer.py::test_a_claim_token_held_only_by_the_other_item_is_still_unsupported']
q3 with no call function handed in, chat_call_fn() is asked whatever the switch: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_unset_calls_chat_call_fn_only_when_the_switch_is_on']
q4 chat_call_fn asks the planner role: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_chat_call_fn_asks_resolve_role_config_and_make_structured_call_fn']
q5 only KeyError is caught around the call: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_a_provider_error_falls_back_with_a_mechanical_label_naming_the_failure']
q6 a reply with no supported sentence is kept: exit=1 failed=2 nodes=['tests/orchestration/test_chat_answer.py::test_a_reply_with_no_supported_sentence_falls_back_to_the_mechanical_answer', 'tests/orchestration/test_chat_answer.py::test_model_canary_suite_over_a_real_node_scope_still_reads_not_in_evidence']
q7 a fallback's label omits its reason: exit=1 failed=2 nodes=['tests/orchestration/test_chat_answer.py::test_a_reply_with_no_supported_sentence_falls_back_to_the_mechanical_answer', 'tests/orchestration/test_chat_answer.py::test_model_canary_suite_over_a_real_node_scope_still_reads_not_in_evidence']
q8 the prompt omits the refusal rule: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_prompt_starts_with_the_question_and_holds_a_rendered_evidence_line']
q9 an outcome that is not ok is not a fallback: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_an_unparseable_reply_falls_back_with_a_mechanical_label_naming_the_failure']
q10 in config.py, the switch defaults to on: exit=1 failed=2 nodes=['tests/orchestration/test_chat_answer.py::test_chat_model_written_reads_false_by_default_and_true_after_the_env_var', 'tests/orchestration/test_chat_answer.py::test_unset_calls_chat_call_fn_only_when_the_switch_is_on']
control (after): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation caught with at least one failing node; both unmutated controls read exit 0; every
mutation restored byte-identical (confirmed both by the tool's own per-mutation restore check and
its printed `restored byte-identical: True` line). No mutation stayed green, so constraint 4's
"add the test that catches it" branch never fired.
`git worktree remove --force .remedy-wt/f038-r4-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list | wc -l` → `68`.

## Authored-text proofs

- `.agent/authored/f038-r4-block.md` (added at `576ec5532`) == `.remedy-wt/f038-r4/block.md`,
  byte for byte (sha256 `35ee28bd...c37b4676` both). MATCH.
- `.agent/authored/f038-r4-plan.md` (added at `576ec5532`) == `.remedy-wt/f038-r4-payloads/plan.md`,
  byte for byte (sha256 `5ed12bfd...3486ad3a7` both). MATCH.
- `.agent/authored/f038-r4-records.diff` (added at `4e70c5afe`) ==
  `.remedy-wt/f038-r4-payloads/records.diff`, byte for byte (sha256 `bca963df...280dc389ce` both). MATCH.
- `.agent/plan.md` after C2 (`d0b001113`) == `.remedy-wt/f038-r4-payloads/plan.md`, byte for byte
  (sha256 `5ed12bfd0216e26fb11446797cc7e57e76ad40bb7cec1f82b84b3433486ad3a7` both, confirmed under
  G2). MATCH.
- `records.diff` applied via `git apply` (not retyped); `.agent/decisions.md` and
  `.agent/live_review.md` after C2 match the reviewer's stated sha256 exactly (G2 table above).
  MATCH.

## Deviations & assumptions

1. **The import-line trim in C4 (`tests/orchestration/test_chat_answer.py`).** `ruff` flagged
   `chat_call_fn` as an unused top-level import once `test_chat_call_fn_asks_resolve_role_config_
   and_make_structured_call_fn` was written to call it through `chat_answer_module.chat_call_fn`
   (monkeypatch target) rather than the bare name. Removed the unused import; no test's behaviour
   changed, and G3's ruff reading is clean at C4. Declared here because it is a one-line change
   inside the C4 diff not named by S7 or the TESTS section verbatim.
2. No payload was repaired, edited or retyped. No existing test was touched, and no existing
   assertion in any file was changed. No file outside the round's tracked path set (constraint 3)
   was touched — confirmed by `git diff --name-only 47747a499` at the branch tip (see below).
3. No gate went red at any point this round; no repair or correction of a committed test was
   needed.
4. C4 measured 499 insertions, one under the 500-insertion cap in constraint 2 — no split was
   needed, but it is close enough to the cap to flag explicitly.

## Tracked path set (constraint 3)

`git diff --name-only 47747a499` at the branch tip after C5:
```
.agent/authored/f038-r4-block.md
.agent/authored/f038-r4-mutations.py
.agent/authored/f038-r4-plan.md
.agent/authored/f038-r4-records.diff
.agent/decisions.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
docs/guides/environment.md
packages/orchestration/chat_answer.py
packages/orchestration/config.py
packages/orchestration/model_routing.py
packages/orchestration/result_tour.py
tests/orchestration/test_chat_answer.py
tests/orchestration/test_model_routing.py
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
| C4 | done | 499 insertions, one under the 500-insertion cap; no split needed |
| C5 | done | this commit |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | all 10 mutations caught first run |
| G6 TREE AND PUSH | done | reported in the round reply, not tabled here (cannot precede this commit) |

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk. (2) The
review of round 4. (3) T002: the intent parse over the exposed commands, the action cards and
their confirmation. Open-findings count: 0. Operator-questions count: 1.
