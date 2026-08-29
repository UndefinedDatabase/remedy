# STEP 28 — F033 Hunk-level diff approval (SESSION 7, round 28; the CLOSURE PREPARATION round)

Goal: book the round 27 verdict, register the one rule violation that round
landed, add its independent confirmation to an OPEN finding rather than minting
a second id for it — then perform the closure preconditions that must be true
BEFORE a STATUS line can be written: the feature file's Built State, the
integrity check, the evidence job, and the review zip built from a clean tree.
The STATUS flip and the pull request belong to the NEXT round and to no part of
this one.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r28.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN28.
4. C2: append slice RECORD28 to `.agent/live_review.md` — books the round 27
   PASS WITH RISKS, REGISTERS R-0750 and EXTENDS the OPEN finding R-0736.
5. C3: append slice BUILTSTATE to `docs/roadmap/features/T5_F033.md`.
6. C4: the closure artifacts — the integrity check, the evidence job and the
   review zip, per G6 and G7. NOTHING from these is committed: the evidence dir
   is gitignored by design and the zip is an artifact, not a tracked file. If
   G6 or G7 produces no file to commit, C4 IS NOT A COMMIT and the Bundle is
   six commits rather than seven. Say which in the handback.
7. C5: rewrite `.agent/handoff.md` as the handback, carrying the evidence job
   id, the package filename, its SHA-256 and its ARCHIVED PATH.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r28.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/roadmap/features/T5_F033.md
    .agent/handoff.md

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `f13134fe`, this round's base.

- THE SELF-USE QUEUE IS EXHAUSTED, which satisfies closure precondition 6 by its
  own words rather than by an exception. `scripts/self_use_queue.json` carries
  one item and ZERO pending: every item's `consumed_by` is set. The closure
  therefore records `self-use NONE (queue exhausted)` and closes normally.
- THE FEATURE FILE HAS NO BUILT STATE SECTION. Its headings run `Goal & Done`,
  `How it fits`, `Design`, `Task slicing`, `Acceptance`, `Edge cases &
  assumption defaults (A9)`, `Orchestrator brief`, `Do not touch` and
  `Amendments`. It is 6358 bytes over 117 lines and ends with a newline. The
  convention to follow is `docs/roadmap/features/T5_F256.md`, whose closure
  appended `## Built State (F256, 2026-08-28)` as the LAST section of the file.
- THE STATUS LINE IS `- [~] F033 — Hunk-level diff approval`, at line 86 of
  `docs/roadmap/STATUS.md`. It is NOT touched this round.
- THE OPEN SET HOLDS R-0736 AND IT IS THIS ROUND'S ANSWER TO A QUESTION THE
  GATE RAISED. R-0736 is Medium and OPEN, headed "THE INTEGRATION GATE'S OWN
  PARITY RECIPE MANUFACTURES 114 FALSE BASE FAILURES ON EVERY RUN THAT FOLLOWS
  IT LITERALLY", and it names the same mechanism and the same count of 114 that
  round 27 measured. Under docs/agents/planner_reviewer_prompt.md §3 item 30
  that evidence joins R-0736 and spends no new id.
- THERE ARE EXACTLY TWO OVERSIZE COMMITS ON THIS BRANCH, walked mechanically
  over all 232 commits of `bd8d9529`..`f13134fe`: `5f0273d8` at 647 insertions
  across three `.agent/` files, and `e313c0c0` at 7561 insertions in one. The
  first is not exempt — the AGENTS.md exemption covers a verbatim rewrite of a
  SINGLE named `.agent/**` state file, and that commit touches three paths — so
  `e313c0c0` is the SECOND, which is what R-0750 registers.
- NO HIGH FINDING IS OPEN, so `integrity check` cannot be blocked by
  `high_blockers_open`. The two findings this round adds to the record are a
  Medium registration and an extension of an existing Medium.

## Slice PLAN28 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file.

<<<BEGIN PLAN28
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7 of this feature, in its closure sequence.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002 and T003 | done | rounds 1-24 |
| R-0749, both instances | done | resolved round 27 |
| the operator guide and its index rows | done | round 26 |
| the integration gate | done | round 27, PASS WITH RISKS |
| the feature file's Built State | open | this round |
| the evidence job and the review zip | open | this round |
| the STATUS line, the README sync and the PR | open | next round |
| R-0745 and R-0750, carried as documented risks | open | see Risks |

