### STEP T001-T003 — F258 Self-use track v2, round 11 (THE EVIDENCE BUNDLE AND THE REVIEW ZIP)

Goal: book the round 10 verdict — all six closure preconditions are satisfied
— and then execute steps 1 and 2 of `docs/roadmap/STATUS_closure_protocol.md`:
the final evidence bundle and a FRESH review zip, built from a clean tree at
the reviewed head. This round does NOT close the feature. No `[x]`, no README
sync, no `consumed_by` edit and no pull request: those are the closure
commit's, which is the NEXT round, and building the package first is what the
protocol's step order requires.

Base: `3d2ab8b5`, the tip of `feature/f258-self-use-v2` and the handback this
round starts from.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f258-r11.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F258 R10 verdict into `.agent/live_review.md`
- then PUSH, and build the bundle and the zip from the clean tree at C2
- C3 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f258-r11.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/handoff.md`

THE EVIDENCE DIRECTORY IS NEVER COMMITTED and neither is the zip. Both are
gitignored by construction — a committed evidence dir puts evidence files
into the `base..HEAD` review subject, which packages BLOCKED_EVIDENCE (the
F147 attempt-2 lesson; this round does not repeat it). NO file under
`packages/`, `apps/`, `tests/`, `scripts/` or `docs/` is edited.
`docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are
NOT touched this round.

ACCEPTED HEAD IS C2. The zip is built after C2 is committed and pushed, so
the manifest's `committed_review_subject.head_commit` is C2's full sha. C3
writes only `.agent/handoff.md` and follows the READY package, exactly as
the protocol's build order states. Report C2's full sha as the accepted
HEAD; the next round's STATUS line will carry it.

### Constraints

0. BEFORE ANYTHING: report
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — expected `[]`; if it is not `[]` now, STOP and hand back without
   committing. Report `git rev-parse HEAD`, which must equal `3d2ab8b5`'s
   full sha, and `git branch --show-current`, which must be
   `feature/f258-self-use-v2`. Create no branch and no pull request. Never
   force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording,
   retitling, correction or shortening. If a slice looks wrong, apply it as
   written and say so in the handback's deviations; the record is repaired
   by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and
   never reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f258-r11.md`, never from this prompt's
   text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push. AGENTS.md also requires that EVERY
   artifact-build attempt — bundle, zip, and the deliberate red control
   below — appears in the handback with its status, failed attempts
   included with the blocking reason.
5. Shell forms rejected by this session's guard are RE-EXPRESSED, never
   skipped and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace
   literals containing quotes, and every form of environment-variable
   assignment are rejected by FORM; route such work through a scratch
   script under the gitignored `.remedy-wt/`, and copy with
   `shutil.copyfile`. Capture real exit codes with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`. This Python
   is 3.10: an f-string expression may not contain a backslash, so hoist
   any regex into a named variable. Report every re-expression.
6. THE APPEND CONVENTION: an appended slice is separated from the text
   before it by exactly ONE BLANK LINE and the file ends with exactly one
   trailing newline. Concretely, for a target whose last byte is already a
   newline, write one newline then the slice, the slice carrying its own
   single terminator.
7. THE OPEN SET IS COUNTED BY DISTINCT ID, as
   `len(set(registered ids) - set(resolved ids))`. It reads 263 at
   `3d2ab8b5`. THIS ROUND REGISTERS NO ID AND RESOLVES NONE, so it must
   still read 263 at C2 and the registered count must be UNMOVED at 318. A
   `Gate:` paragraph is not a registration.
8. EXIT CODE 0 IS NEVER THE READING FOR THE ZIP.
   `scripts/make_review_zip.sh` exits 0 for a BLOCKED_EVIDENCE package as
   readily as for a READY one. The reading is `PACKAGE_STATUS` in the
   printed output and `package_status` in `.review_zip_manifest.json`. A
   handback that reports the zip green on an exit code is a finding.

### The authored slices

