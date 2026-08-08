# Live Review — F103 Token ledger (SQLite)

Branch: feature/f103-token-ledger
Feature file: docs/roadmap/features/T2_F103.md
Tier 2 · depends on F003 and F146 · blocks F074, F115, F116, F150 and
F158. Claimed per Rule A5 as the first `[ ]` entry in
docs/roadmap/STATUS.md after F254 was accepted.

Goal & Done, quoted from the feature file: token and cost actuals
become QUERYABLE — every provider call lands as a row in a per-project
SQLite ledger, and `remedy stats cost` answers per-job, per-role and
per-period questions from it. DONE when the writer sits in the provider
path without slowing it perceptibly, historical file-based actuals can
be backfilled once, and every cost figure names its basis.

This feature INTRODUCES SQLite to the repository — the first and so far
only place. The files stay the source of truth; the database is a
mirror, and a writer failure never fails the run.

Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md) — planner/reviewer in the main
session, one delegated worker subagent per round. Session caps declared
at R1: 8 rounds, ~4 hours wall clock. Reaching a cap with a written
handoff is a SUCCESS, not a failure.

## Steps
- R1 (SPLIT): Open PR Gate — no open PRs, nothing to merge — then the
  STATUS claim, the R-0214 closure-candidate sweep, and the reset of
  live_review, plan, context and candidates to this feature — PASS.
- R2 (SPLIT): T001 — schema, migration bootstrap, the `record_call(...)`
  writer, the never-fail-the-run discipline, miss counting, unit tests —
  PASS.
- R3 (SPLIT): T002 data layer — the call site at the actuals seam, plus
  backfill and reconcile over the evidence tree, idempotent by call_id —
  PASS.
- R4 (SPLIT): T003 — the cost aggregation queries plus `remedy stats
  cost`, `backfill-ledger` and `verify-ledger` in the existing stats
  group, with basis labeling in both output modes — PASS.
- R5: integration gate per docs/agents/integration_gate.md — PASS.
- R6 (SPLIT): wire the live ledger mirror at the task-run evidence seam
  so a real job yields rows (finding R-0220).
- R7: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- R-0218 (Low, R2, reviewer): the ledger's own acceptance criterion —
  "the writer sits in the provider path without slowing it perceptibly"
  (feature file, Goal & Done) — has no measurement anywhere. T001 could
  not have one, because it deliberately adds no call site; but
  `record_call` opens a connection, runs `PRAGMA journal_mode=WAL` and a
  schema-version check on EVERY call, and that per-call cost is now
  fixed by design rather than measured. Not a block condition: at T001
  the writer is inert, so nothing is slowed yet. Fix: R3 lands the call
  site, and R5's integration gate carries a real before/after timing of
  the seam so the criterion is met with a number instead of a claim.
- R-0219 (Low, R2, reviewer): `record_call` reports True when a row with
  that `call_id` already exists, even if the record being written
  differs from the stored one — the presence check asks "is a row
  there", not "is THIS row there". The documented contract ("True when
  the row is durable") is honest and duplicate call_ids are a caller
  bug, so this is not a defect today. It becomes one the moment T002's
  reconcile has to answer "does the ledger agree with the files": a
  content-drifted row would be invisible to a presence-only comparison.
  Fix: R3 must decide explicitly — either pin `call_id` as immutable by
  construction and say so in the docstring, or have `verify_ledger`
  compare content rather than presence. Record which, and why.
- Done: R-0219 — resolved in R3 by CONTENT COMPARISON in `verify_ledger`,
  which re-derives each row from its own evidence through the same
  `call_record_from_evidence` the live hook uses and reports field-level
  mismatches in `drifted_rows`. The reviewer confirmed the fix is
  load-bearing rather than asserted: reducing the comparison to
  presence-only in a disposable worktree turned
  `test_finds_a_content_drifted_row` red. `call_id` is ALSO pinned
  immutable by construction and documented as such, but that guarantees
  only the id, never the contents — which is why the stronger option was
  the right one.
- Done: R-0218 — CLOSED at R5 against a real number, not a claim. The
  gate measured the seam itself: `write_evidence_bundle` costs a median
  0.587 ms with the mirror inert and 1.973 ms with it active, so the
  mirror adds **+1.386 ms per finalized task run** (+236% of a very
  small baseline). The reviewer REPRODUCED it independently with its
  own harness — +1.395 ms median — and the worker's own second run gave
  +1.506 ms; three runs agree within about 0.1 ms, and a row count of
  330/330 proves arm B really inserted on every iteration rather than
  short-circuiting. Judgement: 1.4 ms once per finalized TASK RUN, on a
  path whose sibling work is a provider call measured in SECONDS, is
  not "slowing it perceptibly". The criterion is met with a number.
