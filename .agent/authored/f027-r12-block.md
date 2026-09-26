STEP F027 R12 — THE CLOSURE'S SECOND REPAIR ROUND: book round 11, resolve R-1071, register and repair R-1072, and take the one full suite again on the repaired tree

GOAL
Round 11 repaired R-1071, and its suite read one other node bad: a live test whose job has no target
of its own, so the runner builds a git worktree of the whole live checkout, which fails under the
full suite's parallel load. That is finding R-1072. Book round 11, resolve R-1071, register R-1072,
repair it in its test file, prove the repaired test under load, and take the feature's one full suite
again on the repaired tree, replacing the transcript at the same path (operator amendment
amend0921-operator-feedback rule 1). This is the second of the three repair rounds amend0917-throughput
rule 2 allows. The evidence bundle and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict, never merge, and never write a `Done:` line: when R-1072's repair lands you append a blank
line and ONE line, `Landed: R-1072 — <one line: what changed>, at this round's C3.`, to
`.agent/live_review.md`. NEVER call `run_job` or any runner yourself outside a test the block names:
a runner started from a checkout of this repository creates branches in it.

THE DIRECTORIES
  `.remedy-wt/f027-r12-payloads/` and `.remedy-wt/f027-r12/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f027-r12-drafts/`, `.remedy-wt/f027-r8-dry/`, `.remedy-wt/f027-review/` and every
  older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r12-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners chained
with `;` or `&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
read `${PIPESTATUS[0]}` when you pipe. Use `git -C <path>`; never `cd` into a worktree. The ONE npm
command this round may run is C5's `npm --prefix apps/ui run build`; never `npm install`, `npm ci` or
`npx`. Never `git stash`, `git commit --amend`, `git branch -d`/`-D`, `pkill -f` or `git worktree
prune`.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f027-task-veto`, `git log --oneline -1` `09276159`.
3. Measure this block's line count and sha256 (`.remedy-wt/f027-r12/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l` and `git for-each-ref refs/heads/remedy/ | wc -l` as found;
   the reviewer read 100 and 195.

PAYLOADS — under `.remedy-wt/f027-r12-payloads/`; verify each BEFORE use and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1079 | 7898c757b7fcf9a23790e781f85b578565fe20ea5e7dcd511327976568ee0710 |
| records.diff | 23 | 8585 | 896bead42fbaa18729ec23078cdbbafa0d0844cf16378d05153c537bf86730ba |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `09276159`)
appends round 11's gate entry, R-1071's `Done:` paragraph and R-1072's registration to
`.agent/live_review.md`, and one line to `.agent/prose_slips.md`.

