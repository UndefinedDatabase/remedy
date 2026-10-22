# Local side roles v1: summaries on a model server of your own

> Status (F113, 2026-10-22): the named local endpoints with their probe (T001), the side-role
> table with its refusal and its fallback (T002), and the record of a job's side-role calls in its
> evidence and the cost ledger (T003a) are built. The quality gate with its flip and its status line
> (T003b) is not built yet. DECISIONs F113 D1 and D2 in `.agent/decisions.md`; the feature is
> `docs/roadmap/features/T3_F113.md`.

Some of the model calls Remedy makes are chores: writing the short summary that stands in for a
diff too long to put in a prompt, the result tour, the answer in the cockpit's chat. They run under
the `summary` role. F113 lets an operator send such a role to an Ollama server of their own, so the
chore stops costing paid tokens.

## The endpoints
`local_routing.endpoints` names each server, with exactly a `base_url` and a `model`:

```toml
[remedy.local_routing.endpoints.box]
base_url = "http://127.0.0.1:11434"
model = "muse-glimmer"
```

Several servers may be named; Remedy balances no load between them. A table Remedy cannot read is
refused with a warning naming the fault, and then no role runs locally.

The first time a process uses an endpoint, Remedy asks the server for its list of models and keeps
the answer for 300 seconds, so a long-running process notices a server that went away or came back.
A server that does not answer, or does not list the model, is unavailable, and the reason opens
`provider_unavailable: local endpoint`, the same class model failover reads. A local endpoint keeps
no conversation between calls, so it never resumes one.

## The side roles
`local_routing.side_roles` maps a role to an endpoint by name:

```toml
[remedy.local_routing.side_roles]
summary = "box"
```

Only a side role may be mapped: a role whose task class the routing table sends to the cheap tier,
today `summary`, `teacher` and `study`. A table that maps any other role, such as `builder`,
`reviewer`, `repair`, `planner` or `orchestrator`, is refused whole with the hard rule named,
`core_role_on_local_provider`, the same "core never local" rule model failover applies to its
backup links (`docs/system/model-failover-v1.md`). Remedy deliberately does not check this rule
against a core role's own provider: the shipped defaults run the builder and the reviewer on local
tools, and which provider serves a core role is not this feature's to change.

## What happens on a call
A mapped role runs on its endpoint while the probe says the endpoint serves. When it does not, the
role runs on the path it takes unmapped, its own configured model, exactly as it did before F113.
The summary role's three users, the diff summary, the result tour and the chat answer, all follow
the same route.

A summary written by a mapped role records its route beside its text, as `route`: `local` or
`fallback`, the endpoint, the model that served when it was local, the reason when it fell back,
and the cost basis, `local_zero` for a local call and `unknown` for a fallback. A summary of an
unmapped role carries no route.

## In the job's evidence and the cost ledger
When a job's evidence is exported, every summary a task run wrote through a mapped role becomes one
row of `side_role_calls.json` beside the task's other evidence: the role, the route, the endpoint,
the model, the reason and the cost basis. When the job belongs to a registered project, the rows are
copied into the `side_role_calls` table of that project's cost ledger, which accepts only the bases
`local_zero` and `unknown`. A local call's token count is left empty rather than set to zero, because
the endpoint's client reports none. The tour and the chat answer run outside a job, so their calls
reach no ledger.
