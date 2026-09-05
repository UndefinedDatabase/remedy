STEP CLOSURE ALGORITHM 1-2 (EVIDENCE + ZIP) / ROUND 27 - F262 List commands v2 (dates, sort, filter)
FEATURE F262 - List commands v2 (dates, sort, filter) (Tier 2) - SESSION 9, ROUND 27

Goal
  Book round 26's verdict (RECORD26 - preconditions 3 and 6 confirmed,
  all six closure preconditions now hold), then build F262's
  evidence bundle and review zip - algorithm steps 1-2 of
  docs/roadmap/STATUS_closure_protocol.md. This round does NOT close the
  feature: no `[x]`, no README sync, no consumed_by edit, no pull request.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r27.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD26 to .agent/live_review.md (append) and PLAN28 to
      .agent/plan.md (whole-file replacement)
  then PUSH, and build the evidence bundle and the zip from the clean
      tree at C1 (neither is committed - both are gitignored)
  C2  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r27.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) - .agent/handoff.md (C2)

THE EVIDENCE DIRECTORY IS NEVER COMMITTED and neither is the zip; a
committed evidence dir puts evidence files into the review subject and
packages BLOCKED_EVIDENCE. NO file under packages/, apps/, tests/,
scripts/ or docs/ is edited this round.

ACCEPTED HEAD IS C1 (the last content commit before the package build).
The zip is built after C1 is pushed, so the manifest's
committed_review_subject.head_commit must equal C1's full sha. C2 writes
only .agent/handoff.md and follows the READY package. Report C1's full
sha as the accepted HEAD; the next round's STATUS line carries it.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by its
     one-line BEGIN/END markers from the COMMITTED
     .agent/authored/f262-r27.md (marker lines EXCLUDED), by a Python
     script, never retyped. If a slice looks wrong, apply it as written
     and DECLARE it.
  2. C1 is the first substantive commit of the round.
  3. RECORD26 appends to .agent/live_review.md as EXACTLY TWO newline
     bytes followed by the slice; PLAN28 REPLACES .agent/plan.md whole;
     neither carries a trailing newline.
  4. Read .agent/STOP before C0a, before the zip build and before C2; if
     present, finish the commit in hand, write the handback, stop.
  5. Sandbox forms this session refuses are RE-EXPRESSED, never skipped
     (`cp`, `cmp`, env assignment, loops, `$( )` in compounds): Python
     (`shutil`, `pathlib`, `subprocess.run`) and `bash -c '<cmd>; echo
     REAL_EXIT=$?'`. Scratch work goes under `.remedy-wt/` (gitignored);
     if naming that path in bash is refused, drive the step from a
     `python3 - <<'PY'` heredoc. Report every re-expression.
  6. THE OPEN SET, §3 item 10's line-count formula: report registered /
     Done / open BEFORE C1 and AFTER C1 and confirm both UNCHANGED at
     356 / 77 / 279 - this round registers no id and resolves none.
  7. EXIT CODE 0 IS NEVER THE READING FOR THE ZIP.
     `scripts/make_review_zip.sh` exits 0 for a BLOCKED_EVIDENCE package
     as readily as for a READY one. The reading is `PACKAGE_STATUS` in
     the printed output and `package_status` in `.review_zip_manifest.json`.
  8. This is F262's FIRST package. Delete nothing under
     `/home/decodeux/Repos/remedy-history/zips`.

