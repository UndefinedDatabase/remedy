STEP F278 R10 — the first closure repair round: register and repair R-1039, and re-run the one full suite

GOAL
Book round 9's PASS, register R-1039 and record the self-use run's recurrence of R-1035, repair
R-1039 — the runtime-integration gate's registry check still pins `os.replace`, which round 4 moved
onto `durable_write` — and re-run the feature's full suite, whose five bad nodes must be gone with
no node newly bad (operator amendment amend0917-throughput rule 2, the shrinking rule).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors every payload; you apply them byte for
byte. This round closes nothing: no `docs/roadmap/STATUS.md`, no `README.md`, no
`scripts/self_use_queue.json`, no evidence job, no review zip, no pull request.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r10-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r10-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1 (`build_payloads.py`, `dry_repair.py`, `dry_booking.py`),
      which is read-only to you.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file. Capture real exit codes
as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. A directory outside
the repository is made with Python's `os.makedirs`. NEVER USE `git stash` IN ANY FORM, and never
check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f278-durable-writes-loud-failures`, `git log --oneline -1` reads `82c47da0`.
3. Verify this block's own bytes (R-0954): line count and sha256 of `.remedy-wt/f278-r10-block.md`
   against the two readings your delegation message states. Report both beside both, and stop if
   either differs.
4. Record, before anything runs: `git branch --list 'remedy/job-*'` count, `git worktree list`,
   and the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f278-r10-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| landed.md | 2 | 147 | c8b413fdd277719f569fe85627e917d7f89862ac50ccf864168fb05eff31654b |
| ledger.md | 6 | 6205 | 594167d26796f778b74edc0e9b41d37c0e42992daf22bbd76cf67774cac9d207 |
| plan.md | 31 | 1270 | f49281be6771a77c0371aa6fdfbdb91434276f12b24787eccdfa81f651d870c0 |
| repair.diff | 13 | 608 | fcce9fff5e85668d5b591661d00796b6bc295d8af626e7bf553e294d7dc11fd8 |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 9's
`Gate:` entry, the registration of R-1039 and a `Recurrence: R-1035` paragraph. `landed.md` is an
APPEND of one `Landed: R-1039` line, also beginning with a separating newline. `plan.md` is a
REWRITE. `repair.diff` is a `git apply` patch against `82c47da0`. Never retype or edit a payload.

BUNDLE — commits C1 to C4, in this order.

C1 — `.agent/authored/f278-r10-block.md` := this block; `.agent/authored/f278-r10-<name>` for each
  payload. Byte for byte, with `shutil.copyfile`.
  Subject: `F278 R10 C1: copy round 10 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md. The append is strict byte
  concatenation onto the file as it stands at `82c47da0`. This commit persists the finding FIRST,
  before any repair (docs/agents/planner_reviewer_prompt.md §4 item 4).
  Subject: `F278 R10 C2: book round 9's PASS, register R-1039, record R-1035's recurrence`

C3 — THE REPAIR: `git apply --check` then `git apply` of repair.diff, which changes the one
  `"pattern": "os.replace",` line of the `f146_registry_atomic_save` check in
  `packages/orchestration/runtime_integration_gate.py` to `"pattern": "durable_write(",`; and
  `.agent/live_review.md` += landed.md in the same commit.
  Subject: `F278 R10 C3: pin the registry check on durable_write, not os.replace (R-1039)`

C4 — THE FULL SUITE, re-run under the shrinking rule: `python3 -m pytest -n auto -q` in the
  PRIMARY checkout, after C3, with its log written outside the repository
  (`~/remedy-gate-scratch/f278-r10-suite.log`). REWRITE `.agent/authored/f278-closure-suite.txt`
  in the shape it already has — header naming round 10's C4, real exit code, summary line, the
  full list of bad node ids with its length, and the closure precondition 7 sentence — so the
  transcript belongs to the tree that ships (amend0921-operator-feedback rule 1); the round 9
  transcript stays in git history. Rewrite `.agent/handoff.md` per
  `docs/agents/handback_template.md` in this same commit.
  Subject: `F278 R10 C4: record the repaired suite transcript and rewrite handoff for round 10`
  Then `git push origin feature/f278-durable-writes-loud-failures`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f278-r10-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `.agent/authored/f278-closure-suite.txt` and `packages/orchestration/runtime_integration_gate.py`.
   Report the set you measure.
