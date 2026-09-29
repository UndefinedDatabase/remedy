STEP F042 R8 — THE FIRST CLOSURE REPAIR ROUND: book round 7, repair R-1112, and run the feature's full suite again

GOAL
Round 7 is reviewed PASS at `c83be2032`. Its one full suite stopped at collection and ran no test:
`tests/ui_server/test_projects_route.py` line 111 draws `str(uuid4())` for a parametrize id, so
every pytest-xdist worker collects a different id and xdist refuses the run. This round books
round 7 with R-1107's resolution and registers that defect as R-1112, repairs it with a fixed uuid
and a repository test that refuses a fresh value in any parametrize argument, and runs the full
suite again on the repaired tree (amend0917-throughput rule 2, repair round 1 of at most 3). The
evidence bundle, the review package, the rotation, the STATUS line and the pull request belong to
later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line of your own. Every change
this round makes travels as a payload. Read `docs/roadmap/STATUS_closure_protocol.md` preconditions
3 and 7 and `docs/agents/integration_gate.md` first, and read
`tests/ui_server/test_projects_route.py` whole before C3.

THE DIRECTORIES
  `.remedy-wt/f042-r8-payloads/` and `.remedy-wt/f042-r8/`  READ-ONLY. The reviewer's.
  every other `.remedy-wt/f042-*` path: the reviewer's; do not touch.
  `.remedy-wt/f042-r8-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, `ln`, `sed`, process and command substitution, `cd <dir> && ...`, `for` loops, and one-liners
chained with `;` or `&&` outside a `bash -c`. Capture exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use
`git -C <path>`; never `cd` into a worktree. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`); run a program in another directory with `subprocess.run(..., cwd=...)`.
Never run npm or npx. Never `git stash`, never `git commit --amend`, never `pkill -f`: stop a
process only by its own recorded pid. The `remedy` command may be denied; use
`python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f042-multi-project-cockpit`, `git log --oneline -1`
   `c83be2032`.
3. Measure this block's line count and sha256 (`.remedy-wt/f042-r8/block.md`) against your
   delegation message's readings; report both beside both, and stop if either differs.
4. Report `git worktree list | wc -l` as found, and that `apps/ui/dist/index.html` exists (round 7
   built it; the suite needs it).

PAYLOADS — under `.remedy-wt/f042-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 14 | 8267 | 46881abfaef65f24ae9cd788fa7b4c6ef8cefe3263fa4ed36884615344a088b1 |
| plan.md | 29 | 1018 | 620f83cfc5c61914c80314a935209ba58924e8f60d7e0b6fd28bae3d01c76082 |
| fix.diff | 98 | 3607 | b65865d024bd2637d9465457c00c04ffba0e816ba3eb883cbc2e6ccccee0a254 |

`plan.md` REWRITES `.agent/plan.md`. The two diffs were generated from the reviewer's simulation
tree at `c83be2032` and go on with `git apply`, in the order C2 and C3 name. `records.diff`
appends to `.agent/live_review.md` round 7's gate entry, VERDICT PASS, R-1107's `Done:`
resolution and R-1112's registration. `fix.diff` gives `test_an_unknown_project_is_404` a fixed
uuid under a comment naming R-1112, drops the now unused `uuid4` import, and adds the NEW FILE at
`tests/test_parametrize_ids_stable.py`.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f042-r8-block.md` := this block and each payload as
   `.agent/authored/f042-r8-<name>`, by `shutil.copyfile`. Subject `F042 R8 C1: copy round 8
   block and payloads`. Its insertions are this block's line count plus 141; STOP rather than
   commit at 500 or more.
C2 RECORDS: `git apply --check` then `git apply` records.diff, then `.agent/plan.md` := plan.md.
   Subject `F042 R8 C2: book F042 R7 with R-1107's resolution, register R-1112`. Expected by
   `git show --numstat`: 6/0 .agent/live_review.md, 8/8 .agent/plan.md.
C3 THE REPAIR: `git apply --check` then `git apply` fix.diff. Subject `F042 R8 C3: give the
   unknown-project test a fixed uuid and refuse fresh values in parametrize arguments (R-1112)`.
   Expected by `git show --numstat`: 70/0 tests/test_parametrize_ids_stable.py, 2/2 tests/ui_server/test_projects_route.py.
