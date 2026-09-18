-- STEP R11 closure: repair 1 and round A -- F269 Contract & contract templates --
Session 2 of F269 · round 11 · base `c11fd76a` (branch feature/f269-contract, pushed).

Goal: book round 10's verdict; repair the closure suite's one bad node; then closure round A —
the self-use item (precondition 6), the integrity check (precondition 3), the evidence job
(algorithm step 1) and the review zip (algorithm step 2), reporting the values round B quotes.

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions 3
and 6, Algorithm steps 1 and 2 with every pitfall (a) to (e), "Canonical zip build sequence");
docs/agents/self_drive_protocol.md amend0917-throughput (2); `.agent/authored/f269-closure-suite.txt`;
`tests/test_subprocess_timeouts.py`; `packages/orchestration/contract_hygiene.py` `_git` and
`main`; F268's working closure artefacts, which are this round's recipe: commit `1be1950d` and
`.agent/selfuse_f268/` (the self-use item), `.agent/authored/f268-integrity-check.txt`,
`.remedy-wt/f268-r12/run_selfuse.py`, `.remedy-wt/f268-r12/create_f268_evidence.py` with
`.agent/authored/f268-r12-evidence-summary.txt` (the evidence job),
`.agent/authored/f268-r12-zip-output.txt` (the zip).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r11/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md  sha256 9700b1437e9803edee42568d36ad2458b6390f0f03413d284b888c0a64fb9fb6
  plan.md    sha256 3f5daacfb4a7ab57c32268fa7b5e5605ff7645414a69888d9ae288121e0d9c7b
  block.md   this block (save it as `.agent/authored/f269-r11-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f269-r11-<name>`;
   `.agent/live_review.md` := `git show c11fd76a:.agent/live_review.md` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 repair 1 — one commit, in `packages/orchestration/contract_hygiene.py` and
   `tests/orchestration/test_contract_hygiene.py` only (the reviewer dry-ran exactly this at
   `c11fd76a`: 68 passed over the G2 files, both mutations below red):
   (a) directly above `def _git(`, a module constant with a one-line `#:` comment:
       `_GIT_TIMEOUT_SEC = 60` ("Seconds one ``git`` query may take; a tree that hangs git cannot
       be measured.");
   (b) `_git`'s `subprocess.run(...)` gains `timeout=_GIT_TIMEOUT_SEC`;
   (c) before its `except OSError`, a new `except subprocess.TimeoutExpired as exc:` raising
       `HygieneMeasureError(f"git {' '.join(args)} timed out after {_GIT_TIMEOUT_SEC}s") from exc`
       — so a hanging git is D5 (1)'s "cannot measure", exit 2, a red check;
   (d) a new test directly after `test_an_unknown_rule_exits_2`:
       `test_a_git_query_that_times_out_exits_2_cannot_measure(repo, monkeypatch, capsys)` —
       `monkeypatch.chdir(repo)`; `contract_hygiene.subprocess.run` replaced by a fake that
       records `kwargs.get("timeout")` and raises `subprocess.TimeoutExpired(argv, <that
       timeout>)`; asserts `contract_hygiene.main(["unreferenced"]) == EXIT_CANNOT_MEASURE`, the
       recorded timeouts `== [contract_hygiene._GIT_TIMEOUT_SEC]`, and stderr holding
       `cannot measure` and `timed out after <_GIT_TIMEOUT_SEC>s`.
C3 self-use item — one commit, F268's convention (`1be1950d`): the queue holds no pending
   item, so call `packages.orchestration.self_use_generator.generate_and_append_if_empty`
   first, then `packages.orchestration.self_use_runner.run_next_self_use_item` to the normal
   approval gate (never applied); save the same evidence files as `.agent/selfuse_f268/` under
   `.agent/selfuse_f269/`, including the strings
   `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
   run's `JobPlan`; commit them with the queue change the generator wrote. Do NOT set
   `consumed_by` (round B's closure commit does) and do NOT write a finding into
   `.agent/live_review.md`: quote each defect string verbatim in the handoff; the reviewer
   registers them. If the generator returns None, record `self-use NONE (queue exhausted)` in
   the handoff and commit nothing for C3.
C4 integrity check — one commit adding `.agent/authored/f269-integrity-check.txt`: the output of
   `packages.orchestration.integrity_gate.run_integrity_checks` (an object: `.passed`,
   `.fail_count`, `.checks`), every check's name and status, in F268's shape. It must read
   passed; if it does not, stop and report. Push C1 to C4.
C5 evidence job and zip — from a CLEAN tree at C4, which is the ACCEPTED HEAD: adapt
   `create_f268_evidence.py` into `.remedy-wt/f269-r11/create_f269_evidence.py` with
   `review_feature_id="f269"`, `job_id="f269r11e1001"`, `step_range="T001-T005"`, the evidence
   dir `.remedy-wt/f269_evidence_round11`, `base_commit` = the FORK POINT
   `0955dd4c22b8533823aae05a8ec8b98fac88aafd` (prove it: `git rev-list --ancestry-path
   <base>..<C4>` and `git rev-list <base>..<C4>` print the same count), and sorted test files
   `tests/cli/test_contract_cmd.py`, `tests/cli/test_do_sequence_cli.py`,
   `tests/orchestration/test_contract_hygiene.py`, `tests/orchestration/test_contract_templates.py`,
   `tests/orchestration/test_mission_contract.py`, `tests/orchestration/test_mission_gate.py`,
   `tests/orchestration/test_orchestrator_loop.py`, `tests/orchestration/test_pingpong_job_dod_gate.py`
   (the reviewer ran them at `c11fd76a`: `447 passed`, no skip; C2 adds one test); node ids
   from `--collect-only`, `len(node_ids) == selected`. Run it; then
   `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f269_evidence_round11`. The package
   status must read READY_FOR_REVIEW; read `committed_review_subject.head_commit` OUT of the
   package's manifest and require it equal C4. Do not move the package (its path is then
   `NOT ARCHIVED`). A BLOCKED_EVIDENCE package: fix only what the pitfalls (a) to (e) name and
   rebuild; anything else: stop and report. Never commit the evidence dir or the zip. Then one
   commit adding `.agent/authored/f269-r11-evidence-summary.txt` and
   `.agent/authored/f269-r11-zip-output.txt` in F268's shapes.
C6 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F269 · round 11 · rounds so far 11" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for every commit before
   C6; every gate's real output; and, as a numbered list spelled exactly as the tools printed
   them: the evidence job id, the package filename, its SHA-256, the package path, the accepted
   HEAD in full, the self-use item id. `## Next` names Phase 1 rule 1, then the review of round
   11, then closure round B, and "Operator questions open: <the count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via `monkeypatch.setenv`
   or a script's own `os.environ`; the shell denies `VAR=x cmd`, `cp` and `sed -i` — use python.
   The self-use run is not a test: it runs on the role configuration as F268's did.
3. Never weaken an assertion or delete a test. Any red other than one C2 repairs: stop, commit
   nothing half-done, report.
4. Build every appended file from `git show c11fd76a:<path>` bytes plus the payload.
5. Commit messages "F269 R11 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch docs/roadmap/**, README.md, `.claude/**` or any production file but
   `contract_hygiene.py`; no STATUS edit.

Done when (G1 to G3 after C2; G4 after C4; G5 after C5; report literal output + real exit code):
G1 transport + state: payload digests matched; a python byte check prints True for the append
   against its `c11fd76a` bytes; `.agent/plan.md` byte-equal to plan.md.
G2 repair shrink (amend0917-throughput (2)): `python3 -m pytest -q -p no:cacheprovider
   tests/test_subprocess_timeouts.py tests/orchestration/test_contract_hygiene.py
   tests/orchestration/test_pingpong.py tests/cli/test_golden_path.py` -> 0 failed. Mutation
   red-proof in ONE disposable worktree under `.remedy-wt/` at C2, run from its root with
   `python3 -B -m pytest -q -p no:cacheprovider tests/test_subprocess_timeouts.py
   tests/orchestration/test_contract_hygiene.py`, the imported `contract_hygiene` module path
   printed first: control (exit 0); mutation A — delete the three lines of the
   `except subprocess.TimeoutExpired` clause -> `test_a_git_query_that_times_out_exits_2_cannot_measure`
   red; mutation B — delete `timeout=_GIT_TIMEOUT_SEC` from the call -> that test and
   `test_no_production_subprocess_call_is_missing_a_timeout` red. Report exit codes and failing
   ids; remove the worktree.
G3 `python3 -m ruff check packages/orchestration/contract_hygiene.py
   tests/orchestration/test_contract_hygiene.py` -> "All checks passed!".
G4 the integrity check reads passed; `git status --porcelain` empty; tip equals origin.
G5 the evidence script's printed validation (`is_valid_current_run`, `validation_errors`), the
   two rev-list counts, the zip script's PACKAGE_STATUS and EVIDENCE_AUTHORITATIVE lines, the
   manifest's head_commit read from the package, and `sha256sum` of the package.
G6 after the push: `git status --porcelain` empty, tip equals origin, `git worktree list` one
   row, the `remedy/job-*` branch count — in your final message.
Full suite: NOT run again (amend0917-throughput (1)).
-- end of block --
