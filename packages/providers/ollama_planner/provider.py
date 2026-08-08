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

from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.planner_models import PlannerOutput

#: This provider's built-in default model. Resolved from the single alias table
#: (packages/orchestration/model_aliases.py) so no concrete model id is spelled
#: out here; an upgrade repoints the alias, not this file.
_DEFAULT_MODEL = resolve_model_alias("ollama-default")
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

    Env vars checked directly (always fresh) for backward compatibility.
    TOML config checked via config system as fallback.
    Order: constructor arg > env vars > TOML config > built-in default.
    """
    if override:
        return override
    import os

    planner_model = os.environ.get("REMEDY_OLLAMA_PLANNER_MODEL")
    if planner_model:
        return planner_model
    generic_model = os.environ.get("REMEDY_OLLAMA_MODEL")
    if generic_model:
        return generic_model
    from packages.orchestration.config import get_config

    configured = get_config().get("ollama.planner.model")
    if configured:
        return configured
    return _DEFAULT_MODEL


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
        import os

        from packages.orchestration.config import get_config

        cfg = get_config()
        self.model = _resolve_model(model)
        self.host = host or os.environ.get("REMEDY_OLLAMA_HOST") or cfg.get("ollama.host") or _DEFAULT_HOST

        env_temp = os.environ.get("REMEDY_OLLAMA_PLANNER_TEMPERATURE")
        if temperature is not None:
            self.temperature: float | None = temperature
        elif env_temp is not None:
            try:
                self.temperature = float(env_temp)
            except ValueError:
                raise ValueError(
                    f"Environment variable REMEDY_OLLAMA_PLANNER_TEMPERATURE must be a float (got {env_temp!r})"
                )
        else:
            self.temperature = cfg.get("ollama.planner.temperature")

        env_num = os.environ.get("REMEDY_OLLAMA_PLANNER_NUM_PREDICT")
        if num_predict is not None:
            self.num_predict: int | None = num_predict
        elif env_num is not None:
            try:
                self.num_predict = int(env_num)
            except ValueError:
                raise ValueError(
                    f"Environment variable REMEDY_OLLAMA_PLANNER_NUM_PREDICT must be an integer (got {env_num!r})"
                )
        else:
            self.num_predict = cfg.get("ollama.planner.num_predict")

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

    def raw_call(self, prompt: str, *, schema: dict, system: str | None = None) -> str:
        """Send a prompt to Ollama with native schema enforcement, return raw text.

        No validation — caller is responsible for parsing.  Uses the planner's
        resolved host, model, temperature, and num_predict so there is a single
        configuration surface for all Ollama calls.
        """
        try:
            import ollama
        except ImportError as exc:
            raise ImportError(
                "The 'ollama' package is required for plan-job-local. "
                "Install with: pip install ollama  or  pip install 'remedy[ollama]'"
            ) from exc

        client = ollama.Client(host=self.host)
        options: dict = {}
        if self.temperature is not None:
            options["temperature"] = self.temperature
        if self.num_predict is not None:
            options["num_predict"] = self.num_predict

        messages: list[dict[str, str]] = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = client.chat(
            model=self.model,
            messages=messages,
            format=schema,
            **({"options": options} if options else {}),
        )
        return response.message.content

    def plan_raw(self, prompt: str, *, schema: dict) -> str:
        """F005 native structured call: return the raw Ollama response text.

        Delegates to raw_call with the planner system prompt and "Plan this job:"
        wrapping.
        """
        return self.raw_call(
            f"Plan this job:\n\n{prompt}",
            schema=schema,
            system=_SYSTEM_PROMPT,
        )
