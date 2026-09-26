STEP F289 R6 — THE CLOSURE SEQUENCE'S EVIDENCE ROUND: BOOK ROUND 5, BUILD THE BUNDLE AND THE PACKAGE

GOAL
Round 5 passed with the one full suite green. Book it, then build F289's evidence bundle at the
accepted head and its review package, per `docs/roadmap/STATUS_closure_protocol.md` Algorithm
steps 1 and 2.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full. You never issue a verdict and never merge. Every
change travels as a payload or is produced by a payload tool; you write no code.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f289-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f289-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f289-r6-evidence/`  Where A1 writes the bundle; gitignored, never committed.
  `.remedy-wt/f289-r6-dry/`, `.remedy-wt/f289-r6-sim/`, `.remedy-wt/f289-r6-drafts/` and
  `.remedy-wt/f289-review/`       The reviewer's; do not touch them.
  `.remedy-wt/f289-r6-worker/`    YOURS for logs and scripts; create it if absent.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`
rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`); a
heredoc containing a dollar-brace is refused, so write such a script to a file under your own
directory. Never run npm or npx.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f289-self-use-sources`, and `git log --oneline -1` must read `ba713c34`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f289-r6/block.md` against the two readings your delegation message states; report
   both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f289-r6-payloads/`, lines = newline count. Verify each BEFORE use.

| file | lines | bytes | sha256 |
|---|---|---|---|
| create_f289_evidence.py | 148 | 7143 | c9bb8fc27b975306e39f6e101b66b511e9a2cf3ee04297093f9fff8930a23115 |
| plan.md | 26 | 812 | 7703244cbc2cc4664a196e7a3905c000d874e05b26b812b843a8859611b5b729 |
| records.diff | 10 | 7930 | 0b42e8991f3f7172ec37c83f60e1be24cc3b534b14e52f955b82835a6ff1878e |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `ba713c34`)
appends round 5's gate entry to `.agent/live_review.md`. `create_f289_evidence.py` is a TOOL for
A1, run from the payload directory and never edited.

BUNDLE — C1, C2, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f289-r6-block.md` := this block and each payload as
   `.agent/authored/f289-r6-<name>`, by `shutil.copyfile`. Subject `F289 R6 C1: copy round 6 block
   and payloads`. Its insertions are this block's line count plus 184.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject `F289 R6 C2: book
   round 5`. Expected by `git show --numstat`: 2/0 .agent/live_review.md, 6/7 .agent/plan.md. C2 IS
   THE LAST CONTENT COMMIT BEFORE THE PACKAGE: its full sha is this closure's ACCEPTED HEAD; record
   it under that name. Push after C2, before A1.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
   `bash -c 'python3 .remedy-wt/f289-r6-payloads/create_f289_evidence.py >
   .remedy-wt/f289-r6-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`, and report the log's lines up to
   the summary. It writes the bundle to `.remedy-wt/f289-r6-evidence/`, gitignored, with base
   `d0239fa348ca0685470d98549628a689ed288dc9`, the FORK POINT, job id `f289r6e1001`, step range
   `T001-T003`, feature `f289` and run id `vr-1074`. It exits 1 when the two ancestry counts differ,
   when the collected count differs from the node ids it read, when a real node id is unsafe, or when
   a validation fails. The reviewer's dry run from the primary checkout at `ba713c34`, into a scratch
   directory, read ancestry and plain counts equal at 32, 634 node ids collected with 2 deselected,
   none unsafe, the planted id answering `a local absolute path`, pytest exit 0 with 634 passed and
   0 skipped, an EMPTY `validate_verification_tests` problem list, and `is_valid_current_run` True
   with no validation error. At C2 both ancestry counts read two more.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
   `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f289-r6-evidence`, WITHOUT setting
   `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The reviewer's dry run of the
   same command at `ba713c34`, over its scratch evidence and into a scratch directory, read
   `PACKAGE_STATUS=READY_FOR_REVIEW` and `EVIDENCE_AUTHORITATIVE=true`. A failing package build is a
   closure BLOCKER: report the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying the
   evidence job id, the package name, its SHA-256, its archived directory, the accepted head and every
   gate reading. Subject `F289 R6 C3: rewrite handoff for round 6 with the evidence and package
   readings`. Then `git push`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f289-r6-*` copies,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. No evidence directory is
   committed.
4. If the package does not read `READY_FOR_REVIEW`, or any other gate is red, STOP after recording the
   raw output: commit and push what is verified, write the handoff under AGENTS.md "If Blocked", and
   hand back. Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED: no `gh pr merge`, no `gh pr create`, no STATUS or README edit,
   no ledger rotation, no `consumed_by` edit.
6. Delete nothing you did not create; every existing worktree and every branch stays.
7. A statement in the handback about what a tool produced quotes the tool's own output line.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run before
C3 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f289-r6-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING: at C2 each file below, read with `git show <C2>:<path>`, hashes to the reviewer's
   simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 333667 | 349153378594733fe465cf272d9f9791ac834972af0b06027edba524848d1023 |
   | .agent/plan.md | 812 | 7703244cbc2cc4664a196e7a3905c000d874e05b26b812b843a8859611b5b729 |
   `open_finding_ids` over the ledger at C2 — the reviewer's simulation read `[]`; and, serially at
   C2, `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py`, exit 0,
   which the reviewer's simulation read at 369 passed.
G3 THE BUNDLE, at A1: the script's real exit code; the two ancestry counts and their equality; the
   collected and deselected counts; the red control's two readings; pytest's exit code and counts;
   the `output_hash`; the `validate_verification_tests` problem list; `is_valid_current_run` and the
   validation errors; and the gate files the evidence directory holds.
G4 THE PACKAGE, at A2: `PACKAGE_STATUS`, which must read `READY_FOR_REVIEW` (exit 0 is not the
   reading); `EVIDENCE_AUTHORITATIVE`; the package filename; its SHA-256; the
   `committed_review_subject` base and head read from `.review_zip_manifest.json` INSIDE the package,
   head equal to C2's full sha and base equal to the fork point; `zipfile.is_zipfile` and `testzip()`
   answering None; and the absolute directory the package ended up in, or the literal `NOT ARCHIVED`.
G5 THE TREE, after A2: `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count`
   0; `git status --porcelain` empty; and `git worktree list | wc -l`.
G6 AFTER C3 AND THE PUSH, in your final reply only: `git status --porcelain` empty, `git log
   --oneline -n 4`, the push's real outcome, and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the evidence job id, the package name with its SHA-256 and archived
directory, the accepted head, the authored-text proofs, the item-status table AGENTS.md requires (one
row per commit, action and gate), the deviations, and the next action. Session section: SESSION 1 of
feature F289, round 6, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1,
the review of round 6, then the closing round — the booking of round 6, the ledger rotation, SU-033's
`consumed_by`, the STATUS line with the README counters in the same commit, and the pull request.
State the open-findings count as the script reads it at C2, and "Operator questions open: 0".
