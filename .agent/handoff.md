# Handoff — F038, round 3 (book round 2, record DECISION F038 D4, and land T001's grounded
answer: the citation check, the mechanical answer and the canary suite in both scopes)

## Session

SESSION 1 of feature F038 · round 3 · rounds so far 3. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, both
payloads and the records diff before writing anything, read every named source file whole
(`chat_evidence.py`, `test_chat_evidence.py`, `test_no_orphan_modules.py`, `build_task_run_rounds`
in `run_rounds_view.py`, the handback template, `open_finding_ids`, `estimate_text_tokens`),
verified every payload and every committed copy for real, applied `records.diff`, wrote the new
module and its tests from the specification against real evidence sets and real saved jobs/projects,
verified the tests pass and ruff is clean before committing, wrote a fresh 12-mutation red-proof
tool and ran it for real in a disposable worktree, ran the pinned serial test selection and the
integrity check to completion, and ran every gate (G1–G5) for real before writing this handback.

## Range

Review of `fe18ab6d8..HEAD` (`HEAD` is this handback's own commit, `F038 R3 C5`, on
`feature/f038-grounded-chat`).

## Commits

### 0de81a6b2 F038 R3 C1a: copy round 3 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r3-block.md | 293/0 | copy of the block, verified line count (293) and sha256 |
| .agent/authored/f038-r3-plan.md | 31/0 | copy of the reviewer's plan.md payload |

324 insertions total, exactly the block's own note: 293-line block + 31, under the 500-line cap.

### f03ceb9ee F038 R3 C1b: copy round 3 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f038-r3-records.diff | 56/0 | copy of the reviewer's records.diff payload |

Measured 56 insertions, exactly the block's expected reading.

### a87ddd85f F038 R3 C2: book round 2 and record DECISION F038 D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 38/0 | `git apply records.diff` — appends DECISION F038 D4 |
| .agent/live_review.md | 2/0 | `git apply records.diff` — books round 2's Gate entry |
| .agent/plan.md | 7/6 | rewritten to plan.md payload by `shutil.copyfile` |

Measured numstat matches the block's table exactly: 38/0, 2/0, 7/6.

### 2a319471c F038 R3 C3: check a chat answer's citations and answer mechanically
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/chat_answer.py | 189/0 | NEW FILE — S1 constants, S2 shapes, S3 `split_answer_sentences`, S4 `check_answer_sentence`/`check_answer`/`render_chat_answer`, S5 `question_keywords`/`_item_score`/`mechanical_answer` |
| packages/orchestration/chat_evidence.py | 1/1 | S6 — the prompt-trace run-id check calls `fullmatch` instead of `match` |
| tests/test_no_orphan_modules.py | 3/3 | S6 — `ALLOWED_UNWIRED`'s `chat_evidence.py` line removed, `chat_answer.py` line added in its place |

No insertion count was expected by the block for C3; measured 193 total, under the cap.

