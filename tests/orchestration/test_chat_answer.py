"""F038 T001 — the grounded chat's answer: the citation check, the claim check, the
mechanical answer, the model-written answer behind its switch, and the canary suite
of absent-fact questions over real node and project scopes (DECISION F038 D4,
DECISION F038 D5).
"""

from __future__ import annotations

import json

import pytest

from packages.orchestration.chat_answer import (
    CHAT_GENERATOR_MECHANICAL,
    CHAT_GENERATOR_SUMMARY_ROLE,
    CHAT_NO_SUPPORTED_SENTENCE,
    CHAT_NOT_IN_EVIDENCE,
    ChatAnswer,
    ChatAnswerSentence,
    GeneratedChatAnswer,
    answer_chat_question,
    build_chat_prompt,
    chat_model_written,
    check_answer,
    check_answer_sentence,
    mechanical_answer,
    question_keywords,
    render_chat_answer,
    split_answer_sentences,
)
from packages.orchestration.chat_evidence import (
    compose_chat_evidence,
    make_chat_item,
    node_evidence_set,
    project_evidence_set,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.project_registry import RemyProject


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


def _make_job(**task_overrides) -> tuple[JobPlan, str]:
    """A saved job with one task, carrying the minted default id — the real writer,
    never a monkeypatched shortcut (mirrors test_chat_evidence.py's helper)."""
    task = TaskEntry(**task_overrides)
    job = JobPlan(job_title="f038-chat-answer-job", tasks=[task])
    save_job_plan(job)
    return job, task.task_id


def _make_project_with_one_job() -> RemyProject:
    """A project linking one saved job with no tasks and no run events, so its
    evidence set is real but carries no fact a canary question could match."""
    job = JobPlan(
        job_title="f038-chat-answer-project-job", tasks=[],
        metadata={"target_repo": "/tmp/repo"},
    )
    save_job_plan(job)
    return RemyProject(name="f038-chat-answer-project", job_ids=[job.job_id])


# ---------------------------------------------------------------------------
# S3 THE SPLIT
# ---------------------------------------------------------------------------


def test_split_answer_sentences_splits_after_terminal_punctuation_per_line() -> None:
    assert split_answer_sentences("A [1]. B [2]! C?\nD [3]") == [
        "A [1].", "B [2]!", "C?", "D [3]",
    ]


def test_split_answer_sentences_joins_a_citation_only_fragment_to_its_sentence() -> None:
    assert split_answer_sentences("A. [1] [2]") == ["A. [1] [2]"]


def test_split_answer_sentences_of_blank_text_is_empty() -> None:
    assert split_answer_sentences("") == []
    assert split_answer_sentences("\n") == []


# ---------------------------------------------------------------------------
# S4 THE CHECK
# ---------------------------------------------------------------------------


def test_check_answer_marks_each_sentence_counts_unsupported_and_renders_the_mark() -> None:
    evidence = compose_chat_evidence(
        "node", "T001",
        [
            make_chat_item("node", "T001", "first fact"),
            make_chat_item("node", "T001", "second fact"),
        ],
    )
    text = "Cites one [1]. Cites two [2]. Cites three [3]. Cites nothing."

    answer = check_answer(text, evidence, question="What happened?", generator="mechanical")

    assert answer.scope == "node"
    assert answer.subject == "T001"
    assert answer.question == "What happened?"
    assert answer.generator == "mechanical"
    assert [(s.text, s.supported, s.problem) for s in answer.sentences] == [
        ("Cites one [1].", True, ""),
        ("Cites two [2].", True, ""),
        ("Cites three [3].", False, "cites [3], which the evidence set does not hold"),
        ("Cites nothing.", False, "cites no evidence item"),
    ]
    assert answer.unsupported_count == 2
    assert render_chat_answer(answer) == (
        "Cites one [1]. Cites two [2]. Cites three [3]. [unsupported] "
        "Cites nothing. [unsupported]"
    )


def test_not_in_evidence_and_blank_texts_check_to_the_one_supported_sentence() -> None:
    evidence = compose_chat_evidence("node", "T001", [make_chat_item("node", "T001", "a fact")])

    for text in (CHAT_NOT_IN_EVIDENCE, "", "\n"):
        answer = check_answer(text, evidence, question="Q?", generator="mechanical")
        assert len(answer.sentences) == 1
        sentence = answer.sentences[0]
        assert sentence.text == CHAT_NOT_IN_EVIDENCE
        assert sentence.citations == ()
        assert sentence.supported is True
        assert sentence.problem == ""
        assert answer.unsupported_count == 0


def test_check_answer_sentence_is_a_dataclass_with_the_specified_shape() -> None:
    evidence = compose_chat_evidence("node", "T001", [make_chat_item("node", "T001", "a fact")])
    sentence = check_answer_sentence("Cites it [1].", evidence)
    assert isinstance(sentence, ChatAnswerSentence)
    assert sentence.citations == (1,)


# ---------------------------------------------------------------------------
# S5 THE MECHANICAL ANSWER
# ---------------------------------------------------------------------------


def test_question_keywords_drops_stopwords_short_words_and_dedupes() -> None:
    assert question_keywords(
        "What is the deployment URL for the deployment?"
    ) == ("deployment", "url")


def test_mechanical_answer_matches_item_text_and_ref_and_keeps_an_inner_full_stop_whole() -> None:
    items = [
        make_chat_item("node", "T001", "Nothing to do with the question"),
        make_chat_item("node", "T001", "The checkout flow finished without errors"),
        make_chat_item("round", "checkout-99", "Mr. Smith signed off. Twice."),
    ]
    evidence = compose_chat_evidence("node", "T001", items)

    answer = mechanical_answer("Did the checkout flow work?", evidence)

    assert isinstance(answer, ChatAnswer)
    assert answer.generator == "mechanical"
    assert answer.scope == "node"
    assert answer.subject == "T001"
    assert answer.question == "Did the checkout flow work?"
    assert [(s.text, s.citations, s.supported) for s in answer.sentences] == [
        ("The checkout flow finished without errors [2].", (2,), True),
        ("Mr. Smith signed off. Twice [3].", (3,), True),
    ]


def test_a_keyword_matches_a_longer_run_by_prefix_not_by_whole_word_only() -> None:
    items = [make_chat_item("node", "T001", "The task was archived successfully")]
    evidence = compose_chat_evidence("node", "T001", items)

    # "archive" is a strict prefix of the item's "archived" — not equal to it — so
    # only a prefix match (never an exact-word-only match) finds this item.
    answer = mechanical_answer("Did the archive succeed?", evidence)

    assert answer.sentences[0].text == "The task was archived successfully [1]."
    assert answer.sentences[0].supported is True


def test_eight_matching_items_give_five_sentences_in_item_number_order() -> None:
    items = [make_chat_item("node", f"T{n:03d}", f"Widget report {n}") for n in range(1, 9)]
    evidence = compose_chat_evidence("node", "T001", items)

    answer = mechanical_answer("What about the widget?", evidence)

    assert len(answer.sentences) == 5
    assert [s.citations for s in answer.sentences] == [(1,), (2,), (3,), (4,), (5,)]
    assert all(s.supported for s in answer.sentences)


def test_no_matching_item_answers_not_in_evidence() -> None:
    evidence = compose_chat_evidence("node", "T001", [make_chat_item("node", "T001", "irrelevant")])

    answer = mechanical_answer("What about the widget?", evidence)

    assert len(answer.sentences) == 1
    assert answer.sentences[0].text == CHAT_NOT_IN_EVIDENCE
    assert answer.sentences[0].supported is True


# ---------------------------------------------------------------------------
# A REAL NODE SCOPE
# ---------------------------------------------------------------------------


def test_did_the_tests_pass_over_a_real_node_scope_cites_tests_passed() -> None:
    job, task_id = _make_job(test_passed=True)
    evidence = node_evidence_set(job, task_id)

    answer = mechanical_answer("Did the tests pass?", evidence)

    assert len(answer.sentences) == 1
    assert answer.sentences[0].text == "Tests: passed [4]."
    assert answer.sentences[0].citations == (4,)
    assert answer.sentences[0].supported is True


# ---------------------------------------------------------------------------
# THE CANARY SUITE — absent-fact questions over both real scopes.
# ---------------------------------------------------------------------------


def test_canary_suite_over_a_real_node_scope_reads_not_in_evidence() -> None:
    job, task_id = _make_job()
    evidence = node_evidence_set(job, task_id)

    for question in (
        "What was the deployment URL?",
        "Who approved the invoice?",
        "Which database migration ran in production?",
    ):
        answer = mechanical_answer(question, evidence)
        assert len(answer.sentences) == 1, question
        assert answer.sentences[0].text == CHAT_NOT_IN_EVIDENCE, question
        assert answer.sentences[0].supported is True, question


def test_canary_suite_over_a_real_project_scope_reads_not_in_evidence() -> None:
    project = _make_project_with_one_job()
    evidence = project_evidence_set(project)

    for question in (
        "What is the office address?",
        "Which customer paid the invoice?",
        "How many employees work there?",
    ):
        answer = mechanical_answer(question, evidence)
        assert len(answer.sentences) == 1, question
        assert answer.sentences[0].text == CHAT_NOT_IN_EVIDENCE, question
        assert answer.sentences[0].supported is True, question


# ---------------------------------------------------------------------------
# S1 THE CLAIM CHECK (DECISION F038 D5 (1))
# ---------------------------------------------------------------------------

#: The two-item set the claim-check scenarios below all share.
_CLAIM_CHECK_ITEMS = [
    make_chat_item("round", "T001#2", "Round 2 (repair): tests passed"),
    make_chat_item("round", "T001#3", "The Definition of Done ran: pytest -q"),
]


def _claim_check_evidence():
    return compose_chat_evidence("node", "T001", _CLAIM_CHECK_ITEMS)


def test_a_claim_token_held_by_its_cited_item_is_supported() -> None:
    evidence = _claim_check_evidence()
    sentence = check_answer_sentence("Round 2 passed [1].", evidence)
    assert sentence.supported is True
    assert sentence.problem == ""


def test_a_claim_number_its_cited_item_does_not_hold_is_unsupported() -> None:
    evidence = _claim_check_evidence()
    sentence = check_answer_sentence("3 tests failed [1].", evidence)
    assert sentence.supported is False
    assert sentence.problem == "states 3, which its cited items do not hold"


def test_a_claim_backtick_span_held_by_its_cited_item_is_supported() -> None:
    evidence = _claim_check_evidence()
    sentence = check_answer_sentence("Run `pytest -q` [2].", evidence)
    assert sentence.supported is True
    assert sentence.problem == ""


def test_a_claim_backtick_span_its_cited_item_does_not_hold_is_unsupported() -> None:
    evidence = _claim_check_evidence()
    sentence = check_answer_sentence("Run `make all` [2].", evidence)
    assert sentence.supported is False
    assert sentence.problem == "states make all, which its cited items do not hold"


def test_a_claim_url_its_cited_item_does_not_hold_is_unsupported() -> None:
    evidence = _claim_check_evidence()
    sentence = check_answer_sentence("See https://deploy.example/app [1].", evidence)
    assert sentence.supported is False
    assert sentence.problem == (
        "states https://deploy.example/app, which its cited items do not hold"
    )


def test_a_claim_token_held_only_by_the_other_item_is_still_unsupported() -> None:
    # The sentence cites item [1] only — item [2] holds "pytest -q", but a
    # citation search over the WHOLE set, rather than the cited items alone,
    # is exactly the bug DECISION F038 D5's ALTERNATIVES rejects.
    evidence = _claim_check_evidence()
    sentence = check_answer_sentence("Round 2 ran `pytest -q` [1].", evidence)
    assert sentence.supported is False
    assert sentence.problem == "states pytest -q, which its cited items do not hold"


# ---------------------------------------------------------------------------
# S3 THE PROMPT
# ---------------------------------------------------------------------------


def test_prompt_starts_with_the_question_and_holds_a_rendered_evidence_line() -> None:
    evidence = compose_chat_evidence(
        "node", "T001", [make_chat_item("node", "T001", "Tests: passed")]
    )
    prompt = build_chat_prompt("Did the tests pass?", evidence)
    assert prompt.startswith("Question: Did the tests pass?")
    assert "[1] node:T001 — Tests: passed" in prompt
    assert prompt.endswith(
        f"- when no item answers the question, reply exactly: {CHAT_NOT_IN_EVIDENCE}"
    )


def test_prompt_holds_no_items_marker_for_an_empty_evidence_set() -> None:
    evidence = compose_chat_evidence("node", "T001", [])
    prompt = build_chat_prompt("What happened?", evidence)
    assert "(no items)" in prompt


# ---------------------------------------------------------------------------
# S4 THE SWITCH AND THE CALL
# ---------------------------------------------------------------------------


def test_chat_model_written_reads_false_by_default_and_true_after_the_env_var(
    monkeypatch,
) -> None:
    from packages.orchestration.config import reset_config

    assert chat_model_written() is False

    monkeypatch.setenv("REMEDY_CHAT_MODEL_WRITTEN", "1")
    reset_config()

    assert chat_model_written() is True


def test_chat_call_fn_asks_resolve_role_config_and_make_structured_call_fn(
    monkeypatch,
) -> None:
    import packages.orchestration.chat_answer as chat_answer_module

    calls: dict[str, object] = {}

    def fake_resolve_role_config(role):
        calls["role"] = role
        return type("RoleConfig", (), {"model": "fake-model"})()

    def fake_make_structured_call_fn(model_cls, *, model=None, provider=None):
        calls["model_cls"] = model_cls
        calls["model"] = model
        return None

    monkeypatch.setattr(chat_answer_module, "resolve_role_config", fake_resolve_role_config)
    monkeypatch.setattr(
        chat_answer_module, "make_structured_call_fn", fake_make_structured_call_fn
    )

    result = chat_answer_module.chat_call_fn()

    assert result is None
    assert calls["role"] == "summary"
    assert calls["model_cls"] is GeneratedChatAnswer
    assert calls["model"] == "fake-model"


# ---------------------------------------------------------------------------
# S5 THE ANSWER
# ---------------------------------------------------------------------------


def _stub_call_fn(response_text: str):
    def _call(prompt: str, attempt: int) -> str:
        return response_text
    return _call


def test_unset_calls_chat_call_fn_only_when_the_switch_is_on(monkeypatch) -> None:
    import packages.orchestration.chat_answer as chat_answer_module
    from packages.orchestration.config import reset_config

    calls: list[int] = []

    def spy():
        calls.append(1)
        return None

    monkeypatch.setattr(chat_answer_module, "chat_call_fn", spy)
    evidence = compose_chat_evidence(
        "node", "T001", [make_chat_item("node", "T001", "Tests: passed")]
    )

    answer_chat_question("Did the tests pass?", evidence)
    assert calls == []

    monkeypatch.setenv("REMEDY_CHAT_MODEL_WRITTEN", "1")
    reset_config()

    answer_chat_question("Did the tests pass?", evidence)
    assert calls == [1]


def test_a_reply_with_at_least_one_supported_sentence_is_kept_labelled_summary_role() -> None:
    evidence = compose_chat_evidence(
        "node", "T001", [make_chat_item("node", "T001", "Tests passed")]
    )
    fake = _stub_call_fn(json.dumps({"answer": "Tests passed [1]. It was quick."}))

    answer = answer_chat_question("Did the tests pass?", evidence, call_fn=fake)

    assert answer.generator == CHAT_GENERATOR_SUMMARY_ROLE
    assert [(s.text, s.supported) for s in answer.sentences] == [
        ("Tests passed [1].", True),
        ("It was quick.", False),
    ]


def test_a_reply_with_no_supported_sentence_falls_back_to_the_mechanical_answer() -> None:
    evidence = compose_chat_evidence(
        "node", "T001", [make_chat_item("node", "T001", "Tests passed")]
    )
    fake = _stub_call_fn(json.dumps({"answer": "It shipped [4]."}))

    answer = answer_chat_question("Did the tests pass?", evidence, call_fn=fake)
    mechanical = mechanical_answer("Did the tests pass?", evidence)

    assert answer.generator == f"{CHAT_GENERATOR_MECHANICAL}:{CHAT_NO_SUPPORTED_SENTENCE}"
    assert answer.sentences == mechanical.sentences


def test_a_provider_error_falls_back_with_a_mechanical_label_naming_the_failure() -> None:
    evidence = compose_chat_evidence(
        "node", "T001", [make_chat_item("node", "T001", "Tests passed")]
    )

    def raises_connection(prompt: str, attempt: int) -> str:
        raise ConnectionError("boom")

    answer = answer_chat_question("Did the tests pass?", evidence, call_fn=raises_connection)

    assert answer.generator.startswith(f"{CHAT_GENERATOR_MECHANICAL}:")
    assert answer.generator != f"{CHAT_GENERATOR_MECHANICAL}:{CHAT_NO_SUPPORTED_SENTENCE}"
    mechanical = mechanical_answer("Did the tests pass?", evidence)
    assert answer.sentences == mechanical.sentences


def test_an_unparseable_reply_falls_back_with_a_mechanical_label_naming_the_failure() -> None:
    evidence = compose_chat_evidence(
        "node", "T001", [make_chat_item("node", "T001", "Tests passed")]
    )
    fake = _stub_call_fn("not json")

    answer = answer_chat_question("Did the tests pass?", evidence, call_fn=fake)

    assert answer.generator.startswith(f"{CHAT_GENERATOR_MECHANICAL}:")
    assert answer.generator != f"{CHAT_GENERATOR_MECHANICAL}:{CHAT_NO_SUPPORTED_SENTENCE}"
    mechanical = mechanical_answer("Did the tests pass?", evidence)
    assert answer.sentences == mechanical.sentences


# ---------------------------------------------------------------------------
# THE MODEL CANARY — a model reply inventing a fact for an absent-fact
# question, over a real node scope, still yields "Not in evidence." (DECISION
# F038 D5 (5)).
# ---------------------------------------------------------------------------


def test_model_canary_suite_over_a_real_node_scope_still_reads_not_in_evidence() -> None:
    job, task_id = _make_job()
    evidence = node_evidence_set(job, task_id)
    fake = _stub_call_fn(
        json.dumps({"answer": "The deployment URL is https://deploy.example/app [1]."})
    )

    for question in (
        "What was the deployment URL?",
        "Who approved the invoice?",
        "Which database migration ran in production?",
    ):
        answer = answer_chat_question(question, evidence, call_fn=fake)
        assert answer.generator == f"{CHAT_GENERATOR_MECHANICAL}:{CHAT_NO_SUPPORTED_SENTENCE}", (
            question
        )
        assert len(answer.sentences) == 1, question
        assert answer.sentences[0].text == CHAT_NOT_IN_EVIDENCE, question
        assert answer.sentences[0].supported is True, question
