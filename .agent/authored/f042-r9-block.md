STEP F042 R9 — THE SECOND CLOSURE REPAIR ROUND: book round 8, repair R-1113, and run the feature's full suite again

GOAL
Round 8 is reviewed PASS at `2c8f1a5d0`. Its full suite ran every test and read one failure:
`tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises`, 291 excused blind
handlers against the frozen 290. The 291st is `packages/orchestration/project_cockpit.py` line
180, an `except Exception` this feature added in round 1. This round books round 8 with R-1112's
resolution and registers that handler as R-1113, narrows it to the two ways reading a run log
fails, adds the tests that hold both ways and the error that must pass through, and runs the full
suite again on the repaired tree (amend0917-throughput rule 2, repair round 2 of at most 3).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line of your own. The records
travel as payloads; the code change is YOURS to write from the clauses S1 and S2 below. Read
`packages/orchestration/project_cockpit.py`, `packages/orchestration/timeline.py`'s
`load_run_events`, `tests/orchestration/test_project_cockpit.py` and `tests/test_ble001_ratchet.py`
whole before C3.

THE DIRECTORIES
  `.remedy-wt/f042-r9-payloads/` and `.remedy-wt/f042-r9/`  READ-ONLY. The reviewer's.
  every other `.remedy-wt/f042-*` path: the reviewer's; do not touch.
  `.remedy-wt/f042-r9-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, `ln`, `sed`, process and command substitution, `cd <dir> && ...`, `for` loops, and one-liners
chained with `;` or `&&` outside a `bash -c`. Capture exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use
`git -C <path>`; never `cd` into a worktree. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`); write any script holding a dollar-brace or a brace next to a quote to
a file under your own directory and run it; run a program in another directory with
`subprocess.run(..., cwd=...)`. Never run npm or npx. Never `git stash`, never
`git commit --amend`, never `pkill -f`. The `remedy` command may be denied; use
`python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f042-multi-project-cockpit`, `git log --oneline -1`
   `2c8f1a5d0`.
3. Measure this block's line count and sha256 (`.remedy-wt/f042-r9/block.md`) against your
   delegation message's readings; report both beside both, and stop if either differs.
4. Report `git worktree list | wc -l` as found, and that `apps/ui/dist/index.html` exists.

PAYLOADS — under `.remedy-wt/f042-r9-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 14 | 7045 | 34d95904a0567279bfd96e0f2e95f85bc30f2e0122416c750757d8475e093d33 |
| plan.md | 29 | 1020 | cf269dfbf77d1b43e79f6317acf8f0c6e02046bd995d7b590c30b71f83a52b31 |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` was generated from the reviewer's simulation
tree at `2c8f1a5d0` and appends to `.agent/live_review.md` round 8's gate entry, VERDICT PASS,
R-1112's `Done:` resolution and R-1113's registration.

THE CLAUSES — the change C3 makes, and nothing else.
S1 In `project_summary` of `packages/orchestration/project_cockpit.py`, the handler around
   `load_run_events` and `build_decision_inbox` becomes exactly
   `        except (OSError, ValueError):  # R-1113: an unreadable job's inbox is skipped, never the card`
   — no `noqa` mark; the body stays `continue`. No other line of the module changes, and
   `MAX_EXCUSED` in `tests/test_ble001_ratchet.py` stays 290.
S2 In `tests/orchestration/test_project_cockpit.py`, class `TestProjectSummary`, directly before
   `test_the_open_count_is_the_one_remedy_status_prints`, two tests using the file's `world`
   fixture, `NOW` and its existing imports:
   (a) `test_an_unreadable_jobs_run_log_is_skipped_never_the_card`, parametrized over `damage` in
       `["undecodable", "directory"]`: the `a_run` job's `events.jsonl` under
       `run_log_dir(str(job.job_id), resolve_data_root())` is overwritten with bytes that are not
       UTF-8 (`b"\xff\xfe not utf-8\n"`), or unlinked and made a directory of the same name; the
       expected decisions are computed as the neighbouring test does, over `a_old` and `a_new`
       only; the test holds that `project_summary(world["alpha"], now=NOW)["decisions"]` equals
       that expectation, differs from `{"open_count": 5, "peak_urgency": 3600}`, and that
       `["jobs"]["total"]` is still 3.
   (b) `test_an_unexpected_error_in_the_inbox_is_not_swallowed`: `monkeypatch.setattr` replaces
       `build_decision_inbox` on the module `packages.orchestration.decision_inbox` with a function
       raising `RuntimeError("inbox bug")`, and `pytest.raises(RuntimeError, match="inbox bug")`
       holds around `project_summary(world["alpha"], now=NOW)`.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f042-r9-block.md` := this block and each payload as
   `.agent/authored/f042-r9-<name>`, by `shutil.copyfile`. Subject `F042 R9 C1: copy round 9
   block and payloads`. Its insertions are this block's line count plus 43.
C2 RECORDS: `git apply --check` then `git apply` records.diff, then `.agent/plan.md` := plan.md.
   Subject `F042 R9 C2: book F042 R8 with R-1112's resolution, register R-1113`. Expected by
   `git show --numstat`: 6/0 .agent/live_review.md, 6/6 .agent/plan.md.
C3 THE REPAIR: S1 and S2. Subject `F042 R9 C3: narrow the project card's inbox handler to the
   failures of reading a run log (R-1113)`. Expected: 1/1 in `project_cockpit.py`, and the test
   file's insertions at about 30 with 0 deletions; report both.