The evidence script - ADAPTED FROM THE COMMITTED TEMPLATE, NOT WRITTEN
FRESH. Extract the slice named EVIDENCESCRIPT from the COMMITTED blob
`git show HEAD:.agent/authored/f009-r33.md` by its `<<<SLICE
EVIDENCESCRIPT` and `<<<END EVIDENCESCRIPT` marker lines, save it to
`.remedy-wt/f262_evidence_r27.py`, and change ONLY the values below.
Every other line stays BYTE FOR BYTE - the double path scrub in `_tail`,
node ids from `--collect-only`, the `len(node_ids) == selected` assert,
the sorted `test_files`, the `_unsafe_text` pre-scan with its red control
and the `OUTPUT_HASH` re-derivation are all load-bearing.

  - `EVIDENCE_DIR` -> `<REPO>/.remedy-wt/f262_closure_evidence/remedy-job-evidence-f262-closure`.
  - `BASE` -> `7c65d9ccfb512aef1c3eea0245030647332c26ea` (the merge base with `main`, PR 235's merge,
    confirmed by `git merge-base main HEAD`; the template asserts the
    40-character length).
  - the `runs = [...]` list -> exactly these seven, in this order, no
    `-k` and no deselection (the reviewer scanned every collected id
    with `_unsafe_text` at 0609f113: 0 rejected):
    - `mkrun("vr-0001", "tests/orchestration/test_list_options.py", 11)`
    - `mkrun("vr-0002", "tests/test_command_catalog.py::TestListCommandOptions", 3)`
    - `mkrun("vr-0003", "tests/cli/test_config_cmd.py", 16)`
    - `mkrun("vr-0004", "tests/cli/test_worker_facade_cmd.py", 70)`
    - `mkrun("vr-0005", "tests/cli/test_managed_builder_execution_cli.py", 12)`
    - `mkrun("vr-0006", "tests/cli/test_queue_cmd.py", 28)`
    - `mkrun("vr-0007", "tests/docs/test_docs_consistency.py", 295)`
  - the `create_manual_completion_bundle(...)` keyword arguments:
    `job_id="f262-closure"`, `job_title="F262 List commands v2 (dates,
    sort, filter) - closure"`, `step_range="T001-T003"`,
    `prior_job_ids=["f114-closure"]` (F114's evidence job id - the
    immediately preceding closed feature, `docs/roadmap/STATUS.md`),
    `num_tasks=3`, `note_prefix="operator-attested manual completion -
    F262 closure"`, `review_feature_id="f262"`.

`HEAD` is computed by the template at run time and must come out as
C1's full sha; report it. A verification record may NEVER carry a
full-suite node-id list.

The zip and the red control
  1. Confirm the tree is clean and the branch is pushed, then build with
     `bash scripts/make_review_zip.sh --evidence-dir <the EVIDENCE_DIR
     above>`. Report `PACKAGE_STATUS`, the zip filename and its SHA-256
     computed by you over the file on disk.
  2. THE RED CONTROL. Copy the evidence directory to a SECOND directory
     under `.remedy-wt/`, append ONE node id containing an absolute path
     to the first run of that copy's `verification_tests.json`, and build
     a zip from the COPY. It must report `PACKAGE_STATUS=BLOCKED_EVIDENCE`
     at REAL exit code 0 - report the exit code beside the status and
     the `ready_gate_matrix.blocking_reasons` list from the control's
     manifest, untruncated. Declare it as a DELIBERATE CONTROL in the
     handback, in run.txt-style plain words: the control package is NOT
     evidence about the real bundle and the two were built from
     DIFFERENT inputs (the F114 closure's control was later misread as
     non-determinism - DECISION F262 D6). The real bundle is not touched.
  3. The script writes into `/home/decodeux/Repos/remedy-history/zips`
     directly. If the READY zip is already there when the build
     finishes, say so; if not, move it there with `shutil.move`. Report
     the absolute path the live package occupies and its size in bytes.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 HYGIENE. `.agent/STOP` at each of constraint 4's reads (report
     each); `git status --porcelain | wc -l` after C0a, C0b and C1, and
     again immediately BEFORE the zip build, where it must be 0.
  G2 TRANSPORT. `sha256sum .agent/authored/f262-r27.md
     .agent/last_block.md` - one digest, twice.
  G3 THE PLAN AT C1. `.agent/plan.md` equals PLAN28 byte for byte
     (expect 1681 bytes); `wc -l` under 50 (expect 38);
     `grep -c '^## Goal'` and `grep -c '^## Next Steps'` each 1.
  G4 THE RECORD APPEND (RECORD26). Base size of .agent/live_review.md
     before C1 (expect 2503246, no trailing newline); RECORD26's byte
     length (expect 4992); base + 2 + that (expect 2508240)
     versus the post-C1 length; tail equality "\n\n" + RECORD26; negative
     control in a scratch copy (one flipped byte REJECTED).
  G5 THE LEDGER, per constraint 6: registered / Done / open BEFORE and
     AFTER C1, both UNCHANGED (356 / 77 / 279).
  G6 THE EVIDENCE BUNDLE. (a) Unified diff between the template slice
     EVIDENCESCRIPT and `.remedy-wt/f262_evidence_r27.py` - ONLY the
     values listed above may differ; name each changed line. (b) Per
     verification run: run_id, selected, len(node_ids), whether equal,
     passed/failed/skipped/deselected, whether test_files is sorted.
     Expected passes 11, 3, 16, 70, 12, 28, 295 with failed/skipped/
     deselected 0 everywhere. (c) The `_unsafe_text` pre-scan over every
     node id and command (expect 0 rejected) beside its red control on a
     fabricated absolute-path id (expect a non-empty reason). (d) The
     full list of files the producer wrote; confirm all eight closed-
     schema gates are present: final_verifier_report, fresh_evidence,
     artifact_contract, change_provenance, manifest_integrity,
     postmortem_integrity, commit_execution, runtime_integration. (e)
     Per run, output_hash equals sha256 of stdout_summary. (f) The HEAD
     the template computed equals C1's full sha.
  G7 THE REVIEW ZIP, read under constraint 7. (a) Zip filename, SHA-256
     over the file on disk, the REAL build exit code, PACKAGE_STATUS
     (must be READY_FOR_REVIEW). (b) From `.review_zip_manifest.json`
     inside the zip: package_status, ready_gate_matrix.ok,
     ready_gate_matrix.blocking_reasons (expect empty),
     committed_review_subject.head_commit (equals C1's full sha - report
     both) and committed_review_subject.base_commit (equals 7c65d9ccfb512aef1c3eea0245030647332c26ea).
     (c) THE RED CONTROL: PACKAGE_STATUS (must be BLOCKED_EVIDENCE), REAL
     exit code (expect 0), untruncated blocking_reasons. (d) The absolute
     path the LIVE package occupies, that it exists, its size in bytes.
     (e) `git status --porcelain | wc -l` after all of it (must be 0).
  G8 STRUCTURE. Per-commit `git show --numstat --format=""` for C0a, C0b
     and C1 against this handback's Commits table; each single-parent
     and under 500 insertions; `git ls-files .remedy-wt | wc -l` 0;
     tracked paths matching `remedy-job-evidence` 0; `git diff --numstat
     0609f113..<C1> -- docs/roadmap/STATUS.md README.md scripts/self_use_queue.json`
     empty; re-run `python3 -m apps.cli.grouped integrity check --json`
     and report passed / fail_count / high_blockers_open (expect the
     round-26 reading unchanged).

