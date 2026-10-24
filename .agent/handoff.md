# Handoff — F157 round 3

## Session

SESSION 2 of feature F157 · round 3 · rounds so far 3. This round booked round 2's verdict and
R-1451's repair, landed DECISION F157 D3, retired the `planner_schema_gate` register entry, and
built the first routed consumer — `packages/orchestration/capability_routes.py` with its evidence
file and `stream_evidence_capture` routed inside `create_role_provider` — exactly as the block
ordered, with every gate green on its first run.

Fortschritt: ~55 % (T001 and T002 landed · T003: the stream route landed, two routes, the report
and the end-to-end open) — Schätzung.

## Range

Review of `710ba7e5c`..`dd9e5b499`.

## Commits

### ad9d0de49 F157 R3 C1: book round 2 and R-1451, DECISION F157 D3, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r3.md` | +159/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | append DECISION F157 D3 |
| `.agent/live_review.md` | +5/-0 | book round 2's Gate verdict PASS and register R-1451 |
| `.agent/plan.md` | +12/-11 | rewritten: Current Step → round 3, Next Steps → D3 (2), the report line and the closure sequence |

### 275d90145 F157 R3 C2: the planner entry retired, and the unavailable line held by a test
| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/capability_matrix.py` | +4/-5 | `planner_schema_gate` entry removed from `CAPABILITY_REQUIREMENTS`; two docstring sentences stating DECISION F157 D3 (4) |
| `tests/cli/test_worker.py` | +22/-2 | the two F157 assertions naming `planner_schema_gate` lose that entry; one new test in `TestWorkerShowAdapterLinkage` proves the `unavailable` form of the `Degradations:` line (R-1451's repair) |
| `docs/system/worker-adapter-contract-v2.md` | +6/-5 | the entries sentence names the three remaining entries, and one sentence says why no planner is an entry |

### dd9e5b499 F157 R3 C3: the capability routes, their evidence file, and the stream route
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/capability_routes.py` | +92/-0 | NEW FILE — `CAPABILITY_DECISIONS_FILENAME`, `stream_capture_route`, `record_capability_decisions`, `routed_stream_evidence`, `read_capability_degradations` |
| `tests/orchestration/test_capability_routes.py` | +123/-0 | NEW FILE — one test per promise, the registry adapter and a reduced-capability fixture |
| `packages/orchestration/role_provider_factory.py` | +2/-1 | `create_role_provider`'s `"stream_evidence"` setting becomes `routed_stream_evidence(role, model, stream_evidence, stream_evidence_dir)`; the function's measured length stayed 98 lines before and after (confirmed by AST) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | add `packages.orchestration.capability_routes` in sorted position |
| `docs/system/worker-adapter-contract-v2.md` | +14/-3 | the `CAPABILITY_DEGRADATIONS_FIELD` sentence rewritten to name a later round; one paragraph appended naming the route module, its evidence file and `read_capability_degradations` |

## External actions

`git push origin feature/f157-capability-matrix` — run once after this commit; no PR opened, per
the block's constraint.

## Verification

1. `git -C <repo> status --porcelain` → empty.
   `python3 .remedy-wt/f157-r3/prep/verify.py .` → every line `True`; last line `ALL True`; the
   `C4` row read `absent` at the time this gate ran, before this commit existed.

2. `python3 .remedy-wt/f157-r3/prep/run_selection.py . .remedy-wt/f157-r3-worker/selection-output.txt`
   → `exit 0`; last pytest line `4869 passed, 2 skipped in 38.61s`; no `FAILED`, no `ERROR`, no
   `process(es) behind` line anywhere in the output. The two `SKIPPED` lines: the pre-existing
   `test_install_smoke.py` (opt-in, needs network) and `test_agent_tooling.py` (a standing D12
   quarantine). Run once, as the block's rule states.

3. `python3 -m ruff check packages/contracts/capability_matrix.py packages/orchestration/capability_routes.py packages/orchestration/role_provider_factory.py tests/orchestration/test_capability_routes.py tests/cli/test_worker.py`
   → `All checks passed!`, exit 0.

4. `python3 -m mypy packages/contracts/capability_matrix.py packages/orchestration/capability_routes.py`
   → `Success: no issues found in 2 source files`, exit 0.

5. `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, `"passed": true`, 6 of 6
   checks `pass`.
   `python3 -m apps.cli.main worker show claude_code` →
   ```
   Worker: Claude Code (external harness) (claude_code)
     Roles: builder, reviewer, refactorer
     Mode:  external_harness
     Status: available
     Notes: Anthropic Claude Code CLI as builder and reviewer; its reference adapter claude-cli builds the command line of every call the loop makes and maps the usage of every call that is not streamed.
     Adapter: claude-cli
     Capabilities: json_schema, session_resume, streaming, tool_use
     Degradations: none
   ```

6. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `9`.

Reachability run C3 orders: `python3 -m pytest -q tests/orchestration/test_import_reachability.py`
before the C3 commit landed → 1 failed, 2 passed, naming exactly one new reachable module,
`packages.orchestration.capability_routes`; after adding it to the allowlist in sorted position,
the same run → 3 passed, no further growth named.

## Authored-text proofs

`.agent/authored/f157-r3.md`, applied at C1, compared disk-to-disk against the committed prepared
file `c1-.agent__authored__f157-r3.md` (itself byte-equal to `block.md`): byte-equal, 159 lines,
sha256 `a05b7721effc58b5cfb8df32b7d0b4302d9e96863a310b52407451d8cbf2a8e1` on both sides. The other
three C1 targets (`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`) were each
compared disk-to-disk against their own prepared `c1-*` file before the commit and read byte-equal;
`verify.py`'s gate 1 re-confirms all four after the commit.

## Deviations & assumptions

None. Every commit landed as the block ordered — no split was needed (186, 32 and 232 insertions,
all under the 500-insertion cap) — and every gate passed on its first run.

For the operator: this round's own test run covered a selection the block chose for it, not the
full collection the repository holds; that selection passed in full on its one run.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| R-1451 | done | repaired in C2 (`275d90145`): a new test in `TestWorkerShowAdapterLinkage` proves the `unavailable` form of the `Degradations:` line |
| C3 | done | |
| C4 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Gate 6 | done | |
| Push | done | `git push origin feature/f157-capability-matrix` immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated.
3. Book round 3's verdict in the next round's first commit.
4. Route `reviewer_schema_gate` and `parked_session_resume` in the claude-cli provider (DECISION
   F157 D3 (2)).
5. Operator questions open: 2.
6. Open findings count (gate 6): 9.
