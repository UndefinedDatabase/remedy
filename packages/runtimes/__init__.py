"""
packages.runtimes — Reserved namespace for Remedy pluggable execution runtimes.

Planned purpose:
    Runtime provider abstraction: sandboxed containers, remote environments,
    and cloud execution targets beyond the local workspace runtime.
    Will expose a common Runtime protocol consumed by orchestration.

Current status:
    Reserved namespace — no implementation in this step.
    The only concrete runtime is LocalWorkspaceRuntime in
    packages.orchestration.workspace.

Future layer:
    Pluggable runtime backends — Docker, cloud, or MCP-connected environments
    (planned Step 36+).
"""
