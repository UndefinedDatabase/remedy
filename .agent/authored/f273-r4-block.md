-- STEP R4 T002 -- F273 Findings paydown v1 --
Session 1 of F273 · round 4 · base `4862e71a` (the round 3 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 3's verdict and three resolutions, land DECISION F273 D4, and build T002's eight
live repairs exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D4 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r4/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 d5ae3067dd4e0d9e21d5034a8e4c088a150f9c9857f9af92d772a8ee58e076ec
  ledger.md            sha256 77e5b0216a45184110a624ad365f131e161244db3b3d0472b45508bcb402fbd4
  decisions.md         sha256 b87345c0618ddfb1f12b4955c71f48e3d1376e6fc097e864e6caf8edcf7497a5
  block.md             this block (save it; report its digest)
CODE — three test-only diffs research helpers built at `4862e71a`, which the reviewer applied in
this order, ran and red-proved in its own worktree. Apply with `git apply`; never retype or edit:
  `.remedy-wt/f273-proto-t002a.diff` sha256 cad88b52c6e646aac7c803e108dfc77cab720e20c9838c229f0ce46d2cccb448
  `.remedy-wt/f273-proto-t002b.diff` sha256 6e88d8d1cf3f027d342ffd453f62bec597bce7a4be795a3d7c2ff0377655b468
  `.remedy-wt/f273-proto-t002c.diff` sha256 3c4ef8a315d86aac75a2b3e60fedaa2fbda1f01fefa40d2e7266ed3a3647ece9

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r4-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `4862e71a` bytes + ledger.md bytes; `.agent/decisions.md` := its `4862e71a` bytes +
   decisions.md bytes.
C2 R-0518, R-0569, R-0649, R-0664 — `git apply .remedy-wt/f273-proto-t002a.diff`.
C3 R-0691, R-0708, R-0734, R-0815 — `git apply .remedy-wt/f273-proto-t002b.diff`.
C4 the six other server-start copies — `git apply .remedy-wt/f273-proto-t002c.diff`.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F273 · round 4 · rounds so far 4" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output; open findings by distinct id (`scripts/rotate_live_review.py::count_open_findings`
   now counts that way) measured on the committed ledger; one `Landed: R-xxxx` line naming its
   commit for each of R-0518, R-0569, R-0649, R-0664, R-0691, R-0708, R-0734 and R-0815, in the
   handoff only — never a `Done:` line anywhere; `## Next` naming Phase 1 rule 1 then the review of
   round 4, and "Operator questions open: <the count you read from the file>". Then `git push`.
   Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, compound commands and `cd`
   before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r4/` with an
   explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test. A red gate or an ambiguity D4 does not settle ->
   stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show 4862e71a:<path>` bytes.
5. Commit messages "F273 R4 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real.
7. A reviewer's disposable worktree `.remedy-wt/f273-r4-dry` exists: never run anything in it.

Done when (G1 to G5 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload and diff digest matched; a python check prints True that
   `.agent/plan.md` equals its payload, that `.agent/live_review.md` and `.agent/decisions.md`
   each equal their `4862e71a` bytes + ledger.md and decisions.md, and that each
   `.agent/authored/f273-r4-*` copy equals its payload.
G2 code transport: `git rev-parse <C4>:tests <C4>:apps <C4>:packages` prints exactly
   f952ccd3491b9516afbe71d2f0cd5e873ff538c5, 669c3a23f24a5dca64f2fc47dbd708c9084a1239 and
   33e5de700300b3644f0e979824eae0edcf526627 (the reviewer's dry-run subtrees; `apps` and
   `packages` are unchanged from `4862e71a`).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_product_smoke.py tests/orchestration/test_dod_runners.py
   tests/orchestration/test_test_runner.py tests/ui_contracts/ tests/ui_server/test_live_state.py
   tests/ui_server/test_command_channel.py tests/ui_server/test_server_start.py
   tests/ui_server/test_server_concurrency.py tests/ui_server/test_digest_route.py
   tests/ui_server/test_decisions_endpoint.py tests/ui_server/test_command_dispatch.py
   tests/ui_server/test_diff_endpoint.py tests/orchestration/test_job_stop_integration.py
   tests/test_no_orphan_modules.py tests/cli/test_golden_path.py` -> summary line, 0 failed,
   exit 0, no `R-0803:` line.
G4 `python3 -m ruff check --output-format concise` over the Python files C2 to C4 touch -> exactly
   the four findings `tests/ui_server/test_live_state.py` carries at `4862e71a` (two I001, two F401,
   at base lines 470, 471 and 505 — five lower after C3), and nothing else; report the full output.
G5 mutation red-proofs in ONE fresh disposable worktree under `.remedy-wt/` at C4, run from its
   root with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run,
   the imported `tests.ui_server.server_start` path printed first to prove it resolves inside the
   worktree. FIRST, before any other run (a ui_server run can auto-build `apps/ui/node_modules` into
   the worktree): `tests/orchestration/test_test_runner.py -k test_vitest_passes` must read 1
   skipped, then with its line `        not (_ROOT / "apps" / "ui" / "node_modules").is_dir(),`
   replaced by `        False,` it must fail. Then the UNMUTATED control over the test files named
   below (exit 0). Then, each reverted before the next, counting the mutated bytes in the named
   file first (each must be 1), and naming the failing ids:
   (a) `tests/orchestration/test_product_smoke.py`: in `write_runtime_config`'s signature
   `port: int | None = None,` -> `port: int | None = 5273,` -> that file fails;
   (b) `tests/ui_contracts/test_humanize_catalog.py`: the line
   `        if "node_modules" not in path.relative_to(base).parts` deleted -> that file fails;
   (c) `apps/ui/src/components/panels/ActivityFeedCard.tsx`: the line
   `                <span className={styles.activityTag}>#{row.seq}</span>` deleted ->
   `tests/ui_contracts/test_brain_stream_ring.py` fails;
   (d) `packages/orchestration/pingpong_loop.py`: in the line holding
   `"reviewer_parse_retry_count": result.reviewer_parse_retry_count,` insert ` + 1` before the
   comma -> `tests/orchestration/test_job_stop_integration.py` fails;
   (e) `tests/ui_server/server_start.py`: `    except json.JSONDecodeError:` ->
   `    except FileNotFoundError:` -> `tests/ui_server/test_server_start.py` fails;
   (f) the same file: `        if not thread.is_alive():` -> `        if False:` ->
   `tests/ui_server/test_server_start.py` fails;
   (g) the same file: `            return info` -> `            pytest.fail("mutant: helper reached")`
   -> each of the seven files `test_live_state.py`, `test_command_channel.py`,
   `test_server_concurrency.py`, `test_digest_route.py`, `test_decisions_endpoint.py`,
   `test_command_dispatch.py` and `test_diff_endpoint.py` under `tests/ui_server/` fails;
   (h) `apps/ui/src/components/panels/DecisionInboxCard.tsx`: `  next.add(answerKey);` ->
   `  next.add("pressed");` -> `tests/ui_contracts/test_decision_answer_wiring.py` fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
