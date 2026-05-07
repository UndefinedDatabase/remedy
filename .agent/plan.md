# Plan

## Goal
Step 25.1: Brain Viewer v0 robustness polish + future architecture hooks.

## Prior step
Step 25: Brain Viewer v0 (1252 tests).

## Status
COMPLETE — 1268 tests pass.

## Steps
1. [x] Guard constitution loading in _cmd_brain_view
   - Check path exists/is-dir before loading; catch unexpected exceptions
   - Continue with constitution=None on stale/missing/inaccessible repo
   - Print safe "Warning: project constitution unavailable for viewer." to stderr
   - No raw exception text anywhere
2. [x] Add detail_fallback_count to BrainViewerData
   - detail_fallback_count: int = 0 (frozen dataclass field with default)
   - Increment when fallback detail is used in build_brain_viewer_data
   - Include in export_brain_viewer_json output
   - Include in brain_viewer_prepared run-log metadata
   - New exact schema: {node_count, edge_count, detail_count, detail_fallback_count, mode}
3. [x] Update tests/test_brain_viewer.py (46 tests)
   - Updated _VIEWER_JSON_KEYS and _BRAIN_VIEWER_PREPARED_METADATA_KEYS constants
   - Added _poisoned_events() with event.message + metadata.command_output sentinels
   - TestDetailFallbackCount: happy path 0, forced failure increments, export includes key
   - TestConstitutionGuard: stale repo no crash, generates HTML, safe warning only, no traceback, no-repo works
   - TestBrainViewerRedaction: updated to include poisoned events; event sentinel tests; CLI sentinel tests
   - TestBrainViewCli: detail_fallback_count schema test added
4. [x] Update docs/architecture.md
   - Brain Viewer v0 section: constitution advisory, detail_fallback_count as health signal
   - Future Brain Hierarchy section: Job/Repo/Project/Global layers
   - Future Context Collector section
   - Future "Continue from Node" section
5. [x] Run full suite (1268 pass)
6. [ ] Commit Step 25.1 changes
7. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
