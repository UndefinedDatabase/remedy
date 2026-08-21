# Context — F009 The single write channel

## Active Branch
feature/f009-single-write-channel, cut from `main` at `ce49348b`, the merge
commit of pull request #209, which R1 merged at the Open PR Gate. Self-drive
session per docs/agents/self_drive_protocol.md: the main session plans and
reviews and writes nothing in the work tree, one delegated worker per round makes
every commit. The branch carries no pull request; F009 opens one at its closure.

## Scope
In: ONE authenticated POST door for UI-initiated change —
`/api/jobs/<job_id>/commands` taking {command, args, client_nonce}, validated
against the UI-exposed catalog subset, authenticated by bearer plus an
X-Remedy-CSRF double-submit, rate-limited per token and job, deduplicated by
nonce so a replay returns the ORIGINAL body, audited per job including rejections,
and reaching the effect functions that already exist. Also in: the
`command.accepted` event on the F008 stream, the route-walking proof that every
other POST, PUT and DELETE answers 405, and the two lines D3 rules — the token
comparison becoming constant-time on BOTH doors.

Out, per the feature file's Do not touch: the effect backends' semantics, the
catalog's CLI half, and any file or shell access from a handler, forbidden by the
P3 contract and enforced by an import guard rather than by convention.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- DECISIONS F009 D1 THROUGH D9 ARE RULED as of R3 and bind every later round:
  the test home, the auth pair, the constant-time comparison, the exposed subset
  and its two catalog ids, the effect table with its own commit for the
  plan-approval extraction, the audit record's path and fields, the fingerprint,
  the nonce store, and the rate limit as a typed config key. They are in
  `.agent/decisions.md`; a round that departs from one amends it there first.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py — the second by
  R-0493, tests/docs/ asserting nothing about a feature file's body — and a round
  rewriting `.agent/` state or touching the UI server also gates
  tests/ui_server/, tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource safety
  stays intact. Two pytest processes never run at once.
- COUNT BY PASSED-PLUS-SKIPPED. Data-dependent `pytest.skip(...)` calls in
  tests/ui_server/ make the split vary run to run at an unchanged tree.
- This is a UI-facing feature: docs/ui/design_reference/ is binding for every
  visual surface and assets_spec.md is the asset authority.
- Repository-wide `ruff check .` is RED at base and is NOT a gate (R-0364); ruff
  is gated scoped to the files a round touches, measured against the SAME files
  at the base. `npm run lint` in `apps/ui` is likewise red at base and is R-0622.
- 196 findings are open and none is a code defect of F009. R-0403, R-0607,
  R-0608, R-0609, R-0611, R-0613 and R-0630 stay routed to a paydown branch.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
