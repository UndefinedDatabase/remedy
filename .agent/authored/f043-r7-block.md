STEP F043 R7 — THE CLOSURE'S INTEGRATION GATE: book round 6, land the self-use item SU-038 with two reviewer tests, record it in the Built State, and run the one full suite

GOAL
Round 6 passed. Book it, record DECISION F043 D6, land the self-use job's own diff (the handler in
`_prepare_viewer` of `apps/cli/commands/brain.py` narrowed to `OSError`, `MAX_EXCUSED` lowered to
288) with the reviewer's two tests, add the Built State's self-use paragraph, build the cockpit,
and run F043's one full suite on the tree that ships (closure precondition 2).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line. Every change this round
makes travels as a payload. Read DECISION F043 D6 in records.diff before you start.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r7/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f043-*` path: the reviewer's; do not touch.
  `.remedy-wt/f043-r7-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace or a brace beside a quote is refused: write such a script to a
file under your own directory and run the file. Set environment variables for a child process
inside a Python script (`subprocess.run(..., env=...)`), never on a command line. Never run npm or
npx. Never `pkill -f`. The `remedy` command may be denied; use `python3 -m apps.cli.main`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f043-explanation-layer`, and `git log --oneline -1` must read `6b2c3e8c6`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f043-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 42 | 6305 | beb5fbdcda2eae2abaf6d3b65268515385b7adb5daf4e70b60c07f0cdb3ba22a |
| selfuse.diff | 26 | 1154 | 50178f8e5e5a2a8fc7405806d6bc709923787fbe41f7507a3bd6ef616446eab9 |
| tests.diff | 53 | 2643 | 212f66d3a13555d341783fb2dcff0b3b4f336666db0f6ee014028b5fc73d7865 |
| docs.diff | 18 | 1144 | ab3770115c8c9ec8936ca50f3d7b46487d308c3f2c3f0b73c600e47ef5bede70 |
| plan.md | 28 | 974 | e4cb59cb361c9544bef8d110ab5d7374eec73b270e5d1d596316054a50cac471 |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`, in the order the
commits below name; the reviewer generated them with `git diff HEAD` from a tree at `6b2c3e8c6`,
except `selfuse.diff`, which is byte for byte the output of
`git diff 6b2c3e8c6...remedy/job-d1a4eea4787f420c`, the self-use job's own change to
`apps/cli/commands/brain.py` and `tests/test_ble001_ratchet.py`. `records.diff` appends round 6's
gate entry to `.agent/live_review.md` and DECISION F043 D6 to `.agent/decisions.md`. `tests.diff`
appends two tests to `TestConstitutionGuard` in `tests/test_brain_viewer.py`. `docs.diff` adds the
self-use paragraph to the Built State of `docs/roadmap/features/T5_F043.md`.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — `.agent/authored/f043-r7-block.md` := this block, and `.agent/authored/f043-r7-plan.md`,
  `.agent/authored/f043-r7-records.diff`, `.agent/authored/f043-r7-selfuse.diff`,
  `.agent/authored/f043-r7-tests.diff` and `.agent/authored/f043-r7-docs.diff` := those payloads,
  by `shutil.copyfile`. Subject: `F043 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 167; STOP rather than commit at 500.
C2 — THE RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md.
  Subject: `F043 R7 C2: book F043 R6, record D6`
  Expected by `git show --numstat`: 24/0 .agent/decisions.md, 2/0 .agent/live_review.md, 6/8 .agent/plan.md.
C3 — THE LANDING: `git apply` selfuse.diff. The mark leaves and the ratchet falls in one commit.
  Subject: `F043 R7 C3: land SU-038, narrow the viewer helper's constitution handler to OSError`
  Expected by `git show --numstat`: 1/1 apps/cli/commands/brain.py, 1/1 tests/test_ble001_ratchet.py.
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F043 R7 C4: add the reviewer's tests for the viewer helper's narrowed handler`
  Expected by `git show --numstat`: 42/0 tests/test_brain_viewer.py.
C5 — THE BUILT STATE: `git apply` docs.diff.
  Subject: `F043 R7 C5: record the closure's self-use item in F043's Built State`
  Expected by `git show --numstat`: 8/0 docs/roadmap/features/T5_F043.md.
C6 — THE TOOL: your mutation tool (G3) saved as `.agent/authored/f043-r7-mutations.py`.
  Subject: `F043 R7 C6: add the round 7 mutation tool`
C7 — THE INTEGRATION GATE, in the PRIMARY checkout, after C6 and after G1 to G3. (a) run
  `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its exit
  code and last line — a failing build is a STOP — then `git status --porcelain`, still empty.
  (b) `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f043-r7-worker/`; measure its wall
  time. Write `.agent/authored/f043-closure-suite.txt` holding the command, the real exit code, the
  wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
  `NONE`, and one line naming the tree it ran on (C6's SHA). A summary that reads only `N errors`
  after a few seconds means collection aborted and no test ran; say so in the transcript. After
  the suite, report the processes `pgrep -af server.py` lists, which must be none. (c) Rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with the
  transcript. Subject `F043 R7 C7: record the closure suite transcript and rewrite handoff for
  round 7`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's tracked path set: the `.agent/authored/f043-r7-*` files, `.agent/live_review.md`,
   `.agent/decisions.md`, `.agent/plan.md`, `apps/cli/commands/brain.py`,
   `tests/test_ble001_ratchet.py`, `tests/test_brain_viewer.py`, `docs/roadmap/features/T5_F043.md`,
   `.agent/authored/f043-closure-suite.txt` and `.agent/handoff.md`. Report
   `git diff --name-only 6b2c3e8c6` at the tip. No other file; `scripts/self_use_queue.json` is not
   touched, because the closure commit sets `SU-038`'s `consumed_by`.
4. A RED full suite in C7 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back. Never weaken an assertion, delete a test,
   skip or mark anything xfail, and never repair a suite node yourself. An EXISTING test that goes
   red before C7 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no branch switch or deletion; no force-push; no
   amend; no `git stash`; no evidence job; no zip; no self-use run and no job that calls a
   provider. Do not delete the `remedy/job-d1a4eea4787f420c` branch.
6. Leave every worktree already listed at your step 4, its branch, and every existing stash alone.
   The worktree G3 adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
7. The full suite runs exactly once this round, in C7, and nowhere else (amend0917-throughput
   rule 1).

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G3 run before C7.

G1 TRANSPORT AND RECORDS — each payload's measured lines, bytes and sha256 against the table; each
 `.agent/authored/f043-r7-*` copy byte-equal to its source (the block against
 `.remedy-wt/f043-r7/block.md`) by `git show <commit>:<path>` from C1; and the bytes and sha256 of
 each file below, read with `git show <commit>:<path>` at the commit named, equal to the reviewer's
 reading printed from its simulation tree:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2537033 | 3808a8caf47d080b5d60a0b7c57906b9b0fbe04fb896258e1fca9d134a8d34ff |
 | .agent/live_review.md | C2 | 133368 | a7e7362f0d2f15669a47eaa4bdf80625565b977f9182171a0e45dc729d996dc6 |
 | .agent/plan.md | C2 | 974 | e4cb59cb361c9544bef8d110ab5d7374eec73b270e5d1d596316054a50cac471 |
 | apps/cli/commands/brain.py | C3 | 20311 | 10fa9b4cb196ef1751ffdaa6da14e19462b2d4f05647ba7d1ac07152a264f52c |
 | tests/test_ble001_ratchet.py | C3 | 2243 | 453a2f1d143a872bbb5a6bdfcbf6082b6372fa9f22016d69d53de1f3aac315b3 |
 | tests/test_brain_viewer.py | C4 | 55575 | ee1ce2932b54fb79be61290e4099ee85b61d13e9416f5317616e1cfcfdab1380 |
 | docs/roadmap/features/T5_F043.md | C5 | 8263 | a0e7d8a767f35e92ce15844bb9ea0dd9fea551f167abc9346641bbbb944d9e74 |
 Also `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2 (the reviewer read `[]` and `PASS`), and `cmp` of selfuse.diff against the
 output of `git diff 6b2c3e8c6...remedy/job-d1a4eea4787f420c` written to your own directory, which
 must report no difference.

G2 THE TESTS, in the primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_brain_viewer.py tests/test_ble001_ratchet.py tests/test_context_coverage.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it in its dry tree carrying C2 to C5 but no `.agent/authored/f043-r7-*` copy and
 read `805 passed, 1 skipped` at real exit code 0, the skip the D12 quarantine; report the counts
 and every SKIPPED line. `python3 -m ruff check apps/cli/commands/brain.py tests/test_brain_viewer.py
 tests/test_ble001_ratchet.py .agent/authored/f043-r7-mutations.py`, its real exit code. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks with status
 `pass` at `fail_count` 0.

G3 THE RED PROOFS — your tool `.agent/authored/f043-r7-mutations.py` takes a worktree path, and for
 each mutation below edits `apps/cli/commands/brain.py` INSIDE that worktree, runs `python3 -B -m
 pytest -q -p no:cacheprovider tests/test_brain_viewer.py` with the worktree as the working
 directory and first on `PYTHONPATH` (set through `subprocess.run(..., env=...)`), restores the
 bytes, and prints one line per mutation: its label, the exit code and the failed count. The file
 holds TWO lines reading `        except OSError:` after C3, so the FROM text is the landed
 handler's own four lines, from `        except OSError:` through `    graph =
 build_project_brain`, asserted to occur exactly once. It runs an unmutated control first and last,
 reports `restored byte-identical: True` after each restore, and ends with `ALL MUTATIONS CAUGHT AND
 RESTORED CLEANLY: <bool>`:
  m1 the landed handler goes back to catching `Exception` (no mark is needed inside the worktree);
  m2 the landed handler catches `ValueError` in place of `OSError`.
 Run it: `git worktree add --detach .remedy-wt/f043-r7-mut <C6>`, then
 `python3 -B .agent/authored/f043-r7-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f043-r7-mut`
 and report its whole output. The reviewer's own probe turned both red, each at 1 failed. EVERY
 mutation must exit non-zero; one that stays green is reported as green, never papered over, and
 you then STOP and report it. Then `git worktree remove --force .remedy-wt/f043-r7-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G4 THE INTEGRATION GATE — the UI build's last line and real exit code; `git status --porcelain`
 after it; the suite's real exit code, wall time, summary line and every bad node id, all in
 `.agent/authored/f043-closure-suite.txt`; and what `pgrep -af server.py` lists afterwards.

G5 SIZES, TREE AND PUSH — `git show --numstat --format= <commit>` for C1 to C6, each beside the
 expected insertions of its entry where one is stated and placed in the handback's `## Commits`
 table exactly as the tool printed it; and after C7, in your reply only: `git status --porcelain`
 empty, `git log --oneline -n 8` showing C7, C6, C5, C4, C3, C2, C1 and `6b2c3e8c6` in that order,
 the push's real outcome, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
 EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of feature
F043, round 7, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
7 and of the suite transcript, then the evidence bundle and the review package when the suite is
green, or the first repair round when it is not. State the open-findings count, 0, and the
operator-questions count, 0.
