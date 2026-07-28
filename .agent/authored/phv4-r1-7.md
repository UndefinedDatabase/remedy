On ANY refusal or duplicate STOP (refused-hash-gate /
stopped-duplicate), the worker COMMITS AND PUSHES
`.agent/last_block.md` — OUTCOME line set accordingly, plus one
evidence line (expected vs computed hash, or the duplicate's commit
shas) — as the round's only commit. A refusal that leaves no disk
trace is itself a handback defect. (This clarifies "committed with
the round bookkeeping" for rounds where the bookkeeping commit IS the
refusal.)
