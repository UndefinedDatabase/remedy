# Candidate Generator Adapter — Future Direction (design note)

> **Status: DEPRECATED** — Built as `docs/system/local-candidate-generator-v0.md`.
> Kept for historical context.

This note records WHY automated external candidate generation is deferred and HOW a
future adapter must work. It is design only — no such adapter executes in v0.

## Why direct external execution is deferred

- Remedy must stay provider-/worker-/model-/subscription-/IDE-/account-**agnostic**.
  No single provider may become required infrastructure.
- Any external generator output is **untrusted** and must pass the same Trust Gate as
  human-pasted output — building execution before the trust boundary is proven is
  unsafe.
- Network/SDK/subprocess/browser execution introduces secret-handling, budget, and
  no-cloud-policy concerns that are not yet modeled.

## How future adapters reuse the existing boundary

A future automated adapter implements `CandidateGeneratorAdapter`:

1. `build_request()` — reuses the **same** `build_repair_request_package` (no special
   request path).
2. `execute()` — produces candidate output and writes it to a local file (no other
   side effects).
3. The output re-enters through whatever untrusted-intake path exists at the time.
   There is none today: F275 T001 deleted the Provider Trust Gate and its intake
   command, so an executing adapter would first have to build a replacement
   (R-0866). The adapter never applies, approves, or bypasses a gate.

## Requirements before any executing adapter ships

- **RunContract actions**: a distinct executing action (e.g. `provider_execute_candidate`)
  that is denied by default and separate from `prepare_repair_request`. The former
  intake/materialize actions were deleted with the trust gate (F275 T001).
- **Budget/token tracking**: per-run token + cost accounting wired into RunContract /
  RunUsage; execution blocked when budget is exhausted.
- **No-cloud / provider policy**: honor `no_cloud` and a local-first model policy;
  cloud calls remain `CLOUD_PROVIDER` (denied by default).
- **Provider output trust verification**: a stronger trust verification step (v1) on
  top of the regex scanning used today, since automated volume raises the cost of a
  missed novel secret format.
- **Explicit, foreground, human-invoked** execution only — never a daemon, scheduler,
  or background loop.

## Non-goals (still excluded)

Browser automation, account automation, IDE invocation, auto-approval, auto-apply,
and treating any single provider/subscription as required.

## See also

- [repair-request-builder-v0.md](../system/repair-request-builder-v0.md)
- [provider-patch-materialization-v0.md](../system/provider-patch-materialization-v0.md)
