"""
Ollama-backed planner provider.

Calls a local Ollama instance with structured output (JSON schema enforcement)
to produce a validated PlannerOutput.

Configuration (environment variables):
  REMEDY_OLLAMA_PLANNER_MODEL        — model for the planner role (preferred)
  REMEDY_OLLAMA_MODEL                — fallback if REMEDY_OLLAMA_PLANNER_MODEL is unset
                                       (kept for backward compatibility)
  REMEDY_OLLAMA_HOST                 — Ollama server URL (default: http://localhost:11434)
  REMEDY_OLLAMA_PLANNER_TEMPERATURE  — sampling temperature (optional float, e.g. 0.2)
  REMEDY_OLLAMA_PLANNER_NUM_PREDICT  — max tokens to generate (optional int)

Precedence for model selection:
  1. Constructor argument `model`
  2. REMEDY_OLLAMA_PLANNER_MODEL
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

from packages.orchestration.planner_models import PlannerOutput

_DEFAULT_MODEL = "qwen3-coder-next"
_DEFAULT_HOST = "http://localhost:11434"

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


def _resolve_model(override: str | None) -> str:
    """Resolve model with role-specific precedence.

    Order: constructor arg > REMEDY_OLLAMA_PLANNER_MODEL > REMEDY_OLLAMA_MODEL > default.
    """
    if override:
        return override
    planner_model = os.environ.get("REMEDY_OLLAMA_PLANNER_MODEL")
    if planner_model:
        return planner_model
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


class OllamaPlanner:
    """Planner provider backed by a local Ollama model.

    Role: planner. Configure via REMEDY_OLLAMA_PLANNER_MODEL and related env vars.

    Usage:
        planner = OllamaPlanner()
        output: PlannerOutput = planner.plan("build a CLI tool that summarises files")
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
            else _parse_float_env("REMEDY_OLLAMA_PLANNER_TEMPERATURE")
        )
        self.num_predict: int | None = (
            num_predict if num_predict is not None
            else _parse_int_env("REMEDY_OLLAMA_PLANNER_NUM_PREDICT")
        )

    def plan(self, prompt: str) -> PlannerOutput:
        """Call Ollama and return a validated PlannerOutput.

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
                "The 'ollama' package is required for plan-job-local. "
                "Install with: pip install ollama  or  pip install 'remedy[ollama]'"
            ) from exc

        client = ollama.Client(host=self.host)
        schema = PlannerOutput.model_json_schema()

        options: dict = {}
        if self.temperature is not None:
            options["temperature"] = self.temperature
        if self.num_predict is not None:
            options["num_predict"] = self.num_predict

        response = client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Plan this job:\n\n{prompt}"},
            ],
            format=schema,
            **({"options": options} if options else {}),
        )

        return PlannerOutput.model_validate_json(response.message.content)
