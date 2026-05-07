# Plan

## Goal
Step 26: Context Coverage v0 — deterministic, redaction-safe context-health indicator.

## Prior step
Step 25.1: Brain Viewer robustness polish (1268 tests).

## Status
COMPLETE — 1335 tests pass.

## Steps
1. [x] Create packages/orchestration/context_coverage.py
   - ContextCoverageSignal and ContextCoverageSnapshot frozen dataclasses
   - 10 signals, weights sum to 100
   - derive_context_coverage: deterministic, no LLM, no content read
   - project_memory + mcp_tool_context always absent in v0
   - summarize_context_coverage: bar, present/missing sections, meaning, next actions
   - export_context_coverage_json: version 1, exact schema
2. [x] Update packages/orchestration/project_brain.py
   - Add NT_CONTEXT_COVERAGE, ET_HAS_CONTEXT_SNAPSHOT constants
   - Import derive_context_coverage; create node in build_project_brain (section 8)
   - Status: low/partial/strong based on score
   - Metadata: {score, present_signal_count, missing_signal_count, scope}
   - Update _NODE_TYPE_ORDER, _all_types in summarize_project_brain
3. [x] Update packages/orchestration/brain_detail.py
   - Import NT_CONTEXT_COVERAGE
   - Add _detail_context_coverage handler
   - Detail explains meaning, score, counts, "not model confidence"
4. [x] Update packages/orchestration/brain_viewer.py
   - Add "context_coverage": 1 to _LAYER_MAP
   - Add ctx-badge span in HTML header
   - JS populates badge from context_coverage node metadata.score
5. [x] Update apps/cli/main.py
   - Add _cmd_context: loads job, events, constitution; derives and renders coverage
   - Logs context_coverage_inspected: {score, present_signal_count, missing_signal_count, scope}
   - Registers context subparser with --json flag; dispatch
6. [x] Create tests/test_context_coverage.py (67 tests)
   - All 10 signal detection paths
   - Score math, clamping, weights summing to 100
   - Redaction: no sentinel in summary/JSON/detail
   - summarize: header, bar, meaning, not model confidence, next actions, scope
   - export JSON: exact keys, version, serialisable
   - CLI: text/json output, invalid UUID, unknown job, run-log exact schema
   - Brain: node always present, edge, status, label, metadata, brain --json includes it
   - Brain-node detail: 13 keys, explains meaning, correct node_type
   - Brain Viewer: context_coverage in viewer_data.json, ctx-badge in HTML, no sentinels
7. [x] Update docs/architecture.md
   - Context Coverage v0 section
8. [x] Run full suite (1335 pass)
9. [ ] Commit Step 26 changes

## Branch
feature/step21-project-constitution-v1
