"""The Ollama provider of the ping-pong loop: a local Ollama server as a builder or reviewer.

F307 moved it here from ``pingpong_provider.py`` as that file's structural step (2) in
``docs/system/structure-ledger-v1.md``; ``create_provider`` there builds it by the name ``ollama``.
"""
from __future__ import annotations

import os
import time
from typing import Any

from packages.orchestration.call_identity import prepare_call_input
from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.pingpong_provider import (
    _REVIEWER_JSON_SCHEMA,
    BuilderOutput,
    ReviewerOutput,
    _parse_reviewer_json,
    _parse_reviewer_structured,
    extract_builder_files_from_text,
)
from packages.orchestration.schemas import ReviewVerdict, to_json_schema_str
from packages.orchestration.structured_outputs import reviewer_structured_enabled

#: This provider's built-in default model. Resolved from the single alias table
#: (packages/orchestration/model_aliases.py) so no concrete model id is spelled
#: out here; an upgrade repoints the alias, not this file. The host default
#: mirrors packages/providers/ollama_builder/provider.py.
_DEFAULT_OLLAMA_MODEL = resolve_model_alias("ollama-default")
_DEFAULT_OLLAMA_HOST = "http://localhost:11434"


class OllamaPingPongProvider:
    """Builder/Reviewer provider backed by a local Ollama server.

    WHY this class exists beside ``packages/providers/ollama_builder`` and
    ``packages/providers/ollama_planner``: those two speak the
    ``TaskExecutionContext``/``PlannerOutput`` shapes of the autorun and mission
    layers and cannot be handed to ``run_pingpong``. This class implements the
    :class:`PingPongProvider` protocol (``name``/``supports_resume``/``build``/
    ``review``) over the SAME local surface those two reach — the ``ollama``
    package's chat endpoint, host from ``REMEDY_OLLAMA_HOST``, default
    ``http://localhost:11434`` — so ``role_config.DEFAULT_PROVIDER == "ollama"``
    is actually constructible through :func:`create_provider` on the ping-pong
    job path that self-use runs and ``remedy job run`` both use
    (finding R-0761).

    Every transport, HTTP or rate-limit failure this provider reports carries
    the ``provider_error:`` prefix. That prefix is load-bearing, not cosmetic:
    ``ReviewerOutput.verdict`` defaults to ``"blocked"``, so the loop's reject
    predicate would classify a transport error as a review REJECT — and never
    retry or pace it — were the prefix absent (invariant of finding R-0378).
    Malformed model output keeps the separate ``malformed_output:`` idiom, which
    is what routes it to the loop's single parse retry instead.

    Remedy deliberately does NOT do quality fallback or per-role local model
    routing here — that is feature F113. This provider only makes the product
    default constructible and callable.
    """

    def __init__(
        self,
        *,
        model: str = "",
        host: str = "",
        num_predict: int | None = None,
    ) -> None:
        self._model = model or _DEFAULT_OLLAMA_MODEL
        self._host = (
            host or os.environ.get("REMEDY_OLLAMA_HOST") or _DEFAULT_OLLAMA_HOST
        )
        self._num_predict = num_predict

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def supports_resume(self) -> bool:
        # No server-side session to resume: each chat call is stateless.
        return False

    @property
    def resume_unsupported_reason(self) -> str:
        # WHY: DECISION F287 D7 — names, for an offered relaunch session, why
        # this provider never resumes one.
        return "an Ollama chat call keeps no conversation between calls"

    @property
    def model(self) -> str:
        return self._model

    @property
    def host(self) -> str:
        return self._host

    def _call_options(self) -> dict[str, Any]:
        """The material request knobs — also what the F012 fingerprint binds."""
        return {"num_predict": self._num_predict}

    def _call(
        self,
        prompt: str,
        *,
        timeout_sec: int,
        max_output_chars: int,
        format_schema: dict[str, Any] | None = None,
    ) -> tuple[str, int, int]:
        """Call the local Ollama server. Returns (text, duration_ms, tokens_used).

        ``format_schema`` is the server's NATIVE structured-output enforcement
        (out of band, never duplicated into the prompt), the same shape the
        claude-cli path gets from ``--json-schema``.
        """
        try:
            import ollama
        except ImportError as exc:
            raise RuntimeError(
                "ollama package not installed. "
                "Install with: pip install ollama  or  pip install 'remedy[ollama]'"
            ) from exc

        client = ollama.Client(host=self._host, timeout=float(timeout_sec))
        options = {k: v for k, v in self._call_options().items() if v is not None}
        start = time.monotonic()
        response = client.chat(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            **({"format": format_schema} if format_schema is not None else {}),
            **({"options": options} if options else {}),
        )
        elapsed_ms = int((time.monotonic() - start) * 1000)
        text = getattr(response.message, "content", "") or ""
        tokens = int(getattr(response, "eval_count", 0) or 0)
        if len(text) > max_output_chars:
            text = text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return text, elapsed_ms, tokens

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        # F012: the builder prompt is sent verbatim — fingerprint the exact bytes.
        _pi = prepare_call_input(
            prompt=prompt, model=self._model, mode="ollama-legacy",
            options=self._call_options())
        try:
            text, dur, tokens = self._call(
                prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            return BuilderOutput(
                summary=text[:500],
                files_changed=extract_builder_files_from_text(text),
                raw_text=text,
                provider="ollama",
                duration_ms=dur,
                tokens_used=tokens,
                actual_missing_reason="provider_actuals_unavailable",
                prepared_input=_pi,
            )
        except Exception as exc:  # noqa: BLE001 — a provider failure becomes a typed error, not a crash
            return BuilderOutput(
                error=f"provider_error: {type(exc).__name__}: {exc}",
                provider="ollama",
                actual_missing_reason="provider_error",
                prepared_input=_pi,
            )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        structured = reviewer_structured_enabled()
        if structured:
            # The caller has already built the exact effective prompt; it is sent
            # verbatim and the schema is enforced NATIVELY, out of band, so the
            # fingerprint records it as a schema rather than as prompt bytes.
            full_prompt = prompt
            format_schema: dict[str, Any] | None = ReviewVerdict.model_json_schema()
            _pi = prepare_call_input(
                prompt=full_prompt, model=self._model, mode="ollama-native",
                schema=to_json_schema_str(ReviewVerdict),
                options=self._call_options())
        else:
            full_prompt = prompt + "\n\n" + _REVIEWER_JSON_SCHEMA
            format_schema = None
            _pi = prepare_call_input(
                prompt=full_prompt, model=self._model, mode="ollama-legacy",
                options=self._call_options())
        try:
            text, dur, tokens = self._call(
                full_prompt, timeout_sec=timeout_sec,
                max_output_chars=max_output_chars, format_schema=format_schema,
            )
            out = (
                _parse_reviewer_structured(text, dur, tokens, provider="ollama")
                if structured
                else _parse_reviewer_json(text, dur, tokens, provider="ollama")
            )
            out.actual_missing_reason = "provider_actuals_unavailable"
            out.prepared_input = _pi
            return out
        except Exception as exc:  # noqa: BLE001 — a provider failure becomes a typed error, not a crash
            return ReviewerOutput(
                error=f"provider_error: {type(exc).__name__}: {exc}",
                error_class="provider_error",
                provider="ollama",
                actual_missing_reason="provider_error",
                prepared_input=_pi,
            )
