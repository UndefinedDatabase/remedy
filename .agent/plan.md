# Plan

## Goal
Step 25: Brain Viewer v0 — read-only local static HTML viewer for the Project Brain Graph.

## Prior step
Step 24.3: Brain Smoke Final Polish (1222 tests).

## Status
COMPLETE — 1252 tests pass.

## Steps
1. [x] Create packages/orchestration/brain_viewer.py
   - BrainViewerData frozen dataclass
   - build_brain_viewer_data, export_brain_viewer_json, write_brain_viewer_files
   - _compute_positions (layered radial layout)
   - _render_html + _HTML template (self-contained dark-themed SVG+JS, no external deps)
   - Redaction: same policy as brain_detail.py
2. [x] Add _cmd_brain_view to apps/cli/main.py
   - Validates UUID, loads job, loads events, builds graph/viewer data
   - Writes to REMEDY_DATA_DIR/viewers/<job_id>/
   - Logs brain_viewer_prepared {node_count, edge_count, detail_count, mode}
   - Registers brain-view subparser and dispatch
3. [x] Create tests/test_brain_viewer.py (30 tests)
   - BrainViewerData model, build, export, file writing
   - Redaction hardening: no sentinels in viewer_data.json or index.html
   - _compute_positions: job at centre, layer radii
   - CLI: invalid UUID, job not found, happy path, run-log schema
4. [x] Update docs/architecture.md
   - Brain Viewer v0 section: CLI, run-log event, architecture, v0 constraints
5. [x] Run full suite (1252 pass)
6. [ ] Commit Step 25 changes
7. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
