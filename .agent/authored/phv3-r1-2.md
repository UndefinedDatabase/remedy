  5. **Docs-round gate (PH v3, operator ruling 2026-07-28):** any
     round whose change set includes docs/roadmap/** gates with
     `python3 -m pytest tests/docs/ -q` in addition to the canary;
     a ledger-count change and its test pin land in the SAME commit
     (R-0151 — the F251 registration broke the feature-ledger pins
     because its gate was canary-only).
