STEP T001 (carry-over 1, batch 2 and its test) — F275 One world completion, part three — ROUND 2

Goal:
  Book round 1's PASS verdict and its four reviewer-prose slips, then COMPLETE the first
  carry-over's code move — the second and last staged batch of
  `packages/orchestration/mission_readiness.py` — and land the test file named after it. The
  module is STILL UNWIRED in production when this round ends.

Read first: AGENTS.md · docs/agents/self_drive_protocol.md · docs/roadmap/features/T2_F275.md ·
DECISION F275 D1 in `.agent/decisions.md`, which round 1 landed and which rules this move.

ENVIRONMENT, the same list round 1 carried; none of it has changed:
  - `VAR=x cmd`, `env VAR=x cmd` and `export VAR=x; cmd` are ALL DENIED. Set env in-process.
  - `cp` is DENIED. Copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`.
  - Bare `ruff` is DENIED. Use `python3 -m ruff check <path>`.
  - Wrap a gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. NEVER pipe into `tail` when you need
    the exit code — the pipe reports tail's status. Redirect to a file and read it.
  - Shell loops, `$(...)` in a compound and `$?` in a compound are refused by FORM. Use
    `python3 - <<'PY'` heredocs; if the guard rejects one, write the script to a file under
    `.remedy-wt/` and run `python3 <file>`. The guard also rejects an f-string containing a
    backslash and some brace-and-quote combinations, so prefer plain `%` formatting in probes.
  - Commit subjects carry no leading-slash token, no absolute path and no secret-like string.

Bundle, in this exact commit order. There is no commit after C6.
  C0a  Save THIS ENTIRE BLOCK verbatim as `.agent/authored/f275-r2.md`, copied with
       `shutil.copyfile` from the file the delegating message names. Never retype it.
  C0b  Mirror the same bytes into `.agent/last_block.md` with `shutil.copyfile`.
  C1   Replace `.agent/plan.md` with the PLAN2 slice, byte for byte.
  C2   The record, in ONE commit: append the RECORD2 slice to `.agent/live_review.md` and the
       SLIPS2 slice to `.agent/prose_slips.md`. This is the round's FIRST substantive commit
       after the plan, because it books a verdict that until now exists only in a handback.
  C3   Append batch 2 to `packages/orchestration/mission_readiness.py` per SPEC A.
  C4   Create `tests/orchestration/test_mission_readiness.py` per SPEC B.
  C5   Run every gate G1 to G8 and record its REAL exit code and REAL output. C5 writes no file.
  C6   Rewrite `.agent/handoff.md` as the handback. It quotes all eight gates, which is why they
       run at C5, strictly before this commit. G8's `git log` clause is the one reading that can
       only be completed after C6 exists; take it again after C6 and say so, as round 1 did.

Change set — exactly these paths, and nothing else:
  .agent/authored/f275-r2.md · .agent/last_block.md · .agent/plan.md · .agent/live_review.md ·
  .agent/prose_slips.md · packages/orchestration/mission_readiness.py ·
  tests/orchestration/test_mission_readiness.py · .agent/handoff.md
  NOTHING under `docs/` changes this round, so no docs gate is ordered.

Constraints:
  1. Apply every slice BYTE FOR BYTE. Extract each as the bytes strictly between its
     `BEGIN <NAME>` line and its `END <NAME>` line, verify the extracted bytes against that
     BEGIN line's own sha256 and byte count BEFORE applying, and never let a marker line reach
     any file. Every slice in this block carries both values; round 1's P1 markers did not, and
     that is one of the four slips this round books. Do not edit a slice: if one is wrong, apply
     it as given and declare it.
  2. APPEND CONVENTION, and it is stated as arithmetic because round 1's was not.
     `.agent/live_review.md` and `.agent/prose_slips.md` each end with exactly one newline, and
     each slice ends with its own newline. An append writes ONE newline and then the slice, so
     the file grows by exactly 1 + the slice's byte count. Both predicted totals in G3 are
     computed that way; if your measurement disagrees with the prediction, stop and report.
  3. C3 APPENDS to the existing module and rewrites none of it: the bytes of
     `packages/orchestration/mission_readiness.py` at the base of this round are a byte-exact
     PREFIX of the file after C3.
  4. `packages/orchestration/overnight_readiness.py` IS NOT TOUCHED, and neither is
     `tests/orchestration/cluster_deletion_map.txt` or
     `tests/orchestration/import_reachability_allowlist.txt`. This round cuts no edge and
     deletes nothing; it only adds.
  5. NOTHING UNDER `packages/` OR `apps/` IMPORTS THE NEW MODULE when this round ends. The only
     file in the repository that may import it is the new test.
  6. Run the suites SERIALLY, one command per call.
  7. Nothing destructive runs in the primary checkout. Probe scripts and their temporary data
     roots live under the gitignored `.remedy-wt/`; remove what you create there by EXACT PATH.
  8. Never force-push. Never merge. Push with
     `git push -u origin feature/f275-one-world-completion-part-three`. Do NOT create a pull
     request: under docs/roadmap/STATUS_closure_protocol.md the closure sequence creates it.

SPEC A for C3 — complete `packages/orchestration/mission_readiness.py`, batch 2 of 2, UNWIRED.
  Parse `packages/orchestration/overnight_readiness.py` with `ast` and APPEND, BYTE-IDENTICALLY,
  the source span of each of these TWELVE top-level definitions, in this order, which is their
  source order:
      _build_risks, _integrity_status, _ci, _build_checklist, select_overnight_next_action,
      _build_stop_reasons, build_overnight_readiness, _policy_summary, build_overnight_report,
      export_readiness_json, _CHECK_ICON, render_overnight_report_markdown
  A definition's span STARTS AT ITS FIRST DECORATOR where it has one, exactly as in round 1.
  Separate the appended definitions from each other and from the existing tail by two blank
  lines, which is the convention the file already uses and what `python3 -m ruff check` requires.
  Add NO import: the reviewer verified that the twelve carry no name the module's existing
  import block does not already provide.
  STILL DELIBERATELY EXCLUDED, and this completes the carried set at twenty-nine definitions:
  `OvernightEvidenceStatus`, `_CAP_UNKNOWN`, `OvernightRunPlan`, `build_overnight_plan` and
  `export_plan_json`. The last three are the plan path, which dies with the cluster; the first
  two are reachable from nothing. DECISION F275 D1 carries the measurement.
  RENAME NOTHING.

SPEC B for C4 — `tests/orchestration/test_mission_readiness.py`.
  It is `tests/orchestration/test_overnight_readiness.py` MIRRORED onto the carried module, and
  it is written so that it survives the deletion of the original. Take the existing file as the
  starting point and make exactly these changes:
    (a) Import `from packages.orchestration import mission_readiness as OV` in place of the
        `overnight_readiness` import. Every other import, the `env` fixture and the `_job` and
        `_add_failure` helpers carry over unchanged.
    (b) DROP the whole of `class TestPlan` — both of its tests — because
        `build_overnight_plan` is not carried. This is the only class that disappears.
    (c) In `TestRedaction.test_no_raw_leak`, DROP the one blob built from
        `export_plan_json(build_overnight_plan(...))` and keep the other two. The assertions
        beneath it are unchanged and still run over both surviving blobs.
    (d) In `TestArchitectureGuards`, re-point `SRC` to
        `Path("packages/orchestration/mission_readiness.py").read_text()`. All six guard tests
        carry over unchanged — they are the read-only, no-execution guarantees of this code and
        they must follow it to its new home.
    (e) Give the module a docstring naming the carry-over and DECISION F275 D1.
  That leaves TWENTY tests: 2 in `TestPolicy`, 11 in `TestReadinessTruth`, 1 in `TestRedaction`
  and 6 in `TestArchitectureGuards`. Report the number pytest collects rather than asserting
  this one — if it disagrees, the disagreement is the finding.
  DO NOT write an equivalence test that imports BOTH modules: it would die with the original in
  the deletion round. The equivalence proof is gate G5 of this round, which is a probe.

Done when — EIGHT gates. Run every one at C5, after C4 and before the handback commit C6.
Record the REAL exit code and the REAL output of each; the word "green" is not a result.

  G1 TRANSPORT. sha256 of the committed blob `.agent/authored/f275-r2.md` equals the sha256 of
     the committed blob `.agent/last_block.md`, and both equal the digest of the scratch
     original the delegating message names. Report the three digests and the byte count. This
     proves the chain scratch-original to saved copy to mirror and claims nothing about the
     emitted bytes.
  G2 THE PLAN. `.agent/plan.md` sha256 equals
     `074c2c5ad69e33a96a880b46aa1aa7f8584146abfbb3433f431391973135ff3e`; its byte count is 2368;
     its line count is 41, under the AGENTS.md cap of 50; `^## Goal$` occurs once and
     `^## Next Steps$` occurs once.
  G3 THE RECORD, all six parts, over the committed C2.
     (a) BYTES. `.agent/live_review.md` is 510121 before and 515349 after, a gain of 5228 which
         is RECORD2's 5227 bytes plus one newline. `.agent/prose_slips.md` is 166737 before and
         168030 after, a gain of 1293 which is SLIPS2's 1292 bytes plus one newline. Report both
         numbers you measured.
     (b) EXACT EDGES. For each of the two files the pre-commit blob is a byte-exact PREFIX of
         the post-commit blob, and the slice is a byte-exact SUFFIX of it.
     (c) ORDERED EQUALITY over `.agent/prose_slips.md`, by a reader independent of (b), because
         SLIPS2 is the multi-paragraph append this round carries. Split the post-commit file on
         blank lines, COUNT the SLIPS2 slice's own paragraphs into N rather than taking N from
         this block, and compare the file's last N units against the slice's N paragraphs IN
         ORDER, reporting a per-unit sha256.
     (d) NEGATIVE CONTROL on the FIRST appended paragraph of SLIPS2, in scratch only: flip one
         byte and confirm BOTH the reader of (b) and the reader of (c) REJECT it. Re-read the
         tracked file afterwards and confirm it is unchanged. Never write the mutation to disk.
     (e) COUNTS. In `.agent/live_review.md`: blank-line units 214 to 215 · `^Gate: ` 23 to 24 ·
         `^Gate: F275 R1 ` 0 to 1. In `.agent/prose_slips.md`: blank-line units 229 to 233.
     (f) THE OPEN SET DOES NOT MOVE. Distinct `^- R-\d+ — ` ids 68 to 68, distinct
         `^Done: R-\d+ — ` ids 3 to 3, OPEN SET BY DISTINCT ID 65 to 65. This round mints no id
         and resolves none: all four slips are reviewer-prose defects under amend0827 rule 2 and
         none of them earns an id. Subtract DISTINCT resolved IDS, never `Done:` LINES, of which
         the record carries five.
  G4 THE COMPLETED MODULE, over the committed C3. The base blob of
     `packages/orchestration/mission_readiness.py` is a byte-exact PREFIX of the post-commit
     blob. For EACH of the TWENTY-NINE carried definitions — the seventeen of round 1 and the
     twelve of SPEC A — its byte span in the module is IDENTICAL to that definition's byte span
     in `packages/orchestration/overnight_readiness.py` at
     `a5bf894946ab6de053a4232109d6341a63533768`; report how many of the twenty-nine matched.
     Each of the five excluded names is ABSENT from the module and PRESENT in the source; report
     both readings. The module PARSES under `ast.parse`.
     `bash -c 'python3 -m ruff check packages/orchestration/mission_readiness.py; echo "REAL_EXIT=$?"'`
     exits 0. C3's insertions on that path are UNDER 500 — report the number you measured.
  G5 EQUIVALENCE, THE BEHAVIOURAL PROOF, run as a probe script under `.remedy-wt/`, not as a
     committed test. Build a job fixture the way the test file's `_job` helper does, under a
     temporary data root inside `.remedy-wt/`, with `REMEDY_DATA_DIR` set IN-PROCESS. Then, for
     the SAME job and the SAME data root, compare the carried module against
     `packages.orchestration.overnight_readiness`:
       - `export_readiness_json(build_overnight_readiness(...))` from both must be equal ON
         EVERY KEY EXCEPT `generated_at`, and their key SETS must be equal.
       - `render_overnight_report_markdown(build_overnight_report(...))` from both must be
         EXACTLY equal.
     `generated_at` is excluded because it is a timestamp: the reviewer measured the ORIGINAL
     module disagreeing with ITSELF on that one key across two consecutive calls, so demanding
     equality there would be a gate no correct code can pass. Report the differing-key list you
     measured; it must be empty once `generated_at` is removed. Remove the probe and its data
     root by EXACT PATH afterwards.
  G6 THE TEST FILE, over the committed C4.
     `bash -c 'python3 -m pytest tests/orchestration/test_mission_readiness.py -q; echo "REAL_EXIT=$?"'`
     exits 0; report the collected count. `class TestPlan` does NOT occur in the file and
     `build_overnight_plan` does not either. `TestArchitectureGuards`'s `SRC` names
     `packages/orchestration/mission_readiness.py` and not the original. The file contains no
     import of `overnight_readiness`.
  G7 THE SUITES, each run ALONE and in this order, every one from the primary checkout: the
     FOUR state readers as FOUR separate runs — `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py` — then THIS FEATURE'S OWN RATCHETS as one run,
     `tests/orchestration/test_import_reachability.py` with
     `tests/orchestration/test_cluster_deletion_map.py` and
     `tests/orchestration/test_overnight_readiness.py`, and last the canary
     `tests/cli/test_golden_path.py`. Report each command's REAL exit code and REAL passed
     count. The reviewer measured the four readers at 506, 51, 21 and 16, the three ratchets
     together at 28, and the canary at 42, all at C6 of round 1; the original module's own test
     is in that list because it must STILL PASS — this round copies its subject, it does not
     move it.
  G8 THE TREE AND THE WIRING. `.agent/STOP` does not exist. `git status --porcelain` is EMPTY.
     The branch is `feature/f275-one-world-completion-part-three`. `git worktree list` shows
     only the primary checkout. A repo-wide search over `packages/`, `apps/`, `tests/`,
     `scripts/` and `docs/` for the two dotted import forms of the new module —
     `orchestration\.mission_readiness` and `orchestration import mission_readiness` — returns
     EXACTLY ONE file, `tests/orchestration/test_mission_readiness.py`, and NOTHING under
     `packages/` or `apps/`: production is still unwired. Do NOT gate on the bare token
     `mission_readiness`, which occurs at four unrelated sites in the cluster module
     `packages/orchestration/overnight_mission.py` and its handler. `overnight_readiness.py`,
     `cluster_deletion_map.txt` and `import_reachability_allowlist.txt` are byte-identical to
     their versions at the base of this round.

