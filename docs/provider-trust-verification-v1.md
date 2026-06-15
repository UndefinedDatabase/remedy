# Provider Trust Verification v1 (Steps 1537–1572)

A **second-stage** safety check on UNTRUSTED external candidate output, layered on top of
the [Provider Trust Gate v0](provider-trust-gate-v0.md). Where the Trust Gate answers
*"is this candidate SAFE to ingest?"*, Verification answers *"is this candidate
PLAUSIBLE, RELEVANT, BOUNDED, and WORTHY of becoming a pending repair intent?"*

## Trust vs. Verification vs. Approval vs. Apply

| Stage | Question | Module |
|---|---|---|
| Trust Gate | Safe to ingest? (no secrets, no protected paths, parseable, linked) | `provider_trust.py` |
| **Verification** | Plausible / relevant / bounded / worthy? | `provider_trust_verification.py` |
| Approval | Does a human approve the pending intent? | `approval_queue` / `patch approve` |
| Apply | Snapshot → apply → test → proof | `do continue` |

**`accepted ≠ verified ≠ approved ≠ applied`.** A passing verification only marks a
candidate *eligible* for materialization into a pending, approval-gated intent. Nothing is
applied, approved, or tested by verification.

## Flow

```
quarantine (raw, private 0o600)
  → trust report            (provider_trust)
  → verification report     (provider_trust_verification)   ← NEW in v1
  → materialization         (only if verification PASSED)
  → pending repair intent   (only if verification PASSED)
  → approval_required       (human)
  → do continue             (apply, separate)
```

In `intake_provider_repair`, verification runs **between** trust-accept and
materialization (`_verification_allows_materialization`). An accepted-but-not-passing
candidate creates **NO intent**; the verification report carries the safe outcome and a
catalog-backed next action.

## Why a candidate may be safe yet bad

A candidate can pass the Trust Gate and still be: the wrong problem, touching irrelevant
files, overclaiming that it applied/tested/fixed, unlinked to the failure / self item, too
broad, low-confidence, a repeated failed idea, or inconsistent with the request
constraints. Verification catches these with deterministic checks.

## Checks (deterministic)

- **Request/candidate consistency** — exactly one goal; response format followed; target
  files justified against the request package; docs-request-vs-source-change mismatch.
- **Failure/self relevance** — candidate targets overlap the failure's known related files;
  type match; docs-only-for-source-failure; for self-improvement, candidate is linked to a
  self attempt / proposed task (self-dogfood candidates use the provider label
  `self_dogfood:<attempt>` and route through the self-relevance path).
- **Overclaim detector** — flags "applied / merged / deployed", "tests passed",
  "verified / fixed / resolved". `intended to`/`should`/`will` framing is allowed. Findings
  carry codes only — never the matched text.
- **Minimality / scope** — too many files / lines → too broad; generated/lock/cache targets
  → unexpected file. Safe metadata only (counts, path categories).
- **Testability** — is there linked test evidence to verify after apply? Unknown
  testability is surfaced (LOW for docs-only, MEDIUM otherwise). No tests are executed.
- **Loop risk** — durable history: an identical candidate already rejected → HIGH (repeats
  failed attempt); many verifications for one failure → MEDIUM. HIGH loop risk forces human
  review even on otherwise-low findings.
- **Secret / entropy heuristic** — reuses the trust-gate scanner (private-key headers,
  AKIA/sk-/ghp_, bearer, api-key assignment) and adds an entropy heuristic for novel
  token-like secrets, `.env`-like values, credential assignments, and URL credentials. Runs
  on the PRIVATE raw bytes; reports safe codes/counts only — **never echoes a value**.

## Decision rules

| Findings | Decision |
|---|---|
| any blocker / high | `verification_rejected` |
| any medium | `needs_human_review` |
| low-only | `verification_passed` |
| no candidate / no trust report | `verification_incomplete` |

`verification_incomplete` creates no intent. `verification_passed` still means *pending
approval* — not approved, not applied, not verified-as-correct.

## Persistence

Safe report in job metadata (`provider_verifications_v1`) **and** a private
`.data/workspaces/<job_id>/provider_verification/<verification_id>/report.json`
(atomic write, 0o600, dir 0o700). No raw candidate / diff / source / secrets / absolute
paths. **Idempotent** by `(trust_report_id, candidate_hash, request_package_id /
self_attempt_id)`; `--new` forces a fresh report.

## CLI

- `remedy provider verify <job_id> <trust_report_id> [--request-package-id …] [--self-attempt-id …] [--new] [--json]`
  — metadata-only; runs verification against existing entities + private quarantine bytes.
  Never materializes/approves/applies.
- `remedy provider verification-show <job_id> <verification_id> --json` — read-only.

Both are `may_mutate_repo=false`, `may_execute_commands=false`. Contract actions:
`provider_verify_candidate` (metadata), `provider_verification_show` (read-only) — distinct
from `cloud_provider` (external execution, denied by `no_cloud`).

## Orchestrator integration

`build_orchestrator_situation` gathers verification signals and offers deterministic,
catalog-backed options:
- trust accepted but not verified → recommend `provider verify`;
- verification needs review → human-gated `verification-show` (never auto-approve);
- verification passed + intent pending → existing approve/continue path;
- repeated trust/verification rejection → human-gated "change approach" note (no auto retry).

## Local advisor hook (Step 1555) — DEFERRED

An optional local-advisor critique of the safe verification summary is **deferred** to a
future block (the report carries a forward-compatible `advisor_critique` field, currently
`None`). Per design, if implemented it may **only** lower confidence or add a human-review
concern — it can **never** pass or reject a candidate by itself, create a command, or
override a deterministic check. Deferring avoids a fragile second model-prompt path while
keeping the hard safety invariant trivially true. See
[local-model-advisor-v0.md](local-model-advisor-v0.md).

## What this block does NOT do

No provider/model execution, no cloud API, no external network, no browser, no subprocess
(except CLI runtime tests), no provider SDK. No automatic apply / approval / repair-loop /
PR / merge / git-commit-gate / background orchestration / UI mutation buttons / MCP / dep
upgrades. Verification reports are safe summaries only.

## Next

[Expensive Builder Routing v0](expensive-builder-routing-v0.md) (now built — local-first routing
that requires trust + verification before any external builder route) OR Automated Local Candidate
Generator Adapter v0 — both gated behind request package + trust + verification.
