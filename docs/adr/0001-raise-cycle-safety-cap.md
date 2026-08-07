# ADR-0001 — Raise `CYCLE_SAFETY_CAP` from 1 to 8

> **Status: ACCEPTED & APPLIED.** Applied 2026-08-07 on operator approval
> (relayed). The accompanying diff
> ([0001-raise-cycle-safety-cap.diff](0001-raise-cycle-safety-cap.diff)) is in
> the tree. The three pins named under *Consequences* were flipped in the same
> commit, and so were three further cap-dependent tests the record did not
> list (two CLI capping messages and the `over_cap` evidence pin).

- **Date proposed:** 2026-08-05
- **Feature:** T1_F075 — MILESTONE GATE: 10 flawless self-runs
- **Deciders:** the operator (human). This ADR is a proposal, not a decision.
- **Supersedes:** the F046 rollout rule "one cycle until the F075 milestone
  gate flips it" (`packages/orchestration/long_run_executor.py`, comment above
  `CYCLE_SAFETY_CAP`).

## Context — what the gate proved

F075 exists so that multi-cycle autonomy is earned with data. The rule it was
written against is in the source itself: config value and CLI flag are both
clamped to `CYCLE_SAFETY_CAP`, and *"Only the F075 milestone gate raises this,
via an explicit change with an ADR."*

The gate has now been met.

**Attempt 03 — 10/10 flawless from ONE invocation.**

- Evidence: [`.agent/gauntlet/attempt-03/matrix.json`](../../.agent/gauntlet/attempt-03/matrix.json)
  and [`matrix.md`](../../.agent/gauntlet/attempt-03/matrix.md)
  (`runs_recorded: 10`, `runs_flawless: 10`, `passed: true`,
  `failure_kinds: []`), committed at `67eb8f86` / `d84e114c`.
- Invocation: `self_run_gauntlet.py --live <root outside the repo>/campaign-a03
  --format both --label attempt-03` → exit 0. One invocation, ten orders in
  manifest order, no rerun inside the attempt, no order or template edits.
- Order set v4, frozen: set hash `e50916bf…` re-verified before the run,
  template digest `1c4f41bf…`, `preflight_injections -> []`.
- All nine pass criteria true in all ten runs, including
  `host_data_root_untouched` (the operator's real data root hashed identical
  before and after every run) and `no_unknown_postmortems`.
- All four injected harness failures FIRED and all four settled
  `retry_within_budget` — none `never_fired`, none `silent_success`.

**The history is part of the proof, and it is kept.** Attempt 01 = 0/10,
attempt 02 = 3/10, attempt 03 = 10/10. All three matrices remain committed
under [`.agent/gauntlet/`](../../.agent/gauntlet/). The bar was not lowered to
meet the runs; two product defects found by attempt 02 (R-0196 boundary retry
semantics, R-0197 compiler milestone cap) were fixed and re-proven first.

## Context — the measured usage

