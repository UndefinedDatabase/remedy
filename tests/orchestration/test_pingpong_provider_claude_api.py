"""The direct-API provider keeps the usage it is given (F273 T015 (a)).

``ClaudeProvider`` used to read only ``output_tokens`` and stamp every call
``provider_actuals_unavailable``, send one flat user message, and report every
failure as a bare class name. Every test here drives a FAKE client object whose
``messages.create`` returns a fake response: no network, no real model, no SDK
needed except where a test says so and skips without it.
"""
from __future__ import annotations

import hashlib
import sys
import types
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import run_pingpong
from packages.orchestration.pingpong_provider import ClaudeProvider, FakeProvider
from packages.orchestration.prompt_segments import (
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)

_REPO = Path(__file__).resolve().parents[2]
_VERDICT = '{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}'


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _usage(**fields):
    return types.SimpleNamespace(**fields)


def _provider(usage=None, text=_VERDICT, raises=None):
    captured: dict = {}

    class _Messages:
        @staticmethod
        def create(**kw):
            captured.update(kw)
            if raises is not None:
                raise raises
            block = types.SimpleNamespace(text=text)
            return types.SimpleNamespace(content=[block], usage=usage)

    p = ClaudeProvider(model="claude-x")
    p._client = types.SimpleNamespace(messages=_Messages())
    return p, captured


_FULL = _usage(input_tokens=120, output_tokens=30,
               cache_read_input_tokens=900, cache_creation_input_tokens=40)
_EXPECTED = {"input_tokens": 120, "output_tokens": 30, "cache_read": 900,
             "cache_creation": 40, "parse_source": "anthropic_api"}


class TestTheSdkUsageIsRecorded:
    def test_build_records_all_four_usage_fields(self):
        p, _ = _provider(_FULL, text="- docs/x.md\nchanged")
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert {k: out.usage_actuals[k] for k in _EXPECTED} == _EXPECTED
        assert out.actual_missing_reason == ""
        assert out.tokens_used == 150

    def test_review_records_all_four_usage_fields(self):
        p, _ = _provider(_FULL)
        out = p.review("REVIEW", timeout_sec=5, max_output_chars=1000)
        assert {k: out.usage_actuals[k] for k in _EXPECTED} == _EXPECTED
        assert out.actual_missing_reason == ""

    def test_the_actuals_carry_the_cli_providers_keys(self):
        p, _ = _provider(_FULL)
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert set(out.usage_actuals) == {
            "input_tokens", "output_tokens", "cache_read", "cache_creation",
            "total_cost_usd", "num_turns", "duration_ms", "session_id",
            "cli_version", "parse_source"}

    def test_absent_cache_fields_read_zero(self):
        p, _ = _provider(_usage(input_tokens=7, output_tokens=3,
                                cache_read_input_tokens=None))
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert (out.usage_actuals["cache_read"], out.usage_actuals["cache_creation"]) == (0, 0)

    def test_usage_without_input_tokens_is_usage_missing_not_unavailable(self):
        p, _ = _provider(_usage(output_tokens=5))
        out = p.review("REVIEW", timeout_sec=5, max_output_chars=1000)
        assert out.usage_actuals is None
        assert out.actual_missing_reason == "usage_missing"