### 5f787353 F038 R3 C4: test the answer check, the mechanical answer and the canary suite
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_chat_answer.py | 244/0 | NEW FILE, 14 tests: the two split examples plus a blank text, the four-sentence check over a two-item set (render + `unsupported_count`), the `CHAT_NOT_IN_EVIDENCE`/blank-text supported case, `question_keywords` (stopword + two-letter word + repeated word), the ref-and-text and inner-full-stop mechanical case, a dedicated prefix-vs-exact-word test (DECISION F038 D4's own "pass" would not find "passed" example), the tie-break/cap test over eight matching items, a no-match case, "Did the tests pass?" over a real node scope, and THE CANARY SUITE over a real node scope and a real project scope linking one saved job |
| tests/orchestration/test_chat_evidence.py | 10/0 | ONE new test — a `run_id` of `abcdef01` followed by a newline reads `Prompt trace: not recorded (no_run_recorded)`, proving S6's `fullmatch` change |
| .agent/authored/f038-r3-mutations.py | 207/0 | the G5 tool: 12 mutations (p1–p12), eleven against `chat_answer.py` and one (p12) against `chat_evidence.py`, run against `tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py` |

No insertion count was expected by the block for C4; measured 461 total, under the 500-insertion
cap — no split was needed (unlike round 2's C4a/C4b).

### \<C5-sha\> F038 R3 C5: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f038-r3-mut 5f787353176557b60d55e6e298624afad58506d8` —
  added the disposable G5 worktree at C4. Outcome: `Preparing worktree (detached HEAD 5f7873531)`.
- `python3 -B .agent/authored/f038-r3-mutations.py .../.remedy-wt/f038-r3-mut` — ran the
  12-mutation red-proof tool. Outcome: all 12 caught, both controls exit 0, `restored
  byte-identical: True` on every mutation, `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove --force .remedy-wt/f038-r3-mut` — removed the G5 worktree. Outcome: exit 0.
- `git worktree prune` — outcome: exit 0.
- `git push origin feature/f038-grounded-chat` — reported under G6 in the round reply (run after
  this file's own commit, so its outcome is reported there rather than tabled here, per the
  handback template's self-reference exception).

## Verification

### BEFORE ANYTHING ELSE
1. `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, exit 2. Absent.
2. `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty, exit 0.
   `git branch --show-current` → `feature/f038-grounded-chat`. `git log --oneline -1` →
   `fe18ab6d8 F038 R2 C5: rewrite handoff for round 2`.
3. Block bytes: measured line count 293, sha256
   `b37365a9fd3a315216cf9d6b04e5b69087e41e1bd86ed3366af9176a5cfaa7a8`; both equal the two readings
   the delegation message stated.
4. `git worktree list | wc -l` → `66`.

### PAYLOADS
| file | measured lines | measured bytes | measured sha256 | matches table |
|---|---|---|---|---|
| records.diff | 56 | 10275 | 289b865a0a118f2ef66ad7b5da752fa42c925c6fd99cfe3eb91cc9b1a0ecdb01 | yes |
| plan.md | 31 | 1058 | 424443393cfee0196203a8e46ec338cf226cc02a208ebb8206c3db0b3791d566 | yes |

### G1 TRANSPORT
`git apply --check .remedy-wt/f038-r3-payloads/records.diff` → exit 0. Real `git apply` → exit 0.
Each `.agent/authored/f038-r3-*` copy compared byte-for-byte against its source, read back with
`git show <commit>:<path>`:
- `0de81a6b2:.agent/authored/f038-r3-block.md` == `.remedy-wt/f038-r3/block.md` — MATCH (sha256
  `b37365a9...cfa7a8` both).
- `0de81a6b2:.agent/authored/f038-r3-plan.md` == `.remedy-wt/f038-r3-payloads/plan.md` — MATCH
  (sha256 `42444339...791d566` both).
- `f03ceb9ee:.agent/authored/f038-r3-records.diff` == `.remedy-wt/f038-r3-payloads/records.diff`
  — MATCH (sha256 `289b865a...1a0ecdb01` both).

### G2 THE RECORDS
sha256 of each file read with `git show a87ddd85f:<path>`:
| path | bytes | sha256 | matches reviewer's reading |
|---|---|---|---|
| .agent/decisions.md | 2385590 | fa55e0b8e0050b8afff21549e497bf09821ef394f079f7ae0be86bcb236094f8 | yes |
| .agent/live_review.md | 315369 | d8369556b1ed80a387b11d3af10bd2e39987aec2d30fff6b59d3d2daa4108e93 | yes |
| .agent/plan.md | 1058 | 424443393cfee0196203a8e46ec338cf226cc02a208ebb8206c3db0b3791d566 | yes |

`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s text at
`a87ddd85f` → `[]`, matching the reviewer's stated reading.

`git diff --name-only f03ceb9ee a87ddd85f` →
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Names exactly the three paths of the table above.

### G3 THE CODE
`python3 -m ruff check packages/orchestration/chat_answer.py packages/orchestration/chat_evidence.py
tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py
tests/test_no_orphan_modules.py` at C4 → `All checks passed!`, exit 0.

Quoted from `git show 2a319471c` (C3):

```python
def split_answer_sentences(text: str) -> list[str]:
    """Split `text` into sentences.

    Each line, stripped, is split after every `.`, `!` or `?` that whitespace
    follows. Each fragment is stripped and an empty one is dropped. A fragment
    that, with its citations removed and then stripped of spaces, `.`, `!` and
    `?`, is empty is a citation-only fragment: it joins the sentence before it
    with one space, when there is one. Every other fragment is a sentence.
    """
    sentences: list[str] = []
    for line in text.splitlines():
        stripped_line = line.strip()
        if not stripped_line:
            continue
        for fragment in _SENTENCE_SPLIT_RE.split(stripped_line):
            fragment = fragment.strip()
            if not fragment:
                continue
            bare = _CITATION_RE.sub("", fragment).strip(" .!?")
            if not bare:
                if sentences:
                    sentences[-1] = f"{sentences[-1]} {fragment}"
                else:
                    sentences.append(fragment)
            else:
                sentences.append(fragment)
    return sentences
```

```python
def check_answer_sentence(sentence: str, evidence: ChatEvidenceSet) -> ChatAnswerSentence:
    """Check one sentence's citations against `evidence`.

    A sentence that, stripped, equals `CHAT_NOT_IN_EVIDENCE` and cites nothing is
    supported: it claims an absence, not a fact. Otherwise a sentence citing
    nothing is unsupported; one citing any number outside 1 to the set's item
    count is unsupported, naming the numbers the set does not hold; every other
    sentence is supported.
    """
    citations = tuple(int(number) for number in _CITATION_RE.findall(sentence))
    if sentence.strip() == CHAT_NOT_IN_EVIDENCE and not citations:
        return ChatAnswerSentence(text=sentence, citations=citations, supported=True, problem="")
    if not citations:
        return ChatAnswerSentence(
            text=sentence, citations=citations, supported=False, problem="cites no evidence item"
        )
    item_count = len(evidence.items)
    unheld = [number for number in citations if number < 1 or number > item_count]
    if unheld:
        rendered = ", ".join(f"[{number}]" for number in unheld)
        return ChatAnswerSentence(
            text=sentence, citations=citations, supported=False,
            problem=f"cites {rendered}, which the evidence set does not hold",
        )
    return ChatAnswerSentence(text=sentence, citations=citations, supported=True, problem="")
```

```python
def mechanical_answer(question: str, evidence: ChatEvidenceSet) -> ChatAnswer:
    """Restate the evidence items best matching `question`'s keywords, one sentence
    each, highest score first and the lower item number first on a tie, at most
    `CHAT_MECHANICAL_MAX_SENTENCES`. `CHAT_NOT_IN_EVIDENCE` when none scores."""
    keywords = question_keywords(question)
    scored: list[tuple[int, Any, int]] = []
    for number, item in enumerate(evidence.items, start=1):
        score = _item_score(item.ref, item.text, keywords)
        if score >= 1:
            scored.append((number, item, score))
    scored.sort(key=lambda triple: (-triple[2], triple[0]))
    kept = scored[:CHAT_MECHANICAL_MAX_SENTENCES]
    raw_sentences = (
        [f"{item.text.rstrip('.')} [{number}]." for number, item, _score in kept]
        if kept else [CHAT_NOT_IN_EVIDENCE]
    )
    sentences = tuple(check_answer_sentence(sentence, evidence) for sentence in raw_sentences)
    return ChatAnswer(
        scope=evidence.scope, subject=evidence.subject, question=question,
        generator=CHAT_GENERATOR_MECHANICAL, sentences=sentences,
    )
```

### G4 THE TESTS
Serial run, at C4, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py 2>&1 | tail -4; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
Output:
```
452 passed, 6 skipped in 84.75s (0:01:24)
REAL_EXIT=0
```
The six `SKIPPED` lines, in full:
```
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
```
All six are the F252 quarantine, matching the reviewer's baseline exactly.

Node counts by `--collect-only -q` at C4:
- `tests/orchestration/test_chat_answer.py`: 14 tests (NEW FILE).
- `tests/orchestration/test_chat_evidence.py`: 23 tests (22 at `fe18ab6d8`, +1 this round).

Accounting for 452: the reviewer's own base reading, less `test_chat_answer.py`, was 437 passed at
`fe18ab6d8` (with `test_chat_evidence.py` at its then-22 nodes). This round adds the 14 nodes of
the new `test_chat_answer.py` plus the 1 new node in `test_chat_evidence.py`: 437 + 14 + 1 = 452,
exactly the measured total. No other test file's collection changed.

`python3 -m apps.cli.main integrity check --json`:
```json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0, exit 0.

### G5 THE RED PROOFS
`git worktree add --detach .remedy-wt/f038-r3-mut 5f787353176557b60d55e6e298624afad58506d8` →
exit 0 (`Preparing worktree (detached HEAD 5f7873531)`).
`python3 -B .agent/authored/f038-r3-mutations.py .../.remedy-wt/f038-r3-mut` → whole output:
```
control (before): exit=0 failed=0 nodes=[]
p1 a sentence citing nothing reads supported: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_check_answer_marks_each_sentence_counts_unsupported_and_renders_the_mark'] caught=True
  restored byte-identical: True
p2 a citation outside the set is accepted: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_check_answer_marks_each_sentence_counts_unsupported_and_renders_the_mark'] caught=True
  restored byte-identical: True
p3 "Not in evidence." needs a citation: exit=1 failed=4 nodes=['tests/orchestration/test_chat_answer.py::test_not_in_evidence_and_blank_texts_check_to_the_one_supported_sentence', 'tests/orchestration/test_chat_answer.py::test_no_matching_item_answers_not_in_evidence', 'tests/orchestration/test_chat_answer.py::test_canary_suite_over_a_real_node_scope_reads_not_in_evidence', 'tests/orchestration/test_chat_answer.py::test_canary_suite_over_a_real_project_scope_reads_not_in_evidence'] caught=True
  restored byte-identical: True
p4 a fragment of citation markers stands as its own sentence: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_split_answer_sentences_joins_a_citation_only_fragment_to_its_sentence'] caught=True
  restored byte-identical: True
p5 an empty answer has no sentence: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_not_in_evidence_and_blank_texts_check_to_the_one_supported_sentence'] caught=True
  restored byte-identical: True
p6 a keyword matches whole words only: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_a_keyword_matches_a_longer_run_by_prefix_not_by_whole_word_only'] caught=True
  restored byte-identical: True
p7 on a tied score the higher item number comes first: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_eight_matching_items_give_five_sentences_in_item_number_order'] caught=True
  restored byte-identical: True
p8 the mechanical answer restates every matching item: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_eight_matching_items_give_five_sentences_in_item_number_order'] caught=True
  restored byte-identical: True
p9 the mechanical answer's sentences are split again: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_mechanical_answer_matches_item_text_and_ref_and_keeps_an_inner_full_stop_whole'] caught=True
  restored byte-identical: True
p10 the renderer omits the unsupported mark: exit=1 failed=1 nodes=['tests/orchestration/test_chat_answer.py::test_check_answer_marks_each_sentence_counts_unsupported_and_renders_the_mark'] caught=True
  restored byte-identical: True
p11 stopwords count as keywords: exit=1 failed=3 nodes=['tests/orchestration/test_chat_answer.py::test_question_keywords_drops_stopwords_short_words_and_dedupes', 'tests/orchestration/test_chat_answer.py::test_mechanical_answer_matches_item_text_and_ref_and_keeps_an_inner_full_stop_whole', 'tests/orchestration/test_chat_answer.py::test_canary_suite_over_a_real_project_scope_reads_not_in_evidence'] caught=True
  restored byte-identical: True
p12 in chat_evidence.py, the run-id check calls match again: exit=1 failed=1 nodes=['tests/orchestration/test_chat_evidence.py::test_a_run_id_with_a_trailing_newline_is_no_run'] caught=True
  restored byte-identical: True
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation caught with at least one failing node; both unmutated controls read exit 0; every
mutation restored byte-identical. No mutation stayed green, so constraint 4's "add the test that
catches it" branch never fired — every catching test (including the dedicated p6 prefix-match test
and the p9 inner-full-stop test) was written during C4's authoring, before this tool ever ran.
`git worktree remove --force .remedy-wt/f038-r3-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list | wc -l` → `66`.

## Authored-text proofs

- `.agent/authored/f038-r3-block.md` (added at `0de81a6b2`) == `.remedy-wt/f038-r3/block.md`,
  byte for byte (sha256 `b37365a9...cfa7a8` both). MATCH.
- `.agent/authored/f038-r3-plan.md` (added at `0de81a6b2`) == `.remedy-wt/f038-r3-payloads/plan.md`,
  byte for byte (sha256 `42444339...791d566` both). MATCH.
- `.agent/authored/f038-r3-records.diff` (added at `f03ceb9ee`) ==
  `.remedy-wt/f038-r3-payloads/records.diff`, byte for byte (sha256 `289b865a...1a0ecdb01` both). MATCH.
- `.agent/plan.md` after C2 (`a87ddd85f`) == `.remedy-wt/f038-r3-payloads/plan.md`, byte for byte
  (sha256 `424443393cfee0196203a8e46ec338cf226cc02a208ebb8206c3db0b3791d566` both, confirmed under
  G2). MATCH.
- `records.diff` applied via `git apply` (not retyped); `.agent/decisions.md` and
  `.agent/live_review.md` after C2 match the reviewer's stated sha256 exactly (G2 table above).
  MATCH.

## Deviations & assumptions

1. **A prefix-vs-exact-word test added during C4's authoring, not after an observed green
   mutation (constraint 4).** DECISION F038 D4's own ALTERNATIVES paragraph names the reason
   an exact-word match was rejected: `"pass" would not find "passed"`. Designing mutation p6
   ("a keyword matches whole words only") against my own lines, I noticed neither
   `test_did_the_tests_pass_over_a_real_node_scope_cites_tests_passed` (both its keywords, "tests"
   and "pass", happen to also match some run by exact equality: "tests"=="tests") nor
   `test_mechanical_answer_matches_item_text_and_ref_and_keeps_an_inner_full_stop_whole` (its
   keywords "checkout" and "flow" are also both exact matches) would fail under an exact-match
   mutation, because in both cases the selected item is uniquely identified even with the
   prefix relaxation removed. Added
   `test_a_keyword_matches_a_longer_run_by_prefix_not_by_whole_word_only`, whose keyword
   ("archive") is a strict, non-equal prefix of the only matching run ("archived"), before ever
   running the mutation tool, so p6 was caught on its first and only run (see G5 output — no
   mutation read green at any point). Declared regardless, since it is a test written
   specifically to secure a mutation's catch, mirroring round 2's n10 precedent.
2. No payload was repaired, edited or retyped. No existing test outside the two named in the
   block (`test_chat_evidence.py`'s new test) was touched, and no existing assertion in either
   file was changed. No file outside the round's tracked path set (constraint 3) was touched —
   confirmed by `git diff --name-only fe18ab6d8` at the branch tip (see below).
3. No gate went red at any point this round; no repair or correction of a committed test was
   needed.

## Tracked path set (constraint 3)

`git diff --name-only fe18ab6d8` at the branch tip after C5:
```
.agent/authored/f038-r3-block.md
.agent/authored/f038-r3-mutations.py
.agent/authored/f038-r3-plan.md
.agent/authored/f038-r3-records.diff
.agent/decisions.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
packages/orchestration/chat_answer.py
packages/orchestration/chat_evidence.py
tests/orchestration/test_chat_answer.py
tests/orchestration/test_chat_evidence.py
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
| C4 | done | 461 insertions, under the 500-insertion cap; no split needed |
| C5 | done | this commit |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | all 12 mutations caught first run |
| G6 TREE AND PUSH | done | reported in the round reply, not tabled here (cannot precede this commit) |

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk. (2) The
review of round 3. (3) T001's model-written answer: a chat routing class, a switch that is off
by default, the same check over its reply, and the mechanical answer as its fallback.
Open-findings count: 0. Operator-questions count: 1.
