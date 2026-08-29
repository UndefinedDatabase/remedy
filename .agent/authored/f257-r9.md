### STEP T002 — F257 Self-use track, round 9 (THE EVIDENCE BUNDLE AND THE REVIEW ZIP)

Goal: book the round 8 verdict — closure precondition 6 is satisfied — and then
execute steps 1 and 2 of `docs/roadmap/STATUS_closure_protocol.md`: the final
evidence bundle and a FRESH review zip, built from a clean tree at the reviewed
head. This round does NOT close the feature. No `[x]`, no README sync, no
`consumed_by` edit and no pull request: those are the closure commit's, which is
the NEXT round, and building the package first is what the protocol's step order
requires.

Base: `fcf90e85`, the tip of `feature/f257-self-use-track` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r9.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R8 verdict into `.agent/live_review.md`
- then PUSH, and build the bundle and the zip from the clean tree at C2
- C3 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r9.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/handoff.md`

THE EVIDENCE DIRECTORY IS NEVER COMMITTED and neither is the zip. Both are
gitignored by construction — `.gitignore` line 226 matches `remedy-job-evidence-*/`
and line 223 matches `remedy-review-*` — and a committed evidence dir puts
evidence files into the `base..HEAD` review subject, which packages
BLOCKED_EVIDENCE. That is the F147 attempt-2 lesson and this round does not
repeat it. NO file under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/` is
edited. `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json`
are NOT touched this round.

ACCEPTED HEAD IS C2. The zip is built after C2 is committed and pushed, so the
manifest's `committed_review_subject.head_commit` is C2's full sha. C3 writes only
`.agent/handoff.md` and follows the READY package, exactly as the protocol's build
order states. Report C2's full sha as the accepted HEAD; the next round's STATUS
line will carry it.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `fcf90e85`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch and no pull request. Never
   force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r9.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push. AGENTS.md also requires that EVERY artifact-build
   attempt — bundle, zip, and the deliberate red control below — appears in the
   handback with its status, failed attempts included with the blocking reason.
5. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through a scratch script under the
   gitignored `.remedy-wt/`, and copy with `shutil.copyfile`. Capture real exit
   codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`. This
   Python is 3.10: an f-string expression may not contain a backslash, so hoist
   any regex into a named variable. Report every re-expression.
6. THE APPEND CONVENTION: an appended slice is separated from the text before it
   by exactly ONE BLANK LINE and the file ends with exactly one trailing
   newline. Concretely, for a target whose last byte is already a newline, write
   one newline then the slice, the slice carrying its own single terminator.
   This constraint is the authority on separators; if a gate formula below
   disagrees, follow this constraint and declare the disagreement.
7. THE OPEN SET IS COUNTED BY DISTINCT ID, as
   `len(set(registered ids) - set(resolved ids))`. It reads 255 at `fcf90e85`.
   THIS ROUND REGISTERS NO ID AND RESOLVES NONE, so it must still read 255 at C2
   and the registered count must be UNMOVED at 297. A `Gate:` paragraph is not a
   registration.
8. EXIT CODE 0 IS NEVER THE READING FOR THE ZIP. `scripts/make_review_zip.sh`
   exits 0 for a BLOCKED_EVIDENCE package as readily as for a READY one. The
   reading is `PACKAGE_STATUS` in the printed output and `package_status` in
   `.review_zip_manifest.json`. A handback that reports the zip green on an exit
   code is a finding.

### The authored slices

<<<SLICE PLANF257R9
# Plan — F257 Self-use track

Branch: feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220. F257 was claimed by Rule A5 as the first unchecked line in
`docs/roadmap/STATUS.md` after F256.

## Goal
Remedy is used on Remedy on a schedule that cannot be skipped: a curated queue
of small maintenance jobs, exactly one consumed per feature close, run through
`do job-plan` and `do job-run` against this repository and taken to the normal
approval gate.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the queue file and its read-only loader | done | round 2, 18 tests |
| render a queue item and plan it on the real job path | done | round 3 |
| refuse a job file written outside its destination | done | round 4, R-0733 |
| consume exactly one item per feature close | done | round 4, precondition 6 |
| refuse an id that is not one file name | done | round 5, R-0735 |
| document the format where a reader looks | done | round 5 |
| the integration gate | done | round 6, PASSED, 18186 passed 0 failed |
| the feature file's Built State | done | round 7, precondition 4 |
| plan SU-001 and stop at the approval gate | done | round 8, precondition 6 |
| the evidence bundle and the review zip | done | this round, closure steps 1-2 |
| the closure commit and the PR | open | next, and it is the last round |

## Next Steps
1. The closure commit, in ONE commit: the `[x]` flip on line 85 of
   `docs/roadmap/STATUS.md`, the README capability sync that may never disagree
   with it, the `scripts/self_use_queue.json` `consumed_by` edit that marks SU-001
   consumed by F257, and the final `.agent/` state.
2. Open the pull request. It is NOT merged in this session — the gap is the
   operator's manual-review window, and the next feature's Open PR Gate merges it.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.
<<<END PLANF257R9

<<<SLICE GATEF257R8
Gate: F257 R8 — CLOSURE PRECONDITION 6, the round that made the self-use track run on Remedy itself. THE ROUND PASSED, AND PRECONDITION 6 IS SATISFIED FOR F257. Every gate was re-executed by the reviewer at `fcf90e85` from a script of its own, and the structure reproduced exactly: transport EQUAL at sha256 `36200f7b…d4360e7` over 19141 bytes with ONE blob id `2c252c39…c727` at C0b; the plan byte-equal at 2107 bytes over 42 lines with one `## Goal` and one `## Next Steps`; the record reconstructing 1402722 + 3178 → 1405901 from GATEF257R7 alone, the negative control failing at an offset the script proved inside the appended text and the pre-round blob a byte PREFIX of the result; the ledger registered UNMOVED at 297 all DISTINCT, `Done:` 44 lines over 42 distinct ids and `Landed:` 11 both UNMOVED, `Gate:` 112 → 113, and the open set UNMOVED at 255, which is what a round that registers nothing must produce; both residues empty over five SINGLE-PARENT commits of 285, 167, 10, 8 and 91 insertions; delimiters 0 and 0 in all four targets against a 2/2 control; `.remedy-wt` untracked at 0; and all five named paths ABSENT from the range.

THE RENDERED BYTES ARE THE CURATED BYTES, AND THE REVIEWER RAN THE SHIPPED FUNCTION RATHER THAN READING THE TRANSCRIPT BACK. `.agent/selfuse_f257/SU-001.md` at C3 is byte-identical to the SU-001 `job_markdown` of `scripts/self_use_queue.json` at `ba28d224` — 1235 bytes and sha256 `a26bf662…af51` on both sides — and the reviewer then called `plan_next_self_use_item` itself against this repository and measured `status` `planned`, `job_title` `Document the Markdown job-file format`, tasks `['T001']` and `job_file_sha256` `a26bf662…af51`, the same digest as the curated bytes. That last equality is the one that proves nothing was templated between the queue and the plan. The `job_id` differed between the worker's run and the reviewer's, as it must — it is minted fresh per run, which is precisely why the block ordered it REPORTED and stated no expected value for it.

THE RUN COULD NOT CHECK ITSELF OFF, WHICH IS THE WHOLE POINT OF THE PRECONDITION. `scripts/self_use_queue.json` is byte-identical at `ba28d224` and at C3 and ABSENT from the range's numstat; SU-001's `consumed_by` is still the empty string; and `next_self_use_item()` answered `SU-001` before the worker's run, after it, and again in the reviewer's independent re-run. Consumption stays the closure commit's edit, which is what DECISION F257 D2 rules and what makes this a gate rather than a report.

