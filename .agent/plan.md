# Plan — Steps 775-784: Backend Smoke Python Supervisor

## Goal
Replace Bash shell chaining with Python supervisor so smoke exits cleanly.

## Current Step
784 — Final handoff (complete)

## Steps
- [x] 775: Handoff — Bash chaining is final blocker
- [x] 776: Created scripts/remedy_backend_basis_smoke.py (Python supervisor)
- [x] 777: Shell smoke now thin wrapper → exec python3 supervisor
- [x] 778: Runtime wrapper smoke also Python supervisor
- [x] 779: Contract tests — 8 pass (delegation, isolation, no shell=True)
- [x] 780: Backend smoke — standalone PASS + 166 pytest, clean exit
- [x] 781: Runtime wrapper smoke — propose + worker PASS, clean exit
- [x] 782: Direct proof — 22 passed (helpers + smoke tests + runner tests)
- [x] 783: Completion table — runtime 100%
- [x] 784: Final handoff
