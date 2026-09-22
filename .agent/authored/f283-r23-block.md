STEP F283 R23 — the closure sequence's evidence half: the bundle, the package, and the one finding the self-use run owes

GOAL
Book round 22's PASS, register R-1035 from the self-use run's own defect reader, build this
feature's evidence bundle against the fork point, and build the fresh review package — recording
its name, its SHA-256 and the directory it ends up in. Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors the RECORD payloads; the evidence script
is yours, adapted from the template named below. No commit of this round may touch
`docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` or any file under `apps/`,
`packages/` or `tests/`.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r23-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r23-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1, which is read-only to you.
  `.remedy-wt/f273-r24/create_f273_evidence.py` is the TEMPLATE for A1, the newest one that
      packaged READY on its first build. Adapt its evidence directory, base commit, job id, job
      title, step range, feature id and `TEST_FILES`; everything else in it — node ids from
      `--collect-only`, the collected-count assert, `len(node_ids) == selected`, the sorted
      `test_files`, the `output_hash` over the real pytest output — is load-bearing and stays.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`, a
`grep` pattern holding `$`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`; put multi-step code in a scratch file. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. The `remedy` CLI itself is denied session-wide: run
`python3 -m apps.cli.main ...`, or the module the gate names. NEVER USE `git stash` IN ANY FORM,
and never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `15145f71`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r23-block.md` against the two readings your delegation message states. Report
   both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r23-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 6089 | 2802ddd898dece8bc5e2fbd017956a46d5100ffe442188aaac28e1bfa403429c |
| plan.md | 34 | 1507 | e4677998024b8c3550780c75e0e068b786860220cbe1505cacd000c99a801242 |

`ledger.md` is an APPEND beginning with the single newline that separates records: the round 22
`Gate:` entry and R-1035's registration. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — two commits and two actions, in this order: C1, C2, A1, A2, C3.

C1 — `.agent/authored/f283-r23-block.md` := this block; `.agent/authored/f283-r23-<name>` for each
  payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R23 C1: copy round 23 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md
  Subject: `F283 R23 C2: book round 22's PASS and register R-1035`
  C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE. Its sha is this closure's ACCEPTED HEAD:
  record it, and report it in the handback under that name.

A1 — THE EVIDENCE JOB (closure-protocol algorithm step 1), an ACTION, committing nothing. The
  evidence directory is `.remedy-wt/f283-r23-evidence/`, which is gitignored and therefore outside
  the review subject. Adapt the template into
  `.remedy-wt/f283-r23-scratch/create_f283_evidence.py` with:
    * `base_commit` = `d0d40e89b6aa9afcebd639df7a7c16a260059537`, the FORK POINT. Before building,
      report `git rev-list --count --ancestry-path <base>..<head>` and `git rev-list --count
      <base>..<head>`; they MUST be equal, or the base is wrong and you stop (pitfall (e) in the
      closure protocol). The reviewer read 159 and 159 at `15145f71`.
    * `head_commit` = C2's sha, the accepted HEAD.
    * `job_id` = `f283r23e1001`, `job_title` = `F283 round 23 evidence job`, `step_range` =
      `T001-T002`, `review_feature_id` = `f283`.
    * `TEST_FILES`, sorted, exactly these five: `tests/cli/test_exit_codes.py`,
      `tests/cli/test_json_contract.py`, `tests/cli/test_json_envelope.py`,
      `tests/cli/test_stats_report.py`, `tests/orchestration/test_worktree_resume_cli.py`.
    * one verification run whose `run_id` matches `^vr-\d{4,}$`, whose `node_ids` come from
      `--collect-only` with `len(node_ids) == selected`, and whose `output_hash` is the sha256 of
      the real pytest output.
  Then, BEFORE paying for a package build, run `scripts/build_review_manifest.py`'s
  `validate_verification_tests` over the produced `verification_tests.json` and require an EMPTY
  problem list (pitfall (f)), and run `validate_evidence_candidate` over the directory. Report the
  bundle's gate set, both validations, and the evidence job id.
  RED CONTROL, in memory and never on the real bundle: take the node-id list the run produced, add
  ONE id carrying an absolute path, and show that `build_review_manifest`'s own unsafe-text scan
  REJECTS that list while it accepts the real one. Report both readings. A check that cannot fail
  proves nothing when it passes.

