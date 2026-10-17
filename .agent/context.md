# Context — execution excellence (operator order 2026-10-17, after PR 359)

## Active Branch
feature/execution-excellence from main `6933bb0` in `.remedy-wt/exec-excellence`. The main checkout
stays on main: `remedy serve start` (editable install) runs its code, so nothing is switched there.

## Evidence (read through Remedy's own readers; `.data/**` not read raw)
- Lab jobs ba1336a4c287455d (README), 9123bcef446e42b5 (normalizeName), 9cac3d5c2bd246eb (add()) in
  ~/Repos/remedy-lab; their Pi calls through `review_reports._job_report`.
- Corpus before/after: `tests.orchestration.scale_matrix` v3 run against main `6933bb0` and the branch.

## Scope
Lane over a few named files, verification readings and package-scoped tests, Pi failed-call usage
and builder context in large repositories, an order's jobs and a stop route over HTTP, job titles.

## Do not touch
The roadmap queue, `.agent/STOP`, the supervisor and service, the lab repository, the sandbox,
provider defaults, `pi.*` caps.

## Constraints
- No real model call (no authorized Pi budget); fake providers only.
- One pytest process tree at a time; one full local gate at the end.
- Commits at most 500 insertions; structure ratchet: listed files and functions do not grow.
