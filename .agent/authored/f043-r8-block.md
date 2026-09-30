STEP F043 R8 — THE CLOSURE SEQUENCE'S EVIDENCE ROUND: book round 7, bring the Built State current, reclaim staging copies, then build the evidence bundle and the review package at the accepted head

GOAL
Round 7 passed and the feature's full suite read exit 0 with no bad node. Book round 7's verdict,
the Built State's closure-suite paragraph and the plan in one commit; then run the closure
protocol's algorithm steps 1 and 2 (`docs/roadmap/STATUS_closure_protocol.md`): the staging-copy
reclaim of operator amendment amend0929-context-hygiene, the evidence job and the review package,
built from a clean, pushed tree at the accepted head, whose readings the closing round's STATUS
line will quote.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every change this round makes travels as a payload or is
produced by the payload tool; you write no code and no prose outside the handback.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r8/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f043-r8-evidence/`  Written by the evidence tool itself; never edit a file in it.
  every other `.remedy-wt/f043-*` path   The reviewer's; do not touch them.
  `.remedy-wt/f043-r8-worker/`    YOURS for logs and scripts; create it if absent. Gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace or a brace next to a quote is refused: write such a script to a
file under your own directory and run the file. Never run npm or npx. Stop a process only by its
own recorded pid, never with `pkill -f`. The `remedy` command may be denied; use
`python3 -m apps.cli.main` where a step names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f043-explanation-layer`, and `git log --oneline -1` must read `0e1329230`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f043-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 23 | 6011 | b9b90c21fa9b532e40971170ddc6a7287386bb72e6ecbd82619917acd478d8c4 |
| plan.md | 28 | 965 | 18faa259158bda7867c0f15a37f2c68de934a60c677196880d583a2bbdc04b21 |
| create_f043_evidence.py | 160 | 7765 | cf7f0878b36f87e801cc18914d13aa73a1d8b5ea510aeca23673922daadb0ed2 |

