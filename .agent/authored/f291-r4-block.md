STEP F291 R4 — THE CLOSURE'S FIRST REPAIR ROUND: book round 3, register and repair R-1114, and run the one full suite again on the repaired tree

GOAL
Round 3 passed and its full suite read one bad node, registered here as R-1114: two readers of
`tests/` fail when a temporary module another test wrote there vanishes between the listing and the
read. Book round 3, register R-1114, record DECISION F291 D4, repair Tier 5's reader against the
reviewer's tests, land the reviewer's repair of the parametrize-id guard, and run the one full
suite again on the tree that ships (amend0917-throughput rule 2, the first of at most three repair
rounds).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` or `Landed:` line. THE TESTS ARE THE
REVIEWER'S AND THE CODE IS YOURS: tests.diff is the acceptance, and you write S1 against it. Read
R-1114 and DECISION F291 D4 in records.diff, and `_bound_test_names` in
`packages/orchestration/self_use_generator.py`, before you edit it.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f291-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f291-r4/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f291-*` path: the reviewer's; do not touch.
  `.remedy-wt/f291-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f291-self-use-sources-v2`, and `git log --oneline -1` must read `752164eb2`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f291-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f291-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 50 | 11217 | 7416637ff513a0012da766e930248d54a78806352687a7bdaad6ba8e5daf1f6a |
| tests.diff | 91 | 4166 | e8e64d83c65a8645c5102031ece6c9dc3e004a3e39e43284bec9e2205b97a819 |
| plan.md | 28 | 927 | 2b5f7ad77784ba77c27afc640d55a3f3b489b0ffc012bde775b95636108d8462 |

`plan.md` is a REWRITE of `.agent/plan.md`. Both `.diff` files go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `752164eb2`. `records.diff` appends round 3's
gate entry and R-1114's registration to `.agent/live_review.md` and DECISION F291 D4 to
`.agent/decisions.md`. `tests.diff` edits `tests/test_parametrize_ids_stable.py` (its reader skips
a vanished file, and one test is added) and `tests/orchestration/test_self_use_generator.py` (two
tests join `TestUntestedModuleTier`, and the second reader of `TestUntestedModuleTierRealChain`
reads a vanished file as empty).

THE SPECIFICATION
S1 In `_bound_test_names` of `packages/orchestration/self_use_generator.py`, the read of each test
   file gains, BEFORE its existing `except (OSError, UnicodeDecodeError) as exc:` clause, an
   `except FileNotFoundError:` clause whose body is `continue`, under a comment of at most three
   lines saying the file is gone rather than unreadable because a test can write and remove a
   temporary module under `tests/` beside this read, naming R-1114 and DECISION F291 D4. Nothing
   else in the module changes; Tier 4's reader is untouched, and no line may contain `#` followed
   by `noqa: BLE001`.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — `.agent/authored/f291-r4-block.md` := this block, and `.agent/authored/f291-r4-plan.md`,
  `.agent/authored/f291-r4-records.diff` and `.agent/authored/f291-r4-tests.diff` := those
  payloads, by `shutil.copyfile`. Subject: `F291 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 169; STOP rather than commit at 500.
C2 — THE RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md.
  Subject: `F291 R4 C2: book F291 R3, register R-1114, record D4`
  Expected by `git show --numstat`: 30/0 .agent/decisions.md, 4/0 .agent/live_review.md, 8/7 .agent/plan.md.
C3 — THE REPAIR: S1. Subject: `F291 R4 C3: skip a test file that vanished while Tier 5 reads tests (R-1114)`
  The reviewer's own version of S1 read 4/0 packages/orchestration/self_use_generator.py.
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F291 R4 C4: repair the parametrize-id guard's reader and add the vanished-file tests (R-1114)`
  Expected by `git show --numstat`: 28/1 tests/orchestration/test_self_use_generator.py, 25/1 tests/test_parametrize_ids_stable.py.
C5 — THE TOOL: your mutation tool (G3) saved as `.agent/authored/f291-r4-mutations.py`.
  Subject: `F291 R4 C5: add the round 4 mutation tool`
C6 — THE SUITE, in the PRIMARY checkout, after C5 and after G1 to G3. (a) run
  `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its exit
  code and last line — a failing build is a STOP — then `git status --porcelain`, still empty.
  (b) `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f291-r4-worker/`; measure its wall
  time. REWRITE `.agent/authored/f291-closure-suite.txt` holding the command, the real exit code,
  the wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the
  literal `NONE`, the previous bad set (round 3's one node, from that file at `752164eb2`) with
  whether the new set is strictly smaller and holds no newly bad node, and one line naming the tree
  it ran on (C5's SHA). A summary that reads only `N errors` after a few seconds means collection
  aborted and no test ran; say so. After the suite, report what `pgrep -af server.py` lists, which
  must be nothing. (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` and commit
  it TOGETHER with the transcript. Subject `F291 R4 C6: record the repaired tree's suite transcript
  and rewrite handoff for round 4`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's tracked path set: the `.agent/authored/f291-r4-*` files, `.agent/live_review.md`,
   `.agent/decisions.md`, `.agent/plan.md`, `packages/orchestration/self_use_generator.py`,
   `tests/orchestration/test_self_use_generator.py`, `tests/test_parametrize_ids_stable.py`,
   `.agent/authored/f291-closure-suite.txt` and `.agent/handoff.md`. Report
   `git diff --name-only 752164eb2` at the tip. No other file; `tests/regression/test_resource_safety.py`
   is not touched.
