"""Hermetic tests for the Ollama ping-pong provider (amend0902, R-0761).

The HTTP boundary is mocked by installing a fake ``ollama`` module into
``sys.modules``: the provider imports it inside ``_call``, so the fake is what
the provider actually reaches. No test here touches a live server — see
``tests/conftest.py::_no_live_ollama_reach``, whose refusal of the real
``ollama.Client`` is the reason the transport-failure test needs no network.
"""
from __future__ import annotations

import json
import sys
import types

import pytest

from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.pingpong_provider import (
    OllamaPingPongProvider,
    create_provider,
)

# ---------------------------------------------------------------------------
# Fake ollama module — the mocked HTTP boundary
# ---------------------------------------------------------------------------


class _FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _FakeChatResponse:
    """Mirrors the shape the real ``ollama`` ChatResponse exposes."""

    def __init__(self, content: str, eval_count: int) -> None:
        self.message = _FakeMessage(content)
        self.eval_count = eval_count


def install_fake_ollama(
    monkeypatch,
    *,
    content: str = "",
    eval_count: int = 0,
    chat_raises: Exception | None = None,
    client_raises: Exception | None = None,
) -> dict:
    """Install a fake ``ollama`` module and return the record of what it saw."""
    record: dict = {"client_kwargs": None, "chat_kwargs": None}

    class _FakeClient:
        def __init__(self, **kwargs):
            if client_raises is not None:
                raise client_raises
            record["client_kwargs"] = kwargs

        def chat(self, **kwargs):
            record["chat_kwargs"] = kwargs
            if chat_raises is not None:
                raise chat_raises
            return _FakeChatResponse(content, eval_count)

    module = types.ModuleType("ollama")
    module.Client = _FakeClient
    monkeypatch.setitem(sys.modules, "ollama", module)
    return record


def _verdict_json(**overrides) -> str:
    payload = {
        "schema_v": "rv1",
        "verdict": "needs_repair",
        "findings": [
            {
                "id": "R-0001",
                "severity": "medium",
                "file": "docs/README.md",
                "summary": "Missing verification note",
                "required_fix": "Add a verification note.",
            },
        ],
        "confidence": "medium",
        "summary": "One issue found.",
    }
    payload.update(overrides)
    return json.dumps(payload)


# ---------------------------------------------------------------------------
# 1. The factory constructs the product default
# ---------------------------------------------------------------------------


class TestFactoryConstructsOllama:
    def test_create_ollama(self):
        p = create_provider("ollama")
        assert isinstance(p, OllamaPingPongProvider)
        assert p.name == "ollama"

    def test_ollama_is_named_in_the_error_string(self):
        with pytest.raises(RuntimeError, match="fake, claude, claude-cli, ollama"):
            create_provider("nonexistent_provider")

    def test_role_config_default_provider_is_constructible(self):
        """The product default must be a name the factory actually accepts.

        This is the R-0761 defect stated as a test: role_config resolved
        "ollama" while create_provider knew only three other names, so every
        unflagged job-path run blocked with provider_unavailable.
        """
        from packages.orchestration.role_config import DEFAULT_PROVIDER

        assert create_provider(DEFAULT_PROVIDER).name == DEFAULT_PROVIDER

    def test_does_not_claim_resume(self):
        assert create_provider("ollama").supports_resume is False


# ---------------------------------------------------------------------------
# 2. Model and host resolution
# ---------------------------------------------------------------------------


class TestModelResolution:
    def test_default_model_is_the_alias(self):
        assert create_provider("ollama").model == resolve_model_alias("ollama-default")

    def test_explicit_model_wins(self):
        assert create_provider("ollama", model="qwen-test:latest").model == "qwen-test:latest"

    def test_host_from_env(self, monkeypatch):
        monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://127.0.0.1:9999")
        assert OllamaPingPongProvider().host == "http://127.0.0.1:9999"

    def test_host_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_OLLAMA_HOST", raising=False)
        assert OllamaPingPongProvider().host == "http://localhost:11434"


# ---------------------------------------------------------------------------
# 3. One build round trip over the mocked boundary
# ---------------------------------------------------------------------------


