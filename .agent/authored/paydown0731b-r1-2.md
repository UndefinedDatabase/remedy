- **Round types (operator ruling 2026-07-31, paydown0731
  precedent):** two named round types exist. SPLIT (default): the
  worker executes, the reviewer gates — MANDATORY for any change
  under packages/, apps/, or any other production code path, and
  for all feature work. Production code NEVER merges
  self-certified, regardless of size, test coverage, or honesty of
  labeling. SINGLE-SESSION MICRO-ROUND: one window may author,
  execute, self-review, and merge ONLY when the change set is
  limited to docs/, tests/, .agent/**, and roadmap files; the full
  fidelity ritual (scratchpad originals, hashes, cmp proofs) and
  evidence discipline apply unchanged; the handback and brief
  carry the label "single-session micro-round"; the standing
  same-session-merge approval covers only this type. Retroactive
  note: the 2026-07-31 paydown0731 round is ratified as the
  founding precedent of the single-session type EXCEPT its
  production-code commit (the R-0159 guard fix class): a change of
  that kind requires SPLIT from now on — the precedent cannot
  widen.