## Next Steps
1. This round books the round 27 verdict, registers R-0750, extends R-0736, and
   performs the closure preconditions that must hold BEFORE a STATUS line can be
   authored: the Built State section, the integrity check, the evidence job and
   a review zip built from a clean tree after the last content commit.
2. The NEXT round is the closure commit itself — the STATUS `[x]` line and the
   README capability sync in ONE commit, the final `.agent/` state, then the
   pull request. That PR is NOT merged in this session; it merges at the next
   feature's start via the Open PR Gate, which is the operator's review window.
3. `self-use NONE (queue exhausted)` is recorded at closure: the queue holds no
   pending item, which the closure protocol rules is exhausted rather than
   blocked.

## Risks
- R-0745 (Low) and R-0750 (Medium) stay OPEN at closure, so the STATUS line
  reads PASS_WITH_RISKS. Neither is reachable from this feature's Acceptance:
  the first hardens a guard over the write door, the second is a reviewer's gate
  wording that ordered a full log where the canonical procedure asks for a tail.
<<<END PLAN28

## Slice RECORD28 — appended to `.agent/live_review.md`

Three paragraphs, blank-line separated. The middle one begins `- R-0750 — ` and
is the round's only registration; the last begins `R-0736 EXTENSION — ` with no
leading `- `, so it adds no id.

<<<BEGIN RECORD28
Gate: F033 R27 — THE INTEGRATION GATE. THE ROUND PASSED WITH RISKS, AND THE RISK IS A RULE VIOLATION THE REVIEWER'S OWN GATE ORDERED, REGISTERED BELOW AS R-0750. Every gate was re-executed by the reviewer at `f13134fe`. TRANSPORT: the reviewer's own pre-emission original, `.agent/authored/f033-r27.md` and `.agent/last_block.md` are all 22358 bytes at sha256 `5b81aa42…1bbcf9` and BYTE-EQUAL. THE PLAN is byte-EQUAL to PLAN27 at 2211 bytes over 42 lines. THE RECORD APPEND at `0e0314dc` reconstructs 1618414 plus one newline plus 6988 to 1625403, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 2, the last two units equal to the slice's paragraphs IN ORDER, and a negative control at byte 1620637 — the reviewer's own offset, distinct from the worker's 1620651 and inside the FIRST appended paragraph — REJECTED by both readers. THE LEDGER: registered 310 distinct UNMOVED; `Done:` 54 lines over 52 distinct going to 55 over 53 with the ADDED resolved id exactly `R-0749`; `Landed:` 22 UNMOVED with `^Landed: R-0749 — ` still exactly 2; `^Gate: F033 R26 — ` 0 before and exactly 1 after; and the open set 258 to 257. THE BRANCH RUN is a REAL exit 1 at 2 failed, 18445 passed and 20 skipped in 187.66 seconds, under the five-minute budget. THE BASE RUN in a worktree on the throwaway branch `tmp/base-gate` at `bd8d9529` is a REAL exit 1 at 114 failed, 18072 passed and 20 skipped in 151.21 seconds. THE PARITY CLAIM HOLDS AND IS MEASURED BY THE EVENT, NOT THE OUTCOME: `shutil.copytree(src, dst, symlinks=True)` was written as ordered, 27 of 27 symlinks SURVIVED as symlinks, each destination is a real directory rather than a symlink, `REMEDY_UI_NO_AUTO_BUILD` was set in `os.environ` and never as a shell prefix, and ZERO `apps/ui/dist` mtimes fall inside the run window 1788009268.624 to 1788009420.420, with no file appearing, vanishing or changing. THE COMPARISON: `comm -13` — the BRANCH-ONLY set, and the only set that can hold a blocker — is EMPTY at 0 ids, so no branch-only failure exists to be coupled to feature code. `comm -23` holds 112. Two further ids failed on BOTH sides and therefore appear in NEITHER comm set, and the worker stated them explicitly rather than letting them fall between the two: branch 2 equals branch-only 0 plus shared 2, and base 114 equals base-only 112 plus shared 2, so every FAILED line of both runs is accounted for. THE TWO SHARED IDS ARE THE XDIST-FLAKE CLASS AND THE REVIEWER MEASURED IT INDEPENDENTLY: re-running `test_unresolvable_job_id_matches_the_get_door` and `test_dashboard_no_raw_leaks` SERIALLY in the primary checkout at `f13134fe` gives a REAL exit 0 at 1 passed each, which docs/agents/integration_gate.md step 4 rules "record, not a blocker". THE 112 BASE-ONLY IDS WERE ATTRIBUTED BY A MEASURED A/B RATHER THAN BY THE RAW LOG, which is exactly what finding R-0396 says the log alone cannot supply: in the SAME worktree at the SAME commit, changing ONLY the artifact, the stale state gives 112 of 112 FAILED with 112 occurrences of `ERROR: React UI not built.` and ZERO auto-build lines, and advancing four `apps/ui/dist` mtimes with `os.utime` — `dist/index.html` sha256 UNCHANGED — gives 112 of 112 PASSED. The reviewer confirmed the mechanism by reading `_frontend_is_stale` in `packages/orchestration/ui_server.py`, which returns True when ANY file under `apps/ui/src/` is newer than `dist/index.html`, and by confirming `dist/index.html` is BYTE-IDENTICAL in both trees. ZERO ids are unattributed. THE CLEANUP: the worktree is removed and pruned, `tmp/base-gate` is deleted, `git worktree list` shows the primary checkout alone, `git status --porcelain` is EMPTY and `git ls-files --others --exclude-standard` returns zero paths. G8's under-500 clause is the one that FAILED, honestly reported RED with its real number rather than repaired, and it is R-0750 below. THE WORKER'S JUDGEMENT WAS RIGHT TWICE OVER: it declared the oversize commit rather than truncating evidence to make a gate green, and it declined to make an unqualified "full suite green" claim over a run that exited 1. Both are the behaviour this record exists to encourage.

