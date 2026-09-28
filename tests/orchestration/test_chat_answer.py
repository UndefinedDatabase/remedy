"""F038 T001 — the grounded chat's answer: the citation check, the mechanical answer
and the canary suite of absent-fact questions over real node and project scopes.
"""

from __future__ import annotations

import pytest

from packages.orchestration.chat_answer import (
    CHAT_NOT_IN_EVIDENCE,
    ChatAnswer,
    ChatAnswerSentence,
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