THE HANDBACK'S HONESTY IS THE PART WORTH RECORDING. The job was PLANNED and NOT RUN, and the documentation page SU-001 asks for was NOT written; the handback says exactly that as its first deviation, unhedged, and `docs/` is ABSENT from the range, so the disk agrees with the prose. The committed transcript carries ZERO occurrences of `/home/`, every path relative to the repository root, which keeps the packaging metadata scanner out of the closure's way a round early. The worker also declared that a `${PIPESTATUS[0]}` form was rejected by the guard and that the affected suite was re-run unpiped with only the unpiped reading reported — a re-expression declared rather than a number quietly kept.

THE SUITES WERE RE-RUN, NOT READ: `tests/orchestration/test_self_use_job.py` 18 passed, `tests/orchestration/test_self_use_queue.py` 18 passed, `tests/docs/test_docs_consistency.py` 295 passed, and the canary `tests/cli/test_golden_path.py` 42 passed — one pytest process at a time, every REAL exit 0.
<<<END GATEF257R8

`PLANF257R9` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R8` is a
SINGLE APPEND to `.agent/live_review.md` under constraint 6. This round registers
nothing and resolves nothing.

### The evidence script — ADAPTED FROM THE COMMITTED TEMPLATE, NOT WRITTEN FRESH

Do NOT invent an evidence script. Extract the slice named `EVIDENCESCRIPT` from
the COMMITTED blob `git show HEAD:.agent/authored/f009-r33.md` by its
`<<<SLICE EVIDENCESCRIPT` and `<<<END EVIDENCESCRIPT` marker lines, save it to
`.remedy-wt/f257_evidence.py`, and change ONLY the values listed below. Every
other line stays BYTE FOR BYTE as the template has it — the double path scrub in
`_tail`, node ids from `--collect-only`, the `len(node_ids) == selected` assert,
the sorted `test_files`, the `_unsafe_text` pre-scan with its red control, and the
`OUTPUT_HASH` re-derivation are all load-bearing, each one paid for by a closure
that was blocked without it.

The values to change, and nothing else:

- `EVIDENCE_DIR` → `<REPO>/.remedy-wt/f257_closure_evidence/remedy-job-evidence-f257-closure`
- `BASE` → `f17b1d0d03e4042df8452b2019b719cbe4704b21` — the merge base of this
  branch with `main`, the merge commit of pull request #220, measured with
  `git merge-base main HEAD`. It is 40 characters; the template asserts that.
- the `runs = [...]` list → exactly these four, in this order, with no `-k`
  expression and no deselection on any of them:
  - `mkrun("vr-0001", "tests/orchestration/test_self_use_queue.py", 18)`
  - `mkrun("vr-0002", "tests/orchestration/test_self_use_job.py", 18)`
  - `mkrun("vr-0003", "tests/docs/test_docs_consistency.py", 295)`
  - `mkrun("vr-0004", "tests/cli/test_golden_path.py", 42)`
- the `create_manual_completion_bundle(...)` keyword arguments:
  `job_id="f257-closure"`, `job_title="F257 Self-use track - closure"`,
  `step_range="T001-T002"`, `prior_job_ids=["f256-closure"]`, `num_tasks=2`,
  `note_prefix="operator-attested manual completion - F257 closure"`,
  `review_feature_id="f257"`.

WHY THESE FOUR SUITES AND NOT THE FULL SUITE: a verification record may NEVER
carry a full-suite node-id list. `len(node_ids) == selected` forbids filtering the
list, and the packaging metadata scan correctly rejects the redaction-torture
parametrizations elsewhere in this repository whose ids embed fake secrets and
absolute paths by design. That is the F080 R4 lesson (d). The full-suite proof
rides in the round 6 integration-gate evidence at `.agent/gate_f257_r6/` and in
the reviewer's own re-run, and nothing green is claimed here that was not run.
The reviewer has already scanned all four suites' collected ids with
`build_review_manifest._unsafe_text` and measured ZERO rejections, so the
pre-scan the template performs is expected to pass; if it does not, STOP and hand
back with the rejected strings.

### The zip, the red control and the archive

1. Confirm the tree is clean and the branch is pushed, then build with
   `bash scripts/make_review_zip.sh --evidence-dir <the EVIDENCE_DIR above>`.
   Report `PACKAGE_STATUS`, the zip filename and its SHA-256.
2. THE RED CONTROL, which proves the pipeline can still fail honestly. Copy the
   evidence directory to a SECOND directory under `.remedy-wt/`, append ONE node
   id containing an absolute path to the first run of that copy's
   `verification_tests.json`, and build a zip from the COPY. It must report
   `PACKAGE_STATUS=BLOCKED_EVIDENCE` and `EVIDENCE_AUTHORITATIVE` false, AT EXIT
   CODE 0 — report the exit code beside the status to make the point that the
   status is the reading. Declare this attempt in the handback as a DELIBERATE
   CONTROL, per constraint 4. The real bundle is not touched by it.
3. Move the READY zip — not the control zip — to
   `/home/decodeux/Repos/remedy-history/zips`, which exists and holds the 21
   packages of previous closures. Use `shutil.move`. Report the absolute
   destination path: DECISION amend0827 D1 makes it a recorded value, because the
   round that builds the package is the only actor that knows where it went.
4. Leave the control zip where it was built and say so; do not delete anything by
   glob, and name any path you do remove exactly.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before the zip build; report both answers. If it exists at either reading,
finish the commit in hand, write the handback and stop. Report constraint 0's
three readings and `git status --porcelain | wc -l` after each of C0a, C0b, C1 and
C2, and again immediately BEFORE the zip build, where it must be 0.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r9.md` and of the reviewer's
own original at `.remedy-wt/f257-r9-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r9.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R9 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE RECORD APPEND AT C2. Reconstruct the C2 blob of `.agent/live_review.md`
from the `fcf90e85` blob plus GATEF257R8 under constraint 6, and report `True` or
`False` with all three lengths. NEGATIVE CONTROL: flip one byte at an offset your
script CONFIRMS lies inside the appended text, recompute, and report the equality
is now `False`. Report that the pre-round blob is a byte PREFIX, with both
lengths, and that the C2 blob ends in exactly ONE newline.

G5 THE LEDGER AT C2, counted under constraint 7. Report over
`.agent/live_review.md` at `fcf90e85` and again at C2: the count of lines matching
`^- R-\d+ — ` and whether all are DISTINCT; the count of `^Done: R-\d+ — ` lines
AND the count of DISTINCT ids among them, as two separate numbers; the count of
`^Landed: R-`; the count of `^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered UNMOVED at 297 and
all distinct, the `Done:` numbers and `Landed:` UNMOVED, `Gate:` 113 → 114, and
the open set UNMOVED at 255. Report the count of `^Gate: F257 R8 — ` at C2, which
must be 1.

