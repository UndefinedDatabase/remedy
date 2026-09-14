# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, the classic runner's whole
command surface is gone as of round 34, the record flip landed in round 101, and the bridge
it opened closed at exit 0 in round 103.

## Current Step

ROUND 104 DELETES THE CLASSIC STORE, the rest of T003. `packages/orchestration/storage.py`
and the classic `Job` and `Task` models go; `JobNotFoundError`, `JobStoreError` and the one
atomic text writer move into `packages/orchestration/pingpong_job.py`; the job-id resolver
searches the one store; `resolve_any_job_id`, the adapters and every which-store branch go;
docstrings and `docs/system/` stop describing two stores; and `tests/orchestration/test_one_job_store.py`
pins the absences F260's Acceptance names. The change is one commit, applied from the
reviewer's staged dry run and proved by tree identity, and the round books round 103's verdict,
resolves `R-0885` and `R-0886`, and registers `R-0887` and `R-0888`.

## Next Steps

1. REPAIR `R-0887` and `R-0888`: the one dashboard builder emits `prompt_trace` again, and four
   string attribute probes read the unified record's own field names, each with its test.
2. T001'S CLOSING OBLIGATIONS, re-measured against the tree: DECISION F260 D3, the deletion
   paragraph naming every deleted module and its heir, if it is not yet on disk; the
   deletion map at zero cluster lines; and the open findings this feature owns.
3. THE CLOSURE SEQUENCE, with the integration gate's full-suite runs and the ledger rotation.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE BRIDGE IS CLOSED: from round 104 a round whose suite adds a bad node is FAIL, apart from
  a node whose isolated re-runs all pass, which is reported flaky.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 91 by distinct id at this round's base and again 91 once `R-0885` and
  `R-0886` are resolved and `R-0887` and `R-0888` registered, with `R-0809`, `R-0880`,
  `R-0883` and `R-0884` open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's.