4. A RED full suite in C6 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back. Never weaken an assertion, delete a test,
   skip or mark anything xfail, and never repair a suite node yourself. An EXISTING test that goes
   red before C6 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no branch switch or deletion; no force-push; no
   amend; no `git stash`; no evidence job; no zip; no self-use run and no job that calls a
   provider.
6. Leave every worktree already listed at your step 4, its branch, and every existing stash alone.
   The worktree G3 adds goes under `.remedy-wt/`, is removed as that gate's last action, and
   `git worktree list | wc -l` is reported afterwards.
7. The full suite runs exactly once this round, in C6, and nowhere else.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G3 run before C6.

G1 TRANSPORT AND RECORDS — each payload's measured lines, bytes and sha256 against the table; each
 `.agent/authored/f291-r4-*` payload copy byte-equal to its source (the block against
 `.remedy-wt/f291-r4/block.md`) by `git show <commit>:<path>` from C1; and the bytes and sha256 of
 each file below, read with `git show <commit>:<path>` at the commit named, equal to the reviewer's
 reading printed from its simulation tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2514066 | 745c151bebd5de82785957fcc64ea9e6769734b179df7d910443bafbdd975614 |
 | C2 | .agent/live_review.md | 142833 | 6775f3b4d1663b85645d161add29865424ce7a7f4c550802894470616dc5c68b |
 | C2 | .agent/plan.md | 927 | 2b5f7ad77784ba77c27afc640d55a3f3b489b0ffc012bde775b95636108d8462 |
 | C4 | tests/orchestration/test_self_use_generator.py | 68100 | 8ddc194d23f84a497233ed7c42f71620abdbe7c495a1f982c89d17d1dcfbb874 |
 | C4 | tests/test_parametrize_ids_stable.py | 3227 | 2d92d943ea7fa11d0360ddfc2b970329cf3f583d7f5f1604db667154712a64db |
 Also `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2 (the reviewer read `['R-1114']` and `PASS`).

G2 THE TESTS, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_parametrize_ids_stable.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/regression/test_resource_safety.py tests/test_ble001_ratchet.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it in its simulation tree carrying C2 to C4, with its own version of S1, but no
 `.agent/authored/f291-r4-*` copy, and read `625 passed, 1 skipped` at real exit code 0, the skip
 the D12 quarantine; report the counts and every SKIPPED line. `python3 -m ruff check
 packages/orchestration/self_use_generator.py tests/test_parametrize_ids_stable.py
 tests/orchestration/test_self_use_generator.py .agent/authored/f291-r4-mutations.py`, its real
 exit code; `git show --numstat <C3>`; and the count of lines of the generator at C3 matching
 `#\s*noqa:\s*BLE001\b`, which must be 0. Then `python3 -m apps.cli.main integrity check --json`,
 which must read all six checks `pass` at `fail_count` 0 (R-1114 is Low, so the open set does not
 block it).

G3 THE RED PROOFS — your tool `.agent/authored/f291-r4-mutations.py` takes a worktree path, and for
 each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once there), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/test_parametrize_ids_stable.py tests/orchestration/test_self_use_generator.py` with the
 worktree as the working directory and first on `PYTHONPATH` (set through
 `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation: its label,
 the exit code and the failed count. It runs an unmutated control first and last, reports
 `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  x1 Tier 5's new clause catches `ValueError` in place of `FileNotFoundError`
     (`packages/orchestration/self_use_generator.py`);
  x2 Tier 5's reader skips every read error: the `(OSError, UnicodeDecodeError)` clause also
     `continue`s (same file);
  x3 the guard's new clause catches `ValueError` in place of `FileNotFoundError`
     (`tests/test_parametrize_ids_stable.py`).
 After the mutations, the tool plants a dangling link at
 `tests/regression/test_runtime_chain_zz_gone.py` INSIDE the worktree, runs the same two files
 with `-k "fresh_value_at_collection or real_tree_offers_a_module"`, prints that exit code and
 count, which must be exit 0, and removes the link. Run it: `git worktree add --detach
 .remedy-wt/f291-r4-mut <C5>`, then `python3 -B .agent/authored/f291-r4-mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f291-r4-mut` and report its whole output. The reviewer's
 own probe turned all three red at 1 failed each, and the planted run read `2 passed` at exit 0.
 EVERY mutation must exit non-zero; one that stays green is reported as green, never papered
 over, and you then STOP and report it. Then `git worktree remove --force .remedy-wt/f291-r4-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G4 THE SUITE — the UI build's last line and real exit code; `git status --porcelain` after it; the
 suite's real exit code, wall time, summary line and every bad node id, and the shrink reading
 against round 3's set, all in `.agent/authored/f291-closure-suite.txt`; and what
 `pgrep -af server.py` lists afterwards.

G5 SIZES, TREE AND PUSH — `git show --numstat --format= <commit>` for C1 to C5, each beside the
 expected insertions of its entry where one is stated and placed in the handback's `## Commits`
 table exactly as the tool printed it; and after C6, in your reply only: `git status --porcelain`
 empty, `git log --oneline -n 7` showing C6, C5, C4, C3, C2, C1 and `752164eb2` in that order, the
 push's real outcome, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
 EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of feature
F291, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
4 and of the suite transcript, then the evidence bundle and the review package when the suite is
green, or the second repair round when it is not. State the open-findings count, 1 (R-1114, whose
resolution the reviewer books after this review), and the operator-questions count, 0.
