-- STEP R16 repair loop, catalog contract, evidence refusal, worker-step rules -- F273 Findings paydown v1 --
Session 3 of F273 · round 16 · base `b22fe3bc` (the round 15 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 15's verdict and three resolutions, register R-0991, land DECISION F273 D16, and
build R-0918, R-0923, R-0924, R-0925, R-0926, R-0991, R-0912, R-0940 and R-0954 exactly as the
reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D16, this round's spec;
where this block is terser, it rules).

PAYLOADS: reviewer-authored, gitignored scratch in `.remedy-wt/f273-r16/`. Verify each sha256 before
use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md       sha256 cd414c84652459f9fff29207e1544b735f353ddf9641af3642369e109eb2ce20
  ledger.md     sha256 ab96ccf70a953cce18e9789acce87533d621c1fc1df2d519bfe21607cafddf96
  decisions.md  sha256 ae0459010c97ff46f17eb98463d6bc59ff06792e3c5ae072e6b8be3ba8803aa3
  next.md       sha256 428db3c5d4eb2dd6c79e74a96aa55301be9809b16c6dce359eb09dd50d2337ab
  targets.txt   sha256 a09777cc5f952c2bb4d5a19af1fa2b883d52ee66382750dbfb202575b043c043
  block.md      this block (save it; report its sha256 and line count)
CODE: diffs the reviewer applied in this order at `b22fe3bc`, then ran and red-proved in its own
worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g7a2.diff` sha256 90aa26fc961b0d72efa379521661568c937df0cac5ac9bbecd7612f1b7776185
  `.remedy-wt/f273-proto-g7d1.diff` sha256 250631d39537074f6f6fb6e016c2c899199289edcb0cd5427380c6162e3a4297
  `.remedy-wt/f273-s3/r16_docs.diff` sha256 1e1af63a6537da384250a29d31594167a6ce07004510e0b1e9f16993e5cc57db
Apply no other `.remedy-wt/*.diff` file.

Bundle (commit order):
C1 bookkeeping, one commit holding exactly: byte copies of plan.md, ledger.md, decisions.md and
   block.md as `.agent/authored/f273-r16-<name>`; `.agent/plan.md` := plan.md;
   `.agent/live_review.md` and `.agent/decisions.md` := each one's `b22fe3bc` bytes + ledger.md and
   decisions.md respectively. Before this commit, compare the saved block copy's line count and
   sha256 with the block text you were given, and report both.
C2 R-0918, R-0923, R-0924, R-0925, R-0926, R-0991: `git apply` g7a2.diff.
C3 R-0912: `git apply` g7d1.diff.
C4 R-0940, R-0954, and R-0924's Acceptance line: `git apply` r16_docs.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched,
   deletions included; nothing may be left untracked or unstaged.
C5 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 3 of feature F273 · round 16 · rounds so far 16", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C4, every
   gate's real output, and open findings by distinct id (`count_open_findings`) on the committed
   ledger. Add one `Landed: R-xxxx` line naming its commit for each of R-0918, R-0923, R-0924,
   R-0925, R-0926, R-0991, R-0912, R-0940 and R-0954, in the handoff only; never write a `Done:`
   line of your own. Record under External actions that the branch `remedy/job-81ec65896729405c`
   exists in this repository; a research helper's probe created it, and nobody may delete it without
   the operator. End with a `## Next` section whose body is next.md byte for byte, followed by the
   line "Operator questions open: <the count you read from the file>". Then `git push`. Open no
   pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test may call a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`), heredocs and `cd` before git. Use `git -C <path>` and small python
   scripts under `.remedy-wt/f273-r16/`, with names prefixed `wk_` and an explicit `cwd=`. Never
   use `git stash`.
3. Never weaken an assertion, and never delete a test except where the diffs carry that change. A
   red gate, or an ambiguity D16 does not settle -> stop, commit nothing half-done, and report.
4. Build every edited `.agent/` file from `git show b22fe3bc:<path>` bytes.
5. Commit messages read "F273 R16 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/`. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` for real. Never run the `remedy` CLI, `run_job` against this
   repository, `npm install` or the self-use runner. Create no branch and delete no branch.

Done when (G1 to G5 run at C4, before C5; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched. A python check prints True
   for each of these:
   - `.agent/plan.md` equals its payload;
   - `.agent/live_review.md` and `.agent/decisions.md` each equal their `b22fe3bc` bytes +
     ledger.md and decisions.md;
   - each `.agent/authored/f273-r16-*` copy equals its payload;
   - `git show --name-only --format=` of each of C2, C3 and C4 lists exactly the paths
     `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C4>:tests <C4>:packages <C4>:apps <C4>:docs` prints exactly
   59a351fcfd1565731e63d03b2f2c31cc6fee3ddc, 43a6fc081dca24c6284dd5aa0e752677d7af2239,
   c3ce5c3eaf7e2ad5920469e0a197f763f8c46be8 and 82ebd05ea4af375724587e153c0bd49859876257 (the
   reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider` over every
   path in `.remedy-wt/f273-r16/targets.txt` (one per line; read it, never edit it) -> summary
   line, 0 failed, exit 0, and no `R-0803:` line in the output.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree at `.remedy-wt/f273-r16-g5` (detached at C4).
   - Run from its root with `python3 -B -m pytest -q -p no:cacheprovider` and an env carrying
     `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (through the
     script's `env=`).
   - Purge `__pycache__` before each run.
   - First print the imported `packages.orchestration.ui_server` path, to prove it resolves inside
     the worktree.
   - Run the UNMUTATED control first over the four test files named below; it must exit 0.
   - Then run each mutation below. Before each, count its FROM line (with its newline) in the named
     file; the count must be 1. Revert each file from its saved bytes before the next mutation.
     Name the failing ids.
   The test files: U = tests/ui_contracts/test_humanize_catalog.py;
   M = tests/orchestration/test_mission_readiness.py; S = tests/orchestration/test_self_dogfood.py;
   J = tests/orchestration/test_job_evidence.py.
   (a) U itself: `    helpers = forwarding_helpers(tree)` -> `    helpers: Helpers = {}` -> U fails;
   (b) `packages/orchestration/mission_readiness.py`:
   `                     "pending" if inp.unresolved_failures else "skipped",` ->
   `                     "skipped" if inp.unresolved_failures else "pending",` -> M fails;
   (c) the same file: `    human_needed = bool(inp.pending_intents)` -> `    human_needed = False`
   -> M fails;
   (d) `packages/orchestration/self_dogfood.py`: `            source_type="failure_artifact",` ->
   `            source_type="repair_loop",` -> S fails;
   (e) `apps/cli/commands/do_cmd.py`: `    except UnsafeTaskIdError as exc:` ->
   `    except KeyError as exc:` -> J fails.
   Report exit codes and failing ids. If a mutation stays green, report it as green. Then remove the
   worktree as this step's last action and show `git worktree list`.
G6 after the push: `git status --porcelain` is empty and the local tip equals origin. Report this in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
