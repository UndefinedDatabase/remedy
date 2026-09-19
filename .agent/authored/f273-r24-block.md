-- STEP R24 closure round A, second half: integrity, evidence job, review zip -- F273 Findings paydown v1 --
Session 4 of F273 · round 24 · base `80bd3817` (the round 23 handoff, branch
`feature/f273-findings-paydown-v1`, pushed).

Goal: book round 23's verdict, R-0807's resolution and R-0999's registration; append the closure
paragraph to the feature file's Built State (closure precondition 4); commit the integrity check
(precondition 3); then build the evidence job (algorithm step 1) and the review zip (step 2) from a
clean tree, reporting the values closure round B quotes.

Read first, completely: AGENTS.md; docs/roadmap/STATUS_closure_protocol.md (Preconditions 3 and 4,
Algorithm steps 1 and 2 with every pitfall (a) to (e), "Canonical zip build sequence"); F271's
closure-A artefacts, the recipe this round follows: `.agent/authored/f271-integrity-check.txt`,
`.agent/authored/f271-r5-evidence-summary.txt`, `.agent/authored/f271-r5-zip-output.txt` and
`.remedy-wt/f271-r5/verify_zip.py`.

PAYLOADS: reviewer-authored, gitignored scratch in `.remedy-wt/f273-r24/`. Verify each sha256 before
use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md                sha256 d51e8aa8cb86de191c10a35e5a301d3c61e6c57c0e3c946fb73170b714732841
  slips.md                 sha256 9ebdda05a8a56bad82d31f5498805e23e24da5c87d9896c2e2a303afc4ea2654
  plan.md                  sha256 e6adabd2ad18f9ede28ed396d74b11074fb68ea4a04051337e2581a0db444492
  builtstate.md            sha256 07e1fddd773af747608fd1ea5113f9f0800a1465547e9ebc848f38bc4fac35c9
  next.md                  sha256 10e30e322c1f299d7c65efd6373e14c78b64d156cedb1dcf4994358ee44986f5
  integrity.py             sha256 6084bc1dc2ddd4c8a29a00f49841d397598e13412e90694f4e8d035b523f78c6
  create_f273_evidence.py  sha256 5880664ae50e6f0ad6df40d7a0b4ebeccb0e1e2a1361377f048e78c0cb1f4c11
  block.md                 this block (save it; report its sha256 and line count)

Bundle (commit order):
C1 bookkeeping, one commit: byte copies of ledger.md, slips.md, plan.md, builtstate.md and block.md
   as `.agent/authored/f273-r24-<name>`; `.agent/live_review.md` := its `80bd3817` bytes +
   ledger.md; `.agent/prose_slips.md` := its `80bd3817` bytes + slips.md; `.agent/plan.md` :=
   plan.md. Before this commit, compare the saved block copy's line count and sha256 with the block
   text you were given, and report both.
C2 Built State, one commit: `docs/roadmap/features/T2_F273.md` := its `80bd3817` bytes +
   builtstate.md. Nothing else.
C3 integrity check, one commit adding `.agent/authored/f273-integrity-check.txt`: run
   `python3 -B .remedy-wt/f273-r24/integrity.py` from the repository root on a clean tree at C2.
   It must exit 0 and read passed; if it does not, commit nothing and stop. Then push C1 to C3.
C4 evidence job and zip, from a CLEAN tree at C3, which is the ACCEPTED HEAD:
   `python3 .remedy-wt/f273-r24/create_f273_evidence.py`, then
   `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f273_evidence_round24`. Before the
   zip, prove the base: `git rev-list --ancestry-path --count <base>..<C3>` and `git rev-list
   --count <base>..<C3>` for base `80f7c5290e434b13abc3d637b5fd9d5d06b8b1cc` print the same
   number. The package must read READY_FOR_REVIEW: adapt F271's `verify_zip.py` into
   `.remedy-wt/f273-r24/wk_verify_zip.py`, with the package path the zip script printed and C3's
   full SHA, and require `committed_review_subject.head_commit` read OUT of the package equal to C3.
   Do not move the package. A BLOCKED_EVIDENCE package: fix only what pitfalls (a) to (e) name and
   rebuild; anything else: stop and report. Never commit the evidence dir or the zip. Then one
   commit adding `.agent/authored/f273-r24-evidence-summary.txt` and
   `.agent/authored/f273-r24-zip-output.txt` in F271's shapes, the package path included, written
   `NOT ARCHIVED` beside the directory it was built in.
C5 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 4 of feature F273 · round 24 · rounds so far 24", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C4, every
   gate's real output, open findings by distinct id (`count_open_findings`) on the ledger at C1,
   and, as a numbered list spelled exactly as the tools printed them: the evidence job id, the
   package filename, its SHA-256, the package path, the accepted HEAD in full, the self-use item
   id. Under External actions: the `remedy/job-*` branch count, and that the branches
   `remedy/job-81ec65896729405c` and `remedy/job-468c8e62a2cc4fac` and the worktree
   `.remedy-wt/job-468c8e62a2cc4fac` still exist; nobody may delete them without the operator. End
   with a `## Next` section whose body is next.md byte for byte, then the line "Operator questions
   open: <the count you read from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` (including `$?`), heredocs and `cd`
   before git. Use `git -C <path>` and small python scripts under `.remedy-wt/f273-r24/`, named
   `wk_*.py`, with an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test. A red gate: stop, commit nothing half-done, report.
4. Build every edited file from `git show 80bd3817:<path>` bytes plus its payload.
5. Commit messages read "F273 R24 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. No `.claude/**`, no production code, no README.md, no `docs/roadmap/STATUS.md`, no
   `scripts/self_use_queue.json`. Never run the `remedy` CLI or the self-use runner. Create no
   branch, delete none, and remove no worktree. Do not run the full suite (amend0917-throughput (1)).

Done when (report literal output and the real exit code):
G1 after C1: payload digests matched; a python check prints True that `.agent/live_review.md` and
   `.agent/prose_slips.md` equal their `80bd3817` bytes + ledger.md and slips.md, that
   `.agent/plan.md` equals plan.md, and that each `.agent/authored/f273-r24-*` copy equals its
   payload.
G2 after C2: `git rev-parse <C2>:docs` prints a52990ca2bfa7abb626f4be4095574887762de22 (the
   reviewer's dry-run object), and `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py` -> summary line, 0 failed.
G3 after C3: the integrity script's stderr lines and exit code; `git status --porcelain` empty;
   the local tip equals origin.
G4 C4: the evidence script's printed `is_valid_current_run` and `validation_errors`, the two
   rev-list counts, the zip script's PACKAGE_STATUS, EVIDENCE_AUTHORITATIVE and ZIP_PATH lines,
   and `wk_verify_zip.py`'s output with its exit code.
G5 after the push: `git status --porcelain` is empty, the local tip equals origin, `git worktree
   list`, and the `remedy/job-*` branch count. Report this in your final message only.
-- end of block --
