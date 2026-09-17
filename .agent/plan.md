# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`.

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold. As of round 26, IT DOES.

## Current Step

ROUND 27 — CLOSURE SEQUENCE BEGINS (docs/roadmap/STATUS_closure_protocol.md).
C1 books round 26's PASS. C2 runs the full suite exactly once
(`python3 -m pytest -n auto -q`, primary checkout, worker), per
amend0917-throughput's precondition, and commits the transcript and bad-node
list as `.agent/authored/f281-closure-suite.txt`. This round does NOT
attempt repairs, does NOT touch the STATUS line, does NOT build the
evidence package — those are later closure rounds, once the transcript is
read and any repair need is scoped.

## Next Steps

1. Read `.agent/authored/f281-closure-suite.txt` against
   `docs/agents/self_drive_protocol.md`'s amend0917-throughput rule 2
   (CLOSURE REPAIR): every bad node is F281's to fix UNLESS the hosted CI
   record of the merge base on `main` (`c617dd74`) already shows it red
   there — check before assuming either way. At most three repair rounds,
   each strictly shrinking the bad set; what survives gets
   `xfail(strict=True)` plus a registered follow-up feature.
2. Once the suite is clean (or repaired/attributed), run the closure
   algorithm proper: self-use consumption (precondition 6), evidence job,
   review zip, STATUS line, final commit, PR — reading
   `docs/roadmap/STATUS_closure_protocol.md` step by step.
3. Session 4 continues while context comfortably suffices.

## Risks

- The suite may already carry pre-existing red nodes inherited from F280's
  own closure (F280's own mid-round suite run showed failures later rounds
  fixed before its acceptance) — do not assume today's run is clean, and do
  not assume today's failures are new either; check the merge-base CI record.
