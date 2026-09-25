STEP F020 R5 — T003 SECOND HALF: the conformance probes over the matrix fixture's pixels, judged against the binding spec in a headless harness

GOAL
Book round 4's PASS and record DECISION F020 D5, then land the second half of T003:
`apps/ui/src/components/graph/renderers/glyphConformance.ts`, which places a pixel probe on
every discriminating detail of every matrix cell — the status dot and its outline, the strike and
its outline, the planned ring — and on every place the dot and the strike must NOT be, with the
binding spec it judges against and the pixel judge; its vitest tests; and the committed headless
harness `.agent/authored/f020-r5-conformance_*` that paints the matrix with the live painter,
reads each probe's pixel and applies the judge. Its transcript is committed as the evidence.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f020-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f020-r5/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f020-r5-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f020-r5-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f020-r5-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored. The harness also makes and removes its own work
                                  dir, `.remedy-wt/f020-conformance-run`, under the tree it runs on.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Never run npm or npx; the harness
runs the primary checkout's installed `vite` binary and `/usr/bin/google-chrome` itself.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f020-node-lifecycle-glyph-language`, and `git log --oneline -1` must read
   `106df185`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f020-r5/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f020-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| book.diff | 58 | 11570 | 651525a6621e886722910faf98992ddc49fd9aaf4661c19696a721120d552959 |
| conformance_drive.mjs | 79 | 3145 | 71bfca163f677088315a623242874588666ceb049da55d6760dadf4986981e74 |
| conformance_index.html | 10 | 202 | 941439e425ecc1554e6ca5daadd5b47476ae85eba1d7c5c6b821b62cd3e104a6 |
| conformance_main.tsx | 46 | 2186 | d287fefb13acb92c1d8a3a999d472780b16ecbb34475ccb08ad1333dda017a7b |
| conformance_measure.py | 190 | 6529 | 34b1e5c3cfffb16d657f2e7e7fa8224f86afcc8f87705bc1345e2a0bc96f4d34 |
| conformance_vite.config.mjs | 28 | 775 | e072fd9ed0ee4eb0efc58a396c8c2149ae64f9235313f28543081897de8f09f8 |
| glyphConformance.test.ts | 130 | 6597 | 844d757a1398b77ff7bd1674a2be65ec06087d61ec15a429d575b5aae3bf280d |
| glyphConformance.ts | 146 | 7207 | bb9731ebce8b857cbef6198fca8189277e5a5880352aff1f6e08879ad5903436 |
| harness_redproof.py | 70 | 3651 | 4169214620acf737c668d4b90d8f6dbdef70af9364eb7175980f787222215e43 |
| mutations.py | 163 | 7894 | a24543f8bf80ea3c3a6c2b70058392524beeb0655ec0c0f0625d3f88748e66ea |
| plan.md | 32 | 1169 | e4bc66c01f99a95f829b9e0a8dd581471cccb42de7b246df8c2e9d720e193448 |

`plan.md` is a REWRITE of `.agent/plan.md`. `glyphConformance.ts` and `glyphConformance.test.ts`
are NEW FILES under `apps/ui/src/components/graph/renderers/`, each copied whole. `book.diff` goes
on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at `106df185` into
which it wrote the edits, and it appends round 4's gate entry to `.agent/live_review.md` and
DECISION F020 D5 to `.agent/decisions.md`. The five `conformance_*` payloads are the harness: their
committed copies under `.agent/authored/` ARE the tool, found by `f020-r5-conformance_measure.py`
through its own file-name prefix, and nothing else is built from them. `mutations.py` and
`harness_redproof.py` are TOOLS for G5: they are run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C4e and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f020-r5-block.md` := this block, `.agent/authored/f020-r5-plan.md` := plan.md.
  Both by `shutil.copyfile`.
  Subject: `F020 R5 C1a: copy round 5 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 32. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the diff and the two red-proof tools
  `.agent/authored/f020-r5-book.diff`, `.agent/authored/f020-r5-mutations.py` and
  `.agent/authored/f020-r5-harness_redproof.py`.
  Subject: `F020 R5 C1b: copy round 5 diff and red-proof tools into .agent/authored/`
  Expected insertions: 291.

