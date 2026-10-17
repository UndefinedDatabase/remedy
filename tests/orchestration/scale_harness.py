"""A counting fake planner service and disposable repositories for the scale matrix (version 1).

The planner is faked at the PROVIDER seam (`OllamaPlanner` and the reachability probe), so the real
`make_structured_call_fn` runs, including the order ledger's recording wrapper. Every call is kept
with the schema it was bound to, which names why it was made. No test here reaches a network, a
real model or a host path: repositories are created under the caller's `tmp_path`.
"""
from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HARNESS_VERSION = 1


@dataclass
class FakePlannerService:
    """Answers each structured planner call with a minimal valid document and counts it."""

    #: The file the fake task plan and mission plan name; "" names none.
    target: str = ""
    #: Raise this on every call (a provider failure), or only on the schemas in *fail_schemas*.
    error: Exception | None = None
    fail_schemas: tuple[str, ...] = ()
    #: Seconds each answer takes (never slept; added to the recorded elapsed time only).
    calls: list[dict[str, Any]] = field(default_factory=list)
    #: Each call's prompt, in call order, for the tests that read what the planner was shown.
    prompts: list[str] = field(default_factory=list)

    def answer(self, schema_title: str, prompt: str) -> str:
        began = time.monotonic()
        self.calls.append({"schema": schema_title, "prompt_chars": len(prompt)})
        self.prompts.append(prompt)
        if self.error is not None and (not self.fail_schemas or schema_title in self.fail_schemas):
            self.calls[-1]["error"] = type(self.error).__name__
            raise self.error
        hint = [self.target] if self.target else []
        documents = {
            "JobIntake": {"schema_v": "ji1", "goal": "Test goal.", "context_refs": [],
                          "constraints": [], "acceptance_hints": [], "truncated_input": False,
                          "clarifications": []},
            "TaskPlan": {"schema_v": "task_plan_v1", "risks": [], "tasks": [{
                "id": "T001", "title": f"Change {self.target or 'the code'}", "goal": "Do the change.",
                "acceptance": ["It is done."], "depends_on": [], "est_tokens_band": "S",
                "files_hint": hint}]},
            "MissionPlanDraft": {"schema_v": "mission_plan_draft_v1", "risks": [], "assumptions": [],
                                 "milestones": [{"id": "M001", "goal": "The change is made.",
                                                 "depends_on": [], "rationale": "",
                                                 "jobs_draft": [{"title": "Make the change",
                                                                 "goal": "Make the change.",
                                                                 "est_band": "S"}]}]},
            "StudyCategoryNarration": {"narrative": "A small project."},
        }
        self.calls[-1]["seconds"] = round(time.monotonic() - began, 6)
        return json.dumps(documents[schema_title])

    def count(self, schema: str | None = None) -> int:
        return sum(1 for call in self.calls if schema in (None, call["schema"]))

    def by_schema(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for call in self.calls:
            out[call["schema"]] = out.get(call["schema"], 0) + 1
        return out

    def install(self, monkeypatch) -> FakePlannerService:
        service = self

        class _FakePlanner:
            host = "http://fake.invalid"
            model = "fake-planner"

            def __init__(self, *args: Any, **kwargs: Any) -> None:
                pass

            def raw_call(self, prompt: str, *, schema: dict[str, Any]) -> str:
                return service.answer(str(schema.get("title")), prompt)

        class _FakeClient:
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                pass

            def list(self) -> dict[str, Any]:
                return {"models": []}

        import ollama

        monkeypatch.setattr("packages.providers.ollama_planner.provider.OllamaPlanner", _FakePlanner)
        monkeypatch.setattr(ollama, "Client", _FakeClient)
        return service


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=t", "-c", "commit.gpgsign=false",
         *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def commit_repository(root: Path, files: dict[str, str]) -> Path:
    """A git repository at *root* holding *files* in one commit."""
    root.mkdir(parents=True)
    git(root, "init", "-q")
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "init")
    return root.resolve()


def filler_files(count: int, *, per_dir: int = 50, suffix: str = ".py", body: str = "x = 1\n") -> dict[str, str]:
    """*count* small files spread over directories, for repositories of a given size class."""
    return {f"pkg{n // per_dir:03d}/mod{n}{suffix}": body for n in range(count)}
