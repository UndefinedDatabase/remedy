## What

F298 — Machine client contract v1.1: what a client can rely on, first part. A program that drives
Remedy can now ask Remedy itself what it may rely on, and the answer is read from the code, never
written by hand.

- **T001, the contract is data.** `remedy client interface --json` prints the machine client
  interface that `apps/cli/client_interface.py` reads from the code: every operation a client uses
  with its arguments, whether each argument takes a value and may be repeated (read from the
  command line's own parser), its exit codes, its refusal tokens and its answer keys, the keys
  under those keys as trees, the digest's keys, the job states, mission status words, contract
  templates and budget kinds, the envelope, the exit codes' meanings and the interface's own
  version, `1.1`. The last section of `docs/system/machine-client-contract-v1.md` is that interface
  rendered between two markers; the walk through the path above it stays written by hand.
  `tests/cli/test_client_interface.py` holds each part to the code that produces it and to a real
  run, and the page's section to the rendering.
- **The split (DECISION F298 D21).** F298 reached 20 of its 25 rounds with T002 to T007 open, so it
  closes at T001's scope. T002 to T007 moved, word for word with their Acceptance lines, to F304,
  registered directly after F298 and before F253.
- **The hardening stage (SLOW MODE).** A fresh auditor split what F298 keeps into sixteen claims
  and tried to break each with a mutation; fifteen were proved at once. One gap and one observation
  were registered (R-1179, R-1180) and repaired by tests: a pin of F295's gate test and a check of
  every command and flag it drives. A repeat audit found no gap.
- **The closure's repair.** The one full suite found three modules the interface now reaches
  missing from the reachability allowlist (R-1181); they joined it, and the suite ran again green.

## Why

The universe workspace built Luna, Remedy's first client, against F295's hand-written page and
could not rely on it: the page named too little. A client needs one document, generated from the
code, that names every operation, field, word, token and exit code it meets, and a test that fails
when the code and the document differ. F253's HTTP API will serve the same operations.

## Key decisions (in `.agent/decisions.md`)

- D1: the feature file's slice order, the contract as data first.
- D2 to D18: the interface's parts, one per round, each held to the code that produces it: the
  operations, the digest's key tree, the refusal tokens, the answer keys and their trees.
- D19: whether an argument takes a value and may be repeated is read from the parser (R-1178).
- D20: the page's last section is the interface rendered; the walk stays written by hand.
- D21: F298 closes at T001's scope; T002 to T007 move to F304.
- D22: the hardening stage's audit and its two repairs.
- D23: the reachability repair and the second full suite.

## How to review / test

- Read `docs/roadmap/features/T12_F298.md`'s Built State first, then the last section of
  `docs/system/machine-client-contract-v1.md`.
- `python3 -m apps.cli.main client interface --json`
- `python3 -m pytest -q tests/cli/test_client_interface.py tests/cli/test_machine_client_contract.py tests/cli/test_golden_path.py`
- The closure suite transcript is `.agent/authored/f298-closure-suite.txt`: `21658 passed, 22
  skipped`, exit 0, 1084.16 CPU seconds, 3.4 percent more than F116's closure.

## Changed files (outside `.agent/`, fork point `77493e0f9` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 14 | 2 |
| `apps/cli/client_interface.py` | 831 | 0 |
| `apps/cli/command_catalog.py` | 13 | 0 |
| `apps/cli/commands/__init__.py` | 2 | 1 |
| `apps/cli/commands/client_cmd.py` | 42 | 0 |
| `docs/README.md` | 1 | 1 |
| `docs/agents/planner_reviewer_prompt.md` | 31 | 0 |
| `docs/roadmap/STATUS.md` | 2 | 1 |
| `docs/roadmap/features/T12_F298.md` | 62 | 0 |
| `docs/roadmap/features/T12_F304.md` | 107 | 0 |
| `docs/system/machine-client-contract-v1.md` | 468 | 4 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/test_cli_ux.py` | 5 | 4 |
| `tests/cli/test_client_interface.py` | 1533 | 0 |
| `tests/docs/test_docs_consistency.py` | 4 | 1 |
| `tests/orchestration/import_reachability_allowlist.txt` | 5 | 0 |

## Verdict and evidence

- Latest live review verdict: PASS (round 28); F298 accepted PASS_WITH_RISKS, the risks being the
  open findings below.
- Evidence job `f298r28e1001`, package `remedy-review-20261008-040539-READY_FOR_REVIEW.zip`,
  SHA-256 `03a2010e37b33146587b9ff952a22dd8962dd3c1678354e8e28d97c488452f8d`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `d667e5b49`.
- Resolved on this branch: R-1177 to R-1181.
- Open findings: 11, all owned by F297, Findings paydown v7, all carried from earlier features:
  R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and
  R-1176 (Low).

## Runtime actuals

- Rounds: 29, in 6 sessions, on 2026-10-07 and 2026-10-08. Every round passed review.
- Models: the workers' commit trailers name Claude Sonnet 5.5 and Claude Sonnet 5; the sixth
  session's reviewer ran on
  Claude Opus 5.5. The closure's self-use job SU-048 ran on `claude-cli` / `claude-sonnet-4-6`: 4
  provider calls, a measured $1.79 against a $6.00 budget, completed with the reviewer's verdict
  pass after one repair round, never applied.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: two, in rounds 25 and 26; the first found R-1181, the second was green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
