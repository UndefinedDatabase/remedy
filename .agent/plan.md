# Plan — operator amendment amend1023-universe-trust

## Goal
Five parts from the operator's order of 2026-10-23: (1) the client property `host_tools`, granted
on the command line only, that offers `claude-cli` and the planner choice over HTTP; (2) small
orders stay small: the criteria scope guard, `shape: single-job`, and "no new documentation
files"; (3) `GET /api/v1/orders/{order}/story` and the order's job entries; (4) the F133 and F151
follow-ups, the measured evidence duration and the closure rule; (5) cancel the stuck probe.

## Current Step
C0: the state files, DECISION amend1023 D1 and D2, and the booking of F151 R10 and R11.

## Next Steps
1. Part 4: F133 run directory, docs claims, threshold test; F151 notes, docstrings, worker show
   JSON, kit transport, contract v2 name, the next feature's registration.
2. Part 1: `host_tools` in the registry, the three client commands, execution offer, routes, ledger.
3. Part 2: the three rules with fake-provider tests on the probe's wording.
4. Part 3: the order story route, its twin command, the order job keys, recorded answers.
5. Contract 1.29 everywhere: pages, matrix, changelog, interface.
6. Part 5: cancel the probe with `decline_results`; grant the orbs `host_tools`.
7. One full suite run, the repair loop, the PR, the merge on local evidence, the handback.

## Risks
- The structure ratchet: `serve_http_handler.py`, `pingpong_job.py`, `answer_public_api_post` and
  `plan_order_job` must not grow; `do_sequence.py` (994) and `do_cmd.py` (975) stay under 1000.
- No test runs before the end (operator order); guard tests surface only in the one full run.
