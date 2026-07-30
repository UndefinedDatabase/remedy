   Environment-coupled base failures (R-0155 amendment, operator
   approved 2026-07-30): the throwaway base worktree lacks build
   outputs the suite needs (the ROOT `node_modules`, `apps/ui/dist`),
   so environment-coupled ids (vitest/tsc/ui-server classes) fail at
   base and land in `comm -23` on every gate run — where a GENUINE
   base failure in those same files would be masked. Therefore:
   either restore parity before the base run (share or copy the
   primary checkout's root `node_modules` and `apps/ui/dist` into
   the base worktree, or run the same install/build there), or
   attribute EVERY `comm -23` id to the environment class by direct
   evidence (the missing artifact named per id). An unattributed
   `comm -23` id counts as a genuine base failure and blocks the
   gate verdict.
