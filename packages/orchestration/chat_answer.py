"""F038 T001 — the grounded chat's answer: the check that marks a sentence supported or
unsupported against a composed evidence set, the renderer that marks the unsupported
ones, the mechanical answer that restates the items a question names, or says
"Not in evidence.", and the model-written answer that goes through the same check
before it is ever shown (DECISION F038 D4, DECISION F038 D5).

Remedy deliberately does not let an answer's honesty rest on a prompt: every sentence,
model-written or mechanical, is checked here against its own citations before it is
shown.
"""

from __future__ import annotations

import dataclasses
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar

from pydantic import BaseModel

from packages.orchestration.chat_evidence import ChatEvidenceSet, render_chat_evidence
from packages.orchestration.failure_postmortem import FailureSignals, classify
from packages.orchestration.intake import make_structured_call_fn
from packages.orchestration.result_tour import PROVIDER_CALL_ERRORS
from packages.orchestration.role_config import resolve_role_config
from packages.orchestration.structured_outputs import run_structured_call

#: The one sentence an answer gives when nothing in the evidence set answers the question.
CHAT_NOT_IN_EVIDENCE = "Not in evidence."
#: Appended to an unsupported sentence by :func:`render_chat_answer`.
CHAT_UNSUPPORTED_MARK = "[unsupported]"
#: :attr:`ChatAnswer.generator` for :func:`mechanical_answer`.
CHAT_GENERATOR_MECHANICAL = "mechanical"
#: :attr:`ChatAnswer.generator` for a checked, kept model-written reply (DECISION F038 D5 (5)).
CHAT_GENERATOR_SUMMARY_ROLE = "summary-role"
#: The fallback reason when a model-written reply parses but no sentence of it is supported.
CHAT_NO_SUPPORTED_SENTENCE = "no_supported_sentence"
#: `chat_generator_line(CHAT_GENERATOR_MECHANICAL)` (DECISION F038 D13).
CHAT_GENERATOR_LINE_MECHANICAL = "Built from the job's records, without a model."
#: `chat_generator_line` for any `mechanical:<reason>` label — the model's reply was not kept.
CHAT_GENERATOR_LINE_MECHANICAL_FALLBACK = (
    "The model's answer could not be used, so this one is built from the job's records, without a model."
)
#: `chat_generator_line(CHAT_GENERATOR_SUMMARY_ROLE)`.
CHAT_GENERATOR_LINE_SUMMARY_ROLE = (
    "Written by the summary model; every sentence was checked against the job's records."
)
#: `chat_generator_line` for any other label — never expected, but never silent either.
CHAT_GENERATOR_LINE_UNKNOWN = "How this answer was written is not recorded."
#: :attr:`GeneratedChatAnswer.SCHEMA_V`.
GENERATED_CHAT_ANSWER_SCHEMA_V = "generated_chat_answer_v1"
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
#: One claim token: a URL, a backtick span, or a number — checked in this order so a
#: URL's own digits are never re-matched as a bare number (DECISION F038 D5 (1)).
_CLAIM_TOKEN_RE = re.compile(r"https?://\S+|`[^`]*`|\d+(?:\.\d+)?")
#: Trailing punctuation stripped off a claim token once it is taken.
_CLAIM_TRAILING_CHARS = ".,;:)!?"


class GeneratedChatAnswer(BaseModel):
    """The schema the `summary` role is asked to fill for a model-written chat answer
    (DECISION F038 D5 (3)). No length or content constraint of its own: `check_answer`
    is what actually judges the reply, so this class only fixes the shape a response
    must parse into."""

    SCHEMA_V: ClassVar[str] = GENERATED_CHAT_ANSWER_SCHEMA_V

    answer: str


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


