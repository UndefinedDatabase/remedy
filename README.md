# Remedy

Remedy is a **local-first orchestration kernel** for artifact-driven software work.
It plans a job, runs it through a Builder ⇄ Reviewer loop inside an isolated git
worktree, collects verifiable evidence, and stops at a human approval gate. Nothing
reaches your repository or your remote without you saying so.

## Principles

- **Local-first.** Everything runs on your machine. Providers (Claude CLI, Ollama) are
  optional plug-ins behind interfaces; the core has no cloud dependency.
- **Human approval.** No automatic commit, push, merge or promotion. Ever. The final
  gate (`commit_execution_gate`) is `NEEDS_HUMAN_APPROVAL` by design.
- **Evidence, not claims.** Every completion carries hashes, gates and reproducible
  verification commands. If something is unproven, Remedy says so instead of guessing.

## What exists today (foundation F001–F007, F010, F011)

| Feature | State | What it gives you |
|---|---|---|
| F001 | ✅ | Adaptive timeouts and process isolation for provider calls |
| F002 | ✅ | Prompt-trace evidence: one trace per real provider call |
| F003 | ✅ | Token/cost truth — actual usage, never estimates presented as facts |
| F004 | ✅ | Streaming provider evidence (`raw_stream.jsonl`, run events) |
| F005 | ✅ | Enforced structured outputs (versioned schemas, one parse retry) |
| F006 | ✅ | Worktree isolation per run: one job-owned worktree, deterministic `result.diff`, promotion only from a verified base + diff |
| F007 | ✅ | Runtime harness: `remedy runtime serve/probe/stop` with a persistent dev-server supervisor (externally accepted 2026-07-13) |
| F010 | ✅ | Automatic failure post-mortems: one `postmortem.json` per finally-failed call, task or job, plus `remedy stats failures` (externally accepted 2026-07-14) |
| F011 | ✅ | Kill switch: `remedy job stop <id>` stops a running job at its next safe point — the call in flight finishes, nothing new starts, the job persists as `stopped` and resumes where it left off (externally accepted 2026-07-14) |

