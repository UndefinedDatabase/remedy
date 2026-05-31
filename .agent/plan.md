# Plan — Steps 227-246

## Goal
Responsive UI Rescue with Canvas Force Brain Graph.

## Current Step
All steps complete. Ready to commit.

## Steps
- [x] Step 227: Fix UI contract markers (top-metrics-bar, right-live-panel, etc.)
- [x] Step 228: Dependency swap — remove @xyflow/react, add react-force-graph-2d + d3-force
- [x] Step 229: Responsive shell layout (CSS grid + clamp, no fixed 1678×926 frame)
- [x] Step 230: Single left rail, no duplicate menus, no default LayerSwitcher
- [x] Steps 231-238: Force brain graph (Canvas, seeded topology, glow nodes, curved links)
- [x] Steps 239-242: Size/density pass, responsive panels, better labels
- [x] Steps 243-244: remedy ui start contract + served smoke validation
- [x] Steps 245-246: Cleanup legacy, TypeScript passes, final build clean

## Test Results
- 112 tests passed (test_steps_172_201 + test_steps_208_226), 0 failed
- TypeScript: clean (no errors)
- Build: 1.86s, 514 kB JS, 15 kB CSS
- All bundle markers verified
