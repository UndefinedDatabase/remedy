STEP F028 R11 — THE CLOSURE SEQUENCE'S EVIDENCE ROUND: book round 10, then build the evidence bundle and the review package at the accepted head

GOAL
Round 10 passed and the one full suite is green. Book round 10's verdict, then run the closure
protocol's algorithm steps 1 and 2 (`docs/roadmap/STATUS_closure_protocol.md`): the evidence job and
the review package, built from a clean, pushed tree at the accepted head, whose readings the
closing round's STATUS line will quote.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every change this round makes travels as a payload or is
produced by the payload tool; you write no code and no prose outside the handback.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r11-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r11/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r11-evidence/`  Written by the evidence tool itself; never edit a file in it.
  `.remedy-wt/f028-r10-sim/`, `.remedy-wt/f028-r11-drafts/`, `.remedy-wt/f028-r11-dryev/`,
  `.remedy-wt/f028-r11-dryzip/` and `.remedy-wt/f028-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f028-r11-worker/`    YOURS for logs and scripts; create it if absent. Gitignored.

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
   `feature/f028-task-injection`, and `git log --oneline -1` must read `9023b29b`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r11/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r11-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| create_f028_evidence.py | 167 | 8400 | eb10b5703bf6fa3d3a13a5e5e678c4c46d5309f8aaf8a1ed47eec0f44581a95f |
| plan.md | 25 | 802 | 222cbd69da9cb71a57dc7bf8d13e77c29e3933f6a531fb0bb10595686a61d2d6 |
| records.diff | 10 | 4908 | 928f85e5a560154423a450630b28b93bfc1810619d892cc6f6638f5d0eaddfe3 |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `9023b29b`)
appends round 10's gate entry to `.agent/live_review.md` after one blank line.
`create_f028_evidence.py` is a TOOL for A1, run from the payload directory and never edited.

BUNDLE — C1, C2, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f028-r11-block.md` := this block and each payload as
   `.agent/authored/f028-r11-<name>`, by `shutil.copyfile`. Subject `F028 R11 C1: copy round 11 block
   and payloads`. Its insertions are this block's line count plus 202. Report the number you
   measure and STOP rather than commit if it is 500 or more.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject `F028 R11 C2: book
   round 10`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`, 5/10 `.agent/plan.md`.
   C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE: its full sha is this closure's ACCEPTED HEAD;
   record it under that name. Push after C2, before A1.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
   `bash -c 'python3 .remedy-wt/f028-r11-payloads/create_f028_evidence.py > .remedy-wt/f028-r11-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`,
   with a Bash timeout of 1800000 milliseconds, and report the log's lines up to the summary. It
   writes the bundle to `.remedy-wt/f028-r11-evidence/`, gitignored, with base
   `ceb90b8a8304e8ef95490b8f41a5860d061ad5c7`, the FORK POINT, job id `f028r11e1001`, step range
   `T001-T003`, feature `f028` and run id `vr-0281`. It exits 1 when the two ancestry counts differ,
   when the collected count differs from the node ids it read, when a real node id is unsafe, or
   when a validation fails. The reviewer's dry run from the primary checkout at `9023b29b`, into a
   scratch directory, read ancestry and plain counts equal at 69, 1362 node ids collected with 6
   deselected, none unsafe, the planted id answering `a local absolute path`, pytest exit 0 with
   1362 passed and 0 skipped, an EMPTY `validate_verification_tests` problem list, and
   `is_valid_current_run` True with no validation error. At C2 both ancestry counts read two more.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
   `bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f028-r11-evidence > .remedy-wt/f028-r11-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'`,
   WITHOUT setting `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The
   reviewer's dry run of the same script at `9023b29b`, over its scratch evidence and into a
   scratch directory, read `PACKAGE_STATUS=READY_FOR_REVIEW` and `EVIDENCE_AUTHORITATIVE=true`. A
   failing package build is a closure BLOCKER: report the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying
   the evidence job id, the package name, its SHA-256, its archived directory, the accepted head and
   every gate reading. Subject `F028 R11 C3: rewrite handoff for round 11 with the evidence and
   package readings`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f028-r11-*` copies,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. No evidence directory and no
   package is committed.
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
   `.agent/authored/f028-r11-*` copy byte-equal to its source by `git show <C1>:<path>`, the block
   copy against `.remedy-wt/f028-r11/block.md`.
G2 THE BOOKING: at C2 each file below, read with `git show <C2>:<path>`, hashes to the reviewer's
   simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 341062 | fd65ca2a07874ee93b459000068906a66c17550c2497c575951a0c4d5dcdc08f |
   | .agent/plan.md | 802 | 222cbd69da9cb71a57dc7bf8d13e77c29e3933f6a531fb0bb10595686a61d2d6 |
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
above, every gate's real output, the evidence job id, the package name with its SHA-256 and archived
directory, the accepted head, the authored-text proofs, the deviations, the next action, and —
INSIDE `.agent/handoff.md` itself, as its own section — the item-status table AGENTS.md requires,
one row per commit, action and gate. Session section: SESSION 2 of feature F028, round 11, rounds so
far 11, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of
round 11, then the closing round — the booking of round 11, the ledger rotation, the STATUS line with the README counters in the same commit, and the pull request.
State the open-findings count as the tool reads it at C2, and "Operator questions open: 0".
