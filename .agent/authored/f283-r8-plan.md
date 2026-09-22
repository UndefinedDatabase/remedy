# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 8. It books round 7's PASS and the `Done:` lines of R-1023 and R-1024,
and records DECISION F283 D3. Then, one commit each: the single-pass
`job run --json` answers in the envelope on success, on a verification
failure and when no task is pending; a blocked `job resume` refuses through
`fail()` with its old keys kept; the `patch list` refusal round 7 left
untested gets its test; R-1025 — the product-spine test that pinned
R-1020's prose asserts the envelope; R-1019 — `worker unload` checks for `--model` or
`--all` before it probes for `ollama`; the `do_cmd` group's refusal pairs move
onto `fail()`.

## Next Steps

1. The `project` group, whose refusals mix `Error:` and `ERROR:` prefixes —
   a ruling on the uppercase form lands with the patch that applies it.
2. The remaining groups largest first — `grouped`, `test_cmds`, then the
   tail; `runtime_cmd.py` is its own round.
3. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-four findings are open; R-1019 and R-1025 are this feature's own and
are repaired this round, with their `Done:` lines booked in the next. The refusal
pairs left are several sessions of work, so the soft limit of 7 sessions and
25 rounds is the number to watch.
