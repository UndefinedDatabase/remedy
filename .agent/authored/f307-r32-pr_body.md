## F307 — Findings paydown v9

**What.** The ninth rolling findings paydown (operator amendment amend0911-feedback rule B). Of
the 88 findings open at its claim it resolves 49 with a resolution line naming its evidence, books
the 33 findings that operator branches had repaired (R-1375) with the pull request and the test of
each, and records R-1301 as resolved by deletion. It also repairs eight of the nine findings its
own rounds raised, among them R-1420, which the closure's first full suite found. Behaviour a
person sees: a blocked job keeps its finish time and its retry runs the blocked task again; an
order naming one file by a plain word is resolved to it; a middle lane sits between the bounded and
the full lane; the story and the digest show the dirty files a job started from; both doctor
commands answer one check shape; a `remedy.toml` that does not parse is refused with
`config_invalid`; a backup link of the failover chain books its own calls, stream artifacts and
governor slot. Structural steps from the structure ledger: `run_job`'s step (3) begun, the
provider call, the Ollama and the fake provider, the job report, the `job run` catalog entry and
the doctor's dead-model helpers each moved to a module of their own, and `ui_server.py` renamed
`serve_http_handler.py`. R-1246, R-1281's rest, R-1326, R-1351, R-1353 and R-1418 are carried to
F314, the next paydown, registered here.

**Why.** The ledger only stays readable while it also shrinks, and every later closure's integrity
precondition reads the open set.

**Key decisions.** DECISIONs F307 D1 to D28 in `.agent/decisions.md`: the slice order (D1, D5);
the umbrella writer removed while its readers wait for the operator's reconcile (D12); the data
root guard's two levels and the folders a running supervisor writes (D25); the rename of
`ui_server.py` with no alias left (D26); and R-1326 carried behind `run_job`'s structural steps
(D28).

**How to review.** `docs/roadmap/features/T2_F307.md` (slice list, Acceptance and Built State),
then the round entries `Gate: F307 R1` to `R31` and the `Done:` paragraphs in
`.agent/live_review.md` and its archive. The branch merged nothing in; its fork point is
`eeed13064`.

**Changed files.** 32 rounds over seven sessions; the production modules touched are listed in the
review package's manifest and in each round's `.agent/authored/f307-r<N>.md`.

**Verdict.** Rounds 1 to 31 PASS, booked in the ledger (round 29's suite red on R-1420, repaired
and run again green in round 30); round 32's verdict is the reviewer's and is booked in the next
feature's first commit. Live review PASS_WITH_RISKS: six findings carried with an owner.

**Open findings.** 6 (R-1246, R-1326, R-1353 and R-1418 Low; R-1281 and R-1351 Medium), owned by
F314.

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `412ca4e91` (the tree that
  ships but for records and docs): `23183 passed, 11 skipped, 1 warning in 328.36s`, exit 0
  (`.agent/authored/f307-closure-suite.txt`).
- The evidence job `f307r31e1001`, `python3 .agent/authored/f307-r31-create_f307_evidence.py`, on
  the accepted head `a100201f3a40b1f07ac02abd470836c336e843f1`: 11501 passed, 6 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261022-061118-READY_FOR_REVIEW.zip`, SHA-256
  `e49aa6fde92a4f6c69f5994c3a58e9b7734acef64713a9ee14d118db988dbfd8`, in
  `~/Repos/remedy-history/zips`.

**Runtime actuals.** 32 delegated rounds, seven sessions; wall clock and model tokens not measured
for the rounds themselves; the closure's self-use run used two provider calls and 30504 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
