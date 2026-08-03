# Handback — F070 R1 (SPLIT, LARGE bundle: gate + claim + verb map + T001 + T002)

## Range
Review of `afbe2639`..`d5428fb5` on `feature/f070-orchestrator-loop`.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 Open PR Gate + merge #175 | done | |
| 2 branch | done | |
| 3 save authored 1-4 + sha256 | done | 4/4 match BEGIN digests |
| 4 apply 1-3 by copy, 4 FROM→TO | done | |
| 5 context.md vs full reader list | done | 7 assertions collected from 13 readers |
| 6 claim commit + docs gate + canary | done | |
| 7 verb map | done | every enumerated verb exists; 2 gaps resolved, not blocking |
| 8 move schema + unknown-kind test | done | |
| 9 context assembly, dossier first | done | dossier is a seam (F071 absent) |
| 10 loop skeleton | done | |
| 11 ledger writer + CLI | deviated | ledger done; CLI deferred to T003 (permitted, recorded) |
| 12 protocol document | done | `docs/agents/orchestrator_protocol.md` |
| 13 T001 tests + verify | done | |
| 14 evaluation + A9 refuse/re-prompt/escalate | done | |
| 15 dossier update every iteration | done | |
| 16 era corpus + one test per class | done | 5 classes, real commits cited |

