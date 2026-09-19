-- STEP R3 T003+T016 -- F273 Findings paydown v1 --
Session 1 of F273 · round 3 · base `a5e3b9ce` (the round 2 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 2's verdict and four resolutions, register R-0983 to R-0985, land DECISION F273
D3, and build T003's last clause and T016 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D3 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r3/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 e8a8d3e488569406c0cc7c07e5b266b6c24093f295f1d61c40a427f95921c693
  ledger.md            sha256 0c2631631c53c205cd70f15a776bb32cbea6dd3ffd9783fa8546fbed206e2d08
  decisions.md         sha256 6b9d4cd40b0413a17e6ccd6d2e37d558f3e1e5e6f633822d1267148e03a84813
  gate_from.txt        sha256 d6a81f6bb9520fc0faf8f4802b84c013e4a7ad4dee6f7b9f26498503fb97a910
  gate_to.txt          sha256 ea78e10b01f3bc52c543998903193f781e8f66a2d981479bbe262ab32d353d76
  block.md             this block (save it; report its digest)
CODE — three diffs research helpers built at `a5e3b9ce`, which the reviewer applied in this order,
ran and red-proved in its own worktree. Apply with `git apply`; never retype or edit a hunk:
  `.remedy-wt/f273-proto-t016a.diff` sha256 d9cf7e7793c67c947028228fd417eae805ed50f7849a7b04757d533a0de8dfdc
  `.remedy-wt/f273-proto-t016bc.diff` sha256 bdecc7a80ead41a95a9fe175f1a71607c15e519d10169561a9cd46b4322981a7
  `.remedy-wt/f273-proto-r0983.diff` sha256 aa3eb5b9d493d7fcb26359d696b8dae2a526367e0480933db8948c513a216c1c

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r3-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `a5e3b9ce` bytes + ledger.md bytes; `.agent/decisions.md` := its `a5e3b9ce` bytes +
   decisions.md bytes.
C2 T003, R-0645 — `docs/agents/integration_gate.md`: the bytes of gate_from.txt replaced by
   gate_to.txt (reviewer's containment test: `TO contains FROM: True`, an APPEND — FROM exactly
   1x before and after, and each line gate_to.txt adds exactly 1x among the lines this commit's
   diff adds).
C3 T016 (a), R-0984 — `git apply .remedy-wt/f273-proto-t016a.diff`.
C4 T016 (b) and (c), R-0985 and R-0839 — `git apply .remedy-wt/f273-proto-t016bc.diff`.
C5 R-0983 — `git apply .remedy-wt/f273-proto-r0983.diff`.
C6 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F273 · round 3 · rounds so far 3" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C5; every gate's
   real output; open findings by distinct id AND by the canonical line formula (the formula
   `count_open_findings` had at `a5e3b9ce`: `^- R-\d{4} — ` lines minus `^Done: R-\d{4} — ` lines —
   say which is which), measured on the committed ledger; lines `Landed: R-0645`, `Landed: R-0984`,
   `Landed: R-0985`, `Landed: R-0839` and `Landed: R-0983`, each naming its commit, in the handoff
   only — never a `Done:` line anywhere; `## Next` naming Phase 1 rule 1 then the review of round
   3, and "Operator questions open: <the count you read from the file>". Then `git push`. Open no
   pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, compound commands and `cd`
   before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r3/` with an
   explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test other than the rewrites the t016bc diff carries. A
   red gate or an ambiguity D3 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file, and `docs/agents/integration_gate.md`, from
   `git show a5e3b9ce:<path>` bytes.
5. Commit messages "F273 R3 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real.
7. A reviewer's disposable worktree `.remedy-wt/f273-r3-dry` exists: never run anything in it.

Done when (G1 to G5 at C5, before C6; report literal output and the real exit code):
G1 transport + state: every payload and diff digest matched; a python check prints True that
   `.agent/plan.md` equals its payload, that `.agent/live_review.md` and `.agent/decisions.md`
   each equal their `a5e3b9ce` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r3-*` copy equals its payload, and C2's pair obligations above.
G2 code transport: `git rev-parse <C5>:tests <C5>:packages <C5>:scripts <C5>:docs <C5>:.github`
   prints exactly 7f2abd8ebf29f2260f47f4cf3ef3a00ee9e97969, 33e5de700300b3644f0e979824eae0edcf526627,
   eac614e51c99eabe996a0cebe7b4bebaf2f8abd5, f1fd3da1ac35dae63ca2a6350f1ef205e3b0c2e4 and
   118e627f2d62e6962f7c0d9cdafa54888d110085 (the reviewer's dry-run subtrees).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_job_state_field.py tests/orchestration/test_ci_workflow.py
   tests/orchestration/test_ci_stages.py tests/orchestration/test_final_audit_evidence.py
   tests/orchestration/test_live_review_rotation.py tests/test_no_orphan_modules.py
   tests/orchestration/test_import_reachability.py
   tests/orchestration/test_review_manual_completion_shapes.py
   tests/orchestration/test_review_zip_deleted_path_authority.py
   tests/orchestration/test_job_evidence.py tests/orchestration/test_review_archive_artifacts.py
   tests/orchestration/test_review_authoritative_e2e.py
   tests/orchestration/test_review_final_status_source.py
   tests/orchestration/test_review_package_full_integration.py
   tests/orchestration/test_review_package_root_chain.py
   tests/orchestration/test_review_packaging_collision_safety.py
   tests/orchestration/test_review_zip_hygiene.py tests/orchestration/test_stream_export_e2e.py
   tests/orchestration/test_review_content_proof_strict.py
   tests/orchestration/test_review_subject_deletions.py tests/cli/test_job_show.py
   tests/cli/test_job_report.py tests/orchestration/test_run_state_covers_job_status.py
   tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_release_workflow.py`
   -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check` over the Python files C3 to C5 touch -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C5, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.job_evidence` path printed first to prove it resolves inside
   the worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted before the next, counting the mutated bytes in the named file first (each must be 1):
   (a) `packages/core/models.py`: `    def __str__(self) -> str:` replaced by
   `    def _unused_str(self) -> str:` -> `tests/orchestration/test_job_state_field.py` must fail; (b)
   `scripts/rotate_live_review.py`: `    return len(open_finding_ids(text))` replaced by
   `    return len(_OPEN_REGISTRATION_LINE.findall(text)) - len(_DONE_LINE.findall(text))` ->
   `tests/orchestration/test_live_review_rotation.py` must fail; (c)
   `scripts/build_review_manifest.py`: `            open_findings = _LEDGER_READER.open_finding_ids(content)`
   replaced by `            open_findings = []` -> `tests/orchestration/test_final_audit_evidence.py`
   must fail; (d) `packages/orchestration/job_evidence.py`:
   `        "tombstones": tombstones, "tombstone_count": len(tombstones)})` replaced by
   `        "tombstones": {}, "tombstone_count": 0})` ->
   `tests/orchestration/test_review_manual_completion_shapes.py` must fail; (e) the same file:
   `                _tombstones[_sf] = _f.base_sha256` replaced by
   `                _tombstones[_sf] = {"status": _f.status, "base_sha256": _f.base_sha256}` ->
   `tests/orchestration/test_job_evidence.py` must fail. Report exit codes and failing ids, and a
   mutation that stays green as green. Remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