C4 THE TOOL: your mutation tool (G3) saved as `.agent/authored/f042-r9-mutations.py`. Subject
   `F042 R9 C4: add the round 9 mutation tool`.
C5 THE SUITE, in the PRIMARY checkout, after C4 and after G1 to G3. (a) `python3 -m pytest -n
   auto -q`, its log under `.remedy-wt/f042-r9-worker/`; measure its wall time. (b) REWRITE
   `.agent/authored/f042-closure-suite.txt` holding the command, the real exit code, the wall
   time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
   `NONE`, the previous bad set (round 8's one node) with whether the new set is strictly smaller
   and holds no newly bad node, and one line naming the tree it ran on (C4's SHA). After the
   suite, report what `ps -eo pid,args | grep "[s]erver.py"` lists, which must be nothing. (c)
   Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with
   the transcript. Subject `F042 R9 C5: record the repaired tree's suite transcript and rewrite
   handoff for round 9`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f042-r9-*` files, `.agent/live_review.md`,
   `.agent/plan.md`, `packages/orchestration/project_cockpit.py`,
   `tests/orchestration/test_project_cockpit.py`, `.agent/authored/f042-closure-suite.txt` and
   `.agent/handoff.md`. Report `git diff --name-only 2c8f1a5d0` at the tip. No other file.
4. A RED full suite in C5 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back. Never weaken an assertion, delete a test,
   skip or mark anything xfail, and never repair a suite node yourself. An EXISTING test that
   goes red before C5 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no amend; no evidence job; no
   zip; no self-use runner and no job that calls a provider.
6. Leave every existing worktree, branch and stash alone, the reviewer's included. The worktree G3
   adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
7. The full suite runs ONCE this round, in C5, and nowhere else.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding. G1 to G3 run before C5 is written; G4 is C5's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f042-r9-*` payload copy byte-equal to its source by `git show <C1>:<path>`; and
   `git show <read at>:<path>` of each file below hashes to the reviewer's tree:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 161251 | d7204668204d96dde35bff7e45b3eefd5043b2daed153e53d34138e5860f1a53 |
   | C2 | .agent/plan.md | 1020 | cf269dfbf77d1b43e79f6317acf8f0c6e02046bd995d7b590c30b71f83a52b31 |
   `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the ledger
   at C2 read `['R-1113']` and `PASS`.
G2 THE TESTS, in the primary checkout at C4, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_project_cockpit.py tests/orchestration/test_project_summary.py tests/ui_server/test_projects_route.py tests/ui_server/test_pipeline_contract.py tests/test_ble001_ratchet.py tests/test_parametrize_ids_stable.py tests/cli/test_golden_path.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — the reviewer read `191 passed` at exit 0 in its dry tree carrying its own writing of S1 and
   S2. `python3 -m ruff check packages/orchestration/project_cockpit.py
   tests/orchestration/test_project_cockpit.py .agent/authored/f042-r9-mutations.py`, its real
   exit code. `git grep -c "noqa: BLE001" -- packages/orchestration/project_cockpit.py`, which
   must print nothing and exit 1. Then `python3 -m apps.cli.main integrity check --json`: six
   `pass` at `fail_count` 0; then `python3 -m apps.cli.main integrity block
   .remedy-wt/f042-r9/block.md`, real exit code and whole output; and `git status --porcelain`
   empty.
G3 THE RED PROOFS OF R-1113'S REPAIR: your tool `.agent/authored/f042-r9-mutations.py` takes a
   worktree path, and for each mutation below edits `packages/orchestration/project_cockpit.py`
   INSIDE that worktree (asserting its FROM text occurs exactly once there), runs
   `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_project_cockpit.py` with
   the worktree as the working directory and first on `PYTHONPATH`, restores the bytes, and prints
   its label, exit code, failed count and the FAILED node ids, with an unmutated control first and
   last, `restored byte-identical: True` after each restore, and a last line
   `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
    m1 the handler catches `Exception` again — the reviewer's probe failed (b) alone;
    m2 the handler catches `OSError` alone — failed (a)'s `undecodable` case alone;
    m3 the handler catches `ValueError` alone — failed (a)'s `directory` case alone.
   Run it on `git worktree add --detach .remedy-wt/f042-r9-mut <C4>` and report its whole output;
   then `git worktree remove --force .remedy-wt/f042-r9-mut`, `git worktree prune`, and
   `git worktree list | wc -l`.
G4 THE SUITE: its real exit code, wall time, summary line and every bad node id, all in
   `.agent/authored/f042-closure-suite.txt`; the shrink reading against round 8's set; the
   `server.py` reading; and whether `tests/orchestration/test_import_reachability.py` or
   `tests/test_no_orphan_modules.py` holds a bad node (closure precondition 7).
G5 AFTER C5 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f042-multi-project-cockpit`, `git log --oneline -n 6`,
   `git worktree list | wc -l`, the push's real outcome, and `gh pr list --state open --json number`
   EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next action. Session section: SESSION 2 of feature F042, round 9, rounds so
far 9, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of
round 9 and of its suite transcript, then either the last repair round (if the suite is red) or
the closure's evidence round — the booking of round 9, the reclaim of staging copies, the evidence
bundle and the review package — and then the closing round. State the open-findings count, 1, and
"Operator questions open: 0".
