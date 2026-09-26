STEP F289 R3 — BOOK ROUND 2, REPAIR R-1074, AND LAND T003: three consecutive generator calls on an empty ledger produce three distinct items, and the first runs to completion inside the self-use run's default budget

GOAL
Round 2 passed. Book its verdict and R-1074's registration, record one prose-slip line and
DECISION F289 D3, repair R-1074 in `packages/orchestration/doc_staleness.py`, and land T003, the
proof T5_F289.md's Done line asks for, as a new test class in
`tests/orchestration/test_self_use_runner.py`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE CHANGE IS SPECIFIED, NOT SLICED: you write the code
and the tests yourself against S1 and S2 below. Only the `.agent/` records travel as payloads. Read
R-1074 and DECISION F289 D3 in the records payload first.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f289-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f289-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f289-r3-dry/`, `.remedy-wt/f289-r3-sim/`, `.remedy-wt/f289-r3-drafts/` and
  `.remedy-wt/f289-review/`       The reviewer's; do not touch them.
  `.remedy-wt/f289-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe pytest. Use `git -C <path>` rather than `cd`, and never `cd` your
shell into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a file
under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f289-self-use-sources`, and `git log --oneline -1` must read `c1851178`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f289-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f289-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 28 | 983 | 36d3cc02f68b9574c5f64de05ac327a5f8f855d541839cbdf3e21447f0654f0f |
| records.diff | 61 | 12954 | f1910881558e7405b41c4489c53f65a9f61cddddece2e8e0b863124cd11287d9 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `c1851178`. It appends round 2's gate entry and
R-1074's registration to `.agent/live_review.md`, one line to `.agent/prose_slips.md`, and
DECISION F289 D3 to `.agent/decisions.md`.

THE SPECIFICATION
S1 R-1074. In `_run_c04` of `packages/orchestration/doc_staleness.py`, the resolved link target
   must EXIST, file or folder (`Path.exists()`), and a comment names R-1074; nothing else in the
   module changes. The `truth` text of a C04 claim is unchanged. In
   `tests/orchestration/test_doc_staleness.py`, the C04 class gains a test that a guide linking an
   existing folder (`../system/`, with `docs/system/` present under the root) yields no claim and
   one linking a missing folder (`../nowhere/`) yields exactly one. In the same commit append ONE
   line to the end of `.agent/live_review.md`, starting with its own blank line:
   `Landed: R-1074 — the staleness catalog's link check accepts a link to an existing folder and still reports a missing one, at this round's C3.`
   — one physical line, exactly that text.
S2 T003. In `tests/orchestration/test_self_use_runner.py`, a new class
   `TestThreeConsecutiveItemsOnAnEmptyLedger`, with a docstring naming T5_F289.md's Done line and
   DECISION F289 D3, holding one test that follows D3 exactly, using the file's own
   `isolate_data_root`, `demo_repo`, `_write_queue` and `_pass_provider`:
   - an empty ledger file under `tmp_path`, an empty fixture queue, and `order_path` pointing at a
     missing file on every generator call;
   - `self_use_generator.default_docs_root` monkeypatched to a root under `tmp_path` whose
     `docs/README.md` holds a `## Quick-Find Table` section linking no guide and a `## Guides`
     section linking two guides that exist under that root's `docs/guides/`, so the catalog
     answers exactly two C01 claims;
   - `load_dead_models` and `dead_model_ids` on `packages.orchestration.dead_model_list`
     monkeypatched to declare the id `resolve_model_alias("claude-flagship")` answers dead (read at
     run time, never spelled);
   - `self_use_runner.run_job` monkeypatched to a pass-through that records its keyword arguments
     and returns the real `run_job`'s result;
   - three closures, each: `generate_and_append_if_empty(queue_path=..., ledger_path=...,
     order_path=...)` answers an entry; on the FIRST closure only, while it is the one pending
     item, `run_next_self_use_item(tmp_path / "jobs", str(demo_repo), queue_path=...,
     builder_provider=_pass_provider(), reviewer_provider=_pass_provider(), repair_rounds=0)`
     runs it; then the entry is consumed by writing its `consumed_by` in the queue file with
     `json`, as a closure does;
   - assertions: the three entries' ids are `SU-001`, `SU-002` and `SU-003`; their provenances
     are pairwise distinct, the first two starting `generated (self-use-generator tier 2` and the
     third `generated (self-use-generator tier 3`; the run's entry id is the first entry's; its
     result's `state` is `JOB_COMPLETED`; and the recorded `budgets["max_cost_usd"]` equals
     `self_use_runner._MAX_COST_USD` and `budgets["max_provider_calls"]` equals 8.
   The reviewer's own probe of exactly this sequence at `c1851178` read those three provenances
   and the run `completed` with `max_cost_usd` 6.0.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f289-r3-block.md` := this block, `.agent/authored/f289-r3-plan.md` := plan.md,
  and `.agent/authored/f289-r3-records.diff` := records.diff, by `shutil.copyfile`.
  Subject: `F289 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 89. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKKEEPING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F289 R3 C2: book round 2, register R-1074, record D3`
  Expected by `git show --numstat` (insertions and deletions): 32/0 decisions.md, 4/0 live_review.md, 8/10 plan.md, 1/0 prose_slips.md.

C3 — R-1074: S1, both files and the `Landed:` line.
  Subject: `F289 R3 C3: accept a guide's link to an existing folder (R-1074)`

