# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 6, the `job` group's last mechanical refusals and the `decision` group.
It books round 5's PASS and R-1021's `Done:`, corrects R-1022's three further
sentences, and tests the ambiguous branch's payload.

`_cmd_run_next_task_local` takes `json_output`, its eight print-then-exit
pairs move onto `fail()`, and the ten tests that monkeypatch it with a
single-positional stand-in accept the keyword in the same commit. The
`_plan_rejected_error` / `_plan_rejected_message` pair collapses to one.
`decision.py`'s refusal pairs move onto `fail()` under DECISION F277 D8's
one-token-per-condition rule; the derived-decision refusal, two unprefixed
lines, stays and is counted.

## Next Steps

1. The non-mechanical `job.py` sites: the verification-failure loop, a bare
   exit after a cost confirmation, two hand-rolled JSON objects — and the
   single-pass `job run --json` success line, which is prose.
2. The remaining groups largest first — `brain`, `project`, `patch`,
   `do_cmd`, `grouped`, `test_cmds`, then the tail; `runtime_cmd.py` is its
   own round.
3. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-four findings are open; R-1022 is this feature's own, is repaired this
round, and has its `Done:` booked in the next. The refusal pairs outside `job.py` and `decision.py` are several
sessions of work, so the soft limit of 7 sessions and 25 rounds is the number
to watch.
