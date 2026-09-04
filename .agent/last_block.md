STEP CLOSURE PRECONDITION 4 (BUILT STATE) / ROUND 14 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 3, ROUND 14

Goal
  Book round 13's PASS verdict into the ledger (RECORD13 - closure
  precondition 6's RUN step; its two describe_self_use_run_defects
  strings add evidence to the already-open R-0784, no new id minted -
  precondition 6 is now DISCHARGED for F114 pending only the
  closure commit's own consumed_by=F114 edit), then author
  docs/roadmap/features/T3_F114.md's Built State section (closure
  precondition 4). No code changes this round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r14.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD13 to .agent/live_review.md (append) and PLAN14 to
      .agent/plan.md (whole-file replacement)
  C2  apply BUILTSTATE PAIR to docs/roadmap/features/T3_F114.md
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r14.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  docs/roadmap/features/T3_F114.md (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD13, PLAN14, BUILTSTATE PAIR) is
     applied BYTE FOR BYTE: extract it by delimiter index from the
     COMMITTED .agent/authored/f114-r14.md - marker lines EXCLUDED -
     and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD13 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. PLAN14 REPLACES .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD13 and PLAN14 both carry NO trailing
     newline of their own.
  5. THE BUILTSTATE PAIR is APPEND-shaped: TO contains FROM verbatim
     (containment already verified at authoring time: true). Apply via
     str.replace(FROM, TO, 1) on docs/roadmap/features/T3_F114.md;
     before C2 confirm FROM occurs exactly 1x in that file; after C2
     confirm "TO contains FROM: true".
  6. This round is under docs/roadmap/** (T3_F114.md), so it gates
     tests/orchestration/test_roadmap_index.py BESIDE tests/docs/, per
     the standing .agent/context.md constraint carried forward from
     earlier rounds.
  7. This round does not touch packages/, apps/, or tests/ - only
     docs/roadmap/features/T3_F114.md and .agent/** change.
  8. Read .agent/STOP from disk before the first commit and again
     before C3. If it exists, finish the commit in hand, write the
     handback, and stop.
  9. Self-review loop before every commit (git diff --stat, git diff).
     Push after C3. No pull request, no merge this round - the closure
     commit itself (STATUS/README/PR) is later work, not this round's.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r14.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND (RECORD13). Base size of .agent/live_review.md
     immediately BEFORE C1: report byte length and trailing-newline
     status (expect 2393966, no trailing newline). RECORD13 has ZERO
     internal newlines - report its own byte length (expect 4991).
     Report base + 1 + 4991 and whether it equals the post-C1 file's
     byte length (expect 2398958). Second reader: post-C1 file's bytes
     from `base` to end equal exactly "\n" + RECORD13. Negative control
     in a scratch copy ONLY: flip one byte inside RECORD13's own text,
     confirm the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN14 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; expect 40 (PLAN14 has 41 logical lines but no trailing newline), must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE BUILT STATE PAIR. Report the FROM count in
     docs/roadmap/features/T3_F114.md immediately BEFORE C2 (must be
     1), apply it, then report "TO contains FROM: true" (matching
     constraint 5). Report the file's byte length after C2 (expect
     6744, from a base of 3331 plus one separator newline plus the
     3412-byte BUILTSTATE slice - recompute independently) and whether
     it still ends with a trailing newline (expect yes, since
     BUILTSTATE's own last byte is its structural `\n`).
  G5 THE DOCS GATES:
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q
     Report both counts.
  G6 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY:
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each count.
  G7 THE TREE, THE COMMITS AND THE SWEEP.
       git status --porcelain            -> empty, checked immediately before C3 staged
       git diff --stat <this round's own starting HEAD>..HEAD -- packages/ apps/ tests/  -> empty
     Per-commit numstat cross-check (`git show --numstat`) for C0a,
     C0b, C1 (two paths) and C2 (one path) against this handback's own
     Commits table - report every cell and confirm it matches.
     Staleness sweep: one entry per file this round touched, plus a
     statement that no NEW stale sentence was found outside the change
     set this round.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
There are four: RECORD13, PLAN14, BUILTSTATE PAIR FROM and BUILTSTATE
PAIR TO.

<<<BEGIN RECORD13>>>
Gate: F114 R13 — the round 13 entry, closure precondition 6's RUN step, no production code touched in the primary checkout. VERDICT PASS, over the range `7997a76658289e71b0506f25ee8b48e0e29d165b..c6429dfc13d264ea7abd88aa4696d38f8b616914` (commits C0a `5be393bb6125eadf4bf9cfc1814a3ae6a0af97d1`, C0b `7dcd80fc4b812911f080795fc96ac903876aa824`, C1 `3afc78c52ae7a79efe5e032d81461f490f0d708c`, C2 `c6429dfc13d264ea7abd88aa4696d38f8b616914` — four real content commits — plus handback commit `fdfe587574be7af3625dcb219a99233508d561c9`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r13.md .agent/last_block.md` both print `41d40b623eec851cf41502ff8777df6175216889323f6f9b6f2ef02be340bff4`, reproduced directly. G2 THE LEDGER APPEND (RECORD12) HELD BYTE-EXACT: base 2390210 bytes (no trailing newline), RECORD12 measured 3755 bytes with zero internal newlines, base + 1 + 3755 = 2393966 exactly matching the post-C1 file; the appended tail equals `\n` + RECORD12 byte for byte, a one-byte-flipped negative control was correctly rejected. G3 THE PLAN HELD BYTE-EXACT: PLAN13 extracted from the committed authored file compares equal to `.agent/plan.md` (42 lines by `wc -l`; `## Goal`/`## Next Steps` each exactly once). G4 THE SELF-USE RUN WAS REAL, NOT SIMULATED, REPRODUCED INDEPENDENTLY: `run_next_self_use_item()` ran unflagged (no fake override, no queue_path override) against the real local `ollama` provider for both roles (`plan.execution_config` recording `builder='ollama'`/`reviewer='ollama'`, source `cli` for both, model `muse-glimmer:latest` — the product default), took 77.3 seconds, and produced job `2ac1522a7034440b`: `status='blocked'`, task T001 `final_status='repair_exhausted'`, `reviewer_verdict='fail'` — nothing promoted. The reviewer independently re-loaded the same job via `pingpong_job.load_job_plan('2ac1522a7034440b')` from a fresh process and confirmed `status`/`error` match exactly, then called `describe_self_use_run_defects(plan)` itself and got back the SAME two strings, verbatim: `job 2ac1522a7034440b (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. G5 THE EVIDENCE HELD: `.agent/selfuse_f114/` holds exactly `SU-008.md` and `run.txt`, nothing else; `cmp` against the rendered job file at `.remedy-wt/selfuse-f114-run/SU-008.md` exits 0 (byte-identical), reproduced independently. G6 THE TREE AND THE SWEEP HELD: `git status --porcelain` and `git diff --stat 7997a766..c6429dfc -- packages/ apps/ tests/` are both empty, reproduced independently; the scratch `.remedy-wt/selfuse-f114-run/` is gitignored (invisible to `git status`), the job's own execution worktree `.remedy-wt/job-2ac1522a7034440b/` exists, retained and untouched, exactly as every prior self-use run has left its own; every commit's numstat cells match the handback's own Commits table cell for cell. TWO DEVIATIONS ARE DECLARED (a PLAN13 draft typo caught and fixed before C0a, never landing on disk; and calling `describe_self_use_run_defects` against a re-loaded `JobPlan` in a second process rather than the run's own in-memory return value, to avoid re-spending the job's budget a second time — the reviewer's own independent re-load above confirms this was safe and produced an identical answer); the reviewer found no others. CLOSURE PRECONDITION 6's REGISTRATION OBLIGATION, DISCHARGED PER §3 ITEM 30: the open set was searched for this defect before any id was considered. `R-0784` (registered F109 R19, OPEN, evidence already added by F110 R16 on job `6f74dd7367704fd5` and by F112 R21 on job `848fc4c67d7b405b`) already describes exactly this class — a self-use run against `R-0418` (a reviewer-block-authoring-practice finding no builder can fix in code) blocking at the normal approval gate. This is the SAME defect recurring a FOURTH time, on a FOURTH job (`2ac1522a7034440b`), on a FOURTH feature branch, with the SAME proximate trigger F109's and F112's own instances had — `repair_exhausted` after both repair rounds spent, rather than F110's `review_inconsistent` after one. Per item 30 this evidence is ADDED TO `R-0784` here rather than minted as a fourth id; `R-0784` remains OPEN, its fix unchanged and still owed to F258's generator (a tier-1 filter for reviewer-practice findings, or an explicit acceptance that some generated items will honestly block), not to F114. NO NEW ID IS MINTED. THE OUTCOME IS A NORMAL APPROVAL-GATE RESULT, NOT A ROUND FAILURE: the self-use rail executed end to end against a real local provider and correctly refused to promote unfinished work. Closure precondition 6 is now DISCHARGED for F114 pending only the `consumed_by=F114` edit, which lands in the closure commit itself, not in this round. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD13>>>

<<<BEGIN PLAN14>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 14 books round 13's PASS verdict (RECORD13 - closure
precondition 6's RUN step; its two `describe_self_use_run_defects`
strings ADD EVIDENCE to the already-open `R-0784`, no new id minted),
which DISCHARGES precondition 6 pending only the `consumed_by=F114`
edit the closure commit itself makes. This round also authors
`docs/roadmap/features/T3_F114.md`'s Built State section (closure
precondition 4), appended after "Do not touch". No code changes.

## Next Steps

- `remedy integrity check --json` (precondition 3) - not yet run this
  session; do it alongside the closure-commit round.
- The closure commit: evidence job, fresh review zip, STATUS line,
  README sync, `consumed_by=F114`, the PR
  (STATUS_closure_protocol.md algorithm). A fresh session, per F112's
  own precedent (closure spanned rounds 20/21/22/29/30/31 there).
- Session note: round 14, session 3 - 5th delegated round, at the top
  of the 4-5 default; session ends here with this handback.

## Risks

- `docs/roadmap/features/T3_F114.md` is under `docs/roadmap/**`, so
  this round gates `tests/orchestration/test_roadmap_index.py` beside
  `tests/docs/`, per the standing `.agent/context.md` constraint.
- The Built State section's own file-count/test-count claims (19601/
  19554, the file list) are re-measured at authoring time, not copied
  from memory, since this branch's own rounds keep moving them.
<<<END PLAN14>>>

<<<BEGIN BUILTSTATE PAIR FROM>>>
calibration. Suggested tests: tests/cli/test_cost_preview.py.
<<<END BUILTSTATE PAIR FROM>>>

<<<BEGIN BUILTSTATE PAIR TO>>>
calibration. Suggested tests: tests/cli/test_cost_preview.py.

## Built State — what F114 delivered

`remedy job run` is the first (and, so far, only) command wired to a
cost preview: before an expensive run starts, it prints an estimate
band with its basis and, in attended mode, asks for confirmation above
a configured threshold; `--yes` and `--unattended` both skip the
prompt with an audited line, and a non-tty pipe with neither flag
exits (code 2) with the estimate and the `--yes` hint rather than
hanging.

- `packages/orchestration/token_economy.py` —
  `tokens_to_cost_usd(tokens, price_basis_usd_per_1k_tokens)` extracted
  from `budget_guard.predict_next_task_cost` with no behavior change,
  now the ONE shared token-to-USD conversion both the predictive
  budget gate and the cost preview use.
- `packages/orchestration/cost_preview.py` — `CostBandEstimate`
  (`band_usd_low`/`band_usd_high`/`basis`/`inputs`, the low/high bounds
  always None together, never separately) and
  `estimate_cost_band(band_a, band_b, *, repeat_count, config)`, which
  spans two `TokenBand` values via `tokens_to_cost_usd` and answers
  `ESTIMATE_UNAVAILABLE` (never a fabricated number) for an
  unrecognised class, an unpriced config or a negative `repeat_count`
  (A9: unknown is treated as expensive). `resolve_confirm_above_usd()`
  resolves the `cost_preview.confirm_above_usd` config key (env
  `REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD` > `[remedy.cost_preview]`
  TOML > `DEFAULT_CONFIRM_ABOVE_USD = 0.5`), falling back to the
  default on a malformed or non-positive configured value rather than
  blocking every command.
- `apps/cli/cost_preview_confirm.py` — the ONE shared CLI helper
  (deliberately not a third copy of `loop_cmd.py`'s own
  `_confirm_materialization`/`_stdin_is_a_tty` shape):
  `render_estimate_line` (always carries a `basis:` label, A9),
  `confirm_cost_preview` (an unavailable estimate is treated as
  expensive; `--yes` prints an audited line and proceeds; a non-tty
  stdin exits `EXIT_USAGE = 2` with the `--yes` hint rather than
  calling `input()`; below the threshold, no prompt either way).
- `apps/cli/commands/job.py` (`_cmd_job_run_cycles`) and
  `apps/cli/command_catalog.py` (`job.run`'s `CommandEntry`,
  `is_expensive=True`, its own `--yes` `ArgDef`) — the one real,
  wired caller. Real cost bands for `job.run` do not exist yet, so its
  estimate is always `ESTIMATE_UNAVAILABLE` today (still confirmed,
  per A9), pending future task-class calibration.
- `docs/guides/cost-preview-user-guide-v0.md` — the user-facing guide,
  registered in `docs/README.md`'s Quick-Find Table and Guides
  section.
- Tests: `tests/orchestration/test_cost_preview.py` (T001 unit),
  `tests/cli/test_cost_preview_confirm.py` (T002 unit),
  `tests/cli/test_cost_preview.py` (five acceptance tests exercising
  the REAL `confirm_cost_preview` end to end through `job.run`, not
  mocked), and `tests/test_command_catalog.py::TestCatalogExpensive`
  (pins `is_expensive` as explicit and reviewable, and that exactly
  `job.run` carries it so far).
- Integration gate (round 11): clean at the merge-base with `main` —
  branch 19601 passed / base 19554 passed, both 23 skipped, 0 failed
  on either side, no attribution needed.

Deliberately not yet done, named as future work rather than blockers:
marking further commands `is_expensive` (only `job.run` so far), and
real cost bands for `job.run` (still `ESTIMATE_UNAVAILABLE`, honestly).
<<<END BUILTSTATE PAIR TO>>>
