# Handoff — F266 R1

SESSION 1 of feature F266 · round 1 · rounds so far 1

## Range

Review of `ec520c17`..`c18787a1`.

## Commits

### 159054e9 F266 R1 C1: claim feature, DECISION D1 role wiring design, DECISION D2 provenance design
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | 2 | Claim: `[ ]` → `[~]` on F266 |
| docs/roadmap/features/T4_F266.md | 17 | Add Decisions section summarizing D1, D2 |
| .agent/live_review.md | 53 | Re-head: F280 → F266, update preamble and Steps |
| .agent/plan.md | 52 | Full rewrite: F266 scope, current step, next steps, risks |
| .agent/context.md | 103 | Full rewrite: F266 scope, constraints, assumptions |
| .agent/decisions.md | 32 | Append D1 and D2 full text with rationale |

### 4bd9d17f F266 R1 C2: register study role in role_config and model_routing
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/role_config.py | 7 | Add `study` to KNOWN_ROLES tuple with F266-specific docstring |
| packages/orchestration/model_routing.py | 2 | Add `"study": "summarize"` to ROLE_TASK_CLASSES dict |

### c18787a1 F266 R1 C3: add provenance field and auto-approval to MemoryEntry
| Path | +/- | Reason |
|------|-----|--------|
| packages/memory/models.py | 5 | Add `provenance: str = "human"` field; update `to_json_line()` and `from_dict()` |
| packages/memory/local_gateway.py | 10 | Update `store_memory()` signature and add auto-approval derivation logic |
| tests/test_memory_gateway.py | 35 | Add 4 tests: auto-approval for machine-study, default approval, override behavior, JSON round-trip |

## External actions

`git push -u origin feature/f266-remedy-study` → branch created on origin, tracking set up.

## Verification

**Gate 1 — pytest on model_routing, memory_gateway, project_brain, golden_path:**
```
python3 -m pytest tests/orchestration/test_model_routing.py tests/test_memory_gateway.py tests/test_project_brain.py tests/cli/test_golden_path.py -q

590 passed, 3 skipped, 1 warning in 21.11s
```
Exit code: 0

**Gate 2 — pytest on docs and roadmap_index:**
```
python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q

340 passed in 1.24s
```
Exit code: 0

**Gate 3 — ruff check on touched files:**
```
python3 -m ruff check packages/orchestration/role_config.py packages/orchestration/model_routing.py packages/memory/models.py packages/memory/local_gateway.py

All checks passed!
```
Exit code: 0

**Gate 4 — git status:**
```
git status --porcelain
```
(empty — clean tree)

## Authored-text proofs

Edit 1 (STATUS.md): verified by grep — `[ ]` form does not exist after edit, `[~]` present at line 36.
Edit 2 (live_review.md): verified by reading head — first line is now `# Live Review — F266 remedy study`.
Edit 3 (plan.md): verified by line count (40 lines) and head — under 50-line cap, correct heading.
Edit 4 (context.md): verified by head — first line is now `# Context — F266 remedy study`.
Edit 5 (decisions.md): verified by grep — two new DECISION entries found.
T4_F266.md Decisions section: verified by grep — section exists.

All edits applied without corruption and match intent per DECISION text.

## Deviations & assumptions

None. The round was executed exactly as specified in the block: C1 claims the feature and settles T002's design first (per Orchestrator brief), C2 wires the role, C3 adds the provenance field and auto-approval. No unrelated changes. No scope drift. Gates run once each, all green.

## Next

T001 — the bounded comprehension pass (structure, core modules, conventions, entry points), calling the new `study` role and stopping at its budget cap with an honest partial result. After T001 completes: CLI wiring for a standalone `study` command. After that: T003 — the three-step proved end to end against a foreign repository fixture (including the new memory-card grounding source for `teacher ask`). Finally: closure sequence.