def check_answer_sentence(sentence: str, evidence: ChatEvidenceSet) -> ChatAnswerSentence:
    """Check one sentence's citations against `evidence`.

    A sentence that, stripped, equals `CHAT_NOT_IN_EVIDENCE` and cites nothing is
    supported: it claims an absence, not a fact. Otherwise a sentence citing
    nothing is unsupported; one citing any number outside 1 to the set's item
    count is unsupported, naming the numbers the set does not hold; one citing only
    items that resolve is unsupported when it states a URL, a backtick span or a
    number none of its cited items holds (DECISION F038 D5 (1)); every other
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
    cited_items = tuple(evidence.items[number - 1] for number in citations)
    claim_problem = _unsupported_claim_problem(sentence, cited_items)
    if claim_problem:
        return ChatAnswerSentence(
            text=sentence, citations=citations, supported=False, problem=claim_problem
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


def chat_generator_line(generator: str) -> str:
    """One plain sentence saying how an answer labelled `generator` was written (DECISION
    F038 D13): `CHAT_GENERATOR_LINE_MECHANICAL` for `CHAT_GENERATOR_MECHANICAL` exactly,
    `CHAT_GENERATOR_LINE_MECHANICAL_FALLBACK` for any label starting `mechanical:`,
    `CHAT_GENERATOR_LINE_SUMMARY_ROLE` for `CHAT_GENERATOR_SUMMARY_ROLE`, and
    `CHAT_GENERATOR_LINE_UNKNOWN` for anything else, checked in that order."""
    if generator == CHAT_GENERATOR_MECHANICAL:
        return CHAT_GENERATOR_LINE_MECHANICAL
    if generator.startswith(f"{CHAT_GENERATOR_MECHANICAL}:"):
        return CHAT_GENERATOR_LINE_MECHANICAL_FALLBACK
    if generator == CHAT_GENERATOR_SUMMARY_ROLE:
        return CHAT_GENERATOR_LINE_SUMMARY_ROLE
    return CHAT_GENERATOR_LINE_UNKNOWN


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


# ---------------------------------------------------------------------------
# DECISION F038 D5 — the model-written answer: a prompt, a switch, a call and
# the same check, with a mechanical fallback labelled by its reason.
# ---------------------------------------------------------------------------


def build_chat_prompt(question: str, evidence: ChatEvidenceSet) -> str:
    """The prompt handed to the `summary` role: the question, the numbered evidence
    exactly as :func:`render_chat_evidence` renders it, and the answering rules."""
    rendered = render_chat_evidence(evidence)
    return "\n".join([
        f"Question: {question}",
        "",
        "Evidence, each item numbered:",
        rendered or "(no items)",
        "",
        "Rules:",
        "- answer only from the numbered evidence above",
        "- end every sentence with the number of each item it restates, as [n]",
        "- copy numbers, names and paths exactly as the items hold them",
        f"- at most {CHAT_MECHANICAL_MAX_SENTENCES} sentences",
        f"- when no item answers the question, reply exactly: {CHAT_NOT_IN_EVIDENCE}",
    ])


def chat_model_written() -> bool:
    """Whether the grounded chat asks the summary model for its answer: the
    `chat.model_written` key, off by default (DECISION F038 D5 (2)).

    Reads the key the way `tour_model_written` reads its own, the config import
    kept lazy so this module never forces `config.py` to load at import time.
    """
    from packages.orchestration.config import get_config

    return bool(get_config().get("chat.model_written"))


def chat_call_fn(schema: type[BaseModel] = GeneratedChatAnswer) -> Callable[[str, int], str] | None:
    """Build a call_fn for the `summary` role, or None.

    Mirrors `result_tour.tour_call_fn`: `resolve_role_config("summary")` supplies
    the model, `make_structured_call_fn` does the rest. This call site joins
    `model_routing.ROLE_CONFIG_CALL_SITES`. The model-written intent parse asks
    for its own schema through this same call site.
    """
    role_cfg = resolve_role_config("summary")
    return make_structured_call_fn(schema, model=role_cfg.model)


#: `answer_chat_question`'s own sentinel: distinguishes "no call_fn argument was
#: given" (ask `chat_call_fn()` only when the switch is on) from "call_fn=None was
#: given" (build the mechanical answer). A bare `None` default cannot tell those apart.
_UNSET_CALL_FN = object()


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
