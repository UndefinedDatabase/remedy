# Handback — amend1014b: Pi is the default harness and a dirty tree is the baseline; the two incident commands now run back to back, for real

## Session

Operator amendment amend1014b (2026-10-15) · branch `feature/do-golden-path`, pull request #339 (open,
non-draft, **not merged**; title and body updated to cover the Pi default and the repeatable
dirty-baseline runs) · commits B1 to B10, `9ec2a0065`..`12d3522d8` (on top of `e3d4d333a`) · tip tree
`084a6bd2d91f33515897f01853a54f4023dbb91f`. No review comments existed on any of the three channels
of PR #339. `.agent/STOP` (untracked) and the F078 branch were not touched. Python 3.10.12.

## Result, plainly

**Success.** Both ordered commands worked consecutively in a fresh incident repository with no
provider flag, no commit, stash or reset between them, against the real Pi 1.2.0 and the real
`muse-glimmer:latest`. Acceptances A to E all passed (below).

## Acceptance (real Pi + Ollama, fresh fixtures, isolated data roots, `python3 -m apps.cli.grouped`)

| | Command | Result |
|---|---|---|
| A | `do "<order>" --repo .` | builder and reviewer `pi (ollama/muse-glimmer:latest)`; one job, one task, planning calls 0; cockpit URL printed before `run started` (ui step 0.3 s); run 42.9 s; Pi builder 8 model turns, tools read/bash/bash/edit/read/bash/bash, 29.9 s; reviewer 3 turns, `read,grep,find,ls`, 12.0 s; non-empty `result.diff` (`+Test is a minimal example project…`); target bytes and `git status` unchanged; cockpit stopped after |
| B | `do "<order>" --repo . --apply` | applied 1 file, run 69.4 s, README holds the paragraph, `git status` ` M README.md`, no commit |
| C | `do "…last scentence…" --repo . --commit-auto` run **immediately** after B | no clean-tree refusal; job started from B's bytes (`start_baseline` lists README.md, `diff` shows only the second paragraph as `+`); run 103.4 s; one commit touching only README.md; tree clean; no stash; report says README.md "already held your uncommitted edits, so the commit contains them too" |
| D | `notes.txt` dirtied, README order with `--commit-auto` | commit holds only README.md; `notes.txt` ` M`, sha256 identical; report names `left uncommitted and untouched: notes.txt`; stash empty |
| E | target README edited after the job worktree appeared, then `--apply` | apply blocked; `job apply --json` error `target_changed_during_run`, message names `README.md`; concurrent bytes sha256 identical; no commit; job dir and evidence kept |

Pi call records (argv with the prompt as a hash, tools, turns, usage, exit) are in
`<data root>/runs/<run>/pi/<role>.jsonl`. Pi argv: `pi --mode json --no-session --provider ollama
--model muse-glimmer:latest --offline --no-approve --no-extensions --no-mcp --no-skills
--no-prompt-templates --no-themes --tools <role list> -- <prompt>`. Ollama answered at
`http://localhost:11434` with the model installed (`remedy doctor health` `default_chain`).

## Verification

- Closure gate, once, `python3 -m pytest tests -q -n auto` through `scripts/remedy_pytest.sh`, Python
  3.10.12, at `b14ab678e` (tree `b6e881efd3510e92241baed31515418dd09d5cf0`): `1 failed, 23150 passed,
  22 skipped`. The one failure, `tests/cli/test_do_sequence_cli.py::test_an_apply_the_baseline_check_refuses_fails_the_walk_naming_the_job`,
  asserted the old refusal sentence; B10 changes that one assertion, and that file plus
  `tests/cli/test_do_pi_default.py` pass (`57 passed`) at the tip. The tip tree differs from the gated one by
  that single test line, so the green result is **not** a full-suite result for the tip; a second full run
  was not spent on it.
- Two earlier full runs hung to their timeout: the default builder became the installed `pi`, so a
  provider-less test would have started a real agent. `tests/conftest.py::_no_live_pi_reach` refuses the
  Ollama lookup the Pi chain makes before it spawns anything (like `_no_live_ollama_reach`).
- `ruff check packages apps tests` clean. The structure ratchet is green with three function rows and two
  file rows lowered (`run_pingpong`, `_apply_from_workspace`, `summarize_job_apply`, `pingpong_job.py`,
  `job_apply.py`) and the two pins lowered; no row rose.
- `remedy-review` is not an installed skill in this session; a self-review of the diff stat and of each
  commit ran instead (no external review was run).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| D1 Pi default | done | role defaults `pi`/`muse-glimmer:latest` for builder, reviewer, repair; planner/study stay direct; explicit `--builder-provider pi`; raw `ollama` builder/repair refused at the CLI naming `pi`; raw Ollama reviewer kept |
| D2 subprocess contract | done | `pi_provider.py`, argv vector, cwd = job workspace, private `<data root>/pi_agent/models.json`, env allowlist, role tools, guarded run; wall floor 900 s (decision recorded) |
| D3 JSONL authoritative | done | `pi_events.py`; LF framing, `message_end`, `agent_settled`, summed turns/usage; empty-diff pass rejected (`empty_diff_gate.py`) for job tasks; `no_file_changed` untouched |
| D4 prerequisites | done | checked at provider construction before any model call, no fallback; `doctor health` gained `default_chain`, `worker doctor` the same links; neither runs an agent |
| D5 working tree is baseline | done | `dirty_baseline.py`; captured before the worktree exists, seeded and committed on the job branch; apply source rebuilt from that commit; HEAD/branch movement and changed deliverables stop as `target_changed_during_run` |
| D6 apply and commit-auto | done | `--commit`/`--commit-auto` no longer need a clean tree; only the job's files are added and committed; disclosure and preserved paths in the report and the JSON |
| D7 fences kept | done | no gate weakened (see deviations for one narrowing of scope of the new rule) |
| Tests 1 to 18 | done | 1, 2, 9: `test_pi_provider.py`; 3, 4: `test_pi_events.py` and `test_pi_provider.py`; 5, 6: `test_pi_provider.py`; 7, 8: `test_pi_provider.py` and the updated role/execution tests; 10 to 14: `test_dirty_baseline.py`; 15, 16, 18: `test_do_pi_default.py` and the existing `test_do_bounded_lane.py`; 17: the existing full-lane/scale tests in `test_do_bounded_lane.py`/`test_do_order_file.py`, unchanged and green (no new scale-up test was written) |
| Acceptance A to E | done | table above |

## Deviations and remaining limits

- A reviewer pass on an empty diff is rejected only for job tasks with a non-fake builder (a single
  `remedy run` may still end a clean `builder_no_changes`, which an existing test pins).
- `--commit-with-history` still asks for a clean tree and refuses a dirty-start job (its branch holds the
  baseline commit); recorded in the decision.
- The refusal token `target_changed` was renamed `target_changed_during_run` (no alias).
- The token line shows one ledger "call" per Pi invocation; the real model-turn count is in
  `usage_actuals.model_turns` and the Pi call records.
- Cancellation is the Pi process group dying on a signal (`pi_killed`); the guarded runner has no separate cancel channel.
- Tool events are recorded after the call returns, not streamed live; the heartbeat keeps the wait visible.
- `do` text joins "to <repo>" after the disclosure sentence in the apply line; wording only.
- Pi runs with the user's permissions; no sandbox is claimed. Remedy's workspace, scope, hash and apply gates are the isolation.

## Next expected operator action

Review PR #339 and say whether to merge it (not merged here). A second full-suite run of the tip is
optional; F078 resumes on `feature/f078-autonomy-levels` after the merge.
