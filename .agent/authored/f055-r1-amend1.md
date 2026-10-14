# F055 round 1 — amendment 1

The block missed a generated page and left one order ambiguous. Both are the reviewer's slips.

1. C4 gains two paths:
   - `docs/system/machine-client-contract-v1.md`, regenerated with exactly
     `python3 -c "from apps.cli.client_interface import write_client_interface_page; write_client_interface_page()"`
     after the catalog's `--rehearse` line exists; `tests/cli/test_client_interface.py` holds the
     page equal to the interface, and the flag adds a row. Nothing else edits the page.
   - `.agent/authored/f055-r1-amend1.md`, a Python byte copy of this file, its sha256 reported.
2. `stop_walk_for_rehearsal` walks `ctx.job_ids` ONCE: for each job, the approval line (when its
   task plan waits for approval) and then that job's `remedy job run` line, so each job's two
   lines stand together, as `_run_the_walks_jobs` orders them for a job it stops at.
3. `verify.py` is replaced by the version whose digest the prompt gives; it requires both paths in
   C4 and the amendment's copy byte-equal.
4. Everything else in the block stands. Commit C4 as ordered once the two paths are in, then C5,
   the gates and C6. The handback names this amendment in its deviations, with the worker's one
   slip there too: an edit drafted on `main` before C0, stashed and moved onto the branch before
   any commit.
