
### Q5 — contract jobs are granted automatically (2026-09-18, F269, round 6)

What needs deciding: until now a person had to grant a job, one command at a time, the right to run the repository's tests, to write a generated patch into the repository, and to revert such a write, and had to attach the repository to the job by hand. Those two commands are now removed. Instead, every job that belongs to a mission with a contract is attached to its repository and given those three rights automatically when it is created, because the contract is the order the operator accepted for that repository.

Why it matters: it removes a manual safety step. A job of a planned mission can now run tests, write generated patches and revert them without a separate grant. A job of a mission that was never planned has no way to receive these rights at all.

My recommendation: keep the automatic grants for contract jobs. The three rights are exactly what the remaining test, patch and self-run commands check, and the manual step only ever granted the same three.

What happens if you say nothing: the recommendation is already executed and stands until you say otherwise.