Handback: rewrite `.agent/handoff.md`. It carries the mandated sections — the state block with
the SESSION NUMBER (this is still SESSION 1 of F275) and a Fortschritt line you author and label
`Schätzung`, the per-commit changed-files table with real `git diff --numstat` columns, one line
per gate with its REAL exit code, the open-findings count, the item-status table covering every C
and every G exactly once, the deviations, and the next expected action. It has NO length cap. Do
not write a `Done:` paragraph anywhere: only the reviewer's authored text resolves a finding.

BEGIN PLAN2 sha256=074c2c5ad69e33a96a880b46aa1aa7f8584146abfbb3433f431391973135ff3e bytes=2368
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. T001 runs FIRST, and its `git rm`
sequence is never started by a session that cannot finish it.

## Current Step

ROUND 2 books round 1's PASS verdict and its four reviewer-prose slips into the record, then
COMPLETES the first carry-over's code move: the second and last staged batch of
`packages/orchestration/mission_readiness.py`, which brings the carried set to all twenty-nine
definitions, and the test file named after that module. The module is STILL UNWIRED at the end
of this round — no consumer imports it and no cluster edge is cut yet — so every commit
boundary stays green.

## Next Steps

1. The wiring round gives the CLI and the cockpit the carried readiness view as
   `mission readiness`, cuts the one surviving `packages/orchestration/ui_server.py` edge the
   deletion map records for `overnight_readiness`, and removes that line from the map in the
   SAME commit, which is what `tests/orchestration/test_cluster_deletion_map.py` requires.
