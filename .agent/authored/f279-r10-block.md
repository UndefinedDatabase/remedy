STEP F279 R10 — the closure sequence's evidence half: the bundle and the package

GOAL
Book round 9's PASS and the two flaky suite nodes as recurrences of R-0950 and R-1028, build this
feature's evidence bundle against the fork point, and build the fresh review package — recording
its name, its SHA-256 and the directory it ends up in. Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors every payload, the evidence script
included; you run it and never edit it. No commit of this round may touch `docs/roadmap/STATUS.md`,
`README.md`, `scripts/self_use_queue.json` or any file under `apps/`, `packages/` or `tests/`.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r10-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r10-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1 (`review_r9.py`, `dry_collect.py`, `sim.py`), which is
      read-only to you.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file. Capture real exit codes
as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. The `remedy` CLI is denied: run `python3 -m
apps.cli.main ...`. Nothing under `.data/` is readable to you. NEVER USE `git stash` IN ANY FORM,
and never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f279-configuration-toolchain-truth`, `git log --oneline -1` reads `118b645e`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f279-r10-block.md` against the two readings your delegation message states. Report
   both beside both, and stop if either differs.
4. Record the first line of `git stash list` and `git worktree list`.

PAYLOADS — under `.remedy-wt/f279-r10-payloads/`, printed by the reviewer's simulation
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| create_f279_evidence.py | 133 | 5948 | bac2fe446f8e3017ee98c09663bec053600187965f3cbd5d178c2f83709c70da |
| ledger.md | 6 | 4816 | 787102b238cb87dfba93c90ccbde50666f22364fc42ef00a6543b386ad05de7d |
| plan.md | 29 | 1119 | 04d6e1514f50fae0b28c61acdabaac3b1fe0284cdd960b907e7db10076deb4fa |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 9's
`Gate:` entry and two `Recurrence:` paragraphs, for R-0950 and R-1028. The append is strict byte
concatenation onto the file as it stands at `118b645e`. `plan.md` is a REWRITE.
`create_f279_evidence.py` is a TOOL for A1, run from the payload directory and never edited.
Never retype or edit a payload.

BUNDLE — two commits and two actions, then the handback, in this order: C1, C2, A1, A2, C3.

C1 — `.agent/authored/f279-r10-block.md` := this block; `.agent/authored/f279-r10-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F279 R10 C1: copy round 10 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 168. Report the number you measure.

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md.
  Subject: `F279 R10 C2: book round 9's PASS and record the two flaky nodes as recurrences`
  Expected insertions by `git show --numstat`: 6 live_review.md, 10 plan.md.
  C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE. Its full sha is this closure's ACCEPTED HEAD:
  record it, and report it in the handback under that name. Push after C2, before A1.

A1 — THE EVIDENCE JOB (closure-protocol algorithm step 1), an ACTION, committing nothing. From the
  repository root at C2, run `bash -c 'python3 .remedy-wt/f279-r10-payloads/create_f279_evidence.py
  > .remedy-wt/f279-r10-scratch/evidence.log 2>&1; echo "REAL_EXIT=$?"'` and report the log's
  lines up to the summary. The script writes the bundle to `.remedy-wt/f279-r10-evidence/`, which
  is gitignored and therefore outside the review subject; it uses base
  `c9bc5c2057b57db8e0a6f4505c91374ac364a5f8`, the FORK POINT, job id `f279r10e1001`, step range
  `T001-T004`, feature `f279` and run id `vr-1041`. It stops with exit 1 when the two ancestry
  counts differ, when the collected count differs from the node ids it read, when a real node id
  is unsafe, or when a validation fails. The reviewer's simulation, over a tree carrying C2 without
  C1, read ancestry and plain counts equal at 51, 148 node ids collected, none unsafe, the planted
  id answering `a local absolute path`, pytest exit 0 with 148 passed and nothing skipped, an
  EMPTY `validate_verification_tests` problem list, and `is_valid_current_run` True with no
  validation error. Yours reads one more commit in each count, and one more node id and one more
  pass, because C1's block copy joins the parametrized block test of `test_block_lint.py`.

