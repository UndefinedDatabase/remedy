# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D4).

## Current Step
Round 5 on `feature/f058-model-failover-chain`, session 3: book round 4's verdict (PASS, R-1262
registered, R-1261 resolved), repair R-1262, write the documentation page
`docs/system/model-failover-v1.md` with its two rows in `docs/README.md`, and the feature file's
Built State.

## Next Steps
1. The closure's integration gate: the feature's one full suite, its transcript
   `.agent/authored/f058-closure-suite.txt` and the suite-cost lines.
2. The closure's self-use item, evidence job, review zip and closing round, per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- `run_pingpong`, `export_pingpong_json` and `_call_with_retry` are rows of
  `docs/system/structure-ledger-v1.md` that may not grow.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
