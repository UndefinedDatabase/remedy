STEP R16 — F277 closure: the evidence job and a FRESH review zip

GOAL
The integration gate is green. Build the feature-scoped evidence bundle through the
canonical producer and then a FRESH review zip, and record the package name, its SHA-256
and its archived path. A failing zip is a closure BLOCKER, not a deviation — F281's
closure needed four rounds to get a READY package, so this block names every pitfall
`docs/roadmap/STATUS_closure_protocol.md` records and asks you to derive rather than
transcribe every number the bundle carries.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict.

READ FIRST, BEYOND THE THREE YOUR DELEGATION NAMES
`docs/roadmap/STATUS_closure_protocol.md`, Algorithm steps 1 and 2 and the "Canonical zip
build sequence" and "Evidence dir is not committed" sections. This round IS those two
steps and they carry five named packaging pitfalls that have each blocked a closure.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r16-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r16-scratch/`   YOURS. Every log, exit-code capture, driver script and
      the EVIDENCE DIR itself go here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and NEVER pipe pytest into `tail`. Use
`python3 -c` or `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`);
a `python3 -c` script containing a newline followed by `#` is rejected, so use the
heredoc there.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `b10e9bf1`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r16-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all three under `.remedy-wt/f277-r16-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 5658 | 4666506d04d5788e3edcfef7a793adb8ca2148498226145c6b47fc01bbc5e0ea |
| plan.md | 45 | 2253 | c3a28ba36cd4d552d55f0958b21046e7eb0438c7f846267b3310f91b933c413d |
| slips.md | 1 | 1296 | e2546b3de13ec43f705ffc2ae3945d0e1b99f30e59acc10fb5107e1ca0b7fc8f |

`ledger.md` is an APPEND of ONE PARAGRAPH beginning with a single newline that is the
record separator. `slips.md` is an APPEND of ONE LINE with NO leading newline.
`plan.md` is a REWRITE. There is no diff payload this round and no decisions or questions
payload; `.agent/decisions.md` and `.agent/operator_questions.md` are not touched.

BUNDLE — the commits are C1a, C1b and C2, in this order

C1a — copy this block and all three payloads into `.agent/authored/`
  `.agent/authored/f277-r16-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r16-<name>` per payload, keeping each payload's own file name.
  Subject: `F277 R16 C1a: copy round 16 payloads into .agent/authored/`
  SIZE. The payloads total 48 lines, so this commit's insertions are 48 plus this block's
  own line count, and the 500 cap binds at 452 block lines. Round 12 spent this FEATURE'S
  ONE permitted oversize declaration, so a second is a Medium finding. Compute
  `500 minus 48 minus <the block line count you measured>`, report it, and STOP rather
  than commit if it is negative.

C1b — book round 15's PASS and one reviewer slip, rewrite the plan
  `.agent/live_review.md` += ledger.md (append, +2)
  `.agent/prose_slips.md` += slips.md  (append, +1)
  `.agent/plan.md`        := plan.md   (rewrite, +22/-22)
  Subject: `F277 R16 C1b: book round 15's PASS and the reviewer's worktree slip`
  EXPECTED INSERTIONS: 25 by `git show --numstat` — 2 plus 1 plus the plan rewrite's own
  DIFF insertions of 22, all measured by applying these payloads in a disposable worktree
  at `b10e9bf1` and reading `git diff --numstat`. If yours differs, report what you
  measured and say so; do not adjust the payload.

C2 — THE EVIDENCE JOB AND THE REVIEW ZIP, and this commit's tracked change set is ONLY
     the handback
  Neither the evidence dir nor the zip is committed — `docs/roadmap/STATUS_closure_protocol.md`
  is explicit that a committed evidence dir puts evidence files into the `base..HEAD`
  review subject and the package then builds BLOCKED_EVIDENCE. Build both under
  `.remedy-wt/f277-r16-scratch/`, then rewrite `.agent/handoff.md` and push.
  Subject: `F277 R16 C2: rewrite handoff for round 16 with the evidence and package
  readings`

  (i) THE EVIDENCE BUNDLE. Write ONE driver script under your scratch directory that
      DERIVES every number it passes rather than taking it from this block, and run it:
      - Selection, fixed by this block because it is the feature's own evidence and is
        deliberately SCOPED — pitfall (d) forbids a verification record from ever
        carrying a FULL-SUITE node-id list, because the redaction-torture
        parametrizations embed fake secrets and absolute paths by design and the
        packaging metadata scanner correctly rejects them:
```
tests/orchestration/test_event_names.py tests/cli/test_json_envelope.py
tests/cli/test_memory_cmd.py tests/ui_contracts/test_humanize_catalog.py
tests/cli/test_golden_path.py
```
      - Run `python3 -m pytest -q -p no:cacheprovider --collect-only <selection>` and take
        `node_ids` from its output, one per collected test. Then run
        `python3 -m pytest -q -p no:cacheprovider <selection>` and take `passed`, `failed`
        and `exit_code` from the real run. ASSERT in the script that
        `len(node_ids) == passed + failed` — pitfall (a) is a record whose node ids do not
        account for every selected test — and report all four numbers. The reviewer's dry
        run of both commands in the primary checkout read 105 collected and
        `105 passed in 143.90s` at exit 0; report yours beside that.
      - `test_files` is the five paths of the selection, as FILES. Pitfall (b): a
        directory entry is rejected, so never write `tests/docs/`.
      - `run_id` must match `^vr-\d{4,}$` (pitfall (c)); use `vr-0001`.
      - Then call
        `packages.orchestration.job_evidence.create_manual_completion_bundle` with
        `evidence_dir` under your scratch directory, `repo_root="."`,
        `base_commit="f2494c0216b33d5f261195789ec9f7a300de5fca"` — the FULL-LENGTH SHA,
        because an abbreviated one surfaces only at zip time — `head_commit` the branch
        tip you measure, a 16-hex `job_id` of your choosing, `job_title` naming F277,
        `step_range="T001-T003"`, `prior_job_ids=[]`, the `verification_runs` list of one
        record you just built, `timestamp` and `generated_at` in the shapes the
        producer's own tests use, and `review_feature_id="f277"` — WITHOUT which the
        runtime gate runs every historical feature's bindings and blocks.
      - Report the returned summary dict in full, and report that
        `token_truth.json` exists in the evidence dir.
      WHY THAT BASE, and it is pitfall (e), the one that cost F260's closure a round:
      `base_commit` is the branch's FORK POINT and never `git merge-base` once a branch
      has merged `main` in. The reviewer measured both at `b10e9bf1` —
      `git rev-list --ancestry-path f2494c02..HEAD` and `git rev-list f2494c02..HEAD` both
      count 87, and a disagreement between those two counts is what says the base is
      wrong. RE-RUN BOTH YOURSELF at your own tip and report the two counts; if they
      disagree, STOP and hand back rather than packaging against a base that silently
      drops commits.

  (ii) THE REVIEW ZIP. With the tree CLEAN and the branch pushed — build it AFTER C1b is
      committed and pushed, from the reviewed head — run
      `bash scripts/make_review_zip.sh --evidence-dir <your evidence dir>` and report its
      full output and real exit code. Record the final zip FILENAME and its SHA-256,
      which the script prints, and the ABSOLUTE DIRECTORY the package was written to.
      The script defaults that directory to `$HOME/Repos/remedy-history/zips`, which the
      reviewer confirmed exists; if the sandbox refuses to write there, report the refusal
      verbatim and say so — DECISION amend0827 D1 requires the archived path or the
      literal `NOT ARCHIVED` in the record, and a guess is worse than either.
      A package whose status is not `READY_FOR_REVIEW` is a CLOSURE BLOCKER: report the
      status and the raw error and hand back WITHOUT attempting a second build. The cause
      is the reviewer's to diagnose next round.

CONSTRAINTS
1. Never edit a payload and never retype one.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the four `.agent/authored/f277-r16-*` copies, `.agent/live_review.md`,
   `.agent/prose_slips.md`, `.agent/plan.md` and `.agent/handoff.md`. NOTHING under
   `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`, and in particular NOT
   `scripts/self_use_queue.json`. Report the length you measure rather than checking it
   against a number this block states.
4. If a gate goes red, STOP. The zip's own status is the one reading this block asks you
   to report rather than repair.
5. Nothing this round writes may land inside the repository's tracked tree. The evidence
   dir, every log and the driver script live under `.remedy-wt/f277-r16-scratch/`. F281's
   round 28 left a scratch script under the TRACKED `.agent/` directory and it poisoned
   the evidence snapshot; that is the specific mistake this constraint exists for.
6. Leave the three `remedy/job-*` worktrees alone.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the three payload files, report the line count, byte count and sha256 you
     measured against the PAYLOADS table above. Nine readings, all equal.
 (b) For each `.agent/authored/f277-r16-*` copy at C1a — one per payload plus the block
     copy — compare it byte-for-byte with its source under
     `.remedy-wt/f277-r16-payloads/` (the block copy against
     `.remedy-wt/f277-r16-block.md`). Report one reading per copy and how many you
     compared; all True.
 (c) The two appends at C1b, by strict byte concatenation and never a length comparison:
     the file's bytes at `b10e9bf1` plus the payload's bytes equal the file's bytes at
     C1b. The reviewer measured the pres as 473511 and 353613 and the posts as 479169 and
     354909; report yours beside them. Then ONE negative control, on
     `.agent/live_review.md` only: flip a single bit inside the appended paragraph and
     show the reading returns False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte at 45 lines, under the
     50-line rule of AGENTS.md. Report both sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md` is 22 at `b10e9bf1` and 22 at
     C1b. Report both numbers. Round 16 registers and resolves nothing.

