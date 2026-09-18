-- STEP R12 closure: repair 1 and round A -- F268 remedy do: the one-command start --
Session 2 of F268 · round 12 · base `205b10a5` (branch feature/f268-remedy-do, pushed).

Goal: book round 11's verdict; repair the closure suite's three bad nodes; then closure round
A — the self-use item (precondition 6), the integrity check (precondition 3), the evidence job
(algorithm step 1) and the review zip (algorithm step 2), reporting the values round B quotes.

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions 3
and 6, Algorithm steps 1 and 2 with every pitfall (a) to (e), "Canonical zip build sequence");
docs/agents/self_drive_protocol.md amend0917-throughput (2); `.agent/authored/f268-closure-suite.txt`;
F266's working closure artefacts, which are this round's recipe: commit `8a6dd9a3` and
`.agent/selfuse_f266/` (the self-use item), `.agent/authored/f266-integrity-check.txt`,
`.remedy-wt/scratch/create_f266_evidence_clean.py` with `.agent/authored/f266-r10-evidence-summary.txt`
(the evidence job), `.agent/authored/f266-r10-zip-output.txt` (the zip).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r12/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md  sha256 9b923d5cd901d312eae80588c23ba31c710917cb8a198e1f17b58b40750bc536
  plan.md    sha256 5c6363bf86c68c2b4b86a790e5f6b7506088bd502419bfda44db396dfbb39062
  block.md   this block (save it as `.agent/authored/f268-r12-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f268-r12-<name>`;
   `.agent/live_review.md` := `git show 205b10a5:.agent/live_review.md` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 repair 1 — one commit, BY DESIGN: in `tests/orchestration/test_prompt_trace.py` the three
   `TestSegmentManifest` tests the closure suite lists read the source of
   `packages.orchestration.do_sequence` instead of `apps.cli.commands.do_cmd` (F268 round 1's
   `affb365d` moved the call sites there); every string they assert stays exactly as it is;
   rename the local binding and fix the two docstrings' "CLI" to name where the sites live.
C3 self-use item — one commit, F266's convention (`8a6dd9a3`): the queue holds no pending
   item, so call `packages.orchestration.self_use_generator.generate_and_append_if_empty`
   first, then `packages.orchestration.self_use_runner.run_next_self_use_item` to the normal
   approval gate (never applied); save the same evidence files as `.agent/selfuse_f266/` under
   `.agent/selfuse_f268/`, including the strings
   `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
   run's `JobPlan`; commit them with the queue change the generator wrote. Do NOT set
   `consumed_by` (round B's closure commit does) and do NOT write a finding into
   `.agent/live_review.md`: quote each defect string verbatim in the handoff; the reviewer
   registers them.
C4 integrity check — one commit adding `.agent/authored/f268-integrity-check.txt`: the output of
   `packages.orchestration.integrity_gate.run_integrity_checks` (an object: `.passed`,
   `.fail_count`, `.checks`), every check's name and status. It must read passed; if it does
   not, stop and report. Push C1 to C4.
C5 evidence job and zip — from a CLEAN tree at C4, which is the ACCEPTED HEAD: adapt
   `create_f266_evidence_clean.py` into `.remedy-wt/f268-r12/create_f268_evidence.py` with
   `review_feature_id="f268"`, `job_id="f268r12e1001"`, `step_range="T001-T005"`, the evidence
   dir `.remedy-wt/f268_evidence_round12`, `base_commit` = the FORK POINT
   `8e075bbe` in full (prove it: `git rev-list --ancestry-path <base>..<C4>` and
   `git rev-list <base>..<C4>` print the same count), and sorted test files
   `tests/cli/test_do_evidence_package.py`, `tests/cli/test_do_flags.py`,
   `tests/cli/test_do_sequence_cli.py`, `tests/cli/test_quick_start.py`,
   `tests/orchestration/test_do_run.py`, `tests/orchestration/test_job_evidence.py`,
   `tests/orchestration/test_prompt_trace.py`, `tests/orchestration/test_task_deliverables.py`
   (the reviewer ran all but `test_prompt_trace.py` at `205b10a5`: `208 passed`, no skip);
   node ids from `--collect-only`, `len(node_ids) == selected`. Run it; then
   `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f268_evidence_round12`. The package
   status must read READY_FOR_REVIEW; read `committed_review_subject.head_commit` OUT of the
   package's manifest and require it equal C4. Do not move the package (its path is then
   `NOT ARCHIVED`). A BLOCKED_EVIDENCE package: fix only what the pitfalls (a) to (e) name and
   rebuild; anything else: stop and report. Never commit the evidence dir or the zip. Then one
   commit adding `.agent/authored/f268-r12-evidence-summary.txt` and
   `.agent/authored/f268-r12-zip-output.txt` in F266's shapes.
C6 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F268 · round 12 · rounds so far 12"; per-commit tables with
   `git show --numstat` counts for every commit before C6; every gate's real output; and, as a
   numbered list spelled exactly as the tools printed them: the evidence job id, the package
   filename, its SHA-256, the package path, the accepted HEAD in full, the self-use item id.
   Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via `monkeypatch.setenv`
   or a script's own `os.environ`; the shell denies `VAR=x cmd` and `cp` — copy with python.
   The self-use run is not a test: it runs on the role configuration as F266's did.
3. Never weaken an assertion or delete a test. A red you can repair inside this change set
   without touching a DECISION: repair it in its own commit before C4 and name it. Any other
   red: stop and report.
4. Build every appended file from `git show 205b10a5:<path>` bytes plus the payload.
5. Commit messages "F268 R12 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch docs/roadmap/**, README.md, `.claude/**` or production code; no STATUS edit.

Done when (G1 to G3 after C2; G4 after C4; G5 after C5; report literal output + real exit code):
G1 transport + state: payload digests matched; a python byte check prints True for the append
   against its `205b10a5` bytes; `.agent/plan.md` byte-equal to plan.md.
G2 repair shrink (amend0917-throughput (2)): `python3 -m pytest -q -p no:cacheprovider` over the
   three node ids `.agent/authored/f268-closure-suite.txt` lists -> 3 passed; then over
   `tests/orchestration/test_prompt_trace.py`, `tests/cli/test_do_sequence_cli.py` and
   `tests/cli/test_golden_path.py` -> 0 failed. Mutation red-proof in ONE disposable worktree at
   C2, `__pycache__` purged, the imported `do_sequence.py` printed: control, then
   `composed=plan_composed,` in `packages/orchestration/do_sequence.py` -> `composed=None,`
   -> `test_every_cli_call_site_hands_its_composition_down` red; remove the worktree.
G3 `python3 -m ruff check tests/orchestration/test_prompt_trace.py` -> "All checks passed!".
G4 the integrity check reads passed; `git status --porcelain` empty; tip equals origin.
G5 the evidence script's printed validation (`is_valid_current_run`, `validation_errors`), the
   two rev-list counts, the zip script's PACKAGE_STATUS and EVIDENCE_AUTHORITATIVE lines, the
   manifest's head_commit read from the package, and `sha256sum` of the package.
G6 after the push: `git status --porcelain` empty, tip equals origin, `git worktree list` one
   row, the `remedy/job-*` branch count.
Full suite: NOT run again (amend0917-throughput (1)).
-- end of block --
