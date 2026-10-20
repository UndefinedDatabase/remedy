# F310 round 4 — amendment 3 (reviewer, after the worker's second stop at gate 3)

The worker stopped at gate 3, correctly, on
`tests/cli/test_client_interface.py::test_f295s_gate_test_is_unchanged`, which pins the bytes of F295's
gate test that amendment 2 changed. The pin's own comment asks that a deliberate change updates it
in the same commit and that its DECISION says why. The worker's reading of the client digest, which
carries no payload, through `budget_stop_blockers` in the test's own process is accepted.

1. A new commit C4c goes after C4b, subject
   `F310 R4 C4c: the F295 gate test's pin follows its deliberate change`, paths
   `tests/cli/test_client_interface.py`, `.agent/decisions.md` and `.agent/authored/f310-r4-amend3.md`
   (a Python byte copy of `.remedy-wt/f310-r4/prep/amend3.md`).
2. `F295_GATE_TEST_SHA256` becomes the sha256 of `tests/cli/test_machine_client_contract.py` as C4b
   left it, computed with a Python sha256 reader at C4c and reported in the handback. Nothing else in
   that file changes.
3. Append to `.agent/decisions.md` the bytes of `src-d6-gate-test.md`, as they are.
4. Then re-run gate 3 once, run gates 4 and 5, write C5 and push. The handback's deviations name the
   three stops and the three amendments.
