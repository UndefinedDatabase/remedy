STEP F283 R1 — CLAIM F283 AND LAND T001 SLICE A: job's twenty already-flagged refusals

GOAL
Pull request 263 is merged; `main` is at `d0d40e89` and F283 is the next unchecked line.
Cut its branch, claim it, book F277 round 19's PASS and resolve R-1018, empty
`.agent/candidates.md`, re-head the live review record, and land T001's first slice: the
twenty refusal sites of `apps/cli/commands/job.py` whose handler ALREADY carries
`json_output`, migrated onto the shared `fail()` with nothing threaded and no caller
changed.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS SLICE IS THE SHAPE IT IS — it is what makes the gates checkable.
`apps/cli/commands/job.py` carries 44 `sys.exit` sites; 40 are a single stderr `print()`
immediately before the exit; TWENTY of those 40 sit in a handler whose signature already
has `json_output`, and those are SLICE A. The other twenty sit in `_cmd_create_job`,
`_cmd_show_job`, `_cmd_plan_job_local`, `_cmd_run_next_task_local` and
`_refuse_budget_set`, which have no flag in scope — threading it is its own round. The
remaining four carry a loop or a hand-rolled JSON object and are a behaviour decision, not
a rename. The partition is read off the tree by the test this round ships, so it cannot
drift.

