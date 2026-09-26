STEP F027 R6 — FINISH ROUND 5'S DOOR: the door's `job.veto-task` clause and payload check, the door's answer of a replan proposal, the answerable inbox card, and the guard's walker skipping a type-only import block (DECISION F027 D6)

GOAL
Book round 5's verdict, resolve R-1067, record DECISION F027 D6, and land what round 5 stopped
short of: its uncommitted draft of S4 to S6, now standing in the primary checkout, reviewed and
completed by you; the guard walker's `if TYPE_CHECKING:` skip with its proof; the door tests round 5
never wrote; and the mutation tool over the whole door.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean at the handback, push, and write the
handback. You never issue a verdict and you never merge. THE SPECIFICATION IS ROUND 5'S: S4, S5,
S6 and THE TESTS of `.agent/authored/f027-r5-block.md`, as committed at `a540e6e6`, bind this round
word for word, with the one change DECISION F027 D6 rules for S6's stop clause. The draft is another
worker's unreviewed code: read all of it against those sections before you commit any of it, and
fix what does not meet them.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-review/r5-uncommitted.diff`  READ-ONLY. The reviewer's export of the draft.
  `.remedy-wt/f027-r6-dry/`, `.remedy-wt/f027-r5b-dry/`, `.remedy-wt/f027-r6-drafts/`,
  `.remedy-wt/f027-review/` and every older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r6-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx. Interactive git (`git add -p`) is unavailable.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git branch --show-current` must read `feature/f027-task-veto` and `git log --oneline -1` must
   read `96cb5154`. `git status --porcelain` must name exactly the four modified files
   `packages/orchestration/decision_inbox.py`, `packages/orchestration/ui_server.py`,
   `tests/orchestration/test_decision_inbox.py` and `tests/ui_server/test_command_channel.py`,
   and the sha256 of the bytes `git diff HEAD` prints must read
   `bb6a81da0676e797cd7303d77b4712d58ebefefc7dccd3bcdc99c248d8d8a395`, the digest of the
   reviewer's export. Report all four readings, and stop if any differs.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1127 | 629949b44993842d7db4b9e5451cfde25f05cc3448a0047f2564a7f1c9b0bf2c |
| records.diff | 49 | 9988 | c57e29fdb9193f4f37d6f6ce74d1bd588862a83434641bb368d2ddd1697db874 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a clean tree at `96cb5154`, and it touches neither the
draft's files nor `.agent/plan.md`. It appends to `.agent/live_review.md` round 5's gate entry and
R-1067's `Done:` paragraph, and to `.agent/decisions.md` DECISION F027 D6. Stage only the paths a
commit names (`git add <path>`), so the draft stays out of C1 and C2.

THE WORK
W1 THE WALKER, in `tests/ui_server/test_command_channel.py`, per DECISION F027 D6 (1): inside
   `_module_level_closure`'s `imports_of`, an `ast.If` whose test is the name `TYPE_CHECKING` or an
   attribute named `TYPE_CHECKING` contributes its `orelse` and not its body, with a comment naming
   D6; and a new test over synthetic modules written under `tmp_path` proving the closure still
   reaches a forbidden module imported at module level, one imported under an ordinary `if`, and
   one imported in the `else` of an `if TYPE_CHECKING:`, and does not reach one imported under
   `if TYPE_CHECKING:` or `if typing.TYPE_CHECKING:`. `ACCEPTED_TRANSITIVE_FORBIDDEN` does not
   change. If the transitive test is still red once W1 and the draft are in, stop and report it.
W2 THE DRAFT, read against round 5's S4, S5 and S6 and completed where it falls short. Round 5's
   own handback names two pre-existing channel tests the draft adjusts for the widened exposed set;
   those adjustments stand, declared.
W3 THE DOOR TESTS round 5 ordered in `tests/ui_server/test_command_dispatch.py`, and the inbox and
   decision tests it ordered, where the draft has not written them.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads: `.agent/authored/f027-r6-block.md`,
  `.agent/authored/f027-r6-plan.md` and `.agent/authored/f027-r6-records.diff`, by
  `shutil.copyfile`. Subject: `F027 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 80. STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F027 R6 C2: book round 5, resolve R-1067, record D6`
  Expected by `git show --numstat`: 29/0 decisions.md, 4/0 live_review.md, 11/19 plan.md.
C3 — THE DOOR, THE INBOX AND THE GUARD: W1 and W2 — `ui_server.py`, `decision_inbox.py`,
  `tests/ui_server/test_command_channel.py` and `tests/orchestration/test_decision_inbox.py`.
  Subject: `F027 R6 C3: the door vetoes a task and answers a replan proposal; the guard skips type-only imports`
