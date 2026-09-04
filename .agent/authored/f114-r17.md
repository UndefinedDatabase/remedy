── STEP CLOSURE ALGORITHM 1-2 (EVIDENCE + ZIP) / ROUND 17 — F114 Cost preview per command ──

FEATURE F114 — Cost preview per command (Tier 3) — SESSION 4, ROUND 17

Goal
  Book round 16's PASS verdict into the ledger (RECORD16 — precondition
  3 confirmed, all six closure preconditions now hold), then build
  F114's evidence bundle and review zip — algorithm steps 1-2 of
  docs/roadmap/STATUS_closure_protocol.md. This round does NOT close
  the feature: no `[x]`, no README sync, no `consumed_by` edit, no pull
  request.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r17.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD16 to .agent/live_review.md (append) and PLAN17 to
      .agent/plan.md (whole-file replacement)
  then PUSH, and build the evidence bundle and the zip from the clean
      tree at C1 (neither is committed — both are gitignored)
  C2  rewrite .agent/handoff.md — the handback

Change set — EXACTLY these paths and nothing else
  .agent/authored/f114-r17.md (new, C0a) — .agent/last_block.md (C0b) —
  .agent/live_review.md (C1) — .agent/plan.md (C1) — .agent/handoff.md
  (C2)

THE EVIDENCE DIRECTORY IS NEVER COMMITTED and neither is the zip; both
are gitignored, and a committed evidence dir puts evidence files into
the review subject and packages BLOCKED_EVIDENCE. NO file under
packages/, apps/, tests/, scripts/ or docs/ is edited this round.

ACCEPTED HEAD IS C1 (the last content commit before the package build).
The zip is built after C1 is pushed, so the manifest's
committed_review_subject.head_commit must equal C1's full sha. C2
writes only .agent/handoff.md and follows the READY package. Report
C1's full sha as the accepted HEAD; the next round's STATUS line
carries it.

Constraints
  1. Every authored slice (RECORD16, PLAN17) is applied BYTE FOR BYTE:
     extract it by delimiter index from the COMMITTED
     .agent/authored/f114-r17.md — marker lines EXCLUDED.
  2. C1 is the first substantive commit of the round.
  3. RECORD16 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. PLAN17 REPLACES .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD16 and PLAN17 both carry NO trailing
     newline of their own.
  5. Read .agent/STOP from disk before the first commit, again before
     the zip build, and again before C2. If it exists at any of these,
     finish the commit in hand, write the handback, and stop.
  6. Shell forms rejected by this session's sandbox are RE-EXPRESSED,
     never skipped: loops, `$( )` inside a compound, `cp`, environment-
     variable assignment in any form. Route scratch work through
     `.remedy-wt/` (gitignored), copy with
     `python3 -c "import shutil; shutil.copyfile(a, b)"`, and capture
     real exit codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or via
     `subprocess`. Report every re-expression.
  7. THE OPEN SET IS COUNTED BY DISTINCT ID as
     `len(set(registered) - set(resolved))`. This round registers no
     finding id and resolves none: report the registered count and the
     open count BEFORE C1 and AFTER C1 and confirm both are UNCHANGED
     (354 registered, 278 open).
  8. EXIT CODE 0 IS NEVER THE READING FOR THE ZIP.
     `scripts/make_review_zip.sh` exits 0 for a BLOCKED_EVIDENCE package
     as readily as for a READY one. The reading is `PACKAGE_STATUS` in
     the printed output and `package_status` in
     `.review_zip_manifest.json`.
  9. This is F114's FIRST package — there is no prior F114 package to
     call superseded. Do not delete anything already present under
     `/home/decodeux/Repos/remedy-history/zips`.

The authored slices

