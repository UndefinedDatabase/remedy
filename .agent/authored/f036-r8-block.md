STEP F036 R8 — THE CLOSURE SEQUENCE'S EVIDENCE ROUND: book round 7, read the self-use generator, then build the evidence bundle and the review package at the accepted head

GOAL
Round 7 passed and the one full suite is green. Book round 7's verdict with the resolution of
R-1090, read the self-use generator (closure precondition 6), then run the closure
protocol's algorithm steps 1 and 2 (`docs/roadmap/STATUS_closure_protocol.md`): the evidence job
and the review package, built from a clean, pushed tree at the accepted head, whose readings the
closing round's STATUS line will quote.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every change this round makes travels as a payload or is
produced by the payload tool; you write no code and no prose outside the handback.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f036-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f036-r8/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f036-r8-evidence/`  Written by the evidence tool itself; never edit a file in it.
  `.remedy-wt/f036-r8-sim/`, `.remedy-wt/f036-r8-dryev/`, `.remedy-wt/f036-r8-dryzip/` and
  `.remedy-wt/f036-review/`       The reviewer's; do not touch them.
  `.remedy-wt/f036-r8-worker/`    YOURS for logs and scripts; create it if absent. Gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace or a backslash inside an f-string is refused or fails: write such
a script to a file under your own directory and run the file. Never run npm or npx. The `remedy`
command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f036-guided-result-tour`, and `git log --oneline -1` must read `6842325a`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f036-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 12 | 5122 | df52ceafeb4179852c3feda72d7fbd8cee1fc8e89ef4b2980b138091b51cd8a3 |
| create_f036_evidence.py | 164 | 7969 | 2f33db1973c7c898d73976e30a2af98cbb2c89e23a6657c24141354d3b0e4b3a |
| plan.md | 27 | 908 | 7165b60fd9e75258ee4c871c5589ed37c03c6cbd2cda3b137de3888a71c95c8a |

`plan.md` REWRITES `.agent/plan.md`, by `shutil.copyfile` and never by retyping. `booking.diff`
(`git diff HEAD` from a tree at `6842325a`) appends round 7's gate entry and the `Done:` line of
R-1090 to `.agent/live_review.md`.
`create_f036_evidence.py` is a TOOL for A1, run from the payload directory and never edited.

BUNDLE — C1, C2, A0, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f036-r8-block.md` := this block and each payload as
   `.agent/authored/f036-r8-<name>`, by `shutil.copyfile`. Subject `F036 R8 C1: copy round 8
   block and payloads`. Its insertions are this block's line count plus 203. Report the number you
   measure and STOP rather than commit if it is 500 or more.
C2 RECORDS: `git apply --check` then `git apply` booking.diff, then `.agent/plan.md` := plan.md.
   Subject `F036 R8 C2: book round 7, resolve R-1090`.
   Expected by `git show --numstat`: 4/0 `.agent/live_review.md`, 6/9 `.agent/plan.md`. C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE: its full
   sha is this closure's ACCEPTED HEAD; record it under that name. Push after C2, before A0.
A0 THE SELF-USE READING, an action committing nothing. From the repository root at C2, in a Python
   file of yours: `packages.orchestration.self_use_generator.generate_and_append_if_empty()` with
   no arguments, then `packages.orchestration.self_use_queue.next_self_use_item()`; report both
   return values and `git status --porcelain` after. The reviewer's run of the same two calls in its
   simulation tree read `None` and `None` and wrote nothing, so closure precondition 6 reads
   `self-use NONE (queue exhausted)`. If yours appends an item or answers anything but `None`,
   STOP: do not commit the queue file, restore it with `git checkout -- scripts/self_use_queue.json`,
   write the handoff under AGENTS.md "If Blocked" with the raw output, and hand back.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
   `bash -c 'python3 .remedy-wt/f036-r8-payloads/create_f036_evidence.py > .remedy-wt/f036-r8-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`,
   with a Bash timeout of 1800000 milliseconds, and report the log's lines up to the summary. It
   writes the bundle to `.remedy-wt/f036-r8-evidence/`, gitignored, with base
   `9dc2f2a796d48a47119252c1ec8634230b00bf90`, the FORK POINT, job id `f036r8e1001`, step range
   `T001-T003`, feature `f036` and run id `vr-0361`. It exits 1 when the two ancestry counts differ,
   when the collected count differs from the node ids it read, when a real node id is unsafe, or
   when a validation fails. The reviewer's dry run from the primary checkout at `6842325a`, into a
   scratch directory, read ancestry and plain counts equal at 51, 1258 node ids collected with 7
   deselected, none unsafe, the planted id answering `a local absolute path`, pytest exit 0 with
   1255 passed and 3 skipped, an EMPTY `validate_verification_tests` problem list, and
   `is_valid_current_run` True with no validation error. At C2 both ancestry counts read two more.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
   `bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f036-r8-evidence > .remedy-wt/f036-r8-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'`,
   WITHOUT setting `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The
   reviewer's dry run of the same script at `6842325a`, over its scratch evidence and into a
   scratch directory, read `PACKAGE_STATUS=READY_FOR_REVIEW` and `EVIDENCE_AUTHORITATIVE=true` at
   exit 0. A failing package build is a closure BLOCKER: report the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying
   the self-use reading, the evidence job id, the package name, its SHA-256, its archived
   directory, the accepted head and every gate reading. Subject `F036 R8 C3: rewrite handoff for
   round 8 with the evidence and package readings`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f036-r8-*` copies,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. No evidence directory, no package and no queue file is committed.