C4 — T003: S2 and your mutation tool (G5) saved as `.agent/authored/f289-r3-mutations.py`.
  Subject: `F289 R3 C4: prove three consecutive self-use items on an empty ledger, the first run to completion`

C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F289 R3 C5: rewrite handoff for round 3`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f289-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/doc_staleness.py`, `tests/orchestration/test_doc_staleness.py`,
   `tests/orchestration/test_self_use_runner.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only c1851178` at the branch tip after C5. Do NOT touch
   `packages/orchestration/self_use_generator.py`, `packages/orchestration/self_use_runner.py`,
   `README.md`, anything under `docs/` or `apps/`, `scripts/self_use_queue.json`,
   `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. Code or a test
   this round itself wrote that is wrong may be corrected before C5, and the correction is declared.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list` is reported
   afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F289 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table. Then compare each `.agent/authored/f289-r3-*` copy byte for byte with its
 source (the block copy against `.remedy-wt/f289-r3/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2218696 | bbf0214fc5307101416e99f925e470c8b88275944d10053d0a0003b34ceaff0e |
 | .agent/live_review.md | 325378 | 37364d1a187d9ae55d8f3ad296b7b6e11e1a137f30f9661a11938055b5931cfd |
 | .agent/prose_slips.md | 370935 | fc2c715287f60a735a3158b3ea75a33990022643abfe79d789ee2d8bddc055e4 |
 | .agent/plan.md | 983 | 36d3cc02f68b9574c5f64de05ac327a5f8f855d541839cbdf3e21447f0654f0f |
 Also: the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's TEXT at `c1851178` and at C2 (the reviewer read it empty, then `R-1074`
 alone); at C2 the ledger's last line begins `- R-1074 — `.

G3 THE CODE — `python3 -m ruff check packages/orchestration/doc_staleness.py
 tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_runner.py` at C4;
 `git diff -U0 <C2> <C3> -- packages/orchestration/doc_staleness.py .agent/live_review.md`,
 reported whole, which must change the one existence test with its comment and add the blank line
 and the one `Landed:` line, and nothing else; and `run_staleness_checks()` over the real
 repository at C3, whose claims must still be exactly the two DECISION F289 D2 names.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_queue.py tests/cli/test_advertised_commands.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/test_imports.py tests/test_subprocess_timeouts.py tests/orchestration/test_import_reachability.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection before any code change, serially, inside its authoring tree
 carrying the round's records, and read `695 passed, 1 skipped` at real exit code 0; the skip is
 the D12 quarantine. Report every `SKIPPED` line, the nodes the round adds (`--collect-only -q` on
 the two edited test files at `c1851178` and at C4), and account for any other difference. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0, and `git branch --list 'remedy/*'` counted before C3 and after G4, which must be
 equal: the proof's run works in `demo_repo`, never in this repository.

G5 THE RED PROOFS — your tool `.agent/authored/f289-r3-mutations.py` takes a worktree path, and for
 each mutation below edits the named module INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_doc_staleness.py` and `tests/orchestration/test_self_use_runner.py`
 from the worktree's root after purging its `__pycache__` directories, restores the bytes, and
 prints one line per mutation: its label, the exit code, the failed count and the failing node
 ids. It runs an unmutated control first and last and ends with `restored byte-identical: True`
 per file and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations:
  m1 `_run_c04` goes back to requiring a file;
  m2 `_run_c04` accepts every link whose target's parent folder exists;
  m3 `_doc_staleness_tier` in `self_use_generator.py` ignores the keys the queue already targets;
  m4 `_doctor_warning_tier` in `self_use_generator.py` answers None;
  m5 `_run_c01` in `doc_staleness.py` reads only the Guides section;
  m6 `run_next_self_use_item` in `self_use_runner.py` resolves its default `max_cost_usd` to 1.00
     instead of `_MAX_COST_USD`.
 Run it: `git worktree add --detach .remedy-wt/f289-r3-mut <C4>`, then
 `python3 -B .agent/authored/f289-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f289-r3-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a mutation
 that stays green is reported as green, never papered over, and you then add the assertion that
 catches it in C4 before C5 and re-run the tool. Then `git worktree remove --force
 .remedy-wt/f289-r3-mut`, `git worktree prune`, and report `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty; `git log --oneline
 -n 7`; `git worktree list`, which must show the primary checkout and the worktrees constraint 6
 names, and nothing else; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected (none is expected for C3 and C4), every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next expected action. Your Session section reads SESSION 1 of feature
F289, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then the closure sequence's integration gate: the one full suite of F289. State the
open-findings count, 1 (R-1074, landed and awaiting the reviewer's `Done:`), and the
operator-questions count, 0.