4. If the suite in C4 still lists a bad node, commit the transcript exactly as measured, report
   every bad node id and the shrinking reading, and hand back; the next repair is the reviewer's to
   order. Never weaken an assertion, delete a test or mark anything xfail on your own initiative.
5. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. Any Python you run that edits a module and then imports it again runs under `python3 -B`
   (checklist item 18).
7. Delete nothing you did not create as scratch; never delete a branch or a `remedy/job-*`
   worktree.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C4's handback text is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f278-r10-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f278-r10-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — read with `git show <commit>:.agent/live_review.md`:
 (a) By strict byte CONCATENATION onto the `82c47da0` bytes, the reviewer's dry run composed the
     ledger at C2 as 459330 bytes, sha256
     `dc0a16e000c814b320de877692f503af3ef7c36de036037074eca24c3b185e0b`, and at C3 as 459477
     bytes, sha256 `dff9cb12ada89fe31546426c67cd611ea59c84ddf7fb2e47eef9a30c3034c7d5`. Report
     yours beside them.
 (b) Line-anchored on the ledger at C3: `^Gate: F278 R9 — ` 1, `^- R-1039 — ` 1,
     `^Recurrence: R-1035 — ` 1, `^Landed: R-1039 — ` 1. Open set by distinct id via
     `open_finding_ids` from `scripts/rotate_live_review.py` at `82c47da0` and at C2: the reviewer
     measured 26 and 27, ADDED `R-1039`, REMOVED none.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (under 50).

G3 THE REPAIR — at C3: `git diff <C2> <C3> -- packages/orchestration/runtime_integration_gate.py`
 equals repair.diff byte for byte. `python3 -m ruff check packages/orchestration/runtime_integration_gate.py`
 exit 0. Then, in the primary checkout, `python3 -m pytest -q -p no:cacheprovider` over
 `tests/orchestration/test_runtime_integration_gate.py`,
 `tests/orchestration/test_f018_authority_integration.py`,
 `tests/orchestration/test_f018_package_pipeline_e2e.py`,
 `tests/orchestration/test_f146_package_pipeline_e2e.py`,
 `tests/orchestration/test_project_resolution.py`, `tests/test_project_registry.py` and
 `tests/cli/test_golden_path.py`: exit 0. The reviewer's dry run of the first six at `82c47da0`
 with the repair applied read `314 passed`; report yours with the golden path added.

G4 THE RED PROOF — in a disposable worktree `.remedy-wt/f278-r10-mut` added at C3, under
 `python3 -B -m pytest -q -p no:cacheprovider` over the five node ids the round 9 transcript
 lists: CONTROL first, which must read `5 passed` at exit 0; then replace the exact bytes
 `"pattern": "durable_write(",` in `packages/orchestration/runtime_integration_gate.py` — they
 occur exactly once in that file at C3; report the count — with `"pattern": "os.replace",` and
 run the same five, which must read `5 failed` at exit 1; restore the file from its saved bytes and
 report the restore byte-identical. Remove the worktree, `git worktree prune`, and report
 `git worktree list`.

G5 THE SUITE AND THE SHRINKING RULE — at C4: `python3 -m pytest -n auto -q` in the primary
 checkout, its real exit code, its summary line and the complete list of bad node ids with its
 length, all in the rewritten `.agent/authored/f278-closure-suite.txt`. Then the shrinking reading:
 the previous bad set (the five ids of the round 9 transcript at `82c47da0`), the new bad set,
 whether the new set is a strict subset, and every node newly bad. Report whether
 `tests/orchestration/test_import_reachability.py` and `tests/test_no_orphan_modules.py` are among
 the bad nodes. Then `python3 -m apps.cli.main integrity check --json` — all five checks `pass`
 — and `git status --porcelain`, empty.

G6 TREE AND PUSH — after C4: `git status --porcelain` empty; `git log --oneline -n 6`; `git
 worktree list`; `git stash list`'s first line unchanged from its reading before C1; the push's
 real outcome; `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item and gate: state block, the per-commit changed-files
table with the insertions git MEASURED, every gate's real output and exit code, the suite's
summary line, bad node ids and shrinking reading, the deviations, and the next action. Your
Session section reads SESSION 2 of feature F278, round 10, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
10, then the closure sequence's second half — the evidence job and the review zip — and then the
closing round: the ledger rotation, the STATUS line with the README counters in the same commit,
and the pull request. State the open-findings count, 27 after this round until R-1039's
resolution is booked, and the operator-questions count, 0.
