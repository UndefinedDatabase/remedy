STEP F265 R6 — THE CLOSURE SEQUENCE'S EVIDENCE HALF: BOOK ROUND 5, BUILD THE BUNDLE AND THE PACKAGE

GOAL
Book round 5's PASS, whose one full suite is green, then build this feature's evidence bundle
against the fork point and the fresh review package, recording the evidence job id, the package
name, its SHA-256, the directory it ends up in and the accepted HEAD. Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors every payload, the evidence script
included; you run it and never edit it. No commit of this round may touch `docs/roadmap/STATUS.md`,
`README.md`, `scripts/self_use_queue.json` or any file under `apps/`, `packages/`, `tests/` or
`docs/`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f265-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f265-r6-scratch/`   READ-ONLY. The reviewer's simulation tools and logs.
  `.remedy-wt/f265-r6-worker/`    YOURS for logs, captures and scripts; create it if absent.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>` rather than
`cd`. Put multi-step code in a scratch Python file under your directory. The `remedy` CLI may be
denied: run `python3 -m apps.cli.main ...`. Never use `git stash` in any form, and never check out
another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f265-teacher-learning-ui`, and `git log --oneline -1` must read `0fd206e0`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f265-r6-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f265-r6-payloads/`, printed by the reviewer's simulation
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 10 | 6813 | cad9c25993576496238c951a7d5eb60ac52a4743a6262f50a58218bbafed62a4 |
| plan.md | 28 | 936 | 1944ada52bff7d912ec1d896f8965d46ecadc9127092f06339857f4139e7f6c5 |
| create_f265_evidence.py | 151 | 6845 | 9687330a473a24298be67dd322f1d4c3f6894e18d362c6d75612f91c2c975cb6 |

`ledger.diff` appends one paragraph to `.agent/live_review.md`, round 5's `Gate:` entry, and goes
on with `git apply --check` then `git apply`. `plan.md` is a REWRITE of `.agent/plan.md`.
`create_f265_evidence.py` is a TOOL for A1, run from the payload directory and never edited.
Never retype or edit a payload; copy with `shutil.copyfile`.

BUNDLE — two commits and two actions, then the handback, in this order: C1, C2, A1, A2, C3.

C1 — `.agent/authored/f265-r6-block.md` := this block; `.agent/authored/f265-r6-<name>` for each
  payload, keeping its file name.
  Subject: `F265 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 189. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F265 R6 C2: book round 5's PASS, the one full suite green`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 7/10 plan.md.
  C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE. Its full sha is this closure's ACCEPTED HEAD:
  record it, and report it in the handback under that name. Push after C2, before A1.

A1 — THE EVIDENCE JOB (closure-protocol algorithm step 1), an ACTION, committing nothing. From the
  repository root at C2, run `bash -c 'python3 .remedy-wt/f265-r6-payloads/create_f265_evidence.py
  > .remedy-wt/f265-r6-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'` and report the log's
  lines up to the summary. The script writes the bundle to `.remedy-wt/f265-r6-evidence/`, which
  is gitignored and therefore outside the review subject; it uses base
  `0236e3c3092f02df2a0230af97619f740531f6ba`, the FORK POINT, job id `f265r6e1001`, step range
  `T001-T003`, feature `f265` and run id `vr-1046`. It stops with exit 1 when the two ancestry
  counts differ, when the collected count differs from the node ids it read, when a real node id
  is unsafe, or when a validation fails. The reviewer's simulation, over a tree carrying the
  simulated C1 and C2 and without `apps/ui/node_modules`, read ancestry and plain counts equal at
  35, 751 node ids collected, none unsafe, the planted id answering `a local absolute path`, pytest
  exit 0 with 747 passed and 4 skipped — the eslint, typescript and vitest nodes, which skip
  without the UI toolchain — an EMPTY `validate_verification_tests` problem list, and
  `is_valid_current_run` True with no validation error. Your primary checkout carries the
  toolchain, so those four run there; report the counts you read.