THE ONE TRANSFORMATION TO UNDERSTAND: `fail()` writes the `Error: ` prefix itself, so a
migrated site passes its message WITHOUT it or the operator sees `Error: Error: ...`.
Every site in `job.diff` is already transformed that way, and the existing suite asserts
several of those lines byte-for-byte, which is what proves it.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r1-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f283-r1-scratch/`   YOURS. Every log, exit-code capture and script goes
      here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `python3 -c` or `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`); a `python3 -c` script with a newline followed by `#` is rejected.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read `main`,
   and `git log --oneline -1` must read `d0d40e89`. Report all three. Then
   `git checkout -b feature/f283-machine-contracts-part-two` and report the branch. Do
   NOT pull: `main` is already at the merge commit and the Open PR Gate ran before you.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f283-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all nine under `.remedy-wt/f283-r1-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| candidates.diff | 40 | 2721 | 94d29715f4ff9c8de67a2e0f1d45cedad06868263510dc0a2130f5d389fd7116 |
| context.md | 64 | 3524 | aaefe21dbad44ce009124e1155f766aa067e9ce86a878997baf5a267f7aa441e |
| job.diff | 274 | 10716 | fac6fb4f3d9682c8b0797f02c1f1b5e9e71268f21d1f000e60ee114c5e5eb2a3 |
| ledger.md | 4 | 5446 | ed3dc0e7a728a26ba9eaa3f7983b04f3000dad86c02ba1a8fbc06b484c9d9ad6 |
| plan.md | 49 | 2536 | 2eec9950e3ffe44c769283a155373eea929f50f622a276420f1bd3ee0ff7df61 |
| rehead.diff | 61 | 6758 | 5a232d6a46dc375f499e00b817ce06af94015b9ae396f8b4286510d8b223e3f6 |
| slips.md | 1 | 1160 | 55ad51b2730de76556011efee0b5a5750ba2ee922f211fc401522211179363a9 |
| status.diff | 11 | 1933 | e86c8ce43a4433d84aca8fdd3ea301abd8ed8d42961b4dac4c13f5634f142d86 |
| test_job_refusal_envelope.py | 186 | 6879 | 468fc1c8c398acd95b8da595a955b4ac3ba83441ce195d19522503bf9140aa15 |

`ledger.md` is an APPEND of TWO PARAGRAPHS beginning with a single newline that is the
record separator: the round 19 `Gate:` entry and the `Done: R-1018` resolution, in that
order. `slips.md` is an APPEND of ONE line with no leading newline — the file already ends
in one. `plan.md` and `context.md` are REWRITES. `test_job_refusal_envelope.py` is a NEW
FILE, copied whole. The four `.diff` files go on with `git apply`; every one was generated
from the tree at `d0d40e89` and every one dry-ran with `git apply --check` at real exit
code 0.

THE TWENTY SITES AND THEIR TOKENS, printed by the run that measured them. Each token is
named for the CONDITION (DECISION F277 D8); a catch-all handler gets a token named for the
layer that refused (DECISION F277 D9). You do not apply this table by hand — `job.diff`
already carries it — you use it to READ the diff and confirm the diff does what this says.

| exit line | code | function | token |
|---|---|---|---|
| 169 | 1 | _cmd_list_jobs | invalid_list_option |
| 1132 | 2 | _cmd_job_run_cycles | invalid_argument |
| 1179 | 1 | _cmd_job_run_cycles | job_not_found |
| 1189 | 3 | _cmd_job_run_cycles | plan_awaiting_approval |
| 1195 | 3 | _cmd_job_run_cycles | plan_rejected |
| 1207 | 1 | _cmd_job_run_cycles | permission_denied |
| 1214 | 1 | _cmd_job_run_cycles | builder_unavailable |
| 1404 | 1 | _cmd_job_resume | job_not_found |
| 1417 | 1 | _cmd_job_resume | checkpoints_corrupt |
| 1443 | 3 | _cmd_job_resume | worktree_drift |
| 1451 | 3 | _cmd_job_resume | plan_awaiting_approval |
| 1457 | 3 | _cmd_job_resume | plan_rejected |
| 1535 | 1 | _cmd_resume | job_not_found |
| 1545 | 3 | _cmd_resume | plan_awaiting_approval |
| 1551 | 3 | _cmd_resume | plan_rejected |
| 1582 | 1 | _cmd_resume | checkpoint_not_found |
| 1590 | 1 | _cmd_resume | checkpoint_not_resumable |
| 1917 | 1 | _cmd_job_budget | job_not_found |
| 2171 | 1 | _cmd_job_budget_set | job_not_found |
| 2210 | 1 | _cmd_job_budget_set | budget_not_written |

`job.diff` also splits `_plan_rejected_error` into itself plus a new
`_plan_rejected_message`, returning the same sentence WITHOUT the prefix. Both exist on
purpose for exactly this round: the three migrated sites call the new one, the site slice
B has not reached still calls the old one, and the pair collapses when slice B lands.
EVERY MIGRATED SITE KEEPS THE EXIT CODE IT ALREADY USED — 1, 2 and 3 all appear above;
re-numbering one is T002's work and would hide a behaviour change inside a rename.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3 and C4, in this order. The copies are
THREE commits and not one because the payloads total 690 lines and the cap is 500; each
of the three carries one role, so its arithmetic is checkable on its own. F283 has not
spent its one permitted oversize declaration and none of these is where to spend it.

C1a — copy this block
  `.agent/authored/f283-r1-block.md` := this block, byte-for-byte.
  Subject: `F283 R1 C1a: copy round 1 block into .agent/authored/`
  Its insertions are this block's own line count. Report that count and confirm it is
  under 500; STOP rather than commit if it is not.

C1b — copy the SEVEN bookkeeping payloads into `.agent/authored/`
  One `.agent/authored/f283-r1-<name>` for each of rehead.diff, ledger.md, status.diff,
  candidates.diff, plan.md, context.md and slips.md, keeping each payload's own file name.
  Subject: `F283 R1 C1b: copy round 1 bookkeeping payloads into .agent/authored/`
  Expected insertions: 230.

C1c — copy the TWO product payloads into `.agent/authored/`
  `.agent/authored/f283-r1-job.diff` and
  `.agent/authored/f283-r1-test_job_refusal_envelope.py`.
  Subject: `F283 R1 C1c: copy round 1 product payloads into .agent/authored/`
  Expected insertions: 460.

C2 — THE CLAIM. Apply in EXACTLY this order, because the append's base is the file AFTER
  the re-head and not before it:
   1. `git apply` rehead.diff        → `.agent/live_review.md` (+30/-22)
   2. append ledger.md to `.agent/live_review.md` (+4)
   3. `git apply` status.diff        → `docs/roadmap/STATUS.md` (+1/-1)
   4. `git apply` candidates.diff    → `.agent/candidates.md` (+1/-33)
   5. rewrite `.agent/plan.md` := plan.md (+36/-32)
   6. rewrite `.agent/context.md` := context.md (+36/-21)
   7. append slips.md to `.agent/prose_slips.md` (+1)
  Subject: `F283 R1 C2: claim F283, book round 19's PASS and resolve R-1018`
  EXPECTED INSERTIONS: 109 by `git show --numstat`, measured by applying these payloads in
  a disposable worktree at `d0d40e89`. If yours differs, report what you measured and say
  so. Six paths, all under `.agent/` except `docs/roadmap/STATUS.md`.

