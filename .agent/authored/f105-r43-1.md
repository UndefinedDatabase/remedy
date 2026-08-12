── STEP R43 (SESSION CLOSE) — F105 ───────────────────────────
Goal:        Persist the R42 reviewer gate, register the two findings the T004
             inventory surfaced (R-0265, R-0266), record DECISION F105 D14 —
             which answers all five of the inventory's open questions and sets
             T004's honest scope — and close the session with a handoff that a
             fresh session can resume from without re-deriving any of it.
Bundle:      C1 save this block · C2 every `.agent/live_review.md` edit ·
             C3 `.agent/decisions.md` · C4 plan and closing handoff.
Change:      `.agent/authored/f105-r43-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else.
             NO production code, NO test files, NO `docs/`: state only.
Constraints: This is a CLOSING round: apply these pairs, commit, push, and
             stop. Do NOT start T004, do NOT create `.agent/STOP`, do NOT
             create a PR, do NOT merge anything, do NOT touch `main`. Open PR
             #189 (`docs/amend0810-clerical` -> `main`) is NOT a `feature/*`
             branch, so the AGENTS.md Open PR Gate makes it stop-and-report and
             this session leaves it untouched — say so in the handoff. Write no
             `Done:` paragraph of your own (§4.4).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r43-1.block.md`
      `.agent/authored/f105-r43-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — `.agent/live_review.md`, ONE commit
  Apply PAIR_ID (REWRITE, the header's next-free-ID line), PAIR_F
  (CONTAINS-FROM, R-0265 and R-0266 appended at the end of `## Findings`) and
  PAIR_S (CONTAINS-FROM, the R42 gate record plus the R43 step line at the END
  of the file). All three share ONE path in ONE commit: reconcile them TOGETHER
  against that commit's `git show -U0`.

C3 — `.agent/decisions.md`, ONE commit
  Apply PAIR_DEC, a CONTAINS-FROM append at the very END of the file.

C4 — plan and closing handoff, ONE commit
  Apply PAIR_P_PLAN to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` in your own words per AGENTS.md as the SESSION-CLOSING
  handoff: branch, the commit SHAs, the changed-files table, the gate table
  with real exit codes, the open-findings count, the state of PR #189, and the
  exact first action for whoever resumes this branch.

<<<PAIR_ID_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0265.
<<<END_PAIR_ID_FROM>>>

<<<PAIR_ID_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0267.
<<<END_PAIR_ID_TO>>>

<<<PAIR_F_FROM>>>
  authored and none should be.
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
  authored and none should be.

- R-0265 (Medium, F105 R42, pre-existing, registered NOT fixed): a provider that
  reports usage but no cache field is recorded as a measured ZERO, not as
  "nothing reported". `packages/orchestration/token_actuals.py:110` reads
  `int(usage.get("cache_read_input_tokens", 0) or 0)`, so an absent key and a
  reported 0 land in the same int, and everything downstream — the ledger, and
  any `remedy stats cache` view built on it — loses the distinction the whole
  `unmeasured` vocabulary exists to preserve
  (`apps/cli/commands/stats_ledger_cmd.py:44`). This repository's own rule is
  that a bucket nobody reported prints a WORD and never the digit 0; here the
  digit is manufactured one layer below the printer, so the printer cannot obey
  it. Verified by the reviewer against source, not the inventory: the `or 0`
  collapse is on that line as described. Registered rather than fixed because
  it is pre-existing, it belongs to the token-actuals feature and not to prompt
  composition, and fixing it means changing a field's type from `int` to
  `int | None` with every reader audited — a round of its own, and not one F105
  should absorb. Cost today: bounded and invisible, which is what makes it
  worth writing down. OPEN.

- R-0266 (Medium, F105 R42, pre-existing, registered NOT fixed): the ledger's
  `role` column cannot distinguish roles today. It is populated from exactly one
  key (`packages/orchestration/token_ledger.py:1017`,
  `role=_first_string(accounting, ("role",))`) and its only production producer
  writes the constant `"role": "builder"`
  (`packages/orchestration/pingpong_loop.py:3970`), so every real row says
  `builder` whatever ran; the `reviewer` bucket a grouped view can show exists
  only in hand-written test fixtures. Compounding it, the `intake`,
  `flight_plan`, `orchestrator` and `mission_plan` trace sites pass no
  `job_id`/`task_id` and produce NO ledger row at all, because rows are built
  only from `task_runs/<task_id>/provider_evidence.json`. A genuine per-role
  cache-read aggregate IS computed (`pingpong_loop.py:3598-3698`, `by_role`) but
  reaches `token_accounting.json` only and is never copied into
  `provider_evidence.json`. Verified by the reviewer against source at three of
  those pointers, not accepted from the inventory. This is the gap DECISION D14
  rules on: T004 renders what the ledger carries and NAMES the gap rather than
  inventing a role for a call. OPEN.
<<<END_PAIR_F_TO>>>

<<<PAIR_S_FROM>>>
  T004 needs before any `remedy stats cache` code exists. No production code.
<<<END_PAIR_S_FROM>>>

<<<PAIR_S_TO>>>
  T004 needs before any `remedy stats cache` code exists. No production code.
- Reviewer gate on R42 (2026-08-10): PASS, no deviation beyond the declared
  handoff overage. Range `87ef21d9..1fc4c62c` = five commits, six paths, every
  one under `.agent/`; nothing under `packages/`, `apps/`, `tests/` or `docs/`,
  which is what an investigation round must prove about itself.
  Insertions per commit 280, 198, 70, 259 and 90, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r42-1.block.md`, the
  committed `.agent/authored/f105-r42-1.md` and `.agent/last_block.md` all
  three hash to
  `dc7dd7021699a9b83601c38a25ecfb6c1be906bb8bd1121cc23fd64e545431a4`
  at 280 lines against D5's cap of 400; both `cmp` runs silent.
  The three authored `Done:` texts were read line by line in the applied file
  and are byte-identical to their slices; both worker-authored unreviewed-fix
  markers are gone, counted at 0 and 0, so none survived its own resolution.
  Gates re-run by THIS reviewer, none taken from the handback: `tests/docs/`
  `294 passed in 0.25s`; `test_dashboard_contract.py` `70 passed in 3.91s`; the
  canary `42 passed in 19.94s`; the transport marker count 0 in all four
  touched text files; `.agent/plan.md` 42 lines against the cap of 50.
  The inventory was NOT accepted on its own word: three of its `path:line`
  pointers were opened and read independently — `token_ledger.py:1017` is the
  `role=_first_string(accounting, ("role",))` line, `pingpong_loop.py:3970` is
  the hardcoded `"role": "builder",`, and `token_actuals.py:110` is the
  `or 0` cache-read collapse. All three say what the inventory says they say.
  Those readings are now registered as R-0265 and R-0266.
  `LAST_REVIEWED_SHA` advances 87ef21d9 -> 1fc4c62c.
- R43: SESSION CLOSE — persist the R42 gate, register R-0265 and R-0266, record
  DECISION F105 D14, and stop. No production code. This session ends here with
  T004 unstarted but fully scoped; the next session opens with T004 slice 1.
<<<END_PAIR_S_TO>>>

<<<PAIR_DEC_FROM>>>
Reverse this decision by threading the label through `GauntletDeps` and passing
it at that call site.
<<<END_PAIR_DEC_FROM>>>

<<<PAIR_DEC_TO>>>
Reverse this decision by threading the label through `GauntletDeps` and passing
it at that call site.

D14 — T004 renders the cache-read share the ledger ACTUALLY carries, names the
gap, and does not fix the producer. This answers all five open questions at the
end of `.agent/t004_inventory.md`, which the R42 investigation raised and which
no later round should re-derive.

Q1, the role column: NO, T004 does not fix
`packages/orchestration/pingpong_loop.py:3970` first. F105's goal is prompt
COMPOSITION; rewriting who writes a role into token accounting is a different
feature's change and would put an unreviewed producer edit under a prompt
feature's PR. The view therefore reports per role over what the ledger holds and
states, in its own output, that production rows currently carry one role. A
reader learns the truth including its limit — which is this repository's rule for
every figure it prints.

Q2, one row per task run: MOOT under Q1 and deliberately left so. No row splits,
no role becomes a list, and the view does NOT reach into
`token_accounting.json`'s `by_role` behind the ledger's back. The ledger is the
mirror this surface reads (stats_ledger_cmd's own stated contract); adding a
second, richer path for one subcommand would give the same question two answers.

Q3, fixtures: the evidence-tree-backfilled shape
(`tests/cli/test_stats_cost.py:121`), NOT the directly-written ledger
(`tests/orchestration/test_token_ledger.py:909`). Only the first exercises the
producer path, and a fixture that skips the producer would render green over
exactly the gap R-0266 names.

Q4, the measured-zero collapse: YES, a finding against the actuals feature —
registered as R-0265, not worked around inside T004. A workaround inside the
view would be a second place where "reported 0" and "not reported" are guessed
apart, and the guess would be invisible.

Q5, vocabulary: the EXISTING word `unmeasured`
(`apps/cli/commands/stats_ledger_cmd.py:44`). One spelling per concept
(AGENTS.md, Code Discoverability Conventions); the feature file's phrase "not
reported" is prose describing that word, not a second one to introduce.

The alternative considered and rejected for now: fix the producer inside T004 so
the per-role figure is real. It is the RIGHT eventual fix and R-0266 records it
as such; it is rejected HERE because it is a token-accounting change that would
ride into a prompt-composition PR unreviewed by anyone reading that PR's title.

Reverse this decision by deleting this entry and re-scoping T004 to include the
producer fix, with R-0266 closed in the same round.
<<<END_PAIR_DEC_TO>>>

<<<PAIR_P_PLAN>>>
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
SESSION CLOSED at R43, cleanly and not against a STOP file. T001, T002 and T003
are DONE and gated. R42 is GATED PASS; `LAST_REVIEWED_SHA` is 1fc4c62c. T004 is
the only slice left and is now fully scoped: `.agent/t004_inventory.md` is its
ground truth and DECISION F105 D14 answers all five of its open questions.
Open findings: R-0221, R-0239, R-0247, R-0262, R-0265, R-0266.
No PR; one is created at CLOSURE.

## Next Steps
- T004 slice 1 under D14: `remedy stats cache` beside `remedy stats cost` in
  `apps/cli/commands/stats_ledger_cmd.py`, cache-read share per role read from
  the ledger, `unmeasured` and never `0` where nothing was reported, and output
  that names the R-0266 limit instead of hiding it. Fixtures take the
  evidence-tree-backfilled shape (`tests/cli/test_stats_cost.py:121`).
- Then the before/after comparison note in the feature's evidence, with honest
  numbers whatever they are (the feature file's T004 line).
- Then the integration gate (docs/agents/integration_gate.md); R-0221 will
  attribute phantom base-only failures there and that is expected, not new.
- Then closure (docs/roadmap/STATUS_closure_protocol.md), where the evidence
  job, the FRESH review zip, the STATUS line and the PR all land.

## Risks
- PR #189 (`docs/amend0810-clerical` -> `main`) is open and is NOT a `feature/*`
  branch, so the Open PR Gate makes it stop-and-report. It blocks no work on
  this branch but must be resolved by the operator before a NEW branch is cut.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262, R-0265 and R-0266 stay OPEN and out of scope for F105 by design.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code in the handback

A transport
  `sha256sum .remedy-wt/f105-r43-1.block.md .agent/authored/f105-r43-1.md
  .agent/last_block.md` — all three EQUAL; two `cmp` runs, both silent.

B size
  `wc -l .agent/authored/f105-r43-1.md` against the cap of 400 (D5).

C pair shapes, MEASURED not assumed
  Slice every pair from the COMMITTED `.agent/authored/f105-r43-1.md` with a
  whole-line marker reader; never retype. Verify FIRST that every FROM occurs
  exactly 1x in its target before its write, and STOP if one does not. Then:
  PAIR_ID is a REWRITE — FROM 0x, TO 1x after the write. PAIR_F, PAIR_S and
  PAIR_DEC are CONTAINS-FROM — FROM 1x, TO 1x. PAIR_P_PLAN: `cmp` the applied
  `.agent/plan.md` against the slice, `wc -l` against the cap of 50.
  A declared shape that does not equal the measured shape is a STOP. No pair
  this round writes into another pair's TO region.

D added-line reconciliation for C2 and C3
  For each commit run `git show -U0 <commit>`: every ADDED line appears in some
  TO of that commit, every REMOVED line is a FROM. Both stray counts must be 0
  for both commits.

E marker leakage
  The transport-marker count at line start is 0 in `.agent/live_review.md`,
  `.agent/decisions.md`, `.agent/plan.md` and `.agent/handoff.md`. Report the
  numbers, not the word.

F state-file contracts
  `python3 -m pytest tests/docs/ -q` and
  `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  `.agent/plan.md` keeps `## Goal` and a `Steps` substring;
  `.agent/live_review.md` keeps exactly one `## Steps` heading.

G no production drift
  `git diff --name-only 1fc4c62c..HEAD` lists ONLY these six paths:
  `.agent/authored/f105-r43-1.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
  `.agent/handoff.md`. Report the list. Nothing under `packages/`, `apps/`,
  `tests/` or `docs/`.

H canary
  `python3 -m pytest tests/cli/test_golden_path.py -q`.

I hygiene
  `git status --porcelain` EMPTY. `git worktree list` shows the primary ALONE.
  `.agent/STOP` absent. Per-commit insertions each under 500 via
  `git show --numstat`.

J the gate is left open, on purpose
  Do NOT write a gate record for R43 itself. R43 is the last round of this
  SESSION, so its verdict lives in `.agent/handoff.md` and the session's
  completion report; the NEXT session gates it as an ordinary handback. That is
  the R-0264 distinction, now on disk: §4.13's terminator belongs to the last
  round of a BRANCH, not of a session. State this explicitly in the handoff so
  no reader mistakes the absence for an oversight.

No mutation red-proof is ordered and none is to be run: nothing executable
changes, so there is no branch to mutate (D8 item 5, DECISION F105 D10).

Handback: completion report + rewrite `.agent/handoff.md` (changed-files table,
item-status table for C1a/C1b/C2/C3/C4, the gate table with real exit codes, the
transport and pair proofs, the open-findings count, the state of PR #189, and
the exact first action for whoever resumes). Then `git push` and STOP — no
further rounds, no PR.
──────────────────────────────────────────────────────────────