- R-0750 — Medium, A SECOND OVERSIZE COMMIT LANDED ON THIS FEATURE'S BRANCH, AND THE REVIEWER'S OWN GATE WORDING IS WHAT ORDERED IT. MEASURED by the reviewer at `f13134fe` by walking all 232 commits of `bd8d9529`..`f13134fe` mechanically: exactly TWO exceed the 500-insertion cap AGENTS.md sets — `5f0273d8` at 647 insertions across `.agent/authored/f033-close4.md`, `.agent/handoff.md` and `.agent/last_block.md`, and `e313c0c0` at 7561 insertions in `.agent/gate_f033_r27/base_run.txt` alone. The first is NOT covered by the AGENTS.md exemption, which reaches a commit whose diff is the verbatim rewrite of a SINGLE named `.agent/**` state file and that commit touches three paths. AGENTS.md states the consequence in as many words: an oversize commit is acceptable only when it is declared with its inseparability reason AND is the only such commit in its feature, and "a second one in the same feature, is a finding (Medium)". THE CAUSE IS THE BLOCK, NOT THE WORKER. The R27 block's G5 and G6 ordered "Write the full output to `branch_run.txt`" and `base_run.txt`, while `docs/agents/integration_gate.md` step 1 asks for the "raw tail, full FAILED list, exit code, wall time" — a tail, not the whole log. A base run with 114 failures writes 114 tracebacks, so the order made a commit over the cap unavoidable, and the worker met it, declared it with its inseparability reason and reported G8 RED rather than truncating the evidence to turn a gate green. That is the correct behaviour and it is recorded as such. WHY MEDIUM AND NOT LOW: the violation is durable and on disk, a later reader auditing this branch's commit discipline finds it without any prose to explain it, and the "accepted, not a precedent" allowance AGENTS.md grants once per feature was already spent by `5f0273d8`. FIX, AND IT IS FORWARD-LOOKING BY CONSTRUCTION: the history is NOT rewritten — this workflow forbids force-pushing outright, and deleting committed evidence to satisfy a size rule trades an auditable violation for an unauditable gap, which is the worse of the two. The repair is to the ORDER: an integration-gate block writes the run's RAW TAIL and its full FAILED list to the evidence file, as the canonical procedure already says, and never the whole log; where a full log is genuinely wanted it is an artifact of the review zip rather than a tracked commit. Resolved when a later integration-gate block in this repository orders the tail-plus-FAILED-list form and its evidence commit lands under the cap, and this finding's resolution names that block.

