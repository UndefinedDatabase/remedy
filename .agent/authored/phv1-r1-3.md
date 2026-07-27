**Authored-text fidelity protocol (R-0147/R-0144):** when a paste block
contains reviewer-authored text (findings, verdicts, STATUS lines,
state-file resets), the worker's FIRST action is to save each authored
text VERBATIM from the paste to
`.agent/authored/<feature>-r<round>-<n>.md` and commit it. Applying the
text = copying from that file. Byte-identity proofs = mechanical
disk-to-disk comparison (hash or exact substring) of the applied location
against that file. A proof computed against any retyped or reconstructed
copy is a false verification claim (block condition class, R-0147). Only
reviewer-authored text — arriving this way — may write `## Verdicts`
entries or set findings Resolved.

**Handback form:** every `.agent/handoff.md` rewrite follows
docs/agents/handback_template.md — all sections, in order. A missing or
incomplete section is a Medium finding; the second occurrence within one
feature is High and blocks until a compliant handback exists.