class TestTheStablePrefixIsACachedSystemBlock:
    def test_an_offered_prefix_is_sent_as_a_cached_system_block(self):
        p, captured = _provider(_FULL, text="done")
        p.offer_stable_prefix("RULES")
        out = p.build("RULES\n\nTASK", timeout_sec=5, max_output_chars=1000)
        assert captured["system"] == [{"type": "text", "text": "RULES",
                                       "cache_control": {"type": "ephemeral"}}]
        user = captured["messages"][0]["content"]
        assert user == "\n\nTASK"
        assert out.prepared_input.prompt_sha256 == _sha(captured["system"][0]["text"] + user)

    def test_a_prompt_the_prefix_does_not_start_is_sent_whole(self):
        p, captured = _provider(_FULL, text="done")
        p.offer_stable_prefix("RULES")
        p.build("OTHER\n\nTASK", timeout_sec=5, max_output_chars=1000)
        assert "system" not in captured
        assert captured["messages"][0]["content"] == "OTHER\n\nTASK"

    def test_the_composed_stable_prefix_ends_before_the_first_task_segment(self):
        reg = PromptSegmentRegistry()
        reg.register("sys", SegmentStabilityRank.SYSTEM, "S")
        reg.register("task", SegmentStabilityRank.TASK, "T")
        reg.register("ctx", SegmentStabilityRank.JOB_CONTEXT, "CC")
        composed = compose_prompt_segments(reg.registered_segments())
        assert composed.text == "S\n\nCC\n\nT"
        assert composed.stable_prefix() == "S\n\nCC"

    def test_a_prompt_that_opens_with_its_task_has_no_stable_prefix(self):
        reg = PromptSegmentRegistry()
        reg.register("task", SegmentStabilityRank.TASK, "T")
        assert compose_prompt_segments(reg.registered_segments()).stable_prefix() == ""

    def test_the_loop_offers_each_call_a_prefix_of_its_own_prompt(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "repo"
        (repo / "docs").mkdir(parents=True)
        (repo / "README.md").write_text("# Demo\n")
        (repo / "docs" / "README.md").write_text("# Docs\n")
        seen: list[tuple[str, str]] = []

        class _Recording(FakeProvider):
            offered = ""

            def offer_stable_prefix(self, prefix):
                self.offered = prefix

            def build(self, prompt, **kw):
                seen.append((self.offered, prompt))
                return super().build(prompt, **kw)

            def review(self, prompt, **kw):
                seen.append((self.offered, prompt))
                return super().review(prompt, **kw)

        prov = _Recording()
        run_pingpong("Fix README", str(repo), builder_provider=prov, reviewer_provider=prov)
        assert seen
        assert all(offered and prompt.startswith(offered) and offered != prompt
                   for offered, prompt in seen), [(len(o), p[:60]) for o, p in seen]


def _fake_sdk() -> types.ModuleType:
    """The SDK's error hierarchy, by name and shape, without the SDK."""
    sdk = types.ModuleType("anthropic")

    class APIError(Exception):
        pass

    class APIConnectionError(APIError):
        pass

    class APITimeoutError(APIConnectionError):
        pass

    class APIStatusError(APIError):
        def __init__(self, message, status_code):
            super().__init__(message)
            self.status_code = status_code

    sdk.APIError, sdk.APIStatusError = APIError, APIStatusError
    sdk.APIConnectionError, sdk.APITimeoutError = APIConnectionError, APITimeoutError
    for name in ("AuthenticationError", "PermissionDeniedError", "NotFoundError",
                 "RateLimitError", "BadRequestError", "InternalServerError"):
        setattr(sdk, name, type(name, (APIStatusError,), {}))
    return sdk


_STATUS_CASES = [
    ("AuthenticationError", 401, "authentication_failed"),
    ("PermissionDeniedError", 403, "permission_denied"),
    ("NotFoundError", 404, "not_found"),
    ("RateLimitError", 429, "rate_limited"),
    ("BadRequestError", 400, "bad_request"),
    ("InternalServerError", 500, "server_error"),
    ("APIStatusError", 409, "api_status_error"),
]


class TestEachFailureKeepsItsKindStatusAndMessage:
    @pytest.mark.parametrize("cls_name,status,kind", _STATUS_CASES)
    def test_a_status_error_maps_to_its_kind_and_keeps_the_status(
        self, monkeypatch, cls_name, status, kind,
    ):
        sdk = _fake_sdk()
        monkeypatch.setitem(sys.modules, "anthropic", sdk)
        p, _ = _provider(raises=getattr(sdk, cls_name)("boom said the API", status))
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert out.error == (
            f"provider_error: {cls_name}: {kind} (HTTP {status}): boom said the API")
        assert p.review("R", timeout_sec=5, max_output_chars=1000).error == out.error

    def test_a_timeout_is_not_reported_as_its_connection_parent(self, monkeypatch):
        sdk = _fake_sdk()
        monkeypatch.setitem(sys.modules, "anthropic", sdk)
        p, _ = _provider(raises=sdk.APITimeoutError("Request timed out."))
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert out.error == "provider_error: APITimeoutError: timeout: Request timed out."

    def test_a_missing_key_says_so(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        p = ClaudeProvider(model="claude-x")
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert out.error.startswith("provider_error: RuntimeError: ANTHROPIC_API_KEY not set.")

    @pytest.mark.parametrize("key,in_env", [
        # No redaction pattern knows this shape: only the by-value cut removes it.
        ("plain.secret.value.4815162342", True),
        # Not the live key: only the pattern redaction removes it.
        ("sk-ant-api03-" + "Zq7" * 12, False),
    ])
    def test_no_key_reaches_the_error_text(self, monkeypatch, key, in_env):
        if in_env:
            monkeypatch.setenv("ANTHROPIC_API_KEY", key)
        else:
            monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        sdk = _fake_sdk()
        monkeypatch.setitem(sys.modules, "anthropic", sdk)
        p, _ = _provider(raises=sdk.AuthenticationError(f"invalid x-api-key {key}", 401))
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert key not in out.error and key[:16] not in out.error
        assert out.error.startswith(
            "provider_error: AuthenticationError: authentication_failed (HTTP 401): ")

    def test_the_real_sdk_hierarchy_meets_the_chain(self, monkeypatch):
        anthropic = pytest.importorskip("anthropic")
        import httpx

        req = httpx.Request("POST", "https://api.anthropic.invalid/v1/messages")
        rate = anthropic.RateLimitError(
            "slow down", response=httpx.Response(429, request=req), body=None)
        p, _ = _provider(raises=rate)
        assert p.build("B", timeout_sec=5, max_output_chars=10).error == (
            "provider_error: RateLimitError: rate_limited (HTTP 429): slow down")
        p, _ = _provider(raises=anthropic.APITimeoutError(request=req))
        assert p.build("B", timeout_sec=5, max_output_chars=10).error.startswith(
            "provider_error: APITimeoutError: timeout: ")


class TestTheSdkIsADeclaredExtra:
    def test_the_import_error_names_the_extra(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
        monkeypatch.setitem(sys.modules, "anthropic", None)
        with pytest.raises(RuntimeError, match=r"pip install 'remedy\[anthropic\]'"):
            ClaudeProvider()._get_client()

    def test_pyproject_declares_the_extra(self):
        text = (_REPO / "pyproject.toml").read_text(encoding="utf-8")
        extras = text.split("[project.optional-dependencies]", 1)[1].split("\n[", 1)[0]
        assert 'anthropic = ["anthropic>=' in extras
