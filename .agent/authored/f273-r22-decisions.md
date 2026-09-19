
## DECISION F273 D21 (2026-09-19, reviewer, round 22) — the closure suite's one bad node is repaired by a stronger property, never by a lower floor
CONTEXT: F273's closure suite at `d2fc05b8` read one failed node, the retired-status scan's anti-blindness
guard, which asserts more than 300 tracked production `.py` files. F273's deletions took that count from
310 at the fork point to 299; `main`'s hosted CI at the fork point was green, so the node is this
feature's to repair under amend0917-throughput (2), and R-0997 records it.
CHOSEN: the guard asserts that the scan's corpus holds every tracked production file that calls
`load_job_plan` or `require_job_plan`, found by `git grep` independently of the `git ls-files`
enumeration, and that at least one exists. That names the files the scan exists to read, so it fails
when the enumeration loses any of them, as the reviewer's dry run showed by dropping `apps` from it,
and it no longer falls with the size of the repository. This is the first of at most three repair
rounds; the round re-runs the full suite once, and its bad set must shrink strictly with no node newly
bad.
ALTERNATIVES: lowering the floor to 250, rejected as a weakened assertion that the next deletion
crosses again; marking the node `xfail`, rejected because the repair is one test.
REVERSE: restore `tests/orchestration/test_job_plan_state_reads.py` from `7e717bc4`, and delete this
paragraph.
