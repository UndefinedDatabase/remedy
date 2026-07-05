# Motion Specification

Principles: motion explains causality, never decorates idle time; one thing
moves at a time (max 3 staggered births); everything survives reduced-motion.

| Name | Duration | Easing | Used by |
|---|---|---|---|
| hover/press | --remedy-dur-fast 120ms | ease-standard | chips, buttons, rows |
| surface fade/lift | --remedy-dur-base 220ms | ease-soft | cards, popover, dropdown |
| progress/layout | --remedy-dur-slow 350ms | ease-standard | progress bar, panel resize |
| node birth | --remedy-dur-birth 420ms | ease-soft (spring feel) | graph births + edge draw-in |
| completion ripple | 300ms | ease-out | done transition ring |
| active pulse | --remedy-dur-pulse 1600ms loop | sine | in_progress nodes, LIVE dot |
| core breath | 3200ms loop | sine | job core halo |
| particle traversal | --remedy-dur-particle 2400ms | linear | active edges (estimated) |
| skeleton shimmer | 1200ms loop | ease-in-out | loading states |

Rules: no infinite motion outside pulse/breath/particles; pulses pause when
tab hidden (rAF naturally stops — do not setInterval); crossfade content
changes ≥ replace jumps; scroll-linked motion forbidden. Reduced motion: table
column collapses to fade 180ms / none per ux_spec §16; the global CSS kill in
`globals.css` stays as the safety net, components must ALSO behave (canvas
ignores CSS — renderer reads the media query, pattern exists in
`ForceBrainGraph.tsx:10`).
