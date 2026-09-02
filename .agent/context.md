# Context — F109 Semantic dedupe

## Active Branch
feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432`.

## Scope
F109 (Tier 3, depends on F105 and F106 — both done): within a RESUMED
session, segments whose hash already went to that exact session are
replaced by short reference markers, and only there. The scope rule binds
every round: resumed session only, proven sends only. Task slicing: T001
the sent-index (record at finalization, persist, invalidate on fallback)
plus unit tests; T002 the composition hook, the markers and the scope
guards plus fake-provider chain tests; T003 the measurement fixture, the
disable flag and the docs.

## Do not touch
Cross-session caching, provider-side cache mechanics, and prompt CONTENT —
all explicitly out of scope per `docs/roadmap/features/T3_F109.md` Do not
touch. Segment ranks and composition ORDER stay exactly as F105 set them:
dedupe replaces a segment's text, never its position, because the ordering
is what the provider cache hits.

## Assumptions
- F105 owns `packages/orchestration/prompt_segments.py` and already hashes
  every composed segment into a manifest row, so F109 is bookkeeping over
  those hashes and introduces no second hashing scheme.
- F106 owns the provider resume surface — `supports_resume`,
  `resume_used`, `resume_session_ref` — and F109 reads that session
  reference without widening it.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- No round of F109 gates on `ruff`: this session's reviewer cannot execute
  it, so such a gate would rest on the worker's word alone. The new files
  follow the repository's ruff configuration by construction instead.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for this round lives in the `## Current Step`
section of `.agent/plan.md`. This file deliberately does not restate it.