SLICES. Each lies between its own one-line BEGIN and END marker; the
slice is the bytes between the BEGIN marker's newline and the newline
before the END marker, EXCLUDING that final newline.

<<<BEGIN RECORD26>>>
Gate: R26 — the F262 R26 entry, closure preconditions 6 and 3 of `docs/roadmap/STATUS_closure_protocol.md`, no production code touched. VERDICT PASS over the range `60f48fb6..0609f113` (C0a `d08493a2`, C0b `008ec51f`, C1 `bb8353ef`, C2 `79a73b5a`, C3 `47730045`, handback `0609f113`), independently re-verified by the reviewer. TRANSPORT HELD IN ITS PRIMARY FORM: scratch original, committed `.agent/authored/f262-r26.md` and `.agent/last_block.md` equal byte for byte, sha256 `24ea07da85dce005574c1d40a4f95352de8a6a7c0b2dcaa9e40316610c4b1d31`, 15480 bytes. THE LEDGER APPEND (RECORD25) HELD: 2498900 (at `008ec51f`) plus two newlines plus RECORD25 (4344 bytes) equals 2503246 (at `bb8353ef`), tail equal, the worker's flipped-byte control rejected. THE PLAN HELD: `.agent/plan.md` equals PLAN27 (1979 bytes, 41 lines by `wc -l`, `## Goal` and `## Next Steps` once each). PRECONDITION 6 IS SATISFIED, REPRODUCED FROM THE PERSISTED ARTEFACTS: the queue held eight items, all consumed, and `next_self_use_item()` answered `None`, so `generate_and_append_if_empty()` was called once with no arguments and appended `SU-009` — title "Address ledger finding R-0418", provenance `generated (self-use-generator tier 1, ledger scan, R-0418)`, `consumed_by` empty — as a clean `+8/-0` append to `scripts/self_use_queue.json` (reproduced by `git show --numstat 79a73b5a`; the open `R-0785` full-rewrite class did not show, for the reason RECORD12 of F114 already gave: every earlier item was re-serialised byte-identically once before). `run_next_self_use_item(Path(".remedy-wt/selfuse-f262-run"))` then ran it UNFLAGGED, role resolution picking the real default provider `ollama` for builder and reviewer (models blank with source `default`, i.e. `muse-glimmer:latest`), budgets `max_provider_calls=6`, `max_cost_usd=0.50`, `max_tasks=1`: job `21c19578b8754287` ended `blocked` at the normal approval gate — `T001` `final_status=repair_exhausted`, `reviewer_verdict=fail`, two repair rounds used — never promoted, which is the gate working. `describe_self_use_run_defects(plan)` returns exactly two strings, reproduced by the reviewer from the persisted `JobPlan` via `load_job_plan("21c19578b8754287")`: `job 21c19578b8754287 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. REGISTRATION OBLIGATION DISCHARGED WITHOUT A NEW ID, per §3 checklist item 30: both strings are the identical defect class the OPEN finding `R-0784` already registers — the tier-1 generator picking `R-0418`, a reviewer-practice rule no builder can repair in code, and the approval gate correctly refusing the unfinished job — the fifth consecutive run of that pick (SU-005 through SU-009) to end this way; this entry ADDS that run as evidence to `R-0784` rather than minting a second id, exactly as RECORD13 of F114 did for SU-008. Evidence is committed at `47730045`: `.agent/selfuse_f262/SU-009.md` (1541 bytes, sha256 equal to the plan's own `job_file_sha256`, reproduced) and `.agent/selfuse_f262/run.txt` (5598 bytes). The job's own retained worktree is `.remedy-wt/job-21c19578b8754287/`, untouched. PRECONDITION 3 IS CONFIRMED, REPRODUCED: `python3 -m apps.cli.grouped integrity check --json` (the module `pyproject.toml` maps the denied `remedy` console script to) reads `"passed": true`, `"fail_count": 0`, `"check_count": 5`, `high_blockers_open` "no open blocker/high findings". ONE DEVIATION WAS DECLARED AND IS ACCEPTED AS HARMLESS: the worker's reporter crashed after the run returned (it read `.id` on a `TaskEntry` that carries `task_id`), so the run's fields were read back from the persisted plan rather than the live return value and the wall time is a 136.97 s bracket between `plan.created_at` and the final `job.json` mtime instead of a `time.time()` reading; the run was correctly NOT repeated. A second declared deviation — a `cd <repo>` prefix on two compound commands, unrefused — changed nothing on disk. THE TREE HELD: `git status --porcelain` and `git ls-files .remedy-wt` empty, `.agent/STOP` absent, `git diff --stat 60f48fb6..47730045 -- packages/ apps/ tests/ docs/` empty, every numstat cell matching the handback's Commits table (201/0, 156/177, 3/1 + 21/22, 8/0, 7/0 + 96/0), all commits single-parent and under 500 insertions, head equal to `origin/feature/f262-list-commands-v2`. Open findings, canonical line-count formula: 356 registered minus 77 `Done:` lines equals 279 open, unchanged; `.agent/candidates.md` remains EMPTY. ALL SIX CLOSURE PRECONDITIONS FOR F262 NOW HOLD: 1 (every round PASS), 2 (integration gate clean, round 25), 3 (this round), 4 (Built State, round 24), 5 (clean, pushed), 6 (SU-009 generated, run to the gate, its defects registered as `R-0784` evidence; its `consumed_by` becomes `F262` in the closure commit). The next round is algorithm steps 1-2: the evidence job `f262-closure` and the review zip.
<<<END RECORD26>>>

