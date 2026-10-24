## F314 — Findings paydown v10

### What changed
- **Self-use generator (R-1418, R-1442, DECISION F314 D2).** The order tier that queued the
  toolchain refresh order is deleted: the order reads the network and every builder tool runs in a
  sandbox without one. Tier 4 offers an excused blind handler only when its excuse names a debt.
- **Gauntlet (R-1281, gauntlet half, DECISION F314 D3).** `run_order` opens its order through
  `repo_mission.accept_order`, so the gauntlet measures the path a person's order takes.
- **`[roles]` table (R-1326, DECISIONs F314 D4 and D5).** A project's `.remedy/config.toml` may name
  its builder and reviewer; the job records the source `roles`; explicit options and a continued
  job's record come first. The planner's half is R-1448, carried.
- **Type checks (R-1425, DECISION F314 D6).** `role_provider_factory.py` and `do_sequence.py` carry
  no mypy error; no ratchet is added.
- **Hosted-runner tests (R-1427, R-1428, DECISION F314 D7).** The harness's repositories carry their
  own git identity; the sandbox's disk search prunes the read-only toolchain by full path.
- **Closure cost (R-1421, DECISION F314 D8)** resolved by measurement from the committed transcripts.
- **Structure step (DECISION F314 D9).** `run_job`'s veto terminal is `settle_veto_terminal` in
  `task_veto.py`; the ledger's top row fell from 1381 to 1310 lines.
- R-1443 to R-1447 and R-1449, raised against this feature's own rounds, repaired inside it.

### Why
The rolling findings paydown (operator amendment amend0911-feedback rule B): the ledger only stays
readable while it also shrinks. Twelve findings resolved, eight carried by name to F316.

### Key decisions
DECISIONs F314 D1 to D9 in `.agent/decisions.md`; operator questions Q24 (two self-use sources go
quiet) and Q25 (one hosted test run, please) in `.agent/operator_questions.md`.

### How to review / test
- Every round's gate entry in `.agent/live_review.md` names the reviewer's re-run selection and the
  mutations that turned each new test red.
- The closure's one full suite: `.agent/authored/f314-closure-suite.txt`, `23783 passed, 11 skipped`,
  exit 0, on `277c8184c` (`python3 -m pytest -n auto -q`, Python 3.10.12).
- Evidence job `f314r8e1001` on `7e02a9110`: `12771 passed, 6 skipped`; review package
  `remedy-review-20261024-030553-READY_FOR_REVIEW.zip`, SHA-256
  `cbcf7163ae8ffa580d6ea95e572df6e29b2260b71129ab428280f7a96687fec3`.
- No hosted CI run: the session's dispatch was refused by the machine's permission settings
  (operator amendment amend1011-manual-hosted-ci; R-1426 and R-1428 stay open for it).

### State
Latest verdict: PASS (round 8; round 9 is the closing round). Open findings: 8, all owned by F316.
Runtime: one session, nine delegated rounds; the self-use run spent two priced calls.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