<<<BEGIN RECORD16>>>
Gate: F114 R16 — the round 16 entry, closure precondition 3's first run for this feature, no code changes. VERDICT PASS, over the range `90b2960dc4fe0e4a1920bf7519217f250b25e134..eeeee7c6f0368e38dd0891d92b49cecbd42c9ef0` (commits C0a `26fe0a2283d1d03a761cc9ceb7770638aae54c4d`, C0b `f62b72e5c81872c949390cf73566f2e6828fea31`, C1 `3f9fe7f2ebe92fba201a3dbfa4292f79ebdead15` — three real content commits — plus handback commit `eeeee7c6f0368e38dd0891d92b49cecbd42c9ef0`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r16.md .agent/last_block.md` both print `f8b913d4566610efeb4328597bd94268658bae1d26139d846fe815c9a729ed06`, reproduced directly. G2 THE LEDGER APPEND (RECORD15) HELD BYTE-EXACT: base 2402882 bytes (no trailing newline), RECORD15 measured 2613 bytes with zero internal newlines, base + 1 + 2613 = 2405496 exactly matching the post-C1 file; the appended tail equals `\n` + RECORD15 byte for byte, a one-byte-flipped negative control was correctly rejected. G3 THE PLAN HELD BYTE-EXACT: PLAN16 extracted from the committed authored file compares equal to `.agent/plan.md` (32 lines by `wc -l`; `## Goal`/`## Next Steps` each exactly once). G4 PRECONDITION 3 HELD, REPRODUCED INDEPENDENTLY: `remedy integrity check --json` was denied by the sandbox with the literal text "This command requires approval", so `python3 -m apps.cli.grouped integrity check --json` was run instead — the exact module the `remedy` console script maps to per `pyproject.toml`'s `[project.scripts]` — and the reviewer re-ran the same command directly, getting the same reading both times: `"passed": true`, `"fail_count": 0`, `"check_count": 5`, and `high_blockers_open` reading "no open blocker/high findings". PRECONDITION 3 IS CONFIRMED. G5 THE FOUR STATE READERS AND THE CANARY HELD, REPRODUCED INDEPENDENTLY, ALL FIVE COUNTS IDENTICAL TO EVERY EARLIER ROUND'S OWN BASELINE THIS SESSION: `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42. G6 THE TREE AND THE SWEEP HELD: `git status --porcelain` and `git diff --stat 90b2960d..eeeee7c6 -- packages/ apps/ tests/` are both empty, reproduced independently; every commit's numstat cells match the handback's own Commits table cell for cell (C0a 156/0 `.agent/authored/f114-r16.md`, C0b 105/90 `.agent/last_block.md`, C1 2/1 `.agent/live_review.md` and 13/18 `.agent/plan.md`). ONE DEVIATION WAS DECLARED BY THE ROUND (`cmp` denied by the sandbox, a Python byte-equality read substituted to the same effect) — not a defect on disk. Open findings recount confirmed the round's own figure unchanged: 354 registered R-ids minus 76 `Done:` lines equals 278 open, matching the handback exactly; `.agent/candidates.md` remains EMPTY. ALL SIX CLOSURE PRECONDITIONS FOR F114 NOW HOLD: 1 and 2 (established round 11), 3 (this round, confirmed), 4 (round 14), 5 (clean tree, pushed — `git fetch` plus `git rev-parse HEAD origin/feature/f114-cost-preview-per-command` both equal `eeeee7c6f0368e38dd0891d92b49cecbd42c9ef0`) and 6 (round 13). The next round begins the closure sequence proper: the evidence job and the review zip (algorithm steps 1-2 of `docs/roadmap/STATUS_closure_protocol.md`).
<<<END RECORD16>>>

<<<BEGIN PLAN17>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 17 books round 16's PASS verdict (RECORD16 — precondition 3
confirmed, all six closure preconditions now hold) into the ledger,
then builds the evidence job and the review zip — algorithm steps 1-2
of docs/roadmap/STATUS_closure_protocol.md. No `[x]` flip, no README
sync, no `consumed_by` edit, no pull request this round.

## Next Steps

- The closure commit itself, in ONE commit: the `[x]` flip on
  docs/roadmap/STATUS.md, the README capability sync,
  `scripts/self_use_queue.json`'s `consumed_by=F114` edit and the
  final `.agent/` state.
- Open the pull request. Not merged this session — the operator's
  manual-review window; the next feature's Open PR Gate merges it.

## Risks

- The evidence directory and the zip are gitignored and NEVER
  committed; only `.agent/**` changes land in git this round.
