STEP F285 R2 — BOOK ROUND 1 AND LAND T003: the relaunch of an interrupted task resumes its parked provider session (R-1055)

GOAL
Book round 1's PASS with the resolutions of R-1057 and R-1058, record DECISION F285 D2, and land
T003, R-1055's repair: every round's builder and reviewer blocks in a run's `result.json` carry
the provider session the call reported and whether it resumed one, and `run_job` hands the parked
run's sessions of a task a park or a stop interrupted to the relaunch's first calls, which resume
them where the provider supports resume. Red proofs for it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f285-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f285-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f285-r2-drafts/`    READ-ONLY. The reviewer's drafts and builders.
  `.remedy-wt/f285-r2-dry/`       The reviewer's dry tree; do not touch it.
  `.remedy-wt/f285-r2-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f285-r2-worker/`    YOURS for logs and scripts; create it if absent. All of these
                                  are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or a brace next to a quote is
refused: write such a script to a file under your own directory and run the file. Never run npm
or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f285-findings-paydown-v4`, and `git log --oneline -1` must read `26f44f49`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f285-r2/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f285-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| book.diff | 61 | 11536 | 99d549e0cd517960c470621032d0d77881c83a3317a574a60adb31310067287e |
| plan.md | 28 | 992 | ba2692e1513dd44c877cad521a813da63bf8a95aff18390377fc6f246e732b32 |
| t003.diff | 451 | 23111 | 1c5983158c7dd98eb082e2ca7c73bd4de3fbbe492b2afcefd5f199724a56664a |
| mutations.py | 68 | 2894 | bde3a1817e5b1bc3ecc2bd42c05d37f96596855e1e309c5c911033dfd638ff41 |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` payloads go on with `git apply`; the
reviewer generated each with `git diff HEAD` from a tree at `26f44f49` into which it wrote the
edits. `book.diff` appends to `.agent/live_review.md` (the F285 round 1 gate entry and the
resolutions of R-1058 and R-1057) and to `.agent/decisions.md` (DECISION F285 D2). `t003.diff`
edits `docs/system/session-resume-v1.md`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/pingpong_loop.py` and `tests/orchestration/test_prompt_trace.py`, and
creates `tests/orchestration/test_relaunch_session_resume.py`. `mutations.py` is a TOOL for G4:
it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3 and C4, in this order.