## Commits
### 29184761 chore(f070): claim F070 and reset agent state for R1
| Path | +/- | Reason |
| .agent/authored/f070-r1-1..4.md | +104/-0 | reviewer-authored texts, verified |
| .agent/live_review.md · plan.md · candidates.md | +72/-110 | applied by copy |
| .agent/context.md | +53/-46 | worker-authored for F070 |
| docs/roadmap/STATUS.md | +1/-1 | claim `[ ]`→`[~]` |
### 8bdec7df docs(f070): record the Phase 2 verb map before any loop code
| .agent/decisions.md | +56/-0 | verb map, inspection only |
### 170e2691 refactor(f070): extract the --yes auto-approval into flight_plan
| apps/cli/commands/do_cmd.py | +6/-16 | calls the extracted verb |
| packages/orchestration/flight_plan.py | +37/-0 | `auto_approve_flight_plan` (A6) |
### 6095fb87 feat(f070): add the OrchestratorMove schema, protocol doc and role config
| packages/orchestration/orchestrator_move_schema.py | +112/-0 | `om1`, the authority boundary |
| packages/orchestration/schemas/models.py | +11/-0 | registers `om1` |
| docs/agents/orchestrator_protocol.md | +78/-0 | the versioned protocol |
| docs/README.md | +2/-0 | index rows |
| packages/orchestration/config.py | +26/-0 | `orchestrator.model`, `.max_iterations` |
| packages/orchestration/role_config.py | +8/-0 | `orchestrator` role, same defaults |
| tests/orchestration/test_role_config.py | +5/-1 | pinned tuple grew by one |
### daaa0845 feat(f070): add the protocol reader and pin the move schema
| packages/orchestration/orchestrator_loop.py | +83/-0 | read-only protocol reader |
| tests/orchestration/test_orchestrator_loop.py | +214/-0 | schema + protocol tests |
### ff8160d0 feat(f070): assemble the orchestrator context, dossier first
| packages/orchestration/orchestrator_loop.py | +176/-0 | dossier-first assembly |
| tests/orchestration/test_orchestrator_loop.py | +68/-0 | prefix stability pinned |
### 27e34fa9 feat(f070): add the append-only decision ledger and milestone bookkeeping
| packages/orchestration/orchestrator_loop.py | +248/-3 | JSONL ledger, cost actuals |
| tests/orchestration/test_orchestrator_loop.py | +165/-0 | append-only, torn line |
### d7e6fc35 feat(f070): add run_mission — the loop skeleton over the existing verbs
| packages/orchestration/orchestrator_loop.py | +342/-0 | `run_mission`, `execute_move` |
| tests/orchestration/test_orchestrator_loop.py | +129/-0 | every move kind once |
### 088ea46c test(f070): pin the stop-within-one-iteration and ledger-coverage rules
| tests/orchestration/test_orchestrator_loop.py | +172/-0 | stop, ledger, prompt |
### ee232980 feat(f070): add the era fixture corpus and its integrity detectors
| packages/orchestration/era_integrity.py | +319/-0 | 5 detectors |
| tests/orchestration/fixtures/era/*.json (5) | +124/-0 | minimal reproductions |
### 5ac42a38 test(f070): one detector test per era finding class, plus its repaired twin
| tests/orchestration/test_era_integrity.py | +269/-0 | 43 tests |
### 476a159e feat(f070): add the evaluators that check an orchestrator's claim
| packages/orchestration/orchestrator_loop.py | +219/-0 | dispatch/done evaluators |
| tests/orchestration/test_orchestrator_loop.py | +64/-0 | refusal reasons |
### 6a39fc0e feat(f070): refuse, re-prompt once, then escalate — never a silent loop
| packages/orchestration/orchestrator_loop.py | +94/-7 | refusal wiring, escalation |
| tests/orchestration/test_orchestrator_loop.py | +115/-7 | A9 edge; 2 T001 tests tightened |
### 2b28f15a feat(f070): refresh the dossier every iteration; pin the era corpus in the loop
| packages/orchestration/orchestrator_loop.py | +34/-0 | dossier update call |
| tests/orchestration/test_orchestrator_loop.py | +145/-0 | 5 classes × refuses-to-advance |
### d5428fb5 docs(f070): record the T001/T002 decisions and the branch rebuild
| .agent/decisions.md | +67/-0 | 5 decisions |
### (this commit) chore(f070): handback R1
| .agent/handoff.md | rewrite | this file (R-0149 self-reference exception) |

## External actions
- `gh pr list --state open …` → exactly PR #175, `feature/f069-mission-compiler`→`main`, non-draft.
- `gh pr merge 175 --merge --delete-branch` → merged as `afbe2639` on `main`; branch deleted.
- `git checkout main && git pull --ff-only` → up to date at `afbe2639`, porcelain empty.
- `git checkout -b feature/f070-orchestrator-loop`.
- `git push -u origin feature/f070-orchestrator-loop` (new branch) + pushes at phase boundaries.
- `git branch f070-oversize-backup` (at `08b77ba2`) — created before the rebuild, used for the byte-identity proof below, then `git branch -D` once that proof passed. Local only; never pushed.
- `git push --force-with-lease origin feature/f070-orchestrator-loop` → `+ 56af5046...d5428fb5 (forced update)`. Rebuild reason below.
- No PR created for F070 (SPLIT round: production code merges only after reviewer PASS).
- No worktree added or removed. No mutation/red-proof runs.

## Verification
Phase 1 (claim):
```
$ python3 -m pytest tests/docs/ -q          → 293 passed in 0.25s      exit 0
$ python3 -m pytest tests/cli/test_golden_path.py -q → 42 passed in 19.27s  exit 0
```
Phase 3 (T001 slice gate, then canary):
```
$ python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q
  65 passed in 0.31s                                                  exit 0
$ python3 -m pytest tests/cli/test_golden_path.py -q → 42 passed in 21.20s  exit 0
```
Phase 4 (T002 slice gate, then canary) — at the rebuilt tip `d5428fb5`:
```
$ python3 scripts/remedy_pytest_runner.py tests/orchestration/ -q -n auto
  9439 passed, 7 skipped in 79.88s                                    exit 0
$ python3 -m pytest tests/cli/test_golden_path.py -q → 42 passed in 19.60s  exit 0
$ python3 -m pytest tests/docs/ -q                   → 293 passed in 0.25s  exit 0
$ python3 -m ruff check <every touched file>         → All checks passed!
```
At the tip: `test_orchestrator_loop.py` 95 passed, `test_era_integrity.py` 43 passed.

## Authored-text proofs
`sha256sum .agent/authored/f070-r1-*.md` — all four equal their BEGIN digests:
```
839416ae503d12226b24f4a3e3e0e5faacb874f69abcec4954f97b1c4df168ba  f070-r1-1.md
fc8cae6827860c82f661943d63ecebdc00b49e38e477a0a5637830bcb31e7515  f070-r1-2.md
0db64faaa2cdbee1e187f444b7c458ce92dd8d23d95046720cabbe9d5f7cb3d6  f070-r1-3.md
9998ad4f2ffe5d7efb0038be4aa8465c6330c980a05c9c00465ac523e0aca94c  f070-r1-4.md
```
Disk-to-disk (`cp`, never retyped); committed-file digest vs authored digest:
```
f070-r1-1.md -> .agent/live_review.md  IDENTICAL (839416ae…)
f070-r1-2.md -> .agent/plan.md         IDENTICAL (fc8cae68…)
f070-r1-3.md -> .agent/candidates.md   IDENTICAL (0db64fea…)
```
f070-r1-4.md (FROM→TO, applied by a script reading the saved file):
FROM count before edit = 1, after = 0; TO count after = 1. At the tip:
`grep -c '^- \[~\] F070 — Orchestrator loop inside Remedy$' docs/roadmap/STATUS.md` → 1;
the `[ ]` form → 0.

## Deviations & assumptions
1. **CLI deferred to T003** (permitted by the order; decisions.md 2026-08-03). `run_mission`, `loop_limits_from_config`, `read_ledger`, `render_ledger` are public and stable.
2. **The dossier is a SEAM, not a document.** F071 is unbuilt and `Mission.dossier_ref` is RESERVED/empty. The loop calls a dossier port first (cache-stable prefix) and its default renders the mission record's own facts, labeled a stand-in; the per-iteration update writes that snapshot to `dossier.md`. Writing F071's maintained document here would be the second mechanism A6 forbids. Not an If-Blocked: the dossier is not in Phase 2's enumerated verb list.
3. **`--yes` auto-approval extracted** from `do_cmd.py` into `flight_plan.auto_approve_flight_plan` in its own commit (A6 says extract, not copy). No behavior change; `test_plan_approval.py` 27 passed.
4. **`orchestrator` added to `KNOWN_ROLES`**, defaults unchanged; `test_all_six_roles_present` renamed to `..._seven_...`. A pinned contract test changed — declared, not quiet. Routing policy doc untouched.
5. **Two T001 tests tightened** by T002's evaluator (a milestone-done and an achieved claim now must bring evidence). Tightened, not weakened.
6. **Branch rebuilt and force-pushed.** Two commits had landed at 541 and 712 changed lines; AGENTS.md permits one declared oversize commit per feature and neither was inseparable, so all three over-limit commits were split instead. Proof nothing was lost: `git diff f070-oversize-backup HEAD --stat` is EMPTY (byte-identical trees). Every commit in the range is now ≤471 changed lines.
7. **Handoff exceeds the ≤100-line cap** (15 commits × per-commit tables + the mandatory item-status table). This is the R-0149 collision, routed to planning and still open. No section dropped.
8. Milestone attribution is read from the loop's own ledger, not from `MissionJobLink` — job creation untouched (decisions.md).

## Next
Reviewer verdict for R1. On PASS: T003 (end-to-end two-milestone fixture mission + the `remedy mission run` / `mission ledger` CLI) as its own round.
