STEP F025 R10 — THE CLOSURE SEQUENCE'S EVIDENCE HALF: BOOK ROUND 9, REGISTER R-1057 AND R-1058, BUILD THE BUNDLE AND THE PACKAGE

GOAL
Book round 9's PASS, whose one full suite is green, and register the two findings its self-use run
raised, R-1057 and R-1058, both owned by F285 with their Acceptance lines in F285's file; then build
this feature's evidence bundle against the fork point and the fresh review package, recording the
evidence job id, the package name, its SHA-256, the directory it ends up in and the accepted HEAD.
Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict and never merge. The reviewer authors every payload, the evidence script included;
you run it and never edit it. Read first: `docs/roadmap/STATUS_closure_protocol.md`'s algorithm
steps 1 and 2 with their pitfalls, and `.agent/authored/f024-r7-block.md`, which this round follows.

THE DIRECTORIES
  `.remedy-wt/f025-r10/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r10-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`, never `cd` your shell into a worktree.
Copy and hash with python (`shutil.copyfile`). Never run npm or npx, never `git stash`, and never
check out another commit in the primary checkout.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In the primary checkout `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain`
   must be empty, `git branch --show-current` must read `feature/f025-pause-resume`, and
   `git log --oneline -1` must read `9cceb4cd`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r10/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r10/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| create_f025_evidence.py | 171 | 8703 | e6584e10b4ca80f85f60e9b3a3866bf4f0be8167afcb3db1de513909f06c3628 |
| f285_from.txt | 3 | 262 | f463144f938342096dc23f1a3737a21c2a76f4c32087175f738d63bfe6647d97 |
| f285_to.txt | 9 | 798 | efb16ee24d70c1a5f6f5821cf94f7911ca44e99cfa79361918eed54cad4b8fc7 |
| ledger.md | 6 | 6012 | 95c52aab6d92b41890c1c1128bccd88f14dd361e1686022a53ad54b9a78e1a0a |
| plan.md | 29 | 992 | 08e4c625958fd74a34fd65dd865671cfb68f5a8f33929caae212b25b9e303bf7 |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line); `plan.md`
REWRITES `.agent/plan.md`. In `docs/roadmap/features/T2_F285.md` the bytes of `f285_from.txt` are
replaced by the bytes of `f285_to.txt` — containment test: TO contains FROM: true, so the pair is an
APPEND: FROM occurs exactly once in the file before the edit, and after it TO occurs exactly once
and the file equals its `9cceb4cd` bytes with FROM replaced by TO. `create_f025_evidence.py` is a
TOOL for A1, run from the payload directory and never edited.

BUNDLE — C1, C2, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f025-r10-block.md` := this block and each payload as
    `.agent/authored/f025-r10-<name>`. Subject `F025 R10 C1: copy round 10 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 218, that is the block copy's own lines and 171/0 `.agent/authored/f025-r10-create_f025_evidence.py`, 3/0 `.agent/authored/f025-r10-f285_from.txt`, 9/0 `.agent/authored/f025-r10-f285_to.txt`, 6/0 `.agent/authored/f025-r10-ledger.md`, 29/0 `.agent/authored/f025-r10-plan.md`.