THE SPECIFICATION OF THE REPAIR
S1 R-1072, in `tests/ui_server/test_pause_door_live.py` alone, as its FIX says: in
   `TestWithdrawLiveDoor.test_a_withdrawn_pause_never_parks_the_relaunch`, before the job is built,
   `target = tmp_path / "repo"` is made and holds `README.md` reading `# demo\n`, exactly as
   `TestJobScopeLiveDoor` makes its own, and the `JobPlan` gains `repo_path=str(target)`, with a
   one-line comment naming R-1072. Nothing else in the file changes. The reviewer ran these steps 48
   times under `pytest -n 16` at `09276159` and read 48 passed, with the shared repository's
   `remedy/` branch count and worktree list unchanged.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f027-r12-block.md` := this block and each payload as
   `.agent/authored/f027-r12-<name>`, by `shutil.copyfile`. Subject `F027 R12 C1: copy round 12 block
   and payloads`. Its insertions are this block's line count plus 53.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject
   `F027 R12 C2: book round 11, resolve R-1071, register R-1072`. Expected by `git show --numstat`:
   6/0 .agent/live_review.md, 7/6 .agent/plan.md, 1/0 .agent/prose_slips.md.
C3 THE REPAIR: S1 and the `Landed: R-1072 — ` line. Subject
   `F027 R12 C3: the withdrawn-pause live test runs its job in a target of its own (R-1072)`.
C4 THE LOAD PROBE `.agent/authored/f027-r12-loadprobe.py` (G4). Subject `F027 R12 C4: the round's
   load probe`.
C5 THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4: (a) `bash -c 'npm
   --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — a failing build is
   a STOP — then `git status --porcelain`, still empty. (b) `python3 -m pytest -n auto -q`, its log
   under `.remedy-wt/f027-r12-worker/`; measure its wall time. REWRITE
   `.agent/authored/f027-closure-suite.txt` whole, in round 11's format, with one line naming the tree
   it ran on (C4's SHA) and saying it replaces round 11's run at `29b0c2d2` under
   amend0921-operator-feedback rule 1. (c) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject
   `F027 R12 C5: record the closure suite on the repaired tree and rewrite handoff for round 12`.
   Then `git push origin feature/f027-task-veto`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f027-r12-*` copies and probe,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `tests/ui_server/test_pause_door_live.py`, `.agent/authored/f027-closure-suite.txt` and
   `.agent/handoff.md`. No edit to `packages/`, `apps/`, any other test, `README.md`, `docs/`,
   `scripts/`, `.agent/decisions.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. The repair must STRICTLY SHRINK the bad set with NO node newly bad (amend0917-throughput rule 2):
   round 11's set is the one live-test node. If C5's suite is red, commit the transcript exactly as
   measured, report every bad node id, and hand back; never weaken an assertion, delete a test or
   mark anything xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip.
6. Leave every existing worktree, branch and stash alone, the 91 branches `remedy/<id>` at
   `09276159` included. The G4 worktree goes under `.remedy-wt/` and is removed after.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
C5 is written; G5 is C5's suite.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f027-r12-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE RECORDS: `git show <C2>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 336967 | fd04ea0e756a5bcbc2d31dcb9574abdcb474e9896eda2af8c73729fdfee51709 |
   | C2 | .agent/prose_slips.md | 370262 | 9e64d4fc87e5491b57df2af5b1bd4b59cf20b6be11a4518a089f5186c6f70050 |
   | C2 | .agent/plan.md | 1079 | 7898c757b7fcf9a23790e781f85b578565fe20ea5e7dcd511327976568ee0710 |
   and `open_finding_ids` over the ledger reads `['R-1072']` at C2 and at C4; the ledger's last line
   at C3 begins `Landed: R-1072 — `.
G3 THE CODE: `python3 -m ruff check tests/ui_server/test_pause_door_live.py` at C3, and
   `git diff 09276159 <C3> -- tests/ui_server/test_pause_door_live.py`, whole.
G4 THE TESTS AND THE LOAD PROOF, at C4. In the primary checkout, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_pause_door_live.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0. Then your probe,
   run against `git worktree add --detach .remedy-wt/f027-r12-load <C4>`: it records the shared
   repository's `git for-each-ref refs/heads/remedy/` count and `git worktree list` count, writes
   INSIDE that worktree a scratch file `tests/ui_server/test_zz_r1072_load.py` whose one test,
   parametrized over 48 values, calls
   `TestWithdrawLiveDoor().test_a_withdrawn_pause_never_parks_the_relaunch(tmp_path, monkeypatch)`
   with pytest's own fixtures, runs it once alone from the worktree's root (the UI server there may
   build its page on first start), then runs all 48 with `python3 -m pytest -q -p no:cacheprovider
   -n 16` from the worktree's root, and prints both summary lines, the two counts again, and a last
   line `LOAD PROOF: 48 passed and nothing leaked: <bool>`. The probe never runs the UNREPAIRED test
   under load: that route creates branches in the shared repository, which G2 of the self-drive
   protocol forbids deleting. Then `git worktree remove --force .remedy-wt/f027-r12-load`, and
   `git worktree list | wc -l` reported.
G5 THE INTEGRATION GATE: the UI build's last line and real exit code, `git status --porcelain` after
   it, the full suite's real exit code, wall time, summary line and every bad node id, all in the
   rewritten `.agent/authored/f027-closure-suite.txt`; whether round 11's bad node passes; and whether
   any node is newly bad.
G6 AFTER C5 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f027-task-veto`, `git log --oneline -n 6`, `git worktree list | wc -l`,
   `git for-each-ref refs/heads/remedy/ | wc -l`, the push's real outcome, and `gh pr list --state
   open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the full suite's summary line and bad node ids, the authored-text
proofs, the item-status table AGENTS.md requires (one row per commit, per gate and per S-item), the
deviations, and the next action. Session section: SESSION 2 of feature F027, round 12, plus one
sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of round 12, then
the closure's evidence round — the booking of round 12, the Built State's note on the findings raised
after it, the evidence bundle and the review package — and then the closing round. State the
open-findings count as the script reads it at C4, and "Operator questions open: 5".
