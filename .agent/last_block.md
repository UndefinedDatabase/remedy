STEP CLOSURE PRECONDITIONS 6 + 3 / ROUND 26 - F262 List commands v2 (dates, sort, filter)
FEATURE F262 - List commands v2 (dates, sort, filter) (Tier 2) - SESSION 9, ROUND 26

Goal
  Book round 25's verdict into the ledger (RECORD25), then satisfy
  closure precondition 6 end to end (docs/roadmap/STATUS_closure_protocol.md):
  the queue has no pending item, so generate one with
  packages.orchestration.self_use_generator.generate_and_append_if_empty(),
  run it unflagged to the normal approval gate with
  packages.orchestration.self_use_runner.run_next_self_use_item(), report
  describe_self_use_run_defects() verbatim, save the evidence; then run
  closure precondition 3 (integrity check) read-only. No consumed_by
  edit and no new R-id this round - both are the reviewer's later work.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r26.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD25 to .agent/live_review.md (append) and PLAN27 to
      .agent/plan.md (whole-file replacement)
  C2  GENERATION: call generate_and_append_if_empty() per constraint 5;
      commit scripts/self_use_queue.json
  C3  RUN: run the new item per constraints 6-11; commit the evidence
      under .agent/selfuse_f262/
  C4  rewrite .agent/handoff.md - the handback (precondition 3's reading
      is reported here, it writes no file); then push

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r26.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md, .agent/plan.md (C1) - scripts/self_use_queue.json
  (C2) - .agent/selfuse_f262/<entry-id>.md, .agent/selfuse_f262/run.txt
  (new, C3) - .agent/handoff.md (C4)