R-0736 EXTENSION — INDEPENDENTLY CONFIRMED AT A SECOND FEATURE, WITH THE PER-ID A/B THE RAW LOG CANNOT GIVE, AND WHY THIS IS NOT A NEW ID. R-0736 is OPEN and already states the mechanism and the count; under docs/agents/planner_reviewer_prompt.md §3 item 30 a new id is minted only after the open set is searched for the DEFECT, and this is that defect, so the evidence joins it and R-0751 is not spent. THE CONFIRMATION, measured at the F033 R27 integration gate and re-read by the reviewer at `f13134fe`: the base run at `bd8d9529` produced 114 FAILED lines, the same figure R-0736 records, of which 112 are base-only and 2 are shared with the branch. `dist/index.html` is BYTE-IDENTICAL in the primary checkout and in the base worktree, and `_frontend_is_stale()` answers False in the first and True in the second — because `git worktree add` stamps every checked-out source file with the checkout time while `shutil.copytree` preserves the source mtimes, so the copied build is byte-correct and mtime-stale. WHAT THIS ROUND ADDS THAT R-0736 DID NOT HAVE is the discriminating experiment finding R-0396 asked for: in the same worktree at the same commit, with only the artifact's mtime changed by `os.utime` and its sha256 unchanged, the stale state fails 112 of 112 and the fresh state passes 112 of 112. That is direct per-id evidence rather than an inference from a log line, and it closes R-0396's objection that a present-but-stale `index.html` and an absent one produce byte-identical output. THE COUNTER-MEASURE R-0736's FIX SHOULD CARRY, stated here so the next gate need not rediscover it: after copying `apps/ui/dist` into a base worktree, advance its mtimes past the worktree's own checkout time — the copy is already byte-correct, so nothing is rebuilt and nothing is faked; what is corrected is a timestamp the copy mechanism cannot preserve meaningfully across a fresh checkout.
<<<END RECORD28

## Slice BUILTSTATE — appended to `docs/roadmap/features/T5_F033.md`

<<<BEGIN BUILTSTATE
## Built State (F033, 2026-08-29)

What exists on disk at the close of F033, so a later reader need not reconstruct
it from this file's future tense.

**T001 — stable content-hash hunk ids.** `packages/orchestration/hunk_identity.py`
computes a hunk's public name as the first `HUNK_ID_LENGTH` — 16 — lowercase hex
characters of a SHA-256 over the file's resolved path, the hunk's NORMALISED OLD
side (its context and deleted lines in order, never its added lines) and the
hunk's occurrence rank among byte-identical old sides within the same file. The
stability property a reader may rely on is that a hunk keeps its id when anything
else in its file moves and when its own ADDED lines change, because a second
proposed fix for the same original text is the same hunk; it changes only when
the path changes or when the hunk's own old side does. `diff_parser.py` carries
that id out through `DIFF_VIEW_VERSION` 2 — a REAL bump, because version 1 had
already been served to a consumer by the F256 diff endpoint.

**T002 — the decision core, the ledger and the door.** `hunk_approval.py` decides
whether a decision is coherent and returns one of five refusal codes in a pinned
check order; `hunk_decision_record.py` records a decision onto `job.metadata`
under `hunk_decisions`, keyed by `<task_id>:<attempt>`, and mints two refusal
codes of its own for an absent and for a truncated diff; `hunk_ledger.py` holds
the result on TWO independent axes — `state` in {approved, rejected, pending} and
`landing` in {landed, not_landed, unattempted} — and exports and imports it as
plain data. DECISION F033 D4 is the boundary the whole slice rests on: recording
a decision is NOT applying it, so the command writes `job.metadata` and touches
no repository, `may_mutate_repo` and `requires_permission` are both False in
`apps/cli/command_catalog.py`, and every entry a recording writes lands
`unattempted`. The operator door is `remedy patch approve-hunks`, handled in
`apps/cli/commands/patch.py`; it is documented for operators in
`docs/guides/hunk-approval-user-guide-v1.md`.

