STEP F285 R4 — THE CLOSURE SEQUENCE'S SECOND ROUND: land the self-use run's reviewed diff as R-1064's repair, write the Built State, consolidate the checklist, and run the one full suite

GOAL
Book round 3's PASS, with the reviewer's pass of self-use job `78ecdc636060461c`'s diff. Land that
diff VERBATIM on the branch as R-1064's repair — it is the first self-use diff in the track's
history to land — then the reviewer's pin of the seven real node ids beside it, the Built State of
`docs/roadmap/features/T2_F285.md`, and the checklist consolidation pass. Then run this feature's
ONE full suite on the tree that ships and commit its transcript with the handback. The evidence
bundle, the review package, the rotation, the STATUS line and the pull request belong to later
rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict, never merge, and never write a `Done:` or `Landed:` line.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f285-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f285-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f285-r4-drafts/`    READ-ONLY. The reviewer's drafts and builders.
  `.remedy-wt/f285-r4-dry/`       The reviewer's dry tree; do not touch it.
  `.remedy-wt/f285-r4-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f285-r4-worker/`    YOURS for logs and scripts; create it if absent. All of these
                                  are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or a brace next to a quote is
refused: write such a script to a file under your own directory and run the file. The ONE npm
command this round may run is C6's `npm --prefix apps/ui run build`; never `npm install`,
`npm ci` or `npx`. Never `git stash`, never `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f285-findings-paydown-v4`, and `git log --oneline -1` must read `0f1975b7`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f285-r4/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f285-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 10 | 6900 | 492184c47ff69b4575e51e83727a4e41f32e714afe710d3e0fbf2b1fa57d3aba |
| plan.md | 30 | 1064 | 2e4d7f158a659caadccdc8d90cccec2c1c8ffce97283a1846bb0fc711abae39c |
| r1064.diff | 56 | 3038 | b19e7a4a5b69e439b319c74f6a24c89d1d1360fc34b9160d00bb51fc68f50285 |
| pin.diff | 45 | 2091 | b98b5938e42ce42a24978c853f8bc170457df5fe069f3be481b0538cff21c26a |
| docs.diff | 46 | 3410 | 5e93d64fa961084e5fa23db646246a6548da813d44c9e61c966556daba41001a |
| mutations.py | 58 | 2195 | 84b992d5cbc8c5f466fee690dd72c464aeb96b4a589c10d3ad4dd79a58aaf69c |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`. `records.diff`
appends the F285 round 3 gate entry to `.agent/live_review.md`. `r1064.diff` is EXACTLY
`git diff c67932fe 5796c5b7 -- packages/orchestration/stream_evidence.py
tests/orchestration/test_stream_evidence.py`, the self-use job's own commit on its branch
`remedy/job-78ecdc636060461c`; before applying it, run that `git diff` yourself and report whether
its bytes equal the payload's. `pin.diff` adds the reviewer's tests to
`tests/orchestration/test_stream_evidence.py`. `docs.diff` appends the Built State to
`docs/roadmap/features/T2_F285.md` and inserts the consolidation paragraph in
`docs/agents/planner_reviewer_prompt.md` directly above its line
`  The next consolidation measures against 34.` (containment test: TO contains FROM: true — an
APPEND; that line occurs once before and once after). `mutations.py` is a TOOL for G4.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the payloads other than the tool
  `.agent/authored/f285-r4-block.md` := this block, and `.agent/authored/f285-r4-<name>` := each
  of records.diff, plan.md, r1064.diff, pin.diff and docs.diff. All by `shutil.copyfile`.
  Subject: `F285 R4 C1a: copy round 4 block and payloads into .agent/authored/`
  Expected insertions: 386 (this block's 199 lines plus 187 for the five payloads). Report the number you measure and STOP rather than commit if any
  commit of this round would reach 500 insertions.
C1b — `.agent/authored/f285-r4-mutations.py` := mutations.py.
  Subject: `F285 R4 C1b: copy round 4 mutation tool into .agent/authored/`
  Expected insertions: 58.
C2 — THE BOOKING: `git apply` records.diff, then `.agent/plan.md` := plan.md.
  Subject: `F285 R4 C2: book F285 R3 with the reviewer's pass of the self-use run's diff`
  Expected insertions by `git show --numstat`: 2 .agent/live_review.md, 11 .agent/plan.md.
C3 — THE LANDING: `git apply` r1064.diff, nothing else. The commit message's body names job
  `78ecdc636060461c`, its item `SU-032` and its commit `5796c5b7`, and carries the line
  `Remedy-Job: 78ecdc636060461c` above the trailer.
  Subject: `F285 R4 C3: land self-use job 78ecdc636060461c's reviewed repair of R-1064 verbatim`
  Expected insertions: 3 packages/orchestration/stream_evidence.py, 29 tests/orchestration/test_stream_evidence.py.
C4 — THE PIN: `git apply` pin.diff.
  Subject: `F285 R4 C4: pin the seven real node ids R-1064 measured, and the sk-ant bound`
  Expected insertions: 27 tests/orchestration/test_stream_evidence.py.
C5 — THE BUILT STATE AND THE CONSOLIDATION: `git apply` docs.diff.
  Subject: `F285 R4 C5: write the Built State and consolidate the checklist`
  Expected insertions: 6 docs/agents/planner_reviewer_prompt.md, 21 docs/roadmap/features/T2_F285.md.
C6 — THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after G1 to G5:
  (a) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  — a failing build is a STOP — then `git status --porcelain`, still empty. (b)
  `bash -c 'python3 -m pytest -n auto -q 2>&1 | tee .remedy-wt/f285-r4-worker/full-suite.txt | tail -5; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  with a Bash timeout of 3600000 milliseconds; measure its wall time. Write
  `.agent/authored/f285-closure-suite.txt` holding the command, the real exit code, the wall time,
  the summary line and the FULL list of bad node ids (failed plus errors), or the literal `NONE`.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER
  with the transcript. Subject: `F285 R4 C6: record the closure suite transcript and rewrite
  handoff for round 4`. Then `git push origin feature/f285-findings-paydown-v4`. No pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. `git apply --check` before each `git apply`, its
   exit code reported.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f285-r4-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/stream_evidence.py`,
   `tests/orchestration/test_stream_evidence.py`, `docs/roadmap/features/T2_F285.md`,
   `docs/agents/planner_reviewer_prompt.md`, `.agent/authored/f285-closure-suite.txt` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 0f1975b7 HEAD`.
4. A RED full suite in C6 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to
   order (amend0917-throughput rule 2). Never weaken an assertion, delete a test or mark anything
   xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip; no
   `remedy job apply`. The self-use job's branch and records are left as they are.
6. The full suite runs ONCE, in C6, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C6 is written; G6 is C6's suite.

G1 TRANSPORT — each payload's measured lines, bytes and sha256 against the table; each
 `.agent/authored/f285-r4-*` copy byte-equal to its source by `git show <commit>:<path>`; and
 the reading ordered above for r1064.diff against the job's own commit.

G2 THE FILES — the sha256 of each file below, read with `git show <commit>:<path>` at the commit
 the table names, equals the reviewer's reading, which its builder printed from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 317751 | e897669d0671f18e5aa5ee5aeae59059189a0307f59851f2462896a2f5575c2f |
 | C2 | .agent/plan.md | 1064 | 2e4d7f158a659caadccdc8d90cccec2c1c8ffce97283a1846bb0fc711abae39c |
 | C3 | packages/orchestration/stream_evidence.py | 36384 | bf2c6667b4db5fe064259c58b527df3988ab8376506542c8ca4064a754a5a5aa |
 | C3 | tests/orchestration/test_stream_evidence.py | 21382 | d03f9dea0e0cb448a23608fcb579b72f416939f3067db4d7ff04f7d555015210 |
 | C4 | tests/orchestration/test_stream_evidence.py | 22797 | fa2a8e44aebea4a117a16bad240795af6af55cba115dfe246e4fa351003a704e |
 | C5 | docs/agents/planner_reviewer_prompt.md | 103708 | 00b0f303338239d9cae527782a441947d5e758f114a65e58adb7f41d846f4d93 |
 | C5 | docs/roadmap/features/T2_F285.md | 6242 | aac2753f2b5109eda671927d7db2eee7555dee4133a83bc4a798441fcd649685 |
 Also `packages/orchestration/stream_evidence.py` at C3 equals
 `git show 5796c5b7:packages/orchestration/stream_evidence.py` byte for byte; the open set by
 distinct id, `open_finding_ids` over the ledger's TEXT at C2, reads R-1008 and R-1064; and
 `live_checklist_items` of `packages/orchestration/block_lint.py` over the planner prompt reads the
 same 34 numbers at `0f1975b7` and at C5.

G3 THE TESTS, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_stream_evidence.py tests/orchestration/test_redaction_patterns.py tests/orchestration/test_run_manifest.py tests/orchestration/test_block_lint.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_queue.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection in its simulated tree at C5 and read `602 passed` at real
 exit code 0, the `-rs` summary printing none. Then `python3 -m ruff check
 packages/orchestration/stream_evidence.py tests/orchestration/test_stream_evidence.py`, which
 must read `All checks passed!`; and `python3 -m apps.cli.main integrity check --json`, six
 `pass` at `fail_count` 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f285-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f285-r4-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f285-r4-mut`, its whole output reported. The reviewer
 read, over the same tool against its simulated tree (timings vary):
 control first: exit 0: 59 passed in 0.29s
 m1 (the sk- pattern loses its token-start bound): FROM occurs 1x in packages/orchestration/stream_evidence.py
 m1: exit 1: 12 failed, 47 passed in 0.37s; restored byte-identical: True
 m2 (the sk-ant- pattern loses its token-start bound): FROM occurs 1x in packages/orchestration/stream_evidence.py
 m2: exit 1: 1 failed, 58 passed in 0.32s; restored byte-identical: True
 control last: exit 0: 59 passed in 0.30s
 ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
 Then `git worktree remove --force .remedy-wt/f285-r4-mut`, `git worktree prune`, and
 `git worktree list` reported.

G5 SIZES — `git show --numstat --format= <commit>` for C1a, C1b, C2, C3, C4 and C5, each beside
 the expected insertions of its entry above, and placed in the handback's `## Commits` table
 exactly as the tool printed it.

G6 THE INTEGRATION GATE — the UI build's last line and real exit code, `git status --porcelain`
 after it, then the full suite's real exit code, wall time, summary line and every bad node id,
 all in `.agent/authored/f285-closure-suite.txt`; and whether
 `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
 bad node (closure precondition 7).

G7 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
 equal to `origin/feature/f285-findings-paydown-v4`, `git log --oneline -n 8`, `git worktree
 list`, the push's real outcome, and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next action. Session section: SESSION 1 of feature F285, round 4, plus one
sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of round 4, then
the evidence bundle and the review package, then the closing round. State the open-findings
count, 2, and the operator-questions count, 5.
