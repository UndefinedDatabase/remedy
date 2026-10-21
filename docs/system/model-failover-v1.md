# Model failover v1: a backup model when a role's provider cannot be reached

> Status (F058, 2026-10-12): built. DECISIONs F058 D1 to D4 in `.agent/decisions.md` hold the rules
> this page states; the feature is `docs/roadmap/features/T3_F058.md`.

## What it does

A role (for example `builder`) may name backup models in `remedy.toml`. When a call to the role's
provider cannot be reached, even after the transport retries, Remedy sends the call to the backups
in the order they are written, and the first one that answers without an error serves it. A role
with no chain behaves as it always did. Nothing fails over unless the operator configures it.

## Configuring a chain

```toml
[[remedy.model_failover.chains.builder]]
provider = "claude-cli"
model = "sonnet"
tier = "mid"

[[remedy.model_failover.chains.builder]]
provider = "claude"
model = "claude-sonnet-4-5"
tier = "mid"

[remedy.model_failover]
cooldown_s = 300
```

A link holds exactly `provider`, `model` and `tier`; any other key, a repeated provider and model
pair, a role Remedy does not know, or a provider other than `claude`, `claude-cli`, `fake`, `ollama`
and `pi` is refused. A link names its tier because the hard rules below
are about tiers, and Remedy checks the tier you declare, not a guess from the model name. An
environment variable cannot carry the chains (a table); the cooldown's variable is
`REMEDY_MODEL_FAILOVER_COOLDOWN_S`. Both keys are listed in `docs/guides/environment.md`.

## The hard rules

Every link is checked against the project's own routing table (the shipped table with the
operator's `model_routing` overrides). The three hard rules of `docs/agents/model_routing_policy.md`
apply: a reviewer's link is never weaker than its worker's, an orchestration role's link is never
below the top tier, and a safety-relevant role's link is never below the mid tier. A fourth rule,
`core_role_on_local_provider`, keeps a local provider (today `ollama`) off every role except those
the table routes to the cheap tier. A table that breaks a rule gives one warning naming every
violation, and then no role fails over.

## When it fails over

Only when the provider is unavailable or cannot be connected to (`is_failover_trigger`). That
includes an overloaded service (HTTP 529, `overloaded_error`), a connection that could not be made
and a name that could not be resolved, and it includes a claude-cli that exits non-zero when the
last lines it wrote to its error stream say one of those things, once the transport retries are
spent. A timeout, any other non-zero exit, a rate limit and an unreadable answer never fail over.
The transport retries own the timeout and the non-zero exit, the rate governor waits out a rate
limit, and the single parse retry owns an unreadable answer; a backup would only hide those. A link that cannot be built counts
as a failed attempt, and the walk goes on to the next one. A backup that answers with one of those
failures ends the walk with it, which the transport retries then own: it serves nothing, holds
nothing and leaves the role's sessions as they were. When that failure is a rate limit, the retry
waits it out on the backup's own provider, never on the usual provider's. A backup is built once per
run and hears the round of each call, so a claude-cli backup's stream artifacts land in a directory
of their own, numbered on from the usual provider's, and never over them.

## The cooldown

After a backup serves a call, that role's next calls go to the backups first for `cooldown_s`
seconds (default 300; 0 never holds), so a dead provider is not retried on every call. The record
then says `primary_skipped`. When every backup fails during the hold, the usual provider is tried
last, and if it answers, the hold ends. The hold lasts one run.

## Sessions

A backup is never offered a session. Once a backup has served, the role resumes no session for the
rest of the run. A call that offers a session does not fail over; the run's own fallback calls
again with no session, and that call may fail over. A relaunch never offers a backup's session to
the usual provider: `parked_session_refs` clears the role when a round's `failover` names a
serving link.

## What the record and the report show

A round's builder or reviewer entry carries a `failover` key when the walk reached the call:
`reason` (`failover:provider_unavailable`), `role`, `intended` (provider and model), `used` (the
link that served, or `null` when the chain ran out or a backup answered with a failure),
`primary_error`, `primary_skipped`, and
`attempts` (position, provider, model and error of each link tried). Every real call behind a
failed-over call is booked as a provider attempt of its own, under the provider and model that
served or failed it, so the call count, the cost coverage and the call budget see each one.
`remedy run show` prints one
line, `Failover:`, built of these sentences: "1 call was served by a backup model because its usual
provider could not be reached." (or "N calls were served by backup models because their usual
provider could not be reached."), "1 call found no backup model that served it." (or "N calls
found no backup model that served them."), and always "The run's record names every model
tried."

## What it deliberately does not do

- It does not fail over on a timeout, a rate limit or a parse failure.
- It holds nothing past the end of a run.
- It has no implicit chain: a role without a configured chain has no backup.
- It does not escalate on failed tests or reviews; that belongs to F296.

## Where the code is

- `packages/orchestration/model_failover.py`: the chains, the rules, the trigger, the walk, the cooldown.
- `packages/orchestration/role_provider_factory.py`: wraps a role's provider.
- `packages/orchestration/pingpong_call_record.py`: the `failover` key and `parked_session_refs`.
- `packages/orchestration/pingpong_provider_call.py`: the call's retry, which waits a backup's rate
  limit out on that backup's provider.
- `packages/orchestration/config_keys_model_routing.py`: the two config keys and the cooldown's default.
- `packages/orchestration/provider_names.py`: the provider names a link may name.
- `apps/cli/commands/run_report_cmd.py`: the `Failover:` line.
- Tests: `tests/orchestration/test_model_failover.py`, `tests/orchestration/test_role_provider_factory.py`,
  `tests/orchestration/test_pingpong_call_record.py`, `tests/cli/test_run_report_cmd.py`.