<<<SLICE PLANF258R11
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 11.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001/T002/T003, integration gate | done | rounds 2-7 |
| all six closure preconditions | done | rounds 8-10 |
| the evidence bundle and the review zip | done | this round, closure steps 1-2 |
| the closure commit and the PR | open | next, and it is the last round |

## Next Steps
1. The closure commit, in ONE commit: the `[x]` flip on F258's line of
   `docs/roadmap/STATUS.md`, the README capability sync that may never
   disagree with it, the `scripts/self_use_queue.json` `consumed_by` edit
   that marks SU-002 consumed by F258, and the final `.agent/` state.
2. Open the pull request. It is NOT merged in this session — the gap is
   the operator's manual-review window, and the next feature's Open PR
   Gate merges it.

## Risks
- R-0570 (Low), R-0736 (Medium), R-0757 (Medium): all OPEN, all
  documented, none block a PASS WITH RISKS closure.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays
  there.
- A job must never mark its own queue item consumed; DECISION F257 D2
  rules the consumption point stays the closure commit's edit.
<<<END PLANF258R11

<<<SLICE GATEF258R10
Gate: F258 R10 — PRECONDITION 4 DISCHARGED: THE FEATURE FILE'S BUILT STATE SECTION IS NOW CURRENT. VERDICT PASS, NO DEVIATION. The reviewer re-ran every gate independently against the real diff `9e8b3030..3d2ab8b5`. G1 TRANSPORT: the block, `.agent/authored/f258-r10.md` and `.agent/last_block.md` all sha256 `6ebad7a4c7b2bb603ca43394411d70455f354eab6ab4ade81a2a6e911907fbc9`, 15000 bytes — equal to the reviewer's own scratch original. G2 THE PLAN: `.agent/plan.md` sha256 `221ff160cb16a36ded9811b0ab6f3dd11d40e5c3c1910e1e3897c3376946d145`, 1823 bytes, 42 lines, `## Goal`/`## Next Steps` present, ends `\n`. G3 THE LIVE_REVIEW.MD APPEND: base 1795167 bytes; `base + b"\n" + GATE_R9 (3793 bytes) == committed (1798961 bytes)` True; the last `\n\n`-unit equals GATE_R9 exactly; a negative control (byte flip, disposable worktree, removed after) was independently reproduced by the reviewer and correctly rejected, the true original correctly accepted — the worker ran this same control itself this round and reported it honestly, correcting round 9's process gap. G4 THE PROSE_SLIPS.MD APPEND: base 33397 bytes; `base + b"\n" + PROSE_SLIP (650 bytes) == committed (34048 bytes)` True — byte-equality only, per the gate-budget rule for a prose file. G5 THE BUILT STATE APPEND: base 4140 bytes; `base + BUILTSTATE (3339 bytes) == committed (7479 bytes)` True, pure concatenation, exactly one `## Built State (F258, ` heading in the committed file. G6 DOCS-ROUND GATE: `python3 -m pytest tests/docs/ -q` REAL exit 0, 295 passed, unchanged from baseline. G7 THE LEDGER: before C2, 318 R-ids / 55 Done-ids / `DECISION F258` `['D1','D2']` / `Gate: F258 R` lines ending at R8; after, same R-ids/Done-ids/DECISION, `Gate: F258 R` lines ADDED exactly `['F258 R9']`. G8 THE TREE AND CANARY: `git status --porcelain` empty, single worktree, no `tmp/*` branch, per-commit insertions 205/157/18/2/2/59 all under 500, canary REAL exit 0, 42 passed. THE ROUND PASSES CLEANLY: the branch is pushed and matches `origin` exactly at `3d2ab8b5`. ALL SIX CLOSURE PRECONDITIONS OF STATUS_closure_protocol.md ARE NOW MET FOR F258: precondition 1 (every F258-scoped finding Medium/Low, latest verdicts PASS), precondition 2 (round 7's integration gate PASSED), precondition 3 (integrity check PASSED, re-confirmed round 9), precondition 4 (this round's Built State section), precondition 5 (tree clean, pushed), precondition 6 (round 8's real plan+run of SU-002, findings — R-0757 — registered round 9). The next round is the Algorithm: the evidence job, the fresh review zip, and (the round after) the STATUS line, README sync and final PR.
<<<END GATEF258R10