A2 — THE REVIEW PACKAGE (algorithm step 2), an ACTION, committing nothing. The tree must be clean
  and the branch pushed first. Build with
  `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f279-r10-evidence`. A failing
  package build is a closure BLOCKER: report the raw error and hand back rather than working
  around it.

C3 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, carrying
  the evidence job id, the package name, its SHA-256, its archived directory, the accepted HEAD,
  and every gate reading below.
  Subject: `F279 R10 C3: rewrite handoff for round 10 with the evidence and package readings`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f279-r10-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. Report the set you measure
   with `git diff --name-only 118b645e` after C3. No evidence directory is ever committed: a
   committed one lands inside the review subject and packages BLOCKED_EVIDENCE.
4. If the package does not read `READY_FOR_REVIEW`, STOP after recording the raw output: commit
   and push what is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
   Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no README edit, no `consumed_by` edit, no ledger rotation.
6. Delete nothing you did not create: every `.remedy-wt/job-*` worktree and every `remedy/job-*`
   branch stays exactly as it is.
7. A statement in the handback about what a tool produced quotes the tool's own output line.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C3's handback text is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f279-r10-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f279-r10-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 400675 | 314a0f0eba4b9710ad1526b2febad39736d1a0136561d7715e918c70ec7167d1 |
 | .agent/plan.md | 1119 | 04d6e1514f50fae0b28c61acdabaac3b1fe0284cdd960b907e7db10076deb4fa |
 Also: among the lines C2's diff ADDS, those beginning `Gate: F279 R9 — `, `Recurrence: R-0950 — `
 and `Recurrence: R-1028 — `, each 1; and the open set by distinct id via `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at `118b645e` and at C2, with both set
 differences — the reviewer's simulation read the same size at both and both differences empty.

G3 THE BUNDLE — at A1: the script's real exit code; the two ancestry counts and their equality;
 the collected count; the red control's two readings; pytest's exit code and counts; the
 `output_hash`; the `validate_verification_tests` problem list; `is_valid_current_run` and the
 validation errors; the evidence job id; and the files `.remedy-wt/f279-r10-evidence/` holds whose
 names end `_gate.json`, `_integrity.json` or `final_verifier_report.json`, which must include
 `final_verifier_report`, `fresh_evidence_gate`, `artifact_contract_gate`,
 `change_provenance_gate`, `manifest_integrity`, `postmortem_integrity`, `commit_execution_gate`
 and `runtime_integration_gate`.

G4 THE PACKAGE — at A2: `PACKAGE_STATUS`, which must read `READY_FOR_REVIEW` (exit 0 is NOT the
 reading); `EVIDENCE_AUTHORITATIVE`; the package filename; its SHA-256; the
 `committed_review_subject` base and head read from the manifest INSIDE the package, with head
 equal to C2's full sha and base equal to the fork point; the zip's own import check
 (`zipfile.is_zipfile` and `testzip()` answering None); and the absolute directory the package
 ended up in, or the literal `NOT ARCHIVED` if it stayed where it was built.

G5 THE TREE — after A2: `python3 -m apps.cli.main integrity check --json`, all five checks `pass`
 at `fail_count` 0; `git status --porcelain` empty with no relevant untracked file; and `git
 worktree list`.

G6 TREE AND PUSH — after C3: `git status --porcelain` empty; `git log --oneline -n 4`, showing C3,
 C2, C1 and `118b645e`; `git stash list`'s first line unchanged from its reading before C1; the
 push's real outcome; `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 EMPTY. These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit, action and gate: state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the evidence job id, the package name with its SHA-256 and
archived directory, the accepted HEAD, the deviations, and the next action. Your Session section
reads SESSION 2 of feature F279, round 10, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
10, then the closing round: the ledger rotation, the STATUS line with the README counters and the
self-use item's `consumed_by` in the same commit, and the pull request. State the open findings
after this round as the same set as at `118b645e`, and the operator-questions count, 0.
