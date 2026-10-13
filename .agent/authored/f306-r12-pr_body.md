## F306 — Findings paydown v8

**What.** The eighth rolling findings paydown (operator amendment amend0911-feedback rule B).
It resolves R-1251 (two runtime-flow checks no longer share one port, and a check refuses a
health answer from a process it did not start) and R-1235 (a job's recorded execution
configuration names the claude-cli configuration its calls ran under, and a manifest written
before still validates), plus R-1275, which the closure's first full suite raised. It takes five
structural steps from the structure ledger: `dev_server_ports.py`, `workspace_identity.py`,
`job_input_definition.py` and `execution_config.py` split off, and `run_job`'s configuration
resolution moved out as `resolve_job_execution_config`. R-1246 and R-1252 are carried to F307, the
next paydown, registered here.

**Why.** The ledger only stays readable while it also shrinks, and every later closure's integrity
precondition reads the open set.

**Key decisions.** DECISIONs F306 D1 to D3 in `.agent/decisions.md`: the slice order (D1); R-1252
carried because its repair is a feature's work, and R-1235's optional key reading landed with the
keys (D2); and the two foreign review folders that appeared in the repository root moved, unchanged,
into the ignored scratch folder `.remedy-wt/remedy-review-moved/` (D3). One reversible ruling waits
for the operator in `.agent/operator_questions.md`: where those two folders should live (Q18).

**How to review.** `docs/roadmap/features/T2_F306.md` (slice list and Built State), then the round
entries `Gate: F306 R1` to `R11` and the `Done:` paragraphs in `.agent/live_review.md` and its
archive. The branch merged nothing in; its fork point is `f51232ee2`.

**Changed files.** 12 rounds over three sessions; the production modules touched are listed in the
review package's manifest and in each round's `.agent/authored/f306-r<N>.md`.

**Verdict.** Rounds 1 to 11 PASS, booked in the ledger (round 9's suite reading void, re-run in
round 10); round 12's verdict is the reviewer's and is booked in the next feature's first commit.
Live review PASS_WITH_RISKS: two Low findings carried with an owner.

**Open findings.** 2 (R-1246 and R-1252, Low, owned by F307).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `0c68adcde` (the tree that
  ships but for records and docs): `22976 passed, 22 skipped, 1 warning in 397.60s`, exit 0
  (`.agent/authored/f306-closure-suite.txt`).
- The evidence job `f306r11e1001`, `python3 .agent/authored/f306-r11-create_f306_evidence.py`, on
  the accepted head `87d132b1d8d35cebcc24df9651043380b56441d2`: 4939 passed, 7 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261014-005334-READY_FOR_REVIEW.zip`, SHA-256
  `bfeb7cd3e0c6771d65f60195d1e6b495a034bd5333e56b35059c0244d5943608`, in
  `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 12 delegated rounds, three sessions; wall clock and model tokens not measured
for the rounds themselves; the closure's self-use run used two provider calls and 2796 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
