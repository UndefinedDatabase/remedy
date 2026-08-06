# Self-drive package — plan0806 (2026-08-06, operator-relayed)

Planning output only. Build sequenced AFTER F080 closes.

Operator constraint (verbatim): from 2026-08-13 the operator reaches
this machine ONLY via SSH from a phone. Starting Claude Code and
invoking ONE skill must be the only required touchpoint. Target:
operational and rehearsed by 2026-08-12.

## S1 — New skill /build-remedy-self

Home and conventions: `.claude/skills/`, the seven existing remedy-*
skills. It runs the Window-1 discipline end-to-end in one session:

- (a) deterministic state probe — git status/branch, the F080
  machine-readable roadmap mirror, .agent/handoff.md, candidates.md,
  open PRs, tests/docs + canary;
- (b) decide: next feature per STATUS order, OR review the last state
  and emit+execute a repair if something is off;
- (c) run rounds exactly as today, except the worker blocks execute
  in-session instead of being relayed by the operator; reviewer
  discipline and gates unchanged.

## S2 — Hard guardrails (written into the skill)

- PR-only — merges happen ONLY at the Open PR Gate exactly as today.
- Never force-push.
- Every commit's gates run explicitly.
- If `.agent/STOP` exists, or a session limit is reached
  (rounds/wall-clock cap the skill states up front), or ANY ambiguity
  or red gate appears that the rules don't resolve: write the
  mission/feature handoff (F079 machinery), end cleanly, never guess.
- A session that ends by limit is a success with a handoff, not a
  failure.

## S3 — Delegation ladder

- Default worker is the in-session agent.
- Delegation of suitable small tasks to Remedy's own loop
  (`remedy do run`) is a marked EXPERIMENT lane per order, with the
  F075 experiment-override rules — this is the F082 on-ramp, not a
  replacement for it.
- ADR-0001 application is a prerequisite for multi-cycle loop
  delegation; the plan carries "awaiting human" until the operator
  applies it.

## S4 — Rehearsal is part of done

The skill's acceptance is one full feature built through it with the
operator present — F254 is the designated rehearsal feature (small,
docs+code+doctor). Success = F254 accepted through the skill with
zero operator edits beyond starting it.

## S5 — Remote review stays available

The review-zip command remains the operator's window; nothing in the
skill may assume the operator can paste anything beyond the single
start command.

## Sequence

F080 (R1 sweeps the three candidates: R-0200, R-0202, xdist flake)
-> S1+S2 skill build -> S4 rehearsal on F254 -> normal feature flow
through the skill.

## Round shapes & estimated runtime

| Step | Shape | Est. runtime |
|------|-------|--------------|
| F080 | R1 build + candidate sweep; R2 review/repair; R3 closure | 3 rounds, ~45–90 min each |
| S1+S2 skill build | R1 draft skill + guardrails + dry-run state probe; R2 review + repair + gates | 2 rounds, ~30–45 min each |
| S4 rehearsal | one supervised session: F254 end-to-end through the skill | 1 session, ~60–120 min |
| Buffer before 2026-08-12 | repair round if rehearsal surfaces findings | 1 round, ~30–60 min |