- R-0220 (Medium, R5, reviewer): the live mirror is never switched on,
  so the feature's own acceptance criterion — "a fake-provider job
  yields exactly its calls as rows with correct role/model/basis" — is
  NOT met by the built system. `write_evidence_bundle`'s four
  `ledger_*` arguments are the only way to arm the hook, and the ONLY
  callers that pass them are TESTS: the two production callers,
  `pingpong_evidence.py:633` and `job_evidence.py:2455`, pass none. A
  real job therefore writes ZERO rows and the ledger fills only via
  `remedy stats backfill-ledger`. R3 reviewed the hook and approved its
  inertness as caller-compatibility, which was true as far as it went;
  what nobody asked was who ever turns it on. Not a gate blocker — the
  gate is about regressions and there were none — but a CLOSURE
  blocker: flipping STATUS to `[x]` and syncing the README now would
  claim a capability that is wired and switched off. Fix: R6 arms the
  hook at the task-run seam for real jobs, with a test that drives the
  PRODUCTION path and passes no `ledger_*` argument by hand, and with
  the data-root safety of the opt-in preserved.
- R-0221 (Low, R5, reviewer): `TestAutoBuildBehavior::
  test_auto_build_runs_by_default`
  (`tests/ui_server/test_dashboard_contract.py`) pops
  `REMEDY_UI_NO_AUTO_BUILD` from the environment and calls
  `_auto_build_frontend()` for real, so it runs `npm install` and
  `npm run build` in whatever checkout it is running in. The env var
  cannot suppress a call that deletes it first. This is the R-0169
  class recurring with a NAMED cause. It costs every integration gate
  seven phantom base-only failures: `_frontend_is_stale()`
  (`ui_server.py:2748`) is a pure MTIME comparison, `git worktree add`
  writes src at checkout time while `cp -a` preserves the older dist
  mtimes, so a fresh base worktree is stale by construction. The R5
  gate proved the mechanism with a negative control — moving the dist
  mtimes back reproduced all seven failures without changing one byte,
  restoring them made 42 pass. NOT F103's code and NOT this feature's
  to fix: registered as a closure candidate for the owning feature.
- Next free ID: R-0222. Open findings: 1 (R-0220, Medium). R-0218 and
  R-0219 are closed; R-0221 is carried in `.agent/candidates.md`.

## Decisions
- D15 (F254 closure candidate R-0214, resolved inline per
  docs/agents/planner_reviewer_prompt.md §4 item 7): the AGENTS.md
  handoff line cap gains a STATED-CAUSE OVERAGE clause; the mandated
  handback content is NOT shrunk. Chosen because the cap has now been
  overridden by every handback whose content was entirely mandated —
  S1+S2 R2, F254 R3 at 119 lines, F254 R4 at 122, F254 R12 at 82 —
  including one round whose step block explicitly forbade verbatim
  transcripts, which rules out worker verbosity as the cause. A rule
  that every compliant handback must break is not a rule. Alternatives
  considered: shrinking the mandated content, which would delete the
  evidence set, the pair proofs or the item-status table — the exact
  artifacts the review loop exists to read, and the F056 candidate loss
  shows what dropping a carrier costs; or leaving the cap
  advisory-in-practice, which keeps every future handback nominally
  non-compliant and teaches agents that stated caps are decorative. How
  to reverse: delete the added paragraph from the AGENTS.md handoff.md
  section — it is additive and self-contained, and the original cap
  sentence is untouched by construction. Landed in its OWN commit,
  separate from the feature claim, so the rules change stays reviewable
  apart from F103: the D12 objection to mixing an unrelated fix into a
  feature branch is answered by commit granularity, and the placement
  itself is mandated by docs/roadmap/STATUS_closure_protocol.md, which
  requires the next feature's first reviewed round to resolve the
  candidate and empty `.agent/candidates.md` in that same round.