G6 THE EVIDENCE BUNDLE. (a) Report the unified diff between the template slice
`EVIDENCESCRIPT` and your adapted `.remedy-wt/f257_evidence.py`, and the count of
changed lines: ONLY the values the section above lists may differ, and the
handback names each changed line. (b) Report, per verification run, `run_id`,
`selected`, `len(node_ids)`, whether `len(node_ids) == selected`, `passed`,
`failed`, `skipped`, `deselected`, and `test_files` with whether that list is
SORTED — an unsorted list is rejected by `_vt_safe_files` and packages
BLOCKED_EVIDENCE. Expected passes: 18, 18, 295, 42, with failed and skipped 0 and
deselected 0 everywhere. (c) Report the `_unsafe_text` pre-scan result over every
node id and every command — expected 0 rejected — BESIDE its red control on a
fabricated absolute-path id, which must read True; a scanner that rejects nothing
proves nothing. (d) Report the full list of gate files the producer wrote into
the evidence directory, and confirm all eight closed-schema gates are present:
`final_verifier_report`, `fresh_evidence`, `artifact_contract`,
`change_provenance`, `manifest_integrity`, `postmortem_integrity`,
`commit_execution` and `runtime_integration`. (e) Report, per run, whether
`output_hash` equals sha256 of `stdout_summary` EXACTLY — the preimage rule that
blocked the F083 closure and is still not in the protocol's pitfall list.

