STEP CLOSURE PRECONDITION 6 (RUN) / ROUND 13 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 3, ROUND 13

Goal
  Book round 12's PASS verdict into the ledger (RECORD12 - the
  self-use GENERATION step, SU-008 appended), then perform closure
  precondition 6's RUN step: run SU-008 to the normal approval gate via
  packages.orchestration.self_use_runner.run_next_self_use_item(),
  unflagged (real provider resolution, no fake override), save the
  evidence, and report describe_self_use_run_defects()'s output
  verbatim. No consumed_by edit and no new finding registration this
  round - both are the reviewer's own next-round work.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r13.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD12 to .agent/live_review.md (append) and PLAN13 to
      .agent/plan.md (whole-file replacement)
  C2  run SU-008 per constraints 5-11 below; save evidence under
      .agent/selfuse_f114/
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r13.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  .agent/selfuse_f114/SU-008.md (new, C2) -
  .agent/selfuse_f114/run.txt (new, C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD12, PLAN13) is applied BYTE FOR BYTE:
     extract it by delimiter index from the COMMITTED
     .agent/authored/f114-r13.md - marker lines EXCLUDED - and write it
     with a script, never by retyping. If a slice looks wrong, apply it
     as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD12 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. PLAN13 REPLACES .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD12 and PLAN13 both carry NO trailing
     newline of their own.
  5. C2 runs the queue's pending item:
       from pathlib import Path
       from packages.orchestration.self_use_runner import run_next_self_use_item
       entry, job_file_path, plan = run_next_self_use_item(Path(".remedy-wt/selfuse-f114-run"))
     UNFLAGGED - pass no builder_name/reviewer_name/builder_provider/
     reviewer_provider/fake override of any kind, and no queue_path
     (use the real shipped scripts/self_use_queue.json) - so role
     resolution picks the REAL default provider, exactly as every prior
     self-use run this repository has performed. Report entry.id
     (expected "SU-008"), job_file_path, and measure wall time around
     the call.
  6. If run_next_self_use_item raises SelfUseRunError because role
     resolution cannot produce a usable real provider: STOP right
     there, do NOT retry with a "fake" override or any other
     workaround, and declare the exact exception text in the handback
     instead of a normal C2/C3 completion.
  7. After a successful run, report plan.status, plan.execution_config
     (the provider AND model actually used for both builder and
     reviewer roles), and per-task final_status/reviewer_verdict for
     every task the JobPlan carries.
  8. Call packages.orchestration.self_use_findings.describe_self_use_run_defects(plan)
     and report EVERY string it returns, verbatim, in order (an empty
     tuple is a valid, complete answer - report "empty tuple" plainly
     if so, never omit the check).
  9. EVIDENCE, saved under .agent/selfuse_f114/ (a new directory this
     round creates):
       - SU-008.md: a byte-exact copy of the rendered job file at
         job_file_path (shutil.copyfile, never a retype or
         reconstruction) - verify with cmp against the original after
         copying.
       - run.txt: a plain text file recording - the job id, entry.id,
         job_file_path, provider/model for both roles (from
         plan.execution_config), final plan.status, every task's
         final_status/reviewer_verdict, measured wall time, and the
         full describe_self_use_run_defects() output verbatim
         (or "empty tuple" if empty). Free-form otherwise; this is a
         fresh evidence file, not an authored slice needing byte-exact
         reproduction from anywhere.
  10. Do NOT set consumed_by anywhere in scripts/self_use_queue.json -
      that edit belongs to the closure commit, a later round, not this
      one.
  11. Do NOT register any new R-id finding in .agent/live_review.md
      this round, regardless of the run's outcome (blocked, completed,
      or anything else) - the reviewer performs that analysis (searching
      the open finding set, narrating any connection to an existing
      finding) when booking THIS round's own verdict at the next
      round's C1. Simply report the raw, real facts in the handback;
      do not interpret or classify them as a finding yourself.
  12. The scratch dest_dir (.remedy-wt/selfuse-f114-run/) used only to
      render/plan the job file: confirm after the run whether
      `git status --porcelain` shows it as untracked, and if so
      whether it is covered by .gitignore's existing `.remedy-wt/`
      rule (expected) - report which. Do not delete the job's OWN
      execution worktree (created and managed by run_job itself,
      typically under .remedy-wt/job-<id>/) - every prior self-use
      run has left that one retained deliberately; report its path
      and leave it untouched.
  13. This round does not touch packages/, apps/, or tests/ in the
      PRIMARY checkout - only .agent/** changes (including the new
      .agent/selfuse_f114/ evidence directory).
  14. Read .agent/STOP from disk before the first commit and again
      before C3. If it exists, finish the commit in hand, write the
      handback, and stop.
  15. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r13.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND (RECORD12). Base size of .agent/live_review.md
     immediately BEFORE C1: report byte length and trailing-newline
     status (expect 2390210, no trailing newline). RECORD12 has ZERO
     internal newlines - report its own byte length (expect 3755).
     Report base + 1 + 3755 and whether it equals the post-C1 file's
     byte length (expect 2393966). Second reader: post-C1 file's bytes
     from `base` to end equal exactly "\n" + RECORD12. Negative control
     in a scratch copy ONLY: flip one byte inside RECORD12's own text,
     confirm the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN13 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; expect 42 (PLAN13 has 43 logical lines but no trailing newline), must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE SELF-USE RUN. Report entry.id, job_file_path, measured wall
     time; plan.status; plan.execution_config for both roles
     (provider and model); every task's final_status/reviewer_verdict;
     the full describe_self_use_run_defects(plan) output verbatim (or
     "empty tuple").
  G5 THE EVIDENCE. `ls .agent/selfuse_f114/` names exactly SU-008.md
     and run.txt, nothing else. `cmp .agent/selfuse_f114/SU-008.md
     <job_file_path>` -> exit 0 (report the real job_file_path used).
     Report run.txt's byte length.
  G6 THE TREE AND THE SWEEP.
       git status --porcelain            -> empty, checked immediately before C3 staged
       git diff --stat <this round's own starting HEAD>..HEAD -- packages/ apps/ tests/  -> empty
     Report whether .remedy-wt/selfuse-f114-run is gone, or untracked-
     and-gitignored (name which); report the job's own retained
     worktree path (report it exists, untouched). Per-commit numstat
     cross-check (`git show --numstat`) for C0a, C0b, C1 (two paths)
     and C2 (two paths) against this handback's own Commits table -
     report every cell and confirm it matches. Staleness sweep: one
     entry per file this round touched, plus a statement that no NEW
     stale sentence was found outside the change set this round.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
There are two: RECORD12 and PLAN13.

<<<BEGIN RECORD12>>>
Gate: F114 R12 — the round 12 entry, closure precondition 6's GENERATION step only, no production code touched. VERDICT PASS, over the range `31aa76b79a8dd9eda17039c903cbff3fef1e06bc..5d614a7469171ccdb450b37dc66a306297b4bc6f` (commits C0a `aae446bad07559777368358fd613c97a92f982b1`, C0b `dd6a9203113a7dafa19a534129684aec6f6e00e7`, C1 `1e1f6d3caea7d77af1e88cd6795235d6f444bf16`, C2 `5d614a7469171ccdb450b37dc66a306297b4bc6f` — four real content commits — plus handback commit `7997a76658289e71b0506f25ee8b48e0e29d165b`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r12.md .agent/last_block.md` both print `7dcc5685b027a53c1388f6f9f3cac234d6a53b7a672c4653dc2cde5c5fde8b44`, reproduced directly. G2 THE LEDGER APPEND (RECORD11) HELD BYTE-EXACT: base 2385806 bytes (no trailing newline), RECORD11 measured 4403 bytes with zero internal newlines, base + 1 + 4403 = 2390210 exactly matching the post-C1 file; the appended tail equals `\n` + RECORD11 byte for byte, a one-byte-flipped negative control was correctly rejected. G3 THE PROSE SLIP APPEND (PROSESLIP11) HELD BYTE-EXACT: base 69890 bytes (no trailing newline), PROSESLIP11 measured 1144 bytes with zero internal newlines, base + 1 + 1144 = 71035 exactly matching the post-C1 file. G4 THE PLAN HELD BYTE-EXACT: PLAN12 extracted from the committed authored file compares equal to `.agent/plan.md` (42 lines by `wc -l`, matching the block's own corrected prediction; `## Goal`/`## Next Steps` each exactly once). G5 THE SELF-USE GENERATION HELD, WITH ONE HARMLESS CORRECTED ILLUSTRATION AND ONE CORRECTED PREDICTION, BOTH DECLARED BY THE WORKER: constraint 5's illustrative code named a `.items` attribute `load_self_use_queue()` does not carry (the real return is a plain tuple), and the worker correctly substituted the equivalent real call (`len(load_self_use_queue())`) to perform the same precondition check rather than following broken illustrative code verbatim — reproduced independently: `next_self_use_item()` read `None` and `len(load_self_use_queue())` read 7 before the call, exactly the block's own stated precondition. `generate_and_append_if_empty()` returned `SU-008`, `consumed_by=""`, provenance `generated (self-use-generator tier 1, ledger scan, R-0418)` — matching constraint 6 exactly, and `load_self_use_queue()` read 8 items afterward. Constraint 8 predicted a FULL-FILE rewrite of `scripts/self_use_queue.json` (the open `R-0785` class); the real diff is a clean `+8/-0` append instead — reproduced independently via `git show --numstat 5d614a74 -- scripts/self_use_queue.json`. This does not contradict `R-0785`: that finding's own `ensure_ascii` escaping already ran once, at F109 R19, over the four items shipped at that time, so every item this round's re-serialization touches was ALREADY escaped and re-serializes byte-identical — a full rewrite is only visible in a diff the FIRST time it happens to a given byte range, which was three features ago. No new finding is warranted; `R-0785` remains open, unchanged, for the reason its own fix clause already names. G6 THE TREE AND THE SWEEP HELD: `git status --porcelain` and `git diff --stat 31aa76b7..5d614a74 -- packages/ apps/ tests/` are both empty, reproduced independently; every commit's numstat cells match the handback's own Commits table cell for cell. TWO DEVIATIONS ARE DECLARED (the broken illustrative code and the append-vs-rewrite correction above, neither a defect on disk); the reviewer found no others. Closure precondition 6's RUN step (SU-008 to the approval gate) is round 13's own work, not this round's. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD12>>>

<<<BEGIN PLAN13>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 13 books round 12's PASS verdict (RECORD12 - the self-use
GENERATION step, SU-008 appended) then performs closure precondition
6's RUN step: `run_next_self_use_item()` unflagged, real local
`ollama` provider, default small budget, against SU-008 (the R-0418
paragraph). Evidence (job id, provider, final status,
`describe_self_use_run_defects()` output) saved under
`.agent/selfuse_f114/`. No `consumed_by` edit yet - that is the
closure commit's own edit. No new R-id is minted this round; the
reviewer analyzes and narrates the defect-registration obligation
against the open ledger when booking THIS round's own verdict next
round (the same split F110 R16 / F112 R21 used).

## Next Steps

- Round 14: book round 13 (RECORD13, with the R-0784 evidence-addition
  narration), author T3_F114.md's Built State section (precondition
  4), run `remedy integrity check --json` (precondition 3).
- Then the closure commit: evidence job, fresh review zip, STATUS
  line, README sync, `consumed_by=F114`, the PR.
- Session note: round 13, session 3 - 4th delegated round, at the 4-5
  default; likely the session's last round before a scope check.

## Risks

- The run is a real, budget-capped LLM call against local `ollama`
  (`max_cost_usd=0.50`, `max_provider_calls=6`) - bounded, expected to
  end BLOCKED at the approval gate (the correct, safe outcome for a
  reviewer-practice finding no builder can fix in code), matching
  every prior run against R-0418 (SU-005/006/007).
<<<END PLAN13>>>
