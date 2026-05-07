# Plan

## Goal
Step 26.5: Brain Viewer loading diagnostics and no-infinite-spinner hardening.

## Prior step
Step 26.2: Smoke viewer LAN URL and Context Coverage test polish (1356 tests).

## Status
COMPLETE — 1377 tests pass.

## Steps
1. [x] Update brain_viewer.py HTML template
   - body data-render-status="loading" initial state
   - #render-badge in header (loading → ready/empty/error)
   - #err-panel (hidden by default, shown on JS error)
   - #diag bar: nodes, edges, details, fallbacks, selected, status
   - Global _vErr(cat, msg) + window.onerror
   - IIFE wrapped in try/catch; setRenderStatus inside IIFE
   - #diag-sel updated on node pick
   - setRenderStatus('ready'|'empty') at end of successful init
2. [x] Add TestBrainViewerDiagnostics in test_brain_viewer.py (21 tests)
   - status element, render-badge, error-panel, err-msg
   - all 6 diag-* elements
   - JS try/catch, catch clause, _vErr, window.onerror, setRenderStatus
   - regression: viewer_data.json valid, sentinels absent, schema unchanged, fallback count
3. [x] Update docs/architecture.md
   - Loading diagnostics and failure handling section (Step 26.5)
   - Status table: ready/empty/error conditions
   - #diag bar fields description
4. [x] Run full suite (1377 pass)
5. [ ] Commit Step 26.5 changes

## Branch
feature/step21-project-constitution-v1
