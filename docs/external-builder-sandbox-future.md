# External Builder Sandbox — Future Design Note (Step 1641)

A forward-looking note. **Nothing here is built.** It records why the Automated Local Candidate
Generator came first and what a future External Builder Sandbox must satisfy.

## Why local first

The [Automated Local Candidate Generator v0](local-candidate-generator-v0.md) is local, cheap, and
controlled: loopback-only, disabled by default, routing-gated, with all output forced through the
existing Trust Gate + Verification + Materialization + human-approval pipeline. That makes it the
safest place to introduce *automated* candidate generation.

## What an External Builder Sandbox needs (separately)

- **Separate sandbox + policy + budget.** External builders are expensive and untrusted at a
  different level; they need their own opt-in policy, isolation, and a bounded budget distinct from
  the local candidate budget and the run-contract budgets. Unknown cost must block by default
  (mirroring Builder Routing's external rule).
- **Same intake guarantees.** External output is UNTRUSTED and must pass the SAME Trust Gate +
  Provider Trust Verification before any materialization — no special-casing.
- **Routing-gated.** Only reachable when Builder Routing selects `external_candidate_generator`
  (request package + trust + verification + budget + low loop risk + no pending approval/intent).
- **No direct apply, no automatic approval, no retry loops.** Human approves; `do_continue`
  applies; repeated failure escalates to human review, never auto-retries.

## Explicit non-goals (must stay out of any v0)

No direct provider/cloud SDK execution inside Remedy without a sandbox boundary, no automatic
apply/approval/PR/merge, no background multi-cycle orchestration, no browser. The sandbox produces
candidate output that re-enters the existing pipeline — it does not gain new apply powers.