G7 THE REVIEW ZIP, read under constraint 8. (a) Report the zip filename, its
SHA-256, the REAL exit code of the build, and `PACKAGE_STATUS`, which must be
`READY_FOR_REVIEW`. (b) From `.review_zip_manifest.json` report `package_status`,
`ready_gate_matrix.ok`, `blocking_reasons` — expected empty — and
`committed_review_subject.head_commit`, which must equal C2's FULL sha; report
C2's full sha beside it. (c) THE RED CONTROL: report the control build's
`PACKAGE_STATUS`, which must be `BLOCKED_EVIDENCE`, its `EVIDENCE_AUTHORITATIVE`
value, which must be false, and its REAL exit code, which is expected to be 0 —
state plainly that the exit code did not distinguish the two builds and the
status did. (d) Report the absolute path the READY zip was moved to and confirm
the file exists there afterwards, with its size in bytes. (e) Report
`git status --porcelain | wc -l` after all of it, which must be 0 — both
artifacts are gitignored and neither may dirty the tree.

G8 STRUCTURE AND THE REMAINING PRECONDITIONS, over `fcf90e85..<C2>` for the range
readings. The change set lists `.agent/handoff.md`, which C3 writes AFTER this
range ends, so compute the changeset-minus-range residue over the change set
WITHOUT that ONE path and name the path you excluded; the range-minus-changeset
residue is computed against the FULL change set and must be empty. Report each
commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1 and C2 is
single-parent. Report the number of lines beginning `<<<SLICE ` and `<<<END ` in
`.agent/plan.md` and `.agent/live_review.md` at C2 — each expected 0 — beside the
same counts over `.agent/authored/f257-r9.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0, and
`git ls-files | grep -c remedy-job-evidence`, expected 0 — the evidence dir is not
committed. Report the `git diff --numstat` line over the range for
`docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and
`docs/roadmap/features/T5_F257.md`, all four expected ABSENT. Finally, PRECONDITION
3: run `from packages.orchestration.integrity_gate import run_integrity_checks`
and report `result.passed` and `result.fail_count` — it answers an
`IntegrityGateResult` OBJECT with attributes, not a dict, so `.get(...)` raises.

### Handback

Rewrite `.agent/handoff.md` in C3 per docs/agents/handback_template.md. It
carries: `SESSION 3 of feature F257 · round 9`; the roster of this session's
rounds, this round included; the range `fcf90e85..HEAD`; a per-commit
changed-files table whose `+/-` cells are taken from `git diff --numstat`; ONE
LINE PER GATE G1 through G8 with its real result; the deviations, including every
guard re-expression constraint 5 required; the item-status table with every
C-item and every gate appearing exactly once; the open-findings count, which must
be 255; and the next expected action — the closure commit and the pull request.

It ALSO carries, as the values the next round needs and cannot re-derive:
`Evidence job f257-closure`, the package filename, its SHA-256, the absolute
archived path, and the ACCEPTED HEAD, which is C2's full sha. Write them as a
short labelled list, because the next round's STATUS line is authored from them
and `.agent/handoff.md` is the only carrier between the two.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R8 is
reviewer-authored text you apply verbatim, and any OTHER such paragraph is a
finding however hedged. Do not flip any `[ ]` or `[~]` to `[x]` anywhere. Do not
create a pull request and do not merge anything.

After C3: push with `git push origin feature/f257-self-use-track` and report the
outcome.
