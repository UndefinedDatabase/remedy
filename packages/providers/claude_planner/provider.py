"""Claude-CLI-backed planner provider — the SECOND planning service.

Until this module existed, ``OllamaPlanner``
(``packages/providers/ollama_planner/provider.py``) was the only planner
Remedy had, which is why ``--planner-provider`` could not be offered: a flag
with one legal value advertises a choice that does not exist (operator
question Q1, second ruling). :class:`ClaudeCliPlanner` exposes exactly that
planner's three methods — ``plan``, ``raw_call`` and ``plan_raw`` — with
exactly its return types, so either can serve any caller of
``packages.orchestration.intake.make_structured_call_fn``.

Configuration (environment variables):
  REMEDY_CLAUDE_PLANNER_MODEL    — model for the planner role
  REMEDY_CLAUDE_PLANNER_TIMEOUT  — per-call wall timeout in seconds (int)

Precedence for model selection:
  1. Constructor argument ``model``
  2. REMEDY_CLAUDE_PLANNER_MODEL
  3. ``planner.model`` in the configuration
  4. The alias table's Sonnet alias (``claude-workhorse``)

WHY THE SCHEMA IS STATED IN THE PROMPT AND NOT ON THE COMMAND LINE. Ollama
enforces a schema NATIVELY through ``format=``, so its planner never has to
ask. The ``claude`` CLI has no equivalent this module is willing to depend on:
``--json-schema`` exists on the reviewer path in
``packages.orchestration.pingpong_provider``, and that path carries a
classifier (``_looks_like_unknown_json_schema_option``) precisely because the
flag's support is proven only by the invocation and can be absent. A planner
that fell over on such a CLI would be a planner in name only, so the schema is
stated in the SYSTEM text, the reply is stripped of code fences, and it is
validated here. One retry, then the failure is raised.

Deliberate absences:
  * REMEDY DELIBERATELY DOES NOT SPAWN THE CLI ITSELF. Every ``claude -p`` call
    goes through the helpers the claude-cli ping-pong provider already uses —
    ``build_claude_cli_args``, ``_guarded_cli_run`` and
    ``_extract_cli_result_text`` of
    ``packages.orchestration.pingpong_provider`` — so this planner inherits
    that seam's exec guard (wall deadline, cwd pin, zero core) and its envelope
    parsing rather than growing a second, weaker copy of them.
  * Remedy deliberately does not invent an exception class for a bad reply.
    A reply that survives neither attempt raises ``pydantic.ValidationError``,
    the class ``OllamaPlanner.plan`` already documents for a schema failure, and
    it is raised by validating the reply itself — never hand-built.
  * Remedy deliberately does not count tokens or cost here. The planner path
    has no ledger of its own; ``packages.orchestration.token_actuals`` reads the
    CLI envelope for the roles that do.
"""

from __future__ import annotations

import json
import os
from typing import Any

from pydantic import BaseModel, create_model

from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.planner_models import PlannerOutput

#: This provider's built-in default model: the alias table's Sonnet alias
#: (packages/orchestration/model_aliases.py), so an upgrade repoints the alias
#: and never this file.
_DEFAULT_MODEL = resolve_model_alias("claude-workhorse")

#: How much of one reply is kept. Far past any schema-shaped answer; a reply
#: longer than this is a runaway, and truncating it makes the JSON invalid,
#: which is exactly the outcome a runaway deserves.
_MAX_OUTPUT_CHARS = 200_000

_SYSTEM_PROMPT = """\
You are a project planning assistant. Given a job description, produce a structured plan.

Rules:
- proposed_tasks: list of tasks needed to complete the job. Each task needs:
    task_type: concise snake_case identifier (e.g. write_tests, implement_feature)
    description: one clear sentence describing what the task does
- summary: short paragraph summarising the overall plan
- acceptance_checks: optional list of criteria that must pass for the job to be complete
- notes: optional list of assumptions or caveats

Respond only with valid JSON matching the requested schema. No markdown, no extra text.\
"""

