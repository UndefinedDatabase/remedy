# Context — current state

## Where the product is

- F001–F006 complete and merged.
- **F007 (Runtime harness) is externally ACCEPTED** — verdict
  `PASS_WITH_RISKS — ACCEPTED`, 2026-07-13, zero open findings. It is `[x]` in
  `docs/roadmap/STATUS.md`.
  - accepted package: `remedy-review-20260713-115439-READY_FOR_REVIEW.zip`
    (sha256 `4df642850249b8e1d2763400311aced43a712fd0523e79e4c6c169d5c0b263a9`);
  - accepted Evidence job: `2e820a4dbf9842cf`
    (history: `eb2b76fd1aba4668`, `809b9b5743694abf`);
  - external proof: portability 99 passed, CLI process boundary 15 passed, and both files
    in ONE pytest invocation **114 passed in 525.44s** — with no `/tmp/pytest-*` runtime
    supervisor or application surviving any complete run.
- `remedy runtime serve|probe|stop` is the harness. `serve` is short-lived; it starts a
  **persistent supervisor** (`python -m packages.runtimes.runtime_supervisor`) in its own
  session, which owns the application (own process group) and the bounded log pump, so the
  dev server — and its logging — survive the CLI.
- The hardening work lives on `feature/f007-supervisor-portability`, which is still
  **uncommitted, unpushed and unmerged**, awaiting the human commit decision. The older
  branch `feature/f007-runtime-harness` was merged (PR #127) and deleted.

## What F007 is NOT

- Not a watchdog: nothing restarts a supervisor that is killed. `probe`/`stop` report the
  situation honestly and clean up only what they can prove is theirs.
- Not multi-service: one dev server per project, no Compose-style orchestration.
- Not F008 (SSE stream), not F010 (post-mortems), not F146 (project registry).
- Project identity remains F006's resolved-path digest, so moving a project directory
  orphans its runtime state.

## Boundaries

- **F010 (automatic failure post-mortems) is next and has NOT been started.**
- F008, F009 and F146 are not started.
- No provider call, no Docker, no `shell=True`, no network installation in F007 work.
