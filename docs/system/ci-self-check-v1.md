# CI Self-Check v1

> Remedy's own CI: what it runs, in what order, under which measured budget, and
> what it deliberately never runs. Built by F083 (T001 the stage table, T002 the
> runner and the `remedy ci` seam, T003 the hosted workflow and this note). The
> target plan is [T2_F083.md](../roadmap/features/T2_F083.md); this page describes
> what is built. Hosted wall time is **not** measured here and this page says so.

## Overview

Remedy checks itself with four pieces and no fifth. One stage TABLE,
`packages/orchestration/ci_stages.py`, is data: it holds every stage, what that
stage selects, why it exists, whether CI runs it and how many seconds it may take.
One RUNNER, `packages/orchestration/ci_run.py`, executes a stage through
`scripts/remedy_pytest_runner.py` and returns a result. One local command,
`remedy ci run`, whose seam is `apps/cli/commands/ci_cmd.py`, selects the stages,
prints the summary table and sets the exit code. One hosted workflow,
`.github/workflows/ci.yml`, installs a toolchain and then calls that same command
exactly once. The table is the single source of truth for what CI means: the
workflow names no stage and selects no tests of its own, so the hosted run and a
local `remedy ci run` cannot drift into two opinions about what was checked.

## The stages

In the order CI runs them, taken from `CI_STAGES`.

| Stage | Selects | Why it exists |
|---|---|---|
| `fast` | `not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow` | Pure unit work: no integration state, no subprocess, no UI contract, no live provider. The cheapest signal, so it runs first. |
| `standard` | `(integration or subprocess) and not real_ollama` | Integration and subprocess tests on the fake provider. The determinism suite lives here rather than in a stage of its own (DECISION F083 D4). |
| `ui` | `ui_contract and not real_ollama` | Python-verifiable frontend and UI contracts, including the TypeScript check. |
| `smoke` | `smoke and not real_ollama` | Smoke contracts for the scripts and the infrastructure. |
| `budgets` | `not real_ollama` over four named paths | Repository ceilings: the guard suites that assert what this repository may not exceed. This is the one stage that selects BY PATH; its marker expression only excludes the live provider. |
| `excluded` | `real_ollama` | Live-provider tests. CI never runs them; they are listed so the coverage claim stays honest. |

Remedy deliberately does NOT store a collected test COUNT per stage. A count is
true for one commit and wrong for the next, and a table carrying stale numbers is
worse than one carrying none. For the marker vocabulary itself see
[test-lanes-v0.md](test-lanes-v0.md).

## The runtime budgets

Every budget below was DERIVED from a measurement, not chosen. The measurements
live in `.agent/f083_inventory.md`, three samples per stage, each sample its own
process, nothing averaged; the section named in the Source column is the one that
holds them. The rule that turns a measured maximum into a budget is:

    budget = ceil(2 * measured_max / 300) * 300

— double the slowest observed run, then round up to a whole five minutes. The
factor 2 and the 300-second rounding are not folklore: they are pinned by
`tests/orchestration/test_ci_stages.py`, which recomputes every `timeout_sec` in
`CI_STAGES` from the rule and fails if one drifts.

| Stage | Measured max, seconds | Source | Budget, seconds |
|---|---|---|---|
| fast | 397.45 | `## Q10`, three samples | 900 |
| standard | 935.14 | `## Q11`, three samples | 2100 |
| ui | 8.09 | `## Q10`, three samples | 300 |
| smoke | 11.07 | `## Q10`, three samples | 300 |
| budgets | 1.32 | `## Q12`, three samples | 300 |
| excluded | not run — `runs_in_ci` is False | `## Q10` | 0 |

Two figures follow from that table. The five CI budgets sum to 3900 s, i.e. 65
minutes, which is why the hosted job caps at `timeout-minutes: 90`: the job cap
sits ABOVE the sum of the stage budgets, so a slow stage dies at ITS OWN budget
and names itself in the summary instead of the job being killed first and naming
no stage at all. And the five measured maxima sum to 1353.07 s, about 22.6
minutes, which is what a green serial run actually costs on the machine the
samples came from.

The budget travels to the runner as `REMEDY_PYTEST_TIMEOUT_SEC`, set per stage on
the call rather than left to the ambient environment, and a stage killed at its
budget returns exit code 124 and is reported as timed out.

## What CI does not run, and says so

The `excluded` stage carries `runs_in_ci=False`. It is REPORTED as skipped in the
summary table, together with the command that runs it by hand — never silently
dropped, because the coverage claim is honest only while the exclusions stay
visible:

    python3 -m pytest -m real_ollama -q  # needs a running Ollama server

The benchmark also stays out of CI, on cost grounds, and is an on-demand step
rather than a stage.

## No retries

Remedy deliberately does NOT retry a failing stage, and no step in the hosted
workflow is ever re-attempted automatically. A flaky test is quarantined only by
an explicit marker change in a reviewed diff. The reason is short: retries hide
rot. A red run stays red until a human reads it.

The command has no "stop at the first red" switch either. `run_ci_stage` never
raises on a red stage, so every selected stage always runs and the summary is
always complete. A run in which nothing ran at all is red, not green.

## The UI toolchain is a precondition (DECISION F083 D6)

The hosted workflow runs `npm ci --prefix apps/ui` BEFORE `remedy ci run`. The UI
toolchain is a precondition of the `ui` stage, not a part of it: without that
install the stage's TypeScript check skips hosted, exactly as it skips on a local
checkout that never ran it, and F083's Acceptance line would be met by a skip
instead of by a real compile. The install is a workflow step rather than stage
logic so the stage table stays data and keeps naming no toolchain.

## What is not measured

**Hosted wall time.** Every number in the budget table above was taken on a
developer machine whose `os.cpu_count()` reports 24, under `pytest 9.0.3`. No
hosted run has happened yet, and the first one IS that measurement. A GitHub
runner has fewer cores, so `standard` — by far the slowest stage measured — is
the one to watch. Raising a `timeout_sec` before that evidence exists would be a
guess wearing a budget's name.