F001–F007 and F010 are the accepted foundation. Every finally-failed provider call, task
or job leaves one machine-readable `postmortem.json`, and `remedy stats failures` aggregates
them from the evidence on disk — deterministically, with zero LLM calls and no database.
F001–F007, F010 and F011 are the accepted foundation. A stop is a fact on disk, not a
signal: `remedy job stop <id>` writes one private control file, and the runner honours it at
its next safe point. There is **no daemon**, no background thread and no signal handler; the
runner is not SIGKILL-recoverable (stale-RUNNING recovery is a later feature), checkpoint v1
is the persisted job itself (no deep checkpoints), and there is still **no database**.
F012 (deterministic runs) is **implemented but not yet externally accepted**: every completed
or stopped job EPISODE records one versioned, hashable INPUT manifest (with the exact
provider-transport input fingerprint per call), and `remedy job rerun <id> --check-manifest`
freshly reconstructs the CURRENT would-be inputs (including a content digest of the target
working tree) and reports drift — exit 4 for blocking drift, exit 5 when per-call prompt
coverage is incomplete (the public CLI does not reconstruct assembled prompts for ordinary
jobs; that is worktree replay, F140), exit 0 only when fully verified (e.g. a zero-call job),
exit 1 when the recorded manifest chain is inconsistent. The material invocation controls
(`--timeout-sec`, `--timeout-profile`, `--max-output-chars`, `--stream-evidence` /
`--no-stream-evidence`, `--max-tasks`) resolve explicit > persisted > product default: an
omitted flag keeps the persisted value; an explicit flag — even one equal to the default —
overrides it (supplying both `--stream-evidence` and `--no-stream-evidence` is a usage error).
Every manifest Remedy reads back is decoded through one strict schema layer — standard JSON only
(no `NaN`/`Infinity`), real JSON types, no coercion — and its recorded hashes are bound to what
they identify: the job-input hash to the manifest's own embedded input definition, and each call's
fingerprint to the exact provider-transport components recorded with it. A stored terminal
(completed/stopped) manifest is a REFERENCE: its call coverage must be complete and every call
bound to its input artifact, and the writer refuses to publish — and the canonical loader refuses
to read back — one that is not (exit 1). Only the CURRENT candidate reconstructed from live state
may be incomplete, which is the honest exit 5. A successful write or recovery always implies the
tree is immediately readable through the canonical loader: every append for one job is serialized
by a crash-released per-job claim (so two writers can never both decide they are the next
episode), each writer path validates the COMPLETE existing episode chain — every episode's canonical bytes and every prior episode's call artifacts
— and each episode is published from a private staging area with one atomic rename, so two
concurrent writers either converge on identical content or conflict cleanly, and the loser never
leaves a file inside the winner's episode. Manifest artifacts that EXIST are always fully
validated: the F012 marker decides only whether a MISSING manifest is allowed, never whether a
present one is trusted. Zero recorded calls is only ever "complete" when the episode record
itself proves zero were expected — a pre-work stop, a planning-only job or an all-skipped job is
a genuine zero-call reference, while a task that ran but lost its calls is an integrity failure
(exit 1) rather than a silent blank. That proof is exact and it is EVIDENCE, not an
assertion: every run's finalized calls are published as a canonical, hash-bound ledger artifact
inside the episode, and every recorded call maps to exactly one ledger entry — so a stored
manifest cannot quietly claim a shorter ledger. That ledger is held to what it says: a published
reference's ledger must be COMPLETE (a partial account of a run is a contradiction, not a
caveat); its terminal state is read from the run's own record rather than inferred from the
surrounding task, through a CLOSED map where an unknown outcome is a recorded problem instead of
a plausible default; each entry must agree with its call on every replay-material field including
whether the call succeeded; the recorded ORDER must be the manifest's order, because the order is
the claim and F140's replay is keyed by it; and a FINISHED run's ledger is frozen whole — a later
episode may repeat it byte-for-byte and nothing else, so no prior call can be invented, altered,
reordered or dropped, and no finished run can quietly gain a call or change its outcome. Later
work belongs to a new run id, which is what the product already does. A task's history is
monotonic too: once an episode records a task as completed, every later episode must carry it as
prior work naming the same run and the same frozen ledger — a later episode cannot quietly drop
the ledger and call the task skipped, which is how earlier work could still be denied even after
the ledger itself was frozen. Only a task that was stopped before it finished may start a new
run, because that is exactly what resuming a stopped job does. A manifest also carries
exactly the ledgers its own record accounts for: the ledger set must equal the expectation's
run-owning tasks exactly, so a fabricated ledger for a task nobody planned has nowhere to hide.
Each ledger names its artifact by the hash of its identity, so two different runs can never be
backed by one file. And a call reference — the identity the post-mortems, the manifest and the
future replay all use to name the same call — must match a closed canonical grammar rather than
merely fail to be dangerous, down to the spelling of its numbers: one round has exactly one text
form, so `round-01`, `round-001` and `round-000001` cannot be three names for one call. Once an episode is published, its manifest,
call artifacts and ledgers are immutable: a missing or altered member is reported as corruption
and never silently recreated, and an exact retry of any episode — latest or not — is a no-op.
An impossible lifecycle (a completed episode claiming a task was never dispatched, say) can never
be published, and a contradictory persisted state is reported with both facts intact rather than
tidied away — and an expectation must agree with the task status the JobPlan actually recorded, so
a manifest can no longer claim a task was skipped while recording that its work landed. What a
package is a review OF is equally exact: the base is DECLARED and passed explicitly (never
inferred from the process directory, which is not a credential), the packager RECOMPUTES the whole
review subject and commit chain rather than reading the Evidence job's account of itself, every
commit ships the canonical patch bytes its hash refers to so a ZIP-only reviewer can recompute
them without the repository, and a path is typed by `lstat` and never followed — a symlink is
proven by its target text, and one escaping the repository blocks the package instead of being
followed into it or silently dropped from it. Every file record is typed on BOTH sides (its kind
and git mode at the base and at the current tree, so a committed symlink or a mode-only change is
provable), a dirty deletion carries the tombstone of what it removed and a dirty rename its old
path, and the archive itself is assembled from that exact model by a NUL-safe builder — a filename
containing a newline survives verbatim, containment is decided by path components rather than a
string prefix (so a sibling `repo-evil` is never mistaken for being inside `repo`), and the
finished ZIP is reopened and its every member checked against the model — its exact type and unix
mode included, so an executable stays executable and a regular file cannot pass as a symlink. That
whole file-to-archive boundary is one typed transaction: a single ArchivePlan gives every review
file exactly one disposition (a member, a tombstone, or a block — a policy-excluded change blocks
rather than vanishing), every content read goes through an anchored, atomically no-follow
descriptor (a file swapped to an external symlink mid-read is refused, never followed), and the
review-subject schema is exact down to each commit and each file's kind and mode, so an injected
field cannot ride along. Task truth is read in the
episode's own context: a completed episode's task must be applied or passed, and the status a task
completed under is frozen so a later episode cannot rewrite it.
`--check-manifest` is strictly read-only and stays contained THROUGH the inspection:
containment is decided lexically before anything is opened (so `root/sub/../../outside` is refused
rather than walked, one level per `..`), it holds a verified directory handle open so a renamed or
symlinked workspace cannot redirect it mid-check, neutralizes every configured git helper (a
`core.fsmonitor` script used to run during a "read-only" check), and writes no git object, index,
ref or file. It reports two coverage
dimensions separately — the calls it compared and the material inputs it could actually know —
and claims "same inputs" only when both are complete. Remedy separates three things deliberately: WHICH
run produced the evidence (record/provenance identity), WHETHER two runs were given the same
material inputs (logical input identity — it excludes random run identifiers and the outcome), and
WHAT happened (completed/stopped — never an input). Inputs are reproducible and verified; LLM
outputs are recorded, not promised.
Everything else after F007 in the roadmap (including F008 and F017) is **not implemented**.

