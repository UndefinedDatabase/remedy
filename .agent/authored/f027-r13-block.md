STEP F027 R13 — THE CLOSURE SEQUENCE'S EVIDENCE ROUND: BOOK ROUND 12, RESOLVE R-1072, BRING THE BUILT STATE CURRENT, BUILD THE BUNDLE AND THE PACKAGE

GOAL
Book round 12's PASS, whose one full suite is green on the repaired tree, resolve R-1072, bring the
Built State's findings current, then build this feature's evidence bundle against the fork point and
the fresh review package, recording the evidence job id, the package name, its SHA-256, the directory
it ends up in and the accepted head. Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue
a verdict and never merge. The reviewer authors every payload, the evidence script included; you run
it and never edit it. Read first: `docs/roadmap/STATUS_closure_protocol.md`'s algorithm steps 1 and 2
with their pitfalls, and `.agent/authored/f026-r7-block.md`, which this round follows.

THE DIRECTORIES
  `.remedy-wt/f027-r13-payloads/` and `.remedy-wt/f027-r13/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f027-r13-drafts/`, `.remedy-wt/f027-r13-evdry/`, `.remedy-wt/f027-r13-zipdry/`,
  `.remedy-wt/f027-r8-dry/`, `.remedy-wt/f027-review/` and every older `f027-*` path: the reviewer's.
  `.remedy-wt/f027-r13-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, and one-liners chained with `;` or
`&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C
<path>`; never `cd` into a worktree. Never run npm or npx, never `git stash`, never delete a branch,
never check out another commit in the primary checkout.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f027-task-veto`, `git log --oneline -1` `07c78cd8`.
3. Measure this block's line count and sha256 (`.remedy-wt/f027-r13/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f027-r13-payloads/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| create_f027_evidence.py | 183 | 9487 | 96a71f7b0b94864045d7deb11e3b5acf5f7cfdb42726d13aca4c534ad13e7f6a |
| plan.md | 27 | 913 | 75390184e640f2e6b7c392a937d88698a6f4328045291916a4d8d04859e39a87 |
| records.diff | 29 | 6392 | b55002de18ac67b9af52b9d4aebc939b214d6a0a3bb31ef378841e1c37b03d75 |
`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `07c78cd8`)
appends round 12's gate entry and R-1072's `Done:` paragraph to `.agent/live_review.md`, and one
paragraph after the Built State's findings in `docs/roadmap/features/T5_F027.md`.
`create_f027_evidence.py` is a TOOL for A1, run from the payload directory and never edited.

BUNDLE — C1, C2, A1, A2, C3, in this order.
C1 COPIES: `.agent/authored/f027-r13-block.md` := this block and each payload as
   `.agent/authored/f027-r13-<name>`, by `shutil.copyfile`. Subject `F027 R13 C1: copy round 13 block
   and payloads`. Its insertions are this block's line count plus 239.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject `F027 R13 C2: book
   round 12, resolve R-1072, bring the Built State current`. Expected by `git show --numstat`:
   4/0 .agent/live_review.md, 7/10 .agent/plan.md, 9/0 docs/roadmap/features/T5_F027.md. C2 IS THE
   LAST CONTENT COMMIT BEFORE THE PACKAGE: its full sha is this closure's ACCEPTED HEAD; record it
   under that name. Push after C2, before A1.
A1 THE EVIDENCE JOB, an action committing nothing. From the repository root at C2:
   `bash -c 'python3 .remedy-wt/f027-r13-payloads/create_f027_evidence.py >
   .remedy-wt/f027-r13-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`, and report the log's lines up to
   the summary. It writes the bundle to `.remedy-wt/f027-r13-evidence/`, gitignored, with base
   `557cbbcc5f5f0a46bf6d9c90b971b2723657d651`, the FORK POINT, job id `f027r13e1001`, step range
   `T001-T003`, feature `f027` and run id `vr-1072`. It exits 1 when the two ancestry counts differ,
   when the collected count differs from the node ids it read, when a real node id is unsafe, or when
   a validation fails. The reviewer's dry run from the primary checkout at `07c78cd8`, into a scratch
   directory, read ancestry and plain counts equal at 82, 1661 node ids collected with 10 deselected,
   none unsafe, the planted id answering `a local absolute path`, pytest exit 0 with 1661 passed and
   0 skipped, an EMPTY `validate_verification_tests` problem list, and `is_valid_current_run` True
   with no validation error. At C2 both ancestry counts read two more.
A2 THE REVIEW PACKAGE, an action committing nothing, from a clean and pushed tree:
   `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f027-r13-evidence`, WITHOUT setting
   `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The reviewer's dry run of the
   same command at `07c78cd8`, over its scratch evidence and into a scratch directory, read
   `PACKAGE_STATUS=READY_FOR_REVIEW` and `EVIDENCE_AUTHORITATIVE=true`. A failing package build is a
   closure BLOCKER: report the raw error and hand back.
C3 THE HANDBACK: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, carrying the
   evidence job id, the package name, its SHA-256, its archived directory, the accepted head and every
   gate reading. Subject `F027 R13 C3: rewrite handoff for round 13 with the evidence and package
   readings`. Then `git push origin feature/f027-task-veto`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`, its exit code reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f027-r13-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T5_F027.md` and
   `.agent/handoff.md`. No evidence directory is committed.
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
   `.agent/authored/f027-r13-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING: at C2 each file below, read with `git show <C2>:<path>`, hashes to the reviewer's
   simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 340263 | 1afe8ce86206fab7af699c2915ba34983e0ed412bd66697a9aae0abb25898b86 |
   | C2 | .agent/plan.md | 913 | 75390184e640f2e6b7c392a937d88698a6f4328045291916a4d8d04859e39a87 |
   | C2 | docs/roadmap/features/T5_F027.md | 12413 | 40374dfb9f9ff323bd10096adcd011c18a053eefd63d2533ee46c3ec7d0421db |
   `open_finding_ids` over the ledger at C2 — the reviewer's simulation read `[]`; and, serially at
   C2, `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py`, exit 0.
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
row per commit, action and gate), the deviations, and the next action. Session section: SESSION 2 of
feature F027, round 13, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1,
the review of round 13, then the closing round — the booking of round 13, the ledger rotation, the
STATUS line with the README counters in the same commit, and the pull request. State the
open-findings count as the script reads it at C2, and "Operator questions open: 5".