- D16 (row granularity, reviewer, per
  docs/agents/planner_reviewer_prompt.md §4 item 7): a ledger ROW is one
  FINALIZED TASK RUN, not one HTTP request, and its `call_id` is the
  deterministic `"<job_id>:<task_id>"`. Chosen because the feature file
  says the writer "consumes the same records the actuals feature
  produces", and what that feature actually puts on disk is
  `task_runs/<task_id>/provider_evidence.json` — a per-task-run record
  carrying `provider_call_count` and aggregated usage counters. There is
  no per-HTTP-request record anywhere on disk to backfill from.
  Alternatives considered: synthesising one row per counted provider
  call, which would fabricate `call_id`s, timestamps and a usage split
  that no file records — exactly the invented data P6 and the F075
  tokens-unmeasured lesson forbid; or adding a per-request capture at
  the provider boundary, which is the SECOND CAPTURE PATH the feature
  file's Orchestrator brief rejects outright. How to reverse: when a
  per-request evidence record exists on disk, change
  `call_id_for_task_run` and the backfill scan to read it; the schema
  already carries `call_id` as the primary key and needs no migration.
  The feature file is amended in this same round so the built state and
  the target plan do not disagree.

- D17 (R5, reviewer, per docs/agents/planner_reviewer_prompt.md §4
  item 7): closure MOVES from R6 to R7 and R6 becomes the round that
  arms the live ledger mirror. Chosen because R-0220 shows the feature
  does not meet its own acceptance criterion — a real job produces no
  rows — and closing on that would be an unverified completion claim,
  the exact block-condition class the review loop exists to catch.
  Alternatives considered: closing now and filing the wiring as a
  follow-up feature, rejected because F103's Goal & Done is explicit
  that the writer sits in the provider path and every call lands as a
  row, so the follow-up would be F103 itself under another name; or
  amending the feature file to declare the mirror deliberately opt-in,
  rejected because nothing in the file, the design or DECISION D16
  hints at that intent and the acceptance criterion contradicts it.
  Reversal: any later relay may drop R6 and go straight to closure by
  amending the feature file's Acceptance instead — the cost of that
  choice is that `remedy stats cost` answers only for ledgers someone
  remembered to backfill by hand.

## Verdicts
- R1 (SPLIT) — **PASS**. Reviewed `c1c0fbcb..28781d8f` bottom-up, and
  the reviewer re-ran every verification command itself instead of
  reading the worker's numbers. The diff is exactly the mandated
  13-path set across three commits — no production code, no stray path,
  `git add -A` never used. AGENTS.md **+11/-0**, purely additive, the
  clause sitting inside the handoff.md section directly after the cap
  paragraph with the original cap sentence untouched, so the declared
  APPEND shape is real and not a rewrite in disguise. STATUS.md 315
  lines before and after, one line swapped; `[~]` markers in the whole
  file **1**; F103 appears exactly once. Reviewer-run transport proof:
  `cmp` of each target against its committed receipt —
  `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md`,
  `.agent/candidates.md` — **exit 0 x4**, and receipts 4, 5 and 6 were
  read back byte-for-byte against the authored originals.
  Reviewer-run verification: `tests/docs/` **294 passed**, the
  state-contract trio (dashboard, test_runner, resource_safety) **142
  passed**, canary `tests/cli/test_golden_path.py` **42 passed**,
  `git status --porcelain` empty, branch in sync with
  `origin/feature/f103-token-ledger`, `gh pr list --state open` still
  `[]`. Every number matched the handback's, so nothing was taken on
  trust and nothing had to be corrected. Verification tier: ROUND GATE
  plus the docs-round gate and the canary — NOT the full suite. No
  block condition present. The three declared deviations are accepted:
  the 100-line handoff is the first written under the very clause this
  round added and drops no section; `.agent/decisions.md` was correctly
  left alone as outside the path set; and a commit cannot table its own
  SHA. No finding. Next free ID stays R-0218.
  LAST_REVIEWED_SHA = `28781d8f`.
