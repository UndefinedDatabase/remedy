# Self-Dogfood Overnight — Future Direction (design note)

Design only. No unattended self-improvement runs in v0; Self-Dogfood Execution v0 is
**foreground/manual** (a human invokes each `self execute` / `self reconcile`).

## Requirements before any unattended self-improvement

- **Non-main branch only.** An overnight self run must refuse `main`/`master`/unknown
  branch for any mutation-capable phase (already enforced by the branch gate).
- **Bounded cycles only.** At most one bounded apply cycle per invocation; no
  multi-cycle loop, no daemon/scheduler/background process beyond an explicit,
  human-authorized run.
- **No auto-merge, no auto-PR.** Outputs stop at a reviewable state.
- **All outputs through the same gates.** Candidate → Provider Trust Gate →
  materialization → human approval → `do continue` → snapshot/apply/test/proof. No
  bypass, no direct apply.
- **Morning report must show every self-change**: each attempt, its state, the linked
  intent, proof status, and what still needs human approval — no silent changes.
- **Budget/token + no-cloud policy** must gate any future automated candidate
  generation (see [candidate-generator-adapter-future.md](candidate-generator-adapter-future.md)).

## Non-goals (still excluded)

Self-approval, self-merge, main mutation, provider/network/browser execution, and
treating any single provider/subscription as required.

## See also

- [self-dogfood-execution-v0.md](../system/self-dogfood-execution-v0.md)
- [bounded-overnight-executor-v0.md](bounded-overnight-executor-v0.md)
