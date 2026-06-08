# Reviewer and Test Safety

## Resource-Safety Policy

These rules are mandatory for all agents (workers, reviewers, watchers) operating in this repository.

### Never Do

- Never run `pytest tests/` in background (`run_in_background: true`, `&`, `nohup`).
- Never run multiple reviewer sessions on the same repo if they will execute tests.
- Never run full `pytest tests/` more than once per worker block unless explicitly justified.
- Never run multiple pytest commands in parallel.
- Never use `shell=True` in production Python code.

### Always Do

- Use `scripts/remedy_pytest.sh` for all pytest execution.
- Run pytest in foreground only.
- Use explicit timeout (wrapper default: 600s).
- During active development, run targeted tests only.
- Run full baseline only once, near final handoff.
- If another pytest is already running, fail fast (the wrapper handles this via `flock -n`).

### Reviewer Protocol

Reviewers must prioritize (in order):

1. Code inspection (read diffs, check logic)
2. Relevant targeted tests (`scripts/remedy_pytest.sh tests/specific_file.py -q`)
3. Checking `.agent/live_review.md` findings
4. Checking `git status` and `git diff`
5. Full baseline — only once at final review, only if worker didn't already report one

If the worker already reports a full baseline and no code changes happened since, the reviewer may verify targeted areas instead of rerunning the full suite.

### What the Wrapper Does

`scripts/remedy_pytest.sh` provides:

- **Lock**: `flock -n` on `/tmp/remedy-pytest.lock` — fails fast if another run is active
- **Timeout**: configurable via `REMEDY_PYTEST_TIMEOUT_SEC` (default 600s)
- **Foreground only**: no background execution support
- **Clear errors**: distinct messages for lock-busy and timeout conditions

## Test Command Matrix

### During Development (targeted)

```bash
# Single domain
scripts/remedy_pytest.sh tests/orchestration/test_event_replay.py -q --cache-clear

# CLI tests
scripts/remedy_pytest.sh tests/cli -q --cache-clear

# UI server tests
scripts/remedy_pytest.sh tests/ui_server -q --cache-clear
```

### Before Final Handoff (one full baseline)

```bash
# Full Python suite — run exactly once
scripts/remedy_pytest.sh tests/ -q --cache-clear

# Frontend tests
cd apps/ui && npm run test:unit -- --run

# TypeScript check
cd apps/ui && npx tsc --noEmit

# Build check
cd apps/ui && npm run build
```

### Never

- `pytest tests/` in background
- Repeated full pytest in watcher/review loop
- Parallel reviewer full-suite runs
- `python -m pytest` without the wrapper (in agent context)

## Emergency Cleanup

If pytest processes pile up and CPU overheats:

### Inspect Running Processes

```bash
pgrep -af "pytest|python.*pytest"
```

### Stop Pytest Processes

```bash
# Careful targeted kill (check PIDs first)
pkill -f "python.*pytest"

# Or manual per-PID (safer)
kill <pid>
```

### Warning

- Do not kill unrelated Python services blindly.
- `pkill -f python` will kill everything Python — too broad.
- Always inspect with `pgrep -af` first.

### Check CPU

```bash
top -bn1 | head -20
# or
htop
```

### Prevention

- Run one reviewer session at a time.
- Use `scripts/remedy_pytest.sh` — the lock prevents stacking.
- If a long test is needed, state it explicitly in the final report.
