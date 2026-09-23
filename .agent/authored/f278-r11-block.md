STEP F278 R11 — the closure sequence's evidence half: the bundle and the package

GOAL
Book round 10's PASS and resolve R-1039, build this feature's evidence bundle against the fork
point, and build the fresh review package — recording its name, its SHA-256 and the directory it
ends up in. Nothing closes in this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors the RECORD payloads; the evidence script
is yours, adapted from the template named below. No commit of this round may touch
`docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` or any file under `apps/`,
`packages/` or `tests/`.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r11-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r11-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1 (`build_payloads.py`, `dry_collect.py`), which is read-only to
      you.
  `.remedy-wt/f283-r23-scratch/create_f283_evidence.py` is the TEMPLATE for A1: F283's evidence
      script, which packaged READY on its first build. Adapt its evidence directory, base commit,
      job id, job title, step range, feature id, `run_id` and `TEST_FILES`; everything else in it —
      node ids from `--collect-only`, the collected-count assert, `len(node_ids) == selected`, the
      sorted `test_files`, the `output_hash` over the real pytest output — is load-bearing and
      stays.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file, and never put a `#`
after a newline inside a `python3 -c` argument. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. The `remedy` CLI itself is denied session-wide: run
`python3 -m apps.cli.main ...`, or the module the gate names. NEVER USE `git stash` IN ANY FORM,
and never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f278-durable-writes-loud-failures`, `git log --oneline -1` reads `4d9ae208`.
3. Verify this block's own bytes (R-0954): line count and sha256 of `.remedy-wt/f278-r11-block.md`
   against the two readings your delegation message states. Report both beside both, and stop if
   either differs.
4. Record the first line of `git stash list` and `git worktree list`.

PAYLOADS — under `.remedy-wt/f278-r11-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 3665 | 7eb163090aaa06d2fbe5e8dd6d7d1c85ff33b14911546d3c505d656268290531 |
| plan.md | 27 | 1028 | a8830135c0725acb70cff0fac8dc9cea5090530ee951a411f51f0f0b52049ca4 |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 10's
`Gate:` entry and R-1039's `Done:` paragraph. `plan.md` is a REWRITE. Never retype or edit a
payload.

BUNDLE — two commits and two actions, then the handback, in this order: C1, C2, A1, A2, C3.

C1 — `.agent/authored/f278-r11-block.md` := this block; `.agent/authored/f278-r11-<name>` for each
  payload. Byte for byte, with `shutil.copyfile`.
  Subject: `F278 R11 C1: copy round 11 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md. The append is strict byte
  concatenation onto the file as it stands at `4d9ae208`.
  Subject: `F278 R11 C2: book round 10's PASS and resolve R-1039`
  C2 IS THE LAST CONTENT COMMIT BEFORE THE PACKAGE. Its full sha is this closure's ACCEPTED HEAD:
  record it, and report it in the handback under that name. Push after C2, before A2.

A1 — THE EVIDENCE JOB (closure-protocol algorithm step 1), an ACTION, committing nothing. The
  evidence directory is `.remedy-wt/f278-r11-evidence/`, which is gitignored and therefore outside
  the review subject. Adapt the template into
  `.remedy-wt/f278-r11-scratch/create_f278_evidence.py` with:
    * `base_commit` = `9817a927b5fd41d7867195a51e8a7113ce26ae98`, the FORK POINT. Before building,
      report `git rev-list --count --ancestry-path <base>..<C2>` and `git rev-list --count
      <base>..<C2>`; they MUST be equal, or the base is wrong and you stop (pitfall (e) in the
      closure protocol). The reviewer read 72 and 72 at `4d9ae208`, two commits before C2.
    * `head_commit` = C2's full sha, the accepted HEAD, read with `git rev-parse` after C2.
    * `job_id` = `f278r11e1001`, `job_title` = `F278 round 11 evidence job`, `step_range` =
      `T001-T003`, `review_feature_id` = `f278`, and the run's `run_id` = `vr-1039`.
    * `TEST_FILES`, sorted, exactly these six:
      `tests/orchestration/test_do_sequence.py`, `tests/orchestration/test_durable_write_guard.py`,
      `tests/orchestration/test_f018_authority_integration.py`,
      `tests/orchestration/test_review_subject_strict_schema.py`,
      `tests/orchestration/test_secure_fs_durable_write.py`, `tests/test_ble001_ratchet.py`.
      `tests/orchestration/test_stream_evidence.py` is deliberately NOT among them: the
      reviewer's dry run found six of its node ids carrying secret-shaped parameters by design,
      which the package's own metadata scan rejects (pitfall (d)); the full suite covers it.
      The reviewer's dry run collected 168 node ids over these six at `4d9ae208`, none unsafe.
    * one verification run whose `run_id` matches `^vr-\d{4,}$`, whose `node_ids` come from
      `--collect-only` with `len(node_ids) == selected`, and whose `output_hash` is the sha256 of
      the real pytest output.
  Then, BEFORE paying for a package build, run `scripts/build_review_manifest.py`'s
  `validate_verification_tests` over the produced `verification_tests.json` and require an EMPTY
  problem list (pitfall (f)), and run `validate_evidence_candidate` over the directory. Report the
  bundle's gate set, both validations, and the evidence job id.
  RED CONTROL, in memory and never on the real bundle: run `build_review_manifest._unsafe_text`
  over every node id the run produced — every answer must be None — and then over the one planted
  id `tests/x.py::test_a[/home/someone/secret]`, whose answer must be `a local absolute path`.
  Report both readings. A check that cannot fail proves nothing when it passes.