**T003 — partial truth, and the rejection-to-repair loop end to end.** The
partial apply state is rendered on all three surfaces the feature names, which is
finding R-0738's resolution. The loop itself is complete and each hop is tested:
`hunk_repair_findings.py` renders rejected entries as repair findings holding the
operator's reason BYTE FOR BYTE; `pingpong_loop.py` composes that text as the
`builder_hunk_rejections` segment ahead of the builder directive;
`hunk_decision_record.load_latest_hunk_ledger_from_metadata` selects the latest
record for a task from a metadata MAPPING, dragging no storage behind it; and
`pingpong_job.py` — the one place that holds the job at its `run_pingpong` call —
passes `hunk_ledger=_recorded_hunk_ledger_for_task(job, task)`. A decision
recorded at JOB scope lands under the `DIFF_SCOPE_JOB` sentinel rather than a task
id and is deliberately NOT quoted into any single task's prompt, because it was
never attributed to one.

**What is deliberately NOT here.** No hunk-level APPLY runs from this command;
the apply seam is the job branch's, where an approved patch intent already
exists. Remedy does not render what was APPROVED into a repair prompt — a prompt
listing what the operator accepted is a different feature, and this one carries
only what must change. And a rejection reason is never reformatted, wrapped,
truncated or normalised anywhere along the route: it is the operator's own words,
and the next round is told to act on them.
<<<END BUILTSTATE

## Constraints

1. Apply every slice BYTE FOR BYTE. If one looks wrong, apply it as written and
   declare the problem; never silently repair it.
2. PLAN28 is a FULL REWRITE. RECORD28 and BUILTSTATE are APPENDS. Measured by
   the reviewer at `f13134fe`, `.agent/live_review.md` is 1625403 bytes and
   `docs/roadmap/features/T5_F033.md` is 6358 bytes over 117 lines, and BOTH end
   with a newline, so each append is one blank-line separator then the slice.
   RE-MEASURE both yourself at the commit you append at.
3. Do NOT delete or edit any landed `Landed:`, `Done:` or `Gate:` text, and do
   not edit any existing line of the feature file. The record and that file's
   history are append-only this round.
4. DO NOT TOUCH `docs/roadmap/STATUS.md`, `README.md` or
   `scripts/self_use_queue.json`. The STATUS flip, the README capability sync
   and the self-use edit belong to the NEXT round's single closure commit, and
   splitting them is what the R-0154 pin forbids.
5. Touch no path outside the change set. This round changes NO file under
   `packages/`, `apps/` or `tests/`.
6. THE ZIP IS BUILT FROM A CLEAN TREE AFTER THE LAST CONTENT COMMIT, which is
   C3. A package built from a dirty tree is invalid. Do not commit the evidence
   directory: `.gitignore` excludes `remedy-job-evidence-*/` and a committed
   evidence dir puts evidence files into the review subject and packages
   BLOCKED_EVIDENCE.
7. A FAILING ZIP BUILD IS A CLOSURE BLOCKER, not something to work around.
   Record the raw error in the handback and stop; do not retry with different
   arguments more than once, and never hand-edit a manifest.
8. The `remedy` console script is denied in this sandbox. Use
   `python3 -m apps.cli.grouped <group> <cmd> ...` and SAY in the handback which
   form was used, so the evidence chain stays honest.
9. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, process substitution, a heredoc nested in `bash -c`, and a shell
   line containing a brace with a quote inside it. Write scripts under
   `.remedy-wt/` and run them as `python3 -B <path>`. REAL exit codes come from
   `subprocess.run(...).returncode`, never from a pipe.
10. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
11. G1 through G8 all run at or before C4; the handback commit C5 follows them.
    Remove any scratch you wrote under `.remedy-wt/` BY EXACT PATH, never by
    glob, and leave the evidence directory and the built package where they are.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r28.md`, and the same two readings for
`.agent/last_block.md`. One digest comparison.

G2 THE PLAN. `.agent/plan.md` byte-EQUAL to PLAN28, under 50 lines, holding
`## Goal` and the substring `Steps`. Report the byte length and the line count.

