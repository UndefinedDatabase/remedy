# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 7. It books round 6's PASS and R-1022's `Done:`, registers R-1023 and
R-1024, and records DECISION F283 D2. Then, one commit each:
R-1023 — `decision.py`'s two forked tokens take the spellings the product
already has, and a test pins that module's token set; R-1024 — the
cost-preview gate takes `json_output`, puts its human lines on stderr under
it, and refuses a non-terminal stdin through `fail()`; the `brain` group's
refusal pairs; the `patch` group's refusal pairs.

## Next Steps

1. The non-mechanical `job.py` sites: the verification-failure loop and the
   single-pass `job run --json` success line, which is prose; `_cmd_resume`'s
   two hand-rolled `resumed: false` objects.
2. The remaining groups largest first — `project`, `do_cmd`, `grouped`,
   `test_cmds`, then the tail; `runtime_cmd.py` is its own round.
3. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-five findings are open; R-1023 and R-1024 are this feature's own and
are repaired this round. The refusal pairs left are several sessions of work,
so the soft limit of 7 sessions and 25 rounds is the number to watch.