2. DECISION F260 D3, the deletion paragraph, drafted with R-0832's fix clause binding it and
   R-0831 named among the ideas deleted rather than inherited.
3. The prototype-cluster deletion itself, bounded by the map's edges, one commit per module
   group, under the four measurements amend0906-triage-throughput names for a deletion round.
   It is not started by a session that cannot finish it.

## Risks

- 65 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12. The integrity gate's
  `high_blockers_open` check is WRONG about them, which is R-0648 and itself open.
- The carried module is dead code until the wiring round, by design and by DECISION F275 D1.
  That is the price of staying under the DECISION F104 D1 cap of 500 insertions per commit;
  this feature's single declared-oversize allowance is reserved for T002's atomic flip.
END PLAN2

BEGIN RECORD2 sha256=7f528e43195663edc0b91cfbf24c00a95b5b5bc6e89eb8bef9fe3d23d0d956cc bytes=5227
Gate: F275 R1 — the F275 round 1 entry. VERDICT PASS, and EVERY ONE OF THE EIGHT GATES WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs rather than read from the worker's report. This entry is booked by round 2 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 1 handback committed at `b382ab02` and pushed. Range `a5bf894946ab6de053a4232109d6341a63533768`..`b382ab02`, seven commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C6 — there is no C5 commit because C5 is the measurement step and writes no file, which the block ordered and the handback declares. THE CHANGE SET IS EXACTLY THE NINE PATHS the block named and nothing else, confirmed by the reviewer with `git diff --name-status` over the range. G1 TRANSPORT covers the chain this workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37, and NOT the emitted bytes: the reviewer's scratch original `.remedy-wt/f275-r1-FINAL.md`, the committed `.agent/authored/f275-r1.md` and the committed `.agent/last_block.md` are all 36124 bytes at `6c75575db624c8e932909fc02cb68e667dc4235f4ff14e27daaace496f886071`. G2 THE PLAN: `.agent/plan.md` byte-equal to its slice at 2526 bytes and 43 lines against the AGENTS.md cap of 50, with `^## Goal$` and `^## Next Steps$` once each. G3 THE RECORD at `46e5336d`: `.agent/live_review.md` 506317 to 510121 and `.agent/decisions.md` 919768 to 927408, a gain of 7640 which is the DEC1 slice's 7639 bytes plus one newline; the CARRIED REGION from the `^## Findings$` line to end of file is BYTE-IDENTICAL across the re-head at `ac08353106bfe118095963282161da9db92051b5be4fe03a8a86b53da920169e` before and after, which is the whole point of a re-head and was measured rather than assumed; the file starts with the HEAD1 bytes and ends with the RECORD1 bytes, the pre-commit decisions blob is an exact PREFIX and DEC1 an exact SUFFIX; ordered equality was proved by a second independent reader with N counted from the slice at 8; the negative control on the FIRST appended paragraph was rejected by BOTH readers and never written to disk; and the counts landed on every predicted pair — blank-line units 212 to 214, `^Gate: ` 22 to 23, `^Gate: F274 R23 ` 0 to 1, distinct registrations 68 to 68, distinct resolutions 3 to 3, OPEN SET 65 TO 65 BY DISTINCT ID. The open set does not move because this round minted no id and resolved none. G4 THE CLAIM at `c4cebfcb`: the pair FROM reads 0 and the TO reads 1, `^- \[~\] F275 ` occurs once, `^- \[~\] ` occurs exactly once in the whole ledger, and `^- \[x\] F\d{3} — ` still reads 76 — a claim accepts nothing. G5 THE CARRIED CODE at `352659da`: ALL SEVENTEEN of the batch-1 definitions are BYTE-IDENTICAL to their spans in `packages/orchestration/overnight_readiness.py` at the base commit, the new module parses under `ast.parse`, `python3 -m ruff check` exits 0, and the commit is 369 insertions against the DECISION F104 D1 cap of 500; the five deliberately excluded names — `OvernightEvidenceStatus`, `_CAP_UNKNOWN`, `OvernightRunPlan`, `build_overnight_plan` and `export_plan_json` — are present in the source and ABSENT from the new module, which the reviewer checked in both directions. G6 UNWIRED: both dotted import forms of the new module return ZERO matches over `packages/`, `apps/`, `tests/`, `scripts/` and `docs/`, so nothing imports it; `packages/orchestration/overnight_readiness.py` and `tests/orchestration/cluster_deletion_map.txt` are byte-identical between the base and the tip, so no edge was cut and no map line was removed. G7 THE SUITES, each re-run ALONE by the reviewer, every one exit 0: `tests/docs/` 303, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 506, `tests/orchestration/test_test_runner.py` 51, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, and the canary `tests/cli/test_golden_path.py` 42. G8 THE TREE: no `.agent/STOP`, `git status --porcelain` empty, the branch is `feature/f275-one-world-completion-part-three`, and `git worktree list` shows only the primary checkout. NO PULL REQUEST EXISTS, which is correct: under docs/roadmap/STATUS_closure_protocol.md the pull request is created by the closure sequence, not by an ordinary round. THE FOUR DEVIATIONS THE WORKER DECLARED ARE ALL DEFECTS OF THE REVIEWER'S OWN BLOCK TEXT AND NONE OF THEM PUT ANYTHING WRONG ON DISK, so under operator amendment amend0827-process-diet rule 2 they are dated lines in `.agent/prose_slips.md` and NOT findings, and no id is spent on them: the head-swap separator newline the block's arithmetic required but its prose never stated, the two P1 marker lines carrying no digest while constraint 1 says every slice carries one, the Fortschritt line ordered "repeated verbatim" with no line supplied to repeat, and G8's `git log` clause naming a commit later than the commit the gates were ordered at, which is the §3 item 14 shape. The worker declared each rather than working around it, measured both candidate readings of the first before applying either, and applied the block as written throughout; that is the behaviour the block asks for.
END RECORD2