- `remedy-review-*.zip` files write directly under
  `/home/decodeux/Repos/remedy-history/zips`; nothing there is
  deleted.
<<<END PLAN17>>>

RECORD16 is a SINGLE APPEND to .agent/live_review.md at C1. PLAN17 is a
WHOLE-FILE replacement of .agent/plan.md at C1. This round registers
nothing and resolves nothing.

The evidence script — ADAPTED FROM THE COMMITTED TEMPLATE, NOT WRITTEN
FRESH

Extract the slice named EVIDENCESCRIPT from the COMMITTED blob
`git show HEAD:.agent/authored/f009-r33.md` by its `<<<SLICE
EVIDENCESCRIPT` and `<<<END EVIDENCESCRIPT` marker lines, save it to
`.remedy-wt/f114_evidence_r17.py`, and change ONLY the values below.
Every other line stays BYTE FOR BYTE — the double path scrub in
`_tail`, node ids from `--collect-only`, the `len(node_ids) ==
selected` assert, the sorted `test_files`, the `_unsafe_text` pre-scan
with its red control and the `OUTPUT_HASH` re-derivation are all
load-bearing.

  - `EVIDENCE_DIR` → `<REPO>/.remedy-wt/f114_closure_evidence/remedy-job-evidence-f114-closure`.
  - `BASE` → `a1b5d4bb455550f082da7d6c4c80fd968d6e1a88` (the merge base
    with `main`, confirmed 40 characters and an ancestor of HEAD — the
    template asserts the length).
  - the `runs = [...]` list → exactly these five, in this order, no
    `-k` and no deselection:
    - `mkrun("vr-0001", "tests/orchestration/test_cost_preview.py", 19)`
    - `mkrun("vr-0002", "tests/cli/test_cost_preview_confirm.py", 12)`
    - `mkrun("vr-0003", "tests/cli/test_cost_preview.py", 5)`
    - `mkrun("vr-0004", "tests/test_command_catalog.py::TestCatalogExpensive", 4)`
    - `mkrun("vr-0005", "tests/docs/test_docs_consistency.py", 295)`
  - the `create_manual_completion_bundle(...)` keyword arguments:
    `job_id="f114-closure"`, `job_title="F114 Cost preview per command -
    closure"`, `step_range="T001-T003"`,
    `prior_job_ids=["79b21c8cba8b4352"]` (F112's own evidence job id —
    F112 is the immediately preceding closed feature, `docs/roadmap/
    STATUS.md` line for F112), `num_tasks=3`,
    `note_prefix="operator-attested manual completion - F114 closure"`,
    `review_feature_id="f114"`.

`HEAD` is computed by the template at run time and must come out as
C1's full sha; report it. A verification record may NEVER carry a
full-suite node-id list.

