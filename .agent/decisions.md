# Decisions

## 2026-04-15: Use `typing.Protocol` for interfaces
Protocol-based interfaces (structural subtyping) require no inheritance, keeping core completely decoupled from providers. Any class matching the signature satisfies the contract.

## 2026-04-15: Provider directories are empty stubs
`packages/providers/claude_agent/`, `docker_runtime/`, `mempalace/` exist as empty packages with `__init__.py` only. No implementation until later steps to avoid scope drift.

## 2026-04-15: contracts/ imports from core/ models
Verifier and LLMWorker interfaces need AcceptanceCheck and Task/Artifact types. The contracts package is allowed to depend on core models — both are internal, zero external deps. The dependency flows one way: contracts → core.

## 2026-04-15: LLMWorker.execute takes Task, returns Artifact
Replacing prompt-centric generate(prompt: str) with execute(task: Task) -> Artifact enforces the artifact-driven architecture at the contract level. Raw strings are a provider concern, not an interface concern.

## 2026-04-15: LLMWorker.stream returns AsyncIterator[str]
Streaming full Artifact objects is a more complex problem deferred to a later step. str tokens are kept for now as a pragmatic compromise; this is documented.

## 2026-04-15: Artifact.content kept as str
Binary artifact support (str | bytes) is a non-trivial serialization question. Deferred to Step 2 or later. Documented as a known limitation.

## 2026-04-15: Task.output_artifact_ids is list[UUID]
Task references artifact IDs, not embedded Artifact objects, to avoid circular model issues and keep the models flat.