## Install

```bash
git clone git@github.com:UndefinedDatabase/remedy.git
cd remedy
pip install -e ".[dev]"          # add ,ollama for the local planner provider
```

## Canonical CLI entry points

```bash
remedy job    ...   # create, inspect and resume jobs
remedy do     ...   # plan / run / report / evidence / promote a job
remedy runtime ...  # serve, probe and stop the project's dev server (F007)
remedy job stop ... # ask a running job to stop at its next safe point (F011)
remedy job rerun ... --check-manifest  # verify a job's recorded inputs vs now (F012)
remedy config ...   # view and change settings (remedy.toml)
remedy doctor       # check local health
```

`remedy <group>` with no subcommand prints that group's help.

## Quickstart

- [Simple operator quickstart](docs/guides/simple-operator-quickstart-v0.md)
- [`do run` guide](docs/guides/do-run-v1.md) · [`do continue` guide](docs/guides/do-continue-v1.md)
- [Runtime harness (F007)](docs/system/runtime-harness-v1.md)
- [remedy.toml configuration](docs/guides/remedy-toml-user-guide.md)

## Documentation

- [`docs/README.md`](docs/README.md) — index of everything (`docs/` = built system)
- [`docs/roadmap/ROADMAP.md`](docs/roadmap/ROADMAP.md) — the target plan (250 features)
- [`docs/roadmap/STATUS.md`](docs/roadmap/STATUS.md) — the execution ledger: what is done
- [`AGENTS.md`](AGENTS.md) — the working contract for agents in this repository
- [`docs/archive/remedy-step-history-v0.md`](docs/archive/remedy-step-history-v0.md) — the original Step 1–10 README (historical)

## Development

```bash
python3 -m pytest -q tests/orchestration/test_pingpong.py   # run suites file by file
python3 -m compileall -q packages apps scripts
ruff check .
```

The full suite is large; run the files that cover what you touched.

## Honest limitations

- **The runtime supervisor is not a watchdog.** It owns one dev server and its bounded
  log; if the supervisor is killed while the app lives, `probe`/`stop` report the
  situation honestly and clean up what they can prove is theirs, but nothing restarts it.
  Multi-service (Compose-style) runtimes are out of scope for F007.
- Project identity is still a resolved-path digest (F146 is not implemented), so moving
  a project directory orphans its runtime state.
- Provider work needs the corresponding local tooling (Claude CLI / Ollama) installed;
  without it, provider-backed commands fail honestly rather than degrading silently.
- Evidence bundles are only as good as the verification commands you record in them.
