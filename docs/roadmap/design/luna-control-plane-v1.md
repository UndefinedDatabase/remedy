# Luna's engineering control plane — the strategy and the gates (v1, 2026-10-06)

> Target design annex for operator amendment amend1006-luna-control-plane. It orders Package 1 of
> `docs/roadmap/STATUS.md` and is the source of F295 and F296. It describes what SHALL BE; the
> built state lives in the feature files and in `docs/system/`.

## The one idea

Luna is the person and the interface. Remedy is her engineering department. Models — Claude,
GPT, a local model — are interchangeable workers. Luna knows WHY (the user's intent, priorities,
when to send work, what the shared graphics card is doing); Remedy controls HOW (contract,
plan, budget, routing within the policy, worktree, builder and reviewer, tests, evidence,
approval, recovery, proof); a worker does THE WORK. Three sentences bind every later decision:
self-improving is not self-authorizing; use the cheapest worker that reliably meets the task's
quality and risk requirements, and change that rule only with evidence and a human signature;
evidence, not claims.

## What already exists on both sides

Remedy: the mission contract with templates and the Definition-of-Done compiler (F269, F061);
plan editing, hunk approval and history apply that commits and pushes only on their flags (F015,
F033, F270); evidence per run, `change proof`, the token ledger, the completion digest per job
(F002 to F004, F103, F040); hard job budgets, the autonomy watchdog, the kill switch (F018, F104,
F077, F011); the supervisor `remedy serve` with restart settling (F200); routing by task class with
three hard rules and an evidence-gated promotion rule (F110); the failure classifier (F010); the
self-use track that runs a real job on Remedy itself at every closure (F257, F258, F289, F291);
the JSON envelope and exit codes on every command (F277, F283).

Luna (the universe workspace): the `remedy` mode of the `luna` edition reads the BUILD LOOP's
status export every minute and relays the loop's questions and the operator's answers through a
mailbox; the improve run writes an order into an outbox, a runner working as the operator carries
it out, the result comes back into an inbox, and the operator installs with one tap; improvement
tasks carry an executor (`claude` or `pi`) chosen by the operator; Luna's night (memory, wiki,
learning) runs inside her own service and starts the improve run when reports are open. Luna
never starts a command line and never reads the operator's home.

## The decisions that shape the plan

1. The transport is the file mailbox plus a runner working as the operator, the way Luna's family
   already works. Remedy's side of it is a machine client contract over the command line's JSON
   envelope (F295); the HTTP API (F253) follows for real time and for a replaceable cockpit, it is
   not a precondition.
2. Luna's night stays Luna's. Remedy's job model is built for software changes in a repository;
   her night is a state process with its own rules. The night's ENGINEERING consequences reach
   Remedy as reports, then tasks, then missions — the path that exists today, with Remedy
   replacing the unattended Claude Code in it.
3. No clock in Remedy (A9, Part J). Luna decides when an order goes out and under which
   constraints (for example no local worker while the voice holds the graphics card); Remedy
   takes orders whenever they arrive. Constraints travel as flags and header fields of the order.
4. Routing recommends; a human changes it. History (F133, F074) becomes a recommendation Luna
   relays; the policy changes by configuration and an ADR, audited by git. Escalation after
   classified failures (F296) is a separate mechanism from failover on availability (F058): one
   tier up for the next repair round, never down, never on a provider gap, every step recorded.
5. A machine order without a cost cap is refused. Luna owns the daily envelope; Remedy enforces
   the cap per job.
6. Sol and Gaia wait for tenant, permission, repository and cost isolation (Tier 10, parked).

## Gate A — the machine client (Stage A and B: Luna reads, Luna delegates with approval)

F200 closed, F290 (the rolling paydown keeps its place), F295. Proof: F295's gate test drives
Remedy exactly as the runner will — an order file with a cap, `remedy do <file> --json --no-ui
--yes` with the fake providers, the digest from `remedy status --json`, one decision answered with
`remedy decision resolve --json`, `remedy job apply --approve --json`, `remedy change proof
--json` — with no terminal and no question on stdin. When it is green, the universe workspace
builds Luna's side against `docs/system/machine-client-contract-v1.md`: the contract
`remedy-bridge v1` in universe-kit, a runner and a path unit in universe-engine, the digest in the
status export, the executor `remedy` on improvement tasks, Remedy's decisions through the
existing questions mechanism.

## Gate B — unattended missions

F287 (an interrupted task resumes its provider session and does not pay twice), F116 (a burn
spike warns before the hard budget), F058 (a provider gap fails over with disclosure), F199 (the
supervisor reports its own health and a crash leaves a local report), F203 (what happened at night
is searchable by job id in the morning). Proof: an interrupted, over-spending or provider-less
fixture mission ends honestly and resumes without paying twice.

## Gate C — controlled autonomy (Stage C)

F055 (rehearsal: "four tasks, at most five euros — start?" without a builder call), F078
(autonomy levels: who may start), F141 (the permission matrix: what running work may do), F060
(a portable, verifiable certificate per mission), F253 (the headless API for real time and a
replaceable cockpit). Proof: a routine order starts under a configured level without a question,
inside the matrix, and leaves a certificate that verifies on another machine.

## After the gates

Routing v2 — F296, F113, F074, then F133 under Tier 7: escalation on evidence, local models for
side roles behind a quality gate, estimate calibration from the ledger, the trust score per model
and role as a recommendation. The second worker — F151, F157, F152, F162, F153, F158, F155, F154,
F161: the adapter contract with its conformance kit, the capability matrix with honest
degradation, config isolation, sandbox profiles, the Codex adapter (the operator's second
executor today is `pi`), cost normalization, the local full builder, Gemini, MCP with policy.
Self-dogfood automation — F073, F063, F064, F066, F067, F065: the post-mortem miner proposing
playbooks behind approval, the idea engine with mandatory evidence, routine missions as order
files. Then the rest of Tier 3, the rest of Tier 12, Tier 4, the rest of Tier 7, Tiers 6, 11,
9, 15, 13, 16 and 17 in their earlier relative order.

## The contract, in one paragraph

A client writes an order file: the order text and a header with the project, the contract
template, the cost cap and the constraints. It starts `remedy do <file> --json --no-ui --yes
[--max-cost-usd …] [--builder-provider …] [--reviewer-provider …]` and reads the JSON answer. It
polls `remedy status --json` and reads the machine section: missions, jobs, states, costs with
their basis, evidence references, every open decision with its question and default, the jobs
that wait for apply, whether the supervisor answers. It answers a decision with `remedy decision
resolve <job> <decision> --json`. On the operator's approval it runs `remedy job apply <job>
--approve [--commit-with-history] [--push] --json` and reads `remedy change proof <job> --json`.
Remedy never applies without `--approve`, never commits or pushes without their flags, never
starts a machine order without a cap, and never asks a question on stdin when `--yes` is given.
The page `docs/system/machine-client-contract-v1.md` (F295 T004) is the binding list.

## What this annex deliberately leaves out

A scheduler, a queue or any clock inside Remedy (the operator retired the F048 queue with no
heir, DECISION F261 D14, D22); Luna's logic, persona or memory anywhere in Remedy; an automatic
change of the routing policy; a second coding agent of Remedy's own — Remedy stays the control
plane over the agents that exist.