C3 — THE SLICE, product and its tests in ONE commit because the test is what verifies it
  `git apply .remedy-wt/f283-r1-payloads/job.diff`, then copy
  `test_job_refusal_envelope.py` to `tests/cli/test_job_refusal_envelope.py` and
  `git add` it — an untracked test file fails `integrity check`'s `relevant_untracked`,
  which the reviewer reproduced.
  Subject: `F283 R1 C3: migrate job's twenty flagged refusals onto the shared fail`
  Expected insertions: 262 — 76 for `job.py` and 186 for the new test file.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F283 R1 C4: rewrite handoff for round 1`
  Then `git push -u origin feature/f283-machine-contracts-part-two`. Do NOT create a pull
  request: the branch opens its pull request at F283's closure, not at its claim. Report
  the push's real outcome and the CI run id it starts.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the ten `.agent/authored/f283-r1-*` copies, `.agent/live_review.md`,
   `.agent/candidates.md`, `.agent/plan.md`, `.agent/context.md`,
   `.agent/prose_slips.md`, `docs/roadmap/STATUS.md`, `apps/cli/commands/job.py`,
   `tests/cli/test_job_refusal_envelope.py` and `.agent/handoff.md`. Report the length you
   measure rather than checking it against a number this block states. In particular do
   NOT touch `README.md`, `.agent/decisions.md`, `.agent/operator_questions.md`, a feature
   file under `docs/roadmap/features/`, or any module other than `job.py`.
4. DO NOT MIGRATE A SITE THIS BLOCK DOES NOT NAME. The twenty slice-B sites and the four
   non-mechanical ones stay exactly as they are. If you believe one of them must change
   for a gate to pass, STOP and hand back.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion.
7. Leave the three `remedy/job-*` worktrees alone. Any worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT — for each of the nine payloads report the line count, byte count and sha256
 you measured against the PAYLOADS table; twenty-seven readings, all equal. Then for each
 `.agent/authored/f283-r1-*` copy — one per payload plus the block copy, ten in all —
 compare it byte-for-byte with its source under `.remedy-wt/f283-r1-payloads/` (the block
 copy against `.remedy-wt/f283-r1-block.md`). Report one reading per copy and how many you
 compared; all True.

G2 THE CLAIM'S BOOKKEEPING — at C2:
 (a) The `.agent/live_review.md` append by strict byte CONCATENATION, taking as the base
     the file AFTER the re-head and before the append. The reviewer measured 432408 bytes
     before the re-head, 433255 after it, and 433255 plus 5446 equals 438701. Report all
     four of your numbers beside those.
 (b) The `.agent/prose_slips.md` append the same way: the reviewer measured 357369 plus
     1160 equals 358529.
 (c) The open set by distinct id in `.agent/live_review.md`, computed with the
     repository's OWN canonical reader — `open_finding_ids` from
     `scripts/rotate_live_review.py`, which takes the file's TEXT — at `d0d40e89` and at
     C2. The reviewer measured 24 then 23. Report both counts AND the set difference in
     both directions; the removed set must be exactly `{R-1018}` and the added set empty.
 (d) `.agent/plan.md` and `.agent/context.md` at C2 equal their payloads byte-for-byte.
     Report both sha256 pairs, and `.agent/plan.md`'s line count, which is 49 and must be
     under the AGENTS.md 50-line rule.
 (e) Read back F283's STATUS line in full and the whole of `.agent/candidates.md`. The
     STATUS line must read `- [~] F283 — ` and the candidates file must carry its header
     and the single line `EMPTY — every entry was registered as a finding and the register
     is the record.`
 (f) `git diff --name-only <C1c> <C2>` names exactly six paths. Report the list and its
     length.

G3 THE SLICE IS THE REVIEWER'S BYTES — at C3, report `git apply --check`'s real exit code
 before the real apply, then `git diff --name-only <C2> <C3>`, which must name exactly
 `apps/cli/commands/job.py` and `tests/cli/test_job_refusal_envelope.py`. Then report, by
 a COUNT you take from the committed tree and not from this block: how many
 `fail(` call sites `apps/cli/commands/job.py` now has, and how many the reviewer's table
 above lists. Both are 20.

G4 THE SLICE WORKS AND THE OPERATOR SEES THE SAME BYTES — run and report with real exit
 codes, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/cli/test_job_refusal_envelope.py tests/cli/test_job_budget_set.py tests/cli/test_job_commands.py tests/cli/test_job_show.py tests/cli/test_job_stop.py tests/cli/test_job_report.py tests/cli/test_plan_approval.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/test_data_paths.py; echo "REAL_EXIT=$?"'
```
 The reviewer measured `611 passed` at real exit code 0 over this exact selection with the
 whole round staged. `tests/docs/` and the roadmap index are in it because
 `docs/roadmap/STATUS.md` changed; the job suites are in it because THEY are the identity
 proof — several of them assert a refusal's stderr line byte-for-byte, so a migration that
 changed one visible byte reddens them. Then
 `python3 -m ruff check apps/cli/commands/job.py tests/cli/test_job_refusal_envelope.py`,
 real exit code 0, and `python3 -m apps.cli.main integrity check --json`, which must read
 all five checks `pass` at `fail_count` 0. DO NOT run the full suite: amend0917 rule 1
 gives a feature exactly one full-suite run and F283's belongs to its closure.

G5 THE NEW TEST GATES THE PRODUCT — two mutation red-proofs, both in a disposable worktree
 under `.remedy-wt/` at your C3 tree, neither ever committed:
 (a) Rename one token: change `fail("invalid_list_option"` to `fail("list_error"` and show
     `tests/cli/test_job_refusal_envelope.py` goes RED. The reviewer read
     `1 failed, 7 passed` at exit 1, at
     `TestARefusalIsAnEnvelopeUnderJson::test_an_unknown_sort_field_names_the_condition`.
 (b) Restore one site: put the `checkpoint_not_found` site back to its
     `print(...); sys.exit(1)` pair and show the STRUCTURAL guard goes RED. The reviewer
     read `1 failed, 7 passed` at exit 1, at
     `TestTheFlaggedRefusalsAreAllMigrated::test_no_flagged_print_then_exit_pair_survives`.
 Then REMOVE the worktree and report `git worktree list`. Without (b) the guard could be
 satisfied by a file that no longer parses the way the test thinks it does.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1c, C1b, C1a in that order;
 `git worktree list`, which must show the primary checkout and the three `remedy/job-*`
 worktrees and nothing else; `git push -u origin feature/f283-machine-contracts-part-two`
 with its real outcome; then
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY — this branch opens no pull request at its claim. Finally
 `gh run list --branch feature/f283-machine-contracts-part-two --limit 3 --json databaseId,status,conclusion,headSha`
 and report the run id and status as you read them. Do NOT wait for it.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 1 of feature F283, round 1, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 1, then round 2 — SLICE B, which threads `json_output` into `_cmd_show_job`,
`_cmd_create_job`, `_cmd_plan_job_local`, `_cmd_run_next_task_local` and
`_refuse_budget_set` and migrates their twenty sites. Name that `job.show` and `job.run`
both declare `supports_json: True` and both answer a failure in prose today, which is the
gap T001 exists to close. State the open-findings count, 23 after C2, and the
operator-questions count, 2.