G2 THE BASE IS THE FORK POINT — report `git rev-list --ancestry-path
 f2494c0216b33d5f261195789ec9f7a300de5fca..HEAD` and `git rev-list
 f2494c0216b33d5f261195789ec9f7a300de5fca..HEAD`, both as counts, at your own tip. They
 must be EQUAL; report both numbers rather than the claim that they match, and STOP if
 they differ.

G3 THE VERIFICATION RECORD IS SELF-CONSISTENT — report `len(node_ids)`, `passed`,
 `failed`, `exit_code` and `len(test_files)` for the one record you built, the assertion
 `len(node_ids) == passed + failed` as the boolean your script evaluated, and that every
 `test_files` entry is a FILE by `os.path.isfile`. Report the collect count and the run's
 summary line beside the reviewer's 105 and `105 passed`.

G4 THE EVIDENCE BUNDLE — report the summary dict
 `create_manual_completion_bundle` returned in full, the evidence dir's absolute path,
 that `token_truth.json` is a file in it, and the final verdict the summary carries.

G5 THE PACKAGE — report `bash scripts/make_review_zip.sh --evidence-dir <dir>`'s full
 output and real exit code, then the three things DECISION amend0827 D1 and the closure
 protocol require in the record: the package FILENAME, its SHA-256, and the absolute
 directory it was written to or the literal `NOT ARCHIVED`. Report the package STATUS as
 the filename carries it. State whether `git status --porcelain` was empty immediately
 BEFORE the build, because a package built from a dirty tree is invalid.

G6 PUSH AND TREE — `git push -u origin feature/f277-machine-contracts` after C1b and
 again after C2; report both outcomes, then `git status --porcelain`, which must be
 empty, and `git worktree list`. Write the post-push readings into the handback itself
 after pushing, not into a trailing commit.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 7 of feature F277, round 16. Under AGENTS.md's
`### handoff.md`, every artifact-build attempt appears in the handoff with its status,
INCLUDING a failed one with its blocking reason — that rule is why this round exists as
its own round.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the
review of round 16, then — if the package is READY_FOR_REVIEW — the final closure round:
the §3 checklist consolidation carrying R-1014, the ledger rotation, the open-finding
owner re-assignment, and the STATUS `[x]` flip with the README sync and the `SU-025`
`consumed_by` edit in one commit, then the pull request. State the open-findings count,
which is 22, and the operator-questions count, which is 2.
