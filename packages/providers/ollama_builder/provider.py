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
from dataclasses import dataclass

from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext

_DEFAULT_MODEL = "qwen3-coder-next"
_DEFAULT_HOST = "http://localhost:11434"

_SYSTEM_PROMPT = """\
You are a software builder assistant. Given a task execution context, produce a structured result.

Output fields:
- summary: one short paragraph describing what was done or planned
- proposed_changes: list of concrete changes (e.g. "Write function foo in bar.py")
- notes: optional list of assumptions or observations
- risks: optional list of potential issues
- structured_patch_text: for code changes, a JSON string with this exact schema:
  {"file_ops": [{"path": "relative/path.py", "action": "create"|"modify"|"delete", "content": "full file content"}]}
- structured_patch_format: "json" when structured_patch_text has file_ops, "none" otherwise

Strict rules for structured_patch_text:
- Use relative paths only (no leading / or ..)
- One JSON object only, no wrapper text around it
- "content" must be the complete file content, not a diff
- Do not include shell commands (rm, sudo, curl, wget, chmod)
- Do not target .env, .pem, .key, or binary files
- If the task does not require code changes, set structured_patch_text to null

Respond only with valid JSON matching the requested schema. No markdown fencing, no prose outside the JSON.\
"""


@dataclass
class PromptProfile:
    """A named set of builder instructions.

    Each profile produces different system prompt text for the same task,
    allowing controlled comparison of model behavior.
    """

    name: str
    purpose: str
    system_text: str
    safety_rules: list[str]


@dataclass
class PromptProfileMetadata:
    """Safe metadata about which profile was used. No raw prompt content."""

    name: str
    purpose: str
    prompt_hash: str
    prompt_length: int


def _hash_text(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()[:16]


PROMPT_PROFILES: dict[str, PromptProfile] = {
    "strict_minimal": PromptProfile(
        name="strict_minimal",
        purpose="Shortest strict patch instruction — minimal context, maximum constraint",
        system_text=(
            "You are a code builder. Output valid JSON only.\n\n"
            "Schema: {\"file_ops\": [{\"path\": \"relative/file.py\", "
            "\"action\": \"create\"|\"modify\"|\"delete\", \"content\": \"full file content\"}]}\n\n"
            "Rules:\n"
            "- Relative paths only, no / or .. prefix\n"
            "- Complete file content, not diffs\n"
            "- No shell commands, no .env/.pem/.key files\n"
            "- No markdown, no prose, no explanation outside JSON\n"
            "- If no code change needed, set structured_patch_text to null\n"
        ),
        safety_rules=[
            "relative paths only",
            "no shell commands",
            "no secret files",
            "no prose outside JSON",
        ],
    ),
    "repair_aware": PromptProfile(
        name="repair_aware",
        purpose="Includes test failure and repair guidance for iterative fixing",
        system_text=(
            "You are a code builder that fixes failing tests.\n\n"
            "Schema: {\"file_ops\": [{\"path\": \"relative/file.py\", "
            "\"action\": \"create\"|\"modify\"|\"delete\", \"content\": \"full file content\"}]}\n\n"
            "Rules:\n"
            "- Relative paths only, no / or .. prefix\n"
            "- Complete file content, not diffs\n"
            "- No shell commands, no .env/.pem/.key files\n"
            "- No markdown, no prose, no explanation outside JSON\n"
            "- If no code change needed, set structured_patch_text to null\n\n"
            "Repair guidance:\n"
            "- Read the test expectations carefully\n"
            "- Fix the root cause, not just the symptom\n"
            "- If tests import a missing function, add that function\n"
            "- If a return value is wrong, fix the return statement\n"
            "- Do not change test files unless the task says to\n"
        ),
        safety_rules=[
            "relative paths only",
            "no shell commands",
            "no secret files",
            "no prose outside JSON",
            "fix root cause",
            "do not change test files",
        ],
    ),
    "context_rich": PromptProfile(
        name="context_rich",
        purpose="Full context with file summary, test summary, and detailed output rules",
        system_text=_SYSTEM_PROMPT,
        safety_rules=[
            "relative paths only",
            "no shell commands",
            "no secret files",
            "no prose outside JSON",
            "one JSON object only",
            "complete file content not diff",
        ],
    ),
}


def get_prompt_profile(name: str) -> PromptProfile:
    """Get a prompt profile by name. Falls back to context_rich."""
    return PROMPT_PROFILES.get(name, PROMPT_PROFILES["context_rich"])


def get_prompt_profile_metadata(profile: PromptProfile) -> PromptProfileMetadata:
    """Extract safe metadata from a profile. No raw prompt text."""
    return PromptProfileMetadata(
        name=profile.name,
        purpose=profile.purpose,
        prompt_hash=_hash_text(profile.system_text),
        prompt_length=len(profile.system_text),
    )


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

    if context.memory_context:
        parts.append("")
        parts.append(context.memory_context)

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
        prompt_profile: str | None = None,
    ) -> None:
        self.model = _resolve_model(model)
        self.host = host or os.environ.get("REMEDY_OLLAMA_HOST", _DEFAULT_HOST)
        self.prompt_profile_name = prompt_profile or "context_rich"
        self.prompt_profile = get_prompt_profile(self.prompt_profile_name)

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
                {"role": "system", "content": self.prompt_profile.system_text},
                {"role": "user", "content": _build_user_message(context)},
            ],
            format=schema,
            **({"options": options} if options else {}),
        )

        return BuilderOutput.model_validate_json(response.message.content)
