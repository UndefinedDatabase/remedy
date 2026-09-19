
## Built State (F273, 2026-09-19)

What exists on disk at the close of F273; every DECISION named lives in `.agent/decisions.md`, every
finding and its resolution in `.agent/live_review.md` or, once rotated, its archive.

**The open set.** `scripts/rotate_live_review.py::count_open_findings` read 130 open findings at the claim
base `80f7c529`, 57 at the start of the third session (`b22fe3bc`) and 16 at round 20's handoff
(`c8b91d87`), three of which round 20 landed. Rounds 1 to 20 booked a resolution for every id of T001's
built five but R-0803 and R-0807, and for every id of T002 to T016 but R-0499, R-0622, R-0662 and R-0984; for
each id the Acceptance names but R-0803, R-0807 and R-0892; and for ids registered after the claim and
owned by this feature, among them R-0987 to R-0996, which F273's own rounds found and repaired.

**What changed in the product, by the DECISIONs that ruled it.** The suite writes into an isolated data
root and fails loudly if the configured one changes (R-0803's fixture; its proof is the closure suite).
The integration gate's procedure, the ledger and budget readers, the undefined name and the repository-wide
`ruff` stage, the CLI list options and the job resume move, the command door's closure guard, the
postmortem taxonomy, the bench orders, the evidence package, the self-use track and the docs pins were
repaired slice by slice (DECISIONs F273 D1 to D14). Round 15 onward: the job views read intent ids from the
approval queue, and the manifest drift check and the conventions loader went (D15); the repair loop, the
repair-request builder and their cockpit sections went whole, and the humanize catalog contract reads a
module's forwarding helpers (D16); the operator-attestation writer and its export overlay went while the
closure evidence producer stayed, and the worker queue, the goal-driven path and `worker status` went with
the coupling ceiling held (D17); a definition-of-done check writes no bytecode, each `do` job serves its
milestone without being held on it, and the memory-candidate store went (D18); the moot and met ids were
booked, dead residue went, and DECISION F260 D3 gained the sentences four findings asked of it (D19); and
the direct-API provider keeps its usage and caches its stable prefix, one guard proves every collected
test runs in some CI stage, and the vitest ceiling is measured (D20).

**Carried.** R-0803, R-0807 and R-0984 are resolved by this closure's own evidence: the closure suite's
transcript, the closure self-use run's ledger rows against its calls, and the 3.12 column of the closure
pull request's hosted CI. R-0892 waits on the operator's write of the skill page. R-0499, R-0622, R-0662,
R-0819, R-0820, R-0829, R-0866, R-0880 and R-0950 stay open and move to the next findings-paydown feature
in the closure's ownership paragraph (DECISION F273 D19 (5)).
