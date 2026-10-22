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
| `standard` | `(integration or subprocess) and not real_ollama` | Integration and subprocess tests on the fake provider. The determinism suite lives here rather than in a stage of its own (DECISION F083 D4), and so does the TypeScript compile check, which carries the `integration` marker. |
| `ui` | `ui_contract and not real_ollama` | Python-verifiable frontend and UI contracts. No test in this selection shells out to the node toolchain. |
| `smoke` | `smoke and not real_ollama` | Smoke contracts for the scripts and the infrastructure. |
| `budgets` | `not real_ollama` over seven named paths | Repository ceilings: the guard suites that assert what this repository may not exceed. This is the one stage that selects BY PATH; its marker expression only excludes the live provider. |
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
| budgets | 28.08 | `## Q14`, three samples | 300 |
| excluded | not run — `runs_in_ci` is False | `## Q10` | 0 |

Two figures follow from that table. The five CI budgets sum to 3900 s, i.e. 65
minutes, which is why the hosted job caps at `timeout-minutes: 90`: the job cap
sits ABOVE the sum of the stage budgets, so a slow stage dies at ITS OWN budget
and names itself in the summary instead of the job being killed first and naming
no stage at all. And the five measured maxima sum to 1379.83 s, about 23.0
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

## Hosted CI is manual

DECISION amend1011-manual-hosted-ci (operator, 2026-10-11), temporary. Remedy runs
only on the operator's machine, and the hosted run takes 28 to 34 minutes, so
`.github/workflows/ci.yml` triggers on `workflow_dispatch` alone. The job, the
`3.10` and `3.12` matrix and `remedy ci run` are unchanged; nothing about what CI
means moved. No branch protection or ruleset requires a status check on `main`
(read 2026-10-11), so no GitHub setting changed.

**Still mandatory, locally:** whatever the Commit Gate in AGENTS.md and the active
protocol already require; this change adds and removes no local gate. They run once
per pushed commit. A green result is reused as evidence while the tree, commands
and interpreter match what was recorded (commit SHA, commands, interpreter,
result); opening a pull request starts no second full local run. `remedy ci run`
is the full-suite command for a closure or a control, not a per-commit step.

**Start a control run:**

    gh workflow run ci.yml --ref <branch>
    gh run watch <run-id> --exit-status

or the Actions tab, "CI", "Run workflow". Run it on the release commit before the
release gate: `release.yml` reads that commit's `ci.yml` conclusion and refuses a
missing one.

**Reactivate:** restore `push: branches: [main]` and `pull_request: branches:
[main]` under `on:` in `ci.yml`, change `test_hosted_workflow_is_manual_trigger_only`
in `tests/orchestration/test_ci_workflow.py` to pin them, delete the amend1011
clause under the Open PR Gate in AGENTS.md, and, if wanted, add the `ci` check as
a required status check on `main` (operator action in GitHub: Settings, Rules).

## No retries

Remedy deliberately does NOT retry a failing stage, and no step in the hosted
workflow is ever re-attempted automatically. A flaky test is quarantined only by
an explicit marker change in a reviewed diff. The reason is short: retries hide
rot. A red run stays red until a human reads it.

The command has no "stop at the first red" switch either. `run_ci_stage` never
raises on a red stage, so every selected stage always runs and the summary is
always complete. A run in which nothing ran at all is red, not green.

## No UI toolchain any more (DECISION F083 D6, retired)

DECISION F083 D6 made the UI toolchain a precondition of the `standard` stage, installed by the
hosted workflow before `remedy ci run`. The UI and the tests that needed its toolchain were
deleted on 2026-10-15 (amend1015f D3), so the workflow installs no node toolchain and every stage
needs only the Python environment. The `ui` stage still runs the static brain viewer's checks.

## The tool sandbox on the hosted runner (R-1426)

Since amend1016sb (2026-10-16) a test or DoD command and every Pi tool run only inside the
Bubblewrap sandbox (`docs/system/tool-sandbox-v1.md`). The hosted runner image carries no
Bubblewrap, and Ubuntu 23.10 and later refuse the unprivileged user namespaces it needs, so the
workflow installs `bubblewrap`, allows those namespaces, and starts one `bwrap` before
`remedy ci run`; `tests/orchestration/test_ci_workflow.py` holds that order. Without it the first
dispatched run after amend1016sb, 39856076613 on 2026-10-22, read 166 failures per column, all
`sandbox_unavailable`.

## What is not measured

**Hosted wall time.** Every number in the budget table above was taken on a
developer machine whose `os.cpu_count()` reports 24, under `pytest 9.0.3`. No
hosted run has happened yet, and the first one IS that measurement. A GitHub
runner has fewer cores, so `standard` — by far the slowest stage measured — is
the one to watch. Raising a `timeout_sec` before that evidence exists would be a
guess wearing a budget's name.
