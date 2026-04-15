# Context

## Active Branch
`feature/foundation-hardening`

## Scope
Step 1.5: Harden foundation contracts and models before Step 2.

## Constraints
- No orchestration logic
- No provider implementations
- No agent loops
- contracts/ may import from core/ (internal dependency, no external packages)
- Keep changes minimal and focused — no speculative abstractions

## Assumptions
- Artifact.content remains str-only; documented as a limitation for Step 2 consideration
- LLMWorker.execute returns Artifact (artifact-driven architecture)
- LLMWorker.stream returns AsyncIterator[str] (streaming full Artifacts is out of scope here)
- packages/memory/ and packages/runtimes/ are provider-agnostic internal layers
- packages/providers/* are concrete external adapters only
