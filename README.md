# Remedy

Remedy is a **local-first orchestration kernel** for artifact-driven software work.
It plans a job, runs it through a Builder / Reviewer loop inside an isolated git
worktree, collects verifiable evidence, and stops at a human approval gate. Nothing
reaches your repository or your remote without you saying so.

**Local-first.** Everything runs on your machine. Providers (Claude CLI, Ollama) are
optional plug-ins behind interfaces; the core has no cloud dependency.

**Human approval.** No automatic commit, push, merge or promotion. Ever. The final
gate (`commit_execution_gate`) is `NEEDS_HUMAN_APPROVAL` by design.

**Evidence, not claims.** Every completion carries hashes, gates and reproducible
verification commands. If something is unproven, Remedy says so instead of guessing.

## Status

65 of 258 registered items accepted. Next: the first unchecked item in docs/roadmap/STATUS.md.

| Tier | Name | Done | Total |
|------|------|-----:|------:|
| 0 | Foundation & Trust Core | 16 | 16 |
| 1 | Self-Build Bootstrap | 22 | 22 |
| 2 | Minimal Self-Build Runtime | 14 | 14 |
| 3 | Full Token Economy & Autonomy | 0 | 26 |
| 4 | Memory & Learning | 0 | 16 |
| 5 | Operator Cockpit | 13 | 32 |
| 6 | Design-to-Code | 0 | 16 |
| 7 | Quality & Trust | 0 | 15 |
| 8 | Worker Ecosystem & Neutrality | 0 | 12 |
| 9 | Evidence & Compliance Product | 0 | 12 |
| 10 | Team & Multi-User | 0 | 12 |
| 11 | Verification v2 | 0 | 10 |
| 12 | Observability & Operations | 0 | 9 |
| 13 | Multi-Repo & Organization | 0 | 8 |
| 14 | Productization & Distribution | 0 | 10 |
| 15 | Intelligence v2 | 0 | 10 |
| 16 | Cockpit v2 | 0 | 10 |
| 17 | Self-Improvement & Ecosystem | 0 | 8 |

Accepted foundation (Tier 0, complete):
F001 adaptive timeouts, F002 prompt-trace evidence, F003 token/cost truth,
F004 raw stream evidence, F005 enforced structured outputs, F006 worktree isolation,
F007 runtime harness, F010 failure post-mortems, F011 kill switch,
F012 deterministic runs, F017 scope fences, F018 budgets & stop conditions,
F081 remedy init, F146 project identity & repo autodetection, F147 golden-path CLI,
F148 project scoping everywhere.

Accepted in Tier 1 so far:
F013 job intake, F014 flight plan, F016 scaling task granularity,
F034 bundled clarification, F046 multi-cycle loop, F047 checkpoint & resume,
F048 job queue, F251 full-suite stabilization, F252 standing-red paydown,
F050 DAG scheduling, F051 escalate instead of block,
F052 self-healing test rounds,
F053 final & interim report.

Accepted in Tier 2 so far:
F254 model alias table & dead-model doctor check,
F103 token ledger (SQLite), F104 hard budget enforcement,
F105 cache-optimal prompt ordering, F107 context compiler v2,
F086 release capability (wheel, `remedy --version`, release gate).

