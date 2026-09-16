# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 1 claims F280, cuts the branch, re-points this file and `.agent/context.md`, re-heads
`.agent/live_review.md`, books F261's round 28 verdict and its prose slip, and records DECISION
F280 D1. Its table commit hands `job run`'s `--builder-provider` and `--reviewer-provider` to the
runner, deletes `--builder` and `--reviewer` from `job run`, and refuses `fixture` there.

## Next Steps

1. The ping-pong path of `do run` with the flags only it reads, `--scope-file`, `--approve-scope`
   and the scope plan module (R-0894), with `_VALID_PINGPONG_PROVIDERS`, the `--builder` and
   `--reviewer` special-casing of `apps/cli/grouped.py`, the root help's quick start and the two
   provider messages that name the deleted flags; then R-0767's resolution.
2. `job budget <id> set` over the run-contract budget fields and the token budget profile
   (R-0906, R-0909), then `job fulfill`.
3. The fixtures and smoke sections moved off `job create`, then `job create`, `job attach-repo`
   and `job permit`.
4. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
5. The `flight_plan` rename; `worker doctor` and `job run --tasks`; then T002.

## Risks

- 125 findings are open by distinct id; three are High, R-0803, R-0804 and R-0807, none of them
  this feature's.
- Two provider error messages in `packages/orchestration/pingpong_provider.py` name `--builder`
  and `--reviewer`, which `job run` no longer has, until the next step re-points them.
- Argparse prefix matching refuses `--builder` on `job run` only as an ambiguous prefix of the
  three `--builder-*` flags; `TestJobRunProviderWiring` pins the refusal.
