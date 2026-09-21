STEP R17 — F277 closure: the package, rebuilt against a pre-check that cannot lie

GOAL
Round 16's package is BLOCKED_EVIDENCE on one validator error — the verification record's
`test_files` was dictated in selection order and the validator requires it sorted.
Register the product half as R-1017, land the pitfall as (f) in the closure protocol so
the next closure reads it before paying for it, and rebuild. This round adds ONE thing
round 16 did not have: `validate_verification_tests` is called on the produced document
BEFORE the package build, so a rejection costs seconds instead of a round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r17-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r17-scratch/`   YOURS. Every log, exit-code capture, driver script and
      the EVIDENCE DIR itself go here. Both are gitignored. Do NOT reuse round 16's
      scratch directory: a fresh evidence dir per attempt is what makes the two packages
      distinguishable afterwards.

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
   `feature/f277-machine-contracts` at `f44b8846`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r17-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all four under `.remedy-wt/f277-r17-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 7966 | bd47e0ff9962ec70109e6254c080162acd8997f9eb47baa636a46ff09f545fe4 |
| plan.md | 44 | 2200 | 1fab9568a147897847671aef72084a753c8bf7904737a25fbeea7f342feb9a6e |
| protocol.diff | 31 | 1976 | 749264e80f02c88c389d1becd719ea883426afd61ce3ea5edc9a8ce09543b823 |
| slips.md | 2 | 2460 | b5c2a9d8ae7ad271663c92e594cb25fd9504ac6fd095668da2ceaef46982490d |

`ledger.md` is an APPEND of TWO PARAGRAPHS beginning with a single newline that is the
record separator: the R-1017 registration and the round 16 `Gate:` entry, in that order,
each on one line with a blank line between them, which is the shape every entry in that
file already has. `slips.md` is an APPEND of TWO LINES with NO leading newline.
`plan.md` is a REWRITE. `protocol.diff` goes on with `git apply`; it was generated from
the tree at `f44b8846` and dry-run with `git apply --check` at exit 0, and its pair was
tested mechanically for containment — TO contains FROM: true, so it is APPEND-shaped and
no FROM-zero count is owed. `.agent/decisions.md` and `.agent/operator_questions.md` are
not touched.

BUNDLE — the commits are C1a, C1b, C2 and C3, in this order

C1a — copy this block and all four payloads into `.agent/authored/`
  `.agent/authored/f277-r17-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r17-<name>` per payload, keeping each payload's own file name.
  Subject: `F277 R17 C1a: copy round 17 payloads into .agent/authored/`
  SIZE. The payloads total 81 lines, so this commit's insertions are 81 plus this block's
  own line count, and the 500 cap binds at 419 block lines. Round 12 spent this FEATURE'S
  ONE permitted oversize declaration, so a second is a Medium finding. Compute
  `500 minus 81 minus <the block line count you measured>`, report it, and STOP rather
  than commit if it is negative.

C1b — register R-1017, book round 16's PASS and two slips, rewrite the plan
  `.agent/live_review.md` += ledger.md (append, +4)
  `.agent/prose_slips.md` += slips.md  (append, +2)
  `.agent/plan.md`        := plan.md   (rewrite, +15/-16)
  Subject: `F277 R17 C1b: register R-1017, book round 16's PASS and two reviewer slips`
  EXPECTED INSERTIONS: 21 by `git show --numstat` — 4 plus 2 plus the plan rewrite's own
  DIFF insertions of 15, all measured by applying these payloads in a disposable worktree
  at `f44b8846` and reading `git diff --numstat`. If yours differs, report what you
  measured and say so; do not adjust the payload.

C2 — LAND PITFALL (f) IN THE CLOSURE PROTOCOL
  `git apply .remedy-wt/f277-r17-payloads/protocol.diff`, touching only
  `docs/roadmap/STATUS_closure_protocol.md`. It adds a sixth producer pitfall beside the
  five that file already carries, naming the sorted-`test_files` requirement, the two
  producers that disagree about it, finding R-1017, and the cheap pre-check this round
  introduces. This is a docs edit in the closure's own scope: the file exists so a
  closure stops rediscovering these, and this one has now cost two closures a round each
  while living only in the reviewer's notes.
  Subject: `F277 R17 C2: record the sorted test_files pitfall in the closure protocol`
  Expected insertions: 21, measured the same way.

