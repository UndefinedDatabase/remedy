-- STEP R6 closure round A -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 6 · base `e9750619` (branch feature/f270-history-apply, pushed).

Goal: book round 5's verdict and R-0978; then closure round A — the self-use item (precondition
6), the integrity check (precondition 3), the evidence job (algorithm step 1) and the review zip
(algorithm step 2), reporting the values round B quotes.

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions 3 and 6,
Algorithm steps 1 and 2 with every pitfall (a) to (e), "Canonical zip build sequence"); F269's
working closure artefacts, which are this round's recipe: commit `a971944c` and
`.agent/selfuse_f269/` (the self-use item), `.agent/authored/f269-integrity-check.txt`,
`.remedy-wt/f269-r11/run_selfuse.py`, `.remedy-wt/f269-r11/create_f269_evidence.py` with
`.agent/authored/f269-r11-evidence-summary.txt` (the evidence job), and
`.agent/authored/f269-r11-zip-output.txt` (the zip).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r6/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md      sha256 0e979b1e1d846d81307649a298ff5ba3ca846c1e6305f6a51c532c852fadc917
  plan.md        sha256 85126f76afe2e0be0034082f2a67943f162fca1c4775a42ce5036c3c45a1cae5
  f273_from.txt  sha256 9276418870aba38b4a9a4f057fb26cb23900ea5a3d65793fe0978a6d0a8be21c
  f273_to.txt    sha256 22323acfd1e64c284c2e9e822c14b1249e51465cb67b0b001e3e65147c64779b
  block.md       this block (save it in C1 with the others; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of EVERY payload above, the block included, as
   `.agent/authored/f270-r6-<name>`; `.agent/live_review.md` := its `e9750619` bytes + ledger.md;
   `.agent/plan.md` := plan.md; `docs/roadmap/features/T2_F273.md`: the bytes of f273_from.txt
   replaced by f273_to.txt (reviewer's containment test: `TO contains FROM: True`, an APPEND —
   FROM 1x before and after, and the lines C1's diff adds to that file are exactly the TO-only
   lines, in order).
C2 self-use item — one commit, F269's convention (`a971944c`): call
   `packages.orchestration.self_use_generator.generate_and_append_if_empty` first, then
   `packages.orchestration.self_use_runner.run_next_self_use_item` to the normal approval gate
   (never applied); save the same evidence files as `.agent/selfuse_f269/` under
   `.agent/selfuse_f270/`, including the strings
   `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the run's
   `JobPlan` AND the run's `result_state` (R-0972: a budget stop returns no defect string); commit
   them with the queue change the generator wrote. Do NOT set `consumed_by` (round B's closure
   commit does) and do NOT write a finding into `.agent/live_review.md`: quote each defect string
   and the result state verbatim in the handoff; the reviewer registers them. If the generator
   returns None, record `self-use NONE (queue exhausted)` in the handoff and commit nothing for C2.
C3 integrity check — one commit adding `.agent/authored/f270-integrity-check.txt`: the output of
   `packages.orchestration.integrity_gate.run_integrity_checks` (`.passed`, `.fail_count`,
   `.checks`), every check's name and status, in F269's shape. It must read passed; if it does not,
   stop and report. Push C1 to C3.
C4 evidence job and zip — from a CLEAN tree at C3, which is the ACCEPTED HEAD: adapt
   `create_f269_evidence.py` into `.remedy-wt/f270-r6/create_f270_evidence.py` with
   `review_feature_id="f270"`, `job_id="f270r6e1001"`, `step_range="T001-T004"`, the evidence dir
   `.remedy-wt/f270_evidence_round6`, `base_commit` = the FORK POINT
   `b7f966c0b597ab1da010f3e245c055b9e8d54509` (prove it: `git rev-list --ancestry-path
   <base>..<C3>` and `git rev-list <base>..<C3>` print the same count), and sorted test files
   `tests/cli/test_do_commit_flags.py`, `tests/cli/test_do_sequence_cli.py`,
   `tests/orchestration/test_job_apply_commit.py`, `tests/orchestration/test_job_apply_history.py`,
   `tests/orchestration/test_job_worktree_integration.py` (the reviewer ran them at `e9750619`:
   `164 passed`, no skip); node ids from `--collect-only`, `len(node_ids) == selected`. Run it;
   then `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f270_evidence_round6`. The
   package status must read READY_FOR_REVIEW; read `committed_review_subject.head_commit` OUT of
   the package's manifest and require it equal C3. Do not move the package. A BLOCKED_EVIDENCE
   package: fix only what the pitfalls (a) to (e) name and rebuild; anything else: stop and report.
   Never commit the evidence dir or the zip. Then one commit adding
   `.agent/authored/f270-r6-evidence-summary.txt` and `.agent/authored/f270-r6-zip-output.txt` in
   F269's shapes.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of
   feature F270 · round 6 · rounds so far 6" plus one sentence of context self-assessment;
   per-commit tables with `git show --numstat` counts for every commit before C5; every gate's
   real output; and, as a numbered list spelled exactly as the tools printed them: the evidence job
   id, the package filename, its SHA-256, the package path, the accepted HEAD in full, the self-use
   item id. `## Next` names Phase 1 rule 1, then the review of round 6, then closure round B, and
   "Operator questions open: <the count you read>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via a script's own
   `os.environ`; the shell denies `VAR=x cmd`, `cp` and `sed -i` — use python. The self-use run is
   not a test: it runs on the role configuration as F269's did.
3. Never weaken an assertion or delete a test. Any red: stop, commit nothing half-done, report.
4. Build every edited file from `git show e9750619:<path>` bytes plus the payload.
5. Commit messages "F270 R6 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch README.md, `docs/roadmap/STATUS.md`, `.claude/**` or any production file.

Done when (G1 and G2 after C1; G3 after C3; G4 after C4; report literal output + real exit code):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` equals its `e9750619` bytes + ledger.md, that T2_F273.md equals its
   `e9750619` bytes with the pair applied, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f270-r6-*` copy equals its payload.
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