`PLANF258R11` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF258R10`
is a SINGLE APPEND to `.agent/live_review.md` under constraint 6. This round
registers nothing and resolves nothing.

### The evidence script — ADAPTED FROM THE COMMITTED TEMPLATE, NOT WRITTEN FRESH

Do NOT invent an evidence script. Extract the slice named `EVIDENCESCRIPT`
from the COMMITTED blob `git show HEAD:.agent/authored/f009-r33.md` by its
`<<<SLICE EVIDENCESCRIPT` and `<<<END EVIDENCESCRIPT` marker lines, save it
to `.remedy-wt/f258_evidence.py`, and change ONLY the values listed below.
Every other line stays BYTE FOR BYTE as the template has it — the double
path scrub in `_tail`, node ids from `--collect-only`, the
`len(node_ids) == selected` assert, the sorted `test_files`, the
`_unsafe_text` pre-scan with its red control, and the `OUTPUT_HASH`
re-derivation are all load-bearing, each one paid for by a closure that was
blocked without it.

The values to change, and nothing else:

- `EVIDENCE_DIR` → `<REPO>/.remedy-wt/f258_closure_evidence/remedy-job-evidence-f258-closure`
- `BASE` → `18ae71293cde9b1157aca35d3d02c3a8f4265813` — the merge base of
  this branch with `main`, the merge commit of pull request #225 (F040's
  closure), measured with `git merge-base main HEAD`. It is 40 characters;
  the template asserts that.
- the `runs = [...]` list → exactly these seven, in this order, with no
  `-k` expression and no deselection on any of them:
  - `mkrun("vr-0001", "tests/orchestration/test_self_use_queue.py", 23)`
  - `mkrun("vr-0002", "tests/orchestration/test_self_use_job.py", 18)`
  - `mkrun("vr-0003", "tests/orchestration/test_self_use_generator.py", 20)`
  - `mkrun("vr-0004", "tests/orchestration/test_self_use_runner.py", 7)`
  - `mkrun("vr-0005", "tests/orchestration/test_self_use_findings.py", 3)`
  - `mkrun("vr-0006", "tests/docs/test_docs_consistency.py", 295)`
  - `mkrun("vr-0007", "tests/cli/test_golden_path.py", 42)`
- the `create_manual_completion_bundle(...)` keyword arguments:
  `job_id="f258-closure"`,
  `job_title="F258 Self-use track v2 - closure"`,
  `step_range="T001-T003"`, `prior_job_ids=["f040-closure"]`,
  `num_tasks=3`,
  `note_prefix="operator-attested manual completion - F258 closure"`,
  `review_feature_id="f258"`.

WHY THESE SEVEN SUITES AND NOT THE FULL SUITE: a verification record may
NEVER carry a full-suite node-id list. `len(node_ids) == selected` forbids
filtering the list, and the packaging metadata scan correctly rejects the
redaction-torture parametrizations elsewhere in this repository whose ids
embed fake secrets and absolute paths by design (the F080 R4 lesson (d)).
The full-suite proof rides in the round 7 integration-gate evidence at
`.agent/gate_f258_r7/` and in the reviewer's own re-run, and nothing green
is claimed here that was not run. The reviewer has already run all seven
suites fresh (`python3 -m pytest <path> -q` and, together,
`python3 -m pytest tests/orchestration/test_self_use_*.py -q`) and measured
71 passed over the five self-use suites, matching the per-file counts
above exactly; if `--collect-only` over any of them surfaces a rejected
node id under `_unsafe_text`, STOP and hand back with the rejected
strings.

### The zip, the red control and the archive

1. Confirm the tree is clean and the branch is pushed, then build with
   `bash scripts/make_review_zip.sh --evidence-dir <the EVIDENCE_DIR
   above>`. Report `PACKAGE_STATUS`, the zip filename and its SHA-256.
2. THE RED CONTROL, which proves the pipeline can still fail honestly.
   Copy the evidence directory to a SECOND directory under `.remedy-wt/`,
   append ONE node id containing an absolute path to the first run of
   that copy's `verification_tests.json`, and build a zip from the COPY.
   It must report `PACKAGE_STATUS=BLOCKED_EVIDENCE` and
   `EVIDENCE_AUTHORITATIVE` false, AT EXIT CODE 0 — report the exit code
   beside the status to make the point that the status is the reading.
   Declare this attempt in the handback as a DELIBERATE CONTROL, per
   constraint 4. The real bundle is not touched by it.
3. Move the READY zip — not the control zip — to
   `/home/decodeux/Repos/remedy-history/zips`, which exists and holds
   previous closures' packages. Use `shutil.move`. Report the absolute
   destination path: DECISION amend0827 D1 makes it a recorded value,
   because the round that builds the package is the only actor that
   knows where it went. If that directory is unreachable from this
   sandbox, say so explicitly and record `NOT ARCHIVED` instead of
   guessing.
4. Leave the control zip where it was built and say so; do not delete
   anything by glob, and name any path you do remove exactly.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a
and again before the zip build; report both answers. If it exists at
either reading, finish the commit in hand, write the handback and stop.
Report constraint 0's three readings and `git status --porcelain | wc -l`
after each of C0a, C0b, C1 and C2, and again immediately BEFORE the zip
build, where it must be 0.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of
the committed blob `git show <C0a>:.agent/authored/f258-r11.md` and of the
reviewer's own original at `.remedy-wt/f258-r11/block.md`, and whether
they are EQUAL. Then report that
`git rev-parse <C0b>:.agent/authored/f258-r11.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF258R11 including the
trailing newline — report `True` or `False`, with the byte length of each
side. Report `wc -l`, under 50, and the count of lines exactly `## Goal`
and exactly `## Next Steps`.

