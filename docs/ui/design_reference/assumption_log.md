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
