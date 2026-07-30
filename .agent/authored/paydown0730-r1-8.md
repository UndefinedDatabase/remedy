- Resolved: R-0155 (process, Low) 2026-07-30: integration_gate.md
  now requires base-environment parity (root node_modules +
  apps/ui/dist) or per-id direct-evidence attribution; an
  unattributed comm -23 id counts as a genuine base failure and
  blocks the gate verdict.
  Done: R-0155 (commit <SHA_R0155> — the doc diff is the evidence).
- Resolved: R-0156 (process, Medium) 2026-07-30: tests/docs now pins
  the README accepted-count against the STATUS [x] count; the pin
  landed green (counts agree at 27) with a red negative control
  proving it bites.
  Done: R-0156 (commit <SHA_R0156> — test + red-proof transcript).