G4 THE RECORD APPEND AT C2. Reconstruct the C2 blob of
`.agent/live_review.md` from the `3d2ab8b5` blob plus GATEF258R10 under
constraint 6, and report `True` or `False` with all three lengths.
NEGATIVE CONTROL: flip one byte at an offset your script CONFIRMS lies
inside the appended text, recompute, and report the equality is now
`False`. Report that the pre-round blob is a byte PREFIX, with both
lengths, and that the C2 blob ends in exactly ONE newline.

G5 THE LEDGER AT C2, counted under constraint 7. Report over
`.agent/live_review.md` at `3d2ab8b5` and again at C2: the count of lines
matching `^- R-\d+ — ` and whether all are DISTINCT; the count of
`^Done: R-\d+` lines AND the count of DISTINCT ids among them, as two
separate numbers; the count of `^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered UNMOVED at
318 and all distinct, the `Done:` numbers UNMOVED, `Gate:` count up by
one, and the open set UNMOVED at 263. Report the count of
`^Gate: F258 R10 — ` at C2, which must be 1.

G6 THE EVIDENCE BUNDLE. (a) Report the unified diff between the template
slice `EVIDENCESCRIPT` and your adapted `.remedy-wt/f258_evidence.py`, and
the count of changed lines: ONLY the values the section above lists may
differ, and the handback names each changed line. (b) Report, per
verification run, `run_id`, `selected`, `len(node_ids)`, whether
`len(node_ids) == selected`, `passed`, `failed`, `skipped`, `deselected`,
and `test_files` with whether that list is SORTED — an unsorted list is
rejected by `_vt_safe_files` and packages BLOCKED_EVIDENCE. Expected
passes: 23, 18, 20, 7, 3, 295, 42, with failed and skipped 0 and
deselected 0 everywhere. (c) Report the `_unsafe_text` pre-scan result
over every node id and every command — expected 0 rejected — BESIDE its
red control on a fabricated absolute-path id, which must read True; a
scanner that rejects nothing proves nothing. (d) Report the full list of
gate files the producer wrote into the evidence directory, and confirm
all eight closed-schema gates are present: `final_verifier_report`,
`fresh_evidence`, `artifact_contract`, `change_provenance`,
`manifest_integrity`, `postmortem_integrity`, `commit_execution` and
`runtime_integration`. (e) Report, per run, whether `output_hash` equals
sha256 of `stdout_summary` EXACTLY.

G7 THE REVIEW ZIP, read under constraint 8. (a) Report the zip filename,
its SHA-256, the REAL exit code of the build, and `PACKAGE_STATUS`, which
must be `READY_FOR_REVIEW`. (b) From `.review_zip_manifest.json` report
`package_status`, `ready_gate_matrix.ok`, `blocking_reasons` — expected
empty — and `committed_review_subject.head_commit`, which must equal C2's
FULL sha; report C2's full sha beside it. (c) THE RED CONTROL: report the
control build's `PACKAGE_STATUS`, which must be `BLOCKED_EVIDENCE`, its
`EVIDENCE_AUTHORITATIVE` value, which must be false, and its REAL exit
code, which is expected to be 0 — state plainly that the exit code did not
distinguish the two builds and the status did. (d) Report the absolute
path the READY zip was moved to (or `NOT ARCHIVED` per the fallback above)
and confirm the file exists there afterwards, with its size in bytes. (e)
Report `git status --porcelain | wc -l` after all of it, which must be 0
— both artifacts are gitignored and neither may dirty the tree.

G8 STRUCTURE AND THE REMAINING PRECONDITIONS, over `3d2ab8b5..<C2>` for
the range readings. The change set lists `.agent/handoff.md`, which C3
writes AFTER this range ends, so compute the changeset-minus-range
residue over the change set WITHOUT that ONE path and name the path you
excluded; the range-minus-changeset residue is computed against the FULL
change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1 and C2
is single-parent. Report the number of lines beginning `<<<SLICE ` and
`<<<END ` in `.agent/plan.md` and `.agent/live_review.md` at C2 — each
expected 0 — beside the same counts over `.agent/authored/f258-r11.md` as
the non-zero control. Report `git ls-files .remedy-wt | wc -l`, expected
0, and `git ls-files | grep -c remedy-job-evidence`, expected 0 — the
evidence dir is not committed. Report the `git diff --numstat` line over
the range for `docs/roadmap/STATUS.md`, `README.md`,
`scripts/self_use_queue.json` and `docs/roadmap/features/T5_F258.md`, all
four expected ABSENT. Finally, PRECONDITION 3: run
`from packages.orchestration.integrity_gate import run_integrity_checks`
and report `result.passed` and `result.fail_count` — it answers an
`IntegrityGateResult` OBJECT with attributes, not a dict.

### Handback

Rewrite `.agent/handoff.md` in C3 per docs/agents/handback_template.md.
It carries: `SESSION 3 of feature F258 · round 11`; the roster of this
session's rounds, this round included; the range `3d2ab8b5..HEAD`; a
per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat`; ONE LINE PER GATE G1 through G8 with its real
result; the deviations, including every guard re-expression constraint 5
required; the item-status table with every C-item and every gate
appearing exactly once; the open-findings count, which must be 263; and
the next expected action — the closure commit and the pull request.

It ALSO carries, as the values the next round needs and cannot re-derive:
`Evidence job f258-closure`, the package filename, its SHA-256, the
absolute archived path (or `NOT ARCHIVED`), and the ACCEPTED HEAD, which
is C2's full sha. Write them as a short labelled list, because the next
round's STATUS line is authored from them and `.agent/handoff.md` is the
only carrier between the two.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere —
GATEF258R10 is reviewer-authored text you apply verbatim, and any OTHER
such paragraph is a finding however hedged. Do not flip any `[ ]` or
`[~]` to `[x]` anywhere. Do not create a pull request and do not merge
anything.

After C3: push with `git push origin feature/f258-self-use-v2` and report
the outcome.
