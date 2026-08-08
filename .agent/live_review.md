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
  writer, the never-fail-the-run discipline, miss counting, unit tests.
- R3 (SPLIT): T002 — backfill and reconcile commands, idempotent by
  call_id, tests on fixture evidence.
- R4 (SPLIT): T003 — `remedy stats cost` aggregation, basis labeling,
  read-only cross-project aggregation, tests.
- R5: integration gate per docs/agents/integration_gate.md.
- R6: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- Next free ID: R-0218. Open findings: 0.

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
- R2: pending review.