C1c — commit the harness
  Each `conformance_*` payload to `.agent/authored/f020-r5-<its payload name>`, for example
  `conformance_measure.py` to `.agent/authored/f020-r5-conformance_measure.py`.
  Subject: `F020 R5 C1c: commit the glyph conformance harness into .agent/authored/`
  Expected insertions: 353.

C1d — copy the new product and test files
  `.agent/authored/f020-r5-glyphConformance.ts` and `.agent/authored/f020-r5-glyphConformance.test.ts`.
  Subject: `F020 R5 C1d: copy round 5 conformance module and its tests into .agent/authored/`
  Expected insertions: 276.

C2 — THE BOOKKEEPING, in this order: `git apply` book.diff, then rewrite `.agent/plan.md` :=
  plan.md.
  Subject: `F020 R5 C2: book round 4's PASS, record D5, advance the plan`
  Expected insertions by `git show --numstat`: 40 decisions.md, 2 live_review.md, 11 plan.md.

C3 — THE PRODUCT: copy glyphConformance.ts into `apps/ui/src/components/graph/renderers/` and
  `git add` it — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F020 R5 C3: probe every discriminating detail of the matrix fixture against the binding spec`
  Expected insertions: 146.

C4 — THE TESTS: copy glyphConformance.test.ts into `apps/ui/src/components/graph/renderers/` and
  `git add` it.
  Subject: `F020 R5 C4: pin the probes, the binding spec and the pixel judge`
  Expected insertions: 130.

C4e — THE EVIDENCE: the transcript G4's harness run printed, stdout then stderr, saved whole
  as `.agent/authored/f020-r5-conformance.txt`.
  Subject: `F020 R5 C4e: commit the glyph conformance transcript`
  Report its insertion count as measured; the reviewer does not predict it, because the
  transcript carries process ids.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F020 R5 C5: rewrite handoff for round 5`
  Then `git push origin feature/f020-node-lifecycle-glyph-language`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f020-r5-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the two paths C3 and C4
   name, and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only 106df185 HEAD` after C5. Do NOT touch `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F020.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, the reviewer's worktrees (the
   `-sim` and `-dry` trees of rounds 1 to 5 under the `.remedy-wt/f020-r` prefix, and the older
   `.remedy-wt/f015-r*` and `.remedy-wt/f284-r*` ones), and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F020's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written, and G4
