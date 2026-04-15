"""
Core contracts (Protocol interfaces) for Remedy.

These define the boundaries between the kernel and external providers.
No implementation, no external dependencies beyond core models.
Any conforming class satisfies the contract via structural subtyping.
"""

from __future__ import annotations

from typing import AsyncIterator, Protocol, runtime_checkable

from packages.core.models import AcceptanceCheck, Artifact, Task


@runtime_checkable
class LLMWorker(Protocol):
    """Executes a Task and produces an Artifact.

    Work flows through structured Task objects, not raw prompt strings.
    No provider-specific assumptions.
    """

    async def execute(self, task: Task) -> Artifact:
        """Execute the task and return the resulting artifact."""
        ...

    async def stream(self, task: Task) -> AsyncIterator[str]:
        """Stream output tokens while executing a task.

        Note: streams str tokens rather than a full Artifact — full streaming
        artifact support is deferred to a later step.
        """
        ...


@runtime_checkable
class MemoryGateway(Protocol):
    """Read and write named memory entries."""

    async def read(self, key: str) -> object:
        """Retrieve a stored value by key. Returns None if not found."""
        ...

    async def write(self, key: str, value: object) -> None:
        """Persist a value under the given key."""
        ...

    async def delete(self, key: str) -> None:
        """Remove a stored entry by key."""
        ...


@runtime_checkable
class RuntimeProvider(Protocol):
    """Executes a command or script in an isolated environment."""

    async def run(
        self,
        command: str,
        *,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> tuple[int, str, str]:
        """
        Execute command.

        Returns (exit_code, stdout, stderr).
        """
        ...


@runtime_checkable
class Verifier(Protocol):
    """Checks whether an artifact satisfies its acceptance criteria."""

    async def verify(
        self,
        artifact: Artifact,
        checks: list[AcceptanceCheck],
    ) -> tuple[bool, list[str]]:
        """
        Run acceptance checks against an artifact.

        Returns (passed, list_of_failure_messages).
        """
        ...
