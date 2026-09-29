STEP F291 R3 — THE CLOSURE'S INTEGRATION GATE: book round 2, land the self-use item SU-037 with two reviewer tests, record it in the Built State, and run the one full suite

GOAL
Round 2 passed. Book it, record DECISION F291 D3, land the self-use job's own diff (the handler in
`apps/cli/commands/brain.py` narrowed to `OSError`, `MAX_EXCUSED` lowered to 289) with the
reviewer's two tests, add the Built State's self-use paragraph, build the cockpit, and run F291's
one full suite on the tree that ships (closure precondition 2).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line. Every change this round
makes travels as a payload. Read DECISION F291 D3 in records.diff before you start.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f291-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f291-r3/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f291-*` path: the reviewer's; do not touch.
  `.remedy-wt/f291-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace is refused: write such a script to a file under your own
directory and run the file. Set environment variables for a child process inside a Python script
(`subprocess.run(..., env=...)`), never on a command line. Never run npm or npx. Never `pkill -f`.
The `remedy` command may be denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f291-self-use-sources-v2`, and `git log --oneline -1` must read `8cd5855d7`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f291-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f291-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 45 | 7822 | 83fb49cc0ccaab0d85bd4ae9f3c2b5c3434950e823a769fcb1ff3609ea2ae8c2 |
| selfuse.diff | 26 | 1247 | b10d93928ca92c32c00b210246c6904a0569080532904437b996387ba497a6bf |
| tests.diff | 64 | 2931 | 93a08777429844bdb47da5338b840aacfda47ad11113a33e611891ec51060d8f |
| docs.diff | 16 | 1241 | 05abe7079f3499c6458d2d8ab38a48d1b70f79e35cfd3fe5f851b30fcd9bbe8e |
| plan.md | 27 | 903 | 67a7ca7e49cf1defce5c7bfe91456297550808a232bb97bf402de3d11671c066 |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`, in the order the
commits below name; the reviewer generated them with `git diff HEAD` from a tree at `8cd5855d7`.
`records.diff` appends round 2's gate entry to `.agent/live_review.md` and DECISION F291 D3 to
`.agent/decisions.md`. `selfuse.diff` is byte for byte the output of
`git diff 8cd5855d7...remedy/job-d6d60ea3d586425a`, the self-use job's own change to
`apps/cli/commands/brain.py` and `tests/test_ble001_ratchet.py`. `tests.diff` appends two tests to
`TestConstitutionGuard` in `tests/test_brain_viewer.py`. `docs.diff` appends the self-use
paragraph to the Built State of `docs/roadmap/features/T5_F291.md`.

BUNDLE — the commits are C1, C2, C3, C4, C5, C6 and C7, in this order.

C1 — `.agent/authored/f291-r3-block.md` := this block, and `.agent/authored/f291-r3-plan.md`,
  `.agent/authored/f291-r3-records.diff`, `.agent/authored/f291-r3-selfuse.diff`,
  `.agent/authored/f291-r3-tests.diff` and `.agent/authored/f291-r3-docs.diff` := those payloads,
  by `shutil.copyfile`. Subject: `F291 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 178; STOP rather than commit at 500.
C2 — THE RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md.
  Subject: `F291 R3 C2: book F291 R2, record D3`
  Expected by `git show --numstat`: 27/0 .agent/decisions.md, 2/0 .agent/live_review.md, 8/9 .agent/plan.md.
C3 — THE LANDING: `git apply` selfuse.diff. The mark leaves and the ratchet falls in one commit.
  Subject: `F291 R3 C3: land SU-037, narrow the brain viewer's constitution handler to OSError`
  Expected by `git show --numstat`: 1/1 apps/cli/commands/brain.py, 1/1 tests/test_ble001_ratchet.py.
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F291 R3 C4: add the reviewer's tests for the narrowed constitution handler`
  Expected by `git show --numstat`: 53/0 tests/test_brain_viewer.py.
C5 — THE BUILT STATE: `git apply` docs.diff.
  Subject: `F291 R3 C5: record the closure's self-use item in F291's Built State`
  Expected by `git show --numstat`: 8/0 docs/roadmap/features/T5_F291.md.
C6 — THE TOOL: your mutation tool (G3) saved as `.agent/authored/f291-r3-mutations.py`.
  Subject: `F291 R3 C6: add the round 3 mutation tool`
