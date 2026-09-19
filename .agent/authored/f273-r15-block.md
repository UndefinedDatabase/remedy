-- STEP R15 intent truth, manifest diff, conventions -- F273 Findings paydown v1 --
Session 2 of F273 · round 15 · base `bce5bc3b` (the round 14 handoff, branch
`feature/f273-findings-paydown-v1`). This is the session's last round.

Goal: book round 14's verdict and six resolutions, land DECISION F273 D15, and build R-0990, R-0931
and R-0981 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D15 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r15/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 7225f1e14ceada67d4986880276d5c05e455fcc2b31f6a14087ca4336671555c
  ledger.md            sha256 6b31df1b228d18483bf2f2b2d62c8e2308a8355250385975bc195e086ee1fd43
  decisions.md         sha256 d85a95ca2e94fe67c467cfdc8af12ddec91c4ee2496962834f55239363de6685
  next.md              sha256 128f8a562c29ea5ecb0b4707bb794bcdd8a79d57a96f9cfa923a78dcf136ef31
  block.md             this block (save it; report its digest)
CODE — diffs research helpers built, which the reviewer applied in this order at `bce5bc3b`, ran
and red-proved in its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g6a.diff` sha256 01ca51c761478f6ae93e46dc4d6dde0ce21594ba6b23e4a2f9db245a38c92818
  `.remedy-wt/f273-proto-g6c.diff` sha256 73a5190aa019ae9302ec2ac1e6c8602fec5d84785c32a60c259d4aa3650777bf
Do NOT apply `f273-proto-g6b.diff`, `f273-proto-g6d.diff` or `f273-proto-g6e.diff` (held, D15 (4)).

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of plan.md, ledger.md, decisions.md and
   block.md as `.agent/authored/f273-r15-<name>`; `.agent/plan.md` := plan.md;
   `.agent/live_review.md` and `.agent/decisions.md` := each one's `bce5bc3b` bytes + ledger.md and
   decisions.md respectively.
C2 R-0990 — `git apply` g6a.diff.
C3 R-0931, R-0981 — `git apply` g6c.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched,
   deletions included; nothing may be left untracked or unstaged.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 2 of feature F273 · round 15 · rounds so far 15" plus one sentence of context
   self-assessment and the sentence "Session 2 ran rounds 8 to 15, eight delegated rounds, the top
   of the six-to-eight target; it ends here with the held rulings of DECISION F273 D15 (4) for a
   fresh session."; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0990, R-0931 and R-0981, in the handoff only
   — never a `Done:` line of your own; a `## Next` section whose body is next.md byte for byte,
   followed by the line "Operator questions open: <the count you read from the file>". Then
   `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`) and `cd` before git; use `git -C <path>` and small python scripts under
   `.remedy-wt/f273-r15/` (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D15 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show bce5bc3b:<path>` bytes.
5. Commit messages "F273 R15 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` for real, never run the `remedy` CLI, `run_job` against this
   repository, `npm install` or the self-use runner, and create no branch.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `bce5bc3b` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r15-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 each lists exactly the paths `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:apps <C3>:docs` prints exactly
   38e2208d66688abbec594b93386cba273d0dd0e9, 585f2e6af040f657dc8a9dba41855c3b67f1ef01,
   afdc344919dba92cc79ae5ac8dbb42bc727673fb and 27c3ec810bbb894664d66d6aeea7e28206d32c2e (the
   reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider` over every
   path listed in `.remedy-wt/f273-s2/r15_control.txt` and in `.remedy-wt/f273-s2/r15_extra.txt`
   (one per line; read them, never edit them; sha256 b25d7f3c6237c709f7b35f5e42acb911d2f20b7e3259c28310435e6304d49b44
   and 38ad2b2c43efc4f7b65e1b01f080b15bc0201d3a6f449f93d47cf6942420eff6) -> summary line, 0 failed,
   exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider` and an env carrying
   `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (through the
   script's `env=`), `__pycache__` purged before each run, the imported
   `packages.orchestration.run_manifest` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted from its saved bytes before the next, counting each FROM line (with its newline) in
   the named file first (each must be 1), naming the failing ids. S =
   tests/cli/test_product_spine.py; D = tests/orchestration/test_conventions_documents.py.
   (a) `apps/cli/commands/job.py`: `    patch_intent_ids = [i['intent_id'] for i in intents]` ->
   `    patch_intent_ids = [i['artifact_id'] + '-0' for i in intents]` -> S fails;
   (b) the same file: `        if i['state'] == APPROVAL_PENDING and i['intent_id'] not in applied_ids`
   -> `        if i['intent_id'] not in applied_ids` -> S fails;
   (c) the same file: `                if not code_applied and not intents:` ->
   `                if not code_applied:` -> S fails;
   (d) `docs/agents/teacher_conventions.md`: `## Stance` -> `## Posture` -> D fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