A2 — THE REVIEW PACKAGE (algorithm step 2), an ACTION, committing nothing. The tree must be clean
  and the branch pushed first. Build with
  `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f283-r23-evidence`. Report the
  package filename, its SHA-256, its `PACKAGE_STATUS` (which must read `READY_FOR_REVIEW`; exit 0
  is NOT the reading), `EVIDENCE_AUTHORITATIVE`, and the `committed_review_subject`'s base and
  head, whose head must equal C2's sha. Then report the ABSOLUTE DIRECTORY the package now lives
  in, or the literal `NOT ARCHIVED` if it was left where it was built — DECISION amend0827 D1
  makes that a field of the STATUS line the next round writes, and this round is the only actor
  that knows it. A failing package build is a closure BLOCKER: report the raw error and hand back
  rather than working around it.

C3 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, carrying
  the evidence job id, the package name, its SHA-256, its archived directory, the accepted HEAD,
  and every gate reading below.
  Subject: `F283 R23 C3: rewrite handoff for round 23 with the evidence and package readings`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f283-r23-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. Report the set you measure.
   Nothing else — no `packages/`, no `apps/`, no `tests/`, no `docs/`, no `scripts/`, no
   `README.md`, and no evidence directory: the evidence dir is NEVER committed, because a
   committed one lands inside the review subject and packages BLOCKED_EVIDENCE.
4. If the package does not read `READY_FOR_REVIEW`, STOP after recording the raw output: commit
   and push what is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
   Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no README edit, no `consumed_by` edit, no ledger rotation.
6. Delete nothing you did not create: the `remedy/job-*` branches and the worktree round 22's
   self-use run left behind stay exactly as they are. Report `git worktree list`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C3's handback text is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f283-r23-*` blob, read with `git show <C1>:<path>`, compared
 byte-for-byte with its source (the block copy against `.remedy-wt/f283-r23-block.md`). One
 reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, `.agent/live_review.md` read at `15145f71` (559905) plus
     ledger.md, the reviewer composed 565994.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R22 — ` 1 and `^- R-1035 — ` 1. Open set
     by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at `15145f71` and
     at C2: the reviewer measured 25 and 26, ADDED `R-1035`, REMOVED none.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE BUNDLE — at A1: the two ancestry counts and their equality; the evidence job id; the gate
 set the bundle wrote, which must hold all eight closed-schema gates; `validate_verification_tests`
 with an EMPTY problem list; `validate_evidence_candidate`'s `is_valid_current_run` and its error
 list; the verification run's `run_id`, `selected`, `len(node_ids)`, sorted `test_files` and
 `output_hash`; and the unsafe-text red control's two readings, the real list accepted and the
 planted one rejected.

G4 THE PACKAGE — at A2: `PACKAGE_STATUS`, `EVIDENCE_AUTHORITATIVE`, the package filename, its
 SHA-256, the `committed_review_subject` base and head with head equal to C2's sha, the zip's own
 import check, and the absolute directory the package ended up in.

G5 THE TREE — `python3 -c` calling `run_integrity_checks` from
 `packages.orchestration.integrity_gate` (it answers an object with `.passed`, `.fail_count` and
 `.checks` — attributes, never a dict): `passed` true and `fail_count` 0. Then `git status
 --porcelain`, empty, with no relevant untracked file, and `git worktree list`.

G6 TREE AND PUSH — after C3: `git status --porcelain` empty; `git log --oneline -n 8`; `git
 stash list`'s first line unchanged from its reading before C1; the push's real outcome; `gh pr
 list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final
 reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit changed-files
table with the insertions git MEASURED, every gate's real output and exit code, the evidence job
id, the package name with its SHA-256 and archived directory, the accepted HEAD, the item-status
table with one row per item and gate, the deviations, and the next action. Your Session section
reads SESSION 5 of feature F283, round 23, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
23, then the closure sequence's last round as `.agent/plan.md` lists it. State the open-findings
count, 26 after this round, and the operator-questions count, 0.
