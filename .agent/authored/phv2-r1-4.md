**Authored-text fidelity protocol (R-0147/R-0144/R-0148):** when a paste
block contains reviewer-authored text (findings, verdicts, STATUS lines,
state-file resets), each text arrives between markers of the form
`--- BEGIN <name> sha256=<hex> ---` / `--- END <name> ---`, where the
hash covers the exact bytes between the markers including the trailing
newline. The worker's FIRST action is to save each text VERBATIM from
the paste to `.agent/authored/<feature>-r<round>-<n>.md`, verify
`sha256sum` of the saved file against the marker hash BEFORE committing
— on mismatch STOP: report the mismatch and the received bytes, commit
nothing (transport-wrap guard, R-0148 class) — then commit. Applying the
text = copying from that file. Byte-identity proofs = mechanical
disk-to-disk comparison (hash or exact substring) of the applied
location against that file. A proof computed against any retyped or
reconstructed copy is a false verification claim (block condition class,
R-0147). Only reviewer-authored text — arriving this way — may write
`## Verdicts` entries or set findings Resolved.
