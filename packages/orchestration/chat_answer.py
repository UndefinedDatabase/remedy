"""F038 T001 — the grounded chat's answer: the check that marks a sentence supported or
unsupported against a composed evidence set, the renderer that marks the unsupported
ones, and the mechanical answer that restates the items a question names, or says
"Not in evidence." (DECISION F038 D4).

Remedy deliberately does not let an answer's honesty rest on a prompt: every sentence,
model-written or mechanical, is checked here against its own citations before it is
shown.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from packages.orchestration.chat_evidence import ChatEvidenceSet

#: The one sentence an answer gives when nothing in the evidence set answers the question.
CHAT_NOT_IN_EVIDENCE = "Not in evidence."
#: Appended to an unsupported sentence by :func:`render_chat_answer`.
CHAT_UNSUPPORTED_MARK = "[unsupported]"
#: :attr:`ChatAnswer.generator` for :func:`mechanical_answer`.
CHAT_GENERATOR_MECHANICAL = "mechanical"
#: The mechanical answer restates at most this many items.
CHAT_MECHANICAL_MAX_SENTENCES = 5
#: A question word shorter than this is never a keyword.
CHAT_KEYWORD_MIN_CHARS = 3
#: Question words too common to score a match (DECISION F038 D4 (3)).
CHAT_QUESTION_STOPWORDS = frozenset({
    "about", "and", "any", "are", "can", "did", "does", "for", "from", "had", "has",
    "have", "how", "its", "the", "that", "there", "this", "was", "were", "what",
    "when", "where", "which", "who", "why", "with", "you", "your",
})

#: A citation is `[<digits>]`.
_CITATION_RE = re.compile(r"\[(\d+)\]")
#: A sentence is split after a `.`, `!` or `?` that whitespace follows.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])(?=\s)")
#: A run of keyword-eligible characters, in a question or in an evidence item.
_WORD_RUN_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class ChatAnswerSentence:
    """One sentence of a :class:`ChatAnswer`, checked against its evidence set."""

    text: str
    citations: tuple[int, ...]
    supported: bool
    problem: str


@dataclass(frozen=True)
class ChatAnswer:
    """A checked answer to one question, over one evidence set."""

    scope: str
    subject: str
    question: str
    generator: str
    sentences: tuple[ChatAnswerSentence, ...]

    @property
    def unsupported_count(self) -> int:
        """How many of :attr:`sentences` are not supported."""
        return sum(1 for sentence in self.sentences if not sentence.supported)


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


def check_answer(
    text: str, evidence: ChatEvidenceSet, *, question: str, generator: str
) -> ChatAnswer:
    """Check every sentence of `text` — or `CHAT_NOT_IN_EVIDENCE` when `text` holds
    none — against `evidence`. `scope` and `subject` come from `evidence`."""
    raw_sentences = split_answer_sentences(text) or [CHAT_NOT_IN_EVIDENCE]
    sentences = tuple(check_answer_sentence(sentence, evidence) for sentence in raw_sentences)
    return ChatAnswer(
        scope=evidence.scope, subject=evidence.subject, question=question,
        generator=generator, sentences=sentences,
    )


def render_chat_answer(answer: ChatAnswer) -> str:
    """Every sentence of `answer`, joined by one space, each unsupported one followed
    by a space and `CHAT_UNSUPPORTED_MARK`."""
    parts = [
        sentence.text if sentence.supported else f"{sentence.text} {CHAT_UNSUPPORTED_MARK}"
        for sentence in answer.sentences
    ]
    return " ".join(parts)


def question_keywords(question: str) -> tuple[str, ...]:
    """The lower-cased `question`'s runs of `[a-z0-9]` at least `CHAT_KEYWORD_MIN_CHARS`
    long and not a stopword, each once, in first-seen order."""
    keywords: list[str] = []
    seen: set[str] = set()
    for run in _WORD_RUN_RE.findall(question.lower()):
        if len(run) < CHAT_KEYWORD_MIN_CHARS or run in CHAT_QUESTION_STOPWORDS or run in seen:
            continue
        seen.add(run)
        keywords.append(run)
    return tuple(keywords)


def _item_score(item_ref: str, item_text: str, keywords: tuple[str, ...]) -> int:
    """How many `keywords` begin at least one `[a-z0-9]` run of `item_ref` and
    `item_text` together, lower-cased."""
    runs = _WORD_RUN_RE.findall(f"{item_ref} {item_text}".lower())
    return sum(1 for keyword in keywords if any(run.startswith(keyword) for run in runs))


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
