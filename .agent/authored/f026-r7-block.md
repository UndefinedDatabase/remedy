STEP F026 R7 — THE CLOSURE SEQUENCE'S EVIDENCE ROUND: BOOK ROUND 6, RESOLVE R-1062 AND R-1063, REGISTER R-1064, BUILD THE BUNDLE AND THE PACKAGE

GOAL
Book round 6's PASS, whose one full suite is green on the repaired tree, resolve R-1062 and R-1063,
register R-1064 for F285 with its Acceptance line in F285's file, bring the Built State's findings
current, then build this feature's evidence bundle against the fork point and the fresh review
package, recording the evidence job id, the package name, its SHA-256, the directory it ends up in
and the accepted head. Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue
a verdict and never merge. The reviewer authors every payload, the evidence script included; you run
it and never edit it. Read first: `docs/roadmap/STATUS_closure_protocol.md`'s algorithm steps 1 and 2
with their pitfalls, and `.agent/authored/f025-r10-block.md`, which this round follows.

THE DIRECTORIES
  `.remedy-wt/f026-r7-payloads/` and `.remedy-wt/f026-r7/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f026-r7-sim/`, `.remedy-wt/f026-r7-drafts/`, `.remedy-wt/f026-r7-evdry/`,
  `.remedy-wt/f026-r7-zipdry/`   The reviewer's; do not touch them.
  `.remedy-wt/f026-r7-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

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
   `git branch --show-current` `feature/f026-task-edit-runtime`, `git log --oneline -1` `436ff8a0`.
3. Measure this block's line count and sha256 (`.remedy-wt/f026-r7/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f026-r7-payloads/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| create_f026_evidence.py | 174 | 9018 | bdc953617bbd8e18053ecbd5156025fb9a7c3a342a4f70475f3fc0e49c7a255e |
| plan.md | 29 | 1004 | 08df88f775293582011de55caf8d9d399b5c84aa5c4f13cee153aa819f94a4ca |
| records.diff | 46 | 10021 | 4c578b00a139df283acf34fa480fb08934df299ac481d797adc366454477f9a3 |
`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `436ff8a0`)
appends round 6's gate entry, the `Done:` paragraphs of R-1062 and R-1063 and R-1064's registration
to `.agent/live_review.md`; appends one paragraph after the Built State's findings in
`docs/roadmap/features/T5_F026.md`; and appends R-1064's Acceptance line after R-1058's in
`docs/roadmap/features/T2_F285.md` (both containment tests: TO contains FROM: true — APPENDS).
`create_f026_evidence.py` is a TOOL for A1, run from the payload directory and never edited.

BUNDLE — C1, C2, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f026-r7-block.md` := this block and each payload as
   `.agent/authored/f026-r7-<name>`, by `shutil.copyfile`. Subject `F026 R7 C1: copy round 7 block and
   payloads`. Its insertions are this block's line count plus 249.
C2 RECORDS, one commit, the finding persisted FIRST: `git apply` records.diff, then `.agent/plan.md`
   := plan.md. Subject `F026 R7 C2: book round 6, resolve R-1062 and R-1063, register R-1064 for F285`.
   Expected by `git show --numstat`: 8/0 .agent/live_review.md, 9/11 .agent/plan.md, 3/0 docs/roadmap/features/T2_F285.md, 8/0 docs/roadmap/features/T5_F026.md. C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE:
   its full sha is this closure's ACCEPTED HEAD; record it under that name. Push after C2, before A1.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
   `bash -c 'python3 .remedy-wt/f026-r7-payloads/create_f026_evidence.py >
   .remedy-wt/f026-r7-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`, and report the log's lines up to
   the summary. It writes the bundle to `.remedy-wt/f026-r7-evidence/`, gitignored, with base
   `905558493f1ff6570493a8b212a741ab59242a4a`, the FORK POINT, job id `f026r7e1001`, step range
   `T001-T003`, feature `f026` and run id `vr-1063`. It exits 1 when the two ancestry counts differ,
   when the collected count differs from the node ids it read, when a real node id is unsafe, or when
   a validation fails. The reviewer's dry run from the primary checkout at `436ff8a0`, into a scratch
   directory, read ancestry and plain counts equal at 46, 1543 node ids collected with 5 deselected,
   none unsafe, the planted id answering `a local absolute path`, pytest exit 0 with 1543 passed and
   0 skipped, an EMPTY `validate_verification_tests` problem list, and `is_valid_current_run` True
   with no validation error. At C2 both ancestry counts read two more.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
   `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f026-r7-evidence`, WITHOUT setting
   `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The reviewer's dry run of the
   same command at `436ff8a0`, over its scratch evidence and into a scratch directory, read
   `PACKAGE_STATUS=READY_FOR_REVIEW` and `EVIDENCE_AUTHORITATIVE=true`. A failing package build is a
   closure BLOCKER: report the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying the
   evidence job id, the package name, its SHA-256, its archived directory, the accepted head and every
   gate reading. Subject `F026 R7 C3: rewrite handoff for round 7 with the evidence and package
   readings`. Then `git push origin feature/f026-task-edit-runtime`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f026-r7-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T5_F026.md`,
   `docs/roadmap/features/T2_F285.md` and `.agent/handoff.md`. No evidence directory is committed.
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
   `.agent/authored/f026-r7-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING: at C2 each file below, read with `git show <C2>:<path>`, hashes to the reviewer's
   simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 344410 | 44dc95efbfdf4b6b4b6da4c0dc48d80bf997c9164f528d4f3ed854002f06e4e5 |
   | C2 | .agent/plan.md | 1004 | 08df88f775293582011de55caf8d9d399b5c84aa5c4f13cee153aa819f94a4ca |
   | C2 | docs/roadmap/features/T5_F026.md | 10951 | d57d3a775006ed6ea8eedaa832442b6ebdec7d43e91a02d4f5918502dcf0a431 |
   | C2 | docs/roadmap/features/T2_F285.md | 3337 | 7624be55be8c172809a578e31ab09ccfe51b3a00488864c10c3c54338a01e45f |
   `open_finding_ids` over the ledger at C2 — the reviewer's simulation read `['R-1008', 'R-1055',
   'R-1057', 'R-1058', 'R-1064']`; and, serially at C2, `python3 -m pytest -q -p no:cacheprovider
   tests/docs/ tests/cli/test_golden_path.py`, exit 0 — the reviewer read `369 passed`.
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
   0; `git status --porcelain` empty; and `git worktree list`.
G6 AFTER C3 AND THE PUSH, in your final reply only: `git status --porcelain` empty, `git log
   --oneline -n 4`, the push's real outcome, and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the evidence job id, the package name with its SHA-256 and archived
directory, the accepted head, the authored-text proofs, the item-status table AGENTS.md requires (one
row per commit, action and gate), the deviations, and the next action. Session section: SESSION 1 of
feature F026, round 7, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1,
the review of round 7, then the closing round — the booking of round 7, the ledger rotation, the
STATUS line with the README counters and the self-use item's `consumed_by` in the same commit, and
the pull request. State the open-findings count as the script reads it at C2, and "Operator questions
open: <the count of `### Q` headings at C2>".