- R2 (SPLIT, T001) — **PASS**. Reviewed `28781d8f..c3a03076` bottom-up.
  Diff is exactly the 7-path set: the module, its tests, live_review,
  plan, handoff and two receipts — no stray path, no dependency change
  (`git diff` over pyproject/requirements/setup is EMPTY), bundled
  `sqlite3` only, and NO call site, so the no-second-capture-path
  invariant holds. The mandated docstring sentence is present verbatim:
  "The file evidence remains the source of truth and the database is a
  mirror." Migrations are numbered steps keyed off a `meta` row, not an
  if-ladder; the three covering indexes the feature names all exist;
  `CallRecord` field order matches `_CALL_COLUMNS` exactly; unmeasured
  calls land as NULLs with basis `unknown` and `cost_usd` stays NULL, so
  no price is invented. Reviewer-run verification:
  `tests/orchestration/test_token_ledger.py` **18 passed**, the
  state-contract trio plus the canary **184 passed** (142 + 42),
  `git status --porcelain` empty with no stray `.sqlite`/`-wal`/`-shm`.
  Every number matched the handback's. MUTATION RED-PROOF, run by the
  reviewer in a disposable `git worktree` under the gitignored
  `.remedy-wt/` and removed before this verdict (`git worktree list`
  shows the primary checkout only): (1) making `record_call` re-raise
  instead of returning False turned **5 tests red**, so the never-fail
  rule the Orchestrator brief demands is genuinely pinned and not merely
  asserted; (2) deleting the `rowcount`/constraint guard turned
  `test_rejected_basis_is_a_counted_miss_not_a_silent_drop` red, so the
  worker's `INSERT OR IGNORE` ambiguity fix is load-bearing rather than
  decorative. The worker's two flagged design points are both accepted:
  `INSERT OR IGNORE` does swallow CHECK and NOT NULL rejections exactly
  as it swallows a duplicate key, so asking the table which case
  occurred is correct and not defensive noise; and `kw_only=True` is
  what makes the mandated field order expressible with `ts_utc`
  required. Verification tier: ROUND GATE plus the canary — NOT the full
  suite. No block condition. The declared deviations are accepted: four
  commits instead of three is the step block's own instruction (split
  rather than claim an oversize exception) and no commit exceeded 500
  lines; the 121-line handoff drops no section and states its cause.
  Two findings registered, both Low: R-0218 and R-0219.
  LAST_REVIEWED_SHA = `c3a03076`.
- R3 (SPLIT, T002 data layer) — **PASS**. Reviewed
  `c3a03076..d2bc7d8e` bottom-up. Diff is exactly the 10-path set across
  six commits, no commit over 500 lines, no dependency change, and
  `token_truth.py` is BYTE-UNCHANGED — the no-second-capture-path
  invariant holds by import rather than by promise. The reviewer checked
  the three things a summary could most easily have got wrong, and all
  three hold: `actual_cache_read_tokens` and
  `actual_cache_creation_tokens` are the real canonical keys in
  `token_truth._ACTUAL_ALIASES`, so the cache counters are genuinely
  mapped and not silently always-None; `_strict_cost` really does return
  None for an absent figure and raise on a malformed one, so
  `cost_basis` becomes `provider_reported` only when a real number is
  present; and the model fallback `("model", "builder_model")`
  deliberately excludes `builder_configured_model` and
  `reviewer_configured_model`, so the docstring's claim that a
  configured model is never used as the model that ran is true of the
  code. The call site is correct: four keyword-only `ledger_*` arguments
  all defaulting to None keep every existing caller bit-for-bit
  unchanged, the hook is inert without a target or ids, it never
  resolves a project implicitly, it is wrapped so nothing escapes, and
  it re-reads the file it has just written through the ledger's own
  builder — one producer, which is exactly what makes content
  comparison sound. `backfill_ledger`'s
  `scanned == recorded + skipped + failed` holds on every path,
  including the defensive one. Reviewer-run verification:
  `test_token_ledger.py` **50 passed**, `tests/docs/` **294 passed**,
  the `pingpong or evidence` regression selection **1129 passed, 14926
  deselected**, the state-contract trio plus the canary **184 passed**,
  `git status --porcelain` empty with no stray `.sqlite`/`-wal`/`-shm`.
  Every number matched the handback's. MUTATION RED-PROOF in a
  disposable worktree under the gitignored `.remedy-wt/`, removed before
  this verdict: reducing `verify_ledger` to presence-only turned
  `test_finds_a_content_drifted_row` red, so R-0219's fix is real.
  DECISION D16 and the feature-file amendment landed together, so the
  target plan and the built state do not disagree; the amendment is
  purely additive (+15/-0). Verification tier: ROUND GATE plus the
  docs-round gate and the canary — NOT the full suite. No block
  condition. Declared deviations accepted: six commits not five, on the
  step block's own instruction to split rather than claim an oversize
  exception; the 152-line handoff drops no section and states its cause.
  R-0219 closed; R-0218 stays open for R5.
  LAST_REVIEWED_SHA = `d2bc7d8e`.
