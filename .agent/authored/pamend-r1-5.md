### Operator addition 2026-07-27 — ledger-fixture corpus & integrity pattern
- **Fixture corpus from the external-orchestration era.** The finding
  classes R-0141/R-0143/R-0145 (incomplete handback accounting), R-0144
  (worker-authored verdict), R-0146 (silently dropped flag), R-0147
  (self-consistency proof passed off as verification) and R-0148
  (transport-corrupted authored text) live in git history
  (`.agent/live_review.md` across the F016..F048 branches; PRs
  #154/#155). This feature's build MUST extract them as fixtures: per
  class, a minimal reproduction of the defective artifact.
- **Integrity-pattern note.** The sha256-stamped authored-text pattern
  is retained internally as the artifact-integrity mechanism across the
  dispatch boundary (hash on write, verify on read). The copy-paste
  wrap-guard rationale is transport-specific and obsolete internally.
  This distinction is stated explicitly here rather than silently
  keeping or dropping either half.