C7 — THE INTEGRATION GATE, in the PRIMARY checkout, after C6 and after G1 to G3. (a) run
  `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its exit
  code and last line — a failing build is a STOP — then `git status --porcelain`, still empty.
  (b) `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f291-r3-worker/`; measure its wall
  time. Write `.agent/authored/f291-closure-suite.txt` holding the command, the real exit code, the
  wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
  `NONE`, and one line naming the tree it ran on (C6's SHA). A summary that reads only `N errors`
  after a few seconds means collection aborted and no test ran; say so in the transcript. After
  the suite, report the processes `pgrep -af server.py` lists, which must be none. (c) Rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with the
  transcript. Subject `F291 R3 C7: record the closure suite transcript and rewrite handoff for
  round 3`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's tracked path set: the `.agent/authored/f291-r3-*` files, `.agent/live_review.md`,
   `.agent/decisions.md`, `.agent/plan.md`, `apps/cli/commands/brain.py`,
   `tests/test_ble001_ratchet.py`, `tests/test_brain_viewer.py`, `docs/roadmap/features/T5_F291.md`,
   `.agent/authored/f291-closure-suite.txt` and `.agent/handoff.md`. Report
   `git diff --name-only 8cd5855d7` at the tip. No other file; `scripts/self_use_queue.json` is not
   touched, because the closure commit sets `SU-037`'s `consumed_by`.
4. A RED full suite in C7 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back. Never weaken an assertion, delete a test,
   skip or mark anything xfail, and never repair a suite node yourself. An EXISTING test that goes
   red before C7 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no branch switch or deletion; no force-push; no
   amend; no `git stash`; no evidence job; no zip; no self-use run and no job that calls a
   provider. Do not delete the `remedy/job-d6d60ea3d586425a` branch.
6. Leave every worktree already listed at your step 4, its branch, and every existing stash alone.
   The worktree G3 adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
7. The full suite runs exactly once this round, in C7, and nowhere else (amend0917-throughput
   rule 1).

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G3 run before C7.

G1 TRANSPORT AND RECORDS — each payload's measured lines, bytes and sha256 against the table; each
 `.agent/authored/f291-r3-*` copy byte-equal to its source (the block against
 `.remedy-wt/f291-r3/block.md`) by `git show <commit>:<path>` from C1; and the bytes and sha256 of
 each file below, read with `git show <commit>:<path>` at the commit named, equal to the reviewer's
 reading printed from its simulation tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2511793 | 56aadac91596a5a88fad456575d2e91024f237db90d00275590eb67950d6d7dc |
 | C2 | .agent/live_review.md | 138410 | e4e8e5c349a91d0f14a3167721b425c34e644fe4b7c7384c022519afc96b6d69 |
 | C2 | .agent/plan.md | 903 | 67a7ca7e49cf1defce5c7bfe91456297550808a232bb97bf402de3d11671c066 |
 | C3 | apps/cli/commands/brain.py | 20388 | d6d8c1a92a572f7462bba46e87598fac4c486c7fb77c7d8abbe0aecce4a395e5 |
 | C3 | tests/test_ble001_ratchet.py | 2243 | 673ddb6ad0a8141c2a8f9856e929717a84df930b7e976d7a887ca0ba00150d82 |
 | C4 | tests/test_brain_viewer.py | 53468 | b499ad3119195378e0bc13c6416a83f42073424b967a34ccd0230b01757e6c09 |
 | C5 | docs/roadmap/features/T5_F291.md | 6878 | 60714eee5f25950f3498a16a0f7fbd54bd0211a335e125dce8ebc94b2cf7755d |
 Also `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2 (the reviewer read `[]` and `PASS`), and `cmp` of selfuse.diff against the
 output of `git diff 8cd5855d7...remedy/job-d6d60ea3d586425a` written to your own directory, which
 must report no difference.

G2 THE TESTS, in the primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_brain_viewer.py tests/test_ble001_ratchet.py tests/test_context_coverage.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it in its simulation tree carrying C2 to C5 but no `.agent/authored/f291-r3-*`
 copy and read `801 passed, 1 skipped` at real exit code 0, the skip the D12 quarantine; report the
 counts and every SKIPPED line. `python3 -m ruff check apps/cli/commands/brain.py
 tests/test_brain_viewer.py tests/test_ble001_ratchet.py .agent/authored/f291-r3-mutations.py`, its
 real exit code. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks with status `pass` at `fail_count` 0.

G3 THE RED PROOFS — your tool `.agent/authored/f291-r3-mutations.py` takes a worktree path, and for
 each mutation below edits `apps/cli/commands/brain.py` INSIDE that worktree (asserting its FROM
 text, the line `        except OSError:`, occurs exactly once there), runs `python3 -B -m pytest
 -q -p no:cacheprovider tests/test_brain_viewer.py` with the worktree as the working directory and
 first on `PYTHONPATH` (set through `subprocess.run(..., env=...)`), restores the bytes, and prints
 one line per mutation: its label, the exit code and the failed count. It runs an unmutated
 control first and last, reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 the handler goes back to catching `Exception` (no mark is needed inside the worktree);
  m2 the handler catches `ValueError` in place of `OSError`.
 Run it: `git worktree add --detach .remedy-wt/f291-r3-mut <C6>`, then
 `python3 -B .agent/authored/f291-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f291-r3-mut`
 and report its whole output. The reviewer's own probe turned both red, each at 1 failed. EVERY
 mutation must exit non-zero; one that stays green is reported as green, never papered over, and
 you then STOP and report it. Then `git worktree remove --force .remedy-wt/f291-r3-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G4 THE INTEGRATION GATE — the UI build's last line and real exit code; `git status --porcelain`
 after it; the suite's real exit code, wall time, summary line and every bad node id, all in
 `.agent/authored/f291-closure-suite.txt`; and what `pgrep -af server.py` lists afterwards.

G5 SIZES, TREE AND PUSH — `git show --numstat --format= <commit>` for C1 to C6, each beside the
 expected insertions of its entry where one is stated and placed in the handback's `## Commits`
 table exactly as the tool printed it; and after C7, in your reply only: `git status --porcelain`
 empty, `git log --oneline -n 8` showing C7, C6, C5, C4, C3, C2, C1 and `8cd5855d7` in that order,
 the push's real outcome, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
 EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of feature
F291, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
3 and of the suite transcript, then the evidence bundle and the review package when the suite is
green, or the first repair round when it is not. State the open-findings count, 0, and the
operator-questions count, 0.
