# Plan — Steps 765-774: Pytest Wrapper Process Isolation

## Goal
Make remedy_pytest.sh pipe-safe so backend smoke exits cleanly everywhere.

## Current Step
774 — Final handoff (complete)

## Steps
- [x] 765: Handoff — smoke hangs because remedy_pytest.sh inherits pipes
- [x] 766: Created scripts/remedy_pytest_runner.py (Popen + temp files + killpg)
- [x] 767: Wired remedy_pytest.sh to call runner instead of direct timeout pytest
- [x] 768: Runner contract tests — 8 passed (existence, patterns, pass/fail/timeout)
- [x] 769: Backend smoke — standalone PASS + 166 pytest, clean exit
- [x] 770: Runtime wrapper smoke — propose + worker PASS, clean exit
- [x] 771: Direct wrapper proof — helpers 6 pass, orch+storage 160 pass
- [x] 772: Completion table — runtime 100%
- [x] 773: Final baseline — all commands pass
- [x] 774: Final handoff