A2 — THE REVIEW PACKAGE (algorithm step 2), an ACTION, committing nothing. The tree must be clean
  and the branch pushed first. Build with
  `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f278-r11-evidence`. Report the
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
  Subject: `F278 R11 C3: rewrite handoff for round 11 with the evidence and package readings`
  Then `git push origin feature/f278-durable-writes-loud-failures`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f278-r11-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. Report the set you measure.
   Nothing else — no `packages/`, no `apps/`, no `tests/`, no `docs/`, no `scripts/`, no
   `README.md`, and no evidence directory: the evidence dir is NEVER committed, because a
   committed one lands inside the review subject and packages BLOCKED_EVIDENCE.
4. If the package does not read `READY_FOR_REVIEW`, STOP after recording the raw output: commit
   and push what is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
   Never edit an evidence file by hand to make a validator pass.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no README edit, no `consumed_by` edit, no ledger rotation.
6. Delete nothing you did not create: the `remedy/job-*` branches and the worktrees the self-use
   runs left behind stay exactly as they are.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C3's handback text is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f278-r11-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f278-r11-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION onto the `4d9ae208` bytes, the reviewer's dry run composed
     `.agent/live_review.md` at 463142 bytes, sha256
     `b8740a871c74b59fe9b4ce9b1c20a0b2826ef86a54614d815f8495a253ffb5cb`. Report yours beside it.
 (b) Line-anchored on the committed ledger: `^Gate: F278 R10 — ` 1 and `^Done: R-1039 — ` 1. Open
     set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at `4d9ae208`
     and at C2: the reviewer measured 27 and 26, REMOVED `R-1039`, ADDED none.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (under 50).

G3 THE BUNDLE — at A1: the two ancestry counts and their equality; the evidence job id; the gate
 set the bundle wrote, which must hold all eight closed-schema gates; `validate_verification_tests`
 with an EMPTY problem list; `validate_evidence_candidate`'s `is_valid_current_run` and its error
 list; the verification run's `run_id`, `exit_code`, `passed`, `selected`, `len(node_ids)`, sorted
 `test_files` and `output_hash`; and the unsafe-text red control's two readings.

G4 THE PACKAGE — at A2: `PACKAGE_STATUS`, `EVIDENCE_AUTHORITATIVE`, the package filename, its
 SHA-256, the `committed_review_subject` base and head with head equal to C2's sha, the zip's own
 import check (`zipfile.is_zipfile` and `testzip()`), and the absolute directory the package ended
 up in.

G5 THE TREE — `python3 -m apps.cli.main integrity check --json`: `passed` true and `fail_count` 0,
 all five checks `pass`. Then `git status --porcelain`, empty, with no relevant untracked file,
 and `git worktree list`.

G6 TREE AND PUSH — after C3: `git status --porcelain` empty; `git log --oneline -n 5`; `git
 stash list`'s first line unchanged from its reading before C1; the push's real outcome; `gh pr
 list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final
 reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per item and gate: state block, the per-commit changed-files table
with the insertions git MEASURED, every gate's real output and exit code, the evidence job id, the
package name with its SHA-256 and archived directory, the accepted HEAD, the deviations, and the
next action. Your Session section reads SESSION 2 of feature F278, round 11, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
11, then the closure sequence's last round as `.agent/plan.md` lists it. State the open-findings
count, 26 after this round, and the operator-questions count, 0.
