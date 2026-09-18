# Plan — F266 remedy study (repo comprehension pass)

Branch: feature/f266-remedy-study, cut from `main` at the merge commit of
pull request 254 (F281's closure).

## Goal

The three-step `remedy init` → `remedy study` → `remedy teacher` runs on an
arbitrary repository: `study` performs a bounded, read-only comprehension
pass and files APPROVED memory cards carrying `provenance: "machine-study"`
(DECISION D-C, `docs/roadmap/features/T4_F266.md`), and `teacher ask`
answers questions about that repository from those cards.

## Current Step

ROUND 7 — T003: the three-step proved end to end against a foreign
repository fixture. New test `tests/cli/test_study_teacher_e2e.py` runs
`init` as a real subprocess, `study run` and `teacher ask` in-process (so
both transport seams are controlled deterministically), on a fixture
repository carrying a distinctive top-level directory name, and asserts
`teacher ask` is shown that name only through the `study:structure` card —
never derivable from general knowledge. Also books `Done: R-0959` and
`Done: R-0960` (fixes landed round 5, never booked in round 6 — amend0827
rule 1), and fixes newly-registered `R-0961` (an undersized subprocess
timeout in round 5's own reachability test, made red by this environment's
real, reachable local Ollama).

## Next Steps

1. Closure sequence: Built State, evidence job, review zip, STATUS line, PR.

## Risks

- None new this round.