#: The sentence the whole prompt-side schema discipline rests on, spelled ONCE.
_ONE_OBJECT_INSTRUCTION = "Answer with one JSON object and nothing else."


def _resolve_model(override: str | None) -> str:
    """Resolve the planner model: argument, env var, config, then the Sonnet alias."""
    if override:
        return override
    env_model = os.environ.get("REMEDY_CLAUDE_PLANNER_MODEL")
    if env_model:
        return env_model
    from packages.orchestration.config import get_config

    configured = get_config().get("planner.model")
    if configured:
        return configured
    return _DEFAULT_MODEL


def _resolve_timeout(override: int | None) -> int:
    """Resolve the per-call wall timeout; a malformed env var is an error, not a guess."""
    if override is not None:
        return int(override)
    # The default, 300 seconds, lives in the variable's spec (DECISION F279 D4).
    from packages.orchestration.config import env_value

    return env_value("REMEDY_CLAUDE_PLANNER_TIMEOUT")


def _schema_reply_model(schema: dict) -> type[BaseModel]:
    """A pydantic model that accepts exactly what ``schema`` REQUIRES, and no less.

    ``raw_call`` is handed a JSON schema as a plain mapping, not a model class,
    so there is no model to validate against — and Remedy ships no JSON-schema
    validator. This builds the one thing the schema unambiguously demands: a
    JSON OBJECT carrying every key its top-level ``required`` list names, each
    of any type. Validating through pydantic (rather than checking keys by hand)
    is what makes the raised failure a genuine ``ValidationError`` about the
    reply, which is the class this provider's Ollama twin raises.

    A schema with no ``required`` list yields a model with no fields, so the
    check narrows to "the reply is a JSON object" — which is all such a schema
    actually asks for.
    """
    required = [key for key in schema.get("required", ()) if isinstance(key, str)]
    fields: dict[str, Any] = {name: (Any, ...) for name in required}
    return create_model("ClaudeCliPlannerReply", **fields)