Constraints
  1. Every authored slice (RECORD25, PLAN27) is applied BYTE FOR BYTE:
     extract it by its one-line BEGIN/END markers from the COMMITTED
     .agent/authored/f262-r26.md (marker lines EXCLUDED), written by a
     Python script, never retyped. If a slice looks wrong, apply it as
     written and DECLARE it.
  2. C1 is the first substantive commit of the round.
  3. RECORD25 appends to .agent/live_review.md as EXACTLY TWO newline
     bytes followed by the slice; PLAN27 REPLACES .agent/plan.md whole;
     neither carries a trailing newline.
  4. Read .agent/STOP before C0a, before C3 and before C4; if present,
     finish the commit in hand, write the handback, stop.
  5. C2 IS A PURE PYTHON CALL:
       from packages.orchestration.self_use_queue import next_self_use_item, load_self_use_queue
       from packages.orchestration.self_use_generator import generate_and_append_if_empty
     BEFORE calling the generator verify next_self_use_item() is None
     and len(load_self_use_queue()) is 8 (the return is a tuple). If
     either disagrees, STOP before the call and declare it. Otherwise
     call generate_and_append_if_empty() exactly once, no arguments
     (real shipped queue and ledger paths), and report the returned
     SelfUseQueueEntry field by field (or None). The reviewer measured
     the tier-1 selector at 60f48fb6: the expected pick is R-0418 and the
     expected id SU-009 with consumed_by "" - report the REAL values,
     never assume. Report `git show --numstat <C2> -- scripts/self_use_queue.json`
     and whether the diff is a clean append or a full-file rewrite
     (either is acceptable; the rewrite is the open R-0785 class - do
     NOT mint a finding for it).
  6. C3 runs the new pending item:
       from pathlib import Path
       from packages.orchestration.self_use_runner import run_next_self_use_item
       entry, job_file_path, plan = run_next_self_use_item(Path(".remedy-wt/selfuse-f262-run"))
     UNFLAGGED - no builder_name/reviewer_name/builder_provider/
     reviewer_provider/fake override, no queue_path - so role resolution
     picks the REAL default provider. If the bash guard refuses the
     `.remedy-wt/` path on a python3 -c line, run the same call from a
     heredoc `python3 - <<'PY' ... PY` (no script file is written for
     it) and say so. Measure wall time around the call; report entry.id
     and job_file_path.
  7. If run_next_self_use_item raises SelfUseRunError (planning already
     blocked it, or no usable real provider): STOP there, do NOT retry
     with a fake override, and declare the exact exception text in the
     handback instead of a normal C3/C4 completion.
  8. After the run report plan.status, plan.execution_config (provider
     AND model actually used for builder and reviewer), and every task's
     final_status/reviewer_verdict.
  9. Call packages.orchestration.self_use_findings.describe_self_use_run_defects(plan)
     and report EVERY string it returns verbatim, in order ("empty
     tuple" plainly if empty; never omit the check).
  10. EVIDENCE under .agent/selfuse_f262/ (new directory): <entry-id>.md
      = a byte-exact copy of the rendered job file at job_file_path
      (shutil.copyfile; verify equality with a Python byte read, since
      cmp may be denied); run.txt = plain text recording the job id,
      entry.id, job_file_path, provider/model for both roles, budgets,
      final plan.status, every task's final_status/reviewer_verdict,
      measured wall time, and the full describe_self_use_run_defects()
      output verbatim. Free-form; it is fresh evidence, not a slice.
  11. Do NOT set consumed_by anywhere; do NOT register any R-id; do not
      delete the job's own execution worktree (.remedy-wt/job-<id>/) -
      report its path and leave it. Report whether
      .remedy-wt/selfuse-f262-run is untracked-and-gitignored.
  12. PRECONDITION 3, after C3, read-only: run
      `python3 -m apps.cli.grouped integrity check --json` (the exact
      module `pyproject.toml` maps the `remedy` console script to; the
      script itself is denied here) and report the literal JSON. It is
      CONFIRMED only if `"passed": true`, `"fail_count": 0` and
      `high_blockers_open` reports no open Blocker/High finding; report
      the real reading either way and do not attempt to fix anything.
  13. This round touches no packages/, apps/, tests/ or docs/ path in the
      PRIMARY checkout - only scripts/self_use_queue.json (a data file)
      and .agent/**. Self-review before every commit. Push after C4. No
      pull request, no merge.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. `sha256sum .agent/authored/f262-r26.md
     .agent/last_block.md` - one digest, twice.
  G2 THE LEDGER APPEND (RECORD25). Base size of .agent/live_review.md
     before C1 (expect 2498900, no trailing newline); RECORD25's byte
     length (expect 4344, zero internal newlines); base + 2 + that
     (expect 2503246) versus the post-C1 length; tail
     equality "\n\n" + RECORD25; negative control in a scratch copy
     (one flipped byte REJECTED).
  G3 THE PLAN. .agent/plan.md equals PLAN27 byte for byte (expect
     1979 bytes); `wc -l` under 50 (expect 41); `grep -c
     '^## Goal'` and `grep -c '^## Next Steps'` each 1.
  G4 THE GENERATION (constraint 5): the two precondition readings, the
     returned entry field by field, `len(load_self_use_queue())` after
     (expect 9), the numstat line and append-vs-rewrite reading.
  G5 THE RUN (constraints 6-9): entry.id, job_file_path, wall time,
     plan.status, execution_config for both roles, every task's
     final_status/reviewer_verdict, the full
     describe_self_use_run_defects output verbatim.
  G6 THE EVIDENCE. `ls .agent/selfuse_f262/` names exactly <entry-id>.md
     and run.txt; the .md equals the job file at job_file_path byte for
     byte (report both lengths); run.txt's byte length.
  G7 PRECONDITION 3 (constraint 12): the exact command, the literal
     JSON, and CONFIRMED / NOT CONFIRMED.
  G8 THE TREE AND THE COMMITS. `git status --porcelain` empty before C4
     is staged; `git ls-files .remedy-wt` empty; `.agent/STOP` absent at
     each of constraint 4's reads; the job's retained worktree path;
     per-commit `git show --numstat --format=""` for C0a, C0b, C1 (two
     paths), C2 (one path), C3 (two paths) against this handback's
     Commits table; `git diff --stat 60f48fb6..<C3> -- packages/ apps/
     tests/ docs/` empty; the push result.

SLICES. Each lies between its own one-line BEGIN and END marker; the
slice is the bytes between the BEGIN marker's newline and the newline
before the END marker, EXCLUDING that final newline.

<<<BEGIN RECORD25>>>
Gate: R25 — the F262 R25 entry, the INTEGRATION GATE (docs/agents/integration_gate.md steps 1-5) before closure, no production code touched. VERDICT PASS — GATE CLEAN, over the range `92cc869b..60f48fb6` (C0a `f6f9ed29`, C0b `df882239`, C1 `fe74206b`, C2 `3aeed0e1`, handback `60f48fb6`), independently re-verified by the reviewer. TRANSPORT HELD IN ITS PRIMARY FORM: the reviewer's scratch original, the committed `.agent/authored/f262-r25.md` and `.agent/last_block.md` compare equal byte for byte, sha256 `2f623c61ddd7227eaabf76f4eed7f617de41b417dbed969fda2822dd807fa2aa`, 16851 bytes. THE LEDGER APPEND (RECORD24) HELD: `.agent/live_review.md` 2494695 (at `df882239`) plus two newlines plus RECORD24 (4203 bytes) equals 2498900 (at `fe74206b`), tail equal to the slice, the worker's one-byte-flipped negative control rejected. THE PLAN HELD: `.agent/plan.md` equals PLAN26 (2015 bytes, 42 lines by `wc -l`, `## Goal` and `## Next Steps` once each). THE GATE EVIDENCE HELD: `.agent/gate_f262_r25/` holds exactly the nine files constraint 5 names (attribution.txt 2105, base_failed.txt 0, base_run_tail.txt 3439, branch_failed.txt 0, branch_only.txt 0, branch_run_tail.txt 3414, fixed_by_branch.txt 0, gate_summary.txt 8084, parity_mtime.txt 2265 bytes) and nothing else; gate_summary.txt follows the `.agent/gate_f114_r11/` shape and closes with a measured outcome, not a verdict. THE GATE ITSELF READ CLEAN, REPRODUCED BY THE REVIEWER: the branch run (`python3 -m pytest -n auto -q` at `60f48fb6`, the reviewer's own re-run in the primary checkout) read 19676 passed, 23 skipped, 0 failed, exit 0 in 153.52s — identical counts to the worker's run at `fe74206b` (163.18s); the base run at the merge-base `7c65d9cc` (confirmed equal to `git merge-base main HEAD`, PR 235's merge), performed by the worker in the throwaway worktree `.remedy-wt/f262-r25-base` on branch `tmp/f262-r25-base` with UI parity restored (`shutil.copytree(symlinks=True)`, 44839 node_modules entries with 27 symlinks preserved, dist re-stamped, `_frontend_is_stale()` False measured inside the worktree) read 19601 passed, 23 skipped, 0 failed, exit 0 in 191.27s; `branch_failed.txt`, `base_failed.txt`, `branch_only.txt` and `fixed_by_branch.txt` are all 0 lines, so no attribution target exists on either side and no BLOCKER is possible — the reviewer read the full raw evidence (gate_summary.txt, attribution.txt, parity_mtime.txt, both run tails), not a summary. UI PARITY HELD AS AN EVENT: the base run window 1788598715.63..1788598907.49 contains no `apps/ui/dist` mtime (all four files stamped 1788598700.34 before and after), the accompanying content digest `d60df099…` identical before and after, `REMEDY_UI_NO_AUTO_BUILD=1` passed in the subprocess env dict and not trusted alone. THE TEST-COUNT DELTA IS ACCOUNTED: 19699 branch cases minus 19624 base cases equals 75, matched exactly by `--collect-only` per changed test file in both trees (four new files, 23 cases; fifteen existing files grew by 52). THE CLEANUP AND THE TREE HELD, reproduced independently: `git worktree list` shows no `f262-r25-base` entry, `git branch --list 'tmp/*'` is empty, `git status --porcelain` and `git ls-files .remedy-wt` are both empty, `.agent/STOP` absent; `git diff --stat 92cc869b..3aeed0e1 -- packages/ apps/ tests/ docs/` is empty; every numstat cell matches the handback's Commits table (222/0, 183/415, 3/1 + 20/21, the nine evidence files), all four pre-handback commits single-parent and under 500 insertions; branch head equal to `origin/feature/f262-list-commands-v2`. NO DEVIATION FROM THE COMMIT ORDER WAS DECLARED and the reviewer found none; the worker's one pre-commit edit of gate_summary.txt (replacing an inferred phrase with the measured test id before the file was first committed) is not a deviation. Open findings, canonical line-count formula: 356 registered minus 77 `Done:` lines equals 279 open, unchanged; `.agent/candidates.md` remains EMPTY. This is F262's FIRST 'full suite green' claim, per docs/agents/planner_reviewer_prompt.md §4 item 6 — only an integration-gate round may make it. Closure preconditions after this round: 1 (every round PASS) and 2 (integration gate clean) HOLD; 4 (Built State, round 24) SATISFIED; 5 holds (clean, pushed); 3 (`integrity check --json`) and 6 (the self-use item) are the next round's work.
<<<END RECORD25>>>

<<<BEGIN PLAN27>>>
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

Round 26, session 9 — closure preconditions 6 and 3. The self-use queue
holds no pending item (eight, all consumed), so
`generate_and_append_if_empty()` appends one (expected SU-009, tier 1,
the oldest open Low/Medium finding), `run_next_self_use_item()` runs it
unflagged to the normal approval gate with the default small budget,
`describe_self_use_run_defects()` is reported verbatim, evidence lands
under `.agent/selfuse_f262/`; then `integrity check --json` via the
`apps.cli.grouped` module route. No `consumed_by` edit, no new R-id.

## Next Steps

- Book round 26 (with the reviewer's defect-registration narration
  against the open set — §3 item 30), then closure algorithm steps 1-2:
  evidence job `f262-closure` (EVIDENCESCRIPT template from
  `.agent/authored/f009-r33.md`), fresh review zip with red control.
- The closure commit (STATUS `[x]`, README sync, `consumed_by=F262` on
  the new item) and the pull request; merge under the operator's
  2026-09-05 authorization once hosted CI reads green.

## Risks

- The self-use run is a real, budget-capped call against local
  `ollama` (`max_cost_usd=0.50`, `max_provider_calls=6`); prior runs of
  the same tier-1 pick ended BLOCKED at the approval gate — the correct
  outcome — and their defect strings were added to the open `R-0784`.
- `append_generated_item` may rewrite `scripts/self_use_queue.json`
  whole (open `R-0785` class); report append vs rewrite, never fix it.
<<<END PLAN27>>>

Handback: write .agent/handoff.md per docs/agents/handback_template.md
and AGENTS.md - Session line `SESSION 9 of feature F262 · round 26 ·
rounds so far 26` with one sentence of context self-assessment, Range
`Review of 60f48fb6..<C3>`, one changed-files table per commit (C0a, C0b,
C1, C2, C3; C4 grouped per the self-reference exception), an item-status
table over C0a..C4 and G1..G8, External actions (the push; the job's own
worktree), raw Verification per gate, Authored-text proofs, Deviations,
and Next: "the reviewer books round 26 with the defect-registration
narration, then closure algorithm steps 1-2 (evidence job f262-closure
and the review zip)".
