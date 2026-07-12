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

## What exists today (foundation F001–F007)

| Feature | State | What it gives you |
|---|---|---|
| F001 | ✅ | Adaptive timeouts and process isolation for provider calls |
| F002 | ✅ | Prompt-trace evidence: one trace per real provider call |
| F003 | ✅ | Token/cost truth — actual usage, never estimates presented as facts |
| F004 | ✅ | Streaming provider evidence (`raw_stream.jsonl`, run events) |
| F005 | ✅ | Enforced structured outputs (versioned schemas, one parse retry) |
| F006 | ✅ | Worktree isolation per run: one job-owned worktree, deterministic `result.diff`, promotion only from a verified base + diff |
| F007 | 🟡 | Runtime harness: `remedy runtime serve/probe/stop` with a persistent dev-server supervisor — **merged, external acceptance still pending** |

F007 is **not accepted yet**; treat it as a working checkpoint. Everything after F007 in
the roadmap (including F008 and F010) is **not implemented**.

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

- **F007 is unaccepted.** Its persistent supervisor has no watchdog: if the supervisor
  is killed while the app lives, `probe`/`stop` clean up, but nothing restarts it.
- Project identity is still a resolved-path digest (F146 is not implemented), so moving
  a project directory orphans its runtime state.
- Provider work needs the corresponding local tooling (Claude CLI / Ollama) installed;
  without it, provider-backed commands fail honestly rather than degrading silently.
- Evidence bundles are only as good as the verification commands you record in them.