<<<BEGIN PLAN28>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4; the nine
remaining wirings are F267's per DECISION F262 D5).

## Current Step

Round 27, session 9 — closure algorithm steps 1-2 of
docs/roadmap/STATUS_closure_protocol.md: book round 26 (all six closure
preconditions now hold), then build the evidence bundle (job
`f262-closure`, seven scoped verification runs, EVIDENCESCRIPT template
from `.agent/authored/f009-r33.md`) and the fresh review zip with its
red control, from the clean tree at C1. No `[x]` flip, no README sync,
no `consumed_by` edit, no pull request this round.

## Next Steps

- The closure commit, in ONE commit: STATUS `[x]` line (reviewer-authored,
  carrying the package name, SHA-256, archived path and accepted HEAD =
  this round's C1), README numerals (accepted count, Tier 2 Done cell)
  plus the F262 capability paragraph, `consumed_by=F262` on SU-009.
- Open the pull request; merge under the operator's 2026-09-05
  authorization once hosted CI reads green (checks read as their own
  command first).

## Risks

- The evidence directory and the zip are gitignored and NEVER
  committed; only `.agent/**` changes land in git this round.
- `remedy-review-*.zip` files write under
  `/home/decodeux/Repos/remedy-history/zips`; nothing there is deleted.
<<<END PLAN28>>>

Handback: write .agent/handoff.md per docs/agents/handback_template.md
and AGENTS.md - Session line `SESSION 9 of feature F262 · round 27 ·
rounds so far 27` with one sentence of context self-assessment, Range
`Review of 0609f113..<C1>`, one changed-files table per commit (C0a, C0b,
C1; C2 grouped per the self-reference exception), an item-status table
over C0a..C2 and G1..G8, External actions (the push, both zip builds,
the archive move), raw Verification per gate, Authored-text proofs,
Deviations, and Next: "the closure commit (STATUS line, README sync,
consumed_by=F262) and the pull request". Record the package name, its
SHA-256, its archived path and the accepted HEAD prominently.
