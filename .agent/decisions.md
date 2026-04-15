# Decisions

## 2026-04-15: Use `typing.Protocol` for interfaces
Protocol-based interfaces (structural subtyping) require no inheritance, keeping core completely decoupled from providers. Any class matching the signature satisfies the contract.

## 2026-04-15: Provider directories are empty stubs
`packages/providers/claude_agent/`, `docker_runtime/`, `mempalace/` exist as empty packages with `__init__.py` only. No implementation until later steps to avoid scope drift.
