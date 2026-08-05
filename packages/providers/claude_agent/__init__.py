"""
packages.providers.claude_agent — Reserved namespace for Claude Agent SDK provider.

Planned purpose:
    Builder and planner implementations backed by the Claude Agent SDK
    (claude_agent_sdk).  Will replace or complement the current Ollama-based
    local provider with Anthropic-hosted models.

Current status:
    Reserved namespace — no implementation yet.  Active providers are in
    packages.providers.ollama_builder and packages.providers.ollama_planner.
    The live Claude path today is the ``claude -p`` subprocess provider in
    packages.orchestration.pingpong_provider.

Roadmap:
    Provider work lands with the Tier 2/3 economy features
    (docs/roadmap/STATUS.md).
"""
