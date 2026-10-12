"""The construction of a role's provider (DECISION F058 D2).

The body below moved unchanged out of `packages/orchestration/pingpong_loop.py`, whose
`_create_provider_with_cwd` stays there as a shim that calls `create_role_provider` below,
passing `pingpong_loop`'s own `create_provider` at every call, so a test that replaces
`pingpong_loop.create_provider` still reaches every provider a run builds.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from packages.orchestration.model_failover import FailoverLink, FailoverProvider, resolve_failover_chains
from packages.orchestration.pingpong_provider import ClaudeCliProvider, PingPongProvider, create_provider


# WHY: the seam where a run builds a role's provider, so DECISION F058 D2's failover walk can wrap it.
def create_role_provider(
    name: str,
    *,
    role: str,
    staging_dir: str | None,
    write_mode: str = "none",
    model: str = "",
    stream_evidence: bool = False,
    stream_evidence_dir: str | None = None,
    make_provider: Callable[..., PingPongProvider] = create_provider,
    with_failover: bool = True,
) -> PingPongProvider:
    """Create provider with role-appropriate cwd and write mode.

    Builder claude-cli gets cwd=staging_dir and write_mode from CLI.
    Reviewer claude-cli gets cwd=staging_dir and write_mode="none": it stays
    read-only, but its cwd is pinned to the disposable staging dir so stray
    cwd writes cannot pollute the repo root.

    ``stream_evidence`` is the opt-in F004 mode; when off the provider keeps the
    accepted F003 JSON behaviour. Each role writes its stream artifacts into its
    own subdirectory so builder and reviewer streams never overwrite each other.
    ``make_provider`` builds the final non-claude-cli provider by name; a caller — such as the
    failover walk — may replace it with a wrapper around the provider it would otherwise build.
    ``with_failover`` wraps the built provider in the DECISION F058 D2 walk when `role`'s
    configured chain is not empty; a link built mid-walk passes ``with_failover=False``, so a
    chain never nests a failover walk inside another.
    """
    if name == "claude-cli":
        stream_dir = None
        rel_prefix = ""
        if stream_evidence and stream_evidence_dir:
            rel_prefix = f"streams/{role}"
            stream_dir = str(Path(stream_evidence_dir) / "streams" / role)
        common = {
            "cwd": staging_dir,
            "model": model,
            "stream_evidence": stream_evidence,
            "stream_evidence_dir": stream_dir,
            "stream_rel_prefix": rel_prefix,
        }
        if role == "builder" and staging_dir:
            provider: PingPongProvider = ClaudeCliProvider(write_mode=write_mode, **common)
        else:
            provider = ClaudeCliProvider(**common)
    else:
        provider = make_provider(name, model=model)

    if not with_failover:
        return provider
    chain = resolve_failover_chains().get(role, ())
    if not chain:
        return provider

    def build_link(link: FailoverLink) -> PingPongProvider:
        return create_role_provider(
            link.provider,
            role=role,
            staging_dir=staging_dir,
            write_mode=write_mode,
            model=link.model,
            stream_evidence=stream_evidence,
            stream_evidence_dir=stream_evidence_dir,
            make_provider=make_provider,
            with_failover=False,
        )

    return FailoverProvider(
        provider,
        role=role,
        intended_provider=name,
        intended_model=model,
        links=chain,
        build_link=build_link,
    )