C3 — THE EVIDENCE BUNDLE AND THE PACKAGE, REBUILT; this commit's tracked change set is
     ONLY the handback
  Neither the evidence dir nor the zip is committed. Build both under
  `.remedy-wt/f277-r17-scratch/`, then rewrite `.agent/handoff.md` and push.
  Subject: `F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`

  (i) THE BUNDLE, as round 16 built it with ONE field changed. Write a fresh driver under
      your scratch directory that DERIVES every number rather than taking it from this
      block. The selection is unchanged and is deliberately SCOPED, because pitfall (d)
      forbids a verification record from carrying a full-suite node-id list:
```
tests/cli/test_golden_path.py tests/cli/test_json_envelope.py
tests/cli/test_memory_cmd.py tests/orchestration/test_event_names.py
tests/ui_contracts/test_humanize_catalog.py
```
      THAT LIST IS WRITTEN ABOVE IN SORTED ORDER ON PURPOSE, and `test_files` must be
      exactly it — but do not trust this block for that: call `sorted()` on the list in
      your driver and assert the result equals what you pass, so the property is measured
      in the script rather than read off the page. Everything else is round 16's shape:
      `node_ids` from `--collect-only`, `passed`/`failed`/`exit_code` from the real run,
      the in-script assertion that the node ids account for every selected test,
      `run_id="vr-0001"`, and the same derived `head_sha`, `output_hash`, `selected`,
      `deselected`, `skipped` and `duration_seconds` fields round 16's record carried —
      that record validated clean on every one of those, so change none of them.
      Then call `packages.orchestration.job_evidence.create_manual_completion_bundle`
      with a FRESH `evidence_dir` under your scratch, `repo_root="."`,
      `base_commit="f2494c0216b33d5f261195789ec9f7a300de5fca"` — the full-length fork
      point — `head_commit` the tip you measure, a NEW 16-hex `job_id` distinct from
      round 16's `f2771600aabbccdd`, `job_title` naming F277,
      `step_range="T001-T003"`, `prior_job_ids=[]`, your one-record `verification_runs`,
      `timestamp` and `generated_at`, and `review_feature_id="f277"`.

  (ii) THE PRE-CHECK, WHICH IS THE POINT OF THIS ROUND. Before building any package, load
      `verification_tests.json` from the evidence dir you just wrote and run
      `scripts/build_review_manifest.py`'s `validate_verification_tests` over it. Report
      the problems list and the `passed` value. The problems list MUST be empty and
      `passed` must be 105. The reviewer ran exactly this on round 16's document at
      `9dbd8e6d`: as built it returned
      `['verification_tests.json runs[0] test_files is not sorted']` with `passed`
      unresolvable, and the same document with that one list sorted returned an empty
      list at `passed` 105 — so this check reproduces both colours and is not a gate that
      cannot fail. If the problems list is NOT empty, STOP and hand back with it
      verbatim; do not build a package you already know will be blocked.

  (iii) THE PACKAGE. Only once (ii) is empty, with the tree CLEAN and the branch pushed —
      build after C2 is committed and pushed — run
      `bash scripts/make_review_zip.sh --evidence-dir <your fresh evidence dir>` and
      report its full output and real exit code. Record the package FILENAME, its
      SHA-256, its STATUS as the filename carries it, and the ABSOLUTE DIRECTORY it was
      written to, which round 16 measured as `/home/decodeux/Repos/remedy-history/zips`.
      Also report the manifest's `committed_review_subject.head_commit`, which must equal
      the commit you built from — that value becomes the `accepted HEAD` of the STATUS
      line next round, so a wrong one poisons the permanent record.
      A package that is still not `READY_FOR_REVIEW` is a CLOSURE BLOCKER: report the
      status and the raw error and hand back WITHOUT a second build.

CONSTRAINTS
1. Never edit a payload and never retype one.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the five `.agent/authored/f277-r17-*` copies, `.agent/live_review.md`,
   `.agent/prose_slips.md`, `.agent/plan.md`, `docs/roadmap/STATUS_closure_protocol.md`
   and `.agent/handoff.md`. NOTHING under `packages/`, `apps/`, `tests/` or `scripts/`,
   and in particular NOT `scripts/self_use_queue.json`. Report the length you measure
   rather than checking it against a number this block states.
4. If a gate goes red, STOP. The package's own status is the one reading this block asks
   you to report rather than repair, and the pre-check is the one gate whose red ENDS the
   round before the package is built.
