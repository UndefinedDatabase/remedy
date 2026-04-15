# Context

## Active Branch
`feature/remedy-foundation`

## Scope
Step 1 of Remedy: foundation skeleton only.

## Constraints
- No orchestration logic
- No agent loops
- No provider implementations (Claude, Docker, MemPalace)
- No complex abstractions
- Strict modularity: core must not depend on providers
- Pydantic for models, typing.Protocol for interfaces

## Assumptions
- Python project; no build tooling configured yet in this step
- `packages/` contains library modules, not installable packages yet
- `__init__.py` files added to make directories importable as packages
- No providers are implemented yet; stubs exist as empty packages only
