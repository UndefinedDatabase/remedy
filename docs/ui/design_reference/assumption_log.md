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

None yet.
