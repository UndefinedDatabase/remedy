# Assumption Log — UI Design Deviations

The design reference is binding on visual matters (see the authority chain in
[README.md](README.md)). When a feature cannot follow it for a technical reason,
or has to assume something the reference does not settle, the deviation or
assumption is recorded here, in the same change that ships it. This is the
`assumption_log` every UI feature file and the agent conventions refer to.

An entry does not make a deviation acceptable: the reviewer still rules on it,
and a deviation with no entry here is a review finding.

## Entry format

One row per deviation or assumption, newest last.

| Date | Feature | Surface | Reference says | Shipped instead | Technical reason | Review record |
|------|---------|---------|----------------|-----------------|------------------|---------------|

Column rules:

- **Surface** names the component or file, e.g. `RightLivePanel.module.css`.
- **Reference says** cites the binding source by file and section, e.g.
  `component_spec.md` §4.
- **Technical reason** states why the reference cannot be met; taste is not a
  reason.
- **Review record** names the finding id or DECISION that ruled on the entry.

## Entries

| Date | Feature | Surface | Reference says | Shipped instead | Technical reason | Review record |
|------|---------|---------|----------------|-----------------|------------------|---------------|
| 2026-09-24 | F264 | `ActivityFeedCard.tsx` | `ux_spec.md` §11.3: the input is disabled until steering exists, with the tooltip "Steering arrives with a later feature — watching only for now." | The input is live for a job that can still run. It stays disabled, with a visible reason, in two cases: no job link ("Open a job's dashboard from its own link to steer it.") and an ended job ("This job has ended, so it takes no more steering."). | Steering exists from F264 on, so the reference's sentence became false. The reference gives no wording for the two cases where the input must still be disabled. | DECISION F264 D3 |
| 2026-09-24 | F264 | `ChatInput.tsx` | `ux_spec.md` §11.3 and `component_spec.md` "SteeringInput / ChatInput" do not say what the operator sees after sending. | One line under the input, announced to screen readers, saying what happened to the message. It uses the decision inbox's outcome colours. The typed text is cleared only after the job accepts it. | Without feedback, an operator cannot tell whether the job recorded the message, and is likely to send it again. The reference does not cover this state. | DECISION F264 D3 |
| 2026-09-24 | F264 | `RightLivePanel.module.css` | `ux_spec.md` §14: a 2px `--remedy-focus` outer ring. | A 2px ring in `--remedy-blue-strong`, the colour the other focus rings in this stylesheet already use. | `--remedy-focus` is not defined in the shipped tokens sheet. The guard `TestEveryCustomPropertyResolves` fails on any custom property that is not defined. | DECISION F264 D3 |
| 2026-09-24 | F265 | `LessonsOverlay.tsx` | The reference has no lessons surface. For sheets and dialogs, `tokens.css` puts them on the `--remedy-z-overlay` layer (80), and `component_spec.md` "DetailPopover" asks for a dialog role, a focus trap and Esc to close. | A glass sheet anchored to the right, with a dialog role, a Close button and Esc to close, on z-index 80 written as a number. There is no focus trap. | The shipped tokens sheet defines no z-layer tokens, and an undefined custom property drops the whole declaration. No component in the cockpit traps focus, and with no DOM harness a focus trap could not be proved by a test. | DECISION F265 D3 |
| 2026-09-24 | F265 | `RightLivePanel.tsx` | `ux_spec.md` §11 gives the right panel's order ending with the tasks card and the add-task row. It has no entry point for lessons. | A quiet "Lessons" button above the "System details" toggle, styled like that toggle, opens the overlay. | The learning surface came after the reference and the reference names no place to open it. The right panel is where the rest of the job's live reading happens. | DECISION F265 D3 |
| 2026-09-25 | F020 | `nodeStates.ts`, `tokens.css` | `graph_spec.md` §2 and §7 reserve a gray struck style for `vetoed`; `tokens_rules.md` lets only a `--remedy-state-*` token carry a status colour; `tokens.css` defines none for the veto. | A new token, `--remedy-state-vetoed`, holding `#9aa9c5`, the grey the canvas already drew, added to both token sheets with its line in `tokens_rules.md`. | A status colour must come from the status palette, and the palette had no veto grey. | DECISION F020 D1 |
| 2026-09-25 | F020 | `nodeStates.ts`, `paintNode.ts` | `assets_spec.md` §4: a small status dot on a failed node and a gray 45° strike on a vetoed one. | The dot and the strike are each outlined in the white node ring, `--remedy-graph-node-ring`, drawn twice as wide beneath them. | A red dot on a red sphere and a grey strike on a grey sphere are invisible without an outline, and state must never rest on colour alone. | DECISION F020 D1 |
| 2026-09-25 | F020 | `nodeStates.ts`, `paintNode.ts` | `graph_spec.md` §7: a planned node is white with a ring; the reference does not say what colour a glyph is drawn in on it. | A planned node's glyph, and the lines of a planned artifact, synapse or cluster, are drawn in the planned ring's blue; every other state's glyph is white. | A white glyph on a white sphere vanishes; the reviewer's headless-Chrome render of the kind-by-state matrix showed it. | DECISION F020 D2 |
| 2026-09-25 | F020 | `GraphLegend.tsx`, `BrainGraphStage.tsx` | T5_F020.md: the legend popover is "opened from the graph chrome per the design reference"; the reference designs no legend. | A "Legend" button beside the view toggle at the stage's bottom right opens a dialog listing every kind and every state, drawn from the same paths and tokens the canvas uses, closed by Escape. | The reference names no place or look for the legend, and the view toggle is the graph's only chrome on that side. | DECISION F020 D3 |
| 2026-09-25 | F020 | `stateMotion.ts` | `graph_spec.md` §12 names a state colour crossfade with the completion ripple only. | Every state change of a non-core node crossfades over 300 ms; only a change into `pass` also ripples. | A change into a failed or blocked state would otherwise jump, and the calm rule prefers a crossfade to a jump (`motion_spec.md`). | DECISION F020 D4 |
| 2026-09-25 | F023 | `EvidencePanel.module.css`, `tokens.css` | T5_F023.md's binding CSS for the evidence panel casts its shadow with the raw colour `rgba(37,50,79,.08)` and slides in with `animation: slideIn .22s ease`. | The same shadow through a new token, `--remedy-shadow-panel`, added to both token sheets with its line in `tokens_rules.md`; the slide-in runs over `--remedy-dur-base` (220 ms) with `--remedy-ease-soft`, and not at all under reduced motion. | `tokens_rules.md` forbids raw colours in component CSS and takes every duration and easing from the `--remedy-dur-*` and `--remedy-ease-*` tokens; `ease` is not a token, and `motion_spec.md` gives surfaces the soft curve. | DECISION F023 D5 |
| 2026-09-25 | F023 | `RunDetailPopover.tsx`, `EvidencePanel.tsx` | `component_spec.md` "DetailPopover" asks for a dialog role, a focus trap and Esc to close; `graph_spec.md` §10 anchors the run popover to its node. | Neither the run detail nor the evidence panel is a dialog, and neither traps focus; Escape closes each by walking the zoom back one level. The run detail sits beside the stage's centre, where the L2 camera has just placed the run, and does not follow the run when the reader pans. | In the zoom's model Escape is the walk back (`graph_spec.md` §10), and the zoom's Escape handler steps aside while a dialog is open, so a dialog here would stop Escape from closing it. Following the node would re-render the stage at the canvas's frame rate. | DECISIONS F023 D4 and D5 |
| 2026-09-25 | F023 | `ZoomBreadcrumbs.tsx` | `graph_spec.md` §10: a breadcrumb chip top-left of the stage, Job > Task > Run. | The chip appears from L1 on and is hidden at L0, where its trail would be the single word "Job"; the run's crumb reads the run's kind as the legend names it, such as "Review run". | A chip with nothing to walk back to only covers the graph, and a run has no title of its own in the model, while its kind is the name the legend already teaches. | DECISION F023 D2 |
