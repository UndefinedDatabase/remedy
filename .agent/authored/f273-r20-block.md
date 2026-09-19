-- STEP R20 T015: direct-API usage, CI stage coverage, vitest ceiling -- F273 Findings paydown v1 --
Session 3 of F273 · round 20 · base `fdece9ab` (the round 19 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 19's verdict and fourteen resolutions, register T015's three ids R-0994, R-0995 and
R-0996, land DECISION F273 D20, and build T015 exactly as the reviewer's dry run built it.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D20, this round's spec;
where this block is terser, it rules).

PAYLOADS: reviewer-authored, gitignored scratch. Verify each sha256 before use; any mismatch ->
stop and report. Apply byte-exact; never retype.
  `.remedy-wt/f273-r20/plan.md`        sha256 258e1a798fcb0f97018c537b9fef8d49a9ae09f9275e6753c9ea7b0d31d65f2f
  `.remedy-wt/f273-r20/ledger.md`      sha256 fb9506a48783fb00a5ecb2d1ddf16299fe3235decff6f6d53b7c7e2659243172
  `.remedy-wt/f273-r20/decisions.md`   sha256 108331345a42960d18425d581c07216320e6cf83b29c579493611e9e8015a2ed
  `.remedy-wt/f273-r20/next.md`        sha256 93aa65586e17bbb741f36b0beb8e29385e1778606bee31c2aec86427fd0d2758
  `.remedy-wt/f273-s3/r20_targets.txt` sha256 45d419f87ca105b892b6dc75dcac9d13dfeb177c7a644a4b1e4b3043d2cd928b
  `.remedy-wt/f273-r20/block.md`       this block (save it; report its sha256 and line count)
