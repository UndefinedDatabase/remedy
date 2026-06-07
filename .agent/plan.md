# Plan — Steps 755-764: Backend Smoke Final Isolation

## Goal
Make backend smoke boring and reliable. No runtime pytest wrappers inside it.

## Current Step
764 — Final handoff (complete)

## Steps
- [x] 755: Handoff — smoke runs wrappers which can hang in reviewer env
- [x] 756: Backend smoke uses standalone runtime + helpers + orchestration only
- [x] 757: Created scripts/remedy_runtime_wrapper_smoke.sh (separate wrapper verification)
- [x] 758: Hardened remedy_pytest.sh with --kill-after=10s (GNU timeout)
- [x] 759: Wrappers pass individually (propose 0.73s, worker 0.88s)
- [x] 760: Backend smoke — standalone PASS + 166 pytest tests, clean exit
- [x] 761: Runtime wrapper smoke — propose + worker PASS, clean exit
- [x] 762: Completion table — runtime 100%
- [x] 763: Final baseline — all commands pass
- [x] 764: Final handoff