C4 — THE DOOR TESTS: W3. Subject: `F027 R6 C4: test the door's veto and its answer of a replan proposal`
C5 — THE MUTATION TOOL: `.agent/authored/f027-r6-mutations.py`.
  Subject: `F027 R6 C5: the round's red-proof mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F027 R6 C6: rewrite handoff for round 6`. Then `git push`, and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r6-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/ui_server.py`, `packages/orchestration/decision_inbox.py`,
   `tests/ui_server/test_command_channel.py`, `tests/orchestration/test_decision_inbox.py`,
   `tests/ui_server/test_command_dispatch.py`, `tests/cli/test_decision_cmd.py`, and
   `.agent/handoff.md`. Report the list `git diff --name-only 96cb5154` measures after C6. Do NOT
   touch `packages/orchestration/task_veto.py`, `veto_proposal.py`, `stream_evidence.py`,
   `pingpong_job.py`, `apps/`, `docs/`, `.agent/context.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back with the tree clean: a draft you cannot verify is saved
   as a patch under your own directory and removed from the tree, never left uncommitted. Do not
   repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every worktree `git worktree list` showed at your step 4, and every stash, alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F027 exactly one, at its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload the line count, byte count and sha256 you measured against the
 table; then each `.agent/authored/f027-r6-*` payload copy compared byte for byte with its source
 (the block copy against `.remedy-wt/f027-r6/block.md`), read back with `git show <C1>:<path>`.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 310462 | c08e4485e54fb30c7e9580be127a908fe2887f403885128db3c5b2454658c283 |
 | .agent/decisions.md | 2179770 | 92559cd5450c245b21c4aedc9ae37d8ea3948e95b4ad839aa471424ff42d0a9d |
 | .agent/plan.md | 1127 | 629949b44993842d7db4b9e5451cfde25f05cc3448a0047f2564a7f1c9b0bf2c |
 Also the open set by distinct id, with `open_finding_ids` from `scripts/rotate_live_review.py`
 over the ledger's text at C2 (the reviewer read it empty).

G3 THE CODE — `python3 -m ruff check` over every Python file of the round's path set at the last
 code commit; and `git diff -U0 96cb5154 <C3> -- tests/ui_server/test_command_channel.py`, reported
 whole, which must hold the walker's skip, its test, the door method name, the three import entries
 of round 5's S6 with their comment, and the two declared exposed-set adjustments, and nothing else.

G4 THE TESTS — in the primary checkout at the last code commit, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_job_veto.py tests/cli/test_job_plan_cmd.py tests/cli/test_job_pause.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_contracts/test_steering_send_contract.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_veto_proposal.py tests/orchestration/test_task_veto.py tests/cli/test_decision_cmd.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py tests/cli/test_exit_codes.py tests/orchestration/test_event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, in a scratch tree at
 `96cb5154` carrying the draft and W1's walker change and none of W3, and read `1281 passed` at real
 exit code 0. Report every `SKIPPED` line, the nodes each grown test file contributes
 (`--collect-only -q`), and account for every difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r6-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/ui_server/test_command_dispatch.py`, `tests/ui_server/test_command_channel.py` and
 `tests/orchestration/test_decision_inbox.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and last
 and ends with `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each mutation is a behaviour a test can see:
  m1 the door's payload check lets a blank reason through to the job;
  m2 the door's payload check is removed for `task_id`;
  m3 the door's clause answers a refused veto with a 200;
  m4 the door's clause passes a fixed actor instead of the token fingerprint;
  m5 the door's `veto:` branch is removed, so the answer falls to the escalation route;
  m6 the inbox's `veto:` branch reads true for an answered proposal;
  m7 the walker follows the body of an `if TYPE_CHECKING:` block again;
  m8 the walker skips every `if` body, not only a type-only one.
 Run it in `git worktree add --detach .remedy-wt/f027-r6-mut <last code commit>` and report its
 whole output. EVERY mutation must be red; a green one is reported as green, never papered over:
 you then say whether a test can see the behaviour at all, add the test that catches it if one
 can, and re-run the tool. Then `git worktree remove --force .remedy-wt/f027-r6-mut`,
 `git worktree prune`, and `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty; `git log --oneline`
 from `96cb5154` to the tip; `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected, every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations — every change you made
to the draft among them — and the next expected action. Report what you ran, not what you expected
to find. Your Session section reads SESSION 1 of feature F027, round 6, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then T003 — the strike, the reason on hover, the dimmed unreachable set with its link,
the veto affordance and the inbox card's plain-words menu on the page. State the open-findings
count, 0, and the operator-questions count, 5.
