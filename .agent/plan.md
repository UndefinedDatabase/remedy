# Plan — F151 Worker adapter contract v2

## Goal
Give the neutrality promise its interface: a typed adapter contract (capabilities, invocation
building, stream and usage mapping, isolation) with a reusable conformance kit, today's builder path
wrapped as the reference adapter with golden equality, and orchestration importing only the contract.

## Current Step
Round 10, the closing round, BLOCKED mid-round. C1 (book round 9, Built State) and C2 (ledger
rotation) are committed and pushed. C3's three files (STATUS line, README sync, SU-078
consumed_by) are written in the working tree, byte-verified against the prep folder, and gates 1
and 2 passed. Gate 3 (`python3 .remedy-wt/f151-r10/prep/gate3.py .`) returned exit 1 instead of
the required exit 0, with the identical passed count (793) and no FAILED/ERROR/SKIPPED line, which
points at `tests/conftest.py`'s `pytest_sessionfinish` hook flipping `session.exitstatus` on a
leftover process or a changed configured data root (R-0803/F293 T003) rather than a test failure —
most likely caused by another `remedy` process active on this machine during the run (`remedy serve
start` since 2026-10-20 and a `do run --json --no-ui --run-unattended -- order.md` process started
the same afternoon). The block forbids a second invocation of gate 3's test selection, so this was
not re-run to confirm. Per the block's own rule ("if a gate goes red, STOP"), the round stops here:
no C3 commit, no handoff-bundled-with-C3, no push of C3, no pull request.

## Next Steps
1. Confirm no other `remedy` process (serve daemon, `do run`, loop-runner) is active on this
   machine, then re-run `python3 .remedy-wt/f151-r10/prep/gate3.py .` exactly once.
2. If it reads exit 0 with 793 passed and no FAILED/ERROR/SKIPPED: run gates 4 and 5, commit C3
   (the three files already sit correctly in the working tree) with the handoff, push, and open the
   pull request — the rest of block.md's C3 step and THEN clause, unchanged.
3. If gate 3 is genuinely red (a real failure), stop again and report it; do not weaken or route
   around it.

## Risks
- The round's own commits (C1, C2) are clean and pushed; the blocker is environmental (a shared
  data root/process collision), not a defect in F151's code, but this is not proven — only
  circumstantial.
