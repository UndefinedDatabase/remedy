STEP F285 R5 — THE CLOSURE SEQUENCE'S EVIDENCE ROUND: BOOK ROUND 4, RESOLVE R-1064 AND R-1008, BUILD THE BUNDLE AND THE PACKAGE

GOAL
Book round 4's PASS, whose one full suite is green on the tree that ships, resolve R-1064 and
R-1008 — the second by the first self-use run in the track's history whose diff landed as a
repair — then build this feature's evidence bundle against the fork point and the fresh review
package, recording the evidence job id, the package name, its SHA-256, the directory it ends up in
and the accepted head. Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue
a verdict and never merge. The reviewer authors every payload, the evidence script included; you run
it and never edit it. Read first: `docs/roadmap/STATUS_closure_protocol.md`'s algorithm steps 1 and 2
with their pitfalls, and `.agent/authored/f026-r7-block.md`, which this round follows.

THE DIRECTORIES
  `.remedy-wt/f285-r5-payloads/` and `.remedy-wt/f285-r5/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f285-r5-dry/`, `.remedy-wt/f285-r5-drafts/`, `.remedy-wt/f285-r5-evdry/`,
  `.remedy-wt/f285-r5-zipdry/`   The reviewer's; do not touch them.
  `.remedy-wt/f285-r5-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, and one-liners chained with `;` or
`&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C
<path>`; never `cd` into a worktree. Never run npm or npx, never `git stash`, never check out another
commit in the primary checkout.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f285-findings-paydown-v4`, `git log --oneline -1` `9a7a9c39`.
3. Measure this block's line count and sha256 (`.remedy-wt/f285-r5/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f285-r5-payloads/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| create_f285_evidence.py | 159 | 7964 | 20d3da5cb99dfed5f487c53c3e83b818f1e769b1898db31009e316015c6ddb53 |
| plan.md | 27 | 885 | 4824677b44edc2a3551e5cd08e6d170bdf4256ef50773849c7ebe7da6ff7176b |
| records.diff | 14 | 8788 | 60db6dfc6906b6a557d6d6dc0704d3752c5e8817b7165791f7af51efec5d35a8 |
`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `9a7a9c39`)
appends round 4's gate entry and the `Done:` paragraphs of R-1064 and R-1008 to
`.agent/live_review.md`. `create_f285_evidence.py` is a TOOL for A1, run from the payload directory
and never edited.

BUNDLE — C1, C2, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f285-r5-block.md` := this block and each payload as
   `.agent/authored/f285-r5-<name>`, by `shutil.copyfile`. Subject `F285 R5 C1: copy round 5 block and
   payloads`. Its insertions: 333 (this block's 133 lines plus 200 for the three payloads).
C2 RECORDS, one commit: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject
   `F285 R5 C2: book round 4, resolve R-1064 and R-1008`. Expected by `git show --numstat`:
   6/0 .agent/live_review.md, 8/11 .agent/plan.md. C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE: its full sha is this closure's
   ACCEPTED HEAD; record it under that name. Push after C2, before A1.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
   `bash -c 'python3 .remedy-wt/f285-r5-payloads/create_f285_evidence.py >
   .remedy-wt/f285-r5-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`, and report the log's lines up to
   the summary. It writes the bundle to `.remedy-wt/f285-r5-evidence/`, gitignored, with base
   `83d3bb95901313a529d803a2cb29b2291b34e608`, the FORK POINT, job id `f285r5e1001`, step range
   `T001-T003`, feature `f285` and run id `vr-1064`. It exits 1 when the two ancestry counts differ,
   when the collected count differs from the node ids it read, when a real node id is unsafe, or when
   a validation fails. The reviewer's dry run from the primary checkout at `9a7a9c39`, into a scratch
   directory, read: `ancestry-path count 24` and `plain count 24`; `collected node ids 765, deselected 13`; `red control: unsafe among the real ids 0 []` and `red control: planted id -> a local absolute path`; `pytest exit 0, {'passed': 765, 'failed': 0, 'skipped': 0}, output_hash 6e8ca37cef6ac9337c58d15209b0f1113a3dbb65345d894408e90b0fa2939559`; `validate_verification_tests problems [] passed 765`; `is_valid_current_run True` with `validation_errors []`.
   At C2 both ancestry counts read two more.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
   `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f285-r5-evidence`, WITHOUT setting
   `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The reviewer's dry run of the
   same command at `9a7a9c39`, over its scratch evidence and into a scratch directory, read
   `ZIP CREATED AND READY FOR FINAL REVIEW` and a `READY_FOR_REVIEW` package name. A failing package
   build is a closure BLOCKER: report the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying the
   evidence job id, the package name, its SHA-256, its archived directory, the accepted head and every
   gate reading. Subject `F285 R5 C3: rewrite handoff for round 5 with the evidence and package
   readings`. Then `git push origin feature/f285-findings-paydown-v4`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f285-r5-*` copies,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. No evidence directory is
   committed.
4. If the package does not read `READY_FOR_REVIEW`, or any other gate is red, STOP after recording the
   raw output: commit and push what is verified, write the handoff under AGENTS.md "If Blocked", and
   hand back. Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED: no `gh pr merge`, no `gh pr create`, no STATUS or README edit,
   no ledger rotation, no `consumed_by` edit.
6. Delete nothing you did not create; every existing worktree and every `remedy/job-*` branch stays.
7. A statement in the handback about what a tool produced quotes the tool's own output line.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run before
C3 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f285-r5-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING: at C2 each file below, read with `git show <C2>:<path>`, hashes to the reviewer's
   dry tree:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 322105 | 73201700216618fc230fb16393545150898e71a6cf794ddab3c94536dd4c5b8f |
   | C2 | .agent/plan.md | 885 | 4824677b44edc2a3551e5cd08e6d170bdf4256ef50773849c7ebe7da6ff7176b |
   `open_finding_ids` over the ledger at C2 — the reviewer's dry tree read `[]`; and, serially at
   C2, `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py`,
   exit 0 — the reviewer read `413 passed`.
G3 THE BUNDLE, at A1: the script's real exit code; the two ancestry counts and their equality; the
   collected and deselected counts; the red control's two readings; pytest's exit code and counts;
   the `output_hash`; the `validate_verification_tests` problem list; `is_valid_current_run` and the
   validation errors; and the gate files the evidence directory holds.
G4 THE PACKAGE, at A2: `PACKAGE_STATUS` or the package name's status, which must read
   `READY_FOR_REVIEW` (exit 0 is not the reading); `EVIDENCE_AUTHORITATIVE` where printed; the package
   filename; its SHA-256; the `committed_review_subject` base and head read from
   `.review_zip_manifest.json` INSIDE the package, head equal to C2's full sha and base equal to the
   fork point; `zipfile.is_zipfile` and `testzip()` answering None; and the absolute directory the
   package ended up in, or the literal `NOT ARCHIVED`.
G5 THE TREE, after A2: `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count`
   0; `git status --porcelain` empty; and `git worktree list`.
G6 AFTER C3 AND THE PUSH, in your final reply only: `git status --porcelain` empty, `git log
   --oneline -n 4`, the push's real outcome, and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the evidence job id, the package name with its SHA-256 and archived
directory, the accepted head, the authored-text proofs, the item-status table AGENTS.md requires (one
row per commit, action and gate), the deviations, and the next action. Session section: SESSION 1 of
feature F285, round 5, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1,
the review of round 5, then the closing round — the booking of round 5, the ledger rotation, the next
findings paydown's registration, the STATUS line with the README counters and `SU-032`'s
`consumed_by`, and the pull request. State the open-findings count as the script reads it at C2, and
"Operator questions open: 5".
