# F055 round 3 — amendment 1

`verify.py` was narrower than the round: declaring exit 3 for `job.run` also moves the exit-code
guide table and the client interface's declared tokens, which `tests/cli/test_exit_codes.py` and
`tests/cli/test_client_interface.py` hold, and its check of the warning read the source as one
line. Both are the reviewer's slips; C1 to C5 stand as committed.

1. C3 may name `apps/cli/client_interface.py` and `docs/guides/exit-codes.md`, and C4 may name
   `apps/cli/client_interface.py`, each changed only as those two tests require.
2. Restore `packages/orchestration/do_rehearsal.py` in the working tree to C5's bytes
   (`git -C /home/decodeux/Repos/remedy checkout -- packages/orchestration/do_rehearsal.py`); the
   wrapped f-string stays as committed. `verify.py` now reads the warning across adjacent string
   literals.
3. `verify.py` is replaced by the version whose digest the prompt gives. C6 also carries
   `.agent/authored/f055-r3-amend1.md`, a Python byte copy of this file, its sha256 reported.
4. Run gates 1 to 6 once each now, gate 3 included, then C6 and the push. The handback names
   this amendment and the first gate-1 reading in its deviations.
