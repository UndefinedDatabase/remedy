-- STEP R4 T003 hygiene -- F269 Contract & contract templates --
Session 1 of F269 · round 4 · base `fc9aae2b` (branch feature/f269-contract, pushed).

Goal: T003's hygiene half — a check that measures the three hygiene criteria, the criteria in every
template, and the reviewer's rule, enforced in the ping-pong round and proved with the fake provider.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F269.md; the payload `decisions.md`
(DECISION F269 D5 — this round's spec; where this block is terser, it rules); DECISION F269 D1 in
`.agent/decisions.md`; `packages/orchestration/contract_templates.py`; in
`packages/orchestration/pingpong_loop.py` `_REVIEWER_SYSTEM`, `_apply_fake_builder_changes` and the
round loop of `run_pingpong` from the builder call to `make_repair_decision`;
`tests/orchestration/test_reviewer_prompt_golden.py`'s docstring.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r4/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md          sha256 1dc37f21861e38a05546868f22a736e80e9529a69659ec8b2f82e0cbcab61a99
  decisions.md       sha256 0077df5bfedbaa4dec4268c1c514b173192f840c65a7dd4da7acf65c81b5d102
  plan.md            sha256 43d349136ce24b5de82a6f682737a632894254025a1ed9962d4f3ce1ca6b2be3
  website.md         sha256 f01b81f8f3c45a83f5b66ed7d8002c03422ac741115becfeeecee7079ea4d431
  api-service.md     sha256 633699b2fb83c3af5e5d138adc87f18b806980fd5f6e95a014bd73ec4985abec
  cli-tool.md        sha256 3812b3654025701709ec79857c55266a303ac76a9a8dffd7b82956a5e215c19c
  python-library.md  sha256 983005906fd9fa3d9d5cad05893bee9aa69126e797d01ca0e645da858e1d487c
  block.md           this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of ledger.md, decisions.md, plan.md and block.md as
   `.agent/authored/f269-r4-<name>`; `.agent/live_review.md` := its `fc9aae2b` bytes + ledger.md;
   `.agent/decisions.md` := its `fc9aae2b` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 the check — a new `packages/orchestration/contract_hygiene.py` per D5 (1) to (4), standard
   library only, with a `main(argv)` behind `if __name__ == "__main__"`. Tests in a new
   `tests/orchestration/test_contract_hygiene.py`, each over a tmp git repository with a base
   commit: `unreferenced` reports an added module no other file mentions — the module's own text
   names its stem — and passes once a committed file imports it, and exempts `__init__.py` and a
   test file; `replaced` reports `util_v2.py` beside
   `util.py` and passes when `util.py` is deleted; `stubs` reports a TODO line added to a committed
   file, an added function whose body is `pass`, and passes an `abstractmethod`; each rule exits 0,
   1 and 2 (outside a git work tree) as D5 (1) orders, run as the subprocess
   `python3 -m packages.orchestration.contract_hygiene <rule>` with the repository as cwd; and one
   test runs a `custom_cmd` check of that argv through the REAL `dod_gate.evaluate_dod` in the tmp
   repository and reads it failed with an orphan and passed without.
C3 the templates — `docs/contracts/<name>.md` := the payload of the same name, byte-exact, for all
   four. Tests: every shipped template compiles its three hygiene criteria to the `custom_cmd`
   checks of their `check:` lines (id `ctr-<id>`, blocking).
C4 the reviewer's rule — D5 (6): the sentence in `_REVIEWER_SYSTEM`; the golden renders of
   `tests/orchestration/test_reviewer_prompt_golden.py` and any other test pinning that text
   updated as its docstring prescribes, the content change declared in the handoff; the round hook
   in `run_pingpong`. Tests: THE ACCEPTANCE TEST — `pingpong_job.run_job` on a tmp git repository
   whose base commit holds `main.py`, with `FakeProvider(builder_files=["orphan_module.py"],
   pass_on_round=1)` as builder and a passing `FakeProvider` as reviewer and `repair_rounds=0`, ends
   with the job blocked, and the exported round's reviewer findings carry `orphan_module.py` in
   `file` and in `summary`; the same run with `builder_files=["main.py"]` completes; a run whose
   fake builder adds `util_v2.py` beside a committed `util.py` is rejected naming `util_v2.py`.
   Every existing test whose pinned behaviour D5 changes by design is updated with its property
   kept, and named in the handoff with its reason.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature
   F269 · round 4 · rounds so far 4" plus one sentence of context self-assessment; per-commit
   tables with `git show --numstat` counts for C1 to C4; every gate's real output; `## Next` naming
   Phase 1 rule 1 then the review of round 4, and "Operator questions open: <the count you read>".
   Then `git push`.

Constraints:
1. Change set: the paths the Bundle names plus test files C2 to C4 edit, and the regenerated
   import-reachability allowlist if its test requires it (regenerate from `reachable_closure()`).
   Every commit < 500 inserted lines; split code and tests rather than exceed.
2. Do-not-touch: `dod_compiler.py`, `dod_gate.py`, `dod_runners.py`, `test_runner.py`'s executable
   list; F061's check kinds and runners, F031's inbox contract, F264's channel, F072's renderer.
   `FakeProvider` is not edited: the round hook produces the rejection, not the fake reviewer.
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D5 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show fc9aae2b:<path>` bytes.
6. Commit messages "F269 R4 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that each of the
   four `docs/contracts/<name>.md` equals its payload, that `.agent/plan.md` equals plan.md, and
   that `.agent/live_review.md` and `.agent/decisions.md` equal their `fc9aae2b` bytes + their slice.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_contract_hygiene.py
   tests/orchestration/test_contract_templates.py tests/orchestration/test_pingpong.py
   tests/orchestration/test_pingpong_cli.py tests/orchestration/test_reviewer_prompt_golden.py
   tests/cli/test_cli_ux.py tests/orchestration/test_job_worktree_integration.py
   tests/orchestration/test_run_manifest_recovery.py tests/orchestration/test_job_task_runner.py
   tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_gate.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py
   tests/orchestration/test_import_reachability.py tests/docs/` plus every other test file this
   round created or edited → summary line, 0 failed (the reviewer's base reading of the existing
   files at `fc9aae2b` was 0 failed).
G3 `python3 -m ruff check` over every .py file C2 to C4 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `contract_hygiene` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over `tests/orchestration/test_contract_hygiene.py` and the file holding C4's
   acceptance test first (must be exit 0); each mutation reverted before the next: (a) `unreferenced`
   treats a file's own text as a reference → C2's orphan test and the acceptance test red (the
   fake builder writes the file's own path into it); (b) `stubs` ignores the
   `abstractmethod` exemption → C2's abstractmethod test red; (c) the round hook appends its
   findings but leaves a `pass` verdict unchanged → the acceptance test red. Report each exit code
   and the failing ids; remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
