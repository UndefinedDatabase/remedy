# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
What a program relies on when it drives Remedy is true and written down once: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, and one document generated from the code names
every operation, field, word, token and exit code (docs/roadmap/features/T12_F298.md). DECISION
F298 D1 fixes the slices and their order; D2 names the document the machine client interface.

## Current Step
Session 1, round 2: T001's first part. `apps/cli/client_interface.py` builds the interface from
the code (operations with arguments and exit codes, exit-code meanings, envelope, job states,
mission status words, contract templates, budget kinds, version 1.1), `remedy client interface`
prints it, the page names the command; round 1's verdict is booked.

## Next Steps
1. T001, next part: the keys every operation's answer and the digest return, and the refusal
   tokens, added to the interface, with a test that drives the real commands and fails when the
   code returns a key the interface does not name or the interface names one the code does not.
2. T001, last part: `docs/system/machine-client-contract-v1.md` rendered from the interface, and
   the test that fails when page and interface differ.
3. T002: an order runs in the repository of the project it names, or is refused before any step.
4. T003: honest refusals under `--approve --json`, and one command that declines a result.
5. T004: the second gate test — commit and push, two jobs, one order file started twice.
6. T005, T006, T007; then the amend0930b-slow-cap hardening stage and the closure sequence.

## Risks
- F298 is large for 25 rounds; D1 names the split point if the soft limit is reached.
- The operator's data root holds 11,652 jobs and 13,480 open decisions, so T007's default matters.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.
