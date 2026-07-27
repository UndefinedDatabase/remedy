- Paste block contains reviewer-authored text? FIRST action: save each
  text VERBATIM to .agent/authored/<feature>-r<round>-<n>.md; verify
  sha256sum of the saved file against the sha256=<hex> in its BEGIN
  marker BEFORE committing — mismatch = STOP, report, commit nothing
  (R-0148) — then commit; apply by copying from that file; proofs are
  disk-to-disk against it (R-0147). Never write into `## Verdicts` or
  mark findings Resolved — that text only ever arrives as
  reviewer-authored files under .agent/authored/ (R-0144).
