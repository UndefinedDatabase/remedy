── STEP CLOSURE: EVIDENCE JOB + REVIEW ZIP — F112 Prompt budget per task class ─
Round 23 · session continuing F112 · base `dd80e564` (F112 R22 C4, the tip
of feature/f112-prompt-budget-per-task-class)

Goal:
  Book round 22's PASS verdict (RECORD22, given verbatim below, already
  independently re-verified by the reviewer — do not re-derive it), then
  run docs/roadmap/STATUS_closure_protocol.md's Algorithm steps 1-2: the
  evidence job (`job_evidence.create_manual_completion_bundle`) and the
  mandatory fresh review zip (`scripts/make_review_zip.sh`). Neither step
  produces a repository diff — the evidence dir is NEVER committed
  (closure protocol's own explicit rule) — so this round's only COMMITS
  are the same mechanical bookkeeping every round has: booking the prior
  verdict and updating the plan. The evidence/zip work is an EXTERNAL
  ACTION, reported in the handback, not landed as a diff.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r23.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD22 to `.agent/live_review.md`
  C2   apply PLAN23 to `.agent/plan.md`
  C3   the handback: rewrite `.agent/handoff.md` (this round has no other
       content commit — the evidence/zip work below is an external action
       reported IN this handback, not its own commit)

Change set for COMMITS — NOTHING outside these paths:
  `.agent/authored/f112-r23.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `.agent/handoff.md`
  The evidence dir and the built zip (both described below) are created
  on disk but are NOT git-added, NOT committed — they must remain
  untracked/gitignored. NO file under `packages/`, `apps/`, `tests/` or
  `docs/` is touched. `scripts/self_use_queue.json` is NOT touched this
  round (its `consumed_by` edit is the closure commit's own, later).

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE. If a slice looks wrong,
     apply it anyway and DECLARE the problem in the handback.
  2. `.agent/STOP` is read FROM DISK before the first commit and again
     before C3 (this round's handback commit). If it exists at either
     reading: finish the commit in hand, write the handback, push, stop.
  3. `.agent/plan.md` ends WITHOUT a trailing newline; PLAN23 is applied
     as an exact whole-file replacement, no trailing newline added.
     `.agent/live_review.md` also ends WITHOUT a trailing newline; append
     it as `content_bytes + b"\n" + RECORD22_bytes` — ONE newline, no
     blank line. Confirm the byte immediately before the append point
     yourself before writing, per this feature's own established
     convention since R14.
  4. THE EVIDENCE BUNDLE: build it at repo-root path
     `remedy-job-evidence-f112-closure/` (already gitignored by the
     pattern `remedy-job-evidence-*/` — confirm this yourself with
     `git check-ignore -v remedy-job-evidence-f112-closure` before
     writing anything there). Use a Python driver (write it to disk with
     the Write tool and run it with
     `python3 -c "import runpy; runpy.run_path('/absolute/path/to/driver.py')"`,
     matching the pattern earlier rounds this session used to route around
     this sandbox's `.remedy-wt`-naming quirk — this path does not contain
     `.remedy-wt` so you likely will not hit that quirk here, but use the
     same driver-script approach anyway for reliability) that:
       a. Imports `_run_verifications` from `packages.orchestration.job_evidence`
          (a private helper — that is fine and intentional; it is the
          existing, tested logic that already produces correctly-shaped
          `VerificationTests` runs: real `run_id`s matching `^vr-\\d{4,}$`,
          real sha256 `output_hash`, real `node_ids` from a verbose run,
          `test_files` as FILE paths never directories — precisely the
          shapes that four historical BLOCKED_EVIDENCE attempts (F051,
          F052, F080) got wrong by hand-building these dicts instead).
       b. Runs it against these THREE SCOPED commands, run from the repo
          root, repo=".". Do NOT include the full 19546-test suite here —
          per the closure protocol's own explicit rule, a verification
          record may never carry a full-suite node-id list; the full-suite
          proof already rides in round 19's integration-gate evidence and
          the reviewer's own re-run:
            "python3 -m pytest tests/orchestration/test_class_prompt_budget.py"
            "python3 -m pytest tests/orchestration/test_context_compiler.py -k \"test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded or test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic\""
            "python3 -m pytest tests/cli/test_golden_path.py"
          If ANY of these three commands exits non-zero or reports a
          failure, STOP before calling `create_manual_completion_bundle`
          (which itself refuses a failing run) and declare this as a
          BLOCKING finding in the handback rather than a routine result —
          it would mean something regressed since round 19's own gate.
       c. Calls `create_manual_completion_bundle` from
          `packages.orchestration.job_evidence` with:
          `evidence_dir="remedy-job-evidence-f112-closure"`,
          `repo_root="."`,
          `base_commit="5c28c6741db2d9073fc75cd159d91037e0757fb0"` (the
          FULL 40-character merge-base SHA — an abbreviated one surfaces
          as a defect only at zip time, per the closure protocol's own
          documented lesson),
          `head_commit="dd80e564e034152e8f0becc49829250336ba7399"` (the
          full SHA of this round's own base, `dd80e564` — reconfirm this
          is still HEAD before the call; if the branch has moved, use the
          real current HEAD and declare the discrepancy),
          `job_id=uuid4().hex[:16]` (generate one fresh, matching
          `pingpong_job.py`'s own convention),
          `job_title="F112 Prompt budget per task class — closure evidence"`,
          `step_range="T001-T003"`,
          `prior_job_ids=[]`,
          `verification_runs=<the "runs" list from step (b)'s
          _run_verifications(...) return value>`,
          `timestamp=<current UTC ISO-8601, generated fresh>`,
          `generated_at=<current UTC ISO-8601 with microseconds, generated
          fresh>`,
          `num_tasks=3` (its own default — do not override),
          `note_prefix="F112 closure evidence"`,
          `review_feature_id="f112"`.
          Print and capture the returned summary dict in full.
     If this call raises, capture the FULL exception (class + message +
     traceback) and STOP — do not attempt a second call with different
     parameters on your own initiative; declare it in the handback as a
     blocking outcome for the reviewer to redesign the next round around.
  5. THE REVIEW ZIP: run
     `bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f112-closure`
     from the repository root as a real shell command (not a driver
     script — this one is a plain `bash` invocation with no `.remedy-wt`
     path in it). Capture its full stdout/stderr and real exit code. It
     should print a filename (matching the gitignored `remedy-review-*`
     pattern) and a SHA-256. Confirm the printed SHA-256 yourself with a
     direct `sha256sum` of the produced file. If it exits non-zero or
     prints anything indicating `BLOCKED_EVIDENCE`, that is this round's
     honest result — declare it fully in the handback (the exact blocking
     reason(s) the script/validator prints) rather than retrying blindly;
     do not attempt more than ONE retry, and only if the FIRST failure's
     printed reason names something you are confident this exact
     constraint-4 recipe already gets right (in which case declare why you
     believe a retry is warranted before running it).
  6. ARCHIVING: if the zip built successfully, attempt to copy (not move —
     leave the original where the script wrote it too) it into
     `/home/decodeux/Repos/remedy-history/zips/` (create the directory if
     it does not exist and you have permission to). Report the OUTCOME
     honestly either way: the absolute archived path, or the literal
     string `NOT ARCHIVED` with the reason (e.g. permission denied) if it
     could not be copied there. Do not treat a failed archive attempt as
     a round failure — DECISION amend0827 D1 explicitly allows `NOT
     ARCHIVED` as a valid recorded outcome.
  7. Do not `git add` or commit the evidence directory or the zip file.
     Confirm `git status --porcelain` still reads EMPTY with respect to
     tracked paths after all of this (untracked, gitignored paths do not
     count against this — confirm with `git status --porcelain
     --ignored=no`, which must show nothing for these paths since they
     match `.gitignore` patterns).
  8. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
     `docs/roadmap/features/T3_F112.md` are NOT touched this round.
  9. NEVER force-push, never work on `main`, create NO pull request, merge
     nothing, run no `--approve` / promotion of anything.

THIS ROUND'S PARAMETERS, measured by the reviewer at `dd80e564` before
this block was authored:
  LIVE_REVIEW PRE-C1   `.agent/live_review.md` measures 2299057 bytes,
                       ending WITHOUT a trailing newline.
  RECORD22 LENGTH      3870 bytes (measure this yourself against the
                       committed authored file's own extracted slice).
  POST-C1 EXPECTED     2299057 + 1 + 3870 = 2302928 bytes.
  HEADER SHAPE         lines matching `^Gate: F\\d+ R\\d+ — ` currently
                       number 269; matching `^Gate: F112 R22 — `
                       currently 0. Expected after C1: 270 and 1.
  OPEN SET             350 registered, 72 `Done:`, 278 open. UNMOVED by
                       this round's append. Reconfirm on both sides of C1.
  PLAN.MD PRE-C2       46 lines (per `wc -l`), ends WITHOUT a trailing
                       newline, currently holds PLAN22 (2099 bytes).
  MERGE BASE           `5c28c6741db2d9073fc75cd159d91037e0757fb0`,
                       reconfirm yourself with `git merge-base main HEAD`
                       before using it — declare if it has changed.

<<<BEGIN RECORD22>>>
Gate: F112 R22 — the round 22 entry, closure precondition 4's Built State section (no production code touched). VERDICT PASS, over the range `042d3683..dd80e564` (commits C0a `30c6d9b2`, C0b `99492af8`, C1 `a9387abd`, C2 `818a766e`, C3 `ae0b4111` — five real content commits — plus handback commit `dd80e564`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r22.md` and `HEAD:.agent/last_block.md` both print blob `e9d15484f981a462e56887bbdf0b62bd5c1bd17a`, reproduced directly; `wc -l` reproduced 257. THE PLAN REPLACEMENT AT C2 HELD BYTE-IDENTICAL: PLAN22 extracted from the committed authored file (2099 bytes) compared byte-for-byte against `.agent/plan.md` at C2 — equal, 2099 bytes both sides, no trailing newline, `## Goal` / `## Next Steps` each exactly once. THE RECORD APPEND AT C1 (booking RECORD21) HELD BYTE-IDENTICAL: pre-append `.agent/live_review.md` measured 2293718 bytes at `042d3683`, RECORD21 extracted from the committed authored file measured 5338 bytes exactly as pinned, appended as one newline plus RECORD21, post-append measured 2299057 bytes exactly matching `2293718 + 1 + 5338`; the pre-append content is an exact byte prefix; the file still ends WITHOUT a trailing newline; the open set recomputed mechanically read 350 registered / 72 `Done:` / 278 open on both sides, and lines matching `^Gate: F\d+ R\d+ — ` read 269 after C1 with exactly one matching `^Gate: F112 R21 — `. THE BUILT STATE APPEND AT C3 HELD BYTE-IDENTICAL, WITH TWO DECLARED CORRECTIONS TO THE REVIEWER'S OWN BLOCK, NEITHER A TRANSPORT DEFECT: (1) the block's params paragraph stated `.agent/plan.md`'s pre-C2 `wc -l` as 45; the real reading is 44 (the file has 44 newline characters; its 45th logical line carries no trailing newline) — a wording imprecision about what `wc -l` counts on a no-final-newline file, not a byte disagreement, and PLAN22 was still applied byte-for-byte and verified equal above; (2) the block's own stated arithmetic `3970 + 1 + 3520 + 1 = 7495` is simply wrong addition — the correct sum is 7492 — and BOTH pinned inputs (3970, 3520) were independently confirmed correct by the reviewer, so only the reviewer's own addition was off; the worker applied the slice byte-for-byte and reported the real 7492 rather than the block's wrong target, exactly as constraint 1 requires. Reproduced independently: `docs/roadmap/features/T3_F112.md` pre-C3 measured 3970 bytes ending WITH a trailing newline; BUILT_STATE extracted measured 3520 bytes exactly as pinned; post-C3 measured 7492 bytes exactly matching `3970 + 1 + 3520 + 1`; the pre-C3 content is an exact byte prefix of the post-C3 content; the file still ends with exactly one trailing newline; `grep -c '^## Built State'` reads 0 before and 1 after. G5 RE-VERIFIED BY THE REVIEWER DIRECTLY: `git status --porcelain` reads empty; `git diff --stat 042d3683..dd80e564 -- packages/ apps/ tests/` is empty; the only path touched under `docs/` in this range is `docs/roadmap/features/T3_F112.md`; every commit's insertion count (258, 191, 2, 19, 57) is under 500. NO NEW FINDING AND NONE RESOLVED: the open set is unmoved at 278 (350 registered, 72 `Done:`). Closure precondition 4 (Built State current) is now DISCHARGED. Closure preconditions 1 (latest verdict PASS, this one), 2 (integration gate, round 19), 3 (`remedy integrity_gate.run_integrity_checks()` all-PASS, reviewer-confirmed directly before round 22 was authored), 4 (this round) and 6 (round 21) are all satisfied; precondition 5 (clean tree, pushed, worker idle) holds now. Round 23 runs the evidence job and the mandatory review zip (docs/roadmap/STATUS_closure_protocol.md algorithm steps 1-2), producing no repository diff (the evidence dir is never committed) and reported in that round's own handback for the reviewer to author the STATUS line from.
<<<END RECORD22>>>

<<<BEGIN PLAN23>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use consumed round 21, Built
State landed round 22 (RECORD22: VERDICT PASS, booked this round). All
six closure preconditions are now satisfied. Round 23 runs the evidence
job and the mandatory review zip.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 23 builds the evidence bundle via
`job_evidence.create_manual_completion_bundle` (review_feature_id="f112",
scoped verification runs via `_run_verifications`, never a full-suite
node-id list), then the mandatory review zip
(`scripts/make_review_zip.sh --evidence-dir <path>`). Produces NO
repository diff — the evidence dir is never committed
(docs/roadmap/STATUS_closure_protocol.md). Results (job_id, package
filename, SHA-256, archived path or NOT ARCHIVED) are reported in the
handback for the reviewer to author the STATUS line from.

## Next Steps

- Reviewer authors the STATUS line from round 23's reported job_id/
  package/hash/path/accepted-HEAD.
- Closure commit: STATUS `[x]`, README capability sync (same commit,
  R-0154 pin), `scripts/self_use_queue.json` SU-007 `consumed_by=F112`,
  final `.agent/` state — nothing else.
- AGENTS.md PR workflow; merge deferred to the next feature's start.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to F112,
  carried forward per precondition 1's "Resolved or documented risk".
- Evidence-bundle construction has a documented history of BLOCKED_EVIDENCE
  pitfalls (F051/F052/F080) — round 23 uses the existing
  `_run_verifications` helper rather than hand-building verification_run
  dicts, specifically to avoid them.
<<<END PLAN23>>>

Done when — the gates below, each RUN and reported as ONE LINE in the
handback with its real reading. Every gate runs at a commit STRICTLY
EARLIER than C3 (this round's handback commit), or, for the external
evidence/zip action, before C3 is staged.

G1 TRANSPORT — `sha256sum` and byte length of the committed
   `.agent/authored/f112-r23.md`. Report that
   `git rev-parse HEAD:.agent/authored/f112-r23.md` and
   `git rev-parse HEAD:.agent/last_block.md` print ONE blob id after C0b.
   Report `wc -l .agent/authored/f112-r23.md`.

G2 THE PLAN — extract PLAN23 by delimiter, compare byte-for-byte against
   `.agent/plan.md` at C2 — must be equal. Report `wc -l .agent/plan.md`
   (must be under 50), no trailing newline, `## Goal` and `## Next Steps`
   each exactly once.

G3 THE RECORD APPEND — extract RECORD22 by delimiter, report its byte
   length (expected 3870 — if it does not match, DECLARE the mismatch,
   apply the extracted bytes as-is). Report the arithmetic
   `2299057 + 1 + <len> = <total>` against the real post-append size, the
   byte-prefix property, no trailing newline, a NEGATIVE CONTROL (flip one
   byte, recompute, report `False`), lines matching `^Gate: F112 R22 — `
   before (0) and after (1) C1, and registered/`Done:`/open counts on both
   sides (expected UNMOVED 350/72/278).

G4 THE EVIDENCE JOB — report each of the three scoped commands' exit
   code, passed/failed/skipped counts, and node_ids count (must equal
   `selected` per `_run_verifications`'s own arithmetic). Report the full
   summary dict `create_manual_completion_bundle` returns (job_id, head,
   authority count, partition sizes, final verdict) or the full exception
   if it raised. Report `git check-ignore -v remedy-job-evidence-f112-closure`
   confirming it is gitignored.

G5 THE REVIEW ZIP — report the script's real exit code, the printed
   filename and SHA-256, and your own independent `sha256sum` of the
   produced file (must match the script's own printed digest). Report the
   archiving outcome (absolute path, or `NOT ARCHIVED` with reason).

G6 THE TREE AND THE COMMITS — `git status --porcelain` immediately before
   C3 is staged — EMPTY (tracked paths only; the gitignored evidence dir
   and zip do not count against this — confirm neither appears in `git
   status --porcelain --ignored=no`). PER-COMMIT INSERTIONS (the `+`
   column) for C0a through C2, each confirmed under 500.

Handback: rewrite `.agent/handoff.md` in full — feature and round, session
number, branch, base and head SHAs, per-commit changed-files table, ONE
line per gate above with its real reading, the item-status table
AGENTS.md mandates, deviations, the open-findings count (expected 278,
unmoved), and the next expected action: the reviewer authors the STATUS
line from this round's own reported job_id/package/hash/path/accepted-HEAD,
then the closure commit + PR. It has NO length cap. Do not write a `Done:`
or `Gate:` paragraph anywhere beyond applying RECORD22 verbatim. State
plainly whether the evidence job and the zip both succeeded, or exactly
where either blocked. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report
the outcome; create NO pull request, merge nothing.
══END BLOCK══