C1a — copy this block and the booking payloads
  `.agent/authored/f285-r2-block.md` := this block, and `.agent/authored/f285-r2-book.diff` and
  `.agent/authored/f285-r2-plan.md` := book.diff and plan.md. All by `shutil.copyfile`.
  Subject: `F285 R2 C1a: copy round 2 block and booking payloads into .agent/authored/`
  Expected insertions: 298 (this block's 209 lines plus 89 for the two payloads). Report the number you measure and STOP rather than commit if any
  commit of this round would reach 500 insertions.

C1b — copy the T003 payload
  `.agent/authored/f285-r2-t003.diff` := t003.diff.
  Subject: `F285 R2 C1b: copy round 2 T003 payload into .agent/authored/`
  Expected insertions: 451.

C1c — copy the mutation tool
  `.agent/authored/f285-r2-mutations.py` := mutations.py.
  Subject: `F285 R2 C1c: copy round 2 mutation tool into .agent/authored/`
  Expected insertions: 68.

C2 — THE BOOKING, in this order:
   1. `git apply` book.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F285 R2 C2: book F285 R1 with the resolutions of R-1057 and R-1058, record D2`
  Expected insertions by `git show --numstat`: 39 .agent/decisions.md, 6 .agent/live_review.md, 9 .agent/plan.md.

C3 — T003, R-1055: `git apply` t003.diff.
  Subject: `F285 R2 C3: resume an interrupted task's parked provider session on relaunch`
  Expected insertions: 17 docs/system/session-resume-v1.md, 10 packages/orchestration/pingpong_job.py, 69 packages/orchestration/pingpong_loop.py, 6 tests/orchestration/test_prompt_trace.py, 165 tests/orchestration/test_relaunch_session_resume.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F285 R2 C4: rewrite handoff for round 2`
  Then `git push origin feature/f285-findings-paydown-v4`. Do NOT create a pull request: the
  branch opens one at F285's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f285-r2-*` copies, the two paths
   book.diff edits, `.agent/plan.md`, the five paths t003.diff edits or creates, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 26f44f49 HEAD`
   after C4. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. You write no `Done:` line and no `Landed:` line of your own: the two `Done:` paragraphs
   book.diff carries are the reviewer's, and the reviewer authors R-1055's resolution at the
   next gate.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
7. Leave every existing worktree under `.remedy-wt/` and its branch alone, and every existing
   stash. The worktree G4 adds goes under `.remedy-wt/`, is removed as that step's last action,
   and `git worktree list` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F285's belongs to its closure. Run no self-use job and no `remedy` command that calls a
   provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f285-r2-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f285-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKING AND THE CODE — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit the table names, equals the reviewer's reading, which
 its builder printed from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2147985 | 536da5e02d7890b69974bf5d3567b4e044e1ab83f4078b9a844993f30f73c95d |
 | C2 | .agent/live_review.md | 311104 | 83f0c0bb976f8e22fdaa1bfbe0453deeb4bbbcf0e1d8374b7ed39f1504087857 |
 | C2 | .agent/plan.md | 992 | ba2692e1513dd44c877cad521a813da63bf8a95aff18390377fc6f246e732b32 |
 | C3 | docs/system/session-resume-v1.md | 6782 | ceef08008649e19b645831219e83fa6433e5a471cf94ed0ded954d351beeeb73 |
 | C3 | packages/orchestration/pingpong_job.py | 230224 | fc9fe78ec4e1bf108c5705108d6c2261270f1ae19b0fb8ea7c8af97631a69924 |
 | C3 | packages/orchestration/pingpong_loop.py | 233212 | a18fb30943664f478167bab52e08feebbaf3cf556bcc209aed8196cf593df4c2 |
 | C3 | tests/orchestration/test_prompt_trace.py | 31122 | b20726d798b4ddd44c673cd4985269cdb10398a2defc83aaa56a610a9c432dc9 |
 | C3 | tests/orchestration/test_relaunch_session_resume.py | 7682 | e5609e5d7773a9d1536b6f3b8f6d5a1aeade78a524af674afdb86b57b3279a0c |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `26f44f49` and at C2 (the reviewer read
 R-1008, R-1055, R-1057, R-1058 and R-1064 at the first and R-1008, R-1055 and R-1064 at the
 second); and `git diff --name-only` between each pair of consecutive commits from C1c to C3,
 each of which must name exactly the paths that commit's entry above lists.

G3 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_relaunch_session_resume.py tests/orchestration/test_session_resume.py tests/orchestration/test_prompt_trace.py tests/orchestration/test_semantic_dedupe.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_manifest.py tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_pause_control.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_integration.py tests/orchestration/test_pingpong_job_dod_gate.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_provider_evidence_integration.py tests/orchestration/test_run_manifest_chain_append.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_pause_e2e_live.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection, serially, inside its simulated tree at C3 and read
 `890 passed` at real exit code 0. Its first run, in the freshly created tree, read 1 failed and
 889 passed without the failing node being captured, and five warm re-runs each read the reading
 above; if your run is red, report the failing node id and its error, re-run that one node once,
 and report both readings. Report every `SKIPPED` line the `-rs` summary prints; the reviewer's
 run printed none. Then `python3 -m ruff check` over every `.py` file t003.diff
 edits or creates, named one by one, which must read `All checks passed!`; and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f285-r2-mut <C3>`, then
 `python3 -B .remedy-wt/f285-r2-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f285-r2-mut` and report its whole output. The tool
 asserts each FROM occurs exactly once, restores the bytes after each run, and runs unmutated
 controls first and last. The reviewer read, over the same tool against its simulated tree at
 C3 (timings vary):
 control first: exit 0: 82 passed in 1.56s
 m1 (run_job offers the relaunch no session): FROM occurs 1x in packages/orchestration/pingpong_job.py
 m1: exit 1: 1 failed, 81 passed in 1.68s; restored byte-identical: True
 m2 (the builder's first call ignores the offer): FROM occurs 1x in packages/orchestration/pingpong_loop.py
 m2: exit 1: 3 failed, 79 passed in 1.89s; restored byte-identical: True
 m3 (the reviewer's first call ignores the offer): FROM occurs 1x in packages/orchestration/pingpong_loop.py
 m3: exit 1: 1 failed, 81 passed in 1.81s; restored byte-identical: True
 m4 (the run record drops the session): FROM occurs 1x in packages/orchestration/pingpong_loop.py
 m4: exit 1: 2 failed, 80 passed in 1.45s; restored byte-identical: True
 m5 (the fallback fires on the prompt gate again): FROM occurs 1x in packages/orchestration/pingpong_loop.py
 m5: exit 1: 2 failed, 80 passed in 1.70s; restored byte-identical: True
 control last: exit 0: 82 passed in 1.57s
 ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
 Then `git worktree remove --force .remedy-wt/f285-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G5 SIZES — `git show --numstat --format= <commit>` for C1a, C1b, C1c, C2 and C3, each reported
 beside the expected insertions of its entry above, and placed in the handback's `## Commits`
 table exactly as the tool printed it.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C4, C3, C2, C1c, C1b, C1a and `26f44f49` in that
 order; `git worktree list`, which must show no worktree this round added; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F285, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then the closure sequence's self-use run on R-1064. State the open-findings count, 3,
and the operator-questions count, 5.