class ClaudeCliPlanner:
    """Planner provider backed by the local ``claude`` CLI.

    Role: planner. Configure via REMEDY_CLAUDE_PLANNER_MODEL, or the
    ``planner`` role's ``provider``/``model`` in the configuration.

    Usage:
        planner = ClaudeCliPlanner()
        output: PlannerOutput = planner.plan("build a CLI tool that summarises files")
    """

    def __init__(
        self,
        model: str | None = None,
        *,
        cwd: str | None = None,
        timeout_sec: int | None = None,
    ) -> None:
        self.model = _resolve_model(model)
        self.cwd = cwd
        self.timeout_sec = _resolve_timeout(timeout_sec)

    # -- the CLI seam -------------------------------------------------------

    def _run_cli(self, prompt: str) -> str:
        """One ``claude -p`` call through the ping-pong provider's own helpers.

        Imported inside the body so a planner that is never used costs no
        import of the provider module, and so a test can monkeypatch
        ``packages.orchestration.pingpong_provider._guarded_cli_run`` — the ONE
        spawn point — and see this planner take the same route the ping-pong
        provider takes.
        """
        import shutil
        import subprocess

        from packages.orchestration import pingpong_provider

        claude_path = shutil.which("claude")
        if not claude_path:
            raise RuntimeError(
                "claude CLI not found on PATH. Install Claude Code CLI to use "
                "--planner-provider claude-cli."
            )
        argv = pingpong_provider.build_claude_cli_args(
            claude_path, prompt, write_mode="none", model=self.model,
        )
        try:
            proc = pingpong_provider._guarded_cli_run(
                argv, timeout_sec=self.timeout_sec, cwd=self.cwd,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                f"claude CLI timed out after {self.timeout_sec}s"
            ) from None
        if proc.returncode != 0:
            stderr = (proc.stderr or "")[:500]
            raise RuntimeError(f"claude CLI exited {proc.returncode}: {stderr}")
        text = pingpong_provider._extract_cli_result_text(proc.stdout or "")
        if len(text) > _MAX_OUTPUT_CHARS:
            text = text[:_MAX_OUTPUT_CHARS]
        return text

    # -- the one retry loop -------------------------------------------------

    def _call_validated(
        self, prompt: str, *, system: str, schema_text: str,
        reply_model: type[BaseModel],
    ) -> tuple[str, BaseModel]:
        """Call the CLI until the reply validates, at most twice.

        The system text carries the schema and
        :data:`_ONE_OBJECT_INSTRUCTION`, because the CLI enforces neither. The
        reply is stripped of code fences by
        ``packages.orchestration.schemas.validation._extract_json_object``, the
        repository's own stripper, and validated against ``reply_model``.

        EXACTLY ONE RETRY, and it is told what was wrong with the first reply so
        the second is not a blind re-roll. A second failure raises the
        ``pydantic.ValidationError`` the validation itself produced — the class
        ``OllamaPlanner.plan`` documents for a schema failure.

        Answers ``(json_text, validated)`` — the reply's own bytes, fences
        stripped, beside the model the validation produced.
        """
        from packages.orchestration.schemas.validation import _extract_json_object

        system_text = (
            f"{system}\n\n"
            f"{_ONE_OBJECT_INSTRUCTION} It must be valid against this JSON "
            f"schema:\n{schema_text}"
        )
        attempt_prompt = f"{system_text}\n\n{prompt}"
        last_reason = ""
        for attempt in (1, 2):
            if attempt == 2:
                attempt_prompt = (
                    f"{system_text}\n\n{prompt}\n\n"
                    f"Your previous response was invalid: {last_reason}\n"
                    f"{_ONE_OBJECT_INSTRUCTION}"
                )
            raw = self._run_cli(attempt_prompt)
            obj, reason = _extract_json_object(raw)
            if reason:
                if attempt == 2:
                    # Raises ValidationError for malformed JSON — the same class
                    # the object branch below raises, from the reply itself.
                    return raw, reply_model.model_validate_json(raw)
                last_reason = reason
                continue
            try:
                validated = reply_model.model_validate(obj)
            except Exception as exc:
                if attempt == 2:
                    raise
                last_reason = str(exc)[:500]
                continue
            return json.dumps(obj, separators=(",", ":")), validated
        raise AssertionError("unreachable: the loop returns or raises on attempt 2")

    # -- the three methods, matching OllamaPlanner --------------------------

    def plan(self, prompt: str) -> PlannerOutput:
        """Call the CLI and return a validated :class:`PlannerOutput`.

        Raises:
            RuntimeError: the ``claude`` CLI is missing, timed out, or exited
                non-zero.
            pydantic.ValidationError: two replies in a row failed the schema.
        """
        from packages.orchestration.schemas import to_json_schema_str

        _, validated = self._call_validated(
            f"Plan this job:\n\n{prompt}",
            system=_SYSTEM_PROMPT,
            schema_text=to_json_schema_str(PlannerOutput),
            reply_model=PlannerOutput,
        )
        assert isinstance(validated, PlannerOutput)
        return validated

    def raw_call(self, prompt: str, *, schema: dict, system: str | None = None) -> str:
        """Send a prompt with the schema stated in the system text, return raw text.

        The return is the reply's own JSON object, fences stripped — the
        parallel of what ``OllamaPlanner.raw_call`` returns, which native
        ``format=`` already guarantees to be schema-shaped JSON. The caller
        parses it, exactly as it parses Ollama's.
        """
        text, _ = self._call_validated(
            prompt,
            system=system if system is not None else _SYSTEM_PROMPT,
            schema_text=json.dumps(schema, separators=(",", ":"), sort_keys=True),
            reply_model=_schema_reply_model(schema),
        )
        return text

    def plan_raw(self, prompt: str, *, schema: dict) -> str:
        """Return the raw planner reply text, wrapped the way the planner asks.

        Delegates to :meth:`raw_call` with the planner system prompt and the
        "Plan this job:" wrapping — the same delegation
        ``OllamaPlanner.plan_raw`` makes.
        """
        return self.raw_call(
            f"Plan this job:\n\n{prompt}",
            schema=schema,
            system=_SYSTEM_PROMPT,
        )