The zip and the red control

  1. Confirm the tree is clean and the branch is pushed, then build
     with `bash scripts/make_review_zip.sh --evidence-dir <the
     EVIDENCE_DIR above>`. Report `PACKAGE_STATUS`, the zip filename
     and its SHA-256 computed by you over the file on disk (not merely
     copied from the script's output).
  2. THE RED CONTROL. Copy the evidence directory to a SECOND directory
     under `.remedy-wt/`, append ONE node id containing an absolute
     path to the first run of that copy's `verification_tests.json`,
     and build a zip from the COPY. It must report
     `PACKAGE_STATUS=BLOCKED_EVIDENCE` at REAL exit code 0 — report the
     exit code beside the status, and report the
     `ready_gate_matrix.blocking_reasons` list from the control's
     manifest, untruncated. Declare this as a DELIBERATE CONTROL. The
     real bundle is not touched by it.
  3. The script writes into `/home/decodeux/Repos/remedy-history/zips`
     directly. If the READY zip is already there when the build
     finishes, say so; if not, move it there with `shutil.move`. Report
     the absolute path the live package occupies and confirm the file
     exists there.

Done when — the gates. Run each, record the REAL exit code and the REAL
output.

  G1 HYGIENE. Read `.agent/STOP` with `os.path.exists` before C0a,
     again before the zip build, and again before C2; report all three
     answers. Report `git status --porcelain | wc -l` after each of
     C0a, C0b and C1, and again immediately BEFORE the zip build, where
     it must be 0.
  G2 TRANSPORT. `sha256sum .agent/authored/f114-r17.md
     .agent/last_block.md` — one digest, twice. Report both lines
     verbatim.
  G3 THE PLAN AT C1. `.agent/plan.md` equals PLAN17 byte for byte
     (report byte lengths of each side and the boolean); `wc -l`
     (expect under 50); `grep -c '^## Goal'` and `grep -c '^## Next
     Steps'` (each expect 1).
  G4 THE RECORD APPEND (RECORD16). Base size of .agent/live_review.md
     immediately BEFORE C1 (expect 2405496, no trailing newline);
     RECORD16's own byte length (report it); base + 1 + RECORD16's
     length, and whether it equals the post-C1 file's byte length.
     Second reader: post-C1 bytes from `base` to end equal exactly
     "\n" + RECORD16. Negative control in a scratch copy: flip one byte
     inside RECORD16's own text, confirm the second reader REJECTS it.
  G5 THE LEDGER, per constraint 7: registered count and open count
     BEFORE C1 and AFTER C1, confirming both UNCHANGED (354 / 278).
  G6 THE EVIDENCE BUNDLE. (a) Unified diff between the template slice
     EVIDENCESCRIPT and your adapted `.remedy-wt/f114_evidence_r17.py`
     — ONLY the values listed above may differ; name each changed
     line. (b) Per verification run: run_id, selected, len(node_ids),
     whether they're equal, passed/failed/skipped/deselected, and
     whether test_files is sorted. Expected passes: 19, 12, 5, 4, 295,
     with failed/skipped/deselected 0 everywhere. (c) The
     `_unsafe_text` pre-scan result over every node id and command
     (expect 0 rejected) beside its red control on a fabricated
     absolute-path id (expect True). (d) The full list of files the
     producer wrote into the evidence directory; confirm all eight
     closed-schema gates are present: final_verifier_report,
     fresh_evidence, artifact_contract, change_provenance,
     manifest_integrity, postmortem_integrity, commit_execution,
     runtime_integration. (e) Per run, whether output_hash equals
     sha256 of stdout_summary exactly. (f) The HEAD the template
     computed; confirm it equals C1's full sha.
  G7 THE REVIEW ZIP, read under constraint 8. (a) Zip filename, its
     SHA-256 computed by you over the file on disk, the REAL exit code
     of the build, and PACKAGE_STATUS (must be READY_FOR_REVIEW). (b)
     From `.review_zip_manifest.json` inside the zip: package_status,
     ready_gate_matrix.ok, ready_gate_matrix.blocking_reasons (expect
     empty), committed_review_subject.head_commit (must equal C1's
     full sha — report C1's sha beside it), and
     committed_review_subject.base_commit (must equal
     a1b5d4bb455550f082da7d6c4c80fd968d6e1a88). (c) THE RED CONTROL:
     the control build's PACKAGE_STATUS (must be BLOCKED_EVIDENCE), its
     REAL exit code (expect 0), and its untruncated
     ready_gate_matrix.blocking_reasons. (d) The absolute path the LIVE
     package occupies, that the file exists there, and its size in
     bytes. (e) `git status --porcelain | wc -l` after all of it (must
     be 0).
  G8 STRUCTURE AND PRECONDITION 3, over the round's own starting
     HEAD..C1. Report each commit's insertions from `git diff
     --numstat` (each under 500) and that each of C0a, C0b and C1 is
     single-parent. Report `git ls-files .remedy-wt | wc -l` (expect
     0) and the count of tracked paths matching `remedy-job-evidence`
     (expect 0). Report the `git diff --numstat` line over the range
     for `docs/roadmap/STATUS.md`, `README.md`, and
     `scripts/self_use_queue.json` — all three expected ABSENT.
     Finally, re-run `python3 -m apps.cli.grouped integrity check
     --json` (or `remedy integrity check --json` if it is not denied)
     and report `passed`/`fail_count`/`high_blockers_open` once more —
     it must still read the same as round 16's reading.