"""
Core contracts (Protocol interfaces) for Remedy.

These define the boundaries between the kernel and external providers.
No implementation, no external dependencies, no assumptions about any specific system.
Any conforming class satisfies the contract via structural subtyping.
"""

from __future__ import annotations

from typing import Any, AsyncIterator, Protocol, runtime_checkable


@runtime_checkable
class LLMWorker(Protocol):
    """Generates text or structured output from a prompt."""

    async def generate(
        self,
        prompt: str,
        *,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Return generated text for the given prompt."""
        ...

    async def stream(
        self,
        prompt: str,
        *,
        context: dict[str, Any] | None = None,
    ) -> AsyncIterator[str]:
        """Stream generated text tokens for the given prompt."""
        ...


@runtime_checkable
class MemoryGateway(Protocol):
    """Read and write named memory entries."""

    async def read(self, key: str) -> Any:
        """Retrieve a stored value by key. Returns None if not found."""
        ...

    async def write(self, key: str, value: Any) -> None:
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
    """Checks whether an artifact or result satisfies acceptance criteria."""

    async def verify(
        self,
        artifact: Any,
        checks: list[Any],
    ) -> tuple[bool, list[str]]:
        """
        Run acceptance checks against an artifact.

        Returns (passed, list_of_failure_messages).
        """
        ...