class TestBuildRoundTrip:
    def test_build_returns_parsed_output(self, monkeypatch):
        record = install_fake_ollama(
            monkeypatch,
            content="Changed:\n- docs/README.md updated\n- packages/x/y.py added\n",
            eval_count=42,
        )
        out = OllamaPingPongProvider(model="m:test").build("Do the thing", timeout_sec=7)

        assert out.error == ""
        assert out.provider == "ollama"
        assert out.files_changed == ["docs/README.md", "packages/x/y.py"]
        assert out.tokens_used == 42
        assert "docs/README.md" in out.raw_text
        # The prompt reached the transport verbatim.
        assert record["chat_kwargs"]["messages"] == [
            {"role": "user", "content": "Do the thing"},
        ]
        assert record["chat_kwargs"]["model"] == "m:test"
        # The builder call carries no schema enforcement.
        assert "format" not in record["chat_kwargs"]
        # The caller's timeout reaches the client, not just the loop.
        assert record["client_kwargs"]["timeout"] == 7.0

    def test_build_output_is_capped(self, monkeypatch):
        install_fake_ollama(monkeypatch, content="x" * 500)
        out = OllamaPingPongProvider().build("p", max_output_chars=100)
        assert out.raw_text.endswith("[OUTPUT TRUNCATED]")
        assert len(out.raw_text) < 200


# ---------------------------------------------------------------------------
# 4. One review round trip over the mocked boundary
# ---------------------------------------------------------------------------


class TestReviewRoundTrip:
    def test_structured_review_uses_the_shared_schema_path(self, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        record = install_fake_ollama(monkeypatch, content=_verdict_json(), eval_count=11)
        out = OllamaPingPongProvider().review("Review this", timeout_sec=5)

        assert out.error == ""
        assert out.provider == "ollama"
        assert out.verdict == "needs_repair"
        assert out.confidence == "medium"
        assert out.schema_v == "rv1"
        assert [f.id for f in out.findings] == ["R-0001"]
        assert out.tokens_used == 11
        # Native enforcement, out of band: the schema is a request field, and
        # the prompt is NOT padded with a second copy of it.
        fmt = record["chat_kwargs"]["format"]
        assert isinstance(fmt, dict)
        assert fmt["properties"]["schema_v"]["const"] == "rv1"
        assert record["chat_kwargs"]["messages"][0]["content"] == "Review this"

    def test_freetext_review_falls_back_to_the_json_parser(self, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        record = install_fake_ollama(
            monkeypatch,
            content='{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}',
        )
        out = OllamaPingPongProvider().review("Review this")

        assert out.error == ""
        assert out.verdict == "pass"
        assert out.provider == "ollama"
        # Legacy mode embeds the schema in the prompt and sends no format field.
        assert "format" not in record["chat_kwargs"]
        assert "Review this" in record["chat_kwargs"]["messages"][0]["content"]
        assert len(record["chat_kwargs"]["messages"][0]["content"]) > len("Review this")

    def test_malformed_output_is_not_a_provider_error(self, monkeypatch):
        """Bad model output must keep the malformed_output: idiom.

        The two prefixes route differently: malformed_output: reaches the
        loop's single parse retry, provider_error: reaches the retry/pacing
        path. Reporting one as the other silently misroutes it.
        """
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        install_fake_ollama(monkeypatch, content="not json at all {{{")
        out = OllamaPingPongProvider().review("Review this")

        assert out.error.startswith("malformed_output:")
        assert not out.error.startswith("provider_error:")
        assert out.error_class == "parse"


# ---------------------------------------------------------------------------
# 5. Transport failures carry the provider_error: prefix (R-0378 invariant)
# ---------------------------------------------------------------------------


class TestTransportFailuresArePrefixed:
    """R-0378: ReviewerOutput.verdict defaults to "blocked", so the loop's
    reject predicate reads a transport error as a review REJECT — never
    retried, never paced — unless the error carries the provider_error:
    prefix. Every failure path below must therefore keep it.
    """

    def test_review_connection_refused(self, monkeypatch):
        install_fake_ollama(
            monkeypatch, client_raises=ConnectionError("connection refused"),
        )
        out = OllamaPingPongProvider().review("Review this")
        assert out.error.startswith("provider_error:")
        assert "ConnectionError" in out.error
        assert out.error_class == "provider_error"
        assert out.provider == "ollama"

    def test_review_rate_limited(self, monkeypatch):
        install_fake_ollama(
            monkeypatch, chat_raises=RuntimeError("429 Too Many Requests"),
        )
        out = OllamaPingPongProvider().review("Review this")
        assert out.error.startswith("provider_error:")
        assert "429" in out.error

    def test_build_connection_refused(self, monkeypatch):
        install_fake_ollama(
            monkeypatch, client_raises=ConnectionError("connection refused"),
        )
        out = OllamaPingPongProvider().build("Do the thing")
        assert out.error.startswith("provider_error:")
        assert out.actual_missing_reason == "provider_error"

    def test_missing_ollama_package_is_a_provider_error(self, monkeypatch):
        """An uninstalled ollama package must not look like a review reject."""
        monkeypatch.setitem(sys.modules, "ollama", None)
        out = OllamaPingPongProvider().build("Do the thing")
        assert out.error.startswith("provider_error:")
