## F297 — Findings paydown v7

**What.** The seventh rolling findings paydown (operator amendment amend0911-feedback rule B).
It resolves 26 of the 29 review findings open at its claim, each with a test that fails without
its repair and a reviewer mutation that proved it, and takes the structural step that closes a
paydown: the burn alarm's trip handler left `run_job` for `record_burn_trip` in
`packages/orchestration/job_burn.py`. R-1235, R-1246, R-1251 and R-1252 are carried to F306, the
next paydown, registered here; R-1248 moved to F305.

**Why.** The ledger only stays readable while it also shrinks, and every later closure's integrity
precondition reads the open set.

**Key decisions.** DECISIONs F297 D1 to D12 in `.agent/decisions.md`: the slice order (D1); the
repairs of each round (D3 to D12), among them the order and run starts' own refusals stated as the
route's own (D10), a changed mission listing its jobs as changed (D11), and the burn samples kept in
the job's `metadata` (D12). Two reversible rulings wait for the operator in
`.agent/operator_questions.md`: the toolchain job's raised budget (Q13) and the vocabulary page's
new meaning of a mission (Q14).

**How to review.** `docs/roadmap/features/T2_F297.md` (slice list and Built State), then the
round entries `Gate: F297 R1` to `R13` and the `Done:` paragraphs in `.agent/live_review.md` and
its archive. The branch merged `main` at `f83708293` (pull requests 326 and 327) in F297 R12 C2.

**Changed files.** 14 rounds over two sessions; the production modules touched are listed in the
review package's manifest and in each round's `.agent/authored/f297-r<N>.md`.

**Verdict.** Rounds 1 to 13 PASS, booked in the ledger; round 14's verdict is the reviewer's and is
booked in the next feature's first commit. Live review PASS_WITH_RISKS: four Low findings and one
Medium carried with owners.

**Open findings.** 5 (R-1235, R-1246, R-1251 and R-1252, Low, owned by F306; R-1248, Medium, owned
by F305).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on `ab7d2821c` (the tree that ships but for
  records and docs): `22603 passed, 22 skipped, 1 warning in 346.90s`, exit 0
  (`.agent/authored/f297-closure-suite.txt`).
- The evidence job `f297r13e1001`, `python3 .agent/authored/f297-r13-create_f297_evidence.py`, on
  the accepted head `d10d817b77aaf5af8b4f71a217cfb927cecb2201`: 4181 passed, 4 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261012-012716-READY_FOR_REVIEW.zip`, SHA-256
  `8f11b8ab92ce64b7aa2a15d699852ba9818b45059e2dd716b5d6ea0de59142e2`, in
  `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 14 delegated rounds, two sessions; wall clock and model tokens not measured
for the rounds themselves; the closure's self-use run used two provider calls and 2763 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
