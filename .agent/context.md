# Context — current state

## Where the product is

- F001–F006 complete and merged.
- **F007 (Runtime harness) merged through PR #127** (merge commit `7733a1d`,
  follow-up test fix `d0a08a1`). It stays `[~]`: the persistent-supervisor round has
  NOT been externally accepted.
- `remedy runtime serve|probe|stop` exists. `serve` starts a **persistent supervisor**
  (`python -m packages.runtimes.runtime_supervisor`) in its own session, which owns the
  application and the bounded log pump, so the dev server survives the short-lived CLI.
- The feature branch `feature/f007-runtime-harness` is MERGED AND DELETED. Do not treat
  it as active.

## Open technical findings on F007

1. Cross-process identity depends on reading the app's live cwd; on systems where
   `/proc/<pid>/cwd` is not readable for a detached process, a separate `probe`/`stop`
   fails as `identity_unproven` (exit 5).
2. `probe` verifies the application but not the supervisor's health.
3. A post-handshake validation failure in `serve` can leave the supervisor and app alive.
4. Supervisor failure paths do not all share one finalizer; some clear state
   unconditionally.
5. Supervisor and application currently share a process group.

## Boundaries

- **F008** (SSE stream), **F010** (post-mortems) and **F146** (project registry) are
  NOT started. F010 becomes next only after F007 is externally accepted.
- Project identity remains F006's resolved-path digest.
- No provider call, no Docker, no `shell=True`, no network installation in F007 work.