A2 — THE REVIEW PACKAGE (algorithm step 2), an ACTION, committing nothing. The tree must be clean
  and the branch pushed first. Build with
  `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f265-r6-evidence`, without setting
  `REMEDY_REVIEW_DIR`, so the package goes to the operator's archive. The reviewer's dry run of the
  same command in its simulation, into a scratch directory, read `PACKAGE_STATUS=READY_FOR_REVIEW`
  and `EVIDENCE_AUTHORITATIVE=true`, and `.review_zip_manifest.json` inside the package named the
  fork point as base and the simulated C2 as head. A failing package build is a closure BLOCKER:
  report the raw error and hand back rather than working around it.

C3 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, carrying
  the evidence job id, the package name, its SHA-256, its archived directory, the accepted HEAD,
  and every gate reading below.
  Subject: `F265 R6 C3: rewrite handoff for round 6 with the evidence and package readings`
  Then `git push origin feature/f265-teacher-learning-ui`. Do NOT create a pull request.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f265-r6-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. Report the set you measure
   with `git diff --name-only 0fd206e0 HEAD` after C3. No evidence directory is ever committed: a
   committed one lands inside the review subject and packages BLOCKED_EVIDENCE.
4. If the package does not read `READY_FOR_REVIEW`, STOP after recording the raw output: commit
   and push what is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
   Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no README edit, no ledger rotation.
6. Delete nothing you did not create: every `.remedy-wt/job-*` worktree, every `remedy/job-*`
   branch and the reviewer's worktrees whose names begin `.remedy-wt/f265-` stay exactly as they
   are.
7. A statement in the handback about what a tool produced quotes the tool's own output line.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run before C3 is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f265-r6-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f265-r6-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 316060 | 4d62caeb2774c2d9abc65ce62aad5706dfb1a8595242b1f38316464a8f80c126 |
 | .agent/plan.md | 936 | 1944ada52bff7d912ec1d896f8965d46ecadc9127092f06339857f4139e7f6c5 |
 Also: among the lines C2's diff ADDS, those beginning `Gate: F265 R5 — `, 1; and the open set
 by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT
 at `0fd206e0` and at C2, with both set differences — the reviewer's simulation read 4 at both,
 R-0499, R-0950, R-1008 and R-1046, and both differences empty.

G3 THE BUNDLE — at A1: the script's real exit code; the two ancestry counts and their equality;
 the collected count; the red control's two readings; pytest's exit code and counts; the
 `output_hash`; the `validate_verification_tests` problem list; `is_valid_current_run` and the
 validation errors; the evidence job id; and the files `.remedy-wt/f265-r6-evidence/` holds
 whose names end `_gate.json`, `_integrity.json` or `final_verifier_report.json`.

G4 THE PACKAGE — at A2: `PACKAGE_STATUS`, which must read `READY_FOR_REVIEW` (exit 0 is NOT the
 reading); `EVIDENCE_AUTHORITATIVE`; the package filename; its SHA-256; the
 `committed_review_subject` base and head read from `.review_zip_manifest.json` INSIDE the
 package, with head equal to C2's full sha and base equal to the fork point; the zip's own check
 (`zipfile.is_zipfile` and `testzip()` answering None); and the absolute directory the package
 ended up in, or the literal `NOT ARCHIVED` if it stayed where it was built.

G5 THE TREE — after A2: `python3 -m apps.cli.main integrity check --json`, all six checks `pass`
 at `fail_count` 0; `git status --porcelain` empty with no relevant untracked file; and `git
 worktree list`.

G6 TREE AND PUSH — after C3: `git status --porcelain` empty; `git log --oneline -n 4`, showing C3,
 C2, C1 and `0fd206e0`; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the handback —
 the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit, action and gate: state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the evidence job id, the package name with its SHA-256 and
archived directory, the accepted HEAD, the deviations, and the next action. Your Session section
reads SESSION 1 of feature F265, round 6, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
6, then the closing round: the booking of round 6, the ledger rotation, the STATUS line with the
README counters in the same commit, and the pull request. State the open-findings count, 4, and
the operator-questions count, 1.
