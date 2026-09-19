-- STEP R14 dead readers and placeholder tips -- F273 Findings paydown v1 --
Session 2 of F273 · round 14 · base `3a93d638` (the round 13 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 13's verdict and nine resolutions, register R-0990, land DECISION F273 D14, and
build R-0989, R-0903, R-0908, R-0911, R-0932 and R-0936 exactly as the reviewer's dry run built
them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D14 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r14/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 4836de3e760030259e2c2ed9bacc2d97f28c9fb27a9cf95533413985affb1fc1
  ledger.md            sha256 1decc65f47a0910ad735c19e0ea4892f0a76349454e91dc8d6f7f3d966e0074f
  decisions.md         sha256 3dfd0380c5292239addc81e12967f95754e161fc72e04f4c4050ba3f52d0bb10
  block.md             this block (save it; report its digest)
CODE — diffs research helpers built, which the reviewer applied in this order at `3a93d638`, ran
and red-proved in its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g5a.diff` sha256 31ac88d133b44cd701df61111a36e60ee0a5420ae291653d8069ec6d2ccec499
  `.remedy-wt/f273-proto-g5b.diff` sha256 33773ed2698f51f705a68260ad07617fc1a4adbd40647643be7a0e22ae0f1782
  `.remedy-wt/f273-proto-g5c.diff` sha256 d36c720b0c2452fe85251094f274abe7975b123a670cc6bd39cdc65b7ddf3a1c

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r14-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `3a93d638` bytes + ledger.md and decisions.md respectively.
C2 R-0989, R-0903, R-0908 — `git apply` g5a.diff.
C3 R-0911, R-0932, R-0936 — `git apply` g5b.diff, then `git apply` g5c.diff, ONE commit (g5b alone
   leaves the humanize-catalog test red; g5c completes it).
   Before each code commit run `git status --porcelain` and stage every path the applies touched,
   deletions included; nothing may be left untracked or unstaged.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 2 of feature F273 · round 14 · rounds so far 14" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0989, R-0903, R-0908, R-0911, R-0932 and
   R-0936, in the handoff only — never a `Done:` line of your own; `## Next` naming Phase 1 rule 1
   then the review of round 14, and "Operator questions open: <the count you read from the file>".
   Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`) and `cd` before git; use `git -C <path>` and small python scripts under
   `.remedy-wt/f273-r14/` (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D14 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show 3a93d638:<path>` bytes.
5. Commit messages "F273 R14 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` for real, never run the `remedy` CLI, `run_job` against this
   repository, `npm install` or the self-use runner, and create no branch. Research helpers may
   hold worktrees under `.remedy-wt/f273-h-*`; never touch them.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `3a93d638` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r14-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 lists exactly the paths `git apply --numstat` reads from g5a.diff, and of C3 exactly the
   union of the paths of g5b.diff and g5c.diff.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:apps <C3>:docs <C3>:pyproject.toml`
   prints exactly 3bb96506a48942faa493776a788f8a9eff14763f, 6893b5256164391cc2591a81a7506bfabae95f82,
   c6614371ade5f129651458d8a3a0dbe54f2eb436, 8fe275f9a975addeb3833859997e8594a87bef61 and
   0624d5bf709e869ed44bc23a725b47f880231b0e (the reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider` over every
   path of the list saved at `.remedy-wt/f273-s2/r14_control.txt` (one per line; read it, never
   edit it) plus `tests/orchestration/test_evidence_index.py` and
   `tests/orchestration/test_test_runner.py` -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider` and an env carrying
   `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (through the
   script's `env=`), `__pycache__` purged before each run, the imported
   `packages.orchestration.cockpit` path printed first to prove it resolves inside the worktree.
   The UNMUTATED control first over the test files named below (exit 0). Then, each reverted from
   its saved bytes before the next, counting each FROM line (with its newline) in the named file
   first (each must be 1), naming the failing ids. P = tests/cli/test_product_spine.py;
   Q = tests/test_cockpit.py.
   (a) `apps/cli/commands/job.py`: `        next_action = f"remedy job resume {jid} --json"` ->
   `        next_action = "remedy job resume <job_id> --json"` -> P fails;
   (b) the same file: in the one line starting `        next_action = (f"remedy patch approve {jid} `
   replace `{jid} {pending_ids[0]}` by `<job_id> <patch_intent_id>` -> P fails;
   (c) `packages/orchestration/cockpit.py`: in the one line containing
   `or give Remedy a new order: remedy do, then the order in quotes` replace that text by
   `or create a new job: remedy do run \"<goal>\"` (a backslash before each quote) -> Q fails;
   (d) the same file: in the one line containing `inspect with: remedy brain timeline {jid}` replace
   `{jid}` by `<job_id>` -> Q fails;
   (e) `packages/orchestration/pingpong_evidence.py`: in the one line containing
   `json.dumps(_redact_json_value(data), indent=2)` replace `_redact_json_value(data)` by `data` ->
   tests/orchestration/test_evidence_bundle.py fails;
   (f) `packages/orchestration/pingpong_loop.py`: `            effective_goal = task_input.title` ->
   `            effective_goal = "mutated"` -> tests/cli/test_task_input.py fails;
   (g) the same file: in the one line starting `    specs.append(("builder_context", ` replace
   `[context, ` by `[context + " ", ` -> tests/orchestration/test_builder_prompt_golden.py fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