4. If the package does not read `READY_FOR_REVIEW`, or any other gate is red, STOP after recording
   the raw output: commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked", and hand back. Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED: no `gh pr merge`, no `gh pr create`, no STATUS or README
   edit, no ledger rotation, no `consumed_by` edit.
6. Delete nothing you did not create; every existing worktree and every branch stays.
7. A statement in the handback about what a tool produced quotes the tool's own output line.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C3 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f036-r8-*` copy byte-equal to its source by `git show <C1>:<path>`, the block
   copy against `.remedy-wt/f036-r8/block.md`.
G2 THE BOOKING: at C2 each file below, read with `git show <C2>:<path>`, hashes to the reviewer's
   simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 341971 | 233d6cc5e3ee36457ed1a1222beef4035d9077df886e99554de6d27129d6eb4d |
   | .agent/plan.md | 908 | 7165b60fd9e75258ee4c871c5589ed37c03c6cbd2cda3b137de3888a71c95c8a |
   `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the reviewer's
   simulation read `[]`; and, serially at C2,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the reviewer's simulation read at 369 passed, exit 0.
G3 THE BUNDLE, at A1: the tool's real exit code; the two ancestry counts and their equality; the
   collected and deselected counts; the red control's two readings; pytest's exit code and counts;
   the `output_hash`; the `validate_verification_tests` problem list; `is_valid_current_run` and
   the validation errors; and the gate files the evidence directory holds.
G4 THE PACKAGE, at A2: the script's real exit code; `PACKAGE_STATUS`, which must read
   `READY_FOR_REVIEW` (exit 0 is not the reading); `EVIDENCE_AUTHORITATIVE`; the package filename;
   its SHA-256; the `committed_review_subject` base and head read from `.review_zip_manifest.json`
   INSIDE the package, head equal to C2's full sha and base equal to the fork point;
   `zipfile.is_zipfile` and `testzip()` answering None; and the absolute directory the package
   ended up in, or the literal `NOT ARCHIVED`.
G5 THE TREE, after A2: `python3 -m apps.cli.main integrity check --json`, six checks with status
   `pass` at `fail_count` 0 — each check's status is the reading, not the exit code;
   `git status --porcelain` empty; and `git worktree list | wc -l`.
G6 AFTER C3 AND THE PUSH, in your final reply only: `git status --porcelain` empty,
   `git log --oneline -n 4`, the push's real outcome, and `gh pr list --state open --json number`
   EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the self-use readings, the evidence job id, the package name with
its SHA-256 and archived directory, the accepted head, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status
table AGENTS.md requires, one row per commit, action and gate. Session section: SESSION 2 of
feature F036, round 8, rounds so far 8, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, the review of round 8, then the closing round — the booking of round 8,
the ledger rotation, the STATUS line with the README counters in the same commit, and the pull
request. State the open-findings count as the tool reads it at C2, and "Operator questions open:
1".
