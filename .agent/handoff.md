# Handoff — F115 Prompt breakdown & cost report · SESSION CLOSE-OUT (R15, R16, R17)

Branch `feature/f115-prompt-cost-report`, HEAD `0fa1e40a` before this commit.
NO PR exists; closure has NOT started.

R15, R16 and R17 are ALL REVIEWED and ALL PASS, and all three verdicts are on
disk in `.agent/live_review.md` — not only in this file, which every handback
overwrites. This session did NOT invoke the §4 item-13 branch terminator,
because the branch has NOT ended: T003d, the integration gate and closure all
remain. That is the R-0335 lesson and the whole reason this commit exists.

## Rounds this session
| Round | Slice | Commits | Verdict |
|-------|-------|---------|---------|
| R15 | T003a/4 | `5c7f5159..6752841a` (f77554bf…6752841a) | PASS |
| R16 | T003b/4 | `6752841a..aa7ad8df` (aa1a6cfb…aa7ad8df) | PASS |
| R17 | T003c/4 | `aa7ad8df..69ec82e3` (7899fdb0…69ec82e3) | PASS |
| close-out | — | `69ec82e3..HEAD`, `.agent/**` only | state only, not a review round |

## Item status (R17)
| Item | Status | Reason |
|------|--------|--------|
| C1 | done | own commit, FIRST of the round |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | deviated | ordered content complete; ALSO the module docstring, which said "Three commands" and never named `stats cache` — adding a fifth under a false count would have left a wrong claim on disk beside new code |
| C6 | deviated | the six ordered properties are one test each; FOUR more tests were added because gate (k) orders the wiring proven "the way the suite does" and that proof is a test. The fixtures `data_root`/`project_id`/`ledger_path` are IMPORTED from `tests/cli/test_stats_cost.py`; only the evidence tree is new |
| C7 | done | |

## What the feature can do now
`remedy stats report` exists end to end over one project's ledger, with a
half-open `[since, until)` period, a prior-period comparison that states its
reason when there is none, markdown and json, and goldens that pin the
renderer against a real backfilled ledger.

## Findings
Open: **11** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331,
R-0333, R-0334, R-0336, R-0337. Next free ID **R-0338**.

## Resume here
The NEXT SESSION continues on THIS SAME branch:
1. T003d — the docs page the new user-visible behaviour needs, registered in
   the `docs/README.md` index in the SAME PR.
2. The integration gate (docs/agents/integration_gate.md).
3. Closure per docs/roadmap/STATUS_closure_protocol.md.
A round that touches `docs/roadmap/**` also gates with
`python3 -m pytest tests/docs/ -q`. The Open PR Gate has nothing to merge, so
it does not block this resume.

Sandbox notes: the `remedy` binary is refused in this session for planner and
worker alike, so `remedy plan status` / `plan next` were answered from
`docs/roadmap/STATUS.md`, which AGENTS.md names the roadmap execution ledger;
and `cmp` availability varied by round, so gate (a) records the method used
each time.

Fortschritt: 93 % (T001 ✅ · T002 ✅ · T003 fast fertig) — Schätzung
