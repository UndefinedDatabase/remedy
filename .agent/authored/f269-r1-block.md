-- STEP R1 T001 -- F269 Contract & contract templates --
Session 1 of F269 · round 1 · base `0955dd4c` (main, the merge of PR 256).

Goal: claim F269 and land T001 — the contract record on the mission, the milestone a dispatched
job serves, the derived job slice, and the read-only commands `remedy mission contract <id>` and
`remedy job contract <id>`.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F269.md; the DECISIONs in the
payload `decisions.md` (F269 D2 and D3 — they are this round's spec; where this block is terser,
they rule).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r1/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 550e6001e6f530091a9de009006d979ba89ac49b538c0a22b68f11f6e460cc04
  context.md           sha256 5b234b4ae44b04157b56381d7f59bca0f840da26bce1428cb61b85780133d6f0
  live_review_head.md  sha256 f2aabf0660fbc04b65c8dcbc083891209e93593361f7e4db36a8e6c4dd6f54ff
  ledger.md            sha256 3ab93e571a9543a6a1296aefa6cac78a558c90e593d44c4c9958d8e5b713b8dd
  decisions.md         sha256 994337d5ff4df9785bb75379849d1de4eafb068822f51dcde95cf890a3a88cd5
  status_from.txt      sha256 c87dab295d4e8899e7ab00d282a1cf8caf80de21edf7b871513d46d7deff82c0
  status_to.txt        sha256 8a59002b5ee8c8099eed602b6a9ce8128b44b0f0122a0e75bb9c50632a4cd4f6
  block.md             this block (save it; report its digest)

Bundle (commit order):
C1 claim — branch `feature/f269-contract` from `main` at `0955dd4c` (the reviewer already ran the
   Open PR Gate: it merged PR 256; zero PRs are open). One commit holding exactly: byte copies of
   every payload above as `.agent/authored/f269-r1-<name>`; `.agent/plan.md` := plan.md;
   `.agent/context.md` := context.md; `.agent/live_review.md` := live_review_head.md bytes + the
   old file's bytes from the line `## Findings` (inclusive) to the end + ledger.md bytes;
   `.agent/decisions.md` := old bytes + decisions.md bytes; `docs/roadmap/STATUS.md`: the single
   line equal to status_from.txt replaced by status_to.txt (reviewer's containment test on the
   pair: `TO contains FROM: False`, so a REWRITE — FROM 1x before, 0x after; TO 1x after).
C2 the record — new `packages/orchestration/mission_contract.py` per D2 and D3 (1)(2): frozen
   dataclasses for a criterion and a contract with `to_json`/`from_json`; a `ContractError`
   (ValueError subclass) whose message names the broken rule; a writer that validates and stores
   through `mission_state.set_mission_contract`; a reader taking a `Mission` that returns None when
   it has no contract and raises `ContractError` on a bad body; the job-slice function; a reader of
   a job's milestone; the D3 (1) function that records a milestone on a job record (False and no
   write when the job does not exist); one text renderer (list of lines) used by both commands.
   Name nothing `save_contract`/`load_contract` — `run_contract.py` owns those names. In
   `mission_state.py` change only the docstrings of `Mission` (its `contract` paragraph) and
   `set_mission_contract`, to name the new module as the shape's owner. Tests in a new
   `tests/orchestration/test_mission_contract.py`: a round trip; every D2 rule refused on write AND
   on read of a body stored raw through `set_mission_contract` (parametrized); the slice for a job
   of milestone M1 over criteria scoped [], [M1], [M2] is the [] and [M1] criteria in order, and a
   job with no milestone gets the [] criterion only; the milestone recorder writes, and returns
   False for an unknown job id.
C3 dispatch — in `packages/orchestration/orchestrator_loop.py`'s `MOVE_DISPATCH_JOB` branch, record
   `payload["milestone_id"]` on the created job through C2's function, beside the
   `attach_milestone_dod` call. A test in `tests/orchestration/test_orchestrator_loop.py` proves a
   job dispatched through that branch carries `metadata["milestone_id"]` on disk; read the file's
   existing dispatch tests first and extend the nearest one that creates a real job record.
C4 commands — catalog entries `mission.contract` (args: mission id, the project scope option
   `mission.show` uses, `--json`) and `job.contract` (job id, `--json`), both `read_only`,
   `supports_json=True`, `related=` naming only live ids; handlers in a new
   `apps/cli/commands/contract_cmd.py`, registered in `apps/cli/commands/__init__.py`; behaviour and
   exit codes exactly D3 (3). JSON: mission → `{"version": 1, "mission_id", "contract": <body or
   null>}`; job → `{"version": 1, "job_id", "mission_id", "milestone_id", "contract":
   {"template", "criteria": [<slice>]} or null}`. Help text carries none of the retired words in
   `tests/docs/test_vocabulary.py`'s `RETIRED_SYNONYMS`. Regenerate
   `tests/orchestration/import_reachability_allowlist.txt` from that test module's
   `reachable_closure()`, keeping the file's header lines. Tests in a new
   `tests/cli/test_contract_cmd.py` (subprocess via the helper the mission tests use, fake data
   dir): a three-criterion contract scoped [], [M1], [M2] renders all three for the mission; a job
   recorded for M1 renders two; under `--json` every job criterion equals the mission criterion of
   the same id; no contract → the sentence, exit 0, `null`; a job in no mission → exit 0, `null`;
   unknown mission and unknown job → exit 1; a body breaking a D2 rule → exit 1 naming the rule.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F269 · round 1 · rounds so far 1" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output; `## Next` naming Phase 1 rule 1 then the review of round 1, and "Operator
   questions open: <the count you read from the file>". Then `git push -u origin
   feature/f269-contract`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines; split C2 or C4 into
   code and tests commits (C2a/C2b) rather than exceed.
2. Do-not-touch (T2_F269.md): F061's check kinds and runners, F031's inbox contract, F264's
   channel, F072's renderer; `dod_compiler.py` and `dod_gate.py` are not edited this round.
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D2/D3 do not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` and STATUS file from `git show 0955dd4c:<path>` bytes.
6. Commit messages "F269 R1 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; `cmp` of `.agent/plan.md` and
   `.agent/context.md` against their payloads exit 0; a python check prints True that
   `.agent/live_review.md` equals head + the `0955dd4c` bytes from `## Findings` + ledger.md, and
   that `.agent/decisions.md` equals its `0955dd4c` bytes + decisions.md.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py
   tests/cli/test_contract_cmd.py tests/orchestration/test_orchestrator_loop.py
   tests/orchestration/test_mission_state.py tests/cli/test_mission_cmd.py tests/test_command_catalog.py
   tests/cli/test_command_catalog.py tests/orchestration/test_import_reachability.py
   tests/test_grouped_cli.py tests/cli/test_advertised_commands.py tests/cli/test_do_sequence_cli.py
   tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py` → summary line, 0 failed (serial, no `-n`; the
   reviewer's base reading of the existing files at `0955dd4c` was 0 failed).
G3 `python3 -m ruff check` over every .py file C2 to C4 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `mission_contract` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over the three files below first (must be exit 0); each mutation reverted
   before the next: (a) the job-slice function returns every criterion regardless of milestone →
   the slice tests of both new test files red; (b) the `origin` rule no longer checked → the
   parametrized refusal test red for origin; (c) C3's call removed → C3's dispatch test red. Files:
   `tests/orchestration/test_mission_contract.py`, `tests/cli/test_contract_cmd.py`,
   `tests/orchestration/test_orchestrator_loop.py`. Report each exit code and the failing ids;
   remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
