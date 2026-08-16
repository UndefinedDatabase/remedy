# Plan — amend0816 CI hosted green

Branch: feature/amend0816-ci-hosted-green, cut from origin/main after the F083
closure PR #202 merged. Operator amendment "amend0816-ci-hosted-green".

## Goal
Deliver the half of F083's Acceptance that was never checked: the hosted CI run
must be GREEN with the same stage results as the local one. The hosted `fast`
stage fails 10 tests because they mock the LLM path only halfway —
`packages/orchestration/intake.py::make_structured_call_fn` probes a LIVE Ollama
server, so on the operator machine those tests took the LLM branch and on a
runner they take the deterministic-skeleton branch. DONE when the workflow run
triggered by this branch's PR is green and both local `remedy ci run` invocations
(with and without Ollama reach) report identical stage results.

## Current Step
Measuring the reds in an Ollama-less throwaway venv (`.remedy-wt/amend0816/`),
then fixing each red by its class: (a) incomplete mock -> complete it,
(b) genuine live-provider test -> `real_ollama` marker, (c) other environment
state -> make hermetic. No test is deleted, no assertion weakened, no ceiling
raised.

## Next Steps
1. Add the autouse `tests/conftest.py` fixture that makes a live Ollama
   connection attempt fail immediately for every test without the `real_ollama`
   marker. That fixture is the durable repair; without it the same drift returns
   with the next test.
2. Run the full battery: ruff on touched files, `remedy ci run` in both
   environments, `tests/docs/` and `tests/cli/test_golden_path.py`.
3. Dated operator paragraph in `docs/roadmap/features/T2_F083.md` under
   "How it fits". STATUS.md and the README counters stay untouched.
4. Push, open the PR, `gh run watch` the hosted run to completion, repair any
   remaining reds, merge only on hosted green, restore ORIG_BRANCH.

## Risks
- A stage timeout (exit 124) on a slower runner is NOT to be fixed by raising a
  budget in `ci_stages.py`: stop and show the operator the measured times.
- The autouse fixture may surface further tests that silently relied on a live
  provider. Each one is classified by the same a/b/c rule, not skipped wholesale.