C2 RECORDS, one commit, the findings persisted FIRST: the ledger append, the plan rewrite and the
    F285 pair. Subject `F025 R10 C2: book round 9's PASS, register R-1057 and R-1058 for F285`.
    Expected: 6/0 `.agent/live_review.md`, 8/9 `.agent/plan.md`, 6/0 `docs/roadmap/features/T2_F285.md`. C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE: its full sha is this
    closure's ACCEPTED HEAD; record it under that name. Push after C2, before A1.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
    `bash -c 'python3 .remedy-wt/f025-r10/create_f025_evidence.py >
    .remedy-wt/f025-r10-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`, and report the log's
    lines up to the summary. It writes the bundle to `.remedy-wt/f025-r10-evidence/`, gitignored,
    with base `49624d5c8def4b270697a8c0025e2ab3efc197a7`, the FORK POINT, job id `f025r10e1001`,
    step range `T001-T003`, feature `f025` and run id `vr-1054`. It exits 1 when the two ancestry
    counts differ, when the collected count differs from the node ids it read, when a real node id
    is unsafe, or when a validation fails. The reviewer's dry run at `9cceb4cd`, into a scratch
    directory, read ancestry and plain counts equal at 72, 1033 node ids collected with 4 deselected, none unsafe, the planted id answering `a local absolute path`, pytest exit 0 with 1033 passed and 0 skipped, an EMPTY `validate_verification_tests` problem list, and `is_valid_current_run` True with no validation error. At C2 both ancestry counts read two more.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
    `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f025-r10-evidence`, without setting
    `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The reviewer's dry run of
    the same command at `9cceb4cd`, over its scratch evidence and into a scratch directory, read
    `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true` and `review_subject_alignment` `PASS`. A failing package build is a closure BLOCKER: report the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying the
    evidence job id, the package name, its SHA-256, its archived directory, the accepted HEAD and
    every gate reading. Subject `F025 R10 C3: rewrite handoff for round 10 with the evidence and
    package readings`. Then `git push origin feature/f025-pause-resume`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. Append and replace by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f025-r10-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T2_F285.md` and
   `.agent/handoff.md`. No evidence directory is ever committed.
4. If the package does not read `READY_FOR_REVIEW`, or any other gate is red, STOP after recording
   the raw output: commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked", and hand back. Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED: no `gh pr merge`, no `gh pr create`, no STATUS or README
   edit, no ledger rotation, no `consumed_by` edit.
6. Delete nothing you did not create; every existing worktree and every `remedy/job-*` branch
   stays as it is.
7. A statement in the handback about what a tool produced quotes the tool's own output line.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C3 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r10-*` payload copy byte-equal to its source by `git show <C1>:<path>`
   (the block copy against `.remedy-wt/f025-r10/block.md`).
G2 THE BOOKING: at C2 `.agent/live_review.md` equals its `9cceb4cd` bytes plus ledger.md,
   `.agent/plan.md` equals plan.md, and the F285 pair holds as PAYLOADS states; `open_finding_ids`
   over the ledger at C2 — the reviewer's simulation read `['R-1008', 'R-1055', 'R-1057', 'R-1058']`; and, serially at C2,
   `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py`, exit 0.
G3 THE BUNDLE, at A1: the script's real exit code; the two ancestry counts and their equality; the
   collected and deselected counts; the red control's two readings; pytest's exit code and counts;
   the `output_hash`; the `validate_verification_tests` problem list; `is_valid_current_run` and
   the validation errors; and the gate files the evidence directory holds.
G4 THE PACKAGE, at A2: `PACKAGE_STATUS`, which must read `READY_FOR_REVIEW` (exit 0 is not the
   reading); `EVIDENCE_AUTHORITATIVE`; the package filename; its SHA-256; the
   `committed_review_subject` base and head read from `.review_zip_manifest.json` INSIDE the
   package, head equal to C2's full sha and base equal to the fork point; `zipfile.is_zipfile` and
   `testzip()` answering None; and the absolute directory the package ended up in, or the literal
   `NOT ARCHIVED`.
G5 THE TREE, after A2: `python3 -m apps.cli.main integrity check --json`, six `pass` at
   `fail_count` 0; `git status --porcelain` empty; and `git worktree list`.
G6 AFTER C3 AND THE PUSH, in your final reply only: `git status --porcelain` empty, `git log
   --oneline -n 4`, the push's real outcome, and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the evidence job id, the package name with its SHA-256 and
archived directory, the accepted HEAD, the authored-text proofs, the item-status table AGENTS.md
requires (one row per commit, action and gate), the deviations, and the next action. Session
section: SESSION 2 of feature F025, round 10, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, the review of round 10, then the closing round — the booking of round
10, the ledger rotation, the STATUS line with the README counters and the self-use item's
`consumed_by` in the same commit, and the pull request. State the open-findings count as the
script reads it at C2, and "Operator questions open: <the count of `### Q` headings at C2>".
