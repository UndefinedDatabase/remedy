

## Built State (F266, 2026-09-18)

What exists on disk at the close of F266.

**T001 — the bounded comprehension pass.** `packages/orchestration/study.py` walks a repository (bounded by `DEFAULT_MAX_ENTRIES = 2000`, `_walk_repo`), heuristically detects four categories (`STUDY_CATEGORIES = ("structure", "core_modules", "conventions", "entry_points")`), optionally narrates each through an injectable `call_fn` bounded by `max_provider_calls` (default 4) and the existing `should_stop`/`evaluate_budget` machinery, and writes one memory card per category via `store_memory(..., provenance="machine-study")`. `study_call_fn()` bridges the `study` `role_config` role (registered in `role_config.KNOWN_ROLES`, tiered `summarize` in `model_routing.ROLE_TASK_CLASSES`, DECISION F266 D1) to a real callable through `make_structured_call_fn`, honestly returning `None` when no provider is reachable — never crashing.

**T002 — provenance and auto-approval.** `MemoryEntry` (`packages/memory/local_gateway.py`) carries a plain `provenance: str = "human"` field; `store_memory()`'s `approved` parameter, when left `None`, is derived from `provenance` (`True` for `"machine-study"`, `False` otherwise — DECISION F266 D2). Every downstream approval gate reads `.approved` alone and needed no change.

**CLI wiring.** `apps/cli/commands/study_cmd.py` exposes `study.run` (`remedy study run`), registered as an advanced/internal group (`user_facing=False`, DECISION F266 D3) in `apps/cli/command_catalog.py`, wired into `collect_all_handlers()`, and proven reachable through the real CLI dispatch (`tests/cli/test_study_cmd.py::TestStudyCommandReachability`). It resolves its project scope the same way `teacher ask` does (`resolve_scope(project_flag=project, all_projects=False, cwd=target)`), so both commands agree on a repository's registered project id.

**T003 — the three-step, end to end.** `apps/cli/commands/teacher_cmd.py::_cmd_teacher_ask` fetches every `machine-study` card for the resolved project, deduplicates by key keeping the newest value, and renders them as a `[study]` grounding-source block (`packages/orchestration/teacher_qa.py`'s `SOURCE_STUDY`, fourth in `GROUNDING_SOURCES`). `tests/cli/test_study_teacher_e2e.py` proves the full `init` → `study run` → `teacher ask` chain against a foreign repository fixture carrying a distinctive marker directory name, asserting the model is shown that name only through the `study:structure` card it wrote — the Acceptance criterion "answered ... from `study` cards, proved by a fixture whose answer is only derivable from a card."

**Findings.** R-0958 (dotfile mangling), R-0959 (dispatch reachability) and R-0960 (project-scope mismatch) were raised and resolved within the feature. R-0961 (an undersized subprocess timeout in R-0959's own reachability test, exposed by this environment's real, reachable local Ollama) was raised and resolved in round 7.