G3 THE RECORD APPEND, at C2. Reconstruct the MEASURED base plus one newline plus
the byte length of RECORD28 to the committed size. Prove the pre-commit blob a
byte PREFIX and the slice an exact SUFFIX. COUNT N in the script. Compare the
file's LAST N blank-line units against the slice's paragraphs IN ORDER. Flip one
byte inside the FIRST appended paragraph, report the offset, prove it lies in
that paragraph's span, and show BOTH readers reject the flipped bytes and accept
the unflipped ones.

G4 THE LEDGER, at `f13134fe` and at C2: `^- R-\d+ — ` 310 distinct going to 311
with the ADDED id exactly `R-0750`; `^Done: R-\d+ — ` 55 lines over 53 distinct
UNMOVED, this round resolving nothing; `^Landed: ` 22 UNMOVED;
`^Gate: F033 R27 — ` 0 before and exactly 1 after; and the open set 257 going to
258. Report also that `^R-0736 EXTENSION — ` occurs exactly 1 time and that
`^- R-0736 — ` still occurs exactly 1 time, so the extension added no id.

G5 THE BUILT STATE, at C3. `docs/roadmap/features/T5_F033.md` satisfies ORDERED
EQUALITY: the pre-commit blob is a byte PREFIX of the post-commit file, the slice
is an exact SUFFIX of it, and the lines C3's diff ADDS are exactly the slice's
lines IN ORDER with ZERO deleted lines. Report the before and after byte lengths
and the added-line count. Then `python3 -m pytest tests/docs/ -q` at a REAL exit
0, with its pass count reported against the 295 this branch measured at round 26.

G6 THE INTEGRITY CHECK AND THE EVIDENCE JOB, at C4 with a CLEAN tree.
  (a) `python3 -m apps.cli.grouped integrity check --json` — report the REAL
      exit code and the verdict field. A non-PASS is a closure BLOCKER: report
      it and stop.
  (b) Build the evidence bundle with
      `packages.orchestration.job_evidence.create_manual_completion_bundle`
      with `review_feature_id` set to `f033`. Report the JOB ID and the
      evidence directory path. Then LIST the gate documents the bundle actually
      wrote and name any of these eight that is ABSENT: final_verifier_report,
      fresh_evidence, artifact_contract, change_provenance, manifest_integrity,
      postmortem_integrity, commit_execution, runtime_integration.
      `write_runtime_integration_gate` alone is NOT a bundle and packages as
      BLOCKED_EVIDENCE.

G7 THE REVIEW ZIP, at C4, from a CLEAN tree after C3.
`bash scripts/make_review_zip.sh --evidence-dir <the dir G6 reported>`. Report
the REAL exit code, the package FILENAME, its SHA-256, and its ARCHIVED PATH —
the absolute directory it was moved to, or the literal `NOT ARCHIVED` when it
was left where it was built, which DECISION amend0827 D1 requires. Then report
the manifest's `committed_review_subject` base and head commits and confirm the
head is C3, and report the zip import check's own result. If the build fails,
record the RAW error verbatim and STOP — that is a closure blocker.

G8 STRUCTURE, at C4. `git status --porcelain` EMPTY. Per-commit insertions from
C0a through the last commit before the handback, each reported and each under
500 — this round has no evidence log to commit, so a number over 500 here is a
defect rather than a declared exception. The path set over `f13134fe`..C4 equal
to the change set minus `.agent/handoff.md` in BOTH directions. And
`git ls-files --others --exclude-standard` reported as a COUNT plus the list, so
the evidence directory and the package are shown to be untracked rather than
merely uncommitted.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, SESSION 7 of F033, branch, commit SHAs, changed-files table, one line per
gate G1 through G8 with its REAL exit code, the open-findings count, an
item-status table covering every Bundle item, every deviation, and the next
expected action. No length cap. Carry, as their own labelled lines so the next
round can quote them without re-deriving: the evidence JOB ID, the package
FILENAME, its SHA-256, its ARCHIVED PATH, the accepted HEAD commit, and
`self-use NONE (queue exhausted)`. If any gate is RED, do not repair on your own
initiative: report it and stop.