Accepted in Tier 5 so far:
F255 teacher role (`remedy teach narrate`, `remedy teach ask`, teacher spend
reported as its own role in the token ledger).
F008 sse event stream (per-job SSE endpoint with heartbeat and Last-Event-ID
resume, a cockpit client with reconnect backoff and a polling fallback that
labels itself delayed instead of pretending to be live).
F009 the single write channel (one authenticated, CSRF-guarded, rate-limited
and nonce-idempotent POST endpoint for UI-initiated commands, every other
mutating route answering 405 under a route-walking test).
F021 live activity feed and now-card (a humanization catalog that turns every
Part E event kind into a plain line with an honest generic fallback for an
unknown kind, a NowCard over the ACTION-class subset with a recency dot, and
feed rows that carry their seq and focus their node on click).
F022 live cost ticker (the COST tile renders from budget tick events with a bar
fill against the limit, a '~' prefix and tooltip whenever the basis is
estimated, a warn band at 85 % of the token limit, a spent-only variant for
limitless jobs, and the ledger's own final figure replacing the live one at
terminal with any delta labelled).
F031 decision inbox (every open question as a card carrying its type, age and
blocked-subtree size, derived from the decision queue with no new storage,
ordered by a documented rule over age and blocked size, filtered and badged
live, and answerable from the card through the one existing write channel).
F032 approval with the evidence triple (every producing decision carries its
evidence refs, an expected outcome and a downside, enforced where the decision
is derived so a producer that omits one fails its own test; the inbox card
renders the receipts, the honest note when a card has none, and each answer's
own outcome and downside under the answer it belongs to).
F037 rendered diff viewer (a unified diff parsed server-side into structured
JSON — files, hunks, lines and intraline spans — served per job and per task run,
and rendered in the client with a file sidebar, hunk collapse beyond a size
threshold and virtual scrolling past two thousand rows; syntax highlighting is
modelled and deliberately not wired, per this feature's amendment A6).
F256 diff viewer completion (the highlighting F037 only modelled is now rendered,
with the grammar tables split into their own lazily imported chunk so they leave
the main bundle; the 10k-line fixture measured end to end and its numbers
recorded — the route answers a 1,045,960-byte envelope in 0.1331 s, and the
client draws 48 rows of 10,002 however far the document grows — and the file
sidebar's visual treatment ruled by a named design authority and applied).
F257 self-use track (Remedy now runs a curated maintenance job on its own
repository at every feature close, on a schedule that cannot be skipped: a
shipped queue of operator-curated jobs whose read side owns no writer at all, a
seam that renders one item verbatim onto the job path Remedy already has and
plans it, and a closure precondition that consumes exactly one item per close —
no job may mark its own item consumed, because a run that can check itself off is
not a gate).

F040 completion/return digest (a hero card condensing state, cost with its
basis, open decisions and one recommended action into a single glance, shown
at job end or on the first UI open after an absence; the same envelope is
served to `remedy job digest <id>` so the CLI and the route can never
disagree; a dismissal persists per job and new activity re-arms it).

F258 self-use track v2 (the queue now replenishes itself: a generator appends
exactly one dated, provenanced item whenever the track runs dry, sourced first
from the oldest self-contained open finding in the reviewer's own ledger; the
consumed item is RUN through the real job path to the normal approval gate,
not merely planned; and any defect the run surfaces flows back into that same
ledger as a normal finding).

F106 session resume instead of rebuild (a repair round resumes the prior
round's own provider session — gated on the provider honestly advertising
support and a captured prior session id, never guessed — and sends only a
hunk-selected findings delta in place of the full diff, with an honest,
automatic fallback to full context the instant a resume attempt errors;
the reduction is measured against a fixture repair chain, not assumed).

Full per-feature state: [`docs/roadmap/STATUS.md`](docs/roadmap/STATUS.md)

## Install

```bash
git clone git@github.com:UndefinedDatabase/remedy.git
cd remedy
pip install -e ".[dev]"          # add ,ollama for the local planner provider
```

## Quickstart

```bash
remedy doctor                              # check local health
remedy config show                         # view current settings
remedy job create --plan plan.yaml         # create a job from a plan
remedy do plan <job-id>                    # generate a flight plan
remedy do run <job-id>                     # run the job
remedy do report <job-id>                  # generate the report
remedy job stop <job-id>                   # stop at next safe point (F011)
remedy job rerun <id> --check-manifest     # verify recorded inputs (F012)
remedy runtime serve                       # start dev-server supervisor (F007)
```

`remedy <group>` with no subcommand prints that group's help.

## Documentation

| What | Where |
|------|-------|
| Doc index | [`docs/README.md`](docs/README.md) |
| Roadmap (250 features + registered items) | [`docs/roadmap/ROADMAP.md`](docs/roadmap/ROADMAP.md) |
| Execution ledger | [`docs/roadmap/STATUS.md`](docs/roadmap/STATUS.md) |
| Agent rules | [`AGENTS.md`](AGENTS.md) |
| Operator quickstart | [`docs/guides/simple-operator-quickstart-v0.md`](docs/guides/simple-operator-quickstart-v0.md) |
| `do run` guide | [`docs/guides/do-run-v1.md`](docs/guides/do-run-v1.md) |
| `do continue` guide | [`docs/guides/do-continue-v1.md`](docs/guides/do-continue-v1.md) |
| Runtime harness (F007) | [`docs/system/runtime-harness-v1.md`](docs/system/runtime-harness-v1.md) |
| remedy.toml config | [`docs/guides/remedy-toml-user-guide.md`](docs/guides/remedy-toml-user-guide.md) |
| Step history (archive) | [`docs/archive/remedy-step-history-v0.md`](docs/archive/remedy-step-history-v0.md) |
| Execution guard limits (F085) | [`docs/system/exec-guard-limitations-v0.md`](docs/system/exec-guard-limitations-v0.md) |

## Development

```bash
python3 -m pytest -q tests/orchestration/test_pingpong.py   # run suites file by file
python3 -m compileall -q packages apps scripts
ruff check .
```

The full suite is large; run the files that cover what you touched.

## Honest limitations

- **No watchdog.** The runtime supervisor owns one dev server and its bounded log;
  if the supervisor is killed while the app lives, `probe`/`stop` report honestly.
  Multi-service runtimes are out of scope for F007.
- **Path-based identity.** Project identity uses a resolved-path digest (F146);
  moving a project directory orphans its runtime state.
- **Provider tooling required.** Provider work needs Claude CLI or Ollama installed;
  without it, provider-backed commands fail honestly.
- **No database.** Everything is files on disk — deterministic, portable, auditable.
