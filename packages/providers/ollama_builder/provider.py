"""
Ollama-backed builder provider.

Calls a local Ollama instance with structured output (JSON schema enforcement)
to produce a validated BuilderOutput.

Configuration (environment variables):
  REMEDY_OLLAMA_BUILDER_MODEL        — model for the builder role (preferred)
  REMEDY_OLLAMA_MODEL                — fallback if REMEDY_OLLAMA_BUILDER_MODEL is unset
  REMEDY_OLLAMA_HOST                 — Ollama server URL (default: http://localhost:11434)
  REMEDY_OLLAMA_BUILDER_TEMPERATURE  — sampling temperature (optional float, e.g. 0.3)
  REMEDY_OLLAMA_BUILDER_NUM_PREDICT  — max tokens to generate (optional int)

Precedence for model selection:
  1. Constructor argument `model`
  2. REMEDY_OLLAMA_BUILDER_MODEL
  3. REMEDY_OLLAMA_MODEL
  4. Built-in default (qwen3-coder-next)

The `ollama` Python package is required at runtime but is NOT a hard dependency
of the remedy package. Install it separately:
  pip install ollama
or:
  pip install 'remedy[ollama]'
"""

from __future__ import annotations

import os

from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext

_DEFAULT_MODEL = "qwen3-coder-next"
_DEFAULT_HOST = "http://localhost:11434"

_SYSTEM_PROMPT = """\
You are a software builder assistant. Given a task execution context, produce a structured result.

Rules:
- summary: short paragraph describing what was done or planned for this task
- proposed_changes: non-empty list of concrete changes or actions; at least one item is required \
(e.g. "Write function foo in bar.py", "Add test for edge case X")
- notes: optional list of assumptions or observations
- risks: optional list of potential issues or blockers

Respond only with valid JSON matching the requested schema. No markdown, no extra text.\
"""


def _resolve_model(override: str | None) -> str:
    """Resolve model with role-specific precedence.

    Order: constructor arg > REMEDY_OLLAMA_BUILDER_MODEL > REMEDY_OLLAMA_MODEL > default.
    """
    if override:
        return override
    builder_model = os.environ.get("REMEDY_OLLAMA_BUILDER_MODEL")
    if builder_model:
        return builder_model
    generic_model = os.environ.get("REMEDY_OLLAMA_MODEL")
    if generic_model:
        return generic_model
    return _DEFAULT_MODEL


def _parse_float_env(var: str) -> float | None:
    """Parse a float environment variable, raising ValueError with the var name on failure."""
    val = os.environ.get(var)
    if val is None:
        return None
    try:
        return float(val)
    except ValueError:
        raise ValueError(
            f"Environment variable {var} must be a float (got {val!r})"
        )


def _parse_int_env(var: str) -> int | None:
    """Parse an integer environment variable, raising ValueError with the var name on failure."""
    val = os.environ.get(var)
    if val is None:
        return None
    try:
        return int(val)
    except ValueError:
        raise ValueError(
            f"Environment variable {var} must be an integer (got {val!r})"
        )


def _build_user_message(context: TaskExecutionContext) -> str:
    """Compose the user message from the execution context."""
    parts: list[str] = []

    if context.job_prompt:
        parts.append(f"Job description: {context.job_prompt}")
        parts.append("")

    if context.planning_summary:
        parts.append(f"Planning context: {context.planning_summary}")
        parts.append("")

    parts.append(f"Task type: {context.task_type}")
    parts.append(f"Task: {context.task_description}")

    if context.prior_task_summaries:
        parts.append("")
        parts.append("Prior completed tasks (for context):")
        for summary in context.prior_task_summaries:
            parts.append(f"  - {summary}")

    return "\n".join(parts)


class OllamaBuilder:
    """Builder provider backed by a local Ollama model.

    Role: builder. Configure via REMEDY_OLLAMA_BUILDER_MODEL and related env vars.

    Usage:
        builder = OllamaBuilder()
        output: BuilderOutput = builder.build(context)
    """

    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
        temperature: float | None = None,
        num_predict: int | None = None,
    ) -> None:
        self.model = _resolve_model(model)
        self.host = host or os.environ.get("REMEDY_OLLAMA_HOST", _DEFAULT_HOST)

        self.temperature: float | None = (
            temperature if temperature is not None
            else _parse_float_env("REMEDY_OLLAMA_BUILDER_TEMPERATURE")
        )
        self.num_predict: int | None = (
            num_predict if num_predict is not None
            else _parse_int_env("REMEDY_OLLAMA_BUILDER_NUM_PREDICT")
        )

    def build(self, context: TaskExecutionContext) -> BuilderOutput:
        """Call Ollama with the execution context and return a validated BuilderOutput.

        Raises:
            ImportError: if the 'ollama' package is not installed.
            ValueError: if a numeric env var has an invalid value.
            ollama.RequestError: if the Ollama server is unreachable.
            ollama.ResponseError: if the model returns an error.
            pydantic.ValidationError: if the response fails schema validation.
        """
        try:
            import ollama
        except ImportError as exc:
            raise ImportError(
                "The 'ollama' package is required for run-next-task-local. "
                "Install with: pip install ollama  or  pip install 'remedy[ollama]'"
            ) from exc

        client = ollama.Client(host=self.host)
        schema = BuilderOutput.model_json_schema()

        options: dict = {}
        if self.temperature is not None:
            options["temperature"] = self.temperature
        if self.num_predict is not None:
            options["num_predict"] = self.num_predict

        response = client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_message(context)},
            ],
            format=schema,
            **({"options": options} if options else {}),
        )

        return BuilderOutput.model_validate_json(response.message.content)
