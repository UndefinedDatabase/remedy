-- STEP R3 T003 templates -- F269 Contract & contract templates --
Session 1 of F269 · round 3 · base `b487e3f7` (branch feature/f269-contract, pushed).

Goal: T003's template half — the four contract templates under `docs/contracts/`, their loader and
compiler, the deterministic proposal from the order, and `remedy do --contract <name>`.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F269.md; the payload `decisions.md`
(DECISION F269 D1 — this round's spec; where this block is terser, it rules); DECISIONs F269 D2 to
D4 in `.agent/decisions.md`; `packages/orchestration/mission_contract.py`; in
`packages/orchestration/do_sequence.py` `_step_plan` and `DoContext`; in `apps/cli/commands/do_cmd.py`
`_DO_FLAGS_NOT_YET_AVAILABLE` and `_cmd_do`.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r3/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md          sha256 0bbc5c346828908afef8e0fe7052ca501212aaffc1fc3b0d4280392154bc5f98
  decisions.md       sha256 555cf5d453287aecbe28601c37caa3b143a25683f7c50955218da133a90647ec
  plan.md            sha256 30e768aa370510ebda098e03cb50f669b6a3fe1f86484c262719ee34e4efef30
  website.md         sha256 e72ad6c15cc9ec767e48e6fdc3a559ca6621316000b1e170e06d3a38c8b38fba
  api-service.md     sha256 a13fb0aa3d4bfe8166407315fbc55d34edb1622fcfce09456c85eedaa0e4d61a
  cli-tool.md        sha256 d9aa100db16cfddf8be0993407f3ab35b05f01c8af8932fccad59e5a8a539b7d
  python-library.md  sha256 a6408ab07b022ea6094ee8620b77653c3d445ce2c2c2f4a79f42d8f5424c3cd3
  block.md           this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of ledger.md, decisions.md, plan.md and block.md as
   `.agent/authored/f269-r3-<name>`; `.agent/live_review.md` := its `b487e3f7` bytes + ledger.md;
   `.agent/decisions.md` := its `b487e3f7` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 the templates — `docs/contracts/<name>.md` := the payload of the same name, byte-exact, for all
   four; and `docs/README.md` registers them per AGENTS.md (a Quick-Find row keyed "contract
   templates", and a `## Contract Templates (`docs/contracts/`)` section before `## Roadmap` with a
   File | Description table, one row per template). Touch no other line of `docs/README.md`.
C3 loader + compiler + proposal — a new `packages/orchestration/contract_templates.py` per D1 (1)
   to (3): list the template names, load and validate one (refusing every D1 violation with the
   file and line named), compile it to `ContractCriterion`s through `mission_contract`'s compiler
   (the `check:` line path included), propose a template from an order, and write a template's
   criteria onto a mission that has no contract yet (a mission that already has one is refused).
   Templates are found in `docs/contracts/` beside the package's source tree. Tests in a new
   `tests/orchestration/test_contract_templates.py`: all four shipped templates load, and each
   one's fixture order proposes that template; a bare order and a tied order propose nothing; the
   compiled website template is `origin` `template`, whole-mission, `C001`.. in file order, with the
   blocking flags of the file; a fixture template under `tmp_path` with a `check:` line compiles to
   that check (id `ctr-<id>`); each D1 violation is refused naming its line (parametrized: wrong
   title, unknown section, a malformed bullet, a `check:` line that is not a valid check, no
   criteria); an unknown template name is refused naming the four.
C4 `do --contract` — remove `--contract` from `_DO_FLAGS_NOT_YET_AVAILABLE` and its parametrized
   case in `tests/cli/test_do_sequence_cli.py`; the catalog help of `do.run --contract` describes
   the forced template and names the four; D1 (4) in `do_sequence._step_plan` and `_cmd_do`. Tests
   (in `tests/cli/test_do_sequence_cli.py` or `tests/cli/test_do_flags.py`, the fake roles,
   `--no-llm --no-ui`): `--contract website` on a bare order gives a contract whose template is
   `website` and whose template criteria are exactly the website template's, in order;
   `--contract website` on an order naming one extra requirement gives those criteria plus planner
   criteria (at least one with `origin` `planner`), and every template criterion is present
   unchanged; without the flag, the website fixture order gets the proposed `website` template and
   the plan step's detail says proposed; `--contract nosuch` exits 2 naming the templates, writes
   nothing under the data root and registers no project. Update any existing test whose pinned
   behaviour D1 changes by design, keeping its property, named in the handoff.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature
   F269 · round 3 · rounds so far 3" plus one sentence of context self-assessment; per-commit
   tables with `git show --numstat` counts for C1 to C4; every gate's real output; `## Next` naming
   Phase 1 rule 1 then the review of round 3, and "Operator questions open: <the count you read>".
   Then `git push`.

Constraints:
1. Change set: the paths the Bundle names plus test files C3 and C4 edit, and the regenerated
   import-reachability allowlist if its test requires it (regenerate from `reachable_closure()`).
   Every commit < 500 inserted lines; split code and tests rather than exceed.
2. Do-not-touch: `dod_compiler.py`, `dod_gate.py`, `dod_runners.py`; F061's check kinds and runners,
   F031's inbox contract, F264's channel, F072's renderer. No hygiene criterion is added to any
   template this round (D1 (5)).
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python.
4. Never weaken an assertion or delete a test to pass (the removed `--contract` refusal case is
   the one deletion D1 orders). A red gate or an ambiguity D1 does not settle → stop, commit
   nothing half-done, report.
5. Build every edited `.agent/` file from `git show b487e3f7:<path>` bytes.
6. Commit messages "F269 R3 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that each of the
   four `docs/contracts/<name>.md` equals its payload, that `.agent/plan.md` equals plan.md, and
   that `.agent/live_review.md` and `.agent/decisions.md` equal their `b487e3f7` bytes + their slice.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_contract_templates.py
   tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_gate.py
   tests/cli/test_contract_cmd.py tests/cli/test_do_sequence_cli.py tests/cli/test_do_flags.py
   tests/cli/test_do_cmd_summary.py tests/orchestration/test_do_sequence.py
   tests/cli/test_golden_path.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py
   tests/orchestration/test_import_reachability.py tests/regression/test_resource_safety.py
   tests/docs/` plus every other test file this round created or edited → summary line, 0 failed.
G3 `python3 -m ruff check` over every .py file C3 and C4 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `contract_templates` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over `tests/orchestration/test_contract_templates.py` and the test file holding
   C4's tests first (must be exit 0); each mutation reverted before the next: (a) the proposal
   returns the first template with any match instead of refusing a tie → the tied-order test red;
   (b) the loader skips the `check:` line → the `check:` compile test red; (c) the plan step
   applies no template when `--contract` is given → the `--contract website` tests red. Report
   each exit code and the failing ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