CODE: diffs the reviewer applied in this order at `fdece9ab`, then ran and red-proved in its own
worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g10a.diff`  sha256 148dc01d5b11e57e0350b133168a1c4b19160123159e858b8d62bd3da46d6ef0
  `.remedy-wt/f273-proto-g10b.diff`  sha256 07cd9b065436b7c74dbc3818a0b444a074ff475ac5daef8279f8c38ea64249c2
  `.remedy-wt/f273-proto-g10c2.diff` sha256 01704b7ab94d5a3c2bf9de58512d1acba65f6c6c94248b7c39167d87d53f156d
  `.remedy-wt/f273-s3/r20_docs.diff` sha256 1aee22e7d05c9b9df45e39c97a657d79da6a6c994b1a70ba3d32d8afe79f735b
Apply no other `.remedy-wt/*.diff` file (in particular not `f273-proto-g10c.diff`).

Bundle (commit order):
C1 bookkeeping, one commit holding exactly:
   - byte copies of plan.md, ledger.md, decisions.md and block.md as `.agent/authored/f273-r20-<name>`;
   - `.agent/plan.md` := plan.md;
   - `.agent/live_review.md` and `.agent/decisions.md` := each one's `fdece9ab` bytes + ledger.md and
     decisions.md respectively.
   Before this commit, compare the saved block copy's line count and sha256 with the block text you
   were given, and report both.
C2 R-0994: `git apply` g10a.diff.
C3 R-0995: `git apply` g10b.diff.
C4 R-0996: `git apply` g10c2.diff.
C5 T015's record of its ids: `git apply` r20_docs.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched, new
   files included; nothing may be left untracked or unstaged.
C6 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 3 of feature F273 · round 20 · rounds so far 20", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C5, every
   gate's real output, and open findings by distinct id (`count_open_findings`) on the committed
   ledger. Add one `Landed: R-xxxx` line naming its commit for each of R-0994, R-0995 and R-0996, in
   the handoff only; never write a `Done:` line of your own. Record under External actions that the
   branch `remedy/job-81ec65896729405c` still exists; a research helper's probe created it before
   round 16, and nobody may delete it without the operator. End with a `## Next` section whose body
   is next.md byte for byte, followed by the line "Operator questions open: <the count you read from
   the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test may call a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`), heredocs and `cd` before git. Use `git -C <path>` and small python
   scripts under `.remedy-wt/f273-r20/`, with names prefixed `wk_` and an explicit `cwd=`. Copy a
   file with python, never with `cp`. Never use `git stash`.
3. Never weaken an assertion, and never delete a test except where the diffs carry that change. A
   red gate, or an ambiguity D20 does not settle -> stop, commit nothing half-done, and report.
4. Build every edited `.agent/` file from `git show fdece9ab:<path>` bytes.
5. Commit messages read "F273 R20 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/`. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` yourself. Never run the `remedy` CLI, `run_job` against this
   repository, `npm install` or the self-use runner. Create no branch and delete no branch.

Done when (G1 to G5 run at C5, before C6; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched. A python check prints True
   for each of these:
   - `.agent/plan.md` equals its payload;
   - `.agent/live_review.md` and `.agent/decisions.md` each equal their `fdece9ab` bytes + ledger.md
     and decisions.md;
   - each `.agent/authored/f273-r20-*` copy equals its payload;
   - `git show --name-only --format=` of each of C2, C3, C4 and C5 lists exactly the paths
     `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse` of `<C5>:tests`, `<C5>:packages`, `<C5>:apps`, `<C5>:docs`,
   `<C5>:scripts` and `<C5>:pyproject.toml` prints exactly 6f36fc30471e00a9386dfae2ae930066bf5b2513,
   d11bd01647593af33f1184ce7978e6846e6b76e8, 39a6be279a37193ae0ebcf00d97cadb542da960f,
   84b927c29a16a08a98ab396bc690011037d89d01, 866c1b06bafcedd6f4cca87b588dccae60d37531 and
   ef1bd103cd0c13235a1e8dfd3cc4c40734d3da62 (the reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider` over every
   path in `.remedy-wt/f273-s3/r20_targets.txt` (one per line; read it, never edit it), through a
   script whose `env=` drops `REMEDY_OLLAMA_HOST` and `OLLAMA_HOST` -> summary line, 0 failed,
   exit 0, and no `R-0803:` line in the output.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree at `.remedy-wt/f273-r20-g5` (detached at C5).
   - Run from its root with `python3 -m pytest -q -p no:cacheprovider` and an env carrying
     `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (through the
     script's `env=`).
   - Purge `__pycache__` before each run.
   - First print the imported `packages.orchestration.pingpong_provider` path, to prove it resolves
     inside the worktree.
   - Run the UNMUTATED control first over the three test files named below; it must exit 0.
   - Then run each mutation below. Before each, count its FROM line (with its newline) in the named
     file; the count must be 1. Revert each file from its saved bytes before the next mutation.
     Name the failing ids.
   The test files: A = tests/orchestration/test_pingpong_provider_claude_api.py;
   P = tests/orchestration/test_prompt_segments.py; V = tests/orchestration/test_ci_stage_coverage.py.
   (a) `packages/orchestration/pingpong_provider.py`: `            request["system"] = system` ->
   `            pass` -> A fails;
   (b) the same file: `        head += f" (HTTP {status})"` -> `        pass` -> A fails;
   (c) the same file: delete the line `    shaped["parse_source"] = "anthropic_api"` -> A fails;
   (d) `packages/orchestration/prompt_segments.py`:
   `            if entry.rank >= SegmentStabilityRank.TASK:` ->
   `            if entry.rank > SegmentStabilityRank.TASK:` -> A fails (run A and P);
   (e) V itself: `    covering = [s for s in CI_STAGES if s.runs_in_ci or s.manual_command.strip()]` ->
   `    covering = [s for s in CI_STAGES if s.runs_in_ci]` -> V fails.
   Report exit codes and failing ids (the first six per mutation are enough, plus the count). If a
   mutation stays green, report it as green. Then remove the worktree as this step's last action and
   show `git worktree list`.
G6 after the push: `git status --porcelain` is empty, the local tip equals origin, and
   `git branch --list "remedy/job-*"` still counts 37. Report this in your final message only, since
   the handoff commit precedes it.
Full suite: NOT run in this round (the integration-gate round follows).
-- end of block --