`plan.md` REWRITES `.agent/plan.md`, by `shutil.copyfile` and never by retyping. `records.diff`
(`git diff HEAD` from the reviewer's tree at `0e1329230`) appends round 7's gate entry to
`.agent/live_review.md` and the closure-suite paragraph to the Built State of
`docs/roadmap/features/T5_F043.md`. `create_f043_evidence.py` is a TOOL for A1, run from the
payload directory and never edited.

BUNDLE — C1, C2, A0, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f043-r8-block.md` := this block and each payload as
   `.agent/authored/f043-r8-<name>`, by `shutil.copyfile`. Subject `F043 R8 C1: copy round 8
   block and payloads`. Its insertions are this block's line count plus 211. Report the number you
   measure and STOP rather than commit if it is 500 or more.
C2 RECORDS: `git apply --check` then `git apply` records.diff, then `.agent/plan.md` := plan.md.
   Subject `F043 R8 C2: book round 7 and complete the Built State with the closure suite`.
   Expected by `git show --numstat`: 2/0 .agent/live_review.md, 6/6 .agent/plan.md, 3/0 docs/roadmap/features/T5_F043.md.
   C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE: its full sha is this closure's ACCEPTED HEAD;
   record it under that name. Push after C2, before A0.
A0 THE STAGING RECLAIM, an action committing nothing:
   `bash -c 'python3 -m apps.cli.main data reclaim --orphans > .remedy-wt/f043-r8-worker/reclaim.log 2>&1; echo "REAL_EXIT=$?"'`
   and report the log whole. The reviewer's read-only preview just before authoring read
   `Would free 0 B in 0 paths` with one refused path, `review_staging.n4o46eq_`,
   `class_not_job_keyed`. When your preview also lists no candidate, SKIP `--apply` and record the
   empty reading; when it lists a candidate, run
   `python3 -m apps.cli.main data reclaim --orphans --apply` the same way and report the freed total
   and every refused path with its reason.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
   `bash -c 'python3 .remedy-wt/f043-r8-payloads/create_f043_evidence.py > .remedy-wt/f043-r8-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`,
   with a Bash timeout of 1800000 milliseconds, and report the log's lines up to the summary. It
   writes the bundle to `.remedy-wt/f043-r8-evidence/`, gitignored, with base
   `21bfc1881b81902b267171d0486d82d1ed89fe25`, the FORK POINT, job id `f043r8e1001`, step range
   `T001-T003`, feature `f043` and run id `vr-0387`, and exits 1 when the two ancestry counts
   differ, when the collected count differs from the node ids it read, when a real node id is
   unsafe, when pytest fails, or when a validation fails. The reviewer's dry run from its tree
   carrying this round's C2 but no C1, into a scratch directory, read ancestry and plain counts
   equal at 57, 748 node ids collected with 2 deselected, none unsafe, the planted id answering
   `a local absolute path`, pytest exit 0 with 748 passed and 0 skipped, an EMPTY
   `validate_verification_tests` problem list, and `is_valid_current_run` True with no validation
   error; that tree held `apps/ui/node_modules` as an untracked link, which the bundle reads as a
   changed path, so the reviewer removed the link between the tests and the bundle — your checkout
   holds the real, ignored directory and needs nothing of the kind. At your C2 both ancestry counts
   read one more, for C1.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
   `bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f043-r8-evidence > .remedy-wt/f043-r8-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'`,
   WITHOUT setting `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The
   reviewer's dry run of the same script in its tree, over its scratch evidence and into a scratch
   directory, read `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS` and
   `EVIDENCE_AUTHORITATIVE=true` at exit 0. A failing package build is a closure BLOCKER: report
   the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying
   the reclaim reading, the evidence job id, the package name, its SHA-256, its archived directory,
   the accepted head and every gate reading. Subject `F043 R8 C3: rewrite handoff for round 8
   with the evidence and package readings`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f043-r8-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T5_F043.md` and
   `.agent/handoff.md`. No evidence directory, no package and no queue file is committed.
4. If the package does not read `READY_FOR_REVIEW`, or any other gate is red, STOP after recording
   the raw output: commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked", and hand back. Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED: no `gh pr merge`, no `gh pr create`, no STATUS or README
   edit, no ledger rotation, no queue edit, and no self-use run.
6. Delete nothing you did not create, except what `data reclaim --orphans --apply` frees when A0
   calls for it; every existing worktree and every branch stays.
7. A statement in the handback about what a tool produced quotes the tool's own output line.
8. DO NOT run the full suite: it ran in round 7, on `d6e77ea37`, and read exit 0.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C3 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f043-r8-*` copy byte-equal to its source by `git show <C1>:<path>`, the block
   copy against `.remedy-wt/f043-r8/block.md`.
G2 THE BOOKING: at C2 each file below, read with `git show <C2>:<path>`, hashes to the reviewer's
   tree:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 135097 | 04a3725abe586965fdf088cef9b83e0be6a2de854eeda11e86a99d8400d3fe0f |
   | .agent/plan.md | 965 | 18faa259158bda7867c0f15a37f2c68de934a60c677196880d583a2bbdc04b21 |
   | docs/roadmap/features/T5_F043.md | 8407 | bf74bb52f4d0cd17e964057d5a104dea9269c4f320e11b7bd4149cc951bcc6b6 |
   `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
   ledger at C2 — the reviewer's tree read `[]` and `PASS`; and, serially at C2,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   its counts and real exit code, which must be 0 (the reviewer's tree read `369 passed`).
G3 THE BUNDLE, at A1: the tool's real exit code; the two ancestry counts and their equality; the
   collected and deselected counts; the red control's two readings; pytest's exit code and counts;
   the `output_hash`; the `validate_verification_tests` problem list; `is_valid_current_run` and
   the validation errors; and the gate files the evidence directory holds.
G4 THE PACKAGE, at A2: the script's real exit code; `PACKAGE_STATUS`, which must read
   `READY_FOR_REVIEW` (exit 0 is not the reading); `REVIEW_SUBJECT_ALIGNMENT`;
   `EVIDENCE_AUTHORITATIVE`; the package filename; its SHA-256; the `committed_review_subject` base
   and head read from `.review_zip_manifest.json` INSIDE the package, head equal to C2's full sha
   and base equal to the fork point; `zipfile.is_zipfile` and `testzip()` answering None; and the
   absolute directory the package ended up in, or the literal `NOT ARCHIVED`.
G5 THE TREE, after A2: `python3 -m apps.cli.main integrity check --json`, six checks with status
   `pass` at `fail_count` 0 — each check's status is the reading, not the exit code;
   `git status --porcelain` empty; and `git worktree list | wc -l`.
G6 AFTER C3 AND THE PUSH, in your final reply only: `git status --porcelain` empty,
   `git log --oneline -n 4`, the push's real outcome, and `gh pr list --state open --json number`
   EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the reclaim reading, the evidence job id, the package name with
its SHA-256 and archived directory, the accepted head, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status
table AGENTS.md requires, one row per commit, action and gate. Session section: SESSION 1 of
feature F043, round 8, rounds so far 8, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, the review of round 8, then the closing round — the booking of round
8, the ledger rotation, the STATUS line with the README and the self-use queue in the same commit,
and the pull request. State the open-findings count as the tool reads it at C2, and "Operator
questions open: 0".
