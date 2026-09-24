## What

F020 — Node lifecycle & glyph language. Every node of the brain graph now shows its kind and its
state at a glance, drawn from one source. `renderers/glyphPaths.ts` holds each kind's glyph once, as
SVG path data the canvas builds its Path2D from and the legend renders; `renderers/nodeStates.ts`
gives each state one treatment naming design tokens only — fill, glyph ink, halo, size, marks
(the outlined status dot, the strike, the planned ring), pulse. `renderers/paintNode.ts` paints
every non-core node from those two modules through a palette resolved once per mount, and
`ForceBrainGraph.tsx` routes every non-core kind to it. A "Legend" button beside the view toggle
lists every kind and state from the same modules. State changes crossfade over 300 ms, completions
ripple, in-progress nodes pulse, and the canvas asks for no frame while the page is hidden.

## Why

The graph drew every node as the same sphere, with state colours as literals in the renderer. Now
the kind is visible, the state never rests on colour alone, and the canvas and the legend cannot
drift apart because both read one geometry and one state table.

## Key decisions (in `.agent/decisions.md`)

- F020 D1 — one geometry source of SVG path strings; one state table naming tokens only; a new
  `--remedy-state-vetoed` token for the veto's grey.
- F020 D2 — one node painter over a palette resolved once per mount; the glyph ink rule, found by a
  headless render, so a planned node's glyph shows on its white sphere.
- F020 D3 — the legend renders rows enumerated from the modules; a cluster carries its `+n` count;
  the kind-by-state matrix fixture is painted by the live painter.
- F020 D4 — the state crossfade, the completion ripple, the pulse, and the frame rule that stops
  drawing on a hidden page, particles included (measured: 61 frames a second hidden before, 0 after).
- F020 D5 — conformance probes read real pixels of the matrix fixture and judge them against the
  binding spec, not against the table the painter reads.

## How to review

Start with `apps/ui/src/components/graph/renderers/glyphPaths.ts` and `nodeStates.ts`, then
`paintNode.ts`, `palette.ts`, `stateMotion.ts`, `legendModel.ts`, `GraphLegend.tsx` and the changes
to `ForceBrainGraph.tsx`. The Built State of `docs/roadmap/features/T5_F020.md` names the test for
each acceptance line; each round's mutation tool is `.agent/authored/f020-r<n>-mutations.py`, the
conformance harness is `.agent/authored/f020-r5-conformance_*`, and the design-pack gaps F020
filled are the five F020 rows of `docs/ui/design_reference/assumption_log.md`.

## Verification

- The one full suite: `19111 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f020-closure-suite.txt`).
- Conformance: 144 of 144 pixel probes pass in headless Chrome
  (`.agent/authored/f020-r5-conformance.txt`); the harness goes red four ways under its red-proof.
- Evidence job `f020r7e1001` against the fork point `955a6240`: 807 selected tests passed at exit 0,
  the eslint, tsc and vitest nodes among them.
- Review package `remedy-review-20260925-013441-READY_FOR_REVIEW.zip`, SHA-256
  `a069e502d3956af33f4e7dde2ece1dfd47355c68030181dbd5764af6d026d1e0`, READY_FOR_REVIEW.

## Findings and notes

None registered. The one open finding, R-1008, is owned by the next findings paydown, F285. The
reducer is on this feature's do-not-touch list, so no reducer births a prompt, artifact or repair
node yet; the synapse has its glyph, and the prompt dots stay in the simple view.

## Runtime actuals

Eight rounds in one session; reviewer and workers ran as Claude Opus 5.5; wall clock and tokens not
measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
