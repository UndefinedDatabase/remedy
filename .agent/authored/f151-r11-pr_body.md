## F151 — Worker adapter contract v2

**What.** `packages/contracts/adapter_contract.py` defines `WorkerAdapter`, the one contract any
builder or reviewer backend fills: `capabilities(model)` (vision, JSON schema, session resume,
streaming, tool use, context size), `build_invocation(role, prompt_parts, options)` answering a CLI
or an HTTP invocation, `map_stream` into the stream vocabulary, `map_usage` keeping the provider's
raw counters, `classify_error` into `FailureClass`, and a reserved `isolation()`.
`packages/contracts/adapter_conformance_kit.py` is the reusable kit: seven dimensions, each proved
by a broken toy adapter, the last refusing any retry, timeout, sleep, backoff, process or network
use in the adapter's class chain. `packages/providers/adapters/claude_cli_reference.py` wraps
today's claude-cli functions as the reference adapter with golden equality against them.
`WorkerProviderSpec.adapter_ref` links the v1 worker list to the v2 adapter, resolved by
`packages/providers/adapters/adapter_registry.py` and shown by `remedy worker show`. An AST import
guard keeps `packages/orchestration/` and `packages/contracts/` off every concrete adapter.
`LLMWorker`, the unimplemented worker protocol, is deleted.

**Why.** The neutrality promise needs a load-bearing interface so a vendor adapter plugs in without
touching orchestration, and a kit that fails an adapter which re-implements the loop's transport.

**Key decisions.** DECISIONs F151 D1 to D5 in `.agent/decisions.md`: the worker registry and the
main builder adapter the feature file names were deleted by F275, so the contract reconciles with
what survives and restores nothing (D1); the contract and the kit live under `packages/contracts/`,
with the ownership table and seven kit dimensions (D2); the transport dimension reads the whole
class chain and exempts only `FailureClass` members (D3); the reference adapter re-implements
nothing and the loop is not rewired (D4); the registry linkage, `remedy worker show` as the product
path, the import guard, and `LLMWorker` deleted (D5).

**How to review.** `docs/roadmap/features/T8_F151.md` (slice list and Built State),
`docs/system/worker-adapter-contract-v1.md`, `.agent/f151_inventory.md`, then the round entries
`Gate: F151 R1` to `R9` in `.agent/live_review.md` (moved to the archive by the closing rotation where
the rotation rules say so). Production code: the three modules above, `packages/providers/adapters/__init__.py`,
`packages/orchestration/worker_adapters.py`, `packages/contracts/interfaces.py` and
`apps/cli/commands/worker.py`. Tests: `tests/contracts/` (the kit against broken toys, the contract,
the reference adapter's goldens, the registry, the import guard with its violation fixture),
`tests/cli/test_worker.py` and `tests/test_worker_adapters.py`. The branch merged nothing in; its
fork point is `4232c579e`.

**Changed files.** Eleven rounds in two sessions; the review package's manifest lists the reviewed
range of 40 commits.

**Verdict.** Round 1 PASS; rounds 2 to 5 FAIL on Low findings the reviewer's mutation runs and
reading found (R-1435 to R-1440), each repaired and resolved with its red-proof; round 6 PASS; round
7 FAIL on R-1441, a command name on the docs page that the closure's first full suite caught; rounds
8 and 9 PASS. Round 10 stopped before its last commit when its gate selection read exit 1 with
every test passed, because another session's job wrote into the shared data root during the run; the
reviewer re-ran the selection on the same bytes and read exit 0, and round 11 finished the closure.
The verdicts of rounds 10 and 11 are the reviewer's and are booked in the next feature's first
commit.
Live review PASS: every finding F151 raised is resolved, and it owns no open finding.

**Open findings.** 11 (R-1246, R-1281, R-1326, R-1351, R-1353, R-1418, R-1421, R-1425, R-1426,
R-1427 and R-1428), all owned by F314.

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `7e32f147e` (the tree that
  ships but for records): `23670 passed, 11 skipped, 1 warning in 366.73s`, exit 0
  (`.agent/authored/f151-closure-suite.txt`); the cost script read 7.2 percent below F133's, within
  the 10 percent limit.
- The evidence job `f151r9e1001`, `python3 .agent/authored/f151-r9-create_f151_evidence.py`, on the
  accepted head `76fd568651d04b420027a0f0a233b458fdcc9896`: 12579 passed, 6 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261023-180445-READY_FOR_REVIEW.zip`, SHA-256
  `ff7cc953206489a10d4197704b1016b77d5284f5255e8ba34e34aee3b1906f5c`, in
  `~/Repos/remedy-history/zips`.

**Runtime actuals.** Eleven delegated rounds in two sessions, the branch's commits from 15:15 to the
closing round on 2026-10-23; model tokens of the rounds themselves not measured; the closure's
self-use run used two provider calls and 3149 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