BEGIN SLIPS2 sha256=a7fc937315393a92a00815e4b6d173cf97383dfba4553c836dfd69f2fe717f31 bytes=1292
2026-09-08 · F275 R1 · The round 1 block's constraint 2 ordered the live-review prefix "replaced" by the HEAD1 slice, while its own gates G3(a) and G3(f) were computed from HEAD1 plus one separator newline; a literal substitution gives 510120 bytes and 213 units and fails both, so the worker measured both readings in scratch and applied the only one satisfying the block.

2026-09-08 · F275 R1 · The round 1 block's constraint 1 says every slice's BEGIN line carries its own sha256 and byte count, and the two P1 pair markers carried neither; the worker measured both at 120 bytes and re-ran the containment test rather than trusting the label.

2026-09-08 · F275 R1 · The round 1 block ordered the handback to repeat the Fortschritt line verbatim and supplied no Fortschritt line to repeat, because under self-drive that line lives in the reviewer's operator brief rather than in the block; the worker authored one and labelled it a Schätzung.

2026-09-08 · F275 R1 · The round 1 block ordered all eight gates run at C5 and then had G8 assert `git log` shows C0a through C6, a commit that does not exist until after the gates run — the §3 item 14 shape of a gate reaching a commit it cannot honestly measure; the worker marked it deviated and re-confirmed the clause after C6.
END SLIPS2