- R4 (SPLIT, T003 + T002 surface) — **PASS**. Reviewed
  `d2bc7d8e..25c343d0` bottom-up across seven commits, none over 500
  lines, no dependency change. The P6 rule is the heart of this round
  and it holds in code, not only in prose: there is no `COALESCE`
  anywhere in the queries — the single occurrence of the word is a
  docstring explaining why it is absent — so `SUM()` over all-NULL stays
  NULL and an unmeasured figure never renders as a measured zero. The
  reviewer MUTATION RED-PROOFED exactly that, in a disposable worktree
  under the gitignored `.remedy-wt/`, removed before this verdict:
  wrapping all seven `SUM(...)` in `COALESCE(..., 0)` turned **7 tests
  red** across BOTH layers — `test_an_all_unmeasured_bucket_reports_none_not_zero`,
  `test_an_all_unmeasured_total_reports_none_not_zero`,
  `test_a_cache_counter_nobody_reported_stays_none`,
  `test_two_ledgers_add_up_without_inventing_a_zero`, and three
  basis-labeling tests in the CLI suite. The rule is pinned, not
  asserted. `_connect_readonly` is the round's best judgement call and
  it is correct: `mode=rw` plus `PRAGMA query_only=1` refuses to create
  a database and rejects every write at the driver, while avoiding the
  `mode=ro` trap where a read that cannot checkpoint the WAL leaves
  `-wal`/`-shm` sidecars beside every ledger it merely looked at — a
  read that litters the data root is not read-only. The `COUNT(CASE …)`
  versus `SUM(…)` asymmetry is right for the same P6 reason: a count of
  nothing is honestly 0, a sum of nothing is not. Reviewer-run
  verification: `test_stats_cost.py` + `test_token_ledger.py` **105
  passed**, the whole `tests/cli` catalog/registry contract guard
  **1329 passed in 259s**, the state-contract trio plus the canary **184
  passed**, `git status --porcelain` empty with no stray
  `.sqlite`/`-wal`/`-shm`. Every number matched the handback's.
  The one out-of-path-set edit is DECLARED, minimal and correct, so it
  is not a silent scope change and not a block condition:
  `tests/cli/test_failure_cmd.py` asserted the `stats` group's EXACT
  contents (`== ["stats.failures"]`), which no longer holds once the
  group legitimately grows; it is weakened to a membership assertion
  with F010's own claim intact and a comment saying why. Leaving it red
  was not an option the step block allowed. Verification tier: ROUND
  GATE plus the canary — NOT the full suite; R5 owns that claim. No
  block condition. Deviations accepted: seven commits rather than five,
  on the step block's own split-over-oversize instruction; the extra
  helpers (`merge_cost_reports` and friends) belong in the data layer
  precisely because the block said the CLI only renders.
  LAST_REVIEWED_SHA = `25c343d0`.
- R5 (integration gate) — **PASS**. Reviewed `e984bbab..af91d57b`
  bottom-up: four commits, none over 500 lines, and the change set is
  `.agent/` only — no production code and no test file, exactly as the
  round required. The gate's central claim is REPRODUCED, not accepted:
  the reviewer re-ran the full suite itself and got **16121 passed, 19
  skipped, exit 0**, matching the handback's numbers exactly, with zero
  `FAILED` lines. Branch-only ids: **0**, so nothing can block under
  integration_gate step 4. Base-only ids: 8, every one attributed by
  DIRECT evidence — 1 xdist port race (`OSError: Errno 98` in the base
  log, serial-pass 4 of 4) and 7 sharing one cause. That attribution is
  the round's best work: it is proved by a NEGATIVE CONTROL, which is
  what separates evidence from a story. `_frontend_is_stale()`
  (`ui_server.py:2748`) compares MTIMES; setting the base worktree's
  dist mtimes back behind `apps/ui/src` reproduced all seven failures
  with the dist CONTENT hash unmoved, and restoring them turned the
  file green at 42 passed. The reviewer read both cited sources and
  confirms the mechanism holds in code. Parity by content holds
  (`fb68a729…` before == after); the round declares plainly that the
  neutralization is nonetheless NOT clean and names the writer, rather
  than claiming a pass — that honesty is registered as R-0221. R-0218
  is PAID and CLOSED: see the finding entry, including the reviewer's
  own independent reproduction. Declared deviations accepted: the
  scratchpad and base worktree sat under the gitignored `.remedy-wt/`
  rather than `/tmp` because this session's permission policy refuses
  every write outside the repo — the reviewer HIT THE SAME BLOCK and so
  corroborates the cause, and R-0176's substance was verified rather
  than assumed (`git ls-files --others --exclude-standard`, which
  `run_manifest.py:500` is the digest's untracked input, returns 0
  hits); three evidence commits rather than two, to stay under the
  500-line cap without claiming an exception; the 120-line handoff
  drops no section and states its cause. Verification tier:
  INTEGRATION GATE — this entry is the one place the "full suite green"
  claim may be made, and it is made on the reviewer's OWN run. No block
  condition. The gate did not, however, ask whether the feature's live
  path is armed at all, which is how R-0220 stayed invisible until this
  review; that is a lesson about gate scope, not a defect of this round.
  LAST_REVIEWED_SHA = `af91d57b`.
- R6: pending review.
