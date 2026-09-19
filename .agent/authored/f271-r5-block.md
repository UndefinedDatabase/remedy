-- STEP R5 closure round A -- F271 No more legacy: ownership, reachability, replace-is-delete --
Session 1 of F271 · round 5 · base `10300cdd` (branch `feature/f271-no-more-legacy`, pushed).

Goal: book round 4's verdict; then closure round A — the self-use item (precondition 6), the
integrity check (precondition 3), the evidence job (algorithm step 1) and the review zip
(algorithm step 2), reporting the values round B quotes.

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions 3, 6
and 7, Algorithm steps 1 and 2 with every pitfall (a) to (e), "Canonical zip build sequence");
F270's working closure artefacts, which are this round's recipe: commit `6b08a96f` and
`.agent/selfuse_f270/` (the self-use item), `.agent/authored/f270-integrity-check.txt`,
`.remedy-wt/f270-r6/run_selfuse.py`, `.remedy-wt/f270-r6/create_f270_evidence.py` with
`.agent/authored/f270-r6-evidence-summary.txt` (the evidence job), and
`.agent/authored/f270-r6-zip-output.txt` (the zip).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f271-r5/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md      sha256 a652d7d9a65b3b2e71528ab643a9511267be2f23a6ed1c49cb0d16d09fe16d4f
  plan.md        sha256 24ad4d5cd7d0a5a340773592d0ece3e62741368faee8f95ada4eb46350aafb0c
  block.md       this block (save it in C1 with the others; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of EVERY payload above, the block included, as
   `.agent/authored/f271-r5-<name>`; `.agent/live_review.md` := its `10300cdd` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 self-use item — one commit, F270's convention (`6b08a96f`): call
   `packages.orchestration.self_use_generator.generate_and_append_if_empty` first (the queue
   holds no pending item at `10300cdd`), then
   `packages.orchestration.self_use_runner.run_next_self_use_item` to the normal approval gate
   (never applied); save the same evidence files as `.agent/selfuse_f270/` under
   `.agent/selfuse_f271/`, including the strings
   `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the run's
   `JobPlan` AND the run's `result_state`; commit them with the queue change the generator wrote.
   Do NOT set `consumed_by` (round B's closure commit does) and do NOT write a finding into
   `.agent/live_review.md`: quote each defect string and the result state verbatim in the handoff;
   the reviewer registers them. If the generator returns None, record `self-use NONE (queue
   exhausted)` in the handoff and commit nothing for C2.
C3 integrity check — one commit adding `.agent/authored/f271-integrity-check.txt`: the output of
   `packages.orchestration.integrity_gate.run_integrity_checks` (`.passed`, `.fail_count`,
   `.checks`), every check's name and status, in F270's shape. It must read passed; if it does not,
   stop and report. Push C1 to C3.
C4 evidence job and zip — from a CLEAN tree at C3, which is the ACCEPTED HEAD: adapt
   `create_f270_evidence.py` into `.remedy-wt/f271-r5/create_f271_evidence.py` with
   `review_feature_id="f271"`, `job_id="f271r5e1001"`, `step_range="T001-T002"`, the evidence dir
   `.remedy-wt/f271_evidence_round5`, `base_commit` = the FORK POINT
   `a4f79a94056283ec59da3cf56624001171f96fbd` (prove it: `git rev-list --ancestry-path
   <base>..<C3>` and `git rev-list <base>..<C3>` print the same count), and sorted test files
   `tests/cli/test_worker_facade_cmd.py`, `tests/orchestration/test_source_apply.py`,
   `tests/test_command_catalog.py`, `tests/test_no_orphan_modules.py` (the reviewer ran them at
   `10300cdd`: `131 passed`, no skip); node ids from `--collect-only`, `len(node_ids) ==
   selected`. Run it; then `bash scripts/make_review_zip.sh --evidence-dir
   .remedy-wt/f271_evidence_round5`. The package status must read READY_FOR_REVIEW; read
   `committed_review_subject.head_commit` OUT of the package's manifest and require it equal C3.
   Do not move the package. A BLOCKED_EVIDENCE package: fix only what the pitfalls (a) to (e) name
   and rebuild; anything else: stop and report. Never commit the evidence dir or the zip. Then one
   commit adding `.agent/authored/f271-r5-evidence-summary.txt` and
   `.agent/authored/f271-r5-zip-output.txt` in F270's shapes.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of
   feature F271 · round 5 · rounds so far 5" plus one sentence of context self-assessment;
   per-commit tables with `git show --numstat` counts for every commit before C5; every gate's
   real output; and, as a numbered list spelled exactly as the tools printed them: the evidence job
   id, the package filename, its SHA-256, the package path, the accepted HEAD in full, the self-use
   item id. `## Next` names Phase 1 rule 1, then the review of round 5, then closure round B, and
   "Operator questions open: <the count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via a script's own
   `os.environ`; the shell denies `VAR=x cmd`, `cp` and `sed -i` — use python. The self-use run is
   not a test: it runs on the role configuration as F270's did.
3. Never weaken an assertion or delete a test. Any red: stop, commit nothing half-done, report.
4. Build every edited file from `git show 10300cdd:<path>` bytes plus the payload.
5. Commit messages "F271 R5 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch README.md, `docs/roadmap/STATUS.md`, `.claude/**` or any production file.

Done when (G1 and G2 after C1; G3 after C3; G4 after C4; report literal output + real exit code):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` equals its `10300cdd` bytes + ledger.md, that `.agent/plan.md` equals
   plan.md, and that each `.agent/authored/f271-r5-*` copy equals its payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed.
G3 the integrity check reads passed; `git status --porcelain` empty; tip equals origin.
G4 the evidence script's printed validation (`is_valid_current_run`, `validation_errors`), the two
   rev-list counts, the zip script's PACKAGE_STATUS and EVIDENCE_AUTHORITATIVE lines, the
   manifest's head_commit read from the package, and `sha256sum` of the package.
G5 after the push: `git status --porcelain` empty, tip equals origin, `git worktree list` one row,
   the `remedy/job-*` branch count — in your final message.
Full suite: NOT run again (amend0917-throughput (1)).
-- end of block --