runs at C4, before C4e.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f020-r5-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f020-r5/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 298389 | 4e85f5dd1850b7c234aa36835532ec3197d0bb2e015433f2cf63ec5e60f5d18c |
 | C2 | .agent/decisions.md | 2043706 | 22db38d10317587eff5f2230e11788eaad340b8d2ae777eac92e946e536d2221 |
 | C2 | .agent/plan.md | 1169 | e4bc66c01f99a95f829b9e0a8dd581471cccb42de7b246df8c2e9d720e193448 |
 Also: the number of lines C2's diff of `.agent/live_review.md` adds that begin
 `Gate: F020 R4 — ` (the reviewer read 1); the open set by distinct id, computed with
 `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT at C2 (the reviewer
 read R-1008 alone); and `git diff --name-only <C1d> <C2>`, which must name exactly the paths of
 the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/renderers/glyphConformance.ts | 7207 | bb9731ebce8b857cbef6198fca8189277e5a5880352aff1f6e08879ad5903436 |
 | C4 | apps/ui/src/components/graph/renderers/glyphConformance.test.ts | 6597 | 844d757a1398b77ff7bd1674a2be65ec06087d61ec15a429d575b5aae3bf280d |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must each name exactly the one path
 of that commit; and `python3 -m ruff check .agent/authored/f020-r5-conformance_measure.py
 .agent/authored/f020-r5-harness_redproof.py .agent/authored/f020-r5-mutations.py` at C4, whose
 three paths the repository's ruff configuration excludes by directory and a named path overrides.

G4 THE TESTS AND THE HARNESS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/regression/test_named_bugs.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C2 to C4 and read `1127 passed, 16 skipped` at real exit code 0. FOUR of those skips
 are toolchain nodes a worktree cannot run and the primary checkout can, and each must PASS in
 your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py`, the typescript node in
 `tests/ui_server/test_dashboard_contract.py` and the vitest node in
 `tests/orchestration/test_test_runner.py`, which runs the UI's whole unit suite and so this
 round's test file. Report every `SKIPPED` line. Then `python3 -m apps.cli.main integrity check
 --json`, which must read all six checks `pass` at `fail_count` 0. Then the harness:
 `python3 .agent/authored/f020-r5-conformance_measure.py /home/decodeux/Repos/remedy`, capturing
 its whole stdout and stderr for C4e and its real exit code, which must be 0. The reviewer's run
 over its sim tree printed, among its build and process lines, exactly these:
 `MISSING TOKENS: none`
 `PASSED ring/mark: 8 present, 0 absent`
 `PASSED status_dot/mark: 16 present, 40 absent`
 `PASSED status_dot/outline: 16 present, 0 absent`
 `PASSED strike/mark: 8 present, 48 absent`
 `PASSED strike/outline: 8 present, 0 absent`
 `CONFORMANCE: 144 of 144 probes pass`
 `drive.mjs exit code: 0`
 Report each of those lines as your run printed it, and every line beginning `FAILED` or
 `EXCEPTION`, of which the reviewer's run printed none.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f020-r5-mut <C4>`, then both tools
 against it, reporting each one's whole output and real exit code:
 (a) `python3 -B .agent/authored/f020-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f020-r5-mut`.
 It runs vitest over the WORKTREE's `glyphConformance.test.ts` from the primary `apps/ui` with a
 scratch config under `.remedy-wt/f020-r5-mutscratch/`, and pytest over the worktree's token
 guard. The reviewer read over its sim tree (v = vitest failed, g = guard failed, each red at
 exit 1 wherever its count is not 0): control first vitest 12 passed and guard 8 passed, both at
 exit 0; m1 (the spec drops the failed state's dot) v2 g0; m2 (the dot is probed off its centre)
 v2 g0; m3 (the strike's outline is probed on the strike itself) v1 g0; m4 (a missing ring is
 probed too) v2 g0; m5 (the probes ignore the state's size factor) v1 g0; m6 (a function colour's
 alpha is read unscaled) v1 g0; m7 (the tolerance excludes its own bound) v1 g0; m8 (an unpainted
 pixel counts as a colour) v1 g0; m9 (an absent probe passes when the colour shows) v1 g0; m10 (an
 unresolved token passes) v1 g0; m11 (the strike is judged in the failure red) v1 g0; m12 (a raw
 colour literal enters the conformance module) v0 g1; control last as first; every restore
 byte-identical, and the final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 (b) `python3 -B .agent/authored/f020-r5-harness_redproof.py
 /home/decodeux/Repos/remedy/.remedy-wt/f020-r5-mut
 /home/decodeux/Repos/remedy/.agent/authored/f020-r5-conformance_measure.py`. It runs the harness
 over the worktree unmutated first and last and once per mutation, restoring each file. The
 reviewer read over its sim tree: control first `CONFORMANCE: 144 of 144 probes pass` at exit 0;
 h1 (a failed node loses its status dot) exit 1 at 133 of 144; h2 (the painter draws marks
 without their outline) exit 1 at 120 of 144; h3 (the open state carries the strike too) exit 1
 at 136 of 144; h4 (the status dot is drawn at the top left) exit 1 at 122 of 144; control last
 as first; every `restored byte-identical` True, and the final line
 `ALL HARNESS MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f020-r5-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4e, C4, C3, C2, C1d, C1c, C1b, C1a and
 `106df185` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F020, round 5, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the closure sequence's first round — the Built State, the checklist consolidation,
the self-use track and the one full suite. State the open-findings count, 1, and the
operator-questions count, 3.