C4 THE SUITE, in the PRIMARY checkout, after C3 and after G1 to G3. (a) `python3 -m pytest -n
   auto -q`, its log under `.remedy-wt/f042-r8-worker/`; measure its wall time. (b) REWRITE
   `.agent/authored/f042-closure-suite.txt` (round 7's transcript stays in git history) holding the
   command, the real exit code, the wall time, the summary line, the FULL list of bad node ids
   (failed plus errors) or the literal `NONE`, the previous bad set (round 7's 15 xdist collection
   errors) with whether the new set is strictly smaller and holds no newly bad node, and one line
   naming the tree it ran on (C3's SHA). After the suite, report the processes
   `ps -eo pid,args | grep "[s]erver.py"` lists, which must be none. (c) Rewrite
   `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with the
   transcript. Subject `F042 R8 C4: record the repaired tree's suite transcript and rewrite handoff
   for round 8`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f042-r8-*` files, `.agent/live_review.md`,
   `.agent/plan.md`, `tests/ui_server/test_projects_route.py`,
   `tests/test_parametrize_ids_stable.py`, `.agent/authored/f042-closure-suite.txt` and
   `.agent/handoff.md`. Report `git diff --name-only c83be2032` at the tip. No other file.
4. A RED full suite in C4 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the next repair round is the reviewer's to
   order. Never weaken an assertion, delete a test, skip or mark anything xfail, and never repair
   a suite node yourself. An EXISTING test that goes red before C4 is never edited to pass; report
   it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no amend; no evidence job; no
   zip; no self-use runner and no job that calls a provider.
6. Leave every existing worktree, branch and stash alone, the reviewer's included. The worktree G3
   adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
7. The full suite runs ONCE this round, in C4, and nowhere else.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding. G1 to G3 run before C4 is written; G4 is C4's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f042-r8-*` copy byte-equal to its source by `git show <C1>:<path>`; and
   `git show <read at>:<path>` of each file below hashes to the reviewer's tree:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 156592 | 15798fc88e86a3efacd01a15fcfad33ff72634f2bd36e38f21c75f430bb01983 |
   | C2 | .agent/plan.md | 1018 | 620f83cfc5c61914c80314a935209ba58924e8f60d7e0b6fd28bae3d01c76082 |
   | C3 | tests/ui_server/test_projects_route.py | 7400 | fc17dfb06721aa93321f98bdf38d76ceaab5e5b3f30c094c10acb4251069e23f |
   | C3 | tests/test_parametrize_ids_stable.py | 2329 | 466c34d24b3923cebfa21ac4bf5fa4c119bbe99326a30b19f87a26b4697c8547 |
   `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the ledger
   at C2 read `['R-1112']` and `PASS`.
G2 THE TESTS, in the primary checkout at C3, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_parametrize_ids_stable.py tests/ui_server/test_projects_route.py tests/docs tests/cli/test_golden_path.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py 2>&1 | tail -4; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — the reviewer read `448 passed` at exit 0 in its simulation tree. Then the same two files the
   defect lives in under xdist:
   `bash -c 'python3 -m pytest -n 4 -q -p no:cacheprovider tests/ui_server/test_projects_route.py tests/test_parametrize_ids_stable.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — the reviewer read `13 passed` at exit 0. `python3 -m ruff check
   tests/test_parametrize_ids_stable.py tests/ui_server/test_projects_route.py`, its real exit code.
   Then `python3 -m apps.cli.main integrity check --json`: six `pass` at `fail_count` 0; then
   `python3 -m apps.cli.main integrity block .remedy-wt/f042-r8/block.md`, real exit code and whole
   output; and `git status --porcelain` empty.
G3 THE RED PROOF OF R-1112'S REPAIR: `git worktree add --detach .remedy-wt/f042-r8-mut <C3>`; in
   it, `git -C .remedy-wt/f042-r8-mut checkout <C2> -- tests/ui_server/test_projects_route.py`
   (the file before the repair, the new test kept); then, with the worktree as the working
   directory and first on `PYTHONPATH` (set in-process from Python), run (i)
   `python3 -B -m pytest -q -p no:cacheprovider tests/test_parametrize_ids_stable.py` — must read
   1 failed, 1 passed, its assertion naming `tests/ui_server/test_projects_route.py:111: uuid4()`;
   and (ii) `python3 -B -m pytest -n 2 -q -p no:cacheprovider tests/ui_server/test_projects_route.py`
   — must exit non-zero with xdist's `Different tests were collected` error. Then restore with
   `git -C .remedy-wt/f042-r8-mut checkout <C3> -- tests/ui_server/test_projects_route.py` and run
   (i) and (ii) again as controls, both at exit 0. Report every exit code and summary line; then
   `git worktree remove --force .remedy-wt/f042-r8-mut`, `git worktree prune`, and
   `git worktree list | wc -l`.
G4 THE SUITE: its real exit code, wall time, summary line and every bad node id, all in
   `.agent/authored/f042-closure-suite.txt`; the shrink reading against round 7's set; the
   `server.py` reading; and whether `tests/orchestration/test_import_reachability.py` or
   `tests/test_no_orphan_modules.py` holds a bad node (closure precondition 7).
G5 AFTER C4 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f042-multi-project-cockpit`, `git log --oneline -n 5`,
   `git worktree list | wc -l`, the push's real outcome, and `gh pr list --state open --json number`
   EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next action. Session section: SESSION 2 of feature F042, round 8, rounds so
far 8, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of
round 8 and of its suite transcript, then either the next repair round (if the suite is red) or
the closure's evidence round — the booking of round 8, the reclaim of staging copies, the evidence
bundle and the review package — and then the closing round. State the open-findings count, 1, and
"Operator questions open: 0".
