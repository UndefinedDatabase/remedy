"""
Ollama-backed planner provider.

Calls a local Ollama instance with structured output (JSON schema enforcement)
to produce a validated PlannerOutput.

Configuration (environment variables):
  REMEDY_OLLAMA_MODEL  — model to use (default: qwen3-coder-next)
  REMEDY_OLLAMA_HOST   — Ollama server URL (default: http://localhost:11434)

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


class OllamaPlanner:
    """Planner provider backed by a local Ollama model.

    Usage:
        planner = OllamaPlanner()
        output: PlannerOutput = planner.plan("build a CLI tool that summarises files")
    """

    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
    ) -> None:
        self.model = model or os.environ.get("REMEDY_OLLAMA_MODEL", _DEFAULT_MODEL)
        self.host = host or os.environ.get("REMEDY_OLLAMA_HOST", _DEFAULT_HOST)

    def plan(self, prompt: str) -> PlannerOutput:
        """Call Ollama and return a validated PlannerOutput.

        Raises:
            ImportError: if the 'ollama' package is not installed.
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

        response = client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Plan this job:\n\n{prompt}"},
            ],
            format=schema,
        )

        return PlannerOutput.model_validate_json(response.message.content)