5. Nothing this round writes may land inside the tracked tree. The evidence dir, every
   log and the driver live under `.remedy-wt/f277-r17-scratch/`. Round 16 got this right
   and its path set was eight `.agent/` files; hold that.
6. Leave the three `remedy/job-*` worktrees alone. Leave round 16's BLOCKED_EVIDENCE
   package where it is — it is the record of a real attempt and AGENTS.md requires every
   artifact-build attempt to appear in the handoff, including a failed one.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the four payload files, report the line count, byte count and sha256 you
     measured against the PAYLOADS table above. Twelve readings, all equal.
 (b) For each `.agent/authored/f277-r17-*` copy at C1a — one per payload plus the block
     copy — compare it byte-for-byte with its source under
     `.remedy-wt/f277-r17-payloads/` (the block copy against
     `.remedy-wt/f277-r17-block.md`). Report one reading per copy and how many you
     compared; all True.
 (c) The two appends at C1b, by strict byte concatenation and never a length comparison.
     The reviewer measured the pres at `f44b8846` as 479169 and 354909 and the posts as
     487135 and 357369; report yours beside them. Then reading (b), the independent
     structural reader (§3 item 36): let N be the number of blank-line-separated
     paragraphs your script COUNTS in `ledger.md`, and compare the LAST N such units of
     the whole file against those N paragraphs IN ORDER. Report N as you counted it. Then
     ONE negative control: flip a single bit inside the FIRST appended paragraph and show
     BOTH readings return False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte at 44 lines, under the
     50-line rule of AGENTS.md. Report both sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md` is 22 at `f44b8846` and 23 at
     C1b, because this round registers R-1017 and resolves nothing. Report both numbers
     and the new id.

G2 THE PROTOCOL EDIT — at C2, report the new pitfall paragraph's first four lines
 verbatim from `docs/roadmap/STATUS_closure_protocol.md`, and report the count of the
 string `(f) each verification record` in that file, which must be 1. Then
 `git diff --name-only <C1b> <C2>` must name exactly that one path — report the list and
 its length. Then run `python3 -m pytest -q -p no:cacheprovider tests/docs/` and report
 the summary line and the real exit code; the reviewer read `314 passed` at exit 0 at
 `f44b8846`, and this edit adds prose to a file `tests/docs/` reads.

G3 THE VERIFICATION RECORD IS SORTED AND SELF-CONSISTENT — report `test_files` exactly as
 you passed it, the boolean `test_files == sorted(test_files)` your driver evaluated,
 `len(node_ids)`, `passed`, `failed`, `exit_code`, `len(test_files)`, the assertion that
 the node ids account for every selected test as the boolean your script evaluated, and
 that every `test_files` entry is a FILE by `os.path.isfile`. Report the collect count
 and the run's summary line beside round 16's 105 and `105 passed`.

G4 THE PRE-CHECK — report `validate_verification_tests`'s problems list and `passed`
 value over the document you just produced, and the absolute path of the file you loaded
 it from, which must be inside THIS round's fresh evidence dir and not round 16's. The
 problems list must be empty and `passed` must be 105.

G5 THE PACKAGE — report the build's full output and real exit code, then the package
 FILENAME, its SHA-256, its STATUS, the absolute directory it was written to or the
 literal `NOT ARCHIVED`, and the manifest's `committed_review_subject.head_commit`. State
 whether `git status --porcelain` was empty immediately BEFORE the build. Also report the
 evidence bundle's returned summary dict in full and that `token_truth.json` exists in
 the fresh evidence dir.

G6 PUSH AND TREE — `git push -u origin feature/f277-machine-contracts` after C2 and again
 after C3; report both outcomes, then `git status --porcelain`, which must be empty, and
 `git worktree list`. Write the post-push readings into the handback itself after
 pushing, not into a trailing commit.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 7 of feature F277, round 17. Under AGENTS.md's
`### handoff.md`, EVERY artifact-build attempt appears in the handoff with its status —
so the handback names BOTH packages, round 16's BLOCKED_EVIDENCE one and this round's,
each with its filename, hash and status.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the
review of round 17, then — if the package is READY_FOR_REVIEW — the final closure round:
the §3 checklist consolidation carrying R-1014, the ledger rotation, the open-finding
owner re-assignment, and the STATUS `[x]` flip with the README sync and the `SU-025`
`consumed_by` edit in one commit, then the pull request, which is NOT merged this
session. State the open-findings count, which is 23 after C1b, and the
operator-questions count, which is 2.
