# F310 round 4 — amendment 2 (reviewer, after the worker's stop at gate 3)

The worker stopped at gate 3, correctly, on
`tests/cli/test_machine_client_contract.py::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line`:
it asserts that a budget stop puts two decisions in front of a client, the budget decision and the
remainder decision, and that the `extend` closes the second. That is the behaviour DECISION F310 D6
deletes, so the test pins the replaced mechanism and is changed with it (AGENTS.md, "Replacing is
deleting").

1. A new commit C4b goes after C4, subject
   `F310 R4 C4b: a program driving an order sees one question at a budget stop`, paths
   `tests/cli/test_machine_client_contract.py` and `.agent/authored/f310-r4-amend2.md` (a Python byte
   copy of `.remedy-wt/f310-r4/prep/amend2.md`).
2. In that one test, the client now reads ONE decision for the stopped job: the `token_budget`
   decision, whose payload carries the mission's blocking criteria under `blockers` (not empty), and
   no `task_decision`; the `extend`'s `closed_decisions` is `[]`. Every other step and assertion of
   the test stays as it is; a one-sentence comment above the changed assertions cites DECISION
   F310 D6. No other test of the file changes.
3. Then re-run gate 3 once, run gates 4 and 5 (gate 5 reads 89), write C5 and push. The handback's
   deviations name this stop and amendment 2.