The campaign granted each order an explicit cycle budget, bound into the run
through `experiment_max_cycles` (R-0187 — the one deliberate way past the cap,
reachable only from code, never from config or a flag, and recorded in the
run's evidence as `source "experiment"` with `over_cap` true). Those budgets
are the v4 order set's, committed in `scripts/gauntlet_orders/`:

| order | kind | `max_cycles` granted | `max_iterations` granted | iterations used | terminal |
|-------|------|---------------------|--------------------------|-----------------|----------|
| g01 pure-code-change | pure_code_change | 4 | 12 | 5 | achieved |
| g02 test-add | test_add | 4 | 12 | 3 | achieved |
| g03 small-app-feature-smoke | small_app_feature | 5 | 12 | 5 | achieved |
| g04 doc-generation | doc_generation | 3 | 12 | 5 | achieved |
| g05 two-milestone-mission | two_milestone | 8 | 22 | 7 | achieved |
| g06 provider-api-error-mid-move | injection | 4 | 12 | 4 | achieved |
| g07 truncated-model-response | injection | 4 | 12 | 5 | achieved |
| g08 harness-death-mid-dispatch | injection | 5 | 12 | 6 | achieved |
| g09 harness-death-mid-write | injection | 8 | 22 | 8 | achieved |
| g10 escalate-then-finish | escalation | 3 | 12 | 5 | achieved |

Granted cycle budgets span **3 to 8**. The largest, 8, went to the two hardest
orders: the two-milestone mission (g05) and the mid-write harness death and
the rewrite it forces across a milestone boundary (g09).

**An honest limitation, stated rather than papered over.** Per-run cycle
*consumption* is written into each run's `gauntlet_run.json`
(`cycles_budget`, `cycles_resolved`) under the campaign evidence root, which by
policy (R-0176) lives OUTSIDE the repository during the run; only `matrix.md`
and `matrix.json` are committed, and the attempt-03 campaign root has since
been reclaimed with its session temp directory. What the committed evidence
therefore supports is: every order was granted a budget of 3–8 cycles, and
every order reached `achieved` under the budget it was granted. Iteration
consumption *is* recorded (the table above, audited in the R11 verdict) and
shows every run finishing well inside its iteration budget — the largest, g09,
at 8 of 22.

## Decision proposed

**Raise `CYCLE_SAFETY_CAP` from `1` to `8`** in
`packages/orchestration/long_run_executor.py`, with the comment above it naming
this ADR.

**Why 8 and not another number.** 8 is the largest cycle budget the passing
campaign granted, and the ceiling under which 10/10 was demonstrated. It is
chosen as the *proven ceiling* rather than as measured-maximum-plus-margin,
because per-run consumption is not in the committed evidence (above) and this
ADR will not manufacture a number the evidence does not carry. A higher cap
would permit configurations the gate never exercised; a lower cap would sit
below what the gate actually ran, and would forbid by configuration the very
orders (g05, g09) whose success is the argument for raising it at all. The
budget rationales in the order files already contain their own margin, and the
cap is a **ceiling, not a grant** — nothing runs eight cycles because the cap
is 8; a run reaches eight cycles only if an operator asks for it and the loop's
own stop conditions (budget, deadline, all-green, blocked) do not fire first.

**What stays conservative — recommendation: leave `DEFAULT_MAX_CYCLES` at 1**
(and with it the shipped `cycles.max_cycles` config default, which is
registered from that constant). The gate proved that *budgeted, opted-in*
multi-cycle missions complete flawlessly. It did not prove that multi-cycle
should be what an operator gets without asking. Raising the cap makes
multi-cycle *reachable* through the documented config key and CLI flag, which
is the capability F075 was meant to unlock; raising the default would make
every existing job silently more expensive and longer-running on the next
upgrade. Cap and default are separate knobs precisely so this choice can be
made separately — keep the door unlocked, do not push people through it.

The `experiment_max_cycles` seam stays exactly as it is, for future gauntlet
campaigns: still code-only, still unreachable from config or a flag, still
recording `over_cap` in the run's evidence.

## Consequences

- Config (`cycles.max_cycles`) and the CLI flag can now resolve to any value up
  to 8; above 8 they are still trimmed, and `ResolvedCycles.capped` still
  reports the trim to the operator.
- The shipped behaviour of an unconfigured run is **unchanged**: one cycle.
- Two tests pin the cap at 1 today and must be flipped consciously as part of
  applying this ADR — they are marked so they are findable:
  - `tests/orchestration/test_long_run_executor.py` ::
    `TestCycleConfig::test_the_rollout_cap_is_still_one_until_adr_0001_is_applied`
  - `tests/orchestration/test_checkpoints.py` ::
    `test_the_default_single_pass_still_writes_exactly_one_checkpoint`
    (`assert CYCLE_SAFETY_CAP == 1`)
  - `TestCycleConfig::test_the_cap_trims_both_flag_and_config` asserts
    `CYCLE_SAFETY_CAP == 1` inline and needs the same conscious update.
- Documentation that states the one-cycle rollout rule should be re-read after
  application; the rule's home is the comment above the constant.

## Rollback

One constant. Revert `CYCLE_SAFETY_CAP` to `1` (and the three test pins) — the
diff applies and reverses cleanly. No data migration, no evidence rewrite, no
behaviour change for runs that never asked for more than one cycle.

## Applying this ADR

```
git apply docs/adr/0001-raise-cycle-safety-cap.diff
```

Then update the three pinned assertions listed under *Consequences*, run
`python3 -m pytest tests/orchestration/ -q`, and change this ADR's status line
from PROPOSED to ACCEPTED with the date and the applying human's name. A
machine must not make that edit.